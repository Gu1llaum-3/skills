export const meta = {
  name: 'ticket-chain',
  description: "Enchaîne les tickets ouverts d'une spec, un par un : un agent neuf par ticket, quatre relecteurs indépendants et un juge, une seule vérification complète, une fusion locale par squash, puis un contrôle sur la branche principale",
  whenToUse: "Lancé par le skill /ticket-chain, qui tire les arguments de la section Autonomie du CLAUDE.md. Strictement séquentiel ; s'arrête au premier blocage.",
  phases: [
    { title: 'Inventaire', detail: 'les tickets ouverts de la spec, par le skill tickets' },
    { title: 'Rattrapage', detail: 'relecture indépendante de tickets déjà fusionnés, puis correctifs' },
    { title: 'Tickets', detail: 'implémentation, relecture, corrections et fusion, puis contrôle' },
  ],
}

// Every project-specific value arrives through args (the /ticket-chain skill reads them from the
// "Autonomie" section of the project's CLAUDE.md). Nothing here names a project.
const a = args || {}
const feature = a.feature
const mainBranch = a.mainBranch || 'main'
const branchPattern = a.branchPattern || 'ticket/<feature>-<NN>'
const verifyCmd = a.verify
const targetedTests = a.targetedTests || ''
// The implement skill's folder (real path): the security brief and the unblocking rules are read
// there, so that each rule has a single source.
const implementDir = a.implementDir || '~/.claude/skills/implement'
const journal = a.journal || 'docs/journal.md'
const sensitivePaths = a.sensitivePaths || null
// A remote tracker (GitHub, GitLab, Jira…) is closed only after the merge and its check: a
// local ticket is a file, closed in the squash commit itself.
const remoteTracker = !!a.remoteTracker
const footerPattern = a.commitFooter || 'Ticket: <ref>'
// "À demander" comes from the section, or from the default of implement/references/autonomy.md.
const askFirst = a.askFirst || `l'entrée « À demander » de la section Autonomie du CLAUDE.md, ou sa valeur par défaut dans ${implementDir}/references/autonomy.md`
const bugHunterPath = a.bugHunterPath || ''
const judgePath = a.judgePath || ''
const catchUp = a.catchUp || []
const only = a.tickets || null

if (!feature || !verifyCmd) {
  return { error: "Arguments manquants : feature et verify sont obligatoires (le skill /ticket-chain les tire de la section Autonomie)." }
}

const slug = (ref) => ref.replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^-+|-+$/g, '')
const branchFor = (ref) => {
  const parts = ref.split('/')
  return branchPattern
    .replace('<feature>', feature)
    .replace('<NN>', slug(parts[parts.length - 1]))
    .replace('<ref>', slug(ref))
}
const footerFor = (ref) => footerPattern.replace('<ref>', ref)
// The footer as a whole line, for git log --grep (basic regex): Ticket: x/1 must not match x/10.
const footerLine = (ref) => `^${footerFor(ref).replace(/[.[\]*^$\\]/g, '\\$&')}$`

const INVENTORY = {
  type: 'object',
  properties: {
    tickets: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          ref: { type: 'string' },
          title: { type: 'string' },
          status: { type: 'string' },
          blockedBy: { type: 'array', items: { type: 'string' } },
          merged: { type: 'boolean' },
        },
        required: ['ref', 'title', 'status', 'blockedBy', 'merged'],
      },
    },
  },
  required: ['tickets'],
}

const REPORT = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: ['done', 'ready', 'blocked', 'failed'] },
    summary: { type: 'string' },
    mainCommit: { type: 'string' },
    journalEntries: { type: 'array', items: { type: 'string' } },
    humanActions: { type: 'array', items: { type: 'string' } },
    blockReason: { type: 'string' },
    verifiedTree: { type: 'string' },
  },
  required: ['status', 'summary', 'humanActions'],
}

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          file: { type: 'string' },
          line: { type: 'number' },
          detail: { type: 'string' },
          reference: { type: 'string' },
        },
        required: ['title', 'file', 'detail'],
      },
    },
  },
  required: ['findings'],
}

