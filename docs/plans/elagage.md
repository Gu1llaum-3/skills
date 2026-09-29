# Élagage des skills

> Statut : terminé le 29/09/2026
> Origine : audit des skills du 28/09/2026 (point 4), dans la conversation

## Objectif

Les skills portent des répétitions, des consignes sans effet et des listes qui dérivent : des
sections « Ce que ce skill ne fait jamais » qui redisent le corps, une phrase de langue répétée
quinze fois, des listes d'appelants fausses dans les descriptions chargées à chaque tour. Quatre
incohérences de parcours restent aussi ouvertes. Après ce plan, chaque consigne a une seule
source, en positif, et les descriptions ne portent que leurs déclencheurs.

## Décisions

- Guide : `writing-for-agents` de Matt Pocock (une seule source par consigne, pas de consigne
  sans effet, consigne positive plutôt qu'interdiction, une description = un déclencheur par cas
  distinct).
- **Sections « Ce que ce skill ne fait jamais »** : supprimées. Chaque interdiction qui n'existe
  pas ailleurs dans le skill est réécrite en consigne positive, à l'endroit du corps où elle
  s'applique.
- **Listes d'appelants** retirées des descriptions (un skill en appelle un autre par son nom) ;
  la règle correspondante du `CLAUDE.md` est retirée.
- **Descriptions des skills déclenchés par Claude** : les synonymes d'un même cas regroupés, un
  déclencheur par cas distinct. Les descriptions des skills lancés par l'utilisateur ne sont pas
  chargées pour Claude : on n'y touche pas.
- **« Réponds dans la langue de l'utilisateur »** retiré partout, sauf la consigne d'`adr` sur la
  langue des ADR existants.
- **Déplacer dans `references/`** seulement ce dont la condition est observable : « Provenance
  d'un ticket » de `plan` (source = ticket) ; les cas de fin de plan selon l'origine (jalon, POC,
  ticket) d'`implement`. « Quand ça ne va pas » et les signaux de recherche restent en place.
- **Ticket redécoupé** : après `to-tickets`, `plan` propose de fermer le ticket d'origine avec un
  lien vers les nouveaux, via `tickets`, après accord.
- Un seul commit sur `main` (convention du `CLAUDE.md`).

## Critères d'acceptation

- AC-1 : `feature` lit un fichier POC comme `brainstorming` : verdict d'abord, ce qui est décidé
  repris, les hypothèses rejouées, l'ouvert en question, le code jetable.
- AC-2 : quand `plan` fait redécouper un ticket par `to-tickets`, il propose ensuite de fermer le
  ticket d'origine avec un lien vers les nouveaux, via `tickets`, après accord.
- AC-3 : quand un jalon « gros » tient finalement en une session, `to-spec` propose de corriger
  l'envergure du cahier des charges vers « simple ».
- AC-4 : `implement`, pour un jalon sans plan, appelle `plan` sur ce jalon, comme pour un ticket.
- AC-5 : plus aucune section « Ce que ce skill ne fait jamais » ; chaque interdiction qui n'avait
  pas d'équivalent existe en consigne positive dans le corps (correspondance dans le journal).
- AC-6 : plus de « Réponds dans la langue de l'utilisateur », sauf la consigne d'`adr`.
- AC-7 : les descriptions des 13 skills déclenchés par Claude n'ont plus de liste d'appelants,
  chaque cas distinct garde un déclencheur, et leur longueur totale baisse (mesurée avant et
  après) ; `CLAUDE.md` n'exige plus les appelants.
- AC-8 : le banc d'essai, lancé après accord, ne régresse pas sur les 36 phrases historiques
  (34/36 au dernier passage).
- AC-9 : « Provenance d'un ticket » est dans `plan/references/`, pointée par « si la source est
  un ticket » ; les cas de fin de plan selon l'origine sont dans `implement/references/`, pointés
  par la ligne `Origine :` ; « Quand ça ne va pas » reste dans `implement`.

## Interfaces à tester

- Les fichiers relus et vérifiés par `grep` (AC-1 à AC-7, AC-9).
- Le banc d'essai des déclencheurs (AC-8).

## Hors périmètre

