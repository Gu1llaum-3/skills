# Exporter les tâches en CSV

> Statut : à faire

## Besoin

Les utilisateurs veulent ouvrir leurs tâches dans un tableur.

## Critères d'acceptation

- AC-1 : `tasks export <fichier.csv>` écrit une ligne d'en-tête `id,title,done,due`, puis une
  ligne par tâche ; `done` vaut `oui` ou `non`, pour les tableurs en français.
- AC-2 : avec `--done`, seules les tâches terminées sont exportées.
- AC-3 : la colonne `due` est au format ISO 8601, et vide pour une tâche sans échéance.
- AC-4 : si le fichier existe déjà, la commande s'arrête avec un message d'erreur, sauf avec
  `--force`, qui l'écrase.

## Hors périmètre

- L'export JSON ou Excel.
- L'import.
