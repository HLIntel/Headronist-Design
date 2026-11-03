"""Context-aware asset recommendations and small, original SVG background generation.

No network access, API keys, third-party packages, or implicit asset downloads.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "contracts" / "asset-sources.v1.json"

KEYWORDS = {
    "abstract": ("abstract", "network", "trust", "infrastructure", "ai", "agent", "security", "data center"),
    "product-ui": ("dashboard", "saas", "app", "interface", "product", "software", "admin", "analytics"),
    "editorial-photo": ("editorial", "photography", "people", "team", "office", "workspace", "real world", "portrait"),
    "illustration": ("illustration", "onboarding", "empty state", "explainer", "friendly"),
    "texture": ("texture", "pattern", "background", "subtle", "surface"),
    "placeholder": ("placeholder", "layout testing", "wireframe test"),
}

def classify(intent):
    text = intent.lower()
    for kind, terms in KEYWORDS.items():
        if any(term in text for term in terms):
            return kind
    return "abstract"

def recommend(intent, kind="auto", offline=True, allow_placeholders=False):
    if not isinstance(intent, str) or not 1 <= len(intent.strip()) <= 600:
        raise ValueError("intent must contain 1 to 600 characters")
    if kind == "auto":
        kind = classify(intent)
    aliases = {"hero": "abstract", "photo": "editorial-photo", "illustration": "illustration", "background": "texture", "placeholder": "placeholder"}
    kind = aliases.get(kind, kind)
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    matches = []
    for source_id, source in catalog["sources"].items():
        if kind not in source["bestFor"] and not (kind == "product-ui" and "diagram" in source["bestFor"]):
            continue
        if offline and source["network"]:
            continue
        if source["category"] == "placeholder" and not allow_placeholders:
            continue
        matches.append({
            "id": source_id,
            "label": source["label"],
            "category": source["category"],
            "access": source["access"],
            "url": source.get("url"),
            "production": source["production"],
            "license": source["license"],
            "notes": source["notes"],
        })
    if not matches:
        matches = [{
            "id": "nativeSvg", "label": "Native SVG and CSS", "category": "generated",
            "access": "keyless", "production": True,
            "license": "Original project-generated output",
            "notes": "Use a locally generated SVG/CSS asset; no external request required."
        }]
    return {
        "version": "1",
        "intent": intent,
        "kind": kind,
        "policy": "local-first" if offline else "curated-source",
        "recommendations": matches,
        "selectionGuidance": [
            "Prefer authentic product screenshots for software features.",
            "Use photography only when a real human or physical environment adds information.",
            "Use abstract SVG/CSS for infrastructure, trust, network and technical concepts.",
            "Record source URL, creator, license, retrieval date and any attribution with downloaded assets.",
            "Never treat random placeholders as final creative direction."
        ],
        "networkRequested": False,
    }

def make_pattern(title="Headronist", foreground="#7894b8", background="#0b1422"):
    """Return an original, restrained network-field SVG with no embedded text."""
    for color in (foreground, background):
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise ValueError("colors must be six-digit hex values")
    safe_title = re.sub(r"[^a-zA-Z0-9 _-]", "", title)[:60] or "Abstract network"
    nodes = [(90, 120), (300, 65), (510, 155), (740, 75), (940, 185),
             (180, 390), (430, 330), (680, 430), (900, 370)]
    lines = "".join(
        f'<path d="M{x1} {y1} L{x2} {y2}" />'
        for (x1, y1), (x2, y2) in zip(nodes, nodes[1:])
    )
    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{7 if i in (2, 6) else 4}" />'
        for i, (x, y) in enumerate(nodes)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 512" role="img" aria-labelledby="title desc">
  <title id="title">{safe_title}</title>
  <desc id="desc">Abstract connected network nodes on a quiet dark field.</desc>
  <defs>
    <linearGradient id="field" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{background}"/>
      <stop offset="1" stop-color="#101f32"/>
    </linearGradient>
    <radialGradient id="glow">
      <stop offset="0" stop-color="{foreground}" stop-opacity=".18"/>
      <stop offset="1" stop-color="{foreground}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1024" height="512" fill="url(#field)"/>
  <circle cx="530" cy="245" r="340" fill="url(#glow)"/>
  <g fill="none" stroke="{foreground}" stroke-opacity=".25" stroke-width="1.4">{lines}</g>
  <g fill="{foreground}" fill-opacity=".72">{circles}</g>
</svg>
'''

def main(argv=None):
    parser = argparse.ArgumentParser(description="Recommend contextual visual assets without external fetches.")
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("recommend")
    rec.add_argument("--intent", required=True)
    rec.add_argument("--kind", default="auto", choices=("auto", "abstract", "product-ui", "editorial-photo", "illustration", "texture", "hero", "photo", "background", "placeholder"))
    rec.add_argument("--allow-network-sources", action="store_true")
    rec.add_argument("--allow-placeholders", action="store_true")
    svg = sub.add_parser("pattern")
    svg.add_argument("--output", default="headronist-network.svg")
    svg.add_argument("--title", default="Headronist")
    svg.add_argument("--foreground", default="#7894b8")
    svg.add_argument("--background", default="#0b1422")
    args = parser.parse_args(argv)
    if args.command == "recommend":
        result = recommend(args.intent, args.kind, offline=not args.allow_network_sources, allow_placeholders=args.allow_placeholders)
        print(json.dumps(result, indent=2))
        return 0
    Path(args.output).write_text(make_pattern(args.title, args.foreground, args.background), encoding="utf-8")
    print(json.dumps({"created": args.output, "format": "svg", "network": False}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
