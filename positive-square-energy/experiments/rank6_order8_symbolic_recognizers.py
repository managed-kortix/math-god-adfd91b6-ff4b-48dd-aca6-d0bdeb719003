#!/usr/bin/env python3
"""Predict order-eight equality rows from quotient combinatorics.

This is an experimental recognizer, not a theorem verifier.  It searches the
locked order-eight census for the two known signed-cycle packets and for the
order-eight lift of the order-seven tetrahedron-plus-apex packet.  Every match
is checked by constructing its rational branch Gram matrix, auditing all
principal minors, and evaluating the canonical DNN budget exactly.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PIPELINE = HERE / "rank6_order8_sparse_pipeline.py"
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pipeline():
    spec = importlib.util.spec_from_file_location("rank6_order8_sparse", PIPELINE)
    require(spec is not None and spec.loader is not None, "cannot load sparse census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def audit_psd(gram):
    order = len(gram)
    require(all(len(row) == order for row in gram), "nonsquare Gram")
    require(all(gram[i][i] == 1 for i in range(order)), "nonunit Gram diagonal")
    require(all(gram[i][j] == gram[j][i] for i in range(order) for j in range(order)),
            "nonsymmetric Gram")
    for width in range(1, order + 1):
        for indices in itertools.combinations(range(order), width):
            minor = [[gram[i][j] for j in indices] for i in indices]
            require(determinant(minor) >= 0, "indefinite symbolic Gram")


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def signed_components(order, contraction_edges, contraction_parities):
    adjacency = [[] for _ in range(order)]
    for (u, v), parity in zip(contraction_edges, contraction_parities):
        relation = -1 if parity else 1
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
                else:
                    require(classes[neighbor] == count and signs[neighbor] == expected,
                            "inconsistent signed contraction")
        count += 1
    return tuple(classes), tuple(signs), count


def tetra_apex_structures(pipeline, source):
    number, _, support, multiplicities, _ = source
    values = {pipeline.PAIRS[index]: multiplicity
              for index, multiplicity in zip(support, multiplicities)}
    singleton_edges = tuple(edge for edge, multiplicity in values.items() if multiplicity == 1)
    for contractions in itertools.combinations(singleton_edges, 3):
        classes, _, count = signed_components(pipeline.ORDER, contractions, (0, 0, 0))
        if count != 5:
            continue
        quotient = {}
        valid = True
        for edge, multiplicity in values.items():
            if edge in contractions:
                continue
            left, right = classes[edge[0]], classes[edge[1]]
            if left == right:
                valid = False
                break
            key = tuple(sorted((left, right)))
            if key in quotient:
                valid = False
                break
            quotient[key] = (multiplicity, edge)
        if not valid or sorted(value[0] for value in quotient.values()) != [1] * 6 + [2] * 2:
            continue
        doubled = tuple(key for key, value in quotient.items() if value[0] == 2)
        common = set(doubled[0]) & set(doubled[1])
        if len(common) != 1:
            continue
        apex = next(iter(common))
        tetra = tuple(vertex for vertex in range(5) if vertex != apex)
        tetra_pairs = set(itertools.combinations(tetra, 2))
        if {key for key, value in quotient.items() if value[0] == 1} != tetra_pairs:
            continue
        yield {
            "kernel": number,
            "contractions": tuple(sorted(contractions)),
            "mixed": tuple(sorted(quotient[key][1] for key in doubled)),
            "tetra_support": tuple(sorted(quotient[key][1] for key in tetra_pairs)),
        }


def solve_switches(edges, required_products):
    adjacency = {}
    for (left, right), product in zip(edges, required_products):
        adjacency.setdefault(left, []).append((right, product))
        adjacency.setdefault(right, []).append((left, product))
    switches = {}
    for root in adjacency:
        if root in switches:
            continue
        switches[root] = 1
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor, product in adjacency[vertex]:
                expected = switches[vertex] * product
                if neighbor in switches:
                    if switches[neighbor] != expected:
                        return None
                else:
                    switches[neighbor] = expected
                    stack.append(neighbor)
    return switches


def tetra_apex_gram(pipeline, structure, row_by_edge):
    contractions = structure["contractions"]
    contraction_parities = tuple(row_by_edge[edge] for edge in contractions)
    classes, signs, count = signed_components(pipeline.ORDER, contractions,
                                               contraction_parities)
    require(count == 5, "tetra-apex quotient width changed")
    tetra_edges = structure["tetra_support"]
    products = tuple(signs[u] * signs[v] for u, v in tetra_edges)
    switches = solve_switches(tuple((classes[u], classes[v]) for u, v in tetra_edges), products)
    if switches is None:
        return None
    mixed = structure["mixed"]
    apex_class = next(iter(set(classes[mixed[0][i]] for i in (0, 1)) &
                           set(classes[mixed[1][i]] for i in (0, 1))))
    tetra_classes = tuple(vertex for vertex in range(5) if vertex != apex_class)
    base = [[F(int(i == j)) for j in range(5)] for i in range(5)]
    for left, right in itertools.combinations(tetra_classes, 2):
        base[left][right] = base[right][left] = F(-switches[left] * switches[right], 3)
    prescribed = {}
    for u, v in mixed:
        other = classes[v] if classes[u] == apex_class else classes[u]
        prescribed[other] = F(-signs[u] * signs[v], 2)
    missing = [vertex for vertex in tetra_classes if vertex not in prescribed]
    fill = -sum(prescribed.values(), F()) / len(missing)
    prescribed.update((vertex, fill) for vertex in missing)
    for vertex, value in prescribed.items():
        base[apex_class][vertex] = base[vertex][apex_class] = value
    gram = [[signs[i] * signs[j] * base[classes[i]][classes[j]]
             for j in range(pipeline.ORDER)] for i in range(pipeline.ORDER)]
    return gram


def path_cost(correlation, parity):
    require(parity in (0, 1), "symbolic row is not singleton parity")
    transformed = correlation if parity == 0 else -correlation
    if transformed == 1:
        return F(0)
    if parity == 1:
        return (1 - transformed) / (1 + transformed)
    require(transformed == F(-1, 2), "unsupported symbolic even endpoint")
    return F(2, 3)


def recognize_tetra_apex_row(pipeline, structure, support, multiplicities, row):
    row_by_edge = {pipeline.PAIRS[index]: odd for index, odd in zip(support, row)}
    multiplicity_by_edge = {pipeline.PAIRS[index]: value
                            for index, value in zip(support, multiplicities)}
    if any(row_by_edge[edge] != 1 for edge in structure["tetra_support"]):
        return None
    if any(multiplicity_by_edge[edge] != 2 or row_by_edge[edge] != 1
           for edge in structure["mixed"]):
        return None
    gram = tetra_apex_gram(pipeline, structure, row_by_edge)
    if gram is None:
        return None
    try:
        audit_psd(gram)
        total = F()
        for edge, multiplicity in multiplicity_by_edge.items():
            correlation = gram[edge[0]][edge[1]]
            odd = row_by_edge[edge]
            if multiplicity == 1:
                total += path_cost(correlation, odd)
            else:
                require(multiplicity == 2 and odd == 1 and correlation == F(-1, 2),
                        "mixed bundle geometry changed")
                total += F(1, 3) + F(2, 3)
        require(total == pipeline.BUDGET, "tetra-apex budget is not exact")
    except RuntimeError:
        return None
    return gram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-rows", action="store_true")
    parser.add_argument("--targets", choices=("all", "order7-analogue"),
                        default="order7-analogue")
    args = parser.parse_args()
    pipeline = load_pipeline()
    sources = pipeline.source_kernels()
    structures = []
    for source in sources:
        structures.extend(tetra_apex_structures(pipeline, source))
    by_kernel = {}
    for structure in structures:
        by_kernel.setdefault(structure["kernel"], []).append(structure)

    _, residuals = pipeline.census(collect_residuals=True)
    apex_rows = []
    cycle_rows = []
    for source_index, source in enumerate(residuals):
        number, support, multiplicities, row, _, _, cycle = source
        if cycle:
            cycle_rows.append(source_index)
        for structure in by_kernel.get(number, ()):
            if recognize_tetra_apex_row(pipeline, structure, support, multiplicities, row):
                apex_rows.append((source_index, number, row, structure))
                break

    print(f"tetra_apex_kernel_structures={len(structures)}")
    print("tetra_apex_kernels=" + ",".join(f"K{number}" for number in sorted(by_kernel)))
    print(f"signed_cycle_residual_rows={len(cycle_rows)}")
    print(f"tetra_apex_residual_rows={len(apex_rows)}")
    print(f"predicted_symbolic_rows={len(cycle_rows) + len(apex_rows)}")
    # At order seven the numerical nulls were exactly the canonical target and
    # the coordinate carried by each zero-cost contraction.  Order eight has
    # three contractions, so the direct analogue has four targets per row.
    target_multiplier = 14 if args.targets == "all" else 4
    print(f"target_policy={args.targets}")
    print(f"predicted_symbolic_targets={target_multiplier * (len(cycle_rows) + len(apex_rows))}")
    print(f"predicted_targets_beyond_K744_K756={target_multiplier * len(apex_rows)}")
    if args.list_rows:
        for source_index, number, row, structure in apex_rows:
            print(f"source={source_index} K{number} row={row} "
                  f"contractions={','.join(map(edge_name, structure['contractions']))} "
                  f"mixed={','.join(map(edge_name, structure['mixed']))}")
    print("scope=EXPERIMENTAL_SYMBOLIC_PREDICTION_ONLY full_theorem=false")


if __name__ == "__main__":
    main()
