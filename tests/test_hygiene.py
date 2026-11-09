import tempfile
import unittest
from pathlib import Path
from headronist.hygiene import audit


class HygieneTests(unittest.TestCase):
    def test_detects_broken_link_and_personal_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "assets").mkdir()
            (root / "AGENTS.md").write_text("Instructions", encoding="utf-8")
            (root / "README.md").write_text("[missing](docs/missing.md)\n/Users/example/project", encoding="utf-8")
            result = audit(root)
            self.assertFalse(result["ok"])
            self.assertEqual({e["kind"] for e in result["errors"]}, {"invalid-local-link", "personal-path"})
            (root / "docs" / "missing.md").write_text("Guide", encoding="utf-8")
            (root / "README.md").write_text("[guide](docs/missing.md)", encoding="utf-8")
            self.assertTrue(audit(root)["ok"])
