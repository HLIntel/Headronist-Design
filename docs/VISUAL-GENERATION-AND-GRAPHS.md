# Visual Generation, Asset Lifecycle and Graph Intelligence

*Visual assets and data · Tags: image prompts, asset storage, charts, graphs, provenance · [Documentation index](README.md)*

Headronist treats visual generation as a pipeline, not a one-line prompt. The goal is repeatable creative direction, safe asset handling, and the right visual encoding for the information.

## Prompt preparation

Build a structured prompt brief before sending a request to an image model:

```sh
python -m headronist.visuals prompt \
  --kind background \
  --intent "Abstract AI infrastructure trust network for a developer platform hero" \
  --audience "AI developers and technical buyers" \
  --palette "deep navy, graphite, muted blue and silver" \
  --aspect-ratio 16:9 \
  --style "premium, restrained, geometric, cinematic" \
  --constraint "No text, logos, robots or brains" \
  --constraint "Keep the center dark and open for responsive hero copy"
```

The command returns a JSON brief and a provider-neutral prompt. It does not call an image provider. Keep exact copy in `--text` arguments rather than mixing copy with art direction. For images containing text, verify every character after generation; prefer HTML typography for interface and hero copy.

### Context to pass to the prompt builder

- **Purpose:** what the image must communicate and where it appears.
- **Audience:** who will see it and what they need to understand.
- **Brand context:** palette, typography mood, contrast, existing design profile and reference URLs or notes.
- **Composition:** focal point, negative space, crop tolerance, safe area and subject placement.
- **Output:** kind, aspect ratio, target dimensions, transparency and preferred format.
- **Copy:** exact strings, hierarchy and placement, or explicitly no text.
- **Constraints:** forbidden motifs, licensing, accessibility and responsive behavior.

Separate observed brand properties from inferred properties and user-specified direction. Do not ask an image model to render small UI labels, chart values or critical text when semantic HTML or a chart renderer is more reliable.

## Asset lifecycle and storage

Use a predictable lifecycle:

1. **Brief** — store the structured prompt JSON and intended use.
2. **Generate** — create candidate outputs outside the production asset directory.
3. **Review** — inspect content, crop, contrast, text accuracy, artifacting, brand fit and mobile behavior.
4. **Select** — retain the approved original and useful optimized derivatives.
5. **Record** — write a manifest beside the asset.
6. **Integrate** — reference local assets from components/CSS; avoid remote hotlinks.
7. **Verify** — check dimensions, format, file size, alt text, responsive crop and actual rendered appearance.
8. **Retire** — mark old versions as superseded; do not silently overwrite approved source files.

Recommended layout:

```text
assets/
  backgrounds/
  illustrations/
  diagrams/
  icons/
  charts/
  generated/
  manifest.v1.json
  prompts/
    <asset-id>.json
```

Use stable kebab-case IDs. Keep an editable or highest-quality source where available; create WebP/AVIF derivatives for raster web delivery and retain SVG for clean vector work. Do not convert vector masters to raster unless required. Avoid committing duplicate large exports. Set practical size budgets per target and document intentional exceptions.

### Asset manifest

Each entry should include:
- `id`, `path`, `kind`, `purpose`, `status` (`candidate`, `approved`, `deprecated`)
- `sourceType` (`original`, `generated`, `licensed`, `user-provided`)
- `promptPath`, `provider`, `model`, `createdAt` when applicable
- `creator`, `sourceUrl`, `license`, `attribution`, `retrievedAt` for external material
- `width`, `height`, `format`, `bytes`, `alt`, `focalPoint`, `safeArea`
- `variants` for responsive or optimized files and `supersedes` for version history

Never place API keys, private URLs, personal information or credentials in prompts or manifests. Treat a generated image as original only when provider terms and inputs permit that conclusion. Keep provenance even for AI-generated material.

## Responsive image integration

- Prefer CSS background images only for decorative visuals. Use semantic `img` elements for meaningful content.
- Set `background-size: cover` only when crop tolerance is high; otherwise use `contain` or art-directed mobile variants.
- Record focal point and safe area. Test 320px, 375px, tablet and desktop widths.
- Keep text as HTML. Add a dark text scrim where necessary instead of baking copy into the image.
- Provide meaningful alt text for informative images and empty alt text for decorative imagery.
- Use `prefers-reduced-motion` for animated treatments and avoid autoplay-heavy backgrounds.

## Graph and chart intelligence

Get a chart recommendation from the graph catalog:

```sh
python -m headronist.visuals graph --data-shape time-series --purpose trend --audience executive
python -m headronist.visuals graph --data-shape relationship --purpose relationship --audience analyst
python -m headronist.visuals graph --data-shape flow --purpose process --audience operator
```

Supported families include bars, lines, areas, stacked bars, pie/donut, scatter, histogram, box plots, heatmaps, Sankey, network graphs, treemaps, funnels, maps, small multiples and KPI indicators.

### Select by analytical question

| Question | Strong starting point |
|---|---|
| Compare categories | Bar |
| Show change over time | Line; area for cumulative magnitude |
| Show parts of a whole | Stacked bar; donut only for a few simple parts |
| Understand a distribution | Histogram or box plot |
| Explore two numeric variables | Scatter |
| Find patterns in a matrix | Heatmap |
| Explain weighted movement | Sankey |
| Show connected entities | Network graph |
| Show nested composition | Treemap |
| Explain sequential conversion | Funnel |
| Compare geographic rates | Choropleth; use symbols for counts |
| Compare many repeated trends | Small multiples |
| Surface one metric with context | KPI indicator |

Do not select a chart because it looks impressive. Validate data shape, units, missing values, sample size, normalization, uncertainty and audience. Avoid 3D, decorative dual axes, misleading truncated magnitude scales, and color-only distinctions. Complex charts need a table or text summary. Interactive charts should expose values, keyboard access and accessible labels.

## Current Headronist visual assets

- `assets/backgrounds/headronist-trust-network.svg` — precise, geometric network field.
- `assets/backgrounds/headronist-flow-network.svg` — flowing ribbons and connected nodes, inspired by the second visual direction.

Both are local SVGs with no external runtime requests. The generated raster concept can be retained as a source candidate outside production until its binary is committed and its final crop/quality is reviewed.
