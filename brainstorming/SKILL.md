---
name: brainstorming
description: Cadrer un nouveau projet (app, jeu, outil, site, produit) avant d'écrire du code. Le skill lit l'existant (POC, maquettes, notes), se documente sur le domaine, présente une synthèse critique, puis mène un entretien interactif par séries de questions à choix (AskUserQuestion). Il termine par un cahier des charges avec les points à valider et les questions ouvertes, puis tranche ces points par des recherches. À utiliser dès que l'utilisateur décrit une idée de projet et veut « réfléchir », « aller plus loin dans le détail », « poser des questions », « cadrer », « faire un cahier des charges » ou « brainstormer ». C'est aussi le bon skill quand il partage un prototype en demandant ce qu'on en pense avant de développer, même s'il ne prononce pas le mot brainstorming.
---

# Brainstorming : de l'idée au cahier des charges

L'objectif est d'aider l'utilisateur à transformer une idée, souvent accompagnée d'un prototype, en un **cahier des charges validé**, sans écrire de code. Ce qui a de la valeur : montrer qu'on a compris le domaine mieux qu'une lecture rapide, poser les bonnes questions au bon moment, et rendre chaque décision traçable.

Réponds dans la langue de l'utilisateur. Le déroulé comporte six étapes. Adapte-le si l'utilisateur en saute une ou en demande une autre.

## 1. S'imprégner : l'existant et le domaine

- **Lis en entier** ce que l'utilisateur fournit : prototype, maquettes, notes, code. Un prototype contient souvent des choix implicites (mécaniques, ton, public visé) qu'il faut repérer.
- **Documente-toi sur le domaine** : méthode, bonnes pratiques, public, contraintes réglementaires. Appuie-toi sur tes connaissances, et fais une recherche web quand un point est pointu ou récent. Cite tes sources quand tu en utilises.
- Ne propose pas encore de solution technique, et n'écris pas de code : l'utilisateur veut d'abord être compris.

## 2. Restituer : une synthèse critique

Présente en un message court et structuré :

