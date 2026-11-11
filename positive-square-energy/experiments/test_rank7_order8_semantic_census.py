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

    def test_pure_automorphism_respects_multiplicity(self):
        # This 8-cycle has sixteen simple-support symmetries, but alternating
        # multiplicities preserve only eight.  A simple-graph implementation
        # would therefore accept eight false automorphisms.
        edges = ((0, 1, 1), (1, 2, 2), (2, 3, 1), (3, 4, 2),
                 (4, 5, 1), (5, 6, 2), (6, 7, 1), (0, 7, 2))
        actions = comparator.pure_automorphism_actions(8, edges)
        self.assertEqual(len(actions), 8)
        forged = tuple((u, v, 1) for u, v, _ in edges)
        self.assertEqual(len(comparator.pure_automorphism_actions(8, forged)), 16)

    def test_pure_automorphism_rejects_bool_multiplicity(self):
        with self.assertRaisesRegex(RuntimeError, 'invalid sparse kernel edge'):
            comparator.pure_automorphism_actions(8, ((0, 1, True),))

    def test_pure_fixture_parser_rejects_bool_code(self):
        fixture = copy.deepcopy(comparator.json.loads(
            comparator.KERNEL_SOURCE.read_text('ascii')))
        fixture['kernels'][0]['code'][0] = True
        raw = (comparator.json.dumps(fixture, sort_keys=True,
                                     separators=(',', ':')) + '\n').encode('ascii')
        with patch.object(comparator.Path, 'read_bytes', return_value=raw), \
             patch.object(comparator.hashlib, 'sha256') as digest:
            digest.return_value.hexdigest.return_value = comparator.KERNEL_SOURCE_SHA256
            with self.assertRaisesRegex(RuntimeError, 'invalid dense kernel code'):
                comparator.pure_source_kernels()

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
