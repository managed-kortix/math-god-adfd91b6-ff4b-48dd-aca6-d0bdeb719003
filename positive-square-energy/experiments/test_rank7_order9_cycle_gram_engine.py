#!/usr/bin/env python3
"""Hostile regression tests for the historical order-nine cycle-Gram verifier."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

HERE = Path(__file__).resolve().parent
ENGINE = HERE / "rank7_order9_cycle_gram_engine.py"


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order9_cycle_gram_engine",
                                                  ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_owner_copy(engine, source, directory, mutate):
    with lzma.open(source, "rb") as stream:
        rows = list(stream)
    payload = json.loads(rows[0].decode("ascii"))
    mutate(payload)
    rows[0] = engine.canonical_bytes(payload)
    path = Path(directory) / source.name
    with lzma.open(path, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        output.writelines(rows)
    return path


def adjusted_expected(engine, lane, path):
    expected = copy.deepcopy(lane)
    digest = hashlib.sha256()
    physical = total = 0
    with lzma.open(path, "rb") as stream:
        for raw in stream:
            payload = json.loads(raw.decode("ascii"))
            digest.update(raw)
            total += 1
            physical += payload[0][4]
    expected["owner_stream"] = {
        "artifact_sha256": engine.file_sha256(path),
        "physical_total": physical,
        "raw_sha256": digest.hexdigest(),
        "record_total": total,
        "target_total": total * engine.TARGETS_PER_ROW,
    }
    return expected


def test_historical_streams_replay_exactly():
    engine = load_engine()
    result = engine.audit_historical(sorted(engine.HISTORICAL_LANES))
    assert result == {
        "fourth": {
            "artifact_sha256": "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
            "physical_total": 1283,
            "raw_sha256": "a347d2d7891609156692d0bf0614783d79a9b84c6f4e0902ef6672f1cb4c96f5",
            "record_total": 1036,
            "target_total": 16576,
        },
        "third": {
            "artifact_sha256": "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
            "physical_total": 748,
            "raw_sha256": "2f35c2a76ce054be0d5b2ed18c0bfd77f163c1429af35ca48b91313ba77d0154",
            "record_total": 631,
            "target_total": 10096,
        },
    }


def test_source_index_and_multiplicity_mutations_are_rejected():
    engine = load_engine()
    lane = engine.HISTORICAL_LANES["third"]
    source = engine.authenticate_source()
    for mutate in (
        lambda payload: (payload[0].__setitem__(0, 1_000_000_007),
                         payload[1].__setitem__(0, 1_000_000_007)),
        lambda payload: payload[0].__setitem__(4, payload[0][4] + 1),
    ):
        with TemporaryDirectory() as directory:
            path = write_owner_copy(engine, lane["owners"], directory, mutate)
            expected = adjusted_expected(engine, lane, path)
            with pytest.raises(RuntimeError,
                               match="owner record does not match authenticated source"):
                engine.replay_owner_stream(path, lane["target"], expected,
                                           lane["report"], source)


def test_exact_cost_and_noncanonical_fraction_mutations_are_rejected():
    engine = load_engine()
    lane = engine.HISTORICAL_LANES["third"]
    source = engine.authenticate_source()
    cases = (
        (lambda payload: payload[1][2].__setitem__(0,
                                                   payload[1][2][0] + payload[1][2][1]),
         "owner exact cost mismatch"),
        (lambda payload: payload[1][3][0][0].__setitem__(
            slice(None), [2 * payload[1][3][0][0][0],
                          2 * payload[1][3][0][0][1]]),
         "noncanonical rational pair"),
    )
    for mutate, message in cases:
        with TemporaryDirectory() as directory:
            path = write_owner_copy(engine, lane["owners"], directory, mutate)
            expected = adjusted_expected(engine, lane, path)
            with pytest.raises(RuntimeError, match=message):
                engine.replay_owner_stream(path, lane["target"], expected,
                                           lane["report"], source)


def test_report_identity_mutation_is_rejected():
    engine = load_engine()
    lane = engine.HISTORICAL_LANES["third"]
    report = json.loads(lane["report"].read_text())
    report["target_family"]["orbit_total"] = -7
    with TemporaryDirectory() as directory:
        path = Path(directory) / lane["report"].name
        path.write_text(json.dumps(report, separators=(",", ":")) + "\n")
        with pytest.raises(RuntimeError, match="historical report identity changed"):
            engine.replay_owner_stream(lane["owners"], lane["target"], lane, path)
