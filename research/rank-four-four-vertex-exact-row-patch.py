#!/usr/bin/env python3
"""Exact row-level patch audit for the four-vertex rank-four DNN census.

This is deliberately separate from the fail-closed main verifier.  It checks
new rational planar Gram certificates on the automorphism classes of the 72
failed physical transports and reports the genuine structural residual.
"""

import importlib.util
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path


MAIN = Path(__file__).with_name("rank-four-four-vertex-dnn-verifier.py")
SPEC = importlib.util.spec_from_file_location("rank_four_main", MAIN)
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


# (kernel index, physical row, rational quarter-angle parameters).
# Rows are compressed only by genuine kernel automorphisms, never switching.
ROW_CERTIFICATES = (
    (0, (0, 0, 0, 1, 1, 1), (0, "131/100", "17/50", "543/100")),
    (0, (0, 0, 1, 0, 1, 1), (0, 0, "801/100", "3/5")),
    (0, (0, 0, 1, 0, 2, 0), (0, "26/5", "3/25", "14/25")),
    (0, (0, 0, 1, 1, 0, 0), (0, "17/20", "9/100", "14/25")),
    (0, (0, 0, 1, 1, 1, 0), (0, "61/100", "403/100", "93/50")),
    (0, (0, 0, 1, 1, 1, 1), (0, "3/2", "3821/100", "29/50")),
    (0, (0, 1, 1, 1, 1, 0), (0, "38757/100", "9/10", "59/100")),
    (0, (0, 1, 1, 1, 2, 1), (0, "3/25", "73/100", "48/25")),
    (1, (0, 0, 0, 1, 1, 1), (0, "103/100", "17/50", "27/5")),
    (1, (0, 0, 1, 0, 1, 0), (0, "31/100", "23/50", "73/50")),
    (1, (0, 0, 1, 1, 0, 1), (0, "11/25", "381/50", "3/5")),
    (1, (0, 0, 1, 1, 1, 0), (0, "29/100", 4, "37/20")),
    (1, (0, 0, 1, 1, 1, 1), (0, "7/100", "13/5", "33/50")),
    (1, (0, 0, 1, 2, 0, 0), (0, "1047/100", "57/100", "12/25")),
    (1, (0, 1, 1, 1, 1, 0), (0, "161/50", "9/10", "3/5")),
    (1, (0, 1, 1, 2, 1, 1), (0, "1112/25", "69/50", "53/100")),
    (2, (0, 0, 1, 1, 2, 0), (0, "147/50", "17/100", "11/20")),
    (2, (0, 0, 1, 2, 1, 0), (0, "159/100", "9/50", "11/20")),
    (2, (0, 1, 0, 1, 1, 0), (0, "241/100", "81/100", "1/10")),
    (2, (0, 1, 1, 1, 0, 0), (0, "241/100", "81/100", "37/20")),
    (2, (0, 1, 1, 1, 2, 0), (0, "27/100", 1, "173/100")),
    (2, (0, 1, 1, 2, 1, 0), (0, "28367/100", "101/100", "43/25")),
    (2, (0, 1, 1, 2, 2, 0), (0, "17/100", "5/4", "161/100")),
    (2, (0, 1, 2, 2, 1, 0), (0, "549/100", "39/50", "111/100")),
    (3, (0, 0, 0, 2, 0, 0), (0, "11/4", "11/50", "821/100")),
    (3, (0, 0, 0, 2, 1, 0), (0, "21/25", "1/10", "1199/50")),
    (3, (0, 0, 1, 1, 1, 0), (0, "7/20", "443/50", "179/100")),
    (3, (0, 0, 1, 2, 0, 0), (0, "81/50", "3/100", "43/25")),
    (3, (0, 0, 1, 2, 1, 0), (0, "2/5", "267/50", "46/25")),
    (3, (0, 0, 2, 2, 0, 0), (0, "123/100", "1197/100", "26/25")),
    (3, (0, 0, 2, 2, 1, 0), (0, 4, "8/25", "21/25")),
    (3, (0, 1, 0, 2, 1, 0), (0, "11/25", "143/100", "249/50")),
    (3, (0, 1, 1, 2, 1, 0), (0, "106/25", "19/20", "29/50")),
    (3, (0, 1, 1, 3, 1, 0), (0, "7/50", "61/50", "41/25")),
    (3, (0, 1, 2, 2, 1, 0), (0, "1/10", "17/20", "27/25")),
    (4, (0, 0, 1, 1, 0, 0), (0, "123/50", "12/25", "23/25")),
    (4, (0, 0, 1, 1, 1, 1), (0, "409/100", "29/100", "47/50")),
    (4, (1, 0, 0, 0, 0, 1), (0, "99/100", "37/20", "11/20")),
    (4, (1, 0, 0, 0, 1, 1), (0, "3/4", "39/100", "37/5")),
    (4, (1, 0, 1, 0, 1, 0), (0, "71/100", "193/100", "48/25")),
    (4, (1, 0, 1, 0, 1, 1), (0, "47/25", "117/50", "33/50")),
    (4, (1, 0, 1, 1, 1, 1), (0, "81/50", "3/50", "3/5")),
)


