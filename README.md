# Skills Claude Code

Mes skills personnels pour Claude Code.

| Skill | Rôle |
|---|---|
| `brainstorming` | Cadrer un projet et produire un cahier des charges |
| `feature` | Cadrer une idée de fonctionnalité dans un projet existant, puis l'implémenter ou la mettre de côté |
| `design` | Définir la direction visuelle, prototype HTML et DESIGN.md |
| `implement` | Exécuter un plan validé vague par vague, en TDD |
| `to-spec` | Transformer les décisions en spec, puis en un ou plusieurs tickets |
| `to-tickets` | Découper une spec en tickets par tranches verticales, avec leurs dépendances |
| `tickets` | Lire et publier des tickets (local, GitHub, GitLab, Jira, autre) ; configure le gestionnaire du projet |
| `tdd` | Écrire du code en TDD avec des tests qui valent la peine (appelé par `implement`) |
| `naming` | Trouver un nom de projet et vérifier sa disponibilité |

## Enchaînement

```
brainstorming ──► cahier des charges ──► to-tickets
feature ──┬──► plan ──► implement ──► tdd
          ├──► to-spec ──┬──► 1 ticket
          │              └──► spec ──► to-tickets ──► N tickets
          └──► ROADMAP.md
ticket ──► implement
```

Le gestionnaire de tickets se règle par projet, dans une section `## Tickets` du `CLAUDE.md`,
proposée automatiquement la première fois.

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
