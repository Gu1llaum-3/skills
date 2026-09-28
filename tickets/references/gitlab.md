# GitLab Issues

Tout passe par le CLI `glab`. Vérifier d'abord `glab auth status` ; s'il n'est pas connecté,
demander à l'utilisateur de lancer `! glab auth login`. Dans `glab api`, `:id` est remplacé
automatiquement par le projet courant.

## Créer

```bash
glab issue create --title "<titre>" --description "$(cat <fichier>)" [--label spec] --yes
```

La commande affiche l'URL de l'issue ; son numéro (`iid`) est la fin de l'URL. Ne passer
`--label` que si le label existe (`glab label list`).

- **Spec** : une issue avec le contenu de la spec, label `spec` s'il existe. Les epics GitLab
  demandent une offre payante : ne les utiliser que si la section `## Tickets` le dit.
- **Ticket** : même modèle que pour GitHub (sections Spec, À livrer, Critères d'acceptation,
  Interfaces à tester, Bloqué par), avec des références `#<iid>`.

## Relier

```bash
glab api --method POST projects/:id/issues/<iid ticket>/links \
  -f target_project_id=<id du projet> -f target_issue_iid=<iid cible> -f link_type=<type>
```

- ticket → spec : `link_type=relates_to` ;
- ticket → bloquant : `link_type=is_blocked_by` (offre payante ; sur l'offre gratuite, repli sur
  `relates_to`).

L'identifiant du projet s'obtient avec `glab api projects/:id | jq .id`. Si une commande ou une
option n'existe pas dans la version installée de `glab`, vérifier avec `glab <commande> --help`.
Si un lien échoue, s'en tenir au texte du corps et le signaler.

## Jalons (milestones)

- **Créer** : `glab api --method POST projects/:id/milestones -f title="M1 : <nom>" -f description="<objectif>"`.
- **Rattacher** : `--milestone "<titre>"` à la création, ou
  `glab issue update <iid> --milestone "<titre>"` ensuite.
- **Marquer réalisé** : `glab api --method PUT projects/:id/milestones/<id> -f state_event=close`.
- **Montrer la roadmap** : `glab api projects/:id/milestones` pour la liste, puis
  `glab issue list --milestone "<titre>" --all` pour le détail d'un jalon.

## Lire, lister, commenter, terminer

- **Lire** : `glab issue view <iid> --comments`.
- **Lister les ouverts** : `glab issue list --search "<mots-clés>"`.
- **Commenter**, après feu vert : `glab issue note <iid> --message "<commentaire>"`.
- **Terminer** : de préférence par la merge request, avec `Closes #<iid>` dans sa description.
  Sinon, après feu vert : `glab issue close <iid>`.
