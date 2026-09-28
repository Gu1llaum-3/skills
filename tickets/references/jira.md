# Jira

Jira passe par le **connecteur Atlassian** de Claude. Si ses outils n'apparaissent que sous forme
`authenticate`, lancer l'authentification et laisser l'utilisateur la terminer, puis recharger les
outils. Les noms exacts des outils dépendent du connecteur : chercher ceux qui créent, lisent,
recherchent (JQL), relient et font transiter des issues Jira.

Le site et la clé du projet viennent de la section `## Tickets`. Au premier usage, récupérer les
types d'issue disponibles du projet : ils varient d'une instance à l'autre (Epic, Story, Task,
Bug, parfois en français).

## Créer

- **Spec** : une issue de type **Epic** (ou le type indiqué dans `## Tickets`), avec le contenu de
  la spec.
- **Ticket** : une **Story** (ou **Task**) dont le parent est l'Epic de la spec. Corps : À livrer,
  Critères d'acceptation, Interfaces à tester, Bloqué par, avec les clés Jira (`PROJ-123`).

## Relier

- Parent : le champ parent de l'issue (l'Epic).
- Blocage : un lien de type **Blocks** (« is blocked by » côté ticket bloqué), si le connecteur
  sait créer des liens. Sinon, s'en tenir au texte du corps et le signaler.

## Jalons (versions)

Les jalons sont des **versions** du projet (champ Fix Version), pas des Epics : les Epics portent
déjà les specs.

- **Créer** : avec l'outil du connecteur s'il en a un pour les versions. Sinon, donner à
  l'utilisateur la liste des versions à créer (nom et objectif), qu'il crée dans les réglages du
  projet Jira, puis vérifier qu'elles existent.
- **Rattacher** : renseigner le champ `fixVersions` de l'issue.
- **Montrer la roadmap** : une recherche JQL par version,
  `project = PROJ AND fixVersion = "<nom>" ORDER BY status`, et
  `project = PROJ AND fixVersion is EMPTY AND statusCategory != Done` pour ce qui n'a pas de
  jalon.

## Lire, lister, commenter, terminer

- **Lire** : l'issue avec ses commentaires, puis son Epic.
- **Lister les ouverts** : une recherche JQL, par exemple
  `project = PROJ AND statusCategory != Done AND text ~ "<mots-clés>"`.
- **Commenter**, après feu vert : l'outil d'ajout de commentaire du connecteur.
- **Terminer** : après feu vert, faire passer l'issue au statut « Terminé » de son workflow
  (en récupérant d'abord les transitions disponibles), avec un commentaire de bilan court.
