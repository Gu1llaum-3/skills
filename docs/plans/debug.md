# debug : diagnostiquer un bug qui résiste

> Statut : terminé le 28/09/2026
> Origine : cadrage du 28/09/2026 (point 3 de l'audit des skills, dans la conversation)

## Objectif

Face à un bug qui résiste (intermittent, régression, cause introuvable au premier regard), Claude
lit le code et devine. `debug` l'en empêche : pas d'hypothèse tant qu'une commande n'échoue pas
sur ce bug précis. Puis il reproduit, réduit, formule des hypothèses réfutables, instrumente,
fait confirmer la cause, et corrige lui-même si le correctif tient en une tâche ; sinon il passe
la main à `plan`.

## Décisions

- D'après `diagnosing-bugs` de Matt Pocock : la boucle qui échoue est le verrou d'entrée ; les
  secrets sont masqués dans tout ce qui est montré ; l'absence d'un bon point d'entrée pour le
  test de non-régression est un résultat, pas un échec.
- **Périmètre** : diagnostic, puis correctif si celui-ci tient en une tâche (test de
  non-régression d'abord) ; sinon, le diagnostic est donné et `plan` proposé.
- **Déclenchement** : Claude peut le lancer (`plan` et `next` y renvoient), avec une description
  étroite (bug qui résiste, intermittent, régression) ; le skill commence par « si une réponse
  directe suffit, la donner ». Pièges dans le banc d'essai.
- **Point d'arrêt** : les hypothèses sont montrées sans bloquer ; une fois l'instrumentation
  finie, « Cause confirmée : X, preuve : Y. Je corrige ? » attend l'accord.
- **Trace** : l'hypothèse juste va dans le message de commit ; pas de nouveau dossier.
- **Boucle avec un humain** : pas de script fourni ; Claude demande à l'utilisateur de lancer
  une commande et de coller le résultat.
- Les façons de construire une boucle, les bugs intermittents et les régressions de performance
  vont dans `references/` : ils ne servent que dans certains cas.
- `tdd` et `debug` se départagent dans leurs descriptions : `tdd` pour un bug dont la cause est
  connue, `debug` pour un bug qui résiste.
- Nom `debug`, à vérifier après l'installation (une commande intégrée pourrait le masquer).
- Un seul commit sur `main` (convention du `CLAUDE.md`).

## Critères d'acceptation

- AC-1 : quand une réponse directe suffit (une erreur évidente, une question), `debug` la donne
  sans lancer ses phases.
- AC-2 : aucune hypothèse avant une commande nommée, déjà lancée, qui échoue sur le symptôme
  exact de l'utilisateur, sortie montrée et secrets masqués ; faute de boucle, il s'arrête, dit ce
  qu'il a essayé et demande (accès, artefact, instrumentation temporaire).
- AC-3 : il reproduit et réduit le cas ; il formule 3 à 5 hypothèses réfutables, classées, avec
  leur prédiction, montrées sans bloquer ; il instrumente une variable à la fois, avec des logs
  marqués `[DEBUG-xxxx]`.
- AC-4 : avant tout correctif, il écrit « Cause confirmée : …, preuve : … » et attend l'accord.
- AC-5 : un correctif d'une tâche passe par un test de non-régression vu rouge puis vert (ou
  l'absence de bon point d'entrée est dite), la boucle d'origine repasse au vert, les logs
  marqués sont retirés (`grep`), et le commit nomme l'hypothèse juste ; un correctif plus gros
  donne le diagnostic et propose `plan`.
- AC-6 : une régression de performance passe par une mesure de référence, puis une bissection.
- AC-7 : `plan` appelle `debug` pour un bug de cause inconnue, au lieu de prévoir une tâche de
  localisation ; il part ensuite de son diagnostic.
- AC-8 : dans `next`, « un bug qui résiste » mène à `/debug`, sans contradiction.
- AC-9 : `debug` part sur un bug intermittent ou une régression, pas sur une simple question
  d'erreur ; `tdd` garde le bug à la cause connue ; `MINE` et `evals/triggers.json` sont à jour.
- AC-10 : `README.md`, `CREDITS.md`, `TODO.md` et la carte de `next` sont à jour ; `/debug`
  lance ce skill.

## Interfaces à tester

- `debug` sur un vrai bug, dans un projet de l'utilisateur : scénario d'essai (AC-1 à AC-6).
- `plan`, `next`, `tdd` relus (AC-7, AC-8).
- Le banc d'essai des déclencheurs, lancé après accord (AC-9).
- La liste des skills d'une session neuve (AC-10).

## Hors périmètre

- La passation à une amélioration d'architecture quand aucun bon point d'entrée n'existe (Matt :
  `improve-codebase-architecture`) : le skill le dit, sans autre skill vers qui renvoyer.
