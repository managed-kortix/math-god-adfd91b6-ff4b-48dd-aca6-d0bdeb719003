#!/usr/bin/env python3
"""Exhaust connected shared-cut {3,3,3,5} cores and audit 2R-Z5 I."""

from __future__ import annotations

import hashlib
import itertools
import math
from collections import defaultdict
from functools import lru_cache

import networkx as nx


Cycle = tuple[int, ...]
Polynomial = dict[tuple[int, int], int]
EXPECTED_COUNT = 11
EXPECTED_PROFILES = (
    ((372, 2, 0), (18159, 2, 0)),
    ((380, 2, 0), (15301, 2, 0)),
    ((584, -2, 3), (18231, -2, 3)),
    ((640, 2, 0), (16858, 2, 0)),
    ((591, -2, 3), (17062, -2, 3)),
    ((787, -10, 7), (21103, -10, 7)),
    ((677, -10, 4), (20555, -10, 4)),
    ((852, -10, 8), (19905, -10, 8)),
    ((789, -10, 6), (19560, -10, 6)),
    ((1207, -12, 29), (23011, -86, 32)),
    ((1036, -10, 21), (22326, -56, 24)),
)
EXPECTED_AGGREGATE_SHA256 = "f7f39c81aa13443259ca5a644acfeb639041bc44ff393145a3a031520bac4c03"


def cycle_edges(cycle: Cycle) -> set[tuple[int, int]]:
    return {
        tuple(sorted((cycle[index], cycle[(index + 1) % len(cycle)])))
        for index in range(len(cycle))
    }


def graph_from_cycles(cycles: tuple[Cycle, ...]) -> nx.Graph:
    graph = nx.Graph()
    for cycle in cycles:
        graph.add_edges_from(cycle_edges(cycle))
    return graph


def enumerate_cores() -> list[tuple[Cycle, ...]]:
    """Attach leaf blocks in every order and quotient by graph isomorphism."""

    buckets: dict[
        tuple[int, int, tuple[int, ...]], list[tuple[nx.Graph, tuple[Cycle, ...]]]
    ] = defaultdict(list)
    for lengths in sorted(set(itertools.permutations((3, 3, 3, 5)))):
        states = [(tuple(range(lengths[0])),)]
        next_vertex = lengths[0]
        for length in lengths[1:]:
            new_states = []
            for cycles in states:
                for cut_vertex in sorted(set().union(*map(set, cycles))):
                    leaf = (cut_vertex,) + tuple(
                        range(next_vertex, next_vertex + length - 1)
                    )
                    new_states.append(cycles + (leaf,))
            states = new_states
            next_vertex += length - 1
        for cycles in states:
            graph = graph_from_cycles(cycles)
            key = (len(graph), graph.number_of_edges(), tuple(sorted(dict(graph.degree()).values())))
            if not any(nx.is_isomorphic(graph, old) for old, _ in buckets[key]):
                buckets[key].append((graph, cycles))
    return [cycles for bucket in buckets.values() for _, cycles in bucket]


def cycle_variants(cycle: Cycle) -> tuple[Cycle, ...]:
    variants = []
    for oriented in (cycle, tuple(reversed(cycle))):
        variants.extend(
            oriented[offset:] + oriented[:offset] for offset in range(len(cycle))
        )
    return tuple(variants)


def canonical_cycles(cycles: tuple[Cycle, ...]) -> tuple[Cycle, ...]:
    triangles = [cycle for cycle in cycles if len(cycle) == 3]
    pentagon = next(cycle for cycle in cycles if len(cycle) == 5)
    best: tuple[Cycle, ...] | None = None
    for triangle_order in itertools.permutations(triangles):
        ordered = triangle_order + (pentagon,)
        for variants in itertools.product(*(cycle_variants(cycle) for cycle in ordered)):
            labels: dict[int, int] = {}
            candidate = tuple(
                tuple(labels.setdefault(vertex, len(labels)) for vertex in cycle)
                for cycle in variants
            )
            if best is None or candidate < best:
                best = candidate
    if best is None:
        raise RuntimeError("cannot canonicalize empty cycle family")
    return best


def spread(mask: int) -> int:
    result = 0
    vertex = 0
    while mask:
        if mask & 1:
            result |= 1 << (2 * vertex)
        vertex += 1
        mask >>= 1
    return result


def matching_recursion(vertices: frozenset[int], edges: set[tuple[int, int]]):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[tuple[int, int], ...]:
        if not mask:
            return ((0, 1),)
        low_bit = mask & -mask
        vertex = low_bit.bit_length() - 1
        rest = mask ^ low_bit
        result: dict[int, int] = defaultdict(int)
        for monomial, coefficient in recurse(rest):
            result[monomial | low_bit] += coefficient
        for neighbor in adjacency[vertex]:
            neighbor_bit = 1 << neighbor
            if rest & neighbor_bit:
                for monomial, coefficient in recurse(rest ^ neighbor_bit):
                    result[monomial] += coefficient
        return tuple(sorted(result.items()))

    def partition(remaining: frozenset[int]) -> Polynomial:
        mask = sum(1 << vertex for vertex in remaining)
        return {(spread(monomial), 0): coefficient for monomial, coefficient in recurse(mask)}

    return partition


