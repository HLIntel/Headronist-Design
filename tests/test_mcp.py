import json
import subprocess
import sys
import unittest
from pathlib import Path
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

    def test_visual_prompt_preserves_explicit_context(self):
        response = dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "design_visual_prompt", "arguments": {"kind": "hero", "intent": "A useful hero", "text": ["Exact words"], "references": ["Product screenshot"], "constraints": ["Mobile crop"]}}})
        data = json.loads(response["result"]["content"][0]["text"])
        self.assertEqual(data["exactText"], ["Exact words"])
        self.assertEqual(data["referenceContext"], ["Product screenshot"])
        self.assertEqual(data["constraints"], ["Mobile crop"])

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

    def test_advertised_intake_schema_is_canonical(self):
        schema = json.loads((Path(__file__).resolve().parents[1] / "contracts/intake.v1.schema.json").read_text())
        tools = dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]
        self.assertEqual(next(tool["inputSchema"] for tool in tools if tool["name"] == "design_intake"), schema)

    def test_tool_schema_rejects_invalid_and_unknown_arguments(self):
        cases = [
            ("design_recommend_assets", {"intent": "hero", "offline": "false"}),
            ("design_composition_check", {"html": "<p>x</p>", "typo": True}),
            ("design_discover", {"limit": True}),
            ("design_visual_prompt", {"kind": "hero", "intent": "a useful hero", "audience": []}),
            ("design_visual_prompt", {"kind": "hero", "intent": "a useful hero", "text": [42]}),
            ("design_intake", {"version": "1", "task": "web", "target": "x", "constraints": {"motion": "fast"}}),
        ]
        for name, arguments in cases:
            with self.subTest(name=name):
                response = dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}})
                self.assertTrue(response["result"]["isError"])

    def test_stdio_survives_invalid_tool_request(self):
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "design_recommend_assets", "arguments": {"intent": "hero", "offline": "false"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "ping"},
        ]
        result = subprocess.run([sys.executable, "-m", "headronist.mcp_stdio"], input="".join(json.dumps(r) + "\n" for r in requests), capture_output=True, text=True, timeout=10, check=True)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([response["id"] for response in responses], [1, 2])
        self.assertTrue(responses[0]["result"]["isError"])
        self.assertEqual(responses[1]["result"], {})


if __name__ == "__main__":
    unittest.main()
