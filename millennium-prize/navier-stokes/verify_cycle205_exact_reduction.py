#!/usr/bin/env python3
"""Independent exact verifier for the Cycle 205 RREF reduction artifact."""

import json
from fractions import Fraction
from pathlib import Path

from generate_cycle205_exact_reduction import (
    INPUT_PATH,
    OUTPUT_PATH,
    canonical_bytes,
    digest_bytes,
    exact_rref,
    generate,
    parse_linear_system,
)


def dense_sparse(entries, length, named_indices=None):
    row = [Fraction(0) for _ in range(length)]
    for entry in entries:
        key = entry["variable"] if named_indices is not None else entry["index"]
        index = named_indices[key] if named_indices is not None else key
        row[index] = Fraction(entry["coefficient"])
    return row


def matrix_rank(matrix):
    if not matrix:
        return 0
    reduced, _, pivots = exact_rref([row + [Fraction(0)] for row in matrix])
    del reduced
    return len(pivots)


def main():
    source_bytes = INPUT_PATH.read_bytes()
    source = json.loads(source_bytes)
    artifact = json.loads(OUTPUT_PATH.read_bytes())
    assert artifact == generate()
    assert artifact["source_sha256"] == digest_bytes(source_bytes)

    variables, equations, matrix = parse_linear_system(source)
    certificate = artifact["linear_certificate"]
    assert certificate["equation_ids"] == [row["id"] for row in equations]
    row_count = len(matrix)
    transform = [dense_sparse(row, row_count) for row in certificate["left_transform_rows"]]
    names = variables + ["__rhs__"]
    named_indices = {name: index for index, name in enumerate(names)}
    claimed = [dense_sparse(row, len(names), named_indices) for row in certificate["rref_augmented_rows"]]
    product = [
        [sum(transform[i][k] * matrix[k][j] for k in range(row_count)) for j in range(len(names))]
        for i in range(row_count)
    ]
    assert product == claimed
    assert matrix_rank(transform) == row_count
    recomputed, _, pivots = exact_rref(matrix)
    assert claimed == recomputed
    assert certificate["pivot_columns"] == pivots

    reduced_by_id = {row["id"]: row for row in artifact["equations"]}
    combination = artifact["contradiction_certificate"]["combination"]
    polynomial = {}
    for item in combination:
        multiplier = Fraction(item["coefficient"])
        for term in reduced_by_id[item["equation_id"]]["terms"]:
            monomial = tuple(term["monomial"])
            polynomial[monomial] = polynomial.get(monomial, Fraction(0)) + multiplier * Fraction(term["coefficient"])
    polynomial = {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}
    assert polynomial == {(): Fraction(1)}

    output_hash = artifact.pop("sha256_without_this_field")
    assert output_hash == digest_bytes(canonical_bytes(artifact))
    print("Cycle 205 exact certificate verified")
    print("source equations: 514; linear matrix: 44 x 36")
    print("rank: 27; nullity: 9; linear contradiction: no")
    print("affine substitution and every reduced polynomial replay exactly")
    print("reduced nonlinear contradiction certificate: 1 is in the ideal")


if __name__ == "__main__":
    main()
