---
name: architecture
description: Chercher dans un projet existant où approfondir des modules (là où le code change le plus), présenter les pistes dans un rapport HTML avec des schémas avant et après, puis mener l'entretien sur celle que l'utilisateur choisit.
argument-hint: "[module, dossier ou douleur à regarder]"
disable-model-invocation: true
---

# Architecture : où approfondir le code

Repérer les frictions d'architecture et proposer des **approfondissements** : des
refactorisations qui transforment des modules superficiels en modules profonds. Le but : un code
plus facile à tester, et plus facile à parcourir pour un agent.

Tout le rapport et l'entretien parlent avec le vocabulaire de
[references/vocabulary.md](references/vocabulary.md) (**module**, **interface**, **profondeur**,
**jointure**, **adaptateur**, **levier**, **localité**), exactement, sans glisser vers
« composant », « service », « API » ou « frontière ». Les notions du domaine prennent les termes
de `GLOSSARY.md` (ou `CONTEXT.md`, son ancien nom) s'il existe. Les ADR de `docs/adr/` sont des
décisions à ne pas rediscuter sans raison.

C'est un repérage, pas un sauvetage : sur un vieux code, il trouve de vraies pistes, mais ne
démêle rien tout seul. Pour une fonctionnalité, c'est `/feature` ; pour un bug, `debug`.

## 1. Choisir où regarder

Approfondir un module paie quand on le modifie ensuite : regarder d'abord là où le code change.

- **L'utilisateur a nommé une direction** (un module, un dossier, une douleur) : la prendre,
  sans rien déduire d'autre.
- **Sinon** : lire une bonne longueur d'historique (`git log --name-only`, une centaine de
  commits) pour trouver les fichiers et les zones qui reviennent. Si les changements sont
  dispersés, élargir.

Lire ensuite `GLOSSARY.md` et les ADR de la zone.

## 2. Explorer

Confier la visite à un sous-agent, avec la zone choisie et le vocabulaire. Pas d'heuristique
rigide : il note où il bute.

- Où comprendre une seule notion oblige-t-il à sauter entre beaucoup de petits modules ?
- Où un module est-il **superficiel**, avec une interface presque aussi complexe que son
  implémentation ?
- Où des fonctions pures ont-elles été extraites pour les tests, alors que les vrais bugs se
  cachent dans la façon de les appeler (pas de **localité**) ?
- Où des modules très couplés débordent-ils de leur jointure ?
- Qu'est-ce qui n'est pas testé, ou difficile à tester par son interface actuelle ?

Sur tout module qu'on soupçonne superficiel, faire le **test de suppression** : le supprimer
concentrerait-il la complexité, ou la déplacerait-il seulement ? « Elle se concentre » est le
signal cherché.

## 3. Présenter les pistes dans un rapport HTML

Écrire un fichier HTML autonome dans le dossier temporaire (`$TMPDIR`, sinon `/tmp`), jamais dans
le dépôt : `<tmp>/architecture-<date-heure>.html`. L'ouvrir (`open` sur macOS, `xdg-open` sur
Linux) et donner son chemin. Gabarit, schémas et ton :
[references/html-report.md](references/html-report.md).

Une carte par piste :

- **Fichiers** concernés ;
- **Problème** : pourquoi l'architecture actuelle frotte, en une phrase ;
- **Solution** : ce qui changerait, en une phrase ;
- **Gains**, en termes de localité et de levier, et ce que deviennent les tests ;
- **Schéma avant / après**, côte à côte ;
- **Force** : `Solide`, `À creuser` ou `Spéculative` ;
- la **catégorie de dépendance** (voir [references/deepening.md](references/deepening.md)).

Finir par **la piste à attaquer d'abord**, et pourquoi.

**Une piste qui contredit un ADR** ne se montre que si la friction justifie de le rouvrir, avec
un encadré (« contredit ADR-0007, mais à rouvrir parce que… »). Pas la liste de tout ce qu'un ADR
interdit.

Ne pas proposer d'interface à ce stade. Une fois le fichier écrit, demander : « Laquelle veux-tu
explorer ? »

## 4. L'entretien sur la piste choisie

Appeler le Skill tool avec « interview » pour parcourir les décisions : contraintes,
dépendances, forme du module approfondi, ce qui passe derrière la jointure, quels tests
survivent.

En chemin, dès qu'une décision tombe :

- **un module approfondi nommé d'après une notion absente du glossaire**, ou **un mot flou
  précisé** : appeler le Skill tool avec « domain-modeling » pour l'écrire ;
- **une piste rejetée pour une raison qui compte** : proposer un ADR (« Je le note en ADR, pour
  qu'une prochaine revue d'architecture ne le repropose pas ? »), puis, sur accord, appeler le
  Skill tool avec « adr ». Seulement si la raison servira à la prochaine exploration ; pas pour
  « pas le moment » ni pour l'évident ;
- **l'envie de comparer plusieurs interfaces** : suivre
  [references/design-it-twice.md](references/design-it-twice.md), des sous-agents en parallèle
  qui conçoivent chacun une interface radicalement différente.

## 5. Proposer la suite

Quand la piste est tranchée, résumer les décisions, puis proposer, sans rien lancer avant
l'accord :

- **maintenant**, si le travail tient en une session (critère « Taille » de
  [`to-tickets`](../to-tickets/SKILL.md)) : appeler le Skill tool avec « plan », depuis cette
  conversation ;
- **plus tard, ou trop gros** : appeler le Skill tool avec « to-spec », qui en fera un ticket, ou
  une spec et ses tickets. Un changement mécanique très large y passe en *expand–contract*.
