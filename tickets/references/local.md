# Fichiers locaux

Specs, tickets et roadmap sont des fichiers Markdown versionnés avec le code. Les chemins par
défaut sont ceux de la section `## Tickets` : `docs/specs/<feature>.md`,
`docs/tickets/<feature>/<NN>-<slug>.md` et `ROADMAP.md`.

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

## Roadmap

`ROADMAP.md`, à la racine. Elle **regroupe** les tickets par jalon, elle ne les décrit pas : le
contenu et le statut vivent dans chaque ticket. La case cochée n'est que le reflet du statut, et
seul ce skill l'écrit, en même temps que le statut.

```markdown
# Roadmap

Jalons du [cahier des charges](docs/cahier-des-charges.md). Le détail et le statut de chaque
ticket sont dans son fichier.

## M1 : <nom du jalon>

<Objectif du jalon, en une phrase, repris du cahier des charges.>

- [x] [`export-csv/01` : <titre>](docs/tickets/export-csv/01-<slug>.md)
- [ ] [`export-csv/02` : <titre>](docs/tickets/export-csv/02-<slug>.md) (spec :
  [export-csv](docs/specs/export-csv.md))

## M2 : <nom du jalon>

…

## Plus tard

Tickets rattachés à aucun jalon.
```

Un projet sans cahier des charges n'a pas de phrase d'introduction ni de lien vers lui ; ses
jalons se créent à la demande. Un jalon dont tous les tickets sont terminés garde sa place : la
roadmap sert aussi d'historique.

## Opérations

- **Lire** : lire le fichier, puis la spec qu'il cite.
- **Lister les ouverts** : les fichiers de `docs/tickets/` dont le statut n'est pas « terminé »
  (`grep -L "Statut :\*\* terminé" -r docs/tickets`).
- **Statuts** : `prêt` → `en cours` → `terminé`. Un ticket est démarrable quand tous ses
  bloquants sont `terminé`. Sa spec suit : `en cours` dès qu'un de ses tickets l'est, `terminée`
  quand le dernier l'est.
- **Commenter** : ajouter en fin de fichier une section `## Commentaires`, puis une entrée datée
  par commentaire (`- JJ/MM/AAAA : …`).
- **Terminer** : passer le statut à `terminé`, cocher les critères atteints et la case du ticket
  dans `ROADMAP.md`, dans le même commit que le code ou juste après.
- **Créer les jalons** : créer `ROADMAP.md` s'il n'existe pas, avec une section par jalon.
- **Rattacher à un jalon** : ajouter la ligne du ticket sous son jalon, ou sous « Plus tard ».
  Le plan d'un jalon sans tickets s'y rattache de la même façon :
  `- [ ] [plan : <titre>](docs/plans/<slug>.md)`, cochée quand le plan est terminé. Un jalon est
  réalisé quand toutes ses lignes sont cochées.
  Un ticket n'apparaît qu'à un seul endroit.
- **Montrer la roadmap** : lire `ROADMAP.md`, puis vérifier que chaque case correspond au statut
  du ticket. Un écart se signale et se corrige après accord : c'est le ticket qui fait foi.
- **Commiter** specs et tickets comme le reste du code, selon le format de commit du dépôt.
