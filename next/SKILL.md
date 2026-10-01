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
| Une branche ou un travail à relire contre sa spec et les conventions | `/review` |
| Des bugs à chercher dans un diff | `/code-review` |
| Un bug dont la cause est connue | `/tdd` |
| Un bug qui résiste : intermittent, régression, cause introuvable | `/debug` |
| Des tests à écrire ou à réécrire | `/tdd` |
| Se faire challenger sur une idée ou un plan | `/interview` |
| Un mot flou, deux mots pour la même chose | `/domain-modeling` |
| Une question que seul le métier, un client ou une PO peut trancher, ou sa réponse revenue | `/to-questionnaire` |
| Un point à vérifier sur le web, une bibliothèque à choisir | `/research` |
| Une décision d'architecture à noter | `/adr` |
| Des étapes que toi seul peux faire : un compte à créer, des secrets à poser, un tableau de bord | `/wizard` |
| L'identité visuelle, avant de coder l'interface | `/design` |
| Un nom à trouver | `/naming` |
| Un projet existant sans `CLAUDE.md`, ou avec un `CLAUDE.md` douteux | `/onboard` |
| Des versions à vérifier : failles, fins de vie, paquets en retard ou abandonnés | `/upgrade` |
| Empêcher Claude de pousser ou d'effacer du travail git | `/git-guardrails` |
| Une session laborieuse : Claude a cherché longtemps, fait une erreur qu'un outil aurait vue | `/retro` |
| Un code difficile à changer ou à tester, sans bug ni fonctionnalité en vue | `/architecture` |
| Voir la roadmap, lire ou ranger des tickets | `/tickets` |
| Le dernier message n'est pas compris | `/wtf` |

Le parcours principal : `/brainstorming` ou `/feature` → `/plan` → `/implement` (qui écrit le
code avec `tdd`). Pour un gros travail, `/to-spec` → `/to-tickets` → un `/implement` par
ticket. `interview`, `research`, `adr` et `to-questionnaire` se glissent en cours de route.

**Ce que la carte ne couvre pas** : le dire en une ligne, puis proposer ce qui s'en approche le plus. Ne
recommander que des skills présents dans la liste de la session ; un skill de la carte absent se
signale (« lance `./install.sh` dans le dépôt de skills »).

## 3. Répondre

Court, dans cet ordre :

```markdown
**Lance `/<skill>`** : <pourquoi, en une ligne tirée de la conversation ou du projet>.

    /<skill> <arguments : chemin du plan, numéro du ticket, jalon…>

Sinon :
- `/<autre>` si <ce qui le ferait préférer>.

Session : <un geste de la section 4>, parce que <raison>.
```

- **Une ou deux** autres options au plus, chacune avec sa condition. Aucune si la situation est
  sans ambiguïté.
- **La commande exacte** : avec le chemin, le ticket ou le jalon quand on les connaît.
- **La ligne de session** : un seul geste, choisi avec la section 4.

## 4. La ligne de session

**À la fin d'une phase** (un cadrage fini, un plan validé, une vague ou un ticket terminés),
suivre cet arbre dans l'ordre ; la première réponse « oui » l'emporte :

1. **Continuer ici** : la suite a besoin de cette conversation comme source et elle n'est pas
   très longue. C'est à examiner en premier : tout autre geste remplace la conversation par un
   résumé, qui perd le pourquoi. Un cadrage reste ainsi dans la même conversation jusqu'aux
   tickets, pour que la spec et le découpage partent de la même réflexion ; chaque
   `/implement <ticket>` repart ensuite d'une session vide (branche 2).
2. **`/clear` puis la commande** : plus rien de la conversation ne sert, la suite part d'un
   fichier qui se suffit (un plan validé, un ticket).
3. **`/to-spec` d'abord** : le travail doit voyager (vers une autre session, un autre dossier,
   un autre outil, un collègue) alors que ce qui est décidé n'est encore écrit nulle part : il en
   fait une spec ou un ticket qui se suffit. Si la recommandation est déjà `/to-spec`, la ligne
   de session dit seulement de continuer ici.
4. **Un sous-agent** : la suite est une tâche bien bornée qui peut tourner sans l'utilisateur et
   qu'aucun skill ne prend déjà en charge (`research` et `review` lancent les leurs) ; la session
   reste intacte.
5. Sinon, **`/compact` avec une consigne** qui dit ce que la suite doit garder
   (« `/compact` on passe au plan de l'export »).

**Au milieu d'une phase** (en pleine vague, en plein entretien), la session se décide à la fin
de la phase : d'ici là, continuer ici, ou confier un morceau bien borné à un sous-agent, pour
garder le fil.
