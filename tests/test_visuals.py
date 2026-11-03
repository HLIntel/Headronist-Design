import unittest

from headronist.visuals import build_prompt, recommend_graph


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


if __name__ == "__main__":
    unittest.main()
