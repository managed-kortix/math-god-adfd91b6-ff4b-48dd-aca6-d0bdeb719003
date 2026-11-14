#!/usr/bin/env python3
"""Fail-closed full-R/I diagnostic for the 14 one-side R31-S:D3 records.

This establishes exact finite Sachs data and a corrected signed-dictionary
elimination obstruction.  It deliberately exits nonzero: it proves neither
the half-plane implication nor the continuous-phase area bound for D+T^3.
"""

from __future__ import annotations

import itertools
import subprocess
import sys
from collections import Counter, defaultdict
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
    chain_direct = {
        ("chain2+direct", upstream, direct_root)
        for upstream in DIAMOND_OWNERS
        for direct_root in DIAMOND_OWNERS
        if "x" in (upstream, direct_root)
    }
    fork = {("fork", "x", occupancy) for occupancy in ("same", "split")}
    chain = {("chain3", "x")}
    result = direct | chain_direct | fork | chain
    require(Counter(row[0] for row in result) == Counter({
        "direct3": 6, "chain2+direct": 5, "fork": 2, "chain3": 1,
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
    edges = {("A", "B"), ("A", "x"), ("B", "x"),
             ("A", "z"), ("B", "z")}
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
                    visit(path + (neighbor,))
        visit((start,))
    return tuple(sorted(((frozenset(cycle), len(cycle)) for cycle in cycles),
                        key=lambda item: (item[1], tuple(sorted(item[0])))))


def add_polynomial(target, source, scale):
    for monomial, coefficient in source.items():
        target[monomial] = target.get(monomial, 0) + scale * coefficient
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
        for neighbor in adjacency[vertex] & set(rest):
            reduced = tuple(item for item in rest if item != neighbor)
            result.update(recurse(reduced))
        return dict(result)

    return recurse(remaining)


def full_sachs_polynomial(vertices, edges):
    cycles = simple_cycles(vertices, edges)
    real, imaginary = {}, {}

    def collect(position, used, phase):
        polynomial = matching_polynomial(vertices, edges, used)
        if phase.real:
            add_polynomial(real, polynomial, int(phase.real))
        if phase.imag:
            add_polynomial(imaginary, polynomial, int(phase.imag))
        for cycle_index in range(position, len(cycles)):
            cycle, length = cycles[cycle_index]
            if used.isdisjoint(cycle):
                collect(cycle_index + 1, used | cycle,
                        phase * (-2 * (1j ** (-length))))

    collect(0, frozenset(), 1)
    return real, imaginary, cycles


def activity_expansion(polynomial):
    """Substitute z_v=t+y_v, retaining every signed coefficient."""
    expanded = defaultdict(int)
    for monomial, coefficient in polynomial.items():
        support = monomial
        while True:
            expanded[(support, monomial.bit_count() - support.bit_count())] += coefficient
            if support == 0:
                break
            support = (support - 1) & monomial
    return {key: value for key, value in expanded.items() if value}


def split_variable(polynomial, bit):
    free, linear = defaultdict(int), defaultdict(int)
    for (support, t_power), coefficient in polynomial.items():
        if support & bit:
            linear[(support ^ bit, t_power)] += coefficient
        else:
            free[(support, t_power)] += coefficient
    return ({key: value for key, value in free.items() if value},
            {key: value for key, value in linear.items() if value})


def multiply_squarefree(left, right):
    """Multiply two activity polynomials; record once/twice supports and t power."""
    result = defaultdict(int)
    for (left_support, left_t), left_coefficient in left.items():
        for (right_support, right_t), right_coefficient in right.items():
            key = (left_support ^ right_support,
                   left_support & right_support,
                   left_t + right_t)
            result[key] += left_coefficient * right_coefficient
    return {key: value for key, value in result.items() if value}


def subtract(left, right):
    result = defaultdict(int)
    for key, value in left.items():
        result[key] += value
    for key, value in right.items():
        result[key] -= value
    return {key: value for key, value in result.items() if value}


def signs(polynomial):
    values = tuple(polynomial.values())
    return sum(value > 0 for value in values), sum(value < 0 for value in values)


def defect_line(polynomial, vertices, defect_vertex):
    """Set z_v=t except z_defect=t+y; return (constant, y-linear) t-tuples."""
    bit = 1 << vertices.index(defect_vertex)
    constant_part = defaultdict(int)
    linear_part = defaultdict(int)
    for monomial, coefficient in polynomial.items():
        degree = monomial.bit_count()
        constant_part[degree] += coefficient
        if monomial & bit:
            linear_part[degree - 1] += coefficient
    limit = len(vertices)
    return (tuple(constant_part.get(power, 0) for power in range(limit + 1)),
            tuple(linear_part.get(power, 0) for power in range(limit)))


def bare_defect_formulas():
    result = {}
    for record in sorted(records(), key=repr):
        vertices, edges = graph_for(record)
        real, imaginary, _ = full_sachs_polynomial(vertices, edges)
        imaginary_activity = activity_expansion(imaginary)
        positive = [(key, value) for key, value in imaginary_activity.items() if value > 0]
        if not positive:
            continue
        bit = positive[0][0][0]
        defect_vertex = vertices[bit.bit_length() - 1]
        result[record] = (defect_vertex,
                          defect_line(real, vertices, defect_vertex),
                          defect_line(imaginary, vertices, defect_vertex))
    return result


# Coefficient tuples are low degree first.  They are compact exact
# certificates for the one-dimensional slice z_v=t, z_defect=t+y.
EXPECTED_BARE_DEFECT_FORMULAS = {
    ("chain2+direct", "A", "x"): ("T1b",
        ((-12, 0, -29, 0, 60, 0, 58, 0, 14, 0, 1),
         (0, -36, 0, 26, 0, 41, 0, 12, 0, 1)),
        ((0, -30, 0, -124, 0, -72, 0, -10, 0, 0, 0),
         (6, 0, -68, 0, -50, 0, -8, 0, 0, 0))),
    ("chain2+direct", "B", "x"): ("T1b",
        ((-12, 0, -29, 0, 60, 0, 58, 0, 14, 0, 1),
         (0, -36, 0, 26, 0, 41, 0, 12, 0, 1)),
        ((0, -30, 0, -124, 0, -72, 0, -10, 0, 0, 0),
         (6, 0, -68, 0, -50, 0, -8, 0, 0, 0))),
    ("chain2+direct", "x", "x"): ("T1b",
        ((-12, 0, -33, 0, 54, 0, 56, 0, 14, 0, 1),
         (0, -37, 0, 24, 0, 40, 0, 12, 0, 1)),
        ((0, -26, 0, -118, 0, -70, 0, -10, 0, 0, 0),
         (6, 0, -68, 0, -50, 0, -8, 0, 0, 0))),
    ("chain3", "x"): ("T2b",
        ((-12, 0, -41, 0, 58, 0, 60, 0, 14, 0, 1),
         (0, -37, 0, 26, 0, 42, 0, 12, 0, 1)),
        ((0, -26, 0, -134, 0, -78, 0, -10, 0, 0, 0),
         (6, 0, -70, 0, -52, 0, -8, 0, 0, 0))),
    ("fork", "x", "split"): ("x",
        ((-12, 0, -61, 0, 62, 0, 60, 0, 14, 0, 1),
         (0, -33, 0, 22, 0, 32, 0, 10, 0, 1)),
        ((0, -18, 0, -150, 0, -78, 0, -10, 0, 0, 0),
         (6, 0, -58, 0, -38, 0, -6, 0, 0, 0))),
}


def audit():
    rows = records()
    real_ranges = set()
    defect_rows = []
    elimination_negative = 0
    elimination_positive = 0
    total_real_activity = total_imaginary_activity = 0

    for record in sorted(rows, key=repr):
        vertices, edges = graph_for(record)
        real, imaginary, cycles = full_sachs_polynomial(vertices, edges)
        require(real and imaginary and cycles, f"empty full Sachs state: {record}")
        real_activity = activity_expansion(real)
        imaginary_activity = activity_expansion(imaginary)
        total_real_activity += len(real_activity)
        total_imaginary_activity += len(imaginary_activity)
        real_ranges.add(len(real))

        positive_imaginary = [(key, value) for key, value in imaginary_activity.items()
                              if value > 0]
        require(len(positive_imaginary) <= 1,
                f"multiple imaginary defects: {record}")
        if not positive_imaginary:
            require(all(value < 0 for value in imaginary_activity.values()),
                    f"nonnegative nondefect imaginary coefficient: {record}")
            continue

        (support, t_power), coefficient = positive_imaginary[0]
        require(support.bit_count() == 1 and t_power == 0 and coefficient == 6,
                f"unexpected imaginary defect: {record}")
        bit = support
        a_part, b_part = split_variable(real_activity, bit)
        p_part, q_part = split_variable(imaginary_activity, bit)

        # If R=A+B*y and I=P+Q*y, then on I=0 the numerator of R is
        # A*Q-B*P. A coefficientwise proof would need this to have one sign.
        boundary = subtract(multiply_squarefree(a_part, q_part),
                            multiply_squarefree(b_part, p_part))
        positive, negative = signs(boundary)
        require(positive > 0 and negative > 0,
                f"elimination obstruction ceased to be mixed: {record}")
        require(all(value < 0 for value in p_part.values()),
                f"P is not coefficientwise negative: {record}")
        q_positive = [value for value in q_part.values() if value > 0]
        require(q_positive == [6] and any(value < 0 for value in q_part.values()),
                f"Q defect structure changed: {record}")
        defect_rows.append(record)
        elimination_positive += positive
        elimination_negative += negative

    bare_formulas = bare_defect_formulas()
    require(bare_formulas == EXPECTED_BARE_DEFECT_FORMULAS,
            "bare defect-line R/I formulas changed")

    expected_defects = {
        ("chain2+direct", "A", "x"),
        ("chain2+direct", "B", "x"),
        ("chain2+direct", "x", "x"),
        ("chain3", "x"),
        ("fork", "x", "split"),
    }
    require(set(defect_rows) == expected_defects, "D3 defect-record set changed")
    require(min(real_ranges) == 151 and max(real_ranges) == 196,
            "full real Sachs term range changed")
    require(elimination_positive > 0 and elimination_negative > 0,
            "aggregate boundary obstruction is not mixed")
    return (len(rows), min(real_ranges), max(real_ranges), len(defect_rows),
            total_real_activity, total_imaginary_activity,
            elimination_positive, elimination_negative)


def report(result):
    (row_count, real_minimum, real_maximum, defect_count,
     real_activity, imaginary_activity, boundary_positive,
     boundary_negative) = result
    return (
        "R31-S D3 full Sachs diagnostic: exact finite audit passed\n"
        f"one-side records: {row_count}; reflected marked records: {2 * row_count}\n"
        f"raw real Sachs terms by record: min={real_minimum} max={real_maximum}\n"
        f"activity terms checked: R={real_activity} I={imaginary_activity}\n"
        f"exceptional +6y records: {defect_count}\n"
        f"AQ-BP mixed coefficients: positive={boundary_positive} "
        f"negative={boundary_negative}\n"
        "unverified: I>=0 => R<0; continuous branch; Coulson phase-area bound\n"
        "conclusion: sigma(D+T^3)>3 NOT ESTABLISHED\n"
        "status: OPEN; FAIL CLOSED"
    )


def main():
    output = report(audit())
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=False, capture_output=True, text=True)
        require(child.returncode == 1, "optimized D3 diagnostic did not fail closed")
        require(child.stderr == "", "optimized D3 diagnostic wrote stderr")
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
