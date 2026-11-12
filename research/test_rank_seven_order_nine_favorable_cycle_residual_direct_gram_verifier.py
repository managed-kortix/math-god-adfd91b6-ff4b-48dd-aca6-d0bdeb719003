#!/usr/bin/env python3
"""Hostile tests for the exact 80-target direct-Gram verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
VERIFIER = (HERE /
            "rank-seven-order-nine-favorable-cycle-residual-direct-gram-verifier.py")


def load_verifier():
    spec = importlib.util.spec_from_file_location(
        "rank_seven_order_nine_residual_direct_gram_verifier", VERIFIER
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_committed_exact_fixture():
    verifier = load_verifier()
    result = verifier.verify()
    assert result["certificate_total"] == 80
    assert result["full_theorem"] is False
    assert result["maximum_exact_cost"] == [2196948613770817, 464776880103900]
    assert result["minimum_positive_ldl_pivot"] == [
        737298878818823077577077678332152693,
        9220752281240754918170528712144042981,
    ]


def test_bad_ldl_pivots_are_detected():
    verifier = load_verifier()
    indefinite = [[verifier.F(i == j) for j in range(verifier.ORDER)]
                  for i in range(verifier.ORDER)]
    indefinite[0][1] = indefinite[1][0] = verifier.F(2)
    _, pivots = verifier.exact_ldl(indefinite)
    assert any(pivot < 0 for pivot in pivots)

    singular = [[verifier.F(i == j) for j in range(verifier.ORDER)]
                for i in range(verifier.ORDER)]
    singular[0][1] = singular[1][0] = verifier.F(1)
    _, pivots = verifier.exact_ldl(singular)
    assert any(pivot == 0 for pivot in pivots)


def test_mutated_certificate_bytes_fail_closed(tmp_path, monkeypatch):
    verifier = load_verifier()
    payload = json.loads(verifier.CERTIFICATES.read_text("ascii"))
    mutated = copy.deepcopy(payload)
    mutated["certificates"][0]["matrix"][0][1] = [0, 1]
    path = tmp_path / "mutated.json"
    path.write_bytes(verifier.canonical_bytes(mutated))
    monkeypatch.setattr(verifier, "CERTIFICATES", path)
    with pytest.raises(RuntimeError, match="bytes changed"):
        verifier.verify()
