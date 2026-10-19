# implement autonome, avec un juge de revue distinct

> Statut : terminé le 19/10/2026
> Origine : cadrage du 19/10/2026 (dans la conversation), recherche
> `docs/research/2026-10-19-auteur-juge-revue-autonome.md`

## Objectif

Un ticket cadré doit pouvoir se traiter de bout en bout sans déranger l'utilisateur : il valide
le plan, puis `implement` enchaîne les vagues, fait relire, corrige ce qui doit l'être, vérifie,
écrit le journal et ouvre une PR en brouillon. L'utilisateur ne relit que la PR et le plan.
Aujourd'hui, l'agent qui a écrit le code classe aussi les remarques de relecture et corrige sans
relecture : un juge au contexte vierge prend le classement et la relecture des corrections.

## Décisions

- **Le juge est un agent défini**, `agents/review-judge.md`, relié par `install.sh` dans
  `~/.claude/agents/`. Outils `Read`, `Grep`, `Glob` seulement : il ne peut ni écrire ni lancer
  de commande (AC-2). Il charge le `CLAUDE.md` du projet, comme tout sous-agent. Même modèle que
  la session (`inherit`).
- **Le juge reçoit** les remarques brutes des trois sources (spec, conventions, `/code-review`),
  le chemin d'un fichier de diff écrit par l'agent principal dans
  `$(git rev-parse --git-dir)/review/` (hors du suivi git, lisible sans `Bash`), le chemin du plan
  ou de la spec, et la liste des écarts déjà notés au journal. Jamais le raisonnement de l'auteur
  ni un résumé du travail (AC-2).
- **Le diff s'écrit par redirection shell** (`git diff <base> > <fichier>`) : il ne passe pas par
  le contexte de l'agent principal. Le juge n'en lit que les extraits utiles (`Grep` sur le
  fichier concerné, `Read` par plage) ; il lit le code actuel au `fichier:ligne` de chaque
  remarque.
- **Pas de `Bash` pour le juge** : le contexte vierge retire le biais de l'auteur, l'absence de
  `Bash` garantit qu'il ne modifie rien. Ce qu'il ne peut pas exécuter se vérifie par le TDD de
  l'auteur : un bug « À corriger » commence par le test qui le montre ; si ce test ne peut pas
  échouer, l'auteur conteste et la remarque passe dans « À décider » (AC-4). Si les essais
  montrent trop de remarques renvoyées en « À décider » faute de vérification, rendre `Bash` au
  juge avec une consigne de lecture seule.
- **Quatre groupes**, remplaçant les cinq actuels et la double échelle confirmée / douteuse :
  « À corriger », « À décider », « Écartée » (avec sa preuve, barrée), « Déjà connu ». « À
  trancher » devient « À décider » ; « Rien à faire » et « Fausses » fusionnent dans
  « Écartée » ; une remarque douteuse que le juge ne peut vérifier va dans « À décider » avec ce
  qui manque (AC-5).
- **Règle dure** : une remarque qui montre la violation d'un critère `AC-n` du plan ou d'une règle
  écrite du dépôt est « À corriger » (AC-3). C'est le cas R-12 du cadrage, classé à tort « à
  trancher » par l'auteur.
- **« À décider » est réservé** à ce qui sort du périmètre du plan ou touche : le modèle de
  données ou une migration, une interface publique, un comportement visible non prévu par le plan,
  la sécurité (une correction de sécurité locale reste « À corriger », signalée en tête de PR)
  (AC-3).
- **Seul le juge écarte.** L'auteur corrige ; s'il conteste un verdict, il l'écrit, la remarque
  passe dans « À décider » avec sa contestation, il ne la reclasse pas (AC-4).
- **Relecture des corrections par le même juge**, repris avec `SendMessage` pour garder son tri.
  Repli si la reprise échoue : un nouveau juge qui reçoit le premier verdict. 2 tours au maximum ;
  ce qui reste ouvert passe dans « À décider » (AC-7).
- **Le juge tourne au premier plan** : l'agent principal attend son retour (les rapports vides
  du TODO venaient de sous-agents en arrière-plan).
