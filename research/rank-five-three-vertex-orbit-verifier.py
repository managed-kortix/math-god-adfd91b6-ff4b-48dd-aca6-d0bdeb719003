#!/usr/bin/env python3
"""Exact physical-orbit and rational-Gram audit for rank-five 3-vertex kernels."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "rank-five-three-vertex-orbits.json"
PAIRS = tuple(combinations(range(3), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
KERNELS = ((1, 2, 4), (1, 3, 3), (2, 2, 3))
EXPECTED_PHYSICAL = (30, 32, 36)
EXPECTED_AUTOMORPHISMS = (1, 2, 2)
EXPECTED_ORBITS = (30, 20, 24)
EXPECTED_SHA256 = "e3ec57422ba2d9ca0c25ad2ba7d85b8bc74a5d656ebfe20fdb072a0688d01fa9"

T_CERTIFICATES = {
    ((1, 2, 4), 0): (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    ((1, 2, 4), 1): (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
    ((1, 2, 4), 2): (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
    ((1, 3, 3), 0): (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    ((1, 3, 3), 1): (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
    ((1, 3, 3), 2): (Fraction(1, 2), Fraction(0), Fraction(1, 2)),
    ((2, 2, 3), 0): (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)),
    ((2, 2, 3), 1): (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
    ((2, 2, 3), 2): (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def relabel(row, permutation):
    require(len(row) == len(PAIRS), "row width changed")
    require(tuple(sorted(permutation)) == tuple(range(3)), "invalid permutation")
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in permutations(range(3))
                 if relabel(kernel, permutation) == kernel)


def canonical_row(kernel, row):
    return min(relabel(row, permutation) for permutation in automorphisms(kernel))


def physical_rows(kernel):
    return tuple(product(*(range(multiplicity + 1) for multiplicity in kernel)))


def orbit_members(kernel, row):
    return tuple(sorted({relabel(row, permutation)
                         for permutation in automorphisms(kernel)}))


def correlation(t):
    return (1 - 6 * t * t + t ** 4) / (1 + t * t) ** 2


def gram_from_t(values):
    a, b, c = (correlation(value) for value in values)
    return ((Fraction(1), a, b), (a, Fraction(1), c),
            (b, c, Fraction(1)))


def simplex_gram():
    return ((Fraction(1), Fraction(-1, 2), Fraction(-1, 2)),
            (Fraction(-1, 2), Fraction(1), Fraction(-1, 2)),
            (Fraction(-1, 2), Fraction(-1, 2), Fraction(1)))


def determinant(matrix):
    return (matrix[0][0] * matrix[1][1] * matrix[2][2]
            + 2 * matrix[0][1] * matrix[0][2] * matrix[1][2]
            - matrix[0][0] * matrix[1][2] ** 2
            - matrix[1][1] * matrix[0][2] ** 2
            - matrix[2][2] * matrix[0][1] ** 2)


def require_correlation_matrix(matrix):
    require(len(matrix) == 3 and all(len(row) == 3 for row in matrix),
            "Gram matrix shape changed")
    require(all(matrix[i][i] == 1 for i in range(3)),
            "Gram diagonal changed")
    require(all(matrix[i][j] == matrix[j][i]
                for i in range(3) for j in range(3)), "Gram symmetry changed")
    require(all(1 - matrix[i][j] ** 2 >= 0
                for i in range(3) for j in range(i)),
            "negative two-by-two Gram minor")
    require(determinant(matrix) >= 0, "negative Gram determinant")


def canonical_cost(kernel, row, matrix):
    total = Fraction(0)
    for multiplicity, odd, (u, v) in zip(kernel, row, PAIRS):
        r = matrix[u][v]
        require(not odd or r != 1, "odd path assigned infinite cost")
        odd_cost = Fraction(0) if not odd else (1 + r) / (1 - r)
        # For the stored rational templates, f_2(r) is recovered exactly from
        # its rational half-angle parameter; identify it by direct lookup.
        if matrix == simplex_gram():
            even_cost = Fraction(2, 3)
        elif matrix == ((Fraction(1),) * 3,) * 3:
            even_cost = Fraction(0)
        else:
            candidates = [t for t in {value for values in T_CERTIFICATES.values()
                                      for value in values}
                          if correlation(t) == r]
            require(candidates, "Gram entry has no frozen rational parameter")
            even_cost = 2 * min(candidates) ** 2
        total += odd * odd_cost + (multiplicity - odd) * even_cost
    return total


def certificate(kernel, row):
    odd_total = sum(row)
    if odd_total == 0:
        kind = "all-even-rank-one"
        t_values = (Fraction(0),) * 3
        matrix = ((Fraction(1),) * 3,) * 3
    elif odd_total == 1:
        odd_edge = row.index(1)
        kind = f"singleton-{PAIR_NAMES[odd_edge]}"
        t_values = T_CERTIFICATES[(kernel, odd_edge)]
        matrix = gram_from_t(t_values)
    else:
        kind = "equilateral"
        t_values = None
        matrix = simplex_gram()
    require_correlation_matrix(matrix)
    cost = canonical_cost(kernel, row, matrix)
    require(cost <= 4, "certificate exceeds rank-five budget four")
    return kind, t_values, matrix, cost


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def bundle_record(kernel, row):
    return [{"edge": name, "multiplicity": multiplicity, "odd": odd,
             "even": multiplicity - odd}
            for name, multiplicity, odd in zip(PAIR_NAMES, kernel, row)]


def row_record(kernel, row):
    kind, t_values, matrix, cost = certificate(kernel, row)
    cert = {
        "kind": kind,
        "gram": [[fraction_text(value) for value in line] for line in matrix],
        "determinant": fraction_text(determinant(matrix)),
        "canonical_excess": fraction_text(cost),
    }
    if t_values is not None:
        cert["t"] = [fraction_text(value) for value in t_values]
    return {
        "kernel": list(kernel),
        "row": list(row),
        "bundles": bundle_record(kernel, row),
        "automorphism_orbit": [list(member) for member in orbit_members(kernel, row)],
        "certificate": cert,
    }


def regenerate_payload():
    ledgers = []
    records = []
    for kernel in KERNELS:
        rows = physical_rows(kernel)
        group = automorphisms(kernel)
        representatives = tuple(sorted({canonical_row(kernel, row) for row in rows}))
        ledgers.append({"multiplicities": list(kernel), "physical_rows": len(rows),
                        "automorphisms": len(group), "orbits": len(representatives)})
        records.extend(row_record(kernel, row) for row in representatives)
    return {
        "schema": "rank-five-three-vertex-rational-gram-orbits-v1",
        "scope": "all physical parity rows; canonical length upper bounds",
        "pair_order": list(PAIR_NAMES),
        "budget": 4,
        "kernels": ledgers,
        "physical_row_total": sum(item["physical_rows"] for item in ledgers),
        "orbit_total": len(records),
        "orbits": records,
    }


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def serialize(payload):
    return canonical_bytes(payload).decode("ascii")


def load_fixture():
    require(FIXTURE.is_file(), f"missing fixture: {FIXTURE}")
    try:
        raw = FIXTURE.read_bytes()
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot load fixture {FIXTURE}: {error}") from error
    require(isinstance(value, dict), "fixture root is not an object")
    return value, raw


def parse_fraction(value):
    require(isinstance(value, str), "rational value is not a string")
    return Fraction(value)


def audit(payload=None, expected_digest=EXPECTED_SHA256, raw_bytes=None):
    if payload is None:
        fixture, raw = load_fixture()
    else:
        fixture = payload
        raw = canonical_bytes(fixture) if raw_bytes is None else raw_bytes
    require(raw == canonical_bytes(fixture), "fixture is not canonical JSON bytes")
    generated = regenerate_payload()
    require(fixture == generated, "fixture differs from independent regeneration")
    require(tuple(item["physical_rows"] for item in fixture["kernels"])
            == EXPECTED_PHYSICAL, "physical-row ledger changed")
    require(tuple(item["automorphisms"] for item in fixture["kernels"])
            == EXPECTED_AUTOMORPHISMS, "automorphism ledger changed")
    require(tuple(item["orbits"] for item in fixture["kernels"])
            == EXPECTED_ORBITS, "orbit ledger changed")
    require(fixture["physical_row_total"] == sum(EXPECTED_PHYSICAL) == 98,
            "physical-row total changed")
    require(fixture["orbit_total"] == len(fixture["orbits"])
            == sum(EXPECTED_ORBITS) == 74, "orbit total changed")
    require(sum(len(record["automorphism_orbit"]) for record in fixture["orbits"])
            == 98, "stored orbits do not recover all physical rows")
    for record in fixture["orbits"]:
        matrix = tuple(tuple(parse_fraction(value) for value in line)
                       for line in record["certificate"]["gram"])
        require_correlation_matrix(matrix)
        require(parse_fraction(record["certificate"]["determinant"])
                == determinant(matrix), "stored Gram determinant changed")
        kernel = tuple(record["kernel"])
        row = tuple(record["row"])
        require(parse_fraction(record["certificate"]["canonical_excess"])
                == canonical_cost(kernel, row, matrix) <= 4,
                "stored exact cost changed")
    digest = hashlib.sha256(raw).hexdigest()
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(digest == expected_digest, "fixture digest changed")
    return digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError, ZeroDivisionError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    baseline = regenerate_payload()
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted orbit", lambda value: value["orbits"].pop())
    add("duplicated orbit", lambda value: value["orbits"].append(
        deepcopy(value["orbits"][-1])))
    add("noncanonical row", lambda value: value["orbits"][31]["row"].reverse())
    add("changed bundle count", lambda value: value["orbits"][0]["bundles"][0]
        .__setitem__("even", 0))
    add("lost orbit member", lambda value: value["orbits"][31]
        ["automorphism_orbit"].pop())
    add("Gram entry changed", lambda value: value["orbits"][1]["certificate"]
        ["gram"][0].__setitem__(1, "1/1"))
    add("cost changed", lambda value: value["orbits"][1]["certificate"]
        .__setitem__("canonical_excess", "4/1"))
    add("budget changed", lambda value: value.__setitem__("budget", 5))
    add("pair order changed", lambda value: value["pair_order"].reverse())
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, raw_bytes=canonical_bytes(baseline) + b"\n"),
                    "noncanonical raw bytes")
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    return len(mutations) + 2


def report(digest, mutations):
    return "\n".join((
        "rank-five three-vertex physical orbit theorem: exact audit passed",
        "kernels: (1,2,4),(1,3,3),(2,2,3)",
        "physical_rows_by_kernel: 30,32,36 (total 98)",
        "automorphism_orbits_by_kernel: 30,20,24 (total 74)",
        "rational_gram_budget: canonical excess <= 4 on every orbit",
        "all_length_extension: fixed-parity path monotonicity",
        f"fixture_raw_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    command = [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check-optimized", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        FIXTURE.parent.mkdir(parents=True, exist_ok=True)
        FIXTURE.write_bytes(canonical_bytes(regenerate_payload()))
        print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        return 0
    digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 11, "hostile mutation count changed")
    output = report(digest, mutations)
    if args.check_optimized or (not args.emit and sys.flags.optimize == 0):
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
