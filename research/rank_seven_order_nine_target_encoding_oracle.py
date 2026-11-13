#!/usr/bin/env python3
"""Independent oracle for the StageLedger flat target JSONL encoding.

This deliberately does not import ``rank_seven_order_nine_stage_ledger``.
Its one reviewed fixture fixes field order, array nesting, separators, newline,
coordinate order, byte count, and SHA-256 independently of the producer.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

FIXTURE = Path(__file__).with_name("fixtures") / \
    "rank_seven_order_nine_flat_target_v1.jsonl"
SCHEMA = "rank-seven-order-nine-flat-six-field-target-jsonl-v1"
ROW = [2, 7487, 1, [1, 1, 1, 1, 1, 1, 1, 1, 0, 0], 1]
EXPECTED_SIZE = 598
EXPECTED_SHA256 = "ecf8d6532a80ab79e736ff995b486c0947d67183aec5ff93d6485a0c933feb28"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def oracle_lines() -> tuple[bytes, ...]:
    """Construct the reviewed bytes without calling ledger code."""
    return tuple(
        (json.dumps(
            [ROW[0], ROW[1], ROW[2], ROW[3], ROW[4], coordinate],
            separators=(",", ":"), ensure_ascii=True, allow_nan=False,
        ) + "\n").encode("ascii")
        for coordinate in range(16)
    )


def verify_fixture() -> dict[str, object]:
    data = FIXTURE.read_bytes()
    generated = b"".join(oracle_lines())
    require(data == generated, "target encoding fixture bytes changed")
    require(len(data) == EXPECTED_SIZE, "target encoding fixture size changed")
    digest = hashlib.sha256(data).hexdigest()
    require(digest == EXPECTED_SHA256, "target encoding fixture digest changed")
    records = data.splitlines()
    require(len(records) == 16, "target encoding fixture cardinality changed")
    for coordinate, record in enumerate(records):
        value = json.loads(record.decode("ascii"))
        require(type(value) is list and len(value) == 6,
                "target fixture is not a flat six-field JSON list")
        require(value[:5] == ROW and type(value[5]) is int and
                value[5] == coordinate,
                "target fixture field or coordinate order changed")
    return {
        "schema": SCHEMA,
        "fixture_size": len(data),
        "fixture_sha256": digest,
        "target_total": len(records),
        "verified": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify_fixture(), sort_keys=True, separators=(",", ":")))
