# GitHub Issues

Tout passe par le CLI `gh`. Vérifier d'abord `gh auth status` ; s'il n'est pas connecté, demander
à l'utilisateur de lancer `! gh auth login`. Dans `gh api`, `{owner}/{repo}` est remplacé
automatiquement par le dépôt courant.

## Créer

Écrire le corps dans un fichier temporaire, puis :

```bash
gh issue create --title "<titre>" --body-file <fichier> [--label spec]
```

La commande affiche l'URL de l'issue ; son numéro est la fin de l'URL. Ne passer `--label` que si
le label existe (`gh label list`).

- **Spec** : une issue avec le contenu de la spec, label `spec` s'il existe.
- **Ticket** : une issue avec le modèle ci-dessous.

```markdown
## Spec

#<numéro de la spec> (ou section absente)

## À livrer

Le comportement de bout en bout, du point de vue de l'utilisateur.

## Critères d'acceptation

- [ ] AC-1 : …

## Interfaces à tester

…

## Bloqué par

- #<numéro> (ou « aucun, peut démarrer tout de suite »)
```

## Relier

Les liens natifs utilisent l'**identifiant interne** de l'issue, pas son numéro :

```bash
gh api repos/{owner}/{repo}/issues/<numéro> --jq .id
```

- **Sous-issue de la spec** :
  `gh api repos/{owner}/{repo}/issues/<numéro spec>/sub_issues -X POST -F sub_issue_id=<id ticket>`
- **Bloqué par** :
  `gh api repos/{owner}/{repo}/issues/<numéro ticket>/dependencies/blocked_by -X POST -F issue_id=<id bloquant>`

Si un appel échoue (fonction absente de ce dépôt, droits insuffisants), ne pas insister : la
section « Bloqué par » et la mention de la spec dans le corps suffisent. Le signaler dans le
compte rendu.

## Jalons (milestones)

- **Créer** : `gh api repos/{owner}/{repo}/milestones -X POST -f title="M1 : <nom>" -f description="<objectif>"`.
- **Rattacher** : `--milestone "<titre>"` à la création, ou
  `gh issue edit <numéro> --milestone "<titre>"` ensuite.
- **Marquer réalisé** : `gh api repos/{owner}/{repo}/milestones/<numéro> -X PATCH -f state=closed`.
- **Montrer la roadmap** :
  `gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.title) : \(.closed_issues)/\(.open_issues + .closed_issues)"'`,
  puis `gh issue list --milestone "<titre>" --state all` pour le détail d'un jalon.

## Lire, lister, commenter, terminer

- **Lire** : `gh issue view <numéro> --comments`, puis la spec parente si elle est citée.
- **Lister les ouverts** : `gh issue list --state open --search "<mots-clés>"`.
- **Commenter**, après feu vert : `gh issue comment <numéro> --body-file <fichier>`.
- **Terminer** : de préférence par la pull request, avec `Closes #<numéro>` dans sa description.
  Sinon, après feu vert : `gh issue close <numéro> --comment "<bilan court>"`.
