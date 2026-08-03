#!/usr/bin/env python3
"""Generate and verify the seven graph-sheaf AKS Ext^2 matrices."""

import argparse
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


ARTIFACT = Path(__file__).with_name("cycle268_aks_cocycles.json")
POWERS = ((1, 0), (2, 1), (3, 4), (2, 11), (-7, 24),
          (-38, 41), (-117, 44))
Q = (Fraction(1), Fraction(1), Fraction(3))
EXT1 = ("h_1", "h_2", "h_3", "n_1", "n_2", "n_3")
EXT2 = tuple(combinations(range(6), 2))
TANGENT = tuple((row, column) for row in range(3) for column in range(3))


def scalar(value):
    value = Fraction(value)
    return {
        "re": [value.numerator, value.denominator],
        "im": [0, 1],
    }


def rho_entries(norm):
    """Columns of B -> Q^-1 B^t - norm*B in row-major coordinates."""
    columns = []
    for b_row, b_column in TANGENT:
        entries = {}
        transposed = (b_column, b_row)
        entries[transposed] = entries.get(transposed, Fraction(0)) + 1 / Q[b_column]
        original = (b_row, b_column)
        entries[original] = entries.get(original, Fraction(0)) - norm
        columns.append({key: value for key, value in entries.items() if value})
    return columns


def ext2_entries(rho_columns):
    """Embed H^1(O) tensor H^0(N) in Lambda^2 Ext^1."""
    columns = []
    for rho_column in rho_columns:
        entries = {}
        for (normal, cohomology), value in rho_column.items():
            exterior = (cohomology, 3 + normal)
            entries[exterior] = entries.get(exterior, Fraction(0)) + value
        columns.append({key: value for key, value in entries.items() if value})
    return columns


def sparse_rows(columns, row_labels):
    rows = []
    for row_index, label in enumerate(row_labels):
        entries = []
        for column_index, column in enumerate(columns):
            value = column.get(label, Fraction(0))
            if value:
                entries.append({"column": column_index, "value": scalar(value)})
        rows.append({"row": row_index, "entries": entries})
    return rows


def rank(columns, row_labels):
    matrix = [[column.get(label, Fraction(0)) for column in columns]
              for label in row_labels]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                value = matrix[row][column]
                matrix[row] = [left - value * right
                               for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def form_terms(column):
    return [
        {
            "coefficient": scalar(value),
            "wedge": [EXT1[left], EXT1[right]],
            "ext2_row": EXT2.index((left, right)),
        }
        for (left, right), value in sorted(column.items())
    ]


def build_artifact():
    vertices = []
    for k, (real, imaginary) in enumerate(POWERS):
        norm = real * real + imaginary * imaginary
        rho = rho_entries(norm)
        ext2 = ext2_entries(rho)
        vertices.append({
            "vertex": k,
            "power": {"re": real, "im": imaginary},
            "norm": norm,
            "rho_formula": "rho_k(B)=Q^-1*transpose(B)-norm*B",
            "rho_matrix_9x9_sparse": sparse_rows(
                rho, tuple((row, column) for row in range(3) for column in range(3))
            ),
            "ext2_matrix_15x9_sparse": sparse_rows(ext2, EXT2),
            "cocycles": [
                {
                    "tangent_column": column,
                    "tangent_basis": f"B_{row + 1}{col + 1}",
                    "terms": form_terms(ext2[column]),
                }
                for column, (row, col) in enumerate(TANGENT)
            ],
            "rank": rank(ext2, EXT2),
        })

    return {
        "artifact": "H268-MIN2-AKS-vertex-cocycles",
        "version": 1,
        "field": {
            "name": "Q(i)",
            "model": "Q[t]/(t^2+1)",
            "scalar_encoding": {"re": "[numerator,denominator]", "im": "[numerator,denominator]"},
        },
        "basis": {
            "tangent_columns": [f"B_{row + 1}{column + 1}" for row, column in TANGENT],
            "rho_rows": [f"N_{row + 1},H1_{column + 1}" for row, column in TANGENT],
            "ext1": list(EXT1),
            "ext1_meaning": "h_1..h_3 span H^1(O_Gamma_k); n_1..n_3 span H^0(N_Gamma_k/A_0)",
            "ext2_rows": [[EXT1[left], EXT1[right]] for left, right in EXT2],
            "ext2_decomposition": "Lambda^2 H^1(O) + H^1(O) tensor H^0(N) + Lambda^2 H^0(N)",
        },
        "convention": {
            "Q": [1, 1, 3],
            "closed_form": "o_(k,pq)=Q_qq^-1*h_p wedge n_q - 5^k*h_q wedge n_p (indices 1..3)",
            "matrix_orientation": "rows are target coordinates; columns are row-major tangent matrix units B_pq",
            "representative": "translation-invariant Koszul/Dolbeault minimal representative of the H^1(N) AKS class",
        },
        "vertices": vertices,
        "scope": [
            "These matrices identify the nine geometric AKS cohomology classes at every graph vertex.",
            "They do not provide a dg-resolution representative, an A-infinity module cocycle, higher products, or transferred Atiyah homotopies.",
            "Consequently they are not by themselves sufficient to compute the H268 two-cell transferred obstruction.",
        ],
    }


def verify(artifact):
    assert [vertex["norm"] for vertex in artifact["vertices"]] == [5 ** k for k in range(7)]
    assert [vertex["rank"] for vertex in artifact["vertices"]] == [6, 9, 9, 9, 9, 9, 9]
    assert len(artifact["basis"]["ext2_rows"]) == 15
    for vertex in artifact["vertices"]:
        assert len(vertex["cocycles"]) == 9
        assert len(vertex["rho_matrix_9x9_sparse"]) == 9
        assert len(vertex["ext2_matrix_15x9_sparse"]) == 15
    first = artifact["vertices"][0]["cocycles"]
    assert not first[0]["terms"]
    assert not first[4]["terms"]
    assert first[1]["terms"] and first[3]["terms"]


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
        print("H268 graph AKS cocycle matrices verified")
    else:
        ARTIFACT.write_text(rendered)
        print(f"wrote {ARTIFACT}")


if __name__ == "__main__":
    main()
