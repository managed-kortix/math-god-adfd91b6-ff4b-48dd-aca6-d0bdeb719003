#!/usr/bin/env python3
"""Cluster all order-twelve three-ray failures and test exact Gram families."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OWNER_PATH = HERE / "rank7_order12_structural_owners.py"
MANIFEST_PATH = HERE / "rank7_order12_structural_owner_manifest.json"
F = Fraction
ORDER = 12
PATH_COUNT = 18
BUDGET = F(6)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_owner_engine():
    spec = importlib.util.spec_from_file_location("rank7_order12_obstruction_owner", OWNER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load owner engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def row_signature(edges, row):
    support = len(edges)
    multiplicities = tuple(sorted((edge[2] for edge in edges), reverse=True))
    types = Counter()
    imbalance_degree = [0] * ORDER
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        kind = "zero" if odd == 0 else ("full" if odd == multiplicity else "mixed")
        types[kind] += 1
        value = abs(multiplicity - 2 * odd)
        imbalance_degree[u] += value
        imbalance_degree[v] += value
    return (support, multiplicities, types["zero"], types["mixed"], types["full"],
            tuple(sorted(imbalance_degree, reverse=True)))


def signature_json(signature):
    support, multiplicities, zero, mixed, full, imbalance_degree = signature
    return {
        "support": support,
        "multiplicity_partition": list(multiplicities),
        "bundle_types": [zero, mixed, full],
        "absolute_imbalance_degrees": list(imbalance_degree),
    }


def row_key(source):
    return hashlib.sha256(canonical_bytes([
        source["global_kernel"], source["order_kernel"], source["row"]
    ])).digest()


def signed_matrix(edges, row):
    matrix = [[0] * ORDER for _ in range(ORDER)]
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        matrix[u][v] = matrix[v][u] = multiplicity - 2 * odd
    return matrix


def expanded_paths(edges, row):
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, u, v, length) for length in lengths)
    require(len(paths) == PATH_COUNT, "physical path count changed")
    return paths


def numerical_embedding(edges, row):
    signed = np.asarray(signed_matrix(edges, row), dtype=float)
    spectral = np.linalg.eigvalsh(signed)
    incidence = np.zeros((ORDER, PATH_COUNT), dtype=float)
    for column, (_, u, v, length) in enumerate(expanded_paths(edges, row)):
        incidence[u, column] = 1.0
        incidence[v, column] = -1.0 if length & 1 else 1.0
    singular = np.linalg.svd(incidence, compute_uv=False)
    projection = np.eye(PATH_COUNT) - np.linalg.pinv(incidence) @ incidence
    leverage = np.diag(projection)
    return {
        "signed_spectrum": [round(float(value), 8) for value in spectral],
        "signed_incidence_singular_values": [round(float(value), 8) for value in singular],
        "cycle_space_dimension": int(round(float(np.trace(projection)))),
        "cycle_leverage_histogram": histogram(leverage),
    }


def histogram(values):
    counts = Counter(round(float(value), 6) for value in values)
    return [[key, counts[key]] for key in sorted(counts)]


def candidate_coefficients():
    values = sorted({F(numerator, denominator)
                     for denominator in range(1, 7)
                     for numerator in range(-denominator, denominator + 1)})
    pairs = [(a, b) for a in values for b in values if a or b]
    return sorted(pairs, key=lambda pair: (abs(pair[0]) + abs(pair[1]),
                                           abs(pair[1]), pair[0], pair[1]))


COEFFICIENTS = candidate_coefficients()


def polynomial_gram(signed, a, b):
    square = [[sum(signed[u][w] * signed[w][v] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    gram = [[F(int(u == v)) for v in range(ORDER)] for u in range(ORDER)]
    for u in range(ORDER):
        for v in range(u + 1, ORDER):
            gram[u][v] = gram[v][u] = a * signed[u][v] + b * square[u][v]
    if any(sum(abs(gram[u][v]) for v in range(ORDER) if v != u) > 1
           for u in range(ORDER)):
        return None
    return gram


def path_bound(correlation, length):
    transformed = -correlation if length & 1 else correlation
    if not -1 < transformed <= 1:
        return None
    return (1 - transformed) / (length * (1 + transformed))


def gram_cost(gram, paths, stop=BUDGET):
    total = F()
    for _, u, v, length in paths:
        value = path_bound(gram[u][v], length)
        if value is None:
            return None
        total += value
        if total > stop:
            return total
    return total


def fraction_json(value):
    return [value.numerator, value.denominator]


def search_direct(edges, row):
    signed = signed_matrix(edges, row)
    paths = expanded_paths(edges, row)
    best = None
    for a, b in COEFFICIENTS:
        gram = polynomial_gram(signed, a, b)
        if gram is None:
            continue
        cost = gram_cost(gram, paths)
        if cost is not None and (best is None or cost < best[0]):
            best = cost, a, b
            if cost <= BUDGET:
                break
    if best is None:
        return None
    return {"certified": best[0] <= BUDGET, "cost": fraction_json(best[0]),
            "a": fraction_json(best[1]), "b": fraction_json(best[2]),
            "psd_proof": "symmetric diagonal dominance"}


def delete_path(edges, row, edge_index, length):
    reduced_edges = [list(edge) for edge in edges]
    reduced_row = list(row)
    reduced_edges[edge_index][2] -= 1
    if length & 1:
        reduced_row[edge_index] -= 1
    if reduced_edges[edge_index][2] == 0:
        del reduced_edges[edge_index]
        del reduced_row[edge_index]
    return tuple(map(tuple, reduced_edges)), tuple(reduced_row)


def search_edge_opening(edges, row):
    original_paths = expanded_paths(edges, row)
    for physical_index, (edge_index, u, v, length) in enumerate(original_paths):
        reduced_edges, reduced_row = delete_path(edges, row, edge_index, length)
        signed = signed_matrix(reduced_edges, reduced_row)
        reduced_paths = expanded_paths_variable(reduced_edges, reduced_row)
        for a, b in COEFFICIENTS:
            gram = polynomial_gram(signed, a, b)
            if gram is None:
                continue
            deleted_cost = gram_cost(gram, reduced_paths, F(5))
            if deleted_cost is None or deleted_cost > 5:
                continue
            restored = path_bound(gram[u][v], length)
            if restored is not None and deleted_cost + restored <= BUDGET:
                return {
                    "certified": True,
                    "physical_path": physical_index,
                    "length": length,
                    "rank6_cost": fraction_json(deleted_cost),
                    "restored_path_bound": fraction_json(restored),
                    "a": fraction_json(a),
                    "b": fraction_json(b),
                    "criterion": "E6+(1-t)/(q*(1+t))<=6",
                    "psd_proof": "symmetric diagonal dominance",
                }
    return {"certified": False}


def expanded_paths_variable(edges, row):
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, u, v, length) for length in lengths)
    return paths


def mine(paths, representatives, verify_rows, limit=None, progress=False):
    owner = load_owner_engine()
    counts = Counter()
    samples = {}
    scanned = failures = 0
    kernels_by_chunk = []
    for path in paths:
        header, records, finish = owner.stream_chunk(path)
        kernels = {item["order_kernel"]: tuple(map(tuple, item["edges"]))
                   for item in header["kernels"]}
        kernels_by_chunk.append(len(kernels))
        for source in records:
            if limit is not None and scanned >= limit:
                break
            scanned += 1
            edges = kernels[source["order_kernel"]]
            row = tuple(source["row"])
            if len(edges) == PATH_COUNT:
                continue
            failures += 1
            signature = row_signature(edges, row)
            counts[signature] += 1
            key = row_key(source)
            current = samples.setdefault(signature, [])
            record = (key, source.copy(), edges)
            current.append(record)
            current.sort(key=lambda item: item[0])
            del current[representatives:]
        if limit is None or scanned < limit:
            finish()
        if progress:
            print(f"chunk={path.name} scanned={scanned} failures={failures}", flush=True)
        if limit is not None and scanned >= limit:
            break

    ranked = sorted(counts, key=lambda signature: (-counts[signature], signature))
    clusters = []
    checked = 0
    for signature in ranked:
        records = []
        for _, source, edges in samples[signature]:
            row = tuple(source["row"])
            result = {
                "global_kernel": source["global_kernel"],
                "order_kernel": source["order_kernel"],
                "row": source["row"],
                "orbit_size": source["orbit_size"],
                "embedding": numerical_embedding(edges, row),
            }
            if checked < verify_rows:
                result["polynomial_gram"] = search_direct(edges, row)
                result["rank6_edge_opening"] = search_edge_opening(edges, row)
                checked += 1
            records.append(result)
        clusters.append({"signature": signature_json(signature),
                         "orbit_count": counts[signature], "representatives": records})
    return {
        "schema": "rank-seven-order-twelve-three-ray-obstruction-mining-v1",
        "full_theorem": False,
        "scope": "exact obstruction signatures; numerical embeddings; exact DD Gram tests",
        "scanned_residual_orbits": scanned,
        "three_ray_failure_orbits": failures,
        "obstruction_signature_total": len(counts),
        "representatives_per_signature": representatives,
        "exact_candidate_rows_checked": checked,
        "coefficient_grid": "a,b in reduced rationals [-1,1] with denominator at most 6",
        "gram_family": "G_ii=1; G_uv=a*S_uv+b*(S^2)_uv",
        "clusters": clusters,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chunks", nargs="*", type=Path)
    parser.add_argument("--representatives", type=int, default=1)
    parser.add_argument("--verify-rows", type=int, default=64)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    require(args.representatives >= 1 and args.verify_rows >= 0, "invalid sample size")
    chunks = args.chunks or sorted(HERE.glob("rank7_order12_census_*.json.xz"))
    require(chunks, "no census chunks found")
    payload = mine(chunks, args.representatives, args.verify_rows, args.limit, args.progress)
    if args.limit is None:
        manifest = json.loads(MANIFEST_PATH.read_text("ascii"))
        require(payload["scanned_residual_orbits"] == manifest["coarse_residual_total"],
                "full scan count changed")
        require(payload["three_ray_failure_orbits"] ==
                manifest["structural_residual_orbit_total"], "failure count changed")
    encoded = canonical_bytes(payload)
    if args.output:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(encoded)
    print(f"scanned={payload['scanned_residual_orbits']} "
          f"failures={payload['three_ray_failure_orbits']} "
          f"signatures={payload['obstruction_signature_total']} "
          f"verified={payload['exact_candidate_rows_checked']} "
          f"sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
