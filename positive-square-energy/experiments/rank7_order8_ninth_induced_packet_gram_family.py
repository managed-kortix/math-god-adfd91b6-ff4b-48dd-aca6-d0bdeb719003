#!/usr/bin/env python3
"""Exact induced-packet closure of the ninth order-eight remainder family."""

from __future__ import annotations

import hashlib
import lzma
from collections import Counter
from pathlib import Path

import rank7_order8_fifth_induced_packet_gram_family as lane
import rank7_order8_structural_cycle_gram_lane as structural


HERE = Path(__file__).resolve().parent
SOURCE_REPORT = HERE / "rank7_order8_eighth_induced_packet_gram_family.json"
SOURCE_STREAM = HERE / "rank7_order8_after_eighth_induced_packet_gram_family_remainder.jsonl.xz"
OUTPUT = HERE / "rank7_order8_ninth_induced_packet_gram_family.json"
OWNERS = HERE / "rank7_order8_ninth_induced_packet_gram_family_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order8_after_ninth_induced_packet_gram_family_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-eight-ninth-induced-packet-gram-family-v1"
SCOPE = "full authenticated 65,049-row remainder after complete eighth induced-packet closure"
SOURCE_REMAINDER = 65049
PREVIOUS_FAMILY_TOTAL = 4219
TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 1)
EXPECTED_TARGET = 3765


def source_records(limit=None):
    report_raw = SOURCE_REPORT.read_bytes()
    report = structural.strict_json(report_raw, SOURCE_REPORT.name)
    lane.require(report_raw == lane.canonical_bytes(report),
                 "noncanonical source report")
    source_info = report.get("reduced_remainder_stream")
    owner_info = report.get("owner_stream")
    lane.require(
        report.get("full_theorem") is True
        and report.get("owned_orbit_total") == PREVIOUS_FAMILY_TOTAL
        and report.get("remaining_target_family_total") == 0,
        "eighth induced-packet closure is incomplete",
    )
    lane.require(
        source_info is not None
        and source_info.get("record_total") == SOURCE_REMAINDER
        and source_info.get("path") == SOURCE_STREAM.name
        and lane.file_sha256(SOURCE_STREAM) == source_info.get("artifact_sha256"),
        "wrong authenticated eighth-family remainder stream",
    )
    lane.require(
        owner_info is not None
        and owner_info.get("record_total") == PREVIOUS_FAMILY_TOTAL
        and lane.file_sha256(HERE / owner_info["path"]) == owner_info.get("artifact_sha256"),
        "eighth-family owner stream is not authenticated",
    )
    owner_digest = hashlib.sha256()
    owner_total = 0
    with lzma.open(HERE / owner_info["path"], "rb") as owner_stream:
        for owner_raw in owner_stream:
            owner = structural.strict_json(owner_raw, owner_info["path"])
            lane.require(owner_raw == lane.canonical_bytes(owner),
                         "noncanonical source owner row")
            owner_digest.update(owner_raw)
            owner_total += 1
    lane.require(
        owner_total == PREVIOUS_FAMILY_TOTAL
        and owner_digest.hexdigest() == owner_info.get("raw_sha256"),
        "source owner raw stream authentication failed",
    )

    digest = hashlib.sha256()
    records = []
    remainder_records = []
    strata = Counter()
    physical_strata = Counter()
    target_physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = structural.strict_json(raw, SOURCE_STREAM.name)
            lane.require(raw == lane.canonical_bytes(record) and len(record) == 6,
                         "noncanonical source remainder row")
            digest.update(raw)
            remainder_records.append((record, raw))
            key = structural.family(tuple(map(tuple, record[3])), tuple(record[4]))
            strata[key] += 1
            physical_strata[key] += record[5]
            if key == TARGET:
                target_physical += record[5]
                if limit is None or len(records) < limit:
                    records.append(record)
    lane.require(
        digest.hexdigest() == source_info.get("raw_sha256")
        and len(remainder_records) == SOURCE_REMAINDER,
        "eighth-family reduced remainder authentication failed",
    )
    ranked = sorted(strata, key=lambda key: (-strata[key], -physical_strata[key], key))
    lane.require(
        len(ranked) >= 1 and ranked[0] == TARGET and strata[TARGET] == EXPECTED_TARGET,
        "ninth target family changed",
    )
    return (report_raw, report, source_info, records, remainder_records, strata,
            physical_strata, target_physical, ranked)


def main():
    lane.SOURCE_REPORT = SOURCE_REPORT
    lane.SOURCE_STREAM = SOURCE_STREAM
    lane.OUTPUT = OUTPUT
    lane.OWNERS = OWNERS
    lane.REMAINDER = REMAINDER
    lane.SCHEMA = SCHEMA
    lane.SCOPE = SCOPE
    lane.DOMINANCE_RANK = 1
    lane.SOURCE_REMAINDER = SOURCE_REMAINDER
    lane.CLOSED_FAMILY_TOTAL = PREVIOUS_FAMILY_TOTAL
    lane.EXPECTED_REMAINDER = SOURCE_REMAINDER
    lane.TARGET = TARGET
    lane.EXPECTED_TARGET = EXPECTED_TARGET
    lane.source_records = source_records
    lane.main()


if __name__ == "__main__":
    main()
