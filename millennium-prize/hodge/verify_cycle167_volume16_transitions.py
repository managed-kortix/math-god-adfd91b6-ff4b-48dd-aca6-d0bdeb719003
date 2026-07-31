#!/usr/bin/env python3
"""Exact binary enumeration for the Cycle 167 transition matrix."""

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd


TYPES = ((1, 1, 16), (1, 2, 8), (1, 4, 4), (2, 2, 4))
EXPECTED = {
    (1, 1, 16): (180, 15, 0, 0),
    (1, 2, 8): (192, 228, 12, 3),
    (1, 4, 4): (0, 240, 180, 15),
    (2, 2, 4): (0, 960, 240, 195),
}


def binary_rank(columns):
    pivots = {}
    for column in columns:
        value = sum(bit << i for i, bit in enumerate(column))
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def span_key(columns):
    values = []
    for mask in range(8):
        value = 0
        for i, column in enumerate(columns):
            if (mask >> i) & 1:
                value ^= sum(bit << j for j, bit in enumerate(column))
        values.append(value)
    return tuple(sorted(values))


def all_three_spaces():
    vectors = [tuple((n >> j) & 1 for j in range(6)) for n in range(1, 64)]
    spaces = {}
    for columns in combinations(vectors, 3):
        if binary_rank(columns) == 3:
            spaces.setdefault(span_key(columns), columns)
    assert len(spaces) == 1395
    return spaces.values()


def pairing(left, form, right):
    return sum(left[i] * form[i][j] * right[j] for i in range(6) for j in range(6))


def quotient_basis(columns):
    columns = [list(column) for column in columns]
    pivots = []
    for row in range(6):
        selected = next((j for j in range(len(pivots), 3) if columns[j][row]), None)
        if selected is None:
            continue
        columns[len(pivots)], columns[selected] = columns[selected], columns[len(pivots)]
        selected = len(pivots)
        for j in range(3):
            if j != selected and columns[j][row]:
                columns[j] = [x ^ y for x, y in zip(columns[j], columns[selected])]
        pivots.append(row)
    basis = [[Fraction(x, 2) for x in column] for column in columns]
    basis += [
        [Fraction(i == row) for i in range(6)]
        for row in range(6)
        if row not in pivots
    ]
    return basis


def pfaffian4(form, indices):
    a, b, c, d = indices
    return (
        form[a][b] * form[c][d]
        - form[a][c] * form[b][d]
        + form[a][d] * form[b][c]
    )


def pfaffian6(form):
    total = 0
    for j in range(1, 6):
        remainder = [i for i in range(1, 6) if i != j]
        total += (-1 if j % 2 == 0 else 1) * form[0][j] * pfaffian4(form, remainder)
    return total


def alternating_type(form):
    d1 = gcd(*(abs(entry) for row in form for entry in row))
    pfaffians = (abs(pfaffian4(form, indices)) for indices in combinations(range(6), 4))
    d1d2 = gcd(*pfaffians)
    d1d2d3 = abs(pfaffian6(form))
    return d1, d1d2 // d1, d1d2d3 // d1d2


def transition_counts(source, spaces):
    form = [[0] * 6 for _ in range(6)]
    for i, divisor in enumerate(source):
        form[2 * i][2 * i + 1] = divisor
        form[2 * i + 1][2 * i] = -divisor
    counts = Counter()
    for columns in spaces:
        if any(pairing(x, form, y) % 2 for x in columns for y in columns):
            continue
        basis = quotient_basis(columns)
        target_form = [
            [2 * pairing(basis[i], form, basis[j]) for j in range(6)]
            for i in range(6)
        ]
        assert all(entry.denominator == 1 for row in target_form for entry in row)
        counts[alternating_type([[int(entry) for entry in row] for row in target_form])] += 1
    return tuple(counts[target] for target in TYPES)


def main():
    spaces = tuple(all_three_spaces())
    for source in TYPES:
        counts = transition_counts(source, spaces)
        assert counts == EXPECTED[source], (source, counts)
        print(source, counts, "total", sum(counts))
    print("All Cycle 167 transition counts verified exactly.")


if __name__ == "__main__":
    main()
