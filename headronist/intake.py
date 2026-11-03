"""Compact deterministic agent/chat handoff; Python stdlib only; never executes tasks."""
import argparse
import json
import sys
from . import registry

TASK_ROUTES = {
    "landing": ("landing","navigation","typography","visualQuality"),
    "web": ("web","responsive","navigation","visualQuality"),
    "mobile": ("responsive","navigation","typography","visualQuality"),
    "presentation": ("typography","palette","visualQuality"),
    "dashboard": ("dashboard","responsive","visualQuality"),
    "visual_asset": ("image","visualQuality"),
    "docs": ("docs","typography","visualQuality"),
    "motion": ("motion","visualQuality"),
}
MAX_BYTES = 32768
def route(payload):
    if not isinstance(payload,dict): raise ValueError("Input must be a JSON object")
    if set(payload)-{"version","task","target","intent","content","constraints","evidence"}: raise ValueError("Unknown input fields")
    if payload.get("version")!="1": raise ValueError("Unsupported version")
    task=payload.get("task")
    if task not in TASK_ROUTES: raise ValueError("Unsupported task")
    target=payload.get("target")
    if not isinstance(target,str) or not 0<len(target)<=160: raise ValueError("Invalid target")
    if not isinstance(payload.get("intent",""),str) or len(payload.get("intent",""))>500: raise ValueError("Invalid intent")
    for key,limit,max_len in (("content",24,1200),("evidence",12,256)):
        value=payload.get(key,[])
        if not isinstance(value,list) or len(value)>limit or any(not isinstance(x,str) or len(x)>max_len for x in value): raise ValueError("Invalid "+key)
    c=payload.get("constraints",{})
    if not isinstance(c,dict) or set(c)-{"viewport","theme","motion","offline","noExternalAssets"}: raise ValueError("Invalid constraints")
    for key,values in {"viewport":("auto","mobile","tablet","desktop","split"),"theme":("auto","light","dark"),"motion":("off","subtle","enhanced")}.items():
        if key in c and c[key] not in values: raise ValueError("Invalid "+key)
    for key in ("offline","noExternalAssets"):
        if key in c and not isinstance(c[key],bool): raise ValueError("Invalid "+key)
    reg=registry.load()
    routes=TASK_ROUTES[task]
    paths=list(dict.fromkeys(p for r in routes for p in registry.resolve(r,reg)[1]))
    return {"version":"1","task":task,"target":target,"routes":list(routes),"paths":paths,
            "status":{r:reg["status"].get(r,"unknown") for r in routes},
            "checks":["no-overlap","no-horizontal-overflow","semantic-navigation","reduced-motion","no-fabricated-claims"],
            "note":"Routing only; no design rendered or verified."}
def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",default="-",help="JSON path or stdin")
    args=parser.parse_args(argv)
    try:
        raw=sys.stdin.buffer.read(MAX_BYTES+1) if args.input=="-" else open(args.input,"rb").read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise ValueError("Input too large")
        print(json.dumps(route(json.loads(raw)),sort_keys=True,separators=(",",":")))
        return 0
    except (ValueError,UnicodeError,OSError) as exc:
        print(json.dumps({"ok":False,"error":str(exc)},separators=(",",":")))
        return 2
if __name__=="__main__":sys.exit(main())
