#!/usr/bin/env python3

import importlib.util
import lzma
import tempfile
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order7_pack_auditor.py")


def load_auditor():
    spec = importlib.util.spec_from_file_location("rank7_order7_auditor_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RankSevenOrderSevenPackAuditorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.auditor = load_auditor()
        cls.stream, cls.census, cls.residuals = cls.auditor.load_scope(
            "rank7_order7_test_scope")

    def test_symbolic_dictionary_is_exactly_materialized(self):
        dictionary, keys, dictionary_digest, target_digest = (
            self.auditor.symbolic_owner_dictionary(
                self.stream, self.census, self.residuals))
        self.assertEqual(len(dictionary), 20)
        self.assertEqual(len(keys), 61)
        self.assertEqual(dictionary_digest,
                         "b28fa781036119f3139f0bf49f2d9d8fcbb9ac513768883c3e8e628c0c8c2f12")
        self.assertEqual(target_digest,
                         "11931376eab8ba76a702282cbb82ef08355bbc057b5d07b8b90c5eb7173ab8d2")
        self.assertEqual({entry["source_index"] for entry in dictionary},
                         {5727, 6510, 6829, 23745, 23766, 25672, 25693, 33744,
                          34346, 34350, 38426, 38430, 38942, 39591, 40022, 40282,
                          40482, 40483, 40484, 40882})
        self.assertTrue(all(0 in entry["targets"] and len(entry["targets"]) < 14
                            for entry in dictionary))

    def test_partial_manifest_is_bound_but_not_complete(self):
        records = ((self.stream.base.MODE_UNRESOLVED, None),) * 3
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            packs = []
            for start, stop in ((0, 2), (2, 3)):
                raw = self.stream.base.encode_pack(
                    self.census, start, records[start:stop])
                path = directory / f"chunk-{start}-{stop}.r7g.xz"
                path.write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ))
                packs.append(path)
            manifest_path = directory / "manifest.json"
            manifest = self.auditor.build_manifest(manifest_path, packs)
            self.assertEqual(manifest["covered_residual_range"], [0, 3])
            self.assertEqual(manifest["symbolic_owner_row_total"], 20)
            self.assertEqual(manifest["symbolic_exact_target_total"], 61)
            self.assertEqual(len(manifest["symbolic_owners"]), 20)
            self.assertEqual(len(manifest["symbolic_exact_targets"]), 61)
            report, complete = self.auditor.audit(manifest_path, exact=False)
            self.assertFalse(complete)
            self.assertEqual(report["manifest_covered_residual_range"], [0, 3])
            self.assertFalse(report["theorem_gate_eligible"])

    def test_k2763_direct_spectral_frontiers(self):
        dictionary, keys, digest = self.auditor.direct_spectral_owner_dictionary(
            self.stream, self.census, self.residuals)
        self.assertEqual(keys, {(28385, None), (28385, 10)})
        self.assertEqual([entry["target_order"] for entry in dictionary], [7, 9])
        self.assertTrue(all(entry["all_length_rooted_tree_lift"]
                            for entry in dictionary))
        self.assertTrue(all(entry["packet"] ==
                            "two-actual-K4-one-sum-plus-open-45-path-with-rational-routing"
                            for entry in dictionary))


if __name__ == "__main__":
    unittest.main()
