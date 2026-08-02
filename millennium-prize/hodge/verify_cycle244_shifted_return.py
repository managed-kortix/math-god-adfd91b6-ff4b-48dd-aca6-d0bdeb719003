#!/usr/bin/env python3
"""Generate and verify the exact shifted two-arrow return certificate."""

import argparse
import json
from pathlib import Path


ARTIFACT = Path(__file__).with_name("cycle244_shifted_return.json")


def shifted_degree(ext_degree, source_shift, target_shift):
    """Invert Ext degree = shifted degree - source shift + target shift."""
    return ext_degree + source_shift - target_shift


def multiply_sparse(left, right):
    """Multiply matrices whose entries are (coefficient, basis label) or zero."""
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    result = [[None for _ in range(columns)] for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            terms = []
            for pivot in range(middle):
                a = left[row][pivot]
                b = right[pivot][column]
                if a is not None and b is not None:
                    terms.append((a, b))
            if terms:
                result[row][column] = terms
    return result


def build_artifact():
    source_shift, middle_shift, target_shift = 0, 2, 4
    first_degree = shifted_degree(3, source_shift, middle_shift)
    second_degree = shifted_degree(3, middle_shift, target_shift)
    product_degree = shifted_degree(6, source_shift, target_shift)

    # Rows are targets and columns are sources in the order A, B, C.
    q = [
        [None, None, None],
        [(1, "x_01_0"), None, None],
        [None, (1, "x_10_0"), None],
    ]
    q_squared = multiply_sparse(q, q)

    return {
        "artifact": "cycle244_shifted_return",
        "version": 1,
        "field": "Q(i)",
        "pair": {
            "vertices": [0, 1],
            "u_minus_1": {"re": 1, "im": 1},
            "norm": 2,
            "cross_ext_3_dimension": 8,
        },
        "cells": [
            {"name": "A", "object": "F_0", "shift": source_shift},
            {"name": "B", "object": "F_1", "shift": middle_shift},
            {"name": "C", "object": "F_0", "shift": target_shift},
        ],
        "shift_rule": "Hom^d(F_i[r],F_j[s])=Ext^(d-r+s)(F_i,F_j)",
        "arrows": [
            {"map": "x_01_0", "source": "A", "target": "B",
             "ext_degree": 3, "shifted_degree": first_degree},
            {"map": "x_10_0", "source": "B", "target": "C",
             "ext_degree": 3, "shifted_degree": second_degree},
        ],
        "yoneda_pairing": {
            "x_10_0*x_01_0": "+omega_0",
            "x_01_0*x_10_0": "-omega_1",
            "reason": "normalized perfect Serre pairing; odd-degree cyclicity",
        },
        "return_block": {
            "source": "A",
            "target": "C",
            "same_support": "F_0",
            "ext_degree": 6,
            "shifted_degree": product_degree,
            "value": "+omega_0",
            "nonzero": True,
        },
        "candidate_differential_matrix": q,
        "square_nonzero_entries": {
            "row_C_column_A": q_squared[2][0],
            "interpreted_value": "+omega_0",
        },
        "conclusion": {
            "support_cycle_inference_refuted": True,
            "maurer_cartan_satisfied": False,
            "atiyah_cancellation_demonstrated": False,
            "ki240_disproved": False,
        },
    }


def verify(artifact):
    pair = artifact["pair"]
    assert pair["norm"] == 1 * 1 + 1 * 1
    assert pair["cross_ext_3_dimension"] == pair["norm"] ** 3 == 8

    arrows = artifact["arrows"]
    assert [arrow["shifted_degree"] for arrow in arrows] == [1, 1]
    block = artifact["return_block"]
    assert block["ext_degree"] == 6
    assert block["shifted_degree"] == 2
    assert block["same_support"] == "F_0" and block["nonzero"]

    square = artifact["square_nonzero_entries"]["row_C_column_A"]
    assert square == [((1, "x_10_0"), (1, "x_01_0"))]
    assert artifact["yoneda_pairing"]["x_10_0*x_01_0"] == "+omega_0"
    assert artifact["yoneda_pairing"]["x_01_0*x_10_0"] == "-omega_1"

    conclusion = artifact["conclusion"]
    assert conclusion["support_cycle_inference_refuted"]
    assert not conclusion["maurer_cartan_satisfied"]
    assert not conclusion["atiyah_cancellation_demonstrated"]
    assert not conclusion["ki240_disproved"]


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
        print("cycle244 shifted return artifact verified")
    else:
        ARTIFACT.write_text(rendered)
        print(f"wrote {ARTIFACT}")


if __name__ == "__main__":
    main()
