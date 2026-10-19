---
name: review
description: "Relire un diff (une branche, une PR, le travail en cours) sur deux axes séparés, la spec (plan, ticket : manques, dépassements, erreurs) et les conventions du dépôt, dans deux sous-agents au contexte vierge, puis un juge qui classe chaque remarque avec une preuve. Utilise ce skill quand l'utilisateur veut faire relire son travail (« relis la branche », « vérifie que ça colle au ticket 42 », « review depuis main »). Pas pour chercher des bugs : c'est /code-review."
argument-hint: "[point fixe : branche, commit, main] [spec : plan, ticket, chemin]"
---

# Review : la spec et les conventions

Un diff peut respecter toutes les conventions et faire autre chose que ce qui était demandé, ou
faire exactement ce qui était demandé en cassant les conventions. Ce skill relit les deux
séparément, dans deux sous-agents au contexte vierge, pour qu'un axe ne masque pas l'autre, puis
fait classer leurs remarques par un juge qui n'a pas écrit le code. Il ne modifie rien : il
rapporte, puis propose la suite.

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

## 5. Faire classer par le juge

Un retour de sous-agent est une hypothèse, et l'agent qui lance `review` est souvent l'auteur du
diff : il ne classe pas lui-même. Le juge, l'agent `review-judge`
([../agents/review-judge.md](../agents/review-judge.md)), vérifie chaque remarque dans le code et
la classe, avec une preuve. Ses outils, fixés dans son fichier, ne lui permettent pas de
modifier le dépôt.

1. Numéroter les remarques `R-1`, `R-2`… à travers les axes, dans l'ordre spec, conventions,
   puis les constats de bugs que l'appelant a passés (axe `bug`, ceux de `/code-review` quand
   `implement` appelle).
2. Écrire le diff dans un fichier, sans le faire passer par la conversation, avec des commandes
   `git` seules (une session autonome ou le banc d'essai n'autorisent souvent que `git`, et
   refusent `$(…)`, `>` ou `mkdir`) : lire le dossier git (`git rev-parse --git-dir`), puis
   `git diff <merge-base> --output=<dossier git>/review-diff.patch`, chemin écrit en entier. Les
   fichiers non suivis sont lus par le juge à leur chemin.
3. Lancer l'outil Agent avec `subagent_type` `review-judge`, **au premier plan** (attendre son
   retour), avec seulement : les remarques telles que les sous-agents les ont écrites, le chemin
   du diff, les fichiers non suivis, le chemin de la spec, et les écarts déjà notés (journal du
   plan, bilans de vague). Ni justification des choix, ni résumé du travail. Garder son
   identifiant : la relecture des corrections le reprend (§8).
