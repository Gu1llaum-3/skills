---
name: plan
description: "Rédiger le plan d'implémentation (vagues, tâches à cocher, critères d'acceptation, interfaces à tester) d'un ticket, d'une spec, d'un jalon du cahier des charges, d'un POC ou d'une feature cadrée, après l'avoir confronté au code ; un ticket écrit hors de ces skills est challengé. Utilise ce skill quand l'utilisateur veut planifier, préparer ou analyser un travail avant de coder (« prépare le plan du ticket 42 », « analyse ce ticket de la PO », « fais le plan du jalon 1 »)."
argument-hint: "[ticket | spec | cahier des charges | POC]"
---

# Plan

Un ticket ou une spec disent **quoi** construire ; le plan dit **dans quel ordre, en quelles
tâches, et comment on prouvera chaque critère**, pour qu'`implement` puisse l'exécuter sans la
conversation sous les yeux. Entre l'écriture du ticket et aujourd'hui, le code a pu changer : ce
skill vérifie la source avant de s'y fier, et le dit quand elle est fausse. Il écrit le plan ; le
code s'écrit ensuite avec `implement`.

## 1. Lire la source

- **Ticket** (`#42`, une URL, `PROJ-123`, un fichier de `docs/tickets/`) : appeler le Skill tool
  avec « tickets » pour le lire, commentaires et spec parente compris. Si des bloquants ne sont
  pas terminés, le signaler : le plan peut s'écrire, mais `implement` refusera de démarrer.
  Établir ensuite sa provenance, **cadré** ou **externe**, qui règle la suite de la revue :
  [references/origin.md](references/origin.md).
- **Spec** ou **cahier des charges** : le lire en entier. Pour un cahier des charges, planifier
  un seul jalon à la fois : celui que l'utilisateur désigne, sinon le premier non réalisé de la
  roadmap (skill `tickets`).
- **POC** (`docs/poc/<slug>.md`, appel depuis `/poc`) : un plan court, une seule vague si
  possible, avec `> Branche : poc/<slug>`. Chaque tâche prévoit l'essai ou le test ciblé qui
  tranche l'hypothèse, sans TDD complet : le but est de répondre à la question du POC, pas de
  livrer.
- **Conversation** (appel depuis `feature`, depuis `architecture`, ou depuis `brainstorming` pour
  un petit outil) : la synthèse qui vient d'être validée.
- **Reprise** : si un plan de `docs/plans/` cite déjà cette source et a des cases non cochées, ne
  pas en écrire un autre : le dire et proposer de reprendre avec `implement`.

Lire aussi `CLAUDE.md`, `GLOSSARY.md` s'il existe (le plan nomme les notions avec ses termes),
les ADR (`docs/adr/`) et `docs/design/DESIGN.md` s'il y a de l'interface (ou `DESIGN.md` à la
racine dans les projets plus anciens).

## 2. Confronter au code et au monde

Si l'on vient de `feature`, ou de `brainstorming` pour un petit outil, dans la même conversation,
l'exploration et la recherche sont déjà faites : passer à l'étape 3. Sinon, d'abord le code, puis la décision de chercher.

**Toujours, un sous-agent d'exploration du code**, avec pour mission de rapporter :

