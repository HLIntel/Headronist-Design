# Reusable Hero and Graphic Primitives

*Components and reuse · Tags: hero, graphic assets, CSS, responsive reuse · [Documentation index](README.md)*

Use `components/primitives/hero.css` and copy the semantic markup from `examples/hero-workflows.html`. The example replaces the problematic phrase with **“Smarter workflows. Clearer results.”** It is an example, not a verified edit to an existing production page.

## Prevent text collisions

Never absolutely position headline words or stack independently translated text layers. Use normal-flow heading and description elements with `clamp()`, natural line height, `min-width:0`, and container-based scaling. Do not use fixed height on headline containers. Keep hero text at a maximum of 18ch and body text at 55ch. Test at 320px, 375px, 640px split view, 200% zoom and with 2x-length localization.

## Assets

`assets/primitives/workflow-nodes.svg` is original, vector-scalable and self-hosted. No account, license download or remote dependency is required. Preserve a real text alternative.

## Integration

Import the stylesheet into any site, or copy the classes into an existing CSS build. Avoid competing declarations for `.hd-hero__title`; the canonical primitive controls its flow. This CSS does not guarantee correctness against unknown legacy global styles. Browser screenshot verification is still required.
