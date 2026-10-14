# review : un retour de relecture clair et une question à chaque fois

> Statut : terminé le 14/10/2026
> Origine : cadrage du 13/10/2026 (retour d'une session `implement` en fin de plan, dans la conversation)

## Objectif

Après une longue exécution d'`implement` (turbo, plusieurs vagues), le retour de `review` ne dit
pas clairement ce qu'il faut décider : la vérification (« confirmée ») est confondue avec l'action
(« à corriger »), des écarts déjà notés reviennent comme remarques, l'axe et le `fichier:ligne`
manquent, et aucune question interactive n'est posée. Le retour devient : un bloc d'état court,
les remarques groupées par action, une ligne chacune, puis une question AskUserQuestion avec la
recommandation en premier.

## Décisions

- Périmètre : la partie relecture seulement, c'est-à-dire `review` §5 et l'étape 1 de « Fin du
  plan » d'`implement`. La question de la suite Git et les autres skills ne changent pas.
- **Vérification et action sont distinctes.** La marque (confirmée, douteuse, fausse) dit si la
  remarque est vraie ; l'action proposée dit quoi en faire. On recommande le groupe « À
  corriger », plus « les confirmées ».
- **Vue groupée par action**, dans cet ordre : « À corriger », « À trancher », « Rien à faire »,
  « Déjà connu », « Fausses ». Une ligne par remarque : `R-n · spec|conv · fichier:ligne ·
  constat` (et la raison pour « Rien à faire », « Déjà connu » et « Fausses »). Une remarque fausse reste visible,
  barrée.
- La règle « ne pas reclasser entre les axes » est reformulée : le groupe par action ne change
  ni l'axe affiché sur chaque ligne ni le texte de la remarque, et ne fusionne pas deux remarques.
- **Garde-fous** (l'agent principal est l'auteur du code et juge l'action) :
  - chaque « Rien à faire » porte une raison vérifiable (un fait du code, du dépôt ou du plan),
    pas une préférence ;
  - en cas de doute entre corriger et laisser, la remarque va dans « À trancher » ;
  - la question propose toujours un lot qui reprend aussi les « Rien à faire ».
- **« Déjà connu »** : une remarque qui répète un écart déjà noté dans le journal du plan ou le
  bilan de vague. Elle garde son numéro et tient en une ligne, sans action.
- **La question**, avec AskUserQuestion :
  - « Que corriger ? » : le lot « À corriger » en premier « (Recommandé) », puis un lot plus large
    (avec les « Rien à faire »), puis « Rien, passer au bilan » (ou « Rien, s'arrêter là » si le
    skill est lancé seul) ; la réponse libre est ajoutée par l'outil ;
  - puis une question par remarque « À trancher », options du compromis, la recommandée en
    premier ;
  - 4 questions au plus par appel ; les « À trancher » en trop passent à un second appel ;
  - aucune remarque du tout : pas de question, le dire et continuer.
  - rien à corriger : « Rien » vient en premier, recommandé (relecture R-5).
- **Bloc d'état**, seulement appelé par `implement`, en tête du message, 3 ou 4 lignes : plan et
  branche ; vagues faites et commits ; critères atteints n/m ; vérification complète verte ou
  rouge (et pourquoi en quelques mots). Ce n'est pas le bilan, qui s'écrit après.
- **Rapport complet par axe** (le format actuel `## Spec` / `## Conventions`, avec extraits) :
  appelé par `implement`, il va dans le journal du plan, et le message y renvoie ; lancé seul, il
  s'affiche sous la vue groupée.
- La question vit dans `review` (une seule source) ; `implement` y renvoie et ajoute le bloc
  d'état.
- Pas de changement des briefs des sous-agents : `run_subagents.py` mesure ce qu'ils trouvent,
  pas la présentation.

## Critères d'acceptation

- AC-1 : `review` §5 décrit la vue groupée (groupes, ordre, format de ligne avec axe et
  `fichier:ligne`), sépare la marque de vérification de l'action, et pose les garde-fous.
- AC-2 : `review` §5 décrit la question AskUserQuestion (lots, recommandation en premier, une
  question par « À trancher », limite de 4, cas sans remarque), pour les deux cas : lancé seul et
  appelé par `implement`.
- AC-3 : `implement`, « Fin du plan » étape 1, ajoute le bloc d'état, écrit le rapport complet
  dans le journal, renvoie à la question de `review`, et ne recommande plus « les confirmées ».
- AC-4 : la règle « ne pas reclasser » est reformulée sans contredire la vue groupée.
- AC-5 : aucun renvoi cassé ni contradiction avec les skills rattachés (`next`, `README.md`,
  `docs/skills.template.html`, `evals/run_subagents.py` qui découpe le rapport par `R-n` et y
  cherche un `fichier:ligne`) ; `review/SKILL.md` reste sous 500 lignes.

## Interfaces à tester

- `review/SKILL.md` et `implement/SKILL.md` relus (AC-1 à AC-4).
- `git grep -n "confirmées\|reclass\|En bref" -- ':!docs/plans'` et relecture des skills
  rattachés (AC-5).
- Essai manuel proposé à l'utilisateur après le commit : `/implement` en turbo sur un petit plan
  d'un projet réel, observer le message de fin de relecture (AC-1 à AC-3).

## Hors périmètre

- La question de la suite Git en fin de plan, et les questions de fin des autres skills.
- Les briefs des sous-agents et le contenu du rapport par axe.
- Une évaluation automatique de la présentation.

## Vague 1 : le nouveau retour de relecture

- [x] Réécrire `review` §5 (vue groupée, marque et action, garde-fous, question, rapport complet
  selon le cas, règle des axes reformulée) et l'étape 1 de « Fin du plan » d'`implement` (bloc
  d'état, rapport dans le journal, renvoi à la question), en un seul commit avec le plan
  (convention du dépôt) (AC-1 à AC-5) : vérification prévue : relecture des deux sections,
  grep des skills rattachés, `python3 docs/build_skills_page.py` puis `python3 -m unittest
  docs/test_build_skills_page.py` verts

## Vague 2 : Retours de revue

- [x] R-1, R-2, R-3, R-8, R-9, R-13 : libellé « Rien, s'arrêter là », renvoi au journal, règle
  de la remarque barrée, rôle d'`implement` laissé à `implement`, garde-fou sans négation,
  format de ligne précisé (AC-1 à AC-3) : vérification prévue : relecture des sections
- [x] R-5, R-10, R-12 : « Rien » recommandé inscrit dans les décisions, consigne sans « Pas
  de », constante `NON_INTERACTIVE` partagée par les prompts d'évaluation (AC-5) : vérification
  prévue : `--dry-run` des deux jeux, prompts inchangés au mot près

## Journal

### Vague 1 (13/10/2026)

- Livré : `review` passe de 5 à 7 sections. La 5 (« Vérifier et classer ») sépare la marque de
  l'action, avec cinq groupes et leurs garde-fous. La 6 (« Rapporter ») donne le rapport complet
  par axe et la vue groupée (`R-n · axe · fichier:ligne · constat`). La 7 (« Demander quoi
  corriger ») porte la question AskUserQuestion. `implement`, « Fin du plan » étape 1 : bloc
  d'état, rapport complet dans le journal, renvoi à « Demander quoi corriger ».
- Écarts : une remarque **douteuse** va dans « À trancher » (non prévu, mais c'est le garde-fous
  « en cas de doute ») ; `evals/run_subagents.py` modifié : le prompt de `review` dit que la
  session n'est pas interactive (sinon la question pourrait remplacer le rapport dans le texte
  final), et le commentaire « En bref » est mis à jour. Un seul commit en fin de plan (bilan
  compris) plutôt qu'un commit de tâche puis un de bilan : convention du dépôt.
- Vérifié : aucun renvoi par numéro vers l'ancienne §5 (`git grep`) ; `next`, `README.md`,
  `docs/skills.template.html` décrivent `review` sans son format ; `run_subagents.py --dry-run
  review-new` affiche le nouveau prompt ; page régénérée, 8 tests verts ; pas de tiret long ;
  `review/SKILL.md` fait 160 lignes. Non vérifié : le comportement réel en session (essai manuel).
- Quoi essayer : `/implement <plan> turbo` sur un petit plan d'un projet réel ; regarder le bloc
  d'état en tête, la vue groupée, et la question « Que corriger ? » avec le lot recommandé en
  premier.

### Relecture (13/10/2026)

#### Spec

- R-1 (confirmée) : AC-2 et Décisions (« Rien, s'arrêter là » si lancé seul) ; `review/SKILL.md:146`
  n'a que « Rien » et le cas `implement`.
- R-2 (confirmée) : AC-3 et Décisions (« le message y renvoie ») ; `implement/SKILL.md:137` écrit
  le rapport dans le journal sans dire d'y renvoyer.
- R-3 (confirmée) : AC-1 et Décisions (« une remarque fausse reste visible, barrée ») ;
  `review/SKILL.md:116` ne le dit plus que par l'exemple de la ligne 129.
- R-4 (confirmée) : Hors périmètre ; `evals/run_subagents.py:135` et `:210` modifiés. Déjà dans
  le journal de la vague 1.
- R-5 (confirmée) : Décisions (« le lot À corriger en premier ») ; `review/SKILL.md:148`
  recommande « Rien » quand il n'y a rien à corriger, cas non prévu.
- R-6 (confirmée) : `review/SKILL.md:84`, remarque douteuse dans « À trancher », non prévue.
  Déjà dans le journal de la vague 1.
- ~~R-7 : `evals/run_subagents.py:210`, docstring inverse de l'ordre~~ (fausse) : « recite » dit
  que le rapport complet, placé après, répète les `R-n` de la vue groupée ; c'est l'ordre fixé.

#### Conventions

Violations :
- R-8 (confirmée) : « une seule source par règle » ; `review/SKILL.md:136` et `:156` décrivent ce
  que fait `implement` (journal, vue groupée, vague de corrections), déjà dans
  `implement/SKILL.md:137-143`.
- R-9 (confirmée) : « dire ce qu'il faut faire » ; `review/SKILL.md:88` « ce groupe ne sert pas à
  écarter une remarque gênante » est une interdiction.
- R-10 (confirmée) : même règle ; `review/SKILL.md:152` « Pas d'option Autre ».

Jugements :
- R-11 (confirmée) : possible code dupliqué ; `review/SKILL.md:136-139` et `:156-160`, la cascade
  « appelé par `implement` / lancé seul » écrite deux fois.
- R-12 (confirmée) : possible chirurgie au fusil ; `evals/run_subagents.py:135`, l'évaluation
  dépend de la question de fin.
- R-13 (confirmée) : possible nom mystérieux ; `review/SKILL.md:116`, valeurs de l'axe (`conv`
  contre « conventions ») et groupes qui exigent une raison non précisés.

Retenues : R-1, R-2, R-3, R-5, R-8, R-9, R-10, R-12, R-13 (vague 2). R-11 gardée telle quelle :
§6 dit quoi afficher, §7 ce qui suit la question, deux moments distincts. R-4 et R-6 déjà
connues ; R-7 fausse.

### Vague 2 (14/10/2026)

- Livré : les 9 corrections retenues, dans `review/SKILL.md`, `implement/SKILL.md`,
  `evals/run_subagents.py` et les décisions du plan (R-5).
- Vérifié : `--dry-run --set hard review-new plan-full-new`, prompts identiques à la vague 1
  au mot près ; page régénérée et tests verts (voir le bilan).

## Réalisé

- AC-1 : atteint, `review/SKILL.md` §5 et §6 (groupes, ordre, format `R-n · spec|conv ·
  fichier:ligne · constat`, raisons, remarque barrée, garde-fous).
- AC-2 : atteint, §7 (lots, recommandation en premier, libellés « Rien », une question par « À
  trancher », limite de 4, cas sans remarque ou sans correction).
- AC-3 : atteint, `implement` « Fin du plan » étape 1 (bloc d'état, rapport dans le journal,
  renvoi, plus de « les confirmées »).
- AC-4 : atteint, `review/SKILL.md` fin de §5.
- AC-5 : atteint, aucun renvoi cassé (`git grep`), page et tests verts, `review/SKILL.md` sous
  500 lignes. Le comportement en session reste à essayer à la main.
- Écarts : remarque douteuse dans « À trancher » ; « Rien » recommandé quand rien n'est à
  corriger ; `evals/run_subagents.py` touché (prompt non interactif partagé) ; un seul commit
  pour tout le plan, convention du dépôt.
- Tâches ajoutées : la vague 2, issue de la relecture.
- Hors plan : la question de la suite Git en fin d'`implement` n'a pas changé.
