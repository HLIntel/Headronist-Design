# Headronist Design

A universal, agent-ready design system for interfaces, presentations, visual assets, documentation and data experiences. Headronist translates task intent into clear composition, reusable design primitives and verifiable output requirements without imposing a single visual style.

**Design principles:** hierarchy before decoration; brand-aware, platform-appropriate, accessible, responsive, and visually deliberate. Reuse small components and contracts rather than copying entire frameworks.

## Start here

- [Agent and model handoff](docs/INTAKE.md) · [Design workflows](docs/UNIVERSAL-WORKFLOWS.md)
- [Composition](docs/COMPOSITION.md) · [Cross-platform adaptation](docs/PLATFORM-ADAPTATION.md)
- [Browse design capabilities](contracts/catalog.v1.json) · [Canonical registry](contracts/registry.v1.json) · [Agent instructions](AGENTS.md)
- [Local discovery API and hosting guidance](docs/SERVER.md)
- [Quality requirements](contracts/quality.v1.json) · [Reuse and compatibility](docs/REUSE.md)

```sh
python -m headronist.discover --query landing
python -m headronist.registry routes
python -m headronist.registry inspect landing
python -m headronist.registry check
python -m headronist.intake < task.json
```

## Design coverage

Websites, application interfaces, typography, navigation, visual assets, motion, dashboards, documents and presentations. The registry identifies implemented, partial, guidance-only and planned capabilities; not every medium has a working renderer.

## Architecture

- `contracts/`: task, token, composition, platform and quality contracts
- `foundations/`: palettes and design tokens
- `engines/`: layout, responsive composition, imagery and visual finish
- `components/`: reusable interface patterns
- `headronist/`: deterministic compiler, intake, registry and advisory analysis
- `adapters/`: integration entry points for agents and tools
- `docs/`: workflows, compatibility and design research
- `tests/`: regression checks

## Boundaries

Headronist is independent of Headron. It supplies design intelligence and reusable presentation contracts; Headron may consume them optionally for design tasks. No vendor-specific design language is mandatory. Favor native capabilities and offline assets where practical.

This repository is a **partial import** of earlier v10–v13 work. Archived demos and some output renderers are not fully present. Inspect registry status before claiming an output format is supported. Machine routing and static lint are not substitutes for rendered visual testing.
