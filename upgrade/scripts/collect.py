#!/usr/bin/env python3
"""Collecte les faits d'un audit de versions : fin de vie, maintenance, failles.

Lit un inventaire JSON (voir ../SKILL.md, étape 2) et écrit sur la sortie standard un JSON
enrichi, élément par élément. Sans dépendance externe. Chaque critère qui n'a pas pu être
évalué le dit (`unknown` et une raison) : une donnée absente n'est jamais un feu vert.

    python3 collect.py inventory.json --list list.json --outdated outdated.json \
        [--today AAAA-MM-JJ] [--no-osv] [--no-github] > facts.json

--list : sortie de `pnpm list --json --depth Infinity -r` (ou `npm ls --json --all`) ;
--outdated : sortie de `pnpm outdated --format json -r` (ou `npm outdated --json`).
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone

EOL = "https://endoflife.date/api/v1"
DEPS = "https://api.deps.dev/v3"
OSV = "https://api.osv.dev/v1"

EOL_SOON_DAYS = 180    # fin de vie dans moins de 6 mois
STALE_DAYS = 730       # 365 jours signalent à tort des paquets finis (jinja2 chez Trail of Bits)
FLOATING_TAGS = {"", "latest", "lts", "current", "stable", "alpine", "slim", "bookworm",
                 "bullseye", "trixie", "mainline"}
GH_LOG = {}
SEVERITY_ORDER = ["CRITICAL", "HIGH", "MODERATE", "MEDIUM", "LOW", "UNKNOWN"]


class Fetcher:
    """Appels HTTP avec cache ; remplaçable dans les tests."""

    def __init__(self):
        self.cache = {}
        self.log = {}

    def get(self, url, body=None):
        key = (url, json.dumps(body, sort_keys=True) if body is not None else None)
        if key in self.cache:
            return self.cache[key]
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, headers={
            "Accept": "application/json", "User-Agent": "upgrade-skill",
            **({"Content-Type": "application/json"} if data else {})})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.load(resp)
        except urllib.error.HTTPError as e:
            result = {"_error": f"HTTP {e.code}"}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            result = {"_error": str(e)}
        self.cache[key] = result
        self.log[urllib.parse.urlsplit(url).netloc] = datetime.now(timezone.utc).isoformat(
            timespec="seconds")
        return result


def days_between(start, end):
    return (end - start).days


def parse_day(value):
    if not value or not isinstance(value, str):
        return None
    return date.fromisoformat(value[:10])


# --- Fin de vie (endoflife.date) -------------------------------------------------------------

def match_cycle(releases, version):
    """Le cycle le plus précis qui préfixe la version : 7.2.4 → 7.2 puis 7 ; ou un nom de code."""
    names = {r["name"]: r for r in releases}
    v = str(version).lstrip("vV")
    parts = v.split(".")
    for i in range(len(parts), 0, -1):
        if ".".join(parts[:i]) in names:
            return names[".".join(parts[:i])]
    for r in releases:
        if r.get("codename") and r["codename"].lower() == v.lower():
            return r
    return None


def eol_status(product, version, fetch, today):
    """État de fin de vie d'une version d'un produit, et la cible conseillée."""
    data = fetch.get(f"{EOL}/products/{product}/")
    if "_error" in data:
        return {"status": "unknown", "reason": f"endoflife.date : {data['_error']}"}
    releases = data["result"]["releases"]
    out = {"product": product, "version": version, "status": "unknown"}
    maintained = [r for r in releases if r.get("isMaintained") and not r.get("isEol")]
    lts = [r for r in maintained if r.get("isLts")]
    target = (lts or maintained or [None])[0]
    if target:
        out["target"] = {"cycle": target["name"], "latest": (target.get("latest") or {}).get("name"),
                         "eoasFrom": target.get("eoasFrom"), "eolFrom": target.get("eolFrom"),
                         "lts": bool(target.get("isLts"))}
    release = match_cycle(releases, version)
    if release is None:
        out["reason"] = f"version {version} introuvable parmi les cycles de {product}"
        return out
    eol_from = parse_day(release.get("eolFrom"))
    # eoasFrom : fin du support actif (Node : passage de LTS active à maintenance)
    out.update(cycle=release["name"], eoasFrom=release.get("eoasFrom"),
               eolFrom=release.get("eolFrom"),
               latestInCycle=(release.get("latest") or {}).get("name"),
               lts=bool(release.get("isLts")))
    if release.get("isEol") or (eol_from and eol_from <= today):
        out["status"] = "eol"
    elif eol_from and days_between(today, eol_from) <= EOL_SOON_DAYS:
        out["status"] = "eol-soon"
    elif release.get("isMaintained") is False:
        out["status"] = "eol"
    else:
        out["status"] = "supported"
        if eol_from is None:
            out["reason"] = "date de fin de vie non publiée"
    return out


# --- Images Docker ---------------------------------------------------------------------------

DEBIAN_CODENAMES = {"buster": "10", "bullseye": "11", "bookworm": "12", "trixie": "13",
                    "forky": "14"}


def parse_image(ref):
    """node:18.19-alpine3.18 → nom, tag, version (18.19), système de base (alpine-linux 3.18)."""
    ref = ref.split("@")[0]
    name, _, tag = ref.rpartition(":") if ":" in ref.split("/")[-1] else (ref, "", "")
    name = re.sub(r"^(docker\.io|index\.docker\.io)/", "", name)
    if "/" not in name:
        name = f"library/{name}"
    m = re.match(r"^v?(\d+(?:\.\d+)*)", tag)
    version = m.group(1) if m else None
    base = None
    if a := re.search(r"alpine(\d+\.\d+)", tag):
        base = ("alpine-linux", a.group(1))
    else:
        for codename, cycle in DEBIAN_CODENAMES.items():
            if codename in tag:
                base = ("debian", cycle)
    floating = version is None or tag.lower() in FLOATING_TAGS
    return {"name": name, "tag": tag or "latest", "version": version, "base": base,
            "floating": floating}


def image_product(name, fetch):
    data = fetch.get(f"{EOL}/identifiers/purl/")
    if "_error" in data:
        return None, data["_error"]
    purl = f"pkg:docker/{name}"
    for item in data["result"]:
        if item["identifier"] == purl:
            return item["product"]["name"], None
    return None, f"aucun produit endoflife.date pour {purl}"


def image_status(ref, fetch, today):
    img = parse_image(ref)
    out = {"ref": ref, "tag": img["tag"]}
    product, err = image_product(img["name"], fetch)
    out["product"] = product
    if img["floating"]:
        out["status"] = "floating"
        out["reason"] = "tag flottant : la version réelle dépend du jour du pull"
    elif product is None:
        out["status"] = "unknown"
        out["reason"] = err
    else:
        out.update({k: v for k, v in eol_status(product, img["version"], fetch, today).items()
                    if k not in ("product", "version")})
    if img["base"]:
        out["base"] = eol_status(img["base"][0], img["base"][1], fetch, today)
    return out


# --- Paquets npm (deps.dev, GitHub, OSV) -----------------------------------------------------

def bump_kind(current, latest):
    def nums(v):
        m = re.match(r"^v?(\d+)\.(\d+)\.(\d+)", str(v or ""))
        return tuple(int(x) for x in m.groups()) if m else None
    c, lt = nums(current), nums(latest)
    if not c or not lt:
        return "unknown"
    if c >= lt:
        return "none"
    if c[0] != lt[0] or (c[0] == 0 and c[1] != lt[1]):  # en 0.x, une mineure casse
        return "major"
    return "minor" if c[1] != lt[1] else "patch"


def github_repo(fetch, name, version):
    q = urllib.parse.quote(name, safe="")
    data = fetch.get(f"{DEPS}/systems/npm/packages/{q}/versions/{urllib.parse.quote(version)}")
    if "_error" in data:
        return data, None
    for p in data.get("relatedProjects", []):
        if p.get("relationType") == "SOURCE_REPO" and p["projectKey"]["id"].startswith("github.com/"):
            return data, p["projectKey"]["id"]
    return data, None


def gh_repo_state(repo):
    """archived et pushed_at via gh (authentifié : 5000 requêtes/heure au lieu de 60)."""
    try:
        res = subprocess.run(["gh", "api", f"repos/{repo.removeprefix('github.com/')}",
                              "--jq", "[.archived, .pushed_at]"],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"_error": str(e)}
    if res.returncode != 0:
        return {"_error": res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "gh"}
    archived, pushed = json.loads(res.stdout)
    GH_LOG["api.github.com"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {"archived": archived, "pushedAt": pushed}


def package_status(pkg, fetch, today, use_github):
    name, version = pkg["name"], pkg["version"]
    out = {"name": name, "version": version, "latest": pkg.get("latest"), "signals": []}
    q = urllib.parse.quote(name, safe="")
    listing = fetch.get(f"{DEPS}/systems/npm/packages/{q}")
    if "_error" in listing:
        out["maintenance"] = "unknown"
        out["reason"] = f"deps.dev : {listing['_error']} (paquet privé ou hors du registre public ?)"
        return out
    default = next((v for v in listing["versions"] if v.get("isDefault")), None)
    installed = next((v for v in listing["versions"]
                      if v["versionKey"]["version"] == version), None)
    if default:
        out["latest"] = out["latest"] or default["versionKey"]["version"]
        out["lastPublish"] = default.get("publishedAt")
        if default.get("isDeprecated"):
            out["signals"].append(f"dernière version dépréciée : {default.get('deprecatedReason')}")
    if installed and installed.get("isDeprecated"):
        out["deprecated"] = installed.get("deprecatedReason") or True
    out["bump"] = bump_kind(version, out["latest"])

    version_data, repo = github_repo(fetch, name, version)
    out["advisories"] = [a["id"] for a in version_data.get("advisoryKeys", [])]
    out["repo"] = repo
    if repo:
        project = fetch.get(f"{DEPS}/projects/{urllib.parse.quote(repo, safe='')}")
        checks = (project.get("scorecard") or {}).get("checks", [])
        maintained = next((c["score"] for c in checks if c["name"] == "Maintained"), None)
        out["scorecardMaintained"] = maintained if maintained != -1 else None
        if use_github:
            state = gh_repo_state(repo)
            if "_error" in state:
                out["signals"].append(f"état du dépôt inconnu : {state['_error']}")
            else:
                out.update(state)

    last = parse_day(out.get("lastPublish"))
    if default and default.get("isDeprecated") or out.get("archived"):
        out["maintenance"] = "abandoned"
    elif last and days_between(last, today) > STALE_DAYS:
        out["maintenance"] = "stale"
        out["signals"].append(f"aucune version depuis {days_between(last, today)} jours")
        if out.get("scorecardMaintained") == 0:
            out["signals"].append("Scorecard Maintained à 0 : aucune activité sur 90 jours")
    elif last:
        out["maintenance"] = "active"
    else:
        out["maintenance"] = "unknown"
        out["reason"] = "date de la dernière version introuvable"
    return out


def published_versions(fetch, names):
    """Versions publiées des paquets, d'après deps.dev ; None si inconnu."""
    versions = set()
    for name in names:
        listing = fetch.get(f"{DEPS}/systems/npm/packages/{urllib.parse.quote(name, safe='')}")
        if "_error" in listing:
            return None
        versions.update(v["versionKey"]["version"] for v in listing["versions"])
    return versions


