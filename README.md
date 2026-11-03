# Headronist Design

A universal, agent-ready design system for interfaces, presentations, visual assets, documentation and data experiences. Headronist translates task intent into clear composition, reusable design primitives and verifiable output requirements without imposing a single visual style.

**Design principles:** hierarchy before decoration; brand-aware, platform-appropriate, accessible, responsive, and visually deliberate. Reuse small components and contracts rather than copying entire frameworks.

## Start here

- [Documentation guide](docs/README.md) · [Agent instructions](AGENTS.md)
- [Universal design workflows](docs/UNIVERSAL-WORKFLOWS.md) · [Agent task intake](docs/INTAKE.md)
- [Capability catalog](contracts/catalog.v1.json) · [Canonical route registry](contracts/registry.v1.json)
- [Design quality workflow](docs/QUALITY-FLOW.md) · [Rendered visual QA](docs/VISUAL-INSPECTION.md)

## Visual and data workflows

- [Context-aware asset sourcing](docs/ASSET-SOURCING.md)
- [Visual generation, asset lifecycle and chart intelligence](docs/VISUAL-GENERATION-AND-GRAPHS.md)
- [Design intelligence and reference analysis](docs/DESIGN-INTELLIGENCE.md)
- [Composition and platform adaptation](docs/COMPOSITION.md) · [Cross-platform design](docs/PLATFORM-ADAPTATION.md)

## Agent and developer workflows

- [Agent and MCP integration](docs/CLOUD-MCP.md) · [Discovery and local API](docs/SERVER.md)
- [Operational design engines](docs/DESIGN-ENGINES.md) · [Reuse and compatibility](docs/REUSE.md)
- [Integration guide](docs/INTEGRATION.md) · [Compatibility contract](docs/COMPATIBILITY.md)

## Common commands

```sh
python -m headronist.discover --query landing
python -m headronist.registry routes
python -m headronist.registry inspect landing
python -m headronist.registry check
python -m headronist.intake < task.json
python -m headronist.mcp_stdio
python -m headronist.quality_gate
python -m headronist.assets recommend --intent 'AI infrastructure trust network'
python -m headronist.visuals prompt --kind background --intent 'AI trust network hero'
python -m headronist.visuals graph --data-shape time-series --purpose trend
```

## Project structure

- `contracts/`: versioned schemas, capability metadata, route definitions and quality rules
- `foundations/`: palettes and design tokens
- `engines/`: layout, responsive composition, imagery and visual finish
- `components/`: reusable interface patterns
- `headronist/`: deterministic compiler, intake, registry, reference extraction, visual capture/review, repair handoff, local design memory, asset recommendations and visual prompt/graph guidance
- `assets/`: local reusable visual assets
- `adapters/`: integration entry points for agents and tools
- `docs/`: task-oriented guides and design research
- `tests/`: regression checks

## Scope and boundaries

Headronist is independent of Headron. It supplies design intelligence and reusable presentation contracts; Headron may consume them optionally for design tasks. No vendor-specific design language is mandatory. Favor native capabilities and offline assets where practical.

This repository is a **partial import** of earlier v10–v13 work. Archived demos and some output renderers are not fully present. Inspect registry status before claiming an output format is supported. Machine routing and static lint are not substitutes for rendered visual testing. Playwright and vision-model review are optional integrations; they require explicit installation/configuration and are not silently invoked.
