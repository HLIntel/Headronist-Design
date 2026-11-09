# Background assets

The [asset inventory](../manifest.v1.json) records dimensions, file sizes and alpha channels for the background collection. Files are candidates, not production approvals. Original filenames are retained to preserve source clues. The six images previously at the asset root are now here; update any external consumers of those old paths.

The two `headronist-*-network.svg` files are original, scalable, text-free network fields. The raster images were supplied for exploration. Their creators, rights and permitted redistribution have not been verified; confirm the source, license and attribution for each before use. The three supplied photos (`blue-powder-burst.jpeg`, `blue-water-splash.jpeg`, `cloud-bank-black.jpeg`) retain their source metadata.

## Choose and prepare

- Pick an image for its composition and purpose, not just its resolution. The manifest records dimensions; small 553–720px images are poor candidates for a full-width HD hero. Do not upscale a preview and call it HD.
- All inventoried raster files report **no alpha**, including the file whose name contains “transparent”. Use a CSS overlay or a separately reviewed transparent derivative when transparency is needed; retain the original. A filename is not evidence of transparency.
- Create optimized, appropriately sized derivatives only after licensing and crop review. Keep the highest-quality source separate; record derivative paths and provenance in the manifest. Avoid shipping the multi-megabyte master to every screen.
- Decorative backgrounds need no spoken description; meaningful images need an accurate text alternative. Keep headings and controls in semantic HTML. Use a solid surface or sufficiently opaque scrim under text, and measure contrast over the actual crop at each viewport. Blur alone does not guarantee legibility.
- Use background imagery and optional glass for showcase surfaces. Product tables, forms and dashboards should use flat, opaque surfaces. Check mobile crops, long copy, zoom, reduced motion and keyboard focus in a browser.

See [asset sourcing](../../docs/ASSET-SOURCING.md) and [visual lifecycle](../../docs/VISUAL-GENERATION-AND-GRAPHS.md) for rights and delivery practices.
