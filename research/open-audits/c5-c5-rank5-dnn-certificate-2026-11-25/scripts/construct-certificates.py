#!/usr/bin/env python3
"""Construct exact rational elliptope witnesses after a numerical scout.

The emitted JSON contains the authoritative exact objects.  Floating-point
optimization is used only to find nearby unit vectors; every conclusion is
rechecked with fractions before it is written.  The dependency-free verifier
is the trust boundary.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ATLAS = ROOT / "sources" / "networkx-3.7-atlas.dat.gz"
ENUM = ROOT / "data" / "atlas-rank5-enumeration.json"
CERT = ROOT / "data" / "atlas-rank5-rational-gram-certificates.json"
WITNESS = ROOT / "data" / "n8-multiblock-route-witness.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_atlas(path: Path):
    graphs = []
    with gzip.open(path, "rt", encoding="ascii", newline="") as f:
        lines = iter(f)
        pending = None
        while True:
            try:
                line = pending if pending is not None else next(lines)
                pending = None
            except StopIteration:
                break
            require(line.startswith("GRAPH "), "malformed Atlas GRAPH line")
            index = int(line.split()[1])
            node_line = next(lines)
            require(node_line.startswith("NODES "), "malformed Atlas NODES line")
            n = int(node_line.split()[1])
            edges = []
            for line in lines:
                if line.startswith("GRAPH "):
                    pending = line
                    break
                a, b = map(int, line.split())
                edges.append((min(a, b), max(a, b)))
            graphs.append((index, n, tuple(sorted(edges))))
            if pending is None:
                break
    return graphs


def adjacency(n, edges, skip_vertex=None, skip_edge=None):
    adj = [[] for _ in range(n)]
    for k, (u, v) in enumerate(edges):
        if k == skip_edge or u == skip_vertex or v == skip_vertex:
            continue
        adj[u].append(v)
        adj[v].append(u)
    return adj


def connected(n, edges, skip_vertex=None, skip_edge=None):
    vertices = [v for v in range(n) if v != skip_vertex]
    if not vertices:
        return True
    adj = adjacency(n, edges, skip_vertex, skip_edge)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(vertices)


def bridges(n, edges):
    return [edges[k] for k in range(len(edges)) if not connected(n, edges, skip_edge=k)]


def articulations(n, edges):
    if n <= 2:
        return []
    return [v for v in range(n) if not connected(n, edges, skip_vertex=v)]


def biconnected_edge_blocks(n, edges):
    """Tarjan edge blocks, including one-edge bridge blocks."""
    adj = [[] for _ in range(n)]
    for k, (u, v) in enumerate(edges):
        adj[u].append((v, k))
        adj[v].append((u, k))
    disc = [-1] * n
    low = [0] * n
    parent_edge = [-1] * n
    edge_stack = []
    blocks = []
    clock = 0

    def dfs(u):
        nonlocal clock
        disc[u] = low[u] = clock
        clock += 1
        for v, eid in adj[u]:
            if eid == parent_edge[u]:
                continue
            if disc[v] == -1:
                parent_edge[v] = eid
                edge_stack.append(eid)
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    block = []
                    while True:
                        z = edge_stack.pop()
                        block.append(z)
                        if z == eid:
                            break
                    blocks.append(tuple(sorted(block)))
            elif disc[v] < disc[u]:
                edge_stack.append(eid)
                low[u] = min(low[u], disc[v])

    for root in range(n):
        if disc[root] == -1:
            dfs(root)
            require(not edge_stack, "Tarjan edge stack not empty")
    return blocks


def block_record(edges, ids):
    block_edges = [edges[k] for k in ids]
    vertices = sorted({x for e in block_edges for x in e})
    return {
        "vertices": vertices,
        "edges": [list(e) for e in block_edges],
        "rank": len(block_edges) - len(vertices) + 1,
    }


def graph6_encode(n, edges):
    require(0 <= n <= 62, "only short graph6 is supported")
    eset = set(edges)
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (i, j) in eset else 0)
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(n + 63)]
    for k in range(0, len(bits), 6):
        value = 0
        for bit in bits[k:k + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def fstr(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def objective_gradient(x, n, edges):
    X = x.reshape(n, n)
    norms = np.linalg.norm(X, axis=1)
    V = X / norms[:, None]
    grad_v = np.zeros_like(V)
    objective = 0.0
    for u, v in edges:
        rho = V[u] @ V[v]
        denominator = 1.0 - rho
        objective += 2.0 / denominator
        coefficient = 2.0 / denominator**2
        grad_v[u] += coefficient * V[v]
        grad_v[v] += coefficient * V[u]
    grad_x = (grad_v - (grad_v * V).sum(axis=1)[:, None] * V) / norms[:, None]
    return objective, grad_x.ravel()


def numerical_scout(n, edges, restarts=15):
    best = None
    for restart in range(restarts):
        seed = 991 * n + 103 * len(edges) + 7919 * restart
        initial = np.random.default_rng(seed).normal(size=n * n)
        result = minimize(
            lambda x: objective_gradient(x, n, edges),
            initial,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": 5000, "ftol": 1e-14, "gtol": 1e-9,
                     "maxls": 100},
        )
        if best is None or result.fun < best.fun:
            best = result
    require(best is not None, "optimizer produced no result")
    return best.x.reshape(n, n)


def rational_unit_vectors(X, denominator):
    n = X.shape[0]
    V = X / np.linalg.norm(X, axis=1)[:, None]
    for rotation_seed in range(100):
        Qf, _ = np.linalg.qr(np.random.default_rng(6173 + rotation_seed).normal(size=(n, n)))
        W = V @ Qf
        if np.min(1.0 + W[:, 0]) > 0.25:
            break
    else:
        raise RuntimeError("no safe stereographic pole")
    vectors = []
    parameters = []
    for w in W:
        ints = [int(round(float(a) * denominator)) for a in w[1:] / (1.0 + w[0])]
        t = [Q(a, denominator) for a in ints]
        ss = sum((a * a for a in t), Q(0))
        d = 1 + ss
        vector = [(1 - ss) / d] + [2 * a / d for a in t]
        require(sum((a * a for a in vector), Q(0)) == 1,
                "stereographic vector is not exactly unit")
        vectors.append(vector)
        parameters.append(ints)
    return vectors, parameters, rotation_seed


def gram(vectors):
    return [[sum((a * b for a, b in zip(row_i, row_j)), Q(0))
             for row_j in vectors] for row_i in vectors]


def exact_edge_data(edges, R):
    terms = []
    total = Q(0)
    for u, v in edges:
        rho = R[u][v]
        require(rho < 1, "edge correlation is not below one")
        cost = Q(2) / (1 - rho)
        terms.append({"edge": [u, v], "correlation": fstr(rho), "cost": fstr(cost)})
        total += cost
    return terms, total


def enumeration_record(index, n, edges):
    blocks = [block_record(edges, ids) for ids in biconnected_edge_blocks(n, edges)]
    positive = [b for b in blocks if b["rank"] > 0]
    br = bridges(n, edges)
    return {
        "atlas_index": index,
        "n": n,
        "m": len(edges),
        "graph6": graph6_encode(n, edges),
        "edges": [list(e) for e in edges],
        "bridges": [list(e) for e in br],
        "articulation_vertices": articulations(n, edges),
        "block_rank_profile": sorted((b["rank"] for b in blocks), reverse=True),
        "positive_rank_block_count": len(positive),
        "positive_rank_profile": sorted((b["rank"] for b in positive), reverse=True),
        "selected_bridge_free_core": not br,
        "single_positive_rank_block": len(positive) == 1,
        "bridge_free_core_graph6": graph6_encode(n, edges) if not br else None,
    }


def construct_enumeration(graphs):
    relevant = []
    for index, n, edges in graphs:
        if n and connected(n, edges) and len(edges) - n + 1 == 5:
            relevant.append(enumeration_record(index, n, edges))
    selected = [r for r in relevant if r["selected_bridge_free_core"]]
    single = [r for r in selected if r["single_positive_rank_block"]]
    multi = [r for r in selected if not r["single_positive_rank_block"]]
    require(len(graphs) == 1253, "unexpected Atlas graph count")
    require(len(relevant) == 153, "unexpected connected rank-five count")
    require(len(selected) == 102, "unexpected bridge-free count")
    require(len(single) == 95 and len(multi) == 7, "unexpected block-scope counts")
    graph6_source = [
        {
            "ordinal": ordinal,
            "atlas_index": r["atlas_index"],
            "graph6": r["graph6"],
        }
        for ordinal, r in enumerate(selected)
    ]
    return {
        "schema": "graph-atlas-rank5-enumeration-v1",
        "source": {
            "name": "NetworkX 3.7 atlas.dat.gz (Read-Wilson Graph Atlas data)",
            "relative_path": "../sources/networkx-3.7-atlas.dat.gz",
            "sha256": sha256(ATLAS),
            "graph_count": len(graphs),
            "maximum_order": max(n for _, n, _ in graphs),
            "exhaustiveness_assumption": "standard Graph Atlas exhaustiveness through order 7",
        },
        "filter": "simple connected beta=5; certificates select bridge-free cores",
        "selected_graph6_source_enumeration": graph6_source,
        "counts": {
            "connected_rank5": len(relevant),
            "bridge_free_rank5": len(selected),
            "bridge_bearing_rank5": len(relevant) - len(selected),
            "selected_single_positive_rank_block": len(single),
            "selected_multiblock": len(multi),
        },
        "records": relevant,
    }


def construct_certificates(enumeration):
    selected = [r for r in enumeration["records"] if r["selected_bridge_free_core"]]
    records = []
    for ordinal, source in enumerate(selected):
        n = source["n"]
        edges = [tuple(e) for e in source["edges"]]
        X = numerical_scout(n, edges)
        chosen = None
        for denominator in (2000, 10000, 100000):
            vectors, parameters, rotation_seed = rational_unit_vectors(X, denominator)
            R = gram(vectors)
            edge_terms, cost = exact_edge_data(edges, R)
            excess = cost - len(edges)
            if excess + 4 > 0:
                p, q = excess.numerator, excess.denominator
                slack = 80 * q * q - (p + 4 * q) ** 2
                if slack > 0:
                    chosen = (denominator, vectors, parameters, rotation_seed,
                              R, edge_terms, cost, excess, slack)
                    break
        require(chosen is not None, f"no exact threshold certificate for {source['graph6']}")
        (denominator, vectors, parameters, rotation_seed, R, edge_terms,
         cost, excess, slack) = chosen
        records.append({
            "ordinal": ordinal,
            "atlas_index": source["atlas_index"],
            "graph6": source["graph6"],
            "n": n,
            "m": len(edges),
            "edges": [list(e) for e in edges],
            "single_positive_rank_block": source["single_positive_rank_block"],
            "positive_rank_profile": source["positive_rank_profile"],
            "construction": {
                "method": "numerical elliptope scout then exact rational stereographic projection",
                "stereographic_parameter_denominator": denominator,
                "rotation_seed_offset": rotation_seed,
                "integer_stereographic_parameters": parameters,
            },
            "rational_unit_vectors": [[fstr(x) for x in row] for row in vectors],
            "rational_gram_matrix": [[fstr(x) for x in row] for row in R],
            "psd_certificate": "R=U*U^T over Q; each row of U has exact squared norm 1",
            "edge_terms": edge_terms,
            "edge_cost": fstr(cost),
            "edge_cost_minus_m": fstr(excess),
            "radical_test": {
                "claim": "edge_cost_minus_m < 4*sqrt(5)-4",
                "equivalent_positive_quantity_test": "(edge_cost_minus_m+4)^2 < 80",
                "integer_slack": str(slack),
            },
        })
    require(len(records) == 102, "certificate count changed")
    return {
        "schema": "rank5-c5-c5-rational-elliptope-certificates-v1",
        "claim": "For each listed bridge-free rank-five core C, kappa(C)-m(C) < 4*sqrt(5)-4.",
        "logic": "A listed feasible correlation matrix R gives kappa(C) <= sum_edges 2/(1-R_uv).",
        "arithmetic": "All matrices, costs, and radical tests are exact rational/integer data.",
        "counts": {
            "total": len(records),
            "single_positive_rank_block": sum(r["single_positive_rank_block"] for r in records),
            "multiblock": sum(not r["single_positive_rank_block"] for r in records),
        },
        "records": records,
    }


def graph6_decode(code):
    n = ord(code[0]) - 63
    bits = []
    for ch in code[1:]:
        value = ord(ch) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, tuple(edges)


def attach_two_c5(center_n, center_edges, ports):
    edges = list(center_edges)
    n = center_n
    cycle_vertices = []
    bridge_edges = []
    for port in ports:
        cyc = list(range(n, n + 5))
        n += 5
        bridge_edges.append((port, cyc[0]))
        edges.append((port, cyc[0]))
        edges.extend((min(cyc[i], cyc[(i + 1) % 5]), max(cyc[i], cyc[(i + 1) % 5]))
                     for i in range(5))
        cycle_vertices.append(cyc)
    return n, tuple(sorted(edges)), bridge_edges, cycle_vertices


def construct_witness():
    center_code = "GXgrBC"
    n, edges = graph6_decode(center_code)
    require(n == 8 and len(edges) == 12, "n=8 center encoding changed")
    blocks = [block_record(edges, ids) for ids in biconnected_edge_blocks(n, edges)]
    blocks.sort(key=lambda b: (-b["rank"], b["vertices"]))
    expected_vertices = [[1, 2, 6, 7], [0, 2, 4], [2, 3, 5]]
    require([b["vertices"] for b in blocks] == expected_vertices,
            "witness block decomposition changed")
    full_n, full_edges, bridge_edges, cycles = attach_two_c5(n, edges, (2, 2))
    return {
        "schema": "rank5-c5-c5-n8-route-witness-v1",
        "claim_boundary": "Exact obstruction to the universal all-center DNN threshold only; not a graph counterexample.",
        "center": {
            "description": "K4 one-vertex-summed with two C3 blocks at the same cut vertex",
            "graph6": center_code,
            "n": n,
            "m": len(edges),
            "beta": len(edges) - n + 1,
            "edges": [list(e) for e in edges],
            "blocks": blocks,
            "kappa_blocks": [
                {"type": "K4", "m": 6, "kappa": 9, "excess": 3},
                {"type": "C3", "m": 3, "kappa": 4, "excess": 1},
                {"type": "C3", "m": 3, "kappa": 4, "excess": 1},
            ],
            "kappa": 17,
            "kappa_minus_m": 5,
        },
        "local_exact_kappa_certificates": {
            "K4": {
                "primal": "M=J_4 gives objective 9",
                "dual_correlation": [["1" if i == j else "-1/3" for j in range(4)] for i in range(4)],
                "dual_edge_cost": "9",
            },
            "C3": {
                "primal": "M=J_3 gives objective 4",
                "dual_correlation": [["1" if i == j else "-1/2" for j in range(3)] for i in range(3)],
                "dual_edge_cost": "4",
            },
        },
        "center_threshold_test": {
            "required": "kappa(C)-m(C) <= 4*sqrt(5)-4",
            "actual": "5",
            "positive_gap": "9-4*sqrt(5)",
            "integer_sign_test": "9^2-(4^2*5)=1>0",
        },
        "repeated_port_representative": {
            "ports": [2, 2],
            "graph6": graph6_encode(full_n, full_edges),
            "n": full_n,
            "m": len(full_edges),
            "beta": len(full_edges) - full_n + 1,
            "edges": [list(e) for e in full_edges],
            "bridge_edges": [list(e) for e in bridge_edges],
            "cycle_vertices": cycles,
            "exact_kappa": "39-4*sqrt(5)",
            "dnn_target_cap": "m+6=30",
            "route_gap": "9-4*sqrt(5)>0",
        },
        "port_invariance": "For any two center ports, including equal ports, the block multiset is K4,C3,C3,K2,C5,K2,C5; exact kappa block additivity gives the same route gap.",
    }


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    graphs = parse_atlas(ATLAS)
    enumeration = construct_enumeration(graphs)
    dump(ENUM, enumeration)
    certificates = construct_certificates(enumeration)
    dump(CERT, certificates)
    dump(WITNESS, construct_witness())
    print("constructed 102 exact rational Gram certificates")
    print("construction scout uses floats; scripts/verify-certificates.py does not")


if __name__ == "__main__":
    main()
