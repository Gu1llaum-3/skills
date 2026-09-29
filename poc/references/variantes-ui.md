# Variantes d'interface : plusieurs écrans sur une même route

Pour une question sur **ce à quoi un écran devrait ressembler** dans un projet qui existe déjà :
plusieurs variantes radicalement différentes, qu'on fait défiler dans le navigateur. On en garde
une, ou des morceaux de plusieurs. D'après `prototype` de Matt Pocock. Pour l'identité visuelle
du projet (couleurs, typographie, tokens), c'est `/design`.

## Où les monter

Une variante se juge bien mieux **au milieu du reste de l'application** : le vrai en-tête, la
vraie barre latérale, de vraies données. Seule sur une route vide, toute variante paraît bonne.

- **Sur une page qui existe** (le cas par défaut) : les variantes s'affichent sur la même route,
  choisies par un paramètre `?variant=`. Le chargement des données, les paramètres et
  l'authentification restent ; seul le rendu change. Une chose qui n'a pas encore de page mais
  vivrait naturellement dans une (une nouvelle carte du tableau de bord) se monte dans cette page.
- **Sur une nouvelle page**, en dernier recours, quand rien ne peut l'accueillir : une route
  jetable, selon les conventions de routage du projet, avec `prototype` dans son chemin.

## 1. Fixer le nombre

Trois variantes par défaut, cinq au plus : au-delà, elles cessent d'être vraiment différentes.
Écrire le plan en une ligne en tête du fichier : « Trois variantes de la page réglages, par
`?variant=`, sur la route `/reglages` existante. »

## 2. Des variantes vraiment différentes

Chacune respecte le but de la page, les données disponibles et la bibliothèque de composants du
projet, et exporte un composant nommé (`VarianteA`, `VarianteB`…). Elles diffèrent par la
**structure** : la mise en page, la hiérarchie de l'information, l'action principale. Pas par la
couleur. Si deux brouillons se ressemblent trop, en refaire un avec une consigne explicite
(« pas de grille de cartes »). Un en-tête commun se partage ; une mise en page commune, non.

## 3. Les brancher

Un seul composant d'aiguillage sur la route, sous le chargement des données :

```tsx
// pseudo-code, à adapter au framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VarianteA {...donnees} />}
    {variant === 'B' && <VarianteB {...donnees} />}
    {variant === 'C' && <VarianteC {...donnees} />}
    <SelecteurPrototype variantes={['A', 'B', 'C']} courante={variant} />
  </>
);
```

## 4. La barre de choix

Une petite barre fixe en bas au centre : flèche gauche, le nom de la variante courante
(`B (barre latérale)`), flèche droite, avec retour au début.

- Une flèche met à jour le paramètre d'URL avec le routeur du framework : la variante se partage
  et survit au rechargement.
- Les touches `←` et `→` changent aussi de variante, sauf dans un champ de saisie.
- Elle se distingue nettement de la page, pour qu'on ne la juge pas avec le reste.
- Elle est masquée en production (`process.env.NODE_ENV !== 'production'` ou l'équivalent).

## 5. Montrer

Donner l'URL et les clés `?variant=`. Le retour le plus utile ressemble à « l'en-tête de B avec
la barre latérale de C » : c'est l'écran voulu.

## 6. Garder la réponse

Noter dans le fichier POC la variante retenue et pourquoi. Toutes les variantes et la barre
restent sur la branche `poc/<slug>`, rien de tout ça dans la branche principale. La variante
gagnante se réécrit proprement quand on approfondit : elle a été écrite sans tests.

Les variantes ne modifient rien de réel : une variante qui doit écrire pointe vers un bouchon.
