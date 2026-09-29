---
name: design
description: Définir l'identité visuelle d'un projet avant de coder son interface : recherche du secteur, directions contrastées, prototype HTML, puis docs/design/DESIGN.md avec les tokens.
argument-hint: "[type de projet ou contexte]"
disable-model-invocation: true
---

# Design : de l'intention au DESIGN.md

L'objectif est d'aboutir à une direction visuelle **validée sur un prototype réel**, puis figée
dans `docs/design/DESIGN.md` que les sessions suivantes appliqueront. Sans ce fichier, chaque
session réinvente le style : c'est tout l'intérêt du skill.

Ce skill ne code pas l'application : il s'arrête au prototype et au `DESIGN.md`. Pour retoucher,
auditer ou peaufiner une interface déjà codée, d'autres outils conviennent mieux (par exemple le
plugin `impeccable` s'il est installé).

## Principes

- **Du concret plutôt que de l'abstrait** : « quelle ambiance voulez-vous ? » donne des réponses
  molles. Proposer des options nommées et faire réagir.
- **Montrer tôt** : l'utilisateur doit voir un premier rendu rapidement. Pas plus de 3 séries de
  questions avant le prototype.
- **Voie rapide** : si l'utilisateur dit « fais vite » ou « surprends-moi », résumer les
  hypothèses en 3 lignes et passer directement au prototype.

## 1. Préparer

1. **Plugin frontend-design** : vérifier si le skill `frontend-design` figure dans les skills
   disponibles.
   - S'il est présent, appliquer ses consignes pour les directions et le prototype : il sert à
     éviter le rendu « template IA générique ».
   - S'il est absent, proposer de l'installer avant de continuer, en donnant la commande (on ne
     peut pas la taper à la place de l'utilisateur) :
     ```
     /plugin install frontend-design@claude-plugins-official
     ```
     Si elle échoue, il peut le chercher dans `/plugin`, onglet Discover. Un redémarrage de
     session peut être nécessaire. S'il refuse, continuer sans.
2. **Contexte existant** : lire s'ils existent `README.md`, `CLAUDE.md`,
   `docs/cahier-des-charges.md`, `docs/nommage.md`, les assets (logo, captures), la configuration
   Tailwind ou les CSS existants.
   - Si un `docs/design/DESIGN.md` existe (ou un `DESIGN.md` à la racine dans un projet plus
     ancien) : passer en **mode évolution**. Demander ce qui ne va plus, ne pas repartir de zéro.
   - Déduire tout ce qu'on peut de ces fichiers, pour **ne pas reposer de questions dont la
     réponse est déjà écrite**.

## 2. Le contexte

Appeler le Skill tool avec « interview », pour une série de questions choisies dans
[references/questions.md](references/questions.md) selon le type de projet, chacune avec une
valeur par défaut. Première série typique :

- le type de projet (vitrine, SaaS, back-office, mobile…), s'il n'est pas déduit ;
- qui l'utilise, et dans quel contexte (grand public sur mobile, pro 8 h par jour sur grand
  écran…) ;
- l'identité existante : logo, couleurs imposées, charte (demander le chemin des fichiers) ;
- la stack front visée (utile pour le format des tokens).

## 3. Rechercher le secteur

Après la première série, pas avant : il faut le secteur et la cible pour chercher
intelligemment. Appeler le Skill tool avec « research » sur : les concurrents directs, les
références reconnues du secteur, les conventions UX du domaine. Demander à l'agent d'ouvrir les
pages les plus pertinentes plutôt que de se contenter des extraits.

Restituer une **synthèse courte** (10 lignes au maximum) : conventions à respecter, ce qui
fonctionne bien, pièges fréquents, et **une opportunité de différenciation**. On s'inspire, on ne
copie pas : aucune reprise de logo, de visuel ou de texte d'un concurrent.

## 4. Proposer des directions

**2 ou 3 directions contrastées**, jamais des variations timides d'une même idée. Pour chacune :

- **Nom** évocateur (« Atelier chaleureux », « Cockpit dense »…) ;
- **Intention** en une phrase : ce que l'utilisateur final doit ressentir ;
- **Palette** : 4 à 6 couleurs en hexadécimal, avec leur rôle (fond, texte, primaire, accent…) ;
- **Typographies** : titres et corps (Google Fonts ou polices système), avec la justification ;
- **Densité et rythme** : aéré, équilibré ou dense ; angles vifs ou arrondis ;
- **Élément signature** : le détail dont on se souviendra ;
- **Risque** : ce qui pourrait mal vieillir ou déplaire.

Demander en même temps 1 à 3 sites que l'utilisateur aime (ou déteste), et pourquoi.
L'utilisateur choisit une direction ou en mélange deux ; acter le choix en une ligne.

## 5. Choisir l'écran pivot

- Lister les pages ou écrans clés et le parcours principal (5 à 10 lignes).
- Choisir avec l'utilisateur **l'écran pivot** à prototyper, celui qui porte le plus de
  décisions :
  - vitrine ou landing : la page d'accueil ;
  - SaaS ou back-office : l'écran de travail principal (tableau de bord, liste et détail) ;
  - mobile : l'écran principal de l'app.

## 6. Prototyper

Les règles détaillées sont dans [references/prototype.md](references/prototype.md). L'essentiel :

- **Un seul fichier** `docs/design/prototype.html`, autonome, sans build : HTML, CSS et JS
  vanilla. Google Fonts autorisé.
- Les **tokens en variables CSS** dans `:root`, en tête du fichier : ce seront ceux du
  `DESIGN.md`.
- **Contenu réaliste** tiré du projet, jamais de lorem ipsum : le design se juge sur du vrai
  texte.
- Responsive ; pour du mobile, afficher l'écran dans un cadre de 390 × 844 px centré.
- Contrastes WCAG AA au minimum.

Donner la commande pour l'ouvrir (`open docs/design/prototype.html` sur macOS, `xdg-open` sur
Linux) et demander des retours **précis** : ce qui plaît, ce qui gêne, ce qui manque.

**Itérer** par modifications ciblées sur le même fichier. Si l'utilisateur hésite entre deux
options, ajouter en haut de page un sélecteur qui bascule entre deux jeux de tokens, plutôt
qu'une deuxième page. Au bout de 3 itérations sans convergence, revenir à l'étape 4 plutôt que de
retoucher à l'infini.

## 7. Écrire le DESIGN.md

Quand l'utilisateur valide le prototype :

1. Écrire `docs/design/DESIGN.md` en suivant
   [references/design-md-template.md](references/design-md-template.md). Les tokens doivent être
   **identiques** à ceux du prototype validé.
2. Proposer (sans le faire d'office) d'ajouter dans `CLAUDE.md` une ligne du type : « Avant tout
   travail d'interface, lire `docs/design/DESIGN.md` et utiliser exclusivement ses tokens. »
3. Terminer par un récapitulatif en 3 lignes : direction retenue, fichiers produits, prochaine
   étape suggérée.
