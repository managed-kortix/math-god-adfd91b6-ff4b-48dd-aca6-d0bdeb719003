#!/usr/bin/env python3
"""Coefficient tests for weighted {3,5,5} bridge-cluster cores."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
from itertools import product

import sympy as sp


Cycle = tuple[int, ...]
Edge = tuple[int, int]


@dataclass(frozen=True)
class Core:
    name: str
    family: str
    triangle: Cycle
    pentagons: tuple[Cycle, Cycle]
    edges: frozenset[Edge]

    @property
    def cycles(self) -> tuple[Cycle, Cycle, Cycle]:
        return (self.triangle, *self.pentagons)


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def add_cycle(edges: set[Edge], next_vertex: int, length: int, root: int | None = None) -> tuple[Cycle, int]:
    if root is None:
        root = next_vertex
        next_vertex += 1
    cycle = (root, *range(next_vertex, next_vertex + length - 1))
    next_vertex += length - 1
    edges.update(edge(cycle[j], cycle[(j + 1) % length]) for j in range(length))
    return cycle, next_vertex


def add_path(edges: set[Edge], next_vertex: int, root: int, length: int) -> tuple[int, int]:
    tip = root
    for _ in range(length):
        edges.add(edge(tip, next_vertex))
        tip = next_vertex
        next_vertex += 1
    return tip, next_vertex


def disjoint_path(middle_length: int, separation: int, left: int, right: int) -> Core:
    edges: set[Edge] = set()
    middle, nxt = add_cycle(edges, 0, middle_length)
    left_tip, nxt = add_path(edges, nxt, middle[0], left)
    right_tip, nxt = add_path(edges, nxt, middle[separation], right)
    outer_left_length, outer_right_length = ((5, 5) if middle_length == 3 else (3, 5))
    outer_left, nxt = add_cycle(edges, nxt, outer_left_length, left_tip)
    outer_right, nxt = add_cycle(edges, nxt, outer_right_length, right_tip)
    cycles = (middle, outer_left, outer_right)
    triangle = next(cycle for cycle in cycles if len(cycle) == 3)
    pentagons = tuple(cycle for cycle in cycles if len(cycle) == 5)
    role = "triangle_internal" if middle_length == 3 and separation else "triangle_leaf"
    return Core(
        f"path_middle_C{middle_length}_sep{separation}_lengths_{left}_{right}",
        f"disjoint_path_{role}_middle_C{middle_length}_sep{separation}",
        triangle,
        pentagons,  # type: ignore[arg-type]
        frozenset(edges),
    )


def disjoint_y(arms: tuple[int, int, int]) -> Core:
    edges: set[Edge] = set()
    nxt = 1
    cycles: list[Cycle] = []
    for length, arm in zip((3, 5, 5), arms):
        tip, nxt = add_path(edges, nxt, 0, arm)
        cycle, nxt = add_cycle(edges, nxt, length, tip)
        cycles.append(cycle)
    return Core(
        f"Y_arms_{arms[0]}_{arms[1]}_{arms[2]}",
        "disjoint_Y_triangle_leaf",
        cycles[0],
        (cycles[1], cycles[2]),
        frozenset(edges),
    )


def shared_pair(pair: tuple[int, int], host: int, separation: int, bridge_length: int) -> Core:
    edges: set[Edge] = set()
    first, nxt = add_cycle(edges, 0, pair[0])
    second, nxt = add_cycle(edges, nxt, pair[1], first[0])
    pair_cycles = (first, second)
    attachment = pair_cycles[host][separation]
    tip, nxt = add_path(edges, nxt, attachment, bridge_length)
    singleton_length = 5 if pair == (3, 5) else 3
    singleton, nxt = add_cycle(edges, nxt, singleton_length, tip)
    cycles = (*pair_cycles, singleton)
    triangle = next(cycle for cycle in cycles if len(cycle) == 3)
    pentagons = tuple(cycle for cycle in cycles if len(cycle) == 5)
    host_name = "T" if pair_cycles[host] == triangle else "P"
    role = "triangle_internal" if pair == (3, 5) and host == 0 and separation else "triangle_leaf"
    return Core(
        f"shared_{pair[0]}_{pair[1]}_host_{host_name}_sep{separation}_bridge{bridge_length}",
        f"one_shared_pair_{pair[0]}_{pair[1]}_host_{host_name}_sep{separation}_{role}",
        triangle,
        pentagons,  # type: ignore[arg-type]
        frozenset(edges),
    )


def matching_partition(vertices: frozenset[int], edges: frozenset[Edge], activities: tuple[sp.Symbol, ...]) -> sp.Expr:
    @lru_cache(maxsize=None)
    def recurse(remaining: frozenset[int]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        v = min(remaining)
        rest = remaining - {v}
        result = activities[v] * recurse(rest)
        for w in rest:
            if edge(v, w) in edges:
                result += recurse(rest - {w})
        return result

    return recurse(vertices)


def sachs_parts(core: Core, activities: tuple[sp.Symbol, ...]) -> tuple[sp.Expr, sp.Expr]:
    vertices = frozenset(range(len(activities)))
    multipliers = (-2 * sp.I, 2 * sp.I, 2 * sp.I)
    value = matching_partition(vertices, core.edges, activities)
    for mask in range(1, 8):
        selected = [j for j in range(3) if mask & (1 << j)]
        cycle_sets = [frozenset(core.cycles[j]) for j in selected]
        if any(cycle_sets[j] & cycle_sets[k] for j in range(len(selected)) for k in range(j)):
            continue
        deleted = frozenset().union(*cycle_sets)
        multiplier = sp.prod(multipliers[j] for j in selected)
        value += multiplier * matching_partition(vertices - deleted, core.edges, activities)
    value = sp.expand(value)
    return sp.re(value), sp.im(value)


def isolated_partition(cycle: Cycle, activities: tuple[sp.Symbol, ...]) -> sp.Expr:
    edges = frozenset(edge(cycle[j], cycle[(j + 1) % len(cycle)]) for j in range(len(cycle)))
    return matching_partition(frozenset(cycle), edges, activities)


def coefficient_result(expression: sp.Expr, activities: tuple[sp.Symbol, ...]) -> tuple[int, int, int, tuple[tuple[int, ...], int] | None]:
    polynomial = sp.Poly(expression, *activities, domain=sp.ZZ)
    terms = polynomial.terms()
    negative = [(monomial, int(coefficient)) for monomial, coefficient in terms if coefficient < 0]
    witness = min(negative, key=lambda item: (sum(item[0]), item[0])) if negative else None
    return len(terms), min(map(int, polynomial.coeffs())), len(negative), witness


def analyze(
    core: Core, comparisons: tuple[str, ...]
) -> dict[str, tuple[int, int, int, tuple[tuple[int, ...], int] | None]]:
    vertex_count = 1 + max(max(cycle) for cycle in core.cycles)
    activities = sp.symbols(f"a0:{vertex_count}", real=True)
    real, imag = sachs_parts(core, activities)
    p, q = (isolated_partition(cycle, activities) for cycle in core.pentagons)
    r = isolated_partition(core.triangle, activities)
    comparison_real = p * q - 4
    comparison_imag = 2 * (p + q)
    direct = comparison_imag * real - comparison_real * imag
    # Comparisons obtained by adjoining the triangle factor or cancelling it.
    triangle_product = (comparison_imag * r - 2 * comparison_real) * real - (
        comparison_real * r + 2 * comparison_imag
    ) * imag
    # Weaker comparison with (p+2i)(q+2i)/(r-2i), cleared without division.
    triangle_quotient = r * direct + 2 * (comparison_imag * imag + comparison_real * real)
    core_times_triangle = (comparison_imag * real - (comparison_real * r + 2 * comparison_imag) * imag)
    core_times_triangle_real = comparison_imag * real - comparison_real * r * imag
    results = {
        "two_C5": coefficient_result(sp.expand(direct), activities),
    }
    if "times_triangle" in comparisons:
        results["times_triangle"] = coefficient_result(sp.expand(triangle_product), activities)
    if "divide_triangle" in comparisons:
        results["divide_triangle"] = coefficient_result(sp.expand(triangle_quotient), activities)
    if "core_times_triangle" in comparisons:
        results["core_times_triangle"] = coefficient_result(sp.expand(core_times_triangle), activities)
    if "core_times_triangle_real" in comparisons:
        results["core_times_triangle_real"] = coefficient_result(sp.expand(core_times_triangle_real), activities)
    return results


def representatives(max_length: int) -> list[Core]:
    cores: list[Core] = []
    for left, right in product(range(1, max_length + 1), repeat=2):
        for middle, separations in ((3, range(2)), (5, range(3))):
            for separation in separations:
                cores.append(disjoint_path(middle, separation, left, right))
    for arms in product(range(1, max_length + 1), repeat=3):
        cores.append(disjoint_y(arms))
    for length in range(1, max_length + 1):
        for pair in ((3, 5), (5, 5)):
            for host in range(2 if pair == (3, 5) else 1):
                for separation in range(pair[host] // 2 + 1):
                    cores.append(shared_pair(pair, host, separation, length))
    return cores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=2)
    parser.add_argument("--name", default="")
    parser.add_argument(
        "--comparisons",
        nargs="*",
        choices=("two_C5", "times_triangle", "divide_triangle", "core_times_triangle", "core_times_triangle_real"),
        default=("two_C5", "times_triangle", "divide_triangle"),
    )
    args = parser.parse_args()
    for core in representatives(args.max_length):
        if args.name and args.name not in core.name:
            continue
        fields = []
        for comparison, (terms, minimum, negatives, witness) in analyze(core, tuple(args.comparisons)).items():
            fields.append(f"{comparison}:terms={terms},min={minimum},neg={negatives},witness={witness}")
        print(f"{core.name} family={core.family} " + " ".join(fields))


if __name__ == "__main__":
    main()
