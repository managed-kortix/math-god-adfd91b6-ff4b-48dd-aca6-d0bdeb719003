#!/usr/bin/env python3

import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order8_exact_gram_library.py")


def load_library():
    spec = importlib.util.spec_from_file_location("rank7_order8_library_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExactGramLibraryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library()
        cls.engine = cls.library.load_engine()
        cls.census = cls.engine.load_census_module()
        cls.residuals = cls.engine.residual_rows(cls.census)

    def test_normalized_key_is_vertex_permutation_invariant(self):
        source = self.residuals[7]
        signature, edges, order, cells = self.library.row_data(
            self.engine, self.census, source)
        permutation = tuple(reversed(range(self.engine.ORDER)))
        permuted = tuple((permutation[u], permutation[v], multiplicity, odd)
                         for u, v, multiplicity, odd in edges)
        left = set(self.library.normalized_keys(edges, order, cells, 720))
        other_source = (source[0], source[1], source[2], source[3], source[4],
                        source[5], source[6], source[7])
        incident = [[] for _ in range(self.engine.ORDER)]
        for u, v, multiplicity, odd in permuted:
            incident[u].append((multiplicity, odd))
            incident[v].append((multiplicity, odd))
        fingerprints = tuple(tuple(sorted(values)) for values in incident)
        other_order = tuple(sorted(range(self.engine.ORDER),
                                   key=lambda vertex: (fingerprints[vertex], vertex)))
        other_cells = tuple(tuple(group) for _, group in __import__("itertools").groupby(
            other_order, key=lambda vertex: fingerprints[vertex]))
        right = set(self.library.normalized_keys(permuted, other_order, other_cells, 720))
        self.assertEqual(left, right)
        self.assertEqual(signature, self.library.row_data(
            self.engine, self.census, other_source)[0])

    def test_first_pack_is_exactly_audited_before_mining(self):
        templates, degree_templates, orientations = self.library.load_templates(
            self.engine, self.census, self.residuals,
            self.library.DEFAULT_PACK, 720)
        self.assertEqual(sum(len(values) for values in degree_templates.values()), 5000)
        self.assertGreaterEqual(orientations, 5000)
        self.assertTrue(templates)

    def test_mined_gram_has_exact_rational_unit_diagonal(self):
        import lzma
        raw = lzma.decompress(self.library.DEFAULT_PACK.read_bytes())
        _, records = self.engine.base.exact_decode_pack(self.census, raw, self.residuals)
        gram = self.library.gram_from_witness(self.engine, records[0][1])
        self.assertTrue(all(value == Fraction(1) for value in
                            (gram[index][index] for index in range(self.engine.ORDER))))


if __name__ == "__main__":
    unittest.main()
