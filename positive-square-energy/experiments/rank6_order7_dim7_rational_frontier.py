#!/usr/bin/env python3
"""Chunkable rational DNN frontier attack for order-seven rank-six kernels.

Numerics only propose vectors. Every accepted record is reconstructed and
checked over Fraction before it is written. This remains an experiment until
the complete key universe and every finite residual have separate closure.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CENSUS = HERE / "rank6_order7_orbit_frontier_census.json"
ENGINE_PATH = ROOT / "pentacyclic" / "research" / "order7-dim7-rational-gram-experiment.py"
OUTPUT = HERE / "rank6_order7_dim7_rational_frontier.json"
EXPECTED_CENSUS_SHA256 = "2e38e09a1b7f800e0a17faa9a05c12adda2bfc45367aecd999b10e121b34bdb3"
ORDER = 7
DIMENSION = 7
PATH_COUNT = 12
BUDGET = Fraction(5)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def load_engine():
    spec = importlib.util.spec_from_file_location("rank6_order7_vector_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load vector engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BUDGET = BUDGET
    return module


def load_census():
    raw = CENSUS.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_CENSUS_SHA256,
            "order-seven census digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(payload["full_theorem"] is False and payload["kernel_total"] == 314,
            "census scope changed")
    require(payload["coarse_residual_total"] == 24554 and
            payload["frontier_target_total"] == 319202, "census totals changed")
    return payload


def parse_frontiers(text):
    if text == "all":
        return (None, *range(PATH_COUNT))
    result = tuple(None if value == "canonical" else int(value) for value in text.split(","))
    require(result and len(set(result)) == len(result)
            and all(value is None or 0 <= value < PATH_COUNT for value in result),
            "frontiers must be distinct canonical or coordinates 0..11")
    return result


def exact_record(engine, kernel, source, source_index, frontier, vectors, value, denominators):
    paths = engine.path_ledger(kernel, tuple(source["row"]), frontier)
    witness = engine.rationalize(paths, vectors, denominators)
    return {
        "source_index": source_index,
        "kernel": source["kernel"],
        "row": source["row"],
        "frontier": frontier,
        "lengths": [path[4] for path in paths],
        "numerical_cost": float(f"{value:.12g}"),
        "exact_dnn_le_5": witness is not None,
        "witness": witness,
    }


def run(args):
    census = load_census()
    engine = load_engine()
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    residuals = census["residuals"]
    stop = len(residuals) if args.limit is None else min(len(residuals), args.start + args.limit)
    selected = residuals[args.start:stop]
    frontiers = parse_frontiers(args.frontiers)
    denominators = tuple(int(value) for value in args.denominators.split(","))
    require(denominators and all(value > 0 for value in denominators), "bad denominators")
    records = []
    for local_index, source in enumerate(selected):
        source_index = args.start + local_index
        kernel = kernels[source["kernel"]]
        canonical_paths = engine.path_ledger(kernel, tuple(source["row"]))
        canonical_value, canonical_vectors = engine.optimize(
            canonical_paths, args.seed + 1009 * source_index, args.restarts, args.iterations)
        for frontier in frontiers:
            if frontier is None:
                value, vectors = canonical_value, canonical_vectors
            else:
                paths = engine.path_ledger(kernel, tuple(source["row"]), frontier)
                value, vectors = engine.optimize(
                    paths, args.seed + 1009 * source_index + frontier + 1,
                    args.frontier_restarts, args.iterations, warm=(canonical_vectors,))
            records.append(exact_record(engine, kernel, source, source_index, frontier,
                                        vectors, value, denominators))
        if args.progress:
            exact = sum(row["exact_dnn_le_5"] for row in records)
            print(f"[{local_index + 1}/{len(selected)}] K{source['kernel']} "
                  f"exact={exact}/{len(records)}", flush=True)
    return {
        "schema": "rank-six-order-seven-dim7-rational-frontier-experiment-v1",
        "status": "experimental_partial_exact_certificates",
        "full_theorem": False,
        "dimension": DIMENSION,
        "budget": [5, 1],
        "source_census_sha256": EXPECTED_CENSUS_SHA256,
        "source_residual_total": census["coarse_residual_total"],
        "source_frontier_total": census["frontier_target_total"],
        "selected_residual_start": args.start,
        "selected_residual_total": len(selected),
        "selected_frontiers": list(frontiers),
        "target_total": len(records),
        "exact_certificate_total": sum(row["exact_dnn_le_5"] for row in records),
        "finite_unresolved_total": sum(not row["exact_dnn_le_5"] for row in records),
        "complete_source_cover": (args.start == 0 and len(selected) == len(residuals)
                                  and frontiers == (None, *range(PATH_COUNT))),
        "records": records,
    }


def fraction(raw, label):
    require(isinstance(raw, list) and len(raw) == 2
            and all(isinstance(value, int) and not isinstance(value, bool) for value in raw),
            f"bad {label} fraction")
    value = Fraction(*raw)
    require(raw == [value.numerator, value.denominator], f"uncanonical {label} fraction")
    return value


def verify(payload):
    census = load_census()
    engine = load_engine()
    require(payload["schema"] == "rank-six-order-seven-dim7-rational-frontier-experiment-v1",
            "schema changed")
    require(payload["full_theorem"] is False, "experiment was theorem-promoted")
    require(payload["source_census_sha256"] == EXPECTED_CENSUS_SHA256, "wrong census")
    require(payload["exact_certificate_total"] + payload["finite_unresolved_total"]
            == payload["target_total"] == len(payload["records"]), "partition changed")
    residuals = census["residuals"]
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    keys = set()
    for record in payload["records"]:
        key = (record["source_index"], record["frontier"])
        require(key not in keys, "duplicate target key")
        keys.add(key)
        require(0 <= record["source_index"] < len(residuals), "source index out of range")
        source = residuals[record["source_index"]]
        require((record["kernel"], record["row"]) == (source["kernel"], source["row"]),
                "source key changed")
        paths = engine.path_ledger(kernels[record["kernel"]], tuple(record["row"]),
                                   record["frontier"])
        require(record["lengths"] == [path[4] for path in paths], "path lengths changed")
        witness = record["witness"]
        require(record["exact_dnn_le_5"] == (witness is not None), "witness status changed")
        if witness is None:
            continue
        parameters = tuple(tuple(fraction(value, "branch") for value in row)
                           for row in witness["branches"])
        branches = tuple(engine.rational_unit(row) for row in parameters)
        require(len(branches) == ORDER and all(len(row) == DIMENSION for row in branches),
                "branch dimensions changed")
        require(len(witness["internals"]) == PATH_COUNT, "internal ledger changed")
        total = Fraction(0)
        for (_, _, u, v, length), raw_path in zip(paths, witness["internals"]):
            require(len(raw_path) == length - 1, "internal path width changed")
            internal = tuple(tuple(fraction(value, "internal") for value in row)
                             for row in raw_path)
            require(all(len(row) == DIMENSION - 1 for row in internal),
                    "internal stereographic dimension changed")
            chain = [branches[u], *(engine.rational_unit(row) for row in internal)]
            chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
            total += sum((engine.exact_step_cost(left, right)
                          for left, right in zip(chain, chain[1:])), Fraction(0))
        require(total == fraction(witness["cost"], "cost") and total <= BUDGET,
                "exact witness cost changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=67173)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--frontiers", default="all")
    parser.add_argument("--restarts", type=int, default=3)
    parser.add_argument("--frontier-restarts", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=600)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify is None:
        require(args.start >= 0 and (args.limit is None or args.limit >= 0), "bad source range")
        payload = run(args)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        args.output.write_bytes(canonical_bytes(payload))
    else:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), "result JSON is not canonical")
        verify(payload)
    print(f"targets={payload['target_total']} exact={payload['exact_certificate_total']} "
          f"finite_unresolved={payload['finite_unresolved_total']}")
    print(f"complete_source_cover={str(payload['complete_source_cover']).lower()} "
          "full_theorem=false")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
