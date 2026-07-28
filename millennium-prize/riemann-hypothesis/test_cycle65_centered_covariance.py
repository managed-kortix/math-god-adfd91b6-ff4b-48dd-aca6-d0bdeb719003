#!/usr/bin/env python3

import unittest
from fractions import Fraction

from flint import arb, ctx

from verify_cycle65_centered_covariance import (
    SELECTED_N,
    centered_covariance,
    centered_covariance_values,
)


EXPECTED = {
    4: (
        "0.4062978136297426453742175845460618683",
        "0.2976861096117994637182977733151813080",
        "-0.3117606108328145043430286035039114944",
    ),
    64: (
        "0.057542079240533568252311856177338244",
        "-0.002287092518054619655551604948719619",
        "-0.069419518298677115949915437155614237",
    ),
    220: (
        "0.035368770055655040171143053401880443",
        "-0.00368615445051317825249211693425395",
        "-0.04360024452192088105488760354567388",
    ),
    8192: (
        "0.0238572362482736159285815624966659",
        "-0.010645349793251120043422117233157",
        "-0.036337758060622706428048415306489",
    ),
}


class Cycle65CenteredCovarianceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.rows = centered_covariance_values(bits=192)

    def test_selected_finite_values_and_negative_T(self):
        self.assertEqual(tuple(row.N for row in self.rows), SELECTED_N)
        tolerance = arb("5e-34")
        for row in self.rows:
            for value, expected in zip((row.A, row.C, row.T), EXPECTED[row.N]):
                self.assertLess(abs(value - arb(expected)), tolerance)
            self.assertTrue(row.negative_T_certified, row)
            self.assertLess(row.T, 0)

    def test_exact_rational_weights_and_arb_covariances(self):
        for row in self.rows:
            self.assertEqual(row.indices, tuple(range(row.N // 2, row.N)))
            self.assertEqual(
                row.weights,
                tuple(Fraction(1, k * (k + 1)) for k in row.indices),
            )
            direct_A = sum(
                (arb(weight.numerator) / weight.denominator * value * value
                 for weight, value in zip(row.weights, row.E)),
                arb(0),
            )
            direct_C = sum(
                (arb(weight.numerator) / weight.denominator * left * right
                 for weight, left, right in zip(row.weights, row.E, row.H)),
                arb(0),
            )
            self.assertTrue(row.A.overlaps(direct_A))
            self.assertTrue(row.C.overlaps(direct_C))

    def test_abel_and_square_decompositions(self):
        for row in self.rows:
            self.assertTrue(row.abel_identity_verified, row)
            self.assertTrue(row.square_identity_verified, row)
            self.assertTrue(row.decomposition_verified, row)
            self.assertTrue(row.A.overlaps(
                row.abel_A_boundary + row.abel_A_increments
            ))
            self.assertTrue(row.C.overlaps(
                row.abel_C_boundary + row.abel_C_increments
            ))
            self.assertTrue(row.C.overlaps(row.square_covariance))
            self.assertTrue(row.T.overlaps(row.square_T))
            self.assertGreater(row.A, 0)
            self.assertGreater(row.square_H, 0)
            self.assertGreater(row.square_difference, 0)

    def test_input_validation(self):
        for N in (2, 3, 5):
            with self.assertRaises(ValueError):
                centered_covariance(N)
        with self.assertRaises(ValueError):
            centered_covariance(4, (arb(0),) * 9)
        with self.assertRaises(ValueError):
            centered_covariance_values(())
        with self.assertRaises(ValueError):
            centered_covariance_values((4,), bits=79)


if __name__ == "__main__":
    unittest.main()
