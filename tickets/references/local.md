# Fichiers locaux

Specs et tickets sont des fichiers Markdown versionnés avec le code. Les chemins par défaut sont
ceux de la section `## Tickets` : `docs/specs/<feature>.md` et
`docs/tickets/<feature>/<NN>-<slug>.md`.

- `<feature>` : slug court de la feature, en minuscules avec des tirets (`export-csv`).
- `<NN>` : numéro à deux chiffres, à partir de `01`, dans l'ordre des dépendances (bloquants
  d'abord). Un ticket se désigne par `<feature>/<NN>` (`export-csv/02`).
- Un fichier par ticket, jamais un fichier qui en regroupe plusieurs.

## Spec

Écrire le contenu produit par `to-spec` dans `docs/specs/<feature>.md`, avec en tête :

```markdown
# <Titre de la feature>

**Statut :** prête | en cours | terminée
**Tickets :** `docs/tickets/<feature>/`
```

## Ticket

```markdown
# <NN> : <Titre du ticket>

**Statut :** prêt
**Spec :** [docs/specs/<feature>.md](../../specs/<feature>.md) (ou « aucune »)
**Bloqué par :** `<feature>/01`, `<feature>/03` (ou « aucun, peut démarrer tout de suite »)

## À livrer

Le comportement de bout en bout que ce ticket rend possible, du point de vue de l'utilisateur,
pas une liste de couches à modifier.

## Critères d'acceptation

- [ ] AC-1 : …
- [ ] AC-2 : …

## Interfaces à tester

Les interfaces publiques où placer les tests, et ce qu'on y vérifie.
```

Un ticket sans spec (petite feature) porte en plus, avant « À livrer », les sections utiles de la
spec : problème, solution, décisions, hors périmètre.

## Opérations

- **Lire** : lire le fichier, puis la spec qu'il cite.
- **Lister les ouverts** : les fichiers de `docs/tickets/` dont le statut n'est pas « terminé »
  (`grep -L "Statut :\*\* terminé" -r docs/tickets`).
- **Statuts** : `prêt` → `en cours` → `terminé`. Un ticket est démarrable quand tous ses
  bloquants sont `terminé`.
- **Terminer** : passer le statut à `terminé` et cocher les critères atteints, dans le même
  commit que le code ou juste après.
- **Commiter** specs et tickets comme le reste du code, selon le format de commit du dépôt.
