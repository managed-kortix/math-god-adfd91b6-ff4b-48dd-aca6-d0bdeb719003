#!/usr/bin/env python3
"""Exact structural owners for rank-seven/order-twelve residual rows.

The principal nonlocal owner is a signed three-ray Gram.  Give each branch
vertex one of the six vectors ``+/- z_i``, where the three ``z_i`` are unit
vectors with pairwise inner product ``-1/2``.  A parity signing is owned when
each edge has transformed correlation 1 (equal rays) or 1/2 (distinct rays).

For simple cubic kernels a second owner uses the signed adjacency square

    G = (a I + b S)^2 / (a^2 + 3 b^2).

Both matrices are reconstructed from the kernel and row and require no stored
numeric payload.  All acceptance arithmetic is rational and fail-closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path


F = Fraction
BUDGET = F(6)
ORDER = 12
PATH_COUNT = 18
SCHEMA = "rank-seven-order-twelve-structural-owner-scan-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def read_chunk(path):
    stored = path.read_bytes()
    raw = lzma.decompress(stored) if path.suffix == ".xz" else stored
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"noncanonical chunk: {path}")
    require(payload.get("schema") ==
            "rank-seven-orders9-12-exact-residual-census-chunk-v1",
            f"wrong chunk schema: {path}")
    require(payload.get("order") == ORDER and payload.get("rank") == 7,
            f"wrong rank or order: {path}")
    require(payload.get("coarse_residual_total") == len(payload.get("residuals", [])),
            f"incomplete residual stream: {path}")
    return payload, hashlib.sha256(raw).hexdigest(), hashlib.sha256(stored).hexdigest()


def simple_cubic(edges):
    degree = [0] * ORDER
    if len(edges) != PATH_COUNT or any(multiplicity != 1 for _, _, multiplicity in edges):
        return False
    for u, v, _ in edges:
        degree[u] += 1
        degree[v] += 1
    return degree == [3] * ORDER


def canonical_length(multiplicity, odd, occurrence):
    if occurrence < odd:
        return 1 if occurrence == 0 else 3
    return 2


def path_bound(correlation, length):
    transformed = -correlation if length & 1 else correlation
    if transformed <= -1 or transformed > 1:
        return None
    return (1 - transformed) / (length * (1 + transformed))


def signed_three_ray_owner(edges, row):
    """Decide the six-state signed three-ray constraint exactly.

    State ``2*color+epsilon`` denotes ``(-1)^epsilon z_color``.  For an edge
    of parity bit p, transformed correlation is positive precisely when

        p = epsilon_u xor epsilon_v xor [color_u != color_v].

    Fixing vertex zero to state zero loses no solutions: global negation and a
    permutation of the three rays act transitively on the six states.
    """
    if not simple_cubic(edges) or any(value not in (0, 1) for value in row):
        return False
    adjacency = [[] for _ in range(ORDER)]
    for edge_index, (u, v, _) in enumerate(edges):
        parity = row[edge_index]
        adjacency[u].append((v, parity))
        adjacency[v].append((u, parity))

    allowed = [[[False] * 6 for _ in range(6)] for _ in range(2)]
    for parity in range(2):
        for left in range(6):
            lc, le = divmod(left, 2)
            for right in range(6):
                rc, re = divmod(right, 2)
                allowed[parity][left][right] = parity == (le ^ re ^ (lc != rc))

    domains = [0b111111 for _ in range(ORDER)]
    domains[0] = 1

    def propagate(local, seeds):
        queue = deque(seeds)
        while queue:
            vertex = queue.popleft()
            source = local[vertex]
            for neighbor, parity in adjacency[vertex]:
                old = local[neighbor]
                new = 0
                for target_state in range(6):
                    if not old & (1 << target_state):
                        continue
                    if any(source & (1 << source_state) and
                           allowed[parity][source_state][target_state]
                           for source_state in range(6)):
                        new |= 1 << target_state
                if new == 0:
                    return False
                if new != old:
                    local[neighbor] = new
                    queue.append(neighbor)
        return True

    def solve(local):
        if not propagate(local, range(ORDER)):
            return False
        choices = [(mask.bit_count(), vertex) for vertex, mask in enumerate(local)
                   if mask & (mask - 1)]
        if not choices:
            return True
        _, vertex = min(choices)
        mask = local[vertex]
        while mask:
            bit = mask & -mask
            mask -= bit
            child = local.copy()
            child[vertex] = bit
            if solve(child):
                return True
        return False

    return solve(domains)


def signed_adjacency_square_owner(edges, row, radius=8):
    if not simple_cubic(edges) or any(value not in (0, 1) for value in row):
        return None
    signed = [[0] * ORDER for _ in range(ORDER)]
    for (u, v, _), parity in zip(edges, row, strict=True):
        value = -1 if parity else 1
        signed[u][v] = value
        signed[v][u] = value
    square = [[sum(signed[u][w] * signed[w][v] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    best = None
    for a in range(1, radius + 1):
        for b in range(-radius, radius + 1):
            if b == 0:
                continue
            denominator = a * a + 3 * b * b
            costs = []
            for (u, v, _), parity in zip(edges, row, strict=True):
                numerator = 2 * a * b * signed[u][v] + b * b * square[u][v]
                cost = path_bound(F(numerator, denominator), 1 if parity else 2)
                if cost is None:
                    break
                costs.append(cost)
            else:
                total = sum(costs, F())
                if total <= BUDGET and (best is None or total < best[2]):
                    best = a, b, total
    return best


def scan(paths, progress=False):
    owner_counts = Counter((name, 0) for name in
                           ("signed-three-ray", "signed-adjacency-square"))
    support_counts = Counter()
    residual_by_kernel = Counter()
    scanned = owned = 0
    chunks = []
    stream = hashlib.sha256()
    for path in paths:
        payload, raw_digest, artifact_digest = read_chunk(path)
        kernels = {item["order_kernel"]: tuple(map(tuple, item["edges"]))
                   for item in payload["kernels"]}
        local_counts = Counter()
        for source in payload["residuals"]:
            edges = kernels[source["order_kernel"]]
            row = tuple(source["row"])
            owner = None
            detail = None
            if signed_three_ray_owner(edges, row):
                owner = "signed-three-ray"
            else:
                square = signed_adjacency_square_owner(edges, row)
                if square is not None:
                    owner = "signed-adjacency-square"
                    detail = [square[0], square[1], square[2].numerator,
                              square[2].denominator]
            scanned += 1
            support_counts[f"support-{len(edges)}-{'owned' if owner else 'residual'}"] += 1
            if owner is None:
                residual_by_kernel[str(source["global_kernel"])] += 1
            else:
                owned += 1
                owner_counts[owner] += 1
                local_counts[owner] += 1
            stream.update(canonical_bytes([source["global_kernel"], source["order_kernel"],
                                           source["row"], owner, detail]))
        chunks.append({"path": path.name, "kernel_range": payload["kernel_range"],
                       "residual_total": payload["coarse_residual_total"],
                       "owner_counts": dict(sorted(local_counts.items())),
                       "raw_sha256": raw_digest, "artifact_sha256": artifact_digest})
        if progress:
            print(f"chunk={path.name} scanned={scanned} owned={owned}", flush=True)
    minimal = min(residual_by_kernel.values()) if residual_by_kernel else 0
    minimal_kernels = sorted(int(key) for key, value in residual_by_kernel.items()
                             if value == minimal)
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "exact payload-free structural owners over supplied order-twelve residual chunks",
        "chunks": chunks,
        "scanned_residual_total": scanned,
        "owned_residual_total": owned,
        "residual_total": scanned - owned,
        "owner_counts": dict(sorted(owner_counts.items())),
        "support_status_counts": dict(sorted(support_counts.items())),
        "minimal_positive_kernel_residual": minimal,
        "minimal_positive_residual_kernels": minimal_kernels,
        "residual_by_kernel": dict(sorted(residual_by_kernel.items(), key=lambda item: int(item[0]))),
        "classification_stream_sha256": stream.hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chunks", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    report = scan(args.chunks, args.progress)
    raw = canonical_bytes(report)
    if args.output is not None:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(raw.decode("ascii"), end="")


if __name__ == "__main__":
    main()
