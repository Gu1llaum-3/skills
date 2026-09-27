---
name: feature
description: Cadrer une idée de fonctionnalité dans un projet existant, avant de la coder. Le skill lit le projet (code, ROADMAP, docs), restitue l'idée et ses impacts, fait les recherches utiles, mène un court entretien par questions à choix, puis propose de l'implémenter tout de suite (plan exécuté par implement) ou de la mettre de côté (spec et tickets via to-spec, ou entrée dans ROADMAP.md). Utilise ce skill dès que l'utilisateur a une idée de feature, d'amélioration ou d'évolution pour un projet qui existe déjà (« j'ai une idée », « on pourrait ajouter… », « et si l'app faisait… », « qu'est-ce que tu penses de… »), même hors roadmap, et qu'il veut y réfléchir avant de coder. Pour un nouveau projet, utiliser brainstorming.
---

# Feature : de l'idée à la décision

L'objectif est de transformer une idée de fonctionnalité en **décision claire** : ce qu'on
construit, pourquoi, comment on saura que c'est fait, et quand on le fait. On n'écrit pas de code
pendant le cadrage. Ce qui a de la valeur : montrer qu'on a compris comment l'idée s'insère dans
le projet, ne poser que les questions qui sont vraiment à l'utilisateur, et laisser une trace
qu'une autre session pourra reprendre.

Réponds dans la langue de l'utilisateur. Adapte le déroulé si l'utilisateur saute une étape.

## 1. Lire le projet

- **Documents** : `CLAUDE.md`, `README.md`, `ROADMAP.md`, le cahier des charges, `DESIGN.md`, les
  specs et plans existants (`docs/specs/`, `docs/plans/`).
- **Tickets existants** : si le projet a une section `## Tickets` dans `CLAUDE.md`, appeler le
  Skill tool avec « tickets » pour chercher un ticket proche. Sinon, ne pas configurer de
  gestionnaire maintenant : ce n'est utile que si la feature finit en ticket.
- **Code** : la partie que l'idée touche, les modèles de données, les interfaces publiques
  concernées, les tests voisins. Pour une exploration large, déléguer à un sous-agent et ne
  garder que les conclusions.

## 2. Restituer

En un message court :

1. **Ce que je comprends de l'idée**, en une ou deux phrases, du point de vue de l'utilisateur
   final.
2. **Où elle s'insère** : modules et écrans concernés, ce qui existe déjà et peut servir.
3. **Ce que je remarque** :
   - ✅ ce qui la rend simple (briques existantes, cohérence avec la roadmap) ;
   - ⚠️ les frottements concrets : doublon avec une fonction ou un ticket existant, conflit avec
     la roadmap ou une décision passée, migration de données, impact sur la performance, la
     sécurité ou l'accessibilité.

Un écart précis et justifié vaut mieux qu'un résumé flatteur.

## 3. Rechercher, si c'est utile

Quand l'idée touche un domaine pointu, une bibliothèque à choisir ou un usage établi (« comment
font les autres »), faire une vraie recherche : 2 ou 3 options comparées, une recommandation, les
sources citées, les licences vérifiées si une dépendance est proposée. Si la recherche est longue,
la lancer dans un sous-agent en arrière-plan et poser pendant ce temps les questions qui n'en
dépendent pas.

**Les faits se cherchent, les décisions se demandent** : ne jamais demander à l'utilisateur ce
qu'on peut trouver dans le code, la documentation ou le web.

## 4. L'entretien

Avec l'outil **AskUserQuestion**, en **1 à 3 séries de 4 questions au maximum**. À chaque série,
poser toutes les questions qu'on peut trancher sans attendre d'autres réponses ; une question qui
dépend d'une réponse encore ouverte va dans la série suivante.

Les sujets, à prendre seulement s'ils sont ouverts :

- **Comportement** : le parcours principal, les cas limites qui comptent, les erreurs.
- **Périmètre** : ce qui est inclus dans cette version, ce qui est explicitement exclu.
- **Choix techniques** : l'option recommandée par la recherche, les compromis.
- **Interfaces à tester** : où placer les tests (route, fonction exportée, écran). Les proposer
  plutôt que les demander, pour que `tdd` n'ait rien à redemander ensuite.

Règles de rédaction : 2 à 4 options mutuellement exclusives, dont la description donne le
compromis ; l'option recommandée en premier, suivie de « (Recommandé) » ; pas d'option « Autre »,
l'outil l'ajoute. Lire attentivement les réponses libres, signaler les tensions entre deux
réponses, ne jamais reposer une question tranchée.

On s'arrête quand plus rien d'important n'est supposé en silence.

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

- **Implémenter maintenant** (recommandé si ça tient dans une session) :
  1. écrire le plan dans le dossier de plans du dépôt (par défaut `docs/plans/<feature>.md`), en
     suivant [references/plan.md](references/plan.md) ;
  2. le montrer et demander le feu vert ;
  3. une fois l'accord obtenu, ajouter la ligne « Validé par … le … », puis appeler le Skill tool
     avec « implement » en lui donnant le chemin du plan.
- **En faire une spec et des tickets** (recommandé si plusieurs sessions, ou si ce n'est pas
  pour tout de suite) : appeler le Skill tool avec « to-spec ». Tout ce qui a été décidé est dans
  la conversation ; il n'y a rien à lui redire.
- **Juste l'inscrire dans `ROADMAP.md`** (si le fichier existe) : ajouter une entrée dans le
  format existant, avec la synthèse en quelques lignes, et la commiter si le dépôt commite ses
  docs.
- **Abandonner** : résumer en une ligne pourquoi, pour que la raison ne se perde pas.

## Ce que ce skill ne fait jamais

- Écrire du code pendant le cadrage.
- Lancer `implement` sans feu vert explicite sur le plan.
- Publier un ticket ou modifier `ROADMAP.md` sans que l'utilisateur ait choisi cette suite.
- Réécrire la roadmap : on y ajoute une entrée, on ne réorganise pas le reste.
