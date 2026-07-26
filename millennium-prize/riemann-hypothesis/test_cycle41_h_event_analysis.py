#!/usr/bin/env python3

import unittest

from flint import ctx

from cycle41_h_event_analysis import first_weighted_recovery, h_event_rows


class Cycle41HEventAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.values, cls.rows = h_event_rows(232, 192)

    def test_recurrence_reconstructs_every_next_value(self):
        for row in self.rows:
            reconstructed = row["H_n"] + row["delta_H"]
            self.assertTrue(reconstructed.overlaps(self.values[row["q"]]))

    def test_nonsquarefree_update_is_pure_negative_drift(self):
        for row in self.rows:
            if row["mu_q"] == 0:
                self.assertTrue(row["linear"].is_zero())
                self.assertTrue(row["diagonal"].is_zero())
                self.assertLess(row["drift"], 0)

    def test_certified_negative_indices(self):
        negative = [n for n, value in self.values.items() if value < 0]
        self.assertEqual(
            negative,
            [2, 39, 40, 95, 96, 99, 100, 219, 220, 221, 222, 226],
        )

    def test_structural_crossings_and_compensation_events(self):
        rows = {row["n"]: row for row in self.rows}
        for n in (38, 94, 218, 220, 225):
            self.assertEqual(rows[n]["mu_q"], 1)
            self.assertLess(rows[n]["delta_H"], 0)
        for n in (40, 96, 100, 221, 222, 226, 228, 229, 230):
            self.assertEqual(rows[n]["mu_q"], -1)
            self.assertGreater(rows[n]["delta_H"], 0)

    def test_weighted_compensation_endpoints(self):
        expected = {39: 42, 95: 103, 219: 231, 226: 230}
        for start, stop in expected.items():
            actual, trace = first_weighted_recovery(self.values, start)
            self.assertEqual(actual, stop)
            self.assertLess(trace[-2][2], 0)
            self.assertGreaterEqual(trace[-1][2], 0)


if __name__ == "__main__":
    unittest.main()
