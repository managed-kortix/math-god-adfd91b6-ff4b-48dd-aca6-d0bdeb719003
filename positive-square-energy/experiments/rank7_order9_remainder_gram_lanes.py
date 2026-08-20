#!/usr/bin/env python3
"""Test exact scalar and typed SOS Gram lanes on the order-nine remainder."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
STRATIFIER = HERE / "rank7_order9_unowned_stratifier.py"
OWNER_MANIFEST = HERE / "rank7_order9_structural_owner_manifest.json"
DEFAULT_OUTPUT = HERE / "rank7_order9_remainder_gram_lanes.json"
SCHEMA = "rank-seven-order-nine-remainder-gram-lanes-v1"
ORDER = 9
PATH_COUNT = 15
BUDGET = Fraction(6)
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def pair(value):
    return [value.numerator, value.denominator]


def load_stratifier():
    spec = importlib.util.spec_from_file_location("rank7_order9_gram_stratifier", STRATIFIER)
    require(spec is not None and spec.loader is not None, "cannot load remainder reader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rationals(max_denominator, maximum):
    return tuple(sorted({F(numerator, denominator)
                         for denominator in range(1, max_denominator + 1)
                         for numerator in range(maximum * denominator + 1)}))


def matrix_and_paths(edges, row):
    signed = [[0] * ORDER for _ in range(ORDER)]
    paths = []
    incident = [[] for _ in range(ORDER)]
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        value = multiplicity - 2 * odd
        signed[u][v] = signed[v][u] = value
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "remainder row path count changed")
    keys = tuple((sum(signed[u]), tuple(sorted(incident[u]))) for u in range(ORDER))
    dictionary = {key: index for index, key in enumerate(sorted(set(keys)))}
    type_ids = tuple(dictionary[key] for key in keys)
    return signed, tuple(paths), keys, type_ids


def square_matrix(signed):
    return [[sum(signed[u][w] * signed[w][v] for w in range(ORDER))
             for v in range(ORDER)] for u in range(ORDER)]


def scalar_cost(signed, paths, coefficient):
    square = square_matrix(signed)
    normalizer = 1 + coefficient * coefficient * max(square[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero scalar feature normalizer")
    total = F()
    for _, _, u, v, length in paths:
        correlation = (2 * coefficient * signed[u][v] +
                       coefficient * coefficient * square[u][v]) / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "scalar PSD correlation escaped [-1,1]")
        if transformed == -1:
            return None
        total += (1 - transformed) / (length * (1 + transformed))
    return total


def numerical_scalar_costs(signed, paths, candidates):
    matrix = np.asarray(signed, dtype=np.float64)
    square = matrix @ matrix
    values = np.asarray([float(value) for value in candidates])
    normalizers = 1.0 + values * values * np.max(np.diag(square))
    costs = np.zeros(len(values))
    for _, _, u, v, length in paths:
        correlations = (2.0 * values * matrix[u, v] +
                        values * values * square[u, v]) / normalizers
        transformed = -correlations if length & 1 else correlations
        with np.errstate(divide="ignore", invalid="ignore"):
            costs += (1.0 - transformed) / (length * (1.0 + transformed))
    return costs


def typed_cost(signed, paths, type_ids, parameters):
    x = [[(parameters[type_ids[u]][0] if u == v else F()) +
          parameters[type_ids[u]][1] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    square = [[sum(x[u][w] * x[v][w] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(square[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero typed feature normalizer")
    total = F()
    for _, _, u, v, length in paths:
        correlation = square[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "typed PSD correlation escaped [-1,1]")
        if transformed == -1:
            return None
        total += (1 - transformed) / (length * (1 + transformed))
    return total


def typed_search(signed, paths, type_ids, candidates, passes):
    matrix = np.asarray(signed, dtype=np.float64)
    endpoints = np.asarray([(row[2], row[3]) for row in paths], dtype=np.int64)
    lengths = np.asarray([row[4] for row in paths], dtype=np.int64)
    type_count = max(type_ids) + 1
    selected = [(F(1), F())] * type_count
    ids = np.asarray(type_ids)
    eye = np.eye(ORDER)
    values = np.asarray([float(value) for value in candidates])
    for _ in range(passes):
        changed = False
        for kind in range(type_count):
            diagonal0 = np.broadcast_to(
                np.asarray([float(value[0]) for value in selected]),
                (len(candidates), type_count)).copy()
            diagonal1 = np.broadcast_to(
                np.asarray([float(value[1]) for value in selected]),
                (len(candidates), type_count)).copy()
            diagonal0[:, kind] = 1.0
            diagonal1[:, kind] = values
            vertex0 = diagonal0[:, ids]
            vertex1 = diagonal1[:, ids]
            x = eye[None, :, :] * vertex0[:, :, None] + vertex1[:, :, None] * matrix[None, :, :]
            square = x @ np.swapaxes(x, 1, 2)
            normalizer = np.max(np.diagonal(square, axis1=1, axis2=2), axis=1)
            correlations = square[:, endpoints[:, 0], endpoints[:, 1]] / normalizer[:, None]
            correlations[:, (lengths & 1) == 1] *= -1
            with np.errstate(divide="ignore", invalid="ignore"):
                costs = np.sum((1.0 - correlations) /
                               (lengths[None, :] * (1.0 + correlations)), axis=1)
            best = int(np.nanargmin(costs))
            proposal = (F(1), candidates[best])
            if selected[kind] != proposal:
                selected[kind] = proposal
                changed = True
        if not changed:
            break
    cost = typed_cost(signed, paths, type_ids, tuple(selected))
    return cost, tuple(selected)


def scan(owner_path, scalar_candidates, typed_candidates, representative_total,
         typed_passes, progress=False):
    stratifier = load_stratifier()
    owner_manifest, owner_sha256 = stratifier.strict_canonical_json(
        owner_path, "structural owner manifest")
    kernels = stratifier.kernel_dictionary(stratifier.load_scan_engine())
    scalar_owners = Counter()
    scalar_digest = hashlib.sha256()
    typed_digest = hashlib.sha256()
    scalar_covered = typed_covered = scanned = 0
    representatives = []
    first_scalar_owner = first_scalar_obstruction = first_typed_owner = None
    for record in stratifier.remainder_records(owner_path, owner_manifest):
        source_index, global_kernel, order_kernel, raw_row, orbit_size = record
        expected_global, edges = kernels[order_kernel]
        require(global_kernel == expected_global, "remainder kernel changed")
        signed, paths, type_keys, type_ids = matrix_and_paths(edges, tuple(raw_row))
        numerical = numerical_scalar_costs(signed, paths, scalar_candidates)
        proposal_index = int(np.nanargmin(numerical))
        coefficient = scalar_candidates[proposal_index]
        cost = scalar_cost(signed, paths, coefficient)
        scalar_owner = cost is not None and cost <= BUDGET
        if scalar_owner:
            scalar_covered += 1
            scalar_owners[coefficient] += 1
            if first_scalar_owner is None:
                first_scalar_owner = [source_index, global_kernel, pair(coefficient), pair(cost)]
        elif first_scalar_obstruction is None:
            first_scalar_obstruction = [source_index, global_kernel, pair(coefficient),
                                        None if cost is None else pair(cost)]
        scalar_digest.update(canonical_bytes(
            [source_index, scalar_owner, pair(coefficient), None if cost is None else pair(cost)]))

        if scanned < representative_total:
            typed_cost_value, parameters = typed_search(
                signed, paths, type_ids, typed_candidates, typed_passes)
            typed_owner = typed_cost_value is not None and typed_cost_value <= BUDGET
            typed_covered += typed_owner
            typed_digest.update(canonical_bytes(
                [source_index, typed_owner,
                 [[pair(left), pair(right)] for left, right in parameters],
                 None if typed_cost_value is None else pair(typed_cost_value)]))
            representative = {
                "remainder_index": scanned, "source_index": source_index,
                "global_kernel": global_kernel, "scalar_owner": scalar_owner,
                "scalar_coefficient": pair(coefficient),
                "scalar_cost": None if cost is None else pair(cost),
                "typed_owner": typed_owner,
                "typed_cost": None if typed_cost_value is None else pair(typed_cost_value),
                "typed_parameters": [[pair(left), pair(right)]
                                     for left, right in parameters],
                "local_types": [[key[0], [list(value) for value in key[1]]]
                                for key in sorted(set(type_keys))],
            }
            representatives.append(representative)
            if typed_owner and first_typed_owner is None:
                first_typed_owner = representative
        scanned += 1
        if progress and scanned % 50000 == 0:
            print(f"rows={scanned} scalar_owned={scalar_covered}", flush=True)

    require(scanned == owner_manifest["remainder_orbit_total"], "incomplete remainder scan")
    return {
        "schema": SCHEMA,
        "full_theorem": scalar_covered == scanned,
        "scope": "exact accepted scalar SOS lane on full structural remainder; typed pilot only",
        "owner_manifest_sha256": owner_sha256,
        "remainder_stream_sha256": owner_manifest["remainder_stream_sha256"],
        "formula": {
            "scalar": "G=(I+tS)(I+tS)^T/M+diag(1-diag((I+tS)(I+tS)^T)/M)",
            "typed": "G=(I+DS)(I+DS)^T/M+diag(1-diag((I+DS)(I+DS)^T)/M)",
            "normalizer": "M=max_i (XX^T)_ii",
            "psd_proof": "XX^T/M plus a nonnegative diagonal sum of squares",
            "cost": "sum_p (1-(-1)^L G_uv)/(L(1+(-1)^L G_uv)) <= 6",
            "frontiers": "length plus two preserves parity and weakly decreases its summand",
        },
        "scalar_lane": {
            "status": "exact-theorem-owner" if scalar_covered else "tested-no-owner",
            "proposal_grid": {"maximum_denominator": max(x.denominator for x in scalar_candidates),
                              "range": [pair(scalar_candidates[0]), pair(scalar_candidates[-1])],
                              "distinct_total": len(scalar_candidates)},
            "scanned_remainder_total": scanned,
            "covered_remainder_total": scalar_covered,
            "uncovered_remainder_total": scanned - scalar_covered,
            "covered_target_total": scalar_covered * (PATH_COUNT + 1),
            "classification_stream_sha256": scalar_digest.hexdigest(),
            "used_coefficient_total": len(scalar_owners),
            "top_coefficients": [{"coefficient": pair(value), "owned_rows": count}
                                 for value, count in scalar_owners.most_common(20)],
            "first_owner": first_scalar_owner,
            "first_obstruction": first_scalar_obstruction,
            "audit": "binary64 selects one deterministic grid proposal; every classification is replayed exactly with Fraction",
        },
        "typed_pilot": {
            "status": "representative-pilot-not-full-coverage",
            "selection": "first rows of authenticated remainder stream",
            "representative_total": representative_total,
            "covered_representative_total": typed_covered,
            "proposal_grid": {"maximum_denominator": max(x.denominator for x in typed_candidates),
                              "range": [pair(typed_candidates[0]), pair(typed_candidates[-1])],
                              "distinct_total": len(typed_candidates),
                              "coordinate_passes": typed_passes},
            "classification_stream_sha256": typed_digest.hexdigest(),
            "first_owner": first_typed_owner,
            "records": representatives,
            "audit": "binary64 coordinate descent proposes typed ratios; every pilot result is replayed exactly with Fraction",
        },
        "claim_boundary": "only scalar covered rows are theorem-owned; no claim is made for scalar-uncovered rows or rows outside the typed pilot",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-manifest", type=Path, default=OWNER_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scalar-max-denominator", type=int, default=16)
    parser.add_argument("--scalar-maximum", type=int, default=4)
    parser.add_argument("--typed-max-denominator", type=int, default=4)
    parser.add_argument("--typed-maximum", type=int, default=2)
    parser.add_argument("--typed-representatives", type=int, default=100)
    parser.add_argument("--typed-passes", type=int, default=3)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(min(args.scalar_max_denominator, args.scalar_maximum,
                args.typed_max_denominator, args.typed_maximum,
                args.typed_representatives, args.typed_passes) > 0, "invalid search bounds")
    report = scan(args.owner_manifest,
                  rationals(args.scalar_max_denominator, args.scalar_maximum),
                  rationals(args.typed_max_denominator, args.typed_maximum),
                  args.typed_representatives, args.typed_passes, args.progress)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce byte-for-byte")
    else:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(f"scalar={report['scalar_lane']['covered_remainder_total']}/"
          f"{report['scalar_lane']['scanned_remainder_total']} "
          f"typed_pilot={report['typed_pilot']['covered_representative_total']}/"
          f"{report['typed_pilot']['representative_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
