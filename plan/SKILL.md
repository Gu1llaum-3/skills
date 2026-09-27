---
name: plan
description: Rédiger le plan d'implémentation (vagues, tâches à cocher, critères d'acceptation, interfaces à tester) d'un ticket — fichier local, issue GitHub ou GitLab, Jira — d'une spec, d'un jalon de cahier des charges ou d'une feature qui vient d'être cadrée. Avant d'écrire, le skill confronte la source au code actuel et, si un choix technique reste ouvert, fait une recherche ; il signale ce qui est faux, manquant ou trop gros. Le plan est ensuite exécuté par implement. Utilise ce skill quand l'utilisateur veut planifier ou préparer un ticket (« prépare le plan du ticket 42 », « planifie PROJ-123 », « fais le plan du jalon 1 »), et chaque fois que feature, brainstorming ou implement demandent un plan.
argument-hint: "[ticket | spec | cahier des charges]"
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
- **Conversation** (appel depuis `feature`) : la synthèse qui vient d'être validée.
- **Reprise** : si un plan de `docs/plans/` cite déjà cette source et a des cases non cochées, ne
  pas en écrire un autre : le dire et proposer de reprendre avec `implement`.

Lire aussi `CLAUDE.md`, les ADR (`docs/adr/`) et `docs/design/DESIGN.md` s'il y a de
l'interface (ou `DESIGN.md` à la racine dans les projets plus anciens).

## 2. Confronter au code et au monde

Si l'on vient de `feature` dans la même conversation, l'exploration et la recherche sont déjà
faites : passer à l'étape 3. Sinon, lancer **dans le même message** :

- **Toujours, un sous-agent d'exploration du code**, avec pour mission de rapporter :
  - si l'état de départ décrit par la source est toujours vrai ;
  - où brancher le travail, et ce qui existe déjà et peut servir ;
  - les interfaces publiques concernées et les tests voisins qui servent de modèle ;
  - les refactorisations préalables qui rendraient le travail plus simple ;
  - les risques : migration de données, impact sur d'autres modules, sécurité.
- **Seulement si un choix technique reste ouvert** (bibliothèque, approche, domaine pointu que
  la source ne tranche pas) : appeler le Skill tool avec « research ». Sinon, le dire en une
  ligne (« pas de recherche : rien d'ouvert ») et ne rien lancer.

## 3. Restituer, de façon critique

En un message court :

- ✅ ce qui est prêt : critères clairs, état de départ confirmé, briques réutilisables ;
- ⚠️ ce qui ne va pas, concrètement : un critère manquant ou invérifiable, une contradiction avec
  le code, une dépendance oubliée, une décision passée (ADR) ignorée ;
- 💡 les idées issues de la recherche ou du code, présentées comme des **propositions** ;
- **un verdict** :
  - **prêt** : on planifie ;
  - **à ajuster** : quelques points à trancher, on les tranche à l'étape 4 ;
  - **trop gros** : il ne tient pas en une session ; proposer de le redécouper avec
    `to-tickets` ;
  - **à revoir** : le besoin lui-même n'est pas clair ; proposer de repasser par `feature`.

## 4. Trancher

Pour les points ouverts, appeler le Skill tool avec « interview », en une ou deux séries au
maximum : le ticket a déjà été discuté, on ne rouvre que ce qui l'exige.

Si une proposition est acceptée et change le contenu du ticket, proposer de mettre le ticket à
jour avec le skill `tickets`, pour qu'il reste la référence. Une décision qui coche les trois
critères d'un ADR se propose via le skill `adr`.

## 5. Rédiger

Écrire le plan dans le dossier de plans du dépôt (par défaut `docs/plans/<slug>.md`), en suivant
[references/plan.md](references/plan.md). Le plan ne contient que ce que la source et les
décisions de l'étape 4 demandent : un ajout se propose, il ne s'y glisse pas.

## 6. Valider et passer la main

Montrer le plan et demander le feu vert. Une fois l'accord obtenu, remplacer « Statut : à
valider » par « Validé par <nom> le <JJ/MM/AAAA> ». Le plan n'est pas commité ici : `implement`
le commite avec la première tâche, sur sa branche.

- Appelé par `implement` : lui rendre la main avec le chemin du plan.
- Sinon : proposer de lancer l'implémentation, et sur accord appeler le Skill tool avec
  « implement » en lui donnant le chemin du plan.

## Ce que ce skill ne fait jamais

- Écrire un plan sans avoir confronté la source au code (sauf juste après `feature`).
- Modifier un ticket en silence, ou le publier sans accord.
- Ajouter au plan une tâche que ni la source ni l'utilisateur n'ont demandée.
- Écrire du code.
