#!/usr/bin/env python3
"""Audit the finite structural claims in the order-seven--ten reduction note."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
EXPECTED_SIMPLE = {7: 17, 8: 33, 9: 25, 10: 18}
EXPECTED_DEGREES = {
    7: Counter({(4, 4, 4, 3, 3, 3, 3): 165,
                (5, 4, 3, 3, 3, 3, 3): 134,
                (6, 3, 3, 3, 3, 3, 3): 15}),
    8: Counter({(4, 4, 3, 3, 3, 3, 3, 3): 270,
                (5, 3, 3, 3, 3, 3, 3, 3): 55}),
    9: Counter({(4, 3, 3, 3, 3, 3, 3, 3, 3): 162}),
    10: Counter({(3, 3, 3, 3, 3, 3, 3, 3, 3, 3): 66}),
}
EXPECTED_CYCLE_QUOTIENTS = {
    7: (534, 548),
    8: (744, 756),
    9: (971,),
    10: (1133,),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pairs(n):
    return tuple((u, v) for u in range(n) for v in range(u + 1, n))


def degrees(n, code):
    result = [0] * n
    for value, (u, v) in zip(code, pairs(n)):
        result[u] += value
        result[v] += value
    return tuple(result)


def five_cycle_quotient(n, code):
    """Contract singleton forest and test whether five doubles form C5."""
    if max(code) != 2 or sum(value == 2 for value in code) != 5:
        return False
    parent = list(range(n))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    edge_pairs = pairs(n)
    for value, (u, v) in zip(code, edge_pairs):
        if value != 1:
            continue
        u, v = root(u), root(v)
        if u == v:
            return False
        parent[v] = u
    roots = {root(vertex) for vertex in range(n)}
    if len(roots) != 5:
        return False
    quotient_degree = {vertex: 0 for vertex in roots}
    for value, (u, v) in zip(code, edge_pairs):
        if value != 2:
            continue
        u, v = root(u), root(v)
        if u == v:
            return False
        quotient_degree[u] += 1
        quotient_degree[v] += 1
    return all(value == 2 for value in quotient_degree.values())


def audit():
    payload = json.loads(FIXTURE.read_text())
    kernels = payload["kernels"]
    for order in range(7, 11):
        rows = [(index + 1, tuple(row["code"]))
                for index, row in enumerate(kernels) if row["n"] == order]
        degree_ledger = Counter(tuple(sorted(degrees(order, code), reverse=True))
                                for _, code in rows)
        require(degree_ledger == EXPECTED_DEGREES[order],
                f"order-{order} degree ledger changed")
        require(all(sum(value - 3 for value in degrees(order, code)) == 10 - order
                    for _, code in rows),
                f"order-{order} degree-excess identity failed")
        simple = sum(max(code) == 1 for _, code in rows)
        require(simple == EXPECTED_SIMPLE[order],
                f"order-{order} simple-kernel count changed")
        quotient_ids = tuple(index for index, code in rows
                             if five_cycle_quotient(order, code))
        require(quotient_ids == EXPECTED_CYCLE_QUOTIENTS[order],
                f"order-{order} five-cycle quotient list changed")
    return sum(EXPECTED_SIMPLE.values()), sum(map(len, EXPECTED_CYCLE_QUOTIENTS.values()))


def main():
    simple, equality = audit()
    print("rank-six orders 7-10 structural audit passed")
    print(f"simple_kernel_base_total: {simple}")
    print(f"signed_five_cycle_kernel_total: {equality}")


if __name__ == "__main__":
    main()
