#!/usr/bin/env python3
"""Exact typed/cycle/effective-resistance Gram lane for order twelve."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import lzma
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
PACKET_PATH = HERE / "rank7_order12_typed_packet_gram_lane.py"
STRATIFICATION_PATH = HERE / "rank7_order12_remainder_stratification.json"
SOURCE_REPORT = HERE / "rank7_order12_typed_packet_gram_lane.json"
SOURCE_STREAM = HERE / "rank7_order12_after_typed_packet_remainder.jsonl.xz"
OUTPUT_PATH = HERE / "rank7_order12_next_family_resistance_gram_lane.json"
OWNER_STREAM = HERE / "rank7_order12_next_family_resistance_gram_owners.jsonl.xz"
REMAINDER_STREAM = HERE / "rank7_order12_after_resistance_gram_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-twelve-next-family-resistance-gram-lane-v1"
ORDER = 12
PATH_COUNT = 18
TARGETS_PER_ROW = 19
BUDGET = Fraction(6)
F = Fraction
TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
          (6, 3, 6), 4, 0, 0)
EXPECTED_SOURCE_TOTAL = 122505
EXPECTED_TARGET_TOTAL = 9801
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


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def json_file(path):
    raw = path.read_bytes()
    return json.loads(raw.decode("ascii")), hashlib.sha256(raw).hexdigest()


def pair(value):
    return [value.numerator, value.denominator]


def inverse(matrix):
    size = len(matrix)
    work = [[F(value) for value in row] + [F(i == j) for j in range(size)]
            for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        require(pivot is not None, "singular reduced physical Laplacian")
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
def cut_projector(endpoints):
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
    return tuple(tuple(sum(
        incidence[u][left] * laplacian_inverse[u][v] * incidence[v][right]
        for u in range(ORDER - 1) for v in range(ORDER - 1))
        for right in range(columns)) for left in range(columns))


def resistance_cycle_core(paths):
    endpoints = tuple((u, v) for u, v, _ in paths)
    cut = cut_projector(endpoints)
    signed_incidence = [[F() for _ in paths] for _ in range(ORDER)]
    for column, (u, v, length) in enumerate(paths):
        signed_incidence[u][column] = 1
        signed_incidence[v][column] = -1 if length & 1 else 1
    projected = [[signed_incidence[u][column] - sum(
        signed_incidence[u][left] * cut[left][column]
        for left in range(len(paths))) for column in range(len(paths))]
        for u in range(ORDER)]
    weights = []
    for column in range(len(paths)):
        resistance = cut[column][column]
        require(F() < resistance < F(1), "target path is not cyclic")
        weights.append((1 - resistance) / resistance)
    return tuple(tuple(sum(weights[column] * projected[u][column] *
                               projected[v][column]
                           for column in range(len(paths)))
                       for v in range(ORDER)) for u in range(ORDER))


def numerical_cost(parameters, signed, cycle_core, paths, type_ids):
    type_total = (len(parameters) - 1) // 2
    ids = np.asarray(type_ids)
    diagonal = np.exp(parameters[:type_total])[ids]
    coefficient = parameters[type_total:2 * type_total][ids]
    cycle_weight = np.exp(parameters[-1])
    feature = np.diag(diagonal) + np.diag(coefficient) @ signed
    core = feature @ feature.T + cycle_weight * cycle_core
    normalizer = np.max(np.diag(core))
    total = 0.0
    for u, v, length in paths:
        correlation = core[u, v] / normalizer
        transformed = -correlation if length & 1 else correlation
        if transformed <= -1.0 + 1e-12:
            return 1e6
        total += (1.0 - transformed) / (length * (1.0 + transformed))
    return total


def exact_cost(signed, cycle_core, paths, type_ids, parameters, cycle_weight):
    feature = [[(parameters[type_ids[u]][0] if u == v else F()) +
                parameters[type_ids[u]][1] * signed[u][v]
                for v in range(ORDER)] for u in range(ORDER)]
    core = [[sum(feature[u][w] * feature[v][w] for w in range(ORDER)) +
             cycle_weight * cycle_core[u][v]
             for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(core[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero exact Gram normalizer")
    total = F()
    for u, v, length in paths:
        correlation = core[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "exact PSD correlation escaped [-1,1]")
        if transformed == -1:
            return None, normalizer
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer


def worker(record):
    packet, kernels, max_denominator = _CONTEXT
    source_index, global_kernel, order_kernel, raw_row, _ = record
    edges = kernels[order_kernel]
    signed, paths, type_keys, type_ids = packet.matrix_and_paths(edges, tuple(raw_row))
    cycle_exact = resistance_cycle_core(paths)
    matrix = np.asarray(signed, dtype=np.float64)
    cycle_numerical = np.asarray(cycle_exact, dtype=np.float64)
    type_total = max(type_ids) + 1
    initial = np.concatenate((np.zeros(type_total), np.full(type_total, 0.5),
                              np.asarray([-2.0])))
    proposal = minimize(
        numerical_cost, initial,
        args=(matrix, cycle_numerical, paths, type_ids), method="Powell",
        bounds=([(-2.0, 2.0)] * type_total + [(-4.0, 4.0)] * type_total +
                [(-8.0, 4.0)]),
        options={"ftol": 1e-8, "maxiter": 180})
    parameters = tuple(
        (F(float(np.exp(proposal.x[index]))).limit_denominator(max_denominator),
         F(float(proposal.x[type_total + index])).limit_denominator(max_denominator))
        for index in range(type_total))
    cycle_weight = F(float(np.exp(proposal.x[-1]))).limit_denominator(max_denominator)
    cost, normalizer = exact_cost(signed, cycle_exact, paths, type_ids, parameters,
                                  cycle_weight)
    return (source_index, global_kernel, cost, normalizer, parameters, cycle_weight,
            type_keys, float(proposal.fun))


def family(packet, edges, row):
    base = packet.family(edges, row)
    adjacency = [set() for _ in range(ORDER)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    discovery = [-1] * ORDER
    low = [0] * ORDER
    timer = bridges = 0

    def visit(vertex, parent):
        nonlocal timer, bridges
        discovery[vertex] = low[vertex] = timer
        timer += 1
        for neighbor in adjacency[vertex]:
            if neighbor == parent:
                continue
            if discovery[neighbor] < 0:
                visit(neighbor, vertex)
                low[vertex] = min(low[vertex], low[neighbor])
                bridges += low[neighbor] > discovery[vertex]
            else:
                low[vertex] = min(low[vertex], discovery[neighbor])
    visit(0, -1)
    return (*base, bridges)


def scan(workers, max_denominator, progress=False, limit=None, persist=True):
    global _CONTEXT
    packet = load("rank7_order12_resistance_packet", PACKET_PATH)
    source_report, source_report_sha256 = json_file(SOURCE_REPORT)
    stratification, stratification_sha256 = strict_json(STRATIFICATION_PATH)
    source_info = source_report["updated_remainder_stream"]
    require(source_report["remaining_remainder_orbit_total"] == EXPECTED_SOURCE_TOTAL and
            source_info["record_total"] == EXPECTED_SOURCE_TOTAL and
            file_sha256(SOURCE_STREAM) == source_info["artifact_sha256"],
            "wrong authenticated after-packet remainder")
    kernels = packet.kernel_dictionary()
    all_records = []
    records = []
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
            if family(packet, kernels[record[2]], tuple(record[3])) == TARGET and (
                    limit is None or len(records) < limit):
                records.append(record)
                target_physical += record[4]
    require((len(all_records), physical, source_digest.hexdigest()) ==
            (source_info["record_total"], source_info["physical_total"],
             source_info["raw_sha256"]), "source remainder authentication failed")
    expected = stratification["stratification"]["dominant"]["top_strata"][0]
    require(expected["signature"] == {
        "multiplicity_partition": list(TARGET[0]), "bundle_types": list(TARGET[1]),
        "cycle_rank": TARGET[2], "triangle_total": TARGET[3],
        "bridge_total": TARGET[4]}, "largest stratified family changed")
    if limit is None:
        require(len(records) == expected["orbit_total"] == EXPECTED_TARGET_TOTAL,
                "target family count changed")

    _CONTEXT = packet, kernels, max_denominator
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
        (source_index, _, cost, normalizer, parameters, cycle_weight, type_keys,
         numerical) = result
        accepted = cost is not None and cost <= BUDGET
        certificate = [source_index, accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[pair(left), pair(right)] for left, right in parameters],
                       pair(cycle_weight)]
        classification.update(canonical_bytes(certificate))
        if cost is not None:
            minimum = cost if minimum is None or cost < minimum else minimum
        if accepted:
            denominator_counts.update(
                [cycle_weight.denominator] +
                [value.denominator for values in parameters for value in values])
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
        temporary = OWNER_STREAM.with_name(OWNER_STREAM.name + ".tmp")
        with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for payload in owners:
                raw = canonical_bytes(payload)
                output.write(raw)
                owner_raw.update(raw)
        temporary.replace(OWNER_STREAM)
        temporary = REMAINDER_STREAM.with_name(REMAINDER_STREAM.name + ".tmp")
        with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
            for record, raw in all_records:
                if record[0] in owner_indices:
                    continue
                output.write(raw)
                remainder_raw.update(raw)
                remainder_total += 1
                remainder_physical += record[4]
        temporary.replace(REMAINDER_STREAM)
    else:
        remainder_total = len(all_records) - len(owners)
        remainder_physical = physical - sum(record[4] for record, _, _, _ in owners)
    owner_physical = sum(record[4] for record, _, _, _ in owners)
    require(remainder_total + len(owners) == len(all_records) and
            remainder_physical + owner_physical == physical,
            "updated remainder partition changed")

    report = {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "full exact typed/cycle/effective-resistance Gram replay of the largest remaining stratified order-twelve family",
        "source_report": {"path": SOURCE_REPORT.name, "sha256": source_report_sha256},
        "source_stratification": {"path": STRATIFICATION_PATH.name,
                                  "sha256": stratification_sha256},
        "source_remainder": source_info,
        "scanned_remainder_orbit_total": len(all_records),
        "scanned_remainder_physical_total": physical,
        "target_family": {"multiplicity_partition": list(TARGET[0]),
                          "bundle_types": list(TARGET[1]),
                          "cycle_rank": TARGET[2], "triangle_total": TARGET[3],
                          "bridge_total": TARGET[4],
                          "orbit_total": expected["orbit_total"],
                          "physical_total": expected["physical_total"],
                          "scanned_total": len(records)},
        "gram": {
            "formula": "H=XX^T+w A P_cycle diag(q) P_cycle A^T; G=H/M+diag(1-diag(H)/M)",
            "typed_feature": "X=D0+D1*S, with D0,D1 constant on exact local types",
            "local_type": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
            "cycle_projector": "P_cycle=I-B^T(BB^T)^-1B on physical-path coordinates",
            "effective_resistance": "R_e=(P_cut)_{e,e}; q_e=(1-R_e)/R_e",
            "signed_incidence": "A has entries 1 and (-1)^L at physical-path endpoints",
            "psd_proof": "XX^T and w(A P_cycle)diag(q)(A P_cycle)^T are exact Gram sums for w,q>=0; diagonal completion adds nonnegative coordinate squares",
            "proposal": "one deterministic binary64 Powell start at D0=1,D1=1/2,w=exp(-2)",
            "exact_replay": "all typed entries and w are rounded to bounded rational fractions before exact projector, resistance weights, and cost acceptance",
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
        report["owner_stream"] = {
            "path": OWNER_STREAM.name, "record_total": len(owners),
            "physical_total": owner_physical, "raw_sha256": owner_raw.hexdigest(),
            "artifact_sha256": file_sha256(OWNER_STREAM)}
        report["updated_remainder_stream"] = {
            "path": REMAINDER_STREAM.name, "record_total": remainder_total,
            "physical_total": remainder_physical,
            "raw_sha256": remainder_raw.hexdigest(),
            "artifact_sha256": file_sha256(REMAINDER_STREAM)}
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-denominator", type=int, default=256)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.workers > 0 and args.max_denominator > 0 and
            (args.limit is None or args.limit > 0), "invalid scan parameters")
    require(not args.audit or args.limit is None, "partial scans cannot audit")
    report = scan(args.workers, args.max_denominator, args.progress, args.limit,
                  persist=args.limit is None)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "resistance report does not reproduce")
    elif args.limit is None:
        args.output.write_bytes(raw)
    print(f"scanned={report['scanned_remainder_orbit_total']} "
          f"target={report['target_family']['scanned_total']} "
          f"owned={report['owned_orbit_total']} "
          f"remaining={report['remaining_remainder_orbit_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
