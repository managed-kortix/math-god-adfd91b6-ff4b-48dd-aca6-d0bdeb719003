#!/usr/bin/env python3

import unittest

from flint import ctx

from cycle43_finite_multiprobe_census import FAMILY_ORDER, run_census


class Cycle43FiniteMultiprobeCensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        # A cheap deterministic prefix containing the initial non-unit block.
        cls.small = run_census(cap=16, bits=192)

    def test_small_scope_is_complete_consecutive_first_recovery_census(self):
        self.assertEqual(self.small["census_start_range"], [2, 15])
        self.assertEqual(self.small["block_count"], 14)
        self.assertEqual(
            [row["start"] for row in self.small["blocks"]],
            list(range(2, 16)),
        )
        self.assertEqual(
            (self.small["blocks"][0]["start"],
             self.small["blocks"][0]["stop"]),
            (2, 6),
        )
        self.assertTrue(self.small["all_starts_recovered_by_cap"])

    def test_every_small_verdict_is_certified_and_greedy_passes(self):
        for row in self.small["blocks"]:
            for name in FAMILY_ORDER:
                self.assertIn(
                    row["families"][name]["verdict"],
                    ("PASS", "PASS_EQ", "FAIL"),
                )
            self.assertIn(
                row["families"]["greedy"]["verdict"],
                ("PASS", "PASS_EQ"),
            )

    def test_empty_current_admission_family_fails_without_singular_solve(self):
        row = next(row for row in self.small["blocks"] if row["start"] == 4)
        certificate = row["families"]["current_admissions"]
        self.assertEqual(certificate["family"], ())
        self.assertEqual(certificate["rank"], 0)
        self.assertEqual(certificate["verdict"], "FAIL")

    def test_family_summaries_count_every_block(self):
        for name in FAMILY_ORDER:
            item = self.small["family_summary"][name]
            self.assertEqual(
                item["pass_count"]
                + item["pass_equality_count"]
                + item["fail_count"],
                self.small["block_count"],
            )

    def test_fixed_families_are_not_chosen_from_outcomes(self):
        expected = {
            "affine_only": [0],
            "divisor_1_only": [1],
            "divisor_3_only": [3],
            "affine_plus_1": [0, 1],
            "affine_plus_3": [0, 3],
            "divisors_1_3": [1, 3],
            "affine_plus_1_3": [0, 1, 3],
        }
        for name, family in expected.items():
            self.assertEqual(self.small["fixed_families"][name], family)


if __name__ == "__main__":
    unittest.main()
