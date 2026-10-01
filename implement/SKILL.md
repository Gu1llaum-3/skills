---
name: implement
description: "Exécuter un plan validé, un ticket ou un jalon (fichier local, GitHub, GitLab, Jira), vague par vague, en TDD, une tâche par commit, avec une pause par vague et une relecture à la fin ; reprendre exactement là où on s'est arrêté. Utilise ce skill quand l'utilisateur veut implémenter, lancer ou reprendre un plan (« implémente le plan », « lance la vague 2 », « continue le plan »), un ticket (« implémente le ticket 42 », « on attaque PROJ-123 ») ou un jalon (« on attaque le jalon 2 »). Pas pour écrire, relire ou modifier un plan : c'est plan."
argument-hint: "[chemin du plan | ticket] [turbo]"
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
- **Partir d'un ticket** : si l'argument désigne un ticket (un numéro d'issue, une URL,
  `PROJ-123`, un fichier de `docs/tickets/`) :
  - chercher dans le dossier de plans un plan qui cite déjà ce ticket : c'est une reprise, on le
    prend ;
  - sinon, appeler le Skill tool avec « tickets » pour le lire. S'il a des bloquants non terminés,
    s'arrêter et les citer ;
  - sinon, appeler le Skill tool avec « plan » en lui donnant le ticket. Il confronte le ticket au
    code, rédige le plan et le fait valider ; on reprend ensuite ici avec ce plan.
- **Partir d'un jalon** (« on attaque le jalon 2 ») : un plan non terminé de `docs/plans/` qui
  cite ce jalon dans son `Origine :` est une reprise ; sinon, appeler le Skill tool avec « plan » sur ce jalon
  du cahier des charges, puis reprendre ici avec son plan.
- **Validé** : la ligne `> Statut : validé par … le …`, ou un accord explicite dans la
  conversation (écrire alors cette ligne dans le plan). Une question marquée « bloquante » dans
  le plan interdit aussi de démarrer. Sinon, s'arrêter : un plan brouillon ne s'exécute pas,
  parce qu'on coderait des décisions que personne n'a prises.
- **Conventions du dépôt** : lire `CLAUDE.md`, `README.md` et les documents qu'ils désignent comme
  obligatoires pour le type de tâche (par exemple `docs/design/DESIGN.md` avant un travail d'interface), et les titres des ADR
  (`docs/adr/`) pour ne pas contredire une décision passée sans le savoir. `GLOSSARY.md`, s'il
  existe : les noms du code et des tests reprennent ses termes.
  Relever ce qu'ils disent des branches, des commits, des tests, des essais manuels et de la
  vérification.
- **Commandes** : trouver la commande de vérification complète, celle qui lance un seul fichier
  de test, et celle du typage s'il y en a un (`CLAUDE.md`, `package.json`, `mise.toml`,
  `Makefile`, `justfile`…). Si elles sont introuvables, les demander avant la première tâche. Le skill `tdd` en a besoin aussi : les
  avoir trouvées ici évite de les chercher deux fois.
