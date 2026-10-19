# La pull request de fin de plan

La PR est ce que l'utilisateur relit : elle dit d'abord ce qu'il doit trancher, puis ce qui a été
décidé sans lui, avec de quoi le contester. Le plan reste la trace complète.

## Quand l'ouvrir

Toutes ces conditions, sinon pas de PR :

- la vérification complète est verte ;
- le plan n'est pas d'origine POC ;
- les commits sont autorisés (pas de consigne contraire) ;
- la branche n'est pas la branche principale (un dépôt qui commite sur `main` par convention n'a
  pas de PR) ;
- il y a un dépôt distant (`git remote`) ;
- l'outil de la forge est là et connecté : `gh` pour GitHub, `glab` pour GitLab, `tea` pour
  Forgejo ou Gitea (la section Tickets du `CLAUDE.md` ou l'URL du dépôt distant dit laquelle) ;
- le push n'est pas refusé (un hook comme `git-guardrails` peut l'interdire).

## L'ouvrir

1. `git push -u origin <branche du plan>`. Jamais de `--force`.
2. Créer la PR **en brouillon** vers la branche de départ (`gh pr create --draft --base <départ>`,
   `glab mr create --draft --target-branch <départ>`, ou l'équivalent), avec le titre au format
   du dépôt et le corps ci-dessous écrit dans un fichier (`--body-file`).
3. Donner le lien dans le message final.

## Sinon : afficher le texte

Si une condition manque, ou si le push ou la création échouent, ne pas insister : afficher le
titre et le corps, prêts à coller, et dire en une ligne pourquoi la PR n'est pas ouverte. Sans
commit, le corps le dit aussi : les changements sont dans le travail non commité.

## Le corps

Dans cet ordre, les sections vides omises :

```markdown
## À décider

- R-n · <constat> · options : <a> / <b> (recommandée : <a>)
- <tâche en échec dont rien ne dépendait, avec la raison>
- sécurité : <correction locale faite, signalée ici pour relecture>

## Décidé sans toi

- Corrigé : R-n · <constat> · <commit court>
- Écarté : ~~R-n · <constat>~~ · <preuve du juge>
- Décision autonome : <choix> ; <alternative écartée> ; <raison>

## Critères

- AC-n : atteint, <test qui le prouve> | non atteint, <pourquoi>

## Essayer

<la commande, et deux ou trois choses à regarder, tirées des « quoi essayer » des bilans>

Plan et journal complets : <chemin du plan>
<Closes #n, selon ending-by-origin.md>
```
