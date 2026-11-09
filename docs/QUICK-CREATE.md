# Quick-create workflows

Use this guide to turn a short brief into a reusable design direction. Intake returns pointers and unexecuted checks; it does not create an artifact. Use the actual authoring tool for the target medium and verify its exported output.

## Dashboard starter

Open [the local dashboard example](../examples/dashboard.html). It includes sample metrics, an accessible data table, labeled bars and an optional working status filter. Copy the HTML and adapt the values and data connection to your product; the example does not load live data. Load `foundations/tokens.css`, `components/primitives/dashboard.css`, and optionally `components/primitives/dashboard-filter.js`. Without JavaScript, the complete table remains visible. Select a theme on `<html>` as described in the [visual system guide](VISUAL-SYSTEM.md).

## Start with a small brief

Record the audience, decision or action, essential content/data, destination format, brand references, constraints and evidence. If content or a data source is missing, mark it as missing rather than inventing it. Keep source data, editable masters and exports separate. Choose colors and type from the existing brand or [visual system](VISUAL-SYSTEM.md); preserve platform conventions and accessibility.

```sh
printf '%s' '{"version":"1","task":"dashboard_quick_create","target":"operations dashboard","intent":"show service health and next actions","constraints":{"theme":"dark","viewport":"desktop"}}' | python -m headronist.intake
```

Replace `task` with one of the names below. Read the returned paths, inspect the actual project, then build in its native tools. The checks in the response are a review plan, not a pass result.

| Task | Gather first | Compose and verify |
|---|---|---|
| `dashboard_quick_create`, `dashboard` | Decisions, metrics, definitions, freshness, sources and user actions | Start with a compact header and scope/time controls, a few decision-relevant metrics, a chart and a detail table. Include units, baselines, empty/loading/error states and a text/table alternative. Test keyboard, narrow screens and realistic long labels. |
| `slides`, `presentation` | Audience, message, narrative, duration, source material and output format | Outline one claim per slide, use editable text and graphics, label evidence, and establish hierarchy before decoration. Inspect every exported slide for crop, legibility and reading order. |
| `pdf` | Page size, audience, content, accessibility and print needs | Structure headings and page breaks, keep links and text selectable where possible, and inspect the exported PDF for clipping, reading order, contrast and print margins. |
| `document`, `docs` | Reader, objective, source facts, required format and length | Lead with the decision or answer; use meaningful headings, short paragraphs and useful tables. Check links, heading structure and export. |
| `diagram` | Entities, relationships, direction, boundaries and source of truth | Select a flow, hierarchy, sequence or network to match the relationship. Label arrows, avoid false causal claims, and supply a text description. |
| `graph`, `chart` | Data, units, time range, question, baseline and uncertainty | Use `python -m headronist.visuals graph --data-shape time-series --purpose trend` as a starting example; change inputs to fit the data. Check encoding, scale, labels, missing values and a text or table alternative. Recommendations do not render a chart. |
| `logo` | Name, purpose, audience, context, existing marks and restrictions | Explore original simple forms; keep a vector master when possible. Check clear space and small sizes in monochrome and on light/dark surfaces. Review rights before release; a prompt is not a finished identity. |
| `website`, `web` | Audience, content, key tasks, destination and supported devices | Start with semantic navigation and content hierarchy; use reusable tokens and components. Verify keyboard, focus, states, responsive layout and real links. |
| `landing_page`, `landing` | Offer, audience, proof, primary action and destination | Lead with the proposition, show real evidence and make the action clear. Use authentic visuals and tested contrast; inspect mobile and desktop crops. |
| `visual_asset` | Intended use, dimensions, brand and source rights | Choose a medium, keep text separate where possible, and preserve provenance, source and optimized derivatives. |

For all visual work, use the [asset inventory](../assets/manifest.v1.json) as candidates, not production approval. Review rights and actual image crops. Use flat, dense product surfaces; reserve glass and decorative effects for appropriate showcase contexts. Never infer supported file generation from the existence of a workflow. See [visual inspection](VISUAL-INSPECTION.md) and [quality flow](QUALITY-FLOW.md) for evidence.

## Website starter

Open [the website example](../examples/website.html). It uses semantic, script-free navigation and an adaptive two-column hero that stacks on phones; the three-column section also stacks below tablet width. Load `foundations/tokens.css`, `engines/typography/type.css` and `components/primitives/web.css`, then replace the sample content and links. Columns respond to available width, not device model; check both tablet orientations, long translations, 200% zoom and touch/keyboard use. Provide real imagery and content before publishing.

Serve static files from the repository root for local preview, for example `python -m http.server 8766 --bind 127.0.0.1`, and stop the server when finished. This preview server serves files from its working directory; it is not the read-only discovery API or a production server. For deployment, choose hosting appropriate to the site and its security requirements. See [server boundaries](SERVER.md).
