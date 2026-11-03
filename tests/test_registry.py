import unittest
from headronist import registry

class RegistryTests(unittest.TestCase):
    def test_references(self):
        self.assertEqual(registry.check(registry.load()), [])
    def test_alias(self):
        data=registry.load()
        self.assertEqual(registry.resolve("website",data)[0],"web")
    def test_reject_unknown(self):
        with self.assertRaises(ValueError):
            registry.resolve("nonexistent",registry.load())
    def test_fingerprint_is_stable(self):
        data=registry.load()
        self.assertEqual(registry.fingerprint(data),registry.fingerprint(data))
    def test_no_remote_dependencies(self):
        self.assertTrue(registry.load()["policy"]["offline"])
        self.assertFalse(registry.load()["policy"]["externalRuntimeDependencies"])
    def test_compatibility(self):
        self.assertEqual(registry.load()["compatibility"]["baseline"],["v10","v11","v12","v13"])

if __name__=="__main__":
    unittest.main()
