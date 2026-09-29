# brainstorming : les idées du brainstorming de superpowers

> Statut : terminé le 29/09/2026
> Origine : cadrage du 29/09/2026 (comparaison avec obra/superpowers, skills/brainstorming)

## Objectif

`/brainstorming` mène toujours à un cahier des charges, ne relit pas ce qu'il écrit, découpe
tard et ne sépare pas ce que l'utilisateur a dit de ce que Claude suppose. On reprend de
superpowers l'annonce du chemin, le découpage d'emblée, le dit et le supposé, les 2 ou 3
approches et l'auto-relecture ; la relecture passe aussi dans `to-spec`, l'annonce du chemin
(avec le renvoi vers `/poc`) dans `feature`.

## Décisions

- Le cahier des charges reste le chemin par défaut. L'étape 2 annonce le chemin, que
  l'utilisateur peut corriger : question de faisabilité → `/poc` ; petit outil qui tient en une
  session → synthèse en conversation (format de l'étape 5 de `feature`) puis `plan` ; sinon
  cahier des charges. On ne redescend jamais en cours de route, on peut monter. Le petit
  outil saute la création de la roadmap de l'étape 6 (pas de jalons sans cahier des charges).
- Pas de sous-skill pour le cahier des charges.
- Relecture avant de montrer le document : champs à compléter oubliés, contradictions, phrases
  qu'on peut lire de deux façons, taille. Corriger sans la montrer.
- Découpage d'emblée : plusieurs sous-systèmes indépendants se signalent à l'étape 2, avant les
  questions de détail ; on cadre le premier, les autres deviennent des jalons.
- Restitution : l'intention et les critères de réussite, en séparant ce que l'utilisateur a dit
  de ce que Claude suppose.
- 2 ou 3 approches d'ensemble (compromis, recommandation en premier) en ouverture du thème
  « Technique et contraintes » de l'entretien, pas dans une étape à part : la numérotation ne
  bouge pas (`to-questionnaire` renvoie à « l'étape 5 de `brainstorming` »). Elles portent sur le
  produit et les choix structurants, pas sur les modules : le comment reste à `to-spec` et `plan`.
- `feature` annonce son chemin : question de faisabilité → `/poc` ; trop gros pour une session →
  déjà couvert par `to-spec`. Pas de renvoi vers `/brainstorming` (un seul cahier des charges par
  projet, écrit pour un nouveau projet).
- `plan` accepte la synthèse en conversation venue de `brainstorming`, comme celle de `feature`.
- `CREDITS.md` : superpowers dans une section « Idées reprises » (rien n'est traduit tel quel).

## Critères d'acceptation

- AC-1 : `brainstorming/SKILL.md` annonce le chemin à l'étape 2, avec ses trois sorties et la
  règle « on monte, on ne redescend pas » ; sa description ne promet plus le cahier des charges
  sans condition.
- AC-2 : `brainstorming` et `to-spec` relisent leur document (les quatre vérifications) avant de
  le montrer.
- AC-3 : `brainstorming` signale le découpage à l'étape 2, reformule le dit et le supposé, et
  propose 2 ou 3 approches en ouverture du thème technique ; ses étapes gardent leurs numéros.
- AC-4 : `feature` annonce son chemin et sait renvoyer vers `/poc`.
- AC-5 : `README.md` (tableau et schéma), `CREDITS.md`, `TODO.md` (ligne cochée) et, si besoin,
  la carte de `next/SKILL.md` sont à jour.
- AC-6 : chaque SKILL.md reste sous 500 lignes ; un seul commit en français sur `main`.
- AC-7 : `plan` lit la synthèse en conversation de `brainstorming` ; le chemin du petit outil ne
  propose pas de roadmap ; aucun renvoi d'un autre skill vers une étape de `brainstorming` n'est cassé.
- AC-8 : `CLAUDE.md` demande, pour tout changement, de vérifier qu'il ne casse rien et reste
  cohérent avec les skills qui appellent le skill modifié, qu'il appelle, ou qui renvoient à ses
  étapes, fichiers et formats.

## Interfaces à tester

- `brainstorming/SKILL.md`, `to-spec/SKILL.md`, `feature/SKILL.md` : relecture des étapes
  modifiées et `wc -l` (AC-1 à AC-4, AC-6).
- Scénario d'essai proposé à l'utilisateur : `/brainstorming` sur une idée de petit script, puis
  sur une idée de plateforme à plusieurs sous-systèmes (AC-1, AC-3).

## Hors périmètre

- Le « visual companion », la validation section par section, le tableau de « Red Flags ».
- Rendre `brainstorming` déclenchable par Claude.
- `evals/run_triggers.py` : aucune description de skill déclenchable par Claude ne change.

## Vague 1 : le parcours de cadrage plus souple et plus sûr

- [x] `brainstorming` : description, étape 2 (chemin, découpage, dit et supposé), approches dans
  le thème technique, relecture avant de montrer le cahier des charges, étape 6 sans roadmap pour
  le chemin du petit outil (AC-1, AC-2, AC-3, AC-7) : vérification prévue : relecture, `wc -l`
- [x] `plan` : source « Conversation » venue de `feature` ou de `brainstorming` (AC-7) :
  vérification prévue : relecture
- [x] `to-spec` : relecture du brouillon à l'étape 3 (AC-2) : vérification prévue : relecture
- [x] `feature` : annonce du chemin à l'étape 2 et renvoi vers `/poc` (AC-4) : vérification
  prévue : relecture
- [x] `CLAUDE.md` : la vérification de cohérence dans « Travail » (AC-8) : vérification prévue :
  relecture
- [x] `README.md`, `CREDITS.md`, `TODO.md`, carte de `next` si besoin, puis commit unique (AC-5,
  AC-6) : vérification prévue : `grep -rn "brainstorming" --include='*.md'` (renvois d'étapes
  intacts), `git show --stat`

## Journal

**Vague 1 (29/09/2026)**

- Livré :
  - `brainstorming` : description (cahier des charges, ou synthèse pour un petit outil), intention avec le dit
    et le supposé, découpage et chemin dans l'étape 2 (`/poc`, petit outil → synthèse puis `plan`,
    sinon cahier des charges ; on monte, on ne redescend pas), 1 ou 2 séries pour un petit outil,
    approches en ouverture du thème technique, relecture en quatre points avant de montrer le
    cahier des charges et après chaque version (117 lignes) ;
  - `plan` : la source « Conversation » et le saut de l'exploration valent aussi pour
    `brainstorming` ;
  - `to-spec` : relecture du brouillon à l'étape 3 ;
  - `feature` : point 4 de la restitution, le chemin (`/poc` pour une question de faisabilité) ;
  - `CLAUDE.md` : la vérification contre les skills rattachés, avant le plan et avant le commit ;
  - `README.md` (tableau, schéma), `CREDITS.md` (section « Idées reprises », superpowers sous
    MIT, vérifié sur le dépôt), `TODO.md` (ligne cochée, essai ajouté).
- Écarts : la synthèse du petit outil liste ses rubriques dans `brainstorming` au lieu de
  renvoyer à « l'étape 5 de `feature` » : ce renvoi aurait créé un nouveau numéro d'étape à
  surveiller. Carte de `next` inchangée : le chemin du petit outil laisse un plan dans `docs/plans/`,
  qu'elle sait déjà reprendre.
- Vérifié : les titres d'étapes de `brainstorming`, `feature` et `to-spec` n'ont pas bougé ;
  `grep` des renvois d'étapes (« l'étape 5 de `brainstorming` » de `to-questionnaire` tombe
  toujours sur « Trancher les questions ouvertes ») ; description de `brainstorming` sans `#` ni
  « : » (210 caractères) ; tous les SKILL.md sous 180 lignes.
- Non vérifié : le comportement réel (scénario d'essai à lancer), le banc d'essai (aucune
  description déclenchable par Claude n'a changé).

**Retours de revue (29/09/2026)** : deux sous-agents, spec et conventions ; aucune violation d'une
règle écrite, aucun renvoi entre skills cassé.

- Corrigés :
  - R-1 : schéma du `README.md`, `feature` → `/poc` ;
  - R-2 : étape 6 de `brainstorming` réservée au cahier des charges (« quelle que soit
    l'envergure » contredisait le petit outil) ;
  - R-3 : thème 6 de l'entretien, la synthèse pour un petit outil ;
  - R-4 : titre et objectif de `brainstorming` ;
  - R-6 : la synthèse du petit outil est relue comme le cahier des charges ;
  - R-8 : `plan` ne saute l'exploration après `brainstorming` que pour un petit outil ;
  - R-12 : un seul nom, « petit outil » ;
  - R-13 : ordre des critères du plan ;
  - R-14 : ajouts de `brainstorming` à l'impératif tutoyé, double ligne vide ;
  - R-15 : la règle `CREDITS.md` du `CLAUDE.md` couvre les idées reprises.
- Écartés :
  - R-5 : pas de rubrique « Taille » dans la synthèse du petit outil (la taille est tranchée à
    l'étape 2), ni de renvoi à celle de `feature` (un numéro d'étape de plus à surveiller) ;
  - R-7 : ajouts hors plan gardés (le chemin le plus lourd dans le doute, relecture de chaque
    version, règle `CLAUDE.md` détaillée à la demande de l'utilisateur, ligne d'essai) ;
  - R-9, R-10 : relecture et annonce du chemin proches dans deux skills, mais adaptées à chacun ;
  - R-11 : renvois internes à `brainstorming` par numéro d'étape, risque faible.

## Réalisé

- AC-1 à AC-5, AC-7, AC-8 : atteints, vérifiés par relecture, `grep` des renvois et les deux
  sous-agents de revue (pas de test automatique dans ce dépôt).
- AC-6 : SKILL.md tous sous 180 lignes ; un seul commit.
- Tâches ajoutées : `plan` (source « Conversation ») et `CLAUDE.md` (AC-8, à la demande de
  l'utilisateur).
- Hors plan : le comportement réel reste à essayer (ligne de `TODO.md`).
