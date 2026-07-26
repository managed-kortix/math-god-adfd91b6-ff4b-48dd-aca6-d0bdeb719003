#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from certify_complete_gram import (
    RestrictedGram,
    adaptive_chain,
    block_ratio,
    complete_energies,
    maximal_ratios,
    weighted_prefixes,
)
from analyze_cycle40_h import first_nonnegative_blocks, h_values


class CompleteGramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_full_to_restricted_rank_one_tail(self):
        gram = RestrictedGram()
        expected = gram.c0 / 2 - arb(1) / 4
        self.assertTrue(gram.entry(2, 2).contains(expected))

    def test_vasyunin_reflection(self):
        gram = RestrictedGram()
        self.assertTrue(gram.v(2, 7).overlaps(-gram.v(5, 7)))

    def test_small_exact_norms(self):
        energies = complete_energies(3)
        gamma = arb.const_euler()
        n2 = 3 + (2 * arb.pi()).log() - 3 * gamma - arb(1)
        self.assertTrue(energies[2].overlaps(n2))

        r = (arb(3) / 2).log() / arb(3).log()
        a = 1 - r / 2
        full_n3 = (
            1 - arb(2).log()
            + a * (2 - arb.pi().log() - gamma)
            + 2 * a * a * ((2 * arb.pi()).log() - gamma)
        )
        tail = (1 - r / 2) ** 2
        self.assertTrue(energies[3].overlaps(full_n3 - tail))

    def test_block_ratio_and_first_passage(self):
        energies = complete_energies(8)
        ratio = block_ratio(energies, 2, 4)
        fast_ratio = block_ratio(energies, 2, 4, weighted_prefixes(energies))
        self.assertTrue(ratio.overlaps(fast_ratio))
        self.assertTrue(ratio > arb("0.1"))
        blocks, failure = adaptive_chain(energies, 2, 8, "0.1")
        self.assertIsNone(failure)
        self.assertEqual(blocks[0].start, 2)
        self.assertEqual(blocks[-1].stop, 8)

    def test_maximal_ratios_match_exhaustive_scan(self):
        energies = complete_energies(12)
        maxima = maximal_ratios(energies, 2, 12)
        self.assertEqual([item.start for item in maxima], list(range(2, 12)))
        for item in maxima:
            for b in range(item.start + 1, 13):
                candidate = block_ratio(energies, item.start, b)
                self.assertTrue(item.ratio.upper() >= candidate.upper())

    def test_recurrence_matches_dense_gram(self):
        energies = complete_energies(8)
        gram = RestrictedGram()
        mu = (0, 1, -1, -1, 0, -1, 1, -1, 0)
        for N in range(2, 9):
            log_N = arb(N).log()
            coefficients = [
                arb(mu[a]) * (1 - arb(a).log() / log_N)
                for a in range(1, N + 1)
            ]
            dense = arb(1)
            dense += 2 * sum(
                (coefficients[a - 1] * gram.chi_cross(a)
                 for a in range(1, N + 1)),
                arb(0),
            )
            dense += sum(
                (coefficients[a - 1] * coefficients[b - 1] * gram.entry(a, b)
                 for a in range(1, N + 1)
                 for b in range(1, N + 1)),
                arb(0),
            )
            self.assertTrue(energies[N].overlaps(dense))

    def test_cycle40_h_matches_normalized_energy_difference(self):
        energies = complete_energies(12)
        values = h_values(11)
        for n, value in values.items():
            log_n = arb(n).log()
            log_next = arb(n + 1).log()
            expected = -(log_n * log_next / (log_next - log_n)) * (
                log_next * energies[n + 1] - log_n * energies[n]
            )
            self.assertTrue(value.overlaps(expected))

    def test_cycle40_small_weighted_blocks(self):
        blocks = first_nonnegative_blocks(h_values(8))
        self.assertEqual(blocks[2][0], 6)
        self.assertTrue(all(endpoint is not None for endpoint, _ in blocks.values()))


if __name__ == "__main__":
    unittest.main()
