import json
import re
import unittest
from pathlib import Path

import jsonschema

from headronist.compiler import compile_tokens

ROOT = Path(__file__).resolve().parent.parent
TOKENS_CSS = (ROOT / "foundations" / "tokens.css").read_text(encoding="utf-8")
BOUND_CSS = [
    "engines/typography/type.css",
    "components/primitives/web.css",
    "components/primitives/hero.css",
    "components/primitives/blocks.css",
]


def defined_tokens():
    names = set()
    for rel in ["foundations/tokens.css"] + BOUND_CSS:
        path = ROOT / rel
        if path.exists():
            names.update(re.findall(r"(--hd-[a-z0-9-]+)\s*:", path.read_text(encoding="utf-8")))
    return names


def scale_steps(prefix):
    steps = {}
    for step, value in re.findall(r"--hd-" + prefix + r"-(\d+)\s*:\s*([0-9.]+)rem", TOKENS_CSS):
        steps[int(step)] = float(value)
    return steps


class TokenScaleTests(unittest.TestCase):
    def test_spacing_scale_is_complete_and_increasing(self):
        steps = scale_steps("space")
        self.assertEqual(sorted(steps), list(range(1, 11)))
        values = [steps[k] for k in sorted(steps)]
        self.assertEqual(values, sorted(values))
        self.assertEqual(steps[1] * 16, 4)  # 4px base rhythm

    def test_type_scale_is_complete_and_increasing(self):
        steps = scale_steps("type")
        self.assertEqual(sorted(steps), list(range(1, 10)))
        values = [steps[k] for k in sorted(steps)]
        self.assertEqual(values, sorted(values))
        self.assertEqual(steps[4], 1.0)  # step 4 is the 16px base

    def test_scales_validate_against_token_contract(self):
        schema = json.loads((ROOT / "contracts" / "tokens.v1.schema.json").read_text(encoding="utf-8"))
        space = scale_steps("space")
        spec = {
            "schemaVersion": "1.0.0",
            "id": "starter-stack",
            "colors": {
                "ground": "#08111f", "light": "#f5f8ff", "band": "#0c1626",
                "mark": "#a9c9ff", "soft": "#aebdd2", "deep": "#13233a",
            },
            "spacing": {str(k): v * 16 for k, v in space.items()},
            "radii": {"sm": 8, "md": 12, "lg": 20},
            "type": {"family": "system-ui", "basePx": 16, "scale": 1.25},
        }
        jsonschema.validate(spec, schema)
        compiled = compile_tokens(spec)
        self.assertIn("agent.tokens.json", compiled)

    def test_every_var_reference_resolves(self):
        defined = defined_tokens()
        for rel in BOUND_CSS:
            path = ROOT / rel
            if not path.exists():
                continue
            refs = set(re.findall(r"var\((--hd-[a-z0-9-]+)", path.read_text(encoding="utf-8")))
            self.assertEqual(refs - defined, set(), rel)

    def test_gap_declarations_use_spacing_tokens(self):
        for rel in ["components/primitives/web.css", "components/primitives/hero.css"]:
            css = (ROOT / rel).read_text(encoding="utf-8")
            for decl in re.findall(r"gap\s*:\s*([^;}]+)", css):
                if re.fullmatch(r"[0-9.]+rem", decl.strip()):
                    self.fail(f"{rel}: bare gap value {decl!r} is not a spacing token")


if __name__ == "__main__":
    unittest.main()
