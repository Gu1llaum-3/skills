# Réparer le parcours entre les skills

> Statut : terminé le 28/09/2026
> Origine : audit des skills du 28/09/2026 (point 1, « réparer le parcours »), dans la conversation

## Objectif

Plusieurs parcours s'arrêtent aujourd'hui : des fichiers de `docs/` non commités bloquent
`implement`, le chemin du POC passe deux fois la main et ne revient jamais au verdict, des statuts
sont cherchés que personne n'écrit, et `implement` se contredit sur les branches. Après ce plan,
chaque skill écrit les marqueurs que les autres lisent, dans le même format.

## Décisions

- **Arbre de travail** : `implement` accepte, en plus du plan, les fichiers **nouveaux** de `docs/`
  produits par les skills du parcours (`docs/research/`, `docs/questionnaires/`, `docs/poc/`,
  `docs/specs/`, `docs/tickets/`, `docs/design/`, `docs/cahier-des-charges.md`, `ROADMAP.md`). Il
  les nomme, puis les commite avec la première tâche. Toute autre modification bloque comme avant.
- **Branches** : la convention écrite du dépôt (`CLAUDE.md`) l'emporte ; si elle ne dit rien,
  jamais la branche principale. Plus d'exception à noter dans chaque plan.
- **Statut d'un plan** : une ligne `> Statut :` toujours présente : `à valider` → `validé par
  <nom> le JJ/MM/AAAA` → `terminé le JJ/MM/AAAA`.
- **Question bloquante** : elle peut figurer dans un plan (`[Métier : X, bloquante]`, format de
  `to-questionnaire`) ; le plan reste « à valider » tant qu'elle n'a pas de réponse.
- **Roadmap toujours** : après validation du cahier des charges, ses jalons sont créés dans le
  gestionnaire avec `tickets` (`ROADMAP.md` en local, milestones ou versions ailleurs), même pour
  un projet « simple ». Le plan d'un jalon « simple » s'y rattache comme une ligne ; `implement`
  la coche à la fin. Un jalon est réalisé quand toutes ses lignes sont cochées. Sur un
  gestionnaire distant, `implement` propose de fermer le milestone, sans le faire seul.
- **POC** : `poc` appelle `plan` seulement ; `plan` propose `implement`. Pour un plan d'origine
  POC, la vérification est un essai ou un test qui tranche l'hypothèse, sans TDD complet ;
  `implement` ne propose pas de fusion et renvoie vers `/poc <fichier>` pour le verdict. La
  branche passe par un champ `> Branche :` du plan.
- **Règle des skills lancés par l'utilisateur**, réécrite telle qu'elle est pratiquée : ils
  proposent la suite et ne lancent un skill qu'après accord explicite ; un skill marqué
  `disable-model-invocation` ne peut pas être lancé par Claude, il se propose avec sa commande.
- Un seul commit sur `main` pour tout le plan (convention du `CLAUDE.md`).

## Critères d'acceptation

- AC-1 : `implement` démarre quand l'arbre ne contient, en plus du plan, que des fichiers nouveaux
  de `docs/` produits par les skills ; il les nomme et les commite avec la première tâche ; toute
  autre modification bloque comme avant.
- AC-2 : `implement` ne commite sur la branche principale que si la convention écrite du dépôt le
  dit ; son texte ne se contredit plus.
- AC-3 : un plan porte toujours une ligne `> Statut :` (`à valider`, `validé par … le …`,
  `terminé le …`), écrite et lue de la même façon par le modèle de plan, `plan`, `implement` et
  `next`.
- AC-4 : une question métier bloquante peut figurer dans un plan ; le plan reste « à valider » ;
  `next` la voit et renvoie vers son questionnaire.
- AC-5 : un ticket local passe « en cours » à la première tâche d'`implement` ; une spec locale
  passe « terminée » quand son dernier ticket l'est ; un questionnaire reçoit « envoyé le … » à
  l'envoi.
- AC-6 : `poc` n'appelle que `plan` ; son fichier passe « en cours » après validation et
  « terminé » au verdict ; la branche `poc/<slug>` est reprise par `implement` via `> Branche :`.
- AC-7 : pour un plan d'origine POC, `implement` vérifie par un essai ou un test qui tranche
  l'hypothèse, sans TDD complet, ne propose pas de fusion, et propose `/poc <fichier>` pour le
  verdict.
- AC-8 : après validation du cahier des charges, `brainstorming` propose de créer les jalons avec
  `tickets` ; le plan d'un jalon s'y rattache ; `implement` coche sa ligne à la fin ; `next`
  trouve le premier jalon non réalisé.
- AC-9 : `CLAUDE.md` et `README.md` décrivent la règle des skills lancés par l'utilisateur telle
  qu'elle est pratiquée.
- AC-10 : `next` lit ces marqueurs : statut des plans, questions bloquantes, jalons de la
  roadmap, questionnaires envoyés, POC en cours ou terminés sans suite.

## Interfaces à tester

- Les fichiers des skills, relus et vérifiés par `grep` (AC-1 à AC-10) : plus aucune occurrence de
  l'ancien format (« remplacer « Statut : à valider » par « Validé par… »), de « même si une
  convention semble le permettre », ni d'appel à `implement` dans `poc`.
- Un scénario d'essai proposé à l'utilisateur en fin de plan (AC-1, AC-6, AC-7, AC-8).

## Hors périmètre

- La taille d'`implement` et de `plan` (au-delà de ~150 lignes) : point 4 de l'audit. Ce plan
  ajoute le moins de lignes possible.
- La revue en fin d'`implement` (point 2), `debug` et la contradiction de `next` sur les bugs
  (point 3), les fins de phase de `next` (point 5).
- Harmoniser `**Statut :**` (tickets, specs) et `> Statut :` (plans, POC, questionnaires).
- Proposables plus tard : `feature` qui lit un POC comme `brainstorming`, le ticket redécoupé
  laissé ouvert, l'envergure corrigée vers « simple » par `to-spec`, les listes d'appelants des
  descriptions.

## Vague 1 : `implement`, statuts et règles

- [x] `implement` : arbre de travail (fichiers nouveaux de `docs/` acceptés, nommés, commités avec
  la première tâche) (AC-1) : vérification prévue : relecture.
- [x] `implement` : une seule règle de branche (convention écrite, sinon jamais la branche
  principale) (AC-2) : vérification prévue : `grep` de l'ancienne phrase.
- [x] Statut du plan : modèle de plan (`> Statut :` à trois états, questions bloquantes admises),
  `plan` étape 6, `implement` (préalable « Validé » et « Fin du plan ») (AC-3, AC-4) :
  vérification prévue : `grep "Validé par"` et `grep "Statut"` sur les trois fichiers.
- [x] Statuts des tickets, specs et questionnaires : `implement` passe le ticket local « en
  cours » via `tickets` ; `tickets/references/local.md` termine la spec avec son dernier ticket ;
  `to-questionnaire` étape 4 date l'envoi (AC-5) : vérification prévue : relecture.
- [x] Règle des skills lancés par l'utilisateur, dans `CLAUDE.md` et `README.md` (AC-9) :
  vérification prévue : relecture contre `feature`, `poc`, `brainstorming`.

## Vague 2 : POC, jalons et `next`

- [x] POC : `poc` (appel à `plan` seul, statut en cours puis terminé, `> Branche :`) ; modèle de
  plan (champ `> Branche :`) ; `plan` (source POC : vérification qui tranche l'hypothèse) ;
  `implement` (origine POC : pas de TDD complet, pas de fusion, renvoi vers `/poc`) (AC-6, AC-7) :
  vérification prévue : `grep "implement" poc/SKILL.md`, relecture.
- [x] Jalons : `brainstorming` (création des jalons avec `tickets` après validation) ; `plan`
  (rattacher le plan d'un jalon) ; `tickets/references/local.md` (ligne de plan sous un jalon,
  jalon réalisé quand tout est coché) ; `implement` (cocher la ligne, proposer de fermer le
  milestone distant) (AC-8) : vérification prévue : relecture de bout en bout du chemin
  `brainstorming` → `plan` → `implement` → `next`.
- [x] `next` : lire les nouveaux marqueurs (AC-10) : vérification prévue : relecture contre les
  modèles modifiés.
- [x] Proposer le scénario d'essai à l'utilisateur (AC-1, AC-6, AC-7, AC-8) : vérification
  prévue : l'utilisateur le lance.

## Journal

**Vague 1 (28/09/2026)**

- Livré : `implement` (arbre de travail, règle de branche unique à trois endroits, statut
  `validé par` / `terminé le`, question bloquante qui interdit de démarrer, ticket local passé
  « en cours » à la première tâche) ; modèle de plan (statut à trois états, question bloquante
  admise) ; `plan` étapes 4 et 6 ; `tickets/references/local.md` (la spec suit ses tickets) ;
  `to-questionnaire` étape 4 (`> Statut : envoyé le …`) ; règle des skills lancés par
  l'utilisateur dans `CLAUDE.md` et `README.md`.
- Écart : `docs/plans/next.md` passé au nouveau format (`> Statut : terminé le 28/09/2026`), pour
  que `next` le lise comme les autres.
- Vérifié par `grep` : plus de « semble le permettre » ni de « notée dans le plan » dans
  `implement`, plus de « remplacer « Statut » » nulle part, plus de « ne les lance pas » dans
  `CLAUDE.md` et `README.md`. Relu : `feature` et `brainstorming` passent bien la main après
  accord ; `poc` appelle encore `implement` sans demander (corrigé en vague 2).
- Taille : `implement` passe de 170 à 176 lignes, `plan` de 155 à 156 (point 4 de l'audit).
- Quoi essayer : `git diff` ; relire `implement/SKILL.md` lignes 30-60 (préalables) et la fin
  du plan.

**Vague 2 (28/09/2026)**

- Livré :
  - POC : `poc` n'appelle plus que `plan` (sur accord), passe le fichier « en cours » puis
    « terminé » ; le modèle de plan a un champ `> Branche :` ; `plan` prévoit un essai ou un test
    ciblé par tâche ; `implement` saute le TDD complet, ne propose pas de fusion et renvoie vers
    `/poc`.
  - Jalons : `brainstorming` propose de créer la roadmap avec `tickets` ; `plan` cherche le
    premier jalon non réalisé dans la roadmap et y rattache le plan d'un jalon sans tickets ;
    `tickets` (SKILL.md, local, GitHub, GitLab, Jira) sait rattacher un plan et marquer un jalon
    réalisé ; `implement` coche la ligne et propose de fermer le jalon distant ; `to-spec` ne
    recrée pas des jalons existants.
  - `next` lit les statuts des plans (dont questions bloquantes et POC sans verdict), des
    questionnaires, des tickets en cours, et les jalons de la roadmap.
- Écart : `to-spec` retouché (« s'ils n'existent pas encore ») pour ne pas recréer les jalons que
  `brainstorming` a déjà créés ; `tickets/SKILL.md` et les trois références distantes reçoivent
  l'opération « marquer réalisé », nécessaire à la décision « roadmap toujours ».
- Vérifié par `grep` : aucune trace des anciens formats hors des plans ; aucun appel à
  `implement` dans `poc` ; les statuts écrits (`validé par`, `terminé le`, `en cours`,
  `terminé`, `envoyé le`) sont ceux que `next` et `implement` lisent.
- Non vérifié : les commandes `gh` et `glab` de fermeture de milestone n'ont pas été lancées
  (écriture sur un service distant).
- Taille : `implement` 183 lignes, `plan` 159, `next` 117 (point 4 de l'audit).

## Réalisé

- AC-1, AC-2 : atteints (`implement`, préalables et branche), vérifiés par relecture et `grep`.
- AC-3, AC-4 : atteints (modèle de plan, `plan`, `implement`, `next`).
- AC-5 : atteint (`implement`, `tickets/references/local.md`, `to-questionnaire`).
- AC-6, AC-7 : atteints (`poc`, `plan`, modèle de plan, `implement`).
- AC-8 : atteint sur le papier ; les commandes distantes n'ont pas tourné.
- AC-9, AC-10 : atteints.
- Le comportement réel reste à confirmer par le scénario d'essai : dans un dossier jetable,
  `/poc` sur une petite question → vérifier que `plan` écrit `> Branche : poc/<slug>`, que
  `implement` ne fait pas de TDD complet et renvoie vers `/poc` ; puis `/brainstorming` d'un
  mini-projet « simple » → la roadmap est proposée, le plan du jalon 1 s'y rattache, et `/next`
  dans une session vide trouve le bon jalon.
- Hors plan : rien de nouveau.

