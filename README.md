# Skills Claude Code

Mes skills personnels pour Claude Code.

## Skills

### À lancer toi-même

| Commande | Rôle |
|---|---|
| `/brainstorming` | Cadrer un nouveau projet jusqu'au cahier des charges |
| `/feature` | Cadrer une idée de fonctionnalité dans un projet existant |
| `/design` | Définir l'identité visuelle : prototype HTML et `DESIGN.md` |
| `/naming` | Trouver un nom et vérifier sa disponibilité |

### Utilisables seuls ou appelés par les autres

| Skill | Rôle |
|---|---|
| `plan` | Écrire le plan d'un ticket, d'une spec ou d'un jalon, après l'avoir confronté au code |
| `implement` | Exécuter un plan (ou un ticket) vague par vague, en TDD |
| `tdd` | La boucle rouge-vert et ce qui fait un bon test |
| `to-spec` | Transformer les décisions en spec, puis en un ou plusieurs tickets |
| `to-tickets` | Découper en tickets par tranches verticales, avec leurs dépendances |
| `tickets` | Lire et publier des tickets (local, GitHub, GitLab, Jira, autre) |
| `interview` | Entretien critique : le besoin d'abord, les faits cherchés, les décisions posées |
| `research` | Recherche sur sources primaires, en arrière-plan, notée dans `docs/research/` |
| `adr` | Enregistrer une décision d'architecture dans `docs/adr/` |

## Enchaînement

```
/brainstorming ──► docs/cahier-des-charges.md ──┬──► plan ──► implement ──► tdd
                                                └──► to-tickets
/feature ──┬──► plan ──► implement
           ├──► to-spec ──┬──► 1 ticket
           │              └──► spec ──► to-tickets ──► N tickets
           └──► ROADMAP.md
ticket ──► plan ──► implement

interview, research et adr sont appelés en cours de route.
```

## Où vont les fichiers d'un projet

| Fichier | Produit par |
|---|---|
| `docs/cahier-des-charges.md` | `brainstorming` |
| `docs/design/DESIGN.md`, `docs/design/prototype.html` | `design` |
| `docs/nommage.md` | `naming` |
| `docs/research/` | `research` |
| `docs/adr/` | `adr` |
| `docs/specs/`, `docs/tickets/` | `to-spec`, `to-tickets` (gestionnaire local) |
| `docs/plans/` | `plan`, exécutés par `implement` |

Le gestionnaire de tickets se règle par projet, dans une section « Tickets » du `CLAUDE.md`,
proposée automatiquement la première fois.

## Installation

```bash
git clone git@github.com:Gu1llaum-3/skills.git ~/git/skills
~/git/skills/install.sh            # tous les skills
~/git/skills/install.sh naming     # ou seulement certains
```

Chaque skill est lié par symlink dans `~/.claude/skills/` : une modification
dans le dépôt est immédiatement prise en compte par Claude Code.

## Mise à jour

```bash
cd ~/git/skills && git pull && ./install.sh
```

Le `git pull` suffit pour les skills déjà installés, puisque les liens pointent vers le dépôt.
`./install.sh` n'est utile que si des skills ont été ajoutés ou renommés : il crée les nouveaux
liens et supprime ceux devenus cassés. Le relancer à chaque fois ne coûte rien.

Ajouter un nouveau skill : créer `mon-skill/SKILL.md` dans le dépôt, puis relancer `./install.sh`.

## Tester les déclencheurs

```bash
python3 evals/run_triggers.py
```

Envoie les phrases de `evals/triggers.json` à `claude -p`, avec les skills réellement installés,
et vérifie quel skill part en premier, y compris sur des pièges qui ne doivent rien déclencher.
À relancer après chaque changement de description. Pour une mesure plus fiable, passer le
nombre de passages par phrase en argument (`python3 evals/run_triggers.py 3`).

Les pistes à venir sont dans [TODO.md](TODO.md).

## Crédits

Plusieurs skills adaptent en français le travail de [Matt Pocock](https://github.com/mattpocock/skills)
(licence MIT) : `tdd`, `interview` (d'après `grilling`), `adr` (d'après le format d'ADR de
`domain-modeling`), `research`, `to-spec` et `to-tickets`. L'organisation en skills qui
s'appellent entre eux vient aussi de son dépôt. Voir [CREDITS.md](CREDITS.md).
