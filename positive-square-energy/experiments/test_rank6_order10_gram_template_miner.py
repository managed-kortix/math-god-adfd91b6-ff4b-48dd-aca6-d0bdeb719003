#!/usr/bin/env python3
"""Unit tests for exact R10 branch-Gram canonicalization."""

from __future__ import annotations

import importlib.util
import random
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank6_order10_gram_template_miner.py")
SPEC = importlib.util.spec_from_file_location("rank6_order10_gram_template_tested", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CanonicalGramTest(unittest.TestCase):
    def test_signed_permutation_invariance(self):
        gram = (
            (Fraction(1), Fraction(1, 3), Fraction(-1, 5), Fraction(0)),
            (Fraction(1, 3), Fraction(1), Fraction(2, 7), Fraction(1, 4)),
            (Fraction(-1, 5), Fraction(2, 7), Fraction(1), Fraction(-1, 6)),
            (Fraction(0), Fraction(1, 4), Fraction(-1, 6), Fraction(1)),
        )
        expected = MODULE.canonical_gram(gram)
        generator = random.Random(413)
        for _ in range(30):
            permutation = list(range(4))
            generator.shuffle(permutation)
            signs = [generator.choice((-1, 1)) for _ in range(4)]
            image = tuple(tuple(Fraction(signs[i] * signs[j])
                                * gram[permutation[i]][permutation[j]]
                                for j in range(4)) for i in range(4))
            self.assertEqual(MODULE.canonical_gram(image), expected)

    def test_uniform_balanced_fast_path(self):
        signs = (1, -1, -1, 1, -1, 1, 1, -1, 1, -1)
        gram = tuple(tuple(Fraction(1) if i == j else Fraction(signs[i] * signs[j], 2)
                           for j in range(10)) for i in range(10))
        canonical = MODULE.canonical_gram(gram)
        self.assertEqual(len(canonical), 45)
        self.assertEqual(set(canonical), {(1, 2)})

    def test_balanced_rank_one_recognizer(self):
        census = type("Census", (), {"PAIRS": ((0, 1), (1, 2), (0, 2))})
        source = (0, None, (0, 1, 2), (1, 1, 1), (1, 0, 1), 1, 0, False)
        self.assertTrue(MODULE.load_stream().balanced_rank_one_certified(census, source))
        source = (0, None, (0, 1, 2), (1, 1, 1), (1, 0, 0), 1, 0, False)
        self.assertFalse(MODULE.load_stream().balanced_rank_one_certified(census, source))


if __name__ == "__main__":
    unittest.main()
