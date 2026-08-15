#!/usr/bin/env python3
"""Exact typed-diagonal SOS Gram lane for rank-seven/order-eight residuals.

For exact local vertex types, search rational diagonal matrices D0 and D1 and
put X=D0+D1*S.  The correlation Gram is XX^T/M plus its nonnegative diagonal
completion, where M is the largest diagonal entry of XX^T.  Floating point
coordinate descent only proposes parameters; every accepted row is replayed
with Fraction arithmetic.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
DEFAULT_CACHE = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
DEFAULT_OUTPUT = HERE / "rank7_order8_typed_diagonal_gram_lane_coverage.json"
SCHEMA = "rank-seven-order-eight-typed-diagonal-gram-lane-v1"
ORDER = 8
F = Fraction
_WORKER_CONTEXT = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_typed_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load witness engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def pair(value):
    return [value.numerator, value.denominator]


def rationals(max_denominator, maximum, include_zero=False):
    values = {F(numerator, denominator)
              for denominator in range(1, max_denominator + 1)
              for numerator in range(0 if include_zero else 1, maximum * denominator + 1)}
    return tuple(sorted(values))


def signed_matrix(engine, census, source):
    matrix = [[0] * ORDER for _ in range(ORDER)]
    for dense, multiplicity, odd in zip(source[2], source[3], source[4], strict=True):
        u, v = census.PAIRS[dense]
        matrix[u][v] = matrix[v][u] = multiplicity - 2 * odd
    return matrix


def local_types(engine, census, source, signed):
    """Return canonical exact signed-degree/local-parity type IDs.

    The local parity profile records every incident bundle as (multiplicity,
    odd-count), with repetitions retained.  Its signed sum is stored explicitly
    so the key remains self-describing and easy to audit.
    """
    incident = [[] for _ in range(ORDER)]
    for dense, multiplicity, odd in zip(source[2], source[3], source[4], strict=True):
        u, v = census.PAIRS[dense]
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
    keys = tuple((sum(signed[u]), tuple(sorted(incident[u]))) for u in range(ORDER))
    dictionary = {key: index for index, key in enumerate(sorted(set(keys)))}
    return keys, np.asarray([dictionary[key] for key in keys], dtype=np.int64)


def row_data(engine, census, source):
    signed_exact = signed_matrix(engine, census, source)
    type_keys, type_ids = local_types(engine, census, source, signed_exact)
    paths = tuple(engine.base.path_ledger(census, source))
    endpoints = np.asarray([(path[2], path[3]) for path in paths], dtype=np.int64)
    lengths = np.asarray([path[4] for path in paths], dtype=np.int64)
    return (signed_exact, np.asarray(signed_exact, dtype=np.float64), type_keys,
            type_ids, paths, endpoints, lengths)


def numerical_costs(signed, type_ids, endpoints, lengths, diagonal0, diagonal1,
                    selected_type, candidates):
    count = len(candidates)
    d0 = np.broadcast_to(diagonal0, (count, ORDER)).copy()
    d1 = np.broadcast_to(diagonal1, (count, ORDER)).copy()
    mask = type_ids == selected_type
    d0[:, mask] = np.asarray([value[0] for value in candidates])[:, None]
    d1[:, mask] = np.asarray([value[1] for value in candidates])[:, None]
    x = np.eye(ORDER)[None, :, :] * d0[:, :, None] + d1[:, :, None] * signed[None, :, :]
    square = x @ np.swapaxes(x, 1, 2)
    normalizer = np.max(np.diagonal(square, axis1=1, axis2=2), axis=1)
    correlations = square[:, endpoints[:, 0], endpoints[:, 1]] / normalizer[:, None]
    correlations[:, (lengths & 1) == 1] *= -1
    with np.errstate(divide="ignore", invalid="ignore"):
        costs = np.sum((1.0 - correlations) /
                       (lengths[None, :] * (1.0 + correlations)), axis=1)
    costs[np.any(correlations <= -1.0, axis=1)] = np.inf
    return costs


def exact_cost(paths, signed, type_ids, parameters):
    d0 = [parameters[int(type_ids[u])][0] for u in range(ORDER)]
    d1 = [parameters[int(type_ids[u])][1] for u in range(ORDER)]
    x = [[(d0[u] if u == v else F()) + d1[u] * signed[u][v]
          for v in range(ORDER)] for u in range(ORDER)]
    square = [[sum(x[u][w] * x[v][w] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(square[u][u] for u in range(ORDER))
    require(normalizer > 0, "zero typed feature matrix")
    total = F()
    for _, _, u, v, length in paths:
        correlation = square[u][v] / normalizer
        transformed = -correlation if length & 1 else correlation
        require(-1 <= transformed <= 1, "PSD correlation escaped [-1,1]")
        if transformed == -1:
            return None, normalizer, square
        total += (1 - transformed) / (length * (1 + transformed))
    return total, normalizer, square


def search_row(engine, census, source, ratios, parameter_grid, passes):
    (signed_exact, signed, type_keys, type_ids, paths, endpoints,
     lengths) = row_data(engine, census, source)
    type_count = len(set(type_keys))
    all_one_type = np.zeros(ORDER, dtype=np.int64)
    ones = np.ones(ORDER, dtype=np.float64)
    zeros = np.zeros(ORDER, dtype=np.float64)
    scalar_candidates = tuple((1.0, float(value), F(1), value) for value in ratios)
    costs = numerical_costs(signed, all_one_type, endpoints, lengths, ones, zeros, 0,
                            scalar_candidates)
    best = int(np.argmin(costs))
    scalar_exact_cost = exact_scalar_cost(engine, census, source, scalar_candidates[best][3])
    diagonal0 = ones.copy()
    diagonal1 = np.full(ORDER, scalar_candidates[best][1], dtype=np.float64)
    exact_parameters = [(F(1), scalar_candidates[best][3]) for _ in range(type_count)]
    for _ in range(passes):
        changed = False
        for selected_type in range(type_count):
            proposals = numerical_costs(signed, type_ids, endpoints, lengths,
                                        diagonal0, diagonal1, selected_type, parameter_grid)
            best = int(np.argmin(proposals))
            value0, value1, exact0, exact1 = parameter_grid[best]
            if exact_parameters[selected_type] != (exact0, exact1):
                exact_parameters[selected_type] = exact0, exact1
                diagonal0[type_ids == selected_type] = value0
                diagonal1[type_ids == selected_type] = value1
                changed = True
        if not changed:
            break
    cost, normalizer, square = exact_cost(paths, signed_exact, type_ids, exact_parameters)
    return cost, scalar_exact_cost, normalizer, type_keys, type_ids, tuple(exact_parameters)


def worker_search(index):
    engine, census, residuals, ratios, parameter_grid, passes = _WORKER_CONTEXT
    return search_row(engine, census, residuals[index], ratios, parameter_grid, passes)


def scan(engine, census, residuals, ratios, scales, passes, workers=1, progress=False):
    global _WORKER_CONTEXT
    parameter_grid = tuple((float(scale), float(scale * ratio), scale, scale * ratio)
                           for scale in scales for ratio in ratios)
    covered = solved_covered = 0
    scalar_covered = 0
    type_counts = Counter()
    parameter_hits = Counter()
    classification = hashlib.sha256()
    first_new_owner = None
    hardest_obstruction = None
    _WORKER_CONTEXT = engine, census, residuals, ratios, parameter_grid, passes
    if workers == 1:
        results = map(worker_search, range(len(residuals)))
        executor = None
    else:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=workers)
        results = executor.map(worker_search, range(len(residuals)), chunksize=64)
    for index, (source, result) in enumerate(zip(residuals, results, strict=True)):
        cost, scalar_cost, normalizer, type_keys, type_ids, parameters = result
        scalar_covered += scalar_cost <= 6
        accepted = cost is not None and cost <= 6
        if accepted:
            covered += 1
            solved_covered += index < 5000
            parameter_hits.update(parameters)
            if scalar_cost > 6 and first_new_owner is None:
                first_new_owner = owner_record(index, source, cost, normalizer, type_keys,
                                               type_ids, parameters)
        elif hardest_obstruction is None or cost is None or cost > hardest_obstruction[0]:
            hardest_obstruction = (F(10**9) if cost is None else cost, index, source, cost,
                                   normalizer, type_keys, type_ids, parameters)
        type_counts[len(set(type_keys))] += 1
        classification.update(canonical_bytes([
            index, source[1], accepted, None if cost is None else pair(cost),
            [[pair(left), pair(right)] for left, right in parameters],
        ]))
        if progress and (index + 1) % 25000 == 0:
            print(f"rows={index + 1} covered={covered}", flush=True)
    if executor is not None:
        executor.shutdown()
    require(first_new_owner is not None and hardest_obstruction is not None, "empty scan")
    hard = hardest_obstruction
    hardest = owner_record(hard[1], hard[2], hard[3], hard[4], hard[5], hard[6], hard[7])
    return {
        "schema": SCHEMA,
        "full_theorem": covered == len(residuals),
        "scope": "authenticated rational-search complement of payload-free lanes",
        "source_stream_sha256": census.SOURCE_SHA256,
        "type_key": "(signed degree, sorted incident (multiplicity,odd-count) pairs)",
        "search": {
            "ratio_maximum_denominator": max(value.denominator for value in ratios),
            "ratio_range": [pair(ratios[0]), pair(ratios[-1])],
            "ratio_distinct_total": len(ratios),
            "d0_scales": [pair(value) for value in scales],
            "parameter_pair_total": len(parameter_grid),
            "coordinate_passes": passes,
            "initialization": "best scalar D0=I,D1=tI on the same ratio grid",
            "type_order": "lexicographic exact type key",
        },
        "formula": {
            "feature_matrix": "X=D0+D1*S with D0,D1 diagonal and constant on exact local types",
            "normalizer": "M=max_i (XX^T)_ii",
            "gram": "G=XX^T/M+diag(1-diag(XX^T)/M)",
            "psd_proof": "XX^T/M plus a nonnegative diagonal sum of squares",
            "cost_bound": "sum_p (1-(-1)^L G_uv)/(L(1+(-1)^L G_uv))",
            "frontiers": "length plus two weakly decreases each affected summand",
        },
        "scanned_residual_total": len(residuals),
        "covered_residual_total": covered,
        "uncovered_residual_total": len(residuals) - covered,
        "covered_target_total": covered * (engine.PATH_COUNT + 1),
        "uncovered_target_total": (len(residuals) - covered) * (engine.PATH_COUNT + 1),
        "scalar_grid_covered": scalar_covered,
        "gain_over_scalar_grid": covered - scalar_covered,
        "solved_first_5000_covered": solved_covered,
        "solved_first_5000_uncovered": 5000 - solved_covered,
        "local_type_count_histogram": {str(key): value for key, value in sorted(type_counts.items())},
        "used_parameter_pair_total": len(parameter_hits),
        "top_parameter_pairs": [
            {"d0_d1": [pair(left), pair(right)], "vertex_type_uses": count}
            for (left, right), count in parameter_hits.most_common(20)
        ],
        "first_new_owner_beyond_scalar": first_new_owner,
        "hardest_grid_obstruction": hardest,
        "classification_stream_sha256": classification.hexdigest(),
        "audit": "binary64 coordinate descent proposes parameters; every row cost is replayed with Fraction",
    }


def exact_scalar_cost(engine, census, source, coefficient):
    signed = signed_matrix(engine, census, source)
    square = [[sum(signed[u][w] * signed[w][v] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    normalizer = 1 + coefficient * coefficient * max(square[u][u] for u in range(ORDER))
    total = F()
    for _, _, u, v, length in engine.base.path_ledger(census, source):
        correlation = (2 * coefficient * signed[u][v] +
                       coefficient * coefficient * square[u][v]) / normalizer
        transformed = -correlation if length & 1 else correlation
        if transformed == -1:
            return F(10**9)
        total += (1 - transformed) / (length * (1 + transformed))
    return total


def owner_record(index, source, cost, normalizer, type_keys, type_ids, parameters):
    types = []
    for type_index, key in enumerate(sorted(set(type_keys))):
        signed_degree, profile = key
        d0, d1 = parameters[type_index]
        types.append({
            "signed_degree": signed_degree,
            "incident_parity_profile": [list(value) for value in profile],
            "vertices": [u for u in range(ORDER) if int(type_ids[u]) == type_index],
            "d0": pair(d0),
            "d1": pair(d1),
        })
    return {
        "stream_index": index,
        "source_index": source[1],
        "global_kernel": source[0],
        "support": list(source[2]),
        "multiplicities": list(source[3]),
        "odd_counts": list(source[4]),
        "cost": None if cost is None else pair(cost),
        "normalizer": pair(normalizer),
        "types": types,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census-cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-denominator", type=int, default=8)
    parser.add_argument("--maximum", type=int, default=4)
    parser.add_argument("--passes", type=int, default=3)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    require(args.max_denominator > 0 and args.maximum > 0 and args.passes > 0 and
            args.workers > 0,
            "bad finite search grid")
    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=args.census_cache)
    if args.limit is not None:
        require(5000 <= args.limit <= len(residuals), "limit must include the solved 5,000")
        residuals = residuals[:args.limit]
    ratios = rationals(args.max_denominator, args.maximum, include_zero=True)
    scales = (F(1, 2), F(2, 3), F(1), F(3, 2), F(2))
    report = scan(engine, census, residuals, ratios, scales, args.passes, args.workers,
                  args.progress)
    raw = canonical_bytes(report)
    if args.audit is not None:
        require(args.audit.read_bytes() == raw, "report does not reproduce byte-for-byte")
    else:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(f"covered={report['covered_residual_total']} total={report['scanned_residual_total']} "
          f"first5000={report['solved_first_5000_covered']} "
          f"gain={report['gain_over_scalar_grid']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"full_theorem={'true' if report['full_theorem'] else 'false'}")


if __name__ == "__main__":
    main()