def add(*polynomials: Polynomial) -> Polynomial:
    result: dict[tuple[int, int], int] = defaultdict(int)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(polynomial: Polynomial, multiplier: int) -> Polynomial:
    return {monomial: multiplier * coefficient for monomial, coefficient in polynomial.items()}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: dict[tuple[int, int], int] = defaultdict(int)
    for (left_activity, left_t), left_coefficient in left.items():
        for (right_activity, right_t), right_coefficient in right.items():
            result[(left_activity + right_activity, left_t + right_t)] += (
                left_coefficient * right_coefficient
            )
    return dict(result)


def certificate(cycles: tuple[Cycle, ...]) -> Polynomial:
    vertices = frozenset().union(*map(frozenset, cycles))
    edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    if len(vertices) != 11 or len(edges) != 14:
        raise RuntimeError(f"invalid core order/size: {len(vertices)}/{len(edges)}")
    partition = matching_recursion(vertices, edges)
    real: Polynomial = {}
    imaginary: Polynomial = {}
    for subset_size in range(5):
        for indices in itertools.combinations(range(4), subset_size):
            selected = [cycles[index] for index in indices]
            selected_vertices = [frozenset(cycle) for cycle in selected]
            if any(selected_vertices[i] & selected_vertices[j]
                   for i in range(len(selected)) for j in range(i + 1, len(selected))):
                continue
            multiplier = 1 + 0j
            for cycle in selected:
                multiplier *= -2j if len(cycle) == 3 else 2j
            remainder = vertices - frozenset().union(*selected_vertices)
            term = partition(remainder)
            if int(multiplier.real):
                real = add(real, scale(term, int(multiplier.real)))
            if int(multiplier.imag):
                imaginary = add(imaginary, scale(term, int(multiplier.imag)))
    pentagon = next(cycle for cycle in cycles if len(cycle) == 5)
    isolated_partition = matching_recursion(
        frozenset(pentagon), cycle_edges(pentagon)
    )
    z5 = isolated_partition(frozenset(pentagon))
    return add(scale(real, 2), scale(multiply(z5, imaginary), -1))


def substitute_t_plus_y(polynomial: Polynomial, order: int = 11) -> Polynomial:
    """Expand every activity a_v as t+y_v exactly."""

    result: dict[tuple[int, int], int] = defaultdict(int)
    for (activity, t_power), coefficient in polynomial.items():
        terms = {(0, t_power): coefficient}
        for vertex in range(order):
            exponent = (activity >> (2 * vertex)) & 3
            if not exponent:
                continue
            expanded: dict[tuple[int, int], int] = defaultdict(int)
            for (y_mask, old_t), old_coefficient in terms.items():
                for y_power in range(exponent + 1):
                    expanded[(y_mask + (y_power << (2 * vertex)),
                              old_t + exponent - y_power)] += (
                                  old_coefficient * math.comb(exponent, y_power)
                              )
            terms = expanded
        for monomial, term_coefficient in terms.items():
            result[monomial] += term_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def incidence_signature(cycles: tuple[Cycle, ...]) -> str:
    shared = []
    for vertex in sorted(set().union(*map(set, cycles))):
        blocks = tuple(index for index, cycle in enumerate(cycles) if vertex in cycle)
        if len(blocks) > 1:
            shared.append("".join(map(str, blocks)))
    return "+".join(sorted(shared, key=lambda item: (-len(item), item)))


def digest(polynomial: Polynomial) -> str:
    payload = "\n".join(f"{key}:{value}" for key, value in sorted(polynomial.items()))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def profile(polynomial: Polynomial) -> tuple[int, int, int]:
    coefficients = list(polynomial.values())
    return len(coefficients), min(coefficients), sum(value < 0 for value in coefficients)


def main() -> None:
    raw = enumerate_cores()
    canonical = sorted({canonical_cycles(cycles) for cycles in raw})
    if len(raw) != len(canonical):
        raise RuntimeError(f"quotient disagreement: graph={len(raw)} canonical={len(canonical)}")
    if len(canonical) != EXPECTED_COUNT:
        raise RuntimeError(f"expected {EXPECTED_COUNT} cores, got {len(canonical)}")
    print(f"connected_shared_cut_cores={len(canonical)}")
    ledger = []
    profiles = []
    for index, cycles in enumerate(canonical, 1):
        phi = certificate(cycles)
        shifted = substitute_t_plus_y(phi)
        independent_profile = profile(phi)
        shifted_profile = profile(shifted)
        profiles.append((independent_profile, shifted_profile))
        ledger.append(f"{cycles}:{digest(phi)}:{digest(shifted)}")
        print(
            f"type={index:02d} incidence={incidence_signature(cycles)} "
            f"independent={independent_profile} shifted={shifted_profile} "
            f"phi_sha256={digest(phi)} shifted_sha256={digest(shifted)} cycles={cycles}"
        )
    aggregate = hashlib.sha256("\n".join(ledger).encode("ascii")).hexdigest()
    print(f"aggregate_sha256={aggregate}")
    if tuple(profiles) != EXPECTED_PROFILES:
        raise RuntimeError(f"profile drift: {profiles}")
    if aggregate != EXPECTED_AGGREGATE_SHA256:
        raise RuntimeError(f"aggregate hash drift: {aggregate}")
    passes = sum(independent[2] == shifted[2] == 0 for independent, shifted in profiles)
    print(f"SUMMARY pass={passes} fail={len(canonical) - passes} verified=yes")


if __name__ == "__main__":
    main()
