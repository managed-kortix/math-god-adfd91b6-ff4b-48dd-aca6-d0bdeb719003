#!/usr/bin/env python3
"""Generate and verify the exact H264-KI-MIN endomorphism complex."""

import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


ARTIFACT = Path(__file__).with_name("cycle264_ki_min.json")
CELLS = (("A", 0, 0), ("B", 1, 2), ("C", 0, 4))
CROSS_DIMENSION = 8
TOP = tuple(range(1, 7))


def exterior_subsets():
    return [subset for size in range(7) for subset in combinations(range(1, 7), size)]


def basis_key(element):
    return element[:4]


def build_basis():
    basis = []
    for source_name, source_vertex, source_shift in CELLS:
        for target_name, target_vertex, target_shift in CELLS:
            if source_vertex == target_vertex:
                for subset in exterior_subsets():
                    degree = len(subset) + source_shift - target_shift
                    basis.append((source_name, target_name, "self", subset, degree))
            else:
                for index in range(CROSS_DIMENSION):
                    degree = 3 + source_shift - target_shift
                    basis.append((source_name, target_name, "cross", index, degree))
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
    left_kind, left_label = left[2], left[3]
    right_kind, right_label = right[2], right[3]
    source, target = right[0], left[1]

    if left_kind == right_kind == "self":
        product = exterior_product(left_label, right_label)
        if product is None:
            return None
        coefficient, subset = product
        return coefficient, (source, target, "self", subset)
    if left_kind == "self" and right_kind == "cross":
        return (1, (source, target, "cross", right_label)) if not left_label else None
    if left_kind == "cross" and right_kind == "self":
        return (1, (source, target, "cross", left_label)) if not right_label else None
    if left_label != right_label:
        return None
    source_vertex = next(vertex for name, vertex, _ in CELLS if name == source)
    coefficient = 1 if source_vertex == 0 else -1
    return coefficient, (source, target, "self", TOP)


def differential(element, q):
    degree = element[4]
    result = defaultdict(Fraction)
    left_term = compose(q, element)
    if left_term is not None:
        coefficient, key = left_term
        result[key] += coefficient
    right_term = compose(element, q)
    if right_term is not None:
        coefficient, key = right_term
        result[key] -= ((-1) ** degree) * coefficient
    return {key: value for key, value in result.items() if value}


