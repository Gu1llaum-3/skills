# Enchaînement autonome : la section Autonomie, /ticket-chain et /code-audit

> Statut : terminé le 06/11/2026
> Origine : cadrage du 06/11/2026, à partir d'un projet privé (le « projet d'origine ») : inventaire
> de ce qui y surcharge les skills, puis essais de lancement d'un workflow depuis un skill. Les
> chemins de ses fichiers sont donnés au lancement d'`implement`, jamais écrits dans ce dépôt
> public.
> Branche : ticket-chain

## Objectif

Dans le projet d'origine, une automatisation éprouvée surcharge les skills. Des tickets
spécifiés s'y planifient sans validation. Un workflow les enchaîne un par un :
- un agent neuf par ticket ;
- quatre relecteurs indépendants, puis un juge ;
- une seule vérification complète, puis une fusion locale ;
- un contrôle après chaque ticket.

Un autre workflow audite le code par domaine. Tout cela vit dans ce projet et ne sert qu'à lui.

Ce plan le ramène dans les skills, sous une forme réutilisable par n'importe quel projet. Un
projet ne garde que sa configuration : une section `## Autonomie` et, s'il le veut, une section
`## Audit du code` dans son `CLAUDE.md`.

## Sources à lire (projet d'origine, hors dépôt)

Le brief de lancement donne le chemin de chacun de ces fichiers :
- le `CLAUDE.md`, sections « Autonomie », « Enchaîner les tickets d'une spec », « Relecture de
  sécurité », « Auditer le code », « Git » ;
- le workflow d'enchaînement ;
- le workflow d'audit ;
- l'agent chasseur de bugs ;
- le fichier des chemins sensibles ;
- le journal des décisions (pour son format).

On en reprend la méthode, jamais le contenu propre au projet : noms, chemins, règles métier,
commandes. Le brief donne aussi la liste des termes du projet qui ne doivent apparaître nulle
part dans ce dépôt.

## Décisions

- **Ce dépôt est public** : aucun nom, chemin, terme ni exemple du projet d'origine n'y entre,
  ni dans les fichiers ni dans les messages de commit. Les exemples des skills sont inventés
  (AC-11).
- **La configuration du projet est une section `## Autonomie` de son `CLAUDE.md`**, décrite
  dans `implement/references/autonomy.md`. Elle est lue par `plan`, `implement` et
  `/ticket-chain`. Sans cette section, rien ne change pour ces skills (AC-1). Ses entrées :
  - plan sans validation pour les tickets spécifiés ;
  - fichier du journal des décisions (par défaut `docs/journal.md`, format : Contexte, Décision,
    Alternatives, Sources, À revoir si) ;
  - fin : PR en brouillon (par défaut) ou fusion locale par squash, avec le pied de commit
    (par défaut `Ticket: <ref>`) ;
  - commande de vérification complète, et comment lancer des tests ciblés ;
  - fichier des chemins sensibles (facultatif, un préfixe de chemin par ligne, `#` pour les
    commentaires) ;
  - ce qui reste à demander (métier, hors périmètre, action irréversible ou hors du dépôt).
- **Exception à la règle d'accord explicite du dépôt** (`CLAUDE.md` des skills, « Passer d'une
  étape… ») : la section `## Autonomie` vaut accord permanent entre `plan` et `implement`, pour
  les seuls tickets qu'elle couvre. La règle est mise à jour pour le dire.
- **`plan` se valide seul** quand la section l'autorise et que la source est un ticket cadré
  avec ses critères. La ligne devient `> Statut : validé par autonomie (CLAUDE.md, section
  Autonomie) le <JJ/MM/AAAA>` : elle commence par « validé par », que lisent `implement` et
  `next`. Un ticket externe ou une question bloquante gardent la validation humaine (AC-2).
- **`implement` suit une règle de déblocage**, pour tout projet. Avant de déclarer une tâche en
  échec :
  1. diagnostiquer : lire l'erreur, la reproduire ;
  2. chercher dans les sources primaires (documentation, notes de version, issues) ;
  3. retenir la solution propre, jamais un contournement.

  Ne jamais affaiblir un test ou un critère, ni contourner une règle de sécurité ou un refus de
  permission. Avec la section `## Autonomie`, chaque décision autonome s'écrit aussi dans le
  journal du projet. Une action manuelle qui ne bloque pas (par exemple faire confiance à un
  certificat local) va dans « À faire par toi » sans arrêter le travail (AC-3).
- **Fin locale d'`implement`**. Quand la section dit « fusion locale », que la vérification est
  verte et qu'« À décider » est vide :
  - squash merge dans la branche principale, avec le pied configuré ;
  - dans ce même commit : ticket terminé et case de la roadmap cochée ;
  - suppression de la branche ;
  - pas de PR.

  Le commit de squash a exactement l'arbre vérifié : si la branche principale a bougé, on
  refait le merge et la vérification. Si « À décider » n'est pas vide, il n'y a pas de fusion :
  la branche reste, et le message final le dit (AC-4).
