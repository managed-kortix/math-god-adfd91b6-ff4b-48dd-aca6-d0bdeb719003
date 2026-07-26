#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from diagnose_log_asymptotic import fit_window


class LogAsymptoticDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_exact_two_term_profile_is_recovered(self):
        c = arb("0.046")
        d = arb("2.55")
        values = {}
        for n in range(32, 129):
            inverse_log = 1 / arb(n).log()
            values[n] = c * inverse_log + d * inverse_log ** 2
        for scaled in (False, True):
            fit = fit_window(values, 32, 128, scaled=scaled)
            self.assertTrue(fit["c"].contains(c))
            self.assertTrue(fit["d"].contains(d))
            self.assertTrue(fit["rms"].contains(arb(0)))

    def test_unit_second_coefficient_shift(self):
        restricted = {}
        full = {}
        for n in range(64, 257):
            inverse_log = 1 / arb(n).log()
            restricted[n] = arb("0.046") * inverse_log + arb("2.55") * inverse_log ** 2
            full[n] = restricted[n] + inverse_log ** 2
        for scaled in (False, True):
            restricted_fit = fit_window(restricted, 64, 256, scaled=scaled)
            full_fit = fit_window(full, 64, 256, scaled=scaled)
            self.assertTrue((full_fit["c"] - restricted_fit["c"]).contains(arb(0)))
            self.assertTrue((full_fit["d"] - restricted_fit["d"]).contains(arb(1)))


if __name__ == "__main__":
    unittest.main()
