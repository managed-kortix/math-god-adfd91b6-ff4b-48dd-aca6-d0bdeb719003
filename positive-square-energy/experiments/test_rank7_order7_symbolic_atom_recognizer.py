#!/usr/bin/env python3

import importlib.util
import itertools
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order7_symbolic_atom_recognizer.py")
SPEC = importlib.util.spec_from_file_location("recognizer", PATH)
recognizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recognizer)


class SymbolicAtomRecognizerTest(unittest.TestCase):
    def test_cost_six_profiles_are_complete(self):
        profiles = set()
        for mixed in range(7):
            profiles.update((mixed, profile) for profile in recognizer.simplex_profiles(6 - mixed))
        self.assertEqual(profiles, {
            (0, (3, 3, 3, 3, 3, 3)), (0, (3, 3, 3, 4)), (0, (4, 4)), (0, (5,)),
            (1, (3, 3, 3, 3, 3)), (1, (3, 3, 4)),
            (2, (3, 3, 3, 3)), (2, (3, 4)),
            (3, (3, 3, 3)), (3, (4,)), (4, (3, 3)), (5, (3,)), (6, ()),
        })

    def test_regular_k5_with_three_contractions(self):
        edges = [(u, v, 1) for u, v in itertools.combinations(range(5), 2)]
        edges += [(5, 6, 3)]
        row = [1] * 10 + [0]
        records = recognizer.recognize(tuple(edges), tuple(row))
        owners = [record for record in records if record["geometry"] == "regular-simplex-K5"]
        self.assertTrue(owners)
        self.assertEqual(owners[0]["status"], "exact-equality-owner")
        self.assertEqual(len(owners[0]["equality_frontiers"]), 4)

    def test_six_mixed_pairs_and_one_contraction(self):
        cycle = [(i, (i + 1) % 6, 2) for i in range(6)]
        edges = cycle + [(0, 6, 1)]
        records = recognizer.recognize(tuple(edges), (1,) * 6 + (0,))
        owners = [record for record in records if record["geometry"] == "six-mixed-pairs"]
        self.assertTrue(owners)
        self.assertEqual(owners[0]["equality_frontiers"], [None, 12])

    def test_incompatible_mixed_and_k4_edge_is_rejected(self):
        edges = [(u, v, 1) for u, v in itertools.combinations(range(4), 2)]
        edges[0] = (*edges[0][:2], 2)
        edges += [(4, 5, 2), (5, 6, 2), (4, 6, 2)]
        row = [1] * len(edges)
        self.assertFalse(recognizer.recognize(tuple(edges), tuple(row)))


if __name__ == "__main__":
    unittest.main()
