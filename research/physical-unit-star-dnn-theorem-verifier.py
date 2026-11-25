#!/usr/bin/env python3
"""Fail-closed verifier for the universal physical hostile unit-star DNN theorem.

The theorem audit checks the exact symbolic proof skeleton and authenticates its
analytic imports.  ``check_instance`` is a dependency-free finite-graph
structure checker: it derives all bridges and the reduced positive hull rather
than trusting declared blocks or owners.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import deque
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "fixtures" / "physical-unit-star-dnn-theorem-manifest.json"
MANIFEST_SHA256 = "577ba7fa46737e58a89050b9da7bb1b87e29f7bd273e0c767390165230965c98"
THEOREM_SOURCE = (ROOT / "positive-square-energy" / "heptacyclic-general" /
                  "physical-unit-star-dnn-theorem.md")
THEOREM_SOURCE_SHA256 = "4b01acc39533fe53391157851a06f5c7b07013f2532f449725c120f931ca814e"
DNN_SOURCE = ROOT / "sharp-cactus-dnn" / "paper.tex"
DNN_SOURCE_SHA256 = "79dcffc6eb49d35951d6e8b7778de7f6de838239a467d99f4747bca3f57c0cbb"
STRUCTURAL_SOURCE = (ROOT / "positive-square-energy" / "heptacyclic-general" /
                     "physical-hull-bridge-reduction" / "theorem-note.md")
STRUCTURAL_SOURCE_SHA256 = "e09bdcfd99f85b4660678b1dbc70538bea6de0624b500ede8eae38eae9e639de"


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json_bytes(raw, label):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError(f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise VerificationError(f"nonstandard JSON constant in {label}: {value}")

    try:
        payload = json.loads(raw.decode("ascii"), object_pairs_hook=unique_pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return payload


def sha256_file(path):
    require(path.is_file() and not path.is_symlink(), f"missing or symlinked file: {path}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"path escaped repository: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_scope():
    return {
        "graph": "finite-simple-connected",
        "cyclomatic_rank": 7,
        "reduced_positive_hull": "weighted-unit-leaf-star",
        "center_component": "arbitrary-connected-bridge-free-rank-c",
        "center_rank_rows": [0, 1, 2, 3, 4, 5],
        "ports": "arbitrary-repeated-or-coincident",
        "restored_zero_rank_material":
            "arbitrary-physical-bridge-chains-branching-and-finite-tree-payloads",
    }


def load_manifest():
    raw = MANIFEST.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256,
            "manifest digest changed")
    return strict_json_bytes(raw, "physical unit-star manifest")


def validate_manifest(manifest):
    require(set(manifest) == {
        "schema", "theorem_id", "theorem_source", "scope", "hostile_cycle",
        "closed_rows", "residual_rows", "conclusion", "proof_contract",
        "analytic_import", "structural_source", "verification_boundary",
        "nonclaims",
    }, "manifest fields changed")
    require(manifest["schema"] == "physical-unit-star-dnn-theorem-v1" and
            manifest["theorem_id"] == "PHYSICAL-UNIT-STAR-DNN",
            "theorem identity changed")
    require(manifest["theorem_source"] == {
        "path": "positive-square-energy/heptacyclic-general/physical-unit-star-dnn-theorem.md",
        "sha256": THEOREM_SOURCE_SHA256,
    }, "theorem source identity changed")
    require(manifest["scope"] == exact_scope(), "theorem scope changed")
    require(manifest["hostile_cycle"] == {
        "length_congruence": "1 mod 4", "minimum_length": 5,
    }, "hostile cycle type changed")
    require(manifest["closed_rows"] == [
        {"center_rank_min": 0, "center_rank_max": 4,
         "condition": "all hostile leaf cycles",
         "conclusion": "s+(G)>|V(G)|"},
        {"center_rank": 5, "condition": "max(q_1,q_2)>=9",
         "conclusion": "s+(G)>|V(G)|"},
    ], "closed rows changed")
    require(manifest["residual_rows"] == [
        {"center_rank": 5, "condition": "(q_1,q_2)=(5,5)",
         "status": "OPEN_BY_THIS_CERTIFICATE"},
        {"center_rank": 6, "condition": "one hostile arm",
         "status": "OUT_OF_SCOPE"},
    ], "residual rows changed")
    require(manifest["conclusion"] == {
        "quantity": "s+(G)", "relation": ">", "statement": "s+(G)>|V(G)|",
    }, "conclusion changed")
    require(manifest["proof_contract"] == {
        "center_bound": "kappa(C)<=m_C+c",
        "decomposition": "kappa(G)=kappa(C)+B+sum_i(q_i+epsilon_qi)",
        "edge_ledger": "m=m_C+B+sum_i q_i",
        "master_bound": "kappa(G)<=m+c+sum_i epsilon_qi",
        "rank_identity": "m=n+6",
    }, "proof contract changed")
    require(manifest["analytic_import"] == {
        "path": "sharp-cactus-dnn/paper.tex",
        "sha256": DNN_SOURCE_SHA256,
        "contracts": [
            "universal-LTZ:kappa(H)<=2|E(H)|-|V(H)|+1",
            "one-vertex-sum-additivity", "kappa(K2)=1",
            "kappa(C_q)=q+epsilon_q", "s-(H)<=kappa(H)",
            "odd-epsilon-monotonicity-and-epsilon5-plus-epsilon7-less-than-one",
        ],
    }, "analytic import changed")
    require(manifest["structural_source"] == {
        "path": "positive-square-energy/heptacyclic-general/physical-hull-bridge-reduction/theorem-note.md",
        "sha256": STRUCTURAL_SOURCE_SHA256,
        "contract": "all-global-bridges quotient and weighted unit-star reduction",
    }, "structural source changed")
    require(manifest["verification_boundary"] == {
        "exactly_checked": [
            "canonical manifest identity, theorem identity, and dependency digests",
            "symbolic coefficient ledger", "exact integer radical certificates",
            "dependency-free iterative finite-instance Tarjan structure and edge ledger",
            "hostile mutation rejection",
        ],
        "imported_not_reproved": [
            "universal LTZ inequality", "exact one-vertex-sum additivity",
            "cycle optimization", "spectral DNN inequality",
            "calculus and trigonometric comparison",
        ],
    }, "verification boundary changed")
    require(manifest["nonclaims"] == [
        "c=5 with arm lengths (5,5)", "c=6 unit-star",
        "one-component rank-seven positive hull", "non-unit-star configurations",
        "all heptacyclic graphs", "Gamma>=delta_q",
        "spectral equality in the DNN bound", "publication or peer review",
    ], "nonclaim boundary changed")


def authenticate_imports():
    require(sha256_file(THEOREM_SOURCE) == THEOREM_SOURCE_SHA256,
            "theorem source digest changed")
    require(sha256_file(DNN_SOURCE) == DNN_SOURCE_SHA256,
            "DNN analytic source digest changed")
    require(sha256_file(STRUCTURAL_SOURCE) == STRUCTURAL_SOURCE_SHA256,
            "structural source digest changed")


def audit_symbolic_ledger():
    # Coefficients in (m_C, B, sum(q_i), c, sum(epsilon_i), constant).
    center = (1, 0, 0, 1, 0, 0)       # kappa(C)<=m_C+c
    bridges = (0, 1, 0, 0, 0, 0)      # B copies of K2
    cycles = (0, 0, 1, 0, 1, 0)       # sum(q_i+epsilon_i)
    total = tuple(sum(row) for row in zip(center, bridges, cycles))
    expected = (1, 1, 1, 1, 1, 0)
    require(total == expected, "master kappa coefficient ledger changed")
    # m=m_C+B+sum q_i leaves excess c+sum epsilon_i.
    require(tuple(total[j] - (1 if j < 3 else 0) for j in range(6)) ==
            (0, 0, 0, 1, 1, 0), "edge partition cancellation changed")
    # At fixed a=epsilon_5, E(c)=c+(7-c)a and E(c+1)-E(c)=1-a>0.
    # The exact endpoint E(4)<6 is 13<6sqrt(5), squared as 169<180.
    require(169 < 180, "c<=4 radical certificate changed")
    require(4 * 4 * 5 < 9 * 9,
            "two-C5 residual direction changed")  # 4sqrt(5)<9
    # epsilon_7 certificate: cos(pi/7)>2159/2401>7/8 and
    # 7/15<2sqrt(5)-4 iff 67/30<sqrt(5).
    require(8 * 2159 > 7 * 2401, "cos(pi/7) rational certificate changed")
    require(67 * 67 < 5 * 30 * 30,
            "epsilon_5+epsilon_7 radical certificate changed")
    return {
        "master_coefficients": list(total),
        "c_le_4_endpoint": "4+3epsilon_5=19-6sqrt(5)<6",
        "long_arm": "epsilon_5+epsilon_9<epsilon_5+epsilon_7<1",
        "residual_direction": "5+2epsilon_5>6",
    }


def normalize_adjacency(adjacency):
    require(type(adjacency) is dict and adjacency, "adjacency must be a nonempty dict")
    vertices = set(adjacency)
    require(all(type(v) is int and v >= 0 for v in vertices),
            "vertices must be distinct nonnegative integers")
    require(all(type(neighbours) in (list, tuple, set) for neighbours in adjacency.values()),
            "neighbour rows must be lists, tuples, or sets")
    graph = {}
    for vertex, neighbours in adjacency.items():
        row = list(neighbours)
        require(all(type(neighbour) is int and neighbour >= 0 for neighbour in row),
                "neighbours must be nonnegative integers, not booleans or aliases")
        require(len(row) == len(set(row)), "parallel edge or duplicate neighbour")
        require(vertex not in row, "loop detected")
        require(set(row) <= vertices, "edge endpoint missing from adjacency")
        graph[vertex] = set(row)
    for vertex, neighbours in graph.items():
        for neighbour in neighbours:
            require(vertex in graph[neighbour], "adjacency is not symmetric")
    return graph


def graph_edges(graph):
    return tuple(sorted((u, v) for u in graph for v in graph[u] if u < v))


def connected_vertices(graph, allowed=None, start=None):
    allowed = set(graph) if allowed is None else set(allowed)
    if not allowed:
        return set()
    if start is None:
        start = min(allowed)
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbour in graph[vertex]:
            if neighbour in allowed and neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return seen


def tarjan_bridges(graph):
    """Iterative low-link DFS; no Python call-stack depth bounds a bridge chain."""
    require(connected_vertices(graph) == set(graph), "graph is disconnected")
    timer = 1
    start = min(graph)
    discovery = {start: timer}
    low = {start: timer}
    bridges = set()
    # Mutable frames are [vertex, parent, sorted_neighbours, next_index].  A
    # child is finalized only when its frame pops, exactly when its low-link is
    # complete; then its parent low-link and bridge status can be updated.
    frames = [[start, None, tuple(sorted(graph[start])), 0]]
    while frames:
        vertex, parent, neighbours, next_index = frames[-1]
        if next_index < len(neighbours):
            neighbour = neighbours[next_index]
            frames[-1][3] += 1
            if neighbour == parent:
                # The graph is simple, so the unique parent edge is the only
                # undirected traversal edge that must be skipped.
                continue
            if neighbour not in discovery:
                timer += 1
                discovery[neighbour] = low[neighbour] = timer
                frames.append([neighbour, vertex,
                               tuple(sorted(graph[neighbour])), 0])
            else:
                low[vertex] = min(low[vertex], discovery[neighbour])
            continue

        frames.pop()
        if parent is not None:
            low[parent] = min(low[parent], low[vertex])
            if low[vertex] > discovery[parent]:
                bridges.add(tuple(sorted((parent, vertex))))

    require(len(discovery) == len(graph), "Tarjan traversal missed a vertex")
    return bridges


def bridge_components(graph, bridges):
    unseen = set(graph)
    components = []
    while unseen:
        start = min(unseen)
        component = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            vertex = stack.pop()
            for neighbour in graph[vertex]:
                if tuple(sorted((vertex, neighbour))) in bridges or neighbour not in unseen:
                    continue
                unseen.remove(neighbour)
                component.add(neighbour)
                stack.append(neighbour)
        components.append(frozenset(component))
    components.sort(key=lambda row: (min(row), len(row)))
    owner = {vertex: index for index, row in enumerate(components) for vertex in row}
    quotient_edges = set()
    for u, v in bridges:
        left, right = owner[u], owner[v]
        require(left != right, "bridge endpoints remained in one component")
        quotient_edges.add(tuple(sorted((left, right))))
    return tuple(components), owner, quotient_edges


def component_edge_count(graph, vertices):
    vertices = set(vertices)
    return sum(1 for u, v in graph_edges(graph) if u in vertices and v in vertices)


def quotient_adjacency(order, edges):
    adjacency = {vertex: set() for vertex in range(order)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return adjacency


def path_between(tree, start, finish):
    parent = {start: None}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        if vertex == finish:
            break
        for neighbour in sorted(tree[vertex]):
            if neighbour not in parent:
                parent[neighbour] = vertex
                queue.append(neighbour)
    require(finish in parent, "quotient path missing")
    path = []
    cursor = finish
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    return tuple(reversed(path))


def reduce_positive_hull(tree, ranks):
    positive = sorted(vertex for vertex, rank in ranks.items() if rank > 0)
    require(len(positive) >= 2, "positive hull has no edge")
    hull_vertices = set()
    for vertex in positive[1:]:
        hull_vertices.update(path_between(tree, positive[0], vertex))
    hull_edges = {tuple(sorted((u, v))) for u in hull_vertices for v in tree[u]
                  if v in hull_vertices and u < v}
    reduced = {vertex: {neighbour for neighbour in tree[vertex]
                        if tuple(sorted((vertex, neighbour))) in hull_edges}
               for vertex in hull_vertices}
    active = set(hull_vertices)
    while True:
        candidate = next((vertex for vertex in sorted(active)
                          if ranks[vertex] == 0 and len(reduced[vertex]) == 2), None)
        if candidate is None:
            break
        left, right = sorted(reduced[candidate])
        reduced[left].remove(candidate)
        reduced[right].remove(candidate)
        reduced[candidate].clear()
        active.remove(candidate)
        require(right not in reduced[left], "suppression creates parallel quotient edge")
        reduced[left].add(right)
        reduced[right].add(left)
    return {vertex: reduced[vertex] & active for vertex in active}


def check_instance(adjacency):
    graph = normalize_adjacency(adjacency)
    vertices = len(graph)
    edges = len(graph_edges(graph))
    beta = edges - vertices + 1
    require(beta == 7, "instance cyclomatic rank is not seven")
    bridges = tarjan_bridges(graph)
    components, owner, quotient_edges = bridge_components(graph, bridges)
    require(len(quotient_edges) == len(components) - 1,
            "all-bridge component quotient is not a tree")
    quotient = quotient_adjacency(len(components), quotient_edges)
    require(connected_vertices(quotient) == set(quotient), "quotient is disconnected")
    component_edges = {index: component_edge_count(graph, row)
                       for index, row in enumerate(components)}
    ranks = {index: component_edges[index] - len(row) + 1
             for index, row in enumerate(components)}
    require(all(rank >= 0 for rank in ranks.values()), "negative component rank")
    require(sum(ranks.values()) == 7, "component ranks do not sum to seven")
    for index, rank in ranks.items():
        if rank == 0:
            require(len(components[index]) == 1 and component_edges[index] == 0,
                    "rank-zero bridge-free component is not a singleton")
    reduced = reduce_positive_hull(quotient, ranks)
    positive_reduced = [vertex for vertex in reduced if ranks[vertex] > 0]
    unit_leaves = [vertex for vertex in positive_reduced
                   if ranks[vertex] == 1 and len(reduced[vertex]) == 1]
    centers = [vertex for vertex in reduced if vertex not in unit_leaves]
    require(len(centers) == 1, "reduced positive hull is not a unit-leaf star")
    center = centers[0]
    require(all(neighbours == {center} for vertex, neighbours in reduced.items()
                if vertex != center), "reduced positive hull is not a star")
    require(len(reduced[center]) == len(unit_leaves), "star has a non-unit leaf")
    center_rank = ranks[center]
    require(center_rank in (0, 1, 2, 3, 4, 5),
            "center rank is outside the checked rows")
    require(len(unit_leaves) == 7 - center_rank,
            "unit leaf count does not equal seven minus center rank")
    cycle_lengths = []
    for leaf in sorted(unit_leaves):
        component = components[leaf]
        q = len(component)
        require(component_edges[leaf] == q, "rank-one leaf is not unicyclic")
        require(all(len(graph[vertex] & set(component)) == 2 for vertex in component),
                "rank-one bridge-free leaf is not a chordless cycle")
        require(q >= 5 and q % 4 == 1, "leaf cycle is not hostile")
        cycle_lengths.append(q)
    center_edges = component_edges[center]
    bridge_count = len(bridges)
    require(edges == center_edges + bridge_count + sum(cycle_lengths),
            "edge ledger m=m_C+B+sum q_i failed")
    status = "CLOSED"
    if center_rank == 5 and cycle_lengths == [5, 5]:
        status = "OPEN_BY_THIS_CERTIFICATE"
    elif center_rank == 5:
        require(max(cycle_lengths) >= 9, "unexpected c=5 hostile profile")
    return {
        "vertices": vertices, "edges": edges, "beta": beta,
        "bridge_count": bridge_count, "component_count": len(components),
        "center_rank": center_rank, "center_edges": center_edges,
        "unit_leaf_count": len(unit_leaves), "cycle_lengths": cycle_lengths,
        "edge_ledger": [center_edges, bridge_count, sum(cycle_lengths)],
        "certificate_status": status,
    }


def hostile_self_checks(manifest):
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(manifest)
        mutate(candidate)
        mutations.append((label, candidate))

    add("rank widened", lambda value: value["scope"].update(cyclomatic_rank=8))
    add("theorem source changed", lambda value: value["theorem_source"].update(
        sha256="0" * 64))
    add("nonstar hull", lambda value: value["scope"].update(
        reduced_positive_hull="arbitrary-weighted-tree"))
    add("center classified", lambda value: value["scope"].update(
        center_component="single-positive-block-only"))
    add("ports narrowed", lambda value: value["scope"].update(ports="distinct-core-only"))
    add("c5 two-C5 closed", lambda value: value["residual_rows"][0].update(status="CLOSED"))
    add("c6 admitted", lambda value: value["scope"]["center_rank_rows"].append(6))
    add("weak conclusion", lambda value: value["conclusion"].update(relation=">="))
    add("center debit reduced", lambda value: value["proof_contract"].update(
        center_bound="kappa(C)<=m_C+c-1"))
    add("bridge term omitted", lambda value: value["proof_contract"].update(
        decomposition="kappa(G)=kappa(C)+sum_i(q_i+epsilon_qi)"))
    add("analytic import changed", lambda value: value["analytic_import"].update(
        sha256="0" * 64))
    add("structural import changed", lambda value: value["structural_source"].update(
        sha256="0" * 64))
    add("spectral equality claimed", lambda value: value["nonclaims"].remove(
        "spectral equality in the DNN bound"))
    for label, candidate in mutations:
        try:
            validate_manifest(candidate)
        except (IndexError, KeyError, TypeError, VerificationError, ValueError):
            continue
        raise VerificationError(f"hostile manifest mutation accepted: {label}")
    return tuple(label for label, _ in mutations)


def audit():
    manifest = load_manifest()
    validate_manifest(manifest)
    authenticate_imports()
    ledger = audit_symbolic_ledger()
    rejected = hostile_self_checks(manifest)
    require(len(rejected) == 13, "hostile mutation ledger changed")
    return {
        "schema": "physical-unit-star-dnn-theorem-receipt-v1",
        "theorem": "PHYSICAL-UNIT-STAR-DNN",
        "scope": "physical hostile unit-stars of total rank seven",
        "closed_rows": ["0<=c<=4", "c=5 and max(q_i)>=9"],
        "residual": "c=5 with (q_1,q_2)=(5,5)",
        "strict": True,
        "symbolic_ledger": ledger,
        "instance_checker": ("dependency-free iterative Tarjan derivation; "
                             "adjacency supplied at call time"),
        "authenticated_source_count": 3,
        "hostile_mutations_rejected": list(rejected),
        "nonclaim": "c=6, one-component rank seven, non-unit-stars, and all-heptacyclic closure remain open",
    }


def optimized_output(arguments):
    command = (sys.executable, "-I", "-B", "-O", str(Path(__file__).resolve()),
               "--optimized-child", *arguments)
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
    require(completed.returncode == 0 and completed.stderr == b"",
            "optimized theorem audit failed")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--optimized-child", action="store_true")
    args = parser.parse_args()
    try:
        if args.instance is not None:
            raw = args.instance.read_bytes()
            adjacency = strict_json_bytes(raw, "instance adjacency")
            require(type(adjacency) is dict and adjacency,
                    "instance JSON adjacency must be a nonempty object")
            require(all(type(key) is str and key == str(int(key)) and int(key) >= 0
                        for key in adjacency),
                    "instance vertex keys must be canonical nonnegative decimal integers")
            require(all(type(value) is list for value in adjacency.values()),
                    "instance JSON adjacency rows must be lists")
            integer_adjacency = {int(key): value for key, value in adjacency.items()}
            require(len(integer_adjacency) == len(adjacency),
                    "instance vertex keys collide after integer conversion")
            output = canonical_bytes(check_instance(integer_adjacency))
        else:
            receipt = audit()
            output = canonical_bytes(receipt) if args.print_manifest else (
                b"physical unit-star DNN theorem: exact audit passed\n")
        if not args.optimized_child and not args.emit and sys.flags.optimize == 0:
            child_args = []
            if args.print_manifest:
                child_args.append("--print-manifest")
            if args.instance is not None:
                child_args.extend(("--instance", str(args.instance)))
            require(optimized_output(tuple(child_args)) == output,
                    "normal and optimized theorem outputs differ")
        sys.stdout.buffer.write(output)
        return 0
    except (OSError, VerificationError, TypeError, ValueError) as error:
        sys.stderr.write(f"physical unit-star DNN theorem: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
