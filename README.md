# Headronist Design

A universal, agent-ready design system for interfaces, presentations, visual assets, documentation and data experiences. Headronist translates task intent into clear composition, reusable design primitives and verifiable output requirements without imposing a single visual style.

**Design principles:** hierarchy before decoration; brand-aware, platform-appropriate, accessible, responsive, and visually deliberate. Reuse small components and contracts rather than copying entire frameworks.

## Start here

- [Agent and model handoff](docs/INTAKE.md) · [Design workflows](docs/UNIVERSAL-WORKFLOWS.md)
- [Composition](docs/COMPOSITION.md) · [Cross-platform adaptation](docs/PLATFORM-ADAPTATION.md)
- [Browse design capabilities](contracts/catalog.v1.json) · [Canonical registry](contracts/registry.v1.json) · [Agent instructions](AGENTS.md)
- [Cloud agents and MCP integration](docs/CLOUD-MCP.md) · [Local discovery API](docs/SERVER.md)
- [Quality workflow and anti-drift checks](docs/QUALITY-FLOW.md) · [Expert review lenses](contracts/expertise.v1.json)
- [Design intelligence](docs/DESIGN-INTELLIGENCE.md) · [Visual inspection](docs/VISUAL-INSPECTION.md) · [Operational design engines](docs/DESIGN-ENGINES.md)
- [Depth and contrast](contracts/depth.v1.json) · [Reuse and compatibility](docs/REUSE.md)

```sh
python -m headronist.discover --query landing
python -m headronist.registry routes
python -m headronist.registry inspect landing
python -m headronist.registry check
python -m headronist.intake < task.json
python -m headronist.mcp_stdio
python -m headronist.quality_gate
python -m headronist.reference path/to/page.html --css path/to/site.css --output profile.json
python -m headronist.visual capture http://127.0.0.1:3000
python -m headronist.repair brief findings.json --output repair-brief.json
python -m headronist.memory list
```

## Design coverage

Websites, application interfaces, typography, navigation, visual assets, motion, dashboards, documents and presentations. The registry identifies implemented, partial, guidance-only and planned capabilities; not every medium has a working renderer.

## Architecture

- `contracts/`: task, token, composition, platform and quality contracts
- `foundations/`: palettes and design tokens
- `engines/`: layout, responsive composition, imagery and visual finish
- `components/`: reusable interface patterns
- `headronist/`: deterministic compiler, intake, registry, reference extraction, visual capture/review, repair handoff and local design memory
- `adapters/`: integration entry points for agents and tools
- `docs/`: workflows, compatibility and design research
- `tests/`: regression checks

## Boundaries

Headronist is independent of Headron. It supplies design intelligence and reusable presentation contracts; Headron may consume them optionally for design tasks. No vendor-specific design language is mandatory. Favor native capabilities and offline assets where practical.

This repository is a **partial import** of earlier v10–v13 work. Archived demos and some output renderers are not fully present. Inspect registry status before claiming an output format is supported. Machine routing and static lint are not substitutes for rendered visual testing. Playwright and vision-model review are optional integrations; they require explicit installation/configuration and are not silently invoked.
