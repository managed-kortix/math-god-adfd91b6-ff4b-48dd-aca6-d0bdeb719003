#!/usr/bin/env python3
"""Enumerate norm-one 6-by-3 matrices modulo Q(i)-row span."""

import argparse
from collections import Counter, deque
from fractions import Fraction
import json


ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
UNITS = (ZERO, ONE, (-ONE[0], ONE[1]), (ONE[1], ONE[0]), (ONE[1], -ONE[0]))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def inv(a):
    norm = a[0] * a[0] + a[1] * a[1]
    if norm == 0:
        raise ZeroDivisionError
    return (a[0] / norm, -a[1] / norm)


def div(a, b):
    return mul(a, inv(b))


def rref(rows):
    matrix = [list(row) for row in rows if any(entry != ZERO for entry in row)]
    pivot_row = 0
    for column in range(3):
        pivot = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column] != ZERO),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inv(matrix[pivot_row][column])
        matrix[pivot_row] = [mul(scale, entry) for entry in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row or matrix[index][column] == ZERO:
                continue
            scale = matrix[index][column]
            matrix[index] = [
                sub(entry, mul(scale, pivot_entry))
                for entry, pivot_entry in zip(matrix[index], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def restricted_rank(space, columns):
    return len(rref(tuple(tuple(row[column] for column in columns) + (ZERO,) for row in space)))


def pair_rank_two(space):
    return all(restricted_rank(space, pair) == 2 for pair in ((1, 2), (0, 2), (0, 1)))


def full_support(space):
    return all(any(row[column] != ZERO for row in space) for column in range(3))


def encode_number(value):
    real, imag = value
    if imag == 0:
        return str(real)
    if real == 0:
        return f"{imag}*i"
    sign = "+" if imag > 0 else "-"
    return f"{real}{sign}{abs(imag)}*i"


def encode_space(space):
    return [[encode_number(entry) for entry in row] for row in space]


def enumerate_spaces(rows):
    empty = ()
    spaces = {empty}
    queue = deque([empty])
    while queue:
        space = queue.popleft()
        for row in rows:
            extension = rref(space + (row,))
            if extension not in spaces:
                spaces.add(extension)
                queue.append(extension)
    return spaces


def matrix_counts(rows):
    counts = {(): 1}
    for _ in range(6):
        next_counts = Counter()
        for space, count in counts.items():
            for row in rows:
                next_counts[rref(space + (row,))] += count
        counts = dict(next_counts)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--representatives", action="store_true")
    args = parser.parse_args()
    rows = tuple((a, b, c) for a in UNITS for b in UNITS for c in UNITS)
    spaces = enumerate_spaces(rows)
    counts = matrix_counts(rows)
    if set(counts) != spaces:
        raise AssertionError("six rows do not realize every generated row space")
    if sum(counts.values()) != 5**18:
        raise AssertionError("matrix count does not sum to 5^18")

    by_rank = Counter(len(space) for space in spaces)
    matrices_by_rank = Counter()
    for space, count in counts.items():
        matrices_by_rank[len(space)] += count
    survivors = [space for space in spaces if pair_rank_two(space)]
    survivor_matrices = sum(counts[space] for space in survivors)
    supported_spaces = [space for space in spaces if full_support(space)]
    supported_matrix_count = sum(counts[space] for space in supported_spaces)
    supported_classes_by_rank = Counter(len(space) for space in supported_spaces)
    supported_matrices_by_rank = Counter()
    for space in supported_spaces:
        supported_matrices_by_rank[len(space)] += counts[space]
    support_survivors = (5**6 - 1) ** 3
    if supported_matrix_count != support_survivors:
        raise AssertionError("row-space support count disagrees with direct column count")
    result = {
        "allowed_rows": len(rows),
        "row_space_classes": len(spaces),
        "classes_by_rank": dict(sorted(by_rank.items())),
        "matrices_by_rank": dict(sorted(matrices_by_rank.items())),
        "all_columns_nonzero_matrices": support_survivors,
        "all_columns_nonzero_classes": len(supported_spaces),
        "all_columns_nonzero_classes_by_rank": dict(sorted(supported_classes_by_rank.items())),
        "all_columns_nonzero_matrices_by_rank": dict(sorted(supported_matrices_by_rank.items())),
        "zero_column_rejections": 5**18 - support_survivors,
        "pair_rank_two_classes": len(survivors),
        "pair_rank_two_matrices": survivor_matrices,
        "pair_rank_below_two_matrices": 5**18 - survivor_matrices,
        "total_matrices": 5**18,
    }
    if args.representatives:
        result["pair_rank_two_representatives"] = [
            encode_space(space) for space in sorted(survivors, key=encode_space)
        ]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
