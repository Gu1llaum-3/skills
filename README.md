# Skills Claude Code

Mes skills personnels pour Claude Code.

| Skill | Rôle |
|---|---|
| `brainstorming` | Cadrer un projet et produire un cahier des charges |
| `design` | Définir la direction visuelle, prototype HTML et DESIGN.md |
| `implement` | Exécuter un plan validé vague par vague, en TDD |
| `tdd` | Écrire du code en TDD avec des tests qui valent la peine (appelé par `implement`) |
| `naming` | Trouver un nom de projet et vérifier sa disponibilité |

## Installation

```bash
git clone git@github.com:Gu1llaum-3/skills.git ~/git/skills
~/git/skills/install.sh            # tous les skills
~/git/skills/install.sh naming    # ou seulement certains
```

Chaque skill est lié par symlink dans `~/.claude/skills/` : une modification
dans le dépôt est immédiatement prise en compte par Claude Code.

## Mise à jour

```bash
cd ~/git/skills && git pull
```

Ajouter un nouveau skill : créer `mon-skill/SKILL.md` dans le dépôt, puis relancer `./install.sh`.

## Crédits

`tdd` est adapté du skill `tdd` de [Matt Pocock](https://github.com/mattpocock/skills) (MIT), voir `tdd/CREDITS.md`.
