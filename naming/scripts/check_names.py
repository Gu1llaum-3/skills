#!/usr/bin/env python3
"""Vérifie la disponibilité de noms : domaines, comptes GitHub, paquets npm.

Bibliothèque standard uniquement, aucune clé d'API.

Principe : on ne répond « libre » que sur une preuve positive. Tout le reste
(erreur réseau, limite de débit, TLD non couvert par RDAP sans whois installé,
réponse whois non reconnue) donne « inconnu ».

Stratégie pour un domaine :
  1. DNS : si le domaine résout (A/AAAA), il est pris. L'absence de résolution
     ne prouve rien (domaine réservé mais non configuré).
  2. RDAP : on consulte l'annuaire IANA (data.iana.org/rdap/dns.json). Si le TLD
     y figure, on interroge directement le serveur RDAP du registre :
     200 → pris, 404 → libre. Si le TLD n'y figure pas, un 404 via rdap.org
     ne signifie rien (piège classique avec .io, .co, .de…) : on ne s'y fie pas.
  3. whois (si la commande est installée) en repli, avec motifs « non trouvé »
     et « trouvé » connus.

Usage :
  check_names.py nom1 nom2 --tlds fr,com,app --github --npm
  check_names.py nom1 --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = "naming-skill/1.0 (verification de disponibilite)"
TIMEOUT = 10
IANA_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
CACHE_FILE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "naming" / "rdap-dns.json"
CACHE_MAX_AGE = 7 * 24 * 3600

LIBRE, PRIS, INCONNU = "libre", "pris", "inconnu"

WHOIS_NOT_FOUND = [
    r"no match for",
    r"^not found",
    r"no data found",
    r"no entries found",
    r"status:\s*(free|available)",
    r"domain not found",
    r"no object found",
    r"the queried object does not exist",
    r"object does not exist",
    r"is available for registration",
    r"no information available",
    r"%% not found",
]
# Signaux forts d'enregistrement. « domain: » seul est un signal faible :
# certains registres (EURid…) l'affichent aussi pour un domaine libre.
WHOIS_FOUND = [
    r"^\s*domain name:\s*\S+",
    r"^\s*registrar:\s*\S+",
    r"^\s*creation date:",
    r"^\s*created:",
    r"^\s*registered on:",
]
WHOIS_FOUND_WEAK = [r"^\s*domain:\s*\S+"]
WHOIS_RATE_LIMIT = [r"limit exceeded", r"too many", r"try again later", r"quota"]


def http_get(url: str) -> tuple[int | None, bytes]:
    """GET simple. Retourne (code HTTP, corps) ou (None, b"") en cas d'erreur réseau."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionError):
        return None, b""


# --- RDAP -------------------------------------------------------------------

def load_rdap_bootstrap() -> dict[str, str] | None:
    """Charge l'annuaire IANA TLD → serveur RDAP, avec cache local de 7 jours."""
    data = None
    if CACHE_FILE.exists() and time.time() - CACHE_FILE.stat().st_mtime < CACHE_MAX_AGE:
        try:
            data = json.loads(CACHE_FILE.read_text())
        except (OSError, json.JSONDecodeError):
            data = None
    if data is None:
        code, body = http_get(IANA_BOOTSTRAP)
        if code != 200:
            return None
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return None
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            CACHE_FILE.write_text(json.dumps(data))
        except OSError:
            pass
    mapping: dict[str, str] = {}
    for tlds, urls in data.get("services", []):
        https = [u for u in urls if u.startswith("https://")] or urls
        if not https:
            continue
        base = https[0] if https[0].endswith("/") else https[0] + "/"
        for tld in tlds:
            mapping[tld.lower()] = base
    return mapping


def check_rdap(domain: str, bootstrap: dict[str, str] | None) -> tuple[str, str] | None:
    """Retourne (statut, source) ou None si RDAP ne peut pas trancher."""
    if bootstrap is None:
        return None
    tld = domain.rsplit(".", 1)[-1].lower()
    base = bootstrap.get(tld)
    if not base:
        return None  # TLD non couvert : un 404 ne voudrait rien dire
    code, _ = http_get(f"{base}domain/{domain}")
    if code == 200:
        return PRIS, "rdap"
    if code == 404:
        return LIBRE, "rdap"
    return None  # 429, 5xx, réseau : on laisse le repli décider


# --- whois ------------------------------------------------------------------

def parse_whois(text: str) -> str:
    low = text.lower()
    if any(re.search(p, low, re.M) for p in WHOIS_RATE_LIMIT) and not any(
        re.search(p, low, re.M) for p in WHOIS_FOUND
    ):
        return INCONNU
    not_found = any(re.search(p, low, re.M) for p in WHOIS_NOT_FOUND)
    found = any(re.search(p, low, re.M) for p in WHOIS_FOUND)
    if not_found and found:
        return INCONNU  # signaux contradictoires : on ne tranche pas
    if not_found:
        return LIBRE
    if found or any(re.search(p, low, re.M) for p in WHOIS_FOUND_WEAK):
        return PRIS
    return INCONNU


