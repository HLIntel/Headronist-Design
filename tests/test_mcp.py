import unittest
from headronist.mcp import dispatch

class MCPTests(unittest.TestCase):
 def test_initialize(self):
  r=dispatch({"jsonrpc":"2.0","id":1,"method":"initialize","params":{}})
  self.assertEqual(r["result"]["serverInfo"]["name"],"headronist-design")
 def test_list(self):
  r=dispatch({"jsonrpc":"2.0","id":2,"method":"tools/list"})
  self.assertIn("design_intake",[x["name"] for x in r["result"]["tools"]])
 def test_discover(self):
  r=dispatch({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"design_discover","arguments":{"query":"landing"}}})
  self.assertFalse(r["result"]["isError"])
 def test_unknown(self):
  r=dispatch({"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"missing","arguments":{}}})
  self.assertTrue(r["result"]["isError"])
 def test_notification(self):
  self.assertIsNone(dispatch({"jsonrpc":"2.0","method":"notifications/initialized"}))
if __name__=="__main__":unittest.main()
