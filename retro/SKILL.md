---
name: retro
description: Faire la rétrospective d'une session de travail, la courante ou une autre, et proposer ce qu'il faudrait changer dans l'environnement de Claude (renvois, contrôles automatiques, conventions de relecture, outils, skills) pour que la prochaine se passe mieux.
argument-hint: "[session : courante par défaut]"
disable-model-invocation: true
---

# Retro : améliorer l'environnement après une session

Une session difficile (Claude a cherché longtemps, commis une erreur qu'un outil aurait vue,
manqué d'une information) apprend quelque chose. Ce skill ne corrige pas le code : il cherche
**ce qui, dans l'environnement, a permis la difficulté**, et propose le renvoi, le contrôle ou la
convention qui l'empêcherait la prochaine fois. Il propose seulement ; rien ne change avant que
l'utilisateur choisisse.

Pour juger le code produit, c'est `review` ; pour la structure du code, `/architecture`.

## 1. Lire la session

- **Par défaut, la session courante** : c'est le meilleur cas, les difficultés sont encore dans
  la conversation.
- **Une autre session**, si l'utilisateur la désigne : son journal est dans
  `~/.claude/projects/<dossier du projet>/<id>.jsonl`. Le lire avec un sous-agent, qui rapporte
  les moments où Claude a peiné : recherches longues, erreurs, retours en arrière, corrections de
  l'utilisateur.

Lire ensuite ce que l'environnement offrait : `CLAUDE.md` (et ceux des sous-dossiers),
`ARCHITECTURE.md`, `docs/conventions.md`, les scripts de vérification (`package.json`,
`Makefile`…), les hooks de pre-commit, la CI.

Pour juger une ligne de `CLAUDE.md` ou d'un skill, suivre
[../onboard/references/ecrire-pour-un-agent.md](../onboard/references/ecrire-pour-un-agent.md).

## 2. Chercher les pistes

Chaque piste part d'un **moment précis de la session**, qu'on cite. Une catégorie sans moment
précis ne donne pas de piste : une rétrospective qui remplit ses cases avec des conseils généraux
ne vaut rien.

- **Navigation** : Claude a cherché longtemps un fichier ou un fait. → Un renvoi depuis un
  fichier déjà lu (« avant de toucher à la facturation, lire … »), dans `CLAUDE.md` ou
  `ARCHITECTURE.md`.
- **Contrôles automatiques** : Claude a fait une erreur qu'un outil aurait vue. → Une règle de
  linter, un type, un test, un hook de pre-commit, une étape de CI. Lire d'abord la commande de
  vérification du dépôt et la CI : un contrôle qui existe mais n'est pas branché, ou cassé sans
  bruit, est la vraie piste. Un dépôt **sans garde-fou** (ni pre-commit, ni CI qui lance le lint,
  les types et les tests) est une piste à lui seul.
- **Conventions de relecture** : la relecture a laissé passer une erreur. Classer d'abord :
  - une erreur **mécanique** (une API interdite, une forme d'import, un fichier mal placé) →
    un contrôle automatique, jamais une phrase ;
  - une affaire de **jugement** (la cohérence entre fichiers, « comme le code voisin ») → une
    règle dans `docs/conventions.md`, que `review` lit et qu'`implement` ne charge pas. Le
    créer au premier besoin.
- **`CLAUDE.md` trop lourd** : des consignes qui seraient mieux en contrôle ou dans
  `docs/conventions.md`, et des **consignes sans effet** (que Claude suivrait de toute façon). À
  regarder quand le fichier est long, dans le projet ou dans `~/.claude/CLAUDE.md`.
- **Économie d'outils** : un appel coûteux pour ce qu'il rapportait (une sortie énorme, une
  commande répétée, un outil ou un MCP gourmand). → Une commande plus ciblée, un script.
- **Accès à l'information** : il manquait une information essentielle. → L'élargir : écrire
  les journaux du serveur de développement dans un fichier, un accès en lecture seule à un
  service.
- **Un skill** : un skill a mené Claude de travers (une étape floue, un renvoi manqué, une
  consigne contredite par la situation). → Le nommer, avec l'étape, pour corriger le dépôt de
  skills.

Pourquoi `docs/conventions.md` plutôt que `CLAUDE.md` : celui qui implémente porte déjà le plus
de contexte (explorer, écrire, déboguer) ; celui qui relit ne reçoit qu'un diff. Les règles de
jugement vont là où il reste de la place pour les appliquer.

## 3. Présenter

Les pistes de la plus grave à la moins grave. Pour chacune : le moment de la session, ce qui l'a
permis, le changement proposé et le fichier touché. Écarter soi-même une piste qu'on ne peut pas
rattacher à un moment. Puis demander lesquelles appliquer.

## 4. Appliquer

Pour chaque piste retenue, montrer le changement (le diff, la règle, le script) avant de
l'écrire. Un contrôle se lance sur le dépôt avant d'être branché, pour vérifier qu'il ne bloque
pas du bon code. Une piste qui demande plus qu'une tâche passe par `plan`, sur accord. Commiter
selon le format du dépôt.
