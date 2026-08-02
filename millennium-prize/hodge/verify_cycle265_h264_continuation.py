#!/usr/bin/env python3
"""Verify the exact two-cell counterpacket to universal H264 survival."""

import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


ARTIFACT = Path(__file__).with_name("cycle265_h264_continuation.json")
CELLS = (("A", 0), ("B", -1))
ALPHA = (1, 2)


def exterior_subsets():
    return [subset for size in range(7) for subset in combinations(range(1, 7), size)]


def key(element):
    return element[:3]


def build_basis():
    basis = []
    for source, source_shift in CELLS:
        for target, target_shift in CELLS:
            for subset in exterior_subsets():
                degree = len(subset) + source_shift - target_shift
                basis.append((source, target, subset, degree))
    return basis


def exterior_product(left, right):
    if set(left).intersection(right):
        return None
    inversions = sum(1 for i in left for j in right if i > j)
    return (-1 if inversions % 2 else 1, tuple(sorted(left + right)))


def compose(left, right):
    """Return left after right as (coefficient, basis key), or None."""
    if right[1] != left[0]:
        return None
    product = exterior_product(left[2], right[2])
    if product is None:
        return None
    coefficient, subset = product
    return coefficient, (right[0], left[1], subset)


def differential(element, q):
    result = defaultdict(Fraction)
    left_term = compose(q, element)
    if left_term is not None:
        coefficient, target = left_term
        result[target] += coefficient
    right_term = compose(element, q)
    if right_term is not None:
        coefficient, target = right_term
        result[target] -= ((-1) ** element[3]) * coefficient
    return {target: coefficient for target, coefficient in result.items() if coefficient}


def rank(matrix):
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row != pivot_row and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [a - scale * b for a, b in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def multiply(left, right):
    if not left or not right:
        return []
    return [
        [
            sum(left[row][pivot] * right[pivot][column] for pivot in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def build_artifact():
    basis = build_basis()
    by_degree = defaultdict(list)
    by_key = {}
    for element in basis:
        by_degree[element[3]].append(element)
        by_key[key(element)] = element

    q = by_key[("A", "B", ())]
    h = by_key[("B", "A", ())]
    g = by_key[("B", "A", ALPHA)]
    minimum = min(by_degree)
    maximum = max(by_degree)
    matrices = {}
    ranks = {}
    images = {}
    for degree in range(minimum, maximum + 1):
        source = by_degree[degree]
        target = by_degree[degree + 1]
        rows = {key(element): row for row, element in enumerate(target)}
        matrix = [[Fraction(0) for _ in source] for _ in target]
        degree_images = []
        for column, element in enumerate(source):
            image = differential(element, q)
            degree_images.append(image)
            for target_key, coefficient in image.items():
                matrix[rows[target_key]][column] = coefficient
        matrices[degree] = matrix
        ranks[degree] = rank([row[:] for row in matrix])
        images[degree] = degree_images

    dimensions = {degree: len(by_degree[degree]) for degree in range(minimum, maximum + 1)}
    cohomology = {
        degree: dimensions[degree] - ranks[degree] - ranks.get(degree - 1, 0)
        for degree in dimensions
    }
    d_squared_zero = all(
        all(not entry for row in multiply(matrices[degree + 1], matrices[degree]) for entry in row)
        for degree in range(minimum, maximum - 1)
    )

    q_squared = compose(q, q)
    qh = compose(q, h)
    hq = compose(h, q)
    g_image = differential(g, q)
    alpha_a = ("A", "A", ALPHA)
    alpha_b = ("B", "B", ALPHA)
    alpha_a_row = [int(image.get(alpha_a, 0)) for image in images[1]]

    artifact = {
        "artifact": "H265-H264-BOUNDED-CONTINUATION",
        "version": 1,
        "field": "Q(i)",
        "scope": "strict two-vertex compressed Ext model only; no KI240 claim",
        "counterpacket": {
            "cells": [
                {"name": name, "vertex": "F_0", "shift": shift} for name, shift in CELLS
            ],
            "Q": "unit:A->B",
            "Q_degree": q[3],
            "Q_squared": q_squared is None,
            "contraction": "h=unit:B->A",
            "h_degree": h[3],
            "Qh": [qh[1][0], qh[1][1], list(qh[1][2])] if qh else None,
            "hQ": [hq[1][0], hq[1][1], list(hq[1][2])] if hq else None,
        },
        "diagonal_class": {
            "O": "a_1a_2|A + a_1a_2|B",
            "degree": 2,
            "primitive": "G=a_1a_2*h:B->A",
            "primitive_degree": g[3],
            "d_G": {"a_1a_2:A->A": int(g_image.get(alpha_a, 0)), "a_1a_2:B->B": int(g_image.get(alpha_b, 0))},
            "lambda_A_on_d_G": int(g_image.get(alpha_a, 0)),
            "lambda_A_on_image_d_End_1": alpha_a_row,
            "outcome": "exact",
        },
        "endomorphism_complex": {
            "total_dimension": len(basis),
            "graded_dimensions": {str(degree): dimensions[degree] for degree in sorted(dimensions)},
            "differential_ranks": {str(degree): ranks[degree] for degree in sorted(ranks)},
            "cohomology_dimensions": {str(degree): cohomology[degree] for degree in sorted(cohomology)},
            "d_squared_zero": d_squared_zero,
        },
        "conclusion": {
            "universal_survival_over_all_strict_finite_twisted_complexes": False,
            "counterpacket_is_contractible": True,
            "minimal_packet_question_decided": False,
            "ki240_claim": False,
        },
    }
    verify(artifact)
    return artifact


def verify(artifact):
    packet = artifact["counterpacket"]
    assert packet["Q_degree"] == 1 and packet["Q_squared"]
    assert packet["h_degree"] == -1
    assert packet["Qh"] == ["B", "B", []]
    assert packet["hQ"] == ["A", "A", []]
    diagonal = artifact["diagonal_class"]
    assert diagonal["primitive_degree"] == 1
    assert diagonal["d_G"] == {"a_1a_2:A->A": 1, "a_1a_2:B->B": 1}
    assert diagonal["lambda_A_on_d_G"] == 1
    assert any(diagonal["lambda_A_on_image_d_End_1"])
    endomorphisms = artifact["endomorphism_complex"]
    assert endomorphisms["total_dimension"] == 256
    assert endomorphisms["d_squared_zero"]
    assert not any(endomorphisms["cohomology_dimensions"].values())
    conclusion = artifact["conclusion"]
    assert not conclusion["universal_survival_over_all_strict_finite_twisted_complexes"]
    assert conclusion["counterpacket_is_contractible"]
    assert not conclusion["minimal_packet_question_decided"]
    assert not conclusion["ki240_claim"]


def serialized_artifact():
    return json.dumps(build_artifact(), indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = serialized_artifact()
    if args.check:
        assert ARTIFACT.read_text() == rendered
        print("H264 bounded continuation verified: exact two-cell counterpacket; no KI240 claim")
    else:
        ARTIFACT.write_text(rendered)
        print(f"wrote {ARTIFACT}")


if __name__ == "__main__":
    main()
