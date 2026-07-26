#!/usr/bin/env python3

import gzip
import json
import tempfile
import unittest
from pathlib import Path

from flint import ctx

from cycle40_complete_diagnostics import local_diagnostics
from cycle41_local_scan import (
    cumulative_scan,
    scan_values,
    write_certificate,
)


class Cycle41LocalScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.energies, cls.local, _ = scan_values(16, 192, 1, 4)

    def test_parallel_recurrence_matches_cycle40(self):
        expected = local_diagnostics(self.energies)
        self.assertEqual(len(self.local), len(expected))
        for actual, old in zip(self.local, expected):
            self.assertEqual(actual[0], old["n"])
            self.assertTrue(actual[2].overlaps(old["kappa_n"]))
            self.assertTrue(actual[3].overlaps(old["half_surplus"]))

    def test_linear_cumulative_scan_matches_exhaustive(self):
        rows = cumulative_scan(self.local)
        for a, stop, minimum in rows:
            total = 0
            candidates = []
            for n, _, _, surplus in self.local[a - 2:]:
                total += surplus
                candidates.append((n + 1, total))
            direct_stop, direct_minimum = min(
                candidates, key=lambda item: float(item[1].mid())
            )
            self.assertEqual(stop, direct_stop)
            self.assertTrue(minimum.overlaps(direct_minimum))

    def test_compressed_certificate_is_parseable(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.jsonl.gz"
            digest = write_certificate(path, self.local)
            self.assertEqual(len(digest), 64)
            with gzip.open(path, "rt", encoding="ascii") as handle:
                rows = [json.loads(line) for line in handle]
            self.assertEqual(rows[0]["n"], 2)
            self.assertEqual(len(rows), len(self.local))


if __name__ == "__main__":
    unittest.main()
