# Skills Claude Code

Mes skills personnels pour Claude Code.

## Skills

### À lancer toi-même

| Commande | Rôle |
|---|---|
| `/brainstorming` | Cadrer un nouveau projet jusqu'au cahier des charges |
| `/feature` | Cadrer une idée de fonctionnalité dans un projet existant |
| `/poc` | Vérifier vite qu'une idée tient debout, sur une seule question |
| `/onboard` | Préparer un projet existant pour Claude : créer ou mettre à l'épreuve `CLAUDE.md`, `ARCHITECTURE.md` |
| `/wtf` | Un message n'est pas passé : le faire reformuler, avec le contexte et les mots du projet |
| `/design` | Définir l'identité visuelle : prototype HTML et `DESIGN.md` |
| `/naming` | Trouver un nom et vérifier sa disponibilité |

### Utilisables seuls ou appelés par les autres

| Skill | Rôle |
|---|---|
| `plan` | Écrire le plan d'un ticket, d'une spec ou d'un jalon, après l'avoir confronté au code (et challengé, s'il vient d'ailleurs) |
| `implement` | Exécuter un plan (ou un ticket) vague par vague, en TDD |
| `tdd` | La boucle rouge-vert et ce qui fait un bon test |
| `to-spec` | Transformer les décisions (ou un jalon du cahier des charges) en spec, puis en tickets |
| `to-tickets` | Découper en tickets par tranches verticales, avec leurs dépendances |
| `tickets` | Lire, publier et ranger les tickets et les jalons de la roadmap (local, GitHub, GitLab, Jira) |
| `interview` | Entretien critique : le besoin d'abord, les faits cherchés, les décisions posées, les questions métier repérées |
| `domain-modeling` | Tenir le glossaire du domaine (`CONTEXT.md`) : un mot tranché par concept |
| `to-questionnaire` | Faire remplir par le métier les questions auxquelles tu ne peux pas répondre, puis réintégrer les réponses |
| `research` | Recherche sur sources primaires, en arrière-plan, notée dans `docs/research/` |
| `adr` | Enregistrer une décision d'architecture dans `docs/adr/` |

## Enchaînement

```
/brainstorming ──► cahier des charges ──┬── simple ──► plan ──► implement ──► tdd
                   (verdict d'envergure) └── gros ──► to-spec (un jalon) ──► to-tickets ──► roadmap

/feature ──┬── maintenant ──► plan ──► implement
           └── plus tard ──► to-spec ──┬──► 1 ticket ─────────────┐
                                       └──► to-tickets ──► N ──────┴──► roadmap

/poc ──► docs/poc/<slug>.md ──► plan ──► implement ──► verdict ──► /brainstorming ou /feature

ticket de la roadmap, ou écrit ailleurs ──► /implement <ticket> ──► plan ──► implement ──► tickets

interview, research, adr et to-questionnaire sont appelés en cours de route.
```

- **Simple ou gros** : le verdict est écrit dans le cahier des charges. Simple, chaque jalon
  tient en une session et se planifie directement ; gros, chaque jalon passe par une spec puis
  des tickets. Le critère de taille est celui de `to-tickets`.
- **La roadmap** est tenue par `tickets` : `ROADMAP.md` en local, milestones sur GitHub et
  GitLab, versions sur Jira. Ses jalons sont ceux du cahier des charges.
- **Un ticket écrit hors de ces skills** (par une PO, un client) se reconnaît à son format :
  `plan` questionne alors le besoin, pousse l'entretien et propose un commentaire pour son
  auteur. La recherche part, pour tous les tickets, quand le code ne suffit pas à savoir comment
  faire.
- **Les questions métier** : `interview` repère celles qui ne sont pas à toi de trancher
  (règles métier, juridique, chiffres, priorités produit) et propose « À demander au métier ».
  Elles vont dans les « Questions ouvertes » du document, puis dans un questionnaire par
  destinataire (`docs/questionnaires/`). Une question bloquante empêche de valider le plan qui en
  dépend.
- Un skill que tu lances (`/brainstorming`, `/feature`, `/poc`) propose les autres, il ne les
  lance pas.

## Où vont les fichiers d'un projet

| Fichier | Produit par |
|---|---|
| `CLAUDE.md`, `ARCHITECTURE.md` | `onboard` |
| `CONTEXT.md` | `domain-modeling`, appelé par `interview` |
| `docs/cahier-des-charges.md` | `brainstorming` |
| `docs/poc/` | `poc` |
| `docs/design/DESIGN.md`, `docs/design/prototype.html` | `design` |
| `docs/nommage.md` | `naming` |
| `docs/research/` | `research` |
| `docs/questionnaires/` | `to-questionnaire` |
| `docs/adr/` | `adr` |
| `docs/specs/`, `docs/tickets/`, `ROADMAP.md` | `to-spec`, `to-tickets`, via `tickets` (gestionnaire local) |
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
`domain-modeling`), `domain-modeling`, `research`, `to-spec`, `to-tickets`, `to-questionnaire`
et `wtf` (d'après `wait-what`). L'organisation en skills qui s'appellent entre eux vient aussi de son
dépôt. Voir [CREDITS.md](CREDITS.md).
