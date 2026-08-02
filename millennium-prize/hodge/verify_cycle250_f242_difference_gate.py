#!/usr/bin/env python3
"""Exact tangent-cone gate for an F242 6-by-9 Gaussian matrix."""

import argparse
import json

import sympy as sp


def gaussian(value):
    if isinstance(value, int):
        return sp.Integer(value)
    if not isinstance(value, str):
        raise ValueError(f"matrix entry must be an integer or string: {value!r}")
    return sp.sympify(value.replace("i", "I"), locals={"I": sp.I})


def load_matrix(path):
    with open(path, encoding="ascii") as handle:
        raw = json.load(handle)
    if isinstance(raw, dict):
        raw = raw["M"]
    if len(raw) != 6 or any(len(row) != 9 for row in raw):
        raise ValueError("candidate must be a 6-by-9 matrix (or an object with key M)")
    return sp.Matrix([[gaussian(entry) for entry in row] for row in raw])


def projective_common_zero(forms, variables):
    chart_results = []
    for chart, variable in enumerate(variables):
        chart_forms = [sp.expand(form.subs(variable, 1)) for form in forms]
        chart_variables = variables[:chart] + variables[chart + 1 :]
        basis = sp.groebner(chart_forms, *chart_variables, extension=sp.I)
        empty = basis.contains(sp.Integer(1))
        chart_results.append({"chart": str(variable), "empty": bool(empty)})
    return not all(item["empty"] for item in chart_results), chart_results


def tangent_gate(matrix):
    rank = matrix.rank()
    block_ranks = [matrix[:, 3 * r : 3 * (r + 1)].rank() for r in range(3)]
    result = {"rank": rank, "block_ranks": block_ranks}
    if rank != 6:
        result["outcome"] = "REJECT_TOTAL_RANK"
        return result
    if any(block_rank < 2 for block_rank in block_ranks):
        result["outcome"] = "REJECT_BLOCK_RANK"
        return result

    nullspace = matrix.nullspace()
    if len(nullspace) != 3:
        raise AssertionError("a rank-six 6-by-9 matrix must have nullity three")
    kernel_basis = sp.Matrix.hstack(*nullspace)
    t = sp.symbols("t0:3")
    tangent = kernel_basis * sp.Matrix(t)
    forms = [
        sp.expand(sum(tangent[3 * r + j] ** 4 for j in range(3)))
        for r in range(3)
    ]
    common_zero, charts = projective_common_zero(forms, t)
    result.update(
        {
            "kernel_basis": [[str(x) for x in row] for row in kernel_basis.tolist()],
            "tangent_quartics": [str(form) for form in forms],
            "projective_charts": charts,
        }
    )
    if common_zero:
        result["outcome"] = "REJECT_IDENTITY_SCHEME_DEGENERATE_LEADING_FORMS"
        result["next_gate"] = "FULL_LOCAL_GROEBNER_FOR_ACTUAL_LENGTH"
    else:
        result["outcome"] = "REJECT_FAT_IDENTITY"
        result["identity_local_length"] = 64
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", help="JSON file containing a 6-by-9 matrix M")
    args = parser.parse_args()
    print(json.dumps(tangent_gate(load_matrix(args.candidate)), indent=2))


if __name__ == "__main__":
    main()
