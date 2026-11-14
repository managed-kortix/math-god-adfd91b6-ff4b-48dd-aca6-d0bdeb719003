#!/usr/bin/env python3
"""OPEN hostile audit of the *physical* doubled-C4 coupled split.

This program intentionally does not import the former synthetic diamond/D3
model.  It constructs the six physical paths of the doubled-C4, transports
all marked records through genuine kernel automorphisms, deletes an internal
vertex of the even connector, and cuts an actual edge of the odd connector.

The finite loop probes connector lengths 2,4,6 and 1,3,5 at every possible
opening/cut position.  The final symbolic-remnant check is the exact
all-length step: after the operations, each connector remainder is a pendant
path and contributes equally many vertices and edges.

OPEN RESEARCH ONLY.  A zero exit authenticates the reported structural census;
it is not a promoted theorem receipt.
"""

from __future__ import annotations

import itertools
import subprocess
import sys
from collections import Counter


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def edge(u, v):
    require(u != v, "loop requested")
    return tuple(sorted((u, v), key=repr))


# Physical path order a,A',b,c,C',d.  The doubled fibres are a/A' and c/C';
# b,d are the two single connectors.
ENDPOINTS = ((0, 1), (0, 1), (1, 2), (2, 3), (2, 3), (3, 0))
DOUBLED_FIBRES = ((0, 1), (3, 4))
CONNECTORS = (2, 5)
BASE_ROW = "010011"
EXPECTED_ANCHORS = (
    "010011", "010101", "011010", "011100",
    "100011", "100101", "101010", "101100",
)
LABELS = ("A", "B", "C", "D", "x", "y")
BASE_TOKENS = {
    "A": ("branch", 0), "B": ("branch", 1),
    "C": ("branch", 2), "D": ("branch", 3),
    "x": ("interior", 0), "y": ("interior", 3),
}
BASE_SIDE = {"A": 0, "B": 0, "x": 0, "C": 1, "D": 1, "y": 1}
EVEN_LENGTH_PROBES = (2, 4, 6)
ODD_LENGTH_PROBES = (1, 3, 5)


def adjacency_multiplicities():
    adjacency = [[0] * 4 for _ in range(4)]
    for u, v in ENDPOINTS:
        adjacency[u][v] += 1
        adjacency[v][u] += 1
    return adjacency


def genuine_automorphisms():
    """All genuine (branch-vertex map, physical-path map) pairs."""
    adjacency = adjacency_multiplicities()
    answer = set()
    for vertex_map in itertools.permutations(range(4)):
        if not all(adjacency[u][v] == adjacency[vertex_map[u]][vertex_map[v]]
                   for u in range(4) for v in range(4)):
            continue
        targets = []
        for u, v in ENDPOINTS:
            image_pair = sorted((vertex_map[u], vertex_map[v]))
            targets.append(tuple(i for i, endpoints in enumerate(ENDPOINTS)
                                 if sorted(endpoints) == image_pair))
        for edge_map in itertools.product(*targets):
            if len(set(edge_map)) == 6:
                answer.add((tuple(vertex_map), tuple(edge_map)))
    return tuple(sorted(answer))


def act_on_row(row, edge_map):
    image = [None] * 6
    for old, new in enumerate(edge_map):
        image[new] = row[old]
    require(all(bit is not None for bit in image), "incomplete row action")
    return "".join(image)


def first_simple_lengths(row, even_length, odd_length):
    require(even_length >= 2 and even_length % 2 == 0,
            "even connector length is not positive even")
    require(odd_length >= 1 and odd_length % 2 == 1,
            "odd connector length is not positive odd")
    lengths = [1 if bit == "1" else 2 for bit in row]
    even_connector = next(i for i in CONNECTORS if row[i] == "0")
    odd_connector = next(i for i in CONNECTORS if row[i] == "1")
    require(sum(row[i] == "0" for i in CONNECTORS) == 1,
            "connectors do not have opposite parity")
    lengths[even_connector] = even_length
    lengths[odd_connector] = odd_length
    for fibre in DOUBLED_FIBRES:
        require(sorted(lengths[i] for i in fibre) == [1, 2],
                "doubled members are not first-simple")
    return tuple(lengths), even_connector, odd_connector


