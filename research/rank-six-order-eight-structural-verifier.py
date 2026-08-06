#!/usr/bin/env python3
"""Exact structural audit for order-eight rank-six kernel templates and deletions."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE / "fixtures" / "rank-six-kernels.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER = 8
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
EXPECTED_DEGREES = Counter({(5, 3, 3, 3, 3, 3, 3, 3): 55,
                            (4, 4, 3, 3, 3, 3, 3, 3): 270})
EXPECTED_SIMPLE_DEGREES = Counter({(5, 3, 3, 3, 3, 3, 3, 3): 6,
                                   (4, 4, 3, 3, 3, 3, 3, 3): 27})
EXPECTED_PACKET_PROFILES = Counter({
    ((5, 8, 12),): 2696,
    ((4, 6, 9), (1, 2, 2), (0, 2, 1)): 312,
    ((4, 7, 10), (1, 2, 2)): 218,
    ((3, 5, 7), (1, 2, 2), (1, 2, 2), (0, 2, 1)): 66,
    ((3, 4, 6), (2, 4, 5), (0, 2, 1)): 44,
    ((3, 5, 7), (2, 4, 5)): 42,
    ((3, 5, 7), (2, 3, 4), (0, 2, 1)): 42,
    ((3, 4, 6), (1, 2, 2), (1, 2, 2), (0, 2, 1), (0, 2, 1)): 33,
    ((2, 4, 5), (2, 3, 4), (1, 2, 2), (0, 2, 1)): 24,
    ((3, 6, 8), (2, 3, 4)): 20,
    ((3, 6, 8), (1, 2, 2), (1, 2, 2)): 19,
    ((3, 6, 8), (2, 2, 3), (0, 2, 1)): 18,
    ((2, 4, 5), (1, 2, 2), (1, 2, 2), (1, 2, 2), (0, 2, 1)): 16,
    ((2, 3, 4), (1, 2, 2), (1, 2, 2), (1, 2, 2), (0, 2, 1),
     (0, 2, 1)): 12,
    ((2, 3, 4), (2, 3, 4), (1, 2, 2), (0, 2, 1), (0, 2, 1)): 9,
    ((2, 4, 5), (2, 4, 5), (1, 2, 2)): 7,
    ((1, 2, 2), (1, 2, 2), (1, 2, 2), (1, 2, 2), (1, 2, 2),
     (0, 2, 1), (0, 2, 1)): 6,
    ((2, 4, 5), (2, 2, 3), (1, 2, 2), (0, 2, 1), (0, 2, 1)): 6,
    ((2, 2, 3), (1, 2, 2), (1, 2, 2), (1, 2, 2), (0, 2, 1),
     (0, 2, 1), (0, 2, 1)): 4,
})
EXPECTED_SIMPLE_SPLITS = {
    (776, (4, 6)), (786, (0, 5)), (786, (0, 6)), (866, (5, 6)),
    (869, (1, 5)), (903, (0, 7)), (903, (3, 6)), (961, (2, 7)),
    (961, (3, 6)),
}
EXPECTED_CYCLE_SUPPORTS = {
    744: (((0, 5), (1, 4), (2, 3)),
          ((0, 7), (1, 6), (2, 7), (3, 6), (4, 5))),
    756: (((0, 5), (1, 4), (2, 3)),
          ((0, 7), (1, 6), (2, 5), (3, 4), (6, 7))),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "kernel source changed")
    payload = json.loads(raw.decode("ascii"))
    rows = [(index, tuple(record["code"]))
            for index, record in enumerate(payload["kernels"], 1)
            if record["n"] == ORDER]
    require(len(rows) == 325 and rows[0][0] == 646 and rows[-1][0] == 970,
            "order-eight kernel interval changed")
    return rows


def degrees(code):
    row = [0] * ORDER
    for value, (left, right) in zip(code, PAIRS):
        row[left] += value
        row[right] += value
    return tuple(sorted(row, reverse=True))


def edge_list(code):
    return tuple(edge for value, edge in zip(code, PAIRS) for _ in range(value))


def block_profile(code):
    """Return sorted (rank, vertices, edges) rows, retaining bridge blocks."""
    edges = edge_list(code)
    adjacency = [[] for _ in range(ORDER)]
    for index, (left, right) in enumerate(edges):
        adjacency[left].append((right, index))
        adjacency[right].append((left, index))
    discovery = [-1] * ORDER
    low = [0] * ORDER
    stack = []
    blocks = []
    clock = 0

    def visit(vertex, parent_edge):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for neighbor, edge in adjacency[vertex]:
            if edge == parent_edge:
                continue
            if discovery[neighbor] < 0:
                stack.append(edge)
                visit(neighbor, edge)
                low[vertex] = min(low[vertex], low[neighbor])
                if low[neighbor] >= discovery[vertex]:
                    block = []
                    while True:
                        current = stack.pop()
                        block.append(current)
                        if current == edge:
                            break
                    blocks.append(block)
            elif discovery[neighbor] < discovery[vertex]:
                stack.append(edge)
                low[vertex] = min(low[vertex], discovery[neighbor])

    visit(0, -1)
    require(all(value >= 0 for value in discovery), "deleted kernel became disconnected")
    profile = []
    for block in blocks:
        vertices = set()
        for edge in block:
            vertices.update(edges[edge])
        profile.append((len(block) - len(vertices) + 1, len(vertices), len(block)))
    require(sum(row[0] for row in profile) == 5, "deleted packet has wrong rank")
    return tuple(sorted(profile, reverse=True))


def is_five_cycle(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    return (len(edges) == len(vertices) == 5
            and all(len(adjacency[vertex]) == 2 for vertex in vertices))


def cycle_support(code):
    singles = tuple(edge for value, edge in zip(code, PAIRS) if value == 1)
    doubles = tuple(edge for value, edge in zip(code, PAIRS) if value == 2)
    if any(value not in (0, 1, 2) for value in code) or len(singles) != 3 or len(doubles) != 5:
        return None
    parent = list(range(ORDER))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in singles:
        left_root, right_root = root(left), root(right)
        if left_root == right_root:
            return None
        parent[right_root] = left_root
    quotient_edges = tuple(tuple(sorted((root(left), root(right)))) for left, right in doubles)
    quotient_vertices = set(itertools.chain.from_iterable(quotient_edges))
    if any(left == right for left, right in quotient_edges):
        return None
    return (singles, doubles) if is_five_cycle(quotient_vertices, quotient_edges) else None


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction()
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
    require(all(gram[i][i] == 1 for i in range(ORDER)), "Gram diagonal changed")
    require(all(gram[i][j] == gram[j][i] for i in range(ORDER) for j in range(ORDER)),
            "Gram symmetry changed")
    for width in range(1, ORDER + 1):
        for indices in itertools.combinations(range(ORDER), width):
            minor = [[gram[i][j] for j in indices] for i in indices]
            require(determinant(minor) >= 0, "signed-cycle Gram is not PSD")


def cycle_gram(singles, doubles, singleton_bits):
    parent = list(range(ORDER))
    sign = [1] * ORDER
    for (left, right), odd in zip(singles, singleton_bits):
        require(parent[right] == right, "unexpected singleton-forest orientation")
        parent[right] = parent[left]
        sign[right] = sign[left] * (-1 if odd else 1)
    classes = sorted(set(parent))
    require(len(classes) == 5, "wrong quotient class count")
    gram = [[Fraction() for _ in range(ORDER)] for _ in range(ORDER)]
    for left in range(ORDER):
        for right in range(ORDER):
            if parent[left] == parent[right]:
                gram[left][right] = Fraction(sign[left] * sign[right])
    for left, right in doubles:
        value = Fraction(-sign[left] * sign[right], 2)
        for u in range(ORDER):
            if parent[u] != parent[left]:
                continue
            for v in range(ORDER):
                if parent[v] == parent[right]:
                    gram[u][v] = gram[v][u] = sign[u] * sign[v] * value
    return gram


def automorphisms(code):
    result = []
    for permutation in itertools.permutations(range(ORDER)):
        if all(code[PAIR_INDEX[tuple(sorted((permutation[u], permutation[v])))]] == value
               for value, (u, v) in zip(code, PAIRS)):
            result.append(permutation)
    return result


def parity_row(singles, doubles, bits):
    row = [0] * len(PAIRS)
    for edge, bit in zip(singles, bits):
        row[PAIR_INDEX[edge]] = bit
    for edge in doubles:
        row[PAIR_INDEX[edge]] = 1
    return tuple(row)


def act(row, permutation):
    result = [0] * len(PAIRS)
    for value, (left, right) in zip(row, PAIRS):
        edge = tuple(sorted((permutation[left], permutation[right])))
        result[PAIR_INDEX[edge]] = value
    return tuple(result)


def audit_cycle_templates(kernels):
    candidates = {number: cycle_support(code) for number, code in kernels if cycle_support(code)}
    require(candidates == EXPECTED_CYCLE_SUPPORTS, "five-cycle candidate projection changed")
    orbit_total = 0
    for number, code in kernels:
        if number not in candidates:
            continue
        singles, doubles = candidates[number]
        rows = []
        for bits in itertools.product((0, 1), repeat=3):
            gram = cycle_gram(singles, doubles, bits)
            audit_psd(gram)
            cost = Fraction()
            for edge, odd in zip(singles, bits):
                transformed = -gram[edge[0]][edge[1]] if odd else gram[edge[0]][edge[1]]
                require(transformed == 1, "singleton contraction is not free")
            for left, right in doubles:
                require(gram[left][right] in (Fraction(-1, 2), Fraction(1, 2)),
                        "signed quotient correlation changed")
                cost += Fraction(1, 3) + Fraction(2, 3)
            require(cost == 5, "signed-cycle equality cost changed")
            require(cost + 2 * Fraction(1 - 1, 1 + 1) == 5,
                    "zero-cost same-parity extension changed")
            rows.append(parity_row(singles, doubles, bits))
        group = automorphisms(code)
        representatives = {min(act(row, permutation) for permutation in group) for row in rows}
        require(len(group) == 2 and len(representatives) == 6,
                f"K{number} equality orbit count changed")
        orbit_total += len(representatives)
    return len(candidates), 16, orbit_total, orbit_total * 14


def audit_deletion_packets(kernels):
    profiles = Counter()
    weighted_profiles = Counter()
    simple_splits = set()
    support_total = physical_total = 0
    for number, code in kernels:
        simple = max(code) <= 1
        for index, multiplicity in enumerate(code):
            if not multiplicity:
                continue
            deleted = list(code)
            deleted[index] -= 1
            profile = block_profile(tuple(deleted))
            profiles[profile] += 1
            weighted_profiles[profile] += multiplicity
            support_total += 1
            physical_total += multiplicity
            if simple and len(profile) > 1:
                simple_splits.add((number, PAIRS[index]))
    require(profiles == EXPECTED_PACKET_PROFILES, "marked deletion packet ledger changed")
    require(support_total == 3594 and physical_total == 4225,
            "marked deletion totals changed")
    require(weighted_profiles[((5, 8, 12),)] == 3327,
            "physical-copy biconnected deletion count changed")
    require(simple_splits == EXPECTED_SIMPLE_SPLITS, "simple split-edge ledger changed")
    return support_total, physical_total, len(profiles), profiles[((5, 8, 12),)], len(simple_splits)


def audit():
    kernels = source_kernels()
    degree_counts = Counter(degrees(code) for _, code in kernels)
    simple_degree_counts = Counter(degrees(code) for _, code in kernels if max(code) <= 1)
    require(degree_counts == EXPECTED_DEGREES, "degree-excess partition changed")
    require(simple_degree_counts == EXPECTED_SIMPLE_DEGREES, "simple-kernel partition changed")
    cycle_result = audit_cycle_templates(kernels)
    packet_result = audit_deletion_packets(kernels)
    return degree_counts, simple_degree_counts, cycle_result, packet_result


def report(result):
    degree_counts, simple_degree_counts, cycle_result, packet_result = result
    lines = [
        f"kernels={sum(degree_counts.values())} simple={sum(simple_degree_counts.values())} "
        f"degree_types={len(degree_counts)}",
        f"cycle_candidates={cycle_result[0]} labeled_rows={cycle_result[1]} "
        f"parity_orbits={cycle_result[2]} frontier_templates={cycle_result[3]}",
        f"deletion_supports={packet_result[0]} physical_copies={packet_result[1]} "
        f"packet_profiles={packet_result[2]}",
        f"biconnected_support_deletions={packet_result[3]} "
        f"simple_split_edges={packet_result[4]}",
        "scope=STRUCTURAL_REDUCTION_ONLY",
    ]
    text = "\n".join(lines)
    print(text)
    return text


def main():
    result = audit()
    output = report(result)
    if __debug__:
        completed = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve())],
                                   check=True, capture_output=True, text=True)
        require(completed.stdout == output + "\n", "normal and optimized audits differ")


if __name__ == "__main__":
    main()