BOUNDARY_CERTIFICATES = (
    (2, (0, 1, 1, 1, 1, 0),
     ((1, "1/2", -1, "-1/2"),
      ("1/2", 1, "-1/2", "-1/2"),
      (-1, "-1/2", 1, "1/2"),
      ("-1/2", "-1/2", "1/2", 1)),
     3),
)


RESIDUAL = (
    (4, (1, 1, 1, 1, 1, 1), "unresolved by rational Gram PSD search"),
    (4, (1, 1, 1, 1, 1, 2), "unresolved by rational Gram PSD search"),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def aut_canonical(kernel, row):
    return min(V.relabel(row, p) for p in V.automorphisms(kernel))


def old_failures():
    fixture = {(i, row): (parameters if parameters[0] == "x" else
                           tuple(Fraction(x) for x in parameters))
               for i, row, parameters in V.CERTIFICATES}
    failures = []
    for i, kernel in enumerate(V.KERNELS):
        for row in V.physical_rows(kernel):
            representative, bits, permutation = V.orbit_transport(kernel, row)
            parameters = fixture[(i, representative)]
            failed = parameters[0] == "x" and row != representative
            if not failed:
                try:
                    failed = V.transported_cost(
                        kernel, row, parameters, bits, permutation) > 3
                except RuntimeError:
                    failed = True
            if failed:
                failures.append((i, row))
    return tuple(failures)


def audit():
    certificates = {(i, row): tuple(Fraction(x) for x in parameters)
                    for i, row, parameters in ROW_CERTIFICATES}
    require(len(certificates) == 42, "row-certificate key count changed")
    boundary = {(i, row) for i, row, unused_matrix, unused_cost
                in BOUNDARY_CERTIFICATES}
    require(len(boundary) == 1, "boundary-certificate key count changed")
    residual = {(i, row) for i, row, unused in RESIDUAL}
    require(len(residual) == 2, "residual key count changed")

    worst = Fraction(0)
    for (i, row), parameters in certificates.items():
        require(row == aut_canonical(V.KERNELS[i], row),
                "certificate row is not automorphism-canonical")
        cost, matrix = V.certificate_cost(V.KERNELS[i], row, parameters)
        for size in range(1, 5):
            for indices in combinations(range(4), size):
                minor = V.determinant(V.principal_submatrix(matrix, indices))
                require(minor >= 0, "new Gram matrix is not exactly PSD")
        require(cost <= 3, "new physical-row excess exceeds three")
        worst = max(worst, cost)

    for i, row, matrix_data, displayed_cost in BOUNDARY_CERTIFICATES:
        matrix = tuple(tuple(Fraction(x) for x in line) for line in matrix_data)
        require(matrix == tuple(zip(*matrix)), "boundary Gram matrix is not symmetric")
        require(all(matrix[j][j] == 1 for j in range(4)),
                "boundary Gram diagonal changed")
        for size in range(1, 5):
            for indices in combinations(range(4), size):
                minor = V.determinant(V.principal_submatrix(matrix, indices))
                require(minor >= 0, "boundary Gram matrix is not exactly PSD")
        total = Fraction(0)
        square_for_correlation = {Fraction(-1): Fraction(1),
                                  Fraction(-1, 2): Fraction(1, 3)}
        for (u, v), multiplicity, odd_count in zip(
                V.pairs(), V.KERNELS[i], row):
            if not multiplicity:
                continue
            x = square_for_correlation[matrix[u][v]]
            total += odd_count * (1 - x) ** 2 / (4 * x)
            total += (multiplicity - odd_count) * 2 * x
        require(total == displayed_cost == 3,
                "boundary physical-row cost changed")
        require(row == aut_canonical(V.KERNELS[i], row),
                "boundary row is not automorphism-canonical")

    failures = old_failures()
    require(len(failures) == 72, "old failed-transport count changed")
    covered = 0
    residue = []
    for i, row in failures:
        key = (i, aut_canonical(V.KERNELS[i], row))
        if key in certificates or key in boundary:
            covered += 1
        else:
            require(key in residual, "failed row is absent from patch and residual")
            residue.append((i, row))
    require(covered == 70, "new exact physical-row coverage changed")
    require(len(residue) == 2, "physical residual count changed")
    require(Counter((i, aut_canonical(V.KERNELS[i], row))
                    for i, row in residue) == Counter(residual),
            "physical residual identity changed")
    return worst


def main():
    worst = audit()
    print("new_exact_automorphism_orbits: 43")
    print("new_exact_physical_rows: 70")
    print(f"maximum_new_exact_excess: {worst}")
    print("structural_residual_physical_rows: 2")
    for kernel, row, reason in RESIDUAL:
        print(f"residual: kernel={kernel} row={row} reason={reason}")


if __name__ == "__main__":
    main()
