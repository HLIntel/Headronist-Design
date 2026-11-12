import json
import re
import unittest
from pathlib import Path

from headronist.composition import analyze

ROOT = Path(__file__).resolve().parent.parent

class CompositionTests(unittest.TestCase):
    def test_clean_editorial(self):
        result = analyze("<main><h1>Clear design</h1><p>Useful text.</p></main>")
        self.assertEqual(result["warnings"], [])
        self.assertFalse(result["verified"])

    def test_repeated_cards(self):
        result = analyze('<section>' + '<div class="feature-card">Text</div>' * 4 + '</section>')
        self.assertIn("card-density", [w["code"] for w in result["warnings"]])

    def test_repeated_badges(self):
        result = analyze('<span class="status-badge">Info</span>' * 3)
        self.assertIn("label-density", [w["code"] for w in result["warnings"]])

    def test_long_heading(self):
        result = analyze("<h1>" + "word " * 16 + "</h1>")
        self.assertIn("heading-length", [w["code"] for w in result["warnings"]])

class BlockLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = json.loads((ROOT / "contracts" / "composition-library.v1.json").read_text(encoding="utf-8"))
        cls.blocks_css = (ROOT / "components" / "primitives" / "blocks.css").read_text(encoding="utf-8")
        cls.dashboard = (ROOT / "examples" / "dashboard.html").read_text(encoding="utf-8")

    def test_first_blocks_are_registered(self):
        for name in ("kpi-row", "chart-card", "comparison-table"):
            self.assertIn(name, self.library["blocks"])

    def test_each_block_has_a_matching_css_class(self):
        for name, block in self.library["blocks"].items():
            self.assertIn("." + block["cssClass"], self.blocks_css, name)
            self.assertTrue((ROOT / block["definedIn"]).exists(), name)

    def test_each_block_is_used_in_the_dashboard_example(self):
        for name, block in self.library["blocks"].items():
            self.assertIn(block["cssClass"], self.dashboard, name)

    def test_chart_card_carries_a_table_fallback(self):
        self.assertIn("hd-chart-card__fallback", self.dashboard)
        self.assertIn("Data table", self.dashboard)

    def test_dashboard_data_block_matches_rendered_values(self):
        match = re.search(r'<script type="application/json" id="dashboard-data">(.*?)</script>', self.dashboard, re.S)
        data = json.loads(match.group(1))
        for metric in data["metrics"]:
            self.assertIn(f'<strong class="hd-kpi__value">{metric["value"]}</strong>', self.dashboard)
        for row in data["distribution"]["rows"]:
            self.assertIn(f'<td>{row["tasks"]}</td>', self.dashboard)


if __name__ == "__main__":
    unittest.main()
