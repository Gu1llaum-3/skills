#!/bin/bash
# Hook PreToolUse de Claude Code : bloque les commandes git destructrices.
# D'après git-guardrails-claude-code de Matt Pocock (licence MIT).

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

DANGEROUS_PATTERNS=(
  "git push"
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git checkout -- \."
  "git restore \."
  "push --force"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOQUÉ : '$COMMAND' correspond au motif interdit '$pattern'. L'utilisateur t'a retiré ce droit : demande-lui de lancer la commande lui-même." >&2
    exit 2
  fi
done

exit 0
