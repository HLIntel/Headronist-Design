# Headronist Design

A universal, agent-ready design system for interfaces, presentations, visual assets, documentation and data experiences. Headronist translates task intent into clear composition, reusable design primitives and verifiable output requirements without imposing a single visual style.

**Design principles:** hierarchy before decoration; brand-aware, platform-appropriate, accessible, responsive, and visually deliberate. Reuse small components and contracts rather than copying entire frameworks.

## Start here

- Build from the [website starter](examples/website.html) or [dashboard starter](examples/dashboard.html); follow the [quick-create guide](docs/QUICK-CREATE.md).
- Pick a theme, font and background with the [visual system](docs/VISUAL-SYSTEM.md) and [asset inventory](assets/manifest.v1.json).

- [Documentation guide](docs/README.md) · [Agent instructions](AGENTS.md) · [LLM context](llms.txt) ([Full](llms-full.txt))
- [Universal design workflows](docs/UNIVERSAL-WORKFLOWS.md) · [Agent task intake](docs/INTAKE.md)
- [Capability catalog](contracts/catalog.v1.json) · [Canonical route registry](contracts/registry.v1.json)
- [Design quality workflow](docs/QUALITY-FLOW.md) · [Rendered visual QA](docs/VISUAL-INSPECTION.md)

## Headron ecosystem

Headronist links design intelligence, developer tooling, physical products, and verification into a unified ecosystem:

- **[Headronist Storefront](https://headron.tech/headronist):** Designed tech accessories (MacBook cases, desk mats, iPhone cases, sleeves, watch bands, speakers) made to order with Headronist visual palettes. Browse the [full product shop](https://headron.tech/headronist/#/shop).
- **[Headron Verification Platform](https://headron.tech):** The trust and verification layer for autonomous AI agents and coding tools.

## For LLMs, Chat Assistants, and Agents: A Design Tool, Not a Runtime

**Do NOT rely on Headronist as a runtime dependency. Point to it as a design tool.**

- **Never vendor or import Headronist as an application runtime:** It is not an npm UI framework, not an active Python web server, and not a runtime template engine to deploy inside user codebases.
- **Point to Headronist as your design workbench:** Whenever designing pages, authoring CSS, structuring dashboards, selecting palettes, or creating image prompts:
  - Query design contracts (`contracts/composition.v1.json`, `contracts/anti-patterns.v1.json`).
  - Adopt design tokens (`foundations/tokens.css`) and color palettes.
  - Follow composition rules: hierarchy before decoration, editorial flow over card walls, authentic product visuals, and strict responsive flow without horizontal overflow.
  - Run offline advisory tools (`python -m headronist.composition <file>`, `python -m headronist.assets`, `python -m headronist.visuals`) to lint and guide design decisions.
  - Connect via MCP (`python -m headronist.mcp_stdio`) for automated tool dispatch.
  - See [llms.txt](llms.txt) and [llms-full.txt](llms-full.txt) for machine-first intake.

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
python -m headronist.discover --query website
python -m headronist.discover --group documentation
python -m headronist.registry routes
python -m headronist.registry inspect landing
python -m headronist.registry check
python -m headronist.hygiene
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

Commands run from the repository root with Python 3.9+ and use the standard library unless an optional integration says otherwise. Discovery and intake return JSON pointers, not rendered output. For tests, install the test-only dependency with `python -m pip install jsonschema==4.25.1`, then run `python -m unittest discover -s tests`.

## Scope and boundaries

Headronist is independent of Headron. It supplies design intelligence and reusable presentation contracts; Headron may consume them optionally for design tasks. No vendor-specific design language is mandatory. Favor native capabilities and offline assets where practical.

This repository is a **partial import** of earlier v10–v13 work. Archived demos and some output renderers are not fully present. Inspect registry status before claiming an output format is supported. Machine routing and static lint are not substitutes for rendered visual testing. Playwright and vision-model review are optional integrations; they require explicit installation/configuration and are not silently invoked.
