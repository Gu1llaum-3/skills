# Skills Claude Code

Mes skills personnels pour Claude Code, en français : un dossier `<skill>/SKILL.md` par skill,
lié dans `~/.claude/skills/` par `install.sh`.

## Commandes

- Installer ou relier les skills : `./install.sh` (après un ajout ou un renommage)
- Banc d'essai des déclencheurs : `python3 evals/run_triggers.py [passages]`. Il lance un appel à
  `claude -p` par phrase : le proposer après chaque changement de description, le lancer
  seulement après accord.
- Page des skills : `python3 docs/build_skills_page.py` régénère `docs/skills.html` depuis les
  `SKILL.md` et le gabarit `docs/skills.template.html` ; tests :
  `python3 -m unittest docs/test_build_skills_page.py`.

## Conventions

- Écrire ou modifier un skill : suivre `onboard/references/writing-for-agents.md` (renvois,
  hiérarchie, critères de fin, mots directeurs, élagage).
- Les noms de fichiers et de dossiers sont en anglais, leur contenu en français : ceux des skills
  (`references/smells.md`) comme ceux qu'un skill écrit dans un projet (`docs/requirements.md`,
  `docs/naming.md`). Seuls les noms tirés du sujet (`docs/plans/<slug>.md`, les branches)
  suivent la langue de la conversation. Un fichier de projet renommé garde une lecture de son
  ancien nom, avec la proposition d'un `git mv` (comme `CONTEXT.md` pour `GLOSSARY.md`).
- Un SKILL.md s'adresse à Claude, à l'infinitif ou à l'impératif ; il parle de « l'utilisateur ».
  Son corps reste sous 500 lignes (limite d'Anthropic) ; ce qui ne sert que dans certains cas va
  dans `references/`, pointé depuis le skill. La description, chargée à chaque tour, reste la plus
  courte possible.
- Description d'un skill que Claude peut déclencher, entre guillemets doubles : ce que fait le
  skill, puis « Utilise ce skill quand… » avec une phrase type par cas distinct. Pas de liste des
  skills qui l'appellent : ils l'appellent par son nom. Celle d'un skill que l'utilisateur lance
  lui-même n'est lue que par lui : une phrase qui dit ce qu'il fait.
- Pas de tiret long (—) dans la prose des skills et de la doc : réécrire la phrase avec une
  virgule, un deux-points, des parenthèses ou un point, pas un remplacement aveugle du caractère.
- Un skill que l'utilisateur lance lui-même porte `disable-model-invocation: true` : Claude ne
  peut pas le lancer, il le propose avec sa commande.
- Passer d'une étape du parcours à la suivante (cadrage → `plan` → `implement`, ou `to-spec`) se
  fait après accord explicite de l'utilisateur. Les skills appelés en cours de route (`tdd`,
  `interview`, `research`, `review`, `tickets`…) n'en demandent pas.
- Un skill en appelle un autre avec « appeler le Skill tool avec « nom » », et pointe ses fichiers
  par un lien relatif (`../tickets/SKILL.md`). Un appel par skill : deux skills, c'est « appeler
  deux fois le Skill tool ». Un skill que l'utilisateur lance lui-même ne s'appelle jamais ainsi :
  écrire « proposer à l'utilisateur de lancer `/nom` ».

## Pièges

- Un `#` dans une description sans guillemets est lu comme un commentaire YAML : la description
  est coupée sans erreur.
- Une description est limitée à 1024 caractères (`plan` en fait déjà près de 900).
- Un skill que Claude peut déclencher doit être ajouté à `MINE` dans `evals/run_triggers.py`,
  sinon le banc d'essai le compte comme « autre ».
- Renommer un skill ou l'un de ses fichiers casse ce qui pointe vers lui : les liens relatifs
  des autres skills (`../onboard/references/…`) et des références voisines, `CLAUDE.md`,
  `CREDITS.md`, `README.md` et `docs/skills.template.html`. Les chercher avec
  `git grep -n "<ancien-nom>" -- ':!docs/plans'` (les plans racontent le passé), puis relancer
  `./install.sh` pour un skill.

## Travail

- Ajouter ou modifier un skill, c'est aussi mettre à jour, selon le cas : les tableaux et le
  schéma du `README.md`, `CREDITS.md` (skill adapté de Matt Pocock, ou idées reprises d'ailleurs),
  `evals/triggers.json` (avec des pièges qui ne doivent rien déclencher), `TODO.md`, la carte de
  `next/SKILL.md`, et `docs/skills.template.html` (son groupe sur la carte, ce qu'on enchaîne
  après lui, les parcours, les fichiers qu'il écrit ou relit, les règles du jeu), puis relancer
  `python3 docs/build_skills_page.py` : les appels et les descriptions s'y mettent à jour seuls.
  Tant qu'un skill n'a pas de groupe dans `COLUMNS`, `docs/test_build_skills_page.py` échoue, et
  la page le range dans « Autres ».
- Tout changement se vérifie contre les skills rattachés, avant le plan puis avant le commit : ceux
  qui l'appellent, ceux qu'il appelle, et ceux qui renvoient à ses étapes, ses fichiers ou ses
  formats (`grep -rn "<skill>" --include='*.md' .`). Chercher ce qui casse (un numéro d'étape
  décalé, un fichier ou une section renommés, un renvoi vers un skill qui ne le prévoit pas) et ce
  qui se contredit (deux skills qui tranchent la même chose, un rôle pris à un autre skill). Dire
  ce qui a été vérifié, pas seulement que « c'est cohérent ».
- Un changement de comportement se termine par un scénario d'essai proposé à l'utilisateur :
  quoi lancer, dans quel projet, ce qu'il faut observer.
- Commits en français, directement sur `main`, un seul commit par changement (skill et fichiers
  liés). Exemples : « Ajout de /onboard : préparer un projet existant pour Claude »,
  « to-spec : description plus proche de l'originale ».
