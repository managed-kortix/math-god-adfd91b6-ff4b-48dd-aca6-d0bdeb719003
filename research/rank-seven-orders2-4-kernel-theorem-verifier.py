#!/usr/bin/env python3
"""Exact hostile audit for rank-seven kernel orders two through four."""

from __future__ import annotations

import hashlib
import itertools
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROOF = (ROOT / "positive-square-energy" / "heptacyclic-general"
         / "rank-seven-orders2-4-kernel-theorem.md")
PROOF_SHA256 = "25e84efe5cba507e3ad0287a83505b544bbb8b40a401f7a45373d025b1bff399"
EXPECTED_COUNTS = (1, 6, 47)
ORDERS = (2, 3, 4)
BUDGET = Fraction(6)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_manifest_bytes(value):
    def encode(item):
        if isinstance(item, dict):
            return "{" + ",".join(f"{key}:{encode(item[key])}" for key in sorted(item)) + "}"
        if isinstance(item, (list, tuple)):
            return "[" + ",".join(encode(child) for child in item) + "]"
        return str(item)

    return (encode(value) + "\n").encode("ascii")


def pairs(n):
    return tuple(itertools.combinations(range(n), 2))


def degrees(n, code):
    require(type(code) is tuple and len(code) == n * (n - 1) // 2,
            "malformed multiplicity code")
    result = [0] * n
    for value, (u, v) in zip(code, pairs(n)):
        require(type(value) is int and value >= 0, "invalid multiplicity")
        result[u] += value
        result[v] += value
    return tuple(result)


def connected_after_deleting(n, code, deleted):
    remaining = tuple(vertex for vertex in range(n) if vertex != deleted)
    if len(remaining) <= 1:
        return True
    adjacency = [set() for _ in range(n)]
    for value, (u, v) in zip(code, pairs(n)):
        if value and deleted not in (u, v):
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = {remaining[0]}
    stack = [remaining[0]]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == len(remaining)


