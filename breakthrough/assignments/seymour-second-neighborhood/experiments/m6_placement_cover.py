#!/usr/bin/env python3
"""Build the canonical rooted-cell placement cover for the frozen m=6 supports."""

import argparse
import hashlib
import itertools
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

CELLS = "RABC"
BRANCHES = (("B6", (1, 8, 6, 3)), ("B7", (1, 8, 7, 2)))
SUPPORT_BYTES = 934
SUPPORT_SHA256 = "e97de806f6db6c3ac1768cab9259f7f0cd1c91ee26d949c1a3455ef8e471c8be"

# Frozen after generation and independent checking.  These constants deliberately
# make an accidental change to the cover convention fail loudly.
EXPECTED_ROWS = 187324
EXPECTED_BYTES = 6659672
EXPECTED_SHA256 = "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"


def decode_graph6(code):
    n = ord(code[0]) - 63
    bits = []
    for char in code[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(low, high) for high in range(1, n) for low in range(high)]
    return n, frozenset(edge for edge, bit in zip(pairs, bits) if bit)


def read_supports(path):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != SUPPORT_BYTES or digest != SUPPORT_SHA256:
        raise RuntimeError(f"frozen support payload changed: bytes={len(data)} sha256={digest}")
    lines = data.decode("ascii").splitlines()
    if lines[:4] != [
        "m6-support-census-v1",
        "edges\t6",
        "count\t68",
        "orders\t4:1,5:5,6:15,7:20,8:15,9:7,10:3,11:1,12:1",
    ]:
        raise RuntimeError("malformed frozen support header")
    rows = []
    for expected, line in enumerate(lines[4:]):
        index, order, code = line.split("\t")
        if index != f"{expected:03d}":
            raise RuntimeError("nonconsecutive support index")
        graph = decode_graph6(code)
        if graph[0] != int(order) or len(graph[1]) != 6:
            raise RuntimeError(f"bad support row {index}")
        rows.append((expected, graph[0], code, graph[1]))
    if len(rows) != 68:
        raise RuntimeError(f"expected 68 supports, found {len(rows)}")
    return rows


def components(n, edges):
    adjacent = [set() for _ in range(n)]
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    result = []
    unseen = set(range(n))
    while unseen:
        stack = [min(unseen)]
        vertices = []
        unseen.remove(stack[0])
        while stack:
            u = stack.pop()
            vertices.append(u)
            for v in sorted(adjacent[u], reverse=True):
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        vertices.sort()
        position = {v: i for i, v in enumerate(vertices)}
        local_edges = frozenset(
            tuple(sorted((position[u], position[v])))
            for u, v in edges
            if u in position and v in position
        )
        result.append((tuple(vertices), local_edges))
    return result


def edge_code(n, edges, labels):
    inverse = {old: new for new, old in enumerate(labels)}
    relabeled = {tuple(sorted((inverse[u], inverse[v]))) for u, v in edges}
    return tuple((low, high) in relabeled for high in range(1, n) for low in range(high))


def canonical_component(edges):
    n = max(max(edge) for edge in edges) + 1
    best_code = None
    best_labels = None
    for labels in itertools.permutations(range(n)):
        code = edge_code(n, edges, labels)
        if best_code is None or code < best_code:
            best_code, best_labels = code, labels
    canonical_edges = frozenset(
        (low, high)
        for bit, (low, high) in zip(
            best_code, ((low, high) for high in range(1, n) for low in range(high))
        )
        if bit
    )
    return (n, best_code), best_labels, canonical_edges


def automorphisms(n, edges):
    degrees = [0] * n
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    candidates = {u: [v for v in range(n) if degrees[v] == degrees[u]] for u in range(n)}
    order = sorted(range(n), key=lambda u: (len(candidates[u]), -degrees[u], u))
    mapping = [-1] * n
    used = [False] * n
    result = []

    def visit(depth):
        if depth == n:
            result.append(tuple(mapping))
            return
        u = order[depth]
        for v in candidates[u]:
            if used[v]:
                continue
            if any(
                (((min(u, x), max(u, x)) in edges) !=
                 ((min(v, mapping[x]), max(v, mapping[x])) in edges))
                for x in range(n) if mapping[x] >= 0
            ):
                continue
            mapping[u] = v
            used[v] = True
            visit(depth + 1)
            used[v] = False
            mapping[u] = -1

    visit(0)
    return result


def component_states(n, edges):
    group = automorphisms(n, edges)
    states = []
    for coloring in itertools.product(range(4), repeat=n):
        if coloring.count(0) > 1:
            continue
        if any({coloring[u], coloring[v]} == {0, 1} for u, v in edges):
            continue
        images = {tuple(coloring[permutation[i]] for i in range(n)) for permutation in group}
        if coloring != min(images):
            continue
        states.append((coloring, tuple(coloring.count(i) for i in range(4)), len(images)))
    return states