// The classes are those of agents/review-judge.md; the enum only names them.
const VERDICTS = {
  type: 'object',
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          group: { type: 'string', enum: ['a_corriger', 'option_prudente', 'a_decider', 'ecartee', 'deja_connu'] },
          proof: { type: 'string' },
          option: { type: 'string' },
          test: { type: 'string' },
          defaultChoice: { type: 'string' },
        },
        required: ['id', 'group', 'proof'],
      },
    },
  },
  required: ['verdicts'],
}

const CHECK = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    details: { type: 'string' },
  },
  required: ['ok', 'details'],
}

// One full verification per ticket: targeted tests during the waves, the full command once,
// before the merge, on a committed and clean tree whose hash is kept.
const VERIFY_ONCE = `Lance \`${verifyCmd}\` une seule fois, quand tout est commité et que \`git status --porcelain\` est vide, et lis son code de retour (sortie redirigée vers un fichier, jamais à travers un pipe). S'il échoue, corrige, commite et relance. Une fois vert, relève l'empreinte de l'arbre vérifié (\`git rev-parse HEAD^{tree}\`) et rends-la dans verifiedTree.`

const SQUASH = (ref) => `Squash merge dans ${mainBranch} (\`git switch ${mainBranch}\`, \`git merge --squash <branche>\`, vérifie que \`git write-tree\` donne l'empreinte vérifiée ; si ${mainBranch} a bougé entre-temps, refais le merge de ${mainBranch} dans la branche et la vérification), un seul commit au format du dépôt qui décrit le changement, avec en pied « ${footerFor(ref)} », puis suppression de la branche (\`git branch -D\`). Ni push ni PR.`

const UNBLOCK = `Pour ne pas rester bloqué, suis la règle de déblocage et les arrêts de ${implementDir}/SKILL.md, section « Quand ça ne va pas » (lis-la d'abord), avec le journal ${journal} au format de la section Autonomie. Dans ce workflow, « arrêter » veut dire rendre le statut « blocked » avec blockReason, et une action manuelle qui ne bloque pas la suite va dans humanActions sans arrêter le ticket.`

const bugHunterFallback = bugHunterPath
  ? `Suis la méthode du chasseur de bugs décrite dans ${bugHunterPath} (lis-le d'abord).`
  : 'Cherche seulement les défauts réels, avec un scénario de défaillance concret.'
const judgeFallback = judgePath
  ? `Tu es le juge de relecture décrit dans ${judgePath} : lis-le d'abord et suis-le, en lecture seule.`
  : 'Tu es un juge de relecture au contexte vierge, en lecture seule.'

