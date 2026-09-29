---
name: wizard
description: "Générer un script bash interactif qui guide l'utilisateur, étape par étape, dans ce que lui seul peut faire (ouvrir une URL, cliquer, copier une valeur), puis écrit les valeurs dans .env et les secrets de la CI. Utilise ce skill quand il faut créer un compte ou provisionner un service tiers, configurer des identifiants ou des secrets de CI, parcourir un tableau de bord inconnu, ou mener une migration ponctuelle à la main. Pas pour ce que Claude peut faire lui-même."
---

# Wizard : guider l'utilisateur dans une procédure manuelle

Un **assistant** est un script bash qui mène l'utilisateur dans une procédure manuelle,
fastidieuse à faire comme à réexpliquer à chaque fois : il ouvre chaque URL, dit exactement quoi
cliquer et copier, récupère les valeurs, les écrit là où elles vont (`.env`, secrets GitHub),
confirme à chaque étape et dit combien il en reste. Ce que Claude peut faire lui-même, il le fait :
l'assistant sert aux clics, aux validations et aux tableaux de bord qu'on ne confierait pas à un
agent.

L'ergonomie est déjà réglée par [template.sh](template.sh) : progression, confirmations,
ouverture d'URL sur toutes les plateformes, saisie masquée des secrets, écriture rejouable dans
`.env`, `gh secret` et `gh variable`, et un résumé final. **Le travail se limite à cerner la
procédure et à écrire ses étapes.** La bibliothèque au-dessus du repère `ÉTAPES` ne se modifie
jamais.

Par défaut, un assistant sert une fois : il va dans le dossier temporaire ou `scripts/`, et
s'efface une fois le travail fait. Il ne se commite que si l'utilisateur veut garder un chemin
d'installation rejouable dans le dépôt.

## 1. Cerner la procédure

Lister chaque geste manuel et chaque valeur récupérée. Lire le dépôt avant de demander :

- **Une installation** : `.env`, `.env.example`, `.env.*`, le README, `docker-compose*`, la
  configuration du framework, et `.github/workflows/*` (chaque `secrets.*` ou `vars.*` est une
  valeur que l'assistant doit produire).
- **Une migration** : l'état actuel, l'état visé, et les actions irréversibles entre les deux.

Montrer la liste ordonnée des étapes et les valeurs de chacune, et la faire confirmer (ajouter,
retirer, réordonner). Quand Claude lance ce skill en plein travail, cette liste sert aussi de
proposition : rien ne s'écrit avant l'accord.

**Fini quand** chaque étape est nommée dans l'ordre et que, pour chaque valeur, on sait où
l'utilisateur la trouve, où elle s'écrit (`.env`, un secret GitHub, les deux, ou nulle part) et
si elle est secrète (saisie masquée) ou non.

## 2. Tracer le chemin de chaque étape

Pour chaque étape, le chemin précis : quelle URL, quoi y faire, où la valeur s'affiche, quelle
variable elle remplit (« Tableau de bord → Developers → API keys → Reveal test key → copier »).
Là où l'interface actuelle ou la commande exacte ne sont pas connues, le dire, et demander ou
lire la documentation (skill `research`) : ne jamais inventer une étape qui n'existe peut-être
pas.

**Fini quand** chaque étape se suit par un inconnu, sans deviner.

## 3. Écrire l'assistant

Copier `template.sh` à l'endroit prévu. Remplacer l'exemple par un `stage` par étape, dans
l'ordre des dépendances, avec les fonctions de la bibliothèque : `stage`, `say`, `step`, `note`,
`open_url`, `ask`, `ask_secret`, `write_env`, `set_secret`, `set_var`, `pause`, `confirm`. Fixer
`TOTAL_STAGES` au nombre d'étapes.

Tenir la barre du gabarit : ouvrir l'URL avant de demander sa valeur, `ask_secret` pour tout
secret, `write_env` pour chaque valeur à garder, `set_secret` seulement pour ce dont la CI a
besoin, et `confirm` avant toute action irréversible. Chaque `stage` efface l'écran : une étape
fait une seule chose, pour que rien d'utile ne défile hors de vue. Sur GitLab, remplacer
`set_secret` par un `step` qui dit où poser la variable dans *Settings → CI/CD → Variables*.

## 4. Vérifier et remettre

- `bash -n <script>`, puis `shellcheck` s'il est installé ; `chmod +x <script>`.
- Ne pas le lancer soi-même de bout en bout : il ouvre un navigateur et attend l'utilisateur.
  Le suivre à la lecture : chaque valeur de l'étape 1 est demandée et arrive là où prévu, et
  chaque nom de `set_secret` correspond exactement à un `secrets.*` de la CI.
- Donner la commande pour le lancer. S'il reste dans le dépôt, le commiter et le citer dans le
  README, pour que la personne suivante lance le script au lieu de demander à un agent.
