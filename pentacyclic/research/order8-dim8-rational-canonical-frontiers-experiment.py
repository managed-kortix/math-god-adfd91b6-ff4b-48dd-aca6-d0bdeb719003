#!/usr/bin/env python3
"""Dimension-eight rational canonical-plus-twelve-frontier experiment.

The numerical stage proposes vectors only. Accepted records are rebuilt from
rational stereographic parameters and checked exactly. Missing witnesses stay
explicitly unresolved; this script cannot promote a theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CENSUS_SCRIPT = HERE / "order8-cubic-tetra-census-experiment.py"
OUTPUT = HERE / "order8-dim8-rational-canonical-frontiers-results.json"
PAIRS = tuple(itertools.combinations(range(8), 2))
DIMENSION = 8
BUDGET = Fraction(4)
PATHS_PER_KERNEL = 12


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def normalized(vector):
    norm = math.sqrt(dot(vector, vector))
    require(norm > 1e-14, "cannot normalize zero vector")
    return tuple(value / norm for value in vector)


def canonical_lengths(multiplicity, odd):
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier=None):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == PATHS_PER_KERNEL, "order-eight path count changed")
    if frontier is not None:
        require(0 <= frontier < PATHS_PER_KERNEL, "invalid frontier")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def path_cost_and_derivative(correlation, length):
    sign = -1.0 if length & 1 else 1.0
    transformed = max(-1.0 + 1e-14, min(1.0 - 1e-14, sign * correlation))
    angle = math.acos(transformed)
    tangent = math.tan(angle / (2.0 * length))
    return (length * tangent * tangent,
            -sign * tangent * (1.0 + tangent * tangent)
            / math.sqrt(max(1e-28, 1.0 - transformed * transformed)))


def objective_and_gradient(paths, vectors):
    total = 0.0
    gradient = [[0.0] * DIMENSION for _ in range(8)]
    for _, _, u, v, length in paths:
        cost, derivative = path_cost_and_derivative(dot(vectors[u], vectors[v]), length)
        total += cost
        for coordinate in range(DIMENSION):
            gradient[u][coordinate] += derivative * vectors[v][coordinate]
            gradient[v][coordinate] += derivative * vectors[u][coordinate]
    for vertex in range(1, 8):
        radial = dot(gradient[vertex], vectors[vertex])
        gradient[vertex] = [value - radial * coordinate
                            for value, coordinate in zip(gradient[vertex], vectors[vertex])]
    gradient[0] = [0.0] * DIMENSION
    return total, gradient


def objective(paths, vectors):
    return objective_and_gradient(paths, vectors)[0]


def random_vectors(generator):
    return ((1.0,) + (0.0,) * 7,) + tuple(
        normalized(tuple(generator.gauss(0.0, 1.0) for _ in range(DIMENSION)))
        for _ in range(7))


def descend(paths, initial, iterations):
    vectors = tuple(initial)
    step = 0.25
    for _ in range(iterations):
        value, gradient = objective_and_gradient(paths, vectors)
        norm = math.sqrt(sum(dot(row, row) for row in gradient))
        if norm < 1e-10:
            break
        trial_step = step
        for _ in range(18):
            candidate = [vectors[0]]
            for vertex in range(1, 8):
                candidate.append(normalized(tuple(
                    vectors[vertex][coordinate] - trial_step * gradient[vertex][coordinate]
                    for coordinate in range(DIMENSION))))
            candidate = tuple(candidate)
            candidate_value = objective(paths, candidate)
            if candidate_value < value - 1e-5 * trial_step * norm * norm:
                vectors = candidate
                step = min(0.8, trial_step * 1.35)
                break
            trial_step *= 0.5
        else:
            step *= 0.25
            if step < 1e-11:
                break
    return objective(paths, vectors), vectors


def optimize(paths, seed, restarts, iterations, warm=()):
    generator = random.Random(seed)
    starts = list(warm) + [random_vectors(generator) for _ in range(restarts)]
    return min((descend(paths, initial, iterations) for initial in starts), key=lambda row: row[0])


def rotate_away_from_pole(vectors):
    choices = [(min(1.0 + sign * row[coordinate] for row in vectors), coordinate, sign)
               for coordinate in range(DIMENSION) for sign in (-1.0, 1.0)]
    _, first, sign = max(choices)
    order = (first,) + tuple(index for index in range(DIMENSION) if index != first)
    return tuple(tuple((sign if position == 0 else 1.0) * row[coordinate]
                       for position, coordinate in enumerate(order)) for row in vectors)


def stereographic(vector, denominator):
    scale = 1.0 + vector[0]
    require(abs(scale) > 1e-10, "stereographic pole")
    return tuple(Fraction(round(value / scale * denominator), denominator) for value in vector[1:])


def rational_unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * value / denominator for value in parameters)


def slerp(left, right, fraction):
    correlation = max(-1.0, min(1.0, dot(left, right)))
    angle = math.acos(correlation)
    if angle < 1e-12:
        return left
    sine = math.sin(angle)
    return normalized(tuple((math.sin((1.0 - fraction) * angle) * x
                             + math.sin(fraction * angle) * y) / sine
                            for x, y in zip(left, right)))


def exact_step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal rational step")
    return (1 - correlation) / (1 + correlation)


def pair(value):
    return [value.numerator, value.denominator]


def rationalize(paths, vectors, denominators):
    vectors = rotate_away_from_pole(vectors)
    for denominator in denominators:
        try:
            branch_parameters = tuple(stereographic(vector, denominator) for vector in vectors)
            branches = tuple(rational_unit(row) for row in branch_parameters)
            total = Fraction(0)
            internals = []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                parameters = tuple(stereographic(slerp(vectors[u], endpoint, j / length), denominator)
                                   for j in range(1, length))
                internals.append(parameters)
                chain = [branches[u], *(rational_unit(row) for row in parameters),
                         branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])]
                total += sum((exact_step_cost(left, right)
                              for left, right in zip(chain, chain[1:])), Fraction(0))
        except (RuntimeError, ZeroDivisionError):
            continue
        if total <= BUDGET:
            return {
                "denominator": denominator,
                "cost": pair(total),
                "branches": [[pair(value) for value in row] for row in branch_parameters],
                "internals": [[[pair(value) for value in row] for row in path] for path in internals],
            }
    return None


def load_census():
    spec = importlib.util.spec_from_file_location("order8_census", CENSUS_SCRIPT)
    require(spec is not None and spec.loader is not None, "cannot load census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit()[0]


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def run(args):
    census = load_census()
    kernels = {record["kernel"]: tuple(record["code"]) for record in census["kernels"]}
    stop = len(census["residuals"]) if args.limit is None else min(
        len(census["residuals"]), args.start + args.limit)
    selected = census["residuals"][args.start:stop]
    denominators = tuple(int(value) for value in args.denominators.split(","))
    records = []
    for local_index, source in enumerate(selected):
        source_index = args.start + local_index
        kernel = kernels[source["kernel"]]
        row = tuple(source["row"])
        canonical_paths = path_ledger(kernel, row)
        canonical_value, canonical_vectors = optimize(
            canonical_paths, args.seed + 1009 * source_index, args.restarts, args.iterations)
        for frontier in (None, *range(PATHS_PER_KERNEL)):
            paths = canonical_paths if frontier is None else path_ledger(kernel, row, frontier)
            if frontier is None:
                value, vectors = canonical_value, canonical_vectors
            else:
                value, vectors = optimize(paths, args.seed + 1009 * source_index + frontier + 1,
                                          args.frontier_restarts, args.iterations,
                                          warm=(canonical_vectors,))
            witness = rationalize(paths, vectors, denominators)
            records.append({
                "kernel": source["kernel"], "row": list(row), "frontier": frontier,
                "row118_cycle_equality": source["row118_cycle_equality"],
                "lengths": [path[4] for path in paths],
                "numerical_cost": float(f"{value:.12g}"),
                "exact_dnn_le_4": witness is not None, "witness": witness,
            })
        if args.progress:
            exact = sum(record["exact_dnn_le_4"] for record in records)
            print(f"[{local_index + 1}/{len(selected)}] K{source['kernel']} exact={exact}/{len(records)}",
                  flush=True)
    unresolved = [record for record in records if not record["exact_dnn_le_4"]]
    return {
        "schema": "rank-five-order-eight-dim8-rational-canonical-frontiers-experiment-v1",
        "status": "experimental_partial_exact_certificates",
        "full_theorem": False,
        "experiment_fixture_frozen": True,
        "dimension": DIMENSION,
        "budget": [4, 1],
        "source_census_sha256": hashlib.sha256(canonical_bytes(census)).hexdigest(),
        "source_residual_total": census["tetra_residual_total"],
        "source_frontier_total": census["frontier_target_total"],
        "selected_residual_start": args.start,
        "selected_residual_total": len(selected),
        "frontiers_per_residual": 13,
        "target_total": len(records),
        "exact_certificate_total": len(records) - len(unresolved),
        "finite_unresolved_total": len(unresolved),
        "complete_source_cover": args.start == 0 and len(selected) == len(census["residuals"]),
        "unresolved_keys": [[record["kernel"], record["row"], record["frontier"]]
                            for record in unresolved],
        "records": records,
    }


def verify(payload):
    require(payload["full_theorem"] is False, "experiment was theorem-promoted")
    require(payload["experiment_fixture_frozen"] is True, "experiment is not frozen")
    require(payload["exact_certificate_total"] + payload["finite_unresolved_total"]
            == payload["target_total"], "result partition changed")
    require(len(payload["unresolved_keys"]) == payload["finite_unresolved_total"],
            "unresolved report changed")
    census = load_census()
    kernels = {record["kernel"]: tuple(record["code"]) for record in census["kernels"]}
    require(payload["source_census_sha256"]
            == hashlib.sha256(canonical_bytes(census)).hexdigest(),
            "result points to another census")
    unresolved = []
    for record in payload["records"]:
        witness = record["witness"]
        require(record["exact_dnn_le_4"] == (witness is not None), "witness status changed")
        if witness is None:
            unresolved.append([record["kernel"], record["row"], record["frontier"]])
            continue
        branch_parameters = tuple(tuple(Fraction(*value) for value in row)
                                  for row in witness["branches"])
        branches = tuple(rational_unit(row) for row in branch_parameters)
        require(len(branches) == 8 and all(len(row) == DIMENSION for row in branches),
                "branch dimensions changed")
        paths = path_ledger(kernels[record["kernel"]], tuple(record["row"]), record["frontier"])
        require([path[4] for path in paths] == record["lengths"], "stored lengths changed")
        require(len(witness["internals"]) == PATHS_PER_KERNEL, "internal ledger changed")
        total = Fraction(0)
        for (_, _, u, v, length), raw_internal in zip(paths, witness["internals"]):
            require(len(raw_internal) == length - 1, "internal path width changed")
            parameters = tuple(tuple(Fraction(*value) for value in row) for row in raw_internal)
            chain = [branches[u], *(rational_unit(row) for row in parameters),
                     branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])]
            total += sum((exact_step_cost(left, right)
                          for left, right in zip(chain, chain[1:])), Fraction(0))
        require(total == Fraction(*witness["cost"]) and total <= BUDGET,
                "exact witness cost changed")
    require(unresolved == payload["unresolved_keys"], "unresolved keys changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=8118)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--restarts", type=int, default=6)
    parser.add_argument("--frontier-restarts", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=900)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        payload = json.loads(args.verify.read_text(encoding="ascii"))
        verify(payload)
    else:
        payload = run(args)
        args.output.write_bytes(canonical_bytes(payload))
        verify(payload)
    print(f"targets={payload['target_total']} exact={payload['exact_certificate_total']} "
          f"finite_unresolved={payload['finite_unresolved_total']}")
    print(f"complete_source_cover={str(payload['complete_source_cover']).lower()} "
          "experiment_fixture_frozen=true full_theorem=false")
    for key in payload["unresolved_keys"]:
        print(f"unresolved K{key[0]} row={tuple(key[1])} frontier={key[2]}")


if __name__ == "__main__":
    main()
