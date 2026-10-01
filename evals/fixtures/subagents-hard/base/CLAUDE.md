# Atelier

Réservation de salles municipales pour les associations. Python 3.12, SQLite.

## Commandes

- Tests : `python3 -m pytest -q`
- Base locale : `python3 -m atelier.store --init atelier.db` applique les migrations dans l'ordre.

## Conventions

- Le vocabulaire suit `GLOSSARY.md`, dans le code comme dans les tests.
- Les dates et heures sont des `datetime` avec fuseau, en UTC. L'heure courante vient de
  `dates.now_utc()`, jamais de `datetime.now()` ni de `datetime.utcnow()`.
- SQL : uniquement des requêtes paramétrées (`?`), jamais de f-string ni de concaténation.
- Toute écriture en base passe par `Store.transaction()`, qui ouvre un `BEGIN IMMEDIATE` :
  SQLite verrouille ainsi tôt, et deux réservations concurrentes ne se croisent pas.
- Une migration publiée ne se modifie jamais : tout changement de schéma est un nouveau fichier
  `migrations/NNN_<sujet>.sql`, numéroté à la suite.
- Les règles métier vivent dans `rules.py`, sous forme de fonctions `check_*` qui lèvent
  `RuleError` avec un message en français.
- `cli.py` est le seul module qui attrape `Exception` : il affiche un message propre au lieu
  d'une trace. Ailleurs, on n'attrape que des exceptions précises.
