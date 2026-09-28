# review : relire le travail contre la spec et les conventions

> Statut : terminé le 28/09/2026
> Origine : cadrage du 28/09/2026 (point 2 de l'audit des skills, dans la conversation)

## Objectif

`implement` finit un plan sans second regard : personne ne vérifie que le diff fait ce que le
plan ou le ticket demandait, ni qu'il respecte les conventions du dépôt. `review` relit le diff
sur deux axes séparés, spec et conventions, dans deux sous-agents au contexte vierge. Il se lance
seul sur une branche, ou depuis `implement` en fin de plan, qui corrige ensuite les remarques que
l'utilisateur retient.

## Décisions

- Un skill à part, `review`, que Claude peut déclencher : `implement` l'appelle en fin de plan, et
  l'utilisateur peut le lancer seul (« relis la branche », « review de ce que j'ai fait »).
- Nom `review` : `/code-review` existe déjà dans Claude Code (chasse aux bugs). À vérifier après
  l'installation : `/review` doit lancer ce skill.
- Deux axes, d'après le `code-review` de Matt Pocock :
  - **spec** : ce qui manque ou est partiel, ce qui dépasse le périmètre, ce qui paraît faux,
    chacun avec la ligne de la source citée (`AC-n`, hors périmètre) ;
  - **conventions** : `CLAUDE.md`, `CONTEXT.md`, les ADR, `docs/design/DESIGN.md` s'il y a de
    l'interface, plus une base d'odeurs de code (Fowler) qui ne sont que des jugements ; une règle
    écrite du dépôt l'emporte toujours.
- Les deux rapports restent séparés, jamais fusionnés ni reclassés entre eux. Les bugs restent à
  `/code-review`, que le rapport propose.
- Le diff part de la base de la branche (`git merge-base`) et inclut le travail non commité.
- Depuis `implement` : les remarques sont numérotées `R-1`, `R-2`… dans le journal du plan ;
  l'utilisateur choisit ; les retenues deviennent les tâches d'une vague « Retours de revue »,
  faites en TDD avant le bilan ; les écartées sont notées avec leur raison.
- Pas de revue pour un plan d'origine POC : le code est jetable.
- Un seul commit sur `main` (convention du `CLAUDE.md`).

## Critères d'acceptation

- AC-1 : lancé seul, `review` établit le point fixe (donné, sinon la base de la branche, sinon il
  demande), vérifie qu'il existe et que le diff n'est pas vide, sinon s'arrête ; le diff inclut le
  travail non commité.
- AC-2 : il trouve la source de la spec (chemin donné, plan cité par `Refs:` dans les commits,
  ticket via `tickets`, spec de `docs/specs/`) ; sinon il demande ; sans source, l'axe spec est
  sauté et le rapport le dit.
- AC-3 : deux sous-agents tournent en parallèle, chacun avec le diff, ses sources et (pour les
  conventions) la base d'odeurs ; le rapport les présente sous `## Spec` et `## Conventions`,
  chaque remarque citant sa source, violations et jugements distingués, puis une ligne de
  résumé par axe et la proposition de `/code-review` pour les bugs.
- AC-4 : en fin de plan, `implement` appelle `review` avant le bilan ; les remarques `R-n` vont
  dans le journal ; les retenues deviennent une vague « Retours de revue » exécutée en TDD ; les
  écartées sont notées avec leur raison ; le bilan vient ensuite.
- AC-5 : un plan d'origine POC n'est pas relu.
- AC-6 : `review` part sur « relis la branche » ou « vérifie que ce que j'ai fait colle au
  ticket », pas sur « cherche les bugs de ce diff » ; `MINE` et `evals/triggers.json` sont à
  jour.
- AC-7 : `README.md`, `CREDITS.md`, `TODO.md` et la carte de `next` sont à jour ; `/review` lance
  ce skill.

## Interfaces à tester

- `review` seul, sur une branche de ce dépôt (AC-1 à AC-3) : essai réel.
- `implement`, section « Fin du plan », relue (AC-4, AC-5).
- Le banc d'essai des déclencheurs, lancé après accord (AC-6).
- La liste des skills d'une session neuve (AC-7).

## Hors périmètre

