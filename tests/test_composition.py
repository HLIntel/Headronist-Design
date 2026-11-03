import unittest
from headronist.composition import analyze

class CompositionTests(unittest.TestCase):
    def test_clean_editorial(self):
        result = analyze("<main><h1>Clear design</h1><p>Useful text.</p></main>")
        self.assertEqual(result["warnings"], [])
        self.assertFalse(result["verified"])

    def test_repeated_cards(self):
        result = analyze('<section>' + '<div class="feature-card">Text</div>' * 4 + '</section>')
        self.assertIn("card-density", [w["code"] for w in result["warnings"]])

    def test_repeated_badges(self):
        result = analyze('<span class="status-badge">Info</span>' * 3)
        self.assertIn("label-density", [w["code"] for w in result["warnings"]])

    def test_long_heading(self):
        result = analyze("<h1>" + "word " * 16 + "</h1>")
        self.assertIn("heading-length", [w["code"] for w in result["warnings"]])

if __name__ == "__main__":
    unittest.main()
