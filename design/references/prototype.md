# Règles du prototype HTML

Le prototype sert à **valider une direction**, pas à livrer du code de production. Il doit être rapide à produire et rapide à modifier.

## Format

- Fichier unique : `design/prototype.html`. Crée le dossier `design/` si besoin.
- HTML + CSS + JS vanilla dans le même fichier. Pas de framework, pas de build, pas de CDN hors Google Fonts.
- Doit s'ouvrir par double-clic, hors connexion (à part les polices).

## Structure du CSS

Toutes les valeurs de design passent par des variables dans `:root`, en tête du `<style>`, regroupées ainsi :

```css
:root {
  /* Couleurs */
  --color-bg: #FAF7F2;
  --color-surface: #FFFFFF;
  --color-text: #1C1B19;
  --color-text-muted: #6B6760;
  --color-primary: #1F4E5A;
  --color-accent: #D9822B;
  --color-border: #E6E1D8;

  /* Typographie */
  --font-display: "Fraunces", Georgia, serif;
  --font-body: "Inter", system-ui, sans-serif;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.75rem;
  --text-2xl: 2.5rem;

  /* Espacements, formes */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 1rem;
  --space-4: 1.5rem;
  --space-5: 2.5rem;
  --space-6: 4rem;
  --radius-sm: 4px;
  --radius-md: 10px;
  --shadow-md: 0 4px 16px rgb(0 0 0 / 0.08);
}
```

Aucune couleur ni taille en dur dans le reste du CSS : c'est ce qui rend les itérations rapides et garantit que le `DESIGN.md` correspondra au rendu.

Si le mode sombre est prévu, redéfinis les couleurs sous `@media (prefers-color-scheme: dark)` et ajoute un petit bouton de bascule.

## Contenu

- Textes réalistes issus du projet (nom, offre, vrais libellés de menu). Si l'info manque, invente du plausible et cohérent, jamais de lorem ipsum.
- Pour un SaaS : des données crédibles (noms, montants, dates, statuts variés, y compris un état vide ou une erreur si pertinent).
- Images : pas d'images distantes. Utilise des blocs colorés, du SVG inline simple ou des dégradés, clairement identifiables comme emplacements.

## Ce qu'on montre

- **Vitrine** : hero, 2 ou 3 sections représentatives, pied de page. Pas besoin de toutes les pages.
- **SaaS** : la navigation + l'écran de travail principal, avec au moins un tableau ou une liste, des boutons (principal, secondaire), un champ de formulaire, un badge de statut.
- **Mobile** : l'écran principal dans un cadre 390 × 844 px centré sur fond neutre, barre de navigation incluse.

Quel que soit le type, inclure les états qui comptent : survol, focus visible (clavier), désactivé.

## Qualité minimale

- Contraste texte / fond WCAG AA (4,5:1 pour le texte courant).
- Responsive : le rendu tient de 360 px à 1440 px.
- Focus clavier visible.

## Sélecteur de variantes (optionnel)

Si l'utilisateur hésite entre deux directions, ajoute en haut à droite un petit sélecteur qui applique un attribut `data-theme` sur `<html>`, chaque thème redéfinissant les variables. Une seule page, plusieurs jeux de tokens.
