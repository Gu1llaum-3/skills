export const meta = {
  name: 'code-audit',
  description: "Audit des bugs du code par domaine, sur un commit figé : un chasseur de bugs par domaine, chaque remarque soumise à des agents qui tentent de la réfuter, puis un rapport daté dans docs/audits/",
  whenToUse: "Lancé par le skill /code-audit, qui tire les domaines de la section « Audit du code » du CLAUDE.md. Lecture seule sur le code ; seul le rapport est écrit et commité.",
  phases: [
    { title: 'Snapshot', detail: 'commit audité, date, fichiers modifiés depuis since' },
    { title: 'Hunt', detail: 'un chasseur de bugs par domaine' },
    { title: 'Verify', detail: 'chaque remarque soumise à des agents qui tentent de la réfuter' },
    { title: 'Report', detail: 'rapport dans docs/audits/, commité' },
  ],
}

// Every project-specific value arrives through args (the /code-audit skill reads the domains
// from the "Audit du code" section of the project's CLAUDE.md). Nothing here names a project.
const a = args || {}
const DOMAINS = a.domains || []
const mainBranch = a.mainBranch || 'main'
const ref = a.ref || mainBranch
const since = a.since || null
const selected = a.only || null
const sensitivePaths = a.sensitivePaths || null
const journal = a.journal || 'docs/journal.md'
const repoName = a.repoName || 'repo'
const bugHunterPath = a.bugHunterPath || ''

if (!DOMAINS.length) {
  return { error: "Aucun domaine : le skill /code-audit les tire de la section « Audit du code » du CLAUDE.md." }
}

const SNAPSHOT = {
  type: 'object',
  properties: {
    sha: { type: 'string' },
    date: { type: 'string' },
    changedFiles: { type: 'array', items: { type: 'string' } },
  },
  required: ['sha', 'date', 'changedFiles'],
}

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          titre: { type: 'string' },
          fichier: { type: 'string' },
          ligne: { type: 'integer' },
          gravite: { type: 'string', enum: ['critique', 'majeur', 'mineur'] },
          scenario: { type: 'string' },
          preuve: { type: 'string' },
          confiance: { type: 'string', enum: ['certain', 'probable'] },
        },
        required: ['titre', 'fichier', 'ligne', 'gravite', 'scenario', 'preuve', 'confiance'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT = {
  type: 'object',
  properties: {
    confirmed: { type: 'boolean' },
    gravite: { type: 'string', enum: ['critique', 'majeur', 'mineur'] },
    proof: { type: 'string' },
  },
  required: ['confirmed', 'gravite', 'proof'],
}

const REPORT = {
  type: 'object',
  properties: {
    path: { type: 'string' },
    commit: { type: 'string' },
    summary: { type: 'string' },
  },
  required: ['path', 'commit', 'summary'],
}

const readOnly = (sha) => `Lecture seule : ne modifie rien, ne change pas de branche, ne lance aucun test ni service. Lis le commit ${sha} et non l'arbre de travail (\`git show ${sha}:<chemin>\`, \`git grep -n <motif> ${sha} -- <chemins>\`, \`git ls-tree -r --name-only ${sha} <dossier>\`) : un autre travail peut tourner dans le même dossier.`
const decided = `les décisions consignées (docs/adr/, ${journal}, docs/specs/)`

phase('Snapshot')
const snap = await agent(
  `Donne le commit à auditer et la date du jour, sans rien modifier :
- sha : \`git rev-parse ${ref}\` (le sha complet) ;
- date : \`date +%F\` ;
- changedFiles : ${since ? `\`git diff --name-only ${since} ${ref}\` (fichiers modifiés depuis ${since})` : 'une liste vide'}.`,
  { label: 'snapshot', phase: 'Snapshot', schema: SNAPSHOT },
)
if (!snap) return { error: "Le snapshot n'a rien rendu." }
const sha = snap.sha
const short = sha.slice(0, 7)
// A prefix is a file or a folder: src/auth takes src/auth/a.ts, not src/authors/list.ts.
const inDomain = (file, domain) => domain.paths.some((p) => file === p || file.startsWith(p.replace(/\/?$/, '/')))

let domains = DOMAINS.filter((d) => !selected || selected.includes(d.key))
const unknown = (selected || []).filter((k) => !DOMAINS.some((d) => d.key === k))
if (unknown.length) log(`Domaine(s) inconnu(s), ignoré(s) : ${unknown.join(', ')}. Domaines : ${DOMAINS.map((d) => d.key).join(', ')}.`)
if (since) {
  const before = domains.length
  domains = domains
    .map((d) => ({ ...d, changed: snap.changedFiles.filter((f) => inDomain(f, d)) }))
    .filter((d) => d.changed.length)
  log(`Depuis ${since} : ${snap.changedFiles.length} fichier(s) modifié(s), ${domains.length} domaine(s) touché(s) sur ${before}.`)
}
log(`Audit de ${short} (${ref}) : ${domains.map((d) => d.key).join(', ') || 'aucun domaine'}.`)

const hunt = (d) => {
  const prompt = `Audit des bugs du domaine « ${d.title} » au commit ${sha}.
${readOnly(sha)}
Périmètre (préfixes de chemins) : ${d.paths.join(', ')}. Suis aussi les appels qui en sortent quand le bug est à la frontière.
${d.changed ? `Ne rapporte que des défauts dans ces fichiers, modifiés depuis ${since} (lis le reste pour comprendre) : ${d.changed.join(', ')}.` : ''}
${d.focus ? `Points d'attention du domaine : ${d.focus}.` : ''}
${sensitivePaths ? `Les fichiers dont le chemin commence par un préfixe de ${sensitivePaths} méritent un regard de sécurité renforcé (authentification, autorisation, injections, données personnelles).` : ''}
Avant de rapporter un comportement surprenant, vérifie qu'il n'est pas décidé : ${decided}.`
  const opts = { label: `hunt ${d.key}`, phase: 'Hunt', schema: FINDINGS }
  // A session that does not know the bug-hunter agent type falls back on its method, read from
  // its file.
  return agent(prompt, { ...opts, agentType: 'bug-hunter' }).catch(() =>
    agent(`${prompt}\n${bugHunterPath ? `Suis la méthode du chasseur de bugs décrite dans ${bugHunterPath} (lis-le d'abord).` : ''}`, opts))
}

// Critical and major findings get three refuters (majority), minor ones a single one.
const verify = (f, d) => {
  const votes = f.gravite === 'mineur' ? 1 : 3
  return parallel(
    Array.from({ length: votes }, (_, i) => () =>
      agent(
        `Vérificateur ${i + 1}/${votes}, au contexte vierge. Un chasseur de bugs affirme ce défaut au commit ${sha} (domaine « ${d.title} ») :
${JSON.stringify(f, null, 2)}
${readOnly(sha)}
Essaie de le RÉFUTER : lis le code cité et ce qui l'entoure, les appelants, les contraintes de la base (migrations, schéma), les tests qui couvriraient le cas, et ${decided}. confirmed=true seulement si le scénario se produit réellement avec le code tel qu'il est ; confirmed=false s'il est impossible, déjà empêché ailleurs, ou décidé. En cas de doute, confirmed=false. Donne la preuve (fichier:ligne, extrait) et la gravité que tu retiens.`,
        { label: `verify ${d.key}:${f.fichier.split('/').pop()}:${f.ligne}#${i + 1}`, phase: 'Verify', schema: VERDICT },
      ),
    ),
  ).then((verdicts) => {
    const valid = verdicts.filter(Boolean)
    const yes = valid.filter((v) => v.confirmed)
    // The majority counts over the planned votes: a missing vote is neither a yes nor a no.
    const kept = yes.length > votes / 2
    // Unverified only while the missing votes could still make a majority.
    const unverified = !kept && yes.length + (votes - valid.length) > votes / 2
    return { ...f, domain: d.key, confirmed: kept, unverified, votes: `${yes.length}/${votes} (${valid.length} rendus)`, verdicts: valid }
  })
}

