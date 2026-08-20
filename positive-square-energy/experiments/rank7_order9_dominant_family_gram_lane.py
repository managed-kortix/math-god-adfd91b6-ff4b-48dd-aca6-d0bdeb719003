#!/usr/bin/env python3
"""Exact typed Gram lane for the leading order-nine after-SOS family."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "rank7_order9_unowned_stratifier.py"
GRAM_PATH = HERE / "rank7_order9_remainder_gram_lanes.py"
SOURCE_REPORT = HERE / "rank7_order9_typed_sos_owner_manifest.json"
SOURCE_STREAM = HERE / "rank7_order9_after_sos_remainder.jsonl.xz"
OUTPUT = HERE / "rank7_order9_dominant_family_gram_lane.json"
OWNER_STREAM = HERE / "rank7_order9_dominant_family_gram_owners.jsonl.xz"
SCHEMA = "rank-seven-order-nine-dominant-family-gram-lane-v1"
F = Fraction
BUDGET = F(6)
TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1), (3, 3, 6), 4, 1)
_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def family(base, edges, row):
    support, parity, graph = base.graph_data(edges, row, 9)
    return (tuple(support["multiplicity_partition"]),
            tuple(parity["bundle_types"]), graph["cycle_rank"],
            graph["triangle_total"])


def numerical_cost(parameters, signed, paths, type_ids):
    type_total = len(parameters) // 2
    ids = np.asarray(type_ids)
    diagonal = np.exp(parameters[:type_total])[ids]
    coefficient = parameters[type_total:][ids]
    x = np.diag(diagonal) + np.diag(coefficient) @ signed
    square = x @ x.T
    normalizer = np.max(np.diag(square))
    total = 0.0
    for _, _, u, v, length in paths:
        correlation = square[u, v] / normalizer
        transformed = -correlation if length & 1 else correlation
        if transformed <= -1.0 + 1e-12:
            return 1e6
        total += (1.0 - transformed) / (length * (1.0 + transformed))
    return total


def exact_cost(gram, signed, paths, type_ids, parameters):
    return gram.typed_cost(signed, paths, type_ids, parameters)


def worker(record):
    gram, kernels, max_denominator = _CONTEXT
    source_index, global_kernel, order_kernel, raw_row, _ = record
    expected_global, edges = kernels[order_kernel]
    require(global_kernel == expected_global, "kernel reference changed")
    signed, paths, type_keys, type_ids = gram.matrix_and_paths(edges, tuple(raw_row))
    matrix = np.asarray(signed, dtype=np.float64)
    type_total = max(type_ids) + 1
    best = None
    bounds = [(-2.0, 2.0)] * type_total + [(-4.0, 4.0)] * type_total
    for initial_coefficient in (0.5,):
        initial = np.concatenate((np.zeros(type_total),
                                  np.full(type_total, initial_coefficient)))
        proposal = minimize(numerical_cost, initial,
                            args=(matrix, paths, type_ids), method="Powell",
                            bounds=bounds,
                            options={"ftol": 1e-7, "maxiter": 160})
        if best is None or proposal.fun < best.fun:
            best = proposal
    require(best is not None, "optimizer produced no proposal")
    parameters = tuple(
        (F(float(np.exp(best.x[k]))).limit_denominator(max_denominator),
         F(float(best.x[type_total + k])).limit_denominator(max_denominator))
        for k in range(type_total))
    cost = exact_cost(gram, signed, paths, type_ids, parameters)
    return source_index, cost, parameters, type_keys, float(best.fun)


def scan(workers, max_denominator, progress=False, limit=None):
    global _CONTEXT
    base = load("rank7_order9_dominant_base", BASE_PATH)
    gram = load("rank7_order9_dominant_gram", GRAM_PATH)
    report, report_sha256 = base.strict_canonical_json(SOURCE_REPORT, "SOS owner report")
    stream_info = report["updated_remainder_stream"]
    require(file_sha256(SOURCE_STREAM) == stream_info["artifact_sha256"],
            "after-SOS remainder artifact changed")
    kernels = base.kernel_dictionary(base.load_scan_engine())
    _CONTEXT = gram, kernels, max_denominator

    digest = hashlib.sha256()
    records = []
    scanned = physical = target_total = target_physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as rows:
        for raw in rows:
            record = json.loads(raw.decode("ascii"))
            require(raw == canonical_bytes(record) and len(record) == 5,
                    "noncanonical after-SOS row")
            digest.update(raw)
            scanned += 1
            physical += record[4]
            edges = kernels[record[2]][1]
            if family(base, edges, tuple(record[3])) == TARGET:
                records.append(record)
                target_total += 1
                target_physical += record[4]
                if limit is not None and target_total >= limit:
                    break
    if limit is None:
        require(scanned == stream_info["record_total"] and
                digest.hexdigest() == stream_info["raw_sha256"],
                "full after-SOS remainder authentication failed")
        require(target_total == 21074, "leading family count changed")

    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=16)

    classification = hashlib.sha256()
    owner_raw = hashlib.sha256()
    owner_total = owner_physical = 0
    denominator_counts = Counter()
    temporary = OWNER_STREAM.with_name(OWNER_STREAM.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for index, (record, result) in enumerate(zip(records, results, strict=True)):
            source_index, cost, parameters, type_keys, numerical = result
            owned = cost is not None and cost <= BUDGET
            certificate = [source_index, owned, None if cost is None else pair(cost),
                           [[pair(left), pair(right)] for left, right in parameters]]
            classification.update(canonical_bytes(certificate))
            if owned:
                owner_total += 1
                owner_physical += record[4]
                denominator_counts.update(value.denominator
                                          for parameter in parameters
                                          for value in parameter)
                payload = [record, certificate, numerical,
                           [[key[0], [list(value) for value in key[1]]]
                            for key in sorted(set(type_keys))]]
                raw = canonical_bytes(payload)
                output.write(raw)
                owner_raw.update(raw)
            if progress and (index + 1) % 1000 == 0:
                print(f"target={index + 1} owned={owner_total}", flush=True)
    if executor is not None:
        executor.shutdown()
    temporary.replace(OWNER_STREAM)

    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "exact rational Gram ownership of the leading family within a full authenticated after-SOS remainder scan",
        "source_report_sha256": report_sha256,
        "source_stream": {**stream_info},
        "scanned_remainder_total": scanned,
        "scanned_remainder_physical_total": physical,
        "target_family": {
            "multiplicity_partition": list(TARGET[0]),
            "bundle_types": list(TARGET[1]),
            "cycle_rank": TARGET[2], "triangle_total": TARGET[3],
            "orbit_total": target_total, "physical_total": target_physical,
        },
        "gram": {
            "feature_matrix": "X=D0+D1*S, with D0,D1 constant on exact local types",
            "local_type": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
            "correlation_gram": "G=XX^T/M+diag(1-diag(XX^T)/M), M=max_i(XX^T)_ii",
            "psd_proof": "XX^T/M plus a nonnegative diagonal sum of coordinate squares",
            "proposal": "one deterministic binary64 Powell start at D0=1,D1=1/2",
            "exact_replay": "every D0,D1 entry is rounded to Fraction.limit_denominator before exact cost acceptance",
            "maximum_denominator": max_denominator,
        },
        "owned_orbit_total": owner_total,
        "owned_physical_total": owner_physical,
        "owned_target_total": owner_total * 16,
        "remaining_remainder_total": stream_info["record_total"] - owner_total,
        "remaining_target_family_total": target_total - owner_total,
        "classification_stream_sha256": classification.hexdigest(),
        "used_denominators": dict(sorted(denominator_counts.items())),
        "owner_stream": {"path": OWNER_STREAM.name, "record_total": owner_total,
                         "raw_sha256": owner_raw.hexdigest(),
                         "artifact_sha256": file_sha256(OWNER_STREAM)},
        "claim_boundary": "only records in the owner stream are theorem-owned; optimizer failures and non-target families remain unclassified",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--max-denominator", type=int, default=64)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0 and args.max_denominator > 0, "invalid scan parameters")
    result = scan(args.workers, args.max_denominator, args.progress, args.limit)
    raw = canonical_bytes(result)
    if args.audit:
        require(args.limit is None and args.output.read_bytes() == raw,
                "report does not reproduce byte-for-byte")
    else:
        args.output.write_bytes(raw)
    print(f"scanned={result['scanned_remainder_total']} "
          f"target={result['target_family']['orbit_total']} "
          f"owned={result['owned_orbit_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
