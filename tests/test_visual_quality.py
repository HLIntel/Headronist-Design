import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class VisualQualityTests(unittest.TestCase):
 def test_navigation_targets(self):
  n=json.loads((ROOT/'contracts/navigation.v1.json').read_text())
  html=(ROOT/'examples/hero-workflows.html').read_text()
  for item in n['items']:
   self.assertIn('id="'+item['href'][1:]+'"',html)
 def test_quality_contract(self):
  q=json.loads((ROOT/'contracts/quality.v1.json').read_text())
  self.assertIn('AI-generated text as UI proof',q['visualReferences']['reject'])
  self.assertIn(320,q['gates']['requiredViewports'])
 def test_semantic_markup(self):
  html=(ROOT/'examples/hero-workflows.html').read_text()
  self.assertIn('<h1',html)
  self.assertIn('aria-labelledby',html)
  self.assertNotIn('position:absolute',html)
if __name__=='__main__':unittest.main()
