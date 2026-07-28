#!/usr/bin/env python3
"""Exact Cycle 70 check for one selected Fermat-quartic plane branch.

This is a finite-dimensional algebra calculation, not a Hodge-conjecture
solution.  For the Fermat quartic fourfold, the Jacobian ring is

    R = Q[x0, ..., x5] / (x0^3, ..., x5^3).

A plane obtained by pairing the coordinates uses a nonzero root ``a`` with
``a^4 = -1``.  Its residue polynomial is, up to a nonzero scalar, the product
of ``x^2 + a*x*y + a^2*y^2`` over the three pairs.  Diagonal conjugacy
``y -> a*y`` preserves ranks and changes each factor to ``x^2 + x*y + y^2``.
The verifier therefore works over Q with all root-scaled coefficients set to
one; it does not numerically choose or approximate a root.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable, Sequence


Exponent = tuple[int, ...]
Matrix = list[list[int]]
COORDINATE_PAIRS = ((0, 1), (2, 3), (4, 5))


def bounded_monomials(variable_count: int, degree: int, cap: int) -> tuple[Exponent, ...]:
    """Return the degree part of Q[x_1,...,x_n]/(x_i^(cap+1))."""
    if variable_count <= 0 or degree < 0 or cap < 0:
        raise ValueError("variable_count must be positive; degree and cap nonnegative")
    return tuple(
        exponent
        for exponent in product(range(cap + 1), repeat=variable_count)
        if sum(exponent) == degree
    )


def polynomial_product(
    left: dict[Exponent, int], right: dict[Exponent, int]
) -> dict[Exponent, int]:
    result: dict[Exponent, int] = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exponent, right_exponent))
            result[exponent] = result.get(exponent, 0) + left_coefficient * right_coefficient
    return result


def normalized_plane_class() -> dict[Exponent, int]:
    """Return product (x_2i^2 + x_2i*x_(2i+1) + x_(2i+1)^2)."""
    result = {(0,) * 6: 1}
    for first, second in COORDINATE_PAIRS:
        factor: dict[Exponent, int] = {}
        for first_power, second_power in ((2, 0), (1, 1), (0, 2)):
            exponent = [0] * 6
            exponent[first] = first_power
            exponent[second] = second_power
            factor[tuple(exponent)] = 1
        result = polynomial_product(result, factor)
    return result


def jacobian_multiplication_matrix() -> tuple[Matrix, tuple[Exponent, ...], tuple[Exponent, ...]]:
    """Matrix of multiplication by the normalized plane class, R4 -> R10."""
    source = bounded_monomials(6, 4, 2)
    target = bounded_monomials(6, 10, 2)
    target_rows = {monomial: row for row, monomial in enumerate(target)}
    matrix = [[0 for _ in source] for _ in target]

    for column, source_monomial in enumerate(source):
        for class_monomial, coefficient in normalized_plane_class().items():
            output = tuple(a + b for a, b in zip(source_monomial, class_monomial))
            if max(output) <= 2:
                matrix[target_rows[output]][column] += coefficient
    return matrix, source, target


def incidence_monomial_matrix() -> tuple[Matrix, tuple[Exponent, ...]]:
    """Matrix H0(O_P(1))^3 -> H0(O_P(4)), (l_i) -> sum l_i*u_i^3."""
    target = bounded_monomials(3, 4, 4)
    target_rows = {monomial: row for row, monomial in enumerate(target)}
    matrix = [[0 for _ in range(9)] for _ in target]
    for cubic_variable in range(3):
        for linear_variable in range(3):
            exponent = [0] * 3
            exponent[cubic_variable] = 3
            exponent[linear_variable] += 1
            matrix[target_rows[tuple(exponent)]][3 * cubic_variable + linear_variable] = 1
    return matrix, target


def exact_rank(rows: Iterable[Sequence[int]]) -> int:
    """Compute matrix rank over Q by exact Gauss-Jordan elimination."""
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("matrix rows have unequal lengths")

    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


@dataclass(frozen=True)
class Verification:
    r4_dimension: int
    r10_dimension: int
    jacobian_multiplication_rank: int
    incidence_target_dimension: int
    incidence_monomial_rank: int


def verify() -> Verification:
    multiplication, r4_basis, r10_basis = jacobian_multiplication_matrix()
    incidence, incidence_target = incidence_monomial_matrix()
    result = Verification(
        r4_dimension=len(r4_basis),
        r10_dimension=len(r10_basis),
        jacobian_multiplication_rank=exact_rank(multiplication),
        incidence_target_dimension=len(incidence_target),
        incidence_monomial_rank=exact_rank(incidence),
    )
    expected = Verification(90, 21, 6, 15, 9)
    if result != expected:
        raise AssertionError(f"Cycle 70 verification failed: {result!r} != {expected!r}")
    return result


def main() -> None:
    result = verify()
    print("Cycle 70 exact Fermat-quartic selected formal plane branch")
    print("root normalization: diagonal conjugacy; nonzero root-scaled coefficients = 1")
    print(f"dim R4 = {result.r4_dimension}")
    print(f"dim R10 = {result.r10_dimension}")
    print(f"rank(R4 -> R10) = {result.jacobian_multiplication_rank}")
    print(f"incidence monomial map rank = {result.incidence_monomial_rank}")
    print("Scope: selected formal branch only; this is not a Hodge solution.")


if __name__ == "__main__":
    main()
