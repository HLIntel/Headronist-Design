# Design Reuse and Anti-Drift

*Engineering standards · Tags: reuse, tokens, compatibility, stable identifiers · [Documentation index](README.md)*

The machine contract is `contracts/registry.v1.json`; this file explains consumption, not a second registry.

## Agent / chat / IDE / CLI

Read `AGENTS.md`, then use `python -m headronist.registry inspect <route>` or parse the same JSON without a shell. Read only the returned paths. `routes` lists supported entry points and implementation status. Do not load entire docs or all templates by default.

## Symbols and pointers

Use stable semantic prefixes `hd.color`, `hd.space`, `hd.radius`, `hd.type`, `hd.surface`, `hd.layout`, `hd.state`. Resolve a symbol through the versioned token contract, never through a free-text color name. Pointers must be repository-relative paths, not URLs, and must pass `check`.

## Change rules

Preserve v10–v13 design behavior; change an existing public contract only with a major version and migration. Derive outputs from immutable source specs, write to a separate output directory, and fingerprint the input set. Do not store duplicate route lists in markdown. Never fetch runtime assets, load unpinned remote scripts, or mutate input palettes during rendering.

## Integration

Pin a commit or release in each consumer. Import the needed CSS or renderer directly. Authentication remains a host-application responsibility. GitHub currently contains only part of the archived v13 package; a planned feature is not a working renderer.
