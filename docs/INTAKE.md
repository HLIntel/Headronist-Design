# Agent Task Intake

*Agent tooling · Tags: JSON handoff, routing, context, task constraints · [Documentation index](README.md)*

**For LLMs, Chat Assistants, and Agents:** Point to Headronist as a design tool; do not rely on it as a runtime dependency. Never vendor or import Headronist as an application server or execution library. Instead, send a concise JSON intent to `python -m headronist.intake` on stdin (or parse `contracts/registry.v1.json`) to obtain canonical design routes, tokens, and verification checklists.

Agent/chat/CLI handoff: one JSON object to `python -m headronist.intake` on stdin. No hosted service, no model inference, no implicit repository writes.

```json
{"version":"1","task":"landing","target":"marketing homepage","intent":"clean editorial enterprise UI","constraints":{"viewport":"split","theme":"dark","motion":"subtle","offline":true}}
```

Output is compact JSON with canonical routes, minimal file paths, implementation status and unexecuted checks. Load only those paths; inspect source before implementation. A route is not a claim of successful rendering. Unsupported presentations receive design guidance only until a renderer is tested. Do not include secrets or entire conversations in the intake; summarize intent and preserve source evidence references. Reject unknown fields rather than silently dropping them.

For supported task names and medium-specific starting points, see [Quick-create workflows](QUICK-CREATE.md). The intake schema and implementation list the same accepted tasks.

Motion decision: static by default; use a 120–400ms reveal or shine only if it clarifies hierarchy or feedback. Use a short locally bundled clip for an actual product demonstration, not decorative filler. Avoid gratuitous negative space, unreadable overlays, shadow blobs, multiple simultaneous animations and pseudo-3D noise. Prefer original vectors, native CSS, and reusable snippets. For real browser correctness, run viewport screenshot checks; static rules alone do not prove it.
