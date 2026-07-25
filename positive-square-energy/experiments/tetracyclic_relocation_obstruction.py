#!/usr/bin/env python3
"""Exact obstruction to connector-middle leaf concentration in a tetracyclic cactus.

Build C5--P5--C5 with two triangles wedged at the left endpoint. Compare two
leaves split across the first/last internal connector vertices with both leaves
at the middle connector vertex. SymPy's exact characteristic polynomial and
rational Sturm isolation certify that the split placement has smaller s^+.
"""

import sympy as sp


def add_edge(edges, u, v):
    edges.add(tuple(sorted((u, v))))


def add_cycle(edges, vertices):
    for i, u in enumerate(vertices):
        add_edge(edges, u, vertices[(i + 1) % len(vertices)])


def adjacency(order, edges):
    matrix = sp.zeros(order)
    for u, v in edges:
        matrix[u, v] = matrix[v, u] = 1
    return matrix


def positive_square_bounds(poly, width=10**14):
    lower = sp.Rational(0)
    upper = sp.Rational(0)
    for factor, factor_multiplicity in sp.factor_list(poly)[1]:
        intervals = sp.polys.polytools.intervals(
            factor, eps=sp.Rational(1, width)
        )
        for interval, root_multiplicity in intervals:
            left, right = interval
            if left > 0:
                multiplicity = factor_multiplicity * root_multiplicity
                lower += multiplicity * left**2
                upper += multiplicity * right**2
    return lower, upper


def main():
    edges = set()
    add_cycle(edges, [0, 1, 2, 3, 4])
    add_edge(edges, 0, 5)
    add_edge(edges, 5, 6)
    add_edge(edges, 6, 7)
    add_edge(edges, 7, 8)
    add_cycle(edges, [8, 9, 10, 11, 12])
    add_cycle(edges, [0, 13, 14])
    add_cycle(edges, [0, 15, 16])

    x = sp.symbols("x")
    results = {}
    for name, leaf_edges in (
        ("split", [(5, 17), (7, 18)]),
        ("middle", [(6, 17), (6, 18)]),
    ):
        graph_edges = set(edges)
        for u, v in leaf_edges:
            add_edge(graph_edges, u, v)
        polynomial = sp.Poly(adjacency(19, graph_edges).charpoly(x).as_expr(), x)
        lower, upper = positive_square_bounds(polynomial)
        results[name] = (lower, upper)
        print(name)
        print(sp.factor(polynomial.as_expr()))
        print("slack rational interval:", lower - 19, upper - 19)
        print("slack decimal interval:", sp.N(lower - 19, 20), sp.N(upper - 19, 20))

    split_lower, split_upper = results["split"]
    middle_lower, middle_upper = results["middle"]
    assert split_upper < middle_lower
    print("CERTIFIED: s+(split) < s+(middle)")
    print("certified gap lower bound:", middle_lower - split_upper)


if __name__ == "__main__":
    main()