- Les descriptions des skills lancés par l'utilisateur.
- Les fins de phase de `next` (point 5 de l'audit).
- Harmoniser `**Statut :**` et `> Statut :`.

## Vague 1 : les quatre incohérences

- [x] `feature` lit un POC (AC-1) : vérification prévue : relecture contre `brainstorming`.
- [x] `plan` : fermer le ticket d'origine après redécoupage (AC-2) : vérification prévue :
  relecture.
- [x] `to-spec` : envergure corrigée vers « simple » (AC-3) : vérification prévue : relecture.
- [x] `implement` : jalon sans plan → `plan` (AC-4) : vérification prévue : relecture.

## Vague 2 : une seule source par consigne

- [x] Sections « Ce que ce skill ne fait jamais » supprimées, interdictions nouvelles réécrites
  en positif dans le corps (AC-5) : vérification prévue : `grep "ne fait jamais"`, table de
  correspondance dans le journal.
- [x] « Réponds dans la langue de l'utilisateur » retiré (AC-6) : vérification prévue : `grep`.
- [x] Déplacements dans `references/` (`plan`, `implement`) (AC-9) : vérification prévue :
  relecture des pointeurs, liens relatifs valides.

## Vague 3 : descriptions

- [x] Descriptions des 13 skills déclenchés par Claude : appelants retirés, synonymes regroupés ;
  règle du `CLAUDE.md` retirée (AC-7) : vérification prévue : longueurs avant et après, pas de
  `#`.
- [x] Banc d'essai proposé, lancé après accord (AC-8) : vérification prévue : résultat comparé à
  34/36.

## Vague 4 : Retours de revue

Retenues : R-1 à R-4, R-6 à R-10, R-12, R-14, R-15. R-5 gardée telle quelle (voir la revue).
Écartées : R-11 (la définition se lit dès la source « Ticket »), R-16 (le cas POC reste exprès,
garde-fou), R-17 (c'est à `implement` de dire quoi demander à `tickets`), R-18 (simplification
réelle, hors de ce plan), R-19 (mineur), R-20 (fausse).

- [x] Descriptions : `tickets` (changer de gestionnaire), `adr` (remplacer une décision), `debug`
  (plantage incompris, correctif s'il tient en une tâche), `implement` (modifier un plan) (R-1,
  R-2, R-3, R-8, R-9) : vérification : en-têtes YAML, texte relu.
- [x] `feature` (consigne adressée à `feature`, ligne recoupée), `CLAUDE.md` (description d'un
  skill lancé par l'utilisateur : une phrase) (R-4, R-6, R-7) : vérification : relecture.
- [x] `implement` (renvoi vers `fin-selon-origine.md`, renommé, pour le commit et `Closes #` ;
  plan non terminé pour la reprise d'un jalon), `plan` (« étapes 3, 4 et 6 » dans la seule
  référence) (R-10, R-12, R-14, R-15) : vérification : `grep` des anciens liens, fichier renommé.

## Journal

**Vague 1 (28/09/2026)**

- Livré : `feature` §1 (puce POC reprise de `brainstorming`) ; `plan` étape 3, verdict « trop
  gros » (fermer le ticket d'origine avec un lien, via `tickets`) ; `to-spec` §2 (envergure
  corrigée vers « simple ») ; `implement`, préalables (« Partir d'un jalon » : reprise ou `plan`).
- Écart : dans la description d'`implement`, « le jalon T2 » deviendra « le jalon 2 » en vague 3
  (« T2 » n'existe nulle part ailleurs).
- Vérifié : relecture de chaque passage contre sa source (`brainstorming` §1 pour le POC).

**Vague 2 (28/09/2026)**

- Livré :
  - 15 sections « Ce que ce skill ne fait jamais » supprimées (116 lignes). Interdictions sans
    équivalent, réécrites en positif dans le corps :

    | Skill | Interdiction retirée | Consigne positive |
    |---|---|---|
    | `domain-modeling` | Changer une définition existante sans le dire | « Une définition existante qui change se signale, avec l'ancienne et la nouvelle » (Pendant la session) |
    | `feature` | Écrire dans la roadmap lui-même | « rangés dans la roadmap par `tickets` » (§6) |
    | `plan` | Écrire du code | « Il écrit le plan ; le code s'écrit ensuite avec `implement` » (intro) |
    | `tickets` | Publier, fermer, modifier à distance sans accord ; réorganiser la roadmap ; changer de gestionnaire | nouvelle règle commune « Sur un gestionnaire distant… » |
    | `to-tickets` | Fermer, modifier ou supprimer un ticket existant | « Les tickets existants restent tels quels : les fermer ou les relier se propose à part » (§4) |

    Les autres puces redisaient le corps (inventaire du sous-agent) ; celle d'`implement` sur les
    tests reste portée par `tdd`.
  - « Réponds dans la langue de l'utilisateur » retiré de 15 skills ; `adr` garde « Écris l'ADR
    dans la langue des ADR existants » ; six paragraphes remis en forme.
  - `plan/references/provenance.md` (pointé depuis la source « Ticket ») ;
    `implement/references/origine.md` (jalon, ticket ; pointé par la ligne `Origine :`).
- Écart : le cas POC de la fin de plan reste dans `implement` : il arrête les étapes 3 et 4, un
  garde-fou qui doit être lu à coup sûr.
- Vérifié : `grep` (plus de « ne fait jamais », plus de « langue de l'utilisateur ») ; liens
  relatifs des deux références ; `plan` 159 → 138 lignes, `implement` 189 → 175.

**Vague 3 (28/09/2026)**

- Livré : les 13 descriptions des skills déclenchés par Claude réécrites : appelants retirés, un
  déclencheur par cas distinct, entre guillemets doubles ; 8 620 → 5 939 caractères (−31 %) ;
  « le jalon T2 » devenu « le jalon 2 » ; règle du `CLAUDE.md` réécrite (plus de liste
  d'appelants).
- Banc d'essai (un passage) : 41/42 ; sur les 36 phrases historiques, 35/36 (34/36 avant), y
  compris les deux phrases instables de `to-spec`. Seul échec : « relis le code de ma PR avant
  que je merge » a lancé `review`, alors que le piège attendait `none` ou `/code-review`.
- Écart : ce piège date d'avant `review`, dont c'est le rôle ; son attente accepte maintenant
  `review`.
- Vérifié : en-têtes YAML (guillemets appariés, pas de `#`), résultats du banc.

**Revue (28/09/2026)**

Spec :
- R-1 : `tickets` : le cas « changer de gestionnaire » n'a plus de déclencheur (AC-7).
- R-2 : `adr` : « revenir sur une décision » (la remplacer) est devenu « retrouver pourquoi » ;
  remplacer une décision n'a plus de déclencheur (AC-7).
- R-3 : `debug` : plus de phrase type pour un plantage incompris (AC-7).
- R-4 : `feature` : « rangés dans la roadmap par `tickets` » décrit `to-spec`, ce n'est pas une
  consigne pour `feature` (AC-5).
- R-5 : le piège « relis le code de ma PR » a été adapté après son échec (AC-8).
- R-6 : la règle du `CLAUDE.md` est réécrite, pas retirée ; les skills lancés par l'utilisateur
  n'ont plus de règle de description.
- R-7 : `feature` : paragraphe des lignes 22-24 remis en forme hors plan ; ligne 89 trop longue.
- R-8 : `debug` : la description promet un correctif à chaque fois (condition « tient en une
  tâche » perdue) (AC-7).
- R-9 : `implement` : l'exclusion a perdu « modifier un plan » (AC-7).
- R-10 : `implement` : le pointeur vers `origine.md` ne parle que du commit, alors que la
  référence porte aussi `Closes #` pour le résumé de fusion (AC-9).
- R-11 : `plan` : les étapes 3, 4 et 6 emploient « cadré » et « externe » sans renvoi (AC-9).
- R-12 : `implement` : un plan déjà terminé qui cite le jalon serait pris pour une reprise (AC-4).

Conventions :
- Violations : R-13 : `feature` ligne 89 trop longue (même correction que R-7).
- Jugements :
  - R-14 : possible code dupliqué : « étapes 3, 4 et 6 » dans `plan` et `provenance.md`.
  - R-15 : possible nom mystérieux : `origine.md`.
  - R-16 : possible intermédiaire : la série jalon / ticket / POC coupée entre le skill et la
    référence.
  - R-17 : possible jalousie de fonctionnalité : `origine.md` ne porte que des gestes de
    `tickets`.
  - R-18 : possibles aiguillages répétés : la règle « local / distant, après accord » dans
    `tickets`, `to-tickets`, `origine.md` et `plan`.
  - R-19 : possible code dupliqué : « Partir d'un jalon » calqué sur « Partir d'un ticket ».
  - R-20 : pertes possibles (plafond d'options de `next`, « ne pas créer `CONTEXT.md` »
    d'`onboard`). Fausse : `next:101` et `onboard:59` les portent.



**Retours de revue (29/09/2026)** : corrections faites, voir la vague 4. Descriptions : 6117
caractères au total après les déclencheurs rétablis (8 620 avant ce plan).

## Réalisé

- AC-1 à AC-4 : atteints (`feature`, `plan`, `to-spec`, `implement`), relus ; AC-4 précisé par la
  revue (plan non terminé).
- AC-5 : atteint ; les 60 puces retirées ont un équivalent dans le corps (vérifié par la revue),
  table de correspondance dans le journal.
- AC-6 : atteint (`grep`).
- AC-7 : atteint ; la revue a trouvé trois déclencheurs perdus (`tickets`, `adr`, `debug`),
  rétablis.
- AC-8 : banc d'essai 41/42, 35/36 sur les phrases historiques (34/36 avant). L'attente du piège
  « relis le code de ma PR » a été élargie à `review` après son échec : sans ce changement, 34/36,
  sans régression non plus. Les descriptions retouchées par la revue n'ont pas été rejouées.
- AC-9 : atteint (`plan/references/provenance.md`, `implement/references/fin-selon-origine.md`).
- Écarts : le cas POC reste dans `implement` ; la règle du `CLAUDE.md` est réécrite plutôt que
  retirée.
- Tâches ajoutées : la vague 4, issue de la revue.
- Hors plan : l'entrée « règle local / distant répétée » (R-18) peut rejoindre le TODO.

