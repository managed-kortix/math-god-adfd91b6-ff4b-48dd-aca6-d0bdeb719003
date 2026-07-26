#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve
from cycle41_h_event_analysis import h_event_rows
from cycle42_impulse_pairing_audit import fifo_pairs, lifo_pairs, pair_formula, replacement_map


class Cycle42ImpulsePairingAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.limit = 240
        cls.mu = mobius_sieve(cls.limit)
        cls.logs = [arb(0)] + [arb(n).log() for n in range(1, cls.limit + 2)]
        cls.gram = RestrictedGram()
        _, cls.rows = h_event_rows(cls.limit, 192)

    def test_replacement_map_preserves_positive_mobius_sign(self):
        for q in (39, 95, 219, 221, 226):
            image = replacement_map(q)
            self.assertEqual(self.mu[image], 1)
            self.assertLessEqual(image, q)

    def test_opened_pair_formula_equals_direct_impulse_sum(self):
        for pairing in (fifo_pairs, lifo_pairs):
            pairs, _ = pairing(self.rows)
            for q, r in pairs:
                direct, opened = pair_formula(q, r, self.mu, self.logs, self.gram)
                self.assertTrue(direct.overlaps(opened), (pairing.__name__, q, r))

    def test_selected_lifo_pairs(self):
        pairs, _ = lifo_pairs(self.rows)
        selected = [(q, r) for q, r in pairs if q in (39, 95, 219, 221, 226)]
        self.assertEqual(selected, [(39, 41), (95, 97), (221, 222), (219, 223), (226, 227)])


if __name__ == "__main__":
    unittest.main()
