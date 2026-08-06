#!/usr/bin/env python3
"""Chunkable batched rational search over the order-eight frontier census.

Numerical optimization only proposes vectors.  Every non-null witness is
reconstructed with Fraction before output.  Partial chunks and unresolved
targets are explicit; this experiment cannot claim a theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import multiprocessing
import os
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CENSUS = HERE / "rank6_order8_orbit_frontier_census.json"
VECTOR_ENGINE = HERE.parents[1] / "pentacyclic" / "research" / "order7-dim7-rational-gram-experiment.py"
OUTPUT_DIR = HERE / "rank6_order8_batched_chunks"
CENSUS_SHA256 = "724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e"
SCHEMA = "rank-six-order-eight-batched-exact-gram-experiment-v1"
ORDER = 8
DIMENSION = 8
PATH_COUNT = 13
FRONTIERS = (None, *range(PATH_COUNT))
BUDGET = Fraction(5)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
TETRA_VECTORS = (
    (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    (-1 / 3, 2 * math.sqrt(2) / 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    (-1 / 3, -math.sqrt(2) / 3, math.sqrt(2 / 3), 0.0, 0.0, 0.0, 0.0, 0.0),
    (-1 / 3, -math.sqrt(2) / 3, -math.sqrt(2 / 3), 0.0, 0.0, 0.0, 0.0, 0.0),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_json(raw):
    return json.loads(raw.decode("ascii"), parse_constant=reject_constant)


def load_census():
    raw = CENSUS.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CENSUS_SHA256, "order-eight census changed")
    payload = load_json(raw)
    require(raw == canonical_bytes(payload), "census is not canonical JSON")
    require(payload["full_theorem"] is False and payload["kernel_total"] == 325 and
            payload["tetrahedral_residual_total"] == 102988 and
            payload["frontier_target_total"] == 1441832, "census scope changed")
    return payload


def load_engine():
    spec = importlib.util.spec_from_file_location("rank6_order8_vector_engine", VECTOR_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load vector engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.DIMENSION = DIMENSION
    module.BUDGET = BUDGET
    module.PAIRS = PAIRS
    return module


def color_patterns(prefix=(0,)):
    if len(prefix) == ORDER:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from color_patterns(prefix + (color,))


COLORINGS = tuple(color_patterns())


def tetra_cost(kernel, row, coloring):
    total = 0
    for (u, v), multiplicity, odd in zip(PAIRS, kernel, row):
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        if odd:
            total += 10 + 5 * odd
        total += 18 * (multiplicity - odd)
    return total


def tetrahedral_start(kernel, row):
    coloring = min((value for value in COLORINGS if tetra_cost(kernel, row, value) is not None),
                   key=lambda value: tetra_cost(kernel, row, value))
    vectors = []
    for vertex, color in enumerate(coloring):
        vector = list(TETRA_VECTORS[color])
        vector[vertex] += 0.08
        norm = math.sqrt(sum(value * value for value in vector))
        vectors.append(tuple(value / norm for value in vector))
    return tuple(vectors)


def pair(value):
    return [value.numerator, value.denominator]


def exact_path(engine, left, right, exact_left, exact_right, length, denominator):
    parameters = tuple(engine.stereographic(engine.slerp(left, right, step / length), denominator)
                       for step in range(1, length))
    chain = [exact_left, *(engine.rational_unit(row) for row in parameters), exact_right]
    cost = sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    return parameters, cost


def shared_rationalize(engine, paths, vectors, denominators):
    vectors = engine.rotate_away_from_pole(engine.snap_coincident(vectors))
    for denominator in denominators:
        try:
            parameters = tuple(engine.stereographic(row, denominator) for row in vectors)
            branches = tuple(engine.rational_unit(row) for row in parameters)
            canonical, extended, base_costs, extended_costs = [], [], [], []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                inside, cost = exact_path(engine, vectors[u], endpoint, branches[u],
                                          exact_endpoint, length, denominator)
                longer, longer_cost = exact_path(engine, vectors[u], endpoint, branches[u],
                                                  exact_endpoint, length + 2, denominator)
                canonical.append(inside)
                extended.append(longer)
                base_costs.append(cost)
                extended_costs.append(longer_cost)
        except (RuntimeError, ZeroDivisionError):
            continue
        base = sum(base_costs, Fraction())
        costs = [base] + [base - base_costs[i] + extended_costs[i] for i in range(PATH_COUNT)]
        if all(cost <= BUDGET for cost in costs):
            return {
                "denominator": denominator,
                "costs": [pair(cost) for cost in costs],
                "branches": [[pair(value) for value in row] for row in parameters],
                "canonical_internals": [[[pair(value) for value in row] for row in path]
                                        for path in canonical],
                "extended_internals": [[[pair(value) for value in row] for row in path]
                                       for path in extended],
            }
    return None


WORKER = {}


def initialize_worker(denominators, seed, restarts, iterations, fallback_restarts,
                      fallback_iterations):
    census = load_census()
    WORKER.clear()
    WORKER.update({
        "engine": load_engine(),
        "residuals": census["residuals"],
        "kernels": {row["kernel"]: tuple(row["code"]) for row in census["kernels"]},
        "denominators": denominators,
        "seed": seed,
        "restarts": restarts,
        "iterations": iterations,
        "fallback_restarts": fallback_restarts,
        "fallback_iterations": fallback_iterations,
    })


def generate_record(source_index):
    engine = WORKER["engine"]
    source = WORKER["residuals"][source_index]
    kernel = WORKER["kernels"][source["kernel"]]
    row = tuple(source["row"])
    paths = engine.path_ledger(kernel, row)
    value, vectors = engine.optimize(paths, WORKER["seed"] + 1009 * source_index,
                                     WORKER["restarts"], WORKER["iterations"],
                                     warm=(tetrahedral_start(kernel, row),))
    numerical = [value] + [engine.objective(engine.path_ledger(kernel, row, frontier), vectors)
                           for frontier in range(PATH_COUNT)]
    shared = shared_rationalize(engine, paths, vectors, WORKER["denominators"])
    individual = [None] * len(FRONTIERS)
    if shared is None:
        for position, frontier in enumerate(FRONTIERS):
            target = paths if frontier is None else engine.path_ledger(kernel, row, frontier)
            candidate_value, candidate = numerical[position], vectors
            witness = engine.rationalize(target, candidate, WORKER["denominators"])
            if witness is None and WORKER["fallback_restarts"]:
                candidate_value, candidate = engine.optimize(
                    target, WORKER["seed"] + 1009 * source_index + position,
                    WORKER["fallback_restarts"], WORKER["fallback_iterations"], warm=(vectors,))
                witness = engine.rationalize(target, candidate, WORKER["denominators"])
            numerical[position] = candidate_value
            individual[position] = witness
    return {
        "source_index": source_index,
        "kernel": source["kernel"],
        "row": source["row"],
        "canonical_lengths": [path[4] for path in paths],
        "numerical_costs": [float(f"{item:.12g}") for item in numerical],
        "shared_witness": shared,
        "individual_witnesses": individual if shared is None else None,
        "exact_target_total": len(FRONTIERS) if shared is not None
                              else sum(item is not None for item in individual),
    }


def fraction(raw, label):
    require(type(raw) is list and len(raw) == 2 and all(type(value) is int for value in raw),
            f"bad {label} fraction")
    value = Fraction(*raw)
    require(raw == pair(value), f"uncanonical {label} fraction")
    return value


def audit_witness(engine, paths, witness, frontier):
    require(type(witness) is dict, "bad witness envelope")
    shared = "canonical_internals" in witness
    expected = ({"denominator", "costs", "branches", "canonical_internals",
                 "extended_internals"} if shared else
                {"denominator", "cost", "branches", "internals"})
    require(set(witness) == expected, "witness envelope changed")
    denominator = witness["denominator"]
    require(type(denominator) is int and denominator > 0, "bad witness denominator")

    def parameter(raw, label):
        value = fraction(raw, label)
        require(denominator % value.denominator == 0, f"unauthenticated {label} denominator")
        return value

    branches = tuple(engine.rational_unit(tuple(parameter(x, "branch") for x in row))
                     for row in witness["branches"])
    require(len(branches) == ORDER and all(len(row) == DIMENSION for row in branches),
            "branch dimensions changed")
    if shared:
        raw_paths = list(witness["canonical_internals"])
        if frontier is not None:
            raw_paths[frontier] = witness["extended_internals"][frontier]
        claimed = witness["costs"][0 if frontier is None else frontier + 1]
    else:
        raw_paths, claimed = witness["internals"], witness["cost"]
    require(len(raw_paths) == PATH_COUNT, "internal path count changed")
    total = Fraction()
    for (_, _, u, v, length), raw_path in zip(paths, raw_paths):
        require(len(raw_path) == length - 1, "internal path width changed")
        parameters = tuple(tuple(parameter(x, "internal") for x in row) for row in raw_path)
        require(all(len(row) == DIMENSION - 1 for row in parameters), "internal dimension changed")
        chain = [branches[u], *(engine.rational_unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    require(total == fraction(claimed, "cost") and total <= BUDGET, "exact cost changed")


def verify(payload):
    census = load_census()
    engine = load_engine()
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False, "schema changed")
    require(payload["source_census_sha256"] == CENSUS_SHA256, "wrong census")
    require(payload["source_residual_total"] == len(census["residuals"]) and
            payload["source_frontier_total"] == census["frontier_target_total"],
            "source totals changed")
    require(payload["record_total"] == len(payload["records"]) and
            payload["target_total"] == len(FRONTIERS) * len(payload["records"]),
            "chunk totals changed")
    start, seen, exact = payload["selected_residual_start"], set(), 0
    require(type(start) is int and 0 <= start <= len(census["residuals"]), "bad chunk start")
    for record in payload["records"]:
        index = record["source_index"]
        require(type(index) is int and index not in seen and 0 <= index < len(census["residuals"]),
                "duplicate or invalid source index")
        seen.add(index)
        source = census["residuals"][index]
        require((record["kernel"], record["row"]) == (source["kernel"], source["row"]),
                "source key changed")
        canonical = engine.path_ledger(kernels[record["kernel"]], tuple(record["row"]))
        require(record["canonical_lengths"] == [path[4] for path in canonical], "lengths changed")
        require(len(record["numerical_costs"]) == len(FRONTIERS) and
                all(type(value) in (int, float) and math.isfinite(value)
                    for value in record["numerical_costs"]), "bad numerical costs")
        if record["shared_witness"] is not None:
            require(record["individual_witnesses"] is None, "mixed witness modes")
            for frontier in FRONTIERS:
                paths = canonical if frontier is None else engine.path_ledger(
                    kernels[record["kernel"]], tuple(record["row"]), frontier)
                audit_witness(engine, paths, record["shared_witness"], frontier)
            local = len(FRONTIERS)
        else:
            require(type(record["individual_witnesses"]) is list and
                    len(record["individual_witnesses"]) == len(FRONTIERS), "fallback width changed")
            local = 0
            for frontier, witness in zip(FRONTIERS, record["individual_witnesses"]):
                if witness is not None:
                    paths = canonical if frontier is None else engine.path_ledger(
                        kernels[record["kernel"]], tuple(record["row"]), frontier)
                    audit_witness(engine, paths, witness, frontier)
                    local += 1
        require(record["exact_target_total"] == local, "exact subtotal changed")
        exact += local
    require(seen == set(range(start, start + len(payload["records"]))), "noncontiguous chunk")
    require(payload["exact_target_total"] == exact and
            payload["unresolved_target_total"] == payload["target_total"] - exact,
            "exact partition changed")
    complete = (start == 0 and len(seen) == len(census["residuals"]))
    require(payload["complete_source_cover"] is complete, "completeness flag changed")


def run(args):
    census = load_census()
    stop = min(len(census["residuals"]), args.start + args.count)
    indices = range(args.start, stop)
    denominators = tuple(int(value) for value in args.denominators.split(","))
    require(denominators and all(value > 0 for value in denominators), "bad denominators")
    initargs = (denominators, args.seed, args.restarts, args.iterations,
                args.fallback_restarts, args.fallback_iterations)
    started = time.perf_counter()
    if args.workers == 1:
        initialize_worker(*initargs)
        records = [generate_record(index) for index in indices]
    else:
        with multiprocessing.get_context("fork").Pool(args.workers, initialize_worker, initargs) as pool:
            records = list(pool.imap(generate_record, indices, chunksize=args.worker_batch))
    exact = sum(record["exact_target_total"] for record in records)
    target_total = len(FRONTIERS) * len(records)
    return {
        "schema": SCHEMA,
        "status": "exact_chunk" if exact == target_total else "finite_residual_chunk",
        "full_theorem": False,
        "source_census_sha256": CENSUS_SHA256,
        "source_residual_total": len(census["residuals"]),
        "source_frontier_total": census["frontier_target_total"],
        "selected_residual_start": args.start,
        "record_total": len(records),
        "target_total": target_total,
        "exact_target_total": exact,
        "unresolved_target_total": target_total - exact,
        "complete_source_cover": args.start == 0 and len(records) == len(census["residuals"]),
        "elapsed_seconds": float(f"{time.perf_counter() - started:.6f}"),
        "workers": args.workers,
        "search": {"restarts": args.restarts, "iterations": args.iterations,
                   "fallback_restarts": args.fallback_restarts,
                   "fallback_iterations": args.fallback_iterations,
                   "denominators": list(denominators)},
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=min(16, os.cpu_count() or 1))
    parser.add_argument("--worker-batch", type=int, default=8)
    parser.add_argument("--seed", type=int, default=68183)
    parser.add_argument("--restarts", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=180)
    parser.add_argument("--fallback-restarts", type=int, default=1)
    parser.add_argument("--fallback-iterations", type=int, default=300)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify is not None:
        raw = args.verify.read_bytes()
        payload = load_json(raw)
        require(raw == canonical_bytes(payload), "chunk is not canonical JSON")
    else:
        require(args.start >= 0 and args.count >= 0 and args.workers >= 1 and
                args.worker_batch >= 1, "bad range or workers")
        payload = run(args)
        raw = canonical_bytes(payload)
        output = args.output or OUTPUT_DIR / f"chunk-{args.start:06d}-{args.start + args.count:06d}.json"
        require(output.parent.is_dir(), "output directory is missing")
        temporary = output.with_name(output.name + ".tmp")
        temporary.write_bytes(raw)
        os.replace(temporary, output)
    verify(payload)
    print(f"records={payload['record_total']} targets={payload['target_total']} "
          f"exact={payload['exact_target_total']} unresolved={payload['unresolved_target_total']}")
    print(f"complete_source_cover={str(payload['complete_source_cover']).lower()} "
          f"sha256={hashlib.sha256(raw).hexdigest()} full_theorem=false")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
