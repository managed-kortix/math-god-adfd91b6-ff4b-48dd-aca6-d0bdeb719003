#!/usr/bin/env python3
"""Exact order-ten remainder stratification and defect-adapted Gram pilot."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
OWNER = HERE / "rank7_order10_structural_owners.py"
KERNEL_SOURCE = HERE / "rank7_parity_coarse_digest_census.py"
MANIFEST = HERE / "rank7_order10_structural_owner_manifest.json"
RESULTS = HERE / "rank7_order10_structural_owner_scheduler" / "results"
OUTPUT = HERE / "rank7_order10_near_cubic_gram_lane.json"
SCHEMA = "rank-seven-order-ten-near-cubic-gram-lane-v1"
ORDER = 10
PATH_COUNT = 16
BUDGET = Fraction(6)
F = Fraction
PARAMETERS = ((F(1, 2), F(1, 4)), (F(3, 4), F(1, 2)),
              (F(1, 2), F(1, 2)), (F(1, 4), F(1, 4)),
              (F(3, 4), F(3, 4)))


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


def load_module(name, path):
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


def bridge_total(adjacency):
    timer = total = 0
    discovery = [-1] * ORDER
    low = [0] * ORDER

    def visit(vertex, parent):
        nonlocal timer, total
        discovery[vertex] = low[vertex] = timer
        timer += 1
        for neighbor in adjacency[vertex]:
            if neighbor == parent:
                continue
            if discovery[neighbor] < 0:
                visit(neighbor, vertex)
                low[vertex] = min(low[vertex], low[neighbor])
                total += low[neighbor] > discovery[vertex]
            else:
                low[vertex] = min(low[vertex], discovery[neighbor])
    visit(0, -1)
    return total


def kernel_dictionary():
    source = load_module("rank7_order10_near_cubic_kernels", KERNEL_SOURCE)
    result = {}
    for global_kernel, order_kernel, order, raw_edges in source.source_kernels():
        if order != ORDER:
            continue
        edges = tuple(map(tuple, raw_edges))
        degrees = [0] * ORDER
        adjacency = [set() for _ in range(ORDER)]
        for u, v, multiplicity in edges:
            degrees[u] += multiplicity
            degrees[v] += multiplicity
            adjacency[u].add(v)
            adjacency[v].add(u)
        partition = tuple(sorted(degrees, reverse=True))
        require(partition in ((4, 4) + (3,) * 8, (5,) + (3,) * 9),
                "order-ten kernel is not near cubic with defect four")
        result[order_kernel] = {
            "global_kernel": global_kernel, "edges": edges,
            "degrees": tuple(degrees), "degree_partition": partition,
            "defect_partition": tuple(sorted((degree - 3 for degree in degrees),
                                               reverse=True)),
            "multiplicity_partition": tuple(sorted((edge[2] for edge in edges),
                                                     reverse=True)),
            "support_cycle_rank": len(edges) - ORDER + 1,
            "support_bridge_total": bridge_total(adjacency),
            "triangle_total": sum(len(adjacency[u] & adjacency[v])
                                  for u in range(ORDER) for v in adjacency[u]
                                  if u < v) // 3,
        }
    require(len(result) == 3396, "order-ten kernel total changed")
    return result


def remainder_records(manifest):
    for chunk_index, expected in enumerate(manifest["chunks"]):
        receipt, _ = strict_json(RESULTS / f"chunk-{chunk_index:02d}.json")
        require(receipt["remainder_orbit_total"] == expected["remainder_orbit_total"],
                "remainder receipt count changed")
        stream = receipt["remainder_stream"]
        path = RESULTS / stream["path"]
        require(file_sha256(path) == stream["artifact_sha256"],
                "remainder artifact changed")
        digest = hashlib.sha256()
        count = 0
        with lzma.open(path, "rb") as rows:
            for raw in rows:
                record = json.loads(raw.decode("ascii"))
                require(raw == canonical_bytes(record) and len(record) == 5,
                        "noncanonical remainder row")
                digest.update(raw)
                count += 1
                yield record
        require((count, digest.hexdigest()) ==
                (receipt["remainder_orbit_total"], stream["sha256"]),
                "remainder stream authentication failed")


def cycle_rank(edges, selected):
    adjacency = [set() for _ in range(ORDER)]
    edge_total = 0
    for flag, (u, v, _) in zip(selected, edges, strict=True):
        if flag:
            adjacency[u].add(v)
            adjacency[v].add(u)
            edge_total += 1
    active = {vertex for vertex in range(ORDER) if adjacency[vertex]}
    components = 0
    while active:
        components += 1
        todo = [active.pop()]
        for vertex in todo:
            for neighbor in adjacency[vertex] & active:
                active.remove(neighbor)
                todo.append(neighbor)
    vertices = sum(bool(neighbors) for neighbors in adjacency)
    return edge_total - vertices + components if edge_total else 0


def is_cut(edges, signs):
    adjacency = [[] for _ in range(ORDER)]
    for sign, (u, v, _) in zip(signs, edges, strict=True):
        adjacency[u].append((v, sign))
        adjacency[v].append((u, sign))
    labels = [None] * ORDER
    labels[0] = False
    todo = [0]
    for vertex in todo:
        for neighbor, sign in adjacency[vertex]:
            expected = labels[vertex] ^ sign
            if labels[neighbor] is None:
                labels[neighbor] = expected
                todo.append(neighbor)
            elif labels[neighbor] != expected:
                return False
    return True


def row_invariants(kernel, row):
    signed_degree = [0] * ORDER
    absolute_degree = [0] * ORDER
    odd_degree = [0] * ORDER
    bundle_types = [0, 0, 0]
    negative = []
    odd_support = []
    for (u, v, multiplicity), odd in zip(kernel["edges"], row, strict=True):
        value = multiplicity - 2 * odd
        bundle_types[0 if odd == 0 else (2 if odd == multiplicity else 1)] += 1
        negative.append(value < 0)
        odd_support.append(bool(odd))
        for vertex in (u, v):
            signed_degree[vertex] += value
            absolute_degree[vertex] += abs(value)
            odd_degree[vertex] += odd
    return {
        "parity": {"bundle_types": bundle_types,
                   "odd_count_partition": sorted(row, reverse=True),
                   "odd_degree_partition": sorted(odd_degree, reverse=True)},
        "signed_degree": {
            "signed_degree_partition": sorted(signed_degree, reverse=True),
            "absolute_signed_degree_partition": sorted(absolute_degree, reverse=True),
            "negative_bundle_total": sum(negative)},
        "cycle_cut": {"negative_signature_is_cut": is_cut(kernel["edges"], negative),
                      "negative_support_cycle_rank": cycle_rank(kernel["edges"], negative),
                      "odd_support_cycle_rank": cycle_rank(kernel["edges"], odd_support)},
    }


def gram_cost(edges, degrees, row, cubic_parameter, defect_parameter):
    signed = [[0] * ORDER for _ in range(ORDER)]
    paths = []
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        signed[u][v] = signed[v][u] = multiplicity - 2 * odd
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((u, v, length) for length in lengths)
    require(len(paths) == PATH_COUNT, "path count changed")
    square = [[sum(signed[u][w] * signed[v][w] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    parameters = [cubic_parameter if degree == 3 else defect_parameter
                  for degree in degrees]
    normalizer = max(1 + parameters[u] ** 2 * square[u][u]
                     for u in range(ORDER))
    total = F()
    for u, v, length in paths:
        correlation = ((parameters[u] + parameters[v]) * signed[u][v] +
                       parameters[u] * parameters[v] * square[u][v]) / normalizer
        transformed = -correlation if length & 1 else correlation
        if not -1 < transformed <= 1:
            return None
        total += (1 - transformed) / (length * (1 + transformed))
        if total > BUDGET:
            return total
    return total


def near_cubic_defect_gram_owner(edges, degrees, row):
    """Test G=XX^T/M plus diagonal completion for X=I+D(deg)S."""
    best = None
    for cubic_parameter, defect_parameter in PARAMETERS:
        cost = gram_cost(edges, degrees, row, cubic_parameter, defect_parameter)
        if cost is not None and (best is None or cost < best[0]):
            best = cost, cubic_parameter, defect_parameter
    return best


def pair(value):
    return [value.numerator, value.denominator]


def signature(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def concentration(counter):
    ranked = sorted(counter.values(), reverse=True)
    return {"class_total": len(ranked),
            "largest_class_orbit_total": ranked[0] if ranked else 0,
            "top_10_orbit_total": sum(ranked[:10]),
            "top_100_orbit_total": sum(ranked[:100])}


def top_rows(counter, descriptions, width=20):
    return [{"orbit_total": count, "signature": descriptions[key]}
            for key, count in counter.most_common(width)]


def scan(owner_path, representative_stride, limit=None, progress=False):
    manifest, manifest_sha256 = strict_json(owner_path)
    kernels = kernel_dictionary()
    names = ("degree_defect", "multiplicity", "parity", "signed_degree",
             "cycle_cut", "joint")
    counts = {name: Counter() for name in names}
    descriptions = {name: {} for name in names}
    representatives = []
    digest = hashlib.sha256()
    scanned = physical = 0
    for record in remainder_records(manifest):
        if limit is not None and scanned >= limit:
            break
        source_index, global_kernel, order_kernel, raw_row, orbit_size = record
        kernel = kernels[order_kernel]
        require(global_kernel == kernel["global_kernel"], "kernel reference changed")
        row_data = row_invariants(kernel, tuple(raw_row))
        payloads = {
            "degree_defect": {"degree_partition": kernel["degree_partition"],
                              "defect_partition": kernel["defect_partition"]},
            "multiplicity": {
                "multiplicity_partition": kernel["multiplicity_partition"],
                "support_cycle_rank": kernel["support_cycle_rank"],
                "support_bridge_total": kernel["support_bridge_total"],
                "triangle_total": kernel["triangle_total"]},
            **row_data,
        }
        payloads["joint"] = {name: payloads[name] for name in names[:-1]}
        for name, payload in payloads.items():
            encoded = signature(payload)
            counts[name][encoded] += 1
            descriptions[name].setdefault(encoded, payload)
        if scanned % representative_stride == 0:
            representatives.append((record, kernel))
        digest.update(canonical_bytes(record))
        physical += orbit_size
        scanned += 1
        if progress and scanned % 250000 == 0:
            print(f"rows={scanned} representatives={len(representatives)}", flush=True)
    if limit is None:
        require((scanned, physical, digest.hexdigest()) ==
                (manifest["remainder_orbit_total"], manifest["remainder_physical_total"],
                 manifest["remainder_stream_sha256"]),
                "full remainder authentication failed")

    wrapper = load_module("rank7_order10_near_cubic_owner", OWNER)
    ray_engine = wrapper.load_core().load_engine()
    records = []
    ray_owned = gram_owned = union_owned = gram_not_ray = 0
    for record, kernel in representatives:
        source_index, global_kernel, _, raw_row, _ = record
        row = tuple(raw_row)
        ray_witness = ray_engine.generalized_three_ray_witness(kernel["edges"], row)
        gram_witness = near_cubic_defect_gram_owner(kernel["edges"],
                                                    kernel["degrees"], row)
        ray = ray_witness is not None
        gram = gram_witness is not None and gram_witness[0] <= BUDGET
        ray_owned += ray
        gram_owned += gram
        union_owned += ray or gram
        gram_not_ray += gram and not ray
        records.append({
            "source_index": source_index, "global_kernel": global_kernel,
            "degree_partition": kernel["degree_partition"],
            "generalized_ray_owner": ray,
            "generalized_ray_cost_scaled_18": (None if ray_witness is None else
                                               ray_engine.three_ray_witness_cost(
                                                   kernel["edges"], row, ray_witness)),
            "near_cubic_gram_owner": gram,
            "near_cubic_gram_cost": None if gram_witness is None else pair(gram_witness[0]),
            "parameters": None if gram_witness is None else
                [pair(gram_witness[1]), pair(gram_witness[2])],
        })
    return {
        "schema": SCHEMA, "full_theorem": False,
        "scope": "exact full-remainder stratification; deterministic representative Gram pilot",
        "owner_manifest_sha256": manifest_sha256,
        "remainder_stream_sha256": digest.hexdigest(),
        "scanned_remainder_orbit_total": scanned,
        "scanned_remainder_physical_total": physical,
        "stratification": {name: {"concentration": concentration(counts[name]),
                                   "top_strata": top_rows(counts[name], descriptions[name])}
                           for name in names},
        "near_cubic_kernel_ledger": {
            "kernel_total": len(kernels),
            "degree_partition_counts": dict(sorted(Counter(
                signature({"degree_partition": kernel["degree_partition"]})
                for kernel in kernels.values()).items())),
            "degree_defect_identity": "sum_v(deg(v)-3)=2",
        },
        "generalized_ray_failure": {
            "reason": "the six-state family quantizes transformed correlations to 1, 1/2, -1/2, or -1; mixed bundles must cross a three-cut and the exact bundle table can exceed 108 before defect hubs are accommodated",
            "tested_representative_total": len(representatives),
            "owned_representative_total": ray_owned,
            "failed_representative_total": len(representatives) - ray_owned,
        },
        "near_cubic_defect_gram": {
            "formula": "X=I+D(deg)S; G=XX^T/M+diag(1-diag(XX^T)/M)",
            "parameters": [[pair(a), pair(b)] for a, b in PARAMETERS],
            "parameter_order": ["degree-3", "degree-greater-than-3"],
            "psd_proof": "XX^T/M plus nonnegative diagonal rank-one squares",
            "tested_representative_total": len(representatives),
            "owned_representative_total": gram_owned,
            "owned_beyond_generalized_ray_total": gram_not_ray,
            "union_owned_representative_total": union_owned,
            "records": records,
        },
        "claim_boundary": "the Gram formula owns only representative records marked near_cubic_gram_owner; no full-remainder Gram coverage is claimed",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--representative-stride", type=int, default=10000)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.representative_stride > 0, "representative stride must be positive")
    report = scan(args.owner_manifest, args.representative_stride,
                  args.limit, args.progress)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"scanned={report['scanned_remainder_orbit_total']} "
          f"representatives={report['near_cubic_defect_gram']['tested_representative_total']} "
          f"gram_owned={report['near_cubic_defect_gram']['owned_representative_total']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
