#!/usr/bin/env python3
"""Exact Sachs-phase verifier for the 28 R31-S interior-owner D3 records."""

from __future__ import annotations

import itertools
import subprocess
import sys
from collections import Counter
from functools import lru_cache


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


DIAMOND_OWNERS = ("A", "B", "x")


def records():
    direct = {
        ("direct3", roots)
        for roots in itertools.combinations_with_replacement(DIAMOND_OWNERS, 3)
        if "x" in roots
    }
    chain = {
        ("chain2+direct", upstream, direct_root)
        for upstream in DIAMOND_OWNERS
        for direct_root in DIAMOND_OWNERS
        if "x" in (upstream, direct_root)
    }
    fork = {("fork", "x", occupancy) for occupancy in ("same", "split")}
    chain3 = {("chain3", "x")}
    result = direct | chain | fork | chain3
    require(Counter(row[0] for row in result) == Counter({
        "direct3": 6,
        "chain2+direct": 5,
        "fork": 2,
        "chain3": 1,
    }), "one-side D3 incidence census changed")
    return result


def add_triangle(edges, vertices, root, label):
    left, right = f"{label}a", f"{label}b"
    vertices.update((left, right))
    edges.update((tuple(sorted((root, left))), tuple(sorted((left, right))),
                  tuple(sorted((right, root)))))
    return left, right


def graph_for(record):
    vertices = {"A", "B", "x", "z"}
    edges = {
        ("A", "B"), ("A", "x"), ("B", "x"),
        ("A", "z"), ("B", "z"),
    }
    kind = record[0]
    if kind == "direct3":
        for index, root in enumerate(record[1], 1):
            add_triangle(edges, vertices, root, f"T{index}")
    elif kind == "chain2+direct":
        fresh = add_triangle(edges, vertices, record[1], "T1")[0]
        add_triangle(edges, vertices, fresh, "T2")
        add_triangle(edges, vertices, record[2], "T3")
    elif kind == "fork":
        fresh = add_triangle(edges, vertices, record[1], "T1")
        roots = (fresh[0], fresh[0]) if record[2] == "same" else fresh
        add_triangle(edges, vertices, roots[0], "T2")
        add_triangle(edges, vertices, roots[1], "T3")
    elif kind == "chain3":
        fresh = add_triangle(edges, vertices, record[1], "T1")[0]
        fresh = add_triangle(edges, vertices, fresh, "T2")[0]
        add_triangle(edges, vertices, fresh, "T3")
    else:
        raise AuditError(f"unknown record kind: {kind}")
    return tuple(sorted(vertices)), frozenset(edges)


def simple_cycles(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    cycles = set()
    for start in vertices:
        def visit(path):
            current = path[-1]
            for neighbor in adjacency[current]:
                if neighbor == start and len(path) >= 3:
                    forward = tuple(path)
                    reverse = (start,) + tuple(reversed(path[1:]))
                    cycles.add(min(forward, reverse))
                elif neighbor > start and neighbor not in path:
                    visit(path + [neighbor])
        visit([start])
    return tuple(sorted(((frozenset(cycle), len(cycle)) for cycle in cycles),
                        key=lambda item: (item[1], sorted(item[0]))))


def add_polynomial(target, source, scale):
    for monomial, coefficient in source.items():
        target[monomial] += scale * coefficient
        if target[monomial] == 0:
            del target[monomial]


def matching_polynomial(vertices, edges, deleted):
    remaining = tuple(vertex for vertex in vertices if vertex not in deleted)
    index = {vertex: place for place, vertex in enumerate(vertices)}
    adjacency = {vertex: set() for vertex in remaining}
    for left, right in edges:
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)

    @lru_cache(maxsize=None)
    def recurse(active):
        if not active:
            return {0: 1}
        vertex = active[0]
        rest = active[1:]
        result = Counter()
        for monomial, coefficient in recurse(rest).items():
            result[monomial | (1 << index[vertex])] += coefficient
        active_set = set(active)
        for neighbor in adjacency[vertex] & active_set:
            reduced = tuple(item for item in rest if item != neighbor)
            result.update(recurse(reduced))
        return dict(result)

    return recurse(remaining)


def imaginary_sachs_polynomial(vertices, edges):
    cycles = simple_cycles(vertices, edges)
    terms = Counter()

    def collect(position, used, phase):
        if phase.imag:
            polynomial = matching_polynomial(vertices, edges, used)
            add_polynomial(terms, polynomial, int(phase.imag))
        for cycle_index in range(position, len(cycles)):
            cycle, length = cycles[cycle_index]
            if used.isdisjoint(cycle):
                cycle_phase = -2 * (1j ** (-length))
                collect(cycle_index + 1, used | cycle, phase * cycle_phase)

    collect(0, frozenset(), 1)
    return terms, cycles


def activity_expansion(polynomial):
    """Substitute a_v=t+y_v; keys are (y-support, power of t)."""
    expanded = Counter()
    for monomial, coefficient in polynomial.items():
        support = monomial
        while True:
            expanded[(support, monomial.bit_count() - support.bit_count())] += coefficient
            if support == 0:
                break
            support = (support - 1) & monomial
    return expanded


def audit():
    rows = records()
    signatures = Counter()
    total_coefficients = 0
    for record in rows:
        vertices, edges = graph_for(record)
        polynomial, cycles = imaginary_sachs_polynomial(vertices, edges)
        require(polynomial, f"empty imaginary Sachs polynomial: {record}")
        expanded = activity_expansion(polynomial)
        positive = [(key, value) for key, value in expanded.items() if value > 0]
        # The diamond packet lemma permits precisely one local +6*y defect.
        # Every other coefficient belongs to a negative territory carrier.
        require(len(positive) <= 1,
                f"more than one positive activity defect: {record}")
        if positive:
            (support, t_power), coefficient = positive[0]
            require(support.bit_count() == 1 and t_power == 0 and coefficient == 6,
                    f"unexpected activity defect: {record}")
            require(expanded[(support, 2)] <= -58 and
                    expanded[(support, 4)] <= -38 and
                    expanded[(support, 6)] <= -6,
                    f"diamond defect companions weakened: {record}")
            require(expanded[(0, 1)] <= -18 and
                    expanded[(0, 3)] <= -118 and
                    expanded[(0, 5)] <= -70 and
                    expanded[(0, 7)] <= -10,
                    f"territory carrier companions weakened: {record}")
        require(all(value < 0 for key, value in expanded.items() if (key, value) not in positive),
                f"zero activity coefficient: {record}")
        signatures[(record[0], len(cycles), len(polynomial))] += 1
        total_coefficients += len(expanded)
    require(len(rows) == 14, "one-side D3 record total changed")
    return rows, signatures, total_coefficients


def main():
    rows, signatures, total_coefficients = audit()
    output = (
        "R31-S D3 diamond-packet verifier: exact audit passed\n"
        f"one-side records: {len(rows)}; reflected marked records: {2 * len(rows)}\n"
        f"exact activity-carrier coefficient checks: {total_coefficients}\n"
        "certificate: negative territories plus at most one controlled +6*y diamond defect\n"
        "conclusion (diamond phase-area lemma): sigma(D+T^3)>3"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
