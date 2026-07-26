#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from certify_complete_gram import complete_energies
from cycle40_complete_diagnostics import (
    consecutive_runs,
    cumulative_diagnostics,
    enclosing_extreme,
    local_diagnostics,
)


class Cycle40CompleteDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.energies = complete_energies(12)

    def test_local_half_surplus_identity(self):
        for row in local_diagnostics(self.energies):
            expected = (
                self.energies[row["n"]] - self.energies[row["n"] + 1]
                - row["weight"] * self.energies[row["n"]]
            )
            self.assertTrue(row["half_surplus"].overlaps(expected))
            reconstructed = (
                2 * row["weight"] * self.energies[row["n"]]
                * row["kappa_minus_half"]
            )
            self.assertTrue(row["half_surplus"].overlaps(reconstructed))

    def test_cumulative_scan_matches_direct_sum(self):
        local = {row["n"]: row for row in local_diagnostics(self.energies)}
        for row in cumulative_diagnostics(self.energies):
            total = arb(0)
            candidates = []
            for b in range(row["start"] + 1, 13):
                total += local[b - 1]["half_surplus"]
                candidates.append((b, total))
            direct_stop, direct_minimum = min(
                candidates, key=lambda item: float(item[1].mid())
            )
            self.assertEqual(row["worst_stop"], direct_stop)
            self.assertTrue(row["worst_half_surplus"].overlaps(direct_minimum))

    def test_enclosing_extreme_contains_all_endpoint_extrema(self):
        rows = [{"x": arb("1 +/- 0.1")}, {"x": arb("2 +/- 0.2")}]
        minimum = enclosing_extreme(rows, "x", "min")
        maximum = enclosing_extreme(rows, "x", "max")
        self.assertTrue(minimum.contains(arb("0.9")))
        self.assertTrue(minimum.contains(arb("1.1")))
        self.assertTrue(maximum.contains(arb("1.8")))
        self.assertTrue(maximum.contains(arb("2.2")))

    def test_consecutive_runs(self):
        self.assertEqual(
            consecutive_runs([2, 3, 7, 9, 10, 11]),
            [[2, 3], [7, 7], [9, 11]],
        )


if __name__ == "__main__":
    unittest.main()
