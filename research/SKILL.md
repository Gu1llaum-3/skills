---
name: research
description: "Recherche sur sources primaires, dans un agent en arrière-plan, consignée et sourcée dans docs/research/ : bibliothèque à choisir, bonne pratique, API, réglementation, concurrents. Utilise ce skill quand l'utilisateur veut rechercher, comparer ou vérifier un point sur le web (« compare ces deux bibliothèques », « comment font les autres ? »)."
---

# Recherche

Une recherche vaut ce que valent ses sources. Ce skill délègue la lecture à un **agent en
arrière-plan**, pour que la conversation continue pendant ce temps, et laisse une note sourcée
qu'on pourra relire dans six mois.

## 1. Formuler la question

Avant de lancer l'agent, écrire en quelques lignes :

- **La question**, précise : « quelle bibliothèque d'export PDF pour une app Node, gratuite,
  maintenue, sans dépendance native ? » plutôt que « export PDF ».
- **Le contexte utile** : stack, contraintes (coût, licence, hors ligne, hébergement), ce qui est
  déjà en place dans le projet.
- **Les critères de comparaison**, s'il s'agit de choisir.

Plusieurs questions indépendantes : un agent par question, lancés dans le même message.

## 2. Lancer l'agent

Avec l'outil Agent, en arrière-plan. Lui transmettre la question, le contexte, les critères, le
chemin du fichier à écrire, et ces consignes :

- **Sources primaires** : documentation officielle, code source, spécifications, registres
  (npm, PyPI, crates.io), pages de tarifs et de licences, textes officiels. Remonter chaque
  affirmation jusqu'à la source qui en fait autorité, pas jusqu'à un article qui la résume.
- **Actualité** : noter la date des informations sensibles au temps (versions, prix, maintenance :
  date du dernier commit ou de la dernière version).
- **Choisir** : comparer 2 ou 3 options sur les critères, donner **une recommandation et une
  solution de repli**, et vérifier la licence de toute dépendance proposée.
- **Honnêteté** : distinguer ce qui est vérifié de ce qui est probable ; « non trouvé » plutôt
  qu'une supposition.
- **S'inspirer n'est pas copier** : aucune reprise de texte, de visuel ou de logo d'un tiers.

## 3. Le fichier

`docs/research/<AAAA-MM-JJ>-<slug>.md`, sauf si le dépôt range déjà ce genre de notes ailleurs :
suivre sa convention. Sans dépôt, créer `docs/research/` dans le dossier courant.

```markdown
# <La question>

> Recherche du <JJ/MM/AAAA>. Contexte : <une ligne>.

## En bref

La conclusion en 3 à 5 lignes : la recommandation, le repli, la principale réserve.

## Comparaison

| Option | <critère 1> | <critère 2> | Licence | Source |
|---|---|---|---|---|

## Détails

Les points qui justifient la conclusion, chacun avec sa source ([1], [2]…).

## Sources

1. <titre>, <URL>, consulté le <date>
```

## 4. Restituer

Pendant que l'agent travaille, continuer ce qui n'en dépend pas. À son retour, lire le fichier,
vérifier que les affirmations clés ont bien une source, puis rendre au skill appelant (ou à
l'utilisateur) **la conclusion en 10 lignes au maximum** et le chemin du fichier.