def base_records():
    records = []
    records.extend(("direct3", roots)
                   for roots in itertools.combinations_with_replacement(LABELS, 3))
    records.extend(("chain2+direct", upstream, direct)
                   for upstream in LABELS for direct in LABELS)
    records.extend(("fork", upstream, occupancy)
                   for upstream in LABELS for occupancy in ("same", "split"))
    records.extend(("chain3", upstream) for upstream in LABELS)
    require(len(records) == 110 and len(set(records)) == 110,
            "marked-record census is not 110")
    require(Counter(record[0] for record in records) == Counter({
        "direct3": 56, "chain2+direct": 36, "fork": 12, "chain3": 6,
    }), "marked-record shape census changed")
    return tuple(records)


def record_top_sides(record):
    if record[0] == "direct3":
        roots = record[1]
        return tuple(BASE_SIDE[root] for root in roots)
    if record[0] == "chain2+direct":
        # The upstream root owns two blocks; the direct root owns one.
        return (BASE_SIDE[record[1]], BASE_SIDE[record[1]], BASE_SIDE[record[2]])
    # Fork and length-three chain: all three blocks follow the upstream root.
    return (BASE_SIDE[record[1]],) * 3


def transported_owner(label, vertex_map, edge_map):
    kind, index = BASE_TOKENS[label]
    if kind == "branch":
        return ("B", vertex_map[index])
    target_edge = edge_map[index]
    # Every transported even doubled member has physical length two, hence one
    # internal vertex.  Orientation cannot change its position.
    return ("P", target_edge, 1)


def build_physical_graph(row, witness, record, even_length, odd_length,
                         opening_position, cut_position, decorate=False):
    vertex_map, edge_map = witness
    lengths, even_connector, odd_connector = first_simple_lengths(
        row, even_length, odd_length)
    require(1 <= opening_position < even_length,
            "opening is not an internal even-connector vertex")
    require(0 <= cut_position < odd_length,
            "cut is not an actual odd-connector edge")

    vertices = {("B", i) for i in range(4)}
    edges = set()
    path_vertices = {}
    for path, ((u, v), length) in enumerate(zip(ENDPOINTS, lengths)):
        sequence = [("B", u)]
        for position in range(1, length):
            internal = ("P", path, position)
            vertices.add(internal)
            sequence.append(internal)
        sequence.append(("B", v))
        path_vertices[path] = tuple(sequence)
        edges.update(edge(sequence[i], sequence[i + 1])
                     for i in range(length))

    intrinsic = []
    for fibre in DOUBLED_FIBRES:
        cycle_vertices = set(path_vertices[fibre[0]]) | set(path_vertices[fibre[1]])
        require(len(cycle_vertices) == 3,
                "first-simple doubled fibre is not a physical triangle")
        intrinsic.append(frozenset(cycle_vertices))

    triangles = []
    next_triangle = 0

    def attach(owner):
        nonlocal next_triangle
        left = ("T", next_triangle, 0)
        right = ("T", next_triangle, 1)
        next_triangle += 1
        vertices.update((left, right))
        edges.update((edge(owner, left), edge(owner, right), edge(left, right)))
        triangle = frozenset((owner, left, right))
        triangles.append(triangle)
        return owner, left, right

    kind = record[0]
    if kind == "direct3":
        for label in record[1]:
            attach(transported_owner(label, vertex_map, edge_map))
    elif kind == "chain2+direct":
        parent = attach(transported_owner(record[1], vertex_map, edge_map))
        attach(parent[1])
        attach(transported_owner(record[2], vertex_map, edge_map))
    elif kind == "fork":
        parent = attach(transported_owner(record[1], vertex_map, edge_map))
        attach(parent[1])
        attach(parent[1] if record[2] == "same" else parent[2])
    elif kind == "chain3":
        parent = attach(transported_owner(record[1], vertex_map, edge_map))
        child = attach(parent[1])
        attach(child[1])
    else:
        raise AuditError(f"unknown marked-record shape: {kind}")
    require(len(triangles) == 3, "record did not realize three external triangles")

    descendants = {v: set() for v in vertices}
    if decorate:
        # A fixed nontrivial rooted tree at every physical vertex exercises the
        # ownership code.  The symbolic argument below covers arbitrary trees.
        physical_vertices = tuple(sorted(vertices, key=repr))
        for serial, root in enumerate(physical_vertices):
            a = ("R", serial, 0)
            b = ("R", serial, 1)
            c = ("R", serial, 2)
            vertices.update((a, b, c))
            edges.update((edge(root, a), edge(a, b), edge(root, c)))
            descendants[root] = {a, b, c}

    open_vertex = path_vertices[even_connector][opening_position]
    cut_edge = edge(path_vertices[odd_connector][cut_position],
                    path_vertices[odd_connector][cut_position + 1])
    require(open_vertex[0] == "P" and open_vertex in vertices,
            "physical opening vertex is absent")
    require(cut_edge in edges, "physical odd-connector cut edge is absent")

    # Transport the source-side intrinsic triangles through this witness.  This
    # labels components by source side even for the global-swap witness.
    transported_fibres = []
    for source_fibre in DOUBLED_FIBRES:
        target_fibre = frozenset(edge_map[i] for i in source_fibre)
        require(target_fibre in tuple(frozenset(f) for f in DOUBLED_FIBRES),
                "witness did not transport a doubled fibre as a fibre")
        target_index = next(i for i, fibre in enumerate(DOUBLED_FIBRES)
                            if frozenset(fibre) == target_fibre)
        transported_fibres.append(intrinsic[target_index])

    return {
        "vertices": vertices,
        "edges": edges,
        "path_vertices": path_vertices,
        "intrinsic": tuple(intrinsic),
        "source_intrinsic": tuple(transported_fibres),
        "external": tuple(triangles),
        "open_vertex": open_vertex,
        "open_descendants": descendants.get(open_vertex, set()),
        "cut_edge": cut_edge,
        "even_connector": even_connector,
        "odd_connector": odd_connector,
        "lengths": lengths,
    }


