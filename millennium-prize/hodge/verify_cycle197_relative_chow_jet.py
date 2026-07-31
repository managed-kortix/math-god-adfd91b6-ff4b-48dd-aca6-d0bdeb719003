#!/usr/bin/env python3
"""Exact tangent-intersection certificate for the Cycle 197 Chow pair."""

import json
from fractions import Fraction
from pathlib import Path


INPUT = Path(__file__).with_name("cycle197_tangent_jet_input.json")


def rank(matrix):
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    if not rows:
        return 0
    row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (candidate for candidate in range(row, len(rows)) if rows[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        pivot_value = rows[row][column]
        rows[row] = [entry / pivot_value for entry in rows[row]]
        for candidate in range(len(rows)):
            if candidate == row or not rows[candidate][column]:
                continue
            factor = rows[candidate][column]
            rows[candidate] = [
                left - factor * right
                for left, right in zip(rows[candidate], rows[row])
            ]
        row += 1
        if row == len(rows):
            break
    return row


def rho_matrix(q_diagonal, graph_norm):
    """Matrix of B -> Q^(-1) B^t - graph_norm B in row-major bases."""
    size = len(q_diagonal)
    result = [[Fraction(0) for _ in range(size * size)] for _ in range(size * size)]
    for i in range(size):
        for j in range(size):
            output = size * i + j
            result[output][size * j + i] += Fraction(1, q_diagonal[i])
            result[output][size * i + j] -= graph_norm
    return result


def stack(matrices):
    return [row for matrix in matrices for row in matrix]


def image_dimension(base_dimension, obstruction_matrices):
    return base_dimension - rank(stack(obstruction_matrices))


def verify_pair(data, matrices, key):
    pair = data[key]
    plus = [matrices[index] for index in pair["plus_graphs"]]
    minus = [matrices[index] for index in pair["minus_graphs"]]
    plus_dimension = image_dimension(data["base_dimension"], plus)
    minus_dimension = image_dimension(data["base_dimension"], minus)
    pair_dimension = image_dimension(data["base_dimension"], plus + minus)
    assert plus_dimension == pair["expected_plus_base_image_dimension"]
    assert minus_dimension == pair["expected_minus_base_image_dimension"]
    assert pair_dimension == pair["expected_pair_base_image_dimension"]
    return plus_dimension, minus_dimension, pair_dimension


def main():
    data = json.loads(INPUT.read_text(encoding="ascii"))
    assert data["field"] == "Q"
    assert data["base_dimension"] == 9
    assert len(data["base_coordinates"]) == data["base_dimension"]

    powers = [(1, 0)]
    for _ in range(6):
        real, imaginary = powers[-1]
        powers.append((2 * real - imaginary, real + 2 * imaginary))
    assert [list(value) for value in powers] == data["graph_powers"]
    assert [real * real + imaginary * imaginary for real, imaginary in powers] == data[
        "graph_norms"
    ]

    matrices = [
        rho_matrix(data["hermitian_diagonal"], norm)
        for norm in data["graph_norms"]
    ]
    ranks = [rank(matrix) for matrix in matrices]
    assert ranks == [6, 9, 9, 9, 9, 9, 9]

    lci_dimensions = verify_pair(data, matrices, "lci_test_pair")
    projector_dimensions = verify_pair(data, matrices, "projector_pair")
    assert data["second_order_template"]["explicit_pair_status"].startswith(
        "not_reached"
    )

    print("Cycle 197 relative Chow tangent and jet gate")
    print(f"rho ranks for graph powers 0,...,6 = {ranks}")
    print(
        "lci pair base-image dimensions "
        f"(plus, minus, intersection) = {lci_dimensions}"
    )
    print(
        "projector pair base-image dimensions "
        f"(plus, minus, intersection) = {projector_dimensions}"
    )
    print("rank-nine first-order gate: FAIL")
    print("second-order rank-nine gate: NOT REACHED")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