- **Arbre de travail** (`git status`) :
  - propre : on continue ;
  - seul le plan est nouveau ou modifié (il vient d'être rédigé ou validé) : on continue, il sera
    commité avec la première tâche ;
  - en plus du plan, des fichiers **nouveaux** écrits par les skills du parcours
    (`docs/research/`, `docs/questionnaires/`, `docs/poc/`, `docs/specs/`, `docs/tickets/`,
    `docs/design/`, `docs/requirements.md`, `ROADMAP.md`) : les nommer, puis les commiter
    avec la première tâche ;
  - toute autre modification : montrer le diff. S'il correspond visiblement à la tâche du point
    de reprise (une exécution interrompue), proposer de repartir de ce travail ou de l'écarter ;
    sinon, attendre.
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
4. **Branche** : celle que nomme le plan (`> Branche :`), sinon celle qu'impose la convention du
   dépôt, sinon une branche pour tout le plan, créée depuis la branche de départ et au nom court
   (`feat/<slug>`, `fix/<slug>`, `chore/<slug>`). En reprise, retourner sur cette branche.
   **Jamais sur la branche principale** (`main`, `master`, ou celle que le dépôt désigne comme
   telle), sauf si la convention écrite du dépôt (`CLAUDE.md`) dit d'y commiter : la fusion y a
   lieu sur feu vert, pas au fil des tâches.
5. **Mode turbo** : si l'utilisateur demande d'enchaîner (argument `turbo`, « enchaîne les vagues
   2 et 3 »), noter quelles vagues sont concernées. Hors de ces vagues, la pause reste de règle.

## Une vague

1. Annoncer la vague et lister ses tâches non cochées.
2. Pour chaque tâche, dans l'ordre :
   - **Code : TDD, toujours.** Appeler le Skill tool avec « tdd » (une fois par exécution suffit)
     et suivre sa boucle pour chaque tâche de code : test rouge vu échouer pour la bonne raison,
     code minimal, vert, refactorisation. Les interfaces à tester se déduisent de la tâche et de
     ses critères : le plan étant validé, on ne les redemande pas, sauf réelle ambiguïté. En
     cours de tâche, lancer souvent le typage (s'il existe) et le fichier de test concerné ; la
     suite complète attend la fin de vague.
     **Plan d'origine POC** : pas de TDD complet ; chaque tâche se vérifie par l'essai ou le test
     ciblé que le plan prévoit pour trancher l'hypothèse.
   - **Nommer le test** d'après le critère ou la règle qu'il prouve, avec son numéro si le plan en
     donne un (`AC-2`, `COM-04`), pour qu'on retrouve la preuve de chaque critère dans le bilan.
   - **Ce qui ne se teste pas automatiquement** (configuration, documentation, rendu, CSS,
     animation) : faire la vérification que le dépôt prévoit à la place (essai dans le navigateur
     avec captures, détecteur de design, commande de contrôle) et la décrire dans le compte rendu
     de la tâche. Écrire « non testable » sans rien vérifier ne suffit pas.
   - **Une fois la tâche verte** : vérifier la branche courante (`git branch --show-current`) ; si
     c'est la branche principale sans convention écrite qui l'autorise, s'arrêter et le dire.
     Cocher ensuite la case sans toucher au reste du texte du plan, puis commiter le code **et**
     le plan ensemble. Le message suit le format du dépôt (langue, préfixe, corps qui explique le
     pourquoi, lignes d'attribution) et, par défaut, un message
     conventionnel. Le corps contient `Refs: <chemin du plan>`, pour que `git log` ramène au
     contexte. Une tâche = un commit, case comprise : ainsi, une reprise ne refait jamais une tâche
     déjà commitée.
   - **Première tâche d'un plan tiré d'un ticket local** : dans ce même commit, passer le ticket
     « en cours » avec le skill `tickets`.
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

1. **Faire relire** (sauf plan d'origine POC) : appeler le Skill tool avec « review », avec le
   plan pour spec. Écrire ses remarques `R-n` dans le journal, avec leur marque de vérification
   (confirmée, douteuse, fausse), et demander lesquelles corriger, en recommandant les confirmées.
   Les retenues deviennent les tâches d'une vague « Retours de revue », exécutée en TDD comme
   les autres ; les écartées sont notées avec leur raison. Puis passer au bilan, sans nouvelle
   revue.
2. **Écrire le bilan dans le plan**, pour le relecteur : dans la section « Réalisé » si le plan en
   a une, sinon dans une section ajoutée en fin de fichier. Y mettre :
   - chaque critère, atteint (avec le test qui le prouve) ou non, et pourquoi ;
   - les écarts au plan et leur raison ;
   - les tâches ajoutées ou retirées ;
   - ce qui reste hors plan.
   Passer la ligne de statut à `> Statut : terminé le <JJ/MM/AAAA>` et commiter selon le format
   du dépôt (par défaut `docs: record plan outcome`).
   **Plan d'un jalon ou tiré d'un ticket** (ligne `Origine :`) : suivre
   [references/ending-by-origin.md](references/ending-by-origin.md), pour ce commit et pour le
   résumé de fusion (`Closes #…`).
   **Plan d'origine POC** : s'arrêter là, sans résumé de fusion ni suite Git, et proposer
   `/poc docs/poc/<slug>.md` pour écrire le verdict.
3. **Proposer un résumé de fusion**, tiré du plan : trois lignes de résumé, les critères atteints,
   une ligne par décision, le lien vers le plan. Il sert de description de pull request si le dépôt
   en utilise, sinon de récapitulatif avant la fusion.
4. **Proposer, sans l'exécuter**, la suite Git habituelle du dépôt (fusion dans la branche de
   départ, en avance rapide si c'est la convention, ou pull request) et le push s'il existe un
   dépôt distant. Ces étapes attendent un feu vert explicite. Si la session a été laborieuse
   (recherches longues, erreurs qu'un outil aurait vues), proposer aussi `/retro`.

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
- **Une décision d'architecture prise en route** (difficile à défaire, surprenante sans contexte,
  issue d'un vrai compromis) : la noter dans le journal du plan et proposer de l'enregistrer en
  appelant le Skill tool avec « adr ».
- **Un changement destructeur** (suppression de données, migration irréversible, écriture vers un
  service tiers, réécriture de l'historique) : demander une confirmation explicite, même si le
  plan le prévoit.
