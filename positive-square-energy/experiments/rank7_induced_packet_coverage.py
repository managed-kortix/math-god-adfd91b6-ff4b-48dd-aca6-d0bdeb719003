#!/usr/bin/env python3
"""Exact induced-packet coverage scan for rank-seven residual rows, orders 8--12."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import os
import sys
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORDER_PATH_COUNTS = {8: 14, 9: 15, 10: 16, 11: 17, 12: 18}
ORDER_KERNEL_TOTALS = {8: 4015, 9: 4495, 10: 3396, 11: 1391, 12: 365}
SCHEMAS = {
    8: "rank-seven-order-eight-exact-residual-census-chunk-v1",
    9: "rank-seven-orders9-12-exact-residual-census-chunk-v1",
    10: "rank-seven-orders9-12-exact-residual-census-chunk-v1",
    11: "rank-seven-orders9-12-exact-residual-census-chunk-v1",
    12: "rank-seven-orders9-12-exact-residual-census-chunk-v1",
}
REPORT_SCHEMA = "rank-seven-orders8-12-induced-packet-coverage-v1"
PACKETS = (("K5", 5, 10, 1), ("K4", 4, 6, 2), ("diamond", 4, 5, 1))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def read_chunk(path):
    opener = lzma.open if path.suffix == ".xz" else open
    try:
        with opener(path, "rb") as stream:
            raw = stream.read()
    except lzma.LZMAError as error:
        raise RuntimeError(f"bad XZ chunk: {path.name}") from error
    try:
        payload = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"bad JSON chunk: {path.name}") from error
    require(raw == canonical_bytes(payload), f"noncanonical chunk: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest(), file_sha256(path)


def canonical_graph(order, edges, row, opened=None):
    """Build the canonical realization; ``opened`` replaces its unit path by length 3."""
    adjacency = [set() for _ in range(order)]
    next_vertex = order

    def add_path(u, v, length):
        nonlocal next_vertex
        previous = u
        for _ in range(length - 1):
            adjacency.append(set())
            adjacency[previous].add(next_vertex)
            adjacency[next_vertex].add(previous)
            previous = next_vertex
            next_vertex += 1
        adjacency[previous].add(v)
        adjacency[v].add(previous)

    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        require(type(odd) is int and 0 <= odd <= multiplicity, "nonphysical parity row")
        odd_lengths = ([] if odd == 0 else
                       [3 if edge_index == opened else 1] + [3] * (odd - 1))
        for length in odd_lengths + [2] * (multiplicity - odd):
            add_path(u, v, length)
    return adjacency


def complement_debit(adjacency, anchor):
    outside = set(range(len(adjacency))) - anchor
    debit = 0
    while outside:
        root = min(outside)
        outside.remove(root)
        queue = deque([root])
        vertices = []
        edge_twice = 0
        bipartite = {root: 0}
        odd_cycle = False
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in anchor:
                    continue
                edge_twice += 1
                if neighbor not in bipartite:
                    bipartite[neighbor] = bipartite[vertex] ^ 1
                    outside.remove(neighbor)
                    queue.append(neighbor)
                elif bipartite[neighbor] == bipartite[vertex]:
                    odd_cycle = True
        edges = edge_twice // 2
        if edges == len(vertices) - 1:
            debit += 1
        elif edges == len(vertices) and odd_cycle:
            debit += 1
        else:
            return None
    return debit


def packet_candidates(order, edges):
    pair_index = {(u, v): index for index, (u, v, _) in enumerate(edges)}
    result = []
    for name, size, required_edges, capacity in PACKETS:
        for vertices in combinations(range(order), size):
            indices = [pair_index.get((u, v)) for u, v in combinations(vertices, 2)]
            present = tuple(index for index in indices if index is not None)
            if len(present) == required_edges:
                result.append((name, capacity, vertices, present))
    return tuple(result)


def packet_owner(order, edges, row, candidates, opened=None):
    active = {index for index, odd in enumerate(row) if odd and index != opened}
    possible = [candidate for candidate in candidates
                if all(index in active for index in candidate[3])]
    if not possible:
        return None
    adjacency = canonical_graph(order, edges, row, opened)
    for name, capacity, vertices, _ in possible:
            anchor = set(vertices)
            debit = complement_debit(adjacency, anchor)
            if debit is not None and debit <= capacity:
                return name, debit, list(vertices)
    return None


def classify_row(order, path_count, edges, row, candidates):
    unit_edges = [index for index, odd in enumerate(row) if odd]
    canonical = packet_owner(order, edges, row, candidates)
    opened = {index: packet_owner(order, edges, row, candidates, index)
              for index in unit_edges}
    target_owners = Counter()
    nonunit_frontiers = path_count - len(unit_edges)
    if canonical is not None:
        target_owners[canonical[0]] += 1 + nonunit_frontiers
    for owner in opened.values():
        if owner is not None:
            target_owners[owner[0]] += 1
    return canonical, opened, target_owners


def scan_order(order, paths, output, progress=False):
    path_count = ORDER_PATH_COUNTS[order]
    cursor = residual_orbits = residual_physical = 0
    packet_rows = packet_physical = complete_rows = complete_physical = 0
    target_orbits = Counter({name: 0 for name, *_ in PACKETS})
    target_physical = Counter({name: 0 for name, *_ in PACKETS})
    canonical_rows = Counter({name: 0 for name, *_ in PACKETS})
    canonical_physical = Counter({name: 0 for name, *_ in PACKETS})
    chunks = []
    classification = hashlib.sha256()

    for path in sorted(paths):
        payload, raw_sha256, artifact_sha256 = read_chunk(path)
        require(payload.get("schema") == SCHEMAS[order] and
                (payload.get("rank"), payload.get("order"), payload.get("path_count")) ==
                (7, order, path_count), f"wrong chunk scope: {path.name}")
        start, stop = payload["kernel_range"]
        require(start == cursor and start < stop, f"chunk gap or overlap: {path.name}")
        cursor = stop
        kernels = {item["order_kernel"]: item for item in payload["kernels"]}
        candidates = {index: packet_candidates(order, tuple(map(tuple, item["edges"])))
                      for index, item in kernels.items()}
        local_rows = local_targets = 0
        for record in payload["residuals"]:
            ledger = kernels.get(record["order_kernel"])
            require(ledger is not None and ledger["global_kernel"] == record["global_kernel"],
                    f"bad kernel reference: {path.name}")
            edges = tuple(map(tuple, ledger["edges"]))
            row = tuple(record["row"])
            orbit_size = record["orbit_size"]
            require(type(orbit_size) is int and orbit_size >= 1, "bad orbit size")
            canonical, opened, owners = classify_row(
                order, path_count, edges, row, candidates[record["order_kernel"]])
            owned = sum(owners.values())
            classification.update(canonical_bytes([
                order, record["global_kernel"], record["order_kernel"], record["row"],
                orbit_size, canonical, sorted((key, value) for key, value in opened.items()),
                dict(sorted(owners.items())),
            ]))
            residual_orbits += 1
            residual_physical += orbit_size
            if owned:
                packet_rows += 1
                packet_physical += orbit_size
                local_rows += 1
            if owned == path_count + 1:
                complete_rows += 1
                complete_physical += orbit_size
            if canonical is not None:
                canonical_rows[canonical[0]] += 1
                canonical_physical[canonical[0]] += orbit_size
            for name, count in owners.items():
                target_orbits[name] += count
                target_physical[name] += count * orbit_size
                local_targets += count
        require(len(payload["residuals"]) == payload["coarse_residual_total"],
                f"residual count mismatch: {path.name}")
        chunks.append({
            "artifact_sha256": artifact_sha256,
            "kernel_range": [start, stop],
            "packet_row_total": local_rows,
            "packet_target_total": local_targets,
            "path": os.path.relpath(path, output.parent),
            "raw_sha256": raw_sha256,
            "residual_orbit_total": len(payload["residuals"]),
        })
        if progress:
            print(f"order={order} chunk={path.name} residuals={residual_orbits} "
                  f"packet_rows={packet_rows}", flush=True)

    require(cursor == ORDER_KERNEL_TOTALS[order], f"incomplete order-{order} kernel range")
    return {
        "order": order,
        "kernel_total": cursor,
        "path_count": path_count,
        "frontiers_per_residual": path_count + 1,
        "residual_orbit_total": residual_orbits,
        "residual_physical_total": residual_physical,
        "canonical_packet_orbit_counts": dict(canonical_rows),
        "canonical_packet_physical_counts": dict(canonical_physical),
        "packet_row_orbit_total": packet_rows,
        "packet_row_physical_total": packet_physical,
        "complete_frontier_packet_orbit_total": complete_rows,
        "complete_frontier_packet_physical_total": complete_physical,
        "packet_target_orbit_counts": dict(target_orbits),
        "packet_target_physical_counts": dict(target_physical),
        "packet_target_orbit_total": sum(target_orbits.values()),
        "packet_target_physical_total": sum(target_physical.values()),
        "classification_stream_sha256": classification.hexdigest(),
        "chunks": chunks,
    }


def default_paths(order):
    pattern = ("rank7_order8_residual_chunk_*.json.xz" if order == 8 else
               f"rank7_order{order}_census_*.json.xz")
    return sorted(HERE.glob(pattern))


def build(orders, output, progress=False):
    results = []
    for order in orders:
        paths = default_paths(order)
        require(paths, f"no order-{order} chunks")
        results.append(scan_order(order, paths, output, progress))
    return {
        "schema": REPORT_SCHEMA,
        "status": "complete-exact-induced-packet-scan",
        "full_theorem": False,
        "scope": "coarse-DNN residual canonical-plus-coordinate targets only",
        "packet_rule": {
            "anchors": {"K5": 1, "K4": 2, "diamond": 1},
            "complement": "at most the anchor allowance of induced tree or odd-unicyclic components",
            "lift": "arbitrary same-parity lengthening of non-anchor paths; anchor unit edges must remain unit",
        },
        "orders": results,
        "packet_target_orbit_total": sum(row["packet_target_orbit_total"] for row in results),
        "packet_target_physical_total": sum(row["packet_target_physical_total"] for row in results),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", nargs="+", type=int, default=sorted(ORDER_PATH_COUNTS))
    parser.add_argument("--output", type=Path, default=HERE / "rank7_induced_packet_coverage.json")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    require(set(args.orders) <= set(ORDER_PATH_COUNTS), "orders must lie in 8--12")
    require(args.output.parent.is_dir(), "output parent does not exist")
    actual = build(sorted(set(args.orders)), args.output, args.progress)
    encoded = canonical_bytes(actual)
    if args.audit:
        expected = args.output.read_bytes()
        require(expected == encoded, "coverage report differs from exact rescan")
    else:
        args.output.write_bytes(encoded)
    print(f"orders={','.join(map(str, args.orders))} "
          f"targets={actual['packet_target_orbit_total']} "
          f"physical_targets={actual['packet_target_physical_total']} "
          f"sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as error:
        sys.stderr.write(f"rank-seven induced packet audit: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
