"""Read-only metadata navigation with compact query responses."""
import argparse
import json
from pathlib import Path
from . import registry

CATALOG = Path(__file__).resolve().parents[1] / "contracts/catalog.v1.json"

def discover(query="", group=None, limit=12):
    if not isinstance(query, str) or len(query)>120:
        raise ValueError("Invalid query")
    if group is not None and group not in ("foundations","experience","quality","automation"):
        raise ValueError("Invalid group")
    if not isinstance(limit,int) or not 1<=limit<=50:
        raise ValueError("Invalid limit")
    catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    reg=registry.load()
    terms=query.lower().split()
    result=[]
    for key,paths in reg["routes"].items():
        meta=catalog["routes"].get(key,{})
        if group and meta.get("group")!=group: continue
        hay=" ".join([key,meta.get("label","")," ".join(meta.get("tags",[]))]).lower()
        if any(term not in hay for term in terms): continue
        result.append({"id":key,"label":meta.get("label",key),"group":meta.get("group","other"),
                       "priority":meta.get("priority",99),"status":reg["status"].get(key,"unspecified"),
                       "files":len(paths),"tags":meta.get("tags",[])})
    result.sort(key=lambda x:(x["priority"],x["id"]))
    return {"version":"1","total":len(result),"results":result[:limit],"truncated":len(result)>limit}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--query",default="")
    parser.add_argument("--group")
    parser.add_argument("--limit",type=int,default=12)
    args=parser.parse_args()
    print(json.dumps(discover(args.query,args.group,args.limit),separators=(",",":"),sort_keys=True))

if __name__=="__main__":
    main()
