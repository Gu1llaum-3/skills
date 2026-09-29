# Page des skills : carte, parcours et fichiers

> Statut : terminé le 29/09/2026
> Origine : cadrage du 29/09/2026 (`/feature`, dans la conversation)

## Objectif

Avec 21 skills, on ne retient plus qui appelle qui ni lequel lancer à quel moment : l'information
est éparpillée entre le schéma du `README.md`, la carte de `next/SKILL.md` et les appels écrits
dans chaque `SKILL.md`. Une page `docs/skills.html`, générée par un script depuis les `SKILL.md`
et un gabarit, montre la carte des appels, les parcours par situation, un jeu « quel skill ? »
et les fichiers d'un projet, aux couleurs de Claude.

## Décisions

- **Format** d'après le guide « Claude Code, réglé pour l'équipe » (artifact `9p9ykMYRwjcPGYDNEM9rV5`) :
  barre du haut fixe avec les étapes numérotées, grande introduction avec l'itinéraire numéroté,
  sections à grand numéro, notices et cartes à retourner.
- **Carte** d'après l'atlas des skills Pocock (artifact `FBMfH9rpfVHgKJLzi9tx38`) : deux colonnes
  (toi seul les lances / toi ou Claude), groupées par rôle, cliquables, avec un panneau
  « Appelle / Appelé par / Ensuite / Produit / Dans les parcours ».
- **Sections** : ① La carte, ② Les parcours (nouveau projet ; feature ou POC ; ticket ou bug ; à
  tout moment), ③ Quel skill ? Testez-vous, ④ Les fichiers d'un projet, ⑤ Les règles du jeu.
- **Généré depuis les `SKILL.md`** : nom, description, famille (`disable-model-invocation`), et
  appels « Skill tool avec « x » », en tolérant un retour à la ligne au milieu de la formule
  (`interview` → `domain-modeling`), plus le tableau « La carte » de `next/SKILL.md` pour la
  section ③. **Écrit à la main** dans le gabarit : groupes de la carte, « Ensuite », parcours,
  fichiers, règles.
- **Fichiers** : `docs/build_skills_page.py` (Python 3, bibliothèque standard seulement, comme
  `evals/`), `docs/skills.template.html` (gabarit, avec un emplacement pour les données en JSON),
  `docs/skills.html` (généré, versionné). La page cite le commit court et la date.
