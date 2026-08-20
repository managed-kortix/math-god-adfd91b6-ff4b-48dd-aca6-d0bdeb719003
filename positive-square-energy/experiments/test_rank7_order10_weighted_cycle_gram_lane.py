#!/usr/bin/env python3

import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_weighted_cycle_gram_lane.py")
SPEC = importlib.util.spec_from_file_location("rank7_order10_weighted_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WeightedCycleGramLaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = MODULE.load("weighted_test_source", MODULE.SOURCE)
        cls.projector = MODULE.load("weighted_test_projector", MODULE.PROJECTOR)
        manifest, _ = cls.source.strict_json(cls.source.MANIFEST)
        cls.kernels = cls.source.kernel_dictionary()
        cls.record = next(cls.source.remainder_records(manifest))
        cls.kernel = cls.kernels[cls.record[2]]

    def test_profiles_are_exact_nonnegative_path_weights(self):
        row = tuple(self.record[3])
        paths = self.projector.physical_paths(self.kernel["edges"], row)
        endpoints = tuple((u, v) for _, u, v, _ in paths)
        cut = self.projector.cut_metric(endpoints)
        signed = [[Fraction() for _ in paths] for _ in range(10)]
        for column, (_, u, v, length) in enumerate(paths):
            signed[u][column] = 1
            signed[v][column] = -1 if length & 1 else 1
        cores = MODULE.weighted_cycle_cores(signed, paths, cut)
        self.assertEqual(set(cores), set(MODULE.PROFILES))
        for core in cores.values():
            self.assertTrue(all(isinstance(value, Fraction)
                                for row_values in core for value in row_values))
            for shift in range(10):
                vector = [Fraction((index + shift) % 5 - 2) for index in range(10)]
                quadratic = sum(vector[u] * core[u][v] * vector[v]
                                for u in range(10) for v in range(10))
                self.assertGreaterEqual(quadratic, 0)

    def test_search_returns_exact_cost_and_non_scalar_profile(self):
        cost, parameters, normalizer = MODULE.search(
            self.projector, self.kernel, tuple(self.record[3]))
        self.assertIsInstance(cost, Fraction)
        self.assertIsInstance(normalizer, Fraction)
        self.assertIn(parameters[3], MODULE.PROFILES)

    def test_representative_floor_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "at least 10,000"):
            MODULE.scan(9999)


if __name__ == "__main__":
    unittest.main()
