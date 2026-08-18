#!/usr/bin/env python3
"""Stratify exact order-nine structural-owner residuals without witness search."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
OWNER_SCAN = HERE / "rank7_order9_structural_owners.py"
KERNEL_SOURCE = HERE / "rank7_parity_coarse_digest_census.py"
DEFAULT_CENSUS = HERE / "rank7_order9_exact_residual_census_manifest.json"
DEFAULT_OWNER_MANIFEST = HERE / "rank7_order9_structural_owner_manifest.json"
SCHEMA = "rank-seven-order-nine-unowned-structural-stratification-v2"
INDEX_SCHEMA = "rank-seven-order-nine-unowned-search-indices-v1"


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


def load_scan_engine():
    spec = importlib.util.spec_from_file_location("rank7_order9_stratifier_owner", OWNER_SCAN)
    require(spec is not None and spec.loader is not None, "cannot load owner scan")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strict_canonical_json(path, label):
    raw = path.read_bytes()
    try:
        payload = json.loads(raw.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical JSON")
    return payload, hashlib.sha256(raw).hexdigest()


def signature_id(prefix, payload):
    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return f"{prefix}-{digest[:20]}"


def graph_invariants(edges, row, order):
    adjacency = [set() for _ in range(order)]
    signed_adjacency = [set() for _ in range(order)]
    for (u, v, _), odd in zip(edges, row, strict=True):
        adjacency[u].add(v)
        adjacency[v].add(u)
        if odd:
            signed_adjacency[u].add(v)
            signed_adjacency[v].add(u)

    components = []
    unseen = set(range(order))
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
    discovery = [-1] * order
    low = [0] * order

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

    for vertex in range(order):
        if discovery[vertex] < 0:
            visit(vertex, -1)
    triangles = sum(len(adjacency[u] & adjacency[v])
                    for u in range(order) for v in adjacency[u] if u < v) // 3
    odd_support_edges = sum(bool(odd) for odd in row)
    return {
        "component_order_partition": sorted((len(value) for value in components), reverse=True),
        "cycle_rank": len(edges) - order + len(components),
        "bridge_total": bridges,
        "triangle_total": triangles,
        "odd_support_edge_total": odd_support_edges,
        "odd_support_degree_partition": sorted((len(value) for value in signed_adjacency),
                                                 reverse=True),
    }


def graph_data(edges, row, order):
    support_degrees = [0] * order
    weighted_degrees = [0] * order
    odd_degrees = [0] * order
    absolute_imbalance_degrees = [0] * order
    signed_imbalance_degrees = [0] * order
    support_incidence = [[] for _ in range(order)]
    parity_incidence = [[] for _ in range(order)]
    bundle_types = Counter()
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        signed = multiplicity - 2 * odd
        kind = "zero" if odd == 0 else ("full" if odd == multiplicity else "mixed")
        bundle_types[kind] += 1
        for vertex in (u, v):
            support_degrees[vertex] += 1
            weighted_degrees[vertex] += multiplicity
            odd_degrees[vertex] += odd
            absolute_imbalance_degrees[vertex] += abs(signed)
            signed_imbalance_degrees[vertex] += signed
            support_incidence[vertex].append(multiplicity)
            parity_incidence[vertex].append([multiplicity, odd])
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
        "bundle_types": [bundle_types["zero"], bundle_types["mixed"],
                         bundle_types["full"]],
        "odd_degree_partition": sorted(odd_degrees, reverse=True),
        "absolute_imbalance_degree_partition": sorted(
            absolute_imbalance_degrees, reverse=True),
        "signed_imbalance_degree_partition": sorted(signed_imbalance_degrees,
                                                      reverse=True),
        "vertex_parity_fingerprints": sorted(
            (sorted(values, reverse=True) for values in parity_incidence), reverse=True),
    }
    return support, parity, graph_invariants(edges, row, order)


def kernel_dictionary(engine):
    spec = importlib.util.spec_from_file_location("rank7_order9_stratifier_kernels",
                                                  KERNEL_SOURCE)
    require(spec is not None and spec.loader is not None, "cannot load kernel source")
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    require(source.SOURCE_SHA256 == engine.SOURCE_SHA256, "kernel source pin changed")
    items = tuple(item for item in source.source_kernels() if item[2] == engine.ORDER)
    require(len(items) == engine.KERNEL_TOTAL, "kernel source total changed")
    result = {}
    for global_kernel, order_kernel, order, edges in items:
        require(order_kernel not in result and order == engine.ORDER,
                "duplicate or wrong-order kernel")
        result[order_kernel] = (global_kernel, tuple(map(tuple, edges)))
    return result


def remainder_records(owner_path, owner_manifest):
    result_dir = owner_path.parent / "rank7_order9_structural_owner_scheduler" / "results"
    for chunk_index, expected in enumerate(owner_manifest["chunks"]):
        receipt_path = result_dir / f"chunk-{chunk_index:02d}.json"
        receipt, _ = strict_canonical_json(receipt_path, "structural owner chunk receipt")
        require(receipt["chunk_index"] == chunk_index and
                receipt["remainder_orbit_total"] == expected["remainder_orbit_total"],
                f"wrong remainder receipt: {receipt_path.name}")
        stream = receipt["remainder_stream"]
        path = result_dir / stream["path"]
        require(file_sha256(path) == stream["artifact_sha256"],
                f"remainder artifact changed: {path.name}")
        digest = hashlib.sha256()
        count = 0
        try:
            with lzma.open(path, "rb") as rows:
                for raw in rows:
                    record = json.loads(raw.decode("ascii"))
                    require(raw == canonical_bytes(record) and len(record) == 5,
                            f"noncanonical remainder row: {path.name}")
                    digest.update(raw)
                    count += 1
                    yield record
        except (lzma.LZMAError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RuntimeError(f"cannot read remainder stream: {path.name}") from error
        require(count == receipt["remainder_orbit_total"] and
                digest.hexdigest() == stream["sha256"],
                f"remainder stream authentication failed: {path.name}")


def family_tags(edges, support, parity):
    simple = all(edge[2] == 1 for edge in edges)
    mixed = parity["bundle_types"][1]
    maximum_degree = max(support["weighted_degree_partition"], default=0)
    tags = ["four-ray-switching"]
    if simple:
        tags.append("signed-adjacency-polynomial")
    else:
        tags.extend(("multigraph-adjacency-polynomial", "rank-six-edge-opening"))
    if mixed:
        tags.append("coupled-mixed-bundle-atoms")
    if maximum_degree >= 4:
        tags.append("high-degree-star-simplex")
    return sorted(tags)


def ranked_rows(counts, physical, descriptions, limit):
    keys = sorted(counts, key=lambda key: (-counts[key], -physical[key], key))
    return [{"id": key, "orbit_total": counts[key],
             "physical_total": physical[key], "signature": descriptions[key]}
            for key in keys[:limit]]


def concentration(counts, total):
    ranked = sorted(counts.values(), reverse=True)
    square_sum = sum(value * value for value in ranked)
    result = {
        "class_total": len(ranked),
        "largest_class_orbit_total": ranked[0] if ranked else 0,
        "herfindahl_numerator": square_sum,
        "herfindahl_denominator": total * total if total else 1,
    }
    for width in (1, 10, 100, 1000):
        result[f"top_{width}_orbit_total"] = sum(ranked[:width])
    return result


def scan(census_path, owner_path, index_path, top, limit=None, progress=False):
    engine = load_scan_engine()
    census, census_sha256 = engine.load_manifest(census_path)
    owner_manifest, owner_sha256 = strict_canonical_json(owner_path,
                                                         "structural owner manifest")
    engine.verify_report(owner_manifest)
    require(owner_manifest.get("manifest_sha256") == census_sha256,
            "owner manifest does not reference this census")
    require(owner_manifest.get("owner_engine_sha256") == file_sha256(engine.OWNER_ENGINE),
            "owner engine changed since owner manifest")
    kernels = kernel_dictionary(engine)

    counts = {name: Counter() for name in
              ("kernel", "support", "parity", "signed_degree", "graph",
               "dominant_family", "joint")}
    physical = {name: Counter() for name in counts}
    descriptions = {name: {} for name in counts}
    family_indices = defaultdict(list)
    signature_indices = {name: defaultdict(list) for name in counts}
    unowned_indices = []
    remainder_digest = hashlib.sha256()
    source_index = 0
    unowned_physical = 0
    for record in remainder_records(owner_path, owner_manifest):
        if limit is not None and source_index >= limit:
            break
        original_source_index, global_kernel, order_kernel, raw_row, orbit_size = record
        expected_global, edges = kernels[order_kernel]
        require(global_kernel == expected_global, "remainder kernel reference changed")
        row = tuple(raw_row)
        support, parity, graph = graph_data(edges, row, engine.ORDER)
        signed_degree = {
            "signed_imbalance_degree_partition":
                parity["signed_imbalance_degree_partition"],
            "absolute_imbalance_degree_partition":
                parity["absolute_imbalance_degree_partition"],
        }
        dominant_family = {
            "multiplicity_partition": support["multiplicity_partition"],
            "bundle_types": parity["bundle_types"],
            "cycle_rank": graph["cycle_rank"],
            "triangle_total": graph["triangle_total"],
        }
        kernel_description = {
            "global_kernel": global_kernel,
            "edges": [list(edge) for edge in edges],
        }
        payloads = {
            "kernel": kernel_description,
            "support": support,
            "parity": parity,
            "signed_degree": signed_degree,
            "graph": graph,
            "dominant_family": dominant_family,
            "joint": {"support": support, "parity": parity,
                      "signed_degree": signed_degree, "graph": graph},
        }
        for name, payload in payloads.items():
            key = (f"k-{global_kernel:04d}" if name == "kernel" else
                   signature_id(name[0], payload))
            counts[name][key] += 1
            physical[name][key] += orbit_size
            descriptions[name].setdefault(key, payload)
            signature_indices[name][key].append(source_index)
        for family in family_tags(edges, support, parity):
            family_indices[family].append(source_index)
        unowned_indices.append(original_source_index)
        unowned_physical += orbit_size
        remainder_digest.update(canonical_bytes(record))
        source_index += 1
        if progress and source_index % 50000 == 0:
            print(f"remainder_rows={source_index}", flush=True)

    if limit is None:
        require(source_index == owner_manifest["remainder_orbit_total"] and
                len(unowned_indices) == owner_manifest["remainder_orbit_total"] and
                unowned_physical == owner_manifest["remainder_physical_total"] and
                remainder_digest.hexdigest() == owner_manifest["remainder_stream_sha256"],
                "unowned stream differs from owner manifest")

    indices = {
        "schema": INDEX_SCHEMA,
        "full_theorem": False,
        "scope": "exact unowned source indices only; no rational witness search",
        "owner_manifest_sha256": owner_sha256,
        "source_indices": unowned_indices,
        "source_indices_sha256": hashlib.sha256(
            b"".join(str(value).encode("ascii") + b"\n" for value in unowned_indices)).hexdigest(),
        "family_source_indices": {key: value for key, value in sorted(family_indices.items())},
        "signature_source_indices": {
            name: {key: value for key, value in sorted(groups.items())}
            for name, groups in signature_indices.items()
        },
    }
    index_path.write_bytes(canonical_bytes(indices))
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "exact structural-owner remainder stratification; no rational brute force",
        "census_manifest_sha256": census_sha256,
        "owner_manifest_sha256": owner_sha256,
        "scanned_remainder_total": source_index,
        "source_universe_residual_total": owner_manifest["scanned_residual_total"],
        "unowned_orbit_total": len(unowned_indices),
        "unowned_physical_total": unowned_physical,
        "unowned_target_total": len(unowned_indices) * engine.TARGETS_PER_RESIDUAL,
        "remainder_stream_sha256": remainder_digest.hexdigest(),
        "concentration": {name: concentration(counts[name], len(unowned_indices))
                          for name in counts},
        "top_strata": {name: ranked_rows(counts[name], physical[name],
                                          descriptions[name], top)
                       for name in counts},
        "candidate_owner_family_counts": {
            key: len(value) for key, value in sorted(family_indices.items())},
        "candidate_owner_families": {
            "four-ray-switching": "extend the exhausted switched three-ray state space",
            "signed-adjacency-polynomial": "exact low-degree polynomial Gram on simple supports",
            "multigraph-adjacency-polynomial": "bundle-weighted signed adjacency polynomial Gram",
            "rank-six-edge-opening": "delete one bundled path, own the rank-six core, then restore it",
            "coupled-mixed-bundle-atoms": "compose local mixed atoms across interacting bundles",
            "high-degree-star-simplex": "centered simplex blocks around weighted degree at least four",
        },
        "search_index_artifact": {
            "path": os.path.relpath(index_path, owner_path.parent),
            "artifact_sha256": file_sha256(index_path),
            "source_indices_total": len(unowned_indices),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    parser.add_argument("--owner-manifest", type=Path, default=DEFAULT_OWNER_MANIFEST)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--index-output", required=True, type=Path)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--limit", type=int, help="test-only source-row limit")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    require(args.top >= 1, "top-stratum count must be positive")
    require(args.output.parent.is_dir() and args.index_output.parent.is_dir(),
            "output parent does not exist")
    report = scan(args.census, args.owner_manifest, args.index_output,
                  args.top, args.limit, args.progress)
    args.output.write_bytes(canonical_bytes(report))
    print(f"scanned={report['scanned_remainder_total']} "
          f"unowned={report['unowned_orbit_total']} "
          f"joint_signatures={report['concentration']['joint']['class_total']} "
          f"index_sha256={report['search_index_artifact']['artifact_sha256']}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-nine unowned stratification: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