def relabel(row, permutation, n):
    lookup = dict(zip(pairs(n), row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in pairs(n))


def canonical_code(n, code):
    return min(relabel(code, permutation, n)
               for permutation in itertools.permutations(range(n)))


def partitions(total, width, ceiling=None):
    if width == 0:
        if total == 0:
            yield ()
        return
    maximum = min(total - width + 1, total if ceiling is None else ceiling)
    for first in range(maximum, 0, -1):
        yield from ((first,) + rest for rest in
                    partitions(total - first, width - 1, first))


def incidence_solutions(degree_row):
    n = len(degree_row)
    matrix = [[0] * n for _ in range(n)]

    def visit(vertex, target, residual):
        if vertex == n - 1:
            if residual[vertex] == 0:
                yield tuple(matrix[u][v] for u, v in pairs(n))
            return
        if target == n:
            if residual[vertex] == 0 and sum(residual[vertex + 1:]) % 2 == 0:
                yield from visit(vertex + 1, vertex + 2, residual)
            return
        maximum = min(residual[vertex], residual[target])
        for value in range(maximum + 1):
            matrix[vertex][target] = matrix[target][vertex] = value
            updated = list(residual)
            updated[vertex] -= value
            updated[target] -= value
            yield from visit(vertex, target + 1, tuple(updated))
        matrix[vertex][target] = matrix[target][vertex] = 0

    yield from visit(0, 1, tuple(degree_row))


def direct_census():
    result = []
    for n in ORDERS:
        classes = set()
        for excess in partitions(12, n):
            degree_row = tuple(value + 2 for value in excess)
            if degree_row[0] > sum(degree_row[1:]):
                continue
            for code in incidence_solutions(degree_row):
                if all(connected_after_deleting(n, code, vertex) for vertex in range(n)):
                    classes.add(canonical_code(n, code))
        result.extend((n, code) for code in sorted(classes))
    return tuple(result)


def load_selected(expected_proof_digest=PROOF_SHA256):
    require(expected_proof_digest == PROOF_SHA256, "proof digest policy changed")
    require(hashlib.sha256(PROOF.read_bytes()).hexdigest() == expected_proof_digest,
            "analytic proof note changed")
    selected = direct_census()
    require(tuple(sum(n == order for n, _ in selected) for order in ORDERS)
            == EXPECTED_COUNTS, "selected order counts changed")
    require(selected == tuple(sorted(set(selected))),
            "direct census is not sorted and unique")
    for n, code in selected:
        require(sum(code) == n + 6 and min(degrees(n, code)) >= 3,
                "direct census contains a non-kernel")
        require(all(connected_after_deleting(n, code, vertex) for vertex in range(n)),
                "direct census contains a cut vertex")
        require(code == canonical_code(n, code), "direct census is not canonical")
    return selected


def automorphisms(n, kernel):
    return tuple(permutation for permutation in itertools.permutations(range(n))
                 if relabel(kernel, permutation, n) == kernel)


def parity_orbits(n, kernel):
    physical = tuple(itertools.product(*(range(value + 1) for value in kernel)))
    group = automorphisms(n, kernel)
    representatives = tuple(sorted({min(relabel(row, permutation, n)
                                        for permutation in group)
                                    for row in physical}))
    return len(physical), len(group), representatives


def canonical_lengths(multiplicity, odd):
    require(0 <= odd <= multiplicity, "invalid odd-path count")
    if odd == 0:
        return (2,) * multiplicity
    return (1,) + (3,) * (odd - 1) + (2,) * (multiplicity - odd)


def path_ledger(kernel, row, coordinate=None):
    result = []
    for edge, (multiplicity, odd) in enumerate(zip(kernel, row)):
        result.extend((edge, occurrence, length)
                      for occurrence, length in enumerate(
                          canonical_lengths(multiplicity, odd)))
    require(len(result) == sum(kernel), "physical path count changed")
    if coordinate is not None:
        require(type(coordinate) is int and 0 <= coordinate < len(result),
                "invalid frontier coordinate")
        edge, occurrence, length = result[coordinate]
        result[coordinate] = edge, occurrence, length + 2
    return tuple(result)


def audit_eight_path_atom(row):
    odd = row[0]
    even = 8 - odd
    has_unit = odd > 0
    if not has_unit:
        endpoint_bound = min(2 * even, 8 - even)
        require(endpoint_bound <= 6, "eight-path endpoint atom exceeds six")
        return Fraction(endpoint_bound)
    if even <= 3:
        return Fraction(2 * even)
    # At x=pi/3, 3 tan^2(pi/18)<1/3. The stored rational is a strict upper
    # bound, not a claim that the trigonometric path cost equals this value.
    strict_upper = Fraction(8 + even, 3)
    require(strict_upper <= 5, "unit eight-path tangent bound changed")
    return strict_upper


def determinant3(a, b, c):
    return 1 + 2 * a * b * c - a * a - b * b - c * c


def audit_triangle_atom(kernel, row):
    require(sum(kernel) == 9, "order-three path count changed")
    midpoint_det = determinant3(Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2))
    require(midpoint_det == 0, "triangle midpoint Gram is not PSD")
    cost = sum((odd * Fraction(1, 3) + (multiplicity - odd) * Fraction(2, 3)
                for multiplicity, odd in zip(kernel, row)), Fraction(0))
    require(cost <= BUDGET, "triangle atom exceeds six")
    return cost


def tetrahedral_cost(kernel, row, coloring):
    total = Fraction(0)
    for multiplicity, odd, (u, v) in zip(kernel, row, pairs(4)):
        if coloring[u] == coloring[v]:
            if odd:
                return None
            continue
        if odd:
            total += Fraction(1, 2) + (odd - 1) * Fraction(1, 6)
        total += (multiplicity - odd) * Fraction(3, 5)
    return total


def audit_tetrahedral_atom(kernel, row):
    # Exact checks behind f_3(-1/3)<=1/6 and the length-two 3/5 chain.
    require(Fraction(1241, 6859) < Fraction(1, 3),
            "triple-angle odd-path bound changed")
    require(Fraction(7, 13) ** 2 < Fraction(1, 3),
            "even-path midpoint Gram lost positive definiteness")
    require(2 * (1 - Fraction(7, 13)) / (1 + Fraction(7, 13)) == Fraction(3, 5),
            "even-path midpoint cost changed")
    candidates = tuple(cost for coloring in itertools.product(range(4), repeat=4)
                       if (cost := tetrahedral_cost(kernel, row, coloring)) is not None)
    require(candidates, "order-four parity row has no legal tetrahedral coloring")
    cost = min(candidates)
    require(cost <= BUDGET, "tetrahedral atom exceeds six")
    return cost


def audit_owner(n, kernel, row):
    if n == 2:
        return audit_eight_path_atom(row)
    if n == 3:
        return audit_triangle_atom(kernel, row)
    return audit_tetrahedral_atom(kernel, row)


