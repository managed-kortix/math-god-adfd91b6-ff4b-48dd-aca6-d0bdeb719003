#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from certify_complete_gram import (
    RestrictedGram,
    adaptive_chain,
    block_ratio,
    complete_energies,
)


class CompleteGramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def test_full_to_restricted_rank_one_tail(self):
        gram = RestrictedGram()
        expected = gram.c0 / 2 - arb(1) / 4
        self.assertTrue(gram.entry(2, 2).contains(expected))

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
        self.assertTrue(ratio > arb("0.1"))
        blocks, failure = adaptive_chain(energies, 2, 8, "0.1")
        self.assertIsNone(failure)
        self.assertEqual(blocks[0].start, 2)
        self.assertEqual(blocks[-1].stop, 8)

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


if __name__ == "__main__":
    unittest.main()
