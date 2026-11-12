import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "worker"))
import build  # noqa: E402


class WorkerBuildTest(unittest.TestCase):
    def test_bundle_dispatches_tools_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            dist = build.build(pathlib.Path(tmp) / "dist")
            self.assertTrue((dist / "entry.py").is_file())
            probe = "import json;from headronist import mcp;print(json.dumps(mcp.dispatch({'jsonrpc':'2.0','id':1,'method':'tools/list'})))"
            out = subprocess.run([sys.executable, "-c", probe], cwd=dist, capture_output=True, text=True, check=True)
            names = [tool["name"] for tool in json.loads(out.stdout)["result"]["tools"]]
            self.assertEqual(len(names), 7)
            self.assertTrue(all(name.startswith("design_") for name in names))


if __name__ == "__main__":
    unittest.main()
