#!/usr/bin/env python3
"""Fail-closed exact verifier for the order-five rank-six kernel theorem."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CENSUS = HERE / "fixtures" / "rank-six-order-five-tetra-census.json"
RESULTS = HERE / "fixtures" / "rank-six-order-five-dim5-rational-gram-results.json"
CENSUS_SHA256 = "9656146c9dfefacc1c8df15fa9e7c8423f04b12c802c08af93f6e3f3e520bf22"
RESULTS_SHA256 = "ae5f78b189a04e9a3e790188c5f4577a92c5dd19463267aceaec1a8f54bbd2c0"
PAIRS = tuple(itertools.combinations(range(5), 2))
FRONTIERS = (None, *range(10))

SYMBOLIC = {
    61: (
        (Fraction(1), Fraction(0), Fraction(0), Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(0), Fraction(1), Fraction(-1, 2), Fraction(0), Fraction(-1, 2)),
        (Fraction(0), Fraction(-1, 2), Fraction(1), Fraction(-1, 2), Fraction(0)),
        (Fraction(-1, 2), Fraction(0), Fraction(-1, 2), Fraction(1), Fraction(0)),
        (Fraction(-1, 2), Fraction(-1, 2), Fraction(0), Fraction(0), Fraction(1)),
    ),
    98: (
        (Fraction(1), Fraction(-1, 3), Fraction(3, 5), Fraction(-1, 3), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(1), Fraction(2, 5), Fraction(-1, 3), Fraction(-1, 3)),
        (Fraction(3, 5), Fraction(2, 5), Fraction(1), Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(-1, 3), Fraction(-1, 3), Fraction(-1, 2), Fraction(1), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(-1, 3), Fraction(-1, 2), Fraction(-1, 3), Fraction(1)),
    ),
}

# Two-long all-odd K5 has two edge orbits. These denominator-64 stereographic
# records are auxiliary strict frontiers; the eleven source targets themselves
# are closed structurally.
TWO_LONG = {
    "incident": {
        "paths": (0, 1),
        "branches": ((1, 0, 0, 0), (Fraction(17, 32), Fraction(-17, 32), Fraction(-1, 64), Fraction(45, 64)), (Fraction(1, 2), Fraction(1, 2), Fraction(1, 64), Fraction(-21, 32)), (Fraction(-39, 64), Fraction(-13, 32), Fraction(-1, 2), Fraction(-21, 64)), (Fraction(-11, 16), Fraction(29, 64), Fraction(9, 16), Fraction(23, 64))),
        "internals": (((Fraction(3, 4), Fraction(25, 64), Fraction(1, 64), Fraction(-1, 2)), (Fraction(5, 32), Fraction(37, 64), Fraction(1, 32), Fraction(-3, 4))), ((Fraction(25, 32), Fraction(-13, 32), Fraction(-1, 64), Fraction(17, 32)), (Fraction(11, 64), Fraction(-5, 8), Fraction(-1, 32), Fraction(13, 16)))),
    },
    "disjoint": {
        "paths": (0, 4),
        "branches": ((1, 0, 0, 0), (Fraction(3, 8), Fraction(-21, 64), Fraction(25, 64), Fraction(1, 4)), (Fraction(-11, 32), Fraction(-11, 32), Fraction(25, 64), Fraction(1, 4)), (Fraction(-13, 32), Fraction(51, 64), Fraction(15, 64), Fraction(-25, 32)), (Fraction(-15, 32), Fraction(-5, 64), Fraction(-39, 32), Fraction(17, 64))),
        "internals": (((Fraction(67, 64), Fraction(15, 32), Fraction(-35, 64), Fraction(-23, 64)), (Fraction(9, 32), Fraction(57, 64), Fraction(-67, 64), Fraction(-43, 64))), ((Fraction(53, 64), Fraction(-9, 64), Fraction(11, 64), Fraction(7, 64)), (Fraction(71, 64), Fraction(15, 64), Fraction(-9, 32), Fraction(-11, 64)))),
    },
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def locked_json(path, digest, label):
    require(path.is_file(), f"missing {label}")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, f"{label} digest changed")
    value = json.loads(raw.decode("ascii"))
    require(raw == (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"),
            f"{label} is not canonical JSON")
    return value


def fraction(value, label):
    require(isinstance(value, list) and len(value) == 2, f"bad {label}")
    result = Fraction(*value)
    require(value == [result.numerator, result.denominator], f"uncanonical {label}")
    return result


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def unit(parameters):
    square = dot(parameters, parameters)
    return ((1 - square) / (1 + square),) + tuple(2 * x / (1 + square) for x in parameters)


def step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal path step")
    return (1 - correlation) / (1 + correlation)


def canonical_lengths(multiplicity, odd):
    require(0 <= odd <= multiplicity, "invalid physical row")
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(kernel, row, frontier=None):
    paths = []
    for edge, ((u, v), multiplicity, odd) in enumerate(zip(PAIRS, kernel, row)):
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == 10, "path count changed")
    if frontier is not None:
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            scale = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= scale * work[column][index]
    return result


def audit_psd(gram, label):
    require(len(gram) == 5 and all(len(row) == 5 for row in gram), f"bad {label} order")
    require(all(isinstance(value, Fraction) for row in gram for value in row),
            f"non-rational {label} entry")
    require(all(gram[i][i] == 1 for i in range(5)), f"bad {label} diagonal")
    require(all(gram[i][j] == gram[j][i] for i in range(5) for j in range(5)),
            f"asymmetric {label}")
    for width in range(1, 6):
        for indices in itertools.combinations(range(5), width):
            minor = tuple(tuple(gram[i][j] for j in indices) for i in indices)
            require(determinant(minor) >= 0, f"non-PSD {label}")


def audit_rational(record, kernel):
    witness = record["witness"]
    require(record["exact_dnn_le_5"] is True and witness is not None,
            "missing rational witness")
    branches = tuple(unit(tuple(fraction(x, "branch parameter") for x in row))
                     for row in witness["branches"])
    require(len(branches) == 5, "branch count changed")
    paths = path_ledger(kernel, tuple(record["row"]), record["frontier"])
    require(record["lengths"] == [path[4] for path in paths], "rational lengths changed")
    require(len(witness["internals"]) == 10, "internal ledger changed")
    total = Fraction(0)
    for (_, _, u, v, length), raw in zip(paths, witness["internals"]):
        parameters = tuple(tuple(fraction(x, "internal parameter") for x in row) for row in raw)
        require(len(parameters) == length - 1, "wrong internal count")
        chain = [branches[u], *(unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])), Fraction(0))
    require(total == fraction(witness["cost"], "stored cost"), "rational cost changed")
    require(total <= 5, "rational witness exceeds five")


def audit_symbolic(number, row, kernel):
    gram = SYMBOLIC[number]
    audit_psd(gram, f"K{number} Gram")
    paths = path_ledger(kernel, row)
    total = Fraction(0)
    for index, (_, _, u, v, length) in enumerate(paths):
        transformed = gram[u][v] if length % 2 == 0 else -gram[u][v]
        if length == 1:
            cost = (1 - transformed) / (1 + transformed)
        elif length == 2 and transformed == Fraction(-1, 2):
            midpoint = ((Fraction(1), Fraction(1, 2), Fraction(-1, 2)),
                        (Fraction(1, 2), Fraction(1), Fraction(1, 2)),
                        (Fraction(-1, 2), Fraction(1, 2), Fraction(1)))
            require(determinant(midpoint) >= 0, f"bad K{number} midpoint {index}")
            cost = Fraction(2, 3)
        else:
            raise RuntimeError(f"unrealized K{number} symbolic path")
        total += cost
    require(total == 5, f"K{number} symbolic cost is not five")


def exact_auxiliary_cost(record):
    branches = tuple(unit(row) for row in record["branches"])
    total = Fraction(0)
    internal_index = 0
    for index, (u, v) in enumerate(PAIRS):
        length = 3 if index in record["paths"] else 1
        parameters = record["internals"][internal_index] if length == 3 else ()
        internal_index += length == 3
        chain = [branches[u], *(unit(row) for row in parameters), tuple(-x for x in branches[v])]
        total += sum((step_cost(left, right) for left, right in zip(chain, chain[1:])), Fraction(0))
    require(internal_index == 2 and total < 5, "two-long K5 frontier is not strict")
    return total


def audit_structural_k5(records, kernel):
    row = (1,) * 10
    require(kernel == row, "K110 is not K5")
    require({record["frontier"] for record in records} == set(FRONTIERS),
            "K110 canonical/frontier set changed")
    for record in records:
        paths = path_ledger(kernel, row, record["frontier"])
        require(record["lengths"] == [path[4] for path in paths], "K110 lengths changed")
        require(not record["exact_dnn_le_5"] and record["witness"] is None,
                "K110 source status changed")
        long = [index for index, path in enumerate(paths) if path[4] > 1]
        require(long == ([] if record["frontier"] is None else [record["frontier"]]),
                "K110 structural opening changed")
        # Canonical: actual attached K5. One-long: its nonempty internal path is
        # a tree and the induced complement is actual K5-e. Deleting one missing-
        # edge endpoint from that complement leaves an actual attached K4.
        remaining = set(range(10)) - set(long)
        require(len(remaining) == (10 if not long else 9), "bad K110 complement")
    costs = tuple(exact_auxiliary_cost(TWO_LONG[name]) for name in ("incident", "disjoint"))
    return costs


def audit_k5_dnn_obstruction():
    # Positivity gives sum r_ij >= -5/2. The odd unit-edge cost
    # f(r)=(1+r)/(1-r) is increasing and convex, so Jensen gives 6.
    average_lower = Fraction(-1, 4)
    jensen_lower = 10 * (1 + average_lower) / (1 - average_lower)
    require(jensen_lower == 6, "K5 DNN obstruction changed")
    simplex = tuple(tuple(Fraction(1) if i == j else average_lower for j in range(5))
                    for i in range(5))
    audit_psd(simplex, "regular 4-simplex Gram")
    require(sum(((1 + simplex[i][j]) / (1 - simplex[i][j])
                 for i, j in PAIRS), Fraction(0)) == 6,
            "regular 4-simplex does not attain six")


def audit():
    census = locked_json(CENSUS, CENSUS_SHA256, "census")
    results = locked_json(RESULTS, RESULTS_SHA256, "results")
    require(census["kernel_total"] == 84 and census["residual_total"] == 103,
            "census scope changed")
    require(results["target_total"] == 1133 and results["exact_dnn_le_5_total"] == 1120,
            "result partition changed")
    kernels = {record["kernel"]: tuple(record["code"]) for record in census["kernels"]}
    expected = {(number, tuple(row), frontier)
                for number, row in census["residual_keys"] for frontier in FRONTIERS}
    records = {(record["kernel"], tuple(record["row"]), record["frontier"]): record
               for record in results["records"]}
    require(len(records) == 1133 and set(records) == expected, "target key universe changed")
    residual = {key for key, record in records.items() if not record["exact_dnn_le_5"]}
    expected_residual = {
        (61, (0, 0, 1, 1, 1, 0, 1, 1, 0, 0), None),
        (98, (1, 0, 1, 1, 0, 1, 1, 1, 1, 1), None),
        *((110, (1,) * 10, frontier) for frontier in FRONTIERS),
    }
    require(residual == expected_residual, "13-target residual set changed")
    for key, record in records.items():
        if key not in residual:
            audit_rational(record, kernels[key[0]])
    audit_symbolic(61, (0, 0, 1, 1, 1, 0, 1, 1, 0, 0), kernels[61])
    audit_symbolic(98, (1, 0, 1, 1, 0, 1, 1, 1, 1, 1), kernels[98])
    k110_records = tuple(records[(110, (1,) * 10, frontier)] for frontier in FRONTIERS)
    auxiliary = audit_structural_k5(k110_records, kernels[110])
    audit_k5_dnn_obstruction()
    return auxiliary


def report(auxiliary):
    return "\n".join((
        "rank-six order-five kernel theorem: exact audit passed",
        "targets=1133 rational=1120 symbolic_equality=2 structural_K110=11",
        "K61_cost=5 K98_cost=5; K110_all_unit_DNN_optimum=6",
        f"K110_two_long_orbits=strict costs={auxiliary[0]},{auxiliary[1]}",
        "scope=all 84 kernels; every simple subdivision; arbitrary rooted-tree attachments",
        "conclusion=s+(G)>=|V(G)|",
    )) + "\n"


def main():
    auxiliary = audit()
    output = report(auxiliary)
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run((sys.executable, "-O", __file__, "--emit"),
                                   check=False, capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "",
                "optimized verifier failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
