import json
import tempfile
import unittest
from pathlib import Path

from headronist.reference import extract, read_source
from headronist.repair import create_repair_brief, compare_reinspection
from headronist.memory import save_profile, get_profile, list_profiles


class ReferenceTests(unittest.TestCase):
    def test_extract_observed_css_and_html(self):
        result = extract('<main><h1>Welcome</h1><h2>Details</h2></main>',
                         "brand-home", "body { color: #112233; font-family: Inter, sans-serif; }")
        self.assertEqual(result["source"]["id"], "brand-home")
        self.assertIn("#112233", result["profile"]["color"]["observedLiterals"])
        self.assertEqual(result["evidence"][-1]["classification"], "observed")
        self.assertEqual(result["profile"]["structure"]["headingOutline"][0]["text"], "Welcome")

    def test_network_is_opt_in(self):
        with self.assertRaises(ValueError):
            read_source("https://example.com", allow_network=False)


class RepairTests(unittest.TestCase):
    def setUp(self):
        self.finding = {"id": "mobile-overflow", "dimension": "responsive",
                        "severity": "high", "finding": "Horizontal overflow",
                        "evidence": "375px screenshot", "recommendedAction": "Reflow columns",
                        "viewport": "mobile"}
    def test_repair_brief_is_handoff_only(self):
        result = create_repair_brief({"verification": "visually-reviewed", "findings": [self.finding]})
        self.assertEqual(result["reinspectionRequired"], ["mobile-overflow"])
        self.assertIn("handoff-only", result["execution"])
    def test_compare_reinspection(self):
        after = {"verification": "rendered-captured", "findings": []}
        result = compare_reinspection({"findings": [self.finding]}, after)
        self.assertEqual(result["resolved"], ["mobile-overflow"])


class MemoryTests(unittest.TestCase):
    def test_profile_versions_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "memory.json"
            first = save_profile("brand-a", {"palette": ["#112233"]}, store, approved=True)
            second = save_profile("brand-a", {"palette": ["#ffffff"]}, store)
            self.assertEqual(first["version"], 1)
            self.assertEqual(second["version"], 2)
            self.assertEqual(get_profile("brand-a", store, 1)["profile"]["palette"], ["#112233"])
            self.assertEqual(list_profiles(store)[0]["versions"], 2)


if __name__ == "__main__":
    unittest.main()
