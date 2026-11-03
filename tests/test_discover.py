import unittest
from headronist.discover import discover

class DiscoveryTests(unittest.TestCase):
    def test_search(self):
        results=discover("typography")
        self.assertTrue(any(x["id"]=="typography" for x in results["results"]))
    def test_group(self):
        results=discover(group="quality")
        self.assertTrue(all(x["group"]=="quality" for x in results["results"]))
    def test_limit(self):
        results=discover(limit=1)
        self.assertLessEqual(len(results["results"]),1)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            discover(group="unknown")
if __name__=="__main__":
    unittest.main()
