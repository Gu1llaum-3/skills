---
name: git-guardrails
description: Installer un hook Claude Code qui bloque les commandes git destructrices (push, reset --hard, clean, branch -D, checkout .) avant leur exécution, pour ce projet ou pour tous.
disable-model-invocation: true
---

# Git guardrails : bloquer les commandes git destructrices

Installe un hook `PreToolUse` qui intercepte les commandes Bash de Claude et bloque les commandes
git dangereuses avant qu'elles partent. Claude reçoit alors un message qui lui dit de demander à
l'utilisateur de lancer la commande lui-même.

Bloqué par défaut :

- `git push`, sous toutes ses formes, `--force` compris ;
- `git reset --hard` ;
- `git clean -f` et `git clean -fd` ;
- `git branch -D` ;
- `git checkout .`, `git checkout -- .` et `git restore .`.

Le hook est une vérification par motif : il bloque aussi une commande qui ne fait que contenir
le motif (un message de commit qui cite « git push »). C'est le prix d'un script simple.

## 1. Choisir la portée

Demander : **ce projet seulement** (`.claude/settings.json`, partagé avec le dépôt) ou **tous les
projets** (`~/.claude/settings.json`) ?

## 2. Copier le script

Copier [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh) :

- **ce projet** : `.claude/hooks/block-dangerous-git.sh` ;
- **tous les projets** : `~/.claude/hooks/block-dangerous-git.sh`.

Le rendre exécutable (`chmod +x`). Il a besoin de `jq` : le vérifier (`command -v jq`), et
sinon proposer de l'installer.

## 3. Brancher le hook

Dans le fichier de réglages choisi, ajouter le hook au tableau `hooks.PreToolUse`, **fusionné**
avec ce qui existe : ne rien écraser d'autre. Lire le fichier avant, montrer le diff après.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

Pour tous les projets, la commande devient `~/.claude/hooks/block-dangerous-git.sh`.

## 4. Ajuster la liste

Demander s'il faut ajouter ou retirer des motifs : par exemple autoriser `git push` sur une
branche de travail, ou bloquer `git rebase`. Modifier le script copié en conséquence.

## 5. Vérifier

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <chemin du script>; echo $?
echo '{"tool_input":{"command":"git status"}}' | <chemin du script>; echo $?
```

La première doit afficher un message `BLOQUÉ` et rendre le code 2 ; la seconde, rendre 0. Dire
à l'utilisateur que le hook vaut pour les prochaines commandes de la session, et qu'il se
retire en enlevant l'entrée de `hooks.PreToolUse`.
