#!/usr/bin/env python3
"""Exact all-descendant branch-Gram gate for the order-nine obstruction frontier.

The verifier authenticates and reconstructs the 1,615-row frontier left by the
order-nine induced-partition theorem after the three named persisted Gram
streams.  It checks a deterministic switched-three-ray CSP with rigorous
integer upper charges.  The sole CSP residual is closed by one embedded exact
rational correlation matrix.  Every accepted row is owned by one branch Gram
at its canonical simple vector; fixed-parity path monotonicity therefore owns
all coordinate frontiers and every same-parity descendant.

Only Python's standard library is used.  There is no floating-point arithmetic,
assert statement, numerical PSD decision, or trusted precomputed row list.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURE = HERE / "fixtures/rank-seven-kernel-frontier-census.json"
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
SOURCE = EXPERIMENTS / "rank7_order9_after_sos_remainder.jsonl.xz"
LANES = (
    EXPERIMENTS / "rank7_order9_dominant_family_gram_owners.jsonl.xz",
    EXPERIMENTS / "rank7_order9_third_family_cycle_gram_owners.jsonl.xz",
    EXPERIMENTS / "rank7_order9_fourth_family_cycle_gram_owners.jsonl.xz",
)
EXPECTED = {
    "fixture": "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    "source_xz": "2a45b69d495e65c47d4b3c668572b0b7922e808c905c501c97e513df47d05089",
    "source_raw": "fb28f9f36cafad170995f7dff43fb0d8cd1effa08765dd283461fb011d4cba7b",
    "lanes_xz": (
        "5d41ae256f123a6fa6a31bed226b069ea070e52aaf50199c06d0dbfd0b914de9",
        "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
        "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
    ),
    "lanes_raw": (
        "f2748ded8f67638f6b44dc5dbdb111edddbbead4fe1be7b47f97edcf1cb744ba",
        "2f35c2a76ce054be0d5b2ed18c0bfd77f163c1429af35ca48b91313ba77d0154",
        "a347d2d7891609156692d0bf0614783d79a9b84c6f4e0902ef6672f1cb4c96f5",
    ),
    "lane_rows": (1128, 631, 1036),
}
ORDER = 9
FULL_MASK = (1 << ORDER) - 1
PATH_COUNT = 15
SCALE = 60
BUDGET = 6 * SCALE

# Rigorous upper charges SCALE*f_L(r), indexed by (canonical length,
# transformed endpoint correlation).  The frontier reconstruction below
# fail-closed checks that only lengths one and two occur.  Three entries are
# exact; the strict entry 9 is proved in the companion note.
CHARGE = {
    (1, Fraction(1, 2)): 20,
    (1, Fraction(-1, 2)): 180,
    (2, Fraction(1, 2)): 9,
    (2, Fraction(-1, 2)): 40,
}

DIRECT_SOURCE = (2584311, 11564, 4078, (1,) * 15, 1)
DIRECT_MATRIX_DATA = (
    ((1,1),(10,23),(7,24),(-11,23),(14,17),(3,29),(-4,5),(-7,11),(-10,31)),
    ((10,23),(1,1),(-11,23),(7,24),(14,17),(-4,5),(3,29),(-7,11),(-10,31)),
    ((7,24),(-11,23),(1,1),(-4,27),(-1,8),(17,29),(-18,25),(11,23),(-9,17)),
    ((-11,23),(7,24),(-4,27),(1,1),(-1,8),(-18,25),(17,29),(11,23),(-9,17)),
    ((14,17),(14,17),(-1,8),(-1,8),(1,1),(-13,32),(-13,32),(-13,17),(-5,14)),
    ((3,29),(-4,5),(17,29),(-18,25),(-13,32),(1,1),(-5,9),(6,29),(10,31)),
    ((-4,5),(3,29),(-18,25),(17,29),(-13,32),(-5,9),(1,1),(6,29),(10,31)),
    ((-7,11),(-7,11),(11,23),(11,23),(-13,17),(6,29),(6,29),(1,1),(-3,11)),
    ((-10,31),(-10,31),(-9,17),(-9,17),(-5,14),(10,31),(10,31),(-3,11),(1,1)),
)
DIRECT_COST = Fraction(607593754, 122731245)
DIRECT_PIVOTS = (
    Fraction(1),
    Fraction(429, 529),
    Fraction(114527, 247104),
    Fraction(18575533187, 104690505024),
    Fraction(16893611, 313686669),
    Fraction(22115545080139280247, 466834327076602240000),
    Fraction(43723152036881631881605412, 941583154002604943566179375),
    Fraction(240810798556848021, 4635649647213071861),
    Fraction(177718468252360464231472, 3277126971347347357191141),
)
EXPECTED_FAILURE_DIGEST = "36de30c8246679bd6cafdc7fa2abbe51b5a6f1267e9bf0aa2b1e7d61f447b12a"
EXPECTED_WITNESS_DIGEST = "912058dbc7f22d33bd777c4b848aaba7168f8dd280a1605871403eb22a213d4c"
EXPECTED_COST_HISTOGRAM = (
    (218,16),(220,4),(227,4),(229,13),(238,40),(240,20),(247,23),(249,44),
    (256,5),(258,63),(260,43),(265,2),(267,54),(269,127),(276,8),(278,99),
    (280,170),(287,20),(289,172),(298,53),(300,212),(307,1),(309,106),
    (318,3),(320,182),(329,11),(338,2),(340,44),(347,3),(349,17),
    (356,3),(358,30),(360,20),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def load_kernels():
    require(sha256(FIXTURE) == EXPECTED["fixture"], "kernel fixture changed")
    raw = FIXTURE.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(tuple(payload["counts_by_order_n2_to_n12"]) ==
            (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365),
            "kernel order counts changed")
    kernels = {}
    local = 0
    for global_index, record in enumerate(payload["kernels"], 1):
        if record["n"] != ORDER:
            continue
        local += 1
        require(type(record["code"]) is list and len(record["code"]) == 36,
                "malformed order-nine kernel code")
        edges = tuple((u, v, multiplicity)
                      for (u, v), multiplicity in zip(
                          itertools.combinations(range(ORDER), 2), record["code"], strict=True)
                      if multiplicity)
        require(sum(m for _, _, m in edges) == PATH_COUNT,
                "order-nine physical-edge count changed")
        kernels[local] = (global_index, edges)
    require(len(kernels) == 4495, "order-nine kernel count changed")
    return kernels


def connected_rank(edges, mask):
    vertices = {v for v in range(ORDER) if mask >> v & 1}
    require(vertices, "empty induced territory")
    adjacency = {v: set() for v in vertices}
    edge_total = 0
    for u, v, multiplicity in edges:
        if u in vertices and v in vertices:
            adjacency[u].add(v)
            adjacency[v].add(u)
            edge_total += multiplicity
    seen = {min(vertices)}
    todo = list(seen)
    while todo:
        vertex = todo.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            todo.append(neighbor)
    return seen == vertices, edge_total - len(vertices) + 1


def partition_applicable(edges):
    for mask in range(1, 1 << (ORDER - 1)):
        left = connected_rank(edges, mask)
        right = connected_rank(edges, FULL_MASK ^ mask)
        if left[0] and right[0] and left[1] >= 2 and right[1] >= 2:
            return True
    return False


def canonical_paths(edges, row):
    require(type(row) is list and len(row) == len(edges), "row width changed")
    paths = []
    for (u, v, multiplicity), odd_total in zip(edges, row, strict=True):
        require(type(odd_total) is int and 0 <= odd_total <= multiplicity,
                "invalid odd-count entry")
        lengths = (([1] + [3] * (odd_total - 1)) if odd_total else [])
        lengths += [2] * (multiplicity - odd_total)
        paths.extend((u, v, length) for length in lengths)
    require(len(paths) == PATH_COUNT, "physical path count changed")
    return tuple(paths)


def load_source(kernels):
    require(sha256(SOURCE) == EXPECTED["source_xz"], "source compressed bytes changed")
    digest = hashlib.sha256()
    rows = []
    by_index = {}
    with lzma.open(SOURCE, "rb") as stream:
        for raw in stream:
            digest.update(raw)
            record = json.loads(raw.decode("ascii"))
            require(raw == canonical_bytes(record), "noncanonical source row")
            require(type(record) is list and len(record) == 5, "malformed source row")
            source_index, global_kernel, local_kernel, row, orbit = record
            require(type(source_index) is int and source_index not in by_index,
                    "duplicate or noninteger source index")
            require(type(local_kernel) is int and local_kernel in kernels and
                    kernels[local_kernel][0] == global_kernel,
                    "global/local kernel mismatch")
            require(type(orbit) is int and orbit > 0, "invalid orbit size")
            canonical_paths(kernels[local_kernel][1], row)
            rows.append(record)
            by_index[source_index] = record
    require(digest.hexdigest() == EXPECTED["source_raw"], "source raw bytes changed")
    require(len(rows) == 272520, "source row total changed")
    return rows, by_index


def load_lane_indices(by_index):
    indices = set()
    for position, path in enumerate(LANES):
        require(sha256(path) == EXPECTED["lanes_xz"][position],
                f"{path.name} compressed bytes changed")
        digest = hashlib.sha256()
        count = 0
        with lzma.open(path, "rb") as stream:
            for raw in stream:
                digest.update(raw)
                owner = json.loads(raw.decode("ascii"))
                require(raw == canonical_bytes(owner), f"noncanonical owner in {path.name}")
                require(type(owner) is list and len(owner) == 4 and
                        type(owner[0]) is list and len(owner[0]) == 5,
                        f"malformed owner in {path.name}")
                source_index = owner[0][0]
                require(by_index.get(source_index) == owner[0],
                        f"{path.name} owner is not an exact source row")
                require(source_index not in indices, "persisted owner lanes overlap")
                indices.add(source_index)
                count += 1
        require(digest.hexdigest() == EXPECTED["lanes_raw"][position],
                f"{path.name} raw bytes changed")
        require(count == EXPECTED["lane_rows"][position],
                f"{path.name} row count changed")
    require(len(indices) == 2795, "persisted owner union count changed")
    return indices


def bundle_charge(multiplicity, odd_total, left, right):
    left_color, left_switch = divmod(left, 2)
    right_color, right_switch = divmod(right, 2)
    correlation = Fraction(1) if left_color == right_color else Fraction(-1, 2)
    if left_switch != right_switch:
        correlation = -correlation
    lengths = (([1] + [3] * (odd_total - 1)) if odd_total else [])
    lengths += [2] * (multiplicity - odd_total)
    charge = 0
    for length in lengths:
        transformed = (-1 if length & 1 else 1) * correlation
        if transformed == -1:
            return None
        if transformed != 1:
            require((length, transformed) in CHARGE, "missing canonical charge")
            charge += CHARGE[length, transformed]
    return charge


def switched_three_ray_witness(edges, row):
    tables = []
    bounds = []
    incidence = [[] for _ in range(ORDER)]
    for edge_index, ((u, v, multiplicity), odd_total) in enumerate(
            zip(edges, row, strict=True)):
        table = tuple(tuple(bundle_charge(multiplicity, odd_total, a, b)
                            for b in range(6)) for a in range(6))
        finite = [value for line in table for value in line if value is not None]
        require(finite, "bundle has no finite switched-three-ray state")
        tables.append(table)
        bounds.append((
            min(finite),
            tuple(min(value for value in line if value is not None) for line in table),
            tuple(min(table[a][b] for a in range(6) if table[a][b] is not None)
                  for b in range(6)),
        ))
        incidence[u].append((edge_index, v, False))
        incidence[v].append((edge_index, u, True))

    states = [-1] * ORDER
    states[0] = 0  # removes the global ray-permutation/switch symmetry needed here

    def visit(assigned, cost):
        lower = 0
        for edge_index, (u, v, _) in enumerate(edges):
            if states[u] >= 0 and states[v] >= 0:
                continue
            lower += (bounds[edge_index][1][states[u]] if states[u] >= 0 else
                      bounds[edge_index][2][states[v]] if states[v] >= 0 else
                      bounds[edge_index][0])
        if cost + lower > BUDGET:
            return None
        if assigned == ORDER:
            return tuple(states)
        vertex = max((v for v in range(ORDER) if states[v] < 0),
                     key=lambda v: sum(states[w] >= 0 for _, w, _ in incidence[v]))
        choices = []
        for state in range(6):
            extra = 0
            for edge_index, neighbor, reversed_edge in incidence[vertex]:
                if states[neighbor] < 0:
                    continue
                value = (tables[edge_index][states[neighbor]][state]
                         if reversed_edge else tables[edge_index][state][states[neighbor]])
                if value is None:
                    break
                extra += value
            else:
                choices.append((extra, state))
        for extra, state in sorted(choices):
            if cost + extra <= BUDGET:
                states[vertex] = state
                witness = visit(assigned + 1, cost + extra)
                if witness is not None:
                    return witness
                states[vertex] = -1
        return None

    return visit(1, 0)


def replay_witness(edges, row, witness):
    require(type(witness) is tuple and len(witness) == ORDER and witness[0] == 0 and
            all(type(state) is int and 0 <= state < 6 for state in witness),
            "malformed switched-three-ray witness")
    total = 0
    for (u, v, multiplicity), odd_total in zip(edges, row, strict=True):
        value = bundle_charge(multiplicity, odd_total, witness[u], witness[v])
        require(value is not None, "witness has an infinite bundle")
        total += value
    require(total <= BUDGET, "witness exceeds the exact upper-charge budget")
    return total


def fraction_matrix(data):
    require(type(data) is tuple and len(data) == ORDER, "direct matrix order changed")
    matrix = []
    for row in data:
        require(type(row) is tuple and len(row) == ORDER, "direct matrix row changed")
        parsed = []
        for pair in row:
            require(type(pair) is tuple and len(pair) == 2 and
                    type(pair[0]) is int and type(pair[1]) is int and pair[1] > 0,
                    "malformed direct rational")
            value = Fraction(pair[0], pair[1])
            require((value.numerator, value.denominator) == pair,
                    "noncanonical direct rational")
            parsed.append(value)
        matrix.append(parsed)
    return matrix


def exact_ldl(matrix):
    n = len(matrix)
    lower = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    pivots = []
    for i in range(n):
        lower[i][i] = Fraction(1)
        pivot = matrix[i][i] - sum(lower[i][k] * lower[i][k] * pivots[k]
                                    for k in range(i))
        require(pivot > 0, "direct matrix is not positive definite")
        pivots.append(pivot)
        for j in range(i + 1, n):
            lower[j][i] = (matrix[j][i] -
                           sum(lower[j][k] * lower[i][k] * pivots[k]
                               for k in range(i))) / pivot
    for i in range(n):
        for j in range(n):
            reconstructed = sum(lower[i][k] * pivots[k] * lower[j][k]
                                for k in range(min(i, j) + 1))
            require(reconstructed == matrix[i][j], "direct LDL replay failed")
    return tuple(pivots)


def verify_direct(record, edges):
    require(tuple((record[0], record[1], record[2], tuple(record[3]), record[4])) ==
            DIRECT_SOURCE, "sole CSP residual source key changed")
    require(all(multiplicity == 1 for _, _, multiplicity in edges) and
            len(edges) == PATH_COUNT, "sole residual is not a simple 15-edge kernel")
    matrix = fraction_matrix(DIRECT_MATRIX_DATA)
    require(all(matrix[i][j] == matrix[j][i] for i in range(ORDER)
                for j in range(ORDER)), "direct matrix is not symmetric")
    require(all(matrix[i][i] == 1 for i in range(ORDER)),
            "direct matrix does not have unit diagonal")
    require(exact_ldl(matrix) == DIRECT_PIVOTS, "direct LDL pivots changed")
    cost = Fraction(0)
    for u, v, _ in edges:
        correlation = matrix[u][v]
        require(-1 < correlation < 1, "direct edge correlation is singular")
        # Every canonical path in this row is odd of length one, so
        # f_1(r)=(1+r)/(1-r).
        cost += (1 + correlation) / (1 - correlation)
    require(cost == DIRECT_COST and cost < 6, "direct exact cost changed")
    return cost


def verify():
    kernels = load_kernels()
    partition_owned = {local for local, (_, edges) in kernels.items()
                       if partition_applicable(edges)}
    require(len(partition_owned) == 4022, "partition-applicable kernel count changed")
    rows, by_index = load_source(kernels)
    excluded = load_lane_indices(by_index)
    frontier = [record for record in rows
                if record[0] not in excluded and record[2] not in partition_owned]
    require(len(frontier) == 1615 and sum(record[4] for record in frontier) == 1945 and
            len({record[2] for record in frontier}) == 115,
            "obstruction frontier changed")
    require(all(all(value <= 1 for value in record[3]) for record in frontier),
            "frontier contains a long canonical odd bundle")
    require(all(all(length in (1, 2) for _, _, length in
                    canonical_paths(kernels[record[2]][1], record[3]))
                for record in frontier),
            "frontier contains a canonical path outside lengths one and two")

    owned = []
    failures = []
    costs = Counter()
    for record in frontier:
        edges = kernels[record[2]][1]
        witness = switched_three_ray_witness(edges, record[3])
        if witness is None:
            failures.append(record)
            continue
        cost = replay_witness(edges, record[3], witness)
        owned.append((record, witness, cost))
        costs[cost] += 1

    require(len(owned) == 1614 and sum(item[0][4] for item in owned) == 1944 and
            len(failures) == 1 and failures[0][4] == 1,
            "switched-three-ray coverage changed")
    failure_digest = hashlib.sha256(b"".join(canonical_bytes(record)
                                                for record in failures)).hexdigest()
    witness_digest = hashlib.sha256(b"".join(canonical_bytes([record, witness, cost])
                                                for record, witness, cost in owned)).hexdigest()
    require(failure_digest == EXPECTED_FAILURE_DIGEST, "CSP residual digest changed")
    require(witness_digest == EXPECTED_WITNESS_DIGEST, "CSP witness stream changed")
    require(tuple(sorted(costs.items())) == EXPECTED_COST_HISTOGRAM,
            "CSP cost histogram changed")
    direct_cost = verify_direct(failures[0], kernels[failures[0][2]][1])

    result = {
        "all_descendant_rows": 1615,
        "all_descendant_targets": 1615 * 16,
        "direct_exact_cost": [direct_cost.numerator, direct_cost.denominator],
        "direct_rows": 1,
        "frontier_physical_rows": 1945,
        "frontier_rows": 1615,
        "represented_kernels": 115,
        "switched_three_ray_max_scaled_charge": max(costs),
        "switched_three_ray_rows": 1614,
        "witness_stream_sha256": witness_digest,
    }
    return result


def main():
    result = verify()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("rank-seven order-nine obstruction branch-Gram verifier: PASS")


if __name__ == "__main__":
    main()
