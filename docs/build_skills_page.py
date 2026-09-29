"""Génère docs/skills.html : la carte des skills, leurs appels et leurs parcours.

Usage : python3 docs/build_skills_page.py (depuis n'importe où)
Lit chaque <skill>/SKILL.md du dépôt et injecte les données dans docs/skills.template.html.
"""
import json, re, subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALL = re.compile(r"Skill\s+tool\s+avec\s+«\s*([a-z0-9-]+)\s*»")


def frontmatter(text):
    """Les champs simples « clé: valeur » du bloc --- en tête d'un SKILL.md."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fields = {}
    for line in (m.group(1) if m else "").splitlines():
        key, sep, value = line.partition(":")
        if sep:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
            fields[key.strip()] = value
    return fields


def load_skills(root):
    """{nom: {"desc", "user", "calls"}} pour chaque <dossier>/SKILL.md de root."""
    skills, texts = {}, {}
    for path in sorted(Path(root).glob("*/SKILL.md")):
        name, text = path.parent.name, path.read_text()
        fm = frontmatter(text)
        skills[name] = {
            "desc": fm.get("description", ""),
            "user": fm.get("disable-model-invocation") == "true",
            "calls": [],
        }
        texts[name] = text
    for name, text in texts.items():
        for called in CALL.findall(text):
            if called in skills and called != name and called not in skills[name]["calls"]:
                skills[name]["calls"].append(called)
    return skills


def load_situations(root, skills=None):
    """Les lignes du tableau de next/SKILL.md : [{"q", "s", "cmd"}]."""
    path = Path(root) / "next" / "SKILL.md"
    if not path.exists():
        return []
    skills = skills if skills is not None else load_skills(root)
    rows = []
    for q, cmd in re.findall(r"^\| (.+?) \| `(/[^`]+)` \|$", path.read_text(), re.M):
        name = cmd[1:].split()[0]
        if name in skills:
            rows.append({"q": q, "s": name, "cmd": cmd})
    return rows


def ungrouped(skills, template):
    """Les skills absents de COLUMNS dans le gabarit, par famille : {"u": [...], "m": [...]}."""
    block = re.search(r"const COLUMNS = \[(.*?)\n\s*\];", template, re.S)
    lists = re.findall(r'\["[^"]+", \[([^\]]*)\]\]', block.group(1) if block else "")
    grouped = {name for inner in lists for name in re.findall(r'"([^"]+)"', inner)}
    others = {"u": [], "m": []}
    for name, skill in skills.items():
        if name not in grouped:
            others["u" if skill["user"] else "m"].append(name)
    return others


def build_page(root, template):
    """Le gabarit, avec les données des skills à la place de /*DATA*/."""
    git = subprocess.run(["git", "log", "-1", "--format=%h"], cwd=root,
                         capture_output=True, text=True)
    skills = load_skills(root)
    data = {
        "skills": skills,
        "situations": load_situations(root, skills),
        "others": ungrouped(skills, template),
        "commit": git.stdout.strip() if git.returncode == 0 else "",
        "date": date.today().strftime("%d/%m/%Y"),
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return template.replace("/*DATA*/", payload)


if __name__ == "__main__":
    here = Path(__file__).parent
    html = build_page(ROOT, (here / "skills.template.html").read_text())
    (here / "skills.html").write_text(html)
    print("docs/skills.html générée")
