"""Mesure les relectures par sous-agent sur des défauts plantés, avant et après un changement.

Usage (depuis la racine du dépôt) :
  python3 evals/run_subagents.py [--runs N] [--dry-run] [--before REF] [cas ...]
Cas : plan, doc-explore, doc-general, review-old, review-new (tous par défaut).

- plan : la relecture du plan (plan/SKILL.md, étape 5) sur un brouillon à 5 défauts. Avant ce
  changement, il n'y avait pas de relecture : 0 trouvé par construction.
- doc-explore / doc-general : le brief de relecture de brainstorming, lancé dans Explore ou dans
  general-purpose, sur un cahier des charges à 3 contradictions et 2 renvois faux.
- review-old / review-new : le skill review au commit --before (défaut a1f460b) et dans l'arbre
  de travail, sur une branche à 5 défauts et 2 leurres. Copiés dans le projet de test sous
  d'autres noms, car un skill personnel l'emporte sur un skill de projet du même nom.

Chaque rapport est noté par un correcteur (claude -p séparé) contre evals/fixtures/subagents/
cases.json. --dry-run prépare les projets de test et affiche les prompts sans appeler Claude.
"""
import argparse, json, os, re, shutil, subprocess, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "evals" / "fixtures" / "subagents"
OUT = ROOT / "evals" / "subagents-results.json"
MODEL = "claude-opus-5-5"
JUDGE_MODEL = "claude-sonnet-5-5"
ALLOWED = "Read,Grep,Glob,Bash(git:*),Agent,Task,Skill"
DENIED = "Edit,Write,NotebookEdit"
CASES = ["plan", "doc-explore", "doc-general", "review-old", "review-new"]


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=eval", "-c", "user.email=eval@example.com", *args],
                   cwd=cwd, check=True, capture_output=True)


def brief_after(skill_md, marker):
    """Le premier bloc de citation qui suit marker dans skill_md, sans les « > »."""
    text = skill_md.read_text(encoding="utf-8")
    start = text.index(marker)
    lines, inside = [], False
    for line in text[start:].splitlines():
        if line.lstrip().startswith(">"):
            inside = True
            lines.append(line.lstrip()[1:].strip())
        elif inside:
            break
    if not lines:
        raise SystemExit(f"brief introuvable après « {marker} » dans {skill_md}")
    return " ".join(lines)


def install_skill(src_files, dest, name):
    """Copie un skill (dict chemin relatif -> contenu) dans dest/.claude/skills/<name>/."""
    d = dest / ".claude" / "skills" / name
    for rel, content in src_files.items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        if rel == "SKILL.md":
            content = re.sub(r"^name: .*$", f"name: {name}", content, count=1, flags=re.M)
        f.write_text(content, encoding="utf-8")


def skill_files_at(ref, skill):
    if ref is None:
        base = ROOT / skill
        return {str(p.relative_to(base)): p.read_text(encoding="utf-8")
                for p in base.rglob("*") if p.is_file()}
    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref, f"{skill}/"], cwd=ROOT,
                           check=True, capture_output=True, text=True).stdout.split()
    return {n[len(skill) + 1:]: subprocess.run(["git", "show", f"{ref}:{n}"], cwd=ROOT, check=True,
                                               capture_output=True, text=True).stdout
            for n in names}


def build_project(case, before):
    work = Path(tempfile.mkdtemp(prefix=f"subagents-{case}-"))
    shutil.copytree(FIX / "base", work, dirs_exist_ok=True)
    if case == "plan":
        shutil.copy(FIX / "plan-draft.md", work / "docs" / "plans" / "export-csv.md")
    if case.startswith("doc"):
        shutil.copy(FIX / "requirements.md", work / "docs" / "requirements.md")
    git(work, "init", "-q", "-b", "main")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "base")
    if case.startswith("review"):
        git(work, "checkout", "-q", "-b", "export-csv")
        shutil.copytree(FIX / "branch", work, dirs_exist_ok=True)
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", "feat: export CSV")
        ref = before if case == "review-old" else None
        install_skill(skill_files_at(ref, "review"), work, case)
    return work


def subagent_prompt(agent_type, brief):
    return (f"Lance l'outil Agent avec subagent_type « {agent_type} » et, pour prompt, exactement "
            f"le texte entre les balises <brief>, sans rien y ajouter.\n<brief>\n{brief}\n</brief>\n"
            "Ensuite, réponds uniquement avec le rapport du sous-agent, recopié tel quel.")


