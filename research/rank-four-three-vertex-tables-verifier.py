#!/usr/bin/env python3
"""Exact fail-closed audit of the two three-vertex rank-four DNN tables."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path


KERNELS = ((1, 2, 3), (2, 2, 2))
LOW_TABLES = {
    (1, 2, 3): (
        ((0, 0, 0), (0, 0, 0)),
        ((1, 0, 0), (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))),
        ((0, 1, 0), (Fraction(1, 2), Fraction(1, 2), 0)),
        ((0, 0, 1), (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2))),
        ((1, 1, 0), (Fraction(2, 3), Fraction(2, 3), 0)),
        ((1, 0, 1), (Fraction(3, 4), Fraction(1, 4), Fraction(1, 2))),
        ((0, 2, 0), (Fraction(1, 2), Fraction(3, 4), Fraction(1, 4))),
        ((0, 1, 1), (0, Fraction(1, 2), Fraction(1, 2))),
        ((0, 0, 2), (Fraction(1, 3), Fraction(1, 3), Fraction(2, 3))),
    ),
    (2, 2, 2): (
        ((0, 0, 0), (0, 0, 0)),
        ((1, 0, 0), (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))),
        ((2, 0, 0), (Fraction(3, 4), Fraction(1, 3), Fraction(1, 3))),
        ((1, 1, 0), (Fraction(1, 2), Fraction(1, 2), 0)),
    ),
}
EXPECTED_PARTITIONS = ((24, 9, 15), (27, 10, 17))
EXPECTED_SHA256 = "2c563cde590ba034f1b0e16e127e72309b3a8f2b09ca26a5749438f1babf40e0"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact_fraction(value, label):
    require(type(value) is int or isinstance(value, Fraction), label)
    return Fraction(value)


def correlation(t):
    t = exact_fraction(t, "correlation parameter is not exact rational")
    return (1 - 6 * t * t + t ** 4) / (1 + t * t) ** 2


def determinant3(off_diagonal):
    a, b, c = off_diagonal
    return 1 + 2 * a * b * c - a * a - b * b - c * c


def exact_excess(kernel, odd_counts, parameters):
    total = Fraction(0)
    for multiplicity, odd, t in zip(kernel, odd_counts, parameters):
        t = exact_fraction(t, "DNN parameter is not exact rational")
        require(type(multiplicity) is int and type(odd) is int
                and 0 <= odd <= multiplicity,
                "physical odd count is out of range")
        total += (multiplicity - odd) * 2 * t * t
        if odd:
            require(t != 0, "odd canonical path has infinite cost")
            total += odd * ((1 - t * t) / (2 * t)) ** 2
    return total


def low_certificate(kernel, odd_counts, tables):
    table = tables[kernel]
    if kernel != (2, 2, 2):
        matches = [parameters for row, parameters in table if row == odd_counts]
    else:
        matches = []
        for row, parameters in table:
            for permutation in permutations(range(3)):
                if tuple(row[index] for index in permutation) == odd_counts:
                    matches.append(tuple(parameters[index] for index in permutation))
    require(matches, f"missing low-odd table row: {kernel}, {odd_counts}")
    return min(matches)


def rational_record(kernel, odd_counts, parameters, kind):
    correlations = tuple(correlation(value) for value in parameters)
    require(all(-1 <= value <= 1 for value in correlations),
            "correlation lies outside [-1,1]")
    determinant = determinant3(correlations)
    require(determinant >= 0, "three-by-three Gram matrix is not PSD")
    excess = exact_excess(kernel, odd_counts, parameters)
    require(excess <= 3, "canonical DNN excess exceeds three")
    return {
        "kernel": list(kernel),
        "odd_counts": list(odd_counts),
        "certificate": kind,
        "parameters": [[Fraction(value).numerator, Fraction(value).denominator]
                       for value in parameters],
        "excess": [excess.numerator, excess.denominator],
        "gram_determinant": [determinant.numerator, determinant.denominator],
    }


def regenerate(tables=LOW_TABLES):
    require(set(tables) == set(KERNELS), "three-vertex kernel table changed")
    records = []
    partitions = []
    for kernel in KERNELS:
        rows = tuple(product(*(range(value + 1) for value in kernel)))
        low = high = 0
        for odd_counts in rows:
            if sum(odd_counts) < 3:
                parameters = low_certificate(kernel, odd_counts, tables)
                record = rational_record(kernel, odd_counts, parameters, "low-rational-table")
                require(Fraction(*record["excess"]) < 3,
                        "low-odd table row is not strict")
                low += 1
            else:
                # Correlation -1/2 has odd cost 1/3 and even cost 2/3.
                q = sum(odd_counts)
                excess = Fraction(q, 3) + Fraction(2 * (6 - q), 3)
                require(excess <= 3, "common simplex certificate misses budget")
                record = {
                    "kernel": list(kernel),
                    "odd_counts": list(odd_counts),
                    "certificate": "common-minus-one-half",
                    "parameters": None,
                    "excess": [excess.numerator, excess.denominator],
                    "gram_determinant": [0, 1],
                }
                high += 1
            records.append(record)
        partitions.append((len(rows), low, high))
    require(tuple(partitions) == EXPECTED_PARTITIONS,
            "physical low/high partition changed")
    return {
        "schema": "rank-four-three-vertex-dnn-tables-v1",
        "scope": "kernels (1,2,3) and (2,2,2); every physical parity row; all fixed-parity lengths",
        "partitions": [list(row) for row in partitions],
        "records": records,
    }


def serialize(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def audit(tables=LOW_TABLES, expected_digest=EXPECTED_SHA256):
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    payload = regenerate(tables)
    digest = hashlib.sha256(serialize(payload).encode("ascii")).hexdigest()
    require(digest == expected_digest, "three-vertex table digest changed")
    return payload, digest


def expect_rejected(action, label):
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    changed = deepcopy(LOW_TABLES)
    changed[(1, 2, 3)] = changed[(1, 2, 3)][:-1]
    expect_rejected(lambda: audit(changed), "deleted low table row")
    changed = deepcopy(LOW_TABLES)
    rows = list(changed[(2, 2, 2)])
    rows[1] = (rows[1][0], (Fraction(1, 3),) * 3)
    changed[(2, 2, 2)] = tuple(rows)
    expect_rejected(lambda: audit(changed), "changed rational certificate")
    expect_rejected(lambda: audit(LOW_TABLES, "0" * 64), "digest mutation")
    for label, value in (("boolean exact payload", True),
                         ("floating exact payload", 0.5),
                         ("nonintegral count payload", Fraction(1, 2))):
        changed = deepcopy(LOW_TABLES)
        rows = list(changed[(1, 2, 3)])
        if label == "nonintegral count payload":
            row = list(rows[0][0])
            row[0] = value
            rows[0] = (tuple(row), rows[0][1])
        else:
            parameters = list(rows[1][1])
            parameters[0] = value
            rows[1] = (rows[1][0], tuple(parameters))
        changed[(1, 2, 3)] = tuple(rows)
        expect_rejected(lambda changed=changed: audit(changed), label)
    return 6


def report(payload, digest, mutations):
    partitions = payload["partitions"]
    return "\n".join((
        "three-vertex rank-four DNN tables: exact audit passed",
        "kernels: multiplicities (1,2,3) and (2,2,2)",
        f"physical_partition_123: {partitions[0][0]} = {partitions[0][1]} low-table + {partitions[0][2]} common",
        f"physical_partition_222: {partitions[1][0]} = {partitions[1][1]} low-table + {partitions[1][2]} common",
        "coverage: every physical parity row and every fixed-parity path length",
        "arithmetic: fractions.Fraction; all Gram principal minors exact",
        f"table_payload_sha256: {digest}",
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
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    payload, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 6, "hostile mutation count changed")
    output = report(payload, digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