// Independent review: four reviewers with a blank context (spec, conventions, bugs, security),
// in parallel, then the judge, who checks each finding in the code. None of them changes the
// repository. The security reviewer only works when a sensitive path is touched.
const review = async (ref, target, diffCmd, phaseName) => {
  const common = `Tu relis le ticket ${ref} (lis-le avec le skill tickets, avec sa spec et son plan dans docs/plans/ s'il existe). Le diff à relire : ${target}. Lecture seule : ne modifie rien, ne change pas de branche (git diff, git show et lecture des fichiers). Ne rapporte que des remarques vérifiées dans le code, avec fichier et ligne ; une catégorie sans problème ne produit rien.`
  const [spec, conventions, bugs, security] = await parallel([
    () => agent(`${common}
Axe « spec » : chaque critère d'acceptation du ticket est-il réellement prouvé par un test qui échouerait sans le code ? Manques (critère non couvert, cas limite de la spec oublié), dépassements (ajout hors du ticket), erreurs (comportement contraire à la spec, à un ADR ou à l'architecture documentée). Cite le critère (AC-n) ou le passage en cause dans « reference ».`,
      { label: `review spec ${ref}`, phase: phaseName, schema: FINDINGS }),
    () => agent(`${common}
Axe « conventions » : les règles écrites du CLAUDE.md et des documents qu'il désigne, les idiomes du code voisin, la robustesse (erreurs ignorées, ressources non fermées), les tests fragiles ou qui ne testent rien. Cite la règle en cause dans « reference ».`,
      { label: `review conventions ${ref}`, phase: phaseName, schema: FINDINGS }),
    () => {
      const prompt = `${common}
Axe « bugs » : les défauts réels du diff (logique, états incohérents, concurrence, erreurs avalées, autorisation, sécurité, écart avec le contrat d'API), chacun avec un scénario de défaillance concret dans « detail » et sa gravité (critique, majeur, mineur) au début de « title ». Pas de style ni de préférence.`
      const opts = { label: `review bugs ${ref}`, phase: phaseName, schema: FINDINGS }
      // A session that does not know the bug-hunter agent type falls back on its method, read
      // from its file.
      return agent(prompt, { ...opts, agentType: 'bug-hunter' }).catch(() =>
        agent(`${prompt}\n${bugHunterFallback}`, opts))
    },
    () => sensitivePaths
      ? agent(`${common}
Axe « sécurité ». Lis d'abord ${sensitivePaths} (un préfixe de chemin par ligne, # pour les commentaires) et la liste des fichiers du diff (\`${diffCmd} --name-only\`). Si aucun fichier du diff ne commence par l'un de ces préfixes, rends une liste vide sans rien relire d'autre.
Sinon, relis le diff en suivant la consigne du sous-agent de ${implementDir}/references/local-merge.md (section « Relecture de sécurité ») : lis-la d'abord, et rends ses constats dans le schéma (le scénario d'attaque dans « detail »).`,
        { label: `review security ${ref}`, phase: phaseName, schema: FINDINGS })
      : null,
  ])
  const axes = { spec, conv: conventions, bug: bugs, security }
  // An axis that returned nothing blocks like the judge: no merge without every review. The
  // security axis is null on purpose when no sensitive paths are configured.
  const names = { spec: 'spec', conv: 'conventions', bug: 'bugs', security: 'sécurité' }
  const empty = Object.entries(axes).filter(([axis, r]) => !r && (axis !== 'security' || sensitivePaths)).map(([axis]) => names[axis])
  if (empty.length) return { blocked: `relecteur(s) sans résultat, axe non relu : ${empty.join(', ')} (rien n'a été rendu)` }
  const findings = Object.entries(axes)
    .filter(([, r]) => r)
    .flatMap(([axis, r]) => r.findings.map((f) => ({ axis: axis === 'security' ? 'bug' : axis, ...f, title: axis === 'security' ? `sécurité : ${f.title}` : f.title })))
    .map((f, i) => ({ id: `R-${i + 1}`, ...f }))
  log(`${ref} : ${findings.length} remarque(s) de relecture.`)
  if (!findings.length) return { kept: [] }
  const judgePrompt = (intro) => `${intro}
Juge de relecture du ticket ${ref}. Le diff relu se lit avec \`${diffCmd}\` ; si tu ne peux pas lancer git, lis les fichiers cités à leur état actuel sur la branche. La spec : le ticket ${ref} et son plan dans docs/plans/. Les écarts déjà notés : le journal du plan et ${journal}.
Classe chaque remarque ci-dessous selon les groupes de ta définition (À corriger, Option prudente, À décider, Écartée, Déjà connu), avec leurs règles, sans les redéfinir. Rends-les dans le schéma : group a_corriger, option_prudente, a_decider, ecartee ou deja_connu ; proof ; pour une option prudente, option et test ; pour un « à décider », defaultChoice (le choix « sans avis de ta part »). Les remarques « Vu en vérifiant » vont dans la même liste, avec un id V-n.
Remarques :
${JSON.stringify(findings, null, 2)}`
  const judged = await agent(judgePrompt(''), { label: `judge ${ref}`, phase: phaseName, schema: VERDICTS, agentType: 'review-judge' })
    .catch(() => agent(judgePrompt(judgeFallback), { label: `judge ${ref}`, phase: phaseName, schema: VERDICTS }))
  // Code that the judge did not classify is never merged: the ticket stops, its branch stays.
  if (!judged) return { blocked: "le juge n'a rien rendu : remarques non classées" }
  const unjudged = findings.filter((f) => !judged.verdicts.some((v) => v.id === f.id)).map((f) => f.id)
  if (unjudged.length) return { blocked: `remarques sans verdict du juge : ${unjudged.join(', ')}` }
  const byId = Object.fromEntries(findings.map((f) => [f.id, f]))
  const kept = judged.verdicts
    .filter((v) => ['a_corriger', 'option_prudente', 'a_decider'].includes(v.group))
    .map((v) => ({ ...(byId[v.id] || {}), ...v }))
  log(`${ref} : ${kept.length} remarque(s) retenue(s) par le juge.`)
  return { kept }
}
const reviewBlocked = (ticket, reviewed) => {
  pushReport(ticket, { status: 'blocked', summary: 'Relecture incomplète, pas de fusion.', blockReason: reviewed.blocked, humanActions: [] })
  log(`${ticket} : ${reviewed.blocked}. Arrêt.`)
}

