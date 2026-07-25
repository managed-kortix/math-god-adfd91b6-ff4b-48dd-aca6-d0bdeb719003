#!/usr/bin/env python3
"""Exact audit of the two-root connector continuant."""

from __future__ import annotations

import random
from itertools import combinations

import sympy as sp


def continuant(xs: list[sp.Expr]) -> sp.Expr:
    """K()=1 and K(x1,...,xn)=xn*K(x1,...,x[n-1])+K(x1,...,x[n-2])."""
    km2 = sp.Integer(1)
    if not xs:
        return km2
    km1 = xs[0]
    for x in xs[1:]:
        km2, km1 = km1, sp.expand(x * km1 + km2)
    return km1


def connector_formula(m: int, aa: list[sp.Expr], r1: sp.Expr, r2: sp.Expr) -> sp.Expr:
    if m == 0:
        return 1 + r1 * r2
    if m == 1:
        return aa[0] + r1 + r2
    return continuant([aa[0] + r1, *aa[1:-1], aa[-1] + r2])


def unnormalized_connector(
    m: int,
    aa: list[sp.Expr],
    z1: sp.Expr,
    w1: sp.Expr,
    z2: sp.Expr,
    w2: sp.Expr,
) -> sp.Expr:
    """Characteristic carrier before division by the two lobe factors."""
    if m == 0:
        return z1 * z2 + w1 * w2
    if m == 1:
        return aa[0] * z1 * z2 + w1 * z2 + z1 * w2
    return sp.cancel(z1 * z2 * connector_formula(m, aa, w1 / z1, w2 / z2))


def matching_sum(m: int, aa: list[sp.Expr], r1: sp.Expr, r2: sp.Expr) -> sp.Expr:
    """Enumerate matchings of the path, including its two boundary edges."""
    if m == 0:
        return 1 + r1 * r2

    # Edges 0 and m are the left and right boundary edges. Internal vertices
    # are 1,...,m, and a selected boundary edge has weight r1 or r2.
    total = 0
    for size in range((m + 2) // 2 + 1):
        for chosen in combinations(range(m + 1), size):
            if any(v == u + 1 for u, v in zip(chosen, chosen[1:])):
                continue
            covered = set()
            weight = sp.Integer(1)
            for edge in chosen:
                if edge == 0:
                    weight *= r1
                    covered.add(1)
                elif edge == m:
                    weight *= r2
                    covered.add(m)
                else:
                    covered.update((edge, edge + 1))
            for vertex in range(1, m + 1):
                if vertex not in covered:
                    weight *= aa[vertex - 1]
            total += weight
    return sp.expand(total)


def tridiagonal_factor(m: int, aa: list[sp.Expr], r1: sp.Expr, r2: sp.Expr) -> sp.Expr:
    if m == 0:
        return 1 + r1 * r2
    diagonal = list(aa)
    diagonal[0] += r1
    diagonal[-1] += r2
    matrix = sp.diag(*diagonal)
    for j in range(m - 1):
        matrix[j, j + 1] = sp.I
        matrix[j + 1, j] = sp.I
    return sp.expand(matrix.det())


def normalized_characteristic(vertices: set[int], edges: set[tuple[int, int]], t: int) -> sp.Expr:
    order = sorted(vertices)
    index = {v: j for j, v in enumerate(order)}
    matrix = sp.eye(len(order)) * t
    for u, v in edges:
        if u in index and v in index:
            matrix[index[u], index[v]] = sp.I
            matrix[index[v], index[u]] = sp.I
    return sp.expand(matrix.det())


def random_lobe(rng: random.Random, start: int) -> tuple[set[int], set[tuple[int, int]], int, int]:
    cycle_order = rng.randint(3, 6)
    vertices = set(range(start, start + cycle_order))
    edges = {
        tuple(sorted((start + j, start + (j + 1) % cycle_order)))
        for j in range(cycle_order)
    }
    next_vertex = start + cycle_order
    for _ in range(rng.randint(0, 3)):
        parent = rng.choice(sorted(vertices))
        vertices.add(next_vertex)
        edges.add(tuple(sorted((parent, next_vertex))))
        next_vertex += 1
    root = rng.choice(range(start, start + cycle_order))
    return vertices, edges, root, next_vertex


def random_cactus_check(seed: int = 20260725, trials: int = 10) -> int:
    rng = random.Random(seed)
    checks = 0
    for m in range(7):
        for _ in range(trials):
            left_v, left_e, left_root, next_vertex = random_lobe(rng, 0)
            right_v, right_e, right_root, next_vertex = random_lobe(rng, next_vertex)
            internal = list(range(next_vertex, next_vertex + m))
            next_vertex += m
            path = [left_root, *internal, right_root]
            path_edges = {tuple(sorted(edge)) for edge in zip(path, path[1:])}

            # Random pendant leaves exercise the effective internal activities
            # a_j=t+k_j/t and their common positive prefactor t**sum(k_j).
            leaf_counts = []
            leaf_edges: set[tuple[int, int]] = set()
            leaves: set[int] = set()
            for vertex in internal:
                count = rng.randint(0, 2)
                leaf_counts.append(count)
                for _ in range(count):
                    leaves.add(next_vertex)
                    leaf_edges.add(tuple(sorted((vertex, next_vertex))))
                    next_vertex += 1

            vertices = left_v | right_v | set(internal) | leaves
            edges = left_e | right_e | path_edges | leaf_edges
            t = rng.randint(1, 4)
            actual = normalized_characteristic(vertices, edges, t)
            z1 = normalized_characteristic(left_v, left_e, t)
            w1 = normalized_characteristic(left_v - {left_root}, left_e, t)
            z2 = normalized_characteristic(right_v, right_e, t)
            w2 = normalized_characteristic(right_v - {right_root}, right_e, t)
            aa = [sp.Rational(t) + sp.Rational(k, t) for k in leaf_counts]
            prefactor = sp.Integer(t) ** sum(leaf_counts)
            expected = z1 * z2 * prefactor * connector_formula(m, aa, w1 / z1, w2 / z2)
            assert sp.simplify(actual - expected) == 0
            checks += 1
    return checks


def main() -> None:
    r1, r2 = sp.symbols("r1 r2")
    z1, w1, z2, w2 = sp.symbols("z1 w1 z2 w2")
    activities = list(sp.symbols("a1:7"))
    for m in range(7):
        aa = activities[:m]
        formula = connector_formula(m, aa, r1, r2)
        matching = matching_sum(m, aa, r1, r2)
        determinant = tridiagonal_factor(m, aa, r1, r2)
        assert sp.expand(formula - matching) == 0
        assert sp.expand(formula - determinant) == 0
        carrier = unnormalized_connector(m, aa, z1, w1, z2, w2)
        assert sp.cancel(carrier / (z1 * z2) - formula.subs({r1: w1 / z1, r2: w2 / z2})) == 0
        assert not carrier.as_numer_denom()[1].has(z1, z2)
        print(f"m={m}: {formula}")
    checks = random_cactus_check()
    print(f"exact random cactus checks: {checks}/{checks}")


if __name__ == "__main__":
    main()
