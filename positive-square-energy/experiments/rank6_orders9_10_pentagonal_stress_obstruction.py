#!/usr/bin/env python3
"""Exact order-nine/ten obstruction to a pure non-CP pentagonal stress."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
EXPECTED = {
    9: {"kernel": 971, "cycle_multisets": {"11112": 5, "11122": 40,
                                            "11222": 60, "12222": 20,
                                            "22222": 1}},
    10: {"kernel": 1133, "cycle_multisets": {"11111": 1, "11112": 25,
                                               "11122": 100, "11222": 100,
                                               "12222": 25, "22222": 1}},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fixture():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "kernel fixture changed")
    return json.loads(raw.decode("ascii"))["kernels"]


def audit_algebra():
    # In Q[rho]/(4 rho^2 - 2 rho - 1), verify
    # (1-rho)/(1+rho) = (7-8 rho)/5 by coefficient arithmetic.
    # (a+b*rho)(1+rho) reduces to (a+b/4)+(a+3*b/2)rho.
    # We scale the candidate quotient by five, so it must multiply to
    # 5(1-rho).
    a, b = 7, -8
    require((4 * a + b, 2 * a + 3 * b) == (20, -10),
            "pentagonal odd-unit identity changed")
    require(b != 0, "pentagonal irrational coefficient vanished")


def root(parent, vertex):
    while parent[vertex] != vertex:
        parent[vertex] = parent[parent[vertex]]
        vertex = parent[vertex]
    return vertex


def pentagonal_contractions(order, code):
    pairs = tuple(itertools.combinations(range(order), 2))
    support = tuple((edge, value) for edge, value in zip(pairs, code) if value)
    result = []
    for kept in itertools.combinations(range(len(support)), 5):
        kept = frozenset(kept)
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
        if not valid or len({root(parent, v) for v in range(order)}) != 5:
            continue
        classes = {}
        labels = [classes.setdefault(root(parent, v), len(classes)) for v in range(order)]
        edges = []
        degrees = [0] * 5
        for index in kept:
            (u, v), multiplicity = support[index]
            edge = tuple(sorted((labels[u], labels[v])))
            if edge[0] == edge[1] or edge in [item[0] for item in edges]:
                valid = False
                break
            edges.append((edge, multiplicity))
            degrees[edge[0]] += 1
            degrees[edge[1]] += 1
        if valid and degrees == [2] * 5:
            result.append("".join(str(value) for value in sorted(value for _, value in edges)))
    return tuple(result)


def derive():
    audit_algebra()
    kernels = fixture()
    report = {}
    for order in (9, 10):
        rows = []
        sources = [(number, record) for number, record in enumerate(kernels, 1)
                   if record["n"] == order]
        require(len(sources) == {9: 162, 10: 66}[order],
                f"order-{order} kernel count changed")
        pairs = tuple(itertools.combinations(range(order), 2))
        for number, record in sources:
            require(sum(record["code"]) == order + 5,
                    f"rank-six path count changed at K{number}")
            degrees = [0] * order
            for (u, v), multiplicity in zip(pairs, record["code"]):
                degrees[u] += multiplicity
                degrees[v] += multiplicity
            expected_degrees = [4] + [3] * 8 if order == 9 else [3] * 10
            require(sorted(degrees, reverse=True) == expected_degrees,
                    f"cubic/near-cubic ledger changed at K{number}")
            contractions = pentagonal_contractions(order, tuple(record["code"]))
            if contractions:
                histogram = {key: contractions.count(key) for key in sorted(set(contractions))}
                rows.append({"kernel": number, "cycle_multisets": histogram})
        require(rows == [EXPECTED[order]], f"order-{order} pentagonal ledger changed: {rows}")
        report[str(order)] = rows[0]
    return {
        "schema": "rank6-orders9-10-pentagonal-stress-obstruction-v1",
        "source_sha256": SOURCE_SHA256,
        "orders": report,
        "algebra": {
            "rho_minimal_polynomial": "4*rho^2-2*rho-1",
            "odd_unit_value": "(7-8*rho)/5",
            "coefficient_of_rho": "-8/5",
            "conclusion": "a nonempty pure pentagonal odd-unit ledger has irrational objective",
        },
    }


def main():
    payload = derive()
    print(json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False))


if __name__ == "__main__":
    main()
