---
name: naming
description: Trouver un nom de projet (app, SaaS, CLI, site, produit, bibliothèque) et vérifier réellement sa disponibilité — domaines, GitHub, npm, homonymes, pistes de marque — puis consigner le choix dans docs/nommage.md.
argument-hint: "[projet ou noms envisagés]"
disable-model-invocation: true
---

# Naming : trouver un nom et le vérifier

L'objectif est d'aboutir à **un nom choisi en connaissance de cause** : qui a du sens, se
prononce bien, se distingue dans son secteur, et dont la disponibilité a été **réellement
vérifiée**, pas supposée. Le choix est consigné dans `docs/nommage.md`.

Le travail de génération et de tri se fait sans bruit : l'utilisateur voit une shortlist, pas 40
noms bruts.

## La règle d'honnêteté

Ne jamais affirmer qu'un domaine, un compte ou une marque est libre sans l'avoir vérifié par le
script ou une recherche effective. Trois statuts seulement : **libre**, **pris**, **inconnu**. En
cas de doute, c'est **inconnu**. Pour les marques, ne jamais conclure « marque libre » : signaler
ce qu'on a trouvé et fournir les liens pour la vérification humaine. Un nom présenté à tort comme
disponible fait perdre bien plus de temps qu'il n'en fait gagner.

## 1. Comprendre le projet

**Si le projet existe déjà**, en faire le tour avant toute question :

1. Lire `README.md`, `CLAUDE.md`, `ROADMAP.md`, `docs/cahier-des-charges.md`,
   `docs/design/DESIGN.md` (ou leurs équivalents à la racine dans un projet plus ancien).
2. Lire le manifeste (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`,
   `composer.json`…) : nom actuel, description, dépendances révélatrices.
3. Parcourir l'arborescence (2 niveaux) et les points d'entrée : routes, écrans principaux,
   commandes CLI, modèles de données. Les libellés d'interface et les fichiers de traduction
   disent beaucoup du vocabulaire métier.
4. Regarder le nom du remote git et le nom de code actuel s'il existe.

Ne pas lire tout le code : il s'agit de comprendre ce que fait le logiciel, pour qui, et avec
quel vocabulaire, pas de l'auditer.

Restituer cette compréhension en **5 lignes au maximum** (ce que ça fait, pour qui, ce qui le
distingue, le vocabulaire métier clé, le nom actuel) et demander de corriger. C'est ce résumé qui
guide toute la suite : une erreur ici donne de mauvais noms.

## 2. Cadrer

Appeler le Skill tool avec « interview », pour une ou deux séries, en ne posant que ce que
l'exploration n'a pas révélé. À choisir parmi :

- ce que fait le produit en une phrase, et pour qui (s'il n'y a pas de projet) ;
- **les langues acceptées** : anglais, français, latin, grec ancien, autre langue (japonais,
  finnois, breton…), néologisme sans langue ;
- **le ton** : sérieux, technique, chaleureux, ludique, premium ;
- doit-il **se prononcer naturellement en français et en anglais** ? (par défaut : oui) ;
- **la portée** : outil interne, produit public, open source, marque commerciale (elle fixe le
  niveau d'exigence sur les marques) ;
- **les extensions voulues** : `.fr`, `.com`, `.app`, `.dev`, `.io`… (par défaut selon la
  portée : `.fr` et `.com` pour un produit français) ;
- la longueur maximale, les mots ou sonorités à éviter, les noms déjà envisagés ou rejetés (et
  pourquoi).

## 3. Cartographier le secteur

Appeler le Skill tool avec « research » : comment se nomment les concurrents et les produits
voisins. Restituer en 8 lignes au maximum :

- **les motifs saturés** (« tout finit en -ly », « tout le monde utilise un mot grec »,
  « préfixe Smart- partout ») ;
- **les espaces libres** : les registres que personne n'occupe ;
- **les noms à éviter**, trop proches d'un acteur existant.

## 4. Générer

Lire [references/generation.md](references/generation.md). Générer environ **40 candidats**
répartis entre les familles pertinentes, en exploitant le vocabulaire métier de l'étape 1 et les
espaces libres de l'étape 3. Pour chaque nom issu d'une langue, noter son **sens exact** et sa
langue. Ne pas inventer d'étymologie : en cas de doute sur le sens d'un mot étranger, le vérifier
par une recherche.

## 5. Filtrer et noter

Éliminer sans pitié :

- ce qui est imprononçable ou ambigu à l'oral en français ou en anglais (si c'est requis) ;
- l'orthographe impossible à dicter au téléphone ;
- un sens négatif, vulgaire ou ridicule dans une langue courante (anglais, espagnol, italien,
  allemand, portugais au minimum) ;
- ce qui est trop proche d'un acteur relevé à l'étape 3.

Noter les survivants avec la grille de [references/generation.md](references/generation.md) et
garder une **shortlist de 8 à 12**.

## 6. Vérifier

Lancer le script sur la shortlist :

```bash
python3 <chemin-du-skill>/scripts/check_names.py nom1 nom2 nom3 --tlds fr,com,app --github --npm
```

- `--npm` seulement si c'est pertinent (bibliothèque, outil de développement, CLI).
- Le script fait : résolution DNS, RDAP (avec détection des TLD non couverts), repli sur `whois`
  s'il est installé, comptes GitHub, paquets npm. Il ne répond « libre » que sur une preuve
  positive.
- Si beaucoup de résultats sont **inconnus** (souvent faute de `whois`), le dire et suggérer
  `brew install whois` ou `sudo apt install whois`, ou une vérification chez un registrar.

Compléter par des **recherches web** pour chaque nom de la shortlist :

- `"<nom>" <secteur>` et `"<nom>" app` : un produit homonyme dans le même domaine ?
- la présence sur l'App Store et Google Play, si c'est une app mobile ;
- les réseaux sociaux si l'utilisateur en a besoin (par recherche, sans garantie).

Puis appliquer [references/marques.md](references/marques.md) : pour les 3 finalistes, fournir
les liens de recherche et les classes de Nice pertinentes. Si la portée est « outil interne »,
indiquer simplement que la vérification de marque n'est pas prioritaire.

## 7. Présenter et choisir

Présenter la shortlist dans un tableau : nom, famille, sens ou origine, note, statut des domaines
demandés, GitHub, homonymes repérés. Puis détailler un **top 3**, avec pour chacun :

- le sens, et pourquoi il colle au projet ;
- comment il sonne en français et en anglais ;
- les risques (homonyme, domaine principal pris, marque à vérifier).

Laisser l'utilisateur choisir, mélanger ou relancer. S'il relance, demander ce qui ne va pas
(trop sérieux, trop long, trop abstrait…) et régénérer en ciblant, sans repartir de zéro.

## 8. Consigner

Quand un nom est retenu, écrire `docs/nommage.md` (dans le dossier courant s'il n'y a pas de
projet) en suivant [references/nommage.md](references/nommage.md). Terminer par les actions
concrètes restantes : réserver le domaine, vérifier la marque, renommer le dépôt et le manifeste.
Proposer de faire le renommage technique dans le projet, sans le faire d'office.