def severity(vuln):
    s = ((vuln.get("database_specific") or {}).get("severity") or "UNKNOWN").upper()
    return s if s in SEVERITY_ORDER else "UNKNOWN"


def osv_scan(packages, fetch):
    """Failles connues d'une liste de paquets, par OSV ; dédoublonnées par identifiant."""
    found = {}
    for start in range(0, len(packages), 500):
        chunk = packages[start:start + 500]
        body = {"queries": [{"package": {"name": p["name"], "ecosystem": "npm"},
                             "version": p["version"]} for p in chunk]}
        res = fetch.get(f"{OSV}/querybatch", body)
        if "_error" in res:
            return {"_error": f"OSV : {res['_error']}"}
        for p, r in zip(chunk, res.get("results", [])):
            for v in r.get("vulns", []):
                found.setdefault(v["id"], set()).add(f"{p['name']}@{p['version']}")
    with ThreadPoolExecutor(max_workers=8) as pool:  # remplit le cache du Fetcher
        list(pool.map(lambda vid: fetch.get(f"{OSV}/vulns/{vid}"), found))
        names = {a.rsplit("@", 1)[0] for affected in found.values() for a in affected}
        list(pool.map(lambda n: fetch.get(
            f"{DEPS}/systems/npm/packages/{urllib.parse.quote(n, safe='')}"), names))
    vulns, seen = [], set()
    for vid, affected in sorted(found.items()):
        if vid in seen:  # alias d'une faille déjà gardée (GHSA-a et GHSA-b pour un même CVE)
            continue
        detail = fetch.get(f"{OSV}/vulns/{vid}")
        aliases = detail.get("aliases", [])
        seen.update(aliases)
        names = {a.rsplit("@", 1)[0] for a in affected}
        fixed = sorted({e["fixed"] for a in detail.get("affected", [])
                        if (a.get("package") or {}).get("name") in names
                        for rng in a.get("ranges", []) for e in rng.get("events", [])
                        if "fixed" in e})
        published = published_versions(fetch, names)
        vulns.append({"id": vid, "aliases": aliases,
                      "summary": detail.get("summary"), "severity": severity(detail),
                      "malicious": vid.startswith("MAL-"), "packages": sorted(affected),
                      "fixed": fixed,
                      "fixPublished": (any(f in published for f in fixed)
                                       if published is not None else None)})
    vulns.sort(key=lambda v: (not v["malicious"], SEVERITY_ORDER.index(v["severity"])))
    return vulns


