#!/usr/bin/env python3
"""Exact finite audit of the all-degree Fermat-plane pivot proof.

Finite runs check the combinatorics.  The all-degree conclusion rests on the
symbolic private-pivot argument, not extrapolation from the tested range.
"""

import argparse
import math
from itertools import product


def source_basis(d):
    if d < 3:
        raise ValueError("require d >= 3")
    cap = d - 2
    return tuple(a for a in product(range(cap + 1), repeat=3) if sum(a) == d)


def output_monomial(d, a, j):
    cap = d - 2
    return tuple(e for i in range(3) for e in (a[i] + cap - j[i], j[i]))


def support(d, a):
    cap = d - 2
    return tuple(output_monomial(d, a, j)
                 for j in product(*(range(a_i, cap + 1) for a_i in a)))


def pivot(d, a):
    cap = d - 2
    return tuple(e for a_i in a for e in (cap, a_i))


def verify_degree(d):
    basis = source_basis(d)
    expected = math.comb(d + 2, 2) - 9
    assert len(basis) == expected, (d, len(basis), expected)
    owners = {}
    for a in basis:
        terms = support(d, a)
        assert len(terms) == len(set(terms))
        for monomial in terms:
            assert max(monomial) <= d - 2
            assert sum(monomial) == 4 * d - 6
            owners.setdefault(monomial, set()).add(a)
        assert pivot(d, a) in terms
    assert len({pivot(d, a) for a in basis}) == len(basis)
    for a in basis:
        assert owners[pivot(d, a)] == {a}
    return len(basis), sum(len(support(d, a)) for a in basis)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--d-min", type=int, default=3)
    parser.add_argument("--d-max", type=int, default=20)
    args = parser.parse_args()
    if args.d_min < 3 or args.d_max < args.d_min:
        parser.error("require 3 <= d-min <= d-max")
    for d in range(args.d_min, args.d_max + 1):
        dimension, incidences = verify_degree(d)
        print(f"d={d}: dim={dimension}; support incidences={incidences}: PASS")
    print("finite audit passed; all-d theorem uses the symbolic pivot proof")


if __name__ == "__main__":
    main()
