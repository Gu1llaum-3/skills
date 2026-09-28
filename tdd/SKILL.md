---
name: tdd
description: Écrire du code en TDD (test d'abord, rouge puis vert) avec des tests qui valent la peine d'être gardés — comportement testé par l'interface publique, pas de mocks internes, pas de tests tautologiques, une tranche verticale à la fois. Utilise ce skill dès que l'utilisateur veut développer une fonctionnalité ou corriger un bug dont la cause est connue en commençant par le test, parle de TDD, de « test d'abord », de « red-green », de tests d'intégration, ou demande d'écrire ou d'améliorer des tests ; et chaque fois qu'un autre skill (comme implement) demande d'écrire du code en TDD. Pour un bug qui résiste, c'est debug.
---

# Test-Driven Development

Le TDD, c'est la boucle rouge → vert. Ce skill en donne les règles, et surtout ce qui fait qu'un
test mérite d'être gardé : ce qu'est un bon test, où il se place, les pièges à éviter. Chaque
section s'applique à chaque cycle : on la consulte avant et pendant la boucle, pas après.

**Les conventions du dépôt priment toujours** (framework de test, emplacement et nommage des
fichiers, langue des noms de tests, commandes). Ce skill ne donne que les réglages par défaut.

## Préalables

- **Commandes** : trouver celle qui lance un seul fichier de test et celle de la vérification
  complète (`CLAUDE.md`, `package.json`, `mise.toml`, `Makefile`, `justfile`…). Si elles sont
  introuvables, les demander avant le premier test.
- **Tests existants** : lire deux ou trois tests voisins pour reprendre leur style, leurs helpers et
  leurs fixtures plutôt que d'en inventer.

## Ce qu'est un bon test

Un test vérifie un **comportement** à travers une **interface publique**, jamais un détail
d'implémentation. Le code peut changer de fond en comble ; le test, lui, ne doit pas bouger. Un bon
test se lit comme une spécification : « un utilisateur peut valider un panier valide » dit
exactement quelle capacité existe, et il survit aux refactorisations parce qu'il ignore la
structure interne.

Exemples de bons et mauvais tests dans [references/tests.md](references/tests.md), règles sur les
mocks dans [references/mocking.md](references/mocking.md).

## Où placer les tests : les interfaces à tester

On teste à la **frontière publique** d'un module (fonction exportée, route HTTP, commande CLI,
composant tel que l'utilisateur le voit) : l'endroit où l'on observe le comportement sans regarder
à l'intérieur. Jamais contre des fonctions internes.

On ne peut pas tout tester : fixer ces interfaces à l'avance, c'est ce qui fait porter l'effort sur
les chemins critiques et la logique complexe plutôt que sur chaque cas limite.

- **Avec un plan ou une spécification validés** (appel depuis `implement`, par exemple) : les
  interfaces se déduisent de la tâche et de ses critères. On ne redemande rien, sauf si la tâche
  laisse réellement le choix ; on pose alors une question courte.
- **Sans plan** : avant le premier test, proposer en quelques lignes les interfaces à tester et les
  comportements qu'on y vérifiera, et attendre l'accord. Aucun test sur une interface non validée.

## La boucle

1. **Rouge.** Écrire un seul test, qui exprime un seul comportement. Le lancer seul et **constater
   l'échec pour la bonne raison** : une assertion qui échoue, pas un import manquant ni une erreur
   de syntaxe. Si le code n'existe pas encore, créer d'abord un squelette vide (signature qui
   renvoie une valeur neutre ou lève « non implémenté »). Un test qui n'a jamais échoué ne prouve
   rien.
2. **Vert.** Écrire le code **minimal** qui fait passer ce test, sans anticiper les suivants ni
   ajouter de fonctionnalité spéculative. Relancer et constater le succès.
3. **Refactoriser**, si besoin, en gardant le test vert : noms, duplication, découpage. Relancer
   après chaque changement.
4. **Recommencer** avec le comportement suivant. Chaque test est une balle traçante : il tient
   compte de ce que le cycle précédent a appris.

À chaque cycle, **montrer la commande et la ligne d'échec, puis celle du succès**. C'est la seule
preuve que la boucle a vraiment eu lieu.

- **Correctif** : commencer par le test qui **reproduit** le bug, et le voir échouer avant de
  toucher au code.
- **Nommer le test** d'après le comportement ou la règle qu'il prouve (le *quoi*, pas le
  *comment*), avec l'identifiant du critère s'il y en a un (`AC-2`, `COM-04`).
- **Valeurs attendues** : des littéraux connus, un exemple calculé à la main, la spécification.
  Jamais une valeur recalculée comme le fait le code.

## Les pièges

- **Test couplé à l'implémentation** : il mocke des collaborateurs internes, teste des fonctions
  privées, compte les appels, ou vérifie par un chemin détourné (lire la base au lieu de passer
  par l'interface). Le signe : il casse lors d'une refactorisation alors que le comportement n'a
  pas changé.
- **Test tautologique** : l'assertion refait le calcul du code (`expect(add(a, b)).toBe(a + b)`,
  un snapshot produit de la même façon, une constante comparée à elle-même). Il passe par
  construction et ne peut jamais contredire le code.
- **Découpage horizontal** : écrire tous les tests, puis tout le code. Ces tests vérifient un
  comportement *imaginé* : ils figent la forme des choses avant qu'on ait compris
  l'implémentation, et deviennent insensibles aux vrais changements. On avance par **tranches
  verticales** : un test, son code, puis le suivant.
- **Test adapté au code** : si un test échoue, on corrige le code, pas l'assertion. Changer le test
  n'est légitime que si c'est lui qui exprimait mal le comportement attendu, et on le dit.

## Ce que ce skill ne fait jamais

- Écrire du code de production avant le test qui l'exige.
- Passer au vert sans avoir vu le rouge, ou annoncer un succès sans avoir lu la sortie du test.
- Désactiver, ignorer ou affaiblir un test pour le faire passer.
- Mocker du code qu'on contrôle.
