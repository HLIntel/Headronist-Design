"""Rendered browser capture and opt-in OpenAI-compatible vision review.

Playwright is optional. Vision review sends screenshots only when explicitly invoked
with an endpoint and API key; no provider SDK is required.
"""
import argparse
import base64
import json
import os
import urllib.request
from pathlib import Path

DEFAULT_VIEWPORTS = {
    "small-mobile": (320, 800), "mobile": (375, 812),
    "tablet": (768, 1024), "desktop": (1440, 900), "wide": (1920, 1080)
}

def capture(url, output_dir="artifacts/headronist-visual", viewports=None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install the optional Playwright package and browser binaries to capture screenshots") from exc
    if not url.startswith(("http://", "https://")):
        raise ValueError("Capture URL must use http or https")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    sizes = viewports or DEFAULT_VIEWPORTS
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, size in sizes.items():
            page = browser.new_page(viewport={"width": size[0], "height": size[1]})
            console_errors, request_failures = [], []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("requestfailed", lambda req: request_failures.append({"url": req.url, "failure": req.failure}))
            response = page.goto(url, wait_until="networkidle", timeout=45000)
            page.screenshot(path=str(out / (name + ".png")), full_page=True)
            results.append({
                "viewport": name, "width": size[0], "height": size[1],
                "status": response.status if response else None,
                "screenshot": str(out / (name + ".png")),
                "pageTitle": page.title(), "consoleErrors": console_errors,
                "requestFailures": request_failures,
                "horizontalOverflow": page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            })
            page.close()
        browser.close()
    manifest = {"version": "1", "url": url, "verification": "rendered-captured", "captures": results}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest

def vision_review(image_paths, endpoint, model, api_key, prompt=None, timeout=90):
    if not endpoint.startswith(("https://", "http://")):
        raise ValueError("Vision endpoint must be an HTTP(S) URL")
    if not model or not api_key:
        raise ValueError("Model and API key are required")
    paths = [Path(x) for x in image_paths]
    if not paths or any(not p.is_file() for p in paths):
        raise ValueError("Every screenshot path must exist")
    if sum(p.stat().st_size for p in paths) > 20_000_000:
        raise ValueError("Combined screenshot size exceeds 20MB")
    content = [{"type": "text", "text": prompt or (
        "Review these rendered interface screenshots. Return JSON with findings. "
        "For each finding include id, dimension, severity, finding, evidence, viewport, "
        "recommendedAction. Separate directly observable evidence from inference. "
        "Do not invent interaction behavior from screenshots."
    )}]
    for path in paths:
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + encoded}})
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": content}], "temperature": 0}).encode()
    request = urllib.request.Request(endpoint.rstrip("/") + "/chat/completions", data=body, headers={
        "Authorization": "Bearer " + api_key, "Content-Type": "application/json"
    }, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.loads(response.read(2_000_000).decode("utf-8"))
    return {"version": "1", "provider": "openai-compatible", "model": model,
            "verification": "visually-reviewed", "response": result}

def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("url"); cap.add_argument("--output", default="artifacts/headronist-visual")
    review = sub.add_parser("review")
    review.add_argument("images", nargs="+")
    review.add_argument("--endpoint", default=os.getenv("HEADRONIST_VISION_ENDPOINT", ""))
    review.add_argument("--model", default=os.getenv("HEADRONIST_VISION_MODEL", ""))
    review.add_argument("--api-key-env", default="HEADRONIST_VISION_API_KEY")
    args = parser.parse_args(argv)
    if args.command == "capture":
        result = capture(args.url, args.output)
    else:
        result = vision_review(args.images, args.endpoint, args.model, os.getenv(args.api_key_env, ""))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
