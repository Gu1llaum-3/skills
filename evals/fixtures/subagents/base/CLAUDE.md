# tasks

Petit gestionnaire de tâches en ligne de commande, en Python 3.12.

## Commandes

- Tests : `python3 -m pytest -q`

## Conventions

- Le code vit dans `src/tasks/`, les tests dans `tests/`, un fichier de test par module.
- Pas de `print` dans `src/tasks/`, sauf dans `cli.py`, qui écrit la sortie des commandes : les
  autres modules journalisent avec `logging.getLogger(__name__)`.
- Toute date écrite par l'application (fichier, sortie, export) passe par `dates.iso()`.
- Les erreurs prévues lèvent une exception de `errors.py`, avec un message en français.
