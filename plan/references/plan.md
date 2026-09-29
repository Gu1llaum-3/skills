# Modèle de plan pour implement

Le plan doit pouvoir être exécuté par `implement` sans la conversation sous les yeux : vagues,
tâches en cases à cocher, critères numérotés, et une ligne de validation datée. Une petite feature
tient souvent en une seule vague.

```markdown
# <Titre de la feature>

> Statut : à valider
> Origine : <cadrage du JJ/MM/AAAA | ticket 42 (lien) | spec docs/specs/<feature>.md | jalon N de docs/requirements.md | POC docs/poc/<slug>.md>
> Branche : <seulement si elle est imposée, par exemple poc/<slug>>

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
- **[Métier : <destinataire>, bloquante]** <question> → <lien vers le questionnaire>

## Vague 1 : <ce que la vague rend possible>

- [ ] <tâche> (AC-1)
- [ ] <tâche> (AC-2)
- [ ] <tâche sans test automatique> : vérification prévue : <essai, capture, commande>

## Journal
```

Règles :

- **Tranches verticales** : chaque tâche livre un morceau de comportement de bout en bout, pas
  une couche (« le modèle », puis « l'API », puis « l'écran »).
  **Exception** : un changement mécanique très large (renommer une colonne, changer un type
  partagé) ne passe pas au vert par tranche. Le découper en *expand–contract*, comme dans
  [`to-tickets`](../../to-tickets/SKILL.md) : une tâche ajoute la nouvelle forme à côté de
  l'ancienne, une tâche par lot migre les appels, une dernière supprime l'ancienne forme.
- **Interfaces à tester** : celles qui existent déjà d'abord, les plus hautes possibles, le moins
  possible. Celles d'une spec ou d'un ticket se reprennent telles quelles.
- Chaque tâche cite le ou les critères qu'elle prouve.
- Une tâche = un commit : si une tâche paraît demander plusieurs commits, la découper.
- Les refactorisations préalables repérées dans le code viennent en premières tâches.
- Plusieurs vagues seulement quand une pause d'essai par l'utilisateur a du sens entre elles.
- « Questions ouvertes » : une question **non bloquante** porte l'hypothèse que le plan applique ;
  une question **bloquante** pointe vers son questionnaire et empêche la validation. Section
  absente s'il n'y en a pas.
- La ligne `> Statut :` reste toujours en tête : `à valider`, puis `validé par <nom> le
  <JJ/MM/AAAA>` après l'accord, puis `terminé le <JJ/MM/AAAA>` quand `implement` a fini.
