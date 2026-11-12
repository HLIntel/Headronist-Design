"""Context-aware visual prompt construction and chart/graph selection helpers.

This module prepares prompts and structured chart briefs; it does not call image
providers, render charts, fetch remote assets, or persist files implicitly.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_CATALOG = ROOT / "contracts" / "graphs.v1.json"
PROMPT_CATALOG = ROOT / "contracts" / "visual-prompt.v1.json"
DATA_SHAPES = ("categories", "time-series", "parts-of-whole", "distribution", "relationship", "geospatial", "hierarchy", "flow", "cohort", "single-kpi")
AUDIENCES = ("general", "executive", "analyst", "operator")

def build_prompt(kind, intent, audience="general", palette="brand", aspect_ratio="16:9",
                 text=None, references=None, constraints=None, style="premium restrained"):
    if kind not in {"hero", "background", "illustration", "diagram", "logo", "social", "icon"}:
        raise ValueError("unsupported visual kind")
    if not isinstance(intent, str) or not 4 <= len(intent.strip()) <= 1200:
        raise ValueError("intent must contain 4 to 1200 characters")
    if aspect_ratio not in {"1:1", "4:5", "9:16", "16:9", "3:2", "21:9"}:
        raise ValueError("unsupported aspect ratio")
    required_text = [str(x)[:120] for x in (text or [])[:8]]
    ref_notes = [str(x)[:300] for x in (references or [])[:5]]
    limits = [str(x)[:300] for x in (constraints or [])[:12]]
    prompt = {
        "version": "1",
        "kind": kind,
        "intent": intent.strip(),
        "audience": audience[:160],
        "style": style[:200],
        "palette": palette[:80],
        "aspectRatio": aspect_ratio,
        "exactText": required_text,
        "referenceContext": ref_notes,
        "constraints": limits,
        "prompt": (
            f"Create a {style} {kind} for {audience}. Purpose: {intent.strip()}. "
            f"Palette: {palette}. Aspect ratio: {aspect_ratio}. "
            + ("Render this exact text, preserving spelling and hierarchy: " + " | ".join(required_text) + ". " if required_text else "Do not include text. ")
            + ("Use these references as context, not as material to copy: " + " | ".join(ref_notes) + ". " if ref_notes else "")
            + ("Constraints: " + " | ".join(limits) + ". " if limits else "")
            + "Prioritize clear composition, legibility, deliberate negative space, and a coherent focal point. "
            + "Avoid invented brand marks, gibberish lettering, watermarks, and decorative elements that compete with the purpose."
        ),
        "negativePrompt": [
            "watermarks", "unrequested text", "gibberish lettering", "unapproved logos",
            "visual clutter", "generic AI robot or brain clichés", "unreadable UI text"
        ],
        "workflow": [
            "Resolve the output medium and aspect ratio before generation.",
            "Separate exact required copy from descriptive visual direction.",
            "Use references to extract palette, composition and tone; do not imitate protected artwork.",
            "Generate multiple distinct compositions only when comparison is useful.",
            "Review crop, contrast, focal point, text accuracy and mobile safe areas.",
            "Store the chosen original plus prompt, model/provider, date, dimensions and rights metadata."
        ]
    }
    return prompt

def recommend_graph(data_shape, purpose="comparison", audience="general"):
    catalog = json.loads(GRAPH_CATALOG.read_text(encoding="utf-8"))
    if data_shape not in DATA_SHAPES:
        raise ValueError("unknown data shape; choose one of: " + ", ".join(DATA_SHAPES))
    if purpose not in catalog["purposes"]:
        raise ValueError("unknown graph purpose; choose one of: " + ", ".join(catalog["purposes"]))
    if audience not in AUDIENCES:
        raise ValueError("unknown audience; choose one of: " + ", ".join(AUDIENCES))
    ranked = []
    # Ties keep catalog order: the catalog lists the canonical form for a shape first.
    for order, (graph_id, graph) in enumerate(catalog["types"].items()):
        if data_shape not in graph["dataShapes"] or purpose not in graph["purposes"]:
            continue
        score = 0
        if purpose in graph["purposes"]: score += 3
        if data_shape in graph["dataShapes"]: score += 2
        if audience in graph.get("audiences", ["general"]): score += 1
        if score: ranked.append((score, order, graph_id, graph))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    recommendations = [
        {"id": gid, "label": g["label"], "when": g["when"], "avoid": g["avoid"],
         "encoding": g["encoding"], "accessibility": g["accessibility"]}
        for _, _, gid, g in ranked[:5]
    ]
    result = {
        "version": "1", "purpose": purpose, "dataShape": data_shape,
        "recommendations": recommendations,
        "rules": catalog["rules"]
    }
    # KPI trend path: one KPI tracked over time is the kpi "trend" variant,
    # not a bare line chart. Surface it alongside the generic ranking when
    # the request pairs a KPI or time series with a trend/performance goal.
    variant = catalog["types"].get("kpi", {}).get("variants", {}).get("trend")
    if variant and data_shape in {"time-series", "single-kpi"} and purpose in {"trend", "performance"}:
        result["variant"] = {"type": "kpi", "variant": "trend", **variant}
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description="Build visual prompts and recommend graph forms.")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prompt")
    p.add_argument("--kind", required=True, choices=("hero","background","illustration","diagram","logo","social","icon"))
    p.add_argument("--intent", required=True)
    p.add_argument("--audience", default="general")
    p.add_argument("--palette", default="brand")
    p.add_argument("--aspect-ratio", default="16:9")
    p.add_argument("--style", default="premium restrained")
    p.add_argument("--text", action="append", default=[])
    p.add_argument("--reference", action="append", default=[])
    p.add_argument("--constraint", action="append", default=[])
    g = sub.add_parser("graph")
    g.add_argument("--data-shape", required=True, choices=DATA_SHAPES)
    g.add_argument("--purpose", default="comparison", choices=("comparison","trend","composition","distribution","relationship","geography","process","hierarchy","performance"))
    g.add_argument("--audience", default="general", choices=AUDIENCES)
    args = parser.parse_args(argv)
    if args.command == "prompt":
        result = build_prompt(args.kind,args.intent,args.audience,args.palette,args.aspect_ratio,args.text,args.reference,args.constraint,args.style)
    else:
        result = recommend_graph(args.data_shape,args.purpose,args.audience)
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
