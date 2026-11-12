# Visual system: color, materials and composition

Headronist keeps the existing navy tokens by default. Load `foundations/tokens.css` and opt in with `data-hd-theme="light"` on the root element. Add `data-hd-accent="teal"` or `data-hd-accent="violet"` for an alternative accent in either theme. Leave the attributes off for the existing navy and blue. These attributes change semantic roles, not the existing palette IDs. Recheck contrast when overriding any token or putting content over an image.

For showcase work, load `engines/composition/finish.css` and apply `hd-glass` to a content container. It uses a solid fallback, a restrained translucent surface where backdrop filtering is supported, and system colors in forced-colors mode. Test the actual background and crop: a translucent layer cannot guarantee text contrast. Use opaque surfaces for dense product interfaces.

## Compose with the assets

- **Headers:** keep navigation labels and focus indicators on a stable surface. Over imagery, use an opaque or tested scrim; preserve a solid fallback if the image fails.
- **Words:** use real text, a short headline, comfortable line length and a system or owner-selected typeface. Place copy in a quiet area, but do not assume the same safe area survives a mobile crop.
- **Cards:** use cards when they group distinct content; use prose or a list for continuous information. One border and a surface step are usually enough. Glass is an optional showcase treatment, not a requirement.
- **Backgrounds:** choose from the [inventory](../assets/manifest.v1.json); licensing and crop decisions need review. Add responsive derivatives only after confirming usage rights and source quality.
- **Color:** choose one accent and opaque text roles. Contrast targets are 4.5:1 for normal text and 3:1 for large text and UI boundaries, with a 7:1 body-text target where practical. Measure the actual combination, including any image and transparency.

Run `python -m headronist.registry check` and `python -m headronist.quality_gate`; these are static checks, not rendered visual or accessibility proof. Inspect a real page across small and large screens, 200% zoom, keyboard focus and reduced motion before claiming visual readiness.

## Font roles

Load `engines/typography/type.css` and choose a role where it fits: `.hd-font-ui` for a neutral system interface, `.hd-font-humanist` for a softer sans, `.hd-font-readable` or `.hd-font-editorial` for longer editorial passages, and `.hd-font-code` for code or tabular labels. Set `--hd-font-display` to one of these roles, or override the variables with an owner-selected, locally hosted face. These stacks do not download fonts, and their exact appearance varies by device. Check the selected face with the real languages and weights before release.

## Starting combinations

| Direction | Root attributes | Surface and background | Type and use |
|---|---|---|---|
| Light / teal | `data-hd-theme="light" data-hd-accent="teal"` | White page, pale raised panels; keep text on opaque surfaces | System UI for dashboards or service sites |
| Light / violet | `data-hd-theme="light" data-hd-accent="violet"` | White page with a restrained violet accent | UI sans for controls, editorial serif for longer reading |
| Navy / blue | No attributes | Navy surfaces; an original [network field](../assets/backgrounds/headronist-trust-network.svg) can support a showcase | System UI and monospace labels for technical content |
| Navy / teal | `data-hd-accent="teal"` | Navy surfaces; reserve imagery and optional glass for a showcase | System UI for navigation; choose a display role for headlines |

These are starting points, not automatic approvals. The static contrast tool measures teal on white at 6.858:1, violet on white at 9.027:1, and default blue on navy at 11.245:1. It does not measure transparency, images, borders, or every theme combination. For a specific opaque pair run `python -m headronist.quality_gate --contrast '#00665e' '#ffffff'`. Check actual rendered states and image crops. The public [manifest](../assets/manifest.v1.json) identifies project-original assets.
