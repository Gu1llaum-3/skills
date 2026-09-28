# Skills Claude Code

Mes skills personnels pour Claude Code, en français : un dossier `<skill>/SKILL.md` par skill,
lié dans `~/.claude/skills/` par `install.sh`.

## Commandes

- Installer ou relier les skills : `./install.sh` (après un ajout ou un renommage)
- Banc d'essai des déclencheurs : `python3 evals/run_triggers.py [passages]`. Il lance 36 appels
  à `claude -p` : le proposer après chaque changement de description, le lancer seulement après
  accord.

## Conventions

- Un SKILL.md s'adresse à Claude, à l'infinitif ou à l'impératif ; il parle de « l'utilisateur ».
  Au-delà de ~150 lignes, déplacer le détail dans `references/`.
- Description : ce que fait le skill, puis « Utilise ce skill quand… » avec des phrases types
  entre guillemets, et les skills qui l'appellent.
- Un skill que l'utilisateur lance lui-même porte `disable-model-invocation: true` ; il propose
  les skills suivants, il ne les lance pas.
- Un skill en appelle un autre avec « appeler le Skill tool avec « nom » », et pointe ses fichiers
  par un lien relatif (`../tickets/SKILL.md`).

## Pièges

- Un `#` dans une description sans guillemets est lu comme un commentaire YAML : la description
  est coupée sans erreur.
- Une description est limitée à 1024 caractères (`plan` en fait déjà près de 900).
- Un skill que Claude peut déclencher doit être ajouté à `MINE` dans `evals/run_triggers.py`,
  sinon le banc d'essai le compte comme « autre ».
- Renommer un skill casse les liens relatifs des autres skills : les chercher avec
  `grep -r "../<ancien-nom>/"`, puis relancer `./install.sh`.

## Travail

- Ajouter ou modifier un skill, c'est aussi mettre à jour, selon le cas : les tableaux et le
  schéma du `README.md`, `CREDITS.md` (skill adapté de Matt Pocock), `evals/triggers.json` (avec
  des pièges qui ne doivent rien déclencher), `TODO.md`, la carte de `next/SKILL.md`. Vérifier les
  skills qui l'appellent.
- Un changement de comportement se termine par un scénario d'essai proposé à l'utilisateur :
  quoi lancer, dans quel projet, ce qu'il faut observer.
- Commits en français, directement sur `main`, un seul commit par changement (skill et fichiers
  liés). Exemples : « Ajout de /onboard : préparer un projet existant pour Claude »,
  « to-spec : description plus proche de l'originale ».
