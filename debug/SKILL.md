---
name: debug
description: "Diagnostiquer un bug qui résiste (intermittent, régression entre deux versions, lenteur nouvelle, cause introuvable au premier regard) : une boucle qui échoue sur ce bug avant toute hypothèse, puis la cause confirmée, et un correctif avec test de non-régression s'il tient en une tâche. Utilise ce skill quand l'utilisateur dit « débogue ça », « je ne comprends pas pourquoi ça plante », « ça marche une fois sur dix » ou « c'est cassé depuis la dernière version ». Pas pour une erreur dont la cause se lit dans le message, ni pour un bug à la cause connue : c'est tdd."
argument-hint: "[symptôme]"
---

# Debug : un bug qui résiste

Devant un bug, l'agent lit le code et devine. Ce skill l'en empêche : **pas d'hypothèse tant
qu'aucune commande n'échoue sur ce bug précis**. Une fois cette boucle en place, le reste est
mécanique.

**Si une réponse directe suffit** (la cause se lit dans le message d'erreur, ou c'est une
question), la donner, sans dérouler les phases.

Lire `CONTEXT.md` s'il existe, et les ADR de la zone touchée.

## Masquer les secrets

Ce skill montre des commandes, des sorties et des captures : remplacer chaque secret par
`<MASQUÉ>` avant de les montrer. Construire les boucles avec des variables d'environnement, pour
que les identifiants restent dans l'environnement. D'une capture, ne citer que les lignes qui
portent le signal. Si la sortie masquée ne suffit plus à diagnostiquer, le dire et demander.

## 1. Construire la boucle

**C'est le cœur du skill** : y mettre l'effort, être inventif, ne pas lâcher. Les façons de
construire une boucle, les bugs intermittents et les régressions de performance sont dans
[references/boucles.md](references/boucles.md).

La phase est finie quand on peut nommer **une commande** (un test, un script, un curl), **déjà
lancée**, sortie montrée, qui est :

- **capable d'échouer sur ce bug** : elle passe par le vrai chemin du bug et vérifie le symptôme
  exact de l'utilisateur, pas « ne plante pas » ;
- **déterministe** : le même verdict à chaque fois (un bug intermittent : un taux de
  reproduction élevé et stable) ;
- **rapide** : quelques secondes ;
- **lançable sans l'utilisateur**, sauf dernier recours.

**Faute de boucle**, s'arrêter et le dire, lister ce qui a été essayé, et demander : un accès à
l'environnement qui reproduit, une capture (journal, fichier HAR, enregistrement daté), ou
l'accord pour une instrumentation temporaire. Ne pas passer aux hypothèses sans boucle : lire le
code pour bâtir une théorie avant d'avoir cette commande, c'est exactement l'erreur que ce skill
évite.

## 2. Reproduire et réduire

Lancer la boucle et la voir échouer, sur plusieurs lancers (un bug intermittent : à un taux assez
élevé pour déboguer). Vérifier que c'est **le symptôme de l'utilisateur**, pas un échec voisin :
mauvais bug, mauvais correctif. Noter le symptôme exact (message, sortie fausse, durée) : c'est
lui que le correctif devra faire disparaître.

Puis réduire le cas au plus petit scénario qui échoue encore : retirer les entrées, les appelants,
la configuration, les données, les étapes, **une à la fois**, en relançant la boucle à chaque
retrait. C'est fini quand chaque élément restant compte : en retirer un fait passer la boucle au
vert. Pas d'hypothèse avant d'avoir reproduit **et** réduit.

## 3. Formuler des hypothèses

**3 à 5 hypothèses**, classées, avant d'en tester une : une seule s'accroche à la première idée
plausible. Chacune est **réfutable** et dit sa prédiction :

> « Si <X> est la cause, alors <changer Y> fera disparaître le bug, et <changer Z> l'aggravera. »

Une hypothèse sans prédiction est une impression : la préciser ou l'écarter. Montrer la liste à
l'utilisateur, sans attendre sa réponse : il sait souvent ce qui a changé récemment ou ce qu'il a
déjà écarté.

## 4. Instrumenter

Chaque sonde répond à une prédiction de l'étape 3, **une variable à la fois** : le débogueur
avant les logs, et jamais « tout logger puis chercher ». Marquer chaque log de débogage d'un
préfixe unique, par exemple `[DEBUG-a4f2]` : le nettoyage tiendra en un `grep`. Une régression de
performance ne se piste pas aux logs : mesure de référence, puis bissection (voir la
[référence](references/boucles.md), « Instrumenter » et « Régressions de performance »).

Quand une hypothèse est confirmée, évaluer la taille du correctif (une tâche au sens de
[`to-tickets`](../to-tickets/SKILL.md), ou plus), puis s'arrêter :

> **Cause confirmée** : <la cause>. **Preuve** : <la sonde et ce qu'elle a montré>.
> **Correctif** : <une tâche : je corrige ? | plus gros : je passe à `plan` ?>

Attendre l'accord.

## 5. Corriger

**Le correctif tient en une tâche** :

1. transformer le cas réduit en test qui échoue, au bon point d'entrée, et le voir échouer ;
2. appliquer le correctif, et voir le test passer ;
3. relancer la boucle de l'étape 1 sur le scénario d'origine.

Un bon point d'entrée est celui où le test reproduit le vrai chemin du bug, tel qu'il se produit
chez l'appelant. **S'il n'en existe aucun**, le dire : c'est un résultat, l'architecture empêche
de verrouiller ce bug. Ne pas écrire un test trop superficiel qui rassurerait à tort.

**Le correctif est plus gros** : nettoyer d'abord l'instrumentation (étape 6 : logs marqués et
bancs jetables), puis donner le diagnostic (symptôme, commande de la boucle, cas réduit, cause,
preuve) et appeler le Skill tool avec « plan », qui en partira.

## 6. Nettoyer

Avant de dire que c'est fini :

- la boucle d'origine ne reproduit plus le bug ;
- le test de non-régression passe, ou l'absence de bon point d'entrée est dite ;
- plus aucun log marqué (`grep` du préfixe) ni banc jetable qui traîne ;
- commiter selon le format du dépôt, avec **l'hypothèse qui était la bonne** dans le message,
  pour le prochain qui déboguera.
