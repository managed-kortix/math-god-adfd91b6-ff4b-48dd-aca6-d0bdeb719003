#!/usr/bin/env python3
"""Search the Cycle 204 system for small exact contradiction certificates."""

from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EQUATIONS = ROOT / "cycle204_s2_equations.json"


def add(left, right):
    out = defaultdict(Fraction, left)
    for monomial, coefficient in right.items():
        out[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def multiply(left, right):
    out = defaultdict(Fraction)
    for a, ca in left.items():
        for b, cb in right.items():
            out[tuple(sorted(a + b))] += ca * cb
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def scale(poly, coefficient):
    return {monomial: coefficient * value for monomial, value in poly.items() if coefficient * value}


def normalize(poly):
    if not poly:
        return ()
    denominator = 1
    from math import gcd, lcm
    for coefficient in poly.values():
        denominator = lcm(denominator, coefficient.denominator)
    integers = {monomial: int(coefficient * denominator) for monomial, coefficient in poly.items()}
    content = 0
    for coefficient in integers.values():
        content = gcd(content, abs(coefficient))
    integers = {monomial: coefficient // content for monomial, coefficient in integers.items()}
    first = min(integers)
    if integers[first] < 0:
        integers = {monomial: -coefficient for monomial, coefficient in integers.items()}
    return tuple(sorted(integers.items()))


def linear_elimination(equations, variable_count):
    rows = []
    row_ids = []
    for equation in equations:
        if equation["degree"] != 1:
            continue
        row = [Fraction(0) for _ in range(variable_count)]
        for monomial, coefficient in equation["poly"].items():
            assert len(monomial) == 1
            row[monomial[0]] += coefficient
        rows.append(row)
        row_ids.append({equation["id"]})

    pivot_columns = []
    pivot_row = 0
    for column in range(variable_count):
        selected = next((index for index in range(pivot_row, len(rows)) if rows[index][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        row_ids[pivot_row], row_ids[selected] = row_ids[selected], row_ids[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [value / divisor for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [a - factor * b for a, b in zip(rows[index], rows[pivot_row])]
            row_ids[index] |= row_ids[pivot_row]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    substitutions = {}
    witnesses = {}
    for index, column in enumerate(pivot_columns):
        substitutions[column] = {
            (other,): -rows[index][other]
            for other in range(variable_count)
            if other != column and rows[index][other]
        }
        witnesses[column] = row_ids[index]
    return substitutions, witnesses


def substitute(poly, substitutions):
    result = {}
    for monomial, coefficient in poly.items():
        term = {(): coefficient}
        for variable in monomial:
            term = multiply(term, substitutions.get(variable, {(variable,): Fraction(1)}))
        result = add(result, term)
    return result


def format_poly(poly, names):
    pieces = []
    for monomial, coefficient in sorted(poly.items()):
        body = "*".join(names[index] for index in monomial) or "1"
        sign = "+" if coefficient > 0 else ""
        pieces.append(f"{sign}{coefficient}*{body}")
    return " ".join(pieces).lstrip("+")


def main():
    data = json.loads(EQUATIONS.read_text())
    active_names = data["active_variables"]
    name_to_index = {name: index for index, name in enumerate(active_names)}
    equations = []
    for raw in data["equations"]:
        poly = defaultdict(Fraction)
        for term in raw["terms"]:
            monomial = tuple(sorted(name_to_index[name] for name in term["monomial"]))
            poly[monomial] += Fraction(term["coefficient"])
        equations.append({**raw, "poly": dict(poly)})

    substitutions, witnesses = linear_elimination(equations, len(active_names))
    print("linear rank", len(substitutions), "free variables", len(active_names) - len(substitutions))
    for variable, expression in substitutions.items():
        print(active_names[variable], "=", format_poly(expression, active_names) or "0", sorted(witnesses[variable]))

    reduced = []
    seen = {}
    for equation in equations:
        if equation["degree"] == 1:
            continue
        poly = substitute(equation["poly"], substitutions)
        primitive = normalize(poly)
        if not primitive:
            continue
        if primitive not in seen:
            seen[primitive] = {"poly": poly, "ids": []}
            reduced.append(seen[primitive])
        seen[primitive]["ids"].append(equation["id"])
    print("reduced distinct nonlinear equations", len(reduced))
    counts = defaultdict(int)
    for row in reduced:
        counts[len(row["poly"])] += 1
    print("term-count histogram", dict(sorted(counts.items())))
    print("all reduced equations; small ones appear first")
    reduced.sort(key=lambda row: (len(row["poly"]), row["ids"]))
    for row in reduced:
        print(",".join(row["ids"]), ":", format_poly(row["poly"], active_names))


if __name__ == "__main__":
    main()
