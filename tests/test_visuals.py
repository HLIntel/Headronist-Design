import json
import unittest
from pathlib import Path

from headronist.visuals import build_prompt, recommend_graph

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "contracts" / "graphs.v1.json").read_text(encoding="utf-8"))


class VisualPromptTests(unittest.TestCase):
    def test_prompt_keeps_exact_copy_separate(self):
        result = build_prompt("hero", "AI infrastructure platform", text=["Headronist"])
        self.assertEqual(result["exactText"], ["Headronist"])
        self.assertIn("Headronist", result["prompt"])
        self.assertIn("Do not include text", build_prompt("background", "Dark abstract field")["prompt"])

    def test_prompt_rejects_invalid_ratio(self):
        with self.assertRaises(ValueError):
            build_prompt("hero", "AI platform hero", aspect_ratio="7:3")

    def test_graph_recommends_line_for_time_series(self):
        result = recommend_graph("time-series", "trend", "executive")
        self.assertEqual(result["recommendations"][0]["id"], "line")

    def test_graph_recommends_sankey_for_flow(self):
        result = recommend_graph("flow", "process", "operator")
        ids = [item["id"] for item in result["recommendations"]]
        self.assertIn("sankey", ids)

    def test_graph_rejects_unknown_purpose(self):
        with self.assertRaises(ValueError):
            recommend_graph("categories", "vibes")


class GraphCatalogTests(unittest.TestCase):
    def test_every_type_has_guidance_fields(self):
        for graph_id, graph in CATALOG["types"].items():
            for field in ("label", "when", "avoid", "encoding", "accessibility"):
                self.assertTrue(graph.get(field), f"{graph_id} missing {field}")

    def test_every_variant_has_guidance_fields(self):
        for graph_id, graph in CATALOG["types"].items():
            for variant_id, variant in graph.get("variants", {}).items():
                for field in ("label", "when", "avoid", "encoding", "accessibility"):
                    self.assertTrue(variant.get(field), f"{graph_id}.{variant_id} missing {field}")

    def test_catalog_references_are_valid(self):
        for graph_id, graph in CATALOG["types"].items():
            for purpose in graph["purposes"]:
                self.assertIn(purpose, CATALOG["purposes"], graph_id)
            self.assertTrue(graph["dataShapes"], graph_id)
            self.assertTrue(graph["audiences"], graph_id)

    def test_recommended_ids_exist_in_catalog(self):
        shapes = ("categories", "time-series", "parts-of-whole", "distribution",
                  "relationship", "geospatial", "hierarchy", "flow", "cohort", "single-kpi")
        for shape in shapes:
            for purpose in CATALOG["purposes"]:
                result = recommend_graph(shape, purpose)
                for item in result["recommendations"]:
                    self.assertIn(item["id"], CATALOG["types"])

    def test_kpi_trend_variant_is_reachable(self):
        result = recommend_graph("time-series", "trend", "executive")
        self.assertEqual(result["variant"]["type"], "kpi")
        self.assertEqual(result["variant"]["variant"], "trend")
        self.assertIn("table", result["variant"]["accessibility"])


if __name__ == "__main__":
    unittest.main()
