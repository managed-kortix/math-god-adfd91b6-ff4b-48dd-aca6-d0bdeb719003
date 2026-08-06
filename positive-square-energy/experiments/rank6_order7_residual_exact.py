#!/usr/bin/env python3
"""Exact symbolic certificates for the 39 residual order-seven targets."""

from __future__ import annotations

import importlib.util
import itertools
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
FRONTIER_ENGINE = HERE / "rank6_order7_dim7_rational_frontier.py"
RESIDUAL_INDICES = (10370, 10372, 10427, 10429, 14191, 14206, 14225,
                    15904, 15908, 15927, 16796, 16800, 16819)
FRONTIERS = {469: (None, 0, 10), 511: (None, 2, 5),
             534: (None, 0, 3), 548: (None, 0, 3)}


def load_frontier_engine():
    spec = importlib.util.spec_from_file_location("order7_frontier", FRONTIER_ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matrix(rows):
    return sp.Matrix([[sp.Rational(value) for value in row] for row in rows])


K469_BASE = matrix([
    [1, F(1, 2), F(1, 2), F(-1, 2), 1, F(-1, 2), F(-1, 2)],
    [F(1, 2), 1, F(-1, 3), F(-1, 3), F(1, 2), F(-1, 3), F(-1, 3)],
    [F(1, 2), F(-1, 3), 1, F(-1, 3), F(1, 2), F(-1, 3), F(-1, 3)],
    [F(-1, 2), F(-1, 3), F(-1, 3), 1, F(-1, 2), 1, F(-1, 3)],
    [1, F(1, 2), F(1, 2), F(-1, 2), 1, F(-1, 2), F(-1, 2)],
    [F(-1, 2), F(-1, 3), F(-1, 3), 1, F(-1, 2), 1, F(-1, 3)],
    [F(-1, 2), F(-1, 3), F(-1, 3), F(-1, 3), F(-1, 2), F(-1, 3), 1],
])

K511_BASE = matrix([
    [1, F(-1, 3), F(-1, 3), F(-1, 3), F(-1, 2), F(-1, 3), 1],
    [F(-1, 3), 1, F(-1, 3), F(-1, 3), F(-1, 2), 1, F(-1, 3)],
    [F(-1, 3), F(-1, 3), 1, F(-1, 3), F(1, 2), F(-1, 3), F(-1, 3)],
    [F(-1, 3), F(-1, 3), F(-1, 3), 1, F(1, 2), F(-1, 3), F(-1, 3)],
    [F(-1, 2), F(-1, 2), F(1, 2), F(1, 2), 1, F(-1, 2), F(-1, 2)],
    [F(-1, 3), 1, F(-1, 3), F(-1, 3), F(-1, 2), 1, F(-1, 3)],
    [1, F(-1, 3), F(-1, 3), F(-1, 3), F(-1, 2), F(-1, 3), 1],
])


def switched(gram, vertices):
    signs = [-1 if vertex in vertices else 1 for vertex in range(7)]
    diagonal = sp.diag(*signs)
    return diagonal * gram * diagonal


STRUCTURAL = {
    10370: K469_BASE,
    10372: matrix([
        [1, 0, 0, F(-1, 2), 1, F(1, 2), F(-1, 2)],
        [0, 1, F(-1, 3), F(1, 3), 0, F(-1, 3), F(-1, 3)],
        [0, F(-1, 3), 1, F(1, 3), 0, F(-1, 3), F(-1, 3)],
        [F(-1, 2), F(1, 3), F(1, 3), 1, F(-1, 2), -1, F(1, 3)],
        [1, 0, 0, F(-1, 2), 1, F(1, 2), F(-1, 2)],
        [F(1, 2), F(-1, 3), F(-1, 3), -1, F(1, 2), 1, F(-1, 3)],
        [F(-1, 2), F(-1, 3), F(-1, 3), F(1, 3), F(-1, 2), F(-1, 3), 1],
    ]),
    10427: matrix([
        [1, 0, 0, F(1, 2), -1, F(1, 2), F(-1, 2)],
        [0, 1, F(-1, 3), F(-1, 3), 0, F(-1, 3), F(-1, 3)],
        [0, F(-1, 3), 1, F(-1, 3), 0, F(-1, 3), F(-1, 3)],
        [F(1, 2), F(-1, 3), F(-1, 3), 1, F(-1, 2), 1, F(-1, 3)],
        [-1, 0, 0, F(-1, 2), 1, F(-1, 2), F(1, 2)],
        [F(1, 2), F(-1, 3), F(-1, 3), 1, F(-1, 2), 1, F(-1, 3)],
        [F(-1, 2), F(-1, 3), F(-1, 3), F(-1, 3), F(1, 2), F(-1, 3), 1],
    ]),
    10429: matrix([
        [1, F(1, 2), F(1, 2), F(1, 2), -1, F(-1, 2), F(-1, 2)],
        [F(1, 2), 1, F(-1, 3), F(1, 3), F(-1, 2), F(-1, 3), F(-1, 3)],
        [F(1, 2), F(-1, 3), 1, F(1, 3), F(-1, 2), F(-1, 3), F(-1, 3)],
        [F(1, 2), F(1, 3), F(1, 3), 1, F(-1, 2), -1, F(1, 3)],
        [-1, F(-1, 2), F(-1, 2), F(-1, 2), 1, F(1, 2), F(1, 2)],
        [F(-1, 2), F(-1, 3), F(-1, 3), -1, F(1, 2), 1, F(-1, 3)],
        [F(-1, 2), F(-1, 3), F(-1, 3), F(1, 3), F(1, 2), F(-1, 3), 1],
    ]),
    14191: K511_BASE,
    14206: matrix([
        [1, F(1, 3), F(-1, 3), F(-1, 3), F(-1, 2), F(-1, 3), 1],
        [F(1, 3), 1, F(1, 3), F(1, 3), F(-1, 2), -1, F(1, 3)],
        [F(-1, 3), F(1, 3), 1, F(-1, 3), 0, F(-1, 3), F(-1, 3)],
        [F(-1, 3), F(1, 3), F(-1, 3), 1, 0, F(-1, 3), F(-1, 3)],
        [F(-1, 2), F(-1, 2), 0, 0, 1, F(1, 2), F(-1, 2)],
        [F(-1, 3), -1, F(-1, 3), F(-1, 3), F(1, 2), 1, F(-1, 3)],
        [1, F(1, 3), F(-1, 3), F(-1, 3), F(-1, 2), F(-1, 3), 1],
    ]),
    14225: matrix([
        [1, F(-1, 3), F(1, 3), F(1, 3), F(-1, 2), F(1, 3), -1],
        [F(-1, 3), 1, F(1, 3), F(1, 3), F(-1, 2), -1, F(1, 3)],
        [F(1, 3), F(1, 3), 1, F(-1, 3), F(-1, 2), F(-1, 3), F(-1, 3)],
        [F(1, 3), F(1, 3), F(-1, 3), 1, F(-1, 2), F(-1, 3), F(-1, 3)],
        [F(-1, 2), F(-1, 2), F(-1, 2), F(-1, 2), 1, F(1, 2), F(1, 2)],
        [F(1, 3), -1, F(-1, 3), F(-1, 3), F(1, 2), 1, F(-1, 3)],
        [-1, F(1, 3), F(-1, 3), F(-1, 3), F(1, 2), F(-1, 3), 1],
    ]),
}


def cycle_gram(kernel, row):
    singleton_edges = ((0, 3), (1, 2))
    doubled_edges = ({534: ((0, 6), (1, 6), (2, 5), (3, 4), (4, 5)),
                      548: ((0, 6), (1, 5), (2, 3), (4, 5), (4, 6))}[kernel])
    signs = [None] * 7
    classes = [None] * 7
    class_count = 0
    adjacency = {vertex: [] for vertex in range(7)}
    pair_index = {pair: index for index, pair in enumerate(itertools.combinations(range(7), 2))}
    for u, v in singleton_edges:
        parity = row[pair_index[(u, v)]]
        relation = -1 if parity else 1
        adjacency[u].append((v, relation))
        adjacency[v].append((u, relation))
    for root in range(7):
        if classes[root] is not None:
            continue
        classes[root], signs[root] = class_count, 1
        stack = [root]
        while stack:
            u = stack.pop()
            for v, relation in adjacency[u]:
                if classes[v] is None:
                    classes[v], signs[v] = class_count, signs[u] * relation
                    stack.append(v)
                else:
                    assert classes[v] == class_count and signs[v] == signs[u] * relation
        class_count += 1
    assert class_count == 5
    quotient = sp.eye(5)
    for u, v in doubled_edges:
        quotient[classes[u], classes[v]] = F(-1, 2) * signs[u] * signs[v]
        quotient[classes[v], classes[u]] = quotient[classes[u], classes[v]]
    pullback = sp.zeros(7, 5)
    for vertex in range(7):
        pullback[vertex, classes[vertex]] = signs[vertex]
    return pullback * quotient * pullback.T


def psd_pivots(gram):
    rank = gram.rank()
    for indices in itertools.permutations(range(7), rank):
        determinants = [gram.extract(indices[:size], indices[:size]).det()
                        for size in range(1, rank + 1)]
        if all(value > 0 for value in determinants):
            block = gram.extract(indices, indices)
            remainder = gram - gram[:, indices] * block.inv() * gram[indices, :]
            if remainder == sp.zeros(7):
                return indices, determinants
    raise AssertionError("no exact PSD pivot certificate")


def path_cost(transformed_correlation, length):
    if transformed_correlation == 1:
        return sp.Integer(0)
    if length == 1:
        return (1 - transformed_correlation) / (1 + transformed_correlation)
    if length == 2 and transformed_correlation == F(-1, 2):
        return F(2, 3)
    raise AssertionError((transformed_correlation, length))


def main():
    frontier = load_frontier_engine()
    engine = frontier.load_engine()
    census = frontier.load_census()
    kernels = {entry["kernel"]: tuple(entry["code"]) for entry in census["kernels"]}
    target_total = 0
    for source_index in RESIDUAL_INDICES:
        source = census["residuals"][source_index]
        kernel = source["kernel"]
        gram = STRUCTURAL.get(source_index)
        if gram is None:
            gram = cycle_gram(kernel, tuple(source["row"]))
        assert gram == gram.T and all(gram[i, i] == 1 for i in range(7))
        pivots, determinants = psd_pivots(gram)
        costs = []
        for frontier_index in FRONTIERS[kernel]:
            paths = engine.path_ledger(kernels[kernel], tuple(source["row"]), frontier_index)
            total = sp.Integer(0)
            for _, _, u, v, length in paths:
                transformed = (-1 if length % 2 else 1) * gram[u, v]
                total += path_cost(transformed, length)
            assert total == 5
            costs.append(total)
            target_total += 1
        print(f"{source_index} K{kernel} rank={gram.rank()} pivots={pivots} "
              f"det={tuple(determinants)} costs={tuple(costs)}")
    assert target_total == 39
    print("exact_targets=39 unresolved=0 all_costs=5 psd=true")


if __name__ == "__main__":
    main()
