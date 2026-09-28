---
name: brainstorming
description: Cadrer un nouveau projet (app, jeu, outil, site, produit) avant d'écrire du code, jusqu'à un cahier des charges validé dans docs/.
argument-hint: "[idée, dossier du prototype ou fichier POC]"
disable-model-invocation: true
---

# Brainstorming : de l'idée au cahier des charges

L'objectif est d'aider l'utilisateur à transformer une idée, souvent accompagnée d'un prototype, en un **cahier des charges validé**, sans écrire de code. Ce qui a de la valeur : montrer qu'on a compris le domaine mieux qu'une lecture rapide, poser les bonnes questions au bon moment, et rendre chaque décision traçable.

Ce skill sert aux **nouveaux projets**. Pour une idée de fonctionnalité dans un projet existant, c'est `/feature` qu'il faut.

Réponds dans la langue de l'utilisateur. Le déroulé comporte six étapes. Adapte-le si l'utilisateur en saute une ou en demande une autre.

## 1. S'imprégner : l'existant et le domaine

- **Lis en entier** ce que l'utilisateur fournit : prototype, maquettes, notes, code. Un prototype contient souvent des choix implicites (mécaniques, ton, public visé) qu'il faut repérer.
- **Un fichier POC** (`docs/poc/<slug>.md`, produit par `/poc`) : lis d'abord son verdict. Ses choix sont marqués : **décidé** se reprend tel quel (en le citant dans la synthèse, pour que l'utilisateur puisse le rouvrir), **hypothèse** se rejoue pendant l'entretien, **ouvert** fait partie des questions. Le code du POC est jetable par défaut : ce qu'on en garde se décide pendant l'entretien.
- **Documente-toi sur le domaine** : méthode, bonnes pratiques, public, contraintes réglementaires. Appuie-toi sur tes connaissances, et appelle le Skill tool avec « research » quand un point est pointu ou récent : la recherche tourne en arrière-plan pendant que tu avances. Cite tes sources.
- Ne propose pas encore de solution technique, et n'écris pas de code : l'utilisateur veut d'abord être compris.

## 2. Restituer : une synthèse critique

Présente en un message court et structuré :

