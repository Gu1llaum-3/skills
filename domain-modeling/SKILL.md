---
name: domain-modeling
description: Construire et tenir à jour le glossaire du domaine d'un projet (CONTEXT.md, ou CONTEXT-MAP.md s'il y a plusieurs domaines) pendant qu'on conçoit — confronter les mots employés au glossaire et au code, préciser les termes flous, trancher un seul mot par concept et l'écrire dès qu'il est tranché. Utilise ce skill quand l'utilisateur discute du vocabulaire du projet (« on dit client ou utilisateur ? », « ajoute ce terme au glossaire »), écrit ou modifie CONTEXT.md, et chaque fois qu'un autre skill (interview, onboard) aborde les notions du domaine.
---

# Domain modeling : le glossaire du domaine

Le glossaire sert à ce que l'utilisateur, Claude et le code disent la même chose avec les mêmes
mots. Sa valeur vient de ce qu'il est **tranché** : chaque terme y entre parce qu'on a choisi un
mot pour un concept, pas parce qu'on l'a trouvé dans le code. Ce skill est la pratique
**active** : contester les mots, inventer des cas limites, écrire au moment où c'est décidé.
Simplement lire `CONTEXT.md` pour reprendre son vocabulaire n'est pas ce skill : c'est une
habitude que tout skill peut avoir (voir « Pour les autres skills »).

Réponds dans la langue de l'utilisateur.

## Où vit le glossaire

- **Un seul domaine** (presque tous les dépôts) : `CONTEXT.md` à la racine.
- **Plusieurs domaines** (monorepo, services distincts) : un `CONTEXT-MAP.md` à la racine liste
  les domaines, où vit le `CONTEXT.md` de chacun, et comment ils se parlent. Quand le sujet ne
  désigne pas clairement un domaine, demander lequel.
- **Aucun fichier** : créer `CONTEXT.md` au premier terme tranché, pas avant.

Format : [references/context-format.md](references/context-format.md).

## Pendant la session

- **Confronter au glossaire** : quand l'utilisateur emploie un mot en conflit avec
  `CONTEXT.md`, le dire tout de suite. « Le glossaire définit *annulation* comme X, tu sembles
  parler de Y. Lequel ? »
- **Préciser le flou** : face à un mot vague ou surchargé, proposer un terme précis. « Tu dis
  *compte* : le Client ou l'Utilisateur ? Ce n'est pas la même chose. »
- **Éprouver avec des scénarios** : quand on parle des relations entre notions, inventer des
  cas concrets qui testent les frontières (« un client sans commande peut-il avoir un avoir ? »).
- **Confronter au code** : quand l'utilisateur dit comment une chose marche, vérifier que le
  code est d'accord, et signaler l'écart. « Le code annule des commandes entières, tu viens de
  dire qu'une annulation partielle est possible. Lequel est juste ? »
- **Écrire tout de suite** : un terme tranché s'écrit dans `CONTEXT.md` au moment où il l'est,
  sans attendre la fin de la session. Montrer la ligne ajoutée en une phrase.

`CONTEXT.md` est un glossaire et rien d'autre : ni spec, ni brouillon, ni décisions
d'implémentation. Une décision difficile à défaire, surprenante sans contexte et issue d'un vrai
compromis se propose en ADR, via le skill `adr`.

## Pour les autres skills

Tout skill qui lit le projet (`feature`, `plan`, `to-spec`, `implement`…) applique ces règles,
sans appeler ce skill :

- lire `CONTEXT.md` (ou `CONTEXT-MAP.md` puis le bon `CONTEXT.md`) **s'il existe** ; s'il
  n'existe pas, continuer sans le signaler ni proposer de le créer ;
- nommer les notions du domaine avec les termes du glossaire, dans les titres de tickets, les
  specs, les plans, les noms de tests et le code, jamais avec un synonyme de la liste « À
  éviter » ;
- une notion dont on a besoin et qui manque au glossaire est un signal : soit on invente un mot
  que le projet n'emploie pas (se reprendre), soit il y a un vrai trou (le proposer à
  l'utilisateur, qui peut le trancher avec ce skill).

## Ce que ce skill ne fait jamais

- Écrire un terme que l'utilisateur n'a pas tranché, ou deviner un glossaire depuis le code.
- Mettre dans `CONTEXT.md` des notions générales de programmation ou des détails
  d'implémentation.
- Changer une définition existante sans le dire.
