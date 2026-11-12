#!/usr/bin/env python3
"""Hostile unit gates for the exact order-nine upstream owner replayer."""
from __future__ import annotations

import copy
import importlib.util
import json
import lzma
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

    def assert_rejected(self, function, *args, **kwargs):
        with self.assertRaises(RuntimeError):
            function(*args, **kwargs)

    def test_strict_json_and_rationals_fail_closed(self):
        m = self.module
        self.assert_rejected(m.strict_json, b'{"x":1,"x":2}\n', "duplicate")
        self.assert_rejected(m.strict_json, b'{"x":NaN}\n', "constant")
        self.assert_rejected(m.strict_json, b'{"x":1.25}\n', "float")
        self.assert_rejected(m.strict_json, b'{"x":1e999}\n', "overflow float")
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

    def first_payload(self, path, parser):
        with lzma.open(path, "rb") as rows:
            return parser(rows.readline(), path.name)

    def test_sos_payload_mutation_gates(self):
        m = self.module
        kernels = m.load_kernels()
        payload = self.first_payload(m.SOS_OWNERS, m.strict_json)
        source = {payload[0][0]: payload[0]}
        valid = m.replay_sos_payload(payload, kernels, source, set())
        self.assertEqual(valid["source_index"], payload[0][0])
        self.assertLessEqual(valid["cost"], m.BUDGET)

        def rejected(mutator, *, seen=(), source_records=None, previous_source=-1):
            mutated = copy.deepcopy(payload)
            mutator(mutated)
            self.assert_rejected(
                m.replay_sos_payload, mutated, kernels,
                source if source_records is None else source_records, set(seen),
                previous_remainder_index=-1,
                previous_source_index=previous_source)

        rejected(lambda value: value[0].__setitem__(0, value[0][0] + 1))
        rejected(lambda value: value[1].__setitem__(1, value[1][1] + 1))
        rejected(lambda value: value[1][5][0][0].__setitem__(0,
                                                            value[1][5][0][0][0] + 1))
        rejected(lambda value: value[1][6].__setitem__(0, value[1][6][0] + 1))
        rejected(lambda value: value[1][5][0][0].__setitem__(1, 0))
        rejected(lambda value: None, seen=(payload[0][0],))
        rejected(lambda value: None, previous_source=payload[0][0])
        rejected(lambda value: value[0].__setitem__(4, True))
        rejected(lambda value: None, source_records={})

    def test_dominant_float_is_actually_diagnostic_only(self):
        m = self.module
        kernels = m.load_kernels()
        payload = self.first_payload(m.DOMINANT_OWNERS, m.dominant_json)
        source = {payload[0][0]: payload[0]}

        exact_results = []
        for diagnostic in (-1e300, 0, 1e300):
            mutated = copy.deepcopy(payload)
            mutated[2] = diagnostic
            result = m.replay_dominant_payload(
                mutated, kernels, source, set(), 256)
            exact_results.append(result)
        self.assertEqual(exact_results[0], exact_results[1])
        self.assertEqual(exact_results[1], exact_results[2])
        self.assertNotIn("diagnostic", exact_results[0])

        for diagnostic in (True, math.nan, math.inf, -math.inf):
            mutated = copy.deepcopy(payload)
            mutated[2] = diagnostic
            self.assert_rejected(
                m.replay_dominant_payload, mutated, kernels, source, set(), 256)
        self.assert_rejected(m.dominant_json, b'[[],[],1.5,[2.5]]\n', "nested float")
        self.assert_rejected(m.dominant_json, b'[[],[],1e999,[]]\n', "infinite float")

        for mutator in (
            lambda value: value[0].__setitem__(0, value[0][0] + 1),
            lambda value: value[1].__setitem__(0, value[1][0] + 1),
            lambda value: value[1][2].__setitem__(0, value[1][2][0] + 1),
            lambda value: value[1][3][0][0].__setitem__(0,
                                                       value[1][3][0][0][0] + 1),
            lambda value: value[1][3][0][0].__setitem__(1, 0),
            lambda value: value.__setitem__(3, []),
        ):
            mutated = copy.deepcopy(payload)
            mutator(mutated)
            self.assert_rejected(
                m.replay_dominant_payload, mutated, kernels, source, set(), 256)
        self.assert_rejected(
            m.replay_dominant_payload, payload, kernels, source,
            {payload[0][0]}, 256)
        self.assert_rejected(
            m.replay_dominant_payload, payload, kernels, source, set(), 256,
            previous_source_index=payload[0][0])

    def test_canonical_output_and_no_numerical_dependencies(self):
        m = self.module
        payload = {"z": 1, "a": [2, 3]}
        self.assertEqual(m.canonical_bytes(payload), b'{"a":[2,3],"z":1}\n')
        self.assertEqual(m.SOS_OWNER_PHYSICAL, 134899)
        self.assertEqual(m.UPSTREAM_OWNER_PHYSICAL, 136072)
        source = MODULE.read_text(encoding="utf-8")
        self.assertNotIn("numpy", source)
        self.assertNotIn("scipy", source)
        self.assertNotIn("networkx", source)
        self.assertNotIn("assert ", source)
        self.assertNotIn("write_bytes", source)
        self.assertNotIn("open(temporary", source)


if __name__ == "__main__":
    unittest.main()
