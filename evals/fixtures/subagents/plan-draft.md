# Export CSV des tâches

> Statut : à valider
> Origine : ticket docs/tickets/export/01-export-csv.md

## Objectif

Pouvoir ouvrir ses tâches dans un tableur : une commande `tasks export` écrit un CSV.

## Décisions

- Un module `src/tasks/export.py`, appelé par `cli.py`. Il lit les tâches avec
  `TaskRepository.all()` de `src/tasks/repository.py`, comme le fait déjà la commande `list`.
- Module `csv` de la bibliothèque standard, séparateur virgule.
- La colonne `due` s'écrit avec `dates.iso(t.due)` pour toutes les tâches : `iso()` renvoie une
  chaîne vide quand la date est `None`, il n'y a donc pas de cas particulier à traiter.

## Critères d'acceptation

- AC-1 : en-tête `id,title,done,due`, une ligne par tâche, `done` vaut `oui` ou `non`.
- AC-3 : `due` au format ISO 8601, vide sans échéance.
- AC-4 : fichier existant : erreur, sauf avec `--force`.

## Interfaces à tester

- `export.to_csv(tasks, path)` : contenu du fichier (AC-1, AC-3)
- `cli.main(["export", ...])` : code de retour

## Hors périmètre

- L'import.

## Vague 1 : l'export

- [ ] `export.to_csv` écrit l'en-tête et les lignes, `done` en oui/non, `due` en ISO (AC-1, AC-3)
- [ ] Sous-commande `export` dans `cli.py` (AC-1)
- [ ] `export.to_json`, sur le même modèle, pour préparer l'export suivant

## Journal
