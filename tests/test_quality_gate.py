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
if __name__=="__main__":unittest.main()