# --- Sorties du gestionnaire de paquets -----------------------------------------------------

DEP_KEYS = ("dependencies", "devDependencies", "optionalDependencies")


def packages_from_list(data):
    """Paquets installés d'après `pnpm list --json` (une liste de projets) ou `npm ls --json`.

    Directs : les dépendances de premier niveau de chaque projet. Les liens de workspace
    (`link:`, `file:`) ne sont pas des paquets du registre : ignorés.
    """
    projects = data if isinstance(data, list) else [data]
    found = {}

    def walk(deps, direct, project):
        for name, info in (deps or {}).items():
            version = str(info.get("version", ""))
            if not re.match(r"^\d", version):
                continue
            pkg = found.setdefault((name, version), {"name": name, "version": version,
                                                     "direct": False, "sources": set()})
            if direct:
                pkg["direct"] = True
                pkg["sources"].add(project)
            walk(info.get("dependencies"), False, project)

    for project in projects:
        label = project.get("name") or project.get("path") or "."
        for key in DEP_KEYS:
            walk(project.get(key), True, label)
    return [{"name": p["name"], "version": p["version"], "direct": p["direct"],
             **({"source": ", ".join(sorted(p["sources"]))} if p["sources"] else {})}
            for p in found.values()]


def apply_outdated(packages, outdated):
    """Reporte `latest` (pnpm ou npm outdated) sur les paquets directs à la version installée."""
    for pkg in packages:
        info = outdated.get(pkg["name"])
        if pkg.get("direct") and info and info.get("current") in (None, pkg["version"]):
            pkg["latest"] = info.get("latest")
    return packages


