#!/usr/bin/env python3
"""Audit a rational PSD polynomial-Gram lane on the order-eight residuals.

For the signed bundle matrix S and rational t >= 0, put

    H(t) = (I + t S)^2,
    M(t) = max_i H(t)_ii = 1 + t^2 max_i (S^2)_ii,
    G(t) = H(t)/M(t) + diag(1 - H(t)_ii/M(t)).

Thus G(t) is a rational correlation Gram.  Its PSD proof is the displayed
square plus a nonnegative diagonal sum of squares.  The scan uses binary64
only to propose a coefficient; every accepted row is replayed with Fraction.
"""

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
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
DEFAULT_CACHE = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
DEFAULT_OUTPUT = HERE / "rank7_order8_parametric_gram_ansatz_coverage.json"
SCHEMA = "rank-seven-order-eight-parametric-gram-ansatz-v1"
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_parametric_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load witness engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def pair(value):
    return [value.numerator, value.denominator]


def coefficients(max_denominator, maximum):
    values = {F(numerator, denominator)
              for denominator in range(1, max_denominator + 1)
              for numerator in range(1, maximum * denominator + 1)}
    return tuple(sorted(values))


def signed_matrix(engine, census, source):
    matrix = [[0] * engine.ORDER for _ in range(engine.ORDER)]
    for dense, multiplicity, odd in zip(source[2], source[3], source[4], strict=True):
        u, v = census.PAIRS[dense]
        matrix[u][v] = matrix[v][u] = multiplicity - 2 * odd
    return matrix


def exact_cost(engine, census, source, coefficient):
    signed = signed_matrix(engine, census, source)
    square = [[sum(signed[u][w] * signed[w][v] for w in range(engine.ORDER))
               for v in range(engine.ORDER)] for u in range(engine.ORDER)]
    maximum = 1 + coefficient * coefficient * max(square[i][i]
                                                    for i in range(engine.ORDER))
    total = F()
    for _, _, u, v, length in engine.base.path_ledger(census, source):
        correlation = (2 * coefficient * signed[u][v]
                       + coefficient * coefficient * square[u][v]) / maximum
        transformed = -correlation if length & 1 else correlation
        require(-1 < transformed <= 1, "PSD correlation escaped [-1,1]")
        total += (1 - transformed) / (length * (1 + transformed))
    return total


def numerical_costs(engine, census, source, values):
    signed = np.zeros((engine.ORDER, engine.ORDER), dtype=np.float64)
    for dense, multiplicity, odd in zip(source[2], source[3], source[4], strict=True):
        u, v = census.PAIRS[dense]
        signed[u, v] = signed[v, u] = multiplicity - 2 * odd
    square = signed @ signed
    denominator = 1.0 + values * values * np.max(np.diag(square))
    costs = np.zeros(len(values), dtype=np.float64)
    for _, _, u, v, length in engine.base.path_ledger(census, source):
        correlation = (2.0 * values * signed[u, v]
                       + values * values * square[u, v]) / denominator
        transformed = -correlation if length & 1 else correlation
        with np.errstate(divide="ignore", invalid="ignore"):
            costs += (1.0 - transformed) / (length * (1.0 + transformed))
    return costs


