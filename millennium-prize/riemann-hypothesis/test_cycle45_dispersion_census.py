#!/usr/bin/env python3

import unittest
from fractions import Fraction

from flint import ctx

from cycle45_dispersion_census import (
    DispersionData,
    census_row,
    parse_interval,
    squarefree_rows,
    verify_all_rows,
)
from cycle45_exact_rational_sign_audit import audit


class Cycle45DispersionCensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_predeclared_intervals_are_exact_rationals(self):
        self.assertEqual(parse_interval("1,2"), (Fraction(1), Fraction(2)))
        self.assertEqual(
            parse_interval("1,3/2"), (Fraction(1), Fraction(3, 2))
        )
        data = DispersionData(32, 192)
        self.assertEqual(len(squarefree_rows(data, parse_interval("1,2"))), 19)
        self.assertEqual(
            len(squarefree_rows(data, parse_interval("1,3/2"))), 11
        )

    def test_reconstruction_matches_direct_and_existing_probe(self):
        data = DispersionData(32, 192)
        row = census_row(
            data, parse_interval("1,2"), verify_all_rows(data, 192)
        )
        self.assertEqual(row["rank"], 19)
        self.assertIn("+/-", row["direct_identity_max_error_ball"])
        self.assertIn("+/-", row["existing_probe_identity_max_error_ball"])
        self.assertIn("+/-", row["recombination_error"])

    def test_certified_small_scale_regression(self):
        data = DispersionData(32, 192)
        row = census_row(
            data, parse_interval("1,2"), verify_all_rows(data, 192)
        )
        self.assertEqual(
            row["L3D"],
            "[0.01375383140279139826689717 +/- 4.37e-27]",
        )
        self.assertEqual(
            row["L2Delta"],
            "[0.02386008294667573659102424 +/- 3.40e-27]",
        )
        self.assertEqual(
            row["LD_over_Delta"],
            "[0.5764368645963834020727765 +/- 3.50e-26]",
        )

    def test_exact_rational_sign_audit(self):
        self.assertEqual(audit(4), 6)
        self.assertEqual(audit(8), 11)


if __name__ == "__main__":
    unittest.main()
