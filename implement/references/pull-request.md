# La pull request de fin de plan

La PR décrit le changement, pour celui qui la fusionne et pour l'historique du dépôt : ce qui
change et pourquoi, pas comment le travail s'est fait. La relecture (remarques, verdicts du juge,
décisions autonomes) reste dans le journal du plan ; ce que l'utilisateur doit trancher ou relire
en priorité va dans le message final. Tant qu'un point « À décider » reste ouvert, la PR reste en
brouillon.

## Quand pousser la branche

Toutes ces conditions, sinon ni push ni PR :

- la vérification complète est verte ;
- le plan n'est pas d'origine POC ;
- les commits sont autorisés (pas de consigne contraire) ;
- la branche n'est pas la branche principale (un dépôt qui commite sur `main` par convention n'a
  pas de PR) ;
- il y a un dépôt distant (`git remote`).

Puis `git push -u origin <branche du plan>`, jamais `--force`. Un push refusé (un hook comme
`git-guardrails` peut l'interdire) : ne pas insister, afficher le texte (plus bas).

## Ouvrir la PR

Avec l'outil de la forge, s'il est là et connecté : `gh` pour GitHub, `glab` pour GitLab, `tea`
pour Forgejo ou Gitea (la section Tickets du `CLAUDE.md` ou l'URL du dépôt distant dit
laquelle). Créer la PR **en brouillon** vers la branche de départ (`gh pr create --draft --base
<départ>`, `glab mr create --draft --target-branch <départ>`, ou l'équivalent), avec le titre au
format du dépôt et le corps ci-dessous écrit dans un fichier (`--body-file`). Donner le lien dans
le message final.

**Sans outil** (Bitbucket, par exemple) : la branche est poussée quand même. Donner le lien de
création que la forge affiche au push (`remote: … pull request …`), sinon celui qui se déduit de
l'URL du dépôt distant :

- Bitbucket : `https://bitbucket.org/<espace>/<dépôt>/pull-requests/new?source=<branche>` ;
- GitHub : `https://github.com/<propriétaire>/<dépôt>/compare/<départ>...<branche>?expand=1` ;
- GitLab : `https://<hôte>/<groupe>/<projet>/-/merge_requests/new?merge_request[source_branch]=<branche>` ;
- une autre forge (Bitbucket Server, Forgejo ou Gitea sans `tea`…) : ne deviner aucun lien, le
  dire.

Puis le titre et le corps, prêts à coller, en rappelant de la créer en brouillon.

## Sinon : afficher le texte

Si une condition du push manque, ou si le push échoue : afficher le titre et le corps, prêts à
coller, et dire en une ligne pourquoi rien n'est poussé. Si seule la création échoue (outil
déconnecté, jeton expiré), la branche est poussée : faire comme sans outil, lien compris. Sans commit, le corps le
dit aussi : les changements sont dans le travail non commité.

## Le corps

Le modèle de PR du dépôt s'il en a un (`.github/pull_request_template.md`, ou l'équivalent de sa
forge), sinon celui-ci, sections vides omises, sans numéro `R-n` ni vocabulaire de relecture :

```markdown
<2 ou 3 phrases : le problème, ce qui change, pour qui>

## Changements

- <un comportement par ligne, du point de vue de l'utilisateur ou de l'appelant ; y compris ce
  qu'une correction de relecture a changé>

## Points d'attention

- <ce que le relecteur doit regarder : un risque, une limite connue, un comportement qui peut
  surprendre (par exemple une option prudente appliquée), un changement cassant>

## Critères

- AC-n : <ce que ça garantit>, <test qui le prouve>

## Essayer

<la commande, et deux ou trois choses à regarder, tirées des « quoi essayer » des bilans>

Plan, décisions et relecture : <chemin du plan>
<Closes #n, selon ending-by-origin.md>
```
