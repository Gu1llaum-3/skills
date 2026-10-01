# Export CSV des tâches

> Statut : validé par Guillaume le 01/10/2026
> Origine : ticket docs/tickets/export/01-export-csv.md

## Objectif

Pouvoir ouvrir ses tâches dans un tableur : une commande `tasks export` écrit un CSV.

## Décisions

- Un module `src/tasks/export.py`, appelé par `cli.py` ; il lit les tâches avec `Store.load()`.
- Module `csv` de la bibliothèque standard, séparateur virgule.

## Critères d'acceptation

- AC-1 : en-tête `id,title,done,due`, une ligne par tâche, `done` vaut `oui` ou `non`.
- AC-2 : `--done` n'exporte que les tâches terminées.
- AC-3 : `due` au format ISO 8601 (via `dates.iso()`), vide sans échéance.
- AC-4 : fichier existant : erreur `ExportError`, sauf avec `--force`.

## Interfaces à tester

- `export.to_csv(tasks, path, force=False)` : contenu du fichier, refus d'écraser (AC-1, AC-3, AC-4)
- `cli.main(["export", ...])` : le filtre `--done` et le code de retour (AC-2, AC-4)

## Hors périmètre

- L'export JSON ou Excel, l'import.

## Vague 1 : l'export CSV

- [ ] `export.to_csv` écrit l'en-tête et les lignes, `done` en oui/non, `due` en ISO (AC-1, AC-3)
- [ ] `to_csv` refuse d'écraser un fichier existant sans `force` : `ExportError` (AC-4)
- [ ] Sous-commande `export` dans `cli.py`, avec `--done` et `--force` (AC-2, AC-4)

## Journal
