#!/usr/bin/env bash
# Installe les skills de ce dépôt dans ~/.claude/skills via des liens symboliques.
# Usage : ./install.sh            -> tous les skills
#         ./install.sh naming     -> seulement ceux cités
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"

# Supprime les liens vers des skills du dépôt qui ont été renommés ou supprimés
for link in "$DEST"/*; do
  if [ -L "$link" ] && [ ! -e "$link" ] && [[ "$(readlink "$link")" == "$REPO"/* ]]; then
    rm "$link"
    echo "  lien cassé supprimé : $(basename "$link")"
  fi
done

if [ $# -gt 0 ]; then
  skills=("$@")
else
  skills=()
  for d in "$REPO"/*/; do
    [ -f "$d/SKILL.md" ] && skills+=("$(basename "$d")")
  done
fi

for s in "${skills[@]}"; do
  src="$REPO/$s"
  dst="$DEST/$s"
  [ -f "$src/SKILL.md" ] || { echo "✗ $s : pas de SKILL.md, ignoré"; continue; }
  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -e "$dst" ]; then
    mkdir -p "$HOME/.claude/skills-backup"
    backup="$HOME/.claude/skills-backup/$s.$(date +%Y%m%d%H%M%S)"
    mv "$dst" "$backup"
    echo "  ancien dossier sauvegardé dans $backup"
  fi
  ln -s "$src" "$dst"
  echo "✓ $s -> $dst"
done