def prompt_for(case):
    if case == "plan":
        brief = brief_after(ROOT / "plan" / "SKILL.md", "**Faire relire le plan**")
        brief = brief.replace("<plan>", "docs/plans/export-csv.md").replace(
            "<source>", "docs/tickets/export/01-export-csv.md")
        return subagent_prompt("general-purpose", brief)
    if case.startswith("doc"):
        brief = brief_after(ROOT / "brainstorming" / "SKILL.md", "fais-le relire par un sous-agent")
        brief = brief.replace("<chemin>", "docs/requirements.md")
        return subagent_prompt("Explore" if case == "doc-explore" else "general-purpose", brief)
    return (f"Appelle le Skill tool avec « {case} », avec pour point fixe main et pour spec "
            "docs/plans/export-csv.md. Ne corrige rien : donne le rapport, puis arrête-toi.")


def run_claude(prompt, cwd, model, timeout=900):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", model,
           "--allowedTools", ALLOWED, "--disallowedTools", DENIED]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, env=env,
                         text=True)
    t0, agents, agent_results, result = time.time(), [], {}, {}
    try:
        for line in p.stdout:
            if time.time() - t0 > timeout:
                result["error"] = "timeout"
                break
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = ev.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            for c in content if isinstance(content, list) else []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use" and c.get("name") in ("Agent", "Task"):
                    agents.append({"id": c["id"], "type": c["input"].get("subagent_type"),
                                   "prompt": c["input"].get("prompt", "")})
                if c.get("type") == "tool_result" and c.get("tool_use_id") in {a["id"] for a in agents}:
                    content = c.get("content")
                    if isinstance(content, list):
                        content = "\n".join(x.get("text", "") for x in content if isinstance(x, dict))
                    agent_results[c["tool_use_id"]] = content or ""
            if ev.get("type") == "result":
                result.update(text=ev.get("result", ""), cost=ev.get("total_cost_usd"),
                              ms=ev.get("duration_ms"), turns=ev.get("num_turns"))
                break
    finally:
        if p.poll() is None:
            p.kill()
    result["agents"] = [{"type": a["type"], "prompt": a["prompt"],
                         "report": agent_results.get(a["id"], "")} for a in agents]
    return result


def judge(case_key, report):
    spec = json.loads((FIX / "cases.json").read_text(encoding="utf-8"))[case_key]
    prompt = (
        "Tu notes le rapport d'un relecteur contre une liste de défauts connus. Ne lis aucun "
        "fichier. Un défaut est trouvé si le rapport le signale comme problème, même avec "
        "d'autres mots. Pour chaque leurre (un point correct qui a l'air suspect) : « absent » si "
        "le rapport n'en parle pas, « écarté » s'il en parle en le jugeant correct, douteux ou "
        "faux, « signalé » s'il le présente comme un problème confirmé. Compte à part les "
        "remarques qui ne correspondent à aucun défaut ni leurre : elles peuvent être justes "
        "(un défaut non planté) ou fausses, tu ne les juges pas.\n\n"
        f"Défauts : {json.dumps(spec['expected'], ensure_ascii=False)}\n"
        f"Leurres : {json.dumps(spec['decoys'], ensure_ascii=False)}\n\n"
        f"<rapport>\n{report}\n</rapport>\n\n"
        'Réponds uniquement en JSON : {"found": {"<id>": true|false}, "decoys": {"<id>": '
        '"absent"|"écarté"|"signalé"}, "extras": <entier>, "verdict": "<la ligne VERDICT '
        'du rapport, ou null>"}')
    out = run_claude(prompt, tempfile.mkdtemp(prefix="judge-"), JUDGE_MODEL, timeout=300)
    text = out.get("text", "")
    try:
        return json.loads(text[text.index("{"):text.rindex("}") + 1])
    except ValueError:
        return {"error": "note illisible", "raw": text[:500]}


def refs_check(report, work):
    """Remarques R-n distinctes, et combien citent un fichier:ligne qui existe dans le projet.

    Seule la première apparition d'un R-n compte (« En bref » les recite). Un chemin court
    (`export.py:18`) vaut s'il désigne un seul fichier du projet.
    """
    files = [p for p in work.rglob("*") if p.is_file() and ".git" not in p.parts]
    blocks, seen = {}, []
    for chunk in re.split(r"(?=\bR-\d+\b)", report):
        m = re.match(r"R-(\d+)", chunk)
        if m and m.group(1) not in blocks:
            blocks[m.group(1)] = chunk
    good = 0
    for chunk in blocks.values():
        for path, line in re.findall(r"([\w./-]+\.\w+):(\d+)", chunk):
            hits = [f for f in files if str(f.relative_to(work)) == path
                    or str(f.relative_to(work)).endswith("/" + path)]
            if len(hits) == 1 and 0 < int(line) <= len(hits[0].read_text(encoding="utf-8").splitlines()):
                good += 1
                break
    return {"remarks": len(blocks), "with_valid_ref": good}


