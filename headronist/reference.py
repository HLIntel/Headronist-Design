"""Extract conservative design evidence from HTML, CSS and optional public URLs.

Network access is opt-in. This module does not execute page JavaScript or claim to
recover hidden design tokens from screenshots.
"""
import argparse
from html.parser import HTMLParser
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

MAX_BYTES = 2_000_000
COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FONT_RE = re.compile(r"(?:font-family)\s*:\s*([^;}]+)", re.I)
SIZE_RE = re.compile(r"(?:font-size)\s*:\s*([^;}]+)", re.I)
GAP_RE = re.compile(r"(?:gap|padding|margin)\s*:\s*([^;}]+)", re.I)

class _Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = {}
        self.classes = {}
        self.headings = []
        self._heading = None
    def handle_starttag(self, tag, attrs):
        self.tags[tag] = self.tags.get(tag, 0) + 1
        attrs = dict(attrs)
        for cls in attrs.get("class", "").split():
            if cls:
                self.classes[cls] = self.classes.get(cls, 0) + 1
        if tag in ("h1", "h2", "h3"):
            self._heading = [tag, []]
    def handle_data(self, data):
        if self._heading is not None:
            self._heading[1].append(data.strip())
    def handle_endtag(self, tag):
        if self._heading is not None and tag == self._heading[0]:
            text = " ".join(x for x in self._heading[1] if x)
            if text:
                self.headings.append({"level": tag, "text": text[:240]})
            self._heading = None

def _evidence(source, dimension, claim, confidence="medium", location=None):
    return {"sourceId": source, "dimension": dimension, "claim": claim,
            "classification": "observed", "confidence": confidence,
            "sourceLocation": location or "document"}

def extract(html, source_id="local-html", css="", source_url=None):
    if not isinstance(html, str) or len(html.encode("utf-8")) > MAX_BYTES:
        raise ValueError("HTML must be text no larger than 2MB")
    if not isinstance(css, str) or len(css.encode("utf-8")) > MAX_BYTES:
        raise ValueError("CSS must be text no larger than 2MB")
    parser = _Markup()
    parser.feed(html)
    colors = sorted(set(COLOR_RE.findall(css)))
    fonts = sorted(set(x.strip().strip("\\"'") for x in FONT_RE.findall(css)))
    font_sizes = sorted(set(x.strip() for x in SIZE_RE.findall(css)))
    spacing = sorted(set(x.strip() for x in GAP_RE.findall(css)))
    evidence = []
    if colors:
        evidence.append(_evidence(source_id, "color", {"cssColorLiterals": colors}, "high", "stylesheet"))
    if fonts:
        evidence.append(_evidence(source_id, "typography", {"fontFamilies": fonts}, "high", "stylesheet"))
    if font_sizes:
        evidence.append(_evidence(source_id, "typography", {"fontSizes": font_sizes}, "high", "stylesheet"))
    if spacing:
        evidence.append(_evidence(source_id, "layout", {"spacingDeclarations": spacing[:80]}, "medium", "stylesheet"))
    evidence.append(_evidence(source_id, "layout", {
        "semanticTagCounts": parser.tags,
        "repeatedClassNames": sorted(parser.classes.items(), key=lambda x: (-x[1], x[0]))[:30],
        "headingOutline": parser.headings[:80]
    }, "high", "html"))
    return {
        "version": "1",
        "source": {"id": source_id, "url": source_url, "kind": "html-css"},
        "profile": {
            "typography": {"families": fonts, "observedSizes": font_sizes},
            "color": {"observedLiterals": colors},
            "layout": {"observedSpacingDeclarations": spacing[:80]},
            "structure": {"tagCounts": parser.tags, "headingOutline": parser.headings}
        },
        "evidence": evidence,
        "limitations": [
            "Only supplied HTML and CSS text were inspected; JavaScript-rendered states were not executed.",
            "Computed styles, inherited variables, media-query behavior and actual contrast are not evaluated.",
            "Repeated class names are structural clues, not proof of component purpose.",
            "No screenshot pixels were analyzed."
        ]
    }

def read_source(value, allow_network=False):
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https"):
        if not allow_network:
            raise ValueError("Network retrieval is disabled; pass --allow-network explicitly")
        if not parsed.hostname:
            raise ValueError("Invalid URL")
        request = urllib.request.Request(value, headers={"User-Agent": "Headronist-Reference/1.0"})
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise ValueError("Reference returned HTTP %s" % response.status)
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise ValueError("Reference exceeds 2MB")
            return raw.decode("utf-8", errors="replace"), value
    path = Path(value)
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError("Reference exceeds 2MB")
    return raw.decode("utf-8", errors="replace"), None

def main(argv=None):
    parser = argparse.ArgumentParser(description="Extract evidence-backed design signals from HTML/CSS")
    parser.add_argument("source", help="Local HTML file or URL")
    parser.add_argument("--css", help="Optional local CSS file")
    parser.add_argument("--allow-network", action="store_true", help="Explicitly allow fetching an HTTP(S) URL")
    parser.add_argument("--source-id", default="reference-1")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args(argv)
    html, url = read_source(args.source, args.allow_network)
    css = Path(args.css).read_text(encoding="utf-8") if args.css else ""
    result = extract(html, args.source_id, css, url)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