const check = (ref, phaseName, verifiedTree) =>
  agent(
    `Contrôle indépendant après le ticket ${ref}, dans le dépôt courant (ne modifie rien, sauf pour démarrer ce dont la vérification a besoin) :
- la branche courante est ${mainBranch} et l'arbre de travail est propre ;
- le ticket ${ref} est fusionné dans ${mainBranch} par un squash qui porte en pied « ${footerFor(ref)} », et la branche ${branchFor(ref)} n'existe plus ;
${remoteTracker ? '' : '- le ticket est terminé avec ses critères cochés et sa case de la roadmap cochée (lis-le avec le skill tickets) ;\n'}
- \`${verifyCmd}\` passe au vert sur ${mainBranch}. ${verifiedTree ? `La vérification complète a déjà passé sur l'arbre ${verifiedTree} : si \`git rev-parse ${mainBranch}^{tree}\` donne exactement cette empreinte, le code est identique octet pour octet, ne la relance pas et dis-le dans details ; sinon, lance-la réellement et lis son code de retour.` : 'Lance-la réellement et lis son code de retour.'}
Rends ok=true seulement si tout est vrai ; sinon, détaille précisément ce qui manque ou échoue.`,
    { label: `check ${ref}`, phase: phaseName, schema: CHECK },
  )

const fixInstructions = (kept) => `Remarques retenues par le juge de relecture :
${JSON.stringify(kept, null, 2)}
Traite-les toutes, une par commit : « a_corriger » et « option_prudente » se corrigent en TDD (un bug commence par le test qui le montre ; une option prudente, par le test que le juge a nommé). Ne reclasse jamais un verdict. Un « a_decider » qui relève de « À demander » (${askFirst}) arrête le ticket : statut « blocked », sans fusion. Les autres se tranchent par le choix par défaut du juge (defaultChoice), consigné dans ${journal}. Une remarque que tu ne peux pas corriger (le test du bug ne peut pas échouer) se consigne aussi au journal, avec la preuve.`

// Closing a remote ticket: only once its code is merged and checked on the main branch. A
// failure here stops nothing: the next inventory sees the footer on the main branch and retries.
const closeRemote = async (ref, phaseName) => {
  const closed = await agent(
    `Le ticket ${ref} est fusionné dans ${mainBranch} (commit qui porte en pied « ${footerFor(ref)} ») et contrôlé. Appelle le Skill tool avec « tickets » pour le fermer dans le gestionnaire distant, avec un commentaire de bilan court : ce qui a été livré, le commit sur ${mainBranch} (fusion locale, pas encore poussée), et les entrées du journal ${journal} qui le concernent. Lancer /ticket-chain vaut accord pour cette écriture : ne demande rien. Ne modifie rien dans le dépôt.`,
    { label: `close ${ref}`, phase: phaseName, schema: CHECK },
  )
  if (!closed || !closed.ok) {
    pushReport(`${ref} (fermeture)`, { status: 'failed', summary: closed ? closed.details : 'fermeture sans résultat', humanActions: [`Fermer le ticket ${ref} dans le gestionnaire (code fusionné dans ${mainBranch}).`] })
    log(`${ref} : fermeture du ticket distant en échec, à refaire (le prochain lancement la retente).`)
  }
}

const reports = []
const pushReport = (ticket, r) => reports.push({ ticket, ...(r || { status: 'failed', summary: 'Agent sans résultat.', humanActions: [] }) })

phase('Inventaire')
const inv = await agent(
  `Appelle le Skill tool avec « tickets » pour lister tous les tickets de la spec « ${feature} » (ceux qui la citent comme parente), dans l'ordre de leurs dépendances puis de leurs numéros, avec leur référence telle que le gestionnaire la donne, leur titre, leur statut et leurs bloquants. Pour chacun, merged = true si ${mainBranch} a déjà un commit dont une ligne est exactement son pied (\`git log ${mainBranch} --grep "<pied>" --format=%H\`, avec le motif ${footerLine('<ref>')} où <ref> est sa référence). Ne modifie rien.`,
  { label: 'inventory', phase: 'Inventaire', schema: INVENTORY },
)
if (!inv) return { feature, error: "L'inventaire n'a rien rendu.", reports }
const isDone = (t) => /termin|report|done|closed|ferm/i.test(t.status)
// A ticket whose footer is already on the main branch is merged: never redone, and closed now
// if its remote closing failed last time.
const todo = inv.tickets.filter((t) => !isDone(t) && !t.merged && (!only || only.includes(t.ref)))
const unclosed = remoteTracker ? inv.tickets.filter((t) => !isDone(t) && t.merged) : []
for (const t of unclosed) await closeRemote(t.ref, 'Inventaire')
log(`${todo.length} ticket(s) à faire : ${todo.map((t) => t.ref).join(', ') || 'aucun'}`)

