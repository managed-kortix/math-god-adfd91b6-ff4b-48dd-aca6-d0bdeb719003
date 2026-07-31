#!/usr/bin/env python3
"""Independent vertex-augmentation and isomorphism audit of the m=6 census."""

import argparse
import hashlib
import itertools
from collections import Counter, defaultdict
from pathlib import Path

TARGET_ORDERS = [1, 5, 15, 20, 15, 7, 3, 1, 1]
EXPECTED_BYTES = 934
EXPECTED_SHA256 = "e97de806f6db6c3ac1768cab9259f7f0cd1c91ee26d949c1a3455ef8e471c8be"


def degrees(n, edges):
    result = [0] * n
    for u, v in edges:
        result[u] += 1
        result[v] += 1
    return result


def isomorphic(left, right):
    n, a = left
    _, b = right
    da, db = degrees(n, a), degrees(n, b)
    if sorted(da) != sorted(db):
        return False
    candidates = {u: [v for v in range(n) if db[v] == da[u]] for u in range(n)}
    order = sorted(range(n), key=lambda u: (len(candidates[u]), -da[u], u))
    mapping = {}
    used = set()

    def extend(depth):
        if depth == n:
            return True
        u = order[depth]
        for v in candidates[u]:
            if v in used:
                continue
            if any(((min(u, x), max(u, x)) in a) !=
                   ((min(v, y), max(v, y)) in b) for x, y in mapping.items()):
                continue
            mapping[u] = v
            used.add(v)
            if extend(depth + 1):
                return True
            used.remove(v)
            del mapping[u]
        return False

    return extend(0)


def add_unlabeled(buckets, graph):
    n, edges = graph
    key = (n, tuple(sorted(degrees(n, edges))))
    if not any(isomorphic(graph, old) for old in buckets[key]):
        buckets[key].append(graph)


def connected_components():
    """Add a vertex with any nonempty neighborhood; do not import production code."""
    by_order = {1: [(1, frozenset())]}
    all_graphs = defaultdict(list)
    for n in range(1, 7):
        buckets = defaultdict(list)
        for _, edges in by_order[n]:
            for mask in range(1, 1 << n):
                grown = frozenset(set(edges) | {(u, n) for u in range(n) if mask >> u & 1})
                if len(grown) <= 6:
                    add_unlabeled(buckets, (n + 1, grown))
        by_order[n + 1] = [graph for group in buckets.values() for graph in group]
        for graph in by_order[n + 1]:
            if graph[1]:
                all_graphs[len(graph[1])].append(graph)
    return all_graphs


def encode_graph6(n, edges):
    stream = []
    for high in range(1, n):
        for low in range(high):
            stream.append((low, high) in edges)
    stream += [False] * (-len(stream) % 6)
    chars = [chr(n + 63)]
    for start in range(0, len(stream), 6):
        value = 0
        for bit in stream[start:start + 6]:
            value = 2 * value + bit
        chars.append(chr(63 + value))
    return "".join(chars)


def canonical_code(graph):
    n, edges = graph
    codes = []
    for labels in itertools.permutations(range(n)):
        inverse = {old: new for new, old in enumerate(labels)}
        relabeled = {tuple(sorted((inverse[u], inverse[v]))) for u, v in edges}
        codes.append(encode_graph6(n, relabeled))
    return min(codes)


def decode_graph6(code):
    n = ord(code[0]) - 63
    stream = []
    for char in code[1:]:
        value = ord(char) - 63
        stream.extend(bool(value & (1 << shift)) for shift in range(5, -1, -1))
    pairs = [(low, high) for high in range(1, n) for low in range(high)]
    return n, frozenset(edge for edge, bit in zip(pairs, stream) if bit)


def expected_rows():
    connected = connected_components()
    choices = []
    for m in sorted(connected):
        for graph in connected[m]:
            code = canonical_code(graph)
            choices.append((m, code, decode_graph6(code)))
    choices.sort(key=lambda item: (item[0], item[1]))
    rows = []

    def combine(start, remaining, selected):
        if remaining == 0:
            selected = sorted(selected, key=lambda item: item[1])
            offset = 0
            edges = set()
            for _, _, (n, component_edges) in selected:
                edges.update((u + offset, v + offset) for u, v in component_edges)
                offset += n
            rows.append((offset, encode_graph6(offset, edges)))
            return
        for index in range(start, len(choices)):
            if choices[index][0] > remaining:
                break
            combine(index, remaining - choices[index][0], selected + [choices[index]])

    combine(0, 6, [])
    return sorted(set(rows))


def expected_payload():
    rows = expected_rows()
    distribution = [Counter(n for n, _ in rows)[n] for n in range(4, 13)]
    if len(rows) != 68 or distribution != TARGET_ORDERS:
        raise RuntimeError(f"bad independent census: count={len(rows)} orders={distribution}")
    lines = [
        "m6-support-census-v1",
        "edges\t6",
        "count\t68",
        "orders\t" + ",".join(f"{n}:{count}" for n, count in zip(range(4, 13), distribution)),
    ]
    lines += [f"{i:03d}\t{n}\t{code}" for i, (n, code) in enumerate(rows)]
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path)
    args = parser.parse_args()
    expected = expected_payload()
    actual = args.payload.read_bytes()
    if actual != expected:
        raise RuntimeError(f"payload mismatch: {args.payload}")
    digest = hashlib.sha256(actual).hexdigest()
    if len(actual) != EXPECTED_BYTES or digest != EXPECTED_SHA256:
        raise RuntimeError(f"frozen payload changed: bytes={len(actual)} sha256={digest}")
    print(
        "PASS independent graphs=68 orders=1,5,15,20,15,7,3,1,1 "
        f"bytes={len(actual)} sha256={digest}"
    )


if __name__ == "__main__":
    main()
