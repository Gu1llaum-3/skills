# Contenu d'un CLAUDE.md

Le fichier est lu à chaque session. Court : viser moins de 100 lignes, et chaque ligne doit
répondre à « Claude se tromperait-il sans elle ? ». Supprimer les sections sans contenu.

```markdown
# <Nom du projet>

<Une phrase : ce que fait le projet et pour qui. Pas plus : le README existe.>

## Commandes

- Vérification complète : `<commande>` (ce que lance la CI)
- Un seul fichier de test : `<commande> <chemin>`
- Lint et format : `<commande>`
- Lancer en local : `<commande>` (prérequis : <service, variable>)

## Conventions

- <Seulement ce que ni le linter ni le formateur n'imposent, et qu'on ne devine pas en lisant
  deux fichiers : où placer un nouveau module, comment nommer un test, ce qu'on ne fait jamais.>

## Pièges

- <Ce qui a déjà cassé et ne se voit pas : un ordre d'initialisation, un fichier généré à ne pas
  modifier, un test lent ou instable, une variable d'environnement obligatoire.>

## Travail

- Branches : <convention>. Commits : <format, avec un exemple réel de l'historique>.
- <Ce qu'il faut faire avant de dire « fini » : commande, essai manuel, capture.>

## Documents

- Avant de toucher à <zone> : lire `ARCHITECTURE.md`.
- Avant un travail d'interface : lire `docs/design/DESIGN.md`.
- Glossaire du domaine : `GLOSSARY.md`. Décisions : `docs/adr/`.

## Tickets

<Section tenue par le skill `tickets`.>
```

## Ce qui n'y va pas

- Ce que le code dit déjà : la stack visible dans `package.json`, la liste des dossiers, ce que
  fait chaque fonction.
- Le contenu du README, recopié.
- Les conseils génériques : « écrire des tests », « code lisible », « suivre les bonnes
  pratiques ».
- Ce qui change souvent : versions précises, liste de fonctionnalités, état d'avancement (sa
  place est la roadmap).
- Les secrets, les URL internes sensibles.
- Les préférences personnelles : `CLAUDE.local.md`, non versionné.
- Les règles de jugement qui ne servent qu'à relire (la cohérence entre fichiers) :
  `docs/conventions.md`, lu par `review`. Une règle mécanique devient un contrôle automatique.

## Importer ou pointer

`@chemin` importe un fichier à chaque session : seulement pour un fichier court dont chaque
session a besoin. Tout le reste se **pointe** avec la situation qui doit le faire lire (« avant
de toucher à la facturation, lire … »).
