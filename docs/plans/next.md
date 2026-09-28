# /next : quel skill lancer ensuite

> Validé par Guillaume le 28/09/2026 ; statut : terminé
> Origine : cadrage du 28/09/2026 (`/feature` dans la conversation)

## Objectif

Au milieu d'une conversation menée sans skill, l'utilisateur ne sait pas lequel de ses skills
prendre, et Claude lui propose un « plan » générique au lieu de son parcours. `/next` lit la
conversation (ou l'état du projet si elle est vide) et dit quel skill lancer, pourquoi, et
comment gérer la session.

## Décisions

- Nom `/next`, lancé par l'utilisateur seulement (`disable-model-invocation: true`) : hors du banc
  d'essai des déclencheurs.
- Réponse : le skill recommandé, pourquoi en une ligne, la commande exacte à taper ; puis une ou
  deux autres options et ce qui les ferait préférer ; puis une ligne sur la session (continuer ici,
  ou `/clear` puis la commande).
- Conversation vide : lire les plans à cases non cochées, `ROADMAP.md`, les questionnaires en
  attente, le cahier des charges, et proposer la reprise ; sinon demander la situation.
- `/next` propose, il ne lance rien (convention du dépôt).
- La carte des parcours vit dans `next/SKILL.md`, adaptée du schéma du README et d'`ask-matt` :
  le skill ne peut pas lire le README depuis `~/.claude/skills/`. Le `CLAUDE.md` rappelle de la
  tenir à jour.
- Un seul commit sur `main` pour tout le changement, plan compris : la convention du `CLAUDE.md`
  prime sur « une tâche, un commit » d'`implement`.

## Critères d'acceptation

- AC-1 : après une discussion sans skill où rien n'est tranché, `/next` recommande `/feature`
  (ou `/brainstorming` s'il n'y a pas de projet) ; si tout est décidé, `plan` ; avec la raison
  tirée de la conversation.
- AC-2 : la réponse suit la forme décidée : une recommandation, sa commande exacte, une ou deux
  autres options avec leur condition.
- AC-3 : une ligne dit s'il faut continuer ici ou faire `/clear`, avec la raison.
- AC-4 : dans une conversation vide, avec un plan en cours, `/next` propose
  `/implement <plan>` et la vague à reprendre ; sans rien dans le projet, il demande la situation.
- AC-5 : quand aucun skill ne couvre la situation (bug qui résiste), il le dit et propose ce qui
  s'en approche.
- AC-6 : il ne recommande que des skills qui existent, et n'en lance aucun.
- AC-7 : `README.md`, `CREDITS.md`, `TODO.md` et la checklist du `CLAUDE.md` sont à jour.

## Interfaces à tester

- La commande `/next`, dans une vraie session : scénarios d'essai manuels (AC-1 à AC-6).
- Les fichiers du dépôt, relus (AC-7).

## Hors périmètre

- Lancer le skill recommandé.
- L'arbre complet des fins de phase d'`ask-matt`, le handoff.
- Le déclenchement automatique par Claude.

## Vague 1 : `/next` utilisable

- [x] Écrire `next/SKILL.md` : lire l'état (conversation, sinon projet), la carte des parcours,
  la forme de la réponse, la ligne sur la session, les cas sans skill, ce qu'il ne fait jamais.
  Moins de 150 lignes, description sans `#` (AC-1 à AC-6) : vérification prévue : relecture
  contre les descriptions des skills existants.
- [x] Mettre à jour `README.md` (tableau « À lancer toi-même »), `CREDITS.md` (`next` d'après
  `ask-matt`), `TODO.md` (piste `/guide` cochée, devenue `/next`) et la checklist du
  `CLAUDE.md` (tenir la carte de `next` à jour) (AC-7) : vérification prévue : relecture.
- [x] `./install.sh next` : vérification prévue : le lien `~/.claude/skills/next` existe.
- [x] Proposer les scénarios d'essai à l'utilisateur (AC-1 à AC-6) : l'autre session où Claude
  a proposé « un plan » ; une session vide dans un projet avec un plan en cours ; un bug qui
  résiste. Vérification prévue : l'utilisateur les lance.

## Journal

**Vague 1 (28/09/2026)**

- Livré : `next/SKILL.md` (109 lignes, description de 247 caractères sans `#`) ; `README.md`
  (tableau, schéma, crédits), `CREDITS.md`, `TODO.md`, checklist du `CLAUDE.md` ; lien
  `~/.claude/skills/next` créé par `./install.sh next`.
- Vérifié : chaque skill cité par la carte existe dans le dépôt (`/clear` et `/compact` sont des
  commandes de Claude Code) ; relecture des fichiers mis à jour. Pas de commande de vérification
  complète dans ce dépôt.
- Écart : la ligne de session prévoit aussi `/compact` avec une consigne, pour une conversation
  longue et encore utile ; le cadrage ne parlait que de continuer ou de `/clear`.
- Non vérifié : le comportement réel, qui dépend des scénarios ci-dessous.
- Quoi essayer :
  1. Dans l'autre session (problèmes discutés sans skill, Claude a proposé « un plan ») : `/next`.
     Attendu : `/feature` si rien n'est tranché, `/plan` si tout l'est, avec la raison, et
     « continuer ici ».
  2. Dans une session vide d'un projet qui a un plan validé en cours : `/next`. Attendu :
     `/implement docs/plans/<plan>.md`, la vague et la tâche à reprendre.
  3. Après la description d'un bug intermittent dont la cause résiste : `/next`. Attendu : il dit
     qu'aucun skill ne diagnostique, et propose `/plan` avec une tâche de localisation.

## Réalisé

- AC-1 à AC-6 : écrits dans `next/SKILL.md` (sections 1 à 3 et « jamais ») ; à confirmer par les
  scénarios d'essai 1 à 3.
- AC-7 : atteint, fichiers relus.
- Écart : option `/compact` dans la ligne de session (voir le journal).
- Hors plan : rien.
