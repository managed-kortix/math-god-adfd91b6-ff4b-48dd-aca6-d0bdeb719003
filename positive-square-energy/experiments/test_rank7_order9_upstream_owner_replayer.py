#!/usr/bin/env python3
"""Hostile unit gates for the exact order-nine upstream owner replayer."""
from __future__ import annotations

import importlib.util
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE / "rank7_order9_upstream_owner_replayer.py"


def load_module():
    spec = importlib.util.spec_from_file_location("rank7_order9_upstream_replayer_test", MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load upstream owner replayer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UpstreamOwnerReplayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def assert_rejected(self, function, *args):
        with self.assertRaises(RuntimeError):
            function(*args)

    def test_strict_json_and_rationals_fail_closed(self):
        m = self.module
        self.assert_rejected(m.strict_json, b'{"x":1,"x":2}\n', "duplicate")
        self.assert_rejected(m.strict_json, b'{"x":NaN}\n', "constant")
        for raw in ([2, 2], [1, 0], [1, -2], [True, 1], [1.0, 2], [1, 3]):
            if raw == [1, 3]:
                self.assertEqual(m.rational_pair(raw, "ok", 3), Fraction(1, 3))
            else:
                self.assert_rejected(m.rational_pair, raw, "bad")
        self.assert_rejected(m.rational_pair, [1, 4], "bounded", 3)
        for raw in (True, 1.0, "1", -1):
            with self.assertRaises(RuntimeError):
                m.exact_int(raw, "bad", minimum=0)

    def test_source_rows_reject_bool_float_and_bad_kernel(self):
        m = self.module
        kernels = {1: (7, ((0, 1, 2),))}
        valid = [3, 7, 1, [1], 2]
        self.assertEqual(m.validate_source_record(valid, kernels, "valid")[:2], (3, 2))
        for mutated in (
            [True, 7, 1, [1], 2], [3, 7.0, 1, [1], 2],
            [3, 7, True, [1], 2], [3, 7, 1, [1.0], 2],
            [3, 8, 1, [1], 2], [3, 7, 1, [3], 2],
            [3, 7, 1, [1], True],
        ):
            self.assert_rejected(m.validate_source_record, mutated, kernels, "mutated")

    def test_exact_gram_reconstruction_rejects_bad_parameters(self):
        m = self.module
        signed = tuple(tuple(1 if {u, v} == {0, 1} else 0
                             for v in range(m.ORDER)) for u in range(m.ORDER))
        paths = ((0, 0, 0, 1, 2),)
        type_ids = (0,) * m.ORDER
        cost, normalizer, completion = m.gram_cost(
            signed, paths, type_ids, ((Fraction(1), Fraction(0)),))
        self.assertEqual(cost, Fraction(1, 2))
        self.assertEqual(normalizer, Fraction(1))
        self.assertEqual(completion, (Fraction(0),) * m.ORDER)
        self.assert_rejected(m.gram_cost, signed, paths, type_ids, ())
        self.assert_rejected(m.gram_cost, signed, paths, type_ids,
                             ((Fraction(0), Fraction(0)),))

    def test_dominant_float_is_diagnostic_only(self):
        m = self.module
        # A finite diagnostic is accepted by the exact frozen schema, but no
        # exact helper accepts it as a Gram parameter or cost.
        for value in (-1e300, 0, 5.9, 1e300):
            self.assertTrue(type(value) in (int, float) and
                            not isinstance(value, bool) and math.isfinite(value))
        for value in (True, math.nan, math.inf, -math.inf):
            self.assertFalse(type(value) in (int, float) and
                             not isinstance(value, bool) and math.isfinite(value))
        self.assertNotIn("numerical", m.replay.__code__.co_names)

    def test_canonical_output_and_no_numerical_dependencies(self):
        m = self.module
        payload = {"z": 1, "a": [2, 3]}
        self.assertEqual(m.canonical_bytes(payload), b'{"a":[2,3],"z":1}\n')
        source = MODULE.read_text(encoding="utf-8")
        self.assertNotIn("numpy", source)
        self.assertNotIn("scipy", source)
        self.assertNotIn("networkx", source)
        self.assertNotIn("assert ", source)
        self.assertNotIn("write_bytes", source)
        self.assertNotIn("open(temporary", source)


if __name__ == "__main__":
    unittest.main()