1. **Ce que je retiens du domaine** : les 4 à 6 principes qui vont vraiment conditionner le produit, chacun avec son « pourquoi ».
2. **Ce que j'observe dans l'existant** :
   - ✅ ce qui va déjà dans le bon sens ;
   - ⚠️ les écarts avec les bonnes pratiques et les risques, de façon concrète (« le mot X utilise Y, qui n'a pas été vu »), pas « à améliorer ».

Cette partie crée la confiance. Un écart précis et justifié vaut mieux que dix compliments.

## 3. L'entretien interactif

Pose les questions avec l'outil **AskUserQuestion**, par **séries thématiques de 4 questions au maximum**. Enchaîne 3 à 5 séries, de la plus structurante à la plus fine :

1. **Contexte** : utilisateur final, niveau de départ, plateformes cibles.
2. **Cœur du produit** : mécaniques principales, progression, gestion des erreurs, motivation.
3. **Contenu et expérience** : univers, graphisme, audio, accessibilité, profils.
4. **Technique et contraintes** : stack, stockage, hors ligne, sécurité, publication prévue ou non.
5. **Répartition et suite** : qui produit quoi (contenus, visuels, textes), et la prochaine étape (proposer le cahier des charges en recommandé).

Règles pour rédiger les questions :

- 2 à 4 options, **mutuellement exclusives**, avec une description qui donne le **compromis** (« plus de travail, mais un rendu bien meilleur »).
- Mets l'option que tu recommandes **en premier**, suivie de « (Recommandé) ». N'en recommande pas quand c'est une vraie affaire de goût.
- Utilise `multiSelect` seulement quand les choix se cumulent (par exemple la liste des jeux à inclure).
- N'invente pas d'option « Autre » : l'outil l'ajoute tout seul.

Entre deux séries :

- **Lis attentivement les réponses libres.** C'est là que l'utilisateur livre ses meilleures idées : systèmes de récompense, contraintes cachées, visions à long terme. Reprends-les telles quelles, et fais-en le sujet de la série suivante.
- **Repère les tensions** entre deux réponses (par exemple « des étoiles de 1 à 3 » et « jamais punitif »). Signale-les en une phrase, puis pose la question qui les résout.
- Si l'utilisateur demande ton avis (« sauf si tu me le déconseilles »), donne une **recommandation franche en une ou deux lignes** avant la série suivante.
- Ne repose pas une question déjà tranchée. Si une réponse change la cible (« pars du principe que c'est un débutant, pour d'autres utilisateurs plus tard »), applique-la à tout ce qui suit.

## 4. Rédiger le cahier des charges

Écris `CAHIER_DES_CHARGES.md` à la racine du projet, en suivant la structure de `references/modele-cahier-des-charges.md`. Adapte les sections au projet : un site web n'a pas besoin de système de récompenses.

- Transforme chaque réponse en **décision concrète et chiffrée quand c'est possible** : un seuil, une durée, un ordre, un nom de fichier.
- Là où tu as dû supposer, marque **[À valider]**, et regroupe ces points dans une section « Questions ouvertes » numérotée en fin de document. C'est ce qui permet à l'utilisateur de répondre point par point.
- Ajoute un **découpage en jalons**, du socle jouable à la publication.
- Si la mémoire persistante est disponible, enregistre les décisions clés du projet (un fichier par fait).

Termine le message par : un résumé en quelques puces, la liste des questions ouvertes, et **une proposition de prochaine étape**.

## 5. Trancher les questions ouvertes

L'utilisateur répond en général en liste numérotée. Pour chaque point :

- **Décision directe** : intègre-la dans le document.
- **Point délégué** (« je te laisse rechercher, gratuit si possible ») :
  - fais une vraie recherche web et compare 2 ou 3 options sur les critères demandés (coût, qualité, licence, hors ligne…) ;
  - donne **une recommandation, et une solution de repli** ;
  - cite tes sources ;
  - rends le choix réversible dans l'architecture (une interface, un fichier de configuration) quand l'utilisateur dit qu'il pourra changer.
- **Réponse ambiguë** : applique l'interprétation la plus plausible, **et dis-la explicitement** dans ta réponse.
- **Règle permanente** (« ça sera le cas pour toute l'application ! ») : ajoute-la comme section dédiée du cahier des charges et, si possible, en mémoire (de type feedback), pour qu'elle s'applique aux sessions futures.
- **Nom ou valeur encore inconnu** : prévois qu'il soit centralisé et modifiable (configuration), et propose quelques exemples.

Passe ensuite le document à la version suivante (« v0.2 — décisions du JJ/MM/AAAA intégrées »). Retire les marqueurs **[À valider]** résolus, et ne garde dans les questions ouvertes que ce qui l'est vraiment.

### Licences, si le projet sera publié

Si l'utilisateur envisage de publier ou de diffuser le projet, demande-lui s'il veut une règle de vérification des licences. Elle se traduit par :

- une section « Licences (règle permanente) » dans le cahier des charges : licences acceptées, licences à éviter (non commerciales, GPL ou AGPL embarquées, licence inconnue), contrôle automatique des dépendances ;
- un fichier `LICENCES.md` : ressource, usage, source, licence, obligations, date de vérification, et une liste des ressources écartées avec la raison.

Vérifie chaque ressource proposée (bibliothèque, police, voix, image) au moment où tu la recommandes. Ce n'est pas à faire après coup.

## 6. Proposer la suite

Termine toujours par une ou deux prochaines étapes concrètes, avec celle que tu recommandes. Par exemple : « détailler le contenu étape par étape » ou « initialiser le projet ». N'enchaîne pas sur le développement sans l'accord de l'utilisateur.

## Ton

- Sois concis et structuré : des titres courts, des puces, des tableaux quand on compare.
- Sois franc : si un choix de l'utilisateur pose problème, dis-le avec la raison, puis propose une alternative.
- Montre de l'enthousiasme pour les bonnes idées de l'utilisateur, en une phrase, sans flagornerie.
