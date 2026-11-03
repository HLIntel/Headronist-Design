import json
import unittest
from pathlib import Path

from headronist import registry

ROOT = Path(__file__).resolve().parents[1]


class DesignIntelligenceContractTests(unittest.TestCase):
    def load_contract(self, name):
        return json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))

    def test_new_routes_resolve_to_existing_contracts(self):
        data = registry.load()
        for route in ("referenceProfile", "compositionLibrary", "antiPatterns", "visualInspection"):
            resolved, paths = registry.resolve(route, data)
            self.assertEqual(resolved, route)
            self.assertTrue(paths)
            for path in paths:
                self.assertTrue((ROOT / path).is_file(), path)

    def test_reference_profile_requires_evidence_classification(self):
        contract = self.load_contract("reference-profile.v1.json")
        self.assertTrue(contract["evidence"]["requireSourceId"])
        self.assertEqual(
            contract["evidence"]["classification"],
            ["observed", "inferred", "user-specified"],
        )

    def test_composition_patterns_have_selection_rules(self):
        contract = self.load_contract("composition-library.v1.json")
        self.assertGreaterEqual(len(contract["patterns"]), 5)
        self.assertTrue(contract["selectionRules"])

    def test_antipatterns_require_contextual_evidence(self):
        contract = self.load_contract("anti-patterns.v1.json")
        self.assertTrue(contract["evaluation"]["requireEvidence"])
        self.assertTrue(contract["evaluation"]["neverAutoFailFromSingleHeuristic"])
        self.assertTrue(all(item.get("falsePositive") for item in contract["antiPatterns"]))

    def test_visual_inspection_separates_evidence_states(self):
        contract = self.load_contract("visual-inspection.v1.json")
        self.assertIn("static-only", contract["verificationStates"])
        self.assertIn("visually-reviewed", contract["verificationStates"])
        self.assertIn("human-approved", contract["verificationStates"])


if __name__ == "__main__":
    unittest.main()