- **Relecture de sécurité avant une fusion locale** : si la section nomme un fichier de chemins
  sensibles et que le diff touche l'un d'eux, `implement` lance une relecture de sécurité avant
  de fusionner (le skill `security-review` s'il est disponible, sinon un sous-agent avec la même
  consigne que l'axe sécurité du workflow). Ses remarques passent par le juge comme les autres
  (AC-12).
- **Un mode `enchaîné` d'`implement`**, pour le workflow, au même titre que `pas-à-pas` :
  - des tests ciblés pendant les vagues ;
  - ni relecture, ni PR, ni fusion ;
  - fin au statut « prêt » quand tout est commité, la vérification complète étant laissée à
    l'appelant.

  Ce mode remplace les consignes « ne fais pas la relecture, ne fusionne pas » qui sont
  aujourd'hui écrites dans le prompt du workflow (AC-5).
- **`agents/bug-hunter.md` rejoint `agents/`**, rendu générique : les invariants sont ceux du
  `CLAUDE.md` du projet, sans liste propre à un projet. Un agent du projet du même nom reste
  prioritaire (AC-6).
- **`/ticket-chain <feature>` est un skill lancé par l'utilisateur**
  (`disable-model-invocation: true`), avec son script `ticket-chain/workflow.js`. Le skill :
  - vérifie les préalables ;
  - tire les arguments de la section `## Autonomie` ;
  - lit le script et le passe en entier à l'outil Workflow (paramètre `script`).

  Son texte dit explicitement d'appeler l'outil Workflow : c'est ce qui autorise le lancement
  (règle de l'outil : « un skill dont les instructions demandent d'appeler Workflow »).

  **Essais du 06/11/2026 :**
  - `scriptPath` marche pour un fichier du projet ouvert ou du dossier temporaire de la session,
    y compris à travers un lien symbolique ;
  - les arguments passent tels quels ;
  - une reprise par `resumeFromRunId` rejoue depuis le cache les agents inchangés ;
  - mais `scriptPath` refuse un fichier hors du projet ouvert, que ce soit dans le dépôt des
    skills ou dans `~/.claude/skills`, même après l'avoir lu.

  D'où le passage du script en entier, qui marche partout. L'outil enregistre alors le script et
  renvoie un chemin, utilisable pour reprendre avec `resumeFromRunId` dans la même session.

  Le skill dit aussi :
  - **pendant l'enchaînement**, tout autre travail se fait dans un worktree séparé, puis se
    fusionne entre deux tickets ;
  - **pause** : de préférence entre deux tickets. En cours de ticket : arrêter, commiter le
    travail en cours sur la branche du ticket, puis revenir sur la branche principale ;
  - **reprise dans une nouvelle session** : relancer le skill. Les tickets terminés sont sautés,
    et un ticket commencé reprend sur sa branche (AC-7).
- **Le script reprend le comportement du workflow d'origine**, sans valeur propre à un projet :
  - branche principale, modèle de branche (par défaut `ticket/<feature>-<NN>`), vérification,
    tests ciblés, journal, chemins sensibles et pied de commit arrivent par `args` ;
  - l'inventaire passe par le skill `tickets` au lieu de dossiers écrits en dur. Il saute les
    tickets terminés ou reportés et accepte les filtres `tickets` et `rattrapage` ;
  - le chemin du fichier `bug-hunter.md` arrive aussi par `args`, pour le repli d'une session qui
    ne connaît pas ce type d'agent ;
  - le juge reçoit les classes d'`agents/review-judge.md` sans les redéfinir. Le script d'origine
    en donne des définitions courtes qui divergent : son « option prudente » est une
    « amélioration bon marché », alors que le juge exige cinq conditions ;
  - contraintes de l'outil Workflow : `meta` en littéral pur, ni `Date.now()` ni `new Date()`
    sans argument, JavaScript sans types ;
  - identifiants en anglais, prompts en français (AC-8).
- **`/code-audit` est lancé par l'utilisateur**, avec son script `code-audit/workflow.js`.
  - Les domaines (clé, titre, chemins, points d'attention) viennent d'une section
    `## Audit du code` du `CLAUDE.md` du projet. Si elle manque, le skill propose des domaines
    tirés de l'arborescence et n'écrit la section qu'après accord.
  - Arguments facultatifs : `domains`, `since` (le commit du dernier rapport), `ref`.
  - La méthode est reprise telle quelle : commit figé, en lecture seule ; trois réfutateurs pour
    une remarque critique ou majeure, un pour une mineure.
  - Le rapport `docs/audits/<date>-<sha>.md` se commite sur la branche principale, ou, si un
    autre travail tourne, dans un worktree.
  - L'audit ne corrige rien : les défauts confirmés deviennent une spec et des tickets (AC-9).
- **Dépôt** : le travail se fait sur la branche `ticket-chain`, à la demande de l'utilisateur.
  Une tâche est un changement complet (skill et fichiers liés), donc un commit en français. La
  fusion dans `main` se fait en avance rapide, sur feu vert, et garde un commit par changement.

## Critères d'acceptation

- AC-1 : `implement/references/autonomy.md` décrit la section `## Autonomie` (entrées, valeurs
  par défaut, exemple inventé). Sans la section, `plan`, `implement` et `next` se comportent
  comme avant.
- AC-2 : `plan` passe seul à « validé par autonomie (CLAUDE.md, section Autonomie) le … »
  quand la section l'autorise et que la source est un ticket cadré avec ses critères. Un ticket
  externe ou une question bloquante demandent toujours la validation.
- AC-3 : `implement` suit la règle de déblocage avant toute tâche en échec, sans affaiblir de
  test, de critère, de règle de sécurité ni de refus de permission. Avec la section, chaque
  décision autonome s'écrit aussi dans le journal du projet, au format de la section.
- AC-4 : avec « fusion locale », `implement` termine par un squash merge dans la branche
  principale, avec l'arbre vérifié, le pied configuré, le ticket terminé et la roadmap cochée
  dans ce commit, puis supprime la branche, sans PR. Si « À décider » n'est pas vide, il ne
  fusionne pas et le dit.
- AC-5 : `implement … enchaîné` fait des tests ciblés pendant les vagues, ne fait ni relecture,
  ni PR, ni fusion, et s'arrête au statut « prêt ».
- AC-6 : `agents/bug-hunter.md` est générique (aucune règle propre à un projet), en lecture
  seule, et lit un commit figé quand on le lui donne. `install.sh` le relie dans
  `~/.claude/agents/`.
- AC-7 : `/ticket-chain` refuse de démarrer dans trois cas, en disant ce qui manque :
  - sans section `## Autonomie` qui prévoit la fusion locale et une commande de vérification ;
  - hors de la branche principale ;
  - sur un arbre de travail non propre.

  Sinon, il appelle explicitement l'outil Workflow avec le script en entier et les arguments
  tirés de la section, puis rend le rapport par ticket et les actions humaines. Il dit aussi
  comment travailler à côté, faire une pause et reprendre.
- AC-8 : `ticket-chain/workflow.js` enchaîne les étapes suivantes :
  - inventaire par le skill `tickets` ;
  - rattrapage facultatif ;
  - pour chaque ticket : implémentation en mode `enchaîné` ;
  - relecture sur quatre axes en parallèle : spec, conventions, bugs avec `bug-hunter` (repli
    sur la méthode lue dans son fichier), sécurité (seulement si un fichier de chemins sensibles
    est configuré et que le diff le touche) ;
  - juge `review-judge`, avec ses propres classes ;
  - corrections, une seule vérification complète sur un arbre commité dont l'empreinte est
    gardée, puis squash ;
  - contrôle qui ne relance pas la vérification si l'arbre de la branche principale est
    identique ;
  - une réparation au plus, et arrêt au premier blocage.
- AC-9 : `/code-audit` lit ses domaines dans `## Audit du code`. Si la section manque, il
  propose des domaines et n'écrit la section qu'après accord. Son script reproduit la méthode
  d'origine : commit figé, réfutateurs 3 ou 1, rapport daté commité, ou commité dans un
  worktree.
- AC-10 : la documentation suit :
  - `README.md` (tableaux et schéma), `CREDITS.md`, `TODO.md`, carte de `next/SKILL.md` ;
  - `docs/skills.template.html` (groupe dans `COLUMNS`, enchaînements, fichiers écrits) et
    page régénérée, tests de la page verts ;
  - chaque `SKILL.md` sous 500 lignes, pas de tiret long ;
  - `evals/triggers.json` revu si la description d'`implement` ou de `plan` change. Les deux
    nouveaux skills, lancés par l'utilisateur, n'entrent pas dans `MINE`.
- AC-11 : aucun terme de la liste du brief n'apparaît dans le dépôt
  (`git grep -n -i -E "<termes>"` vide), ni dans les messages de commit de la branche
  (`git log main..ticket-chain`).
- AC-12 : avec un fichier de chemins sensibles touché par le diff, `implement` fait une
  relecture de sécurité avant la fusion locale, et ses remarques passent par le juge.

## Interfaces à tester

- Le texte de `implement`, de ses références, de `plan`, d'`agents/bug-hunter.md`, de
  `ticket-chain` et de `code-audit`, relu contre chaque critère. Le comportement n'a pas de test
  automatique (AC-1 à AC-9, AC-12).
- `node --check` sur une copie `.mjs` de chaque `workflow.js` (syntaxe) (AC-8, AC-9).
- `git grep` et `git log` des termes du brief, vides (AC-11).
- `python3 docs/build_skills_page.py` puis `python3 -m unittest docs/test_build_skills_page.py`
  (AC-10).
- `python3 evals/run_triggers.py`, seulement si une description déclenchable change, et après
  accord (AC-10).
- Scénario d'essai proposé à l'utilisateur en fin de plan : un petit dépôt jetable avec une
  spec, deux tickets, une section `## Autonomie` et une section `## Audit du code`, puis
  `/ticket-chain <feature>` et `/code-audit` (AC-7, AC-8, AC-9).

## Hors périmètre

- La migration du projet d'origine (retirer ses workflows et son agent, réécrire ses sections
  `## Autonomie` et `## Audit du code`) : un travail à part, dans ce projet, après la fusion de
  ce plan. Jusque-là, son workflow `code-audit` et le skill `/code-audit` portent le même nom.
- La fin par PR dans `/ticket-chain` (gestionnaire distant, une PR par ticket) : la v1 exige la
  fusion locale.
- La conversion du dépôt en plugin (espace de noms, workflows livrés par le plugin).
- La proposition de la section `## Autonomie` par `/onboard` : une ligne dans `TODO.md`.

## Vague 1 : le mode autonome dans plan et implement

- [x] `implement/references/autonomy.md`, `plan` §6 (validation par la section), règle « Passer
  d'une étape… » du `CLAUDE.md` des skills, `next` si sa lecture du statut change, `README.md`,
  gabarit et page (AC-1, AC-2, AC-10, AC-11) : vérification prévue : relecture contre AC-1 et
  AC-2, `git grep -n "validé par"` sur les skills qui lisent le statut, tests de la page,
  `git grep` des termes du brief
- [x] `implement` : règle de déblocage, journal du projet, mode `enchaîné`, fin locale,
  relecture de sécurité avant fusion ; `references/ending-by-origin.md` et
  `references/pull-request.md` alignés (pas de PR en fin locale), `README.md`, gabarit et page
  (AC-3, AC-4, AC-5, AC-10, AC-11, AC-12) : vérification prévue : relecture contre AC-3 à AC-5
  et AC-12, `implement/SKILL.md` sous 500 lignes, tests de la page, `git grep` des termes du
  brief

## Vague 2 : /ticket-chain

- [x] `agents/bug-hunter.md` générique, `install.sh` vérifié, `CREDITS.md` (AC-6, AC-11) :
  vérification prévue : relecture contre AC-6, `./install.sh` puis `ls -l ~/.claude/agents`,
  `git grep` des termes du brief
- [x] `ticket-chain/SKILL.md` et `ticket-chain/workflow.js`, `README.md`, `CREDITS.md`,
  `TODO.md`, carte de `next`, gabarit (groupe dans `COLUMNS`) et page (AC-7, AC-8, AC-10,
  AC-11) : vérification prévue : `node --check`, relecture contre AC-7 et AC-8, tests de la
  page, `git grep` des termes du brief

## Vague 3 : /code-audit

- [x] `code-audit/SKILL.md` et `code-audit/workflow.js` (format de la section `## Audit du code`
  dans `code-audit/references/`), `README.md`, `CREDITS.md`, `TODO.md`, carte de `next`, gabarit
  et page (AC-9, AC-10, AC-11) : vérification prévue : `node --check`, relecture contre AC-9,
  tests de la page, `git grep` des termes du brief

## Vague 4 : Retours de revue

- [x] R-6 et R-18 (option prudente) : une fusion `failed` arrête l'enchaînement
- [x] R-16 (option prudente) : sans verdict du juge, ou un id sans verdict, le ticket est bloqué sans fusion ; un axe vide se signale
- [x] R-20 : rattrapage, pied ancré et tous les commits qui le portent
- [x] R-9 : consigne de sécurité lue dans `local-merge.md`, une seule source
- [x] R-10 : règles de déblocage lues dans `implement/SKILL.md`, seul le point propre au workflow reste
- [x] R-11 : « À demander » sans valeur recopiée dans le script
- [x] R-13 : lancement d'un workflow et chemins des agents dans une référence commune
- [x] R-21 (option prudente) : majorité sur les votes prévus, remarques aux votes incomplets « non vérifiées »
- [x] R-23 : `inDomain` avec une frontière de dossier
- [x] R-24 : appel de `tickets` à la forme du dépôt (`ticket-chain/SKILL.md:40`)
- [x] R-26 : même défaut à `ticket-chain/SKILL.md:61`
- [x] R-25 : NEXT de `ticket-chain` vers `code-audit`
- [x] N-1 (introduit par R-21) : une remarque réfutée à la majorité malgré un vote absent est écartée

## Vague 5 : décisions de l'utilisateur (R-17, R-22)

- [x] R-17 : un ticket distant se ferme après le squash et le contrôle, jamais avant ; l'inventaire saute (et ferme) un ticket dont le pied est déjà sur la branche principale ; même fin pour `implement` en fin locale
- [x] R-22 : le rapport de `/code-audit` s'écrit toujours dans un worktree

## Journal

### Vague 1 (06/11/2026)

- **Livré** : `implement/references/autonomy.md` (entrées, valeurs par défaut, journal, exemple
  inventé d'un outil de réservation) ; `plan` étapes 4 et 6 (validation par la section, points
  tranchés sans entretien) et `plan/references/plan.md` ; règle « Passer d'une étape… » du
  `CLAUDE.md` ; `implement` : section lue dans les préalables, autorisation de la fusion locale,
  mode `enchaîné`, relecture de sécurité à l'étape 1, règle de déblocage, journal du projet ;
  `implement/references/local-merge.md` (relecture de sécurité et ordre de la fusion) ;
  `ending-by-origin.md` et `pull-request.md` alignés ; `README.md`, gabarit et page.
- **Écarts** : la fin locale et la relecture de sécurité vont dans une référence à part
  (`local-merge.md`) pour garder `implement/SKILL.md` lisible (253 lignes).
- **Vérifié** : `python3 docs/build_skills_page.py` puis tests de la page (8 tests, code 0) ;
  `git grep "validé par"` : `implement` (`validé par … le …`) et `next` (`validé par …`)
  reconnaissent `validé par autonomie (…) le …` sans changement, `next` n'est donc pas modifié ;
  termes du brief : aucun dans les ajouts, les fichiers non suivis ni les commits. Pas de tiret
  long. Non vérifié : le comportement réel (aucun test automatique), voir le scénario de fin.
- **Bugs** : aucun.
- **Quoi essayer** : dans un dépôt jetable avec une section `## Autonomie`
  (`Fin : fusion locale`), `/implement <ticket cadré>` : le plan doit se valider seul, puis
  finir par un commit de squash sur `main` avec `Ticket: <ref>`, sans PR.
- > Décision autonome (2026-11-06) : la relecture de sécurité d'`implement` se fait dès que la
  > section nomme un fichier de chemins sensibles touché par le diff, que la fin soit une PR ou
  > une fusion locale ; la limiter à la fusion locale est écarté ; une PR non relue en sécurité
  > serait fusionnée à la main sans ce regard.
- > Décision autonome (2026-11-06) : les constats de sécurité passent au juge comme axe `bug`,
  > préfixés « sécurité : » ; un axe `sec` dans `review` et `review-judge` est écarté ; il
  > changerait deux fichiers hors du plan pour une simple étiquette.
- > Décision autonome (2026-11-06) : AC-11 se vérifie sur ce que la branche ajoute (lignes
  > ajoutées, fichiers non suivis, messages de commit) ; sur tout le dépôt, l'un des termes
  > trouve deux mots déjà sur `main`, sans lien avec le projet d'origine (le nom d'un assistant
  > de GitHub dans `CREDITS.md` et la recherche du 19/10, un verbe de `wizard/template.sh`) ;
  > les réécrire est écarté, hors périmètre.
