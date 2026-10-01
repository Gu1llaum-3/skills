# Skills Claude Code

Mes skills personnels pour Claude Code.

## Skills

### À lancer toi-même

| Commande | Rôle |
|---|---|
| `/brainstorming` | Cadrer un nouveau projet jusqu'au cahier des charges (ou une synthèse à planifier pour un petit outil) |
| `/feature` | Cadrer une idée de fonctionnalité dans un projet existant |
| `/poc` | Vérifier vite qu'une idée tient debout, sur une seule question |
| `/onboard` | Préparer un projet existant pour Claude : créer ou mettre à l'épreuve `CLAUDE.md`, `ARCHITECTURE.md` |
| `/architecture` | Chercher où approfondir les modules d'un projet existant : rapport HTML, puis entretien sur la piste choisie |
| `/retro` | Après une session difficile : ce qu'il faudrait changer dans l'environnement (renvois, contrôles, conventions de relecture) |
| `/upgrade` | Auditer les versions (Node, pnpm, paquets, images Docker, Postgres) : failles, fins de vie, paquets abandonnés, mises à jour compatibles, dans `docs/audits/` |
| `/git-guardrails` | Bloquer les commandes git destructrices de Claude (push, reset --hard, clean…) par un hook |
| `/next` | Quel skill lancer maintenant : lit la conversation, ou l'état du projet |
| `/wtf` | Un message n'est pas passé : le faire reformuler, avec le contexte et les mots du projet |
| `/design` | Définir l'identité visuelle : prototype HTML et `DESIGN.md` |
| `/naming` | Trouver un nom et vérifier sa disponibilité |

### Utilisables seuls ou appelés par les autres

| Skill | Rôle |
|---|---|
| `plan` | Écrire le plan d'un ticket, d'une spec ou d'un jalon, après l'avoir confronté au code (et challengé, s'il vient d'ailleurs) |
| `implement` | Exécuter un plan (ou un ticket) vague par vague, en TDD, puis le faire relire |
| `review` | Relire un diff sur deux axes séparés : la spec (plan, ticket) et les conventions du dépôt |
| `tdd` | La boucle rouge-vert et ce qui fait un bon test |
| `debug` | Diagnostiquer un bug qui résiste : une boucle qui échoue d'abord, puis hypothèses, cause confirmée, correctif |
| `to-spec` | Transformer les décisions (ou un jalon du cahier des charges) en spec, puis en tickets |
| `to-tickets` | Découper en tickets par tranches verticales, avec leurs dépendances |
| `tickets` | Lire, publier et ranger les tickets et les jalons de la roadmap (local, GitHub, GitLab, Forgejo / Gitea, Jira) |
| `interview` | Entretien critique : le besoin d'abord, les faits cherchés, les décisions posées, les questions métier repérées |
| `domain-modeling` | Tenir le glossaire du domaine (`GLOSSARY.md`) : un mot tranché par concept |
| `to-questionnaire` | Faire remplir par le métier les questions auxquelles tu ne peux pas répondre, puis réintégrer les réponses |
| `research` | Recherche sur sources primaires, en arrière-plan, notée dans `docs/research/` |
| `adr` | Enregistrer une décision d'architecture dans `docs/adr/` |
| `wizard` | Un script qui guide pas à pas dans ce que toi seul peux faire (comptes, secrets, tableaux de bord), et écrit les valeurs dans `.env` et la CI |

## Enchaînement

```
/brainstorming ──┬── cahier des charges ──┬── simple ──► plan ──► implement ──► tdd
                 │  (verdict d'envergure) └── gros ──► to-spec (un jalon) ──► to-tickets ──► roadmap
                 ├── petit outil ──► synthèse dans la conversation ──► plan ──► implement
                 └── question de faisabilité ──► /poc

/feature ──┬── maintenant ──► plan ──► implement
           ├── plus tard ──► to-spec ──┬──► 1 ticket ─────────────┐
           │                           └──► to-tickets ──► N ──────┴──► roadmap
           └── question de faisabilité ──► /poc

/poc ──► docs/poc/<slug>.md ──► plan ──► implement ──► verdict ──► /brainstorming ou /feature

ticket de la roadmap, ou écrit ailleurs ──► /implement <ticket> ──► plan ──► implement ──► tickets

bug qui résiste ──► debug ──┬── petit correctif ──► test de non-régression, commit
                            └── plus gros ──► plan ──► implement

/upgrade ──► docs/audits/<date>-upgrade.md ──┬── sans risque ──► un commit par groupe
                                             └── chantier ──► tickets ──► /implement <ticket>

/architecture ──► rapport HTML ──► une piste choisie ──┬── maintenant ──► plan ──► implement
                                                       └── plus tard ──► to-spec

interview, research, adr, to-questionnaire et wizard sont appelés en cours de route.
implement écrit le code avec tdd, puis le fait relire par review avant son bilan.
Après une session difficile, /retro propose ce qu'il faudrait changer dans l'environnement.
Perdu en chemin ? /next dit quel skill lancer.
```

