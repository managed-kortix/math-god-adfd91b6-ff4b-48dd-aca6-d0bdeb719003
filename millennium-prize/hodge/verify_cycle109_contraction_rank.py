#!/usr/bin/env python3
"""Exact exterior-algebra verifier for the quartic-CM contraction rank."""

from fractions import Fraction
from itertools import combinations


def wedge(left, right):
    if set(left) & set(right):
        return None, 0
    inversions = sum(a > b for a in left for b in right)
    return tuple(sorted(left + right)), -1 if inversions % 2 else 1


def add(out, monomial, coefficient):
    if monomial is not None and coefficient:
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if not out[monomial]:
            del out[monomial]


def wedge_forms(left, right):
    out = {}
    for ml, cl in left.items():
        for mr, cr in right.items():
            m, sign = wedge(ml, mr)
            add(out, m, cl * cr * sign)
    return out


def contract(form, index):
    out = {}
    for monomial, coefficient in form.items():
        if index in monomial:
            position = monomial.index(index)
            reduced = monomial[:position] + monomial[position + 1:]
            add(out, reduced, coefficient * (-1 if position % 2 else 1))
    return out


def scale(form, scalar):
    return {m: scalar * c for m, c in form.items() if scalar * c}


def gaussian_rank(matrix):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    rank = pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        value = a[pivot_row][col]
        a[pivot_row] = [x / value for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [x - factor * y for x, y in zip(a[r], a[pivot_row])]
        rank += 1
        pivot_row += 1
    return rank


def rank_for(eigenvalues, q=Fraction(1)):
    # x_i (i=0,...,3) is a basis of H^(1,0), y_i=4+i of H^(0,1).
    # Tangent index i denotes the vector dual to x_i.
    assert q
    a = [u * u for u in eigenvalues]
    c = [Fraction(1, 1) / value for value in a]
    ch1 = {(i, 4 + i): a[i] for i in range(4)}
    theta_inv = {(i, 4 + i): c[i] for i in range(4)}
    ch3 = scale(wedge_forms(wedge_forms(theta_inv, theta_inv), theta_inv),
                Fraction(-1, 6) * q)

    sources = []
    # H^2(O), H^1(T), H^0(wedge^2 T).
    sources += [("u", ij) for ij in combinations(range(4, 8), 2)]
    sources += [("v", (i, j)) for i in range(4) for j in range(4, 8)]
    sources += [("w", ij) for ij in combinations(range(4), 2)]

    images = []
    for kind, indices in sources:
        if kind == "u":
            images.append(wedge_forms({indices: Fraction(1)}, ch1))
        elif kind == "v":
            i, y = indices
            image = wedge_forms({(y,): Fraction(1)}, contract(ch1, i))
            high = wedge_forms({(y,): Fraction(1)}, contract(ch3, i))
            for m, coefficient in high.items():
                add(image, m, coefficient)
            images.append(image)
        else:
            i, j = indices
            # i_(x_i wedge x_j) = i_(x_j) i_(x_i).
            images.append(contract(contract(ch3, i), j))

    targets = sorted(set().union(*(image.keys() for image in images)))
    matrix = [[image.get(target, Fraction(0)) for image in images]
              for target in targets]
    return gaussian_rank(matrix), len(sources), len(targets)


def main():
    rank, source_dim, target_dim = rank_for(
        [Fraction(2), Fraction(2), Fraction(1, 2), Fraction(1, 2)]
    )
    # The abstract semiregularity target has dimension 28, but ch_1+ch_3
    # reaches a fixed 24-dimensional coordinate subspace of it.
    assert source_dim == 28 and target_dim == 24
    assert rank == 20
    distinct_rank, _, _ = rank_for(
        [Fraction(2), Fraction(3), Fraction(5), Fraction(7)]
    )
    assert distinct_rank == 24
    print("RM multiplicity (2,2): rank 20, nullity 8")
    print("four distinct eigenvalues: rank 24, nullity 4")


if __name__ == "__main__":
    main()