- > Décision autonome (2026-11-06) : `/ticket-chain` exige aussi `Plan sans validation :
  > tickets cadrés` ; s'en tenir aux trois refus d'AC-7 est écarté ; sans cette entrée, le plan
  > du premier ticket attendrait l'utilisateur et l'enchaînement bloquerait aussitôt.
- > Décision autonome (2026-11-06) : dans `workflow.js`, un « À décider » du juge qui relève de
  > « À demander » arrête le ticket sans fusion ; les autres prennent le choix par défaut du juge,
  > consigné au journal du projet ; c'est ce que faisait le workflow d'origine (« se tranche selon
  > la section Autonomie »), borné par la liste « À demander ».
- > Décision autonome (2026-11-06) : `/ticket-chain` est rangé sur la carte dans la colonne
  > « Toi seul les lances », groupe « Enchaîner » ; le groupe « Construire » est écarté, sa colonne
  > est celle des skills que Claude peut aussi lancer.

### Vague 2 (06/11/2026)

- **Livré** : `agents/bug-hunter.md` générique (invariants du `CLAUDE.md`, journal du projet,
  agent du projet prioritaire) ; `ticket-chain/SKILL.md` (préalables, arguments tirés de la
  section, appel explicite de l'outil Workflow avec le script en entier, travail à côté, pause,
  reprise, rapport) ; `ticket-chain/workflow.js` (inventaire par `tickets`, rattrapage, mode
  `enchaîné`, quatre axes avec repli de `bug-hunter` et du juge sur leur fichier, juge aux classes
  de `review-judge`, une vérification avec empreinte, squash, contrôle, une réparation) ;
  `README.md`, `CREDITS.md`, `TODO.md`, carte de `next`, gabarit et page.
