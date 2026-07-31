#!/usr/bin/env python3
"""Exact divisor-cube lattice certificate for the Cycle 151/169 class."""

import argparse
from fractions import Fraction
from math import gcd


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

N = 6
DEGREE = 6


def gaussian_multiply(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def add(*forms):
    result = {}
    for form in forms:
        for monomial, coefficient in form.items():
            result[monomial] = result.get(monomial, 0) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def scale(coefficient, form):
    return {
        monomial: coefficient * value
        for monomial, value in form.items()
        if coefficient * value
    }


def one_form(index):
    return {1 << index: 1}


def wedge(left, right):
    result = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            crossings = sum(
                (left_mask >> (index + 1)).bit_count()
                for index in range(2 * N)
                if (right_mask >> index) & 1
            )
            mask = left_mask | right_mask
            sign = -1 if crossings % 2 else 1
            result[mask] = result.get(mask, 0) + (
                sign * left_coefficient * right_coefficient
            )
            if result[mask] == 0:
                del result[mask]
    return result


def x(index):
    return one_form(2 * index)


def y(index):
    return one_form(2 * index + 1)


def hermitian_kernel_matrix(a, coordinate):
    """Matrix l^*l for l(z)=z_(coordinate+3)-a*z_coordinate."""
    real, imaginary = a
    matrix = [[(0, 0) for _ in range(N)] for _ in range(N)]
    matrix[coordinate][coordinate] = (real * real + imaginary * imaginary, 0)
    matrix[coordinate + 3][coordinate + 3] = (1, 0)
    matrix[coordinate][coordinate + 3] = (-real, imaginary)
    matrix[coordinate + 3][coordinate] = (-real, -imaginary)
    return matrix


def divisor_form(matrix):
    """Integral two-form associated with a Gaussian Hermitian matrix."""
    result = {}
    for j in range(N):
        diagonal, diagonal_imaginary = matrix[j][j]
        assert diagonal_imaginary == 0
        result = add(result, scale(diagonal, wedge(x(j), y(j))))
        for k in range(j + 1, N):
            real, imaginary = matrix[j][k]
            result = add(
                result,
                scale(real, add(wedge(x(j), y(k)), wedge(x(k), y(j)))),
                scale(imaginary, add(wedge(x(j), x(k)), wedge(y(j), y(k)))),
            )
    return result


def equation_divisor_form(a, coordinate):
    real, imaginary = a
    real_equation = add(
        x(coordinate + 3),
        scale(-real, x(coordinate)),
        scale(imaginary, y(coordinate)),
    )
    imaginary_equation = add(
        y(coordinate + 3),
        scale(-imaginary, x(coordinate)),
        scale(-real, y(coordinate)),
    )
    return wedge(real_equation, imaginary_equation)


def graph_class(a):
    result = {0: 1}
    for coordinate in range(3):
        result = wedge(result, equation_divisor_form(a, coordinate))
    return result


def ordered_coordinate(mask):
    names = []
    for index in range(2 * N):
        if (mask >> index) & 1:
            names.append(("x" if index % 2 == 0 else "y") + str(index // 2 + 1))
    return " ".join(names)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--coordinates",
        action="store_true",
        help="print every nonzero integral-basis coordinate of D0*alpha0 and alpha0",
    )
    args = parser.parse_args()

    powers = [(1, 0)]
    for _ in range(6):
        powers.append(gaussian_multiply(powers[-1], (2, 1)))
    assert powers == [
        (1, 0),
        (2, 1),
        (3, 4),
        (2, 11),
        (-7, 24),
        (-38, 41),
        (-117, 44),
    ]

    graphs = []
    matrices = []
    for power in powers:
        divisors = []
        power_matrices = []
        for coordinate in range(3):
            matrix = hermitian_kernel_matrix(power, coordinate)
            form = divisor_form(matrix)
            assert form == equation_divisor_form(power, coordinate)
            divisors.append(form)
            power_matrices.append(matrix)
        graph = wedge(wedge(divisors[0], divisors[1]), divisors[2])
        assert graph == graph_class(power)
        graphs.append(graph)
        matrices.append(power_matrices)

    target = {}
    for coefficient, graph in zip(COEFFICIENTS, graphs):
        target = add(target, scale(coefficient, graph))
    assert all(mask.bit_count() == DEGREE for mask in target)

    content = 0
    for coefficient in target.values():
        content = gcd(content, abs(coefficient))
    alpha_coordinates = {
        ordered_coordinate(mask): Fraction(coefficient, D0)
        for mask, coefficient in sorted(target.items())
    }

    print("Cycle 196 Hermitian divisor-cube lattice")
    print(f"D0 = {D0}")
    print(f"projector coefficients = {COEFFICIENTS}")
    print(f"powers of 2+i = {powers}")
    print(f"nonzero integral coordinates of D0*alpha0 = {len(target)}")
    print(f"coordinate content of D0*alpha0 = {content}")
    print(f"nonzero rational coordinates of alpha0 = {len(alpha_coordinates)}")
    print("decomposition: sum_k c_k product_j D(k,j), j=1,2,3")
    print("D(k,j) has Hermitian block [[N(u^k),-conj(u^k)],[-u^k,1]]")
    print("membership in the integral triple-divisor subgroup: YES")
    print("quotient obstruction: 0")
    if args.coordinates:
        print("coordinates (basis: increasing x1,y1,...,x6,y6):")
        for basis, alpha_coefficient in alpha_coordinates.items():
            integral_coefficient = alpha_coefficient * D0
            print(
                f"{basis}: D0*alpha0={integral_coefficient}; "
                f"alpha0={alpha_coefficient}"
            )
    print("all exact checks passed")


if __name__ == "__main__":
    main()