- **`review` lancé seul** garde la question à l'utilisateur, avec le juge pour le classement ;
  appelé par `implement`, il rend le classement sans question (AC-6).
- **Enchaînement par défaut** dans `implement` ; l'argument `pas-à-pas` remplace `turbo` et
  rétablit la pause de fin de vague. La vérification complète et le micro-bilan restent à chaque
  fin de vague (AC-8).
- **Arrêts réduits à trois cas** : changement destructeur, plan faux, échec d'une tâche dont la
  suite dépend. Une ambiguïté se tranche par le choix le plus prudent, noté au journal comme
  « Décision autonome » et repris dans la PR ; `tdd` appelé par `implement` fait de même au lieu
  de poser sa question (AC-9, AC-14).
- **PR en brouillon** seulement si la vérification complète est verte, qu'il y a un dépôt distant,
  une branche autre que la principale et l'outil de la forge (`gh`, `glab`…) ; push de la branche,
  puis PR. Sinon, s'arrêter au bilan et afficher le texte de la PR (AC-10, AC-11). Choix validé le
  19/10/2026.
- **Dépôt qui interdit les commits** (consigne ou `CLAUDE.md`) : tout faire sauf commits, push et
  PR ; les corrections restent dans le travail non commité ; le texte de la PR est affiché
  (AC-12). Choix validé le 19/10/2026.
- **Corps de la PR**, dans cet ordre : « À décider » ; « Décidé sans toi » (remarques corrigées
  avec leur commit, remarques écartées avec leur preuve, décisions autonomes) ; critères
  atteints ; quoi essayer à la main ; lien vers le plan (AC-10). Décrit dans
  `implement/references/pull-request.md` pour garder `implement` court.
- Les « proposer » de `implement/references/ending-by-origin.md` (marquer le jalon réalisé,
  commenter le ticket distant) deviennent des lignes « à faire par toi » du message final : ils
  touchent un service tiers ou la roadmap (AC-15).
- `plan/references/plan.md` : plusieurs vagues quand un point de vérification complète ou un essai
  par l'utilisateur en mode `pas-à-pas` a du sens.
- Repo : un seul commit, sur `main`, avec le plan (convention du dépôt).

## Critères d'acceptation

- AC-1 : `./install.sh` relie chaque `agents/*.md` dans `~/.claude/agents/` et supprime les liens
  cassés de ce dossier qui pointent vers le dépôt ; `review-judge` est utilisable depuis un autre
  projet.
- AC-2 : le juge n'a que `Read`, `Grep`, `Glob` ; il reçoit remarques brutes, fichier de diff,
  plan ou spec et écarts connus, sans raisonnement de l'auteur ; il rend pour chaque `R-n` un
  groupe et une preuve (`fichier:ligne` ou ligne de la spec).
- AC-3 : une violation d'un `AC-n` ou d'une règle écrite du dépôt est « À corriger » ; « À
  décider » ne reçoit que le hors périmètre, les données, les interfaces publiques, le
  comportement visible non prévu, la sécurité non locale, et le douteux invérifiable.
- AC-4 : seul le juge écarte, avec une preuve vérifiable ; une contestation de l'auteur (dont un
  bug dont le test ne peut pas échouer) fait passer la remarque dans « À décider ».
- AC-5 : la vue groupée montre « À corriger », « À décider », « Écartée » (barrée, avec sa
  preuve), « Déjà connu », sans marque confirmée / douteuse ; `R-n` et l'axe (`spec`, `conv`,
  `bug`) sont gardés.
- AC-6 : `review` lancé seul : juge, vue groupée, rapport complet, puis la question (lot « À
  corriger » recommandé, une question par « À décider ») ; appelé par `implement` : aucune
  question.
- AC-7 : après les corrections, le même juge (ou son repli) relit le diff des corrections : chaque
  remarque corrigée est-elle réglée, la correction introduit-elle un problème ; 2 tours au
  maximum, le reste passe dans « À décider ».