def merge_packages(*lists):
    merged = {}
    for items in lists:
        for p in items:
            key = (p["name"], p["version"])
            merged[key] = {**merged.get(key, {}), **p,
                           "direct": p.get("direct", True) or merged.get(key, {}).get("direct",
                                                                                       False)}
    return list(merged.values())


# --- Assemblage ------------------------------------------------------------------------------

def collect(inventory, fetch, today, use_osv=False, use_github=True):
    def with_source(item, result):
        return {"source": item.get("source"), **result}

    with ThreadPoolExecutor(max_workers=8) as pool:
        products = list(pool.map(lambda i: with_source(
            i, eol_status(i["product"], i["version"], fetch, today)), inventory.get("products", [])))
        images = list(pool.map(lambda i: with_source(i, image_status(i["ref"], fetch, today)),
                               inventory.get("images", [])))
        direct = [p for p in inventory.get("packages", []) if p.get("direct", True)]
        packages = list(pool.map(lambda p: with_source(
            p, package_status(p, fetch, today, use_github)), direct))
    out = {"today": today.isoformat(), "products": products, "images": images,
           "packages": packages}
    if use_osv:
        out["osv"] = osv_scan(inventory.get("packages", []), fetch)
    out["sources"] = {**fetch.log, **GH_LOG}
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inventory", help="inventaire JSON ; - pour l'entrée standard")
    parser.add_argument("--list", help="sortie JSON de pnpm list ou npm ls")
    parser.add_argument("--outdated", help="sortie JSON de pnpm outdated ou npm outdated")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--no-osv", action="store_true",
                        help="ne pas chercher les failles des paquets dans OSV")
    parser.add_argument("--no-github", action="store_true",
                        help="ne pas lire l'état des dépôts GitHub (archivé, dernier push)")
    args = parser.parse_args(argv)
    with (sys.stdin if args.inventory == "-" else open(args.inventory)) as f:
        inventory = json.load(f)
    listed = []
    if args.list:
        with open(args.list) as f:
            listed = packages_from_list(json.load(f))
    if args.outdated:
        with open(args.outdated) as f:
            text = f.read().strip()
        apply_outdated(listed, json.loads(text) if text else {})
    inventory["packages"] = merge_packages(listed, inventory.get("packages", []))
    use_github = not args.no_github and shutil.which("gh") is not None
    result = collect(inventory, Fetcher(), args.today, not args.no_osv, use_github)
    if not use_github:
        result["githubSkipped"] = "gh absent ou --no-github : état archivé des dépôts non évalué"
    json.dump(result, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
