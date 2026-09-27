---
name: design-cadrage
description: Cadrage du design visuel d'une application avant de la coder — site vitrine, landing page, SaaS, back-office, dashboard, application mobile. Pose des questions par tours courts, recherche le secteur et les concurrents sur le web, propose des directions visuelles contrastées, produit un prototype HTML d'une seule page puis un DESIGN.md avec les tokens (couleurs, typos, espacements). Utilise ce skill dès que l'utilisateur veut trouver, définir, choisir ou refaire le design, le look, le style, l'identité visuelle, la charte ou l'UI d'un projet, ou demande une maquette ou un prototype visuel, même s'il ne prononce pas le mot « design ».
---

# Cadrage design

Objectif : aboutir à une direction visuelle **validée sur un prototype réel** puis figée dans un `DESIGN.md` que les sessions suivantes appliqueront. Sans ce fichier, chaque session réinvente le style ; c'est tout l'intérêt du skill.

Ce skill ne code pas l'application. Il s'arrête au prototype + `DESIGN.md`.

## Principes de conduite

- **Tours courts** : 3 à 4 questions maximum par tour, chacune avec une valeur par défaut proposée. L'utilisateur doit pouvoir répondre « ok pour les défauts ». Utilise l'outil `AskUserQuestion` s'il est disponible, sinon des questions numérotées.
- **Du concret plutôt que de l'abstrait** : « quelle ambiance voulez-vous ? » donne des réponses molles. Propose des options nommées et fais réagir.
- **Montrer tôt** : l'utilisateur doit voir un premier rendu rapidement. Ne pas enchaîner plus de 3 tours de questions avant le prototype.
- **Voie rapide** : si l'utilisateur dit « fais vite » ou « surprends-moi », résume les hypothèses en 3 lignes et passe directement au prototype.
- **Rester en français** avec l'utilisateur, sauf demande contraire.

## Phase 0 — Préparation (silencieuse, rapide)

1. **Plugin frontend-design** : vérifie si le skill `frontend-design` figure dans tes skills disponibles.
   - S'il est présent, applique ses consignes lors de la conception des directions et du prototype : il sert à éviter le rendu « template IA générique ».
   - S'il est absent, propose à l'utilisateur de l'installer avant de continuer. Tu ne peux pas taper les commandes slash à sa place ; donne-lui la commande :
     ```
     /plugin install frontend-design@claude-plugins-official
     ```
     Si elle échoue, il peut le chercher dans `/plugin` → onglet Discover. Précise qu'un redémarrage de session peut être nécessaire. S'il refuse, continue sans.
2. **Contexte existant** : cherche et lis s'ils existent `README.md`, `ARCHITECTURE.md`, `CLAUDE.md`, un cahier des charges, des assets (logo, captures), la config Tailwind ou les CSS existants.
   - Si un `DESIGN.md` existe déjà : bascule en **mode évolution** (demande ce qui ne va plus, ne repars pas de zéro).
   - Déduis tout ce que tu peux de ces fichiers pour **ne pas reposer de questions dont la réponse est déjà écrite**.

## Phase 1 — Contexte (1 tour de questions)

Lis `references/questions.md` et choisis les questions selon le type de projet. Premier tour typique :

- Type de projet (vitrine, SaaS, back-office, mobile…) si non déduit
- Qui utilise ça, et dans quel contexte (grand public sur mobile, pro 8h/jour sur écran large…)
- Identité existante : logo, couleurs imposées, charte ? (demande le chemin des fichiers)
- Stack front visée (utile pour le format des tokens)

## Phase 2 — Recherche web

Après le premier tour, pas avant : il faut le secteur et la cible pour chercher intelligemment.

- 3 à 6 recherches : concurrents directs, références reconnues du secteur, conventions UX du domaine.
- Ouvre les pages les plus pertinentes (WebFetch) plutôt que de te contenter des extraits.
- Restitue une **synthèse courte** (10 lignes max) : conventions du secteur à respecter, ce qui fonctionne bien, pièges fréquents, **une opportunité de différenciation**.
- On s'inspire, on ne copie pas : aucune reprise de logo, de visuel ou de texte d'un concurrent.

## Phase 3 — Directions visuelles (1 tour)

Propose **2 ou 3 directions contrastées**, jamais des variations timides d'une même idée. Pour chacune :

- **Nom** évocateur (« Atelier chaleureux », « Cockpit dense »…)
- **Intention** en une phrase : ce que l'utilisateur final doit ressentir
- **Palette** : 4 à 6 couleurs en hex, avec leur rôle (fond, texte, primaire, accent…)
- **Typographies** : titres + corps (Google Fonts ou polices système), avec la justification
- **Densité et rythme** : aéré / équilibré / dense ; angles vifs ou arrondis
- **Élément signature** : le détail dont on se souviendra
- **Risque** : ce qui pourrait mal vieillir ou déplaire

Demande en même temps 1 à 3 sites que l'utilisateur aime (ou déteste) et pourquoi. L'utilisateur choisit une direction ou en mixe deux ; acte le choix en une ligne.

## Phase 4 — Inventaire des pages / écrans (court)

- Liste les pages ou écrans clés et le parcours principal (5 à 10 lignes, pas plus).
- Choisis avec l'utilisateur **l'écran pivot** à prototyper, celui qui porte le plus de décisions :
  - vitrine / landing → la page d'accueil
  - SaaS / back-office → l'écran de travail principal (dashboard, liste + détail)
  - mobile → l'écran principal de l'app

## Phase 5 — Prototype HTML

Lis `references/prototype.md` pour les règles détaillées. L'essentiel :

- **Un seul fichier** `design/prototype.html`, autonome, sans build : HTML + CSS + JS vanilla. Google Fonts autorisé.
- Les **tokens en variables CSS** dans `:root` en tête du fichier : ce seront ceux du `DESIGN.md`.
- **Contenu réaliste** tiré du projet, jamais de lorem ipsum : le design se juge sur du vrai texte.
- Responsive ; pour du mobile, afficher l'écran dans un cadre de 390 × 844 px centré.
- Contrastes WCAG AA minimum.

Donne ensuite à l'utilisateur la commande pour l'ouvrir (`open design/prototype.html` sur macOS, `xdg-open` sur Linux) et demande des retours **précis** : ce qui plaît, ce qui gêne, ce qui manque.

**Itération** : modifications ciblées sur le même fichier. Si l'utilisateur hésite entre deux options, tu peux ajouter un sélecteur en haut de page qui bascule entre deux jeux de tokens — pas une deuxième page. Au bout de 3 itérations sans convergence, reviens en phase 3 plutôt que de retoucher à l'infini.

## Phase 6 — DESIGN.md

Quand l'utilisateur valide le prototype :

1. Écris `DESIGN.md` à la racine du projet en suivant `references/design-md-template.md`. Les tokens doivent être **identiques** à ceux du prototype validé.
2. Propose (sans le faire d'office) d'ajouter dans `CLAUDE.md` une ligne du type : « Avant tout travail d'interface, lire DESIGN.md et utiliser exclusivement ses tokens. »
3. Termine par un récapitulatif de 3 lignes : direction retenue, fichiers produits, prochaine étape suggérée.
