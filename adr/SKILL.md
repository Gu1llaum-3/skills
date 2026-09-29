---
name: adr
description: "Enregistrer une décision d'architecture dans docs/adr/, au format court, et tenir à jour le statut des ADR remplacés ; seulement pour une décision difficile à défaire, surprenante sans contexte et issue d'un vrai compromis. Utilise ce skill quand l'utilisateur veut noter une décision technique (« fais un ADR », « note cette décision »), revenir sur une décision passée pour la remplacer (« on abandonne Redis ») ou retrouver pourquoi elle a été prise (« pourquoi on avait choisi X ? »)."
---

# ADR

Un ADR (Architecture Decision Record) retient **qu'une décision a été prise, et pourquoi**. Sa
valeur : empêcher qu'on « corrige » dans six mois un choix délibéré, ou qu'on repropose une option
déjà écartée pour de bonnes raisons. Pas de remplir des sections.

Écris l'ADR dans la langue des ADR existants, sinon dans celle du projet.

## Quand un ADR se justifie

Les trois conditions à la fois :

1. **Difficile à défaire** : changer d'avis plus tard coûterait cher.
2. **Surprenante sans contexte** : un futur lecteur se demandera « pourquoi ont-ils fait ça ? ».
3. **Issue d'un vrai compromis** : il y avait de vraies alternatives, et on en a choisi une pour
   des raisons précises.

S'il en manque une, pas d'ADR : une décision facile à défaire, on la défera ; une décision
évidente, personne ne s'interrogera.

Ce qui en mérite souvent un :

- la forme de l'architecture (monorepo, séparation lecture et écriture, rendu serveur) ;
- les choix techniques qui enferment : base de données, authentification, hébergement, bus de
  messages. Pas chaque bibliothèque, seulement celles qu'on mettrait des semaines à remplacer ;
- les frontières et le périmètre : « les données client appartiennent au module Client, les autres
  n'y accèdent que par identifiant ». Les « non » explicites valent autant que les « oui » ;
- les écarts délibérés avec la voie évidente (« du SQL écrit à la main plutôt qu'un ORM, parce
  que… ») ;
- les contraintes invisibles dans le code (conformité, contrat d'un partenaire, performance
  exigée) ;
- une alternative rejetée pour une raison non évidente.

## Écrire

Proposer l'ADR en une ligne (titre et décision), et l'écrire après accord.

- **Emplacement** : `docs/adr/`, créé au premier ADR. Si le dépôt en a déjà un ailleurs, suivre
  sa convention.
- **Nom** : `NNNN-slug.md`, numéro suivant le plus élevé du dossier (`0001-postgres.md`).
- **Format** :

```markdown
# <Titre court de la décision>

<1 à 3 phrases : le contexte, ce qu'on a décidé, et pourquoi.>
```

C'est tout. Sections facultatives, seulement quand elles apportent quelque chose :

- `Statut : proposé | accepté | obsolète | remplacé par ADR-NNNN`, utile quand une décision est
  revue ;
- `Options envisagées`, quand les alternatives écartées valent d'être retenues ;
- `Conséquences`, quand des effets en aval ne sont pas évidents.

Commiter l'ADR avec le travail qui l'a motivé, ou seul s'il n'y en a pas, selon le format de
commit du dépôt.

## Revenir sur une décision

On ne réécrit pas un ADR accepté : on en écrit un nouveau qui cite l'ancien (« remplace
ADR-0003 »), et on passe l'ancien à `Statut : remplacé par ADR-NNNN`.

## Lire

Avant de proposer une option d'architecture, parcourir les titres de `docs/adr/` : si la question
a déjà été tranchée, le dire et citer l'ADR plutôt que de rouvrir le débat sans raison nouvelle.