- **Couleurs Claude** : fond `#faf9f5`, encre `#141413`, corail `#d97757` (skills lancés par
  l'utilisateur), bleu ardoise `#6a9bcc` (skills déclenchés par Claude), filets `#e8e6dc`, gris
  `#b0aea5` ; sombre sur `#262624`. Polices : Poppins (titres) et Lora (texte), charte Anthropic,
  via Google Fonts.
- **Français seulement.**

## Critères d'acceptation

- AC-1 : `python3 docs/build_skills_page.py` produit `docs/skills.html`, sans dépendance hors
  bibliothèque standard ; la page ne charge que Google Fonts.
- AC-2 : la carte montre les 21 skills, chacun dans sa famille, et tous les appels des
  `SKILL.md`, dont `interview` → `domain-modeling`.
- AC-3 : un appel ajouté dans un `SKILL.md` apparaît sur la carte après avoir relancé le script ;
  un skill ajouté apparaît aussi, dans un groupe « Autres » s'il n'a pas de groupe dans le gabarit.
- AC-4 : cliquer un skill (dans la carte, un parcours, une carte « Quel skill ? » ou une notice
  de fichier) affiche sa fiche dans le panneau de la carte.
- AC-5 : la page se lit à 375 px sans défilement horizontal de la page (seule la carte défile
  dans son cadre), en thème clair et sombre.
- AC-6 : `CLAUDE.md` (« Commandes » et « Travail ») et `README.md` disent de relancer le script
  après un changement de skill.

## Interfaces à tester

- `build_skills_page.py`, fonctions d'extraction (frontmatter, appels, tableau de `next`) :
  `docs/test_build_skills_page.py` (unittest), sur de petits `SKILL.md` écrits dans un dossier
  temporaire, et sur le dépôt réel pour AC-2 (AC-1, AC-2, AC-3).
- La page ouverte dans le navigateur : clics, largeur 375 px, thème sombre (AC-4, AC-5).

## Hors périmètre

- Bouton de langue FR/EN.
- Une page par skill.
- Vérification automatique (CI ou banc d'essai) que la page est à jour.
- Publication en artifact (possible ensuite, sur demande).

## Vague 1 : la carte des appels, générée, aux couleurs de Claude

- [x] Extraction et génération : frontmatter, appels (retour à la ligne toléré), injection en
  JSON dans le gabarit ; le gabarit a la barre du haut, l'introduction, la section ① La carte
  (colonnes, groupes, traits, panneau, filtre par famille) et le pied de page daté ; tests
  unitaires de l'extraction (AC-1, AC-2, AC-3, AC-4)

Pause : l'utilisateur ouvre `docs/skills.html` et valide le style avant la suite.

## Vague 2 : parcours, jeu, fichiers et règles

- [x] Section ② Les parcours : quatre onglets de situations, étapes et embranchements, d'après
  l'« Enchaînement » du `README.md` et la ligne de session de `next` ; chaque skill cliquable
  ouvre sa fiche (AC-4)
- [x] Section ③ Quel skill ? Testez-vous : cartes à retourner générées depuis le tableau de
  `next/SKILL.md`, avec test unitaire de l'extraction du tableau (AC-3, AC-4)
- [x] Sections ④ Les fichiers d'un projet (arborescence et notice : qui l'écrit, qui le lit) et
  ⑤ Les règles du jeu ; le panneau de la carte gagne « Produit » (AC-4)
- [x] `CLAUDE.md` et `README.md` : commande de génération, et relance à ajouter dans « Travail » ;
  vérification prévue : page ouverte à 375 px et en thème sombre (AC-5, AC-6)

## Vague 3 : Retours de revue

- [x] R-1, R-2, R-9, R-10 : le script range un skill sans groupe dans « Autres », dans la
  colonne de sa famille (testé) ; le test du dépôt réel vérifie que chaque skill a un groupe
  dans le gabarit, au lieu de figer 21 skills ; `CLAUDE.md` le dit dans « Travail »
- [x] R-11 : les `SKILL.md` ne sont lus qu'une fois par génération
- [x] R-3, R-13, et retour de l'utilisateur : pied de page « généré après le commit » ;
  `inFlows` parcourt la structure ; « Quel skill ? » montre 5 situations tirées au hasard, avec
  un bouton pour 5 autres (22 à la fois, c'était trop) ; vérification prévue : captures de ③ à
  ⑤, et du sombre à 375 px (R-5)

Retenues : R-1, R-2, R-3, R-9, R-10, R-11, R-13, et R-5 pour les captures. R-4 et R-6 sont
déclarés au bilan. Écartées : R-7 et R-14 (générer les groupes, les parcours et les fichiers
serait un chantier à part), R-12 (noms courts repris de l'atlas, locaux au script de la page).

## Journal

### Vague 1 (29/09/2026)

- **Livré** : `docs/build_skills_page.py` (`load_skills`, `build_page`), `docs/skills.template.html`
  (barre du haut et itinéraire construits d'après les sections présentes, introduction, carte,
  panneau, filtre par famille, pied de page daté), `docs/skills.html` généré,
  `docs/test_build_skills_page.py` (6 tests, verts).
- **Écarts** :
  - carte en **trois colonnes** au lieu de deux (tu les lances / le parcours / en cours de
    route) : ici, beaucoup de skills que Claude peut lancer s'appellent entre eux, et une seule
    colonne à droite aurait tout mis en arcs ;
  - le panneau sépare la description en « rôle » et « Se déclenche », en coupant à
    « Utilise ce skill quand » ;
  - pas de commit par tâche : la convention du dépôt (un seul commit par changement, sur `main`)
    prime ; tout sera commité ensemble en fin de plan.
- **Vérifié** : `python3 -m unittest docs/test_build_skills_page.py` (code 0) ; captures de
  Chrome sans interface à 1400 px (thème sombre) et à 375 px dans un cadre : pas de défilement
  horizontal, la carte défile dans le sien. Premier essai à 375 px : la page débordait (colonne
  de grille en `1fr` élargie par le SVG), corrigé en `minmax(0, 1fr)`.
- **Pas vérifié** : le thème clair en capture (la capture sort en sombre) ; le groupe « Autres »
  pour un skill sans groupe (AC-3) est du code de la page, sans test automatique.
- **Quoi essayer** : `python3 docs/build_skills_page.py && open docs/skills.html`, puis :
  1. cliquer `implement` : 5 traits vers `plan`, `review`, `tdd`, `adr`, `tickets`, et
     « Appelé par » vide ;
  2. filtre « Toi seul » : seuls les 8 skills corail et leurs traits restent vifs ;
  3. ouvrir `docs/skills.html#interview` : le panneau s'ouvre sur `interview`, avec son trait
     vers `domain-modeling`.
- **Retour d'essai** : « Tu les lances » laissait croire que `implement`, `review`… ne se tapent
  pas. Tous se tapent avec `/nom` : les familles s'appellent désormais « Toi seul »
  (`disable-model-invocation`) et « Toi ou Claude » (colonne, légende, filtre, badge,
  introduction). Contrôle de design : marges des boutons du panneau élargies (4px 10px) ; filet
  du haut de l'itinéraire ignoré comme « side-tab » (`.impeccable/config.json`).


### Vague 2 (29/09/2026)

- **Livré** : sections ② Les parcours (4 onglets : nouveau projet, feature, ticket ou bug, à tout
  moment), ③ Quel skill ? (22 cartes générées depuis la carte de `next`, bouton « Tout
  retourner »), ④ Les fichiers (14 fichiers, notice « Écrit par / Relu par / Bon à savoir »), ⑤
  Les règles du jeu (8 règles) ; le panneau de la carte gagne « Écrit » et « Dans les parcours » ;
  `load_situations` et son test ; `CLAUDE.md` (Commandes, Travail) et `README.md` (« La page des
  skills »).
- **Écarts** :
  - « Relu par » vient d'un `grep` des chemins dans les `SKILL.md`, recopié à la main dans le
    gabarit (sans l'écrivain) : il ne se met pas à jour seul ;
  - la ligne `/code-review` de la carte de `next` est écartée : ce n'est pas un skill du dépôt.
- **Vérifié** : `python3 -m unittest docs/test_build_skills_page.py` (7 tests, code 0) ;
  `node --check` sur le script de la page ; captures en thème clair à 1400 px et à 375 px dans un
  cadre (pas de défilement horizontal) ; DOM : 14 fichiers dans l'arbre, 22 réponses cachées au
  départ.
- **Bugs trouvés en route** : les réponses du jeu étaient visibles d'emblée (la page autonome n'a
  pas de règle `[hidden]`, et `.ans { display: grid }` passait devant) ; « gardés . » en fin de
  première phrase. Corrigés tous les deux.
- **Pas vérifié** : les sections ④ et ⑤ en capture (hors du cadre de la capture, vérifiées par
  le DOM seulement) ; le clavier dans les onglets des parcours.
- **Quoi essayer** : `python3 docs/build_skills_page.py && open docs/skills.html`, puis :
  1. onglet « Un ticket ou un bug » : trois branches, et `review` en étape 2 ;
  2. dans le panneau de `plan`, « Écrit » → `docs/plans/` : la page descend à la notice ;
  3. « Tout retourner » dans ③, puis cliquer un nom de skill sur une carte : retour à la carte.

### Revue (29/09/2026)

Spec :
- R-1 : un nouveau skill sans groupe va toujours dans « Autres » à droite, même s'il est
  « Toi seul » (AC-2, AC-3) ; plus largement, la colonne suit le gabarit, pas le drapeau.
- R-2 : le groupe « Autres » (AC-3) n'a pas de test automatique.
- R-3 : le pied de page cite le commit qui précède la génération, jamais celui qui contient la
  page (Décisions : « cite le commit court »).
- R-4 : « Produit » du panneau est devenu « Écrit », sans être déclaré.
- R-5 : pas vérifiés : le clavier dans les onglets, ④ et ⑤ en capture, le sombre à 375 px (AC-4,
  AC-5).
- R-6 : ajouts non prévus : JetBrains Mono (toujours Google Fonts), `.impeccable/config.json`.
- R-7 : « Relu par » est recopié à la main (écart déclaré).

Conventions :
- R-8 : statut pas encore « terminé », pas de bilan (à faire à la clôture).
- R-9 : la liste « Travail » du `CLAUDE.md` ne dit pas que `docs/test_build_skills_page.py` casse
  à l'ajout d'un skill.
- R-10 (jugement) : possible chirurgie au fusil : le test sur le dépôt réel fige 21 skills et la
  liste des 8 « Toi seul ».
- R-11 (jugement) : possible code dupliqué : les `SKILL.md` sont relus trois fois
  (`load_situations`, `build_page`, `__main__`).
- R-12 (jugement) : possible nom mystérieux : clés d'une lettre (`q`, `s`, `p`, `w`, `r`…),
  constantes `NW`, `GH`, `GG`.
- R-13 (jugement) : possible obsession des primitifs : `inFlows` cherche dans
  `JSON.stringify(f.steps)`.
- R-14 (jugement) : possible chirurgie au fusil : `COLUMNS`, `NEXT`, `FLOWS`, `FILES` à la main ;
  un renommage se corrige à quatre endroits.

### Vague 3 (29/09/2026)

- **Livré** : `ungrouped` (skills sans groupe, par famille, injectés en `DATA.others`) et son
  test ; le test du dépôt réel vérifie que chaque skill a un groupe, au lieu de figer 21 skills ;
  lecture unique des `SKILL.md` ; `inFlows` parcourt la structure ; pied de page « après le
  commit » ; « Quel skill ? » à 5 cartes tirées au hasard, sans répétition jusqu'à la fin du
  paquet ; `CLAUDE.md` (« Travail ») dit que le test échoue tant qu'un skill n'a pas de groupe.
- **Vérifié** : 8 tests, code 0 ; `node --check` ; `tdd` retiré du gabarit en mémoire :
  `ungrouped` le rend dans `m` ; captures de ③ à ⑤ en clair à 1400 px et de toute la page en
  sombre à 375 px (pas de défilement horizontal).
- **Bug trouvé en route** : la liste de « La ligne de session » empilait chaque mot (grille à
  deux colonnes sur un `<li>` à enfants multiples) ; corrigée par un numéro positionné.

## Réalisé

- AC-1 : atteint. `test_ac1_page_generee_avec_les_donnees_a_la_place_du_marqueur` ; le script
  n'importe que la bibliothèque standard, la page ne charge que Google Fonts.
- AC-2 : atteint. `test_ac2_famille_lue_dans_le_frontmatter`,
  `test_ac2_appels_meme_coupes_par_un_retour_a_la_ligne`,
  `test_ac2_interview_appelle_domain_modeling` (dépôt réel).
- AC-3 : atteint. `test_ac3_appel_vers_un_skill_absent_ignore`,
  `test_ac3_situations_lues_dans_la_carte_de_next`,
  `test_ac3_skill_sans_groupe_range_dans_autres_selon_sa_famille`,
  `test_ac3_chaque_skill_du_depot_a_un_groupe_sur_la_carte`.
- AC-4 : atteint, vérifié à la main (clics de la carte, des parcours, des cartes, des notices) ;
  sans test automatique ; le clavier des onglets n'a pas été essayé.
- AC-5 : atteint, par captures : 375 px en clair et en sombre, 1400 px en clair et en sombre.
- AC-6 : atteint. `CLAUDE.md` (« Commandes », « Travail ») et `README.md` (« La page des skills »).

Écarts au plan :
- carte en trois colonnes, et familles nommées « Toi seul » / « Toi ou Claude » (retour de
  l'utilisateur) ;
- le panneau dit « Écrit » au lieu de « Produit » (R-4), et coupe la description en rôle et
  « Se déclenche » ;
- JetBrains Mono chargée en plus de Poppins et Lora, pour le code et les noms de skills (R-6) ;
- « Relu par » recopié à la main d'après un `grep` (R-7) ;
- « Quel skill ? » montre 5 cartes à la fois au lieu des 22 (retour de l'utilisateur) ;
- un seul commit pour tout le plan, sur `main` : convention du dépôt.

Tâches ajoutées : la vague 3 (retours de revue). Aucune retirée.

Hors plan : `.impeccable/config.json`, créé par l'exception « side-tab » du contrôle de design,
n'est pas commité (à décider par l'utilisateur).

