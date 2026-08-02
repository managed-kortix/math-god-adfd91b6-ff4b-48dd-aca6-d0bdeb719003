#!/usr/bin/env python3
"""Deterministic dimension-seven rational Gram experiment for order seven.

Numerical optimization proposes vectors only. Every accepted certificate is
rebuilt from rational stereographic parameters and checked with Fraction.
The output remains fail-closed and is never a theorem fixture.
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
CENSUS_SCRIPT = HERE / "order7-tetra-census-experiment.py"
OUTPUT = HERE / "order7-dim7-rational-gram-results.json"
PAIRS = tuple(itertools.combinations(range(7), 2))
DIMENSION = 7
BUDGET = Fraction(4)
ORDER_LABEL = "order-seven"
SCHEMA = "rank-five-order-seven-dim7-rational-gram-experiment-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def normalized(vector):
    norm = math.sqrt(dot(vector, vector))
    require(norm > 1e-14, "cannot normalize a zero vector")
    return tuple(value / norm for value in vector)


def canonical_lengths(multiplicity, odd):
    require(0 <= odd <= multiplicity, "invalid physical row")
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier=None):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == sum(kernel), "rank-five path count changed")
    if frontier is not None:
        require(type(frontier) is int and 0 <= frontier < len(paths), "invalid frontier")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def path_cost_and_derivative(correlation, length):
    sign = -1.0 if length & 1 else 1.0
    transformed = max(-1.0 + 1e-14, min(1.0 - 1e-14, sign * correlation))
    angle = math.acos(transformed)
    tangent = math.tan(angle / (2.0 * length))
    cost = length * tangent * tangent
    derivative = (-sign * tangent * (1.0 + tangent * tangent)
                  / math.sqrt(max(1e-28, 1.0 - transformed * transformed)))
    return cost, derivative


def objective_and_gradient(paths, vectors):
    total = 0.0
    gradient = [[0.0] * DIMENSION for _ in range(len(vectors))]
    for _, _, u, v, length in paths:
        cost, derivative = path_cost_and_derivative(dot(vectors[u], vectors[v]), length)
        total += cost
        for coordinate in range(DIMENSION):
            gradient[u][coordinate] += derivative * vectors[v][coordinate]
            gradient[v][coordinate] += derivative * vectors[u][coordinate]
    for vertex in range(1, len(vectors)):
        radial = dot(gradient[vertex], vectors[vertex])
        gradient[vertex] = [value - radial * coordinate
                            for value, coordinate in zip(gradient[vertex], vectors[vertex])]
    gradient[0] = [0.0] * DIMENSION
    return total, gradient


def objective(paths, vectors):
    return objective_and_gradient(paths, vectors)[0]


def random_vectors(generator, order):
    return ((1.0,) + (0.0,) * (DIMENSION - 1),) + tuple(
        normalized(tuple(generator.gauss(0.0, 1.0) for _ in range(DIMENSION)))
        for _ in range(order - 1))


def descend(paths, initial, iterations):
    vectors = tuple(initial)
    value = objective(paths, vectors)
    step = 0.25
    for _ in range(iterations):
        value, gradient = objective_and_gradient(paths, vectors)
        norm = math.sqrt(sum(dot(row, row) for row in gradient))
        if norm < 1e-10:
            break
        trial_step = step
        for _ in range(18):
            candidate = [vectors[0]]
            for vertex in range(1, len(vectors)):
                candidate.append(normalized(tuple(
                    vectors[vertex][coordinate] - trial_step * gradient[vertex][coordinate]
                    for coordinate in range(DIMENSION))))
            candidate = tuple(candidate)
            candidate_value = objective(paths, candidate)
            if candidate_value < value - 1e-5 * trial_step * norm * norm:
                vectors, value = candidate, candidate_value
                step = min(0.8, trial_step * 1.35)
                break
            trial_step *= 0.5
        else:
            step *= 0.25
            if step < 1e-11:
                break
    return value, vectors


def optimize(paths, seed, restarts, iterations, warm=()):
    generator = random.Random(seed)
    order = max(max(path[2], path[3]) for path in paths) + 1
    starts = list(warm) + [random_vectors(generator, order) for _ in range(restarts)]
    best = (float("inf"), None)
    for initial in starts:
        candidate = descend(paths, initial, iterations)
        if candidate[0] < best[0]:
            best = candidate
    return best


def rotate_away_from_pole(vectors):
    choices = []
    for coordinate in range(DIMENSION):
        for sign in (-1.0, 1.0):
            choices.append((min(1.0 + sign * row[coordinate] for row in vectors),
                            coordinate, sign))
    _, first, sign = max(choices)
    order = (first,) + tuple(index for index in range(DIMENSION) if index != first)
    return tuple(tuple((sign if position == 0 else 1.0) * row[coordinate]
                       for position, coordinate in enumerate(order))
                 for row in vectors)


def snap_coincident(vectors):
    result = list(vectors)
    for vertex in range(1, len(result)):
        for earlier in range(vertex):
            correlation = dot(result[vertex], result[earlier])
            if correlation > 1.0 - 1e-9:
                result[vertex] = result[earlier]
                break
            if correlation < -1.0 + 1e-9:
                result[vertex] = tuple(-value for value in result[earlier])
                break
    return tuple(result)


def stereographic(vector, denominator):
    scale = 1.0 + vector[0]
    require(abs(scale) > 1e-10, "stereographic pole encountered")
    return tuple(Fraction(round(value / scale * denominator), denominator)
                 for value in vector[1:])


def rational_unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * value / denominator
                                                  for value in parameters)


def slerp(left, right, fraction):
    correlation = max(-1.0, min(1.0, dot(left, right)))
    angle = math.acos(correlation)
    if angle < 1e-12:
        return left
    sine = math.sin(angle)
    return normalized(tuple(
        (math.sin((1.0 - fraction) * angle) * x + math.sin(fraction * angle) * y) / sine
        for x, y in zip(left, right)))


def exact_step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal rational step")
    return (1 - correlation) / (1 + correlation)


def pair(value):
    return [value.numerator, value.denominator]


def rationalize(paths, vectors, denominators):
    vectors = rotate_away_from_pole(snap_coincident(vectors))
    for denominator in denominators:
        try:
            branch_parameters = tuple(stereographic(vector, denominator) for vector in vectors)
            branches = tuple(rational_unit(row) for row in branch_parameters)
            total = Fraction(0)
            internal_parameters = []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                parameters = tuple(stereographic(slerp(vectors[u], endpoint, j / length),
                                                  denominator)
                                   for j in range(1, length))
                internal_parameters.append(parameters)
                chain = [branches[u], *(rational_unit(row) for row in parameters)]
                chain.append(branches[v] if length % 2 == 0
                             else tuple(-x for x in branches[v]))
                total += sum((exact_step_cost(left, right)
                              for left, right in zip(chain, chain[1:])), Fraction(0))
        except (RuntimeError, ZeroDivisionError):
            continue
        if total <= BUDGET:
            return {
                "denominator": denominator,
                "cost": pair(total),
                "branches": [[pair(value) for value in row] for row in branch_parameters],
                "internals": [[[pair(value) for value in row] for row in path]
                              for path in internal_parameters],
            }
    return None


def load_census():
    spec = importlib.util.spec_from_file_location("order7_census", CENSUS_SCRIPT)
    require(spec is not None and spec.loader is not None, "cannot load census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit()[0]


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def parse_frontiers(text, path_count):
    if text == "all":
        return (None, *range(path_count))
    result = []
    for value in text.split(","):
        result.append(None if value == "canonical" else int(value))
    require(result and all(value is None or 0 <= value < path_count for value in result),
            f"frontiers must be all, canonical, or coordinates 0..{path_count - 1}")
    return tuple(result)


def run(args):
    census = load_census()
    kernels = {record["kernel"]: tuple(record["code"]) for record in census["kernels"]}
    residuals = census["residuals"]
    stop = len(residuals) if args.limit is None else min(len(residuals), args.start + args.limit)
    selected = residuals[args.start:stop]
    path_count = census["paths_per_kernel"]
    frontiers = parse_frontiers(args.frontiers, path_count)
    denominators = tuple(int(value) for value in args.denominators.split(","))
    records = []
    for local_index, source in enumerate(selected):
        source_index = args.start + local_index
        number, row = source["kernel"], tuple(source["row"])
        canonical_paths = path_ledger(kernels[number], row)
        canonical_value, canonical_vectors = optimize(
            canonical_paths, args.seed + 1009 * source_index, args.restarts, args.iterations)
        for frontier in frontiers:
            paths = canonical_paths if frontier is None else path_ledger(kernels[number], row, frontier)
            if frontier is None:
                value, vectors = canonical_value, canonical_vectors
            else:
                value, vectors = optimize(
                    paths, args.seed + 1009 * source_index + frontier + 1,
                    args.frontier_restarts, args.iterations, warm=(canonical_vectors,))
            witness = rationalize(paths, vectors, denominators)
            records.append({
                "kernel": number,
                "row": list(row),
                "frontier": frontier,
                "lengths": [path[4] for path in paths],
                "numerical_cost": float(f"{value:.12g}"),
                "exact_dnn_le_4": witness is not None,
                "witness": witness,
            })
        if args.progress:
            exact = sum(record["exact_dnn_le_4"] for record in records)
            print(f"[{local_index + 1}/{len(selected)}] K{number} exact={exact}/{len(records)}",
                  flush=True)
    census_digest = hashlib.sha256(canonical_bytes(census)).hexdigest()
    return {
        "schema": SCHEMA,
        "status": "experimental_partial_exact_certificates",
        "full_theorem": False,
        "dimension": DIMENSION,
        "budget": [4, 1],
        "source_census_sha256": census_digest,
        "source_residual_total": census["tetra_residual_total"],
        "source_frontier_total": census["frontier_target_total"],
        "selected_residual_start": args.start,
        "selected_residual_total": len(selected),
        "selected_frontiers": list(frontiers),
        "target_total": len(records),
        "exact_certificate_total": sum(record["exact_dnn_le_4"] for record in records),
        "finite_unresolved_total": sum(not record["exact_dnn_le_4"] for record in records),
        "complete_source_cover": (args.start == 0 and len(selected) == len(residuals)
                                  and frontiers == (None, *range(path_count))),
        "records": records,
    }


def verify(payload):
    require(payload["full_theorem"] is False, "experiment was theorem-promoted")
    require(payload["exact_certificate_total"] + payload["finite_unresolved_total"]
            == payload["target_total"], "result partition changed")
    census = load_census()
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    require(payload["source_census_sha256"]
            == hashlib.sha256(canonical_bytes(census)).hexdigest(),
            "result points to another census")
    for record in payload["records"]:
        witness = record["witness"]
        require(record["exact_dnn_le_4"] == (witness is not None), "witness status changed")
        if witness is None:
            continue
        paths = path_ledger(kernels[record["kernel"]], tuple(record["row"]),
                            record["frontier"])
        branches_p = tuple(tuple(Fraction(*value) for value in row)
                           for row in witness["branches"])
        branches = tuple(rational_unit(row) for row in branches_p)
        require(len(branches) == max(max(path[2], path[3]) for path in paths) + 1,
                "branch order changed")
        require(all(len(row) == DIMENSION for row in branches),
                 "branch dimensions changed")
        total = Fraction(0)
        require(len(witness["internals"]) == len(paths), "internal ledger changed")
        require([path[4] for path in paths] == record["lengths"], "stored lengths changed")
        for (_, _, u, v, length), raw_internal in zip(paths, witness["internals"]):
            require(len(raw_internal) == length - 1, "internal path width changed")
            parameters = tuple(tuple(Fraction(*value) for value in row)
                               for row in raw_internal)
            chain = [branches[u], *(rational_unit(row) for row in parameters)]
            chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
            total += sum((exact_step_cost(left, right)
                          for left, right in zip(chain, chain[1:])), Fraction(0))
        require(total == Fraction(*witness["cost"]) and total <= BUDGET,
                "exact witness cost changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=6173)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--frontiers", default="all")
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
        print(f"verified_exact={payload['exact_certificate_total']} "
              f"finite_unresolved={payload['finite_unresolved_total']} "
              f"targets={payload['target_total']}")
        return
    payload = run(args)
    require(args.output.parent.is_dir(), "output parent is missing")
    args.output.write_bytes(canonical_bytes(payload))
    verify(payload)
    print(f"{ORDER_LABEL} dimension-{DIMENSION} rational Gram experiment complete")
    print(f"targets={payload['target_total']} exact={payload['exact_certificate_total']} "
          f"finite_unresolved={payload['finite_unresolved_total']}")
    print(f"complete_source_cover={str(payload['complete_source_cover']).lower()} "
          "full_theorem=false")


if __name__ == "__main__":
    main()
