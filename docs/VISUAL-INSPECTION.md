# Rendered Visual Quality Assurance

*Quality assurance · Tags: screenshots, Playwright, responsive, evidence · [Documentation index](README.md)*

Static checks are useful, but they do not establish that a page looks or behaves correctly in a browser. Use contracts/visual-inspection.v1.json as the evidence contract for rendered reviews.

## Recommended browser loop

1. Start the target application using its documented development command.
2. Use Playwright to open the actual route.
3. Capture the contract viewports: 320, 375, 768, 1440 and 1920 CSS pixels.
4. Capture full-page screenshots and browser console/request failures.
5. Inspect layout, hierarchy, typography, spacing, contrast, responsive reflow and clipping.
6. Exercise keyboard navigation, visible focus and reduced-motion behavior.
7. Write findings with a screenshot or reproducible DOM/interaction reference.
8. Give the implementation agent precise corrections tied to the finding IDs.
9. Re-capture the affected viewports and close findings only when the evidence supports it.

## Finding format

Each finding must include a stable finding ID, dimension and severity, exact route and viewport, screenshot/DOM locator/measured evidence, description of the user-visible problem, specific recommended correction, and verification state after the correction.

## Evidence levels

| State | Meaning |
| --- | --- |
| not-run | No relevant check was executed |
| static-only | Source-level checks ran; no browser evidence |
| rendered-captured | Browser screenshots and runtime signals were captured |
| visually-reviewed | A reviewer inspected the rendered evidence |
| human-approved | A human explicitly approved the result |

Do not collapse these states into a single pass/fail label. Automated accessibility checks, visual-model review and human review are separate evidence sources.

## Playwright integration

A calling project may use its existing Playwright installation. Headronist does not add Playwright as a mandatory runtime dependency. The integration should launch a browser, navigate to the real local route, capture a full-page screenshot at each contract viewport, and collect console and request failures. Replace the route and viewport with the target project's actual values.

This workflow is an integration specification, not a test that Headronist has executed. The calling project must supply the browser installation and start command.

## Limitations

A screenshot cannot prove keyboard behavior, semantic correctness or every interaction state. DOM inspection cannot judge all visual qualities. Human review remains useful for art direction, brand fit and ambiguous trade-offs.
