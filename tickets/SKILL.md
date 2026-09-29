---
name: tickets
description: "Lire, créer, commenter, fermer et relier des tickets, des specs et les jalons de la roadmap dans le gestionnaire du projet (fichiers locaux avec ROADMAP.md, GitHub, GitLab, Jira ou autre), et configurer ce gestionnaire (section Tickets du CLAUDE.md). Utilise ce skill quand l'utilisateur veut agir sur un ticket ou une issue, voir où en est la roadmap, rattacher un ticket à un jalon, savoir où vivent ses tickets ou changer de gestionnaire."
---

# Tickets

Ce skill est la seule source de vérité sur **où vivent les tickets d'un projet, leurs jalons, et
comment on les manipule**. Les autres skills l'appellent au lieu de deviner : ainsi, changer de gestionnaire ne
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
- Jalons : `ROADMAP.md`
```

```markdown
## Tickets

- Gestionnaire : GitHub Issues (`owner/repo`)
- Specs : ticket parent, label `spec` s'il existe
- Tickets : sous-issues de la spec
- Jalons : milestones
```

```markdown
## Tickets

- Gestionnaire : Jira (`https://exemple.atlassian.net`, projet `PROJ`)
- Specs : Epic
- Tickets : Story rattachée à l'Epic
- Jalons : versions (Fix Version)
```

Pour GitLab, le bloc est celui de GitHub avec `GitLab Issues` et des milestones. Sur Jira, les
jalons sont des versions et pas des Epics : les Epics portent déjà les specs.

Pour « Autre », écrire la description de l'utilisateur sous `- Gestionnaire :`, puis les règles
de création, de lecture, de lien et de jalons qu'il a données.

**Section existante sans ligne `Jalons`** (projet configuré avant) : la première fois qu'un jalon
est nécessaire, proposer la valeur par défaut du gestionnaire et l'ajouter après accord.

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
- **Commenter un ticket**, par exemple pour poser des questions à celui qui l'a écrit.
- **Marquer un ticket terminé.**
- **Créer les jalons**, d'après le découpage en jalons du cahier des charges.
- **Rattacher un ticket à un jalon**, ou le laisser hors jalon (« plus tard »). Le plan d'un
  jalon sans tickets (projet « simple ») s'y rattache en local ; ailleurs, le jalon reste vide.
- **Marquer un jalon réalisé** : en local, il l'est quand toutes ses lignes sont cochées ;
  ailleurs, fermer le milestone ou publier la version, après accord.
- **Montrer la roadmap** : les jalons dans l'ordre, et pour chacun ses tickets et leur statut.

Règles communes :

- **Publier dans l'ordre des dépendances** (bloquants d'abord), pour que chaque ticket puisse
  citer l'identifiant réel de ceux qui le bloquent.
- **Toujours écrire les dépendances en clair dans le corps** (« Bloqué par : #12 »), même quand
  le gestionnaire a des liens natifs : si la création du lien échoue, l'information reste.
- **Pas de chemins de fichiers ni d'extraits de code** dans les tickets : ils vieillissent vite.
  Seule exception : un extrait qui fixe une décision mieux que la prose (schéma, type, machine à
  états).
- Réutiliser les labels ou types existants ; ne pas en créer sans le dire.
- **Sur un gestionnaire distant** (GitHub, GitLab, Jira, autre), publier, fermer, commenter ou
  modifier un ticket seulement après avoir montré le contenu et obtenu un accord explicite : un
  ticket publié est vu par d'autres, même supprimé ensuite. Réorganiser la roadmap ou changer de
  gestionnaire se propose de même avant de se faire.
- **Les jalons viennent du cahier des charges** (section « Découpage en jalons ») : reprendre
  leur nom et leur objectif, sans recopier le reste du document. Un jalon ajouté, renommé ou
  réordonné se propose, il ne se fait pas en silence.

## Reconnaître un ticket écrit par ces skills

Un ticket créé par `to-spec` ou `to-tickets` suit les modèles de `references/` et contient
toujours ces trois sections :

- **À livrer** ;
- **Critères d'acceptation**, numérotés `AC-1`, `AC-2`… ;
- **Interfaces à tester**.

`plan` s'en sert pour savoir si un ticket a déjà été cadré avec le code sous les yeux ou s'il
vient d'ailleurs (produit, client, bug remonté). Si un modèle de ticket change, garder cette
liste à jour.
