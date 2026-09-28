# Contenu d'un ARCHITECTURE.md

La carte du dépôt pour quelqu'un qui arrive : où sont les choses, et ce qu'on ne doit pas
casser. Elle décrit ce qui change rarement ; le détail vit dans le code. Viser une ou deux pages.

```markdown
# Architecture

## Vue d'ensemble

<Le problème que résout le système, et son découpage en quelques phrases : les grands blocs et
comment une requête ou une donnée les traverse.>

## Carte du code

### <Module ou dossier>

<Ce dont il est responsable, en deux ou trois phrases, et les noms à chercher pour s'y
retrouver (types, points d'entrée), sans lien vers des lignes précises qui vieilliraient.>

## Invariants

- <Ce qui doit rester vrai et que le code ne dit pas à voix haute : « le module X n'importe
  jamais Y », « toute écriture passe par Z », « aucune donnée personnelle dans les logs ».>

## Frontières

- <Où passent les limites entre modules, services ou couches, et ce qui a le droit de les
  traverser.>

## Préoccupations transverses

- <Erreurs, logs, configuration, sécurité, tests : comment c'est organisé, en une ligne chacune.>
```

Règles :

- Nommer les modules et les types, pas les fichiers et les lignes : un nom se cherche, un lien
  casse.
- Les invariants sont la section la plus précieuse : ce sont souvent des absences (« n'appelle
  jamais »), invisibles dans le code.
- Pas de décision avec son historique : sa place est un ADR.