- AC-8 : `implement` enchaîne les vagues sans pause, avec vérification complète et micro-bilan au
  journal à chaque fin de vague ; `pas-à-pas` rétablit la pause ; une demande pour une vague
  précise s'arrête après elle.
- AC-9 : `implement` ne s'arrête que sur un changement destructeur, un plan faux ou un échec dont
  la suite dépend ; une ambiguïté est tranchée prudemment et notée « Décision autonome » au
  journal ; un échec dont rien ne dépend est noté et la tâche part dans « À décider ».
- AC-10 : fin du plan : `review` et `/code-review`, juge, corrections en TDD (un commit chacune),
  relecture par le juge, vérification complète verte, bilan, push et PR en brouillon dont le
  corps suit l'ordre décidé.
- AC-11 : sans dépôt distant, sans outil de forge, avec un push refusé (par exemple
  `git-guardrails`) ou une vérification rouge : pas de PR ; arrêt au bilan, texte de la PR
  affiché, et la raison.
- AC-12 : dépôt sans commit : tout le parcours sauf commits, push et PR ; corrections dans le
  travail non commité ; texte de la PR affiché.
- AC-13 : un plan d'origine POC s'arrête toujours au bilan, sans PR.
- AC-14 : `tdd` appelé par `implement` tranche une ambiguïté prudemment et la note, sans question.
- AC-15 : jalon à marquer et commentaire de ticket distant apparaissent comme « à faire par toi »
  dans le message final.
- AC-16 : `evals/run_subagents.py` copie `agents/` dans `<projet>/.claude/agents/` du projet de
  test, et son prompt de `review` demande d'attendre le retour des sous-agents.

## Interfaces à tester

- `./install.sh` : liens créés dans `~/.claude/agents/`, liens cassés nettoyés (AC-1)
- `review-judge` lancé depuis un projet temporaire avec `claude -p` : il se lance, refuse
  d'écrire (AC-1, AC-2)
- `python3 evals/run_subagents.py --dry-run review-new` : agents copiés, prompt (AC-16)
- `python3 docs/build_skills_page.py` puis `python3 -m unittest docs/test_build_skills_page.py`
- Le texte des skills, relu contre chaque critère (pas de test automatique du comportement)

## Hors périmètre

