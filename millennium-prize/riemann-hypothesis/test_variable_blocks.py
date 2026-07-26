#!/usr/bin/env python3
"""Exact and hostile tests for the abstract variable-block theorem."""

import unittest
from fractions import Fraction

from verify_variable_blocks import Block, verify_variable_block_prefix


class VariableBlockPrefixTests(unittest.TestCase):
    def test_exact_variable_blocks_telescope(self):
        blocks = (Block(2, 4), Block(4, 7), Block(7, 8))
        values = {
            2: Fraction(3), 3: Fraction(2), 4: Fraction(2),
            5: Fraction(3, 2), 6: Fraction(1), 7: Fraction(1),
            8: Fraction(1, 2),
        }
        weights = {
            2: Fraction(1, 4), 3: Fraction(1, 4),
            4: Fraction(1, 6), 5: Fraction(1, 6), 6: Fraction(1, 6),
            7: Fraction(1, 2),
        }

        result = verify_variable_block_prefix(values, weights, blocks, Fraction(1, 2))

        self.assertEqual(result.total_decrement, Fraction(5, 2))
        self.assertEqual(result.endpoint_decrement, Fraction(5, 2))
        self.assertEqual(result.total_weight, Fraction(3, 2))
        self.assertEqual(
            result.aggregate_slack,
            result.total_decrement - result.kappa * result.total_weighted_energy,
        )
        self.assertTrue(all(check.slack >= 0 for check in result.checks))

    def test_failed_dissipation_is_rejected_exactly(self):
        with self.assertRaisesRegex(ValueError, "fails by 1/2"):
            verify_variable_block_prefix(
                {0: 1, 1: 1}, {0: 1}, (Block(0, 1),), Fraction(1, 2)
            )

    def test_finite_total_weight_hostile_family(self):
        # P_n = 1 + 2^-n has liminf 1 and satisfies every singleton inequality
        # with kappa=1 and w_n=P_n-P_(n+1).  Its total weight is only 1.
        depth = 12
        values = {
            n: 1 + Fraction(1, 2 ** n) for n in range(depth + 1)
        }
        weights = {
            n: (values[n] - values[n + 1]) / values[n]
            for n in range(depth)
        }
        blocks = tuple(Block(n, n + 1) for n in range(depth))

        result = verify_variable_block_prefix(values, weights, blocks, 1)

        self.assertTrue(all(check.slack >= 0 for check in result.checks))
        self.assertLess(result.total_weight, 1)
        self.assertGreaterEqual(min(values.values()), 1)

    def test_gap_that_can_reset_energy_is_rejected(self):
        # Without chaining, disjoint drops 2 -> 1 can be repeated after gaps,
        # while all sequence values stay at least 1 and block weight diverges.
        blocks = (Block(0, 1), Block(2, 3), Block(4, 5))
        values = {0: 2, 1: 1, 2: 2, 3: 1, 4: 2, 5: 1}
        weights = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1}
        with self.assertRaisesRegex(ValueError, "gap"):
            verify_variable_block_prefix(values, weights, blocks, 1)

    def test_overlap_that_reuses_one_drop_is_rejected(self):
        # Both blocks charge the same terminal drop. Repetition would create
        # unbounded counted weight without any new endpoint dissipation.
        blocks = (Block(0, 2), Block(1, 2))
        values = {0: 3, 1: 2, 2: 1}
        weights = {0: 0, 1: Fraction(1, 2)}
        with self.assertRaisesRegex(ValueError, "overlap"):
            verify_variable_block_prefix(values, weights, blocks, 1)

    def test_internal_increases_and_negative_one_step_decrements_are_allowed(self):
        values = {0: 4, 1: 5, 2: 2}
        weights = {0: Fraction(1, 8), 1: Fraction(1, 10)}
        result = verify_variable_block_prefix(
            values, weights, (Block(0, 2),), 1
        )
        self.assertEqual(result.checks[0].decrement, 2)
        self.assertEqual(result.checks[0].weighted_energy, 1)

    def test_exact_input_and_sign_hypotheses_are_enforced(self):
        with self.assertRaises(TypeError):
            verify_variable_block_prefix(
                {0: 1.0, 1: 0}, {0: 1}, (Block(0, 1),), 1
            )
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            verify_variable_block_prefix(
                {0: 1, 1: 0}, {0: -1}, (Block(0, 1),), 1
            )
        with self.assertRaisesRegex(ValueError, "positive"):
            verify_variable_block_prefix(
                {0: 1, 1: 0}, {0: 1}, (Block(0, 1),), 0
            )


if __name__ == "__main__":
    unittest.main()
