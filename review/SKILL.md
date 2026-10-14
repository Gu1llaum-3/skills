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

## 5. Vérifier et classer

Un retour de sous-agent est une hypothèse. Pour chaque remarque :

1. **Vérifier** : relire le passage cité du diff et de la spec, puis marquer la remarque
   **confirmée**, **douteuse** (ce qui manque pour trancher) ou **fausse** (pourquoi, en une
   ligne). Ne rien corriger à cette étape.
2. **Proposer une action**, distincte de la marque (une remarque confirmée n'est pas forcément à
   corriger) :
   - **À corriger** : confirmée, et la correction est locale et sans débat ;
   - **À trancher** : un vrai compromis, que l'utilisateur seul peut arbitrer, ou une remarque
     douteuse ; **en cas de doute entre corriger et laisser, c'est ici** ;
   - **Rien à faire** : confirmée, mais sans effet ; avec une raison vérifiable (un fait du code,
     du dépôt ou de la spec), jamais une préférence. L'agent qui classe est souvent l'auteur du
     diff : sans raison vérifiable, la remarque va dans « À trancher » ;
   - **Déjà connu** : répète un écart déjà noté (journal du plan, bilan de vague) ;
   - **Fausse**.

Numéroter les remarques `R-1`, `R-2`… à travers les deux axes. Le classement par action ne
fusionne pas deux remarques, ne réécrit pas leur texte et ne change pas leur axe : c'est ce que la
séparation des sous-agents protège.

## 6. Rapporter

Le **rapport complet**, par axe, garde les extraits qui permettent de contester une remarque :

```markdown
## Spec

<le rapport du sous-agent, à peine nettoyé, avec R-n et la marque de chaque remarque ;
ou « pas de spec : axe sauté »>

## Conventions

### Violations
<les écarts aux règles écrites>

### Jugements
<les odeurs possibles>
```

La **vue groupée** est ce que l'utilisateur lit d'abord : une ligne par remarque,
`R-n · spec|conv · fichier:ligne · constat`, suivie de sa raison dans « Rien à faire », « Déjà
connu » et « Fausses ». Une remarque fausse reste visible, barrée, pour que l'utilisateur puisse
la contester. Les groupes vides sont omis ; l'ordre est celui-ci :

```markdown
**Relecture : <n> à corriger, <n> à trancher**, sur <n> remarques (spec <n>, conventions <n>).

À corriger
- R-3 · spec · docs/plans/x.md:42 · le plan écrit --migrate, les fichiers compose écrivent migrate
À trancher
- R-6 · conv · mise.toml:12 · calcul de version écrit deux fois ; le mettre en commun lance git à chaque appel
Rien à faire
- R-4 · spec · mise.toml:20 · build affiche le chemin du binaire : sortie seule, sans effet
Déjà connu
- R-1 · spec · mise.toml:41 · verify rouge (govulncheck) : déjà dans le journal
Fausses
- ~~R-7 · conv · README.md:30 · justification répétée~~ : le dépôt le fait partout

Pour les bugs : `/code-review`.
```

- **Appelé par `implement`** : lui rendre la main avec les deux ; il dit où les mettre.
- **Lancé seul** : afficher la vue groupée, puis le rapport complet en dessous, et poser la
  question.

## 7. Demander quoi corriger

Toujours avec AskUserQuestion, sauf s'il n'y a aucune remarque (le dire, puis continuer) :

- **« Que corriger ? »** : en premier le lot « À corriger », suivi de « (Recommandé) » ; puis un
  lot plus large qui reprend aussi les « Rien à faire » ; puis « Rien, passer au bilan » (appelé
  par `implement`) ou « Rien, s'arrêter là » (lancé seul). Chaque option nomme ses `R-n`. S'il n'y a rien à corriger, « Rien » vient en
  premier, recommandé.
- **Une question par remarque « À trancher »**, de 2 à 4 options qui portent le compromis, la
  recommandée en premier. Au-delà de 4 questions par appel, les suivantes vont dans un second
  appel.
- Les options listées seulement : l'outil ajoute de lui-même la réponse libre.

Ensuite :

- **Appelé par `implement`** : lui rendre la main avec les remarques retenues.
- **Lancé seul** : proposer la suite, sans la lancer :
  - quelques corrections locales : les faire ici, avec `tdd` si un comportement change ;
  - un manque de spec ou un vrai chantier : `/plan` à partir des remarques gardées, en
    continuant dans cette conversation, qui en est la source.
