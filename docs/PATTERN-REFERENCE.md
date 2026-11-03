# Pattern Research and Reference

*Research · Tags: patterns, composition, responsive design, design systems · [Documentation index](README.md)*

Headronist borrows *principles* from Webflow (responsive visual composition), Webstudio (open, component-oriented site building), Penpot (shared design tokens and reusable components), Bootstrap (stable layout and predictable responsive utilities), UI Pro Max-style design galleries (scenario-driven inspiration), Ghostty (fast defaults), and accessible primitive systems (state separated from styling). No vendor source, assets, branding, hosted services or dependencies are imported.

## Composition defaults
- Mobile first, but test landscape phones, split-screen desktop and 200% zoom; use intrinsic sizing, `minmax(0,1fr)`, container queries and fluid type.
- No global horizontal scroll. Intentional carousel, code and table scrollers must be visibly discoverable and keyboard usable.
- Use content-led hierarchy: one primary action, readable type, stable header/footer, no overlap with fixed controls or safe areas.
- Avoid layout shift: reserve media dimensions, font fallbacks, stable skeletons and finite animation.
- Design state coverage: idle, loading, empty, partial, error, retry, success, offline, unauthorized.
- For FAQ, privacy and factual documentation, do not invent policies, certifications, security guarantees or statistics. Prefer native `details/summary` for simple disclosure.
- Socials require validated real URLs and labels; never fake social proof or endorsements.
- Logos: original vector-first forms, simple silhouettes, legible at 24px, clear-space rules, monochrome test and trademark review.
- Charts: axes, units, legends, zero-baseline where appropriate, accessible tabular alternative and no fabricated values.
- Streaming UI: bounded updates, cancel/pause, status and error recovery, controlled auto-scroll only when user is at bottom.
- Menus and tabs: keyboard support, focus visibility, escape behavior and no hover-only controls.

## Verification matrix
Check 320x568, 375x812, 812x375, 640x800, 768x1024, 1440x900 and 1920x1080; zoom 200%, long URLs, long translations, RTL, no-JS fallback, slow loading, keyboard, reduced motion and print. No claim of browser validation without executing it.
