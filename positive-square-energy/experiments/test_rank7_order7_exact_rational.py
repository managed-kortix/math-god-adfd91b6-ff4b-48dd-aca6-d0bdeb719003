#!/usr/bin/env python3

import importlib.util
import lzma
import tempfile
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order7_exact_rational.py")


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order7_exact_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExactRationalEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = load_engine()
        cls.census = cls.engine.load_census_module()
        cls.residuals = cls.engine.residual_rows(cls.census)

    def test_scope_and_atom_modes(self):
        self.assertEqual(len(self.residuals), 40964)
        indices = self.engine.atom_source_indices(self.residuals)
        self.assertEqual(len(indices), 20)
        for index in indices:
            targets = self.engine.atom_targets(self.census, self.residuals[index])
            self.assertTrue(targets)
            self.assertLess(len(targets), 14)

    def test_payload_free_modes_are_exact_and_restartable(self):
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
            output = directory / "merged.r7g.xz"
            raw, _, decoded = self.engine.base.merge_fragments(
                self.census, self.residuals, paths, 0, 3, output)
            self.assertEqual(decoded, records)
            self.assertEqual(raw[:4], b"R7G1")


if __name__ == "__main__":
    unittest.main()