- **Écarts** : aucun sur le contenu ; voir les décisions autonomes ci-dessus.
- **Vérifié** : `./install.sh` relie `bug-hunter.md` dans `~/.claude/agents/` et
  `ticket-chain` dans `~/.claude/skills/` ; syntaxe de `workflow.js` : `node --check` sur une
  copie `.mjs` où le corps est enveloppé dans une fonction `async` (le `return` de premier niveau,
  admis par l'outil Workflow, est refusé par `node` tel quel) ; déroulé à blanc avec des agents
  factices : inventaire (ticket terminé sauté), rattrapage, repli de `bug-hunter` quand le type
  d'agent est inconnu, juge, fusion et contrôle, prompts relus ; pas de `Date.now()` ; tests de
  la page verts ; termes du brief absents. Non vérifié : un vrai lancement par l'outil Workflow.
- **Bugs** : aucun.
- **Quoi essayer** : dépôt jetable avec une spec et deux tickets cadrés, section
  `## Autonomie` (`Fin : fusion locale`), puis `/ticket-chain <feature>` : deux commits de squash
  sur `main` avec `Ticket: <ref>`, le contrôle qui dit ne pas relancer la vérification.
- > Décision autonome (2026-11-06) : `upgrade` lit désormais le dernier rapport `*-upgrade.md`
  > de `docs/audits/`, et non le dernier rapport du dossier ; laisser `upgrade` tel quel est
  > écarté ; il aurait pris un rapport de `/code-audit` pour le sien.

### Vague 3 (06/11/2026)

- **Livré** : `code-audit/SKILL.md` (domaines de `## Audit du code`, proposés puis écrits après
  accord s'ils manquent ; arguments `only`, `since`, `ref` ; appel explicite de l'outil Workflow
  avec le script en entier ; rapport et suite vers `to-spec`) ; `code-audit/workflow.js` (commit
  figé, lecture seule, un `bug-hunter` par domaine avec repli sur son fichier, trois réfutateurs
  pour une remarque critique ou majeure, un pour une mineure, rapport daté commité sur la branche
  principale ou dans un worktree) ; `code-audit/references/audit-section.md` (format et exemple
  inventé) ; `upgrade` aligné ; `README.md`, `CREDITS.md`, `TODO.md`, carte de `next`, gabarit
  et page ; `/ticket-chain` propose `/code-audit` après une spec terminée.
- **Écarts** : l'argument de filtre des domaines s'appelle `only` dans le script (le plan dit
  `domains`) : `domains` porte la liste des domaines tirée de la section, puisque le script n'en
  contient plus aucun ; le skill accepte toujours des clés de domaines en argument.
- **Vérifié** : syntaxe (`node --check` sur une copie enveloppée) ; déroulé à blanc : domaine
  inconnu signalé, `since` qui ne garde que le domaine touché, repli de `bug-hunter`, trois
  réfutateurs pour une majeure et un pour une mineure, majorité, prompt du rapport (worktree
  `../demo-audit-<sha>`) ; frontmatter YAML lu sans erreur (description entre guillemets, à
  cause du « : ») ; `./install.sh` relie `code-audit` ; tests de la page verts ; termes du brief
  absents. Non vérifié : un vrai lancement.
- **Bugs** : la description de `code-audit` sans guillemets était du YAML invalide (« : » dans
  une valeur nue) ; corrigée avant le commit.
- **Quoi essayer** : dépôt jetable sans section `## Audit du code`, `/code-audit` : domaines
  proposés, section écrite après accord, puis un rapport `docs/audits/<date>-<sha>.md` commité ;
  relancer avec `since <sha>` après un commit qui ne touche qu'un domaine.

### Relecture de fin de plan (06/11/2026)

`/code-review` (medium) sur `main...ticket-chain`, puis `review` (axes spec et conventions,
juge `review-judge`). 25 remarques (spec 7, conventions 8, bugs 10) et une vue par le juge.

**Relecture : 9 à corriger, 3 options prudentes, 2 à décider**, sur 26 remarques (spec 7,
conventions 8, bugs 10, vues par le juge 1).

À corriger
- R-9 · conv · implement/references/local-merge.md et ticket-chain/workflow.js · consigne de sécurité écrite deux fois, déjà divergente (phrase des invariants absente du script)
- R-10 · conv · ticket-chain/workflow.js (UNBLOCK) · recopie la règle de déblocage d'implement
- R-11 · conv · ticket-chain/workflow.js:23 · valeur par défaut d'« À demander » recopiée, déjà divergente d'autonomy.md
- R-13 · conv · ticket-chain/SKILL.md et code-audit/SKILL.md · « Lancer » et la ligne `bugHunterPath` en double
- R-20 · bug · ticket-chain/workflow.js:233 · `--grep` sans ancrage (`x/1` trouve `x/10`), et le correctif porte le même pied
- R-23 · bug · code-audit/workflow.js:97 · `startsWith` sans frontière : `src/auth` prend `src/authors`
- R-24 · bug · ticket-chain/SKILL.md:40 · « (skill `tickets`) » au lieu de la forme d'appel du dépôt
- R-25 · bug · docs/skills.template.html:405 · NEXT de ticket-chain ne mène pas à code-audit, que le skill propose
- R-26 · conv · ticket-chain/SKILL.md:61 · même défaut que R-24 (vu par le juge)
Option prudente
- R-6 · spec · ticket-chain/workflow.js:301 · un `failed` à la fusion part en contrôle et réparation · option : `merge.status !== 'done'` arrête · test : déroulé à blanc, fusion `failed`, ni contrôle ni réparation
- R-18 · bug · ticket-chain/workflow.js:301 · même constat · option et test de R-6
- R-16 · bug · ticket-chain/workflow.js:193 · juge nul ou ids omis : remarques perdues, fusion · option : statut bloqué sans fusion, et log de chaque axe nul · test : déroulé à blanc, juge nul, pas d'agent de fusion
- R-21 · bug · code-audit/workflow.js:142 · votes manquants comptés comme réfutation, 1/1 vaut majorité · option : majorité sur les votes prévus, votes incomplets dans « non vérifiées » · test : déroulé à blanc, vérificateurs nuls
À décider
- R-17 · bug · ticket-chain/workflow.js:292 · le ticket est terminé avant la vérification ; sur un gestionnaire distant, fermé même sans fusion, puis sauté par l'inventaire · options : (a) ne rien fermer à distance (`humanActions`) et l'inventaire saute les tickets dont le pied est déjà sur la branche principale / (b) refuser les gestionnaires distants en v1 (un refus de plus à AC-7) · recommandée : (a) · sans avis de ta part : (a)
- R-22 · bug · code-audit/workflow.js:174 · « sur main et propre » puis commit : course avec /ticket-chain · options : (a) toujours un worktree / (b) `git commit -- <rapport>` après un second contrôle / (c) interdire l'audit pendant /ticket-chain · recommandée : (a) · sans avis de ta part : (a)
Écartée
- ~~R-7 · spec · ticket-chain/workflow.js:26 · `catchUp` au lieu de `rattrapage`~~ : identifiants en anglais (plan, décision du script), l'argument du skill reste `rattrapage` (ticket-chain/SKILL.md:4, :59)
- ~~R-8 · conv · commits sur `ticket-chain`, pas `main`~~ : décision de la spec, à la demande de l'utilisateur (Décisions, « Dépôt »)
- ~~R-12 · conv · repli `bug-hunter` dupliqué dans les deux scripts~~ : chaque script est passé en entier, sans module partagé possible ; deux lignes
- ~~R-14 · conv · chirurgie au fusil sur l'exception Autonomie~~ : la spec demande ces fichiers, et chaque mention renvoie à autonomy.md ou local-merge.md
- ~~R-15 · conv · trois jetons dans `branchFor`~~ : documentés (ticket-chain/SKILL.md:50)
- ~~R-19 · bug · `blockedBy` inutilisé~~ : l'effet est l'arrêt prévu, avec sa raison (implement refuse et cite les bloquants ; AC-8)
Déjà connu
- R-1 · spec · code-audit/workflow.js:20 · `only` au lieu de `domains` : Journal, vague 3
- R-2 · spec · implement/SKILL.md · relecture de sécurité aussi avant une PR : décision autonome
- R-3 · spec · ticket-chain/SKILL.md:32 · quatrième refus : décision autonome
- R-4 · spec · upgrade/SKILL.md · changé hors plan : décision autonome
- R-5 · spec · ticket-chain/workflow.js · « À décider » tranchés par le choix par défaut : décision autonome (AC-4 vise `implement`)

### Relecture des corrections

- Tour 1 : les 13 remarques traitées sont réglées (R-6, R-9, R-10, R-11, R-13, R-16, R-18, R-20,
  R-21, R-23, R-24, R-25, R-26) ; une remarque introduite, N-1 (À corriger, par R-21 : une
  remarque réfutée à la majorité malgré un vote absent passait en « non vérifiées »).
- Tour 2 : N-1 réglée (808287b), rien d'introduit.

## Réalisé

- **Vérification complète** (06/11/2026), verte : `python3 docs/build_skills_page.py` et les
  8 tests de la page ; `node --check` des deux `workflow.js` (copie enveloppée) ; 30 contrôles de
  déroulé à blanc (21 pour `ticket-chain`, 9 pour `code-audit`, vague 5 comprise) ; termes du brief absents des
  ajouts, des fichiers et des messages de commit ; aucun tiret long ajouté ; le plus long
  `SKILL.md` touché fait 254 lignes.
- **Critères** :
  - AC-1 atteint : `implement/references/autonomy.md` ; sans la section, `plan`, `implement` et
    `next` gardent leur texte d'avant (relecture ; `next` inchangé, il lit déjà `validé par …`).
  - AC-2 atteint : `plan` étapes 4 et 6 (relecture).
  - AC-3 atteint : `implement`, « Déblocage » et journal du projet (relecture).
  - AC-4 atteint : `implement/references/local-merge.md` (relecture).
  - AC-5 atteint : mode `enchaîné` d'`implement` (relecture).
  - AC-6 atteint : `agents/bug-hunter.md`, relié par `./install.sh` (vérifié dans
    `~/.claude/agents`).
  - AC-7 atteint, avec un quatrième refus (décision autonome) : `ticket-chain/SKILL.md`.
  - AC-8 atteint : `ticket-chain/workflow.js`, déroulés à blanc (arrêt sur fusion en échec, sur
    juge nul ou verdict manquant, rattrapage ancré, contrôle sans relance sur arbre identique).
  - AC-9 atteint : `code-audit`, déroulés à blanc (votes, `since`, frontière des préfixes).
  - AC-10 atteint : README, CREDITS, TODO, carte de `next`, gabarit et page, tests verts ;
    `evals/triggers.json` inchangé (descriptions d'`implement` et de `plan` inchangées, les
    deux nouveaux skills sont lancés par l'utilisateur).
  - AC-11 atteint sur ce que la branche ajoute (décision autonome sur deux mots déjà sur `main`).
  - AC-12 atteint : `implement`, étape 1 de « Fin du plan », et `local-merge.md`.
  - Le comportement réel n'a pas de test automatique : un lancement réel reste à faire (scénario
    du message final, et deux lignes de `TODO.md`).
- **Écarts au plan** : fin locale et relecture de sécurité dans `local-merge.md` ; filtre de
  domaines nommé `only` ; références communes `ticket-chain/references/launching-a-workflow.md`
  (R-13) ; `upgrade` ne lit plus que ses rapports `*-upgrade.md`.
- **Tâches ajoutées** : la vague 4 « Retours de revue » (12 remarques et N-1), la vague 5
  (décisions de l'utilisateur sur R-17 et R-22).
- **Relecture** : corrigées R-9 (1589c93), R-10 (7ad1644), R-11 (7d124ec), R-13 (83d6572), R-20
  (a9954b4), R-23 (59fbf3d), R-24 (6e21ee9), R-25 (5dd71c0), R-26 (1357a59), N-1 (808287b) ;
  options prudentes appliquées R-6 et R-18 (bdc9822), R-16 (2f53627), R-21 (4b23725) ; écartées
  R-7, R-8, R-12, R-14, R-15, R-19 (preuves du juge ci-dessus) ; déjà connues R-1 à R-5.
  **À décider**, tranchés par l'utilisateur et appliqués en vague 5 : R-17, sa variante (un
  ticket distant se ferme après le squash et le contrôle, l'inventaire saute et ferme un ticket
  déjà fusionné ; aussi en fin locale d'`implement`) (821ef64) ; R-22, toujours un worktree
  (6e94bcb). Ces deux changements n'ont pas eu de relecture par le juge (les deux tours
  prévus étaient faits) : ils sont couverts par les déroulés à blanc.
- **Décisions autonomes** : voir le Journal (six entrées).
- **Après le regroupement** (06/11/2026, défaut signalé par l'utilisateur) : un relecteur qui ne
  rend rien (bugs, conventions, spec, ou sécurité quand un fichier de chemins sensibles est
  configuré) arrête le ticket comme un juge muet, sans fusion ; avant, l'axe manquant était
  seulement signalé. Rangé dans le commit `/ticket-chain` ; prouvé par des déroulés à blanc
  (axe sécurité vide, axe bugs vide après repli, sécurité non configurée qui fusionne).
- **Historique** : le 06/11/2026, à la demande de l'utilisateur, les commits de correction cités
  plus haut ont été regroupés dans le commit de leur changement : `implement` (841512a),
  `/ticket-chain` (37ae8e1), `/code-audit` (68024dc). Les hashes d'origine restent dans la
  branche locale `ticket-chain-avant-regroupement`, à supprimer une fois la fusion faite.
- **Hors plan** : rien de nouveau ; les suites restent dans « Hors périmètre » et `TODO.md`.

### Décisions de l'utilisateur (06/11/2026)

- R-17 : variante de l'utilisateur, plutôt que (a) ou (b) : fermer le ticket distant **après**
  la fusion, pour être sûr qu'il ne se ferme que sur un code fusionné ; avec le garde-fou de (a)
  (l'inventaire saute un ticket dont le pied est déjà sur la branche principale).
- R-22 : choix par défaut (a), le rapport toujours dans un worktree.