- Le tri des bugs remontés par d'autres (`triage`).
- Un script de boucle avec un humain.

## Vague 1 : `debug` utilisable, et branché sur le parcours

- [x] Écrire `debug/SKILL.md` et `debug/references/boucles.md` (réponse directe d'abord, masquage,
  boucle, reproduire et réduire, hypothèses, instrumentation, cause confirmée, correctif ou
  `plan`, nettoyage ; boucles, intermittents et performance dans la référence) ; description
  étroite sans `#` (AC-1 à AC-6) : vérification prévue : relecture contre `diagnosing-bugs`, puis
  scénario d'essai.
- [x] `plan` : un bug de cause inconnue appelle `debug` (étapes 2 et 5) (AC-7) : vérification
  prévue : `grep "localisation"`.
- [x] `next` : la carte envoie le bug qui résiste vers `/debug`, la contradiction disparaît
  (AC-8) : vérification prévue : `grep "résiste"`.
- [x] Description de `tdd` : bug à la cause connue, renvoi vers `debug` sinon ; `evals` (phrases,
  pièges, `MINE`) (AC-9) : vérification prévue : JSON valide ; banc d'essai proposé.
- [x] `README.md`, `CREDITS.md`, `TODO.md` ; `./install.sh debug` (AC-10) : vérification prévue :
  relecture, lien créé ; `/debug` dans une session neuve (essai de l'utilisateur).

## Vague 2 : Retours de revue

Retenues : R-1 à R-3, R-6 à R-9, R-11, R-12, R-18. Écartées : R-4 (attendu), R-5 (ajouts fidèles
à Matt), R-14 (le skill tourne dans d'autres dépôts), R-15 (nourrit les hypothèses), R-16 (le
titre le dit), R-17 (frontière voulue), R-19 (fausse).

- [x] `debug/SKILL.md` et `references/boucles.md` : fidélité à Matt (R-3), taille évaluée avant
  « Je corrige ? » (R-6), renvoi vers l'instrumentation et la performance (R-7, R-8), nettoyage
  aussi avant de passer à `plan` (R-2), appelant de la description (R-11), doublon retiré (R-12) :
  vérification prévue : relecture.
- [x] `README.md` (schéma, R-1), `evals/triggers.json` (R-9), `next` (R-18) : vérification
  prévue : relecture, JSON valide.

## Journal

**Vague 1 (28/09/2026)**

- Livré : `debug/SKILL.md` (102 lignes, description de 725 caractères sans `#`) et
  `debug/references/boucles.md` (boucles, resserrage, intermittents, performance,
  instrumentation) ; `plan` (bug de cause inconnue → `debug`, plus de tâche de localisation) ;
  `next` (bug qui résiste → `/debug`, contradiction retirée) ; description de `tdd` (bug à la
  cause connue) ; `evals` (3 phrases dont un piège, `debug` dans `MINE`) ; `README.md`,
  `CREDITS.md`, `TODO.md` ; lien `~/.claude/skills/debug`.
- Vérifié : relecture de `debug` contre `diagnosing-bugs` (six phases, masquage, critère de fin de
  la boucle, point d'entrée absent) ; `grep` : plus de « localisation » dans `plan`, plus de
  contradiction dans `next` ; JSON du banc valide (42 phrases) ; lien créé.
- Non vérifié : le comportement réel de `debug` (scénario d'essai sur un vrai bug), `/debug` dans
  une session neuve, le banc d'essai.

**Revue (28/09/2026)**

Spec :
- R-1 : le schéma « Enchaînement » du README ne parle pas de `debug` (AC-10).
- R-2 : le nettoyage (logs marqués, bancs jetables) n'est écrit que quand `debug` corrige ; rien
  quand il passe la main à `plan` (AC-5).
- R-3 : fidélité à Matt : reproduire sur plusieurs lancers, noter le symptôme exact, ne pas
  avancer avant d'avoir reproduit et réduit ; « si la sortie masquée ne suffit pas, demander ».
- R-4 : `/debug` pas encore essayé, commit pas encore fait : attendus (essai de l'utilisateur,
  fin du plan).
- R-5 : ajouts fidèles à Matt non demandés (lecture de `CONTEXT.md`, resserrer la boucle,
  préférence d'outils) et exemple changé dans `next`.
- R-6 : « Je corrige ? » est posé avant de savoir si le correctif tient en une tâche (AC-4).
- R-7 : l'étape 4 ne renvoie pas à la section « Instrumenter » de la référence (AC-3).
- R-8 : la branche performance n'apparaît pas à l'étape 4 (AC-6).
- R-9 : le piège « TypeError… » attend `none` seul, alors qu'AC-1 laisse `debug` répondre
  directement (AC-9).

Conventions :
- Violations :
  - R-10 : schéma du README (même correction que R-1).
  - R-11 : la description cite `next` comme appelant ; il ne fait que proposer `/debug`.
- Jugements :
  - R-12 : possible code dupliqué : « pas « ne plante pas » » dans le skill et la référence.
  - R-13 : possible code dupliqué : « Instrumenter » dans le skill et la référence (même
    correction que R-7).
  - R-14 : possible code dupliqué : « commiter selon le format du dépôt » répète `CLAUDE.md`.
  - R-15 : possible généralité spéculative : lire `CONTEXT.md` et les ADR.
  - R-16 : possible nom mystérieux : `references/boucles.md` contient plus que les boucles.
  - R-17 : possible chirurgie au fusil : la frontière `tdd` / `debug` est écrite à 4 endroits.
  - R-18 : ligne trop longue dans `next` (« fonctionnalité) : le dire… »).
  - R-19 : pas de phrase « bug à cause connue → tdd » dans le banc. Fausse : la phrase de la TVA
    existe déjà.

**Vague 2 : Retours de revue (28/09/2026)**

- Corrigé : R-1 (schéma du README : ligne « bug qui résiste »), R-2 (nettoyage avant de passer à
  `plan`), R-3 (plusieurs lancers, symptôme noté, pas d'hypothèse avant reproduit et réduit,
  sortie masquée insuffisante), R-6 (taille évaluée avant la question, qui propose « je corrige »
  ou « je passe à `plan` »), R-7 et R-8 (étape 4 : débogueur d'abord, performance, renvoi vers la
  référence), R-9 (le piège accepte `none` ou `debug`), R-11 (seul `plan` cité comme appelant),
  R-12 (doublon retiré de la référence), R-18 (ligne recoupée dans `next`).
- Écart : quand le correctif est plus gros, `debug` appelle `plan` après l'accord au lieu de
  seulement le proposer (même question, une étape de moins).
- Vérifié : relecture, JSON valide ; `debug/SKILL.md` fait 110 lignes.

## Réalisé

- AC-1 à AC-6 : écrits dans `debug/SKILL.md` et sa référence, relus contre `diagnosing-bugs` et
  par `review` ; **non vérifiés en réel** : le scénario d'essai sur un vrai bug reste à faire.
- AC-7, AC-8 : atteints (`plan`, `next`), vérifiés par `grep`.
- AC-9 : descriptions départagées, phrases et `MINE` à jour ; le banc d'essai n'a pas tourné (à
  lancer après accord).
- AC-10 : fichiers à jour, lien créé ; **non vérifié** : `/debug` dans une session neuve.
- Tâches ajoutées : la vague 2, issue de la revue.
- Hors plan : rien de nouveau.

