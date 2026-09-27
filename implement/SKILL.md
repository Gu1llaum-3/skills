---
name: implement
description: Exécute un plan markdown déjà validé, vague par vague. Tout le code s'écrit en TDD, chaque tâche fait un commit avec sa case cochée, et le plan est vérifié et mis en pause à la fin de chaque vague ; on reprend exactement là où on s'est arrêté. Utilise ce skill dès que l'utilisateur veut implémenter, exécuter, dérouler ou reprendre un plan (« implémente le plan », « lance la vague 2 », « on attaque le jalon T2 », « continue le plan », « enchaîne les vagues »), même s'il ne dit pas « /implement ». Ne pas l'utiliser pour écrire, relire ou modifier un plan.
argument-hint: "[chemin du plan] [turbo]"
---

# Implémenter un plan

Ce skill sert **uniquement à exécuter**. On ne redessine pas le plan, on ne l'audite pas et on ne le
réécrit pas : on l'exécute en TDD, on coche au fil de l'eau et on s'arrête dès que quelque chose ne
va pas. Le plan a été discuté et validé ; le rôle de ce skill est de le réaliser fidèlement et de
laisser une trace qu'une reprise ou un relecteur pourra suivre sans avoir la conversation sous les
yeux.

**Les conventions du dépôt priment toujours** sur ce qui suit (langue, noms de branches, format des
commits, commandes, essais). Ce skill ne donne que les réglages par défaut.

## Préalables

- **Trouver le plan** : le chemin passé en argument. Sinon, chercher dans le dossier de plans du
  dépôt (`docs/plans/`, `plans/`, ou ce que dit `CLAUDE.md`) les plans qui ont encore des cases non
  cochées, puis `plan.md` à la racine. S'il y a un seul candidat, le prendre et le nommer. S'il y en
  a plusieurs, demander lequel. S'il n'y en a aucun, s'arrêter et le dire.
- **Validé** : une ligne datée du type « Validé par … le … », ou un accord explicite dans la
  conversation. Sinon, s'arrêter : un plan brouillon ne s'exécute pas, parce qu'on coderait des
  décisions que personne n'a prises.
- **Conventions du dépôt** : lire `CLAUDE.md`, `README.md` et les documents qu'ils désignent comme
  obligatoires pour le type de tâche (par exemple un `DESIGN.md` avant un travail d'interface).
  Relever ce qu'ils disent des branches, des commits, des tests, des essais manuels et de la
  vérification.
- **Commandes** : trouver la commande de vérification complète et celle qui lance un seul fichier
  de test (`CLAUDE.md`, `package.json`, `mise.toml`, `Makefile`, `justfile`…). Si elles sont
  introuvables, les demander avant la première tâche. Le skill `tdd` en a besoin aussi : les
  avoir trouvées ici évite de les chercher deux fois.
- **Arbre de travail** (`git status`) :
  - propre : on continue ;
  - sale : montrer le diff. S'il correspond visiblement à la tâche du point de reprise (une
    exécution interrompue), proposer de repartir de ce travail ou de l'écarter ; sinon, attendre.
    Ne jamais jeter ni commiter des modifications qu'on n'a pas faites.
- **Plan hors du dépôt** (convention qui interdit ces fichiers) : ne jamais le commiter, mais y
  cocher les cases et y écrire le bilan quand même.

**Autorisation de commit** : lancer ce skill sur un plan validé autorise les commits d'une tâche à
la fois qu'il prévoit, même si le dépôt demande par ailleurs de « ne commiter que sur demande ».
Cette autorisation ne va pas plus loin : pas de merge, pas de push, pas de pull request.

## Lecture et reprise

