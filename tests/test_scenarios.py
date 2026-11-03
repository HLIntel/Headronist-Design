import json
import unittest
from pathlib import Path
from headronist import registry
from engines.imagery.prompt import build_prompt

ROOT=Path(__file__).resolve().parents[1]

class ScenarioTests(unittest.TestCase):
    def test_routes_resolve(self):
        self.assertEqual(registry.check(registry.load()), [])
    def test_scenarios_have_regions_and_requirements(self):
        data=json.loads((ROOT/'contracts/scenarios.v1.json').read_text())
        self.assertGreaterEqual(len(data['scenarios']),8)
        for key,value in data['scenarios'].items():
            self.assertTrue(value['regions'],key)
            self.assertTrue(value['requirements'],key)
    def test_landscape_and_split(self):
        viewports=json.loads((ROOT/'contracts/scenarios.v1.json').read_text())['viewports']
        self.assertLess(viewports['phoneLandscape']['height'],viewports['phoneLandscape']['width'])
        self.assertIn('splitDesktop',viewports)
    def test_prompt_determinism(self):
        spec={'kind':'logo','intent':'minimal abstract geometric brand symbol','aspectRatio':'1:1','palette':'navy','text':[]}
        self.assertEqual(build_prompt(spec),build_prompt(spec))
        self.assertIn('safe margins',build_prompt(spec))
    def test_prompt_rejects_bad_ratio(self):
        with self.assertRaises(ValueError):
            build_prompt({'kind':'logo','intent':'test','aspectRatio':'7:3','palette':'navy','text':[]})
    def test_no_runtime_cdn(self):
        css=(ROOT/'engines/composition/responsive.css').read_text()
        self.assertNotIn('@import url(',css)
        self.assertIn('minmax(0,1fr)',css)
        self.assertIn('prefers-reduced-motion',css)

if __name__=='__main__':unittest.main()
