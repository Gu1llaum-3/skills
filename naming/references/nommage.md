# Gabarit de docs/nommage.md

Concis : c'est la trace de la décision, pour s'en souvenir dans six mois et ne pas rouvrir le débat sans raison. 40 à 80 lignes.

````markdown
# Nommage : <Nom retenu>

> Décision du <date>. Nom précédent / nom de code : <le cas échéant>

## Le nom

- **Nom** : <Nom> — prononciation : <FR> / <EN>
- **Origine et sens** : <langue, graphie d'origine, sens exact, pourquoi il colle au projet>
- **Déclinaisons** : domaine <…>, dépôt <…>, paquet / commande <…>, handle <…>

## Contexte du choix

- Produit : <1 phrase>
- Cible : <…>
- Critères posés : <langues, ton, longueur, extensions…>
- Secteur : motifs saturés évités <…>, espace visé <…>

## Disponibilité (vérifiée le <date>)

| Élément | Statut | Note |
|---|---|---|
| <nom>.fr | libre / pris / inconnu | |
| <nom>.com | … | |
| github.com/<nom> | … | |
| Homonymes dans le secteur | aucun / <liste> | |
| Marque | **à vérifier** — classes <…> | liens INPI / TMview |

## Alternatives écartées

| Nom | Raison de l'écart |
|---|---|
| <…> | <domaine pris, homonyme, sonne mal en anglais…> |

## Actions restantes

- [ ] Réserver <domaines>
- [ ] Vérifier la marque (INPI, TMview) en classes <…>
- [ ] Renommer dépôt, manifeste, README
````
