#!/usr/bin/env python3

import unittest

from cycle41_adversarial_features import (
    FEATURE_NAMES,
    arithmetic_tables,
    feature_rows,
    necessary_screen,
    threshold_audit,
)


class Cycle41AdversarialFeatureTests(unittest.TestCase):
    def test_exact_arithmetic_tables(self):
        tables = arithmetic_tables(16)
        self.assertEqual(tables["mu"][1:11], [1, -1, -1, 0, -1, 1, -1, 0, 0, 1])
        self.assertEqual(tables["mertens"][10], -1)
        self.assertEqual(tables["pp_exponent"][8], 3)
        self.assertEqual(tables["pp_exponent"][12], 0)
        self.assertEqual(tables["psi_bit_jump"][9], 2)

    def test_feature_values_are_integers(self):
        rows = feature_rows(35, 45)
        self.assertEqual([name for name in rows[0][1]], list(FEATURE_NAMES))
        self.assertTrue(all(isinstance(value, int)
                            for _, row in rows for value in row.values()))
        at_39 = dict(rows)[39]
        self.assertEqual(at_39["distance_prev_prime"], 2)
        self.assertEqual(at_39["distance_next_prime"], 2)
        self.assertEqual(at_39["prime_gap"], 4)

    def test_threshold_audit_exposes_counterexamples(self):
        X = [[0], [1], [2], [3]]
        y = [0, 1, 0, 1]
        audit = threshold_audit(X, y, ["x"])[0]
        self.assertGreater(audit["error_count"], 0)
        self.assertTrue(audit["counterexample_rows"])

    def test_necessary_screen_retains_all_positives(self):
        X = [[0, 0], [1, 1], [2, 1], [3, 0], [4, 2]]
        y = [0, 1, 1, 0, 0]
        screen = necessary_screen(X, y, ["x", "z"], max_literals=2)
        self.assertEqual(screen["confusion"]["fn"], 0)
        self.assertEqual(screen["confusion"]["tp"], 2)


if __name__ == "__main__":
    unittest.main()
