#!/usr/bin/env python3
"""Build and verify an exact Cycle 205 Nullstellensatz certificate."""

from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EQUATIONS = ROOT / "cycle204_s2_equations.json"


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def add(left, right):
    result = defaultdict(Fraction, left)
    for monomial, coefficient in right.items():
        result[monomial] += coefficient
    return clean(result)


def scale(poly, coefficient):
    return clean({monomial: coefficient * value for monomial, value in poly.items()})


def multiply(left, right):
    result = defaultdict(Fraction)
    for a, ca in left.items():
        for b, cb in right.items():
            result[tuple(sorted(a + b))] += ca * cb
    return clean(result)


def load_system():
    data = json.loads(EQUATIONS.read_text())
    names = data["active_variables"]
    indices = {name: index for index, name in enumerate(names)}
    equations = {}
    degrees = {}
    for raw in data["equations"]:
        poly = defaultdict(Fraction)
        for term in raw["terms"]:
            monomial = tuple(sorted(indices[name] for name in term["monomial"]))
            poly[monomial] += Fraction(term["coefficient"])
        equations[raw["id"]] = clean(poly)
        degrees[raw["id"]] = raw["degree"]
    return data, names, equations, degrees


def rref_linear(equations, degrees, variable_count):
    ids = [equation_id for equation_id in equations if degrees[equation_id] == 1]
    rows = []
    provenance = []
    for equation_id in ids:
        row = [equations[equation_id].get((index,), Fraction(0)) for index in range(variable_count)]
        rows.append(row)
        provenance.append({equation_id: Fraction(1)})

    pivots = []
    pivot_row = 0
    for column in range(variable_count):
        selected = next((index for index in range(pivot_row, len(rows)) if rows[index][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        provenance[pivot_row], provenance[selected] = provenance[selected], provenance[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [value / divisor for value in rows[pivot_row]]
        provenance[pivot_row] = scale(provenance[pivot_row], Fraction(1, 1) / divisor)
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [a - factor * b for a, b in zip(rows[index], rows[pivot_row])]
            provenance[index] = add(provenance[index], scale(provenance[pivot_row], -factor))
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    relations = {}
    for index, pivot in enumerate(pivots):
        substitution = {
            (column,): -rows[index][column]
            for column in range(variable_count)
            if column != pivot and rows[index][column]
        }
        relations[pivot] = (substitution, provenance[index])
    return relations


def reduce_with_relations(poly, relations):
    result = dict(poly)
    quotients = {pivot: {} for pivot in relations}
    while True:
        selected = None
        for monomial in sorted(result):
            pivot = next((variable for variable in monomial if variable in relations), None)
            if pivot is not None:
                selected = monomial, pivot
                break
        if selected is None:
            break
        monomial, pivot = selected
        coefficient = result.pop(monomial)
        rest = list(monomial)
        rest.remove(pivot)
        rest_poly = {tuple(rest): coefficient}
        substitution = relations[pivot][0]
        result = add(result, multiply(rest_poly, substitution))
        quotients[pivot] = add(quotients[pivot], rest_poly)
    return result, quotients


def build_certificate(equations, degrees, variable_count):
    relations = rref_linear(equations, degrees, variable_count)
    target_weights = {
        "e0089": Fraction(1),
        "e0436": Fraction(1, 242905),
        "e0509": Fraction(1),
    }
    reductions = {}
    quotient_sums = {pivot: {} for pivot in relations}
    for equation_id, weight in target_weights.items():
        reduced, quotients = reduce_with_relations(equations[equation_id], relations)
        reductions[equation_id] = reduced
        for pivot, quotient in quotients.items():
            quotient_sums[pivot] = add(quotient_sums[pivot], scale(quotient, weight))

    certificate = {equation_id: {(): weight} for equation_id, weight in target_weights.items()}
    for pivot, quotient in quotient_sums.items():
        for equation_id, coefficient in relations[pivot][1].items():
            certificate[equation_id] = add(
                certificate.get(equation_id, {}), scale(quotient, -coefficient)
            )
    certificate = {equation_id: multiplier for equation_id, multiplier in certificate.items() if multiplier}
    return relations, reductions, certificate


def verify_certificate(equations, certificate):
    total = {}
    for equation_id, multiplier in certificate.items():
        total = add(total, multiply(multiplier, equations[equation_id]))
    assert total == {(): Fraction(1)}
    return total


def reduce_mod_prime(poly, prime):
    result = {}
    for monomial, coefficient in poly.items():
        assert coefficient.denominator % prime
        value = coefficient.numerator * pow(coefficient.denominator, -1, prime) % prime
        if value:
            result[monomial] = value
    return result


def build_modular_certificate(equations, degrees, variable_count, prime):
    def madd(left, right):
        result = defaultdict(int, left)
        for monomial, coefficient in right.items():
            result[monomial] = (result[monomial] + coefficient) % prime
        return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}

    def mscale(poly, coefficient):
        return {
            monomial: coefficient * value % prime
            for monomial, value in poly.items()
            if coefficient * value % prime
        }

    def mmultiply(left, right):
        result = defaultdict(int)
        for a, ca in left.items():
            for b, cb in right.items():
                monomial = tuple(sorted(a + b))
                result[monomial] = (result[monomial] + ca * cb) % prime
        return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}

    modular = {equation_id: reduce_mod_prime(poly, prime) for equation_id, poly in equations.items()}
    rows = []
    provenance = []
    for equation_id in equations:
        if degrees[equation_id] != 1:
            continue
        rows.append([modular[equation_id].get((index,), 0) for index in range(variable_count)])
        provenance.append({equation_id: 1})

    relations = {}
    pivot_row = 0
    for column in range(variable_count):
        selected = next((index for index in range(pivot_row, len(rows)) if rows[index][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        provenance[pivot_row], provenance[selected] = provenance[selected], provenance[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime for value in rows[pivot_row]]
        provenance[pivot_row] = mscale(provenance[pivot_row], inverse)
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                (a - factor * b) % prime for a, b in zip(rows[index], rows[pivot_row])
            ]
            provenance[index] = madd(provenance[index], mscale(provenance[pivot_row], -factor))
        relations[column] = (
            {
                (index,): -rows[pivot_row][index] % prime
                for index in range(variable_count)
                if index != column and rows[pivot_row][index]
            },
            provenance[pivot_row],
        )
        pivot_row += 1

    def reduce_poly(poly):
        result = dict(poly)
        quotients = {pivot: {} for pivot in relations}
        while True:
            selected = None
            for monomial in sorted(result):
                pivot = next((variable for variable in monomial if variable in relations), None)
                if pivot is not None:
                    selected = monomial, pivot
                    break
            if selected is None:
                return result, quotients
            monomial, pivot = selected
            coefficient = result.pop(monomial)
            rest = list(monomial)
            rest.remove(pivot)
            rest_poly = {tuple(rest): coefficient}
            result = madd(result, mmultiply(rest_poly, relations[pivot][0]))
            quotients[pivot] = madd(quotients[pivot], rest_poly)

    reductions = {}
    quotient_sums = {pivot: {} for pivot in relations}
    inverse = pow(242905, -1, prime)
    target_weights = {"e0089": 1, "e0436": inverse, "e0509": 1}
    certificate = {equation_id: {(): weight} for equation_id, weight in target_weights.items()}
    for equation_id, weight in target_weights.items():
        reductions[equation_id], quotients = reduce_poly(modular[equation_id])
        for pivot, quotient in quotients.items():
            quotient_sums[pivot] = madd(quotient_sums[pivot], mscale(quotient, weight))
    for pivot, quotient in quotient_sums.items():
        for equation_id, coefficient in relations[pivot][1].items():
            certificate[equation_id] = madd(
                certificate.get(equation_id, {}), mscale(quotient, -coefficient)
            )
    total = {}
    for equation_id, multiplier in certificate.items():
        total = madd(total, mmultiply(multiplier, modular[equation_id]))
    return len(relations), reductions, total


def main():
    data, names, equations, degrees = load_system()
    assert len(equations) == 514
    relations, reductions, certificate = build_certificate(equations, degrees, len(names))
    total = verify_certificate(equations, certificate)
    mod3_rank, mod3_reductions, mod3_total = build_modular_certificate(
        equations, degrees, len(names), 3
    )
    used = sorted(certificate)
    print("Cycle 205 exact infeasibility certificate")
    print("loaded equations:", len(equations))
    print("linear rank:", len(relations))
    print("remaining variables after linear elimination:", len(names) - len(relations))
    print("reduced e0089:", reductions["e0089"])
    print("reduced e0436:", reductions["e0436"])
    print("reduced e0509:", reductions["e0509"])
    print("certificate equations used:", len(used))
    print("certificate identity: sum(h_j * e_j) =", total[()])
    print("mod 3 linear rank:", mod3_rank)
    print("mod 3 certificate identity:", mod3_total)
    assert mod3_rank == 27 and mod3_total == {(): 1}
    print("conclusion: no solution over Q, R, or C")
    assert data["simplification"]["primitive_equations"] == 514


if __name__ == "__main__":
    main()