1. **Ce que je retiens du domaine** : les 4 à 6 principes qui vont vraiment conditionner le produit, chacun avec son « pourquoi ».
2. **Ce que j'observe dans l'existant** :
   - ✅ ce qui va déjà dans le bon sens ;
   - ⚠️ les écarts avec les bonnes pratiques et les risques, de façon concrète (« le mot X utilise Y, qui n'a pas été vu »), pas « à améliorer ».

Cette partie crée la confiance. Un écart précis et justifié vaut mieux que dix compliments.

## 3. L'entretien

Appelle le Skill tool avec « interview », en 3 à 5 séries thématiques, de la plus structurante à la plus fine :

1. **Le besoin** : le problème réel, pour qui, ce qui existe déjà ailleurs, la version la plus simple qui vaudrait le coup.
2. **Contexte** : utilisateur final, niveau de départ, plateformes cibles.
3. **Cœur du produit** : mécaniques principales, progression, gestion des erreurs, motivation.
4. **Contenu et expérience** : univers, graphisme, audio, accessibilité, profils.
5. **Technique et contraintes** : stack, stockage, hors ligne, sécurité, publication prévue ou non.
6. **Répartition et suite** : qui produit quoi (contenus, visuels, textes), et la prochaine étape (proposer le cahier des charges en recommandé).

Saute les thèmes que l'existant a déjà tranchés. Les choix structurants et difficiles à défaire (stack, stockage, hébergement) sont souvent de bons candidats à un ADR : l'entretien les proposera.

## 4. Rédiger le cahier des charges

Écris `docs/cahier-des-charges.md`, en suivant la structure de `references/modele-cahier-des-charges.md`. Adapte les sections au projet : un site web n'a pas besoin de système de récompenses.

- Transforme chaque réponse en **décision concrète et chiffrée quand c'est possible** : un seuil, une durée, un ordre, un nom de fichier.
- Là où tu as dû supposer, marque **[À valider]**, et regroupe ces points dans une section « Questions ouvertes » numérotée en fin de document. C'est ce qui permet à l'utilisateur de répondre point par point.
- Les questions que l'entretien a renvoyées au métier vont dans la même section, marquées **[Métier : <destinataire>, bloquante]** (format du skill `to-questionnaire`).
- Ajoute un **découpage en jalons**, du socle jouable à la publication.
- Termine le découpage par un **verdict d'envergure**, avec sa raison en une phrase. Il décide de la suite, et il est écrit pour que les sessions suivantes n'aient pas à le rejouer :
  - **simple** : chaque jalon tient en une session (critère « Taille » de [`to-tickets`](../to-tickets/SKILL.md)). Chaque jalon se planifie directement avec `plan` ; une spec ne ferait que redire le cahier des charges.
  - **gros** : au moins un jalon dépasse une session. Chaque jalon passe par une spec (`to-spec`), puis des tickets rangés dans ce jalon de la roadmap.
- Si la mémoire persistante est disponible, enregistre les décisions clés du projet (un fichier par fait).

Termine le message par : un résumé en quelques puces, la liste des questions ouvertes, et **une proposition de prochaine étape**. S'il y a des questions pour le métier, propose d'en faire un questionnaire par destinataire en appelant le Skill tool avec « to-questionnaire ».

## 5. Trancher les questions ouvertes

L'utilisateur répond en général en liste numérotée. Pour chaque point :

- **Décision directe** : intègre-la dans le document.
- **Point délégué** (« je te laisse rechercher, gratuit si possible ») :
  - appelle le Skill tool avec « research », avec les critères demandés (coût, qualité, licence, hors ligne…) : il compare 2 ou 3 options, donne **une recommandation et une solution de repli**, et laisse une note sourcée dans `docs/research/` ;
  - rends le choix réversible dans l'architecture (une interface, un fichier de configuration) quand l'utilisateur dit qu'il pourra changer.
- **Réponse ambiguë** : applique l'interprétation la plus plausible, **et dis-la explicitement** dans ta réponse.
- **Règle permanente** (« ça sera le cas pour toute l'application ! ») : ajoute-la comme section dédiée du cahier des charges et, si possible, en mémoire (de type feedback), pour qu'elle s'applique aux sessions futures.
- **Point pour le métier** (« je ne sais pas, faut voir avec le client ») : marque-le **[Métier : <destinataire>]** au lieu de le supposer, et propose un questionnaire avec le skill `to-questionnaire`. Quand le questionnaire revient rempli, ce skill reporte les réponses dans le cahier des charges.
- **Nom ou valeur encore inconnu** : prévois qu'il soit centralisé et modifiable (configuration), et propose quelques exemples.

Passe ensuite le document à la version suivante (« v0.2 — décisions du JJ/MM/AAAA intégrées »). Retire les marqueurs **[À valider]** résolus, et ne garde dans les questions ouvertes que ce qui l'est vraiment.

### Licences, si le projet sera publié

Si l'utilisateur envisage de publier ou de diffuser le projet, demande-lui s'il veut une règle de vérification des licences. Elle se traduit par :

- une section « Licences (règle permanente) » dans le cahier des charges : licences acceptées, licences à éviter (non commerciales, GPL ou AGPL embarquées, licence inconnue), contrôle automatique des dépendances ;
- un fichier `LICENCES.md` : ressource, usage, source, licence, obligations, date de vérification, et une liste des ressources écartées avec la raison.

Vérifie chaque ressource proposée (bibliothèque, police, voix, image) au moment où tu la recommandes. Ce n'est pas à faire après coup.

## 6. Proposer la suite

Termine toujours par une ou deux prochaines étapes concrètes, avec celle que tu recommandes. En général :

- **projet simple** : planifier le premier jalon, en appelant le Skill tool avec « plan » sur `docs/cahier-des-charges.md`, puis `implement` ;
- **gros projet** : écrire la spec du premier jalon, en appelant le Skill tool avec « to-spec » sur `docs/cahier-des-charges.md`. Elle sera découpée en tickets, et chaque ticket se traitera ensuite dans sa propre session avec `/implement <ticket>` ;
- **définir l'identité visuelle** avec `/design`, ou **trouver un nom** avec `/naming`, si ce n'est pas encore fait.

N'enchaîne pas sur le développement sans l'accord de l'utilisateur. Une question métier **bloquante** pour un jalon empêche de le planifier : planifie un jalon qui n'en dépend pas, ou attends la réponse.

## Ton

- Sois concis et structuré : des titres courts, des puces, des tableaux quand on compare.
- Sois franc : si un choix de l'utilisateur pose problème, dis-le avec la raison, puis propose une alternative.
- Montre de l'enthousiasme pour les bonnes idées de l'utilisateur, en une phrase, sans flagornerie.
