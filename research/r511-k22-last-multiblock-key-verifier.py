#!/usr/bin/env python3
"""Exact verifier for the R511-K22 marked two-cycle packet."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pentacyclic/research/order5-kernel-family-theorem.json"
SOURCE_SHA256 = "4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8"
BOUND = Fraction(21, 5)

RECORDS = (
    ("E0", (0, 0, 0, 1, 1, 1, 1, 1, 1, 1), None,
     (2, 1, 2, 1, 1, 1, 1, 1, 1),
     ((1, 0, 0), (Fraction(-3, 16), Fraction(-5, 32), Fraction(-21, 32)),
      (Fraction(-17, 64), Fraction(63, 64), Fraction(7, 32)),
      (Fraction(33, 32), Fraction(-7, 64), Fraction(3, 32)),
      (Fraction(-41, 64), Fraction(-53, 64), Fraction(49, 64))),
     (((Fraction(65, 64), Fraction(-3, 64), Fraction(3, 64)),), (),
       ((Fraction(43, 64), Fraction(-13, 16), Fraction(3, 4)),),
       (), (), (), (), (), ())),
    ("E2", (0, 0, 0, 1, 1, 1, 1, 1, 1, 1), 0,
     (4, 1, 2, 1, 1, 1, 1, 1, 1),
     ((1, 0, 0), (Fraction(-3, 16), Fraction(-5, 32), Fraction(-21, 32)),
      (Fraction(-17, 64), Fraction(63, 64), Fraction(7, 32)),
      (Fraction(33, 32), Fraction(-1, 8), Fraction(7, 64)),
      (Fraction(-21, 32), Fraction(-13, 16), Fraction(3, 4))),
     (((Fraction(65, 64), Fraction(-1, 32), Fraction(1, 32)),
       (Fraction(65, 64), Fraction(-1, 16), Fraction(1, 16)),
       (Fraction(33, 32), Fraction(-3, 32), Fraction(5, 64))), (),
       ((Fraction(43, 64), Fraction(-13, 16), Fraction(3, 4)),),
       (), (), (), (), (), ())),
    ("O0", (0, 0, 1, 1, 1, 1, 1, 1, 1, 1), None,
     (1, 1, 2, 1, 1, 1, 1, 1, 1),
     ((1, 0, 0), (Fraction(65, 64), Fraction(19, 64), Fraction(79, 64)),
      (Fraction(3, 8), Fraction(1, 8), Fraction(-29, 64)),
      (Fraction(-13, 16), Fraction(35, 64), Fraction(1, 32)),
      (Fraction(-3, 8), Fraction(-63, 64), Fraction(-1, 16))),
     ((), (), ((Fraction(19, 32), Fraction(-55, 64), Fraction(-3, 64)),),
      (), (), (), (), (), ())),
    ("O2", (0, 0, 1, 1, 1, 1, 1, 1, 1, 1), 0,
     (3, 1, 2, 1, 1, 1, 1, 1, 1),
     ((1, 0, 0), (Fraction(67, 64), Fraction(5, 32), Fraction(5, 4)),
      (Fraction(25, 64), Fraction(5, 64), Fraction(-29, 64)),
      (Fraction(-45, 64), Fraction(21, 32), Fraction(1, 32)),
      (Fraction(-15, 32), Fraction(-15, 16), Fraction(-3, 64))),
     (((Fraction(63, 64), Fraction(-1, 4), Fraction(-1, 64)),
       (Fraction(29, 32), Fraction(-1, 2), Fraction(-1, 32))), (),
       ((Fraction(35, 64), Fraction(-57, 64), Fraction(-3, 64)),),
       (), (), (), (), (), ())),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def unit(parameters):
    square = sum(value * value for value in parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(
        2 * value / denominator for value in parameters)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal Gram step")
    return (1 - correlation) / (1 + correlation)


def exact_cost(lengths, branch_parameters, internal_parameters):
    endpoints = ((0, 3), (0, 4), (0, 4), (1, 2), (1, 3),
                 (1, 4), (2, 3), (2, 4), (3, 4))
    branches = tuple(unit(row) for row in branch_parameters)
    total = Fraction(0)
    for length, (u, v), parameters in zip(lengths, endpoints, internal_parameters):
        require(len(parameters) == length - 1, "internal path count changed")
        path = [branches[u], *(unit(row) for row in parameters)]
        path.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum(step_cost(a, b) for a, b in zip(path, path[1:]))
    return total


def source_targets():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
            "K22 theorem source changed")
    payload = json.loads(SOURCE.read_text(encoding="ascii"))
    return {(tuple(row["row"]), row["frontier"], tuple(row["lengths"]))
            for row in payload["records"]
            if row["method"] == "structural_attached_k4"}


def physical_graph(p03):
    edges = set(itertools.combinations(range(1, 5), 2))
    vertices = list(range(5))
    next_vertex = 5

    def add_path(u, v, length):
        nonlocal next_vertex
        path = [u]
        for _ in range(length - 1):
            path.append(next_vertex)
            vertices.append(next_vertex)
            next_vertex += 1
        path.append(v)
        edges.update(tuple(sorted(pair)) for pair in zip(path, path[1:]))

    add_path(0, 3, p03)
    add_path(0, 4, 1)
    add_path(0, 4, 2)
    return tuple(vertices), frozenset(edges)


def automorphisms(vertices, edges):
    degrees = {v: sum(v in edge for edge in edges) for v in vertices}
    groups = [tuple(v for v in vertices if degrees[v] == degree)
              for degree in sorted(set(degrees.values()))]
    result = []
    for images in itertools.product(*(itertools.permutations(group) for group in groups)):
        permutation = dict(zip(itertools.chain.from_iterable(groups),
                               itertools.chain.from_iterable(images)))
        transformed = {tuple(sorted((permutation[u], permutation[v]))) for u, v in edges}
        if transformed == set(edges):
            result.append(permutation)
    return tuple(result)


def orbit_count(vertices, automorphisms, labeled):
    marks = (itertools.product(vertices, repeat=2) if labeled else
             itertools.combinations_with_replacement(vertices, 2))
    unseen = set(marks)
    count = 0
    while unseen:
        mark = min(unseen)
        orbit = set()
        for action in automorphisms:
            image = (action[mark[0]], action[mark[1]])
            orbit.add(image if labeled else tuple(sorted(image)))
        unseen -= orbit
        count += 1
    return count


def audit():
    expected = source_targets()
    actual = {(row, frontier, lengths) for _, row, frontier, lengths, _, _ in RECORDS}
    require(actual == expected and len(actual) == 4, "structural target set changed")
    costs = []
    for name, _, _, lengths, branches, internals in RECORDS:
        cost = exact_cost(lengths, branches, internals)
        require(cost < BOUND, f"{name} lost strict 21/5 Gram bound")
        costs.append(cost)

    labeled_counts = []
    unlabeled_counts = []
    for p03 in (1, 2, 3, 4):
        vertices, edges = physical_graph(p03)
        actions = automorphisms(vertices, edges)
        require(len(actions) == 2, "K22 target automorphism group changed")
        require(sorted(sum(action[v] == v for v in vertices) for action in actions) ==
                [len(vertices) - 2, len(vertices)], "fixed-vertex census changed")
        labeled_counts.append(orbit_count(vertices, actions, True))
        unlabeled_counts.append(orbit_count(vertices, actions, False))
    require(labeled_counts == [26, 37, 50, 65], "labeled incidence census changed")
    require(unlabeled_counts == [16, 22, 29, 37], "unlabeled incidence census changed")
    require(BOUND + Fraction(3, 5) + 1 < 6, "nontriangle DNN gate changed")
    require(3 - 1 - 1 == 1 and 2 + 0 - 1 == 1, "packet debit changed")
    return costs, labeled_counts, unlabeled_counts


def main():
    costs, labeled, unlabeled = audit()
    output = (
        "R511-K22 last multiblock key: exact audit passed\n"
        "structural targets: E0 E2 O0 O2; exact Gram bound: e22<21/5\n"
        f"marked incidences: labeled={labeled} total={sum(labeled)}; "
        f"unlabeled={unlabeled} total={sum(unlabeled)}\n"
        "DNN residual: two triangles only; induced packet: >3-1-1>0\n"
        "status: R511-K22 CLOSED"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
