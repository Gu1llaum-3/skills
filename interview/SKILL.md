---
name: interview
description: "Entretien critique pour éclaircir une idée, un besoin ou un plan jusqu'à ce que rien d'important ne reste supposé en silence : le besoin avant la solution, les faits cherchés, seules les décisions posées, les questions du métier mises de côté. Utilise ce skill quand l'utilisateur veut être challengé ou questionné sur son idée ou son plan (« challenge-moi », « pose-moi des questions », « grill me »)."
---

# Entretien

L'entretien sert à atteindre une **compréhension partagée** : ce qu'on construit, pour qui,
pourquoi, et ce qu'on a décidé de ne pas faire. Il est critique par principe : une idée qui
ressort de l'entretien sans avoir été questionnée n'a pas été cadrée.

Le skill appelant peut fixer un cadre (nombre de séries, thèmes à couvrir) : le respecter.

**Le vocabulaire** : si l'entretien porte sur les notions du domaine (ce que sont une commande,
un avoir, un client, et leurs règles), et pas seulement sur de la technique, appeler le Skill
tool avec « domain-modeling » dès le début. Il fait confronter les mots au glossaire et au code
au fil des séries, et écrit dans `CONTEXT.md` chaque terme tranché.

## 1. Questionner le besoin avant la solution

Avant de parler de comment, s'assurer du quoi et du pourquoi :

- **Le problème réel** : qu'est-ce qui ne va pas aujourd'hui, pour qui, à quelle fréquence ?
- **Et si on ne le faisait pas ?** Si la réponse est « pas grand-chose », le dire.
- **La version la plus simple** qui résoudrait l'essentiel du problème.
- **L'existant** : une fonction du projet, une bibliothèque, un outil qui le fait déjà.

Être franc : si une idée paraît mauvaise, trop coûteuse pour ce qu'elle apporte, ou en conflit
avec une décision passée (`docs/adr/`), le dire avec la raison, puis proposer mieux. Pas de
compliments de politesse ; un enthousiasme sincère en une phrase pour une bonne idée, oui.

## 2. Les faits se cherchent, les décisions se demandent

Ne jamais demander à l'utilisateur ce qu'on peut trouver soi-même : dans le code, les docs, les
ADR, les tickets, sur le web. Pour une recherche qui prend du temps, lancer un sous-agent (code)
ou appeler le Skill tool avec « research » (web), et **ne pas bloquer** : poser tout de suite
les questions qui n'en dépendent pas.

Les **décisions** sont posées à l'utilisateur, et on attend sa réponse.

Certaines décisions ne lui appartiennent pas : elles relèvent du **métier** (client, product
owner, juridique, opérationnels). Les signaux :

- une **règle métier** : tarif, remise, remboursement, droit d'accès, délai contractuel ;
- le **juridique ou la conformité** : durée de conservation, mention obligatoire, consentement ;
- un **chiffre que seuls les opérationnels connaissent** : volume, fréquence, pic saisonnier ;
- une **priorité produit** ou un arbitrage entre équipes ou entre clients ;
- une zone floue d'un **ticket écrit par quelqu'un d'autre** : c'est à son auteur d'y répondre ;
- l'utilisateur a déjà répondu « c'est au métier » sur un sujet voisin.

Une telle question se pose quand même à l'utilisateur, qui connaît peut-être la réponse, mais
avec l'option **« À demander au métier »** (voir la série). Pas d'option sur les autres
questions : elle deviendrait une porte de sortie.

## 3. Travailler par séries

Voir l'idée comme un **arbre de décisions** : chaque décision ouvre celles qui en dépendent. La
**frontière**, ce sont les décisions dont tous les prérequis sont tranchés : celles qu'on peut
poser maintenant sans deviner une réponse qu'on n'a pas encore.

- À chaque série, poser la frontière, de la décision la plus structurante à la plus fine. Une
  question qui dépend d'une réponse encore ouverte attend la série suivante.
- Utiliser l'outil **AskUserQuestion**, 4 questions au maximum par appel. Si la frontière en
  compte plus, poser les plus structurantes ; les autres passent à la série suivante.
- **2 à 4 options mutuellement exclusives**, dont la description donne le **compromis** (« plus
  de travail, mais un rendu bien meilleur »).
- **L'option recommandée en premier**, suivie de « (Recommandé) ». Pas de recommandation quand
  c'est une vraie affaire de goût.
- Sur une question qui présente un signal métier, la dernière option est **« À demander au
  métier »**, avec en description l'hypothèse qu'on retiendrait en attendant.
- `multiSelect` seulement quand les choix se cumulent ; `preview` pour comparer des maquettes,
  du code ou des schémas. Pas d'option « Autre » : l'outil l'ajoute.
- Une question vraiment ouverte (« raconte-moi comment tu t'en sers aujourd'hui ») se pose en
  texte, une ou deux à la fois, jamais sous forme de choix artificiels.

## 4. Entre deux séries

- **Lire attentivement les réponses libres** : c'est là que l'utilisateur livre ses meilleures
  idées et ses contraintes cachées. Les reprendre telles quelles, et en faire le sujet de la série
  suivante.
- **Signaler les tensions** entre deux réponses en une phrase, puis poser la question qui les
  résout.
- Si l'utilisateur demande un avis, donner une **recommandation franche** en une ou deux lignes.
- Ne jamais reposer une question tranchée. Si une réponse change la cible, l'appliquer à tout ce
  qui suit.
- **Question renvoyée au métier** (l'option, ou une réponse comme « je ne sais pas, faut voir
  avec la compta ») : ne pas la deviner. La noter avec son destinataire s'il est connu, ce que
  la réponse change, et l'hypothèse de travail. Elle est **bloquante** si d'autres décisions en
  dépendent ou si le comportement principal en dépend, sinon on avance avec l'hypothèse. Les
  branches qui en dépendent attendent ; les autres continuent.
- **Voie rapide** : si l'utilisateur dit « fais vite » ou « je te fais confiance », résumer les
  hypothèses restantes en quelques lignes et s'arrêter là. Les questions métier restent des
  questions : la voie rapide ne les transforme pas en hypothèses silencieuses.

## 5. Conclure

L'entretien est fini quand la frontière est vide : chaque branche visitée, rien d'important
supposé en silence. Alors :

1. **Récapituler** les décisions, une ligne chacune, les questions encore ouvertes, et à part
   les **questions pour le métier**, par destinataire, chacune marquée bloquante ou non avec son
   hypothèse.
2. **Demander confirmation** : « Ai-je bien compris ? » Rien ne s'exécute avant l'accord.
3. **ADR** : pour chaque décision difficile à défaire, surprenante sans contexte et issue d'un vrai
   compromis, proposer de l'enregistrer en appelant le Skill tool avec « adr ».

Le skill appelant reprend ensuite la main avec ce récapitulatif. S'il y a des questions pour le
métier, il les écrit dans son document et propose d'en faire un questionnaire avec le skill
`to-questionnaire`.
