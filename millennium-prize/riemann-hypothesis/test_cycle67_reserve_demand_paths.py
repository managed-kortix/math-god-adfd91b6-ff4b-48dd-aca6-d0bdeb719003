#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from verify_cycle67_reserve_demand_paths import (
    CERTIFICATE_SHA256,
    HARD_WINDOWS,
    load_surplus_certificate,
    reserve_demand_paths,
)


EXPECTED_FINAL_S = {
    (39, 42): "0.0004463390883355535887674870865",
    (40, 42): "0.0004954170994696162929291374873",
    (95, 103): "0.00006797012681613390671994027847",
    (96, 103): "0.0001540690855824485434336508866",
    (99, 102): "0.00007740342441890922992342773995",
    (100, 102): "0.00007837553213435505680151613303",
    (219, 231): "0.000004476389649788149305527412040",
    (220, 231): "0.00001309250690812691767461593005",
    (221, 231): "0.00002196916610539248383982347985",
    (222, 226): "0.000002803828492241390473652644905",
    (226, 230): "0.00001262590481226877742189101383",
}


class Cycle67ReserveDemandPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 160
        cls.paths = reserve_demand_paths(bits=160)

    def test_all_eleven_hard_starts_and_certified_first_successes(self):
        self.assertEqual(
            tuple((path.M, path.first_success) for path in self.paths),
            HARD_WINDOWS,
        )
        tolerance = arb("2e-30")
        for path in self.paths:
            final = path.rows[-1]
            self.assertGreaterEqual(final.direct_S, 0)
            self.assertLess(abs(final.direct_S - arb(EXPECTED_FINAL_S[(path.M, final.B)])), tolerance)
            self.assertTrue(all(row.direct_S < 0 for row in path.rows[:-1]))

    def test_independent_reserve_and_demand_paths_recombine_to_certificate(self):
        for path in self.paths:
            for row in path.rows:
                reserve_components = row.reserve_components
                components = row.components
                rebuilt_reserve = (
                    reserve_components.D_norm - reserve_components.projection
                    - reserve_components.W_M
                )
                rebuilt_theta = (
                    (components.N_U - components.V_D) / row.A
                    - components.projection - components.W_M
                )
                self.assertTrue(row.reserve.overlaps(rebuilt_reserve), row)
                self.assertTrue(row.theta.overlaps(rebuilt_theta), row)
                self.assertTrue(row.direct_S.overlaps(row.factored_S), row)
                self.assertTrue(row.identity_verified, row)
                self.assertGreater(row.A, 0)
                self.assertGreater(row.reserve, 0)

    def test_rank_one_reserve_decrements_and_reported_increments(self):
        for path in self.paths:
            for previous, row in zip(path.rows, path.rows[1:]):
                self.assertIsNotNone(row.reserve_payment)
                self.assertIsNotNone(row.demand_increment)
                self.assertGreater(row.reserve_payment, 0)
                self.assertTrue(
                    previous.reserve.overlaps(row.reserve + row.reserve_payment), row
                )
                self.assertTrue(
                    row.demand_increment.overlaps(row.theta - previous.theta), row
                )
                self.assertTrue(row.rank_one_verified, row)

    def test_certificate_digest_and_input_validation(self):
        self.assertEqual(len(CERTIFICATE_SHA256), 64)
        rows = load_surplus_certificate()
        self.assertIn(39, rows)
        self.assertIn(230, rows)
        with self.assertRaises(ValueError):
            reserve_demand_paths((), bits=160)


if __name__ == "__main__":
    unittest.main()
