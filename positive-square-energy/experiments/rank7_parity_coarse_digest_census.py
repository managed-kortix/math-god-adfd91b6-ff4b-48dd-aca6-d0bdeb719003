#!/usr/bin/env python3
"""Sparse exact/estimated parity-orbit census for rank-seven kernels.

Orders 2--6 are enumerated exactly.  Orders 7--12 use a deterministic
Burnside Monte Carlo estimate: rows fixed by each automorphism are sampled
uniformly, so the resulting sum estimates the number of residual orbits rather
than the number of labelled rows.  The compact artifact stores only ledgers and
stream digests, never the residual witnesses.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import multiprocessing
import random
from functools import partial
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
OUTPUT = HERE / "rank7_parity_coarse_digest_census.json"
SOURCE_SHA256 = "81078a70a46cda4f6f1c7b547c96603baff2b7a347413befafaa8410595de76d"
SCHEMA = "rank-seven-parity-coarse-digest-census-experiment-v1"
EXPECTED_KERNEL_COUNTS = (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365)
RANK = 7
COST_SCALE = 30
BUDGET_SCALED = COST_SCALE * (RANK - 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def stream_line(value):
    return canonical_bytes(value)


def sparse_kernel(n, dense):
    pairs = itertools.combinations(range(n), 2)
    return tuple((u, v, value) for (u, v), value in zip(pairs, dense) if value)


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-seven source changed")
    payload = json.loads(raw.decode("ascii"))
    require(tuple(payload["counts_by_order_n2_to_n12"]) == EXPECTED_KERNEL_COUNTS,
            "rank-seven kernel counts changed")
    records = []
    local = {order: 0 for order in range(2, 13)}
    for global_index, record in enumerate(payload["kernels"], 1):
        n = record["n"]
        local[n] += 1
        edges = sparse_kernel(n, record["code"])
        require(sum(edge[2] for edge in edges) == n + 6, "path count changed")
        records.append((global_index, local[n], n, edges))
    return tuple(records)


def automorphism_actions(n, edges):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((u, v, {"m": multiplicity}) for u, v, multiplicity in edges)
    edge_index = {(u, v): index for index, (u, v, _) in enumerate(edges)}
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph, graph, edge_match=nx.algorithms.isomorphism.categorical_edge_match("m", 0))
    actions = set()
    for mapping in matcher.isomorphisms_iter():
        actions.add(tuple(edge_index[tuple(sorted((mapping[u], mapping[v])))]
                          for u, v, _ in edges))
    require(actions, "automorphism group is empty")
    return tuple(sorted(actions))


def apply_action(row, action):
    return tuple(row[index] for index in action)


def is_coarse_residual(n, edges, row):
    """Decide whether every admissible tetrahedral coloring costs over six."""
    adjacency = [[] for _ in range(n)]
    for index, (u, v, multiplicity) in enumerate(edges):
        odd = row[index]
        weight = 18 * multiplicity + (10 - 13 * odd if odd else 0)
        adjacency[u].append((v, odd != 0, weight))
        adjacency[v].append((u, odd != 0, weight))
    order = sorted(range(n), key=lambda v: (-sum(required for _, required, _ in adjacency[v]),
                                             -len(adjacency[v]), v))
    colors = [-1] * n
    colors[order[0]] = 0

    def visit(position, used, cost):
        if cost > BUDGET_SCALED:
            return False
        if position == n:
            return True
        vertex = order[position]
        limit = min(used + 1, 4)
        for color in range(limit):
            added = 0
            valid = True
            for other, required, weight in adjacency[vertex]:
                other_color = colors[other]
                if other_color < 0:
                    continue
                if required and color == other_color:
                    valid = False
                    break
                if color != other_color:
                    added += weight
            if valid and cost + added <= BUDGET_SCALED:
                colors[vertex] = color
                if visit(position + 1, max(used, color + 1), cost + added):
                    colors[vertex] = -1
                    return True
                colors[vertex] = -1
        return False

    return not visit(1, 1, 0)


def action_cycles(action):
    seen = set()
    cycles = []
    for start in range(len(action)):
        if start in seen:
            continue
        cycle = []
        value = start
        while value not in seen:
            seen.add(value)
            cycle.append(value)
            value = action[value]
        cycles.append(tuple(cycle))
    return tuple(cycles)


def fixed_row_space(edges, action):
    multiplicities = tuple(edge[2] for edge in edges)
    cycles = action_cycles(action)
    require(all(len({multiplicities[index] for index in cycle}) == 1 for cycle in cycles),
            "automorphism does not preserve multiplicity")
    radices = tuple(multiplicities[cycle[0]] + 1 for cycle in cycles)
    return cycles, radices, math.prod(radices)


def row_from_cycle_values(length, cycles, values):
    row = [0] * length
    for cycle, value in zip(cycles, values):
        for index in cycle:
            row[index] = value
    return tuple(row)


def exact_kernel(item):
    global_index, local_index, n, edges = item
    actions = automorphism_actions(n, edges)
    orbit_sizes = {}
    for row in itertools.product(*(range(multiplicity + 1) for _, _, multiplicity in edges)):
        representative = min(apply_action(row, action) for action in actions)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
    orbit_digest = hashlib.sha256()
    residual_digest = hashlib.sha256()
    residuals = 0
    for row in sorted(orbit_sizes):
        orbit_digest.update(stream_line([global_index, list(row), orbit_sizes[row]]))
        if is_coarse_residual(n, edges, row):
            residuals += 1
            residual_digest.update(stream_line([global_index, list(row), orbit_sizes[row]]))
    return {
        "global_kernel": global_index,
        "order_kernel": local_index,
        "support_edges": len(edges),
        "automorphisms": len(actions),
        "physical_rows": sum(orbit_sizes.values()),
        "parity_orbits": len(orbit_sizes),
        "coarse_certified": len(orbit_sizes) - residuals,
        "coarse_residuals": residuals,
        "orbit_stream_sha256": orbit_digest.hexdigest(),
        "residual_stream_sha256": residual_digest.hexdigest(),
    }


def estimate_kernel(item, samples):
    global_index, local_index, n, edges = item
    actions = automorphism_actions(n, edges)
    estimate_sum = 0.0
    variance_sum = 0.0
    fixed_sum = 0
    for action_index, action in enumerate(actions):
        cycles, radices, fixed_total = fixed_row_space(edges, action)
        fixed_sum += fixed_total
        count = min(samples, fixed_total)
        rng = random.Random((global_index << 32) ^ (action_index << 16) ^ samples ^ 0xA7C0A25)
        hits = 0
        if count == fixed_total:
            values_iter = itertools.product(*(range(radix) for radix in radices))
        else:
            values_iter = (tuple(rng.randrange(radix) for radix in radices) for _ in range(count))
        for values in values_iter:
            row = row_from_cycle_values(len(edges), cycles, values)
            hits += is_coarse_residual(n, edges, row)
        probability = hits / count
        estimate_sum += fixed_total * probability
        if count < fixed_total and count > 1:
            variance_sum += fixed_total * fixed_total * probability * (1.0 - probability) / count
    group = len(actions)
    return {
        "global_kernel": global_index,
        "order_kernel": local_index,
        "support_edges": len(edges),
        "automorphisms": group,
        "parity_orbits": fixed_sum // group,
        "estimated_coarse_residuals": estimate_sum / group,
        "estimate_variance": variance_sum / (group * group),
    }


def map_jobs(function, items, jobs):
    if jobs == 1:
        return list(map(function, items))
    with multiprocessing.Pool(jobs) as pool:
        return list(pool.imap(function, items, chunksize=1))


def regenerate(jobs, samples):
    sources = source_kernels()
    sparse_digest = hashlib.sha256()
    for global_index, local_index, n, edges in sources:
        sparse_digest.update(stream_line([global_index, local_index, n, [list(edge) for edge in edges]]))
    exact_items = tuple(item for item in sources if item[2] <= 6)
    estimated_items = tuple(item for item in sources if item[2] >= 7)
    exact = map_jobs(exact_kernel, exact_items, jobs)
    estimated = map_jobs(partial(estimate_kernel, samples=samples), estimated_items, jobs)

    exact_orders = []
    exact_manifest = hashlib.sha256()
    for order in range(2, 7):
        rows = [row for row in exact if sources[row["global_kernel"] - 1][2] == order]
        for row in rows:
            exact_manifest.update(stream_line(row))
        exact_orders.append({
            "order": order,
            "kernels": len(rows),
            "physical_rows": sum(row["physical_rows"] for row in rows),
            "parity_orbits": sum(row["parity_orbits"] for row in rows),
            "coarse_certified": sum(row["coarse_certified"] for row in rows),
            "coarse_residuals": sum(row["coarse_residuals"] for row in rows),
        })
    estimates = []
    estimate_manifest = hashlib.sha256()
    for order in range(7, 13):
        rows = [row for row in estimated if sources[row["global_kernel"] - 1][2] == order]
        for row in rows:
            estimate_manifest.update(stream_line(row))
        point = sum(row["estimated_coarse_residuals"] for row in rows)
        standard_error = math.sqrt(sum(row["estimate_variance"] for row in rows))
        estimates.append({
            "order": order,
            "kernels": len(rows),
            "parity_orbits_exact": sum(row["parity_orbits"] for row in rows),
            "estimated_coarse_residuals": round(point),
            "monte_carlo_standard_error": round(standard_error),
            "approximate_95_percent_interval": [max(0, round(point - 1.96 * standard_error)),
                                                  round(point + 1.96 * standard_error)],
        })
    return {
        "schema": SCHEMA,
        "status": "orders-2-6-exact-orders-7-12-estimated-certificates-open",
        "full_theorem": False,
        "rank": RANK,
        "budget": [RANK - 1, 1],
        "cost_scale": COST_SCALE,
        "source_sha256": SOURCE_SHA256,
        "kernel_counts_n2_to_n12": list(EXPECTED_KERNEL_COUNTS),
        "sparse_encoding": "ordered nonzero triples [u,v,multiplicity]",
        "sparse_source_stream_sha256": sparse_digest.hexdigest(),
        "exact_orders": exact_orders,
        "estimated_orders": estimates,
        "estimate_samples_per_automorphism": samples,
        "estimator": "deterministic uniform fixed-row sampling inside Burnside sum",
        "exact_kernel_manifest_sha256": exact_manifest.hexdigest(),
        "estimate_kernel_manifest_sha256": estimate_manifest.hexdigest(),
    }


def verify(payload):
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False,
            "artifact type changed")
    require(payload["kernel_counts_n2_to_n12"] == list(EXPECTED_KERNEL_COUNTS),
            "kernel scope changed")
    require([row["order"] for row in payload["exact_orders"]] == list(range(2, 7)),
            "exact order scope changed")
    require([row["order"] for row in payload["estimated_orders"]] == list(range(7, 13)),
            "estimate order scope changed")
    for row in payload["exact_orders"]:
        require(row["coarse_certified"] + row["coarse_residuals"] == row["parity_orbits"],
                "exact coarse partition failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    require(args.jobs >= 1 and args.samples >= 2, "jobs and samples must be positive")
    if args.verify:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), "artifact is not canonical JSON")
    else:
        payload = regenerate(args.jobs, args.samples)
        require(args.output.parent.is_dir(), "output parent is missing")
        args.output.write_bytes(canonical_bytes(payload))
    verify(payload)
    for row in payload["exact_orders"]:
        print(f"n={row['order']} exact orbits={row['parity_orbits']} residuals={row['coarse_residuals']}")
    for row in payload["estimated_orders"]:
        print(f"n={row['order']} estimate orbits={row['parity_orbits_exact']} "
              f"residuals={row['estimated_coarse_residuals']}+/-{row['monte_carlo_standard_error']}")
    print("artifact_sha256=" + hashlib.sha256(canonical_bytes(payload)).hexdigest())
    print("full_theorem=false")


if __name__ == "__main__":
    main()
