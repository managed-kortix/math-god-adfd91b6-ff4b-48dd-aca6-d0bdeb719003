#!/usr/bin/env python3
"""Exhaust and certify connected shared-cut {3,3,5,5} cactus cores."""

from __future__ import annotations

import hashlib
import itertools
from collections import defaultdict
from functools import lru_cache

import networkx as nx


Cycle = tuple[int, ...]
Polynomial = dict[int, int]
EXPECTED_COUNT = 20
EXPECTED_AGGREGATE_SHA256 = "5de126495a983d5014f4339a88830cedc8ec053d89680a23e9663736485d71d5"
EXPECTED_FAILURE_PROFILE = (
    (1, 21, -8), (2, 21, -8), (3, 6, -4), (4, 11, -8),
    (5, 21, -8), (7, 21, -8), (8, 6, -4), (9, 11, -8),
    (10, 155, -14), (11, 141, -16), (12, 172, -32), (13, 178, -20),
    (14, 114, -14), (15, 102, -16), (16, 100, -32), (17, 109, -20),
    (18, 154, -16), (19, 166, -16), (20, 161, -16),
)


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


def add_if_new(
    cycles: tuple[Cycle, ...],
    buckets: dict[tuple[int, int, tuple[int, ...]], list[tuple[nx.Graph, tuple[Cycle, ...]]]],
) -> None:
    graph = graph_from_cycles(cycles)
    key = (len(graph), graph.number_of_edges(), tuple(sorted(dict(graph.degree()).values())))
    if any(nx.is_isomorphic(graph, old_graph) for old_graph, _ in buckets[key]):
        return
    buckets[key].append((graph, cycles))


def enumerate_cores() -> list[tuple[Cycle, ...]]:
    """Attach leaf blocks recursively, then quotient by exact graph isomorphism."""

    buckets: dict[
        tuple[int, int, tuple[int, ...]], list[tuple[nx.Graph, tuple[Cycle, ...]]]
    ] = defaultdict(list)
    for lengths in sorted(set(itertools.permutations((3, 3, 5, 5)))):
        first = tuple(range(lengths[0]))
        states = [(first,)]
        next_vertex = lengths[0]
        for length in lengths[1:]:
            new_states: list[tuple[Cycle, ...]] = []
            for cycles in states:
                vertices = sorted(set().union(*map(set, cycles)))
                for cut_vertex in vertices:
                    leaf = (cut_vertex,) + tuple(
                        range(next_vertex, next_vertex + length - 1)
                    )
                    new_states.append(cycles + (leaf,))
            states = new_states
            next_vertex += length - 1
        for cycles in states:
            add_if_new(cycles, buckets)
    return [cycles for bucket in buckets.values() for _, cycles in bucket]


def cycle_variants(cycle: Cycle) -> tuple[Cycle, ...]:
    variants = []
    for oriented in (cycle, tuple(reversed(cycle))):
        variants.extend(
            oriented[offset:] + oriented[:offset] for offset in range(len(cycle))
        )
    return tuple(variants)


def canonical_cycles(cycles: tuple[Cycle, ...]) -> tuple[Cycle, ...]:
    """Canonically label the colored cycle-block incidence and cyclic positions."""

    triangles = [cycle for cycle in cycles if len(cycle) == 3]
    pentagons = [cycle for cycle in cycles if len(cycle) == 5]
    best: tuple[Cycle, ...] | None = None
    for triangle_order in itertools.permutations(triangles):
        for pentagon_order in itertools.permutations(pentagons):
            ordered = triangle_order + pentagon_order
            for variants in itertools.product(*(cycle_variants(cycle) for cycle in ordered)):
                labels: dict[int, int] = {}
                relabeled = []
                for cycle in variants:
                    relabeled.append(
                        tuple(labels.setdefault(vertex, len(labels)) for vertex in cycle)
                    )
                candidate = tuple(relabeled)
                if best is None or candidate < best:
                    best = candidate
    if best is None:
        raise RuntimeError("cannot canonicalize an empty cycle family")
    return best


def spread(mask: int) -> int:
    """Put square-free exponents into two-bit fields for carry-free products."""

    result = 0
    vertex = 0
    while mask:
        if mask & 1:
            result |= 1 << (2 * vertex)
        vertex += 1
        mask >>= 1
    return result


def matching_recursion(
    vertices: frozenset[int], edges: set[tuple[int, int]]
):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    @lru_cache(maxsize=None)
    def recurse(remaining_mask: int) -> tuple[tuple[int, int], ...]:
        if remaining_mask == 0:
            return ((0, 1),)
        low_bit = remaining_mask & -remaining_mask
        vertex = low_bit.bit_length() - 1
        rest = remaining_mask ^ low_bit
        result: Polynomial = defaultdict(int)
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
        return {spread(monomial): coefficient for monomial, coefficient in recurse(mask)}

    return partition


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = defaultdict(int)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(polynomial: Polynomial, multiplier: int) -> Polynomial:
    return {monomial: multiplier * coefficient for monomial, coefficient in polynomial.items()}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = defaultdict(int)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            result[left_monomial + right_monomial] += left_coefficient * right_coefficient
    return dict(result)


