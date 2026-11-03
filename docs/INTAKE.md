# Agent Task Intake

*Agent tooling · Tags: JSON handoff, routing, context, task constraints · [Documentation index](README.md)*
Agent/chat/CLI handoff: one JSON object to `python -m headronist.intake` on stdin. No hosted service, no model inference, no implicit repository writes.

```json
{"version":"1","task":"landing","target":"marketing homepage","intent":"clean editorial enterprise UI","constraints":{"viewport":"split","theme":"dark","motion":"subtle","offline":true}}
```

Output is compact JSON with canonical routes, minimal file paths, implementation status and unexecuted checks. Load only those paths; inspect source before implementation. A route is not a claim of successful rendering. Unsupported presentations receive design guidance only until a renderer is tested. Do not include secrets or entire conversations in the intake; summarize intent and preserve source evidence references. Reject unknown fields rather than silently dropping them.

Motion decision: static by default; use a 120–400ms reveal or shine only if it clarifies hierarchy or feedback. Use a short locally bundled clip for an actual product demonstration, not decorative filler. Avoid gratuitous negative space, unreadable overlays, shadow blobs, multiple simultaneous animations and pseudo-3D noise. Prefer original vectors, native CSS, and reusable snippets. For real browser correctness, run viewport screenshot checks; static rules alone do not prove it.
