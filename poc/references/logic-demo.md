# Démo de logique : un fichier HTML à manipuler

Pour une question sur **une règle métier, des états et leurs transitions, une forme de données** :
ce qui paraît juste sur le papier et ne sonne faux qu'une fois poussé à travers de vrais cas.
Un seul fichier HTML, sans rien à installer : on peut le donner à quelqu'un qui ne code pas (le
métier, une PO) et le laisser sentir le modèle lui-même. D'après `prototype` de Matt Pocock.

## 1. Écrire la question en tête

La question du fichier POC, en un paragraphe, visible en haut de la page (pas seulement en
commentaire).

## 2. Isoler la logique dans un module pur

La logique qui répond à la question tient dans un seul bloc `<script>`, écrit comme un petit
module pur qu'on pourra reprendre tel quel dans le vrai code. Sa forme dépend de la question :

- **un réducteur** `(état, action) => état`, quand les actions sont des événements distincts ;
- **une machine à états**, quand « quelles actions sont permises maintenant » fait partie de la
  question ;
- **quelques fonctions pures** sur un type de données simple, quand il n'y a pas d'état courant ;
- **une classe** avec des méthodes claires, quand la logique garde vraiment un état interne.

Choisir la forme qui colle à la question, pas la plus facile à brancher sur la page. Le module ne
touche jamais au DOM : la page l'appelle, rien ne remonte dans l'autre sens. C'est ce qui le rend
réutilisable une fois la question tranchée.

## 3. Construire la page

HTML, CSS et JS en ligne, sans framework, sans build, sans serveur : le fichier s'ouvre d'un
double-clic et survit à un envoi par mail. Chaque libellé est dans **la langue du métier** (les
termes de `GLOSSARY.md`), pas celle du code. De haut en bas :

1. **Le titre** et une phrase qui dit ce que la démo permet d'explorer.
2. **L'état courant**, entier, en panneau lisible (des champs nommés, pas un JSON brut),
   réaffiché après chaque clic, avec ce qui vient de changer mis en évidence.
3. **Les boutons libres** : un par action, toujours disponibles, pour essayer dans n'importe quel
   ordre.
4. **Les scénarios guidés**, un par onglet : une description courte (la situation, ce qu'il faut
   regarder), puis les boutons à presser dans l'ordre. Chaque étape est un vrai bouton. Lancer un
   scénario repart d'un état initial connu. Choisir les cas difficiles à raisonner sur le papier :
   le cas nominal, un cas limite, une tentative de faire ce qui devrait être interdit.

Sobre : une belle typographie, de l'air, une couleur d'accent, aucune animation.

## 4. La donner

Ouvrir le fichier, ou le donner à qui doit le manipuler. Les moments utiles sont « attends, ça
ne devrait pas être possible » ou « je pensais que X ferait autre chose » : ce sont les bugs de
**l'idée**, ce que le POC cherche. Ajouter les actions ou les scénarios qu'on demande.

## 5. Garder la réponse

Le module pur validé passe dans le vrai code quand on approfondit ; la page reste sur la branche
`poc/<slug>`, rejouable. Le verdict va dans le fichier POC.

Pas de tests, pas de vraie base de données (sauf si c'est la question), pas de généralisation :
la démo répond à une question.
