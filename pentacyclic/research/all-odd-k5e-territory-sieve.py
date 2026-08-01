#!/usr/bin/env python3
"""Exact territory sieve for all-odd subdivisions of K5 minus one edge."""

import itertools
from collections import Counter


# Vertices are a,b,x,y,z.  The missing edge is ab.  A state entry is
# 0 = unit, 1 = long of length 3 mod 4, 2 = long of length 1 mod 4.
EDGES = (
    ("a", "x"), ("a", "y"), ("a", "z"),
    ("b", "x"), ("b", "y"), ("b", "z"),
    ("x", "y"), ("x", "z"), ("y", "z"),
)
CENTERS = ("x", "y", "z")
EDGE_INDEX = {tuple(sorted(edge)): index for index, edge in enumerate(EDGES)}

EXPECTED_DISPOSITIONS = {
    "simplex": 18848,
    "complete-k4": 53,
    "favorable-theta": 640,
    "residual": 142,
}
EXPECTED_RESIDUAL_ORBITS = (
    "000001100", "001010000",
    "000000111", "000001101", "000001102", "000011001",
    "000012010", "001001100", "001002100", "001010002",
    "001010010", "001010020", "001011000", "001012000",
    "001020100", "001120000",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge_index(u, v):
    return EDGE_INDEX[tuple(sorted((u, v)))]


def retained_k4_is_complete(state, deleted_endpoint):
    other = "b" if deleted_endpoint == "a" else "a"
    retained = [edge_index(other, center) for center in CENTERS]
    retained.extend(edge_index(u, v) for u, v in itertools.combinations(CENTERS, 2))
    return all(state[index] == 0 for index in retained)


def center_deletion_is_favorable(state, deleted_center):
    u, v = (center for center in CENTERS if center != deleted_center)
    middle = state[edge_index(u, v)]
    for endpoint in ("a", "b"):
        cycle = (middle, state[edge_index(endpoint, u)], state[edge_index(endpoint, v)])
        # A sum of three odd lengths is 3 mod 4 exactly when an even number
        # of its paths have length 3 mod 4.
        if sum(value == 1 for value in cycle) % 2:
            return False
    return True


def disposition(state):
    long_count = sum(value != 0 for value in state)
    if long_count >= 4:
        return "simplex"
    if any(retained_k4_is_complete(state, endpoint) for endpoint in ("a", "b")):
        return "complete-k4"
    if any(center_deletion_is_favorable(state, center) for center in CENTERS):
        return "favorable-theta"
    return "residual"


def transform(state, center_permutation, swap_endpoints):
    vertex_map = dict(zip(CENTERS, center_permutation))
    vertex_map["a"] = "b" if swap_endpoints else "a"
    vertex_map["b"] = "a" if swap_endpoints else "b"
    transformed = [None] * len(EDGES)
    for index, (u, v) in enumerate(EDGES):
        transformed[edge_index(vertex_map[u], vertex_map[v])] = state[index]
    return tuple(transformed)


def canonical(state):
    return min(
        transform(state, permutation, swap)
        for permutation in itertools.permutations(CENTERS)
        for swap in (False, True)
    )


def audit():
    states = tuple(itertools.product(range(3), repeat=len(EDGES)))
    require(len(states) == 3 ** 9, "state-space size changed")
    dispositions = Counter(disposition(state) for state in states)
    require(dict(dispositions) == EXPECTED_DISPOSITIONS, "disposition ledger changed")

    residuals = tuple(state for state in states if disposition(state) == "residual")
    representatives = tuple(sorted({canonical(state) for state in residuals},
                                   key=lambda state: (sum(value != 0 for value in state), state)))
    encoded = tuple("".join(map(str, state)) for state in representatives)
    require(encoded == EXPECTED_RESIDUAL_ORBITS, "residual orbit ledger changed")
    require(Counter(sum(value != 0 for value in state) for state in residuals) == {2: 12, 3: 130},
            "residual long-count ledger changed")
    return dispositions, encoded


def main():
    dispositions, encoded = audit()
    print("all-odd K5-e territory sieve: exact audit passed")
    print("states=19683 simplex=18848 complete_k4=53 favorable_theta=640 residual=142")
    print(f"residual_orbits={len(encoded)} long_count_2=2 long_count_3=14")
    print("residual_keys=" + ",".join(encoded))


if __name__ == "__main__":
    main()