const results = await pipeline(
  domains,
  (d) => hunt(d),
  (found, d) => {
    const findings = (found && found.findings) || []
    log(`${d.key} : ${findings.length} remarque(s) à vérifier.`)
    return parallel(findings.map((f) => () => verify(f, d)))
  },
)

const all = results.filter(Boolean).flat().filter(Boolean)
const confirmed = all.filter((f) => f.confirmed)
log(`${confirmed.length} défaut(s) confirmé(s) sur ${all.length} remarque(s).`)

phase('Report')
const reportPath = `docs/audits/${snap.date}-${short}.md`
const report = await agent(
  `Écris le rapport de l'audit des bugs du code au commit ${sha} (${ref}), du ${snap.date}${since ? `, limité aux fichiers modifiés depuis ${since}` : ''}. Domaines audités : ${domains.map((d) => `${d.key} (${d.title})`).join(', ') || 'aucun'}.
Remarques, avec le résultat de leur vérification (confirmed, unverified, votes, verdicts) :
${JSON.stringify(all, null, 2)}

1. Fichier : ${reportPath}, en français. Contenu :
   - en-tête : commit audité (sha complet), ref, date, domaines, \`since\` s'il y en a un, et la commande de l'audit suivant : « /code-audit since ${sha} » ;
   - en bref : nombre de défauts confirmés par gravité et par domaine ;
   - défauts confirmés, du plus grave au moins grave : titre, domaine, fichier:ligne, gravité retenue (celle de la majorité des vérificateurs), scénario, preuve ; fusionne les doublons (même défaut vu par deux domaines) ;
   - remarques non vérifiées (unverified : des vérificateurs n'ont rien rendu, la majorité n'est pas atteinte) : titre, domaine, fichier:ligne, gravité annoncée et votes, à revérifier au prochain audit ;
   - remarques écartées (ni confirmées ni non vérifiées) : une ligne chacune avec la raison des vérificateurs, pour qu'on ne les recherche pas la prochaine fois ;
   - aucune valeur de secret ni donnée personnelle, même si le code en contient : nomme seulement l'emplacement.
2. Commit, toujours dans un worktree (un autre travail, comme /ticket-chain, peut changer de branche ou commiter dans le dossier principal à tout moment) : \`git worktree add ../${repoName}-audit-${short} -b audit/${snap.date}-${short} ${mainBranch}\`, écris le rapport et commite-le là, au format de commit du dépôt (par défaut \`docs(audit): record the code audit of ${short}\`), sans toucher au dossier principal. Dis dans le résumé comment le ramener : \`git merge --ff-only audit/${snap.date}-${short}\` depuis ${mainBranch} quand le dossier principal y est et qu'il est propre, puis \`git worktree remove\` et suppression de la branche.
Rends le chemin du rapport, le commit créé et un résumé de cinq lignes.`,
  { label: 'report', phase: 'Report', schema: REPORT },
)

return { sha, date: snap.date, domains: domains.map((d) => d.key), confirmed: confirmed.length, findings: all.length, report }
