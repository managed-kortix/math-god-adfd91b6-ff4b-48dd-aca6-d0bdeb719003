#!/usr/bin/env python3
"""Exact coefficient certificates for four shared-cut {3,5,5} cores."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from functools import lru_cache

import sympy as sp


Cycle = tuple[int, ...]
Edge = tuple[int, int]


@dataclass(frozen=True)
class Core:
    name: str
    triangle: Cycle
    pentagon_p: Cycle
    pentagon_q: Cycle
    expected_intersections: tuple[frozenset[int], frozenset[int], frozenset[int]]
    expected_terms: int
    expected_sha256: str

    @property
    def cycles(self) -> tuple[Cycle, Cycle, Cycle]:
        return self.triangle, self.pentagon_p, self.pentagon_q


CORES = (
    Core(
        name="bouquet",
        triangle=(0, 1, 2),
        pentagon_p=(0, 3, 4, 5, 6),
        pentagon_q=(0, 7, 8, 9, 10),
        expected_intersections=(frozenset({0}), frozenset({0}), frozenset({0})),
        expected_terms=2547,
        expected_sha256="8112f2944f9823177afd48deccfb958ac960548e09d9d838e4965c33eb39e979",
    ),
    Core(
        name="triangle_middle_distinct_vertices",
        triangle=(0, 1, 2),
        pentagon_p=(0, 3, 4, 5, 6),
        pentagon_q=(1, 7, 8, 9, 10),
        expected_intersections=(frozenset({0}), frozenset({1}), frozenset()),
        expected_terms=2192,
        expected_sha256="4fdb04cee38f0c0e2ac2de6dff7e641c2e190a3c018af8308a5c69e378de2ba2",
    ),
    Core(
        name="pentagon_middle_cut_distance_1",
        triangle=(0, 5, 6),
        pentagon_p=(0, 1, 2, 3, 4),
        pentagon_q=(1, 7, 8, 9, 10),
        expected_intersections=(frozenset({0}), frozenset(), frozenset({1})),
        expected_terms=2925,
        expected_sha256="bfa73346f169f28ec6109418ce22fe44daaae6b081ade30074932b139f0828f4",
    ),
    Core(
        name="pentagon_middle_cut_distance_2",
        triangle=(0, 5, 6),
        pentagon_p=(0, 1, 2, 3, 4),
        pentagon_q=(2, 7, 8, 9, 10),
        expected_intersections=(frozenset({0}), frozenset(), frozenset({2})),
        expected_terms=2895,
        expected_sha256="5c6c213471a856cb743afda8e62407d7d27de5984b612c70ab411499011db437",
    ),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def cycle_edges(cycle: Cycle) -> frozenset[Edge]:
    return frozenset(
        tuple(sorted((cycle[index], cycle[(index + 1) % len(cycle)])))
        for index in range(len(cycle))
    )


def matching_partition(
    vertices: frozenset[int],
    edges: frozenset[Edge],
    activities: tuple[sp.Symbol, ...],
) -> sp.Expr:
    """Enumerate Z on an induced vertex set by exposing its least vertex."""

    @lru_cache(maxsize=None)
    def recurse(remaining: frozenset[int]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        vertex = min(remaining)
        rest = remaining - {vertex}
        result = activities[vertex] * recurse(rest)
        for neighbor in sorted(rest):
            if tuple(sorted((vertex, neighbor))) in edges:
                result += recurse(rest - {neighbor})
        return result

    return recurse(vertices)


def validate_core(core: Core) -> tuple[frozenset[int], frozenset[Edge]]:
    require(tuple(map(len, core.cycles)) == (3, 5, 5), f"{core.name}: wrong cycle lengths")
    require(
        all(len(set(cycle)) == len(cycle) for cycle in core.cycles),
        f"{core.name}: a listed cycle repeats a vertex",
    )
    intersections = (
        frozenset(core.triangle) & frozenset(core.pentagon_p),
        frozenset(core.triangle) & frozenset(core.pentagon_q),
        frozenset(core.pentagon_p) & frozenset(core.pentagon_q),
    )
    require(
        intersections == core.expected_intersections,
        f"{core.name}: cycle intersections are {intersections}",
    )
    edge_sets = tuple(cycle_edges(cycle) for cycle in core.cycles)
    require(
        all(not (edge_sets[i] & edge_sets[j]) for i in range(3) for j in range(i + 1, 3)),
        f"{core.name}: cycle blocks share an edge",
    )
    vertices = frozenset().union(*(frozenset(cycle) for cycle in core.cycles))
    edges = frozenset().union(*edge_sets)
    require(vertices == frozenset(range(11)), f"{core.name}: vertices are not exactly 0,...,10")
    require(len(edges) == 13, f"{core.name}: expected 13 edges, got {len(edges)}")
    return vertices, edges


def deleted_partition(
    deleted_cycles: tuple[Cycle, ...],
    vertices: frozenset[int],
    edges: frozenset[Edge],
    activities: tuple[sp.Symbol, ...],
) -> sp.Expr:
    deleted = frozenset().union(*(frozenset(cycle) for cycle in deleted_cycles))
    return matching_partition(vertices - deleted, edges, activities)


def certificate(core: Core) -> tuple[sp.Poly, sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    vertices, edges = validate_core(core)
    activities = sp.symbols("a0:11", positive=True)

    z_h = matching_partition(vertices, edges, activities)
    cycles = core.cycles
    pair_terms: list[tuple[int, sp.Expr]] = []
    for left_index, left in enumerate(cycles):
        for right in cycles[left_index + 1 :]:
            if frozenset(left).isdisjoint(right):
                multiplier = 4 if len(left) != len(right) else -4
                pair_terms.append(
                    (multiplier, deleted_partition((left, right), vertices, edges, activities))
                )

    # Sachs multipliers are -2i for C3 and +2i for C5. No three cycles
    # are pairwise disjoint in any of the four shared-cut configurations.
    real_part = z_h + sum(multiplier * term for multiplier, term in pair_terms)
    imaginary_part = (
        -2 * deleted_partition((core.triangle,), vertices, edges, activities)
        + 2 * deleted_partition((core.pentagon_p,), vertices, edges, activities)
        + 2 * deleted_partition((core.pentagon_q,), vertices, edges, activities)
    )
    p = matching_partition(
        frozenset(core.pentagon_p), cycle_edges(core.pentagon_p), activities
    )
    q = matching_partition(
        frozenset(core.pentagon_q), cycle_edges(core.pentagon_q), activities
    )
    phi = sp.Poly(2 * real_part * (p + q) - imaginary_part * (p * q - 4), *activities, domain=sp.ZZ)
    return phi, real_part, imaginary_part, p, q


def term_digest(polynomial: sp.Poly) -> str:
    payload = "\n".join(
        f"{monomial}:{coefficient}" for monomial, coefficient in polynomial.terms()
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    for core in CORES:
        phi, real_part, imaginary_part, p, q = certificate(core)
        terms = phi.terms()
        coefficients = phi.coeffs()
        digest = term_digest(phi)

        require(len(terms) == core.expected_terms, f"{core.name}: expected {core.expected_terms} terms, got {len(terms)}")
        require(all(coefficient > 0 for coefficient in coefficients), f"{core.name}: Phi has a nonpositive coefficient")
        require(min(coefficients) == 2, f"{core.name}: expected minimum coefficient 2, got {min(coefficients)}")
        require(real_part != 0 and imaginary_part != 0, f"{core.name}: degenerate Sachs decomposition")
        require(p != 0 and q != 0, f"{core.name}: degenerate isolated pentagon partition")
        require(digest == core.expected_sha256, f"{core.name}: expected SHA-256 {core.expected_sha256}, got {digest}")

        print(
            f"PASS {core.name} terms={len(terms)} min_coefficient={min(coefficients)} "
            f"max_coefficient={max(coefficients)} sha256={digest}"
        )


if __name__ == "__main__":
    main()
