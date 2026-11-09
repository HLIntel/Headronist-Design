"""Offline checks for local Markdown links and accidental personal paths."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)]+)\)")
PERSONAL_PATH = re.compile(r"(?:/Users/|/home/)[^/\s]+/")


def audit(root=ROOT):
    files = [root / "README.md", root / "AGENTS.md"]
    files += sorted((root / "docs").glob("*.md"))
    files += sorted((root / "assets").rglob("*.md"))
    errors = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        if PERSONAL_PATH.search(text):
            errors.append({"file": rel, "kind": "personal-path"})
        for raw in LINK.findall(text):
            target = raw.strip().split()[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append({"file": rel, "kind": "invalid-local-link", "target": target})
    return {"ok": not errors, "filesChecked": len(files), "errors": errors,
            "scope": "markdown local paths and personal home paths; no anchors, binary metadata, git history or secret detection"}


def main():
    result = audit()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
