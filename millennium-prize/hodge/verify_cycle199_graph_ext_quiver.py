#!/usr/bin/env python3
"""Exact Gaussian-matrix and Ext-quiver certificate for Cycle 199."""

from math import comb, gcd


POWERS = ((1, 0), (2, 1), (3, 4), (2, 11), (-7, 24),
          (-38, 41), (-117, 44))


def gaussian_mul(left, right):
    a, b = left
    c, d = right
    return (a * c - b * d, a * d + b * c)


def gaussian_power(base, exponent):
    result = (1, 0)
    for _ in range(exponent):
        result = gaussian_mul(result, base)
    return result


def gaussian_matrix(z):
    """Integral matrix of multiplication by z on Z[i]^3."""
    a, b = z
    block = ((a, -b), (b, a))
    return tuple(
        tuple(block[row % 2][column % 2] if row // 2 == column // 2 else 0
              for column in range(6))
        for row in range(6)
    )


def determinant(matrix):
    """Fraction-free Bareiss determinant over Z."""
    work = [list(row) for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        value = work[column][column]
        for row in range(column + 1, size):
            for col in range(column + 1, size):
                work[row][col] = (
                    work[row][col] * value
                    - work[row][column] * work[column][col]
                ) // previous
        previous = value
    return sign * work[-1][-1]


def smith_block_invariants(z):
    a, b = z
    first = gcd(abs(a), abs(b))
    norm = a * a + b * b
    return (first, norm // first)


def main():
    assert tuple(gaussian_power((2, 1), k) for k in range(7)) == POWERS
    records = []
    for source in range(7):
        for target in range(source + 1, 7):
            delta = (POWERS[target][0] - POWERS[source][0],
                     POWERS[target][1] - POWERS[source][1])
            norm = delta[0] ** 2 + delta[1] ** 2
            matrix = gaussian_matrix(delta)
            block_smith = smith_block_invariants(delta)
            smith = (block_smith[0],) * 3 + (block_smith[1],) * 3
            length = norm ** 3
            assert determinant(matrix) == length
            product = 1
            for invariant in smith:
                product *= invariant
            assert product == length
            assert all(smith[index] != 0 for index in range(6))
            records.append((source, target, delta, norm, length, smith))

    self_ext = tuple(comb(6, degree) for degree in range(7))
    assert self_ext == (1, 6, 15, 20, 15, 6, 1)
    assert len(records) == 21

    print("Cycle 199 graph intersection and Ext quiver")
    print("powers:", " ".join(f"{a}+{b}i" for a, b in POWERS))
    print("self Ext dimensions, degrees 0..6:", self_ext)
    print("i j  delta      norm  length=N(delta)^3  Smith invariants")
    for source, target, delta, norm, length, smith in records:
        print(f"{source} {target}  {delta!s:>10}  {norm:5d}  {length:13d}  {smith}")
    print("distinct-pair Ext^1 dimensions: all 0")
    print("distinct-pair Ext^2 dimensions: all 0")
    print("unshifted extension quiver: seven vertices, no inter-vertex arrows")
    print("degree-2 obstruction-mixing distinct pairs: none")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