- **Simple ou gros** : le verdict est écrit dans le cahier des charges. Simple, chaque jalon
  tient en une session et se planifie directement ; gros, chaque jalon passe par une spec puis
  des tickets. Le critère de taille est celui de `to-tickets`.
- **La roadmap** est tenue par `tickets` : `ROADMAP.md` en local, milestones sur GitHub,
  GitLab, Forgejo et Gitea, versions sur Jira. Ses jalons sont ceux du cahier des charges.
- **Jalon, spec, tickets** : un jalon est une étape de livraison, vide au départ. Dans un gros
  projet, l'epic, c'est la spec du jalon (un ticket parent, une Epic sur Jira), et ses tickets
  en sont les enfants, rangés dans le jalon. Un projet simple n'a pas d'epic : le plan du jalon
  s'y rattache.

  | | Jalon | Spec (l'epic) | Ticket |
  |---|---|---|---|
  | Local | section de `ROADMAP.md` | `docs/specs/<feature>.md` | `docs/tickets/<feature>/NN-<slug>.md` |
  | GitHub | milestone | issue parente, label `spec` | sous-issue de la spec |
  | GitLab | milestone | issue, label `spec` | issue qui cite la spec |
  | Forgejo, Gitea | milestone | issue, label `spec` | issue qui cite la spec, bloquants en dépendances natives |
  | Jira | version (Fix Version) | Epic | Story rattachée à l'Epic |
- **Un ticket écrit hors de ces skills** (par une PO, un client) se reconnaît à son format :
  `plan` questionne alors le besoin, pousse l'entretien et propose un commentaire pour son
  auteur. La recherche part, pour tous les tickets, quand le code ne suffit pas à savoir comment
  faire.
- **Les questions métier** : `interview` repère celles qui ne sont pas à toi de trancher
  (règles métier, juridique, chiffres, priorités produit) et propose « À demander au métier ».
  Elles vont dans les « Questions ouvertes » du document, puis dans un questionnaire par
  destinataire (`docs/questionnaires/`). Une question bloquante empêche de valider le plan qui en
  dépend.
- Passer d'une étape à la suivante (du cadrage au plan, du plan à `implement`) se fait après ton
  accord ; les skills appelés en cours de route (`tdd`, `interview`, `research`, `review`…) n'en
  demandent pas. Ceux que tu lances toi-même (`/brainstorming`, `/feature`, `/poc`…) ne peuvent
  pas être lancés par Claude : il te donne la commande à taper.

## Où vont les fichiers d'un projet

| Fichier | Produit par |
|---|---|
| `CLAUDE.md`, `ARCHITECTURE.md` | `onboard` |
| `GLOSSARY.md` | `domain-modeling`, appelé par `interview` |
| `docs/requirements.md` (le cahier des charges) | `brainstorming` |
| `docs/poc/` | `poc` |
| `docs/design/DESIGN.md`, `docs/design/prototype.html` | `design` |
| `docs/naming.md` | `naming` |
| `docs/research/` | `research` |
| `docs/questionnaires/` | `to-questionnaire` |
| `docs/adr/` | `adr` |
| `docs/specs/`, `docs/tickets/`, `ROADMAP.md` | `to-spec`, `to-tickets`, via `tickets` (gestionnaire local) |
| `docs/conventions.md` | `retro`, lu par `review` |
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

## Mesurer les relectures par sous-agent

```bash
python3 evals/run_subagents.py --dry-run
python3 evals/run_subagents.py --runs 3
```

Rejoue les relectures (celle du cahier des charges dans `Explore` ou dans `general-purpose`, et
`review` avant et après un changement) sur un mini-projet aux défauts plantés
(`evals/fixtures/subagents/`). Un correcteur compte, pour chaque cas, les défauts trouvés, les
leurres écartés, les remarques hors liste (à relire : justes ou fausses), les remarques sourcées
et le coût.
`--dry-run` prépare les projets de test sans appeler Claude. `--set hard` prend un jeu plus dur
(`evals/fixtures/subagents-hard/`) : défauts discrets, leurres qui ont l'air de vraies erreurs,
cahier des charges de près de 400 lignes, et `/plan` complet sur un ticket piégé
(`plan-full-old` contre `plan-full-new`).

## La page des skills

```bash
python3 docs/build_skills_page.py && open docs/skills.html
```

[`docs/skills.html`](docs/skills.html) montre qui appelle qui, les parcours par situation, un jeu
« quel skill ? » tiré de la carte de `/next`, et les fichiers que les skills laissent dans un
projet. Les appels et les descriptions viennent des `SKILL.md` ; les groupes, les parcours et
les fichiers sont écrits dans `docs/skills.template.html`. À relancer après chaque changement de
skill.

Les pistes à venir sont dans [TODO.md](TODO.md).

## Crédits

Plusieurs skills adaptent en français le travail de [Matt Pocock](https://github.com/mattpocock/skills)
(licence MIT), dont l'organisation en skills qui s'appellent entre eux. Quelques idées viennent
aussi de [superpowers](https://github.com/obra/superpowers), de Jesse Vincent. La liste des skills
adaptés et leur source : [CREDITS.md](CREDITS.md).
