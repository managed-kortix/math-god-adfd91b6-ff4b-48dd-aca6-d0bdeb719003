"""Bounded exact comparator tests; mutation tests bypass byte checks deliberately."""
import copy
import unittest
from unittest.mock import patch
import rank7_order8_semantic_census as comparator


class SemanticCensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = comparator.load_census()
        cls.path = comparator.HERE/'rank7_order8_exact_residual_census_manifest.json'
        cls.manifest, _, _ = cls.c.read_payload(cls.path)
        cls.chunk_path = cls.path.parent / cls.manifest['chunks'][0]['path']
        cls.chunk, _, _ = cls.c.read_payload(cls.chunk_path)

    def run_compare(self, mutate=None):
        original = self.c.read_payload
        chunk = copy.deepcopy(self.chunk)
        if mutate:
            mutate(chunk)
        def read(path):
            if path == self.chunk_path:
                return chunk, b'', b''
            return original(path)
        with patch.object(comparator, 'load_census', return_value=self.c), \
             patch.object(self.c, 'read_payload', side_effect=read), \
             patch.object(self.c, 'verify_manifest'):
            return comparator.compare(self.path, 0, 1)

    def test_bounded_is_not_complete(self):
        result = self.run_compare()
        self.assertFalse(result['full_census_verified'])
        self.assertEqual(result['kernels_compared'], 1)

    def test_forged_ledger(self):
        with self.assertRaisesRegex(RuntimeError, 'semantic kernel ledger'):
            self.run_compare(lambda x: x['kernels'][0].update(automorphisms=999))

    def test_deleted_residual(self):
        with self.assertRaisesRegex(RuntimeError, 'semantic residual stream'):
            self.run_compare(lambda x: x['residuals'].pop(0))

    def test_bool_is_not_integer(self):
        with self.assertRaisesRegex(RuntimeError, 'semantic residual stream'):
            self.run_compare(lambda x: x['residuals'][0]['row'].__setitem__(0, True))


if __name__ == '__main__':
    unittest.main()
