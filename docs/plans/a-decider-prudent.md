# implement autonome : l'agent tranche ce qui a une option prudente

> Statut : terminé le 19/10/2026
> Origine : cadrage du 19/10/2026 (dans la conversation), après un essai réel d'`implement`
> autonome (plan `delais-mariadb` d'un projet Go et MariaDB)

## Objectif

Dans l'essai, « À décider » a renvoyé à l'utilisateur quatre points techniques (R-4, R-8, R-9,
R-10) qu'il ne pouvait pas trancher, alors que l'agent avait une recommandation solide pour
chacun : une option plus prudente que les autres, ou un doute qu'un test tranche. L'agent
applique désormais l'option prudente quand elle domine, la vérifie et la signale ; seuls les
vrais choix vont à l'utilisateur, avec une recommandation et un choix par défaut. Deux défauts
vus dans le même essai sont corrigés : la branche n'a pas été poussée faute d'outil pour la
forge, et la roadmap a été cochée alors que des points restaient à trancher avant la fusion.

## Décisions

- **Un cinquième groupe, « Option prudente »**, entre « À corriger » et « À décider » : le juge y
  range une remarque qui demande un choix, quand une option domine les autres sur tous ces
  points (AC-1) :
  - elle ne perd ni donnée ni trace (audit, journal, fichier) ;
  - elle se défait sans migration ni reprise de données ;
  - elle ne change ni contrat (statuts HTTP, format d'échange, interface publique), ni
    configuration, ni schéma ;
  - elle reste dans les décisions du plan ;
  - un test peut la vérifier, ou trancher le doute qui la rend incertaine.
  Le juge nomme l'option, la raison de sa domination, et le test qui la vérifie.
- **« À décider » ne garde que ce qui revient à l'utilisateur** (AC-2) : un choix produit ou
  métier (ce que voit l'utilisateur final, un coût, une règle légale ou de conservation), un choix
  qui contredit une décision du plan ou en sort, une remarque sans option dominante, une option
  prudente que son test a réfutée, ou une remarque que le juge ne peut pas vérifier ; s'y
  ajoutent ce que l'auteur y envoie : une contestation, une remarque restée ouverte après deux
  tours, une tâche en échec. Chaque point porte une recommandation et un choix par défaut : « sans
  avis de ta part : <option> ».
- **C'est le juge qui classe en « Option prudente »**, pas l'auteur : l'auteur ne s'autorise pas
  lui-même à trancher (même règle que pour « Écartée »).
- **`implement` applique les options prudentes** dans la vague « Retours de revue », avec les
  « À corriger » : test d'abord (le test nommé par le juge), puis le code. Un test qui réfute
  l'option la fait passer dans « À décider », avec ce que le test a montré. Le juge relit ces
  corrections comme les autres (AC-3).
- **Dans la PR**, une section « Décidé sans toi, à relire en priorité » vient juste après « À
  décider », avec chaque option prudente appliquée, sa raison et son commit (AC-4).
- **`review` lancé seul** : le lot recommandé de « Que corriger ? » comprend les « À corriger » et
  les « Option prudente » (AC-5).
- **« Je n'ai pas d'avis »** : le message final propose d'appliquer les choix par défaut de « À
  décider » dans une nouvelle vague du même plan (AC-6).
- **Push sans outil de forge** : la branche se pousse dès qu'il y a un dépôt distant et que les
  conditions du push sont réunies ; seule la création de la PR demande l'outil. Sans outil, le
  message final donne le lien de création que la forge affiche au push, sinon celui qui se déduit
  de l'URL du dépôt distant (Bitbucket, GitHub, GitLab), avec le texte prêt à coller (AC-7).
- **Roadmap et ticket local** : tant que « À décider » n'est pas vide, la ligne de la roadmap
  n'est pas cochée et le ticket local reste en cours ; une ligne « À faire par toi » le dit
  (AC-8).
- Dépôt : un seul commit, sur `main` (convention du dépôt).

## Critères d'acceptation

- AC-1 : le juge classe en « Option prudente » une remarque à choix dont une option remplit les
  cinq conditions, en nommant l'option, sa raison et son test.
- AC-2 : « À décider » ne reçoit que choix produit ou métier, contradiction du plan ou sortie
  de son périmètre, absence d'option dominante, option réfutée, remarque invérifiable, et ce que
  l'auteur y envoie (contestation d'un verdict, remarque restée ouverte après deux tours, tâche en
  échec) ; chaque point a une recommandation et un « sans avis de ta
  part : <option> ».
- AC-3 : `implement` applique les options prudentes en TDD dans « Retours de revue » ; une option
  réfutée par son test passe dans « À décider » ; le juge relit ces corrections.
- AC-4 : le corps de la PR a, après « À décider », « Décidé sans toi, à relire en priorité » avec
  option, raison et commit.
- AC-5 : `review` lancé seul recommande le lot « À corriger » plus « Option prudente ».
- AC-6 : avec des points « À décider », le message final propose d'appliquer leurs choix par
  défaut dans une nouvelle vague.
- AC-7 : sans outil de forge, la branche est poussée (si les autres conditions le permettent) et
  le message final donne le lien de création de la PR et son texte.
- AC-8 : « À décider » non vide : roadmap non cochée, ticket local laissé en cours, rappel dans
  « À faire par toi ».

## Interfaces à tester

- Le texte de `agents/review-judge.md`, `review`, `implement` et ses références, relu contre
  chaque critère (pas de test automatique du comportement)
- `python3 evals/run_subagents.py --runs 1 review-new` : le juge rend toujours un classement
  sourcé, avec le nouveau groupe s'il s'applique (AC-1, AC-2)
- `python3 docs/build_skills_page.py` puis `python3 -m unittest docs/test_build_skills_page.py`

## Hors périmètre

- Une fixture de banc avec une remarque à option prudente (le correcteur ne vérifie pas encore
  les groupes : déjà au `TODO.md`).
- Un outil pour Bitbucket (création de PR par son API).

## Vague 1 : l'option prudente

- [x] `agents/review-judge.md` : groupe « Option prudente » et ses cinq conditions, « À décider »
  restreint, recommandation et choix par défaut, format de rendu ; `review` §5.4, vue groupée
  (ordre, en-tête), §7 (lot recommandé) (AC-1, AC-2, AC-5) : vérification prévue : relecture
  contre AC-1, AC-2, AC-5, `git grep` des groupes
- [x] `implement` « Fin du plan » (application en TDD, option réfutée, message final avec les
  choix par défaut) ; `references/pull-request.md` (section « à relire en priorité », push sans
  outil, lien de création) ; `references/ending-by-origin.md` (roadmap et ticket laissés ouverts)
  (AC-3, AC-4, AC-6, AC-7, AC-8) : vérification prévue : relecture contre ces critères
- [x] `docs/skills.template.html` et `README.md` si leur texte change, page régénérée, banc
  `review-new` sur un passage : vérification prévue : tests de la page verts, banc sans régression

## Journal

### Vague 1 (19/10/2026)

- Livré : groupe « Option prudente » dans `agents/review-judge.md` (cinq conditions, option,
  raison et test), « À décider » restreint avec recommandation et « sans avis de ta part » ;
  `review` (cinq groupes nommés, vue groupée avec exemple d'option prudente, lot recommandé « À
  corriger » et « Option prudente », relecture des corrections qui couvre aussi les options) ;
  `implement` (application en TDD dans « Retours de revue », option réfutée vers « À décider »,
  message final qui propose d'appliquer les choix par défaut) ; `pull-request.md` (push dès qu'il
  y a un dépôt distant, PR par l'outil de la forge, sinon lien de création, section « Décidé sans
  toi, à relire en priorité ») ; `ending-by-origin.md` (roadmap et ticket local ouverts tant que
  « À décider » n'est pas vide) ; règle du gabarit HTML, page régénérée.
- Écarts : la ligne « sécurité, correction locale » passe de « À décider » à « à relire en
  priorité » (AC-2 la sortait de « À décider ») ; AC-2 étendu en relecture (« sortie du
  périmètre », « remarque invérifiable », et ce que l'auteur y envoie : contestation, remarque
  ouverte après deux tours, tâche en échec) ; « Ambiguïté » d'`implement` ne dit plus « la plus
  prudente », pour ne pas confondre avec le nouveau groupe ; README inchangé (il ne nomme pas les
  groupes).
- Vérifié : page régénérée, 8 tests verts ; banc `review-new --runs 1` : 5 sur 5, 2 leurres sur
  2 écartés, 14 `R-n` sourcés sur 15, 0,95 $, 145 s (tout en « À corriger » : aucun défaut planté
  ne demande de choix) ; pas de tiret long ; `review` 197 lignes, `implement` 217. Non vérifié :
  une option prudente appliquée en vrai, le push sans outil de forge (Bitbucket).
- Quoi essayer : reprendre le plan `delais-mariadb` (vague 3) ou un nouveau plan d'un projet
  Bitbucket ; regarder si R-8, R-9, R-10 et R-4 auraient été classés « Option prudente » et
  appliqués, puis le lien de création de PR après le push.

### Relecture (19/10/2026)

`/code-review` (medium), deux relecteurs, juge (`review-judge`), deux tours de relecture des
corrections ; sans commit en cours de route : instantané `git stash create`.

- Spec : R-1 cases et journal vides ; R-2 ligne sécurité déplacée ; R-3 cas invérifiable hors
  AC-2 ; R-4 « sort de la spec » hors AC-2 ; R-5 « ni terminer » contre le statut terminé ; R-6
  redondance contrat/schéma ; R-7 tâche en échec sans choix par défaut.
- Conventions : R-8 définitions courtes des groupes dans `review` ; R-9 règle de l'option
  réfutée à trois endroits ; R-10 « la plus prudente » dans « Ambiguïté » ; R-11 format « À
  décider » divergent ; R-12 chirurgie au fusil ; R-13 lignes longues.
- Bugs : R-14 correction unique qui change contrat ou schéma tombée en « À corriger » ; R-15 rien
  ne ferme roadmap et ticket sans nouvelle vague ; R-16 option prudente introduite par une
  correction jamais appliquée ; R-17 chemins vers « À décider » sans choix par défaut ; R-18
  exemple sans « recommandée » ; R-19 deux définitions de « prudente » ; R-20 création en échec
  après push sans lien ; R-21 `Closes #n` avec « À décider » ouvert ; R-22 forges sans règle de
  lien ; R-23 lignes longues.
- Classement du juge : à corriger et réglées : R-3, R-4, R-5, R-6, R-7, R-11, R-14 à R-18,
  R-20, R-25 (vue au tour 1 : AC-2 sans les chemins de l'auteur) ; options prudentes appliquées :
  R-10 (retirer « prudente » d'« Ambiguïté »), R-22 (autre forge : aucun lien deviné) ; écartées :
  ~~R-2~~ (AC-2 obligeait à la sortir de « À décider »), ~~R-8~~ (aucun critère redit), ~~R-9~~
  (le juge ne lit que ce qu'on lui passe), ~~R-12~~ (fichiers imposés par le plan), ~~R-13~~ et
  ~~R-23~~ (aucune règle de largeur), ~~R-21~~ (`Closes` ne joue qu'à la fusion, qui attend
  l'utilisateur) ; déjà connu : R-1 ; à décider : R-19, R-24.

## Réalisé

- Critères : AC-1 à AC-8 écrits et relus par le juge ; AC-1 et AC-2 observés en vrai sur cette
  relecture (deux options prudentes classées et appliquées, « À décider » avec recommandation et
  choix par défaut) ; AC-7 non essayé en vrai.
- À décider : R-19 (aligner « Ambiguïté » sur les cinq conditions, ou seulement renommer ; sans
  avis : renommer, déjà fait par R-10) ; R-24 (violation d'AC qui ne se corrige qu'en changeant
  un contrat : « À décider » ou « À corriger » ; sans avis : « À décider », en ajoutant « sauf si
  la correction change le schéma, un contrat ou la configuration » à la phrase « Toujours ici »
  du juge).
- Hors plan : rien de nouveau.

### Décision de l'utilisateur (19/10/2026)

- R-24 : une violation d'AC qui ne se corrige qu'en changeant le schéma, un contrat ou la
  configuration va dans « À décider » : l'utilisateur tranche d'abord. Écrit dans la règle
  « Toujours ici » du juge. R-19 : rien à faire (renommage déjà appliqué par R-10).
