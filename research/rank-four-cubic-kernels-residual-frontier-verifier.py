#!/usr/bin/env python3
"""Freeze and audit rational path-vector frontiers for cubic kernels 13--15."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SIEVE_FIXTURE = HERE / "fixtures" / "rank-four-cubic-kernels-three-color-sieve.json"
FIXTURE = HERE / "fixtures" / "rank-four-cubic-kernels-residual-frontiers.json"
EXPECTED_SHA256 = "8b14bcc20767f2dfdb58577a001b6bc9300295e880c4c84fadc52a60458bc00c"
PAIRS = tuple(combinations(range(6), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
KERNELS = {
    13: (0, 0, 0, 1, 2, 0, 1, 1, 1, 2, 1, 0, 0, 0, 0),
    14: (0, 0, 0, 1, 2, 0, 1, 2, 0, 2, 0, 1, 0, 0, 0),
    15: (0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0),
}
EXPECTED_RESIDUALS = (5, 6, 5)
EXPECTED_TARGETS = 160
EXPECTED_RECORDS = 148
EXPECTED_UNRESOLVED = 12
SEARCH_DIMENSION = 4
SEARCH_RESTARTS = 4
SEARCH_STEPS = 10000
SEARCH_DENOMINATORS = (32, 64, 128, 256)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_lengths(multiplicity, odd_count):
    require(0 <= odd_count <= multiplicity <= 2, "bad physical bundle count")
    return {
        (0, 0): (),
        (1, 0): (2,),
        (1, 1): (1,),
        (2, 0): (2, 2),
        (2, 1): (1, 2),
        (2, 2): (1, 3),
    }[multiplicity, odd_count]


def path_ledger(kernel, row, coordinate=None):
    result = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)):
            result.append((edge, occurrence, u, v, length))
    require(len(result) == 9, "cubic physical path count changed")
    if coordinate is not None:
        require(type(coordinate) is int and 0 <= coordinate < len(result),
                "invalid frontier coordinate")
        path = result[coordinate]
        result[coordinate] = (*path[:-1], path[-1] + 2)
    return tuple(result)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def rational_unit(parameters):
    square = sum(x * x for x in parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(
        2 * x / denominator for x in parameters)


def exact_step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal exact step")
    return (1 - correlation) / (1 + correlation)


def exact_cost(paths, branches, internals):
    require(len(branches) == 6, "branch ledger width changed")
    require(len(paths) == len(internals), "internal path ledger mismatch")
    vectors = tuple(rational_unit(row) for row in branches)
    require(all(dot(vector, vector) == 1 for vector in vectors),
            "rational stereographic vector is not unit")
    total = Fraction(0)
    for (_, _, u, v, length), parameters in zip(paths, internals):
        require(len(parameters) == length - 1, "internal path width changed")
        chain = [vectors[u], *(rational_unit(row) for row in parameters)]
        endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
        chain.append(endpoint)
        total += sum(exact_step_cost(left, right)
                     for left, right in zip(chain, chain[1:]))
    return total


def normalized(vector):
    norm = math.sqrt(sum(x * x for x in vector))
    return tuple(x / norm for x in vector)


def reduced_path_cost(left, right, length):
    correlation = max(-1.0, min(1.0, sum(x * y for x, y in zip(left, right))))
    correlation = -correlation if length % 2 else correlation
    angle = math.acos(correlation)
    return length * math.tan(angle / (2 * length)) ** 2


def reduced_cost(paths, branches):
    return sum(reduced_path_cost(branches[u], branches[v], length)
               for _, _, u, v, length in paths)


def numerical_search(paths, seed):
    generator = random.Random(seed)
    best = (float("inf"), None)
    for _ in range(SEARCH_RESTARTS):
        branches = [(1.0,) + (0.0,) * (SEARCH_DIMENSION - 1)]
        branches.extend(normalized(tuple(generator.gauss(0, 1)
                                         for _ in range(SEARCH_DIMENSION)))
                        for _ in range(5))
        value = reduced_cost(paths, branches)
        scale = 0.8
        for _ in range(SEARCH_STEPS):
            vertex = generator.randrange(1, 6)
            candidate = list(branches)
            candidate[vertex] = normalized(tuple(
                x + generator.gauss(0, scale) for x in branches[vertex]))
            candidate_value = reduced_cost(paths, candidate)
            temperature = max(1e-8, 0.005 * scale)
            if (candidate_value < value or generator.random() < math.exp(
                    max(-50.0, (value - candidate_value) / temperature))):
                branches, value = candidate, candidate_value
            scale *= 0.9995
        if value < best[0]:
            best = value, tuple(branches)
    return best


def slerp(left, right, fraction):
    correlation = max(-1.0, min(1.0, dot(left, right)))
    angle = math.acos(correlation)
    if angle < 1e-12:
        return left
    denominator = math.sin(angle)
    return normalized(tuple(
        (math.sin((1 - fraction) * angle) * x
         + math.sin(fraction * angle) * y) / denominator
        for x, y in zip(left, right)))


def stereographic(vector, denominator):
    scale = 1 + vector[0]
    require(abs(scale) > 1e-10, "stereographic pole encountered")
    return tuple(Fraction(round(x / scale * denominator), denominator)
                 for x in vector[1:])


def rounded_certificate(paths, numerical_branches, denominator):
    branches = tuple(stereographic(vector, denominator)
                     for vector in numerical_branches)
    internals = []
    for _, _, u, v, length in paths:
        endpoint = (numerical_branches[v] if length % 2 == 0 else
                    tuple(-x for x in numerical_branches[v]))
        internals.append(tuple(
            stereographic(slerp(numerical_branches[u], endpoint, j / length),
                          denominator)
            for j in range(1, length)))
    internals = tuple(internals)
    return exact_cost(paths, branches, internals), branches, internals


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in permutations(range(6))
                 if relabel(kernel, permutation) == kernel)


def residual_rows():
    require(SIEVE_FIXTURE.is_file(), "missing cubic-kernel sieve fixture")
    sieve = json.loads(SIEVE_FIXTURE.read_text(encoding="ascii"))
    require(sieve.get("residual_total") == 17, "source residual total changed")
    result = {}
    for number, kernel in KERNELS.items():
        group = automorphisms(kernel)
        rows = tuple(tuple(record["row"]) for record in sieve["records"]
                     if record["kernel"] == number and record["sieve_residual"])
        require(all(row == min(relabel(row, permutation) for permutation in group)
                    for row in rows), "source residual is not canonical")
        result[number] = rows
    require(tuple(len(result[number]) for number in KERNELS) == EXPECTED_RESIDUALS,
            "kernels 13--15 residual split changed")
    require(sum(record["kernel"] == 17 and record["sieve_residual"]
                for record in sieve["records"]) == 1,
            "separate kernel-17 residual changed")
    return result


def encode_rows(rows):
    return [[str(value) for value in row] for row in rows]


def seed_for(number, row_index, coordinate):
    return number * 1000 + row_index * 10 + (0 if coordinate is None else coordinate + 1)


def regenerate_payload():
    records = []
    unresolved = []
    for number, rows in residual_rows().items():
        for row_index, row in enumerate(rows):
            for coordinate in (None, *range(9)):
                paths = path_ledger(KERNELS[number], row, coordinate)
                numerical, vectors = numerical_search(paths,
                                                       seed_for(number, row_index,
                                                                coordinate))
                accepted = None
                for denominator in SEARCH_DENOMINATORS:
                    candidate = rounded_certificate(paths, vectors, denominator)
                    if candidate[0] < 3:
                        accepted = (denominator, *candidate)
                        break
                if accepted is None:
                    unresolved.append({
                        "kernel": number,
                        "row": list(row),
                        "frontier_coordinate": coordinate,
                        "numerical_cost": format(numerical, ".15f"),
                        "status": "no strict rational witness found; numerical equality candidate",
                    })
                    continue
                denominator, cost, branches, internals = accepted
                records.append({
                    "kernel": number,
                    "row": list(row),
                    "frontier_coordinate": coordinate,
                    "lengths": [path[4] for path in paths],
                    "search_seed": seed_for(number, row_index, coordinate),
                    "rounding_denominator": denominator,
                    "branches": encode_rows(branches),
                    "internals": [encode_rows(path) for path in internals],
                    "cost": [cost.numerator, cost.denominator],
                })
    return {
        "schema": "rank-four-cubic-kernels-residual-frontiers-v1",
        "scope": "16 residual orbits of kernels 13--15; kernel 17 is separate",
        "pair_order": list(PAIR_NAMES),
        "search": {
            "algorithm": "seeded rational stereographic path-vector search",
            "dimension": SEARCH_DIMENSION,
            "restarts": SEARCH_RESTARTS,
            "steps": SEARCH_STEPS,
            "denominators": list(SEARCH_DENOMINATORS),
        },
        "residual_orbits_by_kernel": {str(number): len(rows)
                                      for number, rows in residual_rows().items()},
        "target_total": EXPECTED_TARGETS,
        "unresolved": unresolved,
        "records": records,
    }


def serialize(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def load_fixture():
    require(FIXTURE.is_file(), f"missing fixture: {FIXTURE}")
    value = json.loads(FIXTURE.read_text(encoding="ascii"))
    require(isinstance(value, dict), "fixture root is not an object")
    return value


def expected_keys():
    return tuple((number, row, coordinate)
                 for number, rows in residual_rows().items()
                 for row in rows for coordinate in (None, *range(9)))


def audit(payload=None, expected_digest=EXPECTED_SHA256):
    fixture = load_fixture() if payload is None else payload
    require(fixture.get("schema") == "rank-four-cubic-kernels-residual-frontiers-v1",
            "fixture schema changed")
    require(fixture.get("scope") ==
            "16 residual orbits of kernels 13--15; kernel 17 is separate",
            "fixture scope changed")
    require(fixture.get("pair_order") == list(PAIR_NAMES), "pair order changed")
    require(fixture.get("search") == {
        "algorithm": "seeded rational stereographic path-vector search",
        "dimension": SEARCH_DIMENSION,
        "restarts": SEARCH_RESTARTS,
        "steps": SEARCH_STEPS,
        "denominators": list(SEARCH_DENOMINATORS),
    }, "search policy changed")
    require(fixture.get("residual_orbits_by_kernel") == {"13": 5, "14": 6, "15": 5},
            "residual ledger changed")
    require(fixture.get("target_total") == EXPECTED_TARGETS, "target total changed")
    records = fixture.get("records")
    require(isinstance(records, list) and len(records) == EXPECTED_RECORDS,
            "frontier record count changed")
    keys = []
    for record in records:
        require(set(record) == {"kernel", "row", "frontier_coordinate", "lengths",
                                "search_seed", "rounding_denominator", "branches",
                                "internals", "cost"}, "record schema changed")
        number = record["kernel"]
        row = tuple(record["row"])
        coordinate = record["frontier_coordinate"]
        keys.append((number, row, coordinate))
        paths = path_ledger(KERNELS[number], row, coordinate)
        require(record["lengths"] == [path[4] for path in paths],
                "frontier length vector changed")
        row_index = residual_rows()[number].index(row)
        require(record["search_seed"] == seed_for(number, row_index, coordinate),
                "search seed changed")
        require(record["rounding_denominator"] in SEARCH_DENOMINATORS,
                "rounding denominator changed")
        branches = tuple(tuple(Fraction(value) for value in branch)
                         for branch in record["branches"])
        internals = tuple(tuple(tuple(Fraction(value) for value in vector)
                                for vector in path)
                          for path in record["internals"])
        actual = exact_cost(paths, branches, internals)
        require(actual == Fraction(*record["cost"]), "exact Fraction cost mismatch")
        require(actual < 3, "frontier witness is not strict")
    unresolved = fixture.get("unresolved")
    require(isinstance(unresolved, list) and len(unresolved) == EXPECTED_UNRESOLVED,
            "unresolved frontier count changed")
    unresolved_keys = []
    for record in unresolved:
        require(set(record) == {"kernel", "row", "frontier_coordinate",
                                "numerical_cost", "status"},
                "unresolved record schema changed")
        require(record["status"] ==
                "no strict rational witness found; numerical equality candidate",
                "unresolved status changed")
        unresolved_keys.append((record["kernel"], tuple(record["row"]),
                                record["frontier_coordinate"]))
    all_keys = tuple(sorted(keys + unresolved_keys,
                            key=lambda key: expected_keys().index(key)))
    require(all_keys == expected_keys(), "frontier targets are not exact")
    require({(number, row) for number, row, _ in unresolved_keys} == {
        (14, residual_rows()[14][0]),
        (14, residual_rows()[14][1]),
        (14, residual_rows()[14][4]),
    }, "unexpected residual row remains unresolved")
    require({coordinate for _, _, coordinate in unresolved_keys} == {None, 0, 3, 8},
            "unresolved coordinate pattern changed")
    require(len(set(keys)) == EXPECTED_RECORDS, "duplicate frontier key")
    digest = hashlib.sha256(serialize(fixture).encode("ascii")).hexdigest()
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(digest == expected_digest, "fixture digest changed")
    return digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    baseline = load_fixture()
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted certificate", lambda value: value["records"].pop())
    add("changed branch", lambda value: value["records"][0]["branches"][1]
        .__setitem__(0, "1"))
    add("changed internal", lambda value: value["records"][0]["internals"][0]
        .__setitem__(0, ["0", "0", "0"]))
    add("forged cost", lambda value: value["records"][0]["cost"].__setitem__(0, 1))
    add("changed coordinate", lambda value: value["records"][0]
        .__setitem__("frontier_coordinate", 0))
    add("foreign residual", lambda value: value["records"][0]["row"].__setitem__(4, 0))
    add("changed seed", lambda value: value["records"][0].__setitem__("search_seed", 1))
    add("lost unresolved target", lambda value: value["unresolved"].pop())
    add("changed pair order", lambda value: value["pair_order"].reverse())
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    return len(mutations) + 1


def report(digest, mutations):
    fixture = load_fixture()
    costs = [Fraction(*record["cost"]) for record in fixture["records"]]
    equal = sum(cost == 3 for cost in costs)
    return "\n".join((
        "cubic kernels 13--15 residual frontier: exact audit passed",
        "source_residual_orbits: 16 (K13=5, K14=6, K15=5); K17=1 separate",
        "frontier_targets: 16 canonical + 144 one-coordinate-plus-two = 160",
        "strict_fraction_certificates: 148; unresolved_equality_candidates: 12",
        "cost_backend: fractions.Fraction; strict_budget: cost < 3",
        f"maximum_exact_cost: {max(costs)}",
        f"certified_equalities: {equal}; missing_strict_witnesses: 12 "
        "(3 K14 rows x canonical/coordinates 0,3,8)",
        f"fixture_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run(
        [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
        check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    require(completed.stderr == "", "python -O verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        require(FIXTURE.parent.is_dir(), "fixture directory is missing")
        FIXTURE.write_text(serialize(regenerate_payload()), encoding="ascii")
        print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        return 0
    digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 10, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