def support_placements(n, edges, capacity):
    """Return full-group canonical rows for the frozen component-canonical input.

    The construction uses canonical component labels and sorted equal-component
    blocks.  It is therefore tied to the labeling convention of the hashed
    support payload; the independent checker below recomputes each row's true
    minimum under the full automorphism group and is the gate against a broken
    convention or alternate labeling.
    """
    grouped = defaultdict(list)
    for vertices, local_edges in components(n, edges):
        kind, labels, canonical_edges = canonical_component(local_edges)
        grouped[kind].append((vertices, labels, canonical_edges))

    groups = []
    for kind in sorted(grouped):
        copies = grouped[kind]
        copies.sort(key=lambda item: item[0])
        states = component_states(kind[0], copies[0][2])
        groups.append((copies, states))

    rows = []
    selected = []

    def choose_group(group_index, used, internal_weight):
        if group_index == len(groups):
            coloring = [-1] * n
            weight = internal_weight
            for copies, choices in selected:
                multiplicities = Counter(index for index, _ in choices)
                weight *= math.factorial(len(copies))
                for count in multiplicities.values():
                    weight //= math.factorial(count)
                for (vertices, labels, _), (_, state) in zip(copies, choices):
                    canonical_coloring, _, state_weight = state
                    weight *= state_weight
                    for new, old_local in enumerate(labels):
                        coloring[vertices[old_local]] = canonical_coloring[new]
            rows.append((tuple(coloring), weight))
            return

        copies, states = groups[group_index]
        choices = []

        def choose_copy(copy_index, start, counts):
            if copy_index == len(copies):
                selected.append((copies, list(choices)))
                choose_group(group_index + 1, counts, internal_weight)
                selected.pop()
                return
            for state_index in range(start, len(states)):
                state = states[state_index]
                new_counts = tuple(counts[i] + state[1][i] for i in range(4))
                if any(new_counts[i] > capacity[i] for i in range(4)):
                    continue
                choices.append((state_index, state))
                choose_copy(copy_index + 1, state_index, new_counts)
                choices.pop()

        choose_copy(0, 0, used)

    choose_group(0, (0, 0, 0, 0), 1)
    rows.sort()
    return rows


def build_rows(supports):
    result = []
    for branch, capacity in BRANCHES:
        for support, order, code, edges in supports:
            for coloring, weight in support_placements(order, edges, capacity):
                result.append((branch, support, order, code, coloring, weight))
    return result


def make_payload(supports):
    rows = build_rows(supports)
    counts = Counter((branch, order) for branch, _, order, _, _, _ in rows)
    lines = [
        "m6-rooted-cell-placement-cover-v1",
        "supports\t68",
        "colors\tR,A,B,C",
        "forbidden\tR-A",
        "capacities\tB6:1,8,6,3;B7:1,8,7,2",
        f"count\t{len(rows)}",
        "branch-orders\t" + ";".join(
            branch + ":" + ",".join(f"{order}:{counts[branch, order]}" for order in range(4, 13))
            for branch, _ in BRANCHES
        ),
    ]
    lines.extend(
        f"{index:07d}\t{branch}\t{support:03d}\t{order}\t{code}\t"
        f"{''.join(CELLS[color] for color in coloring)}\t{weight}"
        for index, (branch, support, order, code, coloring, weight) in enumerate(rows)
    )
    return ("\n".join(lines) + "\n").encode("ascii"), counts


def assert_frozen(data, row_count):
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_ROWS is not None and row_count != EXPECTED_ROWS:
        raise RuntimeError(f"frozen row count changed: {row_count}")
    if EXPECTED_BYTES is not None and len(data) != EXPECTED_BYTES:
        raise RuntimeError(f"frozen payload size changed: {len(data)}")
    if EXPECTED_SHA256 is not None and digest != EXPECTED_SHA256:
        raise RuntimeError(f"frozen payload changed: sha256={digest}")
    return digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--supports", type=Path, default=Path(__file__).with_name("m6-support-census.txt"))
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--output", type=Path)
    action.add_argument("--check", type=Path)
    args = parser.parse_args()
    data, counts = make_payload(read_supports(args.supports))
    row_count = sum(counts.values())
    digest = assert_frozen(data, row_count)
    if args.check:
        if args.check.read_bytes() != data:
            raise RuntimeError(f"payload differs: {args.check}")
        verb = "PASS"
    elif args.output:
        args.output.write_bytes(data)
        verb = "WROTE"
    else:
        sys.stdout.buffer.write(data)
        verb = "BUILT"
    print(f"{verb} rows={row_count} bytes={len(data)} sha256={digest}", file=sys.stderr)
    for branch, _ in BRANCHES:
        print(branch + " orders=" + ",".join(str(counts[branch, order]) for order in range(4, 13)), file=sys.stderr)


if __name__ == "__main__":
    main()
