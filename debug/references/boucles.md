# Construire la boucle, et les cas particuliers

## Les façons de construire une boucle, à peu près dans l'ordre

1. **Un test qui échoue**, au point d'entrée qui atteint le bug : unitaire, intégration, bout en
   bout.
2. **Un script curl ou HTTP** contre le serveur de développement lancé.
3. **Une commande CLI** avec une entrée de test, dont la sortie est comparée à une sortie connue
   bonne.
4. **Un navigateur sans tête** (Playwright, Puppeteer) qui déroule l'interface et vérifie le DOM,
   la console ou le réseau.
5. **Rejouer une capture** : une vraie requête, une charge ou un journal d'événements enregistré,
   rejoué à travers le code en isolement.
6. **Un banc jetable** : un petit morceau du système (un service, des dépendances simulées) qui
   atteint le bug en un seul appel.
7. **Une boucle de propriétés ou de fuzz** : pour « une sortie parfois fausse », 1 000 entrées au
   hasard, et chercher la forme de l'échec.
8. **Un banc de bissection** : le bug est apparu entre deux états connus (commit, jeu de données,
   version) ; automatiser « démarrer à l'état X, vérifier » pour `git bisect run`.
9. **Une boucle différentielle** : la même entrée dans l'ancienne et la nouvelle version (ou deux
   configurations), et comparer les sorties.
10. **Avec l'utilisateur**, en dernier recours : s'il faut une action humaine (cliquer, se
    connecter), lui donner la commande exacte à lancer et ce qu'il doit coller en retour, étape
    par étape, pour que la boucle reste structurée. Ce qu'il colle, l'agent le lit : lui faire
    rapporter des observations, jamais un identifiant. Se connecter reste une étape qu'il fait
    seul, sans rien coller.

## Resserrer la boucle

Une fois qu'une boucle existe, la traiter comme un produit :

- **Plus rapide** : mettre la préparation en cache, sauter l'initialisation inutile, réduire la
  portée du test.
- **Plus nette** : resserrer la vérification sur le symptôme de l'utilisateur, et lui seul.
- **Plus déterministe** : figer l'heure, fixer la graine aléatoire, isoler le système de fichiers,
  couper le réseau.

Une boucle de 30 secondes et instable ne vaut guère mieux que rien ; une boucle de 2 secondes et
déterministe est un outil puissant.

## Bugs intermittents

Le but n'est pas une reproduction propre, mais un **taux de reproduction plus élevé** : répéter le
déclencheur 100 fois, en parallèle, ajouter de la charge, rétrécir les fenêtres de temps, injecter
des pauses. Un bug qui sort une fois sur deux se débogue ; une fois sur cent, non. Monter le taux
jusqu'à ce qu'il se débogue.

## Régressions de performance

Les logs sont en général le mauvais outil. D'abord une **mesure de référence** (banc de mesure,
`performance.now()`, profileur, plan de requête), puis une **bissection** entre l'état rapide et
l'état lent. Mesurer d'abord, corriger ensuite.

## Instrumenter

Par ordre de préférence :

1. **Débogueur ou REPL**, si l'environnement le permet : un point d'arrêt vaut dix logs.
2. **Des logs ciblés** aux frontières qui départagent les hypothèses.
3. Jamais « tout logger puis chercher ».