def components(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        require(u in adjacency and v in adjacency, "edge endpoint outside vertex set")
        adjacency[u].add(v)
        adjacency[v].add(u)
    answer = []
    unseen = set(vertices)
    while unseen:
        start = min(unseen, key=repr)
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adjacency[u] - seen:
                seen.add(v)
                stack.append(v)
        unseen -= seen
        answer.append(frozenset(seen))
    return tuple(answer)


def is_connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def induced_edges(vertex_set, all_edges):
    return {e for e in all_edges if e[0] in vertex_set and e[1] in vertex_set}


def biconnected_edge_blocks(vertices, edges):
    """Tarjan edge-block decomposition for a finite simple graph."""
    adjacency = {v: [] for v in vertices}
    for e in edges:
        u, v = e
        adjacency[u].append((v, e))
        adjacency[v].append((u, e))
    for value in adjacency.values():
        value.sort(key=lambda item: repr(item[0]))

    discovery = {}
    low = {}
    time = 0
    stack = []
    blocks = []

    def dfs(u, parent_edge=None):
        nonlocal time
        time += 1
        discovery[u] = low[u] = time
        for v, e in adjacency[u]:
            if e == parent_edge:
                continue
            if v not in discovery:
                stack.append(e)
                dfs(v, e)
                low[u] = min(low[u], low[v])
                if low[v] >= discovery[u]:
                    block = set()
                    while stack:
                        popped = stack.pop()
                        block.add(popped)
                        if popped == e:
                            break
                    require(block, "empty biconnected edge block")
                    blocks.append(frozenset(block))
            elif discovery[v] < discovery[u]:
                stack.append(e)
                low[u] = min(low[u], discovery[v])

    for root in sorted(vertices, key=repr):
        if root not in discovery:
            dfs(root)
            require(not stack, "Tarjan edge stack leaked across components")
    return tuple(blocks)


def cyclic_blocks(vertices, edges):
    answer = []
    for block_edges in biconnected_edge_blocks(vertices, edges):
        block_vertices = frozenset(itertools.chain.from_iterable(block_edges))
        if len(block_edges) == 1:
            require(len(block_vertices) == 2, "malformed bridge block")
            continue
        degrees = Counter()
        for u, v in block_edges:
            degrees[u] += 1
            degrees[v] += 1
        require(len(block_edges) == len(block_vertices) and
                set(degrees.values()) == {2},
                "non-cycle biconnected block found")
        answer.append((block_vertices, block_edges))
    return tuple(answer)


def packing_number(triangles):
    best = 0
    for size in range(1, len(triangles) + 1):
        for choice in itertools.combinations(triangles, size):
            if all(left.isdisjoint(right)
                   for left, right in itertools.combinations(choice, 2)):
                best = size
    return best


def shared_cut_connected(triangles):
    if not triangles:
        return False
    if len(triangles) == 1:
        return True
    intersection_edges = {
        edge(i, j) for i, j in itertools.combinations(range(len(triangles)), 2)
        if triangles[i] & triangles[j]
    }
    return is_connected(set(range(len(triangles))), intersection_edges)


def audit_side(side_vertices, all_edges, expected_triangles, intrinsic_triangle):
    side_edges = induced_edges(side_vertices, all_edges)
    require(is_connected(side_vertices, side_edges), "induced side is disconnected")
    beta = len(side_edges) - len(side_vertices) + 1
    blocks = cyclic_blocks(side_vertices, side_edges)
    block_triangles = tuple(block[0] for block in blocks)
    require(all(len(block[0]) == 3 and len(block[1]) == 3 for block in blocks),
            "cyclic block is not a triangle")
    require(Counter(block_triangles) == Counter(expected_triangles),
            "cyclic-block ownership is not exact")
    require(beta == len(blocks), "beta differs from triangular-block count")
    require(intrinsic_triangle in block_triangles,
            "side lost its intrinsic doubled-fibre triangle")
    require(all(len(left & right) <= 1
                for left, right in itertools.combinations(block_triangles, 2)),
            "side is not a cactus")
    require(shared_cut_connected(block_triangles),
            "side triangles are not one shared-cut cluster")
    return {
        "vertices": len(side_vertices),
        "edges": len(side_edges),
        "beta": beta,
        "cyclic_blocks": len(blocks),
        "packing": packing_number(block_triangles),
    }


def audit_case(row, witness, record, even_length, odd_length,
               opening_position, cut_position, decorate=False):
    graph = build_physical_graph(row, witness, record, even_length, odd_length,
                                 opening_position, cut_position, decorate)
    vertices = graph["vertices"]
    edges = graph["edges"]
    deleted = frozenset({graph["open_vertex"]} | graph["open_descendants"])
    require(is_connected(deleted, induced_edges(deleted, edges)),
            "opened vertex plus descendants is not connected")
    require(len(induced_edges(deleted, edges)) == len(deleted) - 1,
            "opened territory is not a tree")

    retained_vertices = set(vertices) - set(deleted)
    retained_edges = induced_edges(retained_vertices, edges)
    require(graph["cut_edge"] in retained_edges,
            "odd cut edge was captured by opening territory")
    split_edges = retained_edges - {graph["cut_edge"]}
    comps = components(retained_vertices, split_edges)
    require(len(comps) == 2, "opened-and-cut graph does not have exactly two components")

    # Order components by the transported source intrinsic triangles.
    ordered = []
    for intrinsic in graph["source_intrinsic"]:
        matches = [component for component in comps if intrinsic <= component]
        require(len(matches) == 1, "intrinsic triangle has ambiguous component owner")
        ordered.append(matches[0])
    require(ordered[0] != ordered[1], "intrinsic triangles lie on the same side")
    sides = tuple(ordered)

    require(set().union(deleted, *sides) == set(vertices) and
            not (set(deleted) & set(sides[0])) and
            not (set(deleted) & set(sides[1])) and
            not (set(sides[0]) & set(sides[1])),
            "vertex territories are not disjoint and exhaustive")

    expected_boundary = {graph["cut_edge"]}
    open_vertex = graph["open_vertex"]
    expected_boundary |= {e for e in edges if open_vertex in e and
                          not set(e) <= set(deleted)}
    actual_boundary = {e for e in edges if not any(set(e) <= set(part)
                      for part in (deleted, sides[0], sides[1]))}
    require(actual_boundary == expected_boundary and len(actual_boundary) == 3,
            "edge partition/boundary ledger is not exactly 2 opening + 1 cut")
    require(sum(len(induced_edges(part, edges)) for part in
                (deleted, sides[0], sides[1])) + len(actual_boundary) == len(edges),
            "edge ownership is not exhaustive")

    expected_side_triangles = []
    metrics = []
    for side_index, side in enumerate(sides):
        external = [triangle for triangle in graph["external"] if triangle <= side]
        require(all(not (triangle & side) or triangle <= side
                    for triangle in graph["external"]),
                "an external triangle was split across territories")
        triangles = (graph["source_intrinsic"][side_index], *external)
        expected_side_triangles.append(triangles)
        metrics.append(audit_side(side, edges, triangles,
                                  graph["source_intrinsic"][side_index]))

    require(sum(len(triangles) - 1 for triangles in expected_side_triangles) == 3,
            "external triangle ownership is not exhaustive")
    ranks = tuple(metric["beta"] for metric in metrics)
    require(min(ranks) >= 1 and sum(ranks) == 5,
            "side ranks are not positive and summing five")
    expected_ranks = tuple(1 + record_top_sides(record).count(side)
                           for side in (0, 1))
    require(ranks == expected_ranks,
            "physical side ranks disagree with decorated-record ownership")
    return {
        "ranks": ranks,
        "packing": tuple(metric["packing"] for metric in metrics),
        "metrics": tuple(metrics),
        "boundary": tuple(sorted(expected_boundary, key=repr)),
    }


def symbolic_remnant_audit():
    """Exact all-length reduction, with no finite upper bound on remnants."""
    # If L_e is even and internal position j is deleted, the retained path
    # lengths are alpha=j-1 and beta=L_e-j-1: nonnegative, even total.
    # If L_o is odd and edge k is cut, the retained lengths are gamma=k and
    # delta=L_o-k-1: nonnegative, even total.  Conversely every such pair
    # yields an admissible connector length and position.
    for total in range(0, 14, 2):
        for left in range(total + 1):
            right = total - left
            even_length = left + right + 2
            opening = left + 1
            require(even_length % 2 == 0 and 1 <= opening < even_length,
                    "symbolic even-remnant converse failed")
            odd_length = left + right + 1
            cut = left
            require(odd_length % 2 == 1 and 0 <= cut < odd_length,
                    "symbolic odd-remnant converse failed")

    # A pendant path of q edges contributes exactly q new vertices and q
    # edges.  The same is true for every one-root tree (edges = nonroot
    # vertices).  Thus neither changes beta.  Starting with r triangles glued
    # one at a time at one cut vertex gives V=2r+1, E=3r, beta=r.
    for r in range(1, 5):
        base_v, base_e = 2 * r + 1, 3 * r
        for alpha, gamma, tree_vertices in itertools.product(range(5), repeat=3):
            vertices = base_v + alpha + gamma + tree_vertices
            edges = base_e + alpha + gamma + tree_vertices
            require(edges - vertices + 1 == r,
                    "symbolic pendant material changed beta")
    return {
        "even": "alpha,beta>=0; alpha+beta even; L=alpha+beta+2",
        "odd": "gamma,delta>=0; gamma+delta even; L=gamma+delta+1",
        "effect": "each remnant/rooted tree adds equally many vertices and edges",
    }


def audit():
    automorphisms = genuine_automorphisms()
    require(len(automorphisms) == 16, "genuine automorphism-pair count is not 16")
    anchors = tuple(sorted({act_on_row(BASE_ROW, edge_map)
                            for _, edge_map in automorphisms}))
    require(anchors == EXPECTED_ANCHORS, "exceptional physical anchor orbit changed")
    witnesses = {
        row: tuple(w for w in automorphisms if act_on_row(BASE_ROW, w[1]) == row)
        for row in anchors
    }
    require(all(len(value) == 2 for value in witnesses.values()),
            "an anchor does not have exactly two genuine witnesses")
    records = base_records()

    rank_profiles = Counter()
    packing_profiles = Counter()
    one_sided_records = 0
    balanced_records = 0
    minimal_strong_failure = None

    identity = ((0, 1, 2, 3), (0, 1, 2, 3, 4, 5))
    require(identity in witnesses[BASE_ROW], "identity base witness disappeared")
    for record_index, record in enumerate(records):
        result = audit_case(BASE_ROW, identity, record, 2, 1, 1, 0)
        rank_profiles[result["ranks"]] += 1
        packing_profiles[(result["ranks"], result["packing"])] += 1
        if set(result["ranks"]) == {1, 4}:
            one_sided_records += 1
        else:
            balanced_records += 1
            if minimal_strong_failure is None:
                minimal_strong_failure = {
                    "record_index": record_index,
                    "record": record,
                    "row": BASE_ROW,
                    "witness": identity,
                    "even_length": 2,
                    "opening_position": 1,
                    "odd_length": 1,
                    "cut_position": 0,
                    "ranks": result["ranks"],
                    "packing": result["packing"],
                    "side_metrics": result["metrics"],
                    "boundary": result["boundary"],
                }

    require(rank_profiles == Counter({(4, 1): 28, (3, 2): 27,
                                      (2, 3): 27, (1, 4): 28}),
            "record-level rank profile changed")
    require(one_sided_records == 56 and balanced_records == 54,
            "one-sided/balanced record census changed")
    require(minimal_strong_failure is not None and
            minimal_strong_failure["record"] == ("direct3", ("A", "A", "C")) and
            minimal_strong_failure["ranks"] == (3, 2),
            "minimal strong-claim counterexample changed")

    concrete_cases = 0
    for row in anchors:
        for witness in witnesses[row]:
            for record in records:
                for even_length in EVEN_LENGTH_PROBES:
                    for opening in range(1, even_length):
                        for odd_length in ODD_LENGTH_PROBES:
                            for cut in range(odd_length):
                                audit_case(row, witness, record,
                                           even_length, odd_length,
                                           opening, cut)
                                concrete_cases += 1
    require(concrete_cases == 8 * 2 * 110 * 9 * 9,
            "concrete connector-position case count changed")

    decorated_cases = 0
    for row in anchors:
        for witness in witnesses[row]:
            for record in records:
                audit_case(row, witness, record, 2, 1, 1, 0, decorate=True)
                decorated_cases += 1
    require(decorated_cases == 8 * 2 * 110,
            "rooted-decoration case count changed")

    symbolic = symbolic_remnant_audit()
    return {
        "anchors": anchors,
        "automorphisms": automorphisms,
        "witnesses": witnesses,
        "records": records,
        "rank_profiles": rank_profiles,
        "packing_profiles": packing_profiles,
        "one_sided_records": one_sided_records,
        "balanced_records": balanced_records,
        "minimal_strong_failure": minimal_strong_failure,
        "concrete_cases": concrete_cases,
        "decorated_cases": decorated_cases,
        "symbolic": symbolic,
    }


def main():
    result = audit()
    failure = result["minimal_strong_failure"]
    output = "\n".join((
        "OPEN R31-S physical coupled-split audit: exact structural checks passed",
        "physical scope: 8 anchors; 16 genuine witnesses; 110 decorated records",
        f"connector probes: {result['concrete_cases']} cases "
        "(even L=2,4,6/all internal openings; odd L=1,3,5/all edge cuts)",
        f"rooted ownership probes: {result['decorated_cases']} cases with a nontrivial tree at every vertex",
        "all-length certificate: arbitrary connector remnants are pendant paths; each adds V=E",
        "uniform conclusion: two connected induced shared-cut triangular cacti; "
        "each has its intrinsic triangle; ranks >=1 and sum 5",
        "record rank profiles: " + repr(dict(sorted(result["rank_profiles"].items()))),
        f"one-sided rank-(4,1)/(1,4) records: {result['one_sided_records']}; "
        f"balanced rank-(3,2)/(2,3) records: {result['balanced_records']}",
        "STRONG CLAIM 'always one rank-4 side plus one rank-1 side': FALSE",
        "minimal counterexample: row=010011; identity witness; L_even=2/open=1; "
        "L_odd=1/cut=0; record=direct3(A,A,C); ranks=(3,2); packings="
        + repr(failure["packing"]),
        "minimal side ledgers: " + repr(failure["side_metrics"]),
        "synthetic diamond diagnostic used: no",
        "status: OPEN/nonpromotional structural audit only",
    ))
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output,
                "normal and optimized audit output differ")
    print(output)


if __name__ == "__main__":
    main()