def check_whois(domain: str) -> tuple[str, str] | None:
    if not shutil.which("whois"):
        return None
    try:
        out = subprocess.run(
            ["whois", domain], capture_output=True, text=True, timeout=20, errors="replace"
        ).stdout
    except (subprocess.TimeoutExpired, OSError):
        return INCONNU, "whois (échec)"
    return parse_whois(out), "whois"


# --- DNS --------------------------------------------------------------------

def resolves(domain: str) -> bool:
    try:
        socket.getaddrinfo(domain, None)
        return True
    except (socket.gaierror, UnicodeError, OSError):
        return False


def check_domain(domain: str, bootstrap: dict[str, str] | None) -> dict:
    if resolves(domain):
        return {"cible": domain, "statut": PRIS, "source": "dns"}
    result = check_rdap(domain, bootstrap)
    if result is None:
        result = check_whois(domain)
    if result is None:
        hint = "installer whois" if not shutil.which("whois") else "vérifier chez un registrar"
        return {"cible": domain, "statut": INCONNU, "source": f"aucune source fiable ({hint})"}
    return {"cible": domain, "statut": result[0], "source": result[1]}


# --- GitHub / npm -----------------------------------------------------------

def check_github(name: str) -> dict:
    code, _ = http_get(f"https://api.github.com/users/{name}")
    target = f"github.com/{name}"
    if code == 200:
        return {"cible": target, "statut": PRIS, "source": "api github"}
    if code == 404:
        return {"cible": target, "statut": LIBRE, "source": "api github"}
    reason = "limite de débit" if code in (403, 429) else "erreur"
    return {"cible": target, "statut": INCONNU, "source": f"api github ({reason})"}


def check_npm(name: str) -> dict:
    code, _ = http_get(f"https://registry.npmjs.org/{name.lower()}")
    target = f"npm:{name.lower()}"
    if code == 200:
        return {"cible": target, "statut": PRIS, "source": "registre npm"}
    if code == 404:
        return {"cible": target, "statut": LIBRE, "source": "registre npm"}
    return {"cible": target, "statut": INCONNU, "source": "registre npm (erreur)"}


# --- Main -------------------------------------------------------------------

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def normalize(name: str) -> str:
    return name.strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser(description="Vérifie la disponibilité de noms.")
    ap.add_argument("names", nargs="+", help="noms à vérifier (sans extension)")
    ap.add_argument("--tlds", default="fr,com", help="extensions séparées par des virgules (défaut : fr,com)")
    ap.add_argument("--github", action="store_true", help="vérifier les comptes/organisations GitHub")
    ap.add_argument("--npm", action="store_true", help="vérifier les paquets npm")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    ap.add_argument("--delay", type=float, default=0.5, help="pause entre requêtes en secondes (défaut : 0.5)")
    args = ap.parse_args()

    tlds = [t.strip().lstrip(".").lower() for t in args.tlds.split(",") if t.strip()]
    bootstrap = load_rdap_bootstrap()
    warnings = []
    if bootstrap is None:
        warnings.append("Annuaire RDAP IANA inaccessible : vérification des domaines via DNS et whois uniquement.")
    if not shutil.which("whois"):
        warnings.append("Commande whois absente : les TLD non couverts par RDAP resteront « inconnu ».")

    results: dict[str, list[dict]] = {}
    for raw in args.names:
        name = normalize(raw)
        rows: list[dict] = []
        if not NAME_RE.match(name):
            rows.append({"cible": raw, "statut": INCONNU, "source": "nom invalide pour un domaine (accents, espaces ?)"})
            results[raw] = rows
            continue
        for tld in tlds:
            rows.append(check_domain(f"{name}.{tld}", bootstrap))
            time.sleep(args.delay)
        if args.github:
            rows.append(check_github(name))
            time.sleep(args.delay)
        if args.npm:
            rows.append(check_npm(name))
            time.sleep(args.delay)
        results[name] = rows

    if args.json:
        print(json.dumps({"avertissements": warnings, "resultats": results}, ensure_ascii=False, indent=2))
        return 0

    for w in warnings:
        print(f"⚠️  {w}", file=sys.stderr)
    icon = {LIBRE: "✅", PRIS: "❌", INCONNU: "❔"}
    print("| Nom | Cible | Statut | Source |")
    print("|---|---|---|---|")
    for name, rows in results.items():
        for r in rows:
            print(f"| {name} | {r['cible']} | {icon[r['statut']]} {r['statut']} | {r['source']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
