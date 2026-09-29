# Approfondir un groupe de modules, selon ses dépendances

Suppose le vocabulaire de [vocabulary.md](vocabulary.md).

## Les catégories de dépendance

La catégorie des dépendances d'une piste décide de la façon de tester le module approfondi à sa
jointure.

1. **Dans le processus** : calcul pur, état en mémoire, aucune entrée-sortie. Toujours
   approfondissable : fusionner les modules et tester directement par la nouvelle interface. Pas
   d'adaptateur.
2. **Remplaçable en local** : une dépendance qui a une doublure locale (PGLite pour Postgres, un
   système de fichiers en mémoire). Approfondissable si la doublure existe : les tests la font
   tourner. La jointure reste interne, sans port à l'interface externe.
3. **Distante mais à nous** (ports et adaptateurs) : nos propres services derrière le réseau.
   Définir un **port** (une interface) à la jointure ; le module profond garde la logique, le
   transport est injecté comme adaptateur. Les tests prennent un adaptateur en mémoire, la
   production un adaptateur HTTP, gRPC ou file de messages.
4. **Vraiment externe** (simulée) : un service tiers qu'on ne maîtrise pas (Stripe, Twilio). Le
   module approfondi reçoit la dépendance comme un port injecté ; les tests fournissent un
   adaptateur simulé.

## La discipline des jointures

- **Un adaptateur : jointure hypothétique. Deux : vraie jointure.** Pas de port sans au moins
  deux adaptateurs justifiés (d'ordinaire, la production et les tests). Une jointure à un seul
  adaptateur n'est qu'un détour.
- **Jointures internes et externes** : ne pas exposer une jointure interne dans l'interface
  simplement parce que des tests s'en servent.

## Les tests : remplacer, pas empiler

- Une fois des tests écrits à l'interface du module approfondi, les anciens tests unitaires des
  modules superficiels deviennent inutiles : les supprimer.
- Les nouveaux tests passent par l'interface du module approfondi, et vérifient ce qu'on observe
  par elle, pas l'état interne.
- Ils survivent aux refactorisations internes. Un test qu'il faut changer quand l'implémentation
  change teste au-delà de l'interface.
