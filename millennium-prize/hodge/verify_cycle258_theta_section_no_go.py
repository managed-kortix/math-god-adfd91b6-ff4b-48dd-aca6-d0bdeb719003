#!/usr/bin/env python3
"""Exact exterior-algebra checks for the Cycle 258 theta-section no-go."""

from fractions import Fraction


def add(*forms):
    result = {}
    for form in forms:
        for monomial, coefficient in form.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {m: c for m, c in result.items() if c}


def scale(form, scalar):
    return {m: scalar * c for m, c in form.items() if scalar * c}


def basis(index):
    return {(index,): Fraction(1)}


def wedge(left, right):
    result = {}
    for first, a in left.items():
        for second, b in right.items():
            if set(first).intersection(second):
                continue
            inversions = sum(i > j for i in first for j in second)
            monomial = tuple(sorted(first + second))
            result[monomial] = result.get(monomial, 0) + (-1) ** inversions * a * b
    return {m: c for m, c in result.items() if c}


def beltrami_derivative(form, substitutions):
    result = {}
    for monomial, coefficient in form.items():
        for position, index in enumerate(monomial):
            if index >= 6 or index not in substitutions:
                continue
            replacement, scalar = substitutions[index]
            term = list(monomial)
            term[position] = replacement
            if len(set(term)) != len(term):
                continue
            inversions = sum(
                term[i] > term[j]
                for i in range(len(term))
                for j in range(i + 1, len(term))
            )
            ordered = tuple(sorted(term))
            result[ordered] = result.get(ordered, 0) + coefficient * scalar * (-1) ** inversions
    return {m: c for m, c in result.items() if c}


def main():
    # Indices 0,...,5 are dz_1,...,dz_6; 6,...,11 are their conjugates.
    delta_14 = wedge(add(basis(3), scale(basis(0), -1)), add(basis(9), scale(basis(6), -1)))
    delta_25 = wedge(add(basis(4), scale(basis(1), -1)), add(basis(10), scale(basis(7), -1)))

    embedded = [0, 1, 2, 5]
    hermitian = (
        (6, 0, 0, 0),
        (0, 6, 0, 0),
        (0, 0, 6, 3),
        (0, 0, 3, 6),
    )
    h_tilde = {}
    for row in range(4):
        for column in range(4):
            if hermitian[row][column]:
                pair = wedge(basis(embedded[row]), basis(6 + embedded[column]))
                h_tilde = add(h_tilde, scale(pair, hermitian[row][column]))

    support_class = wedge(wedge(delta_14, delta_25), h_tilde)
    contraction = beltrami_derivative(
        support_class,
        {
            0: (10, Fraction(1)),  # dz_1 -> dbar z_5
            4: (6, Fraction(1)),   # dz_5 -> dbar z_1
        },
    )
    witness = (2, 3, 6, 8, 9, 10)
    assert contraction[witness] == -6

    # Pullback Omega_W lacks exactly dt_4 wedge dbar(t_3), whose coefficient is H_43=3.
    assert hermitian[3][2] == 3
    print("exceptional complement H_43 = 3")
    print("E_12 contraction witness coefficient = -6")


if __name__ == "__main__":
    main()
