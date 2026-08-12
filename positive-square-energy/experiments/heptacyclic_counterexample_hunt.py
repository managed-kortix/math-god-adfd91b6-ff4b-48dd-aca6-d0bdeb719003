#!/usr/bin/env python3
"""Reproduce the small-order heptacyclic search and exact low-tail certificate.

Scouting uses eigvalsh only to rank a complete nauty-geng stream.  The audit
mode, which produces the accepted artifact, uses integer characteristic
polynomials and rational Sturm intervals only.
"""

from __future__ import annotations

import argparse
import heapq
import json
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

from search_geng import graph6_adjacency


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "data" / "heptacyclic-low-surplus-exact.json"
SCHEMA = "heptacyclic-low-surplus-exact-v1"
MINIMIZERS = {
    6: "E]~o",
    7: "FFzf_",
    8: "G?zVf_",
    9: "H?bF`xw",
    10: "I?`DF`YN?",
    11: "J?`DA`gNCh?",
}
EXPECTED_COUNTS = {
    6: 5,
    7: 95,
    8: 1579,
    9: 20303,
    10: 211866,
    11: 1870168,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rational_text(value: sp.Rational) -> str:
    value = sp.Rational(value)
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def graph(g6: str) -> nx.Graph:
    return nx.from_numpy_array(graph6_adjacency(g6.encode("ascii")).astype(int))


def scout(order: int, keep: int) -> tuple[int, list[str]]:
    process = subprocess.Popen(
        ["nauty-geng", "-cq", str(order), f"{order + 6}:{order + 6}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(process.stdout is not None, "geng stdout unavailable")
    tail: list[tuple[float, str]] = []
    count = 0
    for raw in process.stdout:
        code = raw.decode("ascii").strip()
        adjacency = graph6_adjacency(raw)
        eigenvalues = np.linalg.eigvalsh(adjacency)
        positive = eigenvalues[eigenvalues > 1e-9]
        slack = float(np.dot(positive, positive) - order)
        item = (-slack, code)
        if len(tail) < keep:
            heapq.heappush(tail, item)
        elif item > tail[0]:
            heapq.heapreplace(tail, item)
        count += 1
    stderr = process.stderr.read().decode("ascii") if process.stderr else ""
    require(process.wait() == 0, f"geng failed: {stderr}")
    return count, [code for _, code in sorted(tail, key=lambda row: -row[0])]


def suppress_degree_two(source: nx.Graph) -> dict:
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(source.nodes())
    for u, v in source.edges():
        multigraph.add_edge(u, v, length=1)
    while True:
        vertex = next((v for v, degree in multigraph.degree() if degree == 2), None)
        if vertex is None:
            break
        incident = list(multigraph.edges(vertex, keys=True, data=True))
        require(len(incident) == 2, "unexpected degree-two incidence")
        ends = []
        lengths = []
        for u, v, _, data in incident:
            ends.append(v if u == vertex else u)
            lengths.append(data["length"])
        require(ends[0] != ends[1], "suppression created a loop")
        multigraph.remove_node(vertex)
        multigraph.add_edge(ends[0], ends[1], length=sum(lengths))
    vertices = sorted(multigraph.nodes())
    relabel = {vertex: index for index, vertex in enumerate(vertices)}
    paths = sorted(
        (min(relabel[u], relabel[v]), max(relabel[u], relabel[v]), data["length"])
        for u, v, data in multigraph.edges(data=True)
    )
    multiplicities = Counter((u, v) for u, v, _ in paths)
    return {
        "order": len(vertices),
        "degrees": sorted((degree for _, degree in multigraph.degree()), reverse=True),
        "edge_multiplicities": [
            [u, v, multiplicities[(u, v)]] for u, v in sorted(multiplicities)
        ],
        "subdivision_paths": [list(path) for path in paths],
    }


def exact_record(order: int, g6: str) -> dict:
    source = graph(g6)
    require(nx.is_connected(source), "candidate is disconnected")
    require(nx.is_biconnected(source), "candidate is not one block")
    require(source.number_of_edges() - source.number_of_nodes() + 1 == 7,
            "candidate is not heptacyclic")
    adjacency = sp.Matrix(nx.to_numpy_array(source, dtype=int))
    x = sp.symbols("x")
    polynomial = sp.Poly(adjacency.charpoly(x).as_expr(), x)
    lower = sp.Rational(-order)
    upper = sp.Rational(-order)
    positive_intervals = []
    for (left, right), multiplicity in polynomial.intervals(eps=sp.Rational(1, 10**6)):
        if right <= 0:
            continue
        require(left > 0, "Sturm interval straddles zero")
        lower += multiplicity * left**2
        upper += multiplicity * right**2
        positive_intervals.append(
            [rational_text(left), rational_text(right), multiplicity]
        )
    require(positive_intervals, "no positive Sturm intervals found")
    require(lower > 0, "nonpositive exact lower surplus bound")
    return {
        "order": order,
        "size": source.number_of_edges(),
        "graph6": g6,
        "degree_sequence": sorted((degree for _, degree in source.degree()), reverse=True),
        "one_rank_seven_block": True,
        "characteristic_polynomial": str(sp.factor(polynomial.as_expr())).replace("**", "^"),
        "positive_root_intervals": positive_intervals,
        "surplus_interval": [rational_text(lower), rational_text(upper)],
        "suppressed_kernel": suppress_degree_two(source),
    }


def payload() -> dict:
    return {
        "schema": SCHEMA,
        "claim_scope": "complete connected simple graph census at each listed order",
        "cyclomatic_rank": 7,
        "accepted_arithmetic": "integer characteristic polynomials and rational Sturm intervals",
        "scout_counts": {str(order): EXPECTED_COUNTS[order] for order in sorted(EXPECTED_COUNTS)},
        "hardest_records": [exact_record(order, MINIMIZERS[order]) for order in sorted(MINIMIZERS)],
    }


def canonical_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def audit() -> None:
    expected = payload()
    raw = canonical_bytes(expected)
    if OUTPUT.exists():
        require(OUTPUT.read_bytes() == raw, "persisted exact artifact changed")
    else:
        OUTPUT.write_bytes(raw)
    print(f"PASS {SCHEMA}")
    print(f"orders={','.join(map(str, sorted(MINIMIZERS)))}")
    print("counterexamples=0")
    for record in expected["hardest_records"]:
        print(f"n={record['order']} graph6={record['graph6']} surplus_lower={record['surplus_interval'][0]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scout", type=int, metavar="N")
    parser.add_argument("--keep", type=int, default=20)
    args = parser.parse_args()
    if args.scout is None:
        audit()
        return
    require(args.scout in EXPECTED_COUNTS, "supported scout orders are 6 through 11")
    count, tail = scout(args.scout, args.keep)
    require(count == EXPECTED_COUNTS[args.scout], "geng census count changed")
    require(tail[0] == MINIMIZERS[args.scout], "scouted minimizer changed")
    print(f"PASS scout n={args.scout} count={count}")
    print("\n".join(tail))


if __name__ == "__main__":
    main()
