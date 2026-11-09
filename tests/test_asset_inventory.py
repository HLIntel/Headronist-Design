"""Guard the local background inventory against missing or unlisted files."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AssetInventoryTests(unittest.TestCase):
    def test_background_inventory_matches_files(self):
        entries = json.loads((ROOT / 'assets/manifest.v1.json').read_text())['assets']
        ids = [entry['id'] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        listed = {entry['path'] for entry in entries}
        self.assertEqual(len(listed), len(entries))
        extensions = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.svg'}
        files = {str(path.relative_to(ROOT)) for path in (ROOT / 'assets/backgrounds').iterdir()
                 if path.suffix.lower() in extensions}
        self.assertEqual(listed, files)
        for entry in entries:
            self.assertEqual(entry['bytes'], (ROOT / entry['path']).stat().st_size)



if __name__ == '__main__':
    unittest.main()
