#!/usr/bin/env python3
"""Exact physical-incidence cut/cycle Gram pilot for the order-ten remainder."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from functools import lru_cache
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rank7_order10_near_cubic_gram_lane.py"
OUTPUT = HERE / "rank7_order10_cycle_cut_gram_lane.json"
SCHEMA = "rank-seven-order-ten-cycle-cut-gram-lane-v1"
F = Fraction
ORDER = 10
BUDGET = F(6)
WEIGHT_RATIOS = (F(0), F(1, 16), F(1, 8), F(1, 4), F(1, 2), F(1),
                 F(2), F(4), F(8), F(16))
PARAMETERS = tuple((F(1), ratio, F(2, 3)) for ratio in WEIGHT_RATIOS)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_source():
    spec = importlib.util.spec_from_file_location("rank7_order10_cycle_cut_source", SOURCE)
    require(spec is not None and spec.loader is not None, "cannot load source lane")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def physical_paths(edges, row):
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, u, v, length) for length in lengths)
    require(len(paths) == 16, "physical path count changed")
    return paths


def spanning_tree_columns(paths):
    parent = list(range(ORDER))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    tree = []
    for column, (_, u, v, _) in enumerate(paths):
        left, right = root(u), root(v)
        if left != right:
            parent[left] = right
            tree.append(column)
    require(len(tree) == ORDER - 1, "physical support is disconnected")
    return tuple(tree)


def cycle_basis(paths):
    """Return the canonical fundamental-cycle basis as edge-coordinate columns."""
    tree = spanning_tree_columns(paths)
    tree_set = set(tree)
    adjacency = [[] for _ in range(ORDER)]
    for column in tree:
        _, u, v, _ = paths[column]
        adjacency[u].append((v, column, 1))
        adjacency[v].append((u, column, -1))
    basis = []
    for chord in range(len(paths)):
        if chord in tree_set:
            continue
        _, start, finish, _ = paths[chord]
        previous = {finish: None}
        todo = [finish]
        for vertex in todo:
            if vertex == start:
                break
            for neighbor, column, sign in adjacency[vertex]:
                if neighbor not in previous:
                    previous[neighbor] = (vertex, column, sign)
                    todo.append(neighbor)
        require(start in previous, "tree path disappeared")
        vector = [0] * len(paths)
        vector[chord] = 1
        vertex = start
        while vertex != finish:
            next_vertex, column, sign = previous[vertex]
            vector[column] = -sign
            vertex = next_vertex
        basis.append(tuple(vector))
    require(len(basis) == 7, "rank-seven cycle basis changed")
    return tuple(basis)


def inverse(matrix):
    """Invert a nonsingular rational matrix by exact Gauss-Jordan elimination."""
    size = len(matrix)
    work = [[F(value) for value in row] +
            [F(i == j) for j in range(size)]
            for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        require(pivot is not None, "singular reduced Laplacian")
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [value / divisor for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [left - multiplier * right
                         for left, right in zip(work[row], work[column])]
    return tuple(tuple(row[size:]) for row in work)


@lru_cache(maxsize=None)
def cut_metric(endpoints):
    """Return B^T(BB^T)^-1 B for the reduced physical incidence matrix B."""
    columns = len(endpoints)
    incidence = [[F() for _ in range(columns)] for _ in range(ORDER - 1)]
    for column, (u, v) in enumerate(endpoints):
        if u < ORDER - 1:
            incidence[u][column] = 1
        if v < ORDER - 1:
            incidence[v][column] = -1
    laplacian = [[sum(incidence[u][edge] * incidence[v][edge]
                       for edge in range(columns))
                  for v in range(ORDER - 1)] for u in range(ORDER - 1)]
    laplacian_inverse = inverse(laplacian)
    projector = [[F() for _ in range(columns)] for _ in range(columns)]
    for left in range(columns):
        for right in range(columns):
            projector[left][right] = sum(
                incidence[u][left] * laplacian_inverse[u][v] * incidence[v][right]
                for u in range(ORDER - 1) for v in range(ORDER - 1))
    return tuple(tuple(row) for row in projector)


def embedding_components(edges, row):
    paths = physical_paths(edges, row)
    endpoints = tuple((u, v) for _, u, v, _ in paths)
    cut_projector = cut_metric(endpoints)
    signed_incidence = [[F() for _ in paths] for _ in range(ORDER)]
    for column, (_, u, v, length) in enumerate(paths):
        signed_incidence[u][column] = 1
        signed_incidence[v][column] = -1 if length & 1 else 1
    cut_vectors = [[sum(signed_incidence[u][left] * cut_projector[left][right]
                        for left in range(len(paths)))
                    for right in range(len(paths))] for u in range(ORDER)]
    cycle_vectors = [[signed_incidence[u][column] - cut_vectors[u][column]
                      for column in range(len(paths))] for u in range(ORDER)]
    cut_core = [[F() for _ in range(ORDER)] for _ in range(ORDER)]
    cycle_core = [[F() for _ in range(ORDER)] for _ in range(ORDER)]
    for u in range(ORDER):
        for v in range(u, ORDER):
            cut_value = sum(x * y for x, y in zip(cut_vectors[u], cut_vectors[v]))
            cycle_value = sum(x * y for x, y in zip(cycle_vectors[u], cycle_vectors[v]))
            cut_core[u][v] = cut_core[v][u] = cut_value
            cycle_core[u][v] = cycle_core[v][u] = cycle_value
    return cut_core, cycle_core, paths


def gram_from_components(cut_core, cycle_core, degrees, cut_weight, cycle_weight,
                         defect_scale):
    """Build D A(a P_cut+b P_cycle)A^T D and complete its diagonal."""
    scales = [F(1) if degree == 3 else defect_scale for degree in degrees]
    core = [[scales[u] * scales[v] *
             (cut_weight * cut_core[u][v] + cycle_weight * cycle_core[u][v])
             for v in range(ORDER)] for u in range(ORDER)]
    normalizer = max(F(1), *(core[u][u] for u in range(ORDER)))
    gram = [[core[u][v] / normalizer for v in range(ORDER)] for u in range(ORDER)]
    for u in range(ORDER):
        gram[u][u] = F(1)
    return gram, normalizer


def embedding_gram(edges, degrees, row, cut_weight, cycle_weight, defect_scale):
    cut_core, cycle_core, paths = embedding_components(edges, row)
    gram, normalizer = gram_from_components(
        cut_core, cycle_core, degrees, cut_weight, cycle_weight, defect_scale)
    return gram, paths, normalizer


def gram_cost(gram, paths):
    total = F()
    for _, u, v, length in paths:
        transformed = -gram[u][v] if length & 1 else gram[u][v]
        if not -1 < transformed <= 1:
            return None
        total += (1 - transformed) / (length * (1 + transformed))
    return total


def search(edges, degrees, row):
    best = None
    cut_core, cycle_core, paths = embedding_components(edges, row)
    for parameters in PARAMETERS:
        gram, normalizer = gram_from_components(cut_core, cycle_core, degrees, *parameters)
        cost = gram_cost(gram, paths)
        if cost is not None and (best is None or cost < best[0]):
            best = cost, parameters, normalizer
    return best


def pair(value):
    return [value.numerator, value.denominator]


def scan(sample_size=10000, progress=False, representative_stride=1):
    source = load_source()
    manifest, manifest_sha256 = source.strict_json(source.MANIFEST)
    kernels = source.kernel_dictionary()
    records = []
    tested = owned = 0
    degree_counts = {}
    visited = 0
    for index, record in enumerate(source.remainder_records(manifest)):
        if index % representative_stride:
            continue
        if tested >= sample_size:
            break
        visited = index + 1
        source_index, global_kernel, order_kernel, raw_row, _ = record
        kernel = kernels[order_kernel]
        witness = search(kernel["edges"], kernel["degrees"], tuple(raw_row))
        require(witness is not None, "all exact parameters were singular")
        cost, parameters, normalizer = witness
        partition = "5" if kernel["degree_partition"][0] == 5 else "4+4"
        degree_counts.setdefault(partition, {"tested": 0, "owned": 0})
        degree_counts[partition]["tested"] += 1
        degree_counts[partition]["owned"] += cost <= BUDGET
        tested += 1
        owned += cost <= BUDGET
        records.append({
            "source_index": source_index,
            "global_kernel": global_kernel,
            "degree_pattern": partition,
            "cost": pair(cost),
            "owned": cost <= BUDGET,
            "parameters": [pair(value) for value in parameters],
            "normalizer": pair(normalizer),
        })
        if progress and tested % 1000 == 0:
            print(f"tested={tested} owned={owned}", flush=True)
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "deterministic representatives of the authenticated exact structural remainder",
        "owner_manifest_sha256": manifest_sha256,
        "sampling": {"requested": sample_size, "start": 0, "source_stop": visited,
                     "representative_stride": representative_stride, "tested": tested},
        "family": {
            "formula": "G=H/M+diag(1-diag(H)/M), H=DA(a P_cut+b P_cycle)A^T D",
            "signed_incidence": "A has entries 1 at the first endpoint and (-1)^L at the second endpoint of each physical path",
            "cut_projector": "P_cut=B^T(BB^T)^-1B for reduced oriented physical incidence B",
            "cycle_projector": "P_cycle=I-P_cut=Z(Z^TZ)^-1Z^T for any fundamental cycle basis Z",
            "psd_proof": "P_cut and P_cycle are orthogonal rational projectors; H is the sum of the Gram squares a(DA P_cut)(DA P_cut)^T and b(DA P_cycle)(DA P_cycle)^T; M dominates its diagonal and the completion is a sum of nonnegative coordinate squares",
            "parameter_order": ["cut_weight", "cycle_weight", "defect_scale"],
            "parameters": [[pair(value) for value in row] for row in PARAMETERS],
        },
        "result": {
            "owned": owned,
            "failed": tested - owned,
            "degree_pattern_counts": degree_counts,
            "minimum_cost": pair(min(F(*record["cost"]) for record in records)),
            "obstruction": "no sampled representative reaches the exact budget" if not owned else None,
        },
        "records": records,
        "claim_boundary": "PSD and each displayed cost are exact; failure applies to this finite basis-weight family and sampled records, not to all cycle/cut Grams",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=10000)
    parser.add_argument("--representative-stride", type=int, default=1)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.sample_size > 0, "sample size must be positive")
    require(args.representative_stride > 0, "representative stride must be positive")
    report = scan(args.sample_size, args.progress, args.representative_stride)
    raw = canonical_bytes(report)
    if args.audit:
        require(args.output.read_bytes() == raw, "report does not reproduce")
    else:
        args.output.write_bytes(raw)
    print(f"tested={report['sampling']['tested']} owned={report['result']['owned']} "
          f"minimum={report['result']['minimum_cost']}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
