# next : les fins de phase

> Statut : terminé le 29/09/2026
> Origine : cadrage du 29/09/2026 (point 5 de l'audit des skills, dans la conversation)

## Objectif

La ligne de session de `/next` connaît trois gestes (continuer, `/clear`, `/compact`) sans ordre
ni condition claire. En reprenant l'arbre des fins de phase d'`ask-matt`, elle devient un arbre
court et ordonné : continuer d'abord, `/compact` en dernier, avec le sous-agent pour ce qui
tourne seul, la passation par `/to-spec`, et aucune décision de session au milieu d'une phase.

## Décisions

- D'après `PHASE-BOUNDARIES.md` de Matt Pocock, dans le corps de `next` (chaque réponse porte la
  ligne de session), sous la forme d'un arbre dont la première réponse « oui » l'emporte :
  1. **continuer ici** si la suite a besoin de cette conversation comme source (cadrage → plan)
     et qu'elle n'est pas trop longue : un résumé perd le pourquoi ;
  2. **`/clear` puis la commande** si rien de la conversation ne sert plus : la suite part d'un
     fichier qui se suffit (plan validé, ticket) ;
  3. **`/to-spec`** si le travail doit voyager (autre session plus tard, autre dossier, autre
     outil, un collègue) : il écrit une spec ou un ticket qui se suffit ;
  4. **un sous-agent** pour une tâche bien bornée qui peut tourner sans l'utilisateur
     (recherche, relecture) : la session reste intacte ;
  5. sinon, **`/compact` avec une consigne** qui dit ce que la suite doit garder.
- **Au milieu d'une phase** (en pleine vague, en plein entretien) : continuer, ou confier un
  morceau à un sous-agent ; la question de la session se pose à la fin de la phase.
- **Garder entretien, spec et tickets dans une même conversation**, puis une session vide par
  `/implement <ticket>`.
- **Conversation trop longue** : sans seuil chiffré (« très longue, ou déjà compactée »).
- Un seul commit sur `main` (convention du `CLAUDE.md`).

## Critères d'acceptation

- AC-1 : la ligne de session suit l'arbre, dans l'ordre : continuer, `/clear`, `/to-spec`,
  sous-agent, `/compact` avec une consigne.
- AC-2 : lancé au milieu d'une phase, `next` conseille de continuer ou de confier un morceau à un
  sous-agent, jamais `/clear` ni `/compact`.
- AC-3 : après un cadrage qui mène à des tickets, `next` conseille de rester dans la même
  conversation jusqu'aux tickets, puis une session vide par `/implement <ticket>`.
- AC-4 : aucun seuil chiffré de taille de conversation.

## Interfaces à tester

- `next/SKILL.md`, relu contre `PHASE-BOUNDARIES.md` (AC-1 à AC-4).
- Un scénario d'essai proposé à l'utilisateur.

## Hors périmètre

