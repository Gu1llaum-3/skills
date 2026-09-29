# Format de GLOSSARY.md

```markdown
# <Nom du domaine>

<Une ou deux phrases : ce que couvre ce domaine et pourquoi il existe.>

## Vocabulaire

**Commande** :
Un ensemble de produits payés par un client en une seule fois.
_À éviter_ : panier (le panier n'est pas encore payé), achat

**Avoir** :
Un montant dû au client après un retour, utilisable sur une prochaine commande.
_À éviter_ : remboursement (un remboursement rend l'argent sur la carte)

## Relations

- Un **Client** passe plusieurs **Commandes**
- Un **Avoir** vient toujours d'une **Commande** retournée

## Ambiguïtés tranchées

- « retour » désignait à la fois le colis renvoyé et l'avoir émis. Tranché : le colis est un
  **Retour**, l'argent est un **Avoir**.
```

## Règles

- **Trancher** : quand plusieurs mots existent pour un même concept, choisir le meilleur et mettre
  les autres dans « À éviter », avec la raison si elle n'est pas évidente.
- **Des définitions courtes** : une ou deux phrases, qui disent ce que la chose **est**, pas ce
  qu'elle fait.
- **Seulement les termes propres au projet** : pas de notions générales de programmation
  (timeout, cache, type d'erreur), même si le projet les emploie beaucoup. Avant d'ajouter un
  terme, se demander : est-ce une notion de ce domaine, ou de la programmation en général ?
- **Regrouper** sous des sous-titres quand des familles de termes apparaissent ; sinon, une
  seule liste.
- « Relations » et « Ambiguïtés tranchées » seulement quand il y a quelque chose à y mettre.

## Plusieurs domaines

`GLOSSARY-MAP.md` à la racine :

```markdown
# Carte des domaines

## Domaines

- [Commandes](./src/commandes/GLOSSARY.md) : reçoit et suit les commandes des clients
- [Facturation](./src/facturation/GLOSSARY.md) : émet les factures et les avoirs

## Relations

- **Commandes → Facturation** : une commande expédiée déclenche sa facture
```
