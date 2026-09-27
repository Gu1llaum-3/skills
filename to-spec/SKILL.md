---
name: to-spec
description: Transformer ce qui a été décidé dans la conversation (souvent après feature ou brainstorming) en spec, puis en un ou plusieurs tickets dans le gestionnaire du projet — fichiers locaux, GitHub, GitLab, Jira ou autre — et, si le projet en a un, l'inscrire dans ROADMAP.md. Pas de nouvel entretien : une synthèse fidèle de ce qui est déjà tranché. Utilise ce skill dès que l'utilisateur veut « en faire une spec », « en faire un ticket », « mettre ça de côté pour plus tard », « garder une trace de ce qu'on a décidé » ou « préparer le travail pour une autre session ».
---

# To-spec : des décisions à la spec

La spec existe parce que les conversations se terminent. Tout ce qui a été tranché (la forme de
la solution, les choix discutés, ce qu'on a refusé) tient dans une conversation qui va
disparaître ; la spec est ce qui en reste. Elle **enregistre** des décisions, elle n'en prend
pas : toute affirmation de la spec que l'utilisateur n'a pas faite est un défaut.

Réponds dans la langue de l'utilisateur.

## 1. Rassembler

- La conversation : décisions, critères, interfaces à tester, hors périmètre, recherches et leurs
  sources.
- Si l'utilisateur donne une référence (un ticket, un fichier), la lire en entier.
- Le code, si ce n'est pas déjà fait : ce qui existe, le vocabulaire du projet, les conventions.
- Le gestionnaire de tickets : appeler le Skill tool avec « tickets ». Il lit la section
  `## Tickets` du `CLAUDE.md`, ou la fait configurer la première fois.

**Pas d'entretien.** Si une décision essentielle manque (le comportement principal, le
périmètre), ne pas l'inventer : la marquer **[À valider]** dans la spec et le dire. S'il en manque
beaucoup, proposer de revenir à `feature` plutôt que de publier une spec creuse.

**Interfaces à tester** : si elles n'ont pas été fixées, les proposer (celles qui existent déjà
d'abord, les plus hautes possibles, le moins possible) et les faire confirmer. Elles guideront
`tdd` et la relecture.

## 2. Choisir la forme

Estimer la taille, puis recommander avec AskUserQuestion :

- **Un seul ticket** (recommandé si le travail tient dans une session) : le ticket contient la
  spec complète. Pas de spec séparée.
- **Une spec et plusieurs tickets** (recommandé si plusieurs sessions) : la spec est publiée,
  puis découpée en tickets par le skill `to-tickets`.

## 3. Rédiger

Suivre [references/spec.md](references/spec.md). Montrer le brouillon et laisser l'utilisateur le
corriger avant toute publication.

## 4. Publier

Selon la configuration de `tickets` :

- **Un seul ticket** : le créer (fichier dans `docs/tickets/<feature>/01-<slug>.md` en local,
  issue ailleurs).
- **Spec + tickets** : créer la spec (`docs/specs/<feature>.md` en local, ticket parent
  ailleurs), puis appeler le Skill tool avec « to-tickets » en lui donnant la référence de la
  spec.

Sur un gestionnaire distant, rien n'est publié sans accord explicite sur le contenu final.

## 5. Roadmap et suite

- Si le projet a un `ROADMAP.md`, proposer d'y ajouter une entrée dans son format, avec le lien
  vers la spec ou le ticket.
- Terminer par la référence de ce qui a été créé, et la commande pour s'y mettre :
  `/implement <référence du ticket>`.

## Ce que ce skill ne fait jamais

- Poser une nouvelle série de questions : les décisions se prennent dans `feature` ou
  `brainstorming`.
- Ajouter à la spec une décision que personne n'a prise.
- Publier sans avoir montré le contenu et obtenu l'accord.
