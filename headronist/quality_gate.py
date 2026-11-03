"""Deterministic anti-drift checks for registry/catalog and opaque sRGB contrast."""
import argparse
import json
import re
from pathlib import Path
from . import registry

ROOT=Path(__file__).resolve().parents[1]
def contrast(a,b):
    def luminance(value):
        if not isinstance(value,str) or not re.fullmatch(r"#[0-9a-fA-F]{6}",value):
            raise ValueError("Expected opaque #RRGGBB")
        rgb=[int(value[i:i+2],16)/255 for i in (1,3,5)]
        linear=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in rgb]
        return sum(x*w for x,w in zip(linear,(0.2126,0.7152,0.0722)))
    a,b=sorted((luminance(a),luminance(b)),reverse=True)
    return round((a+0.05)/(b+0.05),3)

def audit():
    reg=registry.load()
    cat=json.loads((ROOT/"contracts/catalog.v1.json").read_text(encoding="utf-8"))
    errors=registry.check(reg)
    warnings=[]
    for key,meta in cat["routes"].items():
        if key not in reg["routes"]: errors.append("Catalog route missing from registry: "+key)
        if not isinstance(meta.get("label"),str) or not meta["label"].strip(): errors.append("Missing label: "+key)
        if meta.get("group") not in cat["groups"]: errors.append("Unknown group: "+key)
        if not isinstance(meta.get("priority"),int) or isinstance(meta.get("priority"),bool) or not 0<=meta["priority"]<=100:
            errors.append("Invalid priority: "+key)
        if not isinstance(meta.get("tags"),list) or not all(isinstance(t,str) and t for t in meta["tags"]):
            errors.append("Invalid tags: "+key)
    for key in reg["routes"]:
        if key not in cat["routes"]: warnings.append("Unlabeled route: "+key)
    for alias,target in reg["aliases"].items():
        if target not in reg["routes"]: errors.append("Unresolved alias: "+alias)
    return {"ok":not errors,"errors":sorted(set(errors)),"warnings":sorted(set(warnings)),"routeCount":len(reg["routes"]),"catalogCount":len(cat["routes"]),"verified":"static-contracts-only"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contrast",nargs=2,metavar=("FOREGROUND","BACKGROUND"))
    args=p.parse_args()
    try:
        result={"ratio":contrast(*args.contrast)} if args.contrast else audit()
    except (ValueError,OSError,KeyError,TypeError) as e:
        result={"ok":False,"errors":[str(e)]}
    print(json.dumps(result,sort_keys=True,separators=(",",":")))
    return 1 if result.get("ok") is False else 0
if __name__=="__main__":
    raise SystemExit(main())
