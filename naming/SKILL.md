---
name: naming
description: Trouver un nom pour un projet — application web, SaaS, application mobile, outil CLI, site, produit, bibliothèque — et vérifier qu'il est réellement disponible. Cadre le besoin (en explorant le projet s'il existe déjà), cartographie les noms du secteur, génère des candidats par familles (mot anglais, mot étranger ou ancien porteur de sens, composé, néologisme…), les filtre et les note, puis vérifie domaines, GitHub, npm et homonymes via un script, et fournit les liens de recherche de marques. Utilise ce skill dès que l'utilisateur cherche un nom, veut renommer un projet, hésite entre plusieurs noms, demande si un nom est libre ou déjà pris, ou cherche un nom de domaine, même s'il ne dit pas explicitement « nommage ».
---

# Nommage

Objectif : aboutir à **un nom choisi en connaissance de cause** — qui a du sens, se prononce bien, se distingue dans son secteur, et dont la disponibilité a été **réellement vérifiée**, pas supposée. Résultat consigné dans `NOMMAGE.md`.

## Règle d'honnêteté (la plus importante)

Ne jamais affirmer qu'un domaine, un compte ou une marque est libre sans l'avoir vérifié par le script ou une recherche effective. Trois statuts seulement : **libre**, **pris**, **inconnu**. En cas de doute, c'est **inconnu**. Pour les marques, tu ne conclus jamais « marque libre » : tu signales ce que tu as trouvé et tu fournis les liens pour la vérification humaine. Un nom présenté à tort comme disponible fait perdre bien plus de temps qu'il n'en fait gagner.

## Conduite

- Tours de questions courts (3-4 questions max, avec défauts proposés). Utilise `AskUserQuestion` s'il est disponible.
- Le travail de génération et de tri se fait en silence ; l'utilisateur voit une shortlist, pas 40 noms bruts.
- En français avec l'utilisateur.

## Phase 1 — Cadrage

### Si le projet existe déjà (dépôt présent)

Avant toute question, fais le tour du projet pour savoir de quoi on parle :

1. Lis `README.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `DESIGN.md`, un cahier des charges s'il y en a un.
2. Lis le manifeste (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `composer.json`…) : nom actuel, description, dépendances révélatrices.
3. Parcours l'arborescence (2 niveaux) et les points d'entrée : routes, écrans principaux, commandes CLI, modèles de données. Les libellés d'interface et fichiers de traduction disent beaucoup du vocabulaire métier.
4. Regarde le nom du remote git et le nom de code actuel s'il existe.

Ne lis pas tout le code : l'objectif est de comprendre ce que fait le logiciel, pour qui, et avec quel vocabulaire, pas d'auditer.

Restitue ensuite ta compréhension en **5 lignes max** (ce que ça fait, pour qui, ce qui le distingue, vocabulaire métier clé, nom actuel) et demande à l'utilisateur de corriger. C'est ce résumé qui guide toute la suite : une erreur ici donne de mauvais noms.

### Questions de cadrage

Ne pose que ce que l'exploration n'a pas révélé. Pioche parmi :

- Ce que fait le produit en une phrase, et pour qui (si pas de projet existant)
- **Langues acceptées** : anglais, français, latin, grec ancien, autre langue (japonais, finnois, breton…), néologisme sans langue
- **Ton** : sérieux / technique / chaleureux / ludique / premium
- Doit-il **se prononcer naturellement en français et en anglais** ? (défaut : oui)
- **Portée** : outil interne, produit public, open source, marque commerciale ? (détermine le niveau d'exigence sur les marques)
- **Extensions voulues** : `.fr`, `.com`, `.app`, `.dev`, `.io`… (défaut selon portée : `.fr` + `.com` pour un produit français)
- Longueur max, mots ou sonorités à éviter, noms déjà envisagés ou rejetés (et pourquoi)

## Phase 2 — Cartographie du secteur

Avec la recherche web (5 à 8 recherches) : comment se nomment les concurrents et produits voisins.

Restitue en 8 lignes max :
- **Motifs saturés** (ex. « tout finit en -ly », « tout le monde utilise un mot grec », « préfixe Smart- partout »)
- **Espaces libres** : les registres que personne n'occupe
- **Noms à éviter** car trop proches d'un acteur existant

## Phase 3 — Génération (silencieuse)

Lis `references/generation.md`. Génère environ **40 candidats** répartis entre les familles pertinentes, en exploitant le vocabulaire métier relevé en phase 1 et les espaces libres de la phase 2. Pour chaque nom issu d'une langue, note son **sens exact** et sa langue — ne pas inventer d'étymologie ; en cas de doute sur le sens d'un mot étranger, vérifie-le par une recherche.

## Phase 4 — Filtre et notation (silencieux)

Élimine sans pitié :
- imprononçable ou ambigu à l'oral en français ou en anglais (si requis)
- orthographe impossible à dicter au téléphone
- sens négatif, vulgaire ou ridicule dans une langue courante (anglais, espagnol, italien, allemand, portugais au minimum)
- trop proche d'un acteur relevé en phase 2

Note les survivants avec la grille de `references/generation.md` et garde une **shortlist de 8 à 12**.

## Phase 5 — Vérification

Lance le script sur la shortlist :

```bash
python3 <chemin-du-skill>/scripts/check_names.py nom1 nom2 nom3 --tlds fr,com,app --github --npm
```

- `--npm` seulement si c'est pertinent (bibliothèque, outil dev, CLI).
- Le script fait : résolution DNS, RDAP (avec détection des TLD non couverts), repli sur `whois` s'il est installé, comptes GitHub, paquets npm. Il ne répond « libre » que sur une preuve positive.
- Si beaucoup de résultats sont **inconnus** (souvent faute de `whois` installé), dis-le et suggère `sudo apt install whois` ou `brew install whois`, ou une vérification chez un registrar.

Complète par des **recherches web** pour chaque nom de la shortlist :
- `"<nom>" <secteur>` et `"<nom>" app` : produit homonyme dans le même domaine ?
- présence sur App Store / Google Play si c'est une app mobile
- réseaux sociaux si l'utilisateur en a besoin (vérification par recherche, sans garantie)

Puis applique `references/marques.md` : pour les 3 finalistes, fournis les liens de recherche et les classes de Nice pertinentes. Si la portée est « outil interne », indique simplement que la vérification de marque n'est pas prioritaire.

## Phase 6 — Présentation et choix

Présente la shortlist dans un tableau : nom, famille, sens/origine, note, statut des domaines demandés, GitHub, homonymes repérés. Puis détaille un **top 3**, pour chacun :
- le sens et pourquoi il colle au projet
- comment il sonne en français et en anglais
- les risques (homonyme, domaine principal pris, marque à vérifier)

Laisse l'utilisateur choisir, mixer ou relancer. S'il relance, demande ce qui ne va pas (trop sérieux, trop long, trop abstrait…) et régénère en ciblant, sans repartir de zéro.

## Phase 7 — NOMMAGE.md

Quand un nom est retenu, écris `NOMMAGE.md` à la racine du projet (ou dans le dossier courant s'il n'y a pas de projet) en suivant `references/nommage-md-template.md`. Termine par les actions concrètes restantes : réserver le domaine, vérifier la marque, renommer le dépôt et le manifeste — et propose de faire le renommage technique dans le projet si l'utilisateur le souhaite (sans le faire d'office).
