# Lancer un workflow depuis un skill

Pour `/ticket-chain` et `/code-audit`, qui livrent chacun un `workflow.js` à côté de leur
`SKILL.md`.

## Les chemins

- **Le dossier d'un skill** : son chemin réel (`realpath ~/.claude/skills/<nom>`), pas le lien
  de `~/.claude/skills/`, d'où `../` ne mène pas au dépôt des skills.
- **Le fichier d'un agent** (`bugHunterPath`, `judgePath`) : le premier qui existe parmi
  `.claude/agents/<nom>.md` du projet (il prend la place de celui des skills),
  `~/.claude/agents/<nom>.md`, puis `../agents/<nom>.md` depuis le chemin réel du skill. Le
  workflow s'en sert quand la session ne connaît pas ce type d'agent : l'agent de repli lit alors
  sa méthode dans ce fichier.

## Le lancement

Lire le `workflow.js` du skill en entier, depuis son chemin réel, puis appeler l'outil Workflow :

- `script` : le contenu du fichier, tel quel ;
- `args` : l'objet des arguments, en JSON (un objet, pas une chaîne).

Pas de `scriptPath` : l'outil refuse un fichier hors du projet ouvert, même à travers un lien
symbolique ou après l'avoir lu. Il enregistre le script et rend son chemin et un identifiant de
run : les garder.

## La reprise

- **Même session** : arrêter le run s'il tourne encore, puis l'outil Workflow avec
  `resumeFromRunId` et le chemin du script enregistré (`scriptPath`, cette fois dans le dossier
  de la session) : les agents inchangés sont rejoués depuis le cache.
- **Nouvelle session** : relancer le skill ; chaque workflow dit ce qu'il saute.
