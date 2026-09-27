---
name: tickets
description: Lire, créer et relier des tickets et des specs dans le gestionnaire du projet — fichiers locaux, GitHub Issues, GitLab Issues, Jira ou un autre outil décrit par l'utilisateur — et configurer ce gestionnaire (section « ## Tickets » du CLAUDE.md). Utilise ce skill dès que l'utilisateur veut créer, lire, lister ou fermer un ticket ou une issue, demande où sont ses tickets ou veut changer de gestionnaire ; et chaque fois qu'un autre skill (to-spec, to-tickets, implement) doit publier ou lire un ticket.
---

# Tickets

Ce skill est la seule source de vérité sur **où vivent les tickets d'un projet et comment on les
manipule**. Les autres skills l'appellent au lieu de deviner : ainsi, changer de gestionnaire ne
demande de modifier qu'un endroit.

## 1. Trouver la configuration

Chercher une section `## Tickets` dans le `CLAUDE.md` du projet (sinon dans `AGENTS.md`). Si elle
existe, l'appliquer telle quelle et passer à l'étape 3.

## 2. Configurer, la première fois

Si la section n'existe pas, **explorer avant de demander** :

- `git remote -v` : GitHub, GitLab (gitlab.com ou instance auto-hébergée) ou aucun remote ;
- des traces d'usage : `docs/tickets/`, `docs/specs/`, des références `PROJ-123` dans `git log`
  (signe de Jira), des issues existantes (`gh issue list --limit 5`, `glab issue list`).

Proposer ensuite **une** valeur par défaut, avec l'outil AskUserQuestion :

- remote GitHub → **GitHub Issues** ; remote GitLab → **GitLab Issues** ; sinon → **fichiers
  locaux** ;
- toujours offrir les autres : fichiers locaux, GitHub, GitLab, Jira. L'utilisateur peut aussi
  décrire un autre outil (option « Autre » de l'outil) : noter sa description telle quelle.

Pour Jira, demander aussi le site et la clé du projet. Pour « Autre », demander comment on crée,
lit et relie un ticket.

Écrire la section dans `CLAUDE.md` s'il existe, sinon dans `AGENTS.md` s'il existe. Si aucun des
deux n'existe, proposer de créer `CLAUDE.md` avec cette seule section. Montrer le bloc avant de
l'écrire. Formats :

```markdown
## Tickets

- Gestionnaire : fichiers locaux
- Specs : `docs/specs/<feature>.md`
- Tickets : `docs/tickets/<feature>/<NN>-<slug>.md`
```

```markdown
## Tickets

- Gestionnaire : GitHub Issues (`owner/repo`)
- Specs : ticket parent, label `spec` s'il existe
- Tickets : sous-issues de la spec
```

```markdown
## Tickets

- Gestionnaire : Jira (`https://exemple.atlassian.net`, projet `PROJ`)
- Specs : Epic
- Tickets : Story rattachée à l'Epic
```

Pour « Autre », écrire la description de l'utilisateur sous `- Gestionnaire :`, puis les règles
de création, de lecture et de lien qu'il a données.

## 3. Opérations

Le détail de chaque gestionnaire est dans `references/` : [local.md](references/local.md),
[github.md](references/github.md), [gitlab.md](references/gitlab.md),
[jira.md](references/jira.md). Lire uniquement celui du projet. Pour un gestionnaire « Autre »,
suivre la section du `CLAUDE.md`.

Les opérations dont les autres skills ont besoin :

- **Créer une spec** : un fichier dans `docs/specs/` en local, un ticket parent ailleurs.
- **Créer un ticket**, avec son parent (la spec, s'il y en a une) et les tickets qui le bloquent.
- **Lire un ticket** : corps, commentaires, statut, parent et bloquants.
- **Lister les tickets ouverts**, par exemple pour repérer un doublon avant d'en créer un.
- **Marquer un ticket terminé.**

Règles communes :

- **Publier dans l'ordre des dépendances** (bloquants d'abord), pour que chaque ticket puisse
  citer l'identifiant réel de ceux qui le bloquent.
- **Toujours écrire les dépendances en clair dans le corps** (« Bloqué par : #12 »), même quand
  le gestionnaire a des liens natifs : si la création du lien échoue, l'information reste.
- **Pas de chemins de fichiers ni d'extraits de code** dans les tickets : ils vieillissent vite.
  Seule exception : un extrait qui fixe une décision mieux que la prose (schéma, type, machine à
  états).
- Réutiliser les labels ou types existants ; ne pas en créer sans le dire.

## Ce que ce skill ne fait jamais

- Publier sur un gestionnaire distant (GitHub, GitLab, Jira, autre) sans avoir montré le contenu
  et obtenu un accord explicite. Un ticket publié est vu par d'autres, même supprimé ensuite.
- Fermer, supprimer ou modifier un ticket distant sans feu vert.
- Changer de gestionnaire sans demander.
