# Routing entry point

Canonical machine-readable registry: `contracts/registry.v1.json`. Do not duplicate route tables here.

Commands (offline, read-only):

- `python -m headronist.registry routes`
- `python -m headronist.registry inspect web`
- `python -m headronist.registry inspect palette`
- `python -m headronist.registry check`
- `python -m headronist.registry fingerprint`

For models without shell access, parse the registry JSON directly. Only open the paths returned by the selected route. Missing and planned renderers must be reported as such rather than fabricated.
