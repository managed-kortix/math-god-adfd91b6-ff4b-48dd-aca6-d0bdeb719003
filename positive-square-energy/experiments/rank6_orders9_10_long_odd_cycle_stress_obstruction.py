#!/usr/bin/env python3
"""Exact exclusion data for pure C7/C9 DNN stresses at orders nine and ten."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
EXPECTED = {
    9: {
        7: {971: {"1111222": 10, "1112222": 20, "1122222": 6}},
        9: {971: {"111122222": 1}},
    },
    10: {
        7: {1133: {"1111122": 10, "1111222": 50,
                   "1112222": 50, "1122222": 10}},
        9: {1133: {"111112222": 5, "111122222": 5}},
    },
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fixture():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256,
            "kernel fixture changed")
    return json.loads(raw.decode("ascii"))["kernels"]


def polynomial(coefficients, value):
    result = Fraction(0)
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def audit_algebra():
    # t_q=tan^2(pi/(2q)). Chebyshev elimination gives these factors.
    p7 = (7, -35, 21, -1)
    p9 = (3, -27, 33, -1)
    require(polynomial(p7, Fraction(0)) < 0 < polynomial(p7, Fraction(1, 16)),
            "C7 root isolation changed")
    require(polynomial(p9, Fraction(0)) < 0 < polynomial(p9, Fraction(1, 30)),
            "C9 root isolation changed")

    # Rational-root theorem, checked without a symbolic algebra dependency.
    for coefficients, numerators, denominators in (
        (p7, (1,), (1, 7)),
        (p9, (1,), (1, 3)),
    ):
        for numerator in numerators:
            for denominator in denominators:
                for sign in (-1, 1):
                    require(polynomial(coefficients,
                                       Fraction(sign * numerator, denominator)) != 0,
                            "long-cycle polynomial acquired a rational root")


def root(parent, vertex):
    while parent[vertex] != vertex:
        parent[vertex] = parent[parent[vertex]]
        vertex = parent[vertex]
    return vertex


def cycle_contractions(order, code, cycle_order):
    pairs = tuple(itertools.combinations(range(order), 2))
    support = tuple((edge, value) for edge, value in zip(pairs, code) if value)
    result = []
    for kept_tuple in itertools.combinations(range(len(support)), cycle_order):
        kept = frozenset(kept_tuple)
        parent = list(range(order))
        valid = True
        for index, ((u, v), _) in enumerate(support):
            if index in kept:
                continue
            u, v = root(parent, u), root(parent, v)
            if u == v:
                valid = False
                break
            parent[v] = u
        classes = {root(parent, v) for v in range(order)}
        if not valid or len(classes) != cycle_order:
            continue
        labels = {value: index for index, value in enumerate(sorted(classes))}
        edges = set()
        degrees = [0] * cycle_order
        multiplicities = []
        for index in kept:
            (u, v), multiplicity = support[index]
            edge = tuple(sorted((labels[root(parent, u)], labels[root(parent, v)])))
            if edge[0] == edge[1] or edge in edges:
                valid = False
                break
            edges.add(edge)
            degrees[edge[0]] += 1
            degrees[edge[1]] += 1
            multiplicities.append(multiplicity)
        if valid and degrees == [2] * cycle_order:
            result.append("".join(str(value) for value in sorted(multiplicities)))
    return tuple(result)


def derive():
    audit_algebra()
    kernels = fixture()
    report = {}
    for order in (9, 10):
        order_report = {}
        sources = [(number, record) for number, record in enumerate(kernels, 1)
                   if record["n"] == order]
        require(len(sources) == {9: 162, 10: 66}[order],
                f"order-{order} kernel count changed")
        for number, record in sources:
            require(sum(record["code"]) == order + 5,
                    f"rank-six path budget changed at K{number}")
        for cycle_order in (7, 9):
            rows = {}
            for number, record in sources:
                contractions = cycle_contractions(order, record["code"], cycle_order)
                if contractions:
                    rows[number] = {
                        key: contractions.count(key) for key in sorted(set(contractions))
                    }
            require(rows == EXPECTED[order][cycle_order],
                    f"order-{order} C{cycle_order} ledger changed: {rows}")
            order_report[str(cycle_order)] = rows
        report[str(order)] = order_report
    return {
        "schema": "rank6-orders9-10-long-odd-cycle-stress-obstruction-v1",
        "source_sha256": SOURCE_SHA256,
        "orders": report,
        "algebra": {
            "C7": {"polynomial": "7*t^3-35*t^2+21*t-1", "bound": "0<t<1/16"},
            "C9": {"polynomial": "3*t^3-27*t^2+33*t-1", "bound": "0<t<1/30"},
            "path_budget": 15,
            "conclusion": "every nonempty pure C7/C9 component has objective in (0,1)",
        },
    }


def main():
    print(json.dumps(derive(), sort_keys=True, separators=(",", ":"), allow_nan=False))


if __name__ == "__main__":
    main()
