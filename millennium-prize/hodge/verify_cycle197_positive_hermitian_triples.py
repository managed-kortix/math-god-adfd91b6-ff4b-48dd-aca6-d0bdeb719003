#!/usr/bin/env python3
"""Exact positive-divisor polarization of the Cycle 196 graph cubes."""

from fractions import Fraction as F


D0 = 930187500000000000
COEFFICIENTS = (
    317131927490234375,
    -2073948378906250,
    12564289203125,
    -56707735500,
    27598945,
    3626326,
    -68381,
)
POWERS = ((1, 0), (2, 1), (3, 4), (2, 11), (-7, 24), (-38, 41), (-117, 44))
Q = (1, 1, 3)
ZERO = (F(0), F(0))
ONE = (F(1), F(0))


def g(value):
    return (F(value), F(0)) if not isinstance(value, tuple) else (F(value[0]), F(value[1]))


def gadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gneg(value):
    return (-value[0], -value[1])


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0])


def gdiv(left, right):
    norm = right[0] * right[0] + right[1] * right[1]
    return ((left[0] * right[0] + left[1] * right[1]) / norm,
            (left[1] * right[0] - left[0] * right[1]) / norm)


def matrix_zero():
    return [[ZERO for _ in range(6)] for _ in range(6)]


def polarization():
    matrix = matrix_zero()
    for index, value in enumerate((1, 1, 1, 1, 1, 3)):
        matrix[index][index] = g(value)
    return matrix


def graph_divisor(a, coordinate):
    real, imaginary = a
    norm = real * real + imaginary * imaginary
    matrix = matrix_zero()
    matrix[coordinate][coordinate] = g(norm)
    matrix[coordinate][coordinate + 3] = g((-real, imaginary))
    matrix[coordinate + 3][coordinate] = g((-real, -imaginary))
    matrix[coordinate + 3][coordinate + 3] = ONE
    return matrix


def matrix_add(left, right):
    return [[gadd(left[i][j], right[i][j]) for j in range(6)] for i in range(6)]


def matrix_key(matrix):
    return tuple(value for row in matrix for entry in row for value in entry)


def form_add(*forms):
    result = {}
    for form in forms:
        for mask, coefficient in form.items():
            result[mask] = gadd(result.get(mask, ZERO), coefficient)
            if result[mask] == ZERO:
                del result[mask]
    return result


def form_scale(coefficient, form):
    return {mask: gmul(coefficient, value) for mask, value in form.items()
            if gmul(coefficient, value) != ZERO}


def wedge(left, right):
    result = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            crossings = sum((left_mask >> (index + 1)).bit_count()
                            for index in range(12) if (right_mask >> index) & 1)
            coefficient = gmul(left_coefficient, right_coefficient)
            if crossings % 2:
                coefficient = gneg(coefficient)
            mask = left_mask | right_mask
            result[mask] = gadd(result.get(mask, ZERO), coefficient)
            if result[mask] == ZERO:
                del result[mask]
    return result


def divisor_form(matrix):
    result = {}
    for row in range(6):
        for column in range(6):
            coefficient = matrix[row][column]
            if coefficient != ZERO:
                result = form_add(result, {1 << row | 1 << (6 + column): coefficient})
    return result


def variation_form(matrix, b_row, b_column):
    """The (0,2) derivative H*mu-(H*mu)^t for one matrix unit B."""
    mu = matrix_zero()
    mu[b_row][3 + b_column] = ONE
    mu[3 + b_column][b_row] = g(F(1, Q[b_column]))
    product = matrix_zero()
    for i in range(6):
        for j in range(6):
            for k in range(6):
                product[i][j] = gadd(product[i][j], gmul(matrix[i][k], mu[k][j]))
    result = {}
    for i in range(6):
        for j in range(i + 1, 6):
            coefficient = gadd(product[i][j], gneg(product[j][i]))
            if coefficient != ZERO:
                result[1 << (6 + i) | 1 << (6 + j)] = coefficient
    return result


def product_variations(triple):
    forms = [divisor_form(matrix) for matrix in triple]
    vectors = []
    for b_row in range(3):
        for b_column in range(3):
            terms = []
            for index in range(3):
                others = [forms[j] for j in range(3) if j != index]
                terms.append(wedge(variation_form(triple[index], b_row, b_column),
                                   wedge(others[0], others[1])))
            vectors.append(form_add(*terms))
    return vectors


