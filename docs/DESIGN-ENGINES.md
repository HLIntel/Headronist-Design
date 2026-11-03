# Operational design intelligence engines

The design intelligence contracts are backed by optional, dependency-light local tools. These tools are deterministic where possible and explicit about the limits of their evidence.

## 1. Reference extraction

`python -m headronist.reference path/to/page.html --css path/to/site.css --source-id brand-home --output brand-profile.json`

For a public URL, network access must be explicitly enabled:

`python -m headronist.reference https://example.com --allow-network --source-id example`

The extractor records HTML structure, heading outline, repeated class names, literal CSS colors, font-family declarations, font sizes and spacing declarations. It does not run JavaScript, compute styles, inspect image pixels or infer hidden responsive states. Use supplied CSS for stronger evidence.

## 2. Browser capture

Install Playwright and its Chromium browser in the calling environment. Then:

`python -m headronist.visual capture http://127.0.0.1:3000 --output artifacts/design-review`

The capture engine writes a screenshot and manifest for 320, 375, 768, 1440 and 1920 pixel viewports. It records page title, response status, console errors, failed requests and horizontal overflow. The local target must already be running. Playwright is optional and is not a package runtime dependency.

## 3. Vision review

Configure an OpenAI-compatible chat-completions endpoint and model, then explicitly run:

`HEADRONIST_VISION_ENDPOINT=https://provider.example/v1 HEADRONIST_VISION_MODEL=model-name HEADRONIST_VISION_API_KEY=... python -m headronist.visual review artifacts/design-review/*.png`

The adapter sends the selected screenshots to the configured provider. The API key is read from an environment variable and is never written into a profile or manifest. Check provider data handling before sending proprietary screenshots. The response is returned for review; it is not proof of human approval. Different providers may vary in their support for image_url data URLs.

## 4. Repair handoff and reinspection

Save a visual-review response as JSON with a top-level findings array, then generate a focused coding-agent brief:

`python -m headronist.repair brief findings.json --output repair-brief.json`

After the coding agent makes changes, capture and review again. Compare the original and new findings:

`python -m headronist.repair compare findings.json reinspected-findings.json`

The repair engine creates an auditable handoff and compares finding IDs. It does not edit project source or invoke an external coding agent. A finding disappearing from the report is not equivalent to human approval.

## 5. Local design memory

Save an extracted or approved profile:

`python -m headronist.memory save brand-acme brand-profile.json --approved`

List profiles or retrieve a specific version:

`python -m headronist.memory list`

`python -m headronist.memory get brand-acme --version 1`

The default store is `~/.headronist/design-memory.v1.json`. Override it with `--store /path/to/store.json`. Each save appends a version; it does not silently overwrite approved history. The store is local JSON, not encrypted or synchronized. Protect it according to the sensitivity of its contents.

## Agent intake

The bounded intake router now recognizes `reference`, `visual_review`, `repair` and `design_memory` tasks. It returns routes and source paths only. It does not launch a browser, call a vision model, modify files or access memory automatically.

## Verification states

- Static analysis: HTML/CSS and registry checks.
- Rendered capture: screenshots and runtime browser signals exist.
- Visually reviewed: a configured vision reviewer has analyzed screenshots.
- Human approved: a person has explicitly approved the output.

Keep these states distinct in reports and release decisions.
