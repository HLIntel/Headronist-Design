"""Local, versioned design-profile memory. Stdlib only; no network or model calls."""
import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PATH = Path.home() / ".headronist" / "design-memory.v1.json"
MAX_BYTES = 2_000_000

def _load(path):
    if not path.exists():
        return {"version": "1", "profiles": {}}
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Design memory exceeds 2MB")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != "1" or not isinstance(data.get("profiles"), dict):
        raise ValueError("Unsupported or invalid design memory")
    return data

def _save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".headronist-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def save_profile(profile_id, profile, path=DEFAULT_PATH, approved=False):
    if not isinstance(profile_id, str) or not profile_id.strip() or len(profile_id) > 120:
        raise ValueError("Invalid profile id")
    if not isinstance(profile, dict):
        raise ValueError("Profile must be a JSON object")
    data = _load(Path(path))
    versions = data["profiles"].setdefault(profile_id, [])
    if not isinstance(versions, list):
        raise ValueError("Invalid profile history")
    version = len(versions) + 1
    record = {
        "version": version, "savedAt": datetime.now(timezone.utc).isoformat(),
        "approved": bool(approved), "profile": profile
    }
    versions.append(record)
    _save(Path(path), data)
    return record

def get_profile(profile_id, path=DEFAULT_PATH, version=None):
    data = _load(Path(path))
    versions = data["profiles"].get(profile_id, [])
    if not versions:
        raise KeyError("Unknown design profile: " + profile_id)
    if version is None:
        return versions[-1]
    for record in versions:
        if record["version"] == version:
            return record
    raise KeyError("Unknown profile version")

def list_profiles(path=DEFAULT_PATH):
    data = _load(Path(path))
    return [{"id": key, "versions": len(value),
             "latestApproved": bool(value and value[-1].get("approved"))}
            for key, value in sorted(data["profiles"].items())]

def main(argv=None):
    parser = argparse.ArgumentParser(description="Local Headronist design memory")
    parser.add_argument("--store", default=str(DEFAULT_PATH))
    sub = parser.add_subparsers(dest="command", required=True)
    save = sub.add_parser("save"); save.add_argument("id"); save.add_argument("profile"); save.add_argument("--approved", action="store_true")
    get = sub.add_parser("get"); get.add_argument("id"); get.add_argument("--version", type=int)
    sub.add_parser("list")
    args = parser.parse_args(argv); path = Path(args.store)
    if args.command == "save":
        result = save_profile(args.id, json.loads(Path(args.profile).read_text(encoding="utf-8")), path, args.approved)
    elif args.command == "get":
        result = get_profile(args.id, path, args.version)
    else:
        result = list_profiles(path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