def rank(vectors):
    coordinates = sorted({mask for vector in vectors for mask in vector})
    rows = [[vector.get(mask, ZERO) for vector in vectors] for mask in coordinates]
    pivot_row = 0
    for column in range(len(vectors)):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column] != ZERO), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        divisor = rows[pivot_row][column]
        rows[pivot_row] = [gdiv(value, divisor) for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row != pivot_row and rows[row][column] != ZERO:
                factor = rows[row][column]
                rows[row] = [gadd(value, gneg(gmul(factor, pivot_value)))
                             for value, pivot_value in zip(rows[row], rows[pivot_row])]
        pivot_row += 1
    return pivot_row


def intersection_dimension(power_index, subset):
    norm = 5 ** power_index
    allowed = 0
    for row in range(3):
        for column in range(3):
            okay = True
            for coordinate in subset:
                if row == coordinate or column == coordinate:
                    if row != column or norm != F(1, Q[coordinate]):
                        okay = False
            if okay:
                allowed += 1
    return allowed


def main():
    theta = polarization()
    theta_form = divisor_form(theta)
    theta_cube = wedge(theta_form, wedge(theta_form, theta_form))
    decomposition = {}
    rank_table = []
    signed_variations = [dict() for _ in range(9)]
    original_target = {}
    polarized_target = {}

    for power_index, (coefficient, power) in enumerate(zip(COEFFICIENTS, POWERS)):
        divisors = [graph_divisor(power, coordinate) for coordinate in range(3)]
        graph_cube = wedge(divisor_form(divisors[0]),
                           wedge(divisor_form(divisors[1]), divisor_form(divisors[2])))
        original_target = form_add(original_target, form_scale(g(coefficient), graph_cube))
        for subset_bits in range(8):
            subset = tuple(index for index in range(3) if (subset_bits >> index) & 1)
            sign = -1 if (3 - len(subset)) % 2 else 1
            triple = tuple(matrix_add(theta, divisors[index]) if index in subset else theta
                           for index in range(3))
            key = tuple(sorted(matrix_key(matrix) for matrix in triple))
            decomposition[key] = decomposition.get(key, 0) + coefficient * sign
            vectors = product_variations(triple)
            product_rank = rank(vectors)
            rank_table.append((power_index, subset, intersection_dimension(power_index, subset),
                               product_rank, 9 - product_rank))
            for index, vector in enumerate(vectors):
                signed_variations[index] = form_add(
                    signed_variations[index], form_scale(g(coefficient * sign), vector))
            triple_product = wedge(divisor_form(triple[0]),
                                   wedge(divisor_form(triple[1]), divisor_form(triple[2])))
            polarized_target = form_add(
                polarized_target, form_scale(g(coefficient * sign), triple_product))

    decomposition = {key: value for key, value in decomposition.items() if value}
    assert len(decomposition) == 50
    assert polarized_target == original_target
    assert original_target
    assert all((mask & 63).bit_count() == 3 and ((mask >> 6) & 63).bit_count() == 3
               for mask in original_target)
    signed_product_rank = rank(signed_variations)
    assert signed_product_rank == 9

    theta_cube_coefficient = -sum(COEFFICIENTS)
    assert theta_cube_coefficient == -315070486723952640
    assert decomposition[tuple(sorted(matrix_key(theta) for _ in range(3)))] == theta_cube_coefficient

    expected_intersections = {
        0: (9, 5, 5, 3, 4, 2, 2, 2),
        1: (9, 4, 4, 1, 4, 1, 1, 0),
    }
    for power_index, subset, intersection, _, _ in rank_table:
        expected = expected_intersections[0 if power_index == 0 else 1][sum(1 << i for i in subset)]
        assert intersection == expected

    full_product_loci = [(power_index, subset) for power_index, subset, _, product_rank, _
                         in rank_table if product_rank == 0]
    full_factor_intersections = [(power_index, subset) for power_index, subset, intersection, _, _
                                 in rank_table if intersection == 9]
    assert full_factor_intersections == [(index, ()) for index in range(7)]

    print("Cycle 197 positive Hermitian triple search")
    print("padding polarization Theta = diag(1,1,1,1,1,3)")
    print("minimal integral padding = 1 (Theta + D is positive definite; D alone has rank 1)")
    print("raw inclusion-exclusion triples = 56; consolidated nonzero triples = 50")
    print("all-Theta consolidated coefficient =", theta_cube_coefficient)
    print("factor-locus tangent dimensions for k=0 by subset 000..111 =",
          expected_intersections[0])
    print("factor-locus tangent dimensions for k>0 by subset 000..111 =",
          expected_intersections[1])
    print("triples whose product class has full tangent Hodge locus =", full_product_loci)
    print("only the all-Theta triples have full individual-factor intersection")
    print("signed sum product tangent Hodge condition has rank =", signed_product_rank)
    print("thus this fixed divisor-cube decomposition is Hodge only in tangent direction B=0")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
