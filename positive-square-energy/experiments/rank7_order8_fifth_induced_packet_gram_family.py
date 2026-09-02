#!/usr/bin/env python3
"""Exact induced-packet closure of the fifth order-eight remainder family."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import lzma
from collections import Counter
from pathlib import Path

import rank7_order8_induced_packet_gram_family as packet
import rank7_order8_structural_cycle_gram_lane as structural


HERE = Path(__file__).resolve().parent
SOURCE_REPORT = HERE / "rank7_order8_induced_packet_gram_family.json"
SOURCE_STREAM = HERE / "rank7_order8_after_third_structural_cycle_gram_remainder.jsonl.xz"
OUTPUT = HERE / "rank7_order8_fifth_induced_packet_gram_family.json"
OWNERS = HERE / "rank7_order8_fifth_induced_packet_gram_family_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order8_after_fifth_induced_packet_gram_family_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-eight-fifth-induced-packet-gram-family-v1"
SCOPE = "full authenticated 80,683-row remainder after complete fourth induced-packet closure"
DOMINANCE_RANK = 5
SOURCE_REMAINDER = 83611
CLOSED_FAMILY_TOTAL = 2928
EXPECTED_REMAINDER = 80683
CLOSED_TARGET = ((2, 2, 2, 2, 1, 1, 1, 1, 1, 1), (2, 4, 4), 3, 1)
TARGET = ((2, 2, 2, 2, 1, 1, 1, 1, 1, 1), (1, 3, 6), 3, 1)
EXPECTED_TARGET = 2571
DENOMINATORS = packet.DENOMINATORS
_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return packet.canonical_bytes(payload)


def file_sha256(path):
    return packet.file_sha256(path)


def source_records(limit=None):
    report_raw = SOURCE_REPORT.read_bytes()
    report = structural.strict_json(report_raw, SOURCE_REPORT.name)
    source_info = report.get("source_stream")
    closed = report.get("target_family")
    require(
        report.get("full_theorem") is True and
        report.get("owned_orbit_total") == CLOSED_FAMILY_TOTAL and
        report.get("remaining_target_family_total") == 0 and
        closed == {
            "bundle_types": [2, 4, 4],
            "cycle_rank": 3,
            "multiplicity_partition": [2, 2, 2, 2, 1, 1, 1, 1, 1, 1],
            "orbit_total": CLOSED_FAMILY_TOTAL,
            "physical_total": 3060,
            "scanned_total": CLOSED_FAMILY_TOTAL,
            "triangle_total": 1,
        },
        "fourth induced-packet closure is incomplete",
    )
    require(
        source_info is not None and
        source_info.get("record_total") == SOURCE_REMAINDER and
        source_info.get("path") == SOURCE_STREAM.name and
        file_sha256(SOURCE_STREAM) == source_info.get("artifact_sha256"),
        "wrong authenticated fourth-family source stream",
    )
    owner_info = report.get("owner_stream")
    require(
        owner_info is not None and
        owner_info.get("record_total") == CLOSED_FAMILY_TOTAL and
        file_sha256(HERE / owner_info["path"]) == owner_info.get("artifact_sha256"),
        "fourth-family owner stream is not authenticated",
    )

    digest = hashlib.sha256()
    records = []
    remainder_records = []
    strata = Counter()
    physical_strata = Counter()
    closed_total = target_physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = structural.strict_json(raw, SOURCE_STREAM.name)
            require(raw == canonical_bytes(record) and len(record) == 6,
                    "noncanonical source remainder row")
            digest.update(raw)
            key = structural.family(tuple(map(tuple, record[3])), tuple(record[4]))
            if key == CLOSED_TARGET:
                closed_total += 1
                continue
            remainder_records.append((record, raw))
            strata[key] += 1
            physical_strata[key] += record[5]
            if key == TARGET:
                target_physical += record[5]
                if limit is None or len(records) < limit:
                    records.append(record)
    require(
        digest.hexdigest() == source_info.get("raw_sha256") and
        closed_total == CLOSED_FAMILY_TOTAL and
        len(remainder_records) == EXPECTED_REMAINDER,
        "fourth-family reduced remainder authentication failed",
    )
    ranked = sorted(strata, key=lambda key: (-strata[key], -physical_strata[key], key))
    require(len(ranked) >= 5 and ranked[4] == TARGET and strata[TARGET] == EXPECTED_TARGET,
            "fifth dominant family changed")
    return (report_raw, report, source_info, records, remainder_records, strata,
            physical_strata, target_physical, ranked)


def worker(record):
    engine, census, residuals, restarts, iterations = _CONTEXT

    class Arguments:
        symbolic_fast_lane = False
        seed = 1729
        fallback_restarts = 0
        fallback_iterations = 0

    Arguments.restarts = restarts
    Arguments.iterations = iterations
    index = record[0]
    result, numerical, shared, _ = engine.base.search_record(
        Arguments, census, residuals[index], index, DENOMINATORS)
    if result[0] != engine.base.MODE_SHARED or shared is None:
        return index, record[1], numerical, None
    engine.base.verify_shared(census, residuals[index], shared)
    return index, record[1], numerical, packet.encode_witness(shared)


def scan(workers, restarts, iterations, progress=False, limit=None, persist=True):
    global _CONTEXT
    (report_raw, source_report, source_info, records, remainder_records, strata,
     physical_strata, target_physical, ranked) = source_records(limit)
    engine = packet.load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=packet.CACHE_PATH)
    for record in records:
        residual = residuals[record[0]]
        require((residual[1], residual[0]) == (record[1], record[2]),
                "family row escaped rational-search stream")
    _CONTEXT = engine, census, residuals, restarts, iterations
    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=4)

    owners = []
    classification = hashlib.sha256()
    for position, (record, result) in enumerate(zip(records, results, strict=True), 1):
        index, source_index, numerical, witness = result
        accepted = witness is not None
        classification.update(canonical_bytes([index, source_index, accepted]))
        if accepted:
            owners.append({
                "stream_index": index,
                "source_index": source_index,
                "global_kernel": record[2],
                "orbit_size": record[5],
                "numerical_canonical_cost": numerical,
                "witness": witness,
            })
        if progress and position % 25 == 0:
            print(f"target={position}/{len(records)} owned={len(owners)}", flush=True)
    if executor is not None:
        executor.shutdown()

    owner_raw = hashlib.sha256()
    remainder_raw = hashlib.sha256()
    if persist:
        owner_tmp = OWNERS.with_name(OWNERS.name + ".tmp")
        with lzma.open(owner_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for owner in owners:
                raw = canonical_bytes(owner)
                output.write(raw)
                owner_raw.update(raw)
        owner_tmp.replace(OWNERS)
        owner_indices = {owner["stream_index"] for owner in owners}
        remainder_tmp = REMAINDER.with_name(REMAINDER.name + ".tmp")
        with lzma.open(remainder_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for record, raw in remainder_records:
                if record[0] not in owner_indices:
                    output.write(raw)
                    remainder_raw.update(raw)
        remainder_tmp.replace(REMAINDER)

    report = {
        "schema": SCHEMA,
        "full_theorem": len(owners) == EXPECTED_TARGET,
        "scope": SCOPE,
        "source_report": {"path": SOURCE_REPORT.name,
                          "sha256": hashlib.sha256(report_raw).hexdigest()},
        "source_stream": source_info,
        "closed_source_family_total": CLOSED_FAMILY_TOTAL,
        "scanned_remainder_total": EXPECTED_REMAINDER,
        "dominant_families": [{
            "multiplicity_partition": list(key[0]),
            "bundle_types": list(key[1]),
            "cycle_rank": key[2],
            "triangle_total": key[3],
            "orbit_total": strata[key],
            "physical_total": physical_strata[key],
        } for key in ranked],
        "target_family": {
            "dominance_rank": DOMINANCE_RANK,
            "multiplicity_partition": list(TARGET[0]),
            "bundle_types": list(TARGET[1]),
            "cycle_rank": TARGET[2],
            "triangle_total": TARGET[3],
            "orbit_total": EXPECTED_TARGET,
            "physical_total": target_physical,
            "scanned_total": len(records),
        },
        "gram": {
            "family": "induced rational waypoint packet",
            "branch_gram": "G_ij=<x_i,x_j> for exact rational stereographic unit vectors",
            "path_packets": "each path stores a rational waypoint chain from x_u to (-1)^L x_v",
            "frontiers": "one exact length-plus-two packet is stored for each physical path",
            "psd_proof": "every branch and waypoint Gram is an explicit rational vector Gram XX^T",
            "exact_acceptance": "Fraction replay is at most six on the canonical row and all fourteen coordinate frontiers",
            "denominators": list(DENOMINATORS),
            "numerical_proposal": {"seed": 1729, "restarts": restarts,
                                   "iterations": iterations},
        },
        "theorem_lift": {
            "all_length": "canonical-plus-coordinate reduction and fixed-parity path monotonicity",
            "induced_owner": "the stored packet owns every same-parity subdivision it induces",
            "rooted_trees": "DNN one-vertex additivity supplies arbitrary rooted-tree attachments",
        },
        "owned_orbit_total": len(owners),
        "owned_physical_total": sum(owner["orbit_size"] for owner in owners),
        "owned_target_total": len(owners) * structural.TARGETS_PER_ROW,
        "remaining_target_family_total": EXPECTED_TARGET - len(owners),
        "remaining_remainder_total": EXPECTED_REMAINDER - len(owners),
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": None,
        "reduced_remainder_stream": None,
        "claim_boundary": "only exact shared packet owners and their all-length/rooted-tree lifts are theorem-owned",
    }
    if persist:
        report["owner_stream"] = {
            "path": OWNERS.name,
            "record_total": len(owners),
            "raw_sha256": owner_raw.hexdigest(),
            "artifact_sha256": file_sha256(OWNERS),
        }
        report["reduced_remainder_stream"] = {
            "path": REMAINDER.name,
            "record_total": EXPECTED_REMAINDER - len(owners),
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER),
        }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0 and args.restarts > 0 and args.iterations > 0 and
            (args.limit is None or args.limit > 0), "invalid scan parameters")
    require(not args.audit or args.limit is None, "partial scans cannot audit")
    report = scan(args.workers, args.restarts, args.iterations, args.progress,
                  args.limit, persist=args.limit is None)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce")
    elif args.limit is None:
        args.output.write_bytes(raw)
    print(f"target={report['target_family']['scanned_total']} "
          f"owned={report['owned_orbit_total']} "
          f"remaining={report['remaining_remainder_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
