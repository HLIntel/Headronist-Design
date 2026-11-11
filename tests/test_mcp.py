import json
import unittest
from headronist.mcp import dispatch


class MCPTests(unittest.TestCase):
    def test_initialize(self):
        r = dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(r["result"]["serverInfo"]["name"], "headronist-design")

    def test_list(self):
        r = dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = [x["name"] for x in r["result"]["tools"]]
        self.assertIn("design_intake", names)
        self.assertIn("design_discover", names)
        self.assertIn("design_inspect", names)
        self.assertIn("design_recommend_assets", names)
        self.assertIn("design_visual_prompt", names)
        self.assertIn("design_graph_guidance", names)
        self.assertIn("design_composition_check", names)

    def test_discover(self):
        r = dispatch(
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "design_discover", "arguments": {"query": "landing"}}}
        )
        self.assertFalse(r["result"]["isError"])

    def test_recommend_assets(self):
        r = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "design_recommend_assets", "arguments": {"intent": "security network"}},
            }
        )
        self.assertFalse(r["result"]["isError"])
        data = json.loads(r["result"]["content"][0]["text"])
        self.assertEqual(data["kind"], "abstract")

    def test_visual_prompt(self):
        r = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "design_visual_prompt",
                    "arguments": {"kind": "hero", "intent": "AI safety platform launch"},
                },
            }
        )
        self.assertFalse(r["result"]["isError"])
        data = json.loads(r["result"]["content"][0]["text"])
        self.assertEqual(data["kind"], "hero")

    def test_graph_guidance(self):
        r = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {
                    "name": "design_graph_guidance",
                    "arguments": {"data_shape": "time-series", "purpose": "trend"},
                },
            }
        )
        self.assertFalse(r["result"]["isError"])
        data = json.loads(r["result"]["content"][0]["text"])
        self.assertTrue(len(data["recommendations"]) > 0)

    def test_composition_check(self):
        r = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "tools/call",
                "params": {
                    "name": "design_composition_check",
                    "arguments": {"html": "<main><h1>Clear Headline</h1><p>Body copy.</p></main>"},
                },
            }
        )
        self.assertFalse(r["result"]["isError"])
        data = json.loads(r["result"]["content"][0]["text"])
        self.assertEqual(data["status"], "advisory")
        self.assertEqual(data["warnings"], [])

    def test_unknown(self):
        r = dispatch({"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "missing", "arguments": {}}})
        self.assertTrue(r["result"]["isError"])

    def test_notification(self):
        self.assertIsNone(dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"}))


if __name__ == "__main__":
    unittest.main()