def scan(engine, census, residuals, candidates, progress=False):
    values = np.asarray([float(value) for value in candidates])
    coefficient_hits = Counter()
    covered = source_covered = 0
    classification = hashlib.sha256()
    hardest = None
    first_obstruction = None
    for index, source in enumerate(residuals):
        costs = numerical_costs(engine, census, source, values)
        order = np.argsort(costs)
        owner = None
        owner_cost = None
        for position in order:
            if costs[position] > 6.0 + 1e-10:
                break
            proposed = candidates[int(position)]
            replay = exact_cost(engine, census, source, proposed)
            if replay <= 6:
                owner, owner_cost = proposed, replay
                break
        best_position = int(order[0])
        best_proposal = candidates[best_position]
        best_exact = exact_cost(engine, census, source, best_proposal)
        if hardest is None or best_exact > hardest[0]:
            hardest = best_exact, index, source, best_proposal
        if owner is None and first_obstruction is None:
            first_obstruction = index, source, best_proposal, best_exact
        if owner is not None:
            covered += 1
            source_covered += index < 5000
            coefficient_hits[owner] += 1
        classification.update(canonical_bytes([
            index, source[1], None if owner is None else pair(owner),
            None if owner_cost is None else pair(owner_cost),
        ]))
        if progress and (index + 1) % 25000 == 0:
            print(f"rows={index + 1} covered={covered}", flush=True)
    require(hardest is not None and first_obstruction is not None, "empty scan")

    def obstruction(record):
        index, source, coefficient, cost = record
        return {
            "stream_index": index,
            "source_index": source[1],
            "global_kernel": source[0],
            "support": list(source[2]),
            "multiplicities": list(source[3]),
            "odd_counts": list(source[4]),
            "best_grid_coefficient": pair(coefficient),
            "best_grid_cost": pair(cost),
        }

    hardest_record = (hardest[1], hardest[2], hardest[3], hardest[0])
    return {
        "schema": SCHEMA,
        "full_theorem": covered == len(residuals),
        "scope": "authenticated rational-search complement of payload-free lanes",
        "source_stream_sha256": census.SOURCE_SHA256,
        "coefficient_grid": {
            "maximum_denominator": max(value.denominator for value in candidates),
            "range": [pair(candidates[0]), pair(candidates[-1])],
            "distinct_total": len(candidates),
        },
        "formula": {
            "signed_matrix": "S_uv=m_uv-2r_uv, S_uu=0",
            "gram": "G=(I+tS)^2/M+diag(1-diag((I+tS)^2)/M)",
            "normalizer": "M=1+t^2 max_i (S^2)_ii",
            "psd_proof": "(I+tS)^2/M plus a nonnegative diagonal sum of squares",
            "cost_bound": "sum_p (1-(-1)^L G_uv)/(L(1+(-1)^L G_uv))",
            "frontiers": "length plus two weakly decreases each affected summand",
        },
        "scanned_residual_total": len(residuals),
        "covered_residual_total": covered,
        "uncovered_residual_total": len(residuals) - covered,
        "covered_target_total": covered * (engine.PATH_COUNT + 1),
        "uncovered_target_total": (len(residuals) - covered) * (engine.PATH_COUNT + 1),
        "solved_first_5000_covered": source_covered,
        "solved_first_5000_uncovered": 5000 - source_covered,
        "used_coefficient_total": len(coefficient_hits),
        "top_coefficients": [
            {"coefficient": pair(value), "exclusive_rows": count}
            for value, count in coefficient_hits.most_common(20)
        ],
        "first_grid_obstruction": obstruction(first_obstruction),
        "hardest_grid_obstruction": obstruction(hardest_record),
        "classification_stream_sha256": classification.hexdigest(),
        "audit": "binary64 proposes coefficients; every accepted cost is replayed with Fraction",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census-cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-denominator", type=int, default=32)
    parser.add_argument("--maximum", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    require(args.max_denominator > 0 and args.maximum > 0, "bad coefficient grid")
    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=args.census_cache)
    if args.limit is not None:
        require(5000 <= args.limit <= len(residuals), "limit must include the solved 5,000")
        residuals = residuals[:args.limit]
    candidates = coefficients(args.max_denominator, args.maximum)
    report = scan(engine, census, residuals, candidates, args.progress)
    raw = canonical_bytes(report)
    if args.audit is not None:
        require(args.audit.read_bytes() == raw, "report does not reproduce byte-for-byte")
    else:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(f"covered={report['covered_residual_total']} total={report['scanned_residual_total']} "
          f"first5000={report['solved_first_5000_covered']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"full_theorem={'true' if report['full_theorem'] else 'false'}")


if __name__ == "__main__":
    main()
