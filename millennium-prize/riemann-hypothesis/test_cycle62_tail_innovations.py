#!/usr/bin/env python3

import unittest
from fractions import Fraction

from flint import arb, ctx

from verify_cycle62_tail_innovations import (
    PUBLISHED_CROSSING_THRESHOLD,
    agrees_with_published_k24,
    cumulative_omega,
    exact_constraint_rows,
    mobius_sieve,
)


class Cycle62TailInnovationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_floor_constraints_remain_exact_rationals(self):
        rows = exact_constraint_rows(220, 231, 254, mobius_sieve(219))
        self.assertEqual(len(rows), 12)
        self.assertEqual(len(rows[0]), 36)
        self.assertTrue(
            all(isinstance(value, Fraction) for row in rows for value in row)
        )

    def test_published_consecutive_k24_value(self):
        omega = cumulative_omega(220, 231, 254, 192)
        self.assertTrue(agrees_with_published_k24(omega), omega)

    def test_reduced_first_crossing_is_certified(self):
        before = cumulative_omega(220, 231, 741, 192)
        crossing = cumulative_omega(220, 231, 742, 192)
        threshold = arb(PUBLISHED_CROSSING_THRESHOLD)
        self.assertLess(before, threshold)
        self.assertGreater(crossing, threshold)
        self.assertGreater(crossing - before, arb(0))


if __name__ == "__main__":
    unittest.main()
