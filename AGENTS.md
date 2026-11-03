# Headronist agent contract

Source of truth: executable code and tests > `contracts/registry.v1.json` > schemas > this file > historical discussion. Do not infer functionality from planned routes.

1. Read this file and `contracts/registry.v1.json` only. Run `python -m headronist.registry routes` or `inspect <route>` to obtain task-specific paths. Load only returned files.
2. Preserve v10/v11/v12/v13 compatibility and public identifiers; follow `docs/COMPATIBILITY.md` when changing behavior. Never silently rename tokens or palette IDs.
3. Prefer immutable inputs, deterministic compilation, semantic symbols, native browser APIs, offline assets, and no new runtime dependencies.
4. Treat generated files as disposable outputs; never edit canonical inputs through generation. No hidden writes, external fetches, secrets, or unreviewed destructive changes.
5. Run `python -m headronist.registry check` and relevant tests. For web, test narrow screens, 200% zoom, long text, sticky header/footer, reduced motion and keyboard focus. Report what was actually tested.
6. Do not copy entire third-party libraries. Prefer native Headronist primitives and explicit versioned adapters.

7. Visual reference gate: read `contracts/quality.v1.json` for landing and image-related work. Never present generated UI imagery with illegible text as a quality benchmark. Use rendered semantic HTML/CSS and inspect screenshots before claiming visual correctness. Preserve fallback navigation when scripts or manifests fail.

8. For model/chat handoffs, accept the bounded JSON in `contracts/intake.v1.schema.json`; run `python -m headronist.intake` and load only returned paths. Route selection is not rendering or verification. Keep input compact; refuse unknown fields and unsupported claims.
9. Visual finish is opt-in: static by default; no shadow blobs, redundant whitespace, or distracting parallax. Prefer local CSS/SVG, reduced-motion fallbacks, and real product clips only when demonstrably useful. See `contracts/motion.v1.json`.

10. Composition precedes effects. For landing/web/docs/dashboard work, load `contracts/composition.v1.json`. Prefer intentional typography, direct content, and authentic product visuals over card walls, redundant badges, emoji, and ornamental gradients. Run `python -m headronist.composition <html-file>` as advisory lint; do not report it as screenshot or accessibility verification.

11. Adapt design to medium and platform using `contracts/platforms.v1.json` and `docs/UNIVERSAL-WORKFLOWS.md`. Borrow Google Material adaptive patterns, Apple platform interaction conventions, and GitHub Primer's developer-focused information clarity selectively. Never force a vendor skin, duplicate a third-party library, or claim unsupported renderers are implemented.

12. For every design task apply the review lenses in `contracts/expertise.v1.json`: design direction, senior web engineering, creative UI engineering, systems architecture, and quality review. These are checklists, not identity claims. Use `contracts/depth.v1.json` for contrast and depth choices. Run `python -m headronist.quality_gate` before release; never conceal registry/catalog drift or missing paths. Follow `docs/QUALITY-FLOW.md`. Static lint does not prove visual correctness.
13. For reference-driven work, read contracts/reference-profile.v1.json and docs/DESIGN-INTELLIGENCE.md. Separate observed, inferred and user-specified design properties. Select contextual layouts using contracts/composition-library.v1.json; use contracts/anti-patterns.v1.json as advisory review signals, not automatic rejection rules.
14. For browser-visible work, follow contracts/visual-inspection.v1.json and docs/VISUAL-INSPECTION.md. Capture actual rendered output when browser tooling is available, record exact viewport/evidence for findings, and reinspect after changes. Never imply that a contract, screenshot request or static test means a browser inspection was executed.
15. Operational design engines: use headronist.reference for supplied HTML/CSS profiles; network retrieval requires explicit --allow-network. Use headronist.visual capture only when the target app is running and Playwright is installed. Vision review is opt-in and may transmit screenshots to the configured provider; disclose this before use when content is sensitive. Use headronist.repair to create a bounded, evidence-linked agent handoff and compare reinspection findings; it does not edit source. Use headronist.memory for explicit local profile versioning; its JSON store is not encrypted. Never imply these engines ran unless their commands actually completed.
