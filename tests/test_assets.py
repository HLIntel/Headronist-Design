import unittest
from headronist.assets import classify, make_pattern, recommend

class AssetTests(unittest.TestCase):
    def test_context_classification(self):
        self.assertEqual(classify("AI infrastructure trust network"), "abstract")
        self.assertEqual(classify("SaaS analytics dashboard"), "product-ui")
        self.assertEqual(classify("editorial office photography"), "editorial-photo")

    def test_offline_recommendations_are_local(self):
        result = recommend("AI infrastructure trust network")
        self.assertTrue(result["recommendations"])
        self.assertTrue(all(not item.get("url") for item in result["recommendations"]))
        self.assertFalse(result["networkRequested"])

    def test_photo_sources_are_not_misrepresented_as_keyless(self):
        result = recommend("editorial photography people", offline=False)
        by_id = {item["id"]: item for item in result["recommendations"]}
        self.assertEqual(by_id["unsplash"]["access"], "api-key")
        self.assertEqual(by_id["pexels"]["access"], "api-key")
        self.assertEqual(by_id["pixabay"]["access"], "api-key")

    def test_placeholder_requires_opt_in(self):
        result = recommend("layout testing placeholder", offline=False)
        self.assertNotIn("picsum", [item["id"] for item in result["recommendations"]])
        result = recommend("layout testing placeholder", offline=False, allow_placeholders=True)
        self.assertIn("picsum", [item["id"] for item in result["recommendations"]])

    def test_svg_is_original_and_valid(self):
        svg = make_pattern()
        self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', svg)
        self.assertIn("Abstract connected network nodes", svg)
        with self.assertRaises(ValueError):
            make_pattern(foreground="url(javascript:alert(1))")

    def test_invalid_intent(self):
        with self.assertRaises(ValueError):
            recommend("")

if __name__ == "__main__":
    unittest.main()