1. Détecter les vagues (sections dont le titre parle de vague, de phase, d'étape ou de jalon) et
   les tâches (`- [ ]`, `- [x]`). S'il n'y a pas de cases, en ajouter aux seules lignes de tâches.
2. **Contrôler la cohérence** entre le plan et `git log` : une case cochée sans commit
   correspondant, ou un commit qui cite le plan sans case cochée, signale une reprise délicate. Le
   dire avant de continuer plutôt que de deviner.
3. Résumer en quelques lignes : les vagues, les tâches de chaque vague, et le **point de reprise**
   (première tâche non cochée de la première vague incomplète). Les tâches cochées sont faites : on
   ne les refait pas.
4. **Branche** : celle que nomme le plan, sinon celle qu'impose la convention du dépôt, sinon une
   branche pour tout le plan, créée depuis la branche de départ et au nom court
   (`feat/<slug>`, `fix/<slug>`, `chore/<slug>`). En reprise, retourner sur cette branche.
   **Jamais sur la branche principale** (`main`, `master`, ou celle que le dépôt désigne comme
   telle), même si une convention semble le permettre : la fusion y a lieu sur feu vert, pas au fil
   des tâches. Seule exception : le propriétaire le demande explicitement pour ce plan, et on le
   note dans le plan.
5. **Mode turbo** : si l'utilisateur demande d'enchaîner (argument `turbo`, « enchaîne les vagues
   2 et 3 »), noter quelles vagues sont concernées. Hors de ces vagues, la pause reste de règle.

## Une vague

1. Annoncer la vague et lister ses tâches non cochées.
2. Pour chaque tâche, dans l'ordre :
   - **Code : TDD, toujours.** Appeler le Skill tool avec « tdd » (une fois par exécution suffit)
     et suivre sa boucle pour chaque tâche de code : test rouge vu échouer pour la bonne raison,
     code minimal, vert, refactorisation. Les interfaces à tester se déduisent de la tâche et de
     ses critères : le plan étant validé, on ne les redemande pas, sauf réelle ambiguïté.
   - **Nommer le test** d'après le critère ou la règle qu'il prouve, avec son numéro si le plan en
     donne un (`AC-2`, `COM-04`), pour qu'on retrouve la preuve de chaque critère dans le bilan.
   - **Ce qui ne se teste pas automatiquement** (configuration, documentation, rendu, CSS,
     animation) : faire la vérification que le dépôt prévoit à la place (essai dans le navigateur
     avec captures, détecteur de design, commande de contrôle) et la décrire dans le compte rendu
     de la tâche. Écrire « non testable » sans rien vérifier ne suffit pas.
   - **Une fois la tâche verte** : vérifier la branche courante (`git branch --show-current`) ; si
     c'est la branche principale sans exception notée dans le plan, s'arrêter et le dire. Cocher
     ensuite la case sans toucher au reste du texte du plan, puis commiter le code **et** le plan
     ensemble. Le message suit le format du dépôt (langue, préfixe,
     corps qui explique le pourquoi, lignes d'attribution) et, par défaut, un message
     conventionnel. Le corps contient `Refs: <chemin du plan>`, pour que `git log` ramène au
     contexte. Une tâche = un commit, case comprise : ainsi, une reprise ne refait jamais une tâche
     déjà commitée.
3. **Fin de vague** : lancer la vérification complète et **lire son code de retour**. Ne jamais
   faire passer la sortie par un pipe (`| tail`, `| grep`) dans la commande qui sert de
   vérification, car le pipe remplace le code de retour et masque l'échec. Rediriger vers un
   fichier, lire le code, puis lire le fichier. Si c'est rouge, la vague n'est pas finie.
4. **Micro-bilan**, écrit aussi dans le plan (sous la vague ou dans une section « Journal » /
   « Retours d'essai » si le plan en a une) :
   - ce qui a été livré : fichiers, tests, comportements ;
   - les écarts au plan et leur raison ;
   - ce qui a été vérifié et comment, et ce qui ne l'a pas été ;
   - les bugs trouvés en route ;
   - **quoi essayer** : la commande pour lancer l'application et deux ou trois choses concrètes à
     regarder, pour que la pause de test soit utile.
   « Fait » n'est pas un bilan.
5. **Pause** : `Vague terminée. Passer à la vague suivante « <titre> » ?`. Les retours d'essai du
   propriétaire sont consignés dans le plan avant de reprendre. Seule exception à la pause : le
   mode turbo sur les vagues nommées.

## Fin du plan

Quand la dernière vague est verte :

1. **Écrire le bilan dans le plan**, pour le relecteur : dans la section « Réalisé » si le plan en
   a une, sinon dans une section ajoutée en fin de fichier. Y mettre :
   - chaque critère, atteint (avec le test qui le prouve) ou non, et pourquoi ;
   - les écarts au plan et leur raison ;
   - les tâches ajoutées ou retirées ;
   - ce qui reste hors plan.
   Passer le statut à « terminé » et commiter selon le format du dépôt (par défaut
   `docs: record plan outcome`).
2. **Proposer un résumé de fusion**, tiré du plan : trois lignes de résumé, les critères atteints,
   une ligne par décision, le lien vers le plan. Il sert de description de pull request si le dépôt
   en utilise, sinon de récapitulatif avant la fusion.
3. **Proposer, sans l'exécuter**, la suite Git habituelle du dépôt (fusion dans la branche de
   départ, en avance rapide si c'est la convention, ou pull request) et le push s'il existe un
   dépôt distant. Ces étapes attendent un feu vert explicite.

## Quand ça ne va pas

- **Échec d'une tâche** (un test qui ne passe pas après un effort raisonnable, une commande qui
  échoue, une contradiction avec le code) : arrêter, écrire sous la tâche
  `> Échec (AAAA-MM-JJ) : …`, rapporter et attendre.
- **Ambiguïté** : si le plan ne dit pas quoi faire, poser une question courte, puis consigner la
  réponse dans le plan avant de continuer, pour qu'elle survive à la conversation.
- **Le plan a tort** (état de départ faux, dépendance manquante, tâche impossible telle
  qu'écrite) : s'arrêter, dire ce qui est faux et proposer l'amendement. Ne pas contourner en
  silence : un écart non dit rend le plan faux pour tous ceux qui le reliront.
- **Une idée en route** : l'écrire en une ligne dans une section « Hors plan » du plan, puis
  continuer. Elle ne se code pas.
- **Un changement destructeur** (suppression de données, migration irréversible, écriture vers un
  service tiers, réécriture de l'historique) : demander une confirmation explicite, même si le
  plan le prévoit.

## Ce que ce skill ne fait jamais

- Exécuter un plan non validé, ou une tâche qui n'y figure pas.
- Écrire du code avant son test, adapter un test au code pour le faire passer, désactiver ou
  ignorer un test.
- Cocher une tâche dont le test ou la vérification n'a pas tourné.
- Masquer le code de retour d'une vérification, ou annoncer du vert sans l'avoir lu.
- Commiter sur la branche principale, sauf demande explicite du propriétaire notée dans le plan.
- Fusionner dans la branche de départ, pousser ou ouvrir une pull request sans feu vert explicite.
- Enchaîner les vagues sans pause quand ce n'est pas demandé.
