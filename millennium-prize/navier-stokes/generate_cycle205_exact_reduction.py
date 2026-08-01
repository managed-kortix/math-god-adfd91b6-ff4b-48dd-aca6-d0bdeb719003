#!/usr/bin/env python3
"""Exactly eliminate the Cycle 204 linear equations and reduce the rest."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_PATH = ROOT / "cycle204_s2_equations.json"
OUTPUT_PATH = ROOT / "cycle205_exact_reduction.json"


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_bytes(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("ascii")


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sparse_vector(row, names=None):
    result = []
    for index, value in enumerate(row):
        if value:
            entry = {"coefficient": fraction_text(value)}
            entry["variable" if names is not None else "index"] = names[index] if names is not None else index
            result.append(entry)
    return result


def parse_linear_system(data):
    variables = data["active_variables"]
    indices = {name: index for index, name in enumerate(variables)}
    equations = [row for row in data["equations"] if row["degree"] <= 1]
    matrix = []
    for equation in equations:
        row = [Fraction(0) for _ in range(len(variables) + 1)]
        for term in equation["terms"]:
            coefficient = Fraction(term["coefficient"])
            monomial = term["monomial"]
            if monomial:
                assert len(monomial) == 1
                row[indices[monomial[0]]] += coefficient
            else:
                row[-1] -= coefficient
        matrix.append(row)
    return variables, equations, matrix


def exact_rref(matrix):
    row_count = len(matrix)
    column_count = len(matrix[0]) - 1
    reduced = [row[:] for row in matrix]
    transform = [
        [Fraction(index == other) for other in range(row_count)]
        for index in range(row_count)
    ]
    pivots = []
    target = 0
    for column in range(column_count):
        source = next((row for row in range(target, row_count) if reduced[row][column]), None)
        if source is None:
            continue
        reduced[target], reduced[source] = reduced[source], reduced[target]
        transform[target], transform[source] = transform[source], transform[target]
        pivot = reduced[target][column]
        reduced[target] = [value / pivot for value in reduced[target]]
        transform[target] = [value / pivot for value in transform[target]]
        for row in range(row_count):
            if row == target or not reduced[row][column]:
                continue
            multiplier = reduced[row][column]
            reduced[row] = [a - multiplier * b for a, b in zip(reduced[row], reduced[target])]
            transform[row] = [a - multiplier * b for a, b in zip(transform[row], transform[target])]
        pivots.append(column)
        target += 1
        if target == row_count:
            break
    return reduced, transform, pivots


def multiply_polynomials(left, right):
    result = defaultdict(Fraction)
    for monomial_a, coefficient_a in left.items():
        for monomial_b, coefficient_b in right.items():
            result[tuple(sorted(monomial_a + monomial_b))] += coefficient_a * coefficient_b
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def substitute_equation(equation, substitutions):
    result = defaultdict(Fraction)
    for term in equation["terms"]:
        product = {(): Fraction(term["coefficient"])}
        for variable in term["monomial"]:
            product = multiply_polynomials(product, substitutions[variable])
        for monomial, coefficient in product.items():
            result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def primitive_polynomial(polynomial):
    if not polynomial:
        return ()
    denominator = 1
    for coefficient in polynomial.values():
        denominator = math.lcm(denominator, coefficient.denominator)
    integers = {monomial: int(coefficient * denominator) for monomial, coefficient in polynomial.items()}
    divisor = 0
    for coefficient in integers.values():
        divisor = math.gcd(divisor, abs(coefficient))
    integers = {monomial: coefficient // divisor for monomial, coefficient in integers.items()}
    leading = min(integers)
    if integers[leading] < 0:
        integers = {monomial: -coefficient for monomial, coefficient in integers.items()}
    return tuple(sorted(integers.items()))


def linear_span_contradiction(equations):
    nonconstant_monomials = sorted({
        tuple(term["monomial"])
        for equation in equations
        for term in equation["terms"]
        if term["monomial"]
    })
    monomial_index = {monomial: index for index, monomial in enumerate(nonconstant_monomials)}
    matrix = []
    for equation in equations:
        row = [Fraction(0) for _ in range(len(nonconstant_monomials) + 1)]
        for term in equation["terms"]:
            coefficient = Fraction(term["coefficient"])
            monomial = tuple(term["monomial"])
            if monomial:
                row[monomial_index[monomial]] += coefficient
            else:
                row[-1] -= coefficient
        matrix.append(row)
    reduced, transform, _ = exact_rref(matrix)
    contradiction_row = next((
        index for index, row in enumerate(reduced)
        if not any(row[:-1]) and row[-1]
    ), None)
    if contradiction_row is None:
        return None
    scale = -reduced[contradiction_row][-1]
    combination = [value / scale for value in transform[contradiction_row]]
    return {
        "identity": "the listed rational linear combination of reduced equation polynomials equals 1",
        "combination": [
            {"equation_id": equations[index]["id"], "coefficient": fraction_text(value)}
            for index, value in enumerate(combination) if value
        ],
    }


def make_reduction(data, input_bytes):
    variables, linear_equations, matrix = parse_linear_system(data)
    reduced, transform, pivots = exact_rref(matrix)
    rank = len(pivots)
    inconsistent_rows = [
        index for index, row in enumerate(reduced)
        if not any(row[:-1]) and row[-1]
    ]

    linear_certificate = {
        "equation_ids": [row["id"] for row in linear_equations],
        "matrix_shape": [len(matrix), len(variables)],
        "rank": rank,
        "pivot_columns": pivots,
        "pivot_variables": [variables[index] for index in pivots],
        "inconsistent_rows": inconsistent_rows,
        "rref_augmented_rows": [sparse_vector(row, variables + ["__rhs__"]) for row in reduced],
        "left_transform_rows": [sparse_vector(row) for row in transform],
        "certificate_identity": "left_transform * input_augmented_matrix = rref_augmented; left_transform is invertible",
    }
    if inconsistent_rows:
        return {
            "schema": "cycle205-exact-reduction-v1",
            "source_file": INPUT_PATH.name,
            "source_sha256": digest_bytes(input_bytes),
            "variable_order": variables,
            "linear_certificate": linear_certificate,
            "outcome": "contradiction",
        }

    free_columns = [index for index in range(len(variables)) if index not in pivots]
    parameters = [f"t{index}" for index in range(len(free_columns))]
    substitutions = {}
    parameterization = []
    pivot_row = {column: row for row, column in enumerate(pivots)}
    for column, variable in enumerate(variables):
        polynomial = defaultdict(Fraction)
        if column in free_columns:
            polynomial[(parameters[free_columns.index(column)],)] = Fraction(1)
        else:
            row = reduced[pivot_row[column]]
            polynomial[()] = row[-1]
            for free_index, parameter in zip(free_columns, parameters):
                polynomial[(parameter,)] = -row[free_index]
        substitutions[variable] = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
        parameterization.append({
            "variable": variable,
            "constant": fraction_text(polynomial.get((), Fraction(0))),
            "terms": [
                {"parameter": monomial[0], "coefficient": fraction_text(coefficient)}
                for monomial, coefficient in sorted(polynomial.items()) if monomial and coefficient
            ],
        })

    reduced_equations = []
    seen = {}
    zero_ids = []
    contradiction_ids = []
    for equation in data["equations"]:
        polynomial = substitute_equation(equation, substitutions)
        primitive = primitive_polynomial(polynomial)
        if not primitive:
            zero_ids.append(equation["id"])
            continue
        if max(map(len, (monomial for monomial, _ in primitive)), default=0) == 0:
            contradiction_ids.append(equation["id"])
        if primitive in seen:
            seen[primitive]["source_equation_ids"].append(equation["id"])
            continue
        row = {
            "id": f"r{len(reduced_equations):04d}",
            "degree": max(len(monomial) for monomial, _ in primitive),
            "source_equation_ids": [equation["id"]],
            "terms": [
                {"coefficient": str(coefficient), "monomial": list(monomial)}
                for monomial, coefficient in primitive
            ],
        }
        reduced_equations.append(row)
        seen[primitive] = row

    degree_counts = defaultdict(int)
    for equation in reduced_equations:
        degree_counts[str(equation["degree"])] += 1
    nonlinear_contradiction = linear_span_contradiction(reduced_equations)
    result = {
        "schema": "cycle205-exact-reduction-v1",
        "source_file": INPUT_PATH.name,
        "source_sha256": digest_bytes(input_bytes),
        "coefficient_domain": "Q for RREF and affine substitution; primitive reduced equations over Z",
        "variable_order": variables,
        "linear_certificate": linear_certificate,
        "outcome": "contradiction_after_affine_substitution" if nonlinear_contradiction else "reduced_nonlinear_system",
        "parameters": parameters,
        "affine_dimension": len(parameters),
        "free_variables": [variables[index] for index in free_columns],
        "parameterization": parameterization,
        "reduction": {
            "input_equations": len(data["equations"]),
            "identically_zero_after_substitution": len(zero_ids),
            "zero_source_equation_ids": zero_ids,
            "duplicate_nonzero_after_substitution": sum(len(row["source_equation_ids"]) - 1 for row in reduced_equations),
            "reduced_equations": len(reduced_equations),
            "degree_counts": dict(sorted(degree_counts.items())),
            "constant_contradiction_source_ids": contradiction_ids,
        },
        "equations": reduced_equations,
    }
    if nonlinear_contradiction:
        result["contradiction_certificate"] = nonlinear_contradiction
    return result


def generate():
    input_bytes = INPUT_PATH.read_bytes()
    data = json.loads(input_bytes)
    result = make_reduction(data, input_bytes)
    result["sha256_without_this_field"] = digest_bytes(canonical_bytes(result))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare regenerated bytes with the committed reduction")
    args = parser.parse_args()
    result = generate()
    output = canonical_bytes(result)
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_bytes() != output:
            raise SystemExit(f"replay mismatch: {OUTPUT_PATH}")
        print("Cycle 205 exact reduction replay matches committed JSON")
    else:
        OUTPUT_PATH.write_bytes(output)
        print("Cycle 205 exact linear reduction")
        print("linear rank:", result["linear_certificate"]["rank"])
        print("free parameters:", len(result.get("parameters", [])))
        reduction = result.get("reduction", {})
        print("reduced equations:", reduction.get("reduced_equations"), reduction.get("degree_counts"))
        print("outcome:", result["outcome"])
        print("wrote", OUTPUT_PATH.name)


if __name__ == "__main__":
    main()
