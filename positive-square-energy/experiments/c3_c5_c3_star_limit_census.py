#!/usr/bin/env python3
"""Exact census of multi-root massive-star limits for both C3-C5-C3 cores."""

import sympy as sp

X = sp.symbols("x")
N = 9
WINNER = {5, 6, 7, 8}


def core(distance):
    edges = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
    edges |= {
        tuple(sorted(edge))
        for edge in (
            (0, 5), (0, 6), (5, 6),
            (distance, 7), (distance, 8), (7, 8),
        )
    }
    return sorted(edges)


def charpoly(vertices, edges):
    vertices = sorted(vertices)
    index = {vertex: i for i, vertex in enumerate(vertices)}
    matrix = sp.zeros(len(vertices))
    for u, v in edges:
        if u in index and v in index:
            matrix[index[u], index[v]] = matrix[index[v], index[u]] = 1
    return sp.Poly(matrix.charpoly(X).as_expr(), X, domain=sp.QQ)


def splus_lower(poly):
    lower = sp.Rational(0)
    for factor, factor_multiplicity in sp.factor_list(poly)[1]:
        for interval, root_multiplicity in factor.intervals(
            eps=sp.Rational(1, 10**12)
        ):
            left, _ = interval
            if left > 0:
                lower += factor_multiplicity * root_multiplicity * left**2
    return lower


def main():
    vertices = set(range(N))
    for distance in (1, 2):
        edges = core(distance)
        for mask in range(1 << N):
            selected = {v for v in vertices if (mask >> v) & 1}
            remaining = vertices - selected
            incident = sum(u in selected or v in selected for u, v in edges)
            polynomial = charpoly(remaining, edges)
            if selected == WINNER:
                assert incident == 6
                assert polynomial.as_expr() == X**5 - 5 * X**3 + 5 * X - 2
                continue
            lower_limit = incident - N + splus_lower(polynomial)
            assert lower_limit > sp.Rational(9, 5), (distance, selected, lower_limit)
        print(
            f"distance {distance}: unique subset below 9/5 is {sorted(WINNER)}; "
            "its exact limit is 4-sqrt(5)"
        )
    print("CERTIFIED: both 512-subset censuses pass")


if __name__ == "__main__":
    main()
