#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from verify_cycle63_complete_tail import WINDOWS, complete_tail_values


PUBLISHED = {
    (98, 99): (
        "0.030162988363064539935",
        "0.045615062017116374369",
        "0.075778050380180914304",
    ),
    (219, 231): (
        "0.026726387237328858507",
        "0.031679021351980235849",
        "0.058405408589309094356",
    ),
    (220, 231): (
        "0.027337641721077888943",
        "0.031062663964177908238",
        "0.058400305685255797182",
    ),
    (222, 226): (
        "0.028763566006604881443",
        "0.033116652858458946834",
        "0.061880218865063828278",
    ),
}


class Cycle63CompleteTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.rows = complete_tail_values(bits=192)

    def test_four_published_windows(self):
        self.assertEqual(tuple((row.M, row.B) for row in self.rows), WINDOWS)
        tolerance = arb("5e-21")
        for row in self.rows:
            expected = PUBLISHED[(row.M, row.B)]
            actual = (row.omega_infinity, row.boundary_schur, row.full_R)
            for value, published in zip(actual, expected):
                self.assertLess(abs(value - arb(published)), tolerance)

    def test_full_R_boundary_identity_and_direct_projection(self):
        for row in self.rows:
            self.assertTrue(
                row.full_R.overlaps(row.omega_infinity + row.boundary_schur)
            )
            self.assertTrue(row.identity_residual.contains(0), row)
            self.assertTrue(row.full_R.overlaps(row.direct_full_R), row)
            self.assertGreater(row.omega_infinity, 0)
            self.assertGreater(row.boundary_schur, 0)


if __name__ == "__main__":
    unittest.main()
