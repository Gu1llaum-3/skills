# Le rapport HTML

Un seul fichier HTML autonome, dans le dossier temporaire. Tailwind et Mermaid viennent de leurs
CDN. Mermaid sert aux schémas en forme de graphe ; des `div` et du SVG faits main servent aux
schémas plus éditoriaux (masses, coupes). Mélanger les deux : tout en Mermaid finit par faire
générique.

## Squelette

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <title>Revue d'architecture : {{nom du dépôt}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .jointure { stroke-dasharray: 4 4; }
      .fuite { stroke: #dc2626; }
      .profond { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="pistes" class="space-y-10">...</section>
      <section id="a-attaquer">...</section>
    </main>
  </body>
</html>
```

## En-tête

Nom du dépôt, date, et une légende compacte : boîte pleine = module, trait pointillé = jointure,
flèche rouge = fuite, boîte épaisse et sombre = module profond. Pas de paragraphe
d'introduction : on entre directement dans les pistes.

## La carte d'une piste

Les schémas portent le propos ; la prose est rare et reprend le vocabulaire sans cérémonie. Un
`<article>` par piste :

- **Titre** court, qui nomme l'approfondissement (« Réunir la prise de commande »).
- **Badges** : la force (`Solide` en vert émeraude, `À creuser` en ambre, `Spéculative` en
  ardoise) et la catégorie de dépendance (`dans le processus`, `remplaçable en local`, `ports et
  adaptateurs`, `simulée`).
- **Fichiers** : liste en `font-mono text-sm`.
- **Schéma avant / après** : la pièce centrale, sur deux colonnes.
- **Problème** : une phrase. **Solution** : une phrase.
- **Gains** : des puces de six mots au plus (« Les tests passent par une interface », « Supprimer
  quatre modules superficiels »).
- **Encadré ADR** s'il y a lieu : une ligne sur fond ambre.

Si un schéma a besoin d'un paragraphe pour se comprendre, le redessiner.

## Les schémas

Choisir celui qui convient à la piste, et varier.

- **Graphe Mermaid** (`flowchart`), pour « X appelle Y qui appelle Z, voyez le fouillis ». Le
  poser dans une carte Tailwind ; `classDef` colore les fuites en rouge et le module profond en
  sombre. Un diagramme de séquence montre bien « avant : 6 allers-retours ; après : 1 ».
- **Boîtes et flèches faites main**, quand la mise en page de Mermaid résiste : des `div`
  bordées, des flèches en SVG placées par-dessus. Utile pour un « après » qui montre un seul
  module épais aux pièces internes grisées.
- **Coupe**, pour des couches superficielles empilées : des bandes horizontales (`h-12
  border-l-4`). Avant : six couches minces qui ne font rien ; après : une bande épaisse.
- **Masses**, pour « une interface aussi large que l'implémentation » : deux rectangles par
  module. Avant : presque de la même hauteur ; après : interface courte, implémentation haute.
- **Graphe d'appels replié** : avant, un arbre d'appels en boîtes imbriquées ; après, une seule
  boîte avec les appels devenus internes en transparence.

## Style

- Éditorial plutôt que tableau de bord : de l'air, un titre en `font-serif` si on veut.
- Peu de couleur : un accent (émeraude ou indigo), du rouge pour les fuites, de l'ambre pour les
  mises en garde.
- Des schémas d'environ 320 px de haut, pour que l'avant et l'après tiennent côte à côte.
- Les noms de modules dans les schémas en `text-xs uppercase tracking-wider`.
- Aucun script en dehors de Tailwind et de Mermaid.

## La piste à attaquer d'abord

Une carte plus grande : le nom de la piste, une phrase sur le pourquoi, un lien vers sa carte.

## Le ton

Court et simple, avec les mots de [vocabulaire.md](vocabulaire.md) : module, interface,
implémentation, profondeur, profond, superficiel, jointure, adaptateur, levier, localité. Jamais
composant, service ou unité pour module ; API ou signature pour interface ; frontière pour
jointure ; couche ou enveloppe quand on parle d'un module.

Les gains se disent avec ces mots (« localité : les bugs se concentrent dans un module »,
« levier : une interface, N appels »), jamais « plus maintenable » ou « code plus propre ». Pas
de précautions oratoires : si une phrase peut devenir une puce, en faire une puce ; si une puce
peut disparaître, la supprimer.
