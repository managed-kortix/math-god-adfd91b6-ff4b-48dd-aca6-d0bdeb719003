#!/usr/bin/env python3
"""Generate exact rational candidates for the rank-seven order-five frontier."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COARSE_PATH = ROOT / "positive-square-energy" / "experiments" / "rank7_parity_coarse_digest_census.py"
ENGINE_PATH = ROOT / "pentacyclic" / "research" / "order5-dim4-rational-gram-search.py"
OUTPUT = ROOT / "research" / "fixtures" / "rank-seven-order-five-rational-gram-results.json"
SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def residual_rows(coarse):
    coarse.SOURCE_SHA256 = SOURCE_SHA256
    result = []
    for item in coarse.source_kernels():
        global_index, local_index, n, edges = item
        if n != 5:
            continue
        actions = coarse.automorphism_actions(n, edges)
        seen = set()
        for row in itertools.product(*(range(multiplicity + 1) for _, _, multiplicity in edges)):
            representative = min(coarse.apply_action(row, action) for action in actions)
            if representative in seen:
                continue
            seen.add(representative)
            if coarse.is_coarse_residual(n, edges, representative):
                result.append((global_index, local_index, edges, representative))
    require(len(result) == 15, "order-five residual count changed")
    return tuple(result)


def canonical_lengths(multiplicity, odd):
    require(type(multiplicity) is int and type(odd) is int and 0 <= odd <= multiplicity,
            "invalid parity row")
    return ((1,) + (3,) * (odd - 1) if odd else ()) + (2,) * (multiplicity - odd)


def path_ledger(edges, row, coordinate=None):
    paths = []
    for edge, ((u, v, multiplicity), odd) in enumerate(zip(edges, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 11, "rank-seven order-five path count changed")
    if coordinate is not None:
        require(type(coordinate) is int and 0 <= coordinate < 11, "invalid coordinate")
        edge, occurrence, u, v, length = paths[coordinate]
        paths[coordinate] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def generate(args):
    coarse = load_module("rank7_coarse", COARSE_PATH)
    engine = load_module("rank7_engine", ENGINE_PATH)
    engine.DIMENSION = 5
    engine.BUDGET = engine.Fraction(6)

    def random_vectors(generator):
        return ((1.0, 0.0, 0.0, 0.0, 0.0),) + tuple(
            engine.normalized(tuple(generator.gauss(0.0, 1.0) for _ in range(5)))
            for _ in range(4))

    engine.random_vectors = random_vectors
    denominators = tuple(map(int, args.denominators.split(",")))
    records = []
    rows = residual_rows(coarse)
    for row_index, (kernel, local, edges, parity) in enumerate(rows):
        canonical = path_ledger(edges, parity)
        base_value, base_vectors = engine.optimize(
            canonical, args.seed + 1009 * row_index, args.restarts, args.iterations)
        for coordinate in (None, *range(11)):
            paths = canonical if coordinate is None else path_ledger(edges, parity, coordinate)
            if coordinate is None:
                value, vectors = base_value, base_vectors
            else:
                value, vectors = engine.optimize(
                    paths, args.seed + 1009 * row_index + coordinate + 1,
                    args.frontier_restarts, args.iterations, warm=(base_vectors,))
            exact, witness = engine.rationalize(paths, vectors, denominators)
            records.append({
                "kernel": kernel,
                "order_kernel": local,
                "row": list(parity),
                "coordinate": coordinate,
                "lengths": [path[4] for path in paths],
                "numerical_cost": float(f"{value:.12g}"),
                "exact_dnn_le_6": exact is not None,
                "witness": witness,
            })
        if args.progress:
            print(f"[{row_index + 1}/15] K{kernel} exact="
                  f"{sum(record['exact_dnn_le_6'] for record in records)}/{len(records)}",
                  flush=True)
    return {
        "schema": "rank-seven-order-five-rational-gram-search-v1",
        "status": "candidate-exact-rational-certificates-not-a-theorem",
        "source_sha256": SOURCE_SHA256,
        "budget": [6, 1],
        "residual_orbits": 15,
        "frontiers_per_orbit": 12,
        "target_total": 180,
        "exact_dnn_le_6_total": sum(record["exact_dnn_le_6"] for record in records),
        "full_theorem": False,
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=719)
    parser.add_argument("--restarts", type=int, default=16)
    parser.add_argument("--frontier-restarts", type=int, default=3)
    parser.add_argument("--iterations", type=int, default=1600)
    parser.add_argument("--denominators", default="64,256,1024,4096,16384")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    payload = generate(args)
    require(args.output.parent.is_dir(), "output parent missing")
    args.output.write_bytes(canonical_bytes(payload))
    print(f"targets=180 exact={payload['exact_dnn_le_6_total']} residual="
          f"{180 - payload['exact_dnn_le_6_total']}")


if __name__ == "__main__":
    main()
