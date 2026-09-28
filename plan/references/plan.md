# Modèle de plan pour implement

Le plan doit pouvoir être exécuté par `implement` sans la conversation sous les yeux : vagues,
tâches en cases à cocher, critères numérotés, et une ligne de validation datée. Une petite feature
tient souvent en une seule vague.

```markdown
# <Titre de la feature>

> Statut : à valider
> Origine : <cadrage du JJ/MM/AAAA | ticket 42 (lien) | spec docs/specs/<feature>.md | jalon N de docs/cahier-des-charges.md | POC docs/poc/<slug>.md>

## Objectif

Le problème et la solution, en deux ou trois phrases, du point de vue de l'utilisateur.

## Décisions

- <une décision par ligne, avec sa raison si elle n'est pas évidente>

## Critères d'acceptation

- AC-1 : <comportement vérifiable>
- AC-2 : …

## Interfaces à tester

- <interface publique> : <ce qu'on y vérifie> (AC-1, AC-2)

## Hors périmètre

- …

## Questions ouvertes

- **[Métier : <destinataire>]** <question> Hypothèse : <ce que le plan suppose en attendant>.
  → <lien vers le questionnaire>

## Vague 1 : <ce que la vague rend possible>

- [ ] <tâche> (AC-1)
- [ ] <tâche> (AC-2)
- [ ] <tâche sans test automatique> : vérification prévue : <essai, capture, commande>

## Journal
```

Règles :

- **Tranches verticales** : chaque tâche livre un morceau de comportement de bout en bout, pas
  une couche (« le modèle », puis « l'API », puis « l'écran »).
- Chaque tâche cite le ou les critères qu'elle prouve.
- Une tâche = un commit : si une tâche paraît demander plusieurs commits, la découper.
- Les refactorisations préalables repérées dans le code viennent en premières tâches.
- Plusieurs vagues seulement quand une pause d'essai par l'utilisateur a du sens entre elles.
- « Questions ouvertes » : seulement des questions **non bloquantes**, chacune avec l'hypothèse
  que le plan applique. Une question bloquante empêche la validation. Section absente s'il n'y en
  a pas.
- Après l'accord, remplacer « Statut : à valider » par « Validé par <nom> le <JJ/MM/AAAA> ».
