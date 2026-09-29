# Écrire pour un agent

Pour tout document qu'un agent lit : un skill, un `CLAUDE.md` ou `AGENTS.md`, un document atteint
par un renvoi. La forme change, pas l'écriture : les mêmes leviers font que l'agent suit le même
chemin à chaque fois. D'après `writing-for-agents` de Matt Pocock.

## Les renvois

Un **renvoi** est une ligne toujours chargée qui nomme un document qu'on ne charge pas, et dit
quand aller le lire : la description d'un skill en est un, une ligne de `CLAUDE.md` qui pointe
vers un fichier aussi. C'est la formulation du renvoi, pas le document visé, qui décide si
l'agent ira le lire. Un document indispensable derrière un renvoi flou sera lu une fois sur deux :
préciser le renvoi d'abord, et ne recopier le document dans le fichier chargé que si ça ne suffit
pas.

Un renvoi dit ce qu'est le document, puis chaque **cas distinct** où le lire. Il coûte à chaque
tour, donc il s'élague plus durement que le reste :

- le mot qui déclenche vient en premier ;
- un déclencheur par cas : trois synonymes pour le même cas, c'est un cas écrit trois fois ;
- rien de ce que le document dit déjà de lui-même.

## Les deux charges

- **La charge de contexte** : ce qui est toujours chargé (une ligne de `CLAUDE.md`, une
  description de skill) coûte des tokens et de l'attention à chaque tour, que ça serve ou non.
- **La charge cognitive** : ce que l'humain doit retenir (quels documents existent, quand lancer
  quel skill). C'est le prix de son contrôle : la dépenser là où son jugement compte.

Un document atteint par un renvoi ne coûte que la ligne du renvoi. Un document sans renvoi ne
repose que sur la mémoire de l'humain.

## La hiérarchie de l'information

Un document mêle des **étapes** (ce que l'agent fait, dans l'ordre) et de la **référence**
(définitions, règles, faits consultés au besoin). Chaque morceau a sa place sur une échelle :

1. l'étape, dans le fichier ;
2. la référence, dans le fichier ;
3. la référence dans un fichier à part (`references/`), lue seulement quand le renvoi le dit.

Le test : ce dont **tous les cas** ont besoin reste dans le fichier ; ce que seuls certains cas
atteignent va derrière un renvoi. De la référence qui aurait dû sortir enterre les étapes, et
l'agent les suit alors au hasard.

Ce qui parle d'une même notion (sa définition, ses règles, ses exceptions) reste sous un même
titre, pas dispersé. Et un document simplement trop long, même sans une ligne fausse, dilue
l'attention : le remède est l'échelle, ou un découpage par cas.

## Chaque étape finit sur un critère

Le **critère de fin** dit à l'agent que l'étape est faite. Deux qualités :

- **Net** : l'agent distingue-t-il fait de pas fait ? Un critère flou (« une fois le besoin
  compris ») invite à finir trop tôt, attiré par les étapes suivantes. Le préciser d'abord. Si
  c'est impossible et qu'on voit l'agent se presser, cacher la suite derrière une vraie coupure
  (un sous-agent, une autre session).
- **Exigeant** : « chaque modèle modifié est traité » force un travail complet, « faire la liste
  des changements » non.

Les meilleurs critères se vérifient et ne laissent rien de côté.

## Les mots directeurs

Un **mot directeur** est un mot que le modèle connaît déjà et qui porte tout un comportement
(*tranche verticale*, *rouge*, *frontière*). Répété comme un mot, jamais comme une phrase, il
ancre ce comportement à peu de frais. Chercher les passages qui s'y réduisent : trois adjectifs
répétés à trois endroits, une phrase entière pour désigner une idée. En inventer un marche s'il
est bien défini, mais un mot connu ne coûte rien à définir.

Le même mot dans les demandes de l'utilisateur, la doc et le code aide l'agent à relier les trois.

## Dire ce qu'il faut faire

Une interdiction met sous les yeux ce qu'elle interdit, et le rend plus probable : écrire le
comportement voulu (« des commentaires d'une ligne ») plutôt que celui qu'on refuse. Une
interdiction ne se garde que comme garde-fou impossible à dire autrement, et toujours avec le
comportement voulu à côté.

## Élaguer

- **Une seule source** par règle : la changer ne touche qu'un endroit. La même règle écrite deux
  fois coûte en tokens et en entretien, et paraît plus importante qu'elle n'est.
- **L'environnement est une source** : les scripts de `package.json`, les fichiers de
  configuration, l'arborescence, la sortie de `--help`. Les recopier, c'est un **cache** qui
  vieillira. N'écrire que ce qu'on ne trouve pas en regardant : la convention non écrite, la
  raison d'un choix, le piège qu'aucune configuration n'avoue.
- **Chaque ligne encore utile ?** Une ligne qui ne sert jamais la tâche, ou qui décrit un état
  passé, s'enlève. Sans élagage, les couches s'accumulent en **sédiment** : ajouter paraît sans
  risque, retirer paraît dangereux.
- **Les consignes sans effet** : une phrase que le modèle suivrait de toute façon ne sert à rien.
  Le test (change-t-elle le comportement par rapport au défaut ?) se tranche en lançant le
  document, pas en débattant. Supprimer la phrase entière plutôt que la raboter. Un mot trop
  faible (« sois rigoureux ») est lui aussi sans effet : il faut un mot plus fort, pas une autre
  technique.

## Propre aux skills

- **Lancé par Claude** : une description toujours chargée, écrite pour le modèle, avec un
  déclencheur par cas. D'autres skills peuvent l'appeler.
- **Lancé par l'utilisateur** (`disable-model-invocation: true`) : aucune charge de contexte, une
  description d'une ligne pour l'humain, et aucun skill ne peut l'appeler.
- Ne rendre un skill déclenchable par Claude que si Claude doit l'atteindre seul, ou si un autre
  skill doit l'appeler.
- Quand les skills lancés à la main deviennent trop nombreux pour s'en souvenir, un skill
  **routeur** (ici `/next`) les nomme et dit quand lancer chacun.
