# Modèle de fichier POC

Un seul fichier, court : mini cahier des charges et spec minimale, puis le verdict une fois le
code fini. Supprimer les sections vides.

```markdown
# POC : <titre court>

> Statut : à valider | en cours | terminé
> Date : JJ/MM/AAAA
> Forme : essai technique | démo de logique | variantes d'interface

## Question

La question que le POC tranche, en une phrase.

## Hypothèse

Ce qu'on pense être vrai, et pourquoi on le pense.

## Critère de réussite

Ce qu'on devra observer pour répondre oui : un seuil, une durée, un essai sur un vrai cas.

## Périmètre

- Ce que le POC construit, au minimum.

## Hors périmètre

- Ce qu'on exclut exprès, pour aller vite.

## Choix

| Sujet | Choix | Statut |
|---|---|---|
| <stack, bibliothèque, source de données…> | <le choix> | décidé / hypothèse / ouvert |

- **décidé** : l'utilisateur l'a tranché, `/brainstorming` le reprend tel quel.
- **hypothèse** : pris pour aller vite, à rejouer si on approfondit.
- **ouvert** : pas tranché, le POC n'en avait pas besoin.

## Notes

Recherches (avec leurs sources), liens vers le plan (`docs/plans/…`) et la branche.

## Verdict

- **Résultat** : oui / non / en partie, au regard du critère de réussite.
- **Ce qui marche** : …
- **Ce qui casse** : …
- **Surprises** : …
- **Recommandation** : approfondir / abandonner / refaire autrement, et pourquoi.
```
