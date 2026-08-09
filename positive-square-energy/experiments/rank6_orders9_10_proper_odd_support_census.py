#!/usr/bin/env python3
"""Exact support-side census for proper odd-cycle DNN stress candidates."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
OUTPUT = HERE / "rank6_orders9_10_proper_odd_support_census.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fixture():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256,
            "kernel fixture changed")
    return json.loads(raw.decode("ascii"))["kernels"]


def root(parent, vertex):
    while parent[vertex] != vertex:
        parent[vertex] = parent[parent[vertex]]
        vertex = parent[vertex]
    return vertex


def has_cycle_length(graph, length):
    """Test for a simple undirected cycle of the specified length."""
    for start in graph:
        stack = [(start, (start,), frozenset((start,)))]
        while stack:
            vertex, path, used = stack.pop()
            if len(path) == length:
                if start in graph[vertex]:
                    return True
                continue
            for neighbor in graph[vertex]:
                if neighbor > start and neighbor not in used:
                    stack.append((neighbor, path + (neighbor,), used | {neighbor}))
    return False


def quotient_graphs(order, code):
    """Contract any zero-stress forest and retain all other physical pairs."""
    pairs = tuple(itertools.combinations(range(order), 2))
    support = tuple(edge for edge, multiplicity in zip(pairs, code) if multiplicity)
    for mask in range(1 << len(support)):
        parent = list(range(order))
        valid = True
        for index, (u, v) in enumerate(support):
            if not (mask >> index) & 1:
                continue
            u, v = root(parent, u), root(parent, v)
            if u == v:
                valid = False
                break
            parent[v] = u
        if not valid:
            continue
        roots = sorted({root(parent, vertex) for vertex in range(order)})
        labels = {value: index for index, value in enumerate(roots)}
        edges = set()
        for index, (u, v) in enumerate(support):
            if (mask >> index) & 1:
                continue
            edge = tuple(sorted((labels[root(parent, u)], labels[root(parent, v)])))
            if edge[0] == edge[1]:
                valid = False
                break
            edges.add(edge)
        if not valid:
            continue
        graph = nx.Graph()
        graph.add_nodes_from(range(len(roots)))
        graph.add_edges_from(edges)
        yield graph


def wl_key(graph):
    return (len(graph), graph.number_of_edges(),
            tuple(sorted(dict(graph.degree()).values())),
            sum(nx.triangles(graph).values()) // 3)


def graph6(graph):
    return nx.to_graph6_bytes(graph, header=False).decode("ascii").strip()


def proper_odd_lengths(graph):
    result = []
    for length in (5, 7, 9):
        if length <= len(graph) and has_cycle_length(graph, length):
            if len(graph) > length or graph.number_of_edges() > length:
                result.append(length)
    return tuple(result)


def admissible_ranks(graph):
    """Ranks not excluded by extremality's zero-equation dimension bound."""
    order = len(graph)
    nonedges = math.comb(order, 2) - graph.number_of_edges()
    return tuple(rank for rank in range(3, order + 1)
                 if math.comb(rank + 1, 2) - 1 <= nonedges)


