"""Deterministic anti-drift checks for registry/catalog, executed static
quality-gate checks against the examples and their bound CSS, and opaque
sRGB contrast."""
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
    surface=surface_checks()
    errors+=surface["errors"]
    return {"ok":not errors,"errors":sorted(set(errors)),"warnings":sorted(set(warnings)),"routeCount":len(reg["routes"]),"catalogCount":len(cat["routes"]),"surfaceChecks":{"examples":surface["examples"],"bodyLineHeights":surface["bodyLineHeights"]},"notExecuted":surface["notExecuted"],"verified":"static-surface-checks-executed"}

def _plain(fragment):
    return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",fragment)).strip()

def _bound_css(example):
    html=example.read_text(encoding="utf-8")
    sheets=[]
    for href in re.findall(r'<link rel="stylesheet" href="([^"]+)"',html):
        target=(example.parent/href).resolve()
        if target.exists(): sheets.append(target.read_text(encoding="utf-8"))
    sheets+=re.findall(r"<style[^>]*>(.*?)</style>",html,re.S)
    return html,"\n".join(sheets)

def surface_checks():
    """Execute the contracts/quality.v1.json gates that static analysis can
    settle, against every example and the CSS it actually binds. Gates that
    need a layout engine are reported under notExecuted, never as passed."""
    gates=json.loads((ROOT/"contracts/quality.v1.json").read_text(encoding="utf-8"))["gates"]
    max_headline=gates["headlineMaxCharacters"]; min_touch=gates["minimumTouchTargetPx"]
    min_line=float(gates["minimumBodyLineHeight"]); min_viewport=min(gates["requiredViewports"])
    ran=["headline-length","touch-target-floor","body-line-height","fixed-width-overflow"]
    errors=[]; per_example={}; body_lines={}
    for example in sorted((ROOT/"examples").glob("*.html")):
        name=example.name
        html,css=_bound_css(example)
        for h in re.findall(r"<h1[^>]*>(.*?)</h1>",html,re.S):
            text=_plain(h)
            if len(text)>max_headline: errors.append(f"{name}: headline {len(text)} chars exceeds {max_headline}")
        clean=re.sub(r"/\*.*?\*/","",css,flags=re.S)
        tokens={var:float(val) for var,val in re.findall(r"(--[a-z0-9-]+)\s*:\s*([0-9.]+)\s*;",clean)}
        for selector,body in re.findall(r"([^{}]+)\{([^{}]*)\}",clean):
            for prop in ("min-height","min-width"):
                m=re.search(prop+r"\s*:\s*([0-9.]+)px",body)
                if m and float(m.group(1))<min_touch:
                    errors.append(f"{name}: {prop} {m.group(1)}px below {min_touch}px floor ({selector.strip()[:48]})")
            if "body" in selector:
                m=re.search(r"line-height\s*:\s*(var\(--[a-z0-9-]+\)|[0-9.]+)",body)
                if m:
                    raw=m.group(1)
                    value=tokens.get(raw[4:-1]) if raw.startswith("var(") else float(raw)
                    if value is not None: body_lines[name]=value
        if name in body_lines and body_lines[name]<min_line:
            errors.append(f"{name}: body line-height {body_lines[name]} below {min_line}")
        scan=re.sub(r"@(media|container)[^{]*\{","",clean)+"\n"+html
        for prop,value in re.findall(r"(?:^|[;{]\s*)(min-width|width)\s*:\s*([0-9.]+)px",scan):
            if float(value)>min_viewport:
                errors.append(f"{name}: fixed {prop} {value}px exceeds smallest required viewport {min_viewport}px")
        per_example[name]=list(ran)
    if not body_lines: errors.append("No body line-height declaration resolved in any example's bound CSS")
    not_executed=["rendered viewport sweep ("+", ".join(str(v) for v in gates["requiredViewports"])+")",
                  "zoom "+" and ".join(str(z)+"%" for z in gates["zoomPercent"]),
                  "measured horizontal overflow <= "+str(gates["horizontalOverflowPx"])+"px (requires layout)"]
    return {"examples":per_example,"bodyLineHeights":body_lines,"errors":sorted(set(errors)),"notExecuted":not_executed}

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
