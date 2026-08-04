#!/usr/bin/env python3
"""Experimental dimension-five rational Gram attack on the rank-six frontier."""

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CENSUS = HERE / "fixtures" / "rank-six-order-five-tetra-census.json"
CENSUS_SHA256 = "9656146c9dfefacc1c8df15fa9e7c8423f04b12c802c08af93f6e3f3e520bf22"
ENGINE_PATH = ROOT / "pentacyclic" / "research" / "order5-dim4-rational-gram-search.py"
OUTPUT = HERE / "fixtures" / "rank-six-order-five-dim5-rational-gram-results.json"
OUTPUT_SHA256 = "ae5f78b189a04e9a3e790188c5f4577a92c5dd19463267aceaec1a8f54bbd2c0"
PAIRS = tuple(itertools.combinations(range(5), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def load_engine():
    spec = importlib.util.spec_from_file_location("dim5_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load Gram engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.DIMENSION = 5
    module.BUDGET = module.Fraction(5)
    def random_vectors(generator):
        return ((1.0, 0.0, 0.0, 0.0, 0.0),) + tuple(
            module.normalized(tuple(generator.gauss(0.0, 1.0) for _ in range(5)))
            for _ in range(4))
    module.random_vectors = random_vectors
    return module


def load_census():
    raw = CENSUS.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CENSUS_SHA256, "census digest changed")
    value = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(value), "census is not canonical JSON")
    require(value["kernel_total"] == 84 and value["residual_total"] == 103,
            "census scope changed")
    return value


def canonical_lengths(multiplicity, odd):
    require(0 <= odd <= multiplicity, "invalid physical row")
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier=None):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 10, "rank-six path count changed")
    if frontier is not None:
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def run(args):
    engine = load_engine()
    census = load_census()
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    denominators = tuple(map(int, args.denominators.split(",")))
    records = []
    for target_index, (number, raw_row) in enumerate(census["residual_keys"]):
        row = tuple(raw_row)
        kernel = kernels[number]
        base_paths = path_ledger(kernel, row)
        base_value, base_vectors = engine.optimize(
            base_paths, args.seed + 1009 * target_index, args.restarts, args.iterations)
        for frontier in (None, *range(10)):
            paths = base_paths if frontier is None else path_ledger(kernel, row, frontier)
            if frontier is None:
                value, vectors = base_value, base_vectors
            else:
                value, vectors = engine.optimize(
                    paths, args.seed + 1009 * target_index + frontier + 1,
                    args.frontier_restarts, args.iterations, warm=(base_vectors,))
            exact, witness = engine.rationalize(paths, vectors, denominators)
            records.append({
                "kernel": number,
                "row": list(row),
                "frontier": frontier,
                "lengths": [path[4] for path in paths],
                "numerical_cost": float(f"{value:.12g}"),
                "exact_dnn_le_5": exact is not None,
                "witness": witness,
            })
        if args.progress:
            covered = sum(row["exact_dnn_le_5"] for row in records)
            print(f"[{target_index + 1}/103] K{number} covered={covered}/{len(records)}",
                  flush=True)
    residual = [row for row in records if not row["exact_dnn_le_5"]]
    structural = {}
    for row in residual:
        kernel = kernels[row["kernel"]]
        simple_support = [f"{u}{v}" for (u, v), multiplicity in zip(PAIRS, kernel)
                          if multiplicity == 1]
        doubled = [f"{u}{v}" for (u, v), multiplicity in zip(PAIRS, kernel)
                   if multiplicity > 1]
        key = f"simple={','.join(simple_support)};multiple={','.join(doubled)}"
        structural[key] = structural.get(key, 0) + 1
        row["structural_signature"] = key
    return {
        "schema": "rank-six-order-five-dim5-rational-gram-search-v1",
        "status": "experimental_exact_positive_certificates",
        "source_census_sha256": CENSUS_SHA256,
        "dimension": 5,
        "budget": [5, 1],
        "canonical_target_total": 103,
        "frontiers_per_target": 11,
        "target_total": len(records),
        "exact_dnn_le_5_total": sum(row["exact_dnn_le_5"] for row in records),
        "residual_total": len(residual),
        "structural_residual_signatures": structural,
        "full_theorem": False,
        "records": records,
    }


def audit_output():
    raw = OUTPUT.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == OUTPUT_SHA256, "result digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "result is not canonical JSON")
    require(payload["source_census_sha256"] == CENSUS_SHA256, "wrong census source")
    require(payload["target_total"] == 1133, "target total changed")
    require(payload["exact_dnn_le_5_total"] == 1120, "certificate total changed")
    require(payload["residual_total"] == 13, "residual total changed")
    require(payload["full_theorem"] is False, "experimental result promoted")
    keys = {(row["kernel"], tuple(row["row"]), row["frontier"])
            for row in payload["records"]}
    require(len(keys) == 1133, "target keys are not unique")
    require(sum(row["exact_dnn_le_5"] for row in payload["records"]) == 1120,
            "record partition changed")
    expected_signatures = {
        "simple=;multiple=03,04,12,14,23": 1,
        "simple=01,03,04,13,14,34;multiple=23,24": 1,
        "simple=01,02,03,04,12,13,14,23,24,34;multiple=": 11,
    }
    require(payload["structural_residual_signatures"] == expected_signatures,
            "structural residual signatures changed")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=619)
    parser.add_argument("--restarts", type=int, default=10)
    parser.add_argument("--frontier-restarts", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=1200)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.audit:
        payload = audit_output()
        print("rank-six order-five dimension-five rational Gram result: exact audit passed")
        print(f"targets={payload['target_total']} exact_dnn_le_5={payload['exact_dnn_le_5_total']} "
              f"residual={payload['residual_total']}")
        print(f"fixture_sha256={OUTPUT_SHA256}")
        return
    payload = run(args)
    require(args.output.parent.is_dir(), "output parent missing")
    args.output.write_bytes(canonical_bytes(payload))
    print("rank-six order-five dimension-five rational Gram search complete")
    print(f"targets={payload['target_total']} exact_dnn_le_5={payload['exact_dnn_le_5_total']} "
          f"residual={payload['residual_total']}")
    print(f"structural_signatures={len(payload['structural_residual_signatures'])}")


if __name__ == "__main__":
    main()
