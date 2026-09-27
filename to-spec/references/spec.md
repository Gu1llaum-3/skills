# Modèle de spec

Supprimer les sections vides. Pas de chemins de fichiers ni d'extraits de code : ils vieillissent
vite. Seule exception : un extrait qui fixe une décision mieux que la prose (schéma, type, machine
à états), réduit à l'essentiel.

```markdown
# <Titre de la feature>

## Problème

Le problème que rencontre l'utilisateur, de son point de vue.

## Solution

La solution, du point de vue de l'utilisateur.

## Récits utilisateur

1. En tant que <acteur>, je veux <capacité>, pour <bénéfice>.
2. …

Une liste complète : tous les parcours, y compris les erreurs et les cas limites retenus.

## Critères d'acceptation

- AC-1 : <comportement vérifiable>
- AC-2 : …

## Décisions

- Modules construits ou modifiés, et leurs interfaces.
- Choix d'architecture, de bibliothèque (avec la source et la licence), de schéma de données,
  de contrat d'API.
- Chaque décision avec sa raison quand elle n'est pas évidente.

## Tests

- Interfaces à tester, et ce qu'on y vérifie (avec les AC concernés).
- Tests existants qui servent de modèle.
- Ce qui ne se teste pas automatiquement, et la vérification prévue à la place.

## Hors périmètre

Ce qui est explicitement exclu de cette version, et pourquoi si ce n'est pas évident.

## Questions ouvertes

Les points **[À valider]**, numérotés. Section absente s'il n'y en a pas.

## Notes

Recherches (avec leurs sources), pistes pour plus tard.
```
