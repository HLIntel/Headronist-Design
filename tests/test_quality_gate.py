import unittest
from headronist.quality_gate import contrast, audit
class QualityGateTests(unittest.TestCase):
 def test_black_white(self):
  self.assertEqual(contrast("#000000","#ffffff"),21.0)
 def test_same_color(self):
  self.assertEqual(contrast("#123456","#123456"),1.0)
 def test_invalid_color(self):
  with self.assertRaises(ValueError): contrast("red","#ffffff")
 def test_audit_shape(self):
  result=audit()
  self.assertIn("errors",result)
  self.assertIn("verified",result)
 def test_surface_checks_executed(self):
  result=audit()
  self.assertEqual(result["verified"],"static-surface-checks-executed")
  self.assertEqual(result["errors"],[])
  self.assertTrue(result["ok"])
  for name in ("dashboard.html","hero-workflows.html","visual-system.html","website.html"):
   self.assertIn(name,result["surfaceChecks"]["examples"])
   self.assertIn("headline-length",result["surfaceChecks"]["examples"][name])
  self.assertGreaterEqual(min(result["surfaceChecks"]["bodyLineHeights"].values()),1.4)
  self.assertTrue(any("viewport sweep" in item for item in result["notExecuted"]))
if __name__=="__main__":unittest.main()