- Un skill de passation à part (le handoff de Matt) : `/to-spec` en tient lieu.
- La description de `next` (lue seulement par l'utilisateur).

## Vague 1 : l'arbre des fins de phase

- [x] Remplacer la « ligne de session » de `next` par l'arbre, la règle du milieu de phase et
  celle des tickets (AC-1 à AC-4) : vérification prévue : relecture contre `PHASE-BOUNDARIES.md`.
- [x] Retirer l'entrée du `TODO.md` et proposer le scénario d'essai : vérification prévue :
  relecture.

## Vague 2 : Retours de revue

Retenues : R-1, R-5 à R-11, R-15, R-16. Écartées : R-2 (le « ou » de Matt ferait continuer une
conversation qui ne sert plus, contre sa propre règle d'une session vide par ticket), R-3 (écart
noté), R-4 (suite logique de l'arbre), R-14 (le sous-agent n'a pas le même moment dans les deux
cas), R-17 (l'introduction du §4 donne des exemples de phases).

- [x] `next` : gabarit « <un geste de la section 4> » et renvoi du §3 (R-5, R-16) ; branche 1 qui
  porte la règle cadrage → tickets et « à examiner en premier » (R-9, R-11) ; branche 3 limitée
  au travail qui n'est encore écrit nulle part, et sans doublon quand la recommandation est
  `/to-spec` (R-6, R-7) ; branche 4 sans sous-agent quand le skill en lance déjà (R-10) ; phrase
  contradictoire de la branche 5 retirée (R-8) ; milieu de phase en positif (R-1, R-15) :
  vérification : relecture de l'arbre de bout en bout.

## Journal

**Vague 1 (29/09/2026)**

- Livré : `next` §4 « La ligne de session » (arbre en cinq branches, milieu de phase, cadrage →
  tickets) ; gabarit de réponse élargi aux cinq gestes ; entrée du `TODO.md` cochée.
- Écart : l'entrée du `TODO.md` est cochée avec un résumé plutôt que retirée, comme les autres
  pistes faites.
- Vérifié : relecture contre `PHASE-BOUNDARIES.md` (ordre des cinq gestes, règle de la frontière,
  une fenêtre de l'entretien aux tickets, aucun seuil chiffré) ; `next` fait 129 lignes.
- Quoi essayer : en fin de cadrage, `/next` doit dire « continuer ici » ; au milieu d'une vague
  d'`implement`, il doit dire de continuer, sans `/clear` ni `/compact` ; après un ticket
  terminé, « `/clear` puis `/implement <ticket suivant>` ».

**Revue (29/09/2026)**

Spec :
- R-1 : au milieu d'une phase, `/clear` n'est exclu qu'implicitement (AC-2).
- R-2 : branche 1 : Matt continue si la suite a besoin de la conversation **ou** s'il reste de la
  place ; ici les deux conditions sont exigées.
- R-3 : l'entrée du `TODO.md` est cochée au lieu d'être retirée (écart déjà noté).
- R-4 : le gabarit passe à cinq gestes sans que l'AC le demande.
- R-5 : pas de ligne vide avant `## 4.`, et le §3 ne renvoie plus au §4.
- R-6 : quand la recommandation est déjà `/to-spec`, la ligne « `/to-spec` d'abord » fait
  doublon.
- R-7 : branche 3 « une autre session plus tard » empiète sur la branche 2 quand un plan ou un
  ticket se suffit déjà.
- R-8 : « Une conversation très longue… y mène plus vite » contredit « la première réponse oui
  l'emporte ».
- R-9 : « Cadrage → tickets » redit la branche 1.
- R-10 : le sous-agent comme ligne de session tombe mal quand le skill recommandé (`research`,
  `review`) lance déjà les siens.

Conventions :
- Violations : aucune.
- Jugements :
  - R-11 : possible nom mystérieux : « à écarter en premier » peut se lire « à rejeter ».
  - R-12 : possible code dupliqué : la condition de longueur en branches 1 et 5 (même correction
    que R-8).
  - R-13 : possible code dupliqué : « Cadrage → tickets » répète la branche 1 et la carte (même
    correction que R-9).
  - R-14 : possible code dupliqué : le milieu de phase reprend la branche 4 (sous-agent).
  - R-15 : formulation négative au milieu de phase (« ne se décide pas », « fait perdre le fil »).
  - R-16 : possibles aiguillages répétés : le gabarit du §3 recopie les cinq gestes du §4.
  - R-17 : « phase » et « geste » sans définition ; « un sous-agent » sans contenu dans le
    gabarit.

## Réalisé

- AC-1 : atteint (§4, cinq gestes dans l'ordre).
- AC-2 : atteint après R-1 : au milieu d'une phase, seuls « continuer ici » et le sous-agent sont
  proposés.
- AC-3 : atteint, porté par la branche 1 après R-9.
- AC-4 : atteint (aucun seuil chiffré).
- Écarts : entrée du `TODO.md` cochée plutôt que retirée ; condition « et » de la branche 1
  gardée contre le « ou » de Matt (R-2).
- Non vérifié : le comportement réel (scénario d'essai du journal).
- Tâches ajoutées : la vague 2, issue de la revue.

