#!/usr/bin/env bash
#
# Un assistant guide un humain, étape par étape, dans une procédure manuelle.
# Généré par le skill wizard (d'après celui de Matt Pocock, licence MIT).
#
# Tout ce qui est au-dessus du repère « ÉTAPES » est la bibliothèque : ne pas
# la modifier à la main. Écrire les étapes sous le repère.

set -euo pipefail

# ──────────────────────────────────────────────────────────────────────────
# Bibliothèque : la même dans chaque assistant.
# ──────────────────────────────────────────────────────────────────────────

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  BOLD=$(tput bold); DIM=$(tput dim); RESET=$(tput sgr0)
  BLUE=$(tput setaf 4); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); RED=$(tput setaf 1)
else
  BOLD=""; DIM=""; RESET=""; BLUE=""; GREEN=""; YELLOW=""; RED=""
fi

# Fixé en tête de la section des étapes.
TOTAL_STAGES=0

_STAGE_INDEX=0
ENV_FILE="${ENV_FILE:-.env}"
WRITTEN_ENV=()    # clés écrites dans ENV_FILE pendant ce passage
WRITTEN_SECRET=() # secrets posés pendant ce passage
SKIPPED=()        # ce qui n'a pas pu se faire (gh absent, par exemple)

# _clear efface le terminal pour ne laisser que l'étape en cours. Sans effet
# hors d'un terminal, pour que les journaux restent lisibles.
_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1; then tput clear; else printf '\033[2J\033[3J\033[H'; fi
}

# banner "Titre" affiche l'écran d'accueil : ce que fait l'assistant.
banner() {
  _clear
  printf '\n%s%s  %s%s\n' "$BOLD" "$BLUE" "$1" "$RESET"
  printf '%s  %s étapes%s\n\n' "$DIM" "$TOTAL_STAGES" "$RESET"
  printf '%s  Tu pilotes le navigateur ; l'\''assistant te dit quoi faire et récupère\n' "$DIM"
  printf '  les valeurs que tu recopies. Ctrl-C arrête à tout moment : relancé plus\n'
  printf '  tard, il garde les valeurs déjà enregistrées.%s\n' "$RESET"
  pause "Prêt à commencer ? (Entrée)"
}

# stage "Nom" efface l'écran, annonce l'étape et montre la progression.
stage() {
  _clear
  _STAGE_INDEX=$((_STAGE_INDEX + 1))
  printf '\n%s%s▸ Étape %s/%s · %s%s\n' \
    "$BOLD" "$BLUE" "$_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$RESET"
}

# say "..." affiche une consigne.
say()  { printf '  %s\n' "$1"; }
# step "..." est une action à faire dans le navigateur.
step() { printf '  %s•%s %s\n' "$BLUE" "$RESET" "$1"; }
note() { printf '  %s%s%s\n' "$DIM" "$1" "$RESET"; }
warn() { printf '  %s⚠ %s%s\n' "$YELLOW" "$1" "$RESET"; }

# open_url URL l'ouvre dans le navigateur, sur toutes les plateformes, WSL compris.
open_url() {
  local url="$1"
  printf '  %s↗ ouverture de%s %s\n' "$GREEN" "$RESET" "$url"
  { if   command -v wslview     >/dev/null 2>&1; then wslview "$url"
    elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$url"
    elif command -v xdg-open    >/dev/null 2>&1; then xdg-open "$url"
    elif command -v open        >/dev/null 2>&1; then open "$url"
    else warn "impossible d'ouvrir un navigateur ; ouvre toi-même : $url"; fi
  } >/dev/null 2>&1 || warn "impossible d'ouvrir un navigateur ; ouvre toi-même : $url"
}

# pause "message" attend que l'humain ait fait la partie manuelle.
pause() {
  printf '  %s%s%s ' "$DIM" "${1:-Entrée pour continuer}" "$RESET"
  read -r _ || true
}

# confirm "question" demande o/N ; réussit sur oui.
confirm() {
  local reply=""
  printf '  %s? %s [o/N] ' "$YELLOW" "$1"
  read -r reply || true
  [[ "$reply" =~ ^[OoYy] ]]
}

