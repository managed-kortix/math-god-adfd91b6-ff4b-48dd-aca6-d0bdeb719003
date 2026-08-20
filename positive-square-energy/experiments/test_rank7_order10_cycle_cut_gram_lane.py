#!/usr/bin/env python3

import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_cycle_cut_gram_lane.py")
SPEC = importlib.util.spec_from_file_location("rank7_order10_cycle_cut_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CycleCutGramLaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = MODULE.load_source()
        cls.kernel = source.kernel_dictionary()[1]

    def test_fundamental_cycle_basis_has_rank_seven(self):
        row = tuple(0 for _ in self.kernel["edges"])
        paths = MODULE.physical_paths(self.kernel["edges"], row)
        basis = MODULE.cycle_basis(paths)
        self.assertEqual((len(paths), len(basis)), (16, 7))

    def test_cut_and_cycle_metrics_are_complementary_projectors(self):
        row = tuple(0 for _ in self.kernel["edges"])
        paths = MODULE.physical_paths(self.kernel["edges"], row)
        endpoints = tuple((u, v) for _, u, v, _ in paths)
        cut = MODULE.cut_metric(endpoints)
        size = len(cut)
        for i in range(size):
            for j in range(size):
                square = sum(cut[i][k] * cut[k][j] for k in range(size))
                self.assertEqual(square, cut[i][j])
                self.assertEqual(cut[i][j], cut[j][i])
        self.assertEqual(sum(cut[i][i] for i in range(size)), 9)
        self.assertEqual(size - sum(cut[i][i] for i in range(size)), 7)

    def test_non_scalar_cycle_metrics_are_exact_psd_sums(self):
        row = tuple(0 for _ in self.kernel["edges"])
        cut_core, cycle_cores, paths = MODULE.embedding_components(
            self.kernel["edges"], row)
        self.assertEqual(len(paths), 16)
        self.assertEqual(set(MODULE.CYCLE_PROFILES) - set(cycle_cores), set())
        for profile in MODULE.CYCLE_PROFILES[1:]:
            core = cycle_cores[profile]
            self.assertTrue(all(isinstance(value, Fraction)
                                for matrix_row in core for value in matrix_row))
            for shift in range(10):
                vector = [Fraction((index + shift) % 5 - 2) for index in range(10)]
                quadratic = sum(vector[u] * core[u][v] * vector[v]
                                for u in range(10) for v in range(10))
                self.assertGreaterEqual(quadratic, 0, profile)

    def test_gram_and_cost_are_exact(self):
        row = tuple(0 for _ in self.kernel["edges"])
        gram, paths, normalizer = MODULE.embedding_gram(
            self.kernel["edges"], self.kernel["degrees"], row,
            Fraction(1), Fraction(1), Fraction(1))
        self.assertTrue(all(value == 1 for value in (gram[i][i] for i in range(10))))
        self.assertIsInstance(normalizer, Fraction)
        self.assertIsInstance(MODULE.gram_cost(gram, paths), Fraction)

    def test_small_representative_scan_is_fail_closed(self):
        report = MODULE.scan(4)
        self.assertEqual(report["sampling"]["tested"], 4)
        self.assertEqual(report["result"]["owned"] + report["result"]["failed"], 4)


if __name__ == "__main__":
    unittest.main()