let stopped = false

if (catchUp.length) phase('Rattrapage')
for (const ref of catchUp) {
  const target = `tous les commits de ${mainBranch} dont une ligne est exactement le pied « ${footerFor(ref)} » (\`git log ${mainBranch} --grep "${footerLine(ref)}" --format=%H\`) : le squash du ticket et ses correctifs, puis \`git show\` de chacun`
  const diffCmd = `git show <chacun de ces commits>`
  const reviewed = await review(ref, target, diffCmd, 'Rattrapage')
  if (reviewed.blocked) {
    reviewBlocked(`${ref} (rattrapage)`, reviewed)
    stopped = true
    break
  }
  const kept = reviewed.kept
  if (!kept.length) {
    log(`${ref} : rien à corriger.`)
    continue
  }
  const br = `${branchFor(ref)}-fix`
  const fix = await agent(
    `Le ticket ${ref} est déjà fusionné dans ${mainBranch} ; une relecture indépendante a retenu des remarques. Pars de ${mainBranch} à jour et propre, crée la branche ${br}, corrige avec des tests ciblés${targetedTests ? ` (${targetedTests})` : ''}, puis commite tout.
${fixInstructions(kept)}
${VERIFY_ONCE}
${SQUASH(ref)}
${UNBLOCK}
Rends ton rapport (status « done » une fois fusionné, avec verifiedTree).`,
    { label: `fix ${ref}`, phase: 'Rattrapage', schema: REPORT },
  )
  pushReport(`${ref} (rattrapage)`, fix)
  if (!fix || fix.status !== 'done') {
    log(`${ref} : correctif non terminé, arrêt.`)
    stopped = true
    break
  }
  const ctrl = await check(ref, 'Rattrapage', fix.verifiedTree)
  if (!ctrl || !ctrl.ok) {
    pushReport(`${ref} (contrôle)`, { status: 'failed', summary: ctrl ? ctrl.details : 'contrôle sans résultat', humanActions: [] })
    log(`${ref} : contrôle en échec après correctif, arrêt.`)
    stopped = true
    break
  }
}

