#!/usr/bin/env python3
"""Exact no-go certificate for replacing rooted trees by same-root stars."""

import sympy as sp

X = sp.symbols("x")


def core(distance):
    edges = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
    edges |= {
        tuple(sorted(edge))
        for edge in (
            (0, 5), (0, 6), (5, 6),
            (distance, 7), (distance, 8), (7, 8),
        )
    }
    return edges


def polynomial(distance, root, shape):
    edges = core(distance)
    if shape == "path":
        edges |= {tuple(sorted((root, 9))), (9, 10)}
    elif shape == "star":
        edges |= {tuple(sorted((root, 9))), tuple(sorted((root, 10)))}
    else:
        raise ValueError(shape)
    matrix = sp.zeros(11)
    for u, v in edges:
        matrix[u, v] = matrix[v, u] = 1
    return sp.Poly(matrix.charpoly(X).as_expr(), X)


def splus_bounds(poly):
    lower = sp.Rational(0)
    upper = sp.Rational(0)
    for factor, factor_multiplicity in sp.factor_list(poly)[1]:
        for interval, root_multiplicity in factor.intervals(
            eps=sp.Rational(1, 10**15)
        ):
            left, right = interval
            if left > 0:
                multiplicity = factor_multiplicity * root_multiplicity
                lower += multiplicity * left**2
                upper += multiplicity * right**2
    return lower, upper


def certify(distance, root, expected_relation):
    path_poly = polynomial(distance, root, "path")
    star_poly = polynomial(distance, root, "star")
    path_lower, path_upper = splus_bounds(path_poly)
    star_lower, star_upper = splus_bounds(star_poly)
    if expected_relation == "path<star":
        assert path_upper < star_lower
        gap = star_lower - path_upper
    else:
        assert star_upper < path_lower
        gap = path_lower - star_upper
    print(f"distance={distance}, root={root}: {expected_relation}")
    print(" path polynomial:", sp.factor(path_poly.as_expr()))
    print(" star polynomial:", sp.factor(star_poly.as_expr()))
    print(" path s+ interval:", sp.N(path_lower, 18), sp.N(path_upper, 18))
    print(" star s+ interval:", sp.N(star_lower, 18), sp.N(star_upper, 18))
    print(" certified gap lower bound:", gap)


def main():
    # At these pentagon roots, the rooted path has smaller positive square
    # energy than the two-leaf star of the same order.
    certify(1, 4, "path<star")
    certify(2, 1, "path<star")
    # At a private triangle root the direction reverses, so neither shape
    # dominates the other uniformly across roots.
    certify(1, 7, "star<path")
    certify(2, 7, "star<path")
    print("CERTIFIED: no uniform same-root path/star domination exists")


if __name__ == "__main__":
    main()
