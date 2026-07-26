#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from cycle41_h_event_analysis import h_event_rows
from cycle42_negative_band_recovery import episode_records


class Cycle42NegativeBandRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        values, rows = h_event_rows(240, 192)
        cls.values = values
        cls.records = episode_records(values, rows)

    def test_exact_payment_endpoints(self):
        self.assertEqual(
            [(row["p"], row["q"], row["t"]) for row in self.records],
            [(2, 3, 6), (39, 41, 42), (95, 101, 103), (219, 227, 231)],
        )

    def test_each_payment_is_first_and_strict(self):
        for row in self.records:
            self.assertGreater(row["margin"], 0)
            previous_gain = row["gain"] - self._weighted_h(row["t"] - 1)
            self.assertLess(previous_gain, row["debt"])

    def test_recurrence_budget_equals_paid_residual(self):
        for row in self.records:
            self.assertTrue(row["residual"].overlaps(row["margin"]))
            self.assertLess(row["drift"], 0)
            self.assertGreater(row["impulse"], 0)

    def test_uniform_post_initial_beta_distortion(self):
        for row in self.records[1:]:
            self.assertLess(row["beta_ratio"], arb("1.124"))

    def _weighted_h(self, n):
        log_n = arb(n).log()
        log_next = arb(n + 1).log()
        weight = (log_next - log_n) / (log_n * log_next ** 2)
        return weight * self.values[n]


if __name__ == "__main__":
    unittest.main()
