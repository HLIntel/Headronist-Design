# Headronist agent contract

Source of truth: executable code and tests > `contracts/registry.v1.json` > schemas > this file > historical discussion. Do not infer functionality from planned routes.

1. Read this file and `contracts/registry.v1.json` only. Run `python -m headronist.registry routes` or `inspect <route>` to obtain task-specific paths. Load only returned files.
2. Preserve v10/v11/v12/v13 compatibility and public identifiers; follow `docs/COMPATIBILITY.md` when changing behavior. Never silently rename tokens or palette IDs.
3. Prefer immutable inputs, deterministic compilation, semantic symbols, native browser APIs, offline assets, and no new runtime dependencies.
4. Treat generated files as disposable outputs; never edit canonical inputs through generation. No hidden writes, external fetches, secrets, or unreviewed destructive changes.
5. Run `python -m headronist.registry check` and relevant tests. For web, test narrow screens, 200% zoom, long text, sticky header/footer, reduced motion and keyboard focus. Report what was actually tested.
6. Do not copy entire third-party libraries. Prefer native Headronist primitives and explicit versioned adapters.
