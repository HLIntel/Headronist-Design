# Asset provenance: assets/backgrounds

License pass executed 2026-11-12 under the asset-sourcing policy
(`contracts/asset-sources.v1.json`: local-first, `requireLicenseReview`,
`requireAttributionMetadata`, no unvetted stock in the production set).
Every background file that ships from this repo carries one of three
statuses here: **own**, **verified**, or **rights-unverified**. Nothing is
marked verified without evidence on file; a self-declared license note is
recorded as a claim, not as verification.

## Current set: kept (2)

| File | Bytes | Status | Rights basis |
|---|---|---|---|
| `headronist-flow-network.svg` | 4,375 | own | Hand-authored project artwork (titled SVG, committed by the project in PR #7). Manifest: `sourceType: original`, `license: project-original`. |
| `headronist-trust-network.svg` | 7,148 | own | Hand-authored project artwork (titled SVG, committed by the project in PR #7). Manifest: `sourceType: original`, `license: project-original`. |

No renames were needed: both kept names are honest and descriptive.
`tests/test_asset_inventory.py` fails if a background file ships without a
manifest entry carrying `sourceType` and `license`, or without a row in
this document.

## Removed set: quarantined (22)

The 22 raster files below sat in `assets/backgrounds/` at commit
`284cf18e` with manifest license `unverified` (source `user-provided`),
except where noted. They were removed from the public, served set by
PR #10 (commit `c81e910`, "Separate public design assets from private
sources"). Removal is the quarantine: the files no longer ship from this
repo and survive only in git history at `284cf18e`, which is the audit
trail. Any file that returns must re-enter through the production-status
path in [ASSET-SOURCING.md](ASSET-SOURCING.md) with evidence, not by
restoring the old copy.

| File (at 284cf18e) | Bytes | Reason |
|---|---|---|
| `AdobeStock_320363623.jpeg` | 2,438,408 | Stock-agency name. Manifest claimed "Adobe Stock standard license (asset #320363623)"; the claim was never independently verified, and the agency name is not an honest production name. |
| `cloud-bank-black.jpeg` | 2,438,408 | Byte-identical duplicate of the Adobe Stock file above (sha256 `65c4c3a1...` for both, measured 2026-11-12) under a second name; manifest said unverified. |
| `istockphoto-1258945887-170667a.jpg` | 121,174 | Stock-agency name (iStock), license unverified. |
| `pngtree-glass-texture-transparent-three-dimensional-3d-background-image_15522954.png` | 414,361 | Stock-agency name (Pngtree), license unverified. |
| `350829-widescreen-website-background-1920x1080-windows-xp.jpg` | 64,574 | Third-party branded material: a Microsoft Windows XP wallpaper. |
| `ChatGPT Image Oct 7, 2026, 09_05_23 PM.png` | 1,562,308 | AI-generated image, license unverified; also against the spirit of the quality contract's rejection of AI-generated imagery as proof. |
| `2092464.webp` | 152,426 | Unknown provenance (opaque stock-style numeric name), license unverified. |
| `3113036.webp` | 118,746 | Unknown provenance (opaque stock-style numeric name), license unverified. |
| `522644.webp` | 233,232 | Unknown provenance (opaque stock-style numeric name), license unverified. |
| `NIIZQw2.jpg` | 79,488 | Unknown provenance (opaque file name), license unverified. |
| `a03b4e4a-d088-4fe1-9d3b-e5a911c11591.png` | 80,860 | Unknown provenance (opaque UUID name), license unverified. |
| `abstract-background-3d-black-geometric-platform-3d-rendering_549858-824.avif` | 9,211 | Stock-style catalog name, license unverified. |
| `abstract-blue-navy-triangle-overlap-with-text-background-vector.jpg` | 50,760 | Stock-style catalog name, license unverified. |
| `abstract-clean-blue-white-business-technology-background-vector.jpg` | 38,051 | Stock-style catalog name, license unverified. |
| `abstract-dynamic-textured-wave-background-photo.jpg` | 16,830 | Stock-style catalog name, license unverified. |
| `black-geometric-tech-corporate-background_88343-1709.avif` | 5,701 | Stock-style catalog name, license unverified. |
| `blue-powder-burst.jpeg` | 8,493,057 | License unverified (user-provided). See the storefront note below. |
| `blue-water-splash.jpeg` | 3,325,069 | License unverified (user-provided). |
| `blue-white-tech-corporate-abstract-background-vector-brochure-template-graphic-design_88343-6496.avif` | 18,441 | Stock-style catalog name, license unverified. |
| `dark-abstract-wallpaper-3840x2160-modern-art-innovative-visuals-26426.jpg` | 1,214,637 | Stock-style catalog name, license unverified. |
| `dark-blue-abstract-tech-corporate-background-vector.jpg` | 167,818 | Stock-style catalog name, license unverified. |
| `wavy-black-white-background_23-2150530931.avif` | 10,648 | Stock-style catalog name, license unverified. |

## Storefront note (flagged, not changed here)

The live storefront at headron.tech/headronist ships its own derivative
copies of two removed images (`blue-powder-burst.jpg` and
`adobestock-320363623.jpg`) inside its template/asset plates, labeled
"Candidate · rights unverified". Those are separate files in a separate
deployment, outside this repo and outside this pass. This record flags
the shared provenance so the site's Candidate labels can be retired or
the plates replaced with evidence, by the site's owner, in the site's
own lane. Nothing here renames or moves a storefront file.