# _existing CLÉ : la valeur actuelle de CLÉ dans ENV_FILE, s'il y en a une.
_existing() {
  [[ -f "$ENV_FILE" ]] || return 1
  local line; line=$(grep -E "^${1}=" "$ENV_FILE" | tail -n1) || return 1
  printf '%s' "${line#*=}"
}

# ask CLÉ "Question" lit une valeur dans $CLÉ. En cas de relance, la valeur du
# .env est proposée par défaut (Entrée la garde). Saisie visible (non secrète).
ask() {
  local key="$1" prompt="$2" current input
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[Entrée : garder la valeur]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -r input || true
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# ask_secret CLÉ "Question" : comme ask, mais la saisie est masquée.
ask_secret() {
  local key="$1" prompt="$2" current input
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[Entrée : garder la valeur]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -rs input || true
  printf '\n'
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# write_env CLÉ VALEUR écrit CLÉ=VALEUR dans ENV_FILE (le crée au besoin,
# remplace la ligne existante). Rejouable sans effet de bord.
write_env() {
  local key="$1" value="$2" tmp
  touch "$ENV_FILE"
  tmp=$(mktemp)
  grep -vE "^${key}=" "$ENV_FILE" > "$tmp" || true
  printf '%s=%s\n' "$key" "$value" >> "$tmp"
  mv "$tmp" "$ENV_FILE"
  WRITTEN_ENV+=("$key")
  printf '  %s✓ écrit%s %s → %s\n' "$GREEN" "$RESET" "$key" "$ENV_FILE"
}

# set_secret NOM VALEUR pose un secret GitHub Actions avec gh. Si gh manque ou
# n'est pas connecté, avertit et le note pour la fin.
set_secret() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if printf '%s' "$value" | gh secret set "$name" >/dev/null 2>&1; then
      WRITTEN_SECRET+=("$name")
      printf '  %s✓ posé%s secret GitHub %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("secret GitHub $name (à poser : gh secret set $name)")
  warn "secret GitHub $name sauté : gh pas prêt, à poser plus tard"
}

# set_var NOM VALEUR pose une variable GitHub Actions (non secrète).
set_var() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if gh variable set "$name" --body "$value" >/dev/null 2>&1; then
      printf '  %s✓ posée%s variable GitHub %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("variable GitHub $name (à poser : gh variable set $name)")
  warn "variable GitHub $name sautée : gh pas prêt, à poser plus tard"
}

# finish efface l'écran et résume tout ce qui a été configuré.
finish() {
  _clear
  printf '\n%s%s  ✓ Terminé%s\n' "$BOLD" "$GREEN" "$RESET"
  (( ${#WRITTEN_ENV[@]} ))    && note "${#WRITTEN_ENV[@]} valeur(s) écrite(s) dans $ENV_FILE : ${WRITTEN_ENV[*]}"
  (( ${#WRITTEN_SECRET[@]} )) && note "${#WRITTEN_SECRET[@]} secret(s) GitHub posé(s) : ${WRITTEN_SECRET[*]}"
  if (( ${#SKIPPED[@]} )); then
    printf '\n'; warn "reste à faire à la main :"
    for s in "${SKIPPED[@]}"; do note "  - $s"; done
  fi
  printf '\n'
}

# ──────────────────────────────────────────────────────────────────────────
# ÉTAPES : section à écrire. Un stage() par étape de l'humain.
# Remplacer l'exemple ci-dessous. TOTAL_STAGES = le nombre d'étapes écrites.
# ──────────────────────────────────────────────────────────────────────────

TOTAL_STAGES=1

banner "Configuration de Stripe"

# ── Exemple d'étape : à remplacer par les vraies ─────────────────────────
stage "Stripe : clés d'API"
say "On récupère les clés de test Stripe, pour le développement local et la CI."
open_url "https://dashboard.stripe.com/test/apikeys"
step "Sur la page des clés d'API, copie la clé publiable (commence par pk_test_)."
ask STRIPE_PUBLISHABLE_KEY "Colle la clé publiable :"
step "Sur la ligne de la clé secrète, clique sur « Reveal test key », puis copie-la."
ask_secret STRIPE_SECRET_KEY "Colle la clé secrète :"
write_env STRIPE_PUBLISHABLE_KEY "$STRIPE_PUBLISHABLE_KEY"
write_env STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"
set_secret STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"   # la CI en a besoin
# ──────────────────────────────────────────────────────────────────────────

finish
