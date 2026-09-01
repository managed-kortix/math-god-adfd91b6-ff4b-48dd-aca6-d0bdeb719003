#!/usr/bin/env python3
"""Stratified order-ten pilot for direct induced packets and Rayleigh owners."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rank7_order10_after_expanded_weighted_remainder.jsonl.xz"
SOURCE_REPORT = HERE / "rank7_order10_expanded_weighted_family_scan.json"
KERNEL_SOURCE = HERE / "rank7_order10_near_cubic_gram_lane.py"
OUTPUT = HERE / "rank7_order10_packet_rayleigh_pilot.json"
OWNERS = HERE / "rank7_order10_packet_rayleigh_pilot_owners.jsonl.xz"
SCHEMA = "rank-seven-order-ten-packet-rayleigh-stratified-pilot-v1"
ORDER = 10
PATH_COUNT = 16
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_json(path):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"noncanonical JSON: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest()


def physical_paths(edges, row, opened=None):
    paths = []
    physical = 0
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        for length in lengths:
            paths.append((edge_index, u, v, length + (2 if physical == opened else 0)))
            physical += 1
    require(len(paths) == PATH_COUNT, "physical path total changed")
    return paths


def canonical_graph(edges, row, opened=None):
    adjacency = [set() for _ in range(ORDER)]
    path_vertices = []
    for edge_index, u, v, length in physical_paths(edges, row, opened):
        vertices = [u]
        previous = u
        for _ in range(length - 1):
            current = len(adjacency)
            adjacency.append(set())
            adjacency[previous].add(current)
            adjacency[current].add(previous)
            vertices.append(current)
            previous = current
        adjacency[previous].add(v)
        adjacency[v].add(previous)
        vertices.append(v)
        path_vertices.append((edge_index, tuple(vertices)))
    return adjacency, path_vertices


def complement_debit(adjacency, anchor, allow_tree=True):
    outside = set(range(len(adjacency))) - anchor
    debit = 0
    while outside:
        root = min(outside)
        outside.remove(root)
        queue = deque([root])
        vertices = []
        edge_twice = 0
        colors = {root: 0}
        odd_cycle = False
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor in anchor:
                    continue
                edge_twice += 1
                if neighbor not in colors:
                    colors[neighbor] = colors[vertex] ^ 1
                    outside.remove(neighbor)
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    odd_cycle = True
        edge_total = edge_twice // 2
        if allow_tree and edge_total == len(vertices) - 1:
            debit += 1
        elif edge_total == len(vertices) and not odd_cycle:
            pass
        elif allow_tree and edge_total == len(vertices) and odd_cycle:
            debit += 1
        else:
            return None
    return debit


def packet_candidates(edges):
    pair_index = {(u, v): index for index, (u, v, _) in enumerate(edges)}
    candidates = []
    for name, size, required, capacity in PACKETS:
        for vertices in combinations(range(ORDER), size):
            indices = tuple(pair_index.get(pair) for pair in combinations(vertices, 2))
            present = tuple(index for index in indices if index is not None)
            if len(present) == required:
                candidates.append((name, capacity, vertices, present))
    return candidates


def packet_target(edges, row, opened, candidates):
    opened_edge = None if opened is None else physical_paths(edges, row)[opened][0]
    active = {index for index, odd in enumerate(row) if odd and index != opened_edge}
    adjacency, _ = canonical_graph(edges, row, opened)
    for name, capacity, vertices, indices in candidates:
        if all(index in active for index in indices):
            debit = complement_debit(adjacency, set(vertices))
            if debit is not None and debit <= capacity:
                return {"anchor": name, "debit": debit, "vertices": list(vertices)}
    return None


def packet_owner(edges, row):
    candidates = packet_candidates(edges)
    certificates = []
    for opened in [None, *range(PATH_COUNT)]:
        certificate = packet_target(edges, row, opened, candidates)
        if certificate is None:
            return None
        certificates.append(certificate)
    return certificates


def theta_target(edges, row, opened):
    adjacency, paths = canonical_graph(edges, row, opened)
    by_edge = {}
    for edge_index, vertices in paths:
        by_edge.setdefault(edge_index, []).append(vertices)
    for edge_index, path_group in by_edge.items():
        if len(path_group) < 3:
            continue
        unit = [path for path in path_group if len(path) == 2]
        nonunit = [path for path in path_group if len(path) > 2]
        choices = []
        if unit and len(nonunit) >= 2:
            choices.extend((unit[0], *pair) for pair in combinations(nonunit, 2))
        if not unit:
            choices.extend(combinations(nonunit, 3))
        for choice in choices:
            anchor = set().union(*map(set, choice))
            induced_edges = sum(len(adjacency[v] & anchor) for v in anchor) // 2
            if induced_edges != sum(len(path) - 1 for path in choice):
                continue
            debit = complement_debit(adjacency, anchor, allow_tree=False)
            if debit == 0:
                return {"anchor": "theta", "bundle_edge": edge_index,
                        "vertices": sorted(anchor), "complement": "bipartite-unicyclic"}
    return None


def theta_owner(edges, row):
    certificates = []
    for opened in [None, *range(PATH_COUNT)]:
        certificate = theta_target(edges, row, opened)
        if certificate is None:
            return None
        certificates.append(certificate)
    return certificates


def rayleigh_certificate(adjacency):
    matrix = np.zeros((len(adjacency), len(adjacency)), dtype=float)
    for u, neighbors in enumerate(adjacency):
        for v in neighbors:
            matrix[u, v] = 1.0
    _, vectors = np.linalg.eigh(matrix)
    proposal = vectors[:, -1]
    for scale in (10**3, 10**4, 10**5, 10**6):
        vector = np.rint(proposal * scale).astype(np.int64)
        denominator = int(vector @ vector)
        numerator = sum(int(vector[u]) * int(vector[v])
                        for u, neighbors in enumerate(adjacency) for v in neighbors)
        strict = numerator * numerator - len(adjacency) * denominator * denominator
        if numerator > 0 and strict > 0:
            divisor = int(np.gcd.reduce(np.abs(vector)))
            if divisor > 1:
                vector //= divisor
                denominator = int(vector @ vector)
                numerator = sum(int(vector[u]) * int(vector[v])
                                for u, neighbors in enumerate(adjacency) for v in neighbors)
                strict = numerator * numerator - len(adjacency) * denominator * denominator
            return {"order": len(adjacency), "numerator": numerator,
                    "denominator": denominator, "strict_square_test": strict,
                    "integer_vector": vector.tolist()}
    return None


def rayleigh_owner(edges, row):
    certificates = []
    for opened in [None, *range(PATH_COUNT)]:
        certificate = rayleigh_certificate(canonical_graph(edges, row, opened)[0])
        if certificate is None:
            return None
        certificates.append(certificate)
    return certificates


def signature(kernel, row, source):
    return json.dumps(source.coarse_signature(source._source_module, kernel, row),
                      sort_keys=True, separators=(",", ":"))


def scan(pilot_size, progress=False):
    report, report_sha256 = strict_json(SOURCE_REPORT)
    stream = report["updated_remainder_stream"]
    require(file_sha256(SOURCE) == stream["artifact_sha256"], "source stream changed")
    total = stream["record_total"]
    require(0 < pilot_size <= total, "invalid pilot size")
    positions = {index * total // pilot_size for index in range(pilot_size)}

    kernel_module = load("rank7_order10_packet_kernel_source", KERNEL_SOURCE)
    kernels = kernel_module.kernel_dictionary()
    weighted = load("rank7_order10_packet_weighted", HERE / "rank7_order10_weighted_cycle_gram_lane.py")
    weighted._source_module = kernel_module
    selected = []
    digest = hashlib.sha256()
    count = 0
    with lzma.open(SOURCE, "rb") as rows:
        for position, raw in enumerate(rows):
            digest.update(raw)
            count += 1
            if position in positions:
                record = json.loads(raw.decode("ascii"))
                require(raw == canonical_bytes(record), "noncanonical selected record")
                selected.append(record)
    require((count, digest.hexdigest()) == (total, stream["raw_sha256"]),
            "source stream authentication failed")
    require(len(selected) == pilot_size, "pilot selection failed")

    owners = []
    strata = Counter()
    stratum_owners = {}
    lane_counts = Counter()
    lane_physical = Counter()
    packet_anchors = Counter()
    for index, record in enumerate(selected, 1):
        source_index, global_kernel, order_kernel, raw_row, orbit_size = record
        kernel = kernels[order_kernel]
        require(kernel["global_kernel"] == global_kernel, "kernel reference changed")
        row = tuple(raw_row)
        key = json.dumps(weighted.coarse_signature(kernel_module, kernel, row),
                         sort_keys=True, separators=(",", ":"))
        strata[key] += 1
        candidates = packet_candidates(kernel["edges"])
        certificates = []
        row_lanes = Counter()
        for frontier, opened in enumerate([None, *range(PATH_COUNT)]):
            certificate = packet_target(kernel["edges"], row, opened, candidates)
            lane = "induced-packet" if certificate is not None else None
            if certificate is None:
                certificate = theta_target(kernel["edges"], row, opened)
                lane = "induced-theta" if certificate is not None else None
            if certificate is None:
                certificate = rayleigh_certificate(
                    canonical_graph(kernel["edges"], row, opened)[0])
                lane = "direct-rayleigh" if certificate is not None else None
            certificates.append([frontier, lane, certificate])
            if lane is not None:
                row_lanes[lane] += 1
                lane_counts[lane] += 1
                lane_physical[lane] += orbit_size
                if lane == "induced-packet":
                    packet_anchors[certificate["anchor"]] += 1
        if row_lanes:
            for lane in row_lanes:
                stratum_owners.setdefault(key, Counter())[lane] += 1
            owners.append([record, dict(sorted(row_lanes.items())), certificates,
                           json.loads(key)])
        if progress and index % 100 == 0:
            print(f"pilot={index}/{pilot_size} owners={len(owners)}", flush=True)

    temporary = OWNERS.with_name(OWNERS.name + ".tmp")
    owner_digest = hashlib.sha256()
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as output:
        for owner in owners:
            raw = canonical_bytes(owner)
            output.write(raw)
            owner_digest.update(raw)
    temporary.replace(OWNERS)
    strongest = max(lane_counts, key=lambda lane: (lane_counts[lane], lane), default=None)
    ranked = sorted(strata, key=lambda key: (-strata[key], key))
    return {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "evenly spaced stratified pilot of the exact order-ten post-weighted remainder",
        "source_report_sha256": report_sha256,
        "source_remainder": stream,
        "pilot": {"method": "floor(i*N/pilot_size)", "record_total": pilot_size,
                  "physical_total": sum(record[4] for record in selected),
                  "signature_total": len(strata)},
        "owner_precedence": ["induced-packet", "induced-theta", "direct-rayleigh"],
        "exact_coverage": {"row_with_owner_total": len(owners),
                           "target_owner_total": sum(lane_counts.values()),
                           "target_owner_physical_total": sum(lane_physical.values()),
                           "lane_target_counts": dict(sorted(lane_counts.items())),
                           "lane_target_physical_counts": dict(sorted(lane_physical.items())),
                           "packet_target_anchor_counts": dict(sorted(packet_anchors.items()))},
        "strongest_lane": strongest,
        "lift_classification": {
            "induced-packet": "rooted-tree and non-anchor same-parity lift; not all-length on anchor edges",
            "induced-theta": "all-length and rooted-tree lift via arbitrary attached theta plus bipartite-unicyclic complement",
            "direct-rayleigh": "exact finite canonical-plus-coordinate owner; no all-length lift",
        },
        "top_strata": [{"signature": json.loads(key), "tested": strata[key],
                        "owners": dict(sorted(stratum_owners.get(key, {}).items()))}
                       for key in ranked[:100]],
        "owner_stream": {"path": OWNERS.name, "record_total": len(owners),
                         "raw_sha256": owner_digest.hexdigest(),
                         "artifact_sha256": file_sha256(OWNERS)},
        "claim_boundary": "coverage counts are exact for the deterministic pilot only; only induced-theta owners have an all-length lift",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-size", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    payload = scan(args.pilot_size, args.progress)
    raw = canonical_bytes(payload)
    if args.audit:
        require(args.output.read_bytes() == raw, "pilot report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(json.dumps({"owners": payload["exact_coverage"]["lane_target_counts"],
                      "strongest_lane": payload["strongest_lane"],
                      "sha256": hashlib.sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
