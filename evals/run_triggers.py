"""Teste quel skill Claude déclenche en premier pour chaque phrase de triggers.json.

Usage : python3 evals/run_triggers.py [passages par phrase] (depuis la racine du dépôt)
Lance claude -p dans un dossier vide, avec les skills réellement installés.
"""
import json, os, subprocess, sys, time, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).parent
WORKDIR=tempfile.mkdtemp(prefix="triggers-")
MINE={"plan","implement","tdd","to-spec","to-tickets","tickets","interview","research","adr","to-questionnaire","domain-modeling","review","debug","wizard"}
def first_skill(q, timeout=120):
    env={k:v for k,v in os.environ.items() if k!="CLAUDECODE"}
    p=subprocess.Popen(["claude","-p",q,"--output-format","stream-json","--verbose","--model","claude-opus-5-5","--max-turns","4"],
        stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,cwd=WORKDIR,env=env,text=True)
    t0=time.time(); tools=[]
    try:
        for line in p.stdout:
            if time.time()-t0>timeout: break
            try: ev=json.loads(line)
            except: continue
            if ev.get("type")=="assistant":
                for c in ev["message"].get("content",[]):
                    if c.get("type")=="tool_use":
                        if c["name"]=="Skill":
                            return c["input"].get("skill","?"), tools
                        tools.append(c["name"])
            if ev.get("type")=="result": break
    finally:
        if p.poll() is None: p.kill()
    return "none", tools
qs=json.load(open(HERE/"triggers.json"))
runs=int(sys.argv[1]) if len(sys.argv)>1 else 1
jobs=[(i,r) for i in range(len(qs)) for r in range(runs)]
def work(j):
    i,r=j; s,t=first_skill(qs[i]["q"]); return i,r,s,t
res=[]
with ThreadPoolExecutor(6) as ex:
    for i,r,s,t in ex.map(work,jobs):
        res.append({"i":i,"q":qs[i]["q"],"ok":qs[i]["ok"],"got":s,"tools_before":t})
json.dump(res,open(HERE/"results.json","w"),ensure_ascii=False,indent=1)
good=0
for x in sorted(res,key=lambda x:x["i"]):
    g=x["got"]; norm=g if g in MINE else ("none" if g=="none" else "autre:"+g)
    passed = norm in x["ok"]
    good+=passed
    print(("✅" if passed else "❌"), f"attendu={'|'.join(x['ok']):14} obtenu={norm:22}", x["q"][:70])
print(f"\n{good}/{len(res)} corrects")
