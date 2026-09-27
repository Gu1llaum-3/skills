# Gabarit DESIGN.md

Suis cette structure. Reste concis : c'est une référence que Claude relira à chaque session d'UI, pas une plaquette. Viser 80 à 150 lignes.

````markdown
# DESIGN.md — [Nom du projet]

> Référence visuelle du projet. Toute interface doit utiliser ces tokens et respecter ces principes.
> Prototype de référence : `design/prototype.html`

## Intention

[2 ou 3 phrases : pour qui, ce que l'utilisateur doit ressentir, la direction retenue et son nom.]

## Principes

- [4 à 6 règles courtes et actionnables, ex. « Une seule action principale visible par écran »,
  « L'accent orange est réservé aux appels à l'action », « Les tableaux restent denses, les pages marketing aérées »]

## Tokens

À copier tel quel dans le CSS global. Avec Tailwind v4, placer ces variables dans un bloc `@theme`.

```css
:root {
  /* reprendre à l'identique le bloc :root du prototype validé */
}
```

| Token | Valeur | Usage |
|---|---|---|
| `--color-primary` | `#1F4E5A` | boutons principaux, liens |
| … | … | … |

## Typographie

- Titres : [police], [graisses utilisées]
- Corps : [police], [taille de base, interlignage]
- Chargement : [lien Google Fonts ou polices système]

## Composants de base

Pour chacun : apparence et règles d'usage en 1 à 3 lignes.

- **Boutons** : principal, secondaire, discret ; états survol / focus / désactivé
- **Champs de formulaire** : bordure, focus, message d'erreur
- **Cartes / surfaces**
- **Navigation**
- **Badges / statuts** (si pertinent)
- **Tableaux** (si SaaS)

## Mise en page

- Largeur max du contenu, grille, points de rupture responsive
- Rythme vertical (quels espacements entre sections / blocs / éléments)

## Iconographie et images

- Jeu d'icônes retenu, style (trait / plein), taille
- Traitement des photos ou illustrations

## Ton rédactionnel

[2 ou 3 lignes : tutoiement / vouvoiement, registre, longueur des libellés.]

## À ne pas faire

- [3 à 5 interdits concrets, ex. « pas de dégradés violets », « pas plus de deux graisses par écran »]

## Accessibilité

- Contraste minimum AA, focus visible, tailles de cibles tactiles ≥ 44 px
````