- Un axe bugs ou sécurité : `/code-review` et `/security-review` existent.
- La divergence de `tdd` avec Matt (la refactorisation dans la boucle plutôt qu'en revue).
- Une revue à chaque vague, la publication des remarques en commentaires de PR.

## Vague 1 : `review` utilisable seul et depuis `implement`

- [x] Écrire `review/SKILL.md` et `review/references/odeurs.md` (point fixe, source de la spec,
  sources des conventions, deux sous-agents, rapport séparé) ; moins de 150 lignes, description
  sans `#` (AC-1 à AC-3) : vérification prévue : essai réel sur une branche de ce dépôt.
- [x] `implement`, « Fin du plan » : appeler `review` avant le bilan, remarques `R-n`, vague
  « Retours de revue », pas de revue pour un POC ; le moins de lignes possible (AC-4, AC-5) :
  vérification prévue : relecture.
- [x] `evals/triggers.json` (phrases et pièges) et `MINE` dans `evals/run_triggers.py` (AC-6) :
  vérification prévue : JSON valide ; banc d'essai proposé, lancé après accord.
- [x] `README.md`, `CREDITS.md`, `TODO.md`, carte de `next` (AC-7) : vérification prévue :
  relecture.
- [x] `./install.sh review` (AC-7) : vérification prévue : le lien existe ; `/review` dans une
  session neuve lance le skill (essai de l'utilisateur).

## Vague 2 : Retours de revue

Retenues : R-1 à R-3, R-6 à R-15 (R-4 reste l'essai de l'utilisateur, R-5 est écartée : écarts
justifiés).

- [x] `review/SKILL.md` : fichiers non suivis inclus (R-1) ; gabarit avec une ligne par axe et
  violations séparées des jugements (R-2) ; formule « appeler le Skill tool » (R-8) ; « point
  fixe » partout (R-9) ; mention des bugs et crédit retirés du corps (R-10, R-11) ;
  « possible <odeur> » dans le brief (R-12) : vérification prévue : relecture et `grep`.
- [x] `implement`, « Fin du plan » : étapes renumérotées (R-6, R-14), vague de retours « en TDD »
  (R-3), puis le bilan sans nouvelle revue (R-7), ligne trop longue recoupée (R-15) :
  vérification prévue : relecture.
- [x] `CLAUDE.md` et `README.md` : la règle d'accord limitée au passage d'une étape du parcours à
  la suivante (R-13) ; ligne du banc d'essai recoupée (R-15) : vérification prévue : relecture
  contre `implement`, `plan`, `feature`.

## Journal

**Revue (28/09/2026)** : `review` lancé sur son propre diff (essai réel de la tâche 1), spec
`docs/plans/review.md`.

Spec :
- R-1 : `git diff <base>` ne montre pas les fichiers non suivis ; AC-1 n'est vrai qu'à moitié.
- R-2 : une seule ligne « En bref » au lieu d'une par axe ; le gabarit ne sépare pas violations
  et jugements (AC-3).
- R-3 : `implement` dit « exécutée comme les autres » ; le TDD n'est pas écrit (AC-4).
- R-4 : rien ne vérifie encore que `/review` lance ce skill (AC-7) : essai de l'utilisateur.
- R-5 : hors demande mais justifiés : « 36 appels » corrigé, lignes recoupées dans `implement`,
  ligne `/code-review` dans `next`, heuristique du point fixe sur `main`, recherche dans
  `docs/plans/`.
- R-6 : l'étape « 0. » d'`implement` paraît greffée ; l'exception POC est à vérifier.
- R-7 : rien ne dit ce qui suit la vague « Retours de revue » (nouvelle revue ou bilan).

Conventions :
- R-8 : « lu avec le skill `tickets` » au lieu de « appeler le Skill tool avec « tickets » »
  (`CLAUDE.md`, Conventions).
- R-9 : trois noms pour une notion : « point fixe », « point de départ », « base ».
- R-10 : « Pas pour les bugs : /code-review » répété trois fois.
- R-11 : crédit à Matt dans le corps du skill, alors que les autres skills adaptés le gardent
  dans `CREDITS.md` et le README.
- R-12 : « possible <odeur> » est dans `odeurs.md` mais pas dans le brief du sous-agent.
- R-13 : `implement` appelle `review` sans accord, alors que `CLAUDE.md` dit « n'en lance un
  autre qu'après accord explicite » : la règle est trop large (même cas pour `tdd`, `interview`,
  `research`).
- R-14 : numérotation « 0. » bricolée (même correction que R-6).
- R-15 : lignes restées trop longues après recoupage (`implement` « Cocher ensuite… »,
  `CLAUDE.md` banc d'essai).

**Vague 1 (28/09/2026)**

- Livré : `review/SKILL.md` et `review/references/odeurs.md` ; `implement` (relecture en fin de
  plan, sauf POC) ; `evals` (3 phrases dont un piège vers `/code-review`, `review` dans `MINE`) ;
  `README.md`, `CREDITS.md`, `TODO.md`, carte de `next` ; lien `~/.claude/skills/review`.
- Vérifié : essai réel de `review` sur son propre diff (deux sous-agents en parallèle, rapports
  séparés, 15 remarques utiles) ; JSON du banc valide ; lien créé.
- Écart : `CLAUDE.md` ne compte plus les appels du banc (« un appel par phrase »).

**Vague 2 : Retours de revue (28/09/2026)**

- Corrigé : R-1 (fichiers non suivis), R-2 (gabarit par axe, violations et jugements), R-3, R-6,
  R-7, R-14 (étapes 1 à 4 de « Fin du plan », vague de retours en TDD, puis le bilan), R-8 à R-12
  (`review` : formule d'appel, « point fixe », mention des bugs et crédits hors du corps,
  « possible <odeur> » dans le brief), R-13 (règle d'accord limitée au passage d'une étape du
  parcours à la suivante, dans `CLAUDE.md` et `README.md`), R-15 (lignes recoupées).
- Écartée : R-5 (écarts justifiés). Laissée à l'utilisateur : R-4.
- Vérifié par `grep` : plus de « point de départ » ni de « lu avec le skill » dans `review`, plus
  d'étape « 0. » dans `implement`, plus de « n'en lance un autre » dans `CLAUDE.md` et `README.md`.

## Réalisé

- AC-1 : atteint après R-1 (diff depuis la base, plus les fichiers non suivis).
- AC-2, AC-3 : atteints, prouvés par l'essai réel (spec trouvée, deux axes séparés) ; le gabarit
  corrigé (R-2) n'a pas été rejoué.
- AC-4, AC-5 : atteints (`implement`, « Fin du plan », étape 1) ; la boucle a tourné une fois à la
  main dans ce plan même.
- AC-6 : phrases et `MINE` à jour ; le banc d'essai n'a pas tourné (à lancer après accord).
- AC-7 : fichiers à jour, lien créé ; **non vérifié** : `/review` lance ce skill et pas une
  commande intégrée (R-4, essai de l'utilisateur).
- Tâches ajoutées : la vague 2, issue de la revue.
- Hors plan : rien de nouveau.

