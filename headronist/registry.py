"""Headronist offline, read-only control interface. Python >=3.9; stdlib only."""
import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "contracts/registry.v1.json"

def load():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def resolve(name, registry):
    name = registry["aliases"].get(name, name)
    if name not in registry["routes"]:
        raise ValueError("Unknown route: " + name)
    return name, registry["routes"][name]

def inspect(name, registry):
    key, paths = resolve(name, registry)
    return {"route": key, "status": registry["status"].get(key, "unspecified"),
            "paths": paths, "symbols": registry["symbols"],
            "policy": registry["policy"]}

def check(registry):
    problems = []
    if registry.get("schemaVersion") != "1.0.0":
        problems.append("Unsupported registry version")
    paths = []
    for route, refs in registry.get("routes", {}).items():
        if not isinstance(refs, list) or not refs:
            problems.append("Empty route: " + route)
            continue
        for ref in refs:
            p = pathlib.PurePosixPath(ref)
            if p.is_absolute() or ".." in p.parts or str(p) != ref:
                problems.append("Unsafe path: " + ref)
                continue
            paths.append(ref)
            if not (ROOT / ref).is_file():
                problems.append("Missing: " + ref)
    for alias in registry.get("aliases", {}):
        try:
            resolve(alias, registry)
        except ValueError:
            # Some routes are intentionally planned, but aliases must not pretend to work.
            problems.append("Unresolved alias: " + alias)
    for key in registry.get("routes", {}):
        if key not in registry.get("status", {}):
            problems.append("Missing status: " + key)
    return sorted(set(problems))

def fingerprint(registry):
    files = sorted({ref for refs in registry["routes"].values() for ref in refs})
    digest = hashlib.sha256()
    for ref in files:
        p = ROOT / ref
        if not p.is_file():
            raise FileNotFoundError(ref)
        digest.update(ref.encode() + b"\\0" + p.read_bytes() + b"\\0")
    return {"algorithm": "sha256", "files": len(files), "digest": digest.hexdigest()}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline Headronist design registry")
    parser.add_argument("command", choices=("routes", "inspect", "check", "fingerprint"))
    parser.add_argument("route", nargs="?")
    args = parser.parse_args(argv)
    registry = load()
    if args.command == "routes":
        result = [{"id": key, "status": registry["status"].get(key, "unspecified")}
                  for key in sorted(registry["routes"])]
    elif args.command == "inspect":
        if not args.route:
            parser.error("inspect requires route")
        result = inspect(args.route, registry)
    elif args.command == "check":
        errors = check(registry)
        result = {"ok": not errors, "errors": errors}
    else:
        result = fingerprint(registry)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 1 if args.command == "check" and not result["ok"] else 0

if __name__ == "__main__":
    sys.exit(main())
