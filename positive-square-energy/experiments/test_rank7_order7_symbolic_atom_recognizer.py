#!/usr/bin/env python3

import importlib.util
import itertools
import unittest
from fractions import Fraction
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order7_symbolic_atom_recognizer.py")
SPEC = importlib.util.spec_from_file_location("recognizer", PATH)
recognizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recognizer)
F = Fraction


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

    def test_all_nine_census_k4_three_mixed_rows_have_exact_grams(self):
        payload = recognizer.load_census(recognizer.DEFAULT_CENSUS)
        kernels = {record["order_kernel"]: tuple(map(tuple, record["edges"]))
                   for record in payload["kernels"]}
        source_indices = set()
        decomposition_count = 0
        for source_index, source in enumerate(payload["residuals"]):
            records = recognizer.recognize(kernels[source["order_kernel"]],
                                           tuple(source["row"]))
            coupled = [record for record in records
                       if record["geometry"] == "coupled-K4+3M"]
            if not coupled:
                continue
            source_indices.add(source_index)
            decomposition_count += len(coupled)
            for record in coupled:
                self.assertEqual(record["status"], "exact-equality-owner")
                self.assertIn("gram_completion", record)
                gram = [[F(*value) for value in row] for row in record["gram_completion"]]
                self.assertTrue(recognizer.is_psd(gram))
                self.assertEqual([gram[i][i] for i in range(len(gram))], [1] * len(gram))
                for edge, value in record["prescribed"]:
                    self.assertEqual(gram[edge[0]][edge[1]], F(*value))
        self.assertEqual(source_indices,
                         {23745, 23766, 25672, 25693, 34346, 34350,
                          40482, 40483, 40484})
        self.assertEqual(decomposition_count, 11)

    def test_full_scan_has_no_open_coupled_decompositions(self):
        report = recognizer.scan_census(recognizer.load_census(recognizer.DEFAULT_CENSUS))
        self.assertEqual(report["recognized_candidate_row_total"], 20)
        self.assertEqual(report["exact_owner_row_total"], 20)
        self.assertEqual(report["geometry_owner_row_counts"]["coupled-K4+3M"], 9)
        self.assertEqual(report["decomposition_status_counts"], {"exact-equality-owner": 23})
        self.assertFalse(report["full_theorem"])


if __name__ == "__main__":
    unittest.main()
