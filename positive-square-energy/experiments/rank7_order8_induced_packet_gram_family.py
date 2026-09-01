#!/usr/bin/env python3
"""Exact shared induced-packet Gram scan of the fourth order-eight family."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path

import rank7_order8_alternate_exact_gram_family as source


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
OUTPUT = HERE / "rank7_order8_induced_packet_gram_family.json"
OWNERS = HERE / "rank7_order8_induced_packet_gram_family_owners.jsonl.xz"
SCHEMA = "rank-seven-order-eight-induced-packet-gram-family-v1"
DENOMINATORS = (256, 1024, 4096, 16384, 65536)
_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_packet_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load witness engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def integer_rows(rows, denominator):
    result = []
    for row in rows:
        require(all(denominator % value.denominator == 0 for value in row),
                "non-shared witness denominator")
        result.append([value.numerator * (denominator // value.denominator)
                       for value in row])
    return result


def encode_witness(witness):
    denominator, branches, canonical, extended = witness
    return {
        "denominator": denominator,
        "branches": integer_rows(branches, denominator),
        "canonical": [integer_rows(path, denominator) for path in canonical],
        "extended": [integer_rows(path, denominator) for path in extended],
    }


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
    return index, record[1], numerical, encode_witness(shared)


def scan(workers, restarts, iterations, progress=False, limit=None, persist=True):
    global _CONTEXT
    ledger_raw, source_info, records, family_total, family_physical = source.source_records(limit)
    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)
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
            owners.append({"stream_index": index, "source_index": source_index,
                           "global_kernel": record[2], "orbit_size": record[5],
                           "numerical_canonical_cost": numerical, "witness": witness})
        if progress and position % 25 == 0:
            print(f"target={position}/{len(records)} owned={len(owners)}", flush=True)
    if executor is not None:
        executor.shutdown()
    owner_raw = hashlib.sha256()
    if persist:
        temporary = OWNERS.with_name(OWNERS.name + ".tmp")
        with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for owner in owners:
                raw = canonical_bytes(owner)
                output.write(raw)
                owner_raw.update(raw)
        temporary.replace(OWNERS)
    report = {
        "schema": SCHEMA, "full_theorem": len(owners) == family_total,
        "scope": "full authenticated 2^4 1^6, (2,4,4), rank-three, one-triangle family",
        "source_report": {"path": source.base.SOURCE_LEDGER.name,
                          "sha256": hashlib.sha256(ledger_raw).hexdigest()},
        "source_stream": source_info,
        "target_family": {
            "multiplicity_partition": list(source.base.TARGET[0]),
            "bundle_types": list(source.base.TARGET[1]),
            "cycle_rank": source.base.TARGET[2], "triangle_total": source.base.TARGET[3],
            "orbit_total": family_total, "physical_total": family_physical,
            "scanned_total": len(records)},
        "gram": {
            "family": "induced rational waypoint packet",
            "branch_gram": "G_ij=<x_i,x_j> for exact rational stereographic unit vectors",
            "path_packets": "each path stores a rational waypoint chain from x_u to (-1)^L x_v",
            "frontiers": "one exact length-plus-two packet is stored for each physical path",
            "psd_proof": "every branch and waypoint Gram is an explicit rational vector Gram XX^T",
            "exact_acceptance": "Fraction replay is at most six on the canonical row and all fourteen coordinate frontiers",
            "denominators": list(DENOMINATORS),
            "numerical_proposal": {"seed": 1729, "restarts": restarts,
                                   "iterations": iterations}},
        "theorem_lift": {
            "all_length": "canonical-plus-coordinate reduction and fixed-parity path monotonicity",
            "induced_owner": "the stored packet owns every same-parity subdivision it induces",
            "rooted_trees": "DNN one-vertex additivity supplies arbitrary rooted-tree attachments"},
        "owned_orbit_total": len(owners),
        "owned_physical_total": sum(owner["orbit_size"] for owner in owners),
        "owned_target_total": len(owners) * source.base.TARGETS_PER_ROW,
        "remaining_target_family_total": family_total - len(owners),
        "classification_stream_sha256": classification.hexdigest(),
        "owner_stream": None,
        "claim_boundary": "only exact shared packet owners and their all-length/rooted-tree lifts are theorem-owned"}
    if persist:
        report["owner_stream"] = {
            "path": OWNERS.name, "record_total": len(owners),
            "raw_sha256": owner_raw.hexdigest(), "artifact_sha256": file_sha256(OWNERS)}
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
          f"remaining={report['remaining_target_family_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
