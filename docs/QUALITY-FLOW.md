# Expert design workflow and enforcement

Headronist uses five expert review lenses, not simulated credentials: design director, senior web engineer, creative UI engineer, design-system architect, and quality reviewer. Their concerns are declared in `contracts/expertise.v1.json`.

## Mandatory sequence

1. Discover the route and capability status. Do not load unrelated files.
2. Resolve task intent, brand, platform and content hierarchy.
3. Select composition and semantic tokens. Choose flat, subtle or expressive depth intentionally.
4. Implement accessible, responsive output. Do not add decorative controls or repetitive cards by default.
5. Run `python -m headronist.quality_gate` and `python -m headronist.composition page.html` where applicable.
6. Render and inspect real viewports, zoom, keyboard focus and reduced motion when tooling is available.
7. Distinguish static checks, rendered tests, and human visual review. Never claim one proves another.

## Contrast and depth

Use `python -m headronist.quality_gate --contrast '#112233' '#ffffff'` to calculate opaque sRGB contrast. Aim for WCAG AA 4.5:1 for normal text, 3:1 for large text and 3:1 for relevant UI boundaries. The function does not handle alpha compositing, gradients, images, dynamic states or APCA. Evaluate those in a browser.

Use depth to clarify structure and interaction: canvas, surface, raised, overlay. Prefer tone, border and spacing before shadows. Keep light direction consistent. Avoid blobs, indiscriminate glows and overused glass.

## Anti-drift

Registry owns routes and statuses. Catalog owns labels and discovery metadata. Expertise and depth contracts own review guidance. No duplicated route tables in Markdown. Validate cross-file references and aliases before release. Do not silently promote guidance-only capabilities to implemented.

The quality gate may report missing source paths in partial imports. Treat these as real integration gaps, not permission to suppress the check.
