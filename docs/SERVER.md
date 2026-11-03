# Discovery and Local API

*Developer tooling · Tags: CLI, route discovery, local server, metadata · [Documentation index](README.md)*

The route catalog is metadata, not a second source of truth. The registry owns paths and statuses; the catalog adds labels, groups, priorities, tags, and intended outputs for search and navigation.

## CLI

```sh
python -m headronist.discover --query typography
python -m headronist.discover --group experience --limit 8
python -m headronist.registry inspect landing
```

## Optional local server

```sh
python -m headronist.server --port 8765
curl http://127.0.0.1:8765/health
curl 'http://127.0.0.1:8765/v1/routes?q=web'
curl 'http://127.0.0.1:8765/v1/route?id=landing'
```

The server binds only to 127.0.0.1 and exposes read-only JSON. It has no authentication and must not be exposed to public networks, reverse proxies, or tunnels. No write API, asset hosting, inference, user sessions, database, or public cloud deployment is provided. For remote hosting, deploy a separately secured API gateway with authentication, quotas, request limits and monitoring; do not simply change the bind address. Static files can be hosted by a conventional static-site provider without running the local API.

Route discovery returns compact metadata. For file paths and source status use route inspection. Server output is not proof of artifact generation or quality verification.
