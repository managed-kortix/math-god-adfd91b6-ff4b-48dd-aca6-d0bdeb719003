#!/usr/bin/env python3
"""Independent exact reconstruction of the rank-7/order-8 singleton territory.

Inputs are source artifacts, not the prose territory note.  The verifier binds
its six-field row to the canonical rank-seven kernel source, the exact residual
stream, the rational-search projection, its full automorphism orbit, and the
induced two-K4 territory decomposition for arbitrary symbolic path/tree sizes.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import lzma
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
if os.environ.get("ORDER8_ROOT"):
    ROOT = Path(os.environ["ORDER8_ROOT"]).resolve()
else:
    candidates = (HERE / "repo", Path("/workspace/order8-audit"),
                  Path("/workspace/repo"), HERE)
    ROOT = next((candidate for candidate in candidates
                 if (candidate / "positive-square-energy" / "experiments" /
                     "rank7_order8_after_post_xii_shared_packet_remainder.jsonl.xz").is_file()),
                candidates[0])
EXP = ROOT / "positive-square-energy" / "experiments"
FIXTURE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
MANIFEST = EXP / "rank7_order8_exact_residual_census_manifest.json"
INDICES = EXP / "rank7_order8_rational_search_indices.json"
SINGLETON = EXP / "rank7_order8_after_post_xii_shared_packet_remainder.jsonl.xz"

PINS = {
    FIXTURE: "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    MANIFEST: "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98",
    INDICES: "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59",
    SINGLETON: "bbadc801837908ada49cdb53a83fb1afa46a5a240a77ecb18c66fbb0a06a6340",
}
EXPECTED_ROW = [
    416536, 416987, 6832,
    [[0, 3, 1], [0, 6, 1], [0, 7, 1], [1, 2, 1], [1, 4, 1], [1, 5, 1],
     [2, 4, 1], [2, 5, 1], [3, 6, 1], [3, 7, 1], [4, 5, 1], [4, 7, 1],
     [5, 6, 1], [6, 7, 1]],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], 2,
]
A = frozenset((0, 3, 6, 7))
B = frozenset((1, 2, 4, 5))
A_EDGES = frozenset(itertools.combinations(sorted(A), 2))
B_EDGES = frozenset(itertools.combinations(sorted(B), 2))
CONNECTORS = frozenset(((4, 7), (5, 6)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_json(raw: bytes, label: str):
    value = json.loads(raw.decode("ascii"))
    canonical = (json.dumps(value, sort_keys=True, separators=(",", ":"),
                            allow_nan=False) + "\n").encode("ascii")
    require(raw == canonical, f"noncanonical JSON: {label}")
    return value


def graph_components(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    components = []
    unseen = set(vertices)
    while unseen:
        todo = [min(unseen)]
        seen = {todo[0]}
        unseen.remove(todo[0])
        while todo:
            u = todo.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    unseen.remove(v)
                    todo.append(v)
        components.append(seen)
    return components


def cyclomatic(vertices, edges):
    return len(edges) - len(vertices) + len(graph_components(vertices, edges))


def expand_symbolic(row, lengths, tree_edges_by_root):
    """Expand paths and attach one arbitrary rooted star/tree-size proxy per root.

    Tree shapes do not affect the invariant: every nonroot tree edge introduces
    exactly one vertex and one edge in the same territory.  We nevertheless
    realize chains, which include arbitrary sizes and connector-interior roots.
    """
    support = [tuple(edge[:2]) for edge in row[3]]
    vertices = set(range(8))
    edges = []
    paths = {}
    next_vertex = 8
    for pair, length in zip(support, lengths, strict=True):
        require(type(length) is int and length >= 1, "invalid positive path length")
        u, v = pair
        path = [u]
        for _ in range(length - 1):
            vertices.add(next_vertex)
            path.append(next_vertex)
            next_vertex += 1
        path.append(v)
        edges.extend(zip(path, path[1:]))
        paths[pair] = tuple(path)
    # Each value t realizes a rooted chain of t edges.  This suffices to test
    # allocation/counting; the proof below uses only the one-new-vertex-per-edge
    # property, valid for every rooted tree shape.
    for root, count in tree_edges_by_root.items():
        require(root in vertices and type(count) is int and count >= 0,
                "invalid tree attachment")
        previous = root
        for _ in range(count):
            vertices.add(next_vertex)
            edges.append((previous, next_vertex))
            previous = next_vertex
            next_vertex += 1
    return vertices, edges, paths


def territory_check(row, lengths, attachment_plan):
    # First expand core/connectors, so attachment roots can be selected by a
    # callback from connector interiors as well as branch/core vertices.
    vertices, edges, paths = expand_symbolic(row, lengths, {})
    tree_spec = attachment_plan(paths)
    vertices, edges, paths = expand_symbolic(row, lengths, tree_spec)

    # Reconstruct the same expanded IDs: tree roots refer to IDs before tree
    # expansion, and all path IDs are deterministic.
    a_core = set(A)
    for pair in A_EDGES:
        a_core.update(paths[pair][1:-1])
    b_core = set(B)
    for pair in B_EDGES:
        b_core.update(paths[pair][1:-1])
    u0 = a_core.copy()
    for pair in CONNECTORS:
        u0.update(paths[pair][1:-1])
    w0 = b_core
    require(u0.isdisjoint(w0), "base territories overlap")

    # Allocate each complete attached chain/tree to its root's base side.  The
    # generated chains appear after all path vertices, in insertion order.
    side = {v: ("U" if v in u0 else "W") for v in u0 | w0}
    path_vertex_count = max(u0 | w0) + 1
    next_tree = path_vertex_count
    for root, count in tree_spec.items():
        root_side = side[root]
        for _ in range(count):
            side[next_tree] = root_side
            next_tree += 1
    require(set(side) == vertices and set(side.values()) == {"U", "W"},
            "territory assignment is not exhaustive")
    U = {v for v in vertices if side[v] == "U"}
    W = vertices - U
    UE = [(u, v) for u, v in edges if u in U and v in U]
    WE = [(u, v) for u, v in edges if u in W and v in W]
    cross = [(u, v) for u, v in edges if side[u] != side[v]]
    require(len(graph_components(U, UE)) == len(graph_components(W, WE)) == 1,
            "an induced territory is disconnected")
    require(cyclomatic(U, UE) == cyclomatic(W, WE) == 3,
            "territory cyclomatic rank is not 3")
    require(len(UE) == len(U) + 2 and len(WE) == len(W) + 2,
            "territory tricyclic edge/vertex identity failed")
    require(len(cross) == 2, "there is not exactly one crossing edge per connector")
    for pair in CONNECTORS:
        path = paths[pair]
        # Source edges are lexicographically oriented, whereas territory
        # orientation is always from the A endpoint toward the B endpoint.
        if path[0] not in A:
            path = tuple(reversed(path))
        pair_cross = [edge for edge in zip(path, path[1:])
                      if side[edge[0]] != side[edge[1]]]
        require(len(pair_cross) == 1, "connector has wrong crossing-edge count")
        # Unit connector: its sole edge must cross and there is no U stub.
        if len(path) == 2:
            require(pair_cross == [tuple(path)], "unit connector allocation failed")
        else:
            require(pair_cross[0][1] in B and pair_cross[0][0] in U,
                    "long connector does not cross at B terminal")
    return len(U), len(W), len(UE), len(WE), tuple(cross)


def main():
    for path, digest in PINS.items():
        require(sha(path) == digest, f"source pin changed: {path.name}")

    raw_singleton = lzma.decompress(SINGLETON.read_bytes(), format=lzma.FORMAT_XZ)
    row = strict_json(raw_singleton, "singleton")
    require(row == EXPECTED_ROW, "six-field singleton changed")

    # Rebuild K6832 directly from the canonical dense kernel source.
    fixture = strict_json(FIXTURE.read_bytes(), "kernel fixture")
    record = fixture["kernels"][row[2] - 1]
    require(record["n"] == 8, "K6832 has wrong order")
    pairs = tuple(itertools.combinations(range(8), 2))
    rebuilt_edges = [[u, v, m] for (u, v), m in zip(pairs, record["code"], strict=True) if m]
    require(rebuilt_edges == row[3], "row edges differ from K6832 source")
    require(sum(1 for item in fixture["kernels"][:row[2]] if item["n"] == 8) == 3361,
            "K6832 order-eight local index changed")

    support = frozenset(tuple(edge[:2]) for edge in row[3])
    require(support == A_EDGES | B_EDGES | CONNECTORS, "not exactly two K4s plus 74,65")
    require(A.isdisjoint(B) and A | B == frozenset(range(8)), "branch partition failed")

    # Locate source index 416987 by exact concatenation of the committed chunks.
    manifest = strict_json(MANIFEST.read_bytes(), "manifest")
    source_offset = 0
    found = []
    for chunk_info in manifest["chunks"]:
        path = EXP / chunk_info["path"]
        require(sha(path) == chunk_info["artifact_sha256"], "chunk artifact changed")
        chunk_raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_XZ)
        require(hashlib.sha256(chunk_raw).hexdigest() == chunk_info["raw_sha256"],
                "chunk raw digest changed")
        chunk = strict_json(chunk_raw, path.name)
        for local, residual in enumerate(chunk["residuals"]):
            if (residual["global_kernel"] == row[2] and residual["row"] == row[4]
                    and residual["orbit_size"] == row[5]):
                found.append(source_offset + local)
        source_offset += len(chunk["residuals"])
    require(source_offset == 493417 and found == [row[1]], "source-index binding failed")

    # Bind selected stream index 416536 to residual source index 416987.
    indices = strict_json(INDICES.read_bytes(), "rational indices")["source_indices"]
    require(len(indices) == 492812 and indices[row[0]] == row[1]
            and indices.index(row[1]) == row[0], "stream/source projection failed")

    # Recompute the complete support automorphism group and parity orbit.
    edge_index = {tuple(edge[:2]): i for i, edge in enumerate(row[3])}
    actions = []
    orbit = set()
    parity = tuple(row[4])
    for permutation in itertools.permutations(range(8)):
        action = []
        for u, v, _ in row[3]:
            image = tuple(sorted((permutation[u], permutation[v])))
            if image not in edge_index:
                break
            action.append(edge_index[image])
        else:
            actions.append(tuple(action))
            orbit.add(tuple(parity[index] for index in action))
    require(len(actions) == 16 and len(orbit) == row[5], "automorphism/orbit count failed")
    require({tuple(row[3][state.index(0)][:2]) for state in orbit} == CONNECTORS,
            "orbit is not exactly the choice of even connector")

    # Canonical graph and every +2 single-coordinate frontier, no attachments.
    canonical = tuple(1 if odd else 2 for odd in row[4])
    cases = [canonical]
    for i in range(14):
        changed = list(canonical)
        changed[i] += 2
        cases.append(tuple(changed))
    for lengths in cases:
        territory_check(row, lengths, lambda paths: {})

    # Hostile edge cases requested: both connectors unit, one/both long; attach
    # nontrivial trees at every available connector-interior root and at both
    # sides' branch/core roots.  Lengths are arbitrary parity-independent tests.
    scenarios = (
        (1, 1), (1, 4), (3, 1), (2, 5), (6, 7),
    )
    for l74, l65 in scenarios:
        lengths = [2 + (i % 4) for i in range(14)]
        # force arbitrary internal K4 path lengths too
        lengths[11] = l74
        lengths[12] = l65
        def attachments(paths):
            roots = [0, 1, 4, 7]
            roots.extend(paths[(4, 7)][1:-1])
            roots.extend(paths[(5, 6)][1:-1])
            return {root: (position % 4) + 1 for position, root in enumerate(roots)}
        territory_check(row, tuple(lengths), attachments)

    print(json.dumps({
        "status": "passed",
        "row": row[:3] + ["edges/parity-bound", row[5]],
        "decomposition": {"A": sorted(A), "B": sorted(B),
                          "connectors": [list(x) for x in sorted(CONNECTORS)]},
        "automorphisms": len(actions), "parity_orbit": len(orbit),
        "source_residuals": source_offset,
        "frontiers_checked": len(cases),
        "tree_connector_scenarios_checked": len(scenarios),
        "induced_ranks": [3, 3],
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
