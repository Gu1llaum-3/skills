# Forgejo et Gitea

Forgejo est un fork de Gitea : leurs API restent compatibles pour tout ce qui suit. Tout passe par
le CLI `tea` (celui de Gitea, qui marche aussi avec Forgejo). Vérifier d'abord `tea login list` :
si l'instance du remote n'y est pas, demander à l'utilisateur de lancer
`! tea login add --url https://<instance> --token <jeton>` (jeton créé dans Réglages >
Applications, avec les droits `issue` et `repository` en écriture). Dans `tea api`, `{owner}` et
`{repo}` sont remplacés automatiquement par le dépôt courant, et le préfixe `/api/v1` est ajouté.

Si `tea api` n'existe pas dans la version installée, la mettre à jour ; à défaut, faire les mêmes
appels avec `curl -H "Authorization: token <jeton>" https://<instance>/api/v1/…`.

## Créer

Écrire le corps dans un fichier temporaire, puis :

```bash
tea issues create --title "<titre>" --description-file <fichier> [--labels spec] [--milestone "<titre du jalon>"]
```

La commande affiche l'URL de l'issue ; son numéro est la fin de l'URL. Ne passer `--labels` que
si le label existe (`tea labels list`).

- **Spec** : une issue avec le contenu de la spec, label `spec` s'il existe. Forgejo et Gitea
  n'ont ni epics ni sous-issues : le lien vers la spec n'existe que dans le corps des tickets.
- **Ticket** : même modèle que pour GitHub (sections Spec, À livrer, Critères d'acceptation,
  Interfaces à tester, Bloqué par), avec des références `#<numéro>`.

## Relier

Les dépendances sont natives et utilisent le **numéro** de l'issue. Pour dire que le ticket est
bloqué par une autre issue du même dépôt :

```bash
tea api -X POST "/repos/{owner}/{repo}/issues/<numéro ticket>/dependencies" \
  -f owner=<owner> -f repo=<repo> -F index=<numéro bloquant>
```

Elles doivent être activées dans les réglages du dépôt (« Dépendances des tickets ») ; c'est le
cas par défaut. Si l'appel échoue (fonction désactivée, droits insuffisants), ne pas insister :
la section « Bloqué par » et la mention de la spec dans le corps suffisent. Le signaler dans le
compte rendu.

## Jalons (milestones)

- **Créer** : `tea milestones create --title "M1 : <nom>" --description "<objectif>"`.
- **Rattacher** : `--milestone "<titre>"` à la création, ou
  `tea issues edit <numéro> --milestone "<titre>"` ensuite.
- **Marquer réalisé** : `tea milestones close "<titre>"` (sans `--force`, qui le supprime).
- **Montrer la roadmap** :
  `tea api "/repos/{owner}/{repo}/milestones?state=all" | jq -r '.[] | "\(.title) : \(.closed_issues)/\(.open_issues + .closed_issues)"'`,
  puis `tea issues list --milestone "<titre>" --state all` pour le détail d'un jalon.

## Lire, lister, commenter, terminer

- **Lire** : `tea issues <numéro> --comments`, puis la spec citée dans le corps ; les bloquants
  avec `tea api "/repos/{owner}/{repo}/issues/<numéro>/dependencies"`.
- **Lister les ouverts** : `tea issues list --state open --keyword "<mots-clés>"`.
- **Commenter**, après feu vert : `tea comment <numéro> --description "<commentaire>"`.
- **Terminer** : de préférence par la pull request, avec `Closes #<numéro>` dans sa description.
  Sinon, après feu vert : `tea issues close <numéro>`.

Si une commande ou une option n'existe pas dans la version installée de `tea`, vérifier avec
`tea <commande> --help`.