def derive():
    kernels = fixture()
    classes = []
    buckets = defaultdict(list)
    labeled = Counter()
    raw = Counter()

    for order in (9, 10):
        sources = [(number, record) for number, record in enumerate(kernels, 1)
                   if record["n"] == order]
        require(len(sources) == {9: 162, 10: 66}[order],
                f"order-{order} kernel count changed")
        for number, record in sources:
            require(sum(record["code"]) == order + 5,
                    f"rank-six path budget changed at K{number}")
            seen_for_kernel = set()
            for graph in quotient_graphs(order, tuple(record["code"])):
                lengths = proper_odd_lengths(graph)
                if not lengths:
                    continue
                raw[(order, number)] += 1
                if len(graph) < 3 or not nx.is_biconnected(graph):
                    continue
                ranks = admissible_ranks(graph)
                if not ranks:
                    continue
                key = wl_key(graph)
                class_index = None
                for candidate in buckets[key]:
                    if nx.is_isomorphic(graph, classes[candidate]["graph"]):
                        class_index = candidate
                        break
                if class_index is None:
                    class_index = len(classes)
                    buckets[key].append(class_index)
                    classes.append({
                        "graph": graph.copy(),
                        "odd_lengths": lengths,
                        "admissible_ranks": ranks,
                        "sources": set(),
                    })
                else:
                    require(classes[class_index]["odd_lengths"] == lengths,
                            "isomorphic graphs disagree on odd cycles")
                    require(classes[class_index]["admissible_ranks"] == ranks,
                            "isomorphic graphs disagree on rank bound")
                token = (class_index, order, number)
                if token not in seen_for_kernel:
                    classes[class_index]["sources"].add((order, number))
                    seen_for_kernel.add(token)
                    labeled[(order, class_index)] += 1

    records = []
    for index, item in enumerate(classes, 1):
        graph = item.pop("graph")
        records.append({
            "id": f"S{index:04d}",
            "graph6": graph6(graph),
            "order": len(graph),
            "size": graph.number_of_edges(),
            "degree_sequence": sorted(dict(graph.degree()).values(), reverse=True),
            "proper_odd_cycles": list(item["odd_lengths"]),
            "extreme_dnn_rank_candidates": list(item["admissible_ranks"]),
            "sources": [f"K{number}@{order}" for order, number in sorted(item["sources"])],
        })

    records.sort(key=lambda row: (row["order"], row["size"],
                                  row["degree_sequence"], row["graph6"]))
    for index, row in enumerate(records, 1):
        row["id"] = f"S{index:04d}"

    by_order = Counter(row["order"] for row in records)
    by_cycle = {str(length): sum(length in row["proper_odd_cycles"] for row in records)
                for length in (5, 7, 9)}
    by_ranks = Counter(
        ",".join(map(str, row["extreme_dnn_rank_candidates"])) for row in records
    )
    source_kernels = sorted(
        {source for row in records for source in row["sources"]},
        key=lambda source: (int(source.split("@")[1]),
                            int(source.split("@")[0][1:])),
    )
    return {
        "schema": "rank6-orders9-10-proper-odd-support-census-v1",
        "source_sha256": SOURCE_SHA256,
        "scope": {
            "orders": [9, 10],
            "contraction": "any subset of underlying support pairs that is a forest",
            "retention": "all uncontracted pairs, merged after quotient; loops rejected",
            "filters": [
                "support is biconnected",
                "support properly contains a simple C5, C7, or C9",
                "some rank r>=3 satisfies binom(r+1,2)-1 <= number_of_nonedges",
            ],
            "claim": "support-side necessary candidates, not DNN-ray existence",
        },
        "counts": {
            "isomorphism_classes": len(records),
            "by_quotient_order": {str(key): by_order[key] for key in sorted(by_order)},
            "by_contained_cycle": by_cycle,
            "by_extreme_rank_candidates": {
                key: by_ranks[key] for key in sorted(by_ranks)
            },
            "source_kernel_count": len(source_kernels),
        },
        "source_kernels": source_kernels,
        "supports": records,
    }


def verify(payload, expected):
    require(payload == expected, "stored proper-odd-support census changed")
    graphs = [nx.from_graph6_bytes(row["graph6"].encode("ascii"))
              for row in payload["supports"]]
    for left, right in itertools.combinations(range(len(graphs)), 2):
        require(not nx.is_isomorphic(graphs[left], graphs[right]),
                f"duplicate isomorphism classes at {left} and {right}")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    payload = derive()
    if args.verify:
        verify(json.loads(args.verify.read_text()), payload)
        print("rank-six orders 9-10 proper odd support census: exact audit passed")
        print(json.dumps(payload["counts"], sort_keys=True))
    elif args.write:
        OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(OUTPUT)
    else:
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
