# Le vocabulaire des modules profonds

Concevoir des **modules profonds** : beaucoup de comportement derrière une petite interface,
placée à une jointure nette, testable par cette interface. Le but : du levier pour ceux qui
appellent le module, de la localité pour ceux qui le maintiennent, et des tests faciles pour
tous. D'après John Ousterhout (*A Philosophy of Software Design*) et Michael Feathers (*Working
Effectively with Legacy Code*).

## Les termes

Employer ces mots exactement : c'est tout l'intérêt d'un vocabulaire commun.

- **Module** : tout ce qui a une interface et une implémentation, à n'importe quelle échelle :
  une fonction, une classe, un paquet, une tranche qui traverse plusieurs couches. *À éviter* :
  unité, composant, service.
- **Interface** : tout ce qu'un appelant doit savoir pour bien utiliser le module : la
  signature, mais aussi les invariants, l'ordre des appels, les cas d'erreur, la configuration
  requise, les performances. *À éviter* : API, signature (trop étroits : ils ne désignent que les
  types).
- **Implémentation** : le code à l'intérieur du module. À distinguer de l'**adaptateur** : un
  petit adaptateur peut avoir une grosse implémentation (un dépôt Postgres), et l'inverse (un
  faux en mémoire). Dire « adaptateur » quand on parle de la jointure, « implémentation »
  sinon.
- **Profondeur** : le levier à l'interface, c'est-à-dire la quantité de comportement qu'un
  appelant (ou un test) atteint pour chaque morceau d'interface à apprendre. Un module est
  **profond** quand beaucoup de comportement tient derrière une petite interface,
  **superficiel** quand l'interface est presque aussi complexe que l'implémentation.
- **Jointure** (*seam*, Feathers) : un endroit où l'on peut changer le comportement sans modifier
  le code à cet endroit ; là où vit l'interface d'un module. Où placer la jointure est une
  décision à part, distincte de ce qu'on met derrière. *À éviter* : frontière (trop proche des
  « contextes délimités » du DDD).
- **Adaptateur** : ce qui remplit une interface à une jointure. Le mot dit un rôle (la place
  qu'il occupe), pas un contenu.
- **Levier** : ce que la profondeur apporte aux appelants : plus de possibilités pour chaque
  morceau d'interface appris. Une implémentation sert N appels et M tests.
- **Localité** : ce que la profondeur apporte aux mainteneurs : les changements, les bugs, le
  savoir et la vérification se concentrent à un seul endroit au lieu de s'éparpiller chez les
  appelants. Corrigé une fois, corrigé partout.

## Profond ou superficiel

```
Module profond                      Module superficiel (à éviter)
┌─────────────────────┐             ┌─────────────────────────────────┐
│  Petite interface   │             │       Grosse interface          │
├─────────────────────┤             ├─────────────────────────────────┤
│                     │             │  Implémentation mince           │
│  Implémentation     │             └─────────────────────────────────┘
│  riche, cachée      │
└─────────────────────┘
```

Face à une interface, se demander : peut-on réduire le nombre de fonctions ? simplifier les
paramètres ? cacher davantage à l'intérieur ?

## Principes

- **La profondeur est une propriété de l'interface**, pas de l'implémentation. Un module profond
  peut être fait de petites pièces remplaçables à l'intérieur ; elles ne font simplement pas
  partie de l'interface. Il peut avoir des **jointures internes** (privées, pour ses propres
  tests) en plus de la **jointure externe** de son interface.
- **Le test de suppression** : imaginer qu'on supprime le module. Si la complexité disparaît, il
  ne faisait que transmettre. Si elle réapparaît chez N appelants, il méritait sa place.
- **L'interface est la surface de test** : appelants et tests passent par la même jointure.
  Vouloir tester *au-delà* de l'interface, c'est le signe que le module a la mauvaise forme.
- **Un adaptateur : jointure hypothétique. Deux adaptateurs : vraie jointure.** Ne pas créer de
  jointure si rien ne varie de part et d'autre.

## Concevoir pour les tests

1. **Recevoir ses dépendances, ne pas les créer** : `traiterCommande(commande, paiement)` se teste,
   une fonction qui fait elle-même `new StripeGateway()` non.
2. **Rendre un résultat plutôt que produire un effet** : `calculerRemise(panier)` qui renvoie la
   remise se teste mieux que `appliquerRemise(panier)` qui modifie le panier.
3. **Une petite surface** : moins de fonctions, moins de tests ; moins de paramètres, une
   préparation plus simple.

## Ce qu'on écarte

- **La profondeur comme rapport entre lignes d'implémentation et lignes d'interface** : cela
  récompense le remplissage. On mesure la profondeur par le levier.
- **« Interface » au sens du mot-clé `interface` ou des méthodes publiques** : trop étroit ;
  l'interface, c'est tout ce qu'un appelant doit savoir.
