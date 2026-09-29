# Noms de fichiers des skills en anglais

> Statut : terminé le 29/09/2026
> Origine : cadrage du 29/09/2026 (conversation : audit face au dépôt de Matt Pocock)
> Branche : chore/english-file-names (demandée par l'utilisateur : pas sur main)

## Objectif

Les dossiers des skills sont en anglais, mais leurs fichiers de `references/` mélangent anglais
et français. Tous passent en anglais, `odeurs.md` compris ; leur contenu reste en français. La
règle entre dans `CLAUDE.md` pour que les prochains fichiers la suivent.

## Décisions

- Correspondance validée par l'utilisateur :

  | Actuel | Nouveau |
  |---|---|
  | `onboard/references/ecrire-pour-un-agent.md` | `onboard/references/writing-for-agents.md` |
  | `architecture/references/vocabulaire.md` | `architecture/references/vocabulary.md` |
  | `architecture/references/approfondir.md` | `architecture/references/deepening.md` |
  | `architecture/references/deux-conceptions.md` | `architecture/references/design-it-twice.md` |
  | `architecture/references/rapport-html.md` | `architecture/references/html-report.md` |
  | `poc/references/demo-logique.md` | `poc/references/logic-demo.md` |
  | `poc/references/variantes-ui.md` | `poc/references/ui-variants.md` |
  | `debug/references/boucles.md` | `debug/references/loops.md` |
  | `review/references/odeurs.md` | `review/references/smells.md` |
  | `implement/references/fin-selon-origine.md` | `implement/references/ending-by-origin.md` |
  | `plan/references/provenance.md` | `plan/references/origin.md` |
  | `brainstorming/references/modele-cahier-des-charges.md` | `brainstorming/references/spec-template.md` |
  | `naming/references/marques.md` | `naming/references/trademarks.md` |
  | `naming/references/nommage.md` | `naming/references/naming-template.md` |

  `naming/references/generation.md` est déjà un mot anglais : il ne bouge pas.
- Renommer avec `git mv`, pour que l'historique suive chaque fichier.
- Les plans de `docs/plans/` gardent les anciens noms : ils racontent ce qui a été fait à
  l'époque.
- **Ce que la vérification a montré** : ni `README.md` ni `docs/skills.template.html` (donc ni
  `docs/skills.html`) ne citent de fichier de `references/`. Ils ne citent que les fichiers
  écrits dans les projets (`docs/nommage.md`…), qui ne changent pas. Pour eux, le travail se
  limite à les relire, à corriger la phrase des crédits du `README.md` (cassée par un ajout du
  29/09 : « `debug` (d'après `diagnosing-bugs`) `retro`, … »), et à régénérer la page.
- Les renvois à mettre à jour, relevés avec `grep` :
  - `onboard/SKILL.md:90`, `retro/SKILL.md:32`, `CLAUDE.md:18`, `CREDITS.md:20` ;
  - `architecture/SKILL.md:15, 58, 68, 94`, et les liens entre ses références
    (`deepening.md:3`, `design-it-twice.md:5, 13`, `html-report.md:93`) ;
  - `poc/SKILL.md:45, 47`, `CREDITS.md:21` ;
  - `debug/SKILL.md:29, 76` ; `review/SKILL.md:44` ; `implement/SKILL.md:150` ;
    `plan/SKILL.md:21` ; `brainstorming/SKILL.md:57` ; `naming/SKILL.md:114, 133`.

## Critères d'acceptation

- AC-1 : chaque fichier de `*/references/` a un nom anglais, selon la correspondance.
- AC-2 : aucun lien relatif cassé dans les `SKILL.md` et les `references/` (en dehors des
  chemins d'exemple des modèles, déjà relevés : `to-questionnaire`, `glossary-format.md`,
  `tickets/references/local.md`).
- AC-3 : aucun ancien nom de fichier n'est cité hors de `docs/plans/`.
- AC-4 : le contenu des fichiers renommés ne change pas, à part les liens qui pointent vers un
  autre fichier renommé.
- AC-5 : `CLAUDE.md` dit la règle (noms de fichiers et de dossiers des skills en anglais,
  contenu en français, fichiers écrits dans les projets inchangés) et le piège d'un renommage de
  fichier de référence.
- AC-6 : la phrase des crédits du `README.md` se lit correctement ; `docs/skills.html` est
  régénérée et ses tests passent.
- AC-7 : tout le travail est sur la branche `chore/english-file-names` ; `main` n'a pas bougé.

## Hors périmètre

- ~~Les noms des fichiers écrits dans les projets~~ : repris par l'amendement du 29/09/2026
  (R-7), sauf les noms tirés du sujet (slugs), qui suivent la langue de la conversation.
- Les titres et le texte à l'intérieur des fichiers.
- Les noms des dossiers de skills (déjà en anglais) et les fichiers de `docs/plans/`.

## Amendement du 29/09/2026 (après la revue)

Décidé par l'utilisateur, en vue d'une migration future vers l'anglais :

- Les fichiers fixes qu'un skill écrit dans un projet passent aussi en anglais :
  `docs/cahier-des-charges.md` → `docs/requirements.md`, `docs/nommage.md` → `docs/naming.md`.
  Les autres sont déjà en anglais (`GLOSSARY.md`, `ROADMAP.md`, `docs/conventions.md`,
  `docs/adr/`, `docs/plans/`, `docs/specs/`, `docs/questionnaires/`…).
- Les noms tirés du sujet (`docs/plans/<slug>.md`, `docs/questionnaires/<slug>-…`, branches)
  restent dans la langue de la conversation.
- Projets existants : lire l'ancien nom s'il est seul, et proposer le `git mv`, comme pour
  `CONTEXT.md`.
- Revue retenue : R-4, R-6, R-8 ; R-7 devient l'amendement ci-dessus ; R-5 se règle par un
  squash à la fusion.

- AC-8 : aucun fichier des skills n'a de nom français (`scripts/` compris).
- AC-9 : les skills écrivent `docs/requirements.md` et `docs/naming.md`, et lisent l'ancien nom
  s'il est seul, en proposant le `git mv` (`brainstorming`, `naming`, `feature`, `design`).
- AC-10 : `README.md`, `docs/skills.template.html`, `evals/triggers.json`, les exemples des
  références et `CLAUDE.md` citent les nouveaux noms ; la règle de `CLAUDE.md` le dit.
- AC-11 : un seul piège de renommage dans `CLAUDE.md` (R-6) ; la liste des filiations ne vit
  que dans `CREDITS.md` (R-8).

## Vague 1 : les fichiers renommés et leurs renvois

- [x] `architecture` : renommer ses quatre références et mettre à jour `SKILL.md` et les liens
  entre elles (AC-1, AC-2, AC-4) ; vérification : le script de liens et `grep`.
- [x] `poc` : renommer `demo-logique.md` et `variantes-ui.md`, mettre à jour `poc/SKILL.md` et
  `CREDITS.md` (AC-1, AC-2) ; vérification : idem.
- [x] `onboard` : renommer `ecrire-pour-un-agent.md`, mettre à jour `onboard/SKILL.md`,
  `retro/SKILL.md`, `CLAUDE.md` et `CREDITS.md` (AC-1, AC-2) ; vérification : idem.
- [x] `debug`, `review`, `implement`, `plan`, `brainstorming`, `naming` : renommer leurs
  références et mettre à jour leur `SKILL.md` (AC-1, AC-2, AC-4) ; vérification : idem.
- [x] `CLAUDE.md` : la règle dans « Conventions », et dans « Pièges » le renommage d'un fichier
  de référence (le chercher avec `grep -rn "<ancien-nom>.md"`) (AC-5) ; vérification : relecture.
- [x] `README.md` : corriger la phrase des crédits, régénérer `docs/skills.html`, lancer ses
  tests, et vérifier que les liens de `~/.claude/skills/` pointent toujours vers le dépôt
  (`./install.sh`) (AC-3, AC-6, AC-7) ; vérification : `python3 -m unittest
  docs/test_build_skills_page.py`, `grep` des anciens noms, `git log main..`.

## Vague 2 : retours de revue

- [x] R-4 : `git-guardrails/scripts/bloquer-git-dangereux.sh` → `block-dangerous-git.sh`, et ses
  5 mentions dans `git-guardrails/SKILL.md` ; vérification : le hook rend 2 sur `git push`, 0 sur
  `git status` (AC-8).
- [x] R-7 : `docs/requirements.md` à la place de `docs/cahier-des-charges.md` dans les skills,
  avec la lecture de l'ancien nom (`brainstorming`, `feature`, `design`, `naming`), et dans
  `implement`, `plan/references/plan.md`, `tickets/references/local.md`, le `README.md`, la page
  et `evals/triggers.json` (AC-9, AC-10).
- [x] R-7 : `docs/naming.md` à la place de `docs/nommage.md` (`naming`, son gabarit, `design`,
  `README.md`, la page) (AC-9, AC-10).
- [x] R-6 et R-7 : `CLAUDE.md`, un seul piège pour renommer un skill ou un fichier, et la règle
  étendue aux fichiers écrits dans les projets (AC-10, AC-11).
- [x] R-8 : les crédits du `README.md` renvoient à `CREDITS.md` au lieu de répéter la liste ;
  régénérer la page, lancer ses tests et le script de vérification complet (AC-11).

## Journal

### Vague 1 (29/09/2026)

- Livré : 14 fichiers renommés avec `git mv` (10 identiques, les 4 d'`architecture` ne changent
  que sur leurs liens mutuels), 16 renvois mis à jour, la règle et le piège dans `CLAUDE.md`, la
  phrase des crédits du `README.md` réparée, la page régénérée.
- Vérifié par script : aucun lien cassé (liens markdown et chemins entre backticks), aucun ancien
  nom hors de `docs/plans/`, appels au Skill tool vers des skills existants que Claude peut
  lancer, les 25 skills dans le `README`, la carte de `next` et `COLUMNS`, `MINE` et
  `triggers.json` à jour, descriptions et longueurs dans les limites, aucun tiret long, liens de
  `~/.claude/skills/` valides. Tests de la page : 8/8.
- Écart : la phrase des crédits réparée nomme aussi `git-guardrails-claude-code`, `prototype` et
  `writing-for-agents`, qui manquaient.

### Revue

- R-1 (spec) : journal vide alors que les cases sont cochées. Comblé par cette section.
- R-2 (spec) : la phrase des crédits fait plus que la réparation demandée (filiations ajoutées).
- R-3 (spec) : `docs/skills.html` affiche le commit d'avant sa régénération ; comportement
  habituel de la page.
- R-4 (conventions, violation) : `git-guardrails/scripts/bloquer-git-dangereux.sh` a un nom
  français, contraire à la nouvelle règle, qui vise tous les fichiers des skills.
- R-5 (conventions, violation) : 6 commits pour un seul changement, contre « un seul commit par
  changement » ; à régler par un squash à la fusion.
- R-6 (conventions, jugement) : possible code dupliqué entre les deux pièges de renommage de
  `CLAUDE.md` (skill, fichier de référence).
- R-7 (conventions, jugement) : possible nom mystérieux, `naming-template.md` produit
  `docs/nommage.md` ; voulu par la règle.
- R-8 (conventions, jugement) : possible changement divergent, les filiations vivent à la fois
  dans `README.md` et `CREDITS.md`.

### Vague 2 (29/09/2026)

- Livré : `block-dangerous-git.sh` (le hook rend 2 sur `git push`, 0 sur `git status`) ;
  `docs/requirements.md` et `docs/naming.md` dans les skills, avec la lecture des anciens noms
  (`brainstorming`, `feature`, `design`, `naming`) et la proposition du `git mv` là où le fichier
  s'écrit ; `CLAUDE.md` (règle étendue, un seul piège) ; crédits du `README.md` réduits à un
  renvoi vers `CREDITS.md`.
- Écart : le cache de `naming/scripts/check_names.py` passe de `~/.cache/nommage` à
  `~/.cache/naming` (un nom de fichier français que le skill écrivait sur la machine). Le cache
  existant est simplement reconstruit au prochain lancement.
- Vérifié par script : mêmes contrôles qu'en vague 1, tous verts (3 faux positifs connus : des
  chemins d'exemple dans `CLAUDE.md`, `README.md` et `CREDITS.md`) ; tous les fichiers des skills
  ont un nom anglais ; les anciens noms de fichiers de projet ne restent que dans les lignes de
  lecture de repli. Tests de la page : 8/8.
- Non vérifié : le banc d'essai des déclencheurs. Une phrase de `evals/triggers.json` cite
  maintenant `docs/requirements.md`.

## Réalisé

- AC-1 à AC-4 : atteints (vague 1 ; `git diff -M` : 10 fichiers identiques à 100 %, 4 changés
  sur leurs seuls liens).
- AC-5 : atteint, puis élargi par l'amendement (AC-10).
- AC-6 : atteint (8/8) ; la phrase des crédits est devenue un renvoi (R-8).
- AC-7 : atteint, `main` est resté à d672e15.
- AC-8 à AC-11 : atteints (vague 2).
- Tâches ajoutées : la vague 2, issue de la revue et de l'amendement.
- Hors plan : R-5 (un seul commit sur `main`) se règle par un squash à la fusion.

