#!/usr/bin/env python3
"""Exact finite search for the rooted triangular-cactus/C5 guard.

No floating-point arithmetic is used.  Characteristic polynomials and the
multiplicity-aware Sturm implementation are imported from the independently
audited rooted packet experiment.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import isqrt

from shared_triangle_rooted_exact import (
    add_cycle,
    add_edge,
    characteristic_polynomial,
    isolate_positive_roots_with_multiplicity,
    rational_text,
)


Graph = tuple[int, frozenset[tuple[int, int]]]


def adjacency(graph: Graph) -> list[set[int]]:
    n, edges = graph
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def vertex_signatures(graph: Graph, colors: tuple[int, ...] | None = None):
    adj = adjacency(graph)
    if colors is None:
        colors = (0,) * len(adj)
    triangles = [sum(1 for u in adj[v] for w in adj[v] if u < w and w in adj[u]) for v in range(len(adj))]
    # The triangle count above intentionally need only be an isomorphism
    # invariant; refinement below supplies the decisive local information.
    labels = [(colors[v], len(adj[v]), triangles[v]) for v in range(len(adj))]
    while True:
        raw = [(labels[v], tuple(sorted(labels[w] for w in adj[v]))) for v in range(len(adj))]
        palette = {value: i for i, value in enumerate(sorted(set(raw)))}
        refined = [palette[value] for value in raw]
        if all((labels[v] == labels[w]) == (refined[v] == refined[w])
               for v, w in itertools.combinations(range(len(adj)), 2)):
            return tuple(refined)
        labels = refined


def isomorphic(left: Graph, right: Graph, left_colors=None, right_colors=None) -> bool:
    if left[0] != right[0] or len(left[1]) != len(right[1]):
        return False
    n = left[0]
    left_colors = tuple(left_colors or (0,) * n)
    right_colors = tuple(right_colors or (0,) * n)
    la, ra = adjacency(left), adjacency(right)
    ls = vertex_signatures(left, left_colors)
    rs = vertex_signatures(right, right_colors)
    if Counter(ls) != Counter(rs):
        return False
    candidates = {u: [v for v in range(n) if ls[u] == rs[v]] for u in range(n)}
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def search() -> bool:
        if len(mapping) == n:
            return True
        unmapped = [u for u in range(n) if u not in mapping]
        u = min(unmapped, key=lambda x: sum(v not in used for v in candidates[x]))
        for v in candidates[u]:
            if v in used:
                continue
            if any((w in la[u]) != (mapping[w] in ra[v]) for w in mapping):
                continue
            mapping[u] = v
            used.add(v)
            if search():
                return True
            used.remove(v)
            del mapping[u]
        return False

    return search()


def invariant(graph: Graph, colors=None):
    n, edges = graph
    colors = tuple(colors or (0,) * n)
    sig = vertex_signatures(graph, colors)
    adj = adjacency(graph)
    return n, len(edges), tuple(sorted((sig[v], len(adj[v])) for v in range(n)))


def unique_graphs(items, colored=False):
    buckets = defaultdict(list)
    result = []
    for item in items:
        graph, colors = (item[0], item[1]) if colored else (item, None)
        key = invariant(graph, colors)
        if any(isomorphic(graph, old_graph, colors, old_colors) for old_graph, old_colors, _ in buckets[key]):
            continue
        buckets[key].append((graph, colors, item))
        result.append(item)
    return result


def triangular_cores(max_triangles: int):
    levels: dict[int, list[Graph]] = {1: [(3, frozenset({(0, 1), (0, 2), (1, 2)}))]}
    for count in range(2, max_triangles + 1):
        candidates = []
        for n, edges in levels[count - 1]:
            for root in range(n):
                new_edges = set(edges)
                add_cycle(new_edges, [root, n, n + 1])
                candidates.append((n + 2, frozenset(new_edges)))
        levels[count] = unique_graphs(candidates)
    return levels


def rooted_orbits(graph: Graph):
    n = graph[0]
    representatives = []
    for root in range(n):
        colors = tuple(1 if v == root else 0 for v in range(n))
        if not any(isomorphic(graph, graph, colors, old_colors) for _, old_colors in representatives):
            representatives.append((root, colors))
    return [root for root, _ in representatives]


def prufer_tree(code: tuple[int, ...]) -> Graph:
    n = len(code) + 2
    degree = [1] * n
    for v in code:
        degree[v] += 1
    edges = set()
    for v in code:
        leaf = min(i for i in range(n) if degree[i] == 1)
        add_edge(edges, leaf, v)
        degree[leaf] -= 1
        degree[v] -= 1
    u, v = [i for i in range(n) if degree[i] == 1]
    add_edge(edges, u, v)
    return n, frozenset(edges)


def rooted_trees(max_vertices: int):
    result = [(1, frozenset(), 0)]
    for n in range(2, max_vertices + 1):
        candidates = []
        for code in itertools.product(range(n), repeat=n - 2):
            graph = prufer_tree(code)
            for root in range(n):
                colors = tuple(1 if v == root else 0 for v in range(n))
                candidates.append((graph, colors, root))
        unique = unique_graphs(candidates, colored=True)
        result.extend((graph[0], graph[1], root) for graph, _, root in unique)
    return result


def join_c5(graph: Graph, root: int, bridge_length: int):
    n, old_edges = graph
    edges = set(old_edges)
    if bridge_length == 0:
        croot = root
    else:
        previous = root
        for _ in range(bridge_length):
            add_edge(edges, previous, n)
            previous = n
            n += 1
        croot = previous
    private = list(range(n, n + 4))
    add_cycle(edges, [croot] + private)
    return (n + 4, frozenset(edges)), croot


def attach_tree(graph: Graph, at: int, tree):
    n, old_edges = graph
    tn, tree_edges, root = tree
    image = {root: at}
    for v in range(tn):
        if v != root:
            image[v] = n
            n += 1
    edges = set(old_edges)
    for u, v in tree_edges:
        add_edge(edges, image[u], image[v])
    return n, frozenset(edges)


def sqrt5_interval(bits: int):
    denominator = 1 << bits
    lower_num = isqrt(5 * denominator * denominator)
    return Fraction(lower_num, denominator), Fraction(lower_num + 1, denominator)


def spectral_certificate(graph: Graph, bits: int):
    n, edges = graph
    poly = characteristic_polynomial(n, edges)
    intervals = isolate_positive_roots_with_multiplicity(poly, bits)
    lower = sum(mult * left * left for left, _, mult in intervals) - n
    upper = sum(mult * right * right for _, right, mult in intervals) - n
    return {
        "vertices": n,
        "edges": len(edges),
        "characteristic_polynomial_desc": poly,
        "positive_root_intervals": [
            {"interval": [rational_text(left), rational_text(right)], "multiplicity": mult}
            for left, right, mult in intervals
        ],
        "surplus_interval": [rational_text(lower), rational_text(upper)],
    }, lower, upper


def describe_edges(graph: Graph):
    return [list(edge) for edge in sorted(graph[1])]


def core_type(graph: Graph):
    adj = adjacency(graph)
    triangles = []
    for u in range(graph[0]):
        for v in adj[u]:
            if v <= u:
                continue
            for w in adj[u] & adj[v]:
                if w > v:
                    triangles.append((u, v, w))
    memberships = Counter(v for triangle in triangles for v in triangle)
    signature = sorted(memberships.values(), reverse=True)
    h = len(triangles)
    if signature and signature[0] == h:
        name = "common-cut bouquet"
    elif h == 4 and any(all(memberships[v] == 2 for v in triangle) for triangle in triangles):
        name = "central-triangle/three-petal Voronoi obstruction"
    elif max(signature, default=0) <= 2:
        name = "distributed chain/tree incidence"
    else:
        name = "partially concentrated branching incidence"
    return name, signature


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-triangles", type=int, default=6)
    parser.add_argument("--max-bridge", type=int, default=3)
    parser.add_argument("--max-tree-vertices", type=int, default=5)
    parser.add_argument("--bits", type=int, default=24)
    parser.add_argument("--keep", type=int, default=20)
    parser.add_argument("--attachments", choices=("none", "root", "all"), default="root")
    parser.add_argument("--output")
    args = parser.parse_args()

    # Regression for the repeated sqrt(3) eigenvalue in the central-three-petal
    # core: multiplicity-aware surplus is exactly 6, not 3.
    central = triangular_cores(4)[4][2]
    central_poly = characteristic_polynomial(*central)
    central_intervals = isolate_positive_roots_with_multiplicity(central_poly, args.bits)
    central_lower = sum(mult * left * left for left, _, mult in central_intervals) - central[0]
    central_upper = sum(mult * right * right for _, right, mult in central_intervals) - central[0]
    assert central_lower <= 6 <= central_upper
    assert sorted(mult for _, _, mult in central_intervals) == [1, 2]

    cores = triangular_cores(args.max_triangles)
    trees = rooted_trees(args.max_tree_vertices)
    sqrt_lower, sqrt_upper = sqrt5_interval(args.bits + 8)
    threshold_lower, threshold_upper = 3 - sqrt_upper, 3 - sqrt_lower
    worst = []
    worst_by_triangles = defaultdict(list)
    census = Counter()
    counterexamples = []
    verdicts = Counter()

    def retain(record, lower, upper):
        worst.append((lower, upper, record))
        worst.sort(key=lambda row: (row[0], row[1]))
        del worst[args.keep:]
        rows = worst_by_triangles[record["triangles"]]
        rows.append((lower, upper, record))
        rows.sort(key=lambda row: (row[0], row[1]))
        del rows[5:]

    for h, level in cores.items():
        for core_index, core in enumerate(level):
            structure, incidence_signature = core_type(core)
            for root in rooted_orbits(core):
                for bridge in range(args.max_bridge + 1):
                    base, croot = join_c5(core, root, bridge)
                    variants = [(base, "none", -1)]
                    if args.attachments != "none":
                        sites = [root] if args.attachments == "root" else list(range(base[0]))
                        for tree_index, tree in enumerate(trees[1:], 1):
                            for site in sites:
                                variants.append((attach_tree(base, site, tree), f"tree-{tree[0]}-{tree_index}", site))
                    for graph, attachment, site in variants:
                        certificate, lower, upper = spectral_certificate(graph, args.bits)
                        census[(h, bridge, attachment == "none")] += 1
                        record = {
                            "triangles": h,
                            "core_index": core_index,
                            "core_root": root,
                            "core_type": structure,
                            "triangle_vertex_memberships_desc": incidence_signature,
                            "bridge_length": bridge,
                            "c5_root": croot,
                            "attachment": attachment,
                            "attachment_site": site,
                            "edges": describe_edges(graph),
                            "certificate": certificate,
                        }
                        retain(record, lower, upper)
                        if upper <= threshold_lower:
                            counterexamples.append(record)
                            verdicts["counterexample"] += 1
                        elif lower > threshold_upper:
                            verdicts["certified_strict"] += 1
                        else:
                            verdicts["unresolved_at_precision"] += 1

    output = {
        "arithmetic": "integer characteristic polynomials; Fraction Sturm isolation; multiplicities restored by squarefree layers",
        "scope": {
            "triangular_blocks": f"all nonisomorphic vertex-coalesced triangular cacti with 1..{args.max_triangles} blocks",
            "root": "one representative of every automorphism orbit",
            "c5_bridge_lengths": [0, args.max_bridge],
            "tree_attachments": args.attachments,
            "rooted_tree_order": [1, args.max_tree_vertices] if args.attachments != "none" else None,
        },
        "core_counts": {str(h): len(level) for h, level in cores.items()},
        "rooted_tree_count_by_order": dict(sorted(Counter(tree[0] for tree in trees).items())),
        "tested_graphs": sum(census.values()),
        "threshold_interval_3_minus_sqrt5": [rational_text(threshold_lower), rational_text(threshold_upper)],
        "counterexamples": counterexamples,
        "verdict_counts": dict(verdicts),
        "worst_cases": [record for _, _, record in worst],
        "worst_by_triangle_count": {
            str(h): [record for _, _, record in rows]
            for h, rows in sorted(worst_by_triangles.items())
        },
        "census": [
            {"triangles": key[0], "bridge_length": key[1], "bare": key[2], "count": value}
            for key, value in sorted(census.items())
        ],
    }
    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="ascii") as handle:
            handle.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
