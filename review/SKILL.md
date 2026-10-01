---
name: review
description: "Relire un diff (une branche, une PR, le travail en cours) sur deux axes séparés, la spec (plan, ticket : manques, dépassements, erreurs) et les conventions du dépôt, dans deux sous-agents au contexte vierge. Utilise ce skill quand l'utilisateur veut faire relire son travail (« relis la branche », « vérifie que ça colle au ticket 42 », « review depuis main »). Pas pour chercher des bugs : c'est /code-review."
argument-hint: "[point fixe : branche, commit, main] [spec : plan, ticket, chemin]"
---

# Review : la spec et les conventions

Un diff peut respecter toutes les conventions et faire autre chose que ce qui était demandé, ou
faire exactement ce qui était demandé en cassant les conventions. Ce skill relit les deux
séparément, dans deux sous-agents au contexte vierge, pour qu'un axe ne masque pas l'autre. Il ne
modifie rien : il rapporte, puis propose la suite.

## 1. Choisir le point fixe

- Le point fixe est celui que donne l'utilisateur ou l'appelant (branche, commit, tag, `main`).
  Sinon, la branche principale ; si l'on est dessus, le commit qui précède le premier commit du
  travail (`Refs:` du plan dans `git log`), sinon demander.
- Le diff part de `git merge-base <point fixe> HEAD` : `git diff <merge-base>` (il inclut le
  travail non commité), plus les fichiers nouveaux non suivis, que `git diff` ne montre pas
  (`git ls-files --others --exclude-standard`) et que les sous-agents lisent en entier. Noter
  aussi `git log <merge-base>..HEAD --oneline`.
- Vérifier que le point fixe existe (`git rev-parse`) et qu'il y a quelque chose à relire ;
  sinon s'arrêter ici et le dire, plutôt que dans deux sous-agents.

## 2. Trouver la spec

Dans cet ordre :

1. le chemin ou le ticket donnés par l'utilisateur ou l'appelant ;
2. un plan cité par `Refs:` dans les commits, ou le plan qu'`implement` exécute ;
3. un ticket cité dans les commits (`#42`, `PROJ-123`), et sa spec : appeler le Skill tool avec
   « tickets » pour les lire ;
4. une spec de `docs/specs/` ou un plan de `docs/plans/` qui correspond à la branche.

Si rien ne vient, demander. S'il n'y en a pas, l'axe spec est sauté et le rapport le dit.

## 3. Trouver les conventions

Ce que le dépôt écrit sur la façon de coder : `CLAUDE.md` (et ceux des sous-dossiers touchés),
`GLOSSARY.md` (les termes du domaine), les ADR de `docs/adr/`, `docs/design/DESIGN.md` si le diff
touche l'interface, `docs/conventions.md` (les règles de jugement, écrites pour la relecture) et
`CONTRIBUTING.md` s'ils existent. S'y ajoute la base d'odeurs de
[references/smells.md](references/smells.md), qu'on colle en entier dans le brief du sous-agent :
il n'y a pas accès autrement.

## 4. Lancer les deux sous-agents, en parallèle

Dans un seul message, deux sous-agents `general-purpose` au contexte vierge : pas `Explore`, qui
ne charge pas `CLAUDE.md`, la première source des conventions ; jamais un fork, qui hérite de la
conversation et donc des raisons de l'auteur. Le brief ne contient que ce qui suit : ni
justification des choix, ni résumé du travail.

**Spec** : la commande du diff, les fichiers non suivis, la liste des commits, la source de la
spec (chemin ou contenu).
Brief :

> Rapporte : (a) ce que la spec demande et qui manque ou n'est fait qu'en partie ; (b) ce que le
> diff fait sans que ce soit demandé, y compris ce que la spec met hors périmètre ; (c) ce qui
> paraît fait mais de travers. Cite pour chaque remarque la ligne de la spec (le critère `AC-n`
> s'il y en a) et le `fichier:ligne` du diff en cause. Une remarque sans ces deux preuves ne se
> rapporte pas. Moins de 400 mots.

**Conventions** : la commande du diff, les fichiers non suivis, la liste des commits, les
fichiers de l'étape 3 et la base d'odeurs. Brief :

> Rapporte, par fichier ou par morceau du diff : (a) les **violations** : chaque écart à une
> règle écrite du dépôt, en citant le `fichier:ligne` du diff et la règle ; (b) les
> **jugements** : chaque odeur de la base repérée, sous la forme « possible <odeur> », avec le
> `fichier:ligne` et l'extrait. Une remarque sans preuve ne se rapporte pas. Une règle du dépôt
> l'emporte sur une odeur. Ce que l'outillage impose déjà (linter, formateur, typage) ne se
> signale pas. Moins de 400 mots.

## 5. Rapporter

```markdown
## Spec

<le rapport du sous-agent, à peine nettoyé, avec la marque de vérification de chaque
remarque ; ou « pas de spec : axe sauté »>

## Conventions

### Violations
<les écarts aux règles écrites>

### Jugements
<les odeurs possibles>

**En bref** :
- Spec : <n> remarques (<n> confirmées), la plus grave : ….
- Conventions : <n> violations et <n> jugements (<n> confirmés), le plus grave : ….

Pour les bugs : `/code-review`.
```

- **Vérifier chaque remarque** avant de la rapporter : un retour de sous-agent est une
  hypothèse. Relire le passage cité du diff et de la spec, puis marquer la remarque
  **confirmée**, **douteuse** (ce qui manque pour trancher) ou **fausse** (pourquoi, en une
  ligne). Une remarque fausse reste au rapport, barrée, pour que l'utilisateur puisse la
  contester. Ne rien corriger à cette étape.
- Ne pas fusionner ni reclasser les remarques entre les deux axes : c'est ce que la séparation
  empêche.
- Numéroter les remarques `R-1`, `R-2`… à travers les deux axes.
- **Appelé par `implement`** : lui rendre la main avec le rapport.
- **Lancé seul** : demander quelles remarques l'utilisateur garde (« R-2 et R-5 ») ; les
  jugements ne sont que des odeurs possibles. Puis proposer la suite, sans la lancer :
  - quelques corrections locales : les faire ici, avec `tdd` si un comportement change ;
  - un manque de spec ou un vrai chantier : `/plan` à partir des remarques gardées, en
    continuant dans cette conversation, qui en est la source.
