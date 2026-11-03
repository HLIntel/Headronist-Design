# Context-aware asset sourcing

Headronist uses a **local-first asset strategy**. It should choose the visual medium that explains the product rather than defaulting to stock photography or random image URLs.

## Quick use

Recommend sources from a short description:

```sh
python -m headronist.assets recommend --intent "AI infrastructure trust network"
python -m headronist.assets recommend --intent "SaaS analytics dashboard" --kind product-ui
python -m headronist.assets recommend --intent "Editorial team portrait" --kind editorial-photo --allow-network-sources
```

Generate an original, keyless SVG network background:

```sh
python -m headronist.assets pattern --output assets/generated/network-field.svg --title "Network field"
```

The recommender is deterministic and does not fetch images, call a provider, read secrets, or download assets. Network sources appear only when explicitly requested. It returns source and licensing notes for an agent to consider.

## Choosing the right medium

| Context | Preferred visual | Avoid |
|---|---|---|
| AI infrastructure, trust, networks | Original SVG/CSS geometry, restrained node fields, diagrams | Generic robot/brain stock photography |
| SaaS product features | Real product screenshots, diagrams, interface snippets | Stock photos as substitutes for product proof |
| Editorial or human stories | Curated photography with source metadata | Random keyword results without review |
| Onboarding and empty states | Consistent illustration set or native UI | Mixing unrelated illustration styles |
| Dashboard surfaces | CSS texture, subtle SVG pattern, data visualization | Heavy imagery behind data |
| Development layout checks | Lorem Picsum | Shipping random placeholder images |

## Source notes

The machine-readable source inventory is [asset-sources.v1.json](../contracts/asset-sources.v1.json).

- **Native SVG/CSS:** preferred for abstract product visuals. Generated output is original and can be committed locally.
- **Haikei, Hero Patterns, SVG Backgrounds:** authoring tools and generators, not image APIs. Export assets and verify current terms before redistribution.
- **unDraw, Open Doodles, ManyPixels:** illustration libraries. Download assets, retain provenance, and verify each library's current license and brand fit.
- **Unsplash:** its API requires an access key and API terms apply. The free Unsplash license does not remove API integration requirements. Do not use `source.unsplash.com` as a production API.
- **Pexels:** API access requires a key. Its API page currently reports that new key issuance is paused; confirm availability before building an integration.
- **Pixabay:** API access requires a key. Its API docs prohibit permanent hotlinking of API image URLs; download and host assets only when allowed by its terms.
- **Lorem Picsum:** a keyless random placeholder service. Use only for development and layout tests, not final product imagery.
- **LoremFlickr:** intentionally omitted from the recommended source registry. Keyword matches, source rights and operational guarantees are not strong enough to make it a default production dependency.

## Agent rules

1. Start with local assets, authentic product screenshots, diagrams, or CSS/SVG.
2. Use a photo only when a person, place or physical environment adds meaning.
3. Do not invent a direct image URL or treat a homepage URL as an image endpoint.
4. Never fetch remote assets implicitly. Network use must be an explicit task constraint.
5. Preserve `sourceUrl`, `creator`, `license`, `retrievedAt`, and required `attribution` alongside downloaded assets.
6. Treat API keys as optional provider credentials, never hard-code them or store them in contracts.
7. Respect image dimensions, responsive cropping, alt text, contrast, reduced-motion preferences and content licensing.
8. A recommendation is not a license determination. Verify the current terms at the point of use.

## Scope

The recommender returns contextual options; it is not a stock-image search engine and does not validate third-party license compliance. The SVG generator produces one original decorative network background, not a general illustration renderer. No runtime dependencies are added.
