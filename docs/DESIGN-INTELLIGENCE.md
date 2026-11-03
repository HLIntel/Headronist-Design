# Brand and Reference Intelligence

*Design intelligence · Tags: brand analysis, reference profiles, evidence, composition · [Documentation index](README.md)*

Headronist turns references and task context into an evidence-backed design direction. It does not copy a reference or prescribe one universal aesthetic.

## Build A Reference Profile

Read contracts/reference-profile.v1.json before analyzing supplied URLs, screenshots, brand guidelines or source styles.

For every meaningful observation:
- Record the source identifier and source location.
- Classify it as observed, inferred or user-specified.
- Record confidence as high, medium or low.
- Preserve uncertainty and missing evidence.
- Keep brand requirements separate from incidental visual choices.

A screenshot may reveal spacing and hierarchy but cannot reliably reveal the original font family, responsive breakpoints, interaction states or source design tokens. Mark those as inferred or unknown unless additional evidence exists.

## Select Composition

Read contracts/composition-library.v1.json. Choose a pattern from the content hierarchy, medium, audience, density, brand profile and viewport requirements.

Return the selected pattern and why it fits, the primary focal point and content order, section rhythm and density plan, responsive reflow strategy, and deliberate deviations from the pattern.

Patterns are compositional starting points, not templates. Do not default to a repeated card grid or generic hero.

## Review Anti-Patterns

Read contracts/anti-patterns.v1.json. Treat each match as a review signal, not an automatic failure. Include evidence and explain why the signal matters in this particular interface. Dismiss a signal only with a short rationale.

Static HTML checks can identify structural hints. They cannot reliably judge visual balance, whitespace, originality, actual contrast over images, or whether a composition feels appropriate.

## Keep The Profile Reusable

Store approved profiles as versioned JSON alongside the project or brand. Do not silently overwrite an approved profile with a new inference. Keep source references and distinguish brand-wide rules from one-off page decisions.

## Boundaries

- No remote model, hosted service or runtime dependency is required by these contracts.
- Do not fetch external references unless the user or calling environment explicitly authorizes it.
- Do not claim a reference was inspected if only its URL or filename was supplied.
- Preserve existing v10-v13 identifiers and compatibility behavior.
