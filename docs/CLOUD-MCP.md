# Agent and MCP Integration

*Agent tooling · Tags: MCP, stdio, cloud adapter, JSON-RPC, integrations · [Documentation index](README.md)*

Headronist's design contracts are client-neutral. The same dispatcher is available through stdio and a stateless HTTP JSON-RPC adapter. The cloud adapter is a WSGI application, not a deployed service.

## Local MCP (stdio)

```sh
python -m headronist.mcp_stdio
```

Configure an MCP-capable agent to launch this command from the repository root. Tools available:
- `design_discover`: Search compact Headronist design routes and components.
- `design_inspect`: Inspect one design route and its required contract/source paths.
- `design_intake`: Route a structured design task without executing it.
- `design_recommend_assets`: Recommend local and curated visual assets for a given intent.
- `design_visual_prompt`: Build a structured prompt brief for image generation or visual design.
- `design_graph_guidance`: Recommend chart and data graphic encodings based on data shape and purpose.
- `design_composition_check`: Advisory HTML composition analysis against anti-patterns (card walls, badge clutter, run-on headings).

## Cloud deployment

`headronist.cloud:application` is a WSGI callable that can run under a compatible managed Python server. It requires `HEADRONIST_API_TOKEN` (at least 24 characters), accepts authenticated POST requests at `/mcp`, limits bodies to 64KiB, and serves `/health`. Deploy only behind HTTPS, gateway rate limits, monitoring and secret management. This module does not deploy itself.

The HTTP adapter currently implements **JSON-RPC over HTTP**, not a complete MCP Streamable HTTP transport. It does not implement all transport negotiation, session handling, Accept headers or streaming behavior. Do not advertise it as certified MCP HTTP compatibility until protocol conformance tests pass. MCP stdio is the initial transport target.

## Chat and cloud client integration

- ChatGPT and ChatGPT Work: potential integration through a supported remote MCP app/connector surface where available; account authorization, deployment, and compatibility validation are still required.
- Gemini and Google agent ecosystems: use a supported tool or MCP bridge where available; no claim of direct Gemini Work integration.
- Claude, IDEs and other agents: stdio where supported, or an authenticated gateway once remote MCP transport conformance is implemented.
- Generic API clients: can call authenticated HTTP JSON-RPC today once deployed, but this is not automatically a native chat plugin.

Never upload full chat transcripts, proprietary design assets or secrets as task intake. Send concise scoped requests and source references. Tool output describes routing and metadata, not rendered artifacts or verified design quality.

## Integration readiness checks

1. MCP Streamable HTTP transport conformance, including header validation and protocol negotiation.
2. OAuth or trusted gateway auth where required by the consuming platform.
3. Per-tenant limits, request tracing, cache policy and privacy controls.
4. Integration tests against actual remote clients.
5. Artifact rendering and visual verification as separate capabilities.

Reference: https://modelcontextprotocol.io/specification