if (!stopped) phase('Tickets')
for (const t of stopped ? [] : todo) {
  const br = branchFor(t.ref)
  log(`Début de ${t.ref} : ${t.title}`)

  // 1. Implementation in "enchaîné" mode: targeted tests, no review, no merge.
  const impl = await agent(
    `Implémente le ticket ${t.ref} (« ${t.title} ») : appelle le Skill tool avec « implement » et l'argument « ${t.ref} enchaîné ». La section Autonomie du CLAUDE.md s'applique (plan validé par elle, journal ${journal}).
- Branche du ticket : ${br}. Si elle existe déjà, reprends-la là où elle s'est arrêtée (mets-la à jour avec ${mainBranch} par un merge) ; sinon, pars de ${mainBranch} à jour et propre et crée-la. Le plan porte \`> Branche : ${br}\`.
- Tests ciblés seulement${targetedTests ? ` : ${targetedTests}` : ''}. La vérification complète se fait une seule fois, plus tard, avant la fusion.
${UNBLOCK}
Rends ton rapport : status « ready » quand tout est commité sur ${br} et que les tests ciblés y sont verts, sinon « blocked » ou « failed » avec blockReason ; résumé, entrées ajoutées au journal, actions humaines.`,
    { label: `ticket ${t.ref}`, phase: 'Tickets', schema: REPORT },
  )
  pushReport(t.ref, impl)
  if (!impl || impl.status !== 'ready') {
    log(`${t.ref} ${impl ? impl.status : 'sans résultat'} : ${impl ? impl.blockReason || impl.summary : "l'agent n'a rien rendu"}. Arrêt.`)
    break
  }

  // 2. Independent review of the branch diff.
  const reviewed = await review(t.ref, `la branche ${br} depuis ${mainBranch} (\`git diff ${mainBranch}...${br}\`, sans la checkout)`, `git diff ${mainBranch}...${br}`, 'Tickets')
  if (reviewed.blocked) {
    reviewBlocked(t.ref, reviewed)
    break
  }
  const kept = reviewed.kept

  // 3. Fixes, then one full verification and the merge.
  const merge = await agent(
    `Termine le ticket ${t.ref} sur sa branche ${br} (déjà implémentée, tests ciblés verts ; la vérification complète n'a pas encore été lancée).
${kept.length ? fixInstructions(kept) : "La relecture indépendante n'a rien retenu."}
Pour les corrections, des tests ciblés suffisent. Ensuite : mets la branche à jour avec ${mainBranch} (merge) si ${mainBranch} a bougé ; écris le bilan dans le plan (relecture comprise) et passe sa ligne de statut à terminé ; ${remoteTracker ? 'le ticket est sur un gestionnaire distant : ne le ferme pas, il se ferme après la fusion et le contrôle ; coche seulement la case de la roadmap si elle est dans le dépôt' : 'termine le ticket avec le skill tickets (statut, critères cochés, case de la roadmap)'} ; commite.
${VERIFY_ONCE}
${SQUASH(t.ref)}
Le commit de squash a exactement l'arbre vérifié : rien ne change entre la vérification et la fusion.
${UNBLOCK}
Rends ton rapport : status (« done » une fois fusionné), résumé, mainCommit, verifiedTree, entrées ajoutées au journal, actions humaines.`,
    { label: `fix and merge ${t.ref}`, phase: 'Tickets', schema: REPORT },
  )
  if (merge) pushReport(`${t.ref} (fusion)`, merge)
  if (!merge || merge.status !== 'done') {
    log(`${t.ref} : fusion non faite (${merge ? merge.blockReason || merge.summary : 'agent sans résultat'}). Arrêt.`)
    break
  }

  // 4. Check on the main branch, with at most one repair.
  let ctrl = await check(t.ref, 'Tickets', merge.verifiedTree)
  if (!ctrl || !ctrl.ok) {
    log(`${t.ref} : contrôle en échec, une tentative de réparation par un agent neuf.`)
    const repair = await agent(
      `Le ticket ${t.ref} a été implémenté, mais le contrôle sur ${mainBranch} échoue :
${ctrl ? ctrl.details : 'contrôle sans résultat'}
Répare proprement pour satisfaire le ticket et son contrôle : s'il n'est pas fusionné, termine-le sur sa branche ${br} puis fusionne-le ; s'il l'est déjà, corrige sur une branche ${br}-fix puis fusionne-la.
${VERIFY_ONCE}
${SQUASH(t.ref)}
${UNBLOCK}`,
      { label: `repair ${t.ref}`, phase: 'Tickets', schema: REPORT },
    )
    if (repair) pushReport(`${t.ref} (réparation)`, repair)
    ctrl = await check(t.ref, 'Tickets', repair && repair.verifiedTree)
  }
  if (!ctrl || !ctrl.ok) {
    log(`${t.ref} : contrôle toujours en échec après réparation. Arrêt : voir le rapport avant de reprendre.`)
    pushReport(`${t.ref} (contrôle)`, { status: 'failed', summary: ctrl ? ctrl.details : 'contrôle sans résultat', humanActions: [] })
    break
  }
  if (remoteTracker) await closeRemote(t.ref, 'Tickets')
  log(`${t.ref} terminé, relu et vérifié sur ${mainBranch}.`)
}

return { feature, reports }