- si l'état de départ décrit par la source est toujours vrai ;
- où brancher le travail, et ce qui existe déjà et peut servir ;
- **si le dépôt a déjà un modèle pour ce type de travail** (un autre formulaire, un autre appel
  d'API, un autre export), et où ;
- les interfaces publiques concernées et les tests voisins qui servent de modèle ;
- les refactorisations préalables qui rendraient le travail plus simple ;
- les risques : migration de données, impact sur d'autres modules, sécurité.

**Puis la recherche, si le code ne suffit pas** à savoir comment faire proprement. Appeler le
Skill tool avec « research » dès qu'un de ces signaux apparaît, quelle que soit la provenance :

- **première fois dans le dépôt** : aucun modèle existant (premier upload, premier temps réel,
  premier paiement) ;
- **plusieurs approches valables**, et le code ne tranche pas entre elles ;
- **une dépendance à choisir** ;
- **un domaine où l'erreur coûte cher** : sécurité, authentification, données personnelles,
  accessibilité, performance ;
- **une API externe ou une version récente**, dont le comportement a pu changer ;
- **un modèle existant douteux** (API dépréciée, contournement) : le copier propagerait le
  problème.

Sinon, le dire en une ligne en citant le modèle trouvé (« pas de recherche : le dépôt fait déjà
ça dans <module> »), pour que l'utilisateur puisse demander de chercher quand même. La recherche
tourne en arrière-plan : commencer l'étape 3 sans l'attendre, et compléter quand elle revient.

**Bug** : l'exploration cherche aussi la cause. Si elle n'est pas trouvée, appeler le Skill tool
avec « debug » : il la diagnostique, et corrige lui-même si le correctif tient en une tâche (le
plan n'a alors plus lieu d'être). Sinon, le plan part de son diagnostic.

## 3. Restituer, de façon critique

En un message court. Pour un ticket **externe**, commencer par le besoin : quel problème le
ticket résout, et si la solution demandée est la bonne réponse à ce problème, vu le code et la
recherche.

- ✅ ce qui est prêt : critères clairs, état de départ confirmé, briques réutilisables ;
- ⚠️ ce qui ne va pas, concrètement : un critère manquant ou invérifiable, une contradiction avec
  le code, une dépendance oubliée, une décision passée (ADR) ignorée ;
- 💡 les idées issues de la recherche ou du code, présentées comme des **propositions** ;
- **un verdict** :
  - **prêt** : on planifie ;
  - **à ajuster** : quelques points à trancher, on les tranche à l'étape 4 ;
  - **trop gros** : il ne tient pas en une session (critère « Taille » de
    [`to-tickets`](../to-tickets/SKILL.md)) ; proposer de le redécouper avec `to-tickets`, puis
    de fermer le ticket d'origine avec un lien vers les nouveaux, via le skill `tickets`. Si la
    source est un cahier des charges, proposer `to-spec` d'abord, et corriger le verdict
    d'envergure du cahier des charges (« gros ») pour que la prochaine session ne le rejoue pas ;
  - **à revoir** : le besoin lui-même n'est pas clair. Ticket cadré : proposer de relancer
    `/feature`. Ticket externe : les questions vont à celui qui l'a écrit (étape 6).

## 4. Trancher

Pour les points ouverts, appeler le Skill tool avec « interview » :

- **source cadrée** (ticket de ces skills, spec, juste après `feature`) : une ou deux séries au
  maximum. Le travail a déjà été discuté, on ne rouvre que ce qui l'exige ;
- **ticket externe** : sans plafond de séries, en commençant par le besoin. `interview` repère
  ce qui ne peut être tranché que par l'auteur du ticket ou le métier : c'est noté pour le
  questionnaire de l'étape 6, pas deviné.

Les questions pour le métier qui restent, déjà dans la source ou issues de l'entretien :
**bloquantes**, elles vont dans la section « Questions ouvertes » du plan avec le lien vers leur
questionnaire, et empêchent de le valider ; **non bloquantes**, elles y vont avec l'hypothèse
qu'il applique.

Si une proposition est acceptée et change le contenu du ticket, proposer de mettre le ticket à
jour avec le skill `tickets`, pour qu'il reste la référence. Une décision qui coche les trois
critères d'un ADR se propose via le skill `adr`.

## 5. Rédiger

Écrire le plan dans le dossier de plans du dépôt (par défaut `docs/plans/<slug>.md`), en suivant
[references/plan.md](references/plan.md). Le plan ne contient que ce que la source et les
décisions de l'étape 4 demandent : un ajout se propose, il ne s'y glisse pas.

**Bug** : la première tâche est un test qui reproduit le bug et échoue, à partir du cas réduit
par `debug` s'il est passé par là. Le test reste ensuite comme test de non-régression.

**Faire relire le plan** (sauf plan d'origine POC), avant de le montrer : `implement` le suivra à
la lettre, et une erreur coûte moins cher ici que dans le code. L'exploration de l'étape 2
renseignait la rédaction ; cette relecture vérifie ce que le plan affirme une fois écrit. Un
sous-agent `general-purpose` au contexte vierge (pas `Explore`, qui lit par extraits ; jamais un
fork, qui hérite de la conversation). Lui donner le chemin du plan et de quoi lire la source
lui-même (son chemin, la commande qui affiche le ticket, ou son texte collé tel quel ; rien si
c'est la conversation), avec ce brief et rien d'autre :

> Lis en entier <plan>, puis <source>, puis le code que le plan touche. Rapporte, chaque point
> avec sa preuve (ligne du plan, ligne de la source, `fichier:ligne` du code) : (1) un critère de
> la source absent des critères du plan, un `AC-n` qu'aucune tâche ne cite, ou un `AC-n`
> qu'aucune interface à tester ne vérifie ; (2) une affirmation sur le code qui est fausse : un fichier, une
> fonction, un modèle à reprendre qui n'existe pas ou ne fait pas ce que le plan dit ; (3) un
> oubli évident parmi ce que les tâches touchent (migration, types, routes, configuration,
> tests, documentation) ; (4) une tâche que la source ne demande pas, ou que son hors périmètre
> exclut ; (5) un risque non traité (données existantes, compatibilité, sécurité) ; (6) un plan
> qui ne tient visiblement pas en une session. Ne réécris pas le plan. Commence par une ligne
> `VERDICT : PRÊT | À AMENDER | À REDÉCOUPER`. Une catégorie sans problème se dit vide. Moins
> de 400 mots.

Vérifier chaque point dans le code ou la source avant de s'en servir : un retour est une
hypothèse. Corriger le plan pour ce qui est fondé ; ce qui demande une décision de l'utilisateur
se pose à l'étape 6. **À REDÉCOUPER**, s'il est confirmé, mène au verdict « trop gros » de
l'étape 3.

## 6. Valider et passer la main

Montrer le plan et demander le feu vert, avec en quelques lignes le verdict de la relecture, ce
qu'elle a fait corriger et les points écartés avec leur raison. Une fois l'accord obtenu, passer
la ligne de statut à `> Statut : validé par <nom> le <JJ/MM/AAAA>`. Le plan d'un jalon sans
tickets se rattache ensuite à ce jalon avec le skill `tickets`. Le plan n'est pas commité ici :
`implement` le commite avec la première tâche, sur sa branche.

**Questions pour le métier ou pour l'auteur du ticket** : appeler le Skill tool avec
« to-questionnaire ». Pour un ticket externe, le questionnaire porte aussi les réserves sur la
solution demandée et les choix faits à la place de l'auteur, et se publie en commentaire du
ticket après accord sur le texte exact. **S'il reste une question bloquante**, ne pas demander
la validation : le plan reste « à valider » jusqu'à la réponse, et on le reprend avec le
questionnaire rempli.

- Appelé par `implement` : lui rendre la main avec le chemin du plan.
- Sinon : proposer de lancer l'implémentation, et sur accord appeler le Skill tool avec
  « implement » en lui donnant le chemin du plan.
