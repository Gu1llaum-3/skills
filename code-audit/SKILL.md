---
name: code-audit
description: "Auditer les bugs du code par domaine, sur un commit figé et en lecture seule : un chasseur de bugs par domaine, chaque remarque soumise à des agents qui tentent de la réfuter, puis un rapport daté dans docs/audits/."
argument-hint: "[domaines…] [since <commit>] [ref <branche>]"
disable-model-invocation: true
---

# Auditer le code

Ce skill lance un workflow ([workflow.js](workflow.js)) qui cherche les bugs du code, domaine par
domaine, sur un **commit figé** et en **lecture seule** :

1. un agent `bug-hunter` par domaine rapporte les défauts réels, avec un scénario de défaillance ;
2. chaque remarque passe devant des vérificateurs au contexte vierge qui tentent de la
   **réfuter** : trois pour une remarque critique ou majeure (la majorité l'emporte), un pour une
   mineure ;
3. un rapport daté, `docs/audits/<date>-<sha court>.md`, est commité dans un worktree.

L'audit **ne corrige rien** : les défauts confirmés deviennent une spec et des tickets.

## 1. Les domaines

Lire la section `## Audit du code` du `CLAUDE.md` du projet, au format de
[references/audit-section.md](references/audit-section.md) : pour chaque domaine, sa clé, son
titre, ses chemins et ses points d'attention.

**Sans section** : proposer des domaines tirés de l'arborescence, comme le dit la référence, et
n'écrire la section qu'après accord. L'audit attend la section.

## 2. Les arguments

| Argument | Source |
|---|---|
| `domains` | les domaines de la section : `[{ key, title, paths, focus }]` |
| `only` | facultatif : les clés de domaines passées en argument du skill |
| `since` | facultatif : un commit ; seuls les fichiers modifiés depuis sont audités. Sans argument, proposer le commit du dernier rapport d'audit du code de `docs/audits/` (son en-tête le donne ; les rapports `-upgrade.md` sont ceux de `/upgrade`) |
| `ref` | facultatif : la branche ou le commit audité, par défaut la branche principale |
| `mainBranch` | la branche principale |
| `sensitivePaths` | l'entrée « Chemins sensibles » de la section `## Autonomie`, s'il y en a une |
| `journal` | l'entrée « Journal » de la section `## Autonomie`, sinon `docs/journal.md` |
| `repoName` | le nom du dossier du dépôt, pour le worktree du rapport |
| `bugHunterPath` | le fichier de l'agent, trouvé comme le dit [../ticket-chain/references/launching-a-workflow.md](../ticket-chain/references/launching-a-workflow.md) |

Montrer en quelques lignes les domaines audités, `since` et `ref`, puis lancer sans attendre :
lancer le skill est l'accord.

## 3. Lancer

**Appeler l'outil Workflow** avec [workflow.js](workflow.js) en entier pour `script` et les
arguments pour `args`, comme le dit
[../ticket-chain/references/launching-a-workflow.md](../ticket-chain/references/launching-a-workflow.md)
(lancement et reprise).

Le code n'est lu qu'au commit figé : l'audit peut tourner pendant un autre travail, y compris
`/ticket-chain`. Seul le rapport s'écrit, **toujours dans un worktree**
(`../<dépôt>-audit-<sha court>`, branche `audit/<date>-<sha court>`), jamais dans le dossier
principal, où un autre travail peut changer de branche ou commiter à tout moment.

## 4. Rendre

Quand le workflow se termine :

- le chemin du rapport, son commit et son worktree, avec comment le ramener : `git merge
  --ff-only audit/<date>-<sha court>` depuis la branche principale quand le dossier principal y
  est et qu'il est propre (entre deux tickets si `/ticket-chain` tourne), puis `git worktree
  remove` et suppression de la branche ;
- les défauts confirmés par gravité et par domaine, les critiques d'abord ;
- la commande de l'audit suivant : `/code-audit since <sha>` ;
- s'il y a des défauts confirmés : proposer d'en faire une spec et des tickets, et sur accord
  appeler le Skill tool avec « to-spec » en lui donnant le rapport.
