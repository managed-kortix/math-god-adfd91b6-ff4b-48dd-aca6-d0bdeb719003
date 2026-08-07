#!/usr/bin/env python3
"""Search residual support rows for cost-five clique/mixed atom ledgers."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
F = Fraction
EXPECTED_COUNTEREXAMPLES = {
    8: ((78755, 883), (97350, 942)),
    9: ((93749, 1060), (169635, 1119), (169965, 1119), (173903, 1123)),
    10: ((105465, 1188), (124181, 1197)),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def signed_quotient(order, contractions):
    adjacency = [[] for _ in range(order)]
    for (u, v), odd in contractions:
        relation = -1 if odd else 1
        adjacency[u].append((v, relation))
        adjacency[v].append((u, relation))
    classes = [None] * order
    signs = [None] * order
    count = 0
    for root in range(order):
        if classes[root] is not None:
            continue
        classes[root], signs[root] = count, 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, relation in adjacency[vertex]:
                expected = signs[vertex] * relation
                if classes[neighbor] is None:
                    classes[neighbor], signs[neighbor] = count, expected
                    stack.append(neighbor)
                elif classes[neighbor] != count or signs[neighbor] != expected:
                    return None
        count += 1
    return tuple(classes), tuple(signs), count


def clique_partitions(edges):
    edge_set = frozenset(edges)
    vertices = sorted(set(itertools.chain.from_iterable(edge_set)))
    atoms = []
    for width, cost in ((3, 1), (4, 3)):
        for subset in itertools.combinations(vertices, width):
            atom = frozenset(itertools.combinations(subset, 2))
            if atom <= edge_set:
                atoms.append((atom, width, cost))

    def visit(remaining, chosen, cost):
        if not remaining:
            yield tuple(chosen), cost
            return
        first = min(remaining)
        for atom, width, value in atoms:
            if first in atom and atom <= remaining:
                yield from visit(remaining - atom, chosen + [(width, atom)], cost + value)

    yield from visit(edge_set, [], 0)


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = F(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            scale = work[row][column] / value
            for index in range(column + 1, len(work)):
                work[row][index] -= scale * work[column][index]
    return result


def audit_counterexample(module, source, result):
    _, _, mixed, partition, contractions, classes, signs = result
    require(len(mixed) == 1 and tuple(sorted(width for width, _ in partition)) == (3, 4),
            "not a triangle/tetrahedron/mixed counterexample")
    blocks = {width: edges for width, edges in partition}
    triangle, tetrahedron = blocks[3], blocks[4]
    triangle_vertices = set(itertools.chain.from_iterable(triangle))
    tetrahedron_vertices = set(itertools.chain.from_iterable(tetrahedron))
    shared = triangle_vertices & tetrahedron_vertices
    require(len(shared) == 1 and mixed[0] in triangle,
            "counterexample is not a one-sum with a repeated mixed support")
    cut = next(iter(shared))
    quotient_order = max(classes) + 1
    require(set(range(quotient_order)) == triangle_vertices | tetrahedron_vertices,
            "unexpected unused quotient class")
    gram = [[F(int(i == j)) for j in range(quotient_order)]
            for i in range(quotient_order)]
    for edge in triangle:
        u, v = edge
        gram[u][v] = gram[v][u] = F(-1, 2)
    for edge in tetrahedron:
        u, v = edge
        gram[u][v] = gram[v][u] = F(-1, 3)
    for u in triangle_vertices - {cut}:
        for v in tetrahedron_vertices - {cut}:
            gram[u][v] = gram[v][u] = gram[u][cut] * gram[cut][v]
    for width in range(1, quotient_order + 1):
        for indices in itertools.combinations(range(quotient_order), width):
            minor = [[gram[u][v] for v in indices] for u in indices]
            require(determinant(minor) >= 0, "counterexample quotient Gram is indefinite")

    if module.ORDER == 10:
        _, _, support, multiplicities, row, *_ = source
    else:
        _, support, multiplicities, row, *_ = source
    contraction_set = set(contractions)
    used_active = triangle | tetrahedron
    totals = {"contraction": 0, "triangle": 0, "tetrahedron": 0, "mixed": 0}
    for index, multiplicity, odd in zip(support, multiplicities, row):
        u, v = module.PAIRS[index]
        original = ((u, v), bool(odd))
        edge = tuple(sorted((classes[u], classes[v])))
        correlation = signs[u] * signs[v] * gram[classes[u]][classes[v]]
        if original in contraction_set:
            transformed = -correlation if odd else correlation
            require(multiplicity == 1 and transformed == 1, "bad zero-cost contraction")
            totals["contraction"] += 1
        elif multiplicity == 2:
            require(odd == 1 and edge == mixed[0] and correlation == F(-1, 2),
                    "bad mixed-pair atom")
            totals["mixed"] += 1
        elif edge in triangle:
            require(multiplicity == odd == 1 and correlation == F(-1, 2),
                    "bad triangle atom")
            totals["triangle"] += F(1, 3)
        else:
            require(edge in used_active and edge in tetrahedron and multiplicity == odd == 1
                    and correlation == F(-1, 3), "bad tetrahedron atom")
            totals["tetrahedron"] += F(1, 2)
    require(totals == {"contraction": module.ORDER - 6, "triangle": F(1),
                       "tetrahedron": F(3), "mixed": 1},
            f"counterexample cost ledger changed: {totals}")
    return gram


def classify(module, source):
    if module.ORDER == 10:
        number, _, support, multiplicities, row, *_ = source
    else:
        number, support, multiplicities, row, *_ = source
    contractions = []
    mixed = []
    active = []
    for index, multiplicity, odd in zip(support, multiplicities, row):
        edge = module.PAIRS[index]
        if odd in (0, multiplicity):
            if multiplicity == 1 and odd == 1:
                active.append(edge)
            else:
                contractions.append((edge, odd > 0))
        elif multiplicity == 2 and odd == 1:
            mixed.append(edge)
        else:
            return ()

    kept_sizes = set()
    remaining_cost = 5 - len(mixed)
    for tetrahedra in range(remaining_cost // 3 + 1):
        triangles = remaining_cost - 3 * tetrahedra
        kept_sizes.add(6 * tetrahedra + 3 * triangles)
    results = []
    for kept_size in kept_sizes:
      for kept_indices in itertools.combinations(range(len(active)), kept_size):
        active_mask = sum(1 << index for index in kept_indices)
        local_contractions = contractions + [
            (edge, True) for bit, edge in enumerate(active) if not active_mask & (1 << bit)
        ]
        quotient = signed_quotient(module.ORDER, local_contractions)
        if quotient is None:
            continue
        classes, signs, _ = quotient
        active_edges = []
        valid = True
        for bit, (u, v) in enumerate(active):
            if not active_mask & (1 << bit):
                continue
            edge = tuple(sorted((classes[u], classes[v])))
            if edge[0] == edge[1] or signs[u] * signs[v] != 1 or edge in active_edges:
                valid = False
                break
            active_edges.append(edge)
        mixed_edges = []
        for u, v in mixed:
            edge = tuple(sorted((classes[u], classes[v])))
            if edge[0] == edge[1] or signs[u] * signs[v] != 1 or edge in mixed_edges:
                valid = False
                break
            mixed_edges.append(edge)
        if not valid:
            continue
        for partition, clique_cost in clique_partitions(active_edges):
            if clique_cost + len(mixed_edges) == 5:
                results.append((number, tuple(row), tuple(mixed_edges), partition,
                                tuple(local_contractions), classes, signs))
    return tuple(results)


def residuals_by_order():
    order8 = load("atom_order8", HERE / "rank6_order8_sparse_pipeline.py")
    _, rows8 = order8.census(collect_residuals=True)

    order9 = load("atom_order9", HERE / "rank6_order9_sparse_witness.py")
    _, rows9 = order9.census(collect_residuals=True)

    order10 = load("atom_order10", HERE / "rank6_order10_cubic_exact_rational.py")
    census10 = order10.load_census_module()
    order10.PAIRS = census10.PAIRS
    rows10 = order10.residual_rows(census10)
    return ((order8, rows8), (order9, rows9), (order10, rows10))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    totals = {}
    alternatives = []
    for module, rows in residuals_by_order():
        counts = {}
        local_alternatives = []
        for source_index, source in enumerate(rows):
            for result in classify(module, source):
                widths = tuple(sorted(width for width, _ in result[3]))
                key = (len(result[2]), widths)
                counts[key] = counts.get(key, 0) + 1
                if key not in ((5, ()), (2, (4,))):
                    alternatives.append((module.ORDER, source_index, key, result))
                    local_alternatives.append((source_index, source, result))
        observed = tuple((source_index, result[0])
                         for source_index, _, result in local_alternatives)
        require(observed == EXPECTED_COUNTEREXAMPLES[module.ORDER],
                f"order-{module.ORDER} counterexample ledger changed: {observed}")
        for _, source, result in local_alternatives:
            audit_counterexample(module, source, result)
        totals[module.ORDER] = counts
        print(f"order={module.ORDER} residuals={len(rows)} atom_ledgers={counts}")
    print(f"alternative_total={len(alternatives)}")
    print("alternative_rows=" + ",".join(
        f"n{order}:source{source}:K{result[0]}" for order, source, _, result in alternatives))
    if args.list:
        for result in alternatives:
            print(result)


if __name__ == "__main__":
    main()
