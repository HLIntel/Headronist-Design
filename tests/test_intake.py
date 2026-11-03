import unittest
from headronist.intake import route as route_task
class IntakeTests(unittest.TestCase):
 def test_compact_landing(self):
  result=route_task({"version":"1","task":"landing","target":"home"})
  self.assertIn("contracts/quality.v1.json",result["paths"])
  self.assertIn("navigation",result["routes"])
 def test_new_design_workflows(self):
  for task,expected_route in (("reference","referenceProfile"),("visual_review","visualInspection"),("repair","repair"),("design_memory","designMemory")):
   result=route_task({"version":"1","task":task,"target":"brand-site"})
   self.assertIn(expected_route,result["routes"])
 def test_asset_sourcing(self):
  result=route_task({"version":"1","task":"asset_sourcing","target":"hero-background"})
  self.assertIn("assetSourcing",result["routes"])
  self.assertIn("contracts/asset-sources.v1.json",result["paths"])
 def test_motion(self):
  result=route_task({"version":"1","task":"motion","target":"intro"})
  self.assertIn("contracts/motion.v1.json",result["paths"])
 def test_refuses_unknown(self):
  with self.assertRaises(ValueError):route_task({"version":"1","task":"web","target":"x","secret":"x"})
 def test_refuses_invalid_constraints(self):
  with self.assertRaises(ValueError):route_task({"version":"1","task":"web","target":"x","constraints":{"motion":"chaotic"}})
if __name__=="__main__":unittest.main()
