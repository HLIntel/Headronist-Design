# Enterprise starter stack

One starter stack serves the website and landing routes. Both starters share
the same shell, the same token foundation, and the same rules; they differ
only in the sections they compose.

## Starters

- Website: `examples/website.html` on `components/primitives/web.css`
  (route `web`).
- Landing: `examples/hero-workflows.html` on `components/primitives/hero.css`
  plus the shared navigation (route `landing`).

Load order for both: `foundations/tokens.css`, then
`engines/typography/type.css`, then the route primitives. No starter adds a
runtime dependency, a web font, or a script requirement; navigation and
content remain usable with scripts disabled.

## Shared shell

Every page in the stack is built from the same semantic regions, in order:

1. `header` with the primary `nav` (brand plus links, 44px minimum targets).
2. `main` containing a hero region (`.hd-site__hero` or `.hd-hero`), then
   content sections, panels, and columns as the content requires.
3. `footer` with secondary links and status information.

Use landmark elements (`header`, `nav`, `main`, `footer`, `section` with
`aria-labelledby`) instead of generic containers so the outline, keyboard
order, and heading hierarchy describe the page without styling.

## Typography hierarchy

Type comes only from the scale in `foundations/tokens.css`
(`--hd-type-1` to `--hd-type-9`: 12, 13, 14, 16, 20, 24, 32, 40, 52 px at a
16px root) and the role classes in `engines/typography/type.css`:

- `.hd-body` for running text (fluid between the small and body steps).
- `.hd-heading` for headings, with `.hd-heading--section`,
  `.hd-heading--title`, and `.hd-heading--display` selecting scale steps.
- `.hd-label` for labels and eyebrows (step 2, uppercase only in the hero
  and site eyebrow treatments).

One `h1` per page, heading levels in order, line-height at least 1.4 for
body text. Fluid `clamp()` sizes may interpolate between two scale steps;
they may not introduce sizes outside the scale's range.

## Spacing rhythm

Spacing comes only from the scale in `foundations/tokens.css`
(`--hd-space-1` to `--hd-space-10`: 4, 8, 12, 16, 20, 24, 32, 48, 64, 96 px,
a 4px base rhythm). Primitives use scale tokens for every `gap`, `padding`,
and `margin` value; fluid expressions interpolate between two steps.
Borders, outlines, and minimum touch targets (44px) are not spacing and keep
their own values.

## Palette and contrast

The navy foundation in `foundations/tokens.css` is the default palette:
Ink grounds, Bone-tinted text, Deep Ocean accent. Semantic color tokens
(`--hd-color-*`) are the only colors primitives may reference; the opt-in
light theme and teal/violet accents override the same token names, never
the primitives. Text and muted text tokens are the pairs measured for
contrast; decorative color never carries meaning alone.

## No decorative overload

Composition precedes effects. No ornamental gradients, shadow blobs,
parallax, or card walls; one primary action per region; imagery is real
product evidence or local SVG/CSS, sourced under
`docs/ASSET-SOURCING.md`. Motion is opt-in and honors
`prefers-reduced-motion` (see `contracts/motion.v1.json`).

## Token contract

The scales satisfy `contracts/tokens.v1.schema.json`: spacing and radii are
numeric maps in the 0 to 256 range, and the type block is family, `basePx`
16, ratio `scale` 1.25. `headronist/compiler.py` compiles a contract with
these values unchanged, and `tests/test_tokens.py` keeps the shipped CSS
scales, the schema, and the compiler in agreement. Token names are public
identifiers: never rename them (see `docs/COMPATIBILITY.md`).