- Relancer la revue dans la CI avec `claude -p` sur chaque PR.
- Un `test-runner` sur un petit modèle pour la vérification.
- Faire vérifier par le correcteur des évals le groupe de chaque remarque (seulement trouvé ou
  écarté aujourd'hui) : ligne au `TODO.md`.
- Un juge pour les relectures de `brainstorming` et `to-spec`.

## Vague 1 : le juge dans review

- [x] Créer `agents/review-judge.md` et étendre `install.sh` aux agents (dossier
  `~/.claude/agents/`, son propre nettoyage) (AC-1, AC-2, AC-3, AC-4) : vérification prévue :
  `./install.sh`, `ls -l ~/.claude/agents`, puis un `claude -p` dans un projet temporaire qui
  lance `review-judge` (lien symbolique pris en compte, écriture refusée) ; si le lien n'est pas
  lu, copier au lieu de lier
- [x] Réécrire `review` §5 à §7 : diff écrit pour le juge, appel du juge, quatre groupes, vue
  groupée, rapport complet, question seulement lancé seul (AC-2 à AC-6) : vérification prévue :
  relecture contre AC-2 à AC-6, `grep` des anciens libellés dans le dépôt
- [x] Ajouter à `review` la relecture des corrections (reprise du juge, repli, 2 tours) (AC-7) :
  vérification prévue : relecture contre AC-7
- [x] `evals/run_subagents.py` : copie de `agents/`, attente des sous-agents (AC-16) :
  vérification prévue : `--dry-run review-new`

## Vague 2 : implement autonome

- [x] `implement` : enchaînement par défaut, `pas-à-pas`, arrêts réduits, décision autonome ;
  `tdd` sans question quand `implement` l'appelle ; règle des vagues de `plan/references/plan.md`
  (AC-8, AC-9, AC-14) : vérification prévue : relecture, `grep -rn "turbo\|pause" --include='*.md'`
- [x] `implement` « Fin du plan » et `references/pull-request.md` : parcours de relecture, PR en
  brouillon, cas sans PR et sans commit, POC, `ending-by-origin.md` (AC-10 à AC-13, AC-15) :
  vérification prévue : relecture contre AC-10 à AC-15, `implement/SKILL.md` sous 500 lignes
- [x] Fichiers liés : `CLAUDE.md` (convention et piège du dossier `agents/`), `README.md`
  (parcours, installation des agents), `docs/skills.template.html` (règles, note d'`implement`,
  enchaînements), `CREDITS.md` (évaluateur séparé, article d'Anthropic), `TODO.md`, `next` si
  besoin ; page régénérée : vérification prévue : `python3 docs/build_skills_page.py`, tests verts,
  `git grep -n "À trancher\|Rien à faire\|turbo" -- ':!docs/plans' ':!docs/research'` vide

## Journal

### Vague 1 (19/10/2026)

- Livré : `agents/review-judge.md` (outils `Read`, `Grep`, `Glob`, modèle `inherit`, quatre
  groupes, règle dure des `AC-n`, « Vu en vérifiant » numéroté `V-n` et classé, mode « relire les
  corrections ») ; `install.sh` relie `agents/*.md` dans `~/.claude/agents/` (variable
  `CLAUDE_AGENTS_DIR`, nettoyage des liens cassés, sauvegarde d'un fichier existant, un nom
  d'agent accepté en argument) ; `review` §5 « Faire classer par le juge », §6 avec le classement
  du juge dans le rapport complet et la vue à quatre groupes, §7 réservé au lancement seul (plus
  de lot « Rien à faire »), §8 « Relire les corrections » ; description et introduction de
  `review` citent le juge ; `run_subagents.py` copie `agents/` pour `review-new`, autorise
  `mkdir`, et demande d'attendre les sous-agents au premier plan.
- Écarts : `review` numérote aussi les constats passés par l'appelant (axe `bug`), pour que
  `implement` lui donne ceux de `/code-review` avant le classement (l'ordre devient
  `/code-review` puis `review`, à faire en vague 2). Les remarques « vues en vérifiant » sont
  classées par le juge (`V-n`) au lieu d'attendre un second tour.
- Vérifié : `claude -p` dans un projet temporaire : l'agent est chargé par le lien symbolique,
  liste exactement `Read`, `Grep`, `Glob`, et n'a pas pu créer de fichier ;
  `./install.sh review-judge review` ; `--dry-run review-new` montre l'agent copié et le prompt ;
  page régénérée, 8 tests verts ; pas de tiret long ; `review` fait 187 lignes. Non vérifié : une
  relecture réelle avec le juge et sa reprise par `SendMessage` (banc `run_subagents.py`, à
  proposer en fin de plan).
- Quoi essayer : `/review` sur une branche d'un projet réel avec un plan ; regarder le
  classement du juge dans le rapport complet et la vue à quatre groupes.

### Vague 2 (19/10/2026)

- Livré : `implement` autonome par défaut (paragraphe d'introduction, autorisation étendue au
  push de la branche et à la PR en brouillon, consigne sans commit qui l'emporte, mode
  `pas-à-pas`, enchaînement en fin de vague, ambiguïté tranchée sans question) ; « Fin du plan »
  en six étapes (`/code-review` puis `review` et son juge, corrections en TDD sans reclasser,
  relecture des corrections, vérification, bilan, PR, message final avec « À faire par toi ») ;
  « Quand ça ne va pas » réduit à trois arrêts ; `references/pull-request.md` (conditions,
  ouverture, repli sur le texte, corps) ; `ending-by-origin.md` sans « proposer » en cours de
  route ; `tdd` sans question quand `implement` l'appelle ; règle des vagues de
  `plan/references/plan.md` ; `CLAUDE.md` (convention et piège des agents), `README.md`,
  `CREDITS.md`, `TODO.md`, `docs/skills.template.html`, page régénérée.
- Écarts : la ligne ADR garde « appeler le Skill tool avec « adr » » sur accord depuis le message
  final (le test de la page attend cet appel) ; le changement destructeur exclut explicitement le
  push de la branche et la PR, sinon les deux règles se contredisaient (« écriture vers un service
  tiers ») ; `next` inchangé (il ne parle ni de pause ni du format de `review`).
- Vérifié : page régénérée, 8 tests verts ; `git grep` de « À trancher », « Rien à faire »,
  « turbo » vide hors plans et recherche ; `grep` de « pause », « résumé de fusion », « sans
  nouvelle revue » dans les skills : seuls restent le mode pas à pas et d'autres sujets ; pas de
  tiret long ajouté ; `implement` 211 lignes, `review` 187. Non vérifié : une exécution réelle
  de bout en bout dans un projet avec dépôt distant.
- Quoi essayer : `/implement <plan>` sur un petit plan validé d'un projet GitHub, sur une branche ;
  regarder l'enchaînement sans pause, le classement du juge dans le journal, la relecture des
  corrections, puis la PR en brouillon (« À décider » en tête, « Décidé sans toi »).

### Relecture (19/10/2026)

Premier essai du nouveau parcours : `/code-review` (medium), puis les deux relecteurs de
`review`, puis le juge `review-judge` sur les 26 remarques, corrections, et deux tours de
relecture des corrections par le même juge, repris par `SendMessage`. Sans commit en cours de
route (convention du dépôt) : instantané `git stash create` avant la première correction.

#### Spec

- R-1 · review/SKILL.md:136 · l'en-tête ne compte pas l'axe `bug` (AC-5).
- R-2 · implement/SKILL.md:51 · commandes introuvables : une question hors des trois arrêts (AC-9).
- R-3 · tdd/SKILL.md:45 · libellé « Décision autonome » absent, phrase contradictoire (AC-14).
- R-4 · pull-request.md:39 · trois lignes avant « À décider », contre l'ordre décidé.
- R-5 · install.sh:42 · sauvegarde des agents non demandée.
- R-6 · install.sh:42 · sauvegarde en dur malgré `CLAUDE_AGENTS_DIR` (AC-1).
- R-7 · pull-request.md:45 · correction de sécurité rangée dans « À décider ».

#### Conventions

- R-8 · review/SKILL.md:93 et review-judge.md:35 · les quatre groupes définis deux fois.
- R-9 · review/SKILL.md:80 · liste des outils recopiée du frontmatter.
- R-10 · implement/SKILL.md et pull-request.md · rouge, POC et sans commit écrits deux fois.
- R-11 · tdd/SKILL.md:45 · règle d'ambiguïté d'`implement` réécrite.
- R-12 · implement/SKILL.md:15 et :189 · les trois arrêts énumérés deux fois.
- R-13 · install.sh · possible code dupliqué (sauvegarde et lien).
- R-14 · install.sh:42 · possible chemin en dur.
- R-15 · review/SKILL.md:20, :147 · axe `bug` pris sans adapter la vue ni l'en-tête.
- R-16 · pull-request.md:62 · `ending-by-origin.md` sans lien.

#### Bugs (`/code-review`)

- R-17 · implement/SKILL.md:211 · une tâche en échec dont rien ne dépend rend la vérification
  rouge : pas de PR, la ligne « À décider » promise n'apparaît jamais.
- R-18 · install.sh:22 · une installation partielle n'installe pas le juge ; pas de repli.
- R-19 · review/SKILL.md:177 · sans commit, le diff des corrections contient tout le plan.
- R-20 · review/SKILL.md:86 · `$(…)` et `>` peuvent être refusés par des permissions
  `Bash(git:*)` (banc, session autonome).
- R-21 · tdd/SKILL.md:43 · question courte puis exception contraire.
- R-22 · review/SKILL.md:117 · `V-n` renumérotés mais collés tels quels.
- R-23 · review/SKILL.md:141 · les parts de l'en-tête ne font pas le total.
- R-24 · implement/SKILL.md:167 · tour consommé par une contestation non précisé.
- R-25 · install.sh:41 · même constat que R-6.
- R-26 · next/SKILL.md:112 · ligne de session « à la fin d'une vague ».

#### Classement du juge

- À corriger, toutes réglées (tour 1, sauf R-19 et R-22 au tour 2) : R-1, R-2, R-3, R-4, R-6,
  R-8 à R-15, R-19, R-21, R-22, R-23, R-25 ; R-28 et R-29 (vues par le juge au tour 1 :
  commentaire d'`install.sh` faux, `tdd` sans règle quand l'appelant ne dit rien).
- À décider : R-17 et R-27 (vue par le juge : « si c'est rouge, la vague n'est pas finie »
  bloque aussi l'enchaînement après un échec non bloquant) ; R-18 ; R-20 et R-30 (vue au tour 2 :
  `cp`, `diff -u` et `>>` ajoutés pour R-19, mêmes permissions).
- Écartées : ~~R-7~~ (« À décider » est la première section, la ligne dit la correction faite ;
  spec:46) ; ~~R-16~~ (champ du gabarit, le lien existe dans `implement`) ; ~~R-24~~ (une
  contestation va partout dans « À décider », §8.3 ne recorrige que le non réglé) ; ~~R-26~~
  (les fins de vague restent un moment d'intervention en `pas-à-pas` ou pour une vague précise).
- Déjà connu : R-5 (journal de la vague 1).

## Réalisé

- Critères : AC-1 à AC-16 atteints dans le texte des skills, relus par le juge ; AC-1 et AC-2
  vérifiés en vrai (`claude -p` : agent chargé par lien, `Read`, `Grep`, `Glob` seulement,
  écriture impossible ; `install.sh` essayé dans un dossier temporaire) ; AC-7 vérifié en vrai
  sur ce plan (reprise du juge par `SendMessage`, deux tours) ; AC-16 par `--dry-run`. Non
  vérifiés en vrai : AC-8 à AC-12 (exécution complète dans un projet avec dépôt distant).
- Écarts : ordre `/code-review` puis `review` ; « Vu en vérifiant » classé par le juge (`V-n`) ;
  la ligne ADR garde l'appel au skill `adr` sur accord ; le changement destructeur exclut le push
  et la PR ; `install.sh` factorisé en une fonction `link` et sauvegarde à côté de la
  destination (relecture).
- Constaté pendant l'essai : l'outil Agent lance les sous-agents en arrière-plan, « au premier
  plan » revient à attendre leur retour ; la numérotation des `V-n` donnée au juge au tour 2
  était décalée (corrigée dans ce bilan).
- Reste à décider : R-17 et R-27, R-18, R-20 et R-30 (message final), tranchés le jour même (ci-dessous).
- Hors plan : rien de nouveau.

### Décisions de l'utilisateur sur « À décider » (19/10/2026)

- R-17 et R-27 : une tâche en échec dont rien ne dépend est retirée (travail non commité),
  sa case reste vide, la vérification reste verte et la tâche part dans « À décider » de la PR.
- R-18 : `install.sh` relie toujours tous les agents, même quand on nomme des skills.
- R-20 et R-30 : banc lancé d'abord. `run_subagents.py review-new --runs 3` : 5 défauts sur 5,
  6 leurres sur 6 écartés, 45 `R-n` sourcés sur 46, 0,98 $, 148 s ; mais l'écriture de
  `diff.patch` est refusée dans les 3 passages (les agents décrivent le diff au juge à la place).
  Corrigé : `git diff <base> --output=<dossier git>/review-diff.patch`, chemin écrit en entier,
  sans `$(…)`, `>` ni `mkdir` ; les fichiers non suivis sont lus à leur chemin (plus de `cp` ni
  de `diff -u`) ; `Bash(mkdir:*)` retiré du banc. Relancé (`--runs 1`) : le juge reçoit
  `.git/review-diff.patch`, 5 sur 5, 2 leurres sur 2 écartés, 17 `R-n` sourcés sur 18, 0,88 $,
  134 s.
