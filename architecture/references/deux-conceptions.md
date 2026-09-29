# Concevoir deux fois (ou plus)

Pour comparer plusieurs interfaces possibles d'un module approfondi. D'après « Design It Twice »
(Ousterhout) : la première idée est rarement la meilleure. Vocabulaire :
[vocabulaire.md](vocabulaire.md).

## 1. Poser le problème

Avant de lancer les sous-agents, écrire pour l'utilisateur :

- les contraintes que toute nouvelle interface doit respecter ;
- les dépendances sur lesquelles elle s'appuie, et leur catégorie
  ([approfondir.md](approfondir.md)) ;
- une esquisse de code grossière, pour rendre les contraintes concrètes : pas une proposition.

Le montrer, puis passer tout de suite à l'étape 2 : l'utilisateur lit pendant que les
sous-agents travaillent.

## 2. Lancer les sous-agents

Au moins trois en parallèle, chacun avec un brief technique à part (chemins des fichiers,
couplages, catégorie de dépendance, ce qui passe derrière la jointure), le vocabulaire des
modules et celui de `GLOSSARY.md`, et une contrainte différente :

- 1 : « Réduire l'interface au minimum : 1 à 3 points d'entrée, le plus de levier possible pour
  chacun. »
- 2 : « Viser la souplesse : beaucoup d'usages, des extensions possibles. »
- 3 : « Optimiser pour l'appelant le plus courant : rendre le cas par défaut trivial. »
- 4, si c'est pertinent : « Construire autour de ports et d'adaptateurs pour les dépendances
  de l'autre côté de la jointure. »

Chacun rend :

1. l'interface : types, fonctions, paramètres, mais aussi invariants, ordre des appels, cas
   d'erreur ;
2. un exemple d'appel ;
3. ce que l'implémentation cache derrière la jointure ;
4. la stratégie de dépendance et les adaptateurs ;
5. les compromis : où le levier est fort, où il est mince.

## 3. Présenter et comparer

Présenter les conceptions l'une après l'autre, puis les comparer en prose par la **profondeur**
(le levier à l'interface), la **localité** (où les changements se concentrent) et la **place de
la jointure**.

Donner ensuite sa recommandation : la conception la plus solide, et pourquoi. Si des éléments de
plusieurs conceptions se combinent bien, proposer un hybride. Trancher : l'utilisateur attend un
avis net, pas un menu.