def exponents(monomial: int, order: int = 13) -> tuple[int, ...]:
    return tuple((monomial >> (2 * vertex)) & 3 for vertex in range(order))


def polynomial_digest(polynomial: Polynomial) -> str:
    terms = sorted(
        ((exponents(monomial), coefficient) for monomial, coefficient in polynomial.items()),
        reverse=True,
    )
    payload = "\n".join(f"{powers}:{coefficient}" for powers, coefficient in terms)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def core_digest(cycles: tuple[Cycle, ...]) -> str:
    return hashlib.sha256(repr(cycles).encode("ascii")).hexdigest()


def incidence_signature(cycles: tuple[Cycle, ...]) -> str:
    shared = []
    for vertex in sorted(set().union(*map(set, cycles))):
        blocks = tuple(index for index, cycle in enumerate(cycles) if vertex in cycle)
        if len(blocks) > 1:
            shared.append("".join(map(str, blocks)))
    return "+".join(sorted(shared, key=lambda item: (-len(item), item)))


def certificate(cycles: tuple[Cycle, ...]) -> Polynomial:
    vertices = frozenset().union(*map(frozenset, cycles))
    edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    if len(vertices) != 13 or len(edges) != 16:
        raise RuntimeError(f"invalid core order/size: {len(vertices)}/{len(edges)}")
    partition = matching_recursion(vertices, edges)

    real: Polynomial = {}
    imaginary: Polynomial = {}
    for subset_size in range(5):
        for indices in itertools.combinations(range(4), subset_size):
            selected = [cycles[index] for index in indices]
            selected_vertices = [frozenset(cycle) for cycle in selected]
            if any(
                selected_vertices[i] & selected_vertices[j]
                for i in range(len(selected))
                for j in range(i + 1, len(selected))
            ):
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

    pentagons = [cycle for cycle in cycles if len(cycle) == 5]
    isolated = []
    for pentagon in pentagons:
        isolated_partition = matching_recursion(
            frozenset(pentagon), cycle_edges(pentagon)
        )
        isolated.append(isolated_partition(frozenset(pentagon)))
    p, q = isolated
    p_plus_q = add(p, q)
    pq_minus_four = add(multiply(p, q), {0: -4})
    return add(scale(multiply(real, p_plus_q), 2), scale(multiply(imaginary, pq_minus_four), -1))


def main() -> None:
    raw_cores = enumerate_cores()
    canonical = sorted({canonical_cycles(cycles) for cycles in raw_cores})
    if len(raw_cores) != len(canonical):
        raise RuntimeError(
            f"isomorphism quotient disagreement: graph={len(raw_cores)} canonical={len(canonical)}"
        )
    if len(canonical) != EXPECTED_COUNT:
        raise RuntimeError(f"expected {EXPECTED_COUNT} quotient types, got {len(canonical)}")
    print(f"connected_shared_cut_cores={len(canonical)}")

    failures = []
    aggregate_lines = []
    for index, cycles in enumerate(canonical, 1):
        phi = certificate(cycles)
        coefficients = list(phi.values())
        nonpositive = sum(coefficient <= 0 for coefficient in coefficients)
        digest = polynomial_digest(phi)
        incidence_digest = core_digest(cycles)
        aggregate_lines.append(f"{incidence_digest}:{digest}")
        status = "PASS" if nonpositive == 0 else "FAIL"
        if nonpositive:
            failures.append((index, nonpositive, min(coefficients)))
        print(
            f"{status} type={index:02d} terms={len(phi)} min={min(coefficients)} "
            f"max={max(coefficients)} nonpositive={nonpositive} "
            f"incidence={incidence_signature(cycles)} core_sha256={incidence_digest} "
            f"phi_sha256={digest} cycles={cycles}"
        )

    aggregate = hashlib.sha256("\n".join(aggregate_lines).encode("ascii")).hexdigest()
    print(f"aggregate_sha256={aggregate}")
    if aggregate != EXPECTED_AGGREGATE_SHA256:
        raise RuntimeError(f"aggregate hash drift: {aggregate}")
    if tuple(failures) != EXPECTED_FAILURE_PROFILE:
        raise RuntimeError(f"failure profile drift: {failures}")
    print(
        f"SUMMARY pass={len(canonical) - len(failures)} fail={len(failures)} "
        f"failure_profile_verified=yes"
    )


if __name__ == "__main__":
    main()
