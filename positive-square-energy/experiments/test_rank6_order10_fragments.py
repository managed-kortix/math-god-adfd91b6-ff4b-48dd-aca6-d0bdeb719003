#!/usr/bin/env python3
"""Fast format-level tests for restartable R10G1 fragment generation."""

import importlib.util
import lzma
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


HERE = Path(__file__).resolve().parent
STREAM_PATH = HERE / "rank6_order10_cubic_exact_rational.py"


def load_stream():
    spec = importlib.util.spec_from_file_location("rank6_order10_fragment_test_stream", STREAM_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FragmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stream = load_stream()
        cls.census = SimpleNamespace(SOURCE_SHA256="11" * 32, PAIRS=((0, 1),))
        cls.residuals = tuple((0, None, (0,), (15,), (0,), 1, 0, False)
                              for _ in range(7))

    def write_fragment(self, directory, start, stop):
        records = ((self.stream.MODE_UNRESOLVED, None),) * (stop - start)
        raw = self.stream.encode_pack(self.census, start, records)
        path = self.stream.fragment_path(directory, start, stop)
        path.write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6))
        return path

    def test_resume_and_merge_are_exact_and_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            paths = (self.write_fragment(directory, 1, 3),
                     self.write_fragment(directory, 3, 5),
                     self.write_fragment(directory, 5, 6))
            cursor, loaded = self.stream.load_fragments(
                self.census, self.residuals, directory, 1, 6, 2)
            self.assertEqual((cursor, loaded), (6, paths))

            output = directory / "merged.r10g.xz"
            raw, stored, records = self.stream.merge_fragments(
                self.census, self.residuals, loaded, 1, 6, output)
            expected_records = ((self.stream.MODE_UNRESOLVED, None),) * 5
            self.assertEqual(records, expected_records)
            self.assertEqual(raw, self.stream.encode_pack(self.census, 1, expected_records))
            self.assertEqual(stored, output.read_bytes())
            self.assertEqual(self.stream.exact_decode_pack(
                self.census, lzma.decompress(stored), self.residuals),
                (1, expected_records))

    def test_resume_rejects_a_gap(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            self.write_fragment(directory, 1, 3)
            self.write_fragment(directory, 4, 6)
            with self.assertRaisesRegex(RuntimeError, "gap"):
                self.stream.load_fragments(
                    self.census, self.residuals, directory, 1, 6, 2)

    def test_exact_decoder_rejects_noncanonical_header_varints(self):
        records = ((self.stream.MODE_UNRESOLVED, None),)
        raw = self.stream.encode_pack(self.census, 0, records)
        header = len(self.stream.MAGIC) + 32
        noncanonical = raw[:header] + b"\x80\x00" + raw[header + 1:]
        with self.assertRaisesRegex(RuntimeError, "noncanonical"):
            self.stream.exact_decode_pack(self.census, noncanonical, self.residuals)


if __name__ == "__main__":
    unittest.main()
