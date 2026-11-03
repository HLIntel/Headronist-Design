# Cross-Platform Design Adaptation

*Design foundations · Tags: mobile, tablet, desktop, adaptive layouts · [Documentation index](README.md)*

Headronist is not a Google, Apple, or GitHub skin. Translate the most useful interaction principles to the target medium while preserving the user's brand.

Google Material Design: use adaptive layouts, explicit states, token semantics, and responsive component behavior where appropriate.

Apple Human Interface Guidelines: use content-first hierarchy, safe areas, readable dynamic type, native platform behavior, and motion accessibility.

GitHub Primer: use compact information architecture, readable technical content, semantic colors, accessible focus and controls, and maintainable design documentation.

Choose based on the output: web landing pages prioritize editorial composition; applications prioritize interaction semantics; presentations prioritize narrative pacing; technical documentation prioritizes scanability and code readability. Do not force one visual style across all mediums.

## Agent workflow

1. Receive a bounded machine-readable task.
2. Determine medium, audience, platform, content density and brand.
3. Select composition and target-specific conventions.
4. Resolve reusable tokens and components through the registry.
5. Produce native artifacts using available tools.
6. Validate responsiveness, text hierarchy, accessibility and actual output.
7. Report only executed checks; distinguish guidance from renderers.

No remote SDK or vendor assets required. Reference systems are design research, not dependencies or licenses to reuse protected material.

Sources:
- https://m3.material.io/
- https://developer.apple.com/design/human-interface-guidelines/
- https://primer.style/
