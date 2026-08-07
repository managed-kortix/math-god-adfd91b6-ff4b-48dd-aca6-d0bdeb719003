#!/usr/bin/env python3
"""Search residual supports for exact cost-five simplex/mixed atom ledgers.

A K_m regular-simplex atom has cost C(m-1, 2).  K_2 is therefore exactly an
odd zero-cost contraction, while K_5 already costs six and cannot occur in a
cost-five ledger.  The implementation nevertheless derives the search from
the full m=2,...,5 model rather than hard-coding the K_3/K_4 cases.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
F = Fraction
EXPECTED_COUNTS = {
    8: {(5, ()): 12, (2, (4,)): 185, (1, (3, 4)): 4},
    9: {(5, ()): 10, (2, (4,)): 249, (1, (3, 4)): 16},
    10: {(5, ()): 8, (2, (4,)): 152, (1, (3, 4)): 18},
}
SIMPLEX_WIDTHS = tuple(range(2, 6))
ARTIFACT = HERE / "rank6_orders8_10_atom_ledger_classification.json"


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


def simplex_cost(width):
    require(width in SIMPLEX_WIDTHS, f"unsupported simplex width {width}")
    return (width - 1) * (width - 2) // 2


def positive_simplex_profiles(cost):
    """Return all multisets of K_3,...,K_5 atoms having the given cost."""
    profiles = []

    def visit(width, remaining, chosen):
        if width == SIMPLEX_WIDTHS[-1] + 1:
            if remaining == 0:
                profiles.append(tuple(chosen))
            return
        value = simplex_cost(width)
        for count in range(remaining // value + 1):
            visit(width + 1, remaining - count * value,
                  chosen + [width] * count)

    visit(3, cost, [])
    return tuple(profiles)


def clique_partitions(edges, target_cost):
    """Partition indexed quotient multiedges into regular-simplex atoms."""
    edge_indices = frozenset(range(len(edges)))
    vertices = sorted(set(itertools.chain.from_iterable(edge for edge, _ in edges)))
    atoms = []
    for width in SIMPLEX_WIDTHS[1:]:
        cost = simplex_cost(width)
        if cost > target_cost:
            continue
        for subset in itertools.combinations(vertices, width):
            pairs = tuple(itertools.combinations(subset, 2))
            choices = [tuple(index for index, (edge, _) in enumerate(edges) if edge == pair)
                       for pair in pairs]
            if all(choices):
                for occurrence_indices in itertools.product(*choices):
                    atom = frozenset(occurrence_indices)
                    if len(atom) == len(pairs):
                        atoms.append((atom, width, cost))

    def visit(remaining, chosen, cost):
        if not remaining:
            if cost == target_cost:
                yield tuple(chosen), cost
            return
        if cost >= target_cost:
            return
        first = min(remaining)
        for atom, width, value in atoms:
            if first in atom and atom <= remaining and cost + value <= target_cost:
                yield from visit(remaining - atom, chosen + [(width, atom)], cost + value)

    yield from visit(edge_indices, [], 0)


def prescribed_correlations(mixed, partition, active):
    """Return consistent signed quotient correlations, or None on conflict."""
    prescribed = {}

    def assign(edge, value):
        if edge in prescribed and prescribed[edge] != value:
            return False
        prescribed[edge] = value
        return True

    for edge, switch in mixed:
        if not assign(edge, F(-switch, 2)):
            return None
    for width, occurrence_indices in partition:
        for index in occurrence_indices:
            edge, switch = active[index]
            if not assign(edge, F(-switch, width - 1)):
                return None
    return tuple(sorted(prescribed.items()))


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
    _, _, mixed, partition, contractions, classes, signs, prescribed_items = result
    require(len(mixed) == 1 and tuple(sorted(width for width, _ in partition)) == (3, 4),
            "not a triangle/tetrahedron/mixed counterexample")
    blocks = {width: frozenset(edge for edge, _ in occurrences)
              for width, occurrences in partition}
    triangle, tetrahedron = blocks[3], blocks[4]
    triangle_vertices = set(itertools.chain.from_iterable(triangle))
    tetrahedron_vertices = set(itertools.chain.from_iterable(tetrahedron))
    shared = triangle_vertices & tetrahedron_vertices
    require(len(shared) == 1 and mixed[0][0] in triangle,
            "counterexample is not a one-sum with a repeated mixed support")
    cut = next(iter(shared))
    quotient_order = max(classes) + 1
    require(set(range(quotient_order)) == triangle_vertices | tetrahedron_vertices,
            "unexpected unused quotient class")
    gram = [[F(int(i == j)) for j in range(quotient_order)]
            for i in range(quotient_order)]
    for (u, v), value in prescribed_items:
        gram[u][v] = gram[v][u] = value
    for edge in triangle | tetrahedron:
        u, v = edge
        require(gram[u][v], "missing prescribed simplex correlation")
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
    atom_width = {edge: width for width, occurrences in partition
                  for edge, _ in occurrences}
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
            require(odd == 1 and edge == mixed[0][0] and correlation == F(-1, 2),
                    "bad mixed-pair atom")
            totals["mixed"] += 1
        elif edge in triangle:
            require(multiplicity == odd == 1 and correlation == F(-1, 2),
                    "bad triangle atom")
            totals["triangle"] += F(1, 3)
        else:
            require(edge in atom_width and edge in tetrahedron and multiplicity == odd == 1
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

    remaining_cost = 5 - len(mixed)
    if remaining_cost < 0:
        return ()
    profiles = positive_simplex_profiles(remaining_cost)
    kept_sizes = {sum(width * (width - 1) // 2 for width in profile)
                  for profile in profiles}
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
            if edge[0] == edge[1]:
                valid = False
                break
            active_edges.append((edge, signs[u] * signs[v]))
        mixed_edges = []
        for u, v in mixed:
            edge = tuple(sorted((classes[u], classes[v])))
            if edge[0] == edge[1]:
                valid = False
                break
            mixed_edges.append((edge, signs[u] * signs[v]))
        if not valid:
            continue
        for partition, clique_cost in clique_partitions(active_edges, remaining_cost):
            prescribed = prescribed_correlations(mixed_edges, partition, active_edges)
            if clique_cost + len(mixed_edges) == 5 and prescribed is not None:
                atoms = tuple((width, tuple(active_edges[index]
                                             for index in sorted(occurrence_indices)))
                              for width, occurrence_indices in partition)
                results.append((number, tuple(row), tuple(mixed_edges), atoms,
                                tuple(local_contractions), classes, signs, prescribed))
    return tuple(results)


def residuals_by_order(orders):
    result = []
    if 8 in orders:
        order8 = load("atom_order8", HERE / "rank6_order8_sparse_pipeline.py")
        _, rows8 = order8.census(collect_residuals=True)
        result.append((order8, rows8))
    if 9 in orders:
        order9 = load("atom_order9", HERE / "rank6_order9_sparse_witness.py")
        _, rows9 = order9.census(collect_residuals=True)
        result.append((order9, rows9))
    if 10 in orders:
        order10 = load("atom_order10", HERE / "rank6_order10_cubic_exact_rational.py")
        census10 = order10.load_census_module()
        order10.PAIRS = census10.PAIRS
        rows10 = order10.residual_rows(census10)
        result.append((order10, rows10))
    return tuple(result)


def audit_atom_model():
    require(tuple(simplex_cost(width) for width in SIMPLEX_WIDTHS) == (0, 1, 3, 6),
            "simplex cost ledger changed")
    require(set(positive_simplex_profiles(5)) == {(3, 3, 3, 3, 3), (3, 3, 4)},
            "cost-five simplex profiles changed")
    require(all(5 not in profile for cost in range(6)
                for profile in positive_simplex_profiles(cost)),
            "K5 incorrectly entered a cost-at-most-five profile")


def result_record(order, source_index, result):
    number, row, mixed, partition, contractions, classes, signs, prescribed = result
    return {
        "order": order,
        "source_index": source_index,
        "kernel": number,
        "row": list(row),
        "profile": {"mixed": len(mixed),
                    "simplex_widths": sorted(width for width, _ in partition)},
        "mixed": [[list(edge), switch] for edge, switch in mixed],
        "simplexes": [{"width": width,
                       "edges": [[list(edge), switch] for edge, switch in edges]}
                      for width, edges in partition],
        "contractions": [[list(edge), odd] for edge, odd in contractions],
        "classes": list(classes),
        "signs": list(signs),
        "prescribed": [[list(edge), [value.numerator, value.denominator]]
                       for edge, value in prescribed],
    }


def canonical_json(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--orders", default="8,9,10",
                        help="comma-separated subset of 8,9,10")
    parser.add_argument("--write-artifact", action="store_true")
    parser.add_argument("--verify-artifact", action="store_true")
    args = parser.parse_args()
    orders = tuple(int(value) for value in args.orders.split(",") if value)
    require(orders and len(set(orders)) == len(orders)
            and all(order in (8, 9, 10) for order in orders), "invalid --orders")
    audit_atom_model()
    totals = {}
    alternatives = []
    records = []
    for module, rows in residuals_by_order(orders):
        counts = {}
        local_alternatives = []
        for source_index, source in enumerate(rows):
            for result in classify(module, source):
                records.append(result_record(module.ORDER, source_index, result))
                widths = tuple(sorted(width for width, _ in result[3]))
                key = (len(result[2]), widths)
                counts[key] = counts.get(key, 0) + 1
                if key not in ((5, ()), (2, (4,))):
                    alternatives.append((module.ORDER, source_index, key, result))
                    local_alternatives.append((source_index, source, result))
        require(counts == EXPECTED_COUNTS[module.ORDER],
                f"order-{module.ORDER} atom counts changed: {counts}")
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
    payload = {
        "schema": "rank6-orders8-10-exact-atom-ledger-classification-v1",
        "scope": {
            "orders": list(orders),
            "source": "canonical coarse residual parity-orbit representatives",
            "atoms": "regular simplexes K_m for 2<=m<=5 and mixed odd/even doubled pairs",
            "cost": 5,
            "overlaps": "physical occurrences disjoint; quotient supports may overlap",
            "contractions": "every unused odd singleton and every non-odd singleton is signed-contracted",
        },
        "counts": {str(order): [{"mixed": key[0], "simplex_widths": list(key[1]),
                                  "decompositions": value}
                                for key, value in sorted(order_counts.items())]
                   for order, order_counts in sorted(totals.items())},
        "decompositions": records,
    }
    encoded = canonical_json(payload)
    digest = hashlib.sha256(encoded).hexdigest()
    print(f"artifact_sha256={digest} records={len(records)}")
    if args.write_artifact:
        ARTIFACT.write_bytes(encoded)
    if args.verify_artifact:
        require(ARTIFACT.read_bytes() == encoded, "atom-ledger artifact mismatch")


if __name__ == "__main__":
    main()
