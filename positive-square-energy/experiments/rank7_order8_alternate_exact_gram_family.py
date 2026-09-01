#!/usr/bin/env python3
"""Exact simplex-glued resistance-packet Gram scan of the fourth order-eight family."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

import rank7_order8_structural_cycle_gram_lane as base


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "rank7_order8_alternate_exact_gram_family.json"
OWNERS = HERE / "rank7_order8_alternate_exact_gram_family_owners.jsonl.xz"
SCHEMA = "rank-seven-order-eight-alternate-exact-gram-family-v1"
F = Fraction
_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def pair(value):
    return [value.numerator, value.denominator]


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def resistance_cycle_core(paths):
    endpoints = tuple((u, v) for _, _, u, v, _ in paths)
    cycle = base.exact_cycle_projector(endpoints)
    cut = tuple(tuple(F(left == right) - cycle[left][right]
                      for right in range(len(paths)))
                for left in range(len(paths)))
    signed = [[F() for _ in paths] for _ in range(base.ORDER)]
    for column, (_, _, u, v, length) in enumerate(paths):
        signed[u][column] = 1
        signed[v][column] = -1 if length & 1 else 1
    projected = [[sum(signed[u][left] * cycle[left][column]
                      for left in range(len(paths)))
                  for column in range(len(paths))] for u in range(base.ORDER)]
    weights = []
    for column in range(len(paths)):
        resistance = cut[column][column]
        require(F() < resistance < F(1), "target path is not cyclic")
        weights.append((1 - resistance) / resistance)
    return tuple(tuple(sum(weights[column] * projected[u][column] *
                           projected[v][column]
                           for column in range(len(paths)))
                       for v in range(base.ORDER)) for u in range(base.ORDER))


def triangle_simplex_cores(edges):
    adjacency = [set() for _ in range(base.ORDER)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = []
    for u in range(base.ORDER):
        for v in adjacency[u]:
            if u >= v:
                continue
            for w in adjacency[u] & adjacency[v]:
                if v < w:
                    triangles.append((u, v, w))
    require(len(triangles) == 1, "target no longer has exactly one triangle")
    triangle = triangles[0]
    cores = []
    for signs in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)):
        core = [[F() for _ in range(base.ORDER)] for _ in range(base.ORDER)]
        for left, u in enumerate(triangle):
            for right, v in enumerate(triangle):
                simplex = F(1) if left == right else F(-1, 2)
                core[u][v] = signs[left] * signs[right] * simplex
        cores.append(tuple(tuple(row) for row in core))
    return triangle, tuple(cores)


def square(matrix):
    return tuple(tuple(sum(matrix[u][w] * matrix[w][v]
                           for w in range(base.ORDER))
                       for v in range(base.ORDER)) for u in range(base.ORDER))


def feature_core(signed, signed_square, parameters):
    feature = [[(parameters[u][0] if u == v else F()) +
                parameters[u][1] * signed[u][v] +
                parameters[u][2] * signed_square[u][v]
                for v in range(base.ORDER)] for u in range(base.ORDER)]
    return [[sum(feature[u][w] * feature[v][w] for w in range(base.ORDER))
             for v in range(base.ORDER)] for u in range(base.ORDER)]


def exact_cost(signed, signed_square, paths, resistance, simplex, parameters,
               resistance_weight, simplex_weight):
    core = feature_core(signed, signed_square, parameters)
    for u in range(base.ORDER):
        for v in range(base.ORDER):
            core[u][v] += (resistance_weight * resistance[u][v] +
                           simplex_weight * simplex[u][v])
    normalizer = max(core[u][u] for u in range(base.ORDER))
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


def numerical_cost(vector, signed, signed_square, paths, resistance, simplex):
    parameters = vector[:3 * base.ORDER].reshape((base.ORDER, 3)).copy()
    parameters[:, 0] = np.exp(parameters[:, 0])
    feature = (np.diag(parameters[:, 0]) +
               np.diag(parameters[:, 1]) @ signed +
               np.diag(parameters[:, 2]) @ signed_square)
    core = (feature @ feature.T + np.exp(vector[-2]) * resistance +
            np.exp(vector[-1]) * simplex)
    normalizer = np.max(np.diag(core))
    total = 0.0
    for _, _, u, v, length in paths:
        correlation = core[u, v] / normalizer
        transformed = -correlation if length & 1 else correlation
        if transformed <= -1.0 + 1e-12:
            return 1e6
        total += (1.0 - transformed) / (length * (1.0 + transformed))
    return total


def worker(record):
    max_denominator = _CONTEXT
    _, source_index, _, raw_edges, raw_row, _ = record
    edges = tuple(map(tuple, raw_edges))
    row = tuple(raw_row)
    signed, paths, _, _ = base.paths_and_types(edges, row)
    signed_square = square(signed)
    resistance = resistance_cycle_core(paths)
    triangle, simplex_cores = triangle_simplex_cores(edges)
    signed_np = np.asarray(signed, dtype=np.float64)
    square_np = np.asarray(signed_square, dtype=np.float64)
    resistance_np = np.asarray(resistance, dtype=np.float64)
    best = None
    best_orientation = None
    for orientation, simplex in enumerate(simplex_cores):
        simplex_np = np.asarray(simplex, dtype=np.float64)
        for coefficient in (0.5, -0.5):
            initial = np.zeros(3 * base.ORDER + 2)
            initial[1:3 * base.ORDER:3] = coefficient
            initial[-2:] = (-2.0, -2.0)
            proposal = minimize(
                numerical_cost, initial,
                args=(signed_np, square_np, paths, resistance_np, simplex_np),
                method="Powell",
                bounds=([(-2.0, 2.0), (-4.0, 4.0), (-2.0, 2.0)] * base.ORDER +
                        [(-10.0, 4.0), (-10.0, 4.0)]),
                options={"ftol": 1e-8, "maxiter": 260})
            if best is None or proposal.fun < best.fun:
                best = proposal
                best_orientation = orientation
    require(best is not None and best_orientation is not None, "no numerical proposal")
    parameters = tuple(
        (F(float(np.exp(best.x[3 * u]))).limit_denominator(max_denominator),
         F(float(best.x[3 * u + 1])).limit_denominator(max_denominator),
         F(float(best.x[3 * u + 2])).limit_denominator(max_denominator))
        for u in range(base.ORDER))
    resistance_weight = F(float(np.exp(best.x[-2]))).limit_denominator(max_denominator)
    simplex_weight = F(float(np.exp(best.x[-1]))).limit_denominator(max_denominator)
    cost, normalizer = exact_cost(
        signed, signed_square, paths, resistance, simplex_cores[best_orientation],
        parameters, resistance_weight, simplex_weight)
    return (source_index, cost, normalizer, parameters, resistance_weight,
            simplex_weight, best_orientation, triangle, float(best.fun))


def source_records(limit=None):
    base.configure_fourth_family()
    ledger_raw = base.SOURCE_LEDGER.read_bytes()
    ledger = base.strict_json(ledger_raw, base.SOURCE_LEDGER.name)
    source_info = ledger["reduced_remainder_stream"]
    require(ledger["remaining_remainder_total"] == base.EXPECTED_REMAINDER and
            source_info["record_total"] == base.EXPECTED_REMAINDER and
            file_sha256(base.SOURCE_STREAM) == source_info["artifact_sha256"],
            "wrong authenticated third-family remainder")
    digest = hashlib.sha256()
    records = []
    family_total = family_physical = 0
    with lzma.open(base.SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = base.strict_json(raw, base.SOURCE_STREAM.name)
            require(raw == canonical_bytes(record) and len(record) == 6,
                    "noncanonical remainder row")
            digest.update(raw)
            key = base.family(tuple(map(tuple, record[3])), tuple(record[4]))
            if key == base.TARGET:
                family_total += 1
                family_physical += record[5]
                if limit is None or len(records) < limit:
                    records.append(record)
    require(digest.hexdigest() == source_info["raw_sha256"] and
            family_total == base.EXPECTED_TARGET, "source family authentication failed")
    return ledger_raw, source_info, records, family_total, family_physical


def scan(workers, max_denominator, progress=False, limit=None, persist=True):
    global _CONTEXT
    ledger_raw, source_info, records, family_total, family_physical = source_records(limit)
    _CONTEXT = max_denominator
    if workers == 1:
        results = map(worker, records)
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker, records, chunksize=4)
    owners = []
    classification = hashlib.sha256()
    denominators = Counter()
    minimum = None
    for position, (record, result) in enumerate(zip(records, results, strict=True), 1):
        (source_index, cost, normalizer, parameters, resistance_weight,
         simplex_weight, orientation, triangle, numerical) = result
        accepted = cost is not None and cost <= base.BUDGET
        certificate = [source_index, accepted, None if cost is None else pair(cost),
                       pair(normalizer),
                       [[[value.numerator, value.denominator] for value in row]
                        for row in parameters],
                       pair(resistance_weight), pair(simplex_weight), orientation]
        classification.update(canonical_bytes(certificate))
        if cost is not None and (minimum is None or cost < minimum):
            minimum = cost
        if accepted:
            denominators.update([resistance_weight.denominator,
                                 simplex_weight.denominator] +
                                [value.denominator for row in parameters for value in row])
            owners.append([record, certificate, numerical, list(triangle)])
        if progress and position % 50 == 0:
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
        "schema": SCHEMA,
        "full_theorem": len(owners) == family_total,
        "scope": "full authenticated 2^4 1^6, (2,4,4), rank-three, one-triangle family",
        "source_report": {"path": base.SOURCE_LEDGER.name,
                          "sha256": hashlib.sha256(ledger_raw).hexdigest()},
        "source_stream": source_info,
        "target_family": {
            "multiplicity_partition": list(base.TARGET[0]),
            "bundle_types": list(base.TARGET[1]), "cycle_rank": base.TARGET[2],
            "triangle_total": base.TARGET[3], "orbit_total": family_total,
            "physical_total": family_physical, "scanned_total": len(records)},
        "gram": {
            "formula": "H=XX^T+w_r A P_cycle diag((1-R)/R) P_cycle A^T+w_s Q_triangle; G=H/M+diag(1-diag(H)/M)",
            "induced_packet": "X=D0+D1*S+D2*S^2 with independent rational row coefficients",
            "effective_resistance": "R_e=(P_cut)_{e,e} on physical-path coordinates",
            "simplex_gluing": "Q_triangle is one of the four switchings of the embedded regular 2-simplex Gram",
            "psd_proof": "each displayed core is an exact rational Gram sum with nonnegative weight; diagonal completion is nonnegative",
            "exact_acceptance": "bounded-denominator rational replay of every correlation and canonical path cost at most six",
            "maximum_denominator": max_denominator},
        "theorem_lift": {
            "all_length": "at fixed parity and Gram, each path term decreases when its length increases by two",
            "induced_owner": "each accepted kernel owns every same-parity subdivision induced from it",
            "rooted_trees": "DNN one-vertex additivity supplies arbitrary rooted-tree attachments"},
        "owned_orbit_total": len(owners),
        "owned_physical_total": sum(owner[0][5] for owner in owners),
        "owned_target_total": len(owners) * base.TARGETS_PER_ROW,
        "remaining_target_family_total": family_total - len(owners),
        "minimum_exact_cost": None if minimum is None else pair(minimum),
        "classification_stream_sha256": classification.hexdigest(),
        "used_denominators": dict(sorted(denominators.items())),
        "owner_stream": None,
        "claim_boundary": "only exact accepted rows and their all-length/rooted-tree lifts are theorem-owned"}
    if persist:
        report["owner_stream"] = {
            "path": OWNERS.name, "record_total": len(owners),
            "raw_sha256": owner_raw.hexdigest(), "artifact_sha256": file_sha256(OWNERS)}
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-denominator", type=int, default=512)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path, default=OUTPUT)
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
        require(args.output.read_bytes() == raw, "report does not reproduce")
    elif args.limit is None:
        args.output.write_bytes(raw)
    print(f"target={report['target_family']['scanned_total']} "
          f"owned={report['owned_orbit_total']} "
          f"remaining={report['remaining_target_family_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
