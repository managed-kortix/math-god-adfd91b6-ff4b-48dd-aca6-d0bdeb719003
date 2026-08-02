#!/usr/bin/env python3

import json
import unittest
from fractions import Fraction

from flint import arb

from verify_cycle243_small_nb import (
    DEFAULT_CERTIFICATE,
    complete_energy_parts,
    compute,
    verify_certificate,
)
from certify_complete_gram import RestrictedGram, complete_energies, mobius_sieve


class Cycle243SmallNBTests(unittest.TestCase):
    def test_dense_four_part_formula_matches_recurrence(self):
        parts, _ = compute(192)
        recurrence = complete_energies(6, 192)
        for N in (3, 6):
            self.assertTrue(parts[N].total.overlaps(recurrence[N]))

    def test_offdiagonal_is_present(self):
        mu = mobius_sieve(6)
        logs = [arb(0)] + [arb(n).log() for n in range(1, 7)]
        parts = complete_energy_parts(6, RestrictedGram(), mu, logs)
        self.assertFalse(parts.affine.contains(0))
        self.assertFalse(parts.offdiagonal.contains(0))

    def test_checked_in_certificate_proves_claim(self):
        certificate = json.loads(DEFAULT_CERTIFICATE.read_text())
        verify_certificate(certificate)
        p3_lower = Fraction(certificate["energies"]["3"]["total"]["lower"])
        p6_upper = Fraction(certificate["energies"]["6"]["total"]["upper"])
        self.assertLessEqual(p6_upper, Fraction(3, 4) * p3_lower)


if __name__ == "__main__":
    unittest.main()
