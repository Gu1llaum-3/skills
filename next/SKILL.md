---
name: next
description: "Quel skill lancer maintenant ? Lit la conversation, ou l'état du projet si elle est vide, et recommande le skill suivant avec la commande exacte, une ou deux autres options, et s'il faut continuer ici ou repartir d'une session vide."
argument-hint: "[ta situation]"
disable-model-invocation: true
---

# Next : quel skill lancer ensuite

L'utilisateur ne retient pas tous ses skills, et une conversation menée sans skill finit souvent
par « je te fais un plan ? » au lieu de passer par son parcours. Ce skill lit où on en est et
dit quel skill lancer. Il **propose, il ne lance rien**, et ne fait pas le travail du skill
recommandé (pas d'entretien, pas de plan).

Réponds dans la langue de l'utilisateur.

## 1. Lire la situation

**La conversation d'abord**, et l'argument s'il y en a un. Relever :

- **le sujet** : un nouveau projet, une fonctionnalité, un bug, un ticket, un doute technique,
  un mot flou, une question pour quelqu'un d'autre ;
- **ce qui est tranché** : un besoin clair, des décisions, un périmètre, ou seulement des
  problèmes décrits et des pistes ;
- **ce qui est écrit** : un fichier créé (cahier des charges, spec, plan, ticket, POC) ;
- **ce qui a été proposé** : si Claude a proposé « un plan » ou « de coder » hors skill, juger
  sur le fond. Rien de tranché : `/feature`. Tout tranché : `/plan`.

**Si la conversation est vide** (début de session, juste après `/clear`), lire l'état du projet :

- `docs/plans/`, d'après la ligne `> Statut :` :
  - `validé par …` avec des cases `- [ ]` → le reprendre avec `implement`, en citant la vague et
    la première tâche non cochée ;
  - `à valider` → s'il porte une question `[Métier : …, bloquante]`, le plan attend la réponse à
    son questionnaire ; sinon, le faire valider ;
  - `terminé le …` d'origine POC, alors que le POC n'a pas de verdict → `/poc <fichier>` ;
- `docs/questionnaires/` : `> Statut : envoyé le …` → la réponse est-elle revenue ? Si oui,
  `to-questionnaire` la réintègre ; sinon, le travail qui en dépend attend ;
- `docs/tickets/` : un ticket `en cours` → le reprendre ; sinon un ticket `prêt` dont les
  bloquants sont `terminé` ;
- `ROADMAP.md` (ou les jalons du gestionnaire, avec `tickets`) : le premier jalon qui a des
  lignes non cochées, ou aucune ligne. Sans ligne, son envergure dans le cahier des charges
  décide : « simple » → `plan` du jalon ; « gros » → `to-spec` du jalon. Un cahier des charges
  sans roadmap → la créer avec `tickets` ;
- `docs/poc/` : `> Statut : en cours` → reprendre ; `terminé` avec un verdict qui n'a pas encore
  de suite → la proposer.

Ne citer que ce qui a été lu. S'il n'y a rien, ni dans la conversation ni dans le projet, poser
une seule question en texte : « Qu'est-ce que tu veux faire ? », puis orienter avec la réponse.

## 2. La carte

| Situation | Skill |
|---|---|
| Pas encore de projet, une idée de produit | `/brainstorming` |
| Une idée dont on ne sait pas si elle tient, sur une seule question | `/poc` |
| Une idée de fonctionnalité, ou des problèmes discutés sans rien trancher | `/feature` |
| Tout est décidé dans la conversation, ça tient en une session | `/plan` |
| Tout est décidé, mais pour plus tard ou trop gros pour une session | `/to-spec` |
| Une spec ou un cahier des charges à découper en tickets | `/to-tickets` |
| Un ticket (des skills, d'une PO, d'un client) à analyser avant de coder | `/plan <ticket>` |
| Un plan validé, ou un ticket à attaquer directement | `/implement <plan ou ticket>` |
| Un bug dont la cause est connue | `/tdd` |
| Un bug qui résiste | `/plan` (tâche de localisation d'abord) |
| Des tests à écrire ou à réécrire | `/tdd` |
| Se faire challenger sur une idée ou un plan | `/interview` |
| Un mot flou, deux mots pour la même chose | `/domain-modeling` |
| Une question que seul le métier, un client ou une PO peut trancher, ou sa réponse revenue | `/to-questionnaire` |
| Un point à vérifier sur le web, une bibliothèque à choisir | `/research` |
| Une décision d'architecture à noter | `/adr` |
| L'identité visuelle, avant de coder l'interface | `/design` |
| Un nom à trouver | `/naming` |
| Un projet existant sans `CLAUDE.md`, ou avec un `CLAUDE.md` douteux | `/onboard` |
| Voir la roadmap, lire ou ranger des tickets | `/tickets` |
| Le dernier message n'est pas compris | `/wtf` |

Le parcours principal : `/brainstorming` ou `/feature` → `/plan` → `/implement` (qui écrit le
code avec `tdd`). Pour un gros travail, `/to-spec` → `/to-tickets` → un `/implement` par
ticket. `interview`, `research`, `adr` et `to-questionnaire` se glissent en cours de route.

**Ce que la carte ne couvre pas** (aucun skill ne diagnostique un bug qui résiste, par exemple) :
le dire en une ligne, puis proposer ce qui s'en approche le plus. Ne recommander que des skills
présents dans la liste de la session ; un skill de la carte absent se signale (« lance
`./install.sh` dans le dépôt de skills »).

## 3. Répondre

Court, dans cet ordre :

```markdown
**Lance `/<skill>`** : <pourquoi, en une ligne tirée de la conversation ou du projet>.

    /<skill> <arguments : chemin du plan, numéro du ticket, jalon…>

Sinon :
- `/<autre>` si <ce qui le ferait préférer>.

Session : <continuer ici | /clear puis la commande>, parce que <raison>.
```

- **Une ou deux** autres options au plus, chacune avec sa condition. Aucune si la situation est
  sans ambiguïté.
- **La commande exacte** : avec le chemin, le ticket ou le jalon quand on les connaît.
- **La ligne de session** :
  - **continuer ici** quand le skill suivant a besoin de cette discussion comme source
    (`/feature`, `/plan` ou `/to-spec` juste après un échange) : un résumé perdrait le pourquoi ;
  - **`/clear` puis la commande** quand le skill suivant part d'un fichier qui se suffit (un plan
    validé, un ticket) et que la conversation ne sert plus ;
  - si la conversation est longue et encore utile : **`/compact` avec une consigne**
    (« `/compact` on passe au plan de l'export ») avant la commande.

## Ce que ce skill ne fait jamais

- Lancer le skill recommandé : l'utilisateur tape la commande.
- Commencer le travail du skill suivant : questions de cadrage, plan, code.
- Recommander un skill qui n'existe pas, ou citer un fichier qu'il n'a pas lu.
- Donner plus de trois options : au-delà, l'utilisateur n'est pas plus avancé qu'avant.
