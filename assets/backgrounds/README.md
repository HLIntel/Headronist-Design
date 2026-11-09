# Headronist trust network background

Original, locally hosted visual asset for the Headronist AI developer platform.

- **File:** `assets/backgrounds/headronist-trust-network.svg`
- **Format:** SVG, 1600 × 900 viewBox
- **Palette:** deep navy and graphite with muted blue and silver nodes
- **Composition:** connection mesh concentrated around the edges and lower field, with open central space for hero content
- **Use:** hero background, section backdrop, or responsive page surface
- **Runtime:** no external requests, scripts, fonts, or dependencies

## Usage

Use as a CSS background so the artwork remains decorative and does not interfere with content:

```css
.hero {
  background-color: #030d1b;
  background-image: url("/assets/backgrounds/headronist-trust-network.svg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
```

For mobile layouts, keep the focal area centered and add a dark overlay behind text when needed:

```css
@media (max-width: 640px) {
  .hero {
    background-position: 50% 50%;
  }
}
```

The SVG is intentionally text-free and logo-free. Keep hero copy in HTML for accessibility and responsive control.

## Supplied photographic mechanisms

These locally hosted JPEGs were supplied by the project owner for design exploration. Their original Adobe Stock filenames and embedded camera metadata are preserved only in the source files; confirm licensing and attribution before production redistribution.

| Asset | Intended mechanism | Contrast guidance |
|---|---|---|
| `blue-powder-burst.jpeg` | Dark hero or feature texture | Place copy in the open black area on the left |
| `blue-water-splash.jpeg` | Light editorial section backdrop | Use a dark text panel or overlay for readable copy |
| `cloud-bank-black.jpeg` | Atmospheric divider or depth layer | Keep content above the cloud line and preserve the black upper field |

Use them as CSS backgrounds or contained media with `object-fit: cover`; do not rely on the image itself for essential text or controls.