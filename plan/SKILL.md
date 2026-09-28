---
name: plan
description: Rédiger le plan d'implémentation (vagues, tâches à cocher, critères d'acceptation, interfaces à tester) d'un ticket — fichier local, issue GitHub ou GitLab, Jira — d'une spec, d'un jalon de cahier des charges, d'un POC ou d'une feature qui vient d'être cadrée. Avant d'écrire, le skill confronte la source au code actuel, fait une recherche quand le code ne suffit pas à savoir comment faire proprement, et challenge le besoin d'un ticket écrit hors de ces skills (produit, client, bug remonté) ; il signale ce qui est faux, manquant ou trop gros. Le plan est ensuite exécuté par implement. Utilise ce skill quand l'utilisateur veut planifier, préparer ou analyser un ticket avant de coder (« prépare le plan du ticket 42 », « planifie PROJ-123 », « analyse ce ticket de la PO », « fais le plan du jalon 1 »), et chaque fois que feature, brainstorming ou implement demandent un plan.
argument-hint: "[ticket | spec | cahier des charges | POC]"
---

# Plan

Un ticket ou une spec disent **quoi** construire ; le plan dit **dans quel ordre, en quelles
tâches, et comment on prouvera chaque critère**, pour qu'`implement` puisse l'exécuter sans la
conversation sous les yeux. Entre l'écriture du ticket et aujourd'hui, le code a pu changer : ce
skill vérifie la source avant de s'y fier, et le dit quand elle est fausse.

Réponds dans la langue de l'utilisateur.

## 1. Lire la source

- **Ticket** (`#42`, une URL, `PROJ-123`, un fichier de `docs/tickets/`) : appeler le Skill tool
  avec « tickets » pour le lire, commentaires et spec parente compris. Si des bloquants ne sont
  pas terminés, le signaler : le plan peut s'écrire, mais `implement` refusera de démarrer.
- **Spec** ou **cahier des charges** : le lire en entier. Pour un cahier des charges, planifier
  un seul jalon à la fois : celui que l'utilisateur désigne, sinon le premier non réalisé.
- **POC** (`docs/poc/<slug>.md`, appel depuis `/poc`) : un plan court, une seule vague si
  possible, dont les tests portent sur l'hypothèse à valider. Le but est de répondre à la
  question du POC, pas de livrer.
- **Conversation** (appel depuis `feature`) : la synthèse qui vient d'être validée.
- **Reprise** : si un plan de `docs/plans/` cite déjà cette source et a des cases non cochées, ne
  pas en écrire un autre : le dire et proposer de reprendre avec `implement`.

Lire aussi `CLAUDE.md`, les ADR (`docs/adr/`) et `docs/design/DESIGN.md` s'il y a de
l'interface (ou `DESIGN.md` à la racine dans les projets plus anciens).

### Provenance d'un ticket

Un ticket écrit par `to-spec` ou `to-tickets` a été cadré avec le code sous les yeux ; un ticket
écrit ailleurs (product owner, client, bug remonté) décrit souvent bien le besoin, mais pas
comment l'implémenter proprement, et sa solution n'a pas été discutée par des devs. Le skill
[`tickets`](../tickets/SKILL.md) liste les sections qui signent un ticket de ces skills
(« Reconnaître un ticket écrit par ces skills ») :

- **toutes présentes** : ticket **cadré**, revue normale ;
- **aucune** : ticket **externe**, revue poussée (étapes 3, 4 et 6) ;
- **en partie** : demander en une ligne d'où vient le ticket, plutôt que deviner.

Lire aussi les commentaires et, si le gestionnaire le permet, l'historique : un ticket cadré
dont le périmètre ou un critère a été changé ensuite par quelqu'un d'autre est traité comme
externe **pour ce point-là**.

## 2. Confronter au code et au monde

Si l'on vient de `feature` dans la même conversation, l'exploration et la recherche sont déjà
faites : passer à l'étape 3. Sinon, d'abord le code, puis la décision de chercher.

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

**Bug** : l'exploration cherche aussi la cause. Si elle n'est pas trouvée, le dire : le plan
commencera par la reproduire et la localiser.

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
    [`to-tickets`](../to-tickets/SKILL.md)) ; proposer de le redécouper avec `to-tickets`. Si la
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
**bloquantes**, elles empêchent de valider le plan ; **non bloquantes**, elles vont dans la
section « Questions ouvertes » du plan avec l'hypothèse qu'il applique.

Si une proposition est acceptée et change le contenu du ticket, proposer de mettre le ticket à
jour avec le skill `tickets`, pour qu'il reste la référence. Une décision qui coche les trois
critères d'un ADR se propose via le skill `adr`.

## 5. Rédiger

Écrire le plan dans le dossier de plans du dépôt (par défaut `docs/plans/<slug>.md`), en suivant
[references/plan.md](references/plan.md). Le plan ne contient que ce que la source et les
décisions de l'étape 4 demandent : un ajout se propose, il ne s'y glisse pas.

**Bug** : la première tâche est un test qui reproduit le bug et échoue. Si la cause n'est pas
connue, une tâche de localisation la précède : réduire le cas, formuler des hypothèses, les
vérifier une à une. Le test reste ensuite comme test de non-régression.

## 6. Valider et passer la main

Montrer le plan et demander le feu vert. Une fois l'accord obtenu, remplacer « Statut : à
valider » par « Validé par <nom> le <JJ/MM/AAAA> ». Le plan n'est pas commité ici : `implement`
le commite avec la première tâche, sur sa branche.

**Questions pour le métier ou pour l'auteur du ticket** : appeler le Skill tool avec
« to-questionnaire ». Pour un ticket externe, le questionnaire porte aussi les réserves sur la
solution demandée et les choix faits à la place de l'auteur, et se publie en commentaire du
ticket après accord sur le texte exact. **S'il reste une question bloquante**, ne pas demander
la validation : le plan reste « à valider » jusqu'à la réponse, et on le reprend avec le
questionnaire rempli.

- Appelé par `implement` : lui rendre la main avec le chemin du plan.
- Sinon : proposer de lancer l'implémentation, et sur accord appeler le Skill tool avec
  « implement » en lui donnant le chemin du plan.

## Ce que ce skill ne fait jamais

- Écrire un plan sans avoir confronté la source au code (sauf juste après `feature`).
- Modifier ou commenter un ticket en silence, ou le publier sans accord.
- Ajouter au plan une tâche que ni la source ni l'utilisateur n'ont demandée.
- Écrire du code.
