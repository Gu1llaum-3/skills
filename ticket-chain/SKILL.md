---
name: ticket-chain
description: Enchaîner en autonomie les tickets ouverts d'une spec, un par un, chacun implémenté par un agent neuf, relu par quatre relecteurs indépendants et un juge, vérifié puis fusionné en local.
argument-hint: "<feature> [tickets : ref…] [rattrapage : ref…]"
disable-model-invocation: true
---

# Enchaîner les tickets d'une spec

Ce skill lance un workflow ([workflow.js](workflow.js)) qui traite les tickets ouverts d'une spec
**un par un**, sans attendre l'utilisateur entre deux tickets :

1. un agent neuf implémente le ticket sur sa branche avec `implement` en mode `enchaîné` (tests
   ciblés, ni relecture ni fusion) ;
2. quatre relecteurs au contexte vierge relisent le diff en parallèle : spec, conventions, bugs
   (agent `bug-hunter`), sécurité (seulement si le diff touche un chemin sensible) ; le juge
   `review-judge` classe leurs remarques ;
3. un agent neuf applique les remarques retenues, lance la **seule** vérification complète du
   ticket sur un arbre commité, puis fait le squash merge ;
4. un contrôle vérifie la branche principale, sans relancer la vérification si son arbre est
   celui qui a été vérifié ; une réparation au plus, puis arrêt.

Le workflow s'arrête au **premier blocage**. Ses décisions vont dans le journal du projet.

**Fermeture des tickets** : un ticket local se termine dans le commit de squash. Un ticket
distant se ferme **après** le squash et le contrôle, avec un commentaire de bilan, jamais
avant : lancer le skill vaut accord pour cette écriture. Une fermeture qui échoue n'arrête rien :
le lancement suivant voit le pied du ticket sur la branche principale, saute le ticket et retente
la fermeture. La fusion reste locale : le push est à l'utilisateur.

## 1. Préalables

Refuser de démarrer, en disant ce qui manque et comment le régler, si l'un de ces points manque :

- **Section `## Autonomie`** dans le `CLAUDE.md` du projet
  ([../implement/references/autonomy.md](../implement/references/autonomy.md)) avec
  `Fin : fusion locale`, une commande de **vérification** complète, et
  `Plan sans validation : tickets cadrés` (sans elle, chaque plan attendrait l'utilisateur et
  le premier ticket bloquerait). Proposer d'écrire la section manquante d'après l'exemple de
  la référence, et ne l'écrire qu'après accord.
- **Sur la branche principale** (`main`, ou celle que le dépôt désigne) : le workflow crée chaque
  branche de ticket depuis elle, et son contrôle l'exige.
- **Arbre de travail propre** (`git status --porcelain` vide) : les agents changent de branche et
  commitent dans ce dossier. Montrer ce qui traîne ; ne jamais le jeter ni le commiter soi-même.
- **La feature** en argument (le nom de la spec, comme `reservations`). Sans argument, appeler le
  Skill tool avec « tickets » pour lister les specs qui ont des tickets ouverts, et demander
  laquelle.

## 2. Les arguments

Tirés de la section `## Autonomie` et du dépôt, sans rien inventer :

| Argument | Source |
|---|---|
| `feature` | l'argument du skill |
| `mainBranch` | la branche principale |
| `branchPattern` | la convention de branches du `CLAUDE.md` (`<feature>`, `<NN>` et `<ref>` remplacés), sinon `ticket/<feature>-<NN>` |
| `verify` | l'entrée « Vérification » : la commande complète |
| `targetedTests` | l'entrée « Vérification » : comment lancer des tests ciblés |
| `journal` | l'entrée « Journal » |
| `sensitivePaths` | l'entrée « Chemins sensibles », ou absent |
| `commitFooter` | l'entrée « Pied de commit » |
| `remoteTracker` | `true` si la section « Tickets » du `CLAUDE.md` nomme un gestionnaire distant (GitHub, GitLab, Forgejo, Gitea, Jira…), `false` pour des fichiers locaux |
| `askFirst` | l'entrée « À demander », ou absent : le workflow renvoie alors à la valeur par défaut d'`autonomy.md` |
| `bugHunterPath`, `judgePath` | le fichier de l'agent, trouvé comme le dit [references/launching-a-workflow.md](references/launching-a-workflow.md) |
| `implementDir` | le chemin réel du dossier du skill `implement` : le workflow y lit la consigne de sécurité et les règles de déblocage |
| `tickets` | facultatif : ne traiter que ces tickets (`["reservations/03"]`) |
| `catchUp` | facultatif : tickets déjà fusionnés à relire et corriger (« rattrapage ») |

Appeler le Skill tool avec « tickets » pour lire les tickets de la spec, puis montrer en quelques
lignes ceux qui vont être traités (statuts et bloquants) et les arguments, et lancer sans
attendre : lancer le skill est l'accord.

## 3. Lancer

**Appeler l'outil Workflow** avec [workflow.js](workflow.js) en entier pour `script` et les
arguments pour `args`, comme le dit
[references/launching-a-workflow.md](references/launching-a-workflow.md).

Le workflow tourne en arrière-plan. Dire à l'utilisateur, en quelques lignes :

- **Pendant l'enchaînement**, les agents changent de branche et commitent dans ce dossier : tout
  autre travail se fait dans un worktree séparé
  (`git worktree add ../<dépôt>-<sujet> -b <branche> <principale>`), puis se fusionne dans la
  branche principale entre deux tickets, quand le dépôt y est et qu'il est propre.
- **Pause** : de préférence entre deux tickets (dépôt sur la branche principale, contrôle
  passé). En cours de ticket : arrêter le workflow, commiter le travail en cours sur la branche
  du ticket, puis revenir sur la branche principale.
- **Reprise** : comme le dit la référence. Dans une nouvelle session, relancer `/ticket-chain
  <feature>` : les tickets terminés sont sautés, et un ticket commencé reprend sur sa branche.

## 4. Rendre le rapport

Quand le workflow se termine, rendre :

- une ligne par ticket : statut (fusionné, bloqué, en échec), commit sur la branche principale,
  résumé ;
- **la raison de l'arrêt**, s'il y en a un, et ce qu'il faut faire pour reprendre ;
- les **actions humaines** de tous les rapports (celles qui ne bloquaient pas) ;
- les entrées ajoutées au journal du projet, à relire en priorité ;
- après une spec terminée, proposer à l'utilisateur de lancer `/code-audit since <commit>` sur
  ce qui vient d'être fusionné.
