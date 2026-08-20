#!/usr/bin/env python3
"""Stratify the exact order-eight combined remainder and add finite owner lanes."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import os
import sys
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
LEDGER_PATH = HERE / "rank7_order8_combined_owner_ledger.json"
INDICES_PATH = HERE / "rank7_order8_combined_owner_indices.json.xz"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
REPORT_PATH = HERE / "rank7_order8_combined_remainder_analysis.json"
OWNERS_PATH = HERE / "rank7_order8_packet_spectral_owners.json.xz"
REMAINDER_PATH = HERE / "rank7_order8_after_packet_spectral_remainder.jsonl.xz"
SCHEMA = "rank-seven-order-eight-combined-remainder-analysis-v2"
OWNER_SCHEMA = "rank-seven-order-eight-packet-spectral-owners-v2"
EXPECTED_REMAINDER = 84152
ORDER = 8
PATH_COUNT = 14
TARGETS_PER_ROW = 15
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


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              RuntimeError(f"nonstandard constant in {label}: {value}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def read_canonical(path, compressed=False):
    stored = path.read_bytes()
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ) if compressed else stored
    except lzma.LZMAError as error:
        raise RuntimeError(f"cannot decompress {path.name}") from error
    payload = strict_json(raw, path.name)
    require(raw == canonical_bytes(payload), f"noncanonical artifact: {path.name}")
    return payload, hashlib.sha256(raw).hexdigest(), hashlib.sha256(stored).hexdigest()


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_remainder_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load order-eight engine")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def signature_id(prefix, payload):
    return f"{prefix}-{hashlib.sha256(canonical_bytes(payload)).hexdigest()[:20]}"


def graph_data(edges, row):
    adjacency = [set() for _ in range(ORDER)]
    odd_adjacency = [set() for _ in range(ORDER)]
    support_degrees = [0] * ORDER
    weighted_degrees = [0] * ORDER
    odd_degrees = [0] * ORDER
    absolute_degrees = [0] * ORDER
    signed_degrees = [0] * ORDER
    support_incidence = [[] for _ in range(ORDER)]
    parity_incidence = [[] for _ in range(ORDER)]
    bundle_types = Counter()
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        signed = multiplicity - 2 * odd
        kind = "zero" if odd == 0 else ("full" if odd == multiplicity else "mixed")
        bundle_types[kind] += 1
        adjacency[u].add(v)
        adjacency[v].add(u)
        if odd:
            odd_adjacency[u].add(v)
            odd_adjacency[v].add(u)
        for vertex in (u, v):
            support_degrees[vertex] += 1
            weighted_degrees[vertex] += multiplicity
            odd_degrees[vertex] += odd
            absolute_degrees[vertex] += abs(signed)
            signed_degrees[vertex] += signed
            support_incidence[vertex].append(multiplicity)
            parity_incidence[vertex].append([multiplicity, odd])

    unseen = set(range(ORDER))
    components = []
    while unseen:
        todo = [min(unseen)]
        unseen.remove(todo[0])
        component = []
        for vertex in todo:
            component.append(vertex)
            for neighbor in sorted(adjacency[vertex] & unseen):
                unseen.remove(neighbor)
                todo.append(neighbor)
        components.append(component)

    bridges = 0
    timer = 0
    discovery = [-1] * ORDER
    low = [0] * ORDER

    def visit(vertex, parent):
        nonlocal bridges, timer
        discovery[vertex] = low[vertex] = timer
        timer += 1
        for neighbor in adjacency[vertex]:
            if neighbor == parent:
                continue
            if discovery[neighbor] < 0:
                visit(neighbor, vertex)
                low[vertex] = min(low[vertex], low[neighbor])
                bridges += low[neighbor] > discovery[vertex]
            else:
                low[vertex] = min(low[vertex], discovery[neighbor])

    for vertex in range(ORDER):
        if discovery[vertex] < 0:
            visit(vertex, -1)
    triangles = sum(len(adjacency[u] & adjacency[v])
                    for u in range(ORDER) for v in adjacency[u] if u < v) // 3
    support = {
        "edge_support": len(edges),
        "multiplicity_partition": sorted((edge[2] for edge in edges), reverse=True),
        "support_degree_partition": sorted(support_degrees, reverse=True),
        "weighted_degree_partition": sorted(weighted_degrees, reverse=True),
        "vertex_multiplicity_fingerprints": sorted(
            (sorted(values, reverse=True) for values in support_incidence), reverse=True),
    }
    parity = {
        "bundle_parity_partition": sorted(
            ([edge[2], odd] for edge, odd in zip(edges, row, strict=True)), reverse=True),
        "bundle_types": [bundle_types["zero"], bundle_types["mixed"], bundle_types["full"]],
        "odd_degree_partition": sorted(odd_degrees, reverse=True),
        "absolute_imbalance_degree_partition": sorted(absolute_degrees, reverse=True),
        "signed_imbalance_degree_partition": sorted(signed_degrees, reverse=True),
        "vertex_parity_fingerprints": sorted(
            (sorted(values, reverse=True) for values in parity_incidence), reverse=True),
    }
    graph = {
        "component_order_partition": sorted((len(value) for value in components), reverse=True),
        "cycle_rank": len(edges) - ORDER + len(components),
        "bridge_total": bridges,
        "triangle_total": triangles,
        "odd_support_edge_total": sum(bool(odd) for odd in row),
        "odd_support_degree_partition": sorted((len(value) for value in odd_adjacency),
                                                  reverse=True),
    }
    return support, parity, graph


def packet_candidates(edges):
    pair_index = {(u, v): index for index, (u, v, _) in enumerate(edges)}
    result = []
    for name, size, required_edges, capacity in PACKETS:
        for vertices in combinations(range(ORDER), size):
            indices = [pair_index.get((u, v)) for u, v in combinations(vertices, 2)]
            present = tuple(index for index in indices if index is not None)
            if len(present) == required_edges:
                result.append((name, capacity, vertices, present))
    return tuple(result)


def canonical_graph(edges, row, opened=None):
    adjacency = [set() for _ in range(ORDER)]
    next_vertex = ORDER

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

    physical_index = 0
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        odd_lengths = ([] if odd == 0 else [1] + [3] * (odd - 1))
        lengths = odd_lengths + [2] * (multiplicity - odd)
        for length in lengths:
            add_path(u, v, length + (2 if physical_index == opened else 0))
            physical_index += 1
    require(physical_index == PATH_COUNT, "physical path count changed")
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
        if edge_total == len(vertices) - 1 or (edge_total == len(vertices) and odd_cycle):
            debit += 1
        else:
            return None
    return debit


def packet_target(edges, row, candidates, frontier):
    opened_edge = None
    if frontier is not None:
        cursor = 0
        for edge_index, (_, odd) in enumerate(zip(edges, row, strict=True)):
            multiplicity = edges[edge_index][2]
            if cursor <= frontier < cursor + multiplicity:
                if odd and frontier == cursor:
                    opened_edge = edge_index
                break
            cursor += multiplicity
    active = {index for index, odd in enumerate(row) if odd and index != opened_edge}
    possible = [candidate for candidate in candidates
                if all(index in active for index in candidate[3])]
    if not possible:
        return None
    adjacency = canonical_graph(edges, row, frontier)
    for name, capacity, vertices, _ in possible:
        debit = complement_debit(adjacency, set(vertices))
        if debit is not None and debit <= capacity:
            return {"anchor": name, "debit": debit, "vertices": list(vertices)}
    return None


def packet_owner(edges, row):
    candidates = packet_candidates(edges)
    certificates = []
    for frontier in [None, *range(PATH_COUNT)]:
        certificate = packet_target(edges, row, candidates, frontier)
        if certificate is None:
            return None
        certificates.append(certificate)
    return certificates


def adjacency_matrix(adjacency):
    matrix = np.zeros((len(adjacency), len(adjacency)), dtype=float)
    for vertex, neighbors in enumerate(adjacency):
        for neighbor in neighbors:
            matrix[vertex, neighbor] = 1.0
    return matrix


def rayleigh_certificate(adjacency):
    matrix = adjacency_matrix(adjacency)
    _, vectors = np.linalg.eigh(matrix)
    proposal = vectors[:, -1]
    if proposal.sum() < 0:
        proposal = -proposal
    for scale in (10**3, 10**4, 10**5, 10**6):
        vector = np.rint(proposal * scale).astype(np.int64)
        denominator = int(vector @ vector)
        numerator = sum(int(vector[u]) * int(vector[v])
                        for u, neighbors in enumerate(adjacency) for v in neighbors)
        if numerator > 0 and numerator * numerator > len(adjacency) * denominator * denominator:
            divisor = int(np.gcd.reduce(np.abs(vector)))
            if divisor > 1:
                vector //= divisor
                denominator = int(vector @ vector)
                numerator = sum(int(vector[u]) * int(vector[v])
                                for u, neighbors in enumerate(adjacency) for v in neighbors)
            return {
                "target_order": len(adjacency),
                "rayleigh_numerator": numerator,
                "rayleigh_denominator": denominator,
                "integer_vector": vector.tolist(),
                "strict_square_test": numerator * numerator - len(adjacency) * denominator * denominator,
            }
    return None


def spectral_owner(edges, row):
    certificates = []
    for frontier in [None, *range(PATH_COUNT)]:
        certificate = rayleigh_certificate(canonical_graph(edges, row, frontier))
        if certificate is None:
            return None
        certificates.append(certificate)
    return certificates


def owner_lift_evidence(lane, certificates):
    if lane == "induced-packet":
        return {
            "classification": "conditional-structural-lift",
            "all_length_lift": False,
            "rooted_tree_lift": True,
            "valid_scope": "same-parity subdivisions outside the selected unit-edge anchor, with arbitrary rooted trees",
            "obstruction": "a general descendant may lengthen an edge of every available unit-edge anchor",
        }
    capacities = []
    for certificate in certificates:
        numerator = certificate["rayleigh_numerator"]
        denominator = certificate["rayleigh_denominator"]
        order = certificate["target_order"]
        capacities.append((numerator * numerator - 1) // (denominator * denominator) - order)
    return {
        "classification": "finite-direct-spectral-only",
        "all_length_lift": False,
        "rooted_tree_lift": False,
        "zero_extension_vertex_capacities": capacities,
        "minimum_zero_extension_vertex_capacity": min(capacities),
        "valid_scope": "induced-supergraph zero extension through the displayed finite vertex capacities",
        "obstruction": "the fixed Rayleigh quotient does not grow with order, and subdivision is not induced-supergraph inclusion",
    }


def strata_payload(rows, top):
    names = ("kernel", "support", "parity", "signed_degree", "dominant_family", "joint")
    counts = {name: Counter() for name in names}
    physical = {name: Counter() for name in names}
    descriptions = {name: {} for name in names}
    for item in rows:
        support, parity, graph = graph_data(item["edges"], item["row"])
        signed_degree = {
            "signed_imbalance_degree_partition": parity["signed_imbalance_degree_partition"],
            "absolute_imbalance_degree_partition": parity["absolute_imbalance_degree_partition"],
        }
        dominant = {
            "multiplicity_partition": support["multiplicity_partition"],
            "bundle_types": parity["bundle_types"],
            "cycle_rank": graph["cycle_rank"],
            "triangle_total": graph["triangle_total"],
        }
        payloads = {
            "kernel": {"global_kernel": item["global_kernel"],
                       "edges": [list(edge) for edge in item["edges"]]},
            "support": support,
            "parity": parity,
            "signed_degree": signed_degree,
            "dominant_family": dominant,
            "joint": {"support": support, "parity": parity,
                      "signed_degree": signed_degree, "graph": graph},
        }
        for name, payload in payloads.items():
            key = (f"k-{item['global_kernel']:04d}" if name == "kernel" else
                   signature_id(name[0], payload))
            counts[name][key] += 1
            physical[name][key] += item["orbit_size"]
            descriptions[name].setdefault(key, payload)
    concentration = {}
    top_strata = {}
    for name in names:
        ranked = sorted(counts[name].values(), reverse=True)
        concentration[name] = {
            "class_total": len(ranked),
            "largest_class_orbit_total": ranked[0] if ranked else 0,
            **{f"top_{width}_orbit_total": sum(ranked[:width])
               for width in (1, 10, 100, 1000)},
        }
        keys = sorted(counts[name], key=lambda key: (-counts[name][key],
                                                      -physical[name][key], key))
        top_strata[name] = [
            {"id": key, "orbit_total": counts[name][key],
             "physical_total": physical[name][key], "signature": descriptions[name][key]}
            for key in keys[:top]
        ]
    return {"concentration": concentration, "top_strata": top_strata}


def write_canonical(path, payload, compressed=False):
    raw = canonical_bytes(payload)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6) if compressed else raw
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(stored)
    temporary.replace(path)
    return {"path": path.name, "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "artifact_sha256": hashlib.sha256(stored).hexdigest(), "bytes": len(stored)}


def write_remainder(path, rows):
    raw_digest = hashlib.sha256()
    temporary = path.with_name(path.name + ".tmp")
    with lzma.open(temporary, "wb", format=lzma.FORMAT_XZ, preset=6) as stream:
        for item in rows:
            raw = canonical_bytes([
                item["stream_index"], item["source_index"], item["global_kernel"],
                [list(edge) for edge in item["edges"]], list(item["row"]), item["orbit_size"],
            ])
            raw_digest.update(raw)
            stream.write(raw)
    temporary.replace(path)
    return {"path": path.name, "record_total": len(rows),
            "raw_sha256": raw_digest.hexdigest(), "artifact_sha256": file_sha256(path)}


def build(top, progress=False):
    ledger, ledger_raw, _ = read_canonical(LEDGER_PATH)
    indices, indices_raw, indices_xz = read_canonical(INDICES_PATH, compressed=True)
    require(ledger.get("combined_indices") == {
        "path": INDICES_PATH.name, "raw_sha256": indices_raw, "xz_sha256": indices_xz,
    }, "combined ledger/index link changed")
    require(ledger.get("remaining_residual_total") == EXPECTED_REMAINDER and
            indices.get("schema") == "rank-seven-order-eight-combined-owner-indices-v1",
            "wrong combined remainder scope")
    remaining_indices = indices["exclusive_stream_indices"]["remaining"]
    require(len(remaining_indices) == EXPECTED_REMAINDER and
            remaining_indices == sorted(set(remaining_indices)), "combined remainder changed")

    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=CACHE_PATH)
    rows = []
    for stream_index in remaining_indices:
        source = residuals[stream_index]
        edges = tuple((census.PAIRS[dense][0], census.PAIRS[dense][1], multiplicity)
                      for dense, multiplicity in zip(source[2], source[3], strict=True))
        rows.append({"stream_index": stream_index, "source_index": source[1],
                     "global_kernel": source[0], "edges": edges, "row": tuple(source[4]),
                     "orbit_size": source[5]})
    require([item["source_index"] for item in rows] == indices["remaining_source_indices"],
            "remaining source indices changed")

    input_strata = strata_payload(rows, top)
    packet_owners = []
    spectral_owners = []
    unresolved = []
    for position, item in enumerate(rows, 1):
        packet = packet_owner(item["edges"], item["row"])
        if packet is not None:
            packet_owners.append({**item, "lane": "induced-packet", "certificates": packet})
        else:
            spectral = spectral_owner(item["edges"], item["row"])
            if spectral is not None:
                spectral_owners.append({**item, "lane": "direct-spectral-rayleigh",
                                        "certificates": spectral})
            else:
                unresolved.append(item)
        if progress and position % 5000 == 0:
            print(f"rows={position} packet={len(packet_owners)} "
                  f"spectral={len(spectral_owners)} unresolved={len(unresolved)}", flush=True)

    owner_rows = packet_owners + spectral_owners
    for item in owner_rows:
        item["lift_evidence"] = owner_lift_evidence(item["lane"], item["certificates"])
    theorem_owners = [item for item in owner_rows
                      if item["lift_evidence"]["all_length_lift"] and
                      item["lift_evidence"]["rooted_tree_lift"]]
    owner_payload = {
        "schema": OWNER_SCHEMA,
        "source_ledger_sha256": ledger_raw,
        "precedence": ["induced-packet", "direct-spectral-rayleigh"],
        "owners": [
            {"stream_index": item["stream_index"], "source_index": item["source_index"],
             "global_kernel": item["global_kernel"], "row": list(item["row"]),
             "lane": item["lane"], "certificates": item["certificates"],
             "lift_evidence": item["lift_evidence"]}
            for item in sorted(owner_rows, key=lambda value: value["stream_index"])
        ],
    }
    owner_artifact = write_canonical(OWNERS_PATH, owner_payload, compressed=True)
    remainder_artifact = write_remainder(REMAINDER_PATH, unresolved)
    output_strata = strata_payload(unresolved, top)
    packet_anchor_counts = Counter(certificate["anchor"]
                                   for item in packet_owners
                                   for certificate in item["certificates"])
    report = {
        "schema": SCHEMA,
        "status": "complete-exact-finite-remainder-scan",
        "full_theorem": len(unresolved) == 0,
        "scope": "84152-row order-eight combined remainder; finite canonical-plus-coordinate targets",
        "authenticated_inputs": {
            "combined_owner_ledger": {"path": LEDGER_PATH.name, "raw_sha256": ledger_raw},
            "combined_owner_indices": {"path": INDICES_PATH.name,
                                       "raw_sha256": indices_raw, "artifact_sha256": indices_xz},
            "source_stream_sha256": census.SOURCE_SHA256,
        },
        "input_remainder_orbit_total": len(rows),
        "input_remainder_physical_total": sum(item["orbit_size"] for item in rows),
        "input_remainder_target_total": len(rows) * TARGETS_PER_ROW,
        "owner_precedence": ["induced-packet", "direct-spectral-rayleigh"],
        "owner_evidence_status": "classified-finite-versus-theorem",
        "exclusive_owner_orbit_counts": {
            "induced-packet": len(packet_owners),
            "direct-spectral-rayleigh": len(spectral_owners),
        },
        "exclusive_owner_physical_counts": {
            "induced-packet": sum(item["orbit_size"] for item in packet_owners),
            "direct-spectral-rayleigh": sum(item["orbit_size"] for item in spectral_owners),
        },
        "exclusive_owner_target_counts": {
            "induced-packet": len(packet_owners) * TARGETS_PER_ROW,
            "direct-spectral-rayleigh": len(spectral_owners) * TARGETS_PER_ROW,
        },
        "packet_target_anchor_counts": dict(sorted(packet_anchor_counts.items())),
        "remaining_orbit_total": len(unresolved),
        "remaining_physical_total": sum(item["orbit_size"] for item in unresolved),
        "remaining_target_total": len(unresolved) * TARGETS_PER_ROW,
        "theorem_eligible_owner_orbit_total": len(theorem_owners),
        "theorem_eligible_owner_target_total": len(theorem_owners) * TARGETS_PER_ROW,
        "theorem_eligible_remainder_orbit_total": len(rows) - len(theorem_owners),
        "theorem_eligible_remainder_target_total": ((len(rows) - len(theorem_owners)) *
                                                     TARGETS_PER_ROW),
        "lift_classification_orbit_counts": {
            "conditional-structural-lift": len(packet_owners),
            "finite-direct-spectral-only": len(spectral_owners),
            "full-descendant-lift": len(theorem_owners),
        },
        "partition_identity": (f"{len(rows)} = {len(packet_owners)} + "
                               f"{len(spectral_owners)} + {len(unresolved)}"),
        "exact_methods": {
            "induced-packet": "K5/K4/diamond induced anchor plus exact tree-or-odd-unicyclic complement debit on every target",
            "direct-spectral-rayleigh": "integer vector x with (x^T A x)^2 > |V|(x^T x)^2 and x^T A x > 0 on every target",
        },
        "owner_artifact": owner_artifact,
        "updated_remainder_stream": remainder_artifact,
        "input_stratification": input_strata,
        "output_stratification": output_strata,
        "claim_boundary": "all 296 owners remain theorem-ineligible: packet lifts require an untouched unit-edge anchor, while fixed Rayleigh quotients have only bounded zero-extension scope",
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=REPORT_PATH)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.top > 0 and args.output.parent.is_dir(), "invalid output or top count")
    expected_report = args.output.read_bytes() if args.audit else None
    expected_owners = OWNERS_PATH.read_bytes() if args.audit else None
    expected_remainder = REMAINDER_PATH.read_bytes() if args.audit else None
    report = build(args.top, args.progress)
    raw = canonical_bytes(report)
    if args.audit:
        require(expected_report == raw, "analysis report differs from exact rescan")
        require(expected_owners == OWNERS_PATH.read_bytes(),
                "owner artifact differs from exact rescan")
        require(expected_remainder == REMAINDER_PATH.read_bytes(),
                "updated remainder differs from exact rescan")
    else:
        args.output.write_bytes(raw)
    print(json.dumps({
        "input": report["input_remainder_orbit_total"],
        "owners": report["exclusive_owner_orbit_counts"],
        "remaining": report["remaining_orbit_total"],
        "sha256": hashlib.sha256(raw).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as error:
        sys.stderr.write(f"rank-seven order-eight remainder analysis: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
