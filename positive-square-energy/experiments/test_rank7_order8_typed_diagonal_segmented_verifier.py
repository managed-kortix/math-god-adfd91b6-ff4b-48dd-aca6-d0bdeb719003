#!/usr/bin/env python3

import base64
import importlib.util
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace


PATH = Path(__file__).with_name("rank7_order8_typed_diagonal_segmented_verifier.py")
SPEC = importlib.util.spec_from_file_location("typed_segmented_test", PATH)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class TypedDiagonalSegmentedVerifierTest(unittest.TestCase):
    def test_bitmap_round_trip_and_padding(self):
        values = (True, False, True, True, False, False, True, False, True)
        encoded = verifier.bitmap_encode(values)
        self.assertEqual(verifier.bitmap_decode(encoded, len(values)), values)
        raw = bytearray(base64.b64decode(encoded))
        raw[-1] |= 0x80
        with self.assertRaises(RuntimeError):
            verifier.bitmap_decode(base64.b64encode(raw).decode("ascii"), len(values))

    def test_exact_certificate_checks_psd_formula_and_all_frontiers(self):
        class Base:
            @staticmethod
            def path_ledger(census, source):
                return tuple((0, occurrence, 0, 1, 4) for occurrence in range(14))

        engine = SimpleNamespace(base=Base(), BUDGET=Fraction(6))
        census = SimpleNamespace(PAIRS=((0, 1),))
        source = (0, 3, (0,), (1,), (0,), 1, None, False)
        type_keys = tuple((index, ()) for index in range(verifier.ORDER))
        type_ids = tuple(range(verifier.ORDER))
        parameters = tuple((Fraction(1), Fraction(0)) for _ in range(verifier.ORDER))
        result = (Fraction(7, 2), Fraction(0), Fraction(1), type_keys, type_ids, parameters)
        accepted, cost, worst = verifier.exact_certificate(
            None, engine, census, source, result)
        self.assertTrue(accepted)
        self.assertEqual(cost, Fraction(7, 2))
        self.assertEqual(worst, Fraction(7, 2))

    def test_receipt_rejects_coverage_digest_mutation(self):
        residuals = ((0, 10, (), (), (), 1, None, False),
                     (0, 12, (), (), (), 1, None, False))
        census = SimpleNamespace(SOURCE_SHA256="1" * 64)
        values = (True, False)
        encoded = verifier.bitmap_encode(values)
        digest = __import__("hashlib").sha256()
        for index, accepted in enumerate(values):
            digest.update(verifier.canonical_bytes([index, residuals[index][1], accepted]))
        receipt = {
            "schema": verifier.RECEIPT_SCHEMA,
            "source_stream_sha256": census.SOURCE_SHA256,
            "row_range": [0, 2],
            "row_total": 2,
            "first_source_index": 10,
            "last_source_index": 12,
            "search": {},
            "verified": {"rational_feature_formula_rows": 2,
                         "exact_psd_decomposition_rows": 2,
                         "exact_frontier_cost_total": 30},
            "typed_owner_total": 1,
            "unowned_total": 1,
            "ownership_bitmap_base64": encoded,
            "ownership_bitmap_sha256": __import__("hashlib").sha256(
                base64.b64decode(encoded)).hexdigest(),
            "coverage_stream_sha256": digest.hexdigest(),
        }
        verifier.validate_receipt(receipt, census, residuals)
        receipt["coverage_stream_sha256"] = "0" * 64
        with self.assertRaises(RuntimeError):
            verifier.validate_receipt(receipt, census, residuals)


if __name__ == "__main__":
    unittest.main()