def audit_frontier(selected):
    physical_total = orbit_total = target_total = 0
    maxima = {order: Fraction(0) for order in ORDERS}
    keys = set()
    for n, kernel in selected:
        physical, group_size, rows = parity_orbits(n, kernel)
        require(group_size >= 1, "empty automorphism group")
        physical_total += physical
        orbit_total += len(rows)
        for row in rows:
            cost = audit_owner(n, kernel, row)
            maxima[n] = max(maxima[n], cost)
            paths = path_ledger(kernel, row)
            for coordinate in (None, *range(len(paths))):
                target = path_ledger(kernel, row, coordinate)
                key = (n, kernel, row, coordinate)
                require(key not in keys, "duplicate canonical-plus-coordinate key")
                keys.add(key)
                require(len(target) == n + 6, "frontier target width changed")
                require(cost <= BUDGET, "frontier owner exceeds six")
                target_total += 1
    require(target_total == len(keys), "frontier key set equality failed")
    require(maxima[4] == Fraction(28, 5), "order-four sharp ledger changed")
    return physical_total, orbit_total, target_total, maxima


def validate_scope(scope):
    expected = {
        "rank": 7,
        "orders": [2, 3, 4],
        "kernel_counts": [1, 6, 47],
        "budget": 6,
        "lengths": "canonical-plus-one-coordinate and fixed-parity coordinatewise lift",
        "attachments": "arbitrary rooted trees at branch or subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "excluded": [
            "rank-seven kernel orders five through twelve",
            "multiple positive-rank blocks",
            "all connected heptacyclic graphs",
            "parity-changing or spectral subdivision monotonicity",
        ],
    }
    require(scope == expected, "theorem scope changed or widened")


def scope_manifest():
    return {
        "rank": 7,
        "orders": [2, 3, 4],
        "kernel_counts": [1, 6, 47],
        "budget": 6,
        "lengths": "canonical-plus-one-coordinate and fixed-parity coordinatewise lift",
        "attachments": "arbitrary rooted trees at branch or subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "excluded": [
            "rank-seven kernel orders five through twelve",
            "multiple positive-rank blocks",
            "all connected heptacyclic graphs",
            "parity-changing or spectral subdivision monotonicity",
        ],
    }


def expect_rejected(action, label):
    try:
        action()
    except (KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_checks():
    mutations = 0
    expect_rejected(lambda: load_selected("0" * 64), "proof digest")
    mutations += 1
    for label, field, value in (
            ("order-five overclaim", "orders", [2, 3, 4, 5]),
            ("budget widening", "budget", 7),
            ("canonical-only", "lengths", "canonical vectors only"),
            ("connector widening", "attachments", "arbitrary connectors"),
            ("global overclaim", "conclusion", "all connected heptacyclic graphs")):
        changed = deepcopy(scope_manifest())
        changed[field] = value
        expect_rejected(lambda changed=changed: validate_scope(changed), label)
        mutations += 1
    expect_rejected(lambda: path_ledger((8,), (0,), 8), "invalid coordinate")
    mutations += 1
    expect_rejected(lambda: degrees(4, (1, 2)), "malformed census row")
    mutations += 1
    return mutations


def audit():
    selected = load_selected()
    validate_scope(scope_manifest())
    ledger = audit_frontier(selected)
    return selected, ledger


def report(selected, ledger, mutations):
    physical, orbits, targets, maxima = ledger
    manifest = {
        "scope": scope_manifest(),
        "selected_codes": [[n, list(code)] for n, code in selected],
        "physical_parity_rows": physical,
        "parity_orbits": orbits,
        "frontier_targets": targets,
        "maxima": {str(n): [maxima[n].numerator, maxima[n].denominator]
                   for n in ORDERS},
    }
    digest = hashlib.sha256(canonical_manifest_bytes(manifest)).hexdigest()
    return "\n".join((
        "rank-seven orders2-4 kernel theorem: exact hostile audit passed",
        "direct_kernel_census: counts=1+6+47=54",
        f"physical_parity_rows={physical} parity_orbits={orbits}",
        f"canonical_plus_coordinate_targets={targets}",
        f"max_excess_by_order=2:{maxima[2]} 3:{maxima[3]} 4:{maxima[4]}",
        "scope: every simple subdivision; arbitrary rooted-tree attachments",
        "conclusion: s+(G)>=|V(G)| for rank-seven kernel orders 2 through 4",
        "nonclaim: orders 5-12, multiblock graphs, and all connected heptacyclic graphs",
        f"exact_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def main():
    selected, ledger = audit()
    mutations = hostile_checks()
    require(mutations == 8, "hostile mutation count changed")
    output = report(selected, ledger, mutations)
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run((sys.executable, "-O", str(Path(__file__).resolve()),
                                    "--emit"), check=False, capture_output=True, text=True)
        require(completed.returncode == 0, "python -O verifier failed")
        require(completed.stderr == "", "python -O verifier wrote stderr")
        require(completed.stdout == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
