# Vérification des marques

Tu ne peux pas conclure qu'une marque est libre : les bases officielles ne s'interrogent pas de façon fiable par script, et l'appréciation d'un risque (similarité phonétique, produits similaires) relève d'un humain, voire d'un conseil en propriété industrielle pour un produit commercial. Ton rôle : **préparer la vérification** et signaler ce que tu as déjà trouvé par recherche web.

## Bases à consulter

| Base | Couverture | Lien |
|---|---|---|
| **INPI** (base marques) | marques françaises | https://data.inpi.fr/ |
| **TMview** | marques de l'UE, des offices nationaux européens et de nombreux offices partenaires, en une recherche | https://www.tmdn.org/tmview/ |
| **EUIPO eSearch** | marques de l'Union européenne | https://euipo.europa.eu/eSearch/ |
| **WIPO Global Brand Database** | marques internationales (Madrid) et nombreux offices nationaux | https://branddb.wipo.int/ |

Pour un projet ciblant la France : INPI + TMview suffisent en première approche. Pour un produit international : ajouter WIPO.

## Classes de Nice pertinentes

Indique à l'utilisateur les classes à filtrer selon le projet :

| Classe | Couvre notamment |
|---|---|
| **9** | logiciels téléchargeables, applications mobiles |
| **42** | SaaS, conception et développement de logiciels, hébergement |
| **35** | publicité, gestion commerciale, vente en ligne |
| **38** | télécommunications, messagerie, plateformes de communication |
| **41** | éducation, formation, divertissement, jeux |
| **44** | services médicaux, santé, bien-être |

Un logiciel se vérifie presque toujours en 9 + 42, plus la classe du métier servi.

## Ce qu'il faut expliquer à l'utilisateur

- Une recherche doit porter sur le nom **exact** et sur les **variantes proches à l'oral** (ex. « Kalia » / « Calya ») : l'antériorité s'apprécie aussi sur la ressemblance phonétique.
- Une marque identique dans une classe sans rapport n'est généralement pas bloquante ; dans la même classe, elle l'est.
- Un nom **sans dépôt** mais utilisé par un produit actif dans le même secteur reste un risque (et une source de confusion pour les utilisateurs) : c'est pourquoi la recherche web d'homonymes compte autant que les bases.
- Pour un outil interne ou un projet perso non commercialisé, le risque est faible : la vérification sert surtout à éviter la confusion.
- Pour un produit commercial, déposer la marque avant le lancement public est une bonne pratique ; un conseil en propriété industrielle peut faire une recherche d'antériorité plus poussée.

## Format de restitution pour chaque finaliste

```
**<Nom>** : à vérifier en classes 9, 42 (+ <classe métier>)
- Recherche web : <ce qui a été trouvé, ou « aucun homonyme repéré dans le secteur »>
- INPI : https://data.inpi.fr/  → rechercher « <nom> »
- TMview : https://www.tmdn.org/tmview/  → rechercher « <nom> » + variantes « <v1> », « <v2> »
```
