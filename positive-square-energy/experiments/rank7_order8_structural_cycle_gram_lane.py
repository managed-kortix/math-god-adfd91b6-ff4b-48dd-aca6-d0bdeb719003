#!/usr/bin/env python3
"""Exact structural cycle-Gram lane for the leading order-eight remainder family."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import lzma
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
SOURCE_LEDGER = HERE / "rank7_order8_theorem_eligible_combined_ledger.json"
SOURCE_STREAM = HERE / "rank7_order8_after_packet_spectral_remainder.jsonl.xz"
OUTPUT = HERE / "rank7_order8_structural_cycle_gram_lane.json"
OWNERS = HERE / "rank7_order8_structural_cycle_gram_owners.jsonl.xz"
REMAINDER = HERE / "rank7_order8_after_structural_cycle_gram_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-eight-structural-cycle-gram-lane-v1"
ORDER = 8
PATH_COUNT = 14
TARGETS_PER_ROW = 15
BUDGET = Fraction(6)
EXPECTED_REMAINDER = 83856
TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 2)
F = Fraction
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


def pair(value):
    return [value.numerator, value.denominator]


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              RuntimeError(f"nonstandard constant in {label}: {value}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def inverse(matrix):
    size = len(matrix)
    work = [[F(value) for value in row] + [F(i == j) for j in range(size)]
            for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        require(pivot is not None, "singular reduced Laplacian")
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [value / divisor for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [left - multiplier * right
                         for left, right in zip(work[row], work[column])]
    return tuple(tuple(row[size:]) for row in work)


@lru_cache(maxsize=None)
def exact_cycle_projector(endpoints):
    columns = len(endpoints)
    incidence = [[F() for _ in range(columns)] for _ in range(ORDER - 1)]
    for column, (u, v) in enumerate(endpoints):
        if u < ORDER - 1:
            incidence[u][column] = 1
        if v < ORDER - 1:
            incidence[v][column] = -1
    laplacian = [[sum(incidence[u][edge] * incidence[v][edge]
                       for edge in range(columns))
                  for v in range(ORDER - 1)] for u in range(ORDER - 1)]
    laplacian_inverse = inverse(laplacian)
    cut = [[sum(incidence[u][left] * laplacian_inverse[u][v] * incidence[v][right]
                for u in range(ORDER - 1) for v in range(ORDER - 1))
            for right in range(columns)] for left in range(columns)]
    return tuple(tuple(F(left == right) - cut[left][right]
                       for right in range(columns)) for left in range(columns))


def paths_and_types(edges, row):
    signed = [[F() for _ in range(ORDER)] for _ in range(ORDER)]
    incident = [[] for _ in range(ORDER)]
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        value = multiplicity - 2 * odd
        signed[u][v] = signed[v][u] = value
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "physical path total changed")
    signed_degrees = [sum(row) for row in signed]
    keys = [(signed_degrees[u], tuple(sorted(incident[u], reverse=True)))
            for u in range(ORDER)]
    dictionary = {key: index for index, key in enumerate(sorted(set(keys)))}
    return (tuple(tuple(row) for row in signed), tuple(paths), tuple(keys),
            tuple(dictionary[key] for key in keys))


def exact_cycle_core(paths):
    projector = exact_cycle_projector(tuple((u, v) for _, _, u, v, _ in paths))
    incidence = [[F() for _ in paths] for _ in range(ORDER)]
    for column, (_, _, u, v, length) in enumerate(paths):
        incidence[u][column] = 1
        incidence[v][column] = -1 if length & 1 else 1
    projected = [[sum(incidence[u][left] * projector[left][right]
                      for left in range(len(paths)))
                  for right in range(len(paths))] for u in range(ORDER)]
    return tuple(tuple(sum(x * y for x, y in zip(projected[u], projected[v]))
                       for v in range(ORDER)) for u in range(ORDER))


def numerical_cycle_core(paths):
    incidence = np.zeros((ORDER - 1, len(paths)))
    for column, (_, _, u, v, _) in enumerate(paths):
        if u < ORDER - 1:
            incidence[u, column] = 1.0
        if v < ORDER - 1:
            incidence[v, column] = -1.0
    cycle = np.eye(len(paths)) - incidence.T @ np.linalg.inv(incidence @ incidence.T) @ incidence
    signed = np.zeros((ORDER, len(paths)))
    for column, (_, _, u, v, length) in enumerate(paths):
        signed[u, column] = 1.0
        signed[v, column] = -1.0 if length & 1 else 1.0
    projected = signed @ cycle
    return projected @ projected.T


def numerical_cost(parameters, signed, cycle_core, paths, type_ids):
    type_total = (len(parameters) - 1) // 2
    ids = np.asarray(type_ids)
    diagonal = np.exp(parameters[:type_total])[ids]
    coefficient = parameters[type_total:2 * type_total][ids]
    x = np.diag(diagonal) + np.diag(coefficient) @ signed
    square = x @ x.T + np.exp(parameters[-1]) * cycle_core
    normalizer = np.max(np.diag(square))
    total = 0.0
    for _, _, u, v, length in paths:
        correlation = square[u, v] / normalizer
        transformed = -correlation if length & 1 else correlation
        if transformed <= -1.0 + 1e-12:
            return 1e6
        total += (1.0 - transformed) / (length * (1.0 + transformed))
    return total


def exact_cost(signed, cycle_core, paths, type_ids, parameters, cycle_weight):
    x = [[(parameters[type_ids[u]][0] if u == v else F()) +
          parameters[type_ids[u]][1] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    core = [[sum(x[u][w] * x[v][w] for w in range(ORDER)) +
             cycle_weight * cycle_core[u][v]
             for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(core[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero Gram normalizer")
    total = F()
    for _, _, u, v, length in paths:
        correlation = core[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "exact correlation escaped [-1,1]")
        if transformed == -1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


def family(edges, row):
    kinds = [0, 0, 0]
    adjacency = [set() for _ in range(ORDER)]
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        adjacency[u].add(v)
        adjacency[v].add(u)
        kinds[0 if odd == 0 else 2 if odd == multiplicity else 1] += 1
    triangles = sum(len(adjacency[u] & adjacency[v])
                    for u in range(ORDER) for v in adjacency[u] if u < v) // 3
    return (tuple(sorted((edge[2] for edge in edges), reverse=True)), tuple(kinds),
            len(edges) - ORDER + 1, triangles)


def worker(record):
    max_denominator = _CONTEXT
    _, source_index, _, raw_edges, raw_row, _ = record
    edges = tuple(map(tuple, raw_edges))
    row = tuple(raw_row)
    signed, paths, type_keys, type_ids = paths_and_types(edges, row)
    matrix = np.asarray(signed, dtype=np.float64)
    cycle_numerical = numerical_cycle_core(paths)
    type_total = max(type_ids) + 1
    initial = np.concatenate((np.zeros(type_total), np.full(type_total, 0.5), [-2.0]))
    proposal = minimize(numerical_cost, initial,
                        args=(matrix, cycle_numerical, paths, type_ids),
                        method="Powell",
                        bounds=[(-2.0, 2.0)] * type_total +
                               [(-4.0, 4.0)] * type_total + [(-8.0, 4.0)],
                        options={"ftol": 1e-7, "maxiter": 180})
    parameters = tuple(
        (F(float(np.exp(proposal.x[k]))).limit_denominator(max_denominator),
         F(float(proposal.x[type_total + k])).limit_denominator(max_denominator))
        for k in range(type_total))
    cycle_weight = F(float(np.exp(proposal.x[-1]))).limit_denominator(max_denominator)
    cost, normalizer = exact_cost(signed, exact_cycle_core(paths), paths, type_ids,
                                  parameters, cycle_weight)
    return (source_index, cost, normalizer, parameters, cycle_weight, type_keys,
            float(proposal.fun))


def scan(workers, max_denominator, progress=False, limit=None, persist=True):
    global _CONTEXT
    ledger_raw = SOURCE_LEDGER.read_bytes()
    ledger = strict_json(ledger_raw, SOURCE_LEDGER.name)
    require(ledger_raw == canonical_bytes(ledger), "noncanonical theorem ledger")
    source_info = ledger["exact_remainder_stream"]
    require(ledger["remaining_residual_total"] == EXPECTED_REMAINDER and
            source_info["record_total"] == EXPECTED_REMAINDER and
            file_sha256(SOURCE_STREAM) == source_info["artifact_sha256"],
            "wrong authenticated theorem remainder")

    digest = hashlib.sha256()
    records = []
    all_records = []
    strata = Counter()
    physical_strata = Counter()
    physical = target_physical = 0
    with lzma.open(SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = strict_json(raw, SOURCE_STREAM.name)
            require(raw == canonical_bytes(record) and len(record) == 6,
                    "noncanonical remainder row")
            digest.update(raw)
            all_records.append((record, raw))
            physical += record[5]
            key = family(tuple(map(tuple, record[3])), tuple(record[4]))
            strata[key] += 1
            physical_strata[key] += record[5]
            if key == TARGET and (limit is None or len(records) < limit):
                records.append(record)
                target_physical += record[5]
    require(len(all_records) == EXPECTED_REMAINDER and
            digest.hexdigest() == source_info["raw_sha256"],
            "full source remainder authentication failed")
    require(strata[TARGET] == 6929, "leading family count changed")

    _CONTEXT = max_denominator
    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=16)

    owners = []
    classification = hashlib.sha256()
    denominator_counts = Counter()
    for position, (record, result) in enumerate(zip(records, results, strict=True), 1):
        source_index, cost, normalizer, parameters, cycle_weight, type_keys, numerical = result
        accepted = cost is not None and cost <= BUDGET
        certificate = [source_index, accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[pair(left), pair(right)] for left, right in parameters],
                       pair(cycle_weight)]
        classification.update(canonical_bytes(certificate))
        if accepted:
            denominator_counts.update([cycle_weight.denominator] +
                                      [value.denominator for values in parameters
                                       for value in values])
            owners.append((record, certificate, numerical,
                           [[int(key[0]), [list(value) for value in key[1]]]
                            for key in sorted(set(type_keys))]))
        if progress and position % 500 == 0:
            print(f"target={position}/{len(records)} owned={len(owners)}", flush=True)
    if executor is not None:
        executor.shutdown()

    owner_indices = {record[0] for record, _, _, _ in owners}
    owner_raw_digest = hashlib.sha256()
    remainder_raw_digest = hashlib.sha256()
    if persist:
        owner_tmp = OWNERS.with_name(OWNERS.name + ".tmp")
        with lzma.open(owner_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for payload in owners:
                raw = canonical_bytes(payload)
                output.write(raw)
                owner_raw_digest.update(raw)
        owner_tmp.replace(OWNERS)
        remainder_tmp = REMAINDER.with_name(REMAINDER.name + ".tmp")
        with lzma.open(remainder_tmp, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for record, raw in all_records:
                if record[0] not in owner_indices:
                    output.write(raw)
                    remainder_raw_digest.update(raw)
        remainder_tmp.replace(REMAINDER)

    ranked = sorted(strata, key=lambda key: (-strata[key], -physical_strata[key], key))
    result = {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "full authenticated 83,856-row theorem-eligible order-eight remainder",
        "source_ledger": {"path": SOURCE_LEDGER.name,
                          "sha256": hashlib.sha256(ledger_raw).hexdigest()},
        "source_stream": source_info,
        "scanned_remainder_total": len(all_records),
        "scanned_remainder_physical_total": physical,
        "dominant_family_total": len(strata),
        "dominant_families": [{"multiplicity_partition": list(key[0]),
                               "bundle_types": list(key[1]), "cycle_rank": key[2],
                               "triangle_total": key[3], "orbit_total": strata[key],
                               "physical_total": physical_strata[key]}
                              for key in ranked],
        "target_family": {"multiplicity_partition": list(TARGET[0]),
                          "bundle_types": list(TARGET[1]), "cycle_rank": TARGET[2],
                          "triangle_total": TARGET[3], "orbit_total": strata[TARGET],
                          "physical_total": physical_strata[TARGET],
                          "scanned_total": len(records)},
        "gram": {
            "formula": "H=XX^T+w A P_cycle A^T; G=H/M+diag(1-diag(H)/M)",
            "typed_feature": "X=D0+D1*S, with D0,D1 constant on exact local types",
            "local_type": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
            "cycle_projector": "P_cycle=I-B^T(BB^T)^-1B on physical-path coordinates",
            "psd_proof": "XX^T and w(A P_cycle)(A P_cycle)^T are Gram squares; diagonal completion is a nonnegative coordinate-square sum",
            "exact_acceptance": "rational replay of every Gram entry and canonical path-chain cost at most six",
            "maximum_denominator": max_denominator,
        },
        "theorem_lift": {
            "all_length": "for fixed parity and Gram, each nonnegative path cost (1-t)/(L(1+t)) weakly decreases when L increases by two",
            "induced_owner": "each accepted kernel realization is owned together with every same-parity subdivision it induces",
            "rooted_trees": "DNN one-vertex additivity supplies arbitrary rooted-tree attachments",
        },
        "owned_orbit_total": len(owners),
        "owned_physical_total": sum(record[5] for record, _, _, _ in owners),
        "owned_target_total": len(owners) * TARGETS_PER_ROW,
        "remaining_remainder_total": EXPECTED_REMAINDER - len(owners),
        "remaining_target_family_total": strata[TARGET] - len(owners),
        "classification_stream_sha256": classification.hexdigest(),
        "used_denominators": dict(sorted(denominator_counts.items())),
        "owner_stream": None,
        "reduced_remainder_stream": None,
        "claim_boundary": "only exact accepted rows and their all-length/rooted-tree lifts are theorem-owned; every other row remains unclassified",
    }
    if persist:
        result["owner_stream"] = {"path": OWNERS.name, "record_total": len(owners),
                                  "raw_sha256": owner_raw_digest.hexdigest(),
                                  "artifact_sha256": file_sha256(OWNERS)}
        result["reduced_remainder_stream"] = {
            "path": REMAINDER.name, "record_total": EXPECTED_REMAINDER - len(owners),
            "raw_sha256": remainder_raw_digest.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER),
        }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--max-denominator", type=int, default=256)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT)
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
        require(args.output.read_bytes() == raw, "report does not reproduce byte-for-byte")
    elif args.limit is None:
        args.output.write_bytes(raw)
    print(f"scanned={result['scanned_remainder_total']} "
          f"target={result['target_family']['scanned_total']} "
          f"owned={result['owned_orbit_total']} "
          f"remaining={result['remaining_remainder_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
