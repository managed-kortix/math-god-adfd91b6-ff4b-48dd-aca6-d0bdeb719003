#!/usr/bin/env python3
"""Produce the exact unlabeled isolate-free six-edge support census."""

import argparse
import hashlib
import itertools
import sys
from pathlib import Path

TARGET_ORDERS = {4: 1, 5: 5, 6: 15, 7: 20, 8: 15, 9: 7, 10: 3, 11: 1, 12: 1}
EXPECTED_BYTES = 934
EXPECTED_SHA256 = "e97de806f6db6c3ac1768cab9259f7f0cd1c91ee26d949c1a3455ef8e471c8be"


def graph6(n, edges):
    bits = [int((j, i) in edges) for i in range(1, n) for j in range(i)]
    bits.extend([0] * (-len(bits) % 6))
    return chr(n + 63) + "".join(
        chr(63 + sum(bits[i + j] << (5 - j) for j in range(6)))
        for i in range(0, len(bits), 6)
    )


def canonical(n, edges):
    """Canonicalize only a connected component, whose order is at most seven."""
    best = None
    for order in itertools.permutations(range(n)):
        relabeled = {
            (i, j)
            for i in range(n)
            for j in range(i + 1, n)
            if tuple(sorted((order[i], order[j]))) in edges
        }
        code = graph6(n, relabeled)
        if best is None or code < best:
            best = code
    return best


def decode_graph6(code):
    n = ord(code[0]) - 63
    bits = []
    for char in code[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(j, i) for i in range(1, n) for j in range(i)]
    return n, {edge for edge, bit in zip(pairs, bits) if bit}


def connected_components():
    """Use one-edge canonical augmentation to obtain connected components."""
    levels = {1: {(2, graph6(2, {(0, 1)}))}}
    for m in range(1, 6):
        next_level = set()
        for n, code in sorted(levels[m]):
            _, edges = decode_graph6(code)
            for u in range(n):
                for v in range(u + 1, n):
                    if (u, v) not in edges:
                        grown = edges | {(u, v)}
                        next_level.add((n, canonical(n, grown)))
            for u in range(n):
                grown = edges | {(u, n)}
                next_level.add((n + 1, canonical(n + 1, grown)))
        levels[m + 1] = next_level
    return levels


def disjoint_union(parts):
    edges = set()
    offset = 0
    for _, code in parts:
        n, component_edges = decode_graph6(code)
        edges.update((u + offset, v + offset) for u, v in component_edges)
        offset += n
    return offset, edges


def support_rows():
    components = [
        (m, n, code)
        for m, level in connected_components().items()
        for n, code in level
    ]
    components.sort()
    rows = set()

    def visit(start, remaining, parts):
        if remaining == 0:
            ordered = sorted(((n, code) for _, n, code in parts), key=lambda x: x[1])
            n, edges = disjoint_union(ordered)
            rows.add((n, graph6(n, edges)))
            return
        for index in range(start, len(components)):
            m, _, _ = components[index]
            if m > remaining:
                break
            visit(index, remaining - m, parts + [components[index]])

    visit(0, 6, [])
    return sorted(rows)


def payload():
    rows = support_rows()
    orders = {n: sum(row_n == n for row_n, _ in rows) for n in range(4, 13)}
    if len(rows) != 68 or orders != TARGET_ORDERS:
        raise RuntimeError(f"bad census: count={len(rows)} orders={orders}")
    lines = [
        "m6-support-census-v1",
        "edges\t6",
        "count\t68",
        "orders\t" + ",".join(f"{n}:{orders[n]}" for n in range(4, 13)),
    ]
    lines.extend(f"{index:03d}\t{n}\t{code}" for index, (n, code) in enumerate(rows))
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--output", type=Path, help="write the deterministic ASCII payload")
    action.add_argument("--check", type=Path, help="compare a file with a fresh census")
    args = parser.parse_args()
    data = payload()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != EXPECTED_BYTES or digest != EXPECTED_SHA256:
        raise RuntimeError(f"frozen payload changed: bytes={len(data)} sha256={digest}")
    if args.check:
        if args.check.read_bytes() != data:
            print(f"FAIL payload differs: {args.check}", file=sys.stderr)
            return 1
        print(f"PASS graphs=68 orders=1,5,15,20,15,7,3,1,1 bytes={len(data)} sha256={digest}")
    elif args.output:
        args.output.write_bytes(data)
        print(f"WROTE graphs=68 bytes={len(data)} sha256={digest} path={args.output}")
    else:
        sys.stdout.buffer.write(data)
        print(f"graphs=68 bytes={len(data)} sha256={digest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
