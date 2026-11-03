# Headronist Design

Native, offline-first, machine-readable design foundations for agents, chat models, IDEs and applications.

## Start here

- Human or agent: [AGENTS.md](AGENTS.md)
- Canonical routes, semantic symbols and status: [contracts/registry.v1.json](contracts/registry.v1.json)
- Typed tokens: [contracts/tokens.v1.schema.json](contracts/tokens.v1.schema.json)
- Reuse and anti-drift: [docs/REUSE.md](docs/REUSE.md)

```sh
python -m headronist.registry routes
python -m headronist.registry inspect web
python -m headronist.registry check
python -m headronist.registry fingerprint
python -m unittest discover -s tests -p 'test_registry.py'
```

All commands are offline. Registry inspection is read-only and returns compact JSON. There is one canonical route map; Markdown documents link to it rather than duplicating it.

## Modules

- `foundations/`: palettes and typed tokens
- `engines/`: composition and anti-breakage
- `components/`: behavioral primitives and authentication guidance
- `renderers/`: intended target-specific output adapters
- `contracts/`: machine-readable schema and route graph
- `adapters/`: agent integrations
- `headronist/`: standard-library compiler and registry CLI
- `tests/`: regression checks

## Implementation boundary

This repository is currently a **partial source import** of the original v10 through v13 design package. Do not assume the archived web demos, Excel/PPTX renderers or all palette definitions are present here. The registry distinguishes implemented, partial, guidance and planned routes. No third-party hosted API, payment card, sign-up or network fetch is required by the registry and compiler.

Headronist owns presentation contracts and design mechanisms; Headron owns governance, verification and product behavior.
