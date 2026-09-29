# Odeurs de code : la base de l'axe conventions

D'après Martin Fowler (*Refactoring*, chapitre 3). Elles s'appliquent même quand le dépôt ne
documente rien, avec deux règles :

- **Le dépôt l'emporte** : une règle écrite du dépôt qui autorise ce qu'une odeur signalerait
  fait taire l'odeur.
- **Toujours un jugement** : chaque odeur se signale comme « possible <odeur> », jamais comme une
  violation. Ce que l'outillage impose déjà (linter, formateur) ne se signale pas.

Chaque odeur : ce qu'elle est → comment la corriger.

- **Nom mystérieux** : une fonction, une variable ou un type dont le nom ne dit pas ce qu'il fait
  ou contient. → Le renommer ; si aucun nom honnête ne vient, c'est la conception qui est floue.
- **Code dupliqué** : la même forme de logique dans plusieurs morceaux du diff. → Extraire la
  forme commune et l'appeler des deux côtés.
- **Jalousie de fonctionnalité** : une méthode qui manipule les données d'un autre objet plus que
  les siennes. → La déplacer vers les données qu'elle envie.
- **Groupes de données** : les mêmes champs ou paramètres voyagent toujours ensemble. → Les réunir
  dans un type, et passer ce type.
- **Obsession des primitifs** : une chaîne ou un nombre tient lieu d'une notion du domaine qui
  mériterait son type. → Lui donner un petit type à elle.
- **Aiguillages répétés** : le même `switch` ou la même cascade de `if` sur le même type revient
  dans le diff. → Polymorphisme, ou une table partagée par les deux endroits.
- **Chirurgie au fusil** : un seul changement logique oblige à modifier de nombreux fichiers. →
  Regrouper ce qui change ensemble dans un seul module.
- **Changement divergent** : un fichier ou un module modifié pour plusieurs raisons sans rapport.
  → Le découper pour que chaque module change pour une seule raison.
- **Généralité spéculative** : une abstraction, un paramètre ou un point d'extension ajouté pour un
  besoin que la spec n'a pas. → Le supprimer, et le remettre le jour où le besoin existe.
- **Chaînes de messages** : une longue navigation `a.b().c().d()` dont l'appelant ne devrait pas
  dépendre. → La cacher derrière une méthode du premier objet.
- **Intermédiaire** : une classe ou une fonction qui ne fait presque que déléguer. → La retirer et
  appeler directement la vraie cible.
- **Héritage refusé** : une sous-classe qui ignore ou redéfinit presque tout ce dont elle hérite. →
  Abandonner l'héritage au profit de la composition.
