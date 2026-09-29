---
name: onboard
description: Préparer un projet existant pour Claude — créer, ou mettre à l'épreuve s'ils existent, les fichiers lus au démarrage d'une session (CLAUDE.md ou AGENTS.md, ARCHITECTURE.md si le dépôt le justifie, et la vérification de GLOSSARY.md), pour qu'ils ne contiennent que ce qui est vrai, utile et impossible à deviner en lisant le code.
argument-hint: "[vérifier seulement]"
disable-model-invocation: true
---

# Onboard : préparer un projet pour Claude

Un fichier de contexte est lu à chaque session : chaque ligne coûte, et une ligne fausse coûte
deux fois, parce que Claude la croit. Il ne doit donc contenir que **ce que Claude ne peut pas
deviner en lisant le code** : les commandes, les conventions que rien n'impose, les pièges, les
règles de travail. Ce skill crée ces fichiers quand ils manquent, et surtout **met à l'épreuve**
ceux qui existent : il ne les prend pas pour acquis.

Pour vérifier sans rien réécrire, l'utilisateur relance simplement ce skill en le disant (« vérifie
seulement ») : on s'arrête alors à l'étape 3.

## 1. Explorer

Lire, sans rien supposer :

- **Les fichiers de contexte** : `CLAUDE.md`, `AGENTS.md`, `CLAUDE.local.md`, les `CLAUDE.md` des
  sous-dossiers, `.claude/` (règles, commandes), `GLOSSARY.md` et `GLOSSARY-MAP.md`,
  `ARCHITECTURE.md`, `README.md`, et ce que `docs/` contient (`adr/`, `design/`, `specs/`…).
- **Les commandes** : `package.json`, `Makefile`, `justfile`, `mise.toml`, `pyproject.toml`,
  `Cargo.toml`, les scripts de `bin/` ou `scripts/`, la CI (`.github/workflows/`,
  `.gitlab-ci.yml`) : c'est elle qui dit ce qui est vraiment vérifié.
- **L'historique** : `git log` pour le format des commits et des branches, et les commits de
  correction (« fix », « revert ») qui révèlent des pièges.
- **Le code** : la structure, les modules, les frontières, avec un sous-agent d'exploration pour
  un gros dépôt. Signes de plusieurs domaines : `pnpm-workspace.yaml`, `workspaces` dans
  `package.json`, des `packages/*` ou services qui ont chacun leur code.

## 2. Mettre à l'épreuve ce qui existe

Chaque affirmation des fichiers de contexte est confrontée au dépôt, et classée :

- **faux** : une commande qui n'existe plus, un chemin disparu, une version dépassée, une
  convention que l'historique contredit ;
- **inutile** : ce qui se lit dans le code ou le README, un conseil générique (« écrire du code
  propre »), une liste de fichiers, une description de ce que fait chaque dossier évident ;
- **manquant** : la commande qui lance un seul test, un piège que la CI ou les correctifs
  révèlent, une règle de branche ou de commit que tout le monde suit ;
- **mal placé** : une règle qui ne vaut que pour un dossier, dans le fichier racine ; un long
  document importé à chaque session (`@fichier`) alors qu'il suffirait de le pointer ; une
  préférence personnelle dans le fichier partagé (sa place est `CLAUDE.local.md`) ;
- **contradictoire** : deux fichiers qui disent l'inverse, ou un fichier et le code.

**Les commandes** : vérifier que chacune existe (script, cible, binaire). Proposer ensuite la
liste des commandes rapides à lancer pour de vrai (lint, un seul fichier de test, vérification
de types), les lancer après accord, et noter le résultat. Les commandes longues ou à effets de
bord (build complet, déploiement, migration, envoi de données) se vérifient sur le papier
seulement.

**`GLOSSARY.md`**, s'il existe (un `CONTEXT.md` seul est son ancien nom : proposer le
`git mv`) : le vérifier avec le format du skill
[`domain-modeling`](../domain-modeling/references/glossary-format.md) (un terme par concept,
définitions courtes, pas de notion générale de programmation, pas d'implémentation) et contre le
code (un terme défini que le code nomme autrement). **Ne jamais le créer** : il naît au premier
terme tranché, pendant un entretien, avec `domain-modeling`.

## 3. Restituer

En un message court :

- ✅ ce qui est juste et utile, en une ligne ;
- ⚠️ les constats de l'étape 2, groupés par fichier, chacun avec sa preuve (« `npm run test:unit`
  n'existe plus : le script s'appelle `test` depuis le commit abc123 ») ;
- ce qui manque, et les fichiers qu'il faudrait créer ou non, avec la raison ;
- le résultat des commandes lancées.

En mode « vérifier seulement », s'arrêter ici.

## 4. Trancher

Ce qui ne se trouve pas dans le dépôt se demande : une convention non écrite, une règle d'équipe,
un piège connu de l'utilisateur seul. Appeler le Skill tool avec « interview », en une ou deux
séries au maximum, sur ces seuls points.

## 5. Rédiger

- **`CLAUDE.md` ou `AGENTS.md`** : suivre [references/claude-md.md](references/claude-md.md).
  Modifier celui qui existe ; si aucun n'existe, demander lequel créer. Si les deux existent,
  proposer d'en garder un comme source et de faire importer l'autre (`@AGENTS.md` dans
  `CLAUDE.md`), pour qu'ils ne divergent plus. Ne jamais effacer un passage de l'utilisateur sans
  le montrer dans les constats.
- **Un `CLAUDE.md` de sous-dossier**, quand des règles ne valent que pour lui (un front et un back
  aux conventions différentes).
- **`ARCHITECTURE.md`**, seulement si la structure ne se devine pas vite (plusieurs modules ou
  services, des frontières à respecter) : suivre
  [references/architecture.md](references/architecture.md). Il est **pointé** depuis `CLAUDE.md`
  (« lire avant de toucher à … »), pas importé.
- **La section `## Tickets`** : si elle manque, proposer de la configurer maintenant en appelant
  le Skill tool avec « tickets ». Sinon elle se configurera au premier ticket.
- **Une décision structurante découverte** (le choix d'une base, d'une architecture) sans ADR :
  la proposer en ADR, via le skill `adr`, sans l'écrire dans `CLAUDE.md`.

Montrer chaque fichier, ou le diff d'un fichier existant, avant d'écrire.

## 6. Écrire et conclure

Écrire après accord, puis proposer de commiter selon le format du dépôt. Terminer par ce qui a
changé, en quelques lignes, et rappeler qu'on peut relancer `/onboard` pour vérifier les fichiers
quand le projet aura bougé. Si les mêmes commandes demandent souvent une permission, suggérer
`/fewer-permission-prompts`.
