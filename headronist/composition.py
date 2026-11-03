"""Advisory HTML composition analysis. No dependencies or file writes."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re

class Analyzer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = 0
        self.labels = 0
        self.effects = 0
        self.headings = []
        self.active_heading = None
    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").lower().split()
        self.cards += any(re.search(r"(?:^|-)(?:card|tile|panel)(?:$|-)", c) for c in classes)
        self.labels += any(re.search(r"(?:^|-)(?:badge|chip|pill|tag)(?:$|-)", c) for c in classes)
        self.effects += any(re.search(r"(?:^|-)(?:glow|blur|parallax|shine)(?:$|-)", c) for c in classes)
        if tag in ("h1", "h2", "h3"):
            self.active_heading = []
    def handle_data(self, data):
        if self.active_heading is not None:
            self.active_heading.append(data)
    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3") and self.active_heading is not None:
            self.headings.append(" ".join(" ".join(self.active_heading).split()))
            self.active_heading = None

def analyze(html):
    parser = Analyzer()
    parser.feed(html)
    warnings = []
    for name, count, threshold in (("card-density", parser.cards, 4), ("label-density", parser.labels, 3), ("effect-density", parser.effects, 3)):
        if count >= threshold:
            warnings.append({"code": name, "severity": "review", "count": count})
    for heading in parser.headings:
        if len(heading.split()) > 14:
            warnings.append({"code": "heading-length", "severity": "review", "words": len(heading.split())})
    return {"status": "advisory", "verified": False, "counts": {"cards": parser.cards, "labels": parser.labels, "effects": parser.effects}, "warnings": warnings}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    path = Path(args.path)
    if path.stat().st_size > 1000000:
        parser.error("Input exceeds 1MB")
    print(json.dumps(analyze(path.read_text(encoding="utf-8")), separators=(",", ":"), sort_keys=True))

if __name__ == "__main__":
    main()
