#!/usr/bin/env python3
"""Hostile regression tests for the favorable-cycle residual miner."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MINER = HERE / "rank-seven-order-nine-favorable-cycle-residual-miner.py"


def load_miner():
    spec = importlib.util.spec_from_file_location(
        "rank_seven_order_nine_favorable_cycle_residual_miner", MINER
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_report_reproduces_and_occurrence_identity_is_consistent():
    miner = load_miner()
    kernels = miner.load_kernels()
    rows, by_index = miner.load_source(kernels)
    excluded = miner.load_lane_indices(by_index)
    report = miner.analyze(rows, kernels, excluded)

    assert report["frontier"] == {
        "orbit_rows": 1615,
        "physical_rows": 1945,
        "represented_kernels": 115,
        "targets": 25840,
    }
    assert report["owned_targets"] == 25760
    assert report["residual_targets"] == 80
    assert report["residual_rows"] == 39
    assert report["canonical_residual_targets"] == 0
    assert report["residual_targets_per_row_histogram"] == {"2": 37, "3": 2}

    failures = report["failures"]
    assert len(failures) == 80
    assert len({failure["source_index"] for failure in failures}) == 39
    assert all(failure["source_record"] == failure["key"][:5]
               for failure in failures)
    assert all(failure["frontier_path_index"] == failure["key"][5]
               for failure in failures)
    assert all(failure["physical_occurrence_key"] ==
               [failure["frontier_support"], failure["frontier_occurrence"]]
               for failure in failures)
    assert all(len(failure["target_length_vector"]) == miner.PATH_COUNT
               for failure in failures)
    assert all(failure["target_length_vector"][failure["frontier_path_index"]] ==
               failure["frontier_base_length"] + 2
               for failure in failures)
    assert all(sum(
        length != base_length
        for length, base_length in zip(
            failure["target_length_vector"],
            [path[4] for path in miner.canonical_paths(
                kernels[failure["order9_kernel"]][1], failure["row"]
            )],
            strict=True,
        )
    ) == 1 for failure in failures)
    assert Counter(
        option["cycle_mod4"]
        for failure in failures
        for option in failure["rank_one_options"]
    ) == Counter({1: 650})


def test_bad_source_hash_is_rejected(monkeypatch):
    miner = load_miner()
    kernels = miner.load_kernels()
    monkeypatch.setitem(miner.EXPECTED, "source_xz", "0" * 64)
    with pytest.raises(RuntimeError, match="source artifact changed"):
        miner.load_source(kernels)


def test_bad_lane_hash_is_rejected(monkeypatch):
    miner = load_miner()
    kernels = miner.load_kernels()
    _, by_index = miner.load_source(kernels)
    monkeypatch.setitem(miner.EXPECTED, "lanes_xz", ("0" * 64,) +
                        miner.EXPECTED["lanes_xz"][1:])
    with pytest.raises(RuntimeError, match="compressed bytes changed"):
        miner.load_lane_indices(by_index)
