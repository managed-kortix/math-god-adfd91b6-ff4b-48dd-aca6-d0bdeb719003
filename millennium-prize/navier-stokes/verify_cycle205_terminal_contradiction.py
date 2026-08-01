#!/usr/bin/env python3
"""Verify the corrected exact Cycle 205 reduced unit-ideal certificate."""

from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "cycle204_s2_equations.json"


LINEAR_IDS = {
    "e0042", "e0043", "e0068", "e0069", "e0084", "e0085",
    "e0090", "e0091", "e0092", "e0093", "e0094", "e0095",
    "e0096", "e0097", "e0101", "e0102", "e0103", "e0104",
    "e0105",
}
NONLINEAR_IDS = {"e0089", "e0436", "e0509"}


def polynomial(row):
    result = defaultdict(Fraction)
    for term in row["terms"]:
        result[tuple(sorted(term["monomial"]))] += Fraction(term["coefficient"])
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def evaluate(poly, values):
    result = Fraction(0)
    for monomial, coefficient in poly.items():
        term = coefficient
        for variable in monomial:
            term *= values[variable]
        result += term
    return result


def add(left, right):
    result = defaultdict(Fraction, left)
    for monomial, coefficient in right.items():
        result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def multiply(left, right):
    result = defaultdict(Fraction)
    for a, ca in left.items():
        for b, cb in right.items():
            result[tuple(sorted(a + b))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def substitute(poly, values):
    result = {}
    for monomial, coefficient in poly.items():
        term = {(): coefficient}
        for variable in monomial:
            term = multiply(term, values[variable])
        result = add(result, term)
    return result


def matrix_rank(matrix):
    reduced = [row[:] for row in matrix]
    target = 0
    for column in range(len(reduced[0])):
        source = next((row for row in range(target, len(reduced)) if reduced[row][column]), None)
        if source is None:
            continue
        reduced[target], reduced[source] = reduced[source], reduced[target]
        pivot = reduced[target][column]
        reduced[target] = [value / pivot for value in reduced[target]]
        for row in range(len(reduced)):
            if row != target and reduced[row][column]:
                factor = reduced[row][column]
                reduced[row] = [a - factor * b for a, b in zip(reduced[row], reduced[target])]
        target += 1
        if target == len(reduced):
            break
    return target


def main():
    data = json.loads(DATA.read_text())
    rows = {row["id"]: row for row in data["equations"]}
    selected = LINEAR_IDS | NONLINEAR_IDS
    assert selected <= rows.keys()
    assert all(rows[equation_id]["degree"] == 1 for equation_id in LINEAR_IDS)
    names = data["active_variables"]
    linear_matrix = [
        [polynomial(rows[equation_id]).get((name,), Fraction(0)) for name in names]
        for equation_id in sorted(LINEAR_IDS)
    ]
    assert matrix_rank(linear_matrix) == 19

    zero_variables = {
        "q1_o0_planar_re", "q1_o0_planar_im",
        "q1_o2_planar_re", "q1_o2_planar_im",
        "q1_o4_planar_re", "q1_o4_planar_im",
        "q1_o5_planar_re", "q1_o5_planar_im",
        "q1_o6_planar_re", "q1_o6_planar_im",
        "q1_o8_planar_re", "q1_o8_planar_im",
    }

    zero = {}
    values = {name: {(name,): Fraction(1)} for name in names}
    values.update({name: zero for name in zero_variables})
    values.update({
        "q1_o9_planar_im": {("a",): Fraction(1)},
        "q1_o10_planar_im": {("b",): Fraction(1)},
        "q1_o10_planar_re": {("c",): Fraction(1)},
        "q1_o9_planar_re": {("c",): Fraction(1, 2)},
        "q1_o4_vertical_re": {("c",): Fraction(-1, 2)},
        "q1_o4_vertical_im": {("a",): Fraction(-1)},
        "q1_o5_vertical_re": zero,
        "q1_o5_vertical_im": {("a",): Fraction(2), ("b",): Fraction(-1)},
        "q1_o6_vertical_re": {("c",): Fraction(1, 2)},
        "q1_o6_vertical_im": {("a",): Fraction(-1)},
    })
    assert all(not substitute(polynomial(rows[equation_id]), values) for equation_id in LINEAR_IDS)
    a2 = {("a", "a"): Fraction(1)}
    ab = {("a", "b"): Fraction(1)}
    c2 = {("c", "c"): Fraction(1)}
    reduced = {
        equation_id: substitute(polynomial(rows[equation_id]), values)
        for equation_id in NONLINEAR_IDS
    }
    assert reduced["e0089"] == add({m: -v for m, v in a2.items()}, {m: v / 4 for m, v in c2.items()})
    assert reduced["e0436"] == add(
        {(): Fraction(242905)},
        add({m: -242905 * v for m, v in a2.items()}, add(
            {m: 485810 * v for m, v in ab.items()},
            {m: Fraction(-728715, 4) * v for m, v in c2.items()},
        )),
    )
    q = add({m: 2 * v for m, v in a2.items()}, add(
        {m: -2 * v for m, v in ab.items()},
        {m: v / 2 for m, v in c2.items()},
    ))
    assert reduced["e0509"] == q
    assert substitute(polynomial(rows["e0513"]), values) == q
    total = add(reduced["e0089"], add(
        {m: v / 242905 for m, v in reduced["e0436"].items()},
        reduced["e0509"],
    ))
    assert total == {(): Fraction(1)}

    print("Cycle 205 corrected exact contradiction verified")
    print("linear closure equations: 19")
    print("terminal equations e0509 and e0513 both reduce to Q = 0")
    print("nonlinear equations: e0089, e0436, e0509")
    print("certificate: e0089 + e0436/242905 + e0509 = 1 after substitution")


if __name__ == "__main__":
    main()
