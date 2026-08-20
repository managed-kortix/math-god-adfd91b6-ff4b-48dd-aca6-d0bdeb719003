#!/usr/bin/env python3
"""Exact typed direct-packet Gram lane for a dominant order-twelve family."""

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
OWNER_PATH = HERE / "rank7_order12_structural_owners.py"
STRATIFICATION_PATH = HERE / "rank7_order12_remainder_stratification.json"
SOURCE_STREAM = HERE / "rank7_order12_exact_owner_remainder.jsonl.xz"
OUTPUT_PATH = HERE / "rank7_order12_typed_packet_gram_lane.json"
OWNER_STREAM = HERE / "rank7_order12_typed_packet_gram_owners.jsonl.xz"
REMAINDER_STREAM = HERE / "rank7_order12_after_typed_packet_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-twelve-typed-direct-packet-gram-lane-v1"
ORDER = 12
PATH_COUNT = 18
TARGETS_PER_ROW = 19
BUDGET = Fraction(6)
F = Fraction
TARGET = ((2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (5, 3, 6), 3, 0)
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


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def load_owner():
    spec = importlib.util.spec_from_file_location("rank7_order12_packet_owner", OWNER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load owner engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def kernel_dictionary():
    owner = load_owner()
    kernels = {}
    for path in sorted(HERE.glob("rank7_order12_census_*.json.xz")):
        header, records, _ = owner.stream_chunk(path)
        kernels.update({item["order_kernel"]: tuple(map(tuple, item["edges"]))
                        for item in header["kernels"]})
        records.close()
    require(len(kernels) == 365, "order-twelve kernel dictionary changed")
    return kernels


def family(edges, row):
    adjacency = [set() for _ in range(ORDER)]
    kinds = [0, 0, 0]
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        adjacency[u].add(v)
        adjacency[v].add(u)
        kinds[0 if odd == 0 else 2 if odd == multiplicity else 1] += 1
    triangles = sum(len(adjacency[u] & adjacency[v])
                    for u in range(ORDER) for v in adjacency[u] if u < v) // 3
    return (tuple(sorted((edge[2] for edge in edges), reverse=True)), tuple(kinds),
            len(edges) - ORDER + 1, triangles)


def matrix_and_paths(edges, row):
    signed = [[0] * ORDER for _ in range(ORDER)]
    incident = [[] for _ in range(ORDER)]
    paths = []
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        signed[u][v] = signed[v][u] = multiplicity - 2 * odd
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((u, v, length) for length in lengths)
    require(len(paths) == PATH_COUNT, "physical path total changed")
    keys = tuple((sum(signed[u]), tuple(sorted(incident[u]))) for u in range(ORDER))
    dictionary = {key: index for index, key in enumerate(sorted(set(keys)))}
    return (tuple(tuple(value) for value in signed), tuple(paths), keys,
            tuple(dictionary[key] for key in keys))


def numerical_cost(parameters, signed, paths, type_ids):
    type_total = len(parameters) // 2
    ids = np.asarray(type_ids)
    diagonal = np.exp(parameters[:type_total])[ids]
    coefficient = parameters[type_total:][ids]
    feature = np.diag(diagonal) + np.diag(coefficient) @ signed
    core = feature @ feature.T
    normalizer = np.max(np.diag(core))
    total = 0.0
    for u, v, length in paths:
        correlation = core[u, v] / normalizer
        transformed = -correlation if length & 1 else correlation
        if transformed <= -1.0 + 1e-12:
            return 1e6
        total += (1.0 - transformed) / (length * (1.0 + transformed))
    return total


def exact_cost(signed, paths, type_ids, parameters):
    feature = [[(parameters[type_ids[u]][0] if u == v else F()) +
                parameters[type_ids[u]][1] * signed[u][v]
                for v in range(ORDER)] for u in range(ORDER)]
    core = [[sum(feature[u][w] * feature[v][w] for w in range(ORDER))
             for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(core[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero packet normalizer")
    total = F()
    for u, v, length in paths:
        correlation = core[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "packet correlation escaped [-1,1]")
        if transformed == -1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


def worker(record):
    kernels, max_denominator = _CONTEXT
    source_index, global_kernel, order_kernel, raw_row, _ = record
    edges = kernels[order_kernel]
    signed, paths, type_keys, type_ids = matrix_and_paths(edges, tuple(raw_row))
    matrix = np.asarray(signed, dtype=np.float64)
    type_total = max(type_ids) + 1
    best = None
    for initial_coefficient in (0.5, -0.5):
        initial = np.concatenate((np.zeros(type_total),
                                  np.full(type_total, initial_coefficient)))
        proposal = minimize(
            numerical_cost, initial, args=(matrix, paths, type_ids), method="Powell",
            bounds=[(-2.0, 2.0)] * type_total + [(-4.0, 4.0)] * type_total,
            options={"ftol": 1e-8, "maxiter": 180})
        if best is None or proposal.fun < best.fun:
            best = proposal
    require(best is not None, "optimizer produced no packet proposal")
    parameters = tuple(
        (F(float(np.exp(best.x[index]))).limit_denominator(max_denominator),
         F(float(best.x[type_total + index])).limit_denominator(max_denominator))
        for index in range(type_total))
    cost, normalizer = exact_cost(signed, paths, type_ids, parameters)
    return source_index, global_kernel, cost, normalizer, parameters, type_keys, float(best.fun)


def pair(value):
    return [value.numerator, value.denominator]


def scan(workers, max_denominator, progress=False, limit=None, persist=True):
    global _CONTEXT
    stratification, stratification_sha256 = strict_json(STRATIFICATION_PATH)
    source_info = stratification["remainder_stream"]
    require(stratification["remainder_orbit_total"] == 123329 and
            file_sha256(SOURCE_STREAM) == source_info["artifact_sha256"],
            "wrong authenticated order-twelve remainder")
    kernels = kernel_dictionary()
    records = []
    all_records = []
    source_digest = hashlib.sha256()
    physical = target_physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as rows:
        for raw in rows:
            record = json.loads(raw.decode("ascii"))
            require(raw == canonical_bytes(record) and len(record) == 5,
                    "noncanonical source remainder row")
            source_digest.update(raw)
            all_records.append((record, raw))
            physical += record[4]
            edges = kernels[record[2]]
            if family(edges, tuple(record[3])) == TARGET and (
                    limit is None or len(records) < limit):
                records.append(record)
                target_physical += record[4]
    require((len(all_records), physical, source_digest.hexdigest()) ==
            (source_info["record_total"], source_info["physical_total"],
             source_info["raw_sha256"]), "source remainder authentication failed")
    expected_target = next(item for item in
                           stratification["stratification"]["dominant"]["top_strata"]
                           if item["signature"]["multiplicity_partition"] == list(TARGET[0]) and
                           item["signature"]["bundle_types"] == list(TARGET[1]) and
                           item["signature"]["cycle_rank"] == TARGET[2] and
                           item["signature"]["triangle_total"] == TARGET[3])
    if limit is None:
        require(len(records) == expected_target["orbit_total"] == 6843,
                "target family count changed")

    _CONTEXT = kernels, max_denominator
    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=8)
    owners = []
    classification = hashlib.sha256()
    denominator_counts = Counter()
    minimum = None
    for index, (record, result) in enumerate(zip(records, results, strict=True), 1):
        source_index, global_kernel, cost, normalizer, parameters, type_keys, numerical = result
        accepted = cost is not None and cost <= BUDGET
        certificate = [source_index, accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[pair(left), pair(right)] for left, right in parameters]]
        classification.update(canonical_bytes(certificate))
        if cost is not None:
            minimum = cost if minimum is None or cost < minimum else minimum
        if accepted:
            denominator_counts.update(value.denominator for values in parameters
                                      for value in values)
            owners.append((record, certificate, numerical,
                           [[key[0], [list(value) for value in key[1]]]
                            for key in sorted(set(type_keys))]))
        if progress and index % 100 == 0:
            print(f"target={index}/{len(records)} owned={len(owners)}", flush=True)
    if executor is not None:
        executor.shutdown()

    owner_indices = {record[0] for record, _, _, _ in owners}
    owner_raw = hashlib.sha256()
    remainder_raw = hashlib.sha256()
    remainder_total = remainder_physical = 0
    if persist:
        owner_temporary = OWNER_STREAM.with_name(OWNER_STREAM.name + ".tmp")
        with lzma.open(owner_temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for payload in owners:
                raw = canonical_bytes(payload)
                output.write(raw)
                owner_raw.update(raw)
        owner_temporary.replace(OWNER_STREAM)
        remainder_temporary = REMAINDER_STREAM.with_name(REMAINDER_STREAM.name + ".tmp")
        with lzma.open(remainder_temporary, "wb", format=lzma.FORMAT_XZ,
                       preset=6) as output:
            for record, raw in all_records:
                if record[0] in owner_indices:
                    continue
                output.write(raw)
                remainder_raw.update(raw)
                remainder_total += 1
                remainder_physical += record[4]
        remainder_temporary.replace(REMAINDER_STREAM)
    else:
        remainder_total = len(all_records) - len(owners)
        remainder_physical = physical - sum(record[4] for record, _, _, _ in owners)

    owner_physical = sum(record[4] for record, _, _, _ in owners)
    require(remainder_total + len(owners) == len(all_records) and
            remainder_physical + owner_physical == physical,
            "updated remainder partition changed")
    result = {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "full exact typed direct-packet Gram replay of one dominant order-twelve remainder family",
        "source_stratification": {"path": STRATIFICATION_PATH.name,
                                  "sha256": stratification_sha256},
        "source_remainder": source_info,
        "scanned_remainder_orbit_total": len(all_records),
        "scanned_remainder_physical_total": physical,
        "target_family": {"multiplicity_partition": list(TARGET[0]),
                          "bundle_types": list(TARGET[1]),
                          "cycle_rank": TARGET[2], "triangle_total": TARGET[3],
                          "orbit_total": expected_target["orbit_total"],
                          "physical_total": expected_target["physical_total"],
                          "scanned_total": len(records)},
        "gram": {
            "formula": "X=D0+D1*S; H=XX^T; G=H/M+diag(1-diag(H)/M)",
            "local_type": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
            "psd_proof": "XX^T/M plus nonnegative diagonal coordinate squares",
            "proposal": "two deterministic Powell starts at D0=1 and D1=1/2,-1/2",
            "exact_acceptance": "rational replay of every Gram entry and path cost at most six",
            "maximum_denominator": max_denominator,
        },
        "owned_orbit_total": len(owners), "owned_physical_total": owner_physical,
        "owned_target_total": len(owners) * TARGETS_PER_ROW,
        "remaining_remainder_orbit_total": remainder_total,
        "remaining_remainder_physical_total": remainder_physical,
        "remaining_target_family_total": len(records) - len(owners),
        "minimum_exact_cost": None if minimum is None else pair(minimum),
        "classification_stream_sha256": classification.hexdigest(),
        "used_denominators": dict(sorted(denominator_counts.items())),
        "owner_stream": None, "updated_remainder_stream": None,
        "claim_boundary": "only exact accepted owner-stream rows are closed; all other source rows remain persisted and unclassified",
    }
    if persist:
        result["owner_stream"] = {"path": OWNER_STREAM.name,
                                  "record_total": len(owners),
                                  "physical_total": owner_physical,
                                  "raw_sha256": owner_raw.hexdigest(),
                                  "artifact_sha256": file_sha256(OWNER_STREAM)}
        result["updated_remainder_stream"] = {
            "path": REMAINDER_STREAM.name, "record_total": remainder_total,
            "physical_total": remainder_physical,
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER_STREAM)}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-denominator", type=int, default=64)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0 and args.max_denominator > 0 and
            (args.limit is None or args.limit > 0), "invalid scan parameters")
    require(not args.audit or args.limit is None, "partial scans cannot audit")
    result = scan(args.workers, args.max_denominator, args.progress, args.limit,
                  persist=args.limit is None)
    raw = canonical_bytes(result)
    if args.audit:
        require(args.output.read_bytes() == raw, "packet report does not reproduce")
    elif args.limit is None:
        args.output.write_bytes(raw)
    print(f"scanned={result['scanned_remainder_orbit_total']} "
          f"target={result['target_family']['scanned_total']} "
          f"owned={result['owned_orbit_total']} "
          f"remaining={result['remaining_remainder_orbit_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
