#!/usr/bin/env python3

import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_expanded_weighted_family_scan.py")
SPEC = importlib.util.spec_from_file_location("rank7_order10_expanded_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExpandedWeightedFamilyScanTests(unittest.TestCase):
    def test_parameter_grid_is_exact_and_non_scalar(self):
        self.assertEqual(len(MODULE.PARAMETERS), 120)
        self.assertEqual(len(MODULE.PROFILES), 8)
        self.assertTrue(all(isinstance(value, Fraction)
                            for row in MODULE.PARAMETERS for value in row[:3]))

    def test_high_precision_signature_selection(self):
        rows = {
            "selected": {"tested": 20, "owned": 19},
            "imprecise": {"tested": 20, "owned": 18},
            "small": {"tested": 4, "owned": 4},
            "empty": {"tested": 20, "owned": 0},
        }
        selected = MODULE.choose_signatures(rows, 5, Fraction(19, 20))
        self.assertEqual(selected, {"selected"})

    def test_new_metric_weights_are_positive_exact_rationals(self):
        paths = tuple((index, 0, 1, length)
                      for index, length in enumerate((1, 2, 3)))
        cut = ((Fraction(1, 2), 0, 0),
               (0, Fraction(1, 3), 0),
               (0, 0, Fraction(2, 3)))
        weights = MODULE.metric_weights(paths, cut)
        self.assertEqual(set(weights), set(MODULE.PROFILES))
        self.assertTrue(all(value > 0 and isinstance(value, Fraction)
                            for row in weights.values() for value in row))


if __name__ == "__main__":
    unittest.main()
