# Documentation Guide

Headronist documentation is organized by the work an agent or designer is trying to complete. Start with the task area, then follow the linked workflow. The [repository README](../README.md) is the project overview; [AGENTS.md](../AGENTS.md) defines agent operating rules.

## Start here

| Need | Read first | Also useful |
|---|---|---|
| Understand the system and choose a workflow | [Universal Design Workflows](UNIVERSAL-WORKFLOWS.md) | [Design Intake](INTAKE.md), [Reuse and Compatibility](REUSE.md) |
| Find a capability or command | [Discovery and Local API](SERVER.md) | [Capability Catalog](../contracts/catalog.v1.json), [Canonical Registry](../contracts/registry.v1.json) |
| Give an agent a task | [Design Intake](INTAKE.md) | [Agent and MCP Integration](CLOUD-MCP.md), [Agent Contract](../AGENTS.md) |

## Design and implementation

| Topic | Guide | Search tags |
|---|---|---|
| Composition and hierarchy | [Composition-First Design](COMPOSITION.md) | composition, hierarchy, layout, typography |
| Brand and reference analysis | [Design Intelligence](DESIGN-INTELLIGENCE.md) | brand, references, tokens, evidence |
| Platform adaptation | [Cross-Platform Design](PLATFORM-ADAPTATION.md) | responsive, mobile, tablet, desktop |
| Hero and graphic reuse | [Reusable Hero and Graphic Primitives](HERO-REUSE.md) | hero, graphics, CSS, reuse |
| Pattern research | [Pattern Research](PATTERN-REFERENCE.md) | patterns, inspiration, implementation |
| Integration | [Integration Guide](INTEGRATION.md) | CSS, consumers, migration |

## Visual assets and data graphics

| Topic | Guide | Search tags |
|---|---|---|
| Find or select visual sources | [Context-Aware Asset Sourcing](ASSET-SOURCING.md) | images, SVG, photography, licensing |
| Build image-model prompts and manage assets | [Visual Generation and Asset Lifecycle](VISUAL-GENERATION-AND-GRAPHS.md) | image generation, prompts, brand context, provenance, storage |
| Select charts and graph forms | [Chart and Graph Intelligence](VISUAL-GENERATION-AND-GRAPHS.md#chart-and-graph-intelligence) | charts, graphs, trends, distribution, network, Sankey |
| Inspect rendered interfaces | [Rendered Visual QA](VISUAL-INSPECTION.md) | screenshots, Playwright, responsive, evidence |
| Reuse design assets and tokens | [Reuse and Compatibility](REUSE.md) | reuse, tokens, anti-drift |

## Quality, operations and compatibility

| Topic | Guide | Search tags |
|---|---|---|
| Review and release quality | [Design Quality Workflow](QUALITY-FLOW.md) | quality, accessibility, contrast, review |
| Run local design engines | [Operational Design Engines](DESIGN-ENGINES.md) | reference extraction, capture, repair, memory |
| Connect agents and MCP clients | [Agent and MCP Integration](CLOUD-MCP.md) | MCP, stdio, cloud, JSON-RPC |
| Run local discovery | [Discovery and Local API](SERVER.md) | CLI, HTTP, routes, metadata |
| Preserve behavior across versions | [Compatibility Contract](COMPATIBILITY.md) | compatibility, migration, versioning |
| Research external design patterns | [Pattern Research](PATTERN-REFERENCE.md) | research, design systems, inspiration |
| Review open-source inspirations | [Open-Source Design Research](OPEN_SOURCE_RESEARCH.md) | research, libraries, references |

## Navigation rules

- Use [the canonical registry](../contracts/registry.v1.json) for route paths and implementation status.
- Use [the capability catalog](../contracts/catalog.v1.json) for searchable labels, groups, priorities, tags and output types.
- Use this guide for human navigation. It does not replace executable contracts.
- Prefer links to focused task guides; avoid loading every document into an agent context.
- A documented workflow is not proof that a renderer, integration or automated check is implemented.