def rank(matrix):
    if not matrix:
        return 0
    rows = len(matrix)
    columns = len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(rows):
            if row != pivot_row and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [a - scale * b for a, b in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def multiply_matrices(left, right):
    if not left or not right:
        return []
    return [
        [sum(left[row][pivot] * right[pivot][column] for pivot in range(len(right)))
         for column in range(len(right[0]))]
        for row in range(len(left))
    ]


def complex_data():
    basis = build_basis()
    by_degree = defaultdict(list)
    by_key = {}
    for element in basis:
        by_degree[element[4]].append(element)
        by_key[basis_key(element)] = element
    q = by_key[("A", "B", "cross", 0)]
    minimum_degree = min(element[4] for element in basis)
    maximum_degree = max(element[4] for element in basis)
    matrices = {}
    images = {}
    ranks = {}
    for degree in range(minimum_degree, maximum_degree + 1):
        source_basis = by_degree[degree]
        target_basis = by_degree[degree + 1]
        target_rows = {basis_key(element): row for row, element in enumerate(target_basis)}
        matrix = [[Fraction(0) for _ in source_basis] for _ in target_basis]
        degree_images = []
        for column, element in enumerate(source_basis):
            image = differential(element, q)
            degree_images.append(image)
            for key, coefficient in image.items():
                matrix[target_rows[key]][column] = coefficient
        matrices[degree] = matrix
        images[degree] = degree_images
        ranks[degree] = rank([row[:] for row in matrix])
    dimensions = {degree: len(by_degree[degree]) for degree in range(minimum_degree, maximum_degree + 1)}
    cohomology = {
        degree: dimension - ranks[degree] - ranks.get(degree - 1, 0)
        for degree, dimension in dimensions.items()
    }
    d_squared_zero = all(
        all(not entry for row in multiply_matrices(matrices[degree + 1], matrices[degree]) for entry in row)
        for degree in range(minimum_degree, maximum_degree - 1)
    )
    return basis, by_degree, by_key, q, ranks, images, dimensions, cohomology, d_squared_zero


def build_artifact():
    data = complex_data()
    basis, by_degree, by_key, q, ranks, images, dimensions, cohomology, d_squared_zero = data
    alpha_keys = [(name, name, "self", (1, 2)) for name, _, _ in CELLS]
    assert all(not differential(by_key[key], q) for key in alpha_keys)
    alpha_a_row = [image.get(alpha_keys[0], Fraction(0)) for image in images[1]]
    y = by_key[("B", "C", "cross", 0)]
    y_image = differential(y, q)
    omega_ac_key = ("A", "C", "self", TOP)

    return {
        "artifact": "H264-KI-MIN",
        "version": 1,
        "field": "Q(i)",
        "scope": "minimal two-vertex shifted-return mechanism test only",
        "cells": [
            {"name": name, "vertex": f"F_{vertex}", "shift": shift}
            for name, vertex, shift in CELLS
        ],
        "ext_algebra": {
            "model": "strict minimal A-infinity model: m_1=0, m_2=Yoneda product, m_n=0 for n>=3",
            "self": "Ext*(F_i,F_i)=Lambda(a_1,...,a_6)",
            "cross": "Ext^3(F_0,F_1)=Ext^3(F_1,F_0)=K^8; all other cross Ext vanish",
            "normalized_pair": "x_10,s*x_01,t=delta_st*omega_0; x_01,t*x_10,s=-delta_st*omega_1",
        },
        "twisted_object": {
            "underlying": "A direct-sum B direct-sum C",
            "Q": "x_01,0:A->B",
            "Q_degree": q[4],
            "Q_squared": 0,
            "two_arrow_candidate": "x_01,0:A->B plus x_10,0:B->C",
            "two_arrow_candidate_squared": "+omega_0:A->C (nonzero, so not Maurer-Cartan)",
            "return_generator": "y=x_10,0:B->C",
            "return_generator_degree": y[4],
        },
        "endomorphism_complex": {
            "differential": "d(f)=Q*f-(-1)^degree(f)*f*Q",
            "total_dimension": len(basis),
            "graded_dimensions": {str(k): dimensions[k] for k in sorted(dimensions)},
            "differential_ranks": {str(k): ranks[k] for k in sorted(ranks)},
            "cohomology_dimensions": {str(k): cohomology[k] for k in sorted(cohomology)},
            "d_squared_zero": d_squared_zero,
        },
        "return_block": {
            "class": "omega_0:A->C",
            "degree": by_key[omega_ac_key][4],
            "primitive": "y=x_10,0:B->C",
            "d_y": "+omega_0:A->C",
            "verified_coefficient": int(y_image[omega_ac_key]),
            "outcome": "killed",
        },
        "diagonal_obstruction": {
            "cocycle": "O=a_1a_2|A + a_1a_2|B + a_1a_2|C",
            "degree": 2,
            "d_O": 0,
            "dual_cocycle": "lambda_A extracts the coefficient of a_1a_2:A->A",
            "lambda_A_on_O": 1,
            "lambda_A_on_image_d_End_1": [int(value) for value in alpha_a_row],
            "outcome": "survives",
        },
        "conclusion": {
            "shifted_return_top_class_is_boundary": True,
            "diagonal_ext2_obstruction_survives": True,
            "mechanism_test_pass": True,
            "ki240_claim": False,
        },
    }


def verify(artifact):
    assert artifact["twisted_object"]["Q_degree"] == 1
    assert artifact["twisted_object"]["return_generator_degree"] == 1
    assert artifact["twisted_object"]["Q_squared"] == 0
    assert artifact["endomorphism_complex"]["total_dimension"] == 352
    assert artifact["endomorphism_complex"]["d_squared_zero"]
    assert artifact["return_block"]["degree"] == 2
    assert artifact["return_block"]["verified_coefficient"] == 1
    obstruction = artifact["diagonal_obstruction"]
    assert obstruction["d_O"] == 0 and obstruction["lambda_A_on_O"] == 1
    assert not any(obstruction["lambda_A_on_image_d_End_1"])
    conclusion = artifact["conclusion"]
    assert conclusion["shifted_return_top_class_is_boundary"]
    assert conclusion["diagonal_ext2_obstruction_survives"]
    assert conclusion["mechanism_test_pass"] and not conclusion["ki240_claim"]


def serialized_artifact():
    artifact = build_artifact()
    verify(artifact)
    return json.dumps(artifact, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = serialized_artifact()
    if args.check:
        assert ARTIFACT.read_text() == rendered
        print("H264-KI-MIN exact artifact verified: diagonal Ext^2 survives; no KI240 claim")
    else:
        ARTIFACT.write_text(rendered)
        print(f"wrote {ARTIFACT}")


if __name__ == "__main__":
    main()
