---
name: to-spec
description: "Transformer ce qui est déjà décidé dans la conversation, ou un jalon du cahier des charges d'un gros projet, en spec, puis en tickets rangés dans un jalon de la roadmap, sans nouvel entretien. Utilise ce skill quand l'utilisateur veut « en faire une spec » ou un ticket, garder une trace de ce qui est décidé pour plus tard (« mets ça de côté », « garde une trace de ce qu'on a décidé », « prépare le travail pour une autre session »), ou écrire la spec d'un jalon (« fais la spec du jalon 1 »)."
---

# To-spec : des décisions à la spec

La spec existe parce que les conversations se terminent. Tout ce qui a été tranché (la forme de
la solution, les choix discutés, ce qu'on a refusé) tient dans une conversation qui va
disparaître ; la spec est ce qui en reste. Elle **enregistre** des décisions, elle n'en prend
pas : toute affirmation de la spec que l'utilisateur n'a pas faite est un défaut.

## 1. Rassembler

- La conversation : décisions, critères, interfaces à tester, hors périmètre, recherches et leurs
  sources.
- **Un cahier des charges** (gros projet) : le lire en entier, puis traiter **un seul jalon** :
  celui que l'utilisateur désigne, sinon le premier qui n'a pas de spec. Les décisions qui valent
  pour tout le projet (architecture, modèle de données) se proposent en ADR, pour que les specs
  des jalons suivants les reprennent au lieu de les redécider.
- Si l'utilisateur donne une référence (un ticket, un fichier), la lire en entier.
- Le code, si ce n'est pas déjà fait : ce qui existe, le vocabulaire du projet (`CONTEXT.md`
  s'il existe : la spec emploie ses termes), les conventions.
- Les titres des ADR (`docs/adr/`) : la spec ne contredit pas une décision passée sans le dire.
- Le gestionnaire de tickets : appeler le Skill tool avec « tickets ». Il lit la section
  `## Tickets` du `CLAUDE.md`, ou la fait configurer la première fois.

**Pas d'entretien** sur le quoi. Si une décision essentielle manque (le comportement principal,
le périmètre), ne pas l'inventer : la marquer **[À valider]** dans la spec et le dire. Les
questions renvoyées au métier par `feature` ou `brainstorming` se reportent au format du skill
`to-questionnaire`. S'il en
manque beaucoup, proposer de revenir à `feature` ou à `brainstorming` plutôt que de publier une
spec creuse.

**Exception, depuis un cahier des charges** : il dit quoi construire, pas comment. Les points
techniques qu'il laisse ouverts (modules, interfaces, modèle de données, contrats d'API) se
tranchent ici :

- explorer le code s'il y en a déjà ;
- appeler le Skill tool avec « research » sur les mêmes signaux que `plan` (première fois,
  plusieurs approches valables, dépendance à choisir, domaine sensible, API externe) ;
- appeler le Skill tool avec « interview » sur **ces seuls points techniques**, en une ou deux
  séries. Le besoin et le périmètre ont été tranchés par `brainstorming` : on ne les rouvre pas.
  Un vrai trou dans le cahier des charges se note **[À valider]** et se remonte.

**Interfaces à tester** : si elles n'ont pas été fixées, les proposer (celles qui existent déjà
d'abord, les plus hautes possibles, le moins possible) et les faire confirmer. Elles guideront
`tdd` et la relecture.

## 2. Choisir la forme

Estimer la taille avec le critère « Taille » de [`to-tickets`](../to-tickets/SKILL.md), puis
recommander avec AskUserQuestion :

- **Un seul ticket** (recommandé si le travail tient en une session) : le ticket contient la
  spec complète. Pas de spec séparée.
- **Une spec et plusieurs tickets** (recommandé si plusieurs sessions) : la spec est publiée,
  puis découpée en tickets par le skill `to-tickets`.

Un jalon de gros projet prend presque toujours la deuxième forme : c'est ce qui l'a classé
« gros ». S'il tient finalement en une session, le dire : il peut se planifier directement avec
`plan`, et proposer de corriger le verdict d'envergure du cahier des charges (« simple »), pour
que la prochaine session ne le rejoue pas.

## 3. Rédiger

Suivre [references/spec.md](references/spec.md). Avant de montrer le brouillon, le relire d'un
œil neuf et corriger sans le signaler :

- **les trous** : « à définir », TODO, section vide, critère invérifiable ;
- **les contradictions** entre sections, par exemple une décision que le hors périmètre exclut ;
- **les phrases qu'on peut lire de deux façons** : écrire la lecture que la conversation a
  tranchée, sinon la marquer **[À valider]** ;
- **la taille** : si elle ne correspond plus à la forme choisie à l'étape 2, le dire.

Montrer ensuite le brouillon et laisser l'utilisateur le corriger avant toute publication.

## 4. Publier

Selon la configuration de `tickets` :

- **Un seul ticket** : le créer (fichier dans `docs/tickets/<feature>/01-<slug>.md` en local,
  issue ailleurs).
- **Spec + tickets** : créer la spec (`docs/specs/<feature>.md` en local, ticket parent
  ailleurs), puis appeler le Skill tool avec « to-tickets » en lui donnant la référence de la
  spec.

Sur un gestionnaire distant, rien n'est publié sans accord explicite sur le contenu final.

Une décision de la spec difficile à défaire, surprenante sans contexte et issue d'un vrai
compromis se propose en ADR, via le skill `adr`.

## 5. Roadmap et suite

- **Ranger le travail dans la roadmap**, avec le skill `tickets` :
  - depuis un cahier des charges : dans le jalon traité. S'ils n'existent pas encore, créer les
    jalons du cahier des charges, après accord sur la liste ;
  - sinon : proposer le jalon qui convient, ou « plus tard ». Si le projet n'a pas encore de
    jalons, ne pas en créer pour un seul ticket : le laisser hors jalon.
  - Pour une spec découpée, `to-tickets` range les tickets : lui indiquer le jalon.
- S'il y a des questions pour le métier sans questionnaire, proposer d'en faire un avec le
  skill `to-questionnaire`, publiable en commentaire de la spec ou du ticket.
- Terminer par la référence de ce qui a été créé, et la commande pour s'y mettre :
  `/implement <référence du ticket>`, un ticket par session.
