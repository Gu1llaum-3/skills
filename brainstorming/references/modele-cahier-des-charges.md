# Modèle de cahier des charges

Utilise cette structure comme point de départ. Supprime les sections qui ne s'appliquent pas, et renomme-les selon le domaine (par exemple « Progression pédagogique » pour une app éducative, « Parcours utilisateur » pour un SaaS).

```markdown
# <Nom de travail du projet> — Cahier des charges

> Version 0.1 — brouillon à valider. Les points marqués **[À valider]** attendent ta décision.

## 1. Vision
Une ou deux phrases : pour qui, pour quoi faire, avec quel fil conducteur.

### Principes non négociables
3 à 6 principes issus du domaine et des réponses (par exemple « jamais punitif », « hors ligne »), chacun avec son pourquoi en une phrase.

## 2. Public et plateformes
Un tableau : public, V1, V2, V3, profils, hors ligne, publication.

## 3. <Cœur métier : progression, parcours, règles du domaine>
Le contenu structurant du produit, sous forme de tableau quand c'est possible. Signale les pièges du domaine.

## 4. Structure d'une unité d'usage (<chapitre, session, écran, commande…>)
Le déroulé pas à pas.

## 5. Fonctionnalités détaillées
Une sous-section par fonctionnalité : comportement, et écarts corrigés par rapport au prototype.

## 6. <Motivation, récompenses, monétisation…> (si pertinent)
Des règles chiffrées : seuils, paliers.

## 7. Univers, contenus et identité
Personnages, textes, ton. Les noms encore inconnus sont centralisés dans la configuration.

## 8. Technique
### 8.1 Stack (avec le pourquoi)
### 8.2 Organisation du code (arborescence proposée)
### 8.3 Services externes (fournisseur recommandé, solution de repli, coût, sources)
### 8.4 Outillage de validation (scripts qui vérifient les règles métier automatiquement)
### 8.x Graphisme, accessibilité, polices

## 9. Espace d'administration / parent / réglages

## 10. Contraintes transverses (durée d'usage, sécurité, RGPD…)

## 11. Découpage en jalons
Un tableau : M1 (socle utilisable), M2, M3… jusqu'à la publication. Pour chaque jalon : son objectif en une phrase, et ce qu'on pourra montrer à la fin.

**Envergure : simple | gros** — la raison en une phrase (par exemple « chaque jalon tient en une session » ou « M2 demande plusieurs sessions : synchronisation et mode hors ligne »).

## 12. Licences (règle permanente) — seulement si le projet sera publié

## 13. Questions ouvertes
1. Un point [À valider] par ligne, formulé comme une question avec une proposition par défaut.
```

## Règles d'écriture

- Pour chaque décision : ce qui a été choisi, la valeur (chiffre, nom) et le pourquoi en une demi-phrase.
- Préfère les tableaux pour les comparaisons, les progressions et les jalons.
- Les marqueurs **[À valider]** apparaissent là où la supposition est faite, **et** sont repris dans la section « Questions ouvertes ».
