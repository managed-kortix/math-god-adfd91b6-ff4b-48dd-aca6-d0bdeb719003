#!/usr/bin/env python3

import importlib.util
import lzma
import tempfile
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order8_exact_rational.py")


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_exact_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExactRationalEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = load_engine()
        cls.census = cls.engine.load_census_module()
        cls.residuals = cls.engine.residual_rows(cls.census)

    def test_authenticated_rational_search_scope(self):
        self.assertEqual(len(self.residuals), 492812)
        self.assertEqual(self.residuals[0][1], 0)
        self.assertEqual(len(self.engine.base.path_ledger(self.census, self.residuals[0])), 14)
        self.assertEqual(self.engine.atom_source_indices(self.residuals), frozenset())

    def test_fraction_replay_and_restartable_fragments(self):
        records = ((self.engine.base.MODE_UNRESOLVED, None),) * 3
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for start, stop in ((0, 2), (2, 3)):
                raw = self.engine.base.encode_pack(self.census, start, records[start:stop])
                path = self.engine.fragment_path(directory, start, stop)
                path.write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ))
            cursor, paths = self.engine.base.load_fragments(
                self.census, self.residuals, directory, 0, 3, 2)
            self.assertEqual(cursor, 3)
            output = directory / "merged.r7o8g.xz"
            raw, _, decoded = self.engine.base.merge_fragments(
                self.census, self.residuals, paths, 0, 3, output)
            self.assertEqual(decoded, records)
            self.assertEqual(raw[:6], b"R7O8G1")

    def test_canonical_binary_census_cache(self):
        raw = self.engine.cache_bytes(self.census, self.residuals)
        self.assertEqual(self.engine.decode_cache(self.census, raw), self.residuals)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "census.r7o8c.xz"
            path.write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ, preset=3))
            self.engine._RESIDUALS = None
            self.assertEqual(self.engine.residual_rows(self.census, cache_path=path), self.residuals)

    def test_accelerated_objective_is_base_identical(self):
        paths = self.engine.base.path_ledger(self.census, self.residuals[0])
        vectors = self.engine.base.random_vectors(__import__("random").Random(17))
        expected_value, expected_gradient = self.engine.base._r10_objective_gradient(paths, vectors)
        self.assertEqual(self.engine.objective(paths, vectors), self.engine.base._r10_objective(paths, vectors))
        self.assertEqual(self.engine.objective_gradient(paths, vectors),
                         (expected_value, expected_gradient))

    def test_shard_expansion(self):
        arguments = self.engine.expand_shard_arguments(
            ["--output", "out.xz", "--shard-index", "2", "--shard-count", "99",
             "--shard-rows", "5000"])
        self.assertEqual(arguments[-4:], ["--start", "10000", "--count", "5000"])

    def test_baseline_pack_artifact_identity(self):
        path = PATH.with_name("rank7_order8_chunk_000000_005000.r7o8g.xz")
        self.assertEqual(__import__("hashlib").sha256(path.read_bytes()).hexdigest(),
                         "2f3773dc99c930f9aeacff1e3566e037eb6d7d106d866e81a829c1b53797a2ee")


if __name__ == "__main__":
    unittest.main()
