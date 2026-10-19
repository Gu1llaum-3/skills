#!/usr/bin/env bash
# Installe les skills de ce dépôt dans ~/.claude/skills, et ses agents (agents/*.md) dans
# ~/.claude/agents, via des liens symboliques.
# Usage : ./install.sh                  -> tous les skills et tous les agents
#         ./install.sh naming           -> seulement ceux cités (skills ou agents)
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
AGENTS_DEST="${CLAUDE_AGENTS_DIR:-$HOME/.claude/agents}"
mkdir -p "$DEST" "$AGENTS_DEST"

# Supprime les liens vers des skills ou des agents du dépôt qui ont été renommés ou supprimés
for link in "$DEST"/* "$AGENTS_DEST"/*; do
  if [ -L "$link" ] && [ ! -e "$link" ] && [[ "$(readlink "$link")" == "$REPO"/* ]]; then
    rm "$link"
    echo "  lien cassé supprimé : $(basename "$link")"
  fi
done

if [ $# -gt 0 ]; then
  skills=()
  agents=()
  for a in "$@"; do
    if [ -f "$REPO/agents/$a.md" ]; then agents+=("$a"); else skills+=("$a"); fi
  done
else
  skills=()
  for d in "$REPO"/*/; do
    [ -f "$d/SKILL.md" ] && skills+=("$(basename "$d")")
  done
  agents=()
  for f in "$REPO"/agents/*.md; do
    [ -f "$f" ] && agents+=("$(basename "$f" .md)")
  done
fi

# Relie src dans dst ; un fichier ou dossier déjà là (pas un lien) part dans <dossier de dst>-backup
link() {
  local src="$1" dst="$2" backup_dir
  backup_dir="$(dirname "$dst")-backup"
  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -e "$dst" ]; then
    mkdir -p "$backup_dir"
    local backup
    backup="$backup_dir/$(basename "$dst").$(date +%Y%m%d%H%M%S)"
    mv "$dst" "$backup"
    echo "  ancienne version sauvegardée dans $backup"
  fi
  ln -s "$src" "$dst"
}

for a in "${agents[@]+"${agents[@]}"}"; do
  link "$REPO/agents/$a.md" "$AGENTS_DEST/$a.md"
  echo "✓ agent $a -> $AGENTS_DEST/$a.md"
done

for s in "${skills[@]+"${skills[@]}"}"; do
  [ -f "$REPO/$s/SKILL.md" ] || { echo "✗ $s : pas de SKILL.md, ignoré"; continue; }
  link "$REPO/$s" "$DEST/$s"
  echo "✓ $s -> $DEST/$s"
done
