---
name: to-tickets
description: Découper une spec, un cahier des charges, un plan ou la conversation en tickets par tranches verticales, chacun avec ses critères d'acceptation et les tickets qui le bloquent, puis les publier dans le gestionnaire du projet (fichiers locaux, GitHub, GitLab, Jira ou autre). Utilise ce skill dès que l'utilisateur veut découper du travail en tickets, en issues ou en tâches à répartir sur plusieurs sessions (« découpe en tickets », « crée les issues », « fais-en des tickets »), et quand to-spec lui passe une spec à découper.
---

# To-tickets : découper en tranches verticales

Un bon découpage permet de prendre n'importe quel ticket démarrable, de le finir en une session,
et de montrer un résultat. C'est ce qui fait avancer un projet sur plusieurs sessions sans
tout garder en tête.

Réponds dans la langue de l'utilisateur.

## 1. Rassembler

- La source : la spec passée par `to-spec`, une référence donnée par l'utilisateur (la lire en
  entier, commentaires compris), un cahier des charges, ou la conversation.
- Le gestionnaire : appeler le Skill tool avec « tickets » pour connaître sa configuration.
- Le code, si ce n'est pas déjà fait : ce qui existe, et les **refactorisations préalables** qui
  rendraient le travail plus simple. « Rendre le changement facile, puis faire le changement
  facile. »

## 2. Découper

Des **tranches verticales** (balles traçantes) :

- chaque ticket traverse toutes les couches nécessaires (données, logique, API, écran, tests),
  sur un chemin étroit mais complet : jamais « tout le schéma », puis « toute l'API » ;
- un ticket terminé se montre ou se vérifie seul ;
- un ticket tient dans une session de travail ;
- les refactorisations préalables viennent en premier ;
- chaque ticket reprend les critères de la spec qu'il prouve (`AC-n`), et ses interfaces à
  tester.

Donner à chaque ticket ses **bloquants** : les tickets qui doivent être terminés avant qu'il
puisse démarrer. Un ticket sans bloquant démarre tout de suite. Ne déclarer que les dépendances
réelles : plus il y a de tickets démarrables en parallèle, mieux c'est.

**Exception : le changement mécanique très large** (renommer une colonne, changer un type
partagé), qui casse tout d'un coup et ne peut pas passer au vert par tranche. Le séquencer en
*expand–contract* : ajouter la nouvelle forme à côté de l'ancienne, migrer les appels par lots
(un ticket par lot), puis supprimer l'ancienne forme dans un dernier ticket bloqué par tous les
lots.

## 3. Faire valider

Présenter le découpage en liste numérotée. Pour chaque ticket : **titre**, **bloqué par**, **ce
qu'il livre**, **critères**. Puis demander :

- la granularité convient-elle (trop gros, trop fin) ?
- les dépendances sont-elles justes ?
- faut-il fusionner ou scinder des tickets ?

Itérer jusqu'à l'accord.

## 4. Publier

Avec le skill `tickets`, dans l'ordre des dépendances (bloquants d'abord), en rattachant chaque
ticket à la spec s'il y en a une. Sur un gestionnaire distant, l'accord donné à l'étape 3 vaut
pour ce contenu exact : toute modification ensuite se remontre.

Terminer par la liste des tickets créés (références et liens), en signalant ceux qui peuvent
démarrer tout de suite, et la commande pour attaquer le premier : `/implement <référence>`.

## Ce que ce skill ne fait jamais

- Publier un découpage que l'utilisateur n'a pas validé.
- Fermer, modifier ou supprimer un ticket existant, y compris la spec parente.
- Découper par couche technique.
