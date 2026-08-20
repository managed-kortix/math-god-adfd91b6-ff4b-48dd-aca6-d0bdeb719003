#!/usr/bin/env python3

import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_near_cubic_gram_lane.py")
SPEC = importlib.util.spec_from_file_location("rank7_order10_near_cubic_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NearCubicGramLaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kernels = MODULE.kernel_dictionary()

    def test_kernel_degree_defect_ledger(self):
        counts = {}
        for kernel in self.kernels.values():
            partition = kernel["degree_partition"]
            counts[partition] = counts.get(partition, 0) + 1
            self.assertEqual(sum(value - 3 for value in partition), 2)
        self.assertEqual(counts, {
            (4, 4, 3, 3, 3, 3, 3, 3, 3, 3): 2888,
            (5, 3, 3, 3, 3, 3, 3, 3, 3, 3): 508,
        })

    def test_gram_is_exact_and_psd_by_construction(self):
        kernel = self.kernels[1]
        row = tuple(0 for _ in kernel["edges"])
        cost = MODULE.gram_cost(kernel["edges"], kernel["degrees"], row,
                                Fraction(1, 2), Fraction(1, 4))
        self.assertIsInstance(cost, Fraction)
        self.assertGreaterEqual(cost, 0)

    def test_cut_and_cycle_invariants(self):
        kernel = self.kernels[1]
        edges = kernel["edges"]
        self.assertTrue(MODULE.is_cut(edges, [False] * len(edges)))
        self.assertEqual(MODULE.cycle_rank(edges, [False] * len(edges)), 0)


if __name__ == "__main__":
    unittest.main()
