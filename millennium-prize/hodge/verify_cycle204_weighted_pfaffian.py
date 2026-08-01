#!/usr/bin/env python3
"""Dependency-free exact checks for the weighted 5 x 5 Pfaffian scout."""

from fractions import Fraction
from itertools import product


def polynomial_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def linear_cube(linear):
    out = {}
    for i, j, k in product(range(len(linear)), repeat=3):
        monomial = [0] * len(linear)
        monomial[i] += 1
        monomial[j] += 1
        monomial[k] += 1
        key = tuple(monomial)
        out[key] = out.get(key, Fraction(0)) + linear[i] * linear[j] * linear[k]
    return out


def scale(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items()}


def center_cubic(classes):
    dimension = len(classes[0])
    total = tuple(sum(row[j] for row in classes) // 2 for j in range(dimension))
    assert all(2 * total[j] == sum(row[j] for row in classes) for j in range(dimension))
    numerator = linear_cube(total)
    for row in classes:
        numerator = polynomial_add(numerator, linear_cube(row))
        complement = tuple(total[j] - row[j] for j in range(dimension))
        numerator = polynomial_add(numerator, scale(linear_cube(complement), -1))
    return scale(numerator, Fraction(1, 6))


def scalar_coefficient(weights):
    total = sum(weights) // 2
    assert 2 * total == sum(weights)
    numerator = (
        sum(weight**3 for weight in weights)
        - sum((total - weight) ** 3 for weight in weights)
        + total**3
    )
    assert numerator % 6 == 0
    return numerator // 6


def scalar_search(limit, strict):
    answers = []
    best_sum = None
    for weights in product(range(1, limit + 1), repeat=5):
        if tuple(sorted(weights)) != weights or sum(weights) % 2:
            continue
        total = sum(weights) // 2
        entry_degrees = [
            total - weights[i] - weights[j]
            for i in range(5)
            for j in range(i + 1, 5)
        ]
        if min(entry_degrees) < strict:
            continue
        weight_sum = sum(weights)
        if best_sum is None or weight_sum < best_sum:
            best_sum = weight_sum
            answers = [(weights, total, scalar_coefficient(weights), entry_degrees)]
        elif weight_sum == best_sum:
            answers.append((weights, total, scalar_coefficient(weights), entry_degrees))
    return answers


def coordinate_patterns(max_sum):
    patterns = []
    for weights in product(range(max_sum + 1), repeat=5):
        weight_sum = sum(weights)
        if not weight_sum or weight_sum > max_sum or weight_sum % 2:
            continue
        total = weight_sum // 2
        if all(
            total - weights[i] - weights[j] >= 0
            for i in range(5)
            for j in range(i + 1, 5)
        ):
            patterns.append((weight_sum, weights, total))
    return patterns


def smallest_xyz_coefficient(target, max_total):
    patterns = coordinate_patterns(max_total)
    best = None
    witness = None
    for x_data, y_data, z_data in product(patterns, repeat=3):
        vector_total = x_data[0] + y_data[0] + z_data[0]
        if vector_total > max_total or (best is not None and vector_total >= best):
            continue
        directions = (x_data[1], y_data[1], z_data[1])
        totals = (x_data[2], y_data[2], z_data[2])
        if any(sum(direction[i] for direction in directions) == 0 for i in range(5)):
            continue
        if any(
            sum(totals[k] - directions[k][i] - directions[k][j] for k in range(3)) == 0
            for i in range(5)
            for j in range(i + 1, 5)
        ):
            continue
        xyz = (
            sum(directions[0][i] * directions[1][i] * directions[2][i] for i in range(5))
            - sum(
                (totals[0] - directions[0][i])
                * (totals[1] - directions[1][i])
                * (totals[2] - directions[2][i])
                for i in range(5)
            )
            + totals[0] * totals[1] * totals[2]
        )
        if xyz == target:
            best = vector_total
            witness = directions
    return best, witness


def main():
    # X, Y, Z, H and X+Y+Z-H give C(N)=XYZ.
    formal = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 1, 1, -1),
    )
    assert center_cubic(formal) == {(1, 1, 1, 0): Fraction(1)}

    weak = scalar_search(10, strict=0)
    positive = scalar_search(10, strict=1)
    assert len(weak) == 1
    assert weak[0][0:3] == ((1, 1, 1, 1, 2), 3, 1)
    assert weak[0][3].count(0) == 4
    assert len(positive) == 1
    assert positive[0][0:3] == ((2, 2, 2, 2, 2), 5, 5)

    near_miss = (
        (0, 1, 1),
        (1, 0, 2),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
    )
    expected = {
        (2, 1, 0): Fraction(1),
        (2, 0, 1): Fraction(1),
        (1, 2, 0): Fraction(1),
        (1, 1, 1): Fraction(3),
        (1, 0, 2): Fraction(2),
        (0, 2, 1): Fraction(2),
        (0, 1, 2): Fraction(2),
        (0, 0, 3): Fraction(1),
    }
    assert center_cubic(near_miss) == expected
    smallest_total, coordinate_witness = smallest_xyz_coefficient(3, 14)
    assert smallest_total == 14
    assert coordinate_witness is not None

    print("formal weighted identity: C(X,Y,Z,H,X+Y+Z-H) = XYZ")
    print("smallest weak scalar weights:", weak[0][0], "coefficient", weak[0][2])
    print("zero entry degrees in weak minimum:", weak[0][3].count(0))
    print("smallest positive scalar weights:", positive[0][0], "coefficient", positive[0][2])
    print("three-direction near-miss XYZ coefficient:", expected[(1, 1, 1)])
    print("smallest effective coordinate-vector total for coefficient 3:", smallest_total)
    print("all Cycle 204 exact checks passed")


if __name__ == "__main__":
    main()
