"""Generate bounded, auditable repair briefs and compare reinspection findings.

This module does not modify source code or pretend to control an external coding agent.
It produces a structured handoff that an agent can apply, then checks reinspection data.
"""
import argparse
import json
from pathlib import Path

SEVERITY = {"critical": 0, "high": 1, "medium": 2, "low": 3, "note": 4}

def _findings(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("findings"), list):
        raise ValueError("Expected an object containing a findings array")
    result = {}
    for item in payload["findings"]:
        if not isinstance(item, dict):
            raise ValueError("Each finding must be an object")
        required = ("id", "dimension", "severity", "finding", "evidence", "recommendedAction")
        if any(not item.get(k) for k in required):
            raise ValueError("Finding missing required fields")
        if item["severity"] not in SEVERITY:
            raise ValueError("Invalid severity: " + str(item["severity"]))
        if item["id"] in result:
            raise ValueError("Duplicate finding id: " + item["id"])
        result[item["id"]] = item
    return result

def create_repair_brief(payload, max_findings=12):
    findings = _findings(payload)
    ordered = sorted(findings.values(), key=lambda x: (SEVERITY[x["severity"]], x["id"]))[:max_findings]
    return {
        "version": "1",
        "task": "repair-design-findings",
        "sourceVerification": payload.get("verification", "unknown"),
        "findings": ordered,
        "agentInstructions": [
            "Inspect the cited route, viewport and evidence before changing code.",
            "Fix the underlying layout or interaction issue rather than hiding the symptom.",
            "Preserve brand constraints, semantics, keyboard access and reduced-motion behavior.",
            "Make the smallest coherent change and avoid unrelated redesign.",
            "Return changed files, rationale and any finding that cannot be safely resolved."
        ],
        "reinspectionRequired": [x["id"] for x in ordered],
        "execution": "handoff-only; no files modified and no coding agent invoked"
    }

def compare_reinspection(before, after):
    old, new = _findings(before), _findings(after)
    resolved = sorted(set(old) - set(new))
    remaining = sorted(set(old) & set(new))
    new_issues = sorted(set(new) - set(old))
    return {
        "version": "1", "resolved": resolved, "remaining": remaining,
        "newFindings": new_issues,
        "resolvedCount": len(resolved), "remainingCount": len(remaining),
        "newCount": len(new_issues),
        "verification": after.get("verification", "unknown"),
        "note": "Finding disappearance is not proof of human approval; compare the rendered evidence."
    }

def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    brief = sub.add_parser("brief"); brief.add_argument("findings"); brief.add_argument("--output")
    compare = sub.add_parser("compare"); compare.add_argument("before"); compare.add_argument("after")
    args = parser.parse_args(argv)
    if args.command == "brief":
        result = create_repair_brief(json.loads(Path(args.findings).read_text(encoding="utf-8")))
        output = json.dumps(result, indent=2, sort_keys=True)
        if args.output: Path(args.output).write_text(output + "\n", encoding="utf-8")
        else: print(output)
    else:
        result = compare_reinspection(
            json.loads(Path(args.before).read_text(encoding="utf-8")),
            json.loads(Path(args.after).read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