4. Reprendre son classement tel quel, en cinq groupes : « À corriger », « Option prudente »
   (un choix dont une option domine, que l'auteur applique), « À décider » (ce qui revient à
   l'utilisateur), « Écartée », « Déjà connu ». Ce qui va dans chacun est défini dans le fichier
   du juge, et nulle part ailleurs.

**Seul le juge écarte.** Désaccord avec un verdict : l'écrire à côté de la remarque, qui passe
dans « À décider » avec une recommandation et un choix par défaut ; ne jamais la reclasser soi-même. Le classement ne fusionne pas deux
remarques, ne réécrit pas leur texte et ne change pas leur axe. Ce que le juge a « vu en
vérifiant » (`V-n`, déjà classé par lui) s'ajoute à la suite, renuméroté en `R-n` suivants,
partout : vue groupée, rapport complet et relecture des corrections.

## 6. Rapporter

Le **rapport complet**, par axe, garde les extraits qui permettent de contester une remarque :

```markdown
## Spec

<le rapport du sous-agent, à peine nettoyé, avec R-n ;
ou « pas de spec : axe sauté »>

## Conventions

### Violations
<les écarts aux règles écrites>

### Jugements
<les odeurs possibles>

## Classement du juge

<son rendu, tel quel, ses V-n remplacés par leur R-n>
```

La **vue groupée** est ce que l'utilisateur lit d'abord : une ligne par remarque,
`R-n · spec|conv|bug · fichier:ligne · constat`, suivie de l'option et de son test dans « Option
prudente », des options, de la recommandation et du choix par défaut dans « À décider », et de la
preuve du juge dans « Écartée » et « Déjà connu ». Une remarque écartée reste visible, barrée,
pour que l'utilisateur puisse la contester. Les groupes vides sont omis ; l'ordre est celui-ci :

```markdown
**Relecture : <n> à corriger, <n> options prudentes, <n> à décider**, sur <n> remarques (spec <n>, conventions <n>, bugs <n>, vues par le juge <n>).

À corriger
- R-3 · spec · docs/plans/x.md:42 · le plan écrit --migrate, les fichiers compose écrivent migrate
Option prudente
- R-8 · bug · store/invoice.go:60 · INSERT validé après l'échéance, PDF supprimé · option : relire la ligne avant de supprimer le PDF · test : échéance dépassée après validation, le PDF reste
À décider
- R-6 · conv · mise.toml:12 · calcul de version écrit deux fois · options : le mettre en commun (lance git à chaque appel) / laisser · recommandée : laisser · sans avis de ta part : laisser
Écartée
- ~~R-4 · spec · mise.toml:20 · build affiche le chemin du binaire~~ : sortie seule, aucun appelant ne la lit (mise.toml:20)
Déjà connu
- R-1 · spec · mise.toml:41 · verify rouge (govulncheck) : déjà dans le journal

Pour les bugs : `/code-review`.
```

Dans l'en-tête, une part à zéro est omise. La dernière ligne n'apparaît que si aucun constat de
bug n'a été passé.
- **Appelé par `implement`** : lui rendre la main avec les deux, sans question ; il dit où les
  mettre et corrige.
- **Lancé seul** : afficher la vue groupée, puis le rapport complet en dessous, et poser la
  question.

## 7. Demander quoi corriger (lancé seul)

Toujours avec AskUserQuestion, sauf s'il n'y a aucune remarque (le dire, puis s'arrêter) :

- **« Que corriger ? »** : en premier le lot « À corriger » et « Option prudente », suivi de
  « (Recommandé) » ; puis « Rien, s'arrêter là ». Chaque option nomme ses `R-n`. S'il n'y a rien
  à corriger, « Rien » vient en premier, recommandé.
- **Une question par remarque « À décider »**, avec les options du juge, la recommandée en
  premier, suivie de « (Recommandé) ». Au-delà de 4 questions par appel, les suivantes vont dans un second appel.
- Les options listées seulement : l'outil ajoute de lui-même la réponse libre, qui permet aussi
  de reprendre une remarque écartée.

Puis proposer la suite, sans la lancer :

- quelques corrections locales : les faire ici, avec `tdd` si un comportement change, puis la
  relecture des corrections (§8) ;
- un manque de spec ou un vrai chantier : `/plan` à partir des remarques gardées, en continuant
  dans cette conversation, qui en est la source.

## 8. Relire les corrections

Après les corrections (par `implement`, ou ici sur demande) :

1. Écrire le diff des corrections seules de la même façon,
   `git diff <base> --output=<dossier git>/review-fixes-<tour>.patch`, où `<base>` est le commit
   d'avant la première correction. **Sans commit** : `<base>` est un instantané du travail noté
   avant la première correction, `git stash create` (il ne touche à rien ; vide s'il n'y a rien à
   garder : prendre `HEAD`). Les fichiers non suivis que les corrections touchent se donnent par
   leur chemin, et le juge les relit.
2. Reprendre le juge avec `SendMessage` et son identifiant, en lui donnant ce chemin, la
   correspondance de ses `V-n` renumérotés (`V-1 = R-27`) et, pour chaque remarque « À corriger »
   ou « Option prudente », le commit qui la corrige (sans commit : les fichiers touchés) ou la
   contestation de l'auteur (par exemple un test qui ne peut pas échouer). Si la reprise échoue,
   lancer un nouveau `review-judge` avec son premier classement en plus.
3. Ce qu'il marque **non réglé**, et ce qu'une correction introduit et qu'il classe « À
   corriger » ou « Option prudente », se corrige ou s'applique à nouveau, puis un second tour.
   **Deux tours au maximum** : ce qui reste ouvert passe dans « À décider », avec la raison, une
   recommandation et un choix par défaut.
