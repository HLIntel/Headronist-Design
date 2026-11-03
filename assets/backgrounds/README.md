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