def one(job, before):
    try:
        return run_one(job, before)
    except Exception as exc:  # un cas qui casse ne doit pas perdre les autres
        return {"case": job[0], "run": job[1], "cost": None, "ms": None, "error": repr(exc),
                "agent_types": [], "agent_prompts": [], "report": "", "score": {}}


def run_one(job, before):
    case, run = job
    work = build_project(case, before)
    out = run_claude(prompt_for(case), work, MODEL)
    report = out.get("text", "")
    if case != "review-old" and case != "review-new" and out["agents"]:
        report = out["agents"][0]["report"] or report
    key = "plan" if case == "plan" else "doc" if case.startswith("doc") else "review"
    row = {"case": case, "run": run, "cost": out.get("cost"), "ms": out.get("ms"),
           "error": out.get("error"), "agent_types": [a["type"] for a in out["agents"]],
           "agent_prompts": [a["prompt"] for a in out["agents"]], "report": report,
           "score": judge(key, report)}
    if key == "review":
        row["refs"] = refs_check(report, work)
    shutil.rmtree(work, ignore_errors=True)
    return row


def summary(rows):
    print(f"\n{'cas':12} {'trouvés':>9} {'leurres écartés':>16} {'hors liste':>10} "
          f"{'R-n sourcés':>12} {'coût $':>7} {'durée':>6}  sous-agents")
    for case in CASES:
        rs = [r for r in rows if r["case"] == case]
        if not rs:
            continue
        sc = [r["score"] for r in rs if "found" in r["score"]]
        n = len(sc) or 1
        found = sum(sum(s["found"].values()) for s in sc) / n
        total = len(sc[0]["found"]) if sc else 0
        decoys = [v for s in sc for v in s.get("decoys", {}).values()]
        ok_decoys = f"{sum(v != 'signalé' for v in decoys)}/{len(decoys)}" if decoys else "-"
        fa = sum(s.get("extras", 0) for s in sc) / n
        refs = [r["refs"] for r in rs if "refs" in r]
        refs_s = (f"{sum(x['with_valid_ref'] for x in refs)}/{sum(x['remarks'] for x in refs)}"
                  if refs else "-")
        cost = sum(r["cost"] or 0 for r in rs) / len(rs)
        dur = sum(r["ms"] or 0 for r in rs) / len(rs) / 1000
        types = sorted({t for r in rs for t in r["agent_types"] if t})
        verdicts = {s.get("verdict") for s in sc if s.get("verdict")}
        print(f"{case:12} {found:5.1f}/{total:<3} {ok_decoys:>16} {fa:10.1f} {refs_s:>12} "
              f"{cost:7.2f} {dur:5.0f}s  {', '.join(types) or '-'}"
              + (f"  verdict : {' | '.join(verdicts)}" if verdicts else ""))
        errors = [r["error"] for r in rs if r["error"]] + [s["error"] for s in
                                                            (r["score"] for r in rs) if "error" in s]
        if errors:
            print(f"{'':12} erreurs : {errors}")
    print("\nplan avant le changement : pas de relecture, 0 trouvé par construction.")
    print(f"Détail (rapports, prompts des sous-agents) : {OUT.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="*", default=CASES)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--before", default="a1f460b")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    unknown = set(args.cases) - set(CASES)
    if unknown:
        raise SystemExit(f"cas inconnus : {', '.join(sorted(unknown))}")
    if args.dry_run:
        for case in args.cases:
            work = build_project(case, args.before)
            files = sorted(str(p.relative_to(work)) for p in work.rglob("*")
                           if p.is_file() and ".git/" not in str(p.relative_to(work)) + "/")
            print(f"=== {case} : {work}\n{prompt_for(case)}\n--- fichiers : {', '.join(files)}\n")
        return
    jobs = [(c, r) for c in args.cases for r in range(args.runs)]
    rows = []
    with ThreadPoolExecutor(4) as ex:
        for row in ex.map(lambda j: one(j, args.before), jobs):
            rows.append(row)
            OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{row['case']} #{row['run']} : {row['error'] or 'fini'}", flush=True)
    summary(rows)


if __name__ == "__main__":
    main()
