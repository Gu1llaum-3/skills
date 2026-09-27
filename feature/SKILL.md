---
name: feature
description: Cadrer une idée de fonctionnalité dans un projet existant, puis la planifier tout de suite ou en faire une spec, des tickets ou une entrée de roadmap.
argument-hint: "[description de l'idée]"
disable-model-invocation: true
---

# Feature : de l'idée à la décision

L'objectif est de transformer une idée de fonctionnalité en **décision claire** : ce qu'on
construit, pourquoi, comment on saura que c'est fait, et quand on le fait. On n'écrit pas de code
pendant le cadrage. Ce qui a de la valeur : montrer qu'on a compris comment l'idée s'insère dans
le projet, questionner le besoin, et laisser une trace qu'une autre session pourra reprendre.

Réponds dans la langue de l'utilisateur. Pour un projet qui n'existe pas encore, c'est
`/brainstorming` qu'il faut.

## 1. Lire le projet

- **Documents** : `CLAUDE.md`, `README.md`, `ROADMAP.md`, `docs/cahier-des-charges.md`,
  `docs/design/DESIGN.md`, les specs, plans et recherches de `docs/`, et les titres des ADR
  (`docs/adr/`). Dans les projets plus anciens, ces fichiers peuvent être à la racine.
- **Tickets existants** : si le `CLAUDE.md` a une section « Tickets », appeler le Skill tool avec
  « tickets » pour chercher un ticket proche. Sinon, ne rien configurer maintenant.
- **Code** : la partie que l'idée touche, les modèles de données, les interfaces publiques, les
  tests voisins. Pour une exploration large, la déléguer à un sous-agent et ne garder que les
  conclusions.

## 2. Restituer

En un message court :

1. **Ce que je comprends de l'idée**, en une ou deux phrases, du point de vue de l'utilisateur
   final.
2. **Où elle s'insère** : modules et écrans concernés, ce qui existe déjà et peut servir.
3. **Ce que je remarque** :
   - ✅ ce qui la rend simple (briques existantes, cohérence avec la roadmap) ;
   - ⚠️ les frottements concrets : doublon avec une fonction ou un ticket, conflit avec la
     roadmap ou un ADR, migration de données, performance, sécurité, accessibilité.

Un écart précis et justifié vaut mieux qu'un résumé flatteur.

## 3. Rechercher, si c'est utile

Quand l'idée touche un domaine pointu, une bibliothèque à choisir ou un usage établi (« comment
font les autres »), appeler le Skill tool avec « research ». La recherche tourne en arrière-plan :
commencer l'entretien sans l'attendre, par les questions qui n'en dépendent pas.

## 4. L'entretien

Appeler le Skill tool avec « interview », en 1 à 3 séries, sur les sujets encore ouverts parmi :

- **Le besoin** : le problème réel, ce qui se passe si on ne le fait pas, la version la plus
  simple.
- **Le comportement** : le parcours principal, les cas limites qui comptent, les erreurs.
- **Le périmètre** : ce qui est inclus dans cette version, ce qui est explicitement exclu.
- **Les choix techniques** : l'option recommandée par la recherche, les compromis.
- **Les interfaces à tester** : où placer les tests (route, fonction exportée, écran). Les
  proposer plutôt que les demander, pour que `tdd` n'ait rien à redemander.

## 5. Synthèse

Dans la conversation, sans écrire de fichier :

- **Problème** et **solution**, du point de vue de l'utilisateur ;
- **Décisions** prises, une ligne chacune ;
- **Critères d'acceptation** numérotés (`AC-1`, `AC-2`…), vérifiables ;
- **Interfaces à tester** ;
- **Hors périmètre** ;
- **Taille** : tient-elle dans une session de travail, ou en faudra-t-il plusieurs ?

## 6. Décider de la suite

Poser la question avec AskUserQuestion, en recommandant selon la taille :

- **Planifier maintenant** (recommandé si ça tient dans une session) : appeler le Skill tool avec
  « plan ». L'exploration et la recherche sont faites : il passe directement à la rédaction, puis
  propose de lancer `implement`.
- **En faire une spec et des tickets** (recommandé si plusieurs sessions, ou si ce n'est pas pour
  tout de suite) : appeler le Skill tool avec « to-spec ». Tout est dans la conversation.
- **Juste l'inscrire dans `ROADMAP.md`** (si le fichier existe) : ajouter une entrée dans son
  format, avec la synthèse en quelques lignes.
- **Abandonner** : résumer en une ligne pourquoi, pour que la raison ne se perde pas.

## Ce que ce skill ne fait jamais

- Écrire du code pendant le cadrage.
- Publier un ticket ou modifier `ROADMAP.md` sans que l'utilisateur ait choisi cette suite.
- Réécrire la roadmap : on y ajoute une entrée, on ne réorganise pas le reste.
