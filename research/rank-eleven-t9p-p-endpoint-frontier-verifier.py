#!/usr/bin/env python3
"""Fail-closed physical-owner census for the rank-eleven T^9P | P endpoint.

The executable projects the triangular-hull slice bijectively to the hardened
P | A_9 | P verifier and realizes every ordinary and repaired plan as an
exhaustive physical owner certificate.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            f"cannot load census dependency {filename}")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


INCIDENCE = load_module(
    "rank_eleven_t9p_p_incidence", "nonacyclic-fully-shared-incidence-census.py"
)
ROOTS = load_module(
    "rank_eleven_t9p_p_roots", "nonacyclic-t7p-last-bridge-conservative.py"
)
CORE = load_module("geometry_router_owner_core", "geometry_router_owner_core.py")
A9 = load_module(
    "rank_eleven_a9_two_interface_verifier", "rank-eleven-a9-two-interface-verifier.py"
)

EXPECTED_ALL_BY_CUT = Counter(
    {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2201, 7: 2393, 8: 1372, 9: 321}
)
EXPECTED_LEAF_BY_CUT = Counter(
    {1: 1, 2: 8, 3: 56, 4: 232, 5: 632, 6: 1054, 7: 1031, 8: 512, 9: 98}
)
EXPECTED_ROW_DIGESTS = {
    "all-incidence": "ac73c8ccfdbbae914c79499b5c4fc8cf8575ec8c085d928d151c996a704be6a4",
    "leaf-incidence": "7b61358ef6f13c003a24c97e5cb05b6e497f7fef386188b9a4f93630e1b74f84",
    "triangular-rows": "72078c6c3d7a7a7be50c89e423484353ad828627230f92bf3eb6d75ace81dd41",
    "private-rows": "2f4bac13f4bd512a7ebcd8d7ea784d600e8ece4bde4d2efd8c9721609f37fb0e",
    "combined-rows": "73946e20dbfe1f3569ef79db036ba7d869ea367dbf57000a9d26874c3e0f9802",
}
EXPECTED_GEOMETRY_DIGESTS = {
    "incidence-geometry": "f1db45b36e04eb68ddf6d549e1daf75c0cdae65b22052505e98abf5d4e9ca530",
    "triangular-connectors": "3ba0f596836c4421986d8f8c3e97887dc87c84e6a1902975383642329f3af8f8",
    "private-connectors": "d9d3b59003b5d6827d82011eb5c120c6776e7c648576deb4c01453341215d3a1",
    "combined-geometry": "3da4ebec400a236a10ffb242603b485c7b549a2503fa5c4ee061dcc7afa70b7b",
}
REPORTED_SEVENTEEN_DIGEST = (
    17, "fcf002bb4150db6dc4c5b19f2e9d76b05de066898413b28ee11c4e0a9619747c"
)
BLUEPRINT = HERE / "rank-eleven-t9p-p-seventeen-repair-blueprint-2026-07-28.md"
EXPECTED_BLUEPRINT_DIGEST = "d9b9820780624eb9215cd569105b84adeaf3ea0bd016410cc21ce38b85800063"
EXPECTED_PROJECTION_DIGEST = "9897c86b3e197ea3da1fbc2e0ef5ed4440e53bec0d8ac34d6024466c26ccf1a1"
EXPECTED_PROJECTED_PLAN_DIGEST = "c3fd37ebc47de29a7f49471c6ecd61a280581fe30c3fdf72905548345d814566"
EXPECTED_PHYSICAL_CERTIFICATE_DIGEST = "63305ff27b19d07bd705eec8f489dcfcfd12cc8cc129dbe93cf914d1c29c4a1a"
EXPECTED_PRIVATE_CERTIFICATE_DIGEST = "815040d4da58efb5edb5660de47d14d4012eb6245afcabb5b77c98e2a8a8e43d"
EXPECTED_RESIDUAL_CERTIFICATE_DIGEST = "740a1385503bdf58761be38057ca9d548f85289183ef4a4c515fbc6038398da3"


CyclicVertex = CORE.CyclicVertex
CycleGeometry = CORE.CycleGeometry
EXPECTED_BLOCK_CACHE = {}


@dataclass(frozen=True)
class Connector:
    label: str
    pentagon_root: CyclicVertex
    hull_position: CyclicVertex
    path_vertices: tuple[str, ...]
    remnant: str
    edges: tuple[tuple[object, object], ...]
    remnant_anchor: object


@dataclass(frozen=True)
class PrivateOrbit:
    distance: int
    positions: tuple[CyclicVertex, ...]
    stabilizer_images: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class PrivateTheorem:
    owner: str
    theorem: str
    hypothesis: str
    cycles: tuple[int, ...]
    pentagons: tuple[str, ...]
    bound: object


@dataclass(frozen=True)
class PrivateCertificate:
    row_id: str
    distance: int
    operation: str
    router: int | None
    open_vertex: CyclicVertex | None
    two_p_cycles: tuple[int, ...]
    strict_cycles: tuple[int, ...]
    interval_vertices: tuple[tuple[object, ...], ...]
    interval_owners: tuple[str, ...]
    theorems: tuple[PrivateTheorem, ...]
    bound: object
    vertices: tuple[object, ...]
    edges: tuple[tuple[object, object], ...]
    vertex_owners: tuple[tuple[object, str], ...]
    attachment_owners: tuple[tuple[object, str], ...]


@dataclass(frozen=True)
class ResidualCertificate:
    row_id: str
    operation: str
    router: int | None
    open_vertex: object | None
    interval_vertices: tuple[tuple[object, ...], ...]
    interval_owners: tuple[str, ...]
    vertices: tuple[object, ...]
    edges: tuple[tuple[object, object], ...]
    vertex_owners: tuple[tuple[object, str], ...]
    attachment_owners: tuple[tuple[object, str], ...]


def digest(records):
    return sha256(("\n".join(records) + "\n").encode("ascii")).hexdigest()


def file_digest(path):
    require(path.is_file(), f"missing repair blueprint: {path.name}")
    return sha256(path.read_bytes()).hexdigest()


def unique_map(records, expected_domain, label):
    return CORE.exact_owner_map(records, expected_domain, label)


def make_cycle(label, length, cut_bindings=()):
    require(length in (3, 5), "unsupported cycle length")
    bindings = tuple(cut_bindings)
    require(len(bindings) <= length and len(bindings) == len(set(bindings)),
            "cycle cut bindings are not unique")
    vertices = tuple(
        CyclicVertex(label, index, "cut" if index < len(bindings) else "private",
                     bindings[index] if index < len(bindings) else None)
        for index in range(length)
    )
    edges = tuple((vertices[index], vertices[(index + 1) % length])
                  for index in range(length))
    geometry = CycleGeometry(label, length, vertices, edges)
    verify_cycle(geometry, bindings)
    return geometry


def verify_cycle(geometry, cut_bindings):
    CORE.verify_cycle(geometry)
    cut_vertices = tuple(vertex for vertex in geometry.vertices if vertex.role == "cut")
    private_vertices = tuple(vertex for vertex in geometry.vertices if vertex.role == "private")
    require(tuple(vertex.cut for vertex in cut_vertices) == tuple(cut_bindings),
            "cycle cut vertices do not match incidence bindings")
    require(all(vertex.cut is None for vertex in private_vertices),
            "private cyclic vertex carries a cut")


def consecutive_intervals(geometry):
    """Enumerate every ordered two- and three-part cyclic interval partition."""
    counts = (2, 3) if geometry.length == 3 else (2,)
    return CORE.consecutive_intervals(geometry, counts)


def verify_intervals(geometry, intervals):
    CORE.verify_intervals(geometry, intervals)


def rooted_c5_stabilizer():
    """Derive the rooted C5 dihedral stabilizer by testing all D5 actions."""
    rotations = tuple(tuple((index + shift) % 5 for index in range(5))
                      for shift in range(5))
    reflections = tuple(tuple((shift - index) % 5 for index in range(5))
                        for shift in range(5))
    dihedral = tuple(dict.fromkeys(rotations + reflections))
    require(len(dihedral) == 10, "D5 action does not have order ten")
    stabilizer = tuple(action for action in dihedral if action[0] == 0)
    require(len(stabilizer) == 2 and all(action[0] == 0 for action in stabilizer),
            "rooted C5 stabilizer is not the order-two reflection group")
    return stabilizer


def rooted_private_orbits(pentagon):
    stabilizer = rooted_c5_stabilizer()
    remaining = set(range(1, 5))
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = tuple(sorted({action[seed] for action in stabilizer}))
        require(set(orbit) <= remaining, "rooted stabilizer orbit overlaps an earlier orbit")
        distance = min(seed, 5 - seed)
        orbits.append(PrivateOrbit(
            distance, tuple(pentagon.vertices[index] for index in orbit), stabilizer))
        remaining -= set(orbit)
    require(tuple(orbit.distance for orbit in orbits) == (1, 2) and
            Counter(vertex for orbit in orbits for vertex in orbit.positions) ==
            Counter(pentagon.vertices[1:]),
            "rooted C5 private distance orbits are not exact")
    return tuple(orbits)


def hull_position_for_mark(geometries, mark):
    if mark.kind == "cut":
        candidates = tuple(vertex for geometry in geometries
                           for vertex in geometry.vertices if vertex.cut == mark.vertex)
        require(candidates, "cut mark has no concrete cyclic position")
        return candidates[0]
    candidates = tuple(vertex for vertex in geometries[mark.vertex].vertices
                       if vertex.role == "private")
    require(candidates, "private triangle mark has no concrete cyclic position")
    return candidates[0]


def incidence_geometry(signature, tree):
    adj = INCIDENCE.adjacency(tree)
    geometries = []
    for cycle, color in enumerate(tree.colors):
        cuts = tuple(sorted(adj[cycle]))
        geometry = make_cycle(f"{signature}:C{cycle}:{color}", 3 if color == "T" else 5, cuts)
        geometries.append(geometry)
        if color == "T":
            partitions = consecutive_intervals(geometry)
            require(any(sorted(map(len, item)) == [1, 2] for item in partitions),
                    "triangle has no concrete (1,2) interval partition")
            require(any(sorted(map(len, item)) == [1, 1, 1] for item in partitions),
                    "triangle has no concrete singleton interval partition")
    cut_owners = []
    for cut in range(len(tree.colors), len(adj)):
        positions = tuple(vertex for geometry in geometries for vertex in geometry.vertices
                          if vertex.cut == cut)
        require(len(positions) == len(adj[cut]), "cut incidence lacks one concrete position per cycle")
        cut_owners.append((cut, positions))
    unique_map(cut_owners, range(len(tree.colors), len(adj)), "incidence cut-position ledger")
    return tuple(geometries)


def connector_for_mark(label, pentagon, hull_position, row_id):
    root = pentagon.vertices[0]
    path = (f"{row_id}:{label}:path-root", f"{row_id}:{label}:path-hull")
    require(len(path) == len(set(path)), "connector path repeats a symbolic attachment")
    remnant = f"{row_id}:{label}:remnant"
    edges = ((root, path[0]), (path[0], path[1]), (path[1], hull_position),
             (path[1], remnant))
    connector = Connector(label, root, hull_position, path, remnant, edges, path[1])
    verify_connector(connector, pentagon, hull_position)
    return connector


def connector_specification(label, pentagon_root, hull_position, row_id):
    """Reconstruct the required connector domain without reading a certificate."""
    path = (f"{row_id}:{label}:path-root", f"{row_id}:{label}:path-hull")
    remnant = f"{row_id}:{label}:remnant"
    vertices = path + (remnant,)
    edges = ((pentagon_root, path[0]), (path[0], path[1]),
             (path[1], hull_position), (path[1], remnant))
    return vertices, edges, path[1]


def verify_connector(connector, pentagon, hull_position):
    require(connector.pentagon_root in pentagon.vertices and
            connector.pentagon_root == pentagon.vertices[0],
            "connector root is not the named pentagon root")
    require(connector.hull_position == hull_position,
            "connector is not bound to its concrete hull position")
    require(len(connector.path_vertices) >= 1 and
            len(connector.path_vertices) == len(set(connector.path_vertices)),
            "connector path is empty or repeats an attachment object")
    require(connector.remnant not in connector.path_vertices,
            "connector remnant aliases a path vertex")
    expected = ((connector.pentagon_root, connector.path_vertices[0]),
                (connector.path_vertices[0], connector.path_vertices[1]),
                (connector.path_vertices[1], connector.hull_position),
                (connector.path_vertices[1], connector.remnant))
    require(connector.edges == expected, "connector chain edges are incomplete or out of order")
    require(connector.remnant_anchor == connector.path_vertices[1] and
            (connector.remnant_anchor, connector.remnant) in connector.edges,
            "connector remnant has no explicit chain anchor")


def geometry_text(geometries):
    return repr(tuple((geometry.label,
                       tuple((vertex.index, vertex.role, vertex.cut)
                             for vertex in geometry.vertices))
                       for geometry in geometries))


def expected_incidence_geometry_text(signature, tree):
    """Serialize canonical cycle domains directly from the incidence row."""
    adjacency = INCIDENCE.adjacency(tree)
    records = []
    for cycle, color in enumerate(tree.colors):
        cuts = tuple(sorted(adjacency[cycle]))
        length = 3 if color == "T" else 5
        vertices = tuple((index, "cut" if index < len(cuts) else "private",
                          cuts[index] if index < len(cuts) else None)
                         for index in range(length))
        records.append((f"{signature}:C{cycle}:{color}", vertices))
    return repr(tuple(records))


def connector_text(row_id, connector):
    return repr((row_id, connector.label, connector.pentagon_root.index,
                 connector.hull_position.cycle, connector.hull_position.index,
                  connector.path_vertices, connector.remnant, connector.edges,
                  connector.remnant_anchor))


def expected_connector_text(row_id, label, pentagon_root, hull_position):
    vertices, edges, remnant_anchor = connector_specification(
        label, pentagon_root, hull_position, row_id
    )
    path = vertices[:-1]
    remnant = vertices[-1]
    return repr((row_id, label, pentagon_root.index, hull_position.cycle,
                 hull_position.index, path, remnant, edges, remnant_anchor))


def expected_blocks(signature, tree):
    cached = EXPECTED_BLOCK_CACHE.get(signature)
    if cached is None:
        cached = (incidence_geometry(signature, tree),
                  make_cycle(f"{signature}:remote-P1", 5, ()))
        EXPECTED_BLOCK_CACHE[signature] = cached
    return cached


def expected_triangular_connector_text(signature, tree, row_id, root_mark):
    geometries, remote = expected_blocks(signature, tree)
    hull = hull_position_for_mark(geometries, root_mark)
    return expected_connector_text(row_id, "P1", remote.vertices[0], hull)


def expected_private_connector_text(signature, tree, row_id, hull_index):
    geometries, remote = expected_blocks(signature, tree)
    p0 = tree.colors.index("P")
    hull = geometries[p0].vertices[hull_index]
    require(hull.role == "private", "expected private connector hull is not private")
    return expected_connector_text(row_id, "P1", remote.vertices[0], hull)


def projection_structure(tree):
    adj = INCIDENCE.adjacency(tree)
    p0 = tree.colors.index("P")
    require(len(adj[p0]) == 1, "projection requires a clustered-P incidence leaf")
    clustered_cut = adj[p0][0]
    clustered_triangles = tuple(cycle for cycle in adj[clustered_cut] if cycle != p0)
    require(clustered_triangles and
            all(tree.colors[cycle] == "T" for cycle in clustered_triangles),
            "clustered-P leaf cut has no triangular hull neighbor")
    suppress_clustered_cut = len(clustered_triangles) == 1
    old_triangles = tuple(cycle for cycle, color in enumerate(tree.colors) if color == "T")
    old_cuts = tuple(cut for cut in range(len(tree.colors), len(adj))
                     if cut != clustered_cut or not suppress_clustered_cut)
    return adj, p0, clustered_cut, clustered_triangles, suppress_clustered_cut, \
        old_triangles, old_cuts


def canonical_projection_maps(tree):
    """Derive the sole allowed relabeling from sorted original vertex labels."""
    (*_, old_triangles, old_cuts) = projection_structure(tree)
    cycle_map = {old: new for new, old in enumerate(old_triangles)}
    cut_map = {old: 9 + index for index, old in enumerate(old_cuts)}
    return cycle_map, cut_map


def incidence_symmetric_triangle_pair(tree):
    """Find two original triangles with identical incidence neighborhoods."""
    adj = INCIDENCE.adjacency(tree)
    triangles = tuple(cycle for cycle, color in enumerate(tree.colors) if color == "T")
    for index, first in enumerate(triangles):
        for second in triangles[index + 1:]:
            if tuple(sorted(adj[first])) == tuple(sorted(adj[second])):
                return first, second
    return None


def verify_geometry_incidence_binding(signature, tree, geometries):
    """Bind every named cyclic position to one original incidence-tree edge."""
    adj = INCIDENCE.adjacency(tree)
    require(len(geometries) == len(tree.colors),
            "geometry ledger does not cover every original cycle")
    bound_edges = []
    for cycle, (color, geometry) in enumerate(zip(tree.colors, geometries)):
        expected_label = f"{signature}:C{cycle}:{color}"
        expected_cuts = tuple(sorted(adj[cycle]))
        require(geometry.label == expected_label,
                "cycle geometry is attached to the wrong original cycle")
        require(geometry.length == (3 if color == "T" else 5),
                "cycle geometry length disagrees with original cycle color")
        CORE.verify_cycle(geometry)
        require(all(vertex.cycle == expected_label and vertex.index == index
                    for index, vertex in enumerate(geometry.vertices)),
                "cyclic vertex identity aliases another geometry")
        cut_vertices = tuple(vertex for vertex in geometry.vertices if vertex.role == "cut")
        private_vertices = tuple(vertex for vertex in geometry.vertices
                                 if vertex.role == "private")
        require(tuple(vertex.cut for vertex in cut_vertices) == expected_cuts,
                "geometry cut labels disagree with original incidence identities")
        require(all(vertex.cut is None for vertex in private_vertices),
                "private geometry position aliases an incidence cut")
        bound_edges.extend((cycle, vertex.cut) for vertex in cut_vertices)
    require(Counter(bound_edges) == Counter(tree.edges),
            "geometry positions do not bind exactly to original incidence edges")


def verify_projection_binding(signature, tree, geometries, projected_tree,
                              cycle_map, cut_map):
    """Bind relabeling maps and projected edges to the original T9P object."""
    verify_geometry_incidence_binding(signature, tree, geometries)
    (_, p0, clustered_cut, _, suppress_clustered_cut,
     old_triangles, old_cuts) = projection_structure(tree)
    cycles = CORE.exact_relabel_map(
        tuple(cycle_map.items()), old_triangles, range(9), "projection cycle map"
    )
    cuts = CORE.exact_relabel_map(
        tuple(cut_map.items()), old_cuts, range(9, 9 + len(old_cuts)),
        "projection cut map"
    )
    canonical_cycles, canonical_cuts = canonical_projection_maps(tree)
    require(cycles == canonical_cycles,
            "projection cycle map differs from canonical original-label map")
    require(cuts == canonical_cuts,
            "projection cut map differs from canonical original-label map")
    expected_edges = tuple(sorted(
        (cycles[cycle], cuts[cut]) for cycle, cut in tree.edges
        if cycle != p0 and (cut != clustered_cut or not suppress_clustered_cut)
    ))
    require(projected_tree.colors == ("T",) * 9,
            "projected tree does not have exactly nine triangles")
    require(projected_tree.edges == expected_edges,
            "projected edges disagree with original incidence identities and maps")


def triangular_projection(tree, root_mark):
    """Delete the clustered leaf P and project both interfaces onto A9."""
    (adj, p0, clustered_cut, clustered_triangles, suppress_clustered_cut,
     old_triangles, old_cuts) = projection_structure(tree)
    cycle_map, cut_map = canonical_projection_maps(tree)
    projected_tree = A9.BASE.BASE.Tree(
        ("T",) * 9,
        tuple(sorted((cycle_map[cycle], cut_map[cut])
                     for cycle, cut in tree.edges
                     if cycle != p0 and
                     (cut != clustered_cut or not suppress_clustered_cut))),
    )
    clustered = (
        A9.BASE.Position("private", cycle_map[clustered_triangles[0]], 0)
        if suppress_clustered_cut
        else A9.BASE.Position("cut", cut_map[clustered_cut])
    )
    if root_mark.kind == "cut":
        remote = (clustered if root_mark.vertex == clustered_cut else
                  A9.BASE.Position("cut", cut_map[root_mark.vertex]))
    else:
        require(root_mark.vertex in cycle_map,
                "triangular-hull root does not lie on a retained triangle")
        slot = 1 if (suppress_clustered_cut and
                     root_mark.vertex == clustered_triangles[0]) else 0
        remote = A9.BASE.Position("private", cycle_map[root_mark.vertex], slot)
    signature = A9.BASE.marked_signature(projected_tree, (clustered, remote))
    return signature, projected_tree, (clustered, remote), cycle_map, cut_map


def projected_vertex(position, router, geometries, cycle_inverse, cut_inverse):
    old_router = cycle_inverse[router]
    geometry = geometries[old_router]
    if position.kind == "cut":
        old_cut = cut_inverse[position.vertex]
        matches = tuple(vertex for vertex in geometry.vertices if vertex.cut == old_cut)
    else:
        require(position.vertex == router, "projected private owner is on another router")
        retained_cuts = set(cut_inverse.values())
        matches = tuple(vertex for vertex in geometry.vertices
                        if vertex.cut not in retained_cuts)
        require(0 <= position.slot < len(matches), "projected private slot is invalid")
        matches = (matches[position.slot],)
    require(len(matches) == 1, "A9 position does not project to one concrete T9P vertex")
    return matches[0]


def verify_projected_plan(plan, geometries, cycle_map, cut_map):
    """Realize every A9 router interval on the corresponding T9P triangles."""
    cycle_inverse = {new: old for old, new in cycle_map.items()}
    cut_inverse = {new: old for old, new in cut_map.items()}
    require(len(cycle_inverse) == 9 and len(cut_inverse) == len(cut_map),
            "projection relabeling is not bijective")
    records = []
    for split in plan.splits:
        geometry = geometries[cycle_inverse[split.router]]
        intervals = tuple(
            tuple(projected_vertex(position, split.router, geometries,
                                   cycle_inverse, cut_inverse)
                  for position in positions)
            for positions, _ in split.owners
        )
        CORE.verify_router_owner_split(
            geometry, intervals, tuple(range(len(intervals))), split.interval_sizes
        )
        records.append(repr((split.router, split.active, split.interval_sizes,
                             tuple(tuple(vertex.index for vertex in interval)
                                   for interval in intervals))))
    return tuple(records)


def projected_owner_resolver(projected_tree, plan, marked_positions):
    """Derive final packet owners from recursive splits, never packet demands."""
    adjacency = A9.BASE.BASE.adjacency(projected_tree)
    split_by_active = {frozenset(split.active): split for split in plan.splits}
    terminals = {frozenset(packet.cycles): index for index, packet in enumerate(plan.packets)
                 if packet.cycles}
    root = frozenset(range(9))

    def descend(active, site):
        if active in terminals:
            return terminals[active]
        require(active in split_by_active, "physical owner reaches no terminal packet")
        split = split_by_active[active]
        matches = []
        for interval_index, (positions, cycles) in enumerate(split.owners):
            child = frozenset(cycles)
            if site in positions:
                matches.append((interval_index, child))
            elif site.kind == "private" and site.vertex in cycles:
                matches.append((interval_index, child))
            elif site.kind == "cut" and set(adjacency[site.vertex]) & set(cycles):
                matches.append((interval_index, child))
        require(len(matches) == 1, "physical recursive adhesion is ambiguous")
        interval_index, child = matches[0]
        if child:
            return descend(child, site)
        return ("empty", active, interval_index)

    empty_tokens = tuple(sorted({descend(root, position) for position in marked_positions
                                 if not isinstance(descend(root, position), int)},
                                key=repr))
    empty_owners = tuple(index for index, packet in enumerate(plan.packets)
                         if not packet.cycles)
    require(len(empty_tokens) == len(empty_owners),
            "hostile-only physical intervals and terminals differ")
    empty_map = dict(zip(empty_tokens, empty_owners))

    def resolve(site):
        owner = descend(root, site)
        if not isinstance(owner, int):
            require(owner in empty_map, "hostile-only physical interval has no owner")
            return empty_map[owner]
        return owner

    return resolve


def physical_vertex(value):
    return CORE.CutSite(value.cut) if isinstance(value, CyclicVertex) and value.cut is not None else value


def physical_graph_from_parts(geometries, remote, connector_vertices, connector_edges):
    """Canonicalize one submitted or independently reconstructed physical graph."""
    vertices = []
    edges = []
    for geometry in geometries + (remote,):
        vertices.extend(physical_vertex(vertex) for vertex in geometry.vertices)
        edges.extend((physical_vertex(left), physical_vertex(right))
                     for left, right in geometry.edges)
    vertices.extend(connector_vertices)
    edges.extend((physical_vertex(left), physical_vertex(right))
                 for left, right in connector_edges)
    return tuple(dict.fromkeys(vertices)), tuple(edges)


def reconstruct_expected_physical_graph(signature, tree, row_id, root_mark):
    """Derive the graph solely from incidence data and canonical block specs."""
    expected_geometries, expected_remote = expected_blocks(signature, tree)
    hull_position = hull_position_for_mark(expected_geometries, root_mark)
    connector_vertices, connector_edges, _ = connector_specification(
        "P1", expected_remote.vertices[0], hull_position, row_id
    )
    vertices, edges = physical_graph_from_parts(
        expected_geometries, expected_remote, connector_vertices, connector_edges
    )
    return vertices, edges, vertices


def reconstruct_expected_private_graph(signature, tree, row_id, hull_index):
    expected_geometries, expected_remote = expected_blocks(signature, tree)
    p0 = tree.colors.index("P")
    hull_position = expected_geometries[p0].vertices[hull_index]
    require(hull_position.role == "private",
            "private certificate connector does not enter a private P0 vertex")
    connector_vertices, connector_edges, _ = connector_specification(
        "P1", expected_remote.vertices[0], hull_position, row_id
    )
    vertices, edges = physical_graph_from_parts(
        expected_geometries, expected_remote, connector_vertices, connector_edges
    )
    return vertices, edges, vertices


def canonical_private_router(tree):
    adjacency = INCIDENCE.adjacency(tree)
    p0 = tree.colors.index("P")
    root = adjacency[p0][0]
    cuts = tuple(range(len(tree.colors), len(adjacency)))
    require(len(cuts) > 1, "private router requested for a bouquet")
    target = min(cut for cut in cuts if cut != root)
    parent = {root: None}
    queue = [root]
    for vertex in queue:
        if vertex == target:
            break
        for neighbor in sorted(adjacency[vertex]):
            if neighbor not in parent:
                parent[neighbor] = vertex
                queue.append(neighbor)
    require(target in parent, "private router target is unreachable")
    path = []
    vertex = target
    while vertex is not None:
        path.append(vertex)
        vertex = parent[vertex]
    path.reverse()
    require(len(path) >= 3 and path[1] < len(tree.colors) and
            tree.colors[path[1]] == "T",
            "first private path router is not a triangle")
    router = path[1]
    seen = {root}
    queue = [root]
    for vertex in queue:
        for neighbor in adjacency[vertex]:
            if neighbor != router and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    x_cycles = tuple(sorted(vertex for vertex in seen
                            if vertex < len(tree.colors) and tree.colors[vertex] == "T"))
    strict_cycles = tuple(sorted(set(range(9)) - {router} - set(x_cycles)))
    root_vertex = next(vertex for vertex in adjacency[router] if vertex == root)
    require(root_vertex == root, "private router lacks its root-cut singleton")
    return router, root, x_cycles, strict_cycles


def private_theorems(two_p_cycles, strict_cycles, bouquet=False):
    """Independently classify the two terminal territories and exact ledger."""
    if bouquet:
        retained = PrivateTheorem(
            "A9P1", "one-hostile-packing-one",
            "nine pairwise-intersecting triangles and complete P1 connector",
            tuple(range(9)), ("P1",), A9.Bound(A9.Fraction(9), 1, True),
        )
        opened = PrivateTheorem(
            "opened-P0", "nonempty-tree-exact",
            "one opened P0 vertex with its rooted attachment",
            (), (), A9.Bound(A9.Fraction(-1), 0, False),
        )
        return (retained, opened), retained.bound + opened.bound
    rank = len(two_p_cycles) + 2
    require(2 <= rank <= 9, "private two-P theorem rank is outside 2..9")
    if rank <= 3:
        theorem = "connected-rank-2/3-nonnegative"
        bound = A9.ZERO
    else:
        theorem = "connected-rank-4..9-strict"
        bound = A9.Bound(A9.Fraction(0), 0, True)
    two_p = PrivateTheorem(
        "two-P", theorem,
        f"complete connected cyclic rank {rank} with P0 and P1",
        tuple(two_p_cycles), ("P0", "P1"), bound,
    )
    strict = PrivateTheorem(
        "strict", "pure-triangular-strict",
        "nonempty connected triangular cactus", tuple(strict_cycles), (),
        A9.Bound(A9.Fraction(0), 0, True),
    )
    return (two_p, strict), two_p.bound + strict.bound


def expected_private_owner_map(signature, tree, row_id, distance):
    """Derive every physical owner from canonical intervals and branch components."""
    geometries, remote = expected_blocks(signature, tree)
    p0 = tree.colors.index("P")
    expected_vertices, _, _ = reconstruct_expected_private_graph(
        signature, tree, row_id, distance
    )
    adjacency = INCIDENCE.adjacency(tree)
    if len(adjacency) - len(tree.colors) == 1:
        open_index = 3 if distance == 1 else 4
        open_vertex = physical_vertex(geometries[p0].vertices[open_index])
        owners = {vertex: "opened-P0" if vertex == open_vertex else "A9P1"
                  for vertex in expected_vertices}
        return owners, (), (), tuple(range(9)), (), geometries[p0].vertices[open_index]

    router, root_cut, two_p_cycles, strict_cycles = canonical_private_router(tree)
    router_geometry = geometries[router]
    root_site = CORE.CutSite(root_cut)
    intervals = ((root_site,), tuple(physical_vertex(vertex)
                                     for vertex in router_geometry.vertices
                                     if physical_vertex(vertex) != root_site))
    interval_owners = ("two-P", "strict")
    owner_sets = {owner: set(interval) for owner, interval in zip(interval_owners, intervals)}
    for cycle in two_p_cycles:
        owner_sets["two-P"].update(physical_vertex(vertex)
                                   for vertex in geometries[cycle].vertices)
    for cycle in strict_cycles:
        owner_sets["strict"].update(physical_vertex(vertex)
                                    for vertex in geometries[cycle].vertices)
    owner_sets["two-P"].update(physical_vertex(vertex)
                               for vertex in geometries[p0].vertices)
    owner_sets["two-P"].update(remote.vertices)
    connector_vertices, _, _ = connector_specification(
        "P1", remote.vertices[0], geometries[p0].vertices[distance], row_id
    )
    owner_sets["two-P"].update(connector_vertices)
    require(owner_sets["two-P"].isdisjoint(owner_sets["strict"]),
            "canonical private owner components overlap")
    require(owner_sets["two-P"] | owner_sets["strict"] == set(expected_vertices),
            "canonical private owner components are not exhaustive")
    owners = {vertex: owner for owner, domain in owner_sets.items() for vertex in domain}
    return owners, intervals, interval_owners, two_p_cycles, strict_cycles, None


def make_private_certificate(signature, tree, geometries, remote, orbit):
    p0 = tree.colors.index("P")
    hull = min(orbit.positions, key=lambda vertex: vertex.index)
    row_id = f"P\t{signature}\tdistance={orbit.distance}"
    connector = connector_for_mark("P1", remote, hull, row_id)
    submitted_vertices, submitted_edges = physical_graph_from_parts(
        geometries, remote, connector.path_vertices + (connector.remnant,), connector.edges
    )
    adjacency = INCIDENCE.adjacency(tree)
    if len(adjacency) - len(tree.colors) == 1:
        open_index = 3 if orbit.distance == 1 else 4
        open_vertex = geometries[p0].vertices[open_index]
        theorems, bound = private_theorems(tuple(range(9)), (), True)
        owners = tuple((vertex, "opened-P0" if vertex == open_vertex else "A9P1")
                       for vertex in submitted_vertices)
        return PrivateCertificate(
            row_id, orbit.distance, "distance-specific-open-P0", None,
            open_vertex, tuple(range(9)), (), (), (), theorems, bound,
            submitted_vertices, submitted_edges,
            owners, owners,
        ), connector

    router, _, x_cycles, strict_cycles = canonical_private_router(tree)
    two_p_cycles = x_cycles
    router_geometry = geometries[router]
    root_cut = adjacency[p0][0]
    owners = []
    for vertex in submitted_vertices:
        owner = None
        if vertex in {physical_vertex(item) for item in geometries[p0].vertices} or \
                vertex in set(remote.vertices) | set(connector.path_vertices) | {connector.remnant}:
            owner = "two-P"
        if isinstance(vertex, CORE.CutSite) and vertex.cut == root_cut:
            owner = "two-P"
        for cycle in two_p_cycles:
            if vertex in {physical_vertex(item) for item in geometries[cycle].vertices}:
                owner = "two-P" if owner is None else owner
        for cycle in strict_cycles:
            if vertex in {physical_vertex(item) for item in geometries[cycle].vertices}:
                require(owner in (None, "strict"), "private terminal cycles overlap")
                owner = "strict"
        if vertex in {physical_vertex(item) for item in router_geometry.vertices}:
            candidate = "two-P" if isinstance(vertex, CORE.CutSite) and \
                vertex.cut == root_cut else "strict"
            require(owner in (None, candidate), "private router vertex has competing owner")
            owner = candidate
        require(owner is not None, "private physical vertex has no derived terminal owner")
        owners.append((vertex, owner))
    root_site = CORE.CutSite(root_cut)
    intervals = ((root_site,), tuple(physical_vertex(vertex)
                                     for vertex in router_geometry.vertices
                                     if physical_vertex(vertex) != root_site))
    interval_owners = ("two-P", "strict")
    theorems, bound = private_theorems(two_p_cycles, strict_cycles)
    return PrivateCertificate(
        row_id, orbit.distance, "leaf-P-router", router, None,
        two_p_cycles, strict_cycles, intervals, interval_owners, theorems, bound,
        submitted_vertices, submitted_edges,
        tuple(owners), tuple(owners),
    ), connector


def verify_private_certificate(signature, tree, certificate):
    expected_geometries, expected_remote = expected_blocks(signature, tree)
    p0 = tree.colors.index("P")
    hull_index = certificate.distance
    expected_vertices, expected_edges, expected_attachments = (
        reconstruct_expected_private_graph(
            signature, tree, certificate.row_id, hull_index
        )
    )
    adjacency = INCIDENCE.adjacency(tree)
    bouquet = len(adjacency) - len(tree.colors) == 1
    (expected_owner_map, expected_intervals, expected_interval_owners,
     expected_two_p_cycles, expected_strict_cycles, expected_open) = (
        expected_private_owner_map(
            signature, tree, certificate.row_id, certificate.distance
        )
    )
    submitted_owner_map = CORE.exact_owner_map(
        certificate.vertex_owners, expected_vertices, "private submitted vertex owners"
    )
    submitted_attachment_map = CORE.exact_owner_map(
        certificate.attachment_owners, expected_attachments,
        "private submitted attachment owners"
    )
    require(submitted_owner_map == expected_owner_map,
            "private submitted vertex owners differ from canonical branch owners")
    require(submitted_attachment_map == expected_owner_map,
            "private submitted attachments differ from canonical branch owners")
    if bouquet:
        require(certificate.operation == "distance-specific-open-P0" and
                certificate.router is None,
                "bouquet private row does not use the opening theorem")
        require(certificate.distance in (1, 2), "unknown private distance orbit")
        require(certificate.open_vertex == expected_open,
                "wrong distance/open vertex for bouquet")
        require(not certificate.interval_vertices and not certificate.interval_owners,
                "bouquet opening carries private router intervals")
        owner_map, edge_keys, owned = CORE.verify_physical_owner_certificate(
            expected_vertices, expected_edges, expected_attachments,
            certificate.vertices, certificate.edges, certificate.vertex_owners,
            certificate.attachment_owners, ("A9P1", "opened-P0")
        )
        p0_vertices = {physical_vertex(vertex) for vertex in expected_geometries[p0].vertices}
        require({vertex for vertex in p0_vertices if owner_map[vertex] == "opened-P0"} ==
                {expected_open}, "bouquet opening does not remove exactly its named vertex")
        require(all(owner_map[vertex] == "A9P1" for vertex in p0_vertices - {expected_open}),
                "retained P0 path is incomplete")
        require(certificate.two_p_cycles == tuple(range(9)) and
                not certificate.strict_cycles,
                "bouquet retained A9 profile changed")
        require(len(owned["opened-P0"]) == 1,
                "opened P0 territory is not the exact nonempty tree charge")
    else:
        router, root_cut, two_p_cycles, strict_cycles = canonical_private_router(tree)
        require(certificate.operation == "leaf-P-router" and
                certificate.router == router and certificate.open_vertex is None,
                "private row does not use its canonical first triangle router")
        require(len(certificate.two_p_cycles) + 2 <= 9, "rank10+ two-P child")
        require(certificate.strict_cycles, "empty strict sibling")
        require(certificate.two_p_cycles == two_p_cycles and
                certificate.strict_cycles == strict_cycles,
                "private router children differ from incidence components")
        router_geometry = expected_geometries[router]
        root_site = CORE.CutSite(root_cut)
        intervals = ((root_site,), tuple(physical_vertex(vertex)
                                        for vertex in router_geometry.vertices
                                        if physical_vertex(vertex) != root_site))
        require(certificate.interval_vertices == expected_intervals == intervals and
                certificate.interval_owners == expected_interval_owners ==
                ("two-P", "strict"),
                "private concrete intervals are not bound to their final owners")
        CORE.verify_router_owner_split(
            CycleGeometry(router_geometry.label, 3,
                          tuple(physical_vertex(vertex) for vertex in router_geometry.vertices),
                          tuple((physical_vertex(left), physical_vertex(right))
                                for left, right in router_geometry.edges)),
            intervals, ("two-P", "strict"), (1, 2)
        )
        owner_map, edge_keys, owned = CORE.verify_physical_owner_certificate(
            expected_vertices, expected_edges, expected_attachments,
            certificate.vertices, certificate.edges, certificate.vertex_owners,
            certificate.attachment_owners, ("two-P", "strict")
        )
        p0_vertices = {physical_vertex(vertex) for vertex in expected_geometries[p0].vertices}
        remote_vertices = set(expected_remote.vertices)
        require(all(owner_map[vertex] == "two-P"
                    for vertex in p0_vertices | remote_vertices), "C5 split")
    derived_theorems, derived_bound = private_theorems(
        expected_two_p_cycles, expected_strict_cycles, bouquet
    )
    require(certificate.theorems == derived_theorems,
            "private terminal theorem records were not independently rederived")
    require(certificate.bound == derived_bound and certificate.bound.positive(),
            "private exact theorem ledger is not positive")
    theorem = tuple((record.owner, record.theorem, record.hypothesis,
                     record.cycles, record.pentagons, record.bound)
                    for record in derived_theorems)
    text = repr((certificate.row_id, certificate.operation, certificate.distance,
                 certificate.router, certificate.open_vertex,
                 certificate.two_p_cycles, certificate.strict_cycles,
                 certificate.interval_vertices, certificate.interval_owners,
                 tuple(sorted((repr(vertex), owner) for vertex, owner in owner_map.items())),
                 tuple(sorted(tuple(sorted(map(repr, edge))) for edge in edge_keys)),
                 theorem, derived_bound))
    return text, (signature, tree, certificate)


def certify_projected_physical_plan(row_id, plan, projected_tree, geometries,
                                    projected_positions, clustered, remote, connector,
                                    cycle_map, cut_map, signature, tree, root_mark):
    """Materialize all vertices/edges and derive terminal facts on the owned graph."""
    resolve = projected_owner_resolver(projected_tree, plan, projected_positions)
    cycle_inverse = {new: old for old, new in cycle_map.items()}
    cut_inverse = {new: old for old, new in cut_map.items()}
    concrete_to_position = {}
    for router in range(9):
        for position in A9.local_triangle_positions(projected_tree, router):
            vertex = projected_vertex(position, router, geometries, cycle_inverse, cut_inverse)
            concrete_to_position[physical_vertex(vertex)] = position

    packet_owners = tuple(range(len(plan.packets)))
    cycle_owner = {cycle: index for index, packet in enumerate(plan.packets)
                   for cycle in packet.cycles}
    p0_owner, p1_owner = tuple(resolve(position) for position in projected_positions)
    owner_records = []

    def add_vertex(vertex, owner):
        owner_records.append((vertex, owner))

    for old_cycle, geometry in enumerate(geometries):
        for vertex in geometry.vertices:
            physical = physical_vertex(vertex)
            if old_cycle == geometries.index(clustered):
                owner = p0_owner
            else:
                projected_cycle = cycle_map[old_cycle]
                owner = cycle_owner.get(projected_cycle)
                if owner is None:
                    owner = resolve(concrete_to_position[physical])
            add_vertex(physical, owner)
    for vertex in remote.vertices:
        add_vertex(vertex, p1_owner)
    for vertex in connector.path_vertices + (connector.remnant,):
        add_vertex(vertex, p1_owner)

    submitted_vertices, submitted_edges = physical_graph_from_parts(
        geometries, remote, connector.path_vertices + (connector.remnant,),
        connector.edges
    )
    expected_vertices, expected_edges, expected_attachment_domain = (
        reconstruct_expected_physical_graph(
            signature, tree, row_id, root_mark
        )
    )

    owner_map = {}
    for vertex, owner in owner_records:
        old = owner_map.setdefault(vertex, owner)
        require(old == owner, "split C5/cut ownership or competing shared-cut owner")
    attachment_records = tuple(owner_map.items())
    owner_map, edge_keys, owned = CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachment_domain,
        submitted_vertices, submitted_edges, tuple(owner_map.items()),
        attachment_records, packet_owners
    )

    complete_triangles = {owner: [] for owner in packet_owners}
    for old_cycle, geometry in enumerate(geometries):
        if geometry.length != 3:
            continue
        physicals = {physical_vertex(vertex) for vertex in geometry.vertices}
        owners = {owner_map[vertex] for vertex in physicals}
        if len(owners) == 1:
            complete_triangles[next(iter(owners))].append(cycle_map[old_cycle])
    pentagons = tuple(zip(A9.PENTAGONS, (clustered, remote)))
    derived_demands = {owner: [] for owner in packet_owners}
    for label, geometry in pentagons:
        owners = {owner_map[physical_vertex(vertex)] for vertex in geometry.vertices}
        require(len(owners) == 1, "split C5 ownership")
        derived_demands[next(iter(owners))].append(label)

    for owner, packet in enumerate(plan.packets):
        cycles = tuple(sorted(complete_triangles[owner]))
        demands = tuple(sorted(derived_demands[owner]))
        require(cycles == packet.cycles, "owned graph derives different terminal triangles")
        derived = A9.terminal_packet(projected_tree, cycles, demands, packet.name)
        require((derived.theorem, derived.hypothesis, derived.bound) ==
                (packet.theorem, packet.hypothesis, packet.bound),
                "owned graph does not derive declared theorem hypotheses")
    text = repr((row_id, tuple(sorted((repr(vertex), owner)
                                     for vertex, owner in owner_map.items())),
                 tuple(sorted(tuple(sorted(map(repr, edge))) for edge in edge_keys)),
                 tuple((owner, tuple(sorted(map(repr, domain))))
                       for owner, domain in sorted(owned.items()))))
    return text, (expected_vertices, expected_edges, expected_attachment_domain,
                  submitted_vertices, submitted_edges, tuple(owner_map.items()),
                  attachment_records, packet_owners, clustered, connector, plan,
                  projected_tree, geometries, remote, cycle_map, cut_map, row_id)


def residual_geometry(projected_tree, positions):
    """Classify the six repair geometries from incidence and marked positions."""
    adjacency = A9.BASE.BASE.adjacency(projected_tree)
    cuts = tuple(range(9, len(adjacency)))
    first, second = positions
    if len(cuts) == 2:
        routers = tuple(cycle for cycle in range(9) if len(adjacency[cycle]) == 2)
        hubs = tuple(cut for cut in cuts if len(adjacency[cut]) == 8)
        if len(routers) != 1 or len(hubs) != 1:
            return None
        router = routers[0]
        private = A9.BASE.Position("private", router, 0)
        hub = A9.BASE.Position("cut", hubs[0])
        if {first, second} == {private, hub}:
            leaf_cut = next(cut for cut in cuts if cut != hubs[0])
            return "split-router", router, hubs[0], leaf_cut
        return None
    if len(cuts) != 1 or not all(cuts[0] in adjacency[cycle] for cycle in range(9)):
        return None
    marked_shape = (
        first.kind == second.kind == "cut"
        or {first.kind, second.kind} == {"cut", "private"}
        or first.kind == second.kind == "private" and first.vertex != second.vertex
    )
    return ("open-clustered-P", None, cuts[0], None) if marked_shape else None


def make_residual_certificate(row_id, projected_row, geometries, clustered, remote,
                              connector, cycle_map, cut_map):
    classification = residual_geometry(projected_row.tree, projected_row.positions)
    require(classification is not None, "residual certificate requested outside repair geometry")
    repair = A9.make_safe_repair(projected_row, "physical-A9-repair")
    A9.verify_safe_repair(projected_row, repair)
    submitted_vertices, submitted_edges = physical_graph_from_parts(
        geometries, remote, connector.path_vertices + (connector.remnant,), connector.edges
    )
    operation, projected_router, _, _ = classification
    owners = {}

    def own(vertex, owner):
        physical = physical_vertex(vertex)
        old = owners.setdefault(physical, owner)
        require(old == owner, "residual geometry gives one physical vertex two owners")

    cycle_inverse = {new: old for old, new in cycle_map.items()}
    if operation == "split-router":
        packet_by_cycle = {cycle: packet.name for packet in repair.packets
                           for cycle in packet.cycles}
        concrete_intervals = tuple(
            tuple(projected_vertex(position, projected_router, geometries,
                                   cycle_inverse, {new: old for old, new in cut_map.items()})
                  for position in interval)
            for interval in repair.interval_positions
        )
        router_geometry = geometries[cycle_inverse[projected_router]]
        CORE.verify_router_owner_split(
            router_geometry, concrete_intervals, repair.interval_owners,
            repair.interval_sizes
        )
        router_owner = {
            physical_vertex(vertex): owner
            for interval, owner in zip(concrete_intervals, repair.interval_owners)
            for vertex in interval
        }
        for old_cycle, geometry in enumerate(geometries):
            if old_cycle == geometries.index(clustered):
                owner = repair.connector_owners[0]
            elif old_cycle == cycle_inverse[projected_router]:
                for vertex in geometry.vertices:
                    own(vertex, router_owner[physical_vertex(vertex)])
                continue
            else:
                owner = packet_by_cycle[cycle_map[old_cycle]]
            for vertex in geometry.vertices:
                own(vertex, owner)
        remote_owner = repair.connector_owners[1]
        for vertex in remote.vertices + connector.path_vertices + (connector.remnant,):
            own(vertex, remote_owner)
        open_vertex = None
        interval_owners = repair.interval_owners
    else:
        root = physical_vertex(clustered.vertices[0])
        retained = repair.opening.retained_owner
        opened = repair.opening.opening_owner
        c5_intervals = ((root,), tuple(physical_vertex(vertex)
                                       for vertex in clustered.vertices[1:]))
        physical_clustered = CycleGeometry(
            clustered.label, 5,
            tuple(physical_vertex(vertex) for vertex in clustered.vertices),
            tuple((physical_vertex(left), physical_vertex(right))
                  for left, right in clustered.edges),
        )
        CORE.verify_router_owner_split(
            physical_clustered, c5_intervals, (retained, opened), (1, 4)
        )
        for geometry in geometries:
            for vertex in geometry.vertices:
                own(vertex, retained if geometry is not clustered or
                    physical_vertex(vertex) == root else opened)
        for vertex in remote.vertices + connector.path_vertices + (connector.remnant,):
            own(vertex, retained)
        concrete_intervals = c5_intervals
        interval_owners = (retained, opened)
        open_vertex = tuple(physical_vertex(vertex) for vertex in clustered.vertices[1:])
    require(set(owners) == set(submitted_vertices),
            "residual owner construction does not cover the physical graph")
    records = tuple(owners.items())
    certificate = ResidualCertificate(
        row_id, operation, cycle_inverse[projected_router] if projected_router is not None else None,
        open_vertex, concrete_intervals, interval_owners,
        submitted_vertices, submitted_edges, records, records,
    )
    return certificate, repair


def verify_residual_certificate(signature, tree, root_mark, projected_row, geometries,
                                clustered, remote, connector, cycle_map, cut_map,
                                certificate, repair):
    classification = residual_geometry(projected_row.tree, projected_row.positions)
    require(classification is not None, "physical repair no longer has residual geometry")
    operation, projected_router, _, _ = classification
    require(certificate.operation == operation and
            certificate.router == ({new: old for old, new in cycle_map.items()}[projected_router]
                                   if projected_router is not None else None),
            "physical repair operation/router differs from geometry predicate")
    A9.verify_safe_repair(projected_row, repair)
    expected_vertices, expected_edges, expected_attachments = reconstruct_expected_physical_graph(
        signature, tree, certificate.row_id, root_mark
    )
    owner_names = tuple(dict.fromkeys(owner for _, owner in certificate.vertex_owners))
    owner_map, edge_keys, owned = CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachments,
        certificate.vertices, certificate.edges, certificate.vertex_owners,
        certificate.attachment_owners, owner_names
    )
    cycle_inverse = {new: old for old, new in cycle_map.items()}
    complete_triangles = {owner: [] for owner in owner_names}
    for projected_cycle in range(9):
        geometry = geometries[cycle_inverse[projected_cycle]]
        cycle_owners = {owner_map[physical_vertex(vertex)] for vertex in geometry.vertices}
        if len(cycle_owners) == 1:
            complete_triangles[next(iter(cycle_owners))].append(projected_cycle)
    complete_pentagons = {owner: [] for owner in owner_names}
    for label, geometry in zip(A9.PENTAGONS, (clustered, remote)):
        cycle_owners = {owner_map[physical_vertex(vertex)] for vertex in geometry.vertices}
        if len(cycle_owners) == 1:
            complete_pentagons[next(iter(cycle_owners))].append(label)
    for packet in repair.packets:
        require(tuple(sorted(complete_triangles[packet.name])) == packet.cycles and
                tuple(sorted(complete_pentagons[packet.name])) == packet.demands,
                "physical residual packet profile differs from owned blocks")
        derived = A9.terminal_packet(
            projected_row.tree, complete_triangles[packet.name],
            complete_pentagons[packet.name], packet.name
        )
        require(derived == packet, "physical residual theorem/bound was not rederived")
    if operation == "split-router":
        router_geometry = geometries[certificate.router]
        CORE.verify_router_owner_split(
            router_geometry, certificate.interval_vertices,
            certificate.interval_owners, (2, 1)
        )
        require(repair.bound == A9.Bound(A9.Fraction(8), 2, True) and
                repair.bound.positive(), "physical TP+A7P ledger changed")
    else:
        root = physical_vertex(clustered.vertices[0])
        require(certificate.interval_vertices == (
                    (root,), tuple(physical_vertex(vertex) for vertex in clustered.vertices[1:])),
                "physical opening is not the rooted C5 singleton/four-path")
        opened = repair.opening.opening_owner
        require(set(owned[opened]) == set(certificate.interval_vertices[1]) and
                len(owned[opened]) == 4,
                "opened clustered pentagon territory is not the exact four-path")
        require(repair.bound == A9.Bound(A9.Fraction(8), 1, True) and
                repair.bound.positive(), "physical opened-A9P ledger changed")
    text = repr((certificate.row_id, certificate.operation, certificate.router,
                 certificate.interval_vertices, certificate.interval_owners,
                 tuple(sorted((repr(vertex), owner) for vertex, owner in owner_map.items())),
                 tuple(sorted(tuple(sorted(map(repr, edge))) for edge in edge_keys)),
                 tuple((packet.name, packet.cycles, packet.demands, packet.theorem,
                        packet.hypothesis, packet.bound) for packet in repair.packets),
                 repair.bound))
    return text


def verify_projection_bijection(records, expected_sources, a9_rows):
    require(digest(sorted(expected_sources)) == EXPECTED_ROW_DIGESTS["triangular-rows"],
            "independently derived projection source domain digest changed")
    by_source = unique_map(((source, target) for source, target in records),
                           expected_sources, "projection source ledger")
    targets = tuple(by_source.values())
    expected = tuple(row.signature for row in a9_rows)
    require(len(targets) == len(set(targets)), "triangular projection is not injective")
    require(set(targets) == set(expected), "triangular projection is not onto A9 rows")
    return by_source


def derive_triangular_source_domain(classes):
    """Independently derive and freeze the projection source census."""
    sources = []
    physical = 0
    for signature, tree in classes:
        adj = INCIDENCE.adjacency(tree)
        p0 = tree.colors.index("P")
        if len(adj[p0]) != 1:
            continue
        for root_code, _, multiplicity in ROOTS.root_orbits(tree):
            sources.append(f"T\t{signature}\t{root_code}")
            physical += multiplicity
    sources.sort()
    require(len(sources) == len(set(sources)),
            "independent triangular source census has duplicates")
    require(len(sources) == 43151 and physical == 68856,
            "independent triangular source census count changed")
    require(digest(sources) == EXPECTED_ROW_DIGESTS["triangular-rows"],
            "independent triangular source census digest changed")
    return tuple(sources), physical


def expect_rejected(action, label):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def mutation_self_tests(triangle, pentagon, connector, orbits, projected_fixture,
                        binding_fixture, physical_fixture, private_router_fixture,
                        private_bouquet_fixture, residual_split_fixture,
                        residual_open_fixture):
    bad_edges = pentagon.edges[:-1] + ((pentagon.vertices[4], pentagon.vertices[1]),)
    expect_rejected(lambda: verify_cycle(replace(pentagon, edges=bad_edges), (pentagon.vertices[0].cut,)),
                    "noncyclic pentagon edge")
    duplicate = replace(pentagon, vertices=pentagon.vertices[:-1] + (pentagon.vertices[1],))
    expect_rejected(lambda: verify_cycle(duplicate, (pentagon.vertices[0].cut,)),
                    "duplicate pentagon vertex")
    expect_rejected(lambda: verify_connector(replace(connector, pentagon_root=pentagon.vertices[1]),
                                              pentagon, connector.hull_position),
                    "moved connector root")
    expect_rejected(lambda: verify_connector(replace(connector, remnant=connector.path_vertices[0]),
                                              pentagon, connector.hull_position),
                    "aliased connector remnant")
    expect_rejected(lambda: verify_connector(replace(connector, edges=connector.edges[:-1]),
                                              pentagon, connector.hull_position),
                    "connector edge loss")
    expect_rejected(lambda: verify_intervals(pentagon, ((pentagon.vertices[0], pentagon.vertices[2]),
                                                        (pentagon.vertices[1], pentagon.vertices[3],
                                                         pentagon.vertices[4]))),
                    "nonconsecutive cyclic interval")
    expect_rejected(lambda: verify_intervals(triangle, ((triangle.vertices[0],),
                                                        (triangle.vertices[1],))),
                    "omitted triangle position")
    expect_rejected(lambda: unique_map((("a", "x"), ("a", "y")), ("a",), "mutation"),
                    "duplicate owner key")
    expect_rejected(lambda: unique_map((("a", "x"),), ("a", "b"), "mutation"),
                    "incomplete owner domain")
    bad_orbits = (replace(orbits[0], positions=(orbits[0].positions[0],)), orbits[1])
    expect_rejected(lambda: require(
        Counter(vertex for orbit in bad_orbits for vertex in orbit.positions) ==
        Counter(pentagon.vertices[1:]), "mutated C5 orbits are incomplete"),
        "incomplete rooted C5 orbit")
    projection_records, projection_sources, a9_rows = projected_fixture
    duplicate_target = projection_records[:-1] + (
        (projection_records[-1][0], projection_records[0][1]),
    )
    expect_rejected(lambda: verify_projection_bijection(
        duplicate_target, projection_sources, a9_rows),
                    "nonbijective triangular projection")
    fresh_source = projection_records[:-1] + (
        ("T\tfresh-source-alias\tR()", projection_records[-1][1]),
    )
    expect_rejected(lambda: verify_projection_bijection(
        fresh_source, projection_sources, a9_rows),
        "fresh projection source alias")
    expect_rejected(lambda: CORE.verify_router_owner_split(
        triangle,
        ((triangle.vertices[0],), (triangle.vertices[1],)),
        ("left", "right"), (1, 2)),
        "incomplete projected router interval")
    (binding_signature, binding_tree, binding_geometries, projected_tree,
     cycle_map, cut_map) = binding_fixture
    cut_items = tuple(cut_map.items())
    require(len(cut_items) >= 2, "cut-map mutation fixture has fewer than two cuts")
    bad_cut_map = dict(cut_map)
    bad_cut_map[cut_items[0][0]], bad_cut_map[cut_items[1][0]] = (
        cut_items[1][1], cut_items[0][1]
    )
    expect_rejected(lambda: verify_projection_binding(
        binding_signature, binding_tree, binding_geometries, projected_tree,
        cycle_map, bad_cut_map), "swapped projection cut map")
    symmetric_pair = incidence_symmetric_triangle_pair(binding_tree)
    require(symmetric_pair is not None,
            "cycle-map mutation fixture has no incidence-symmetric triangles")
    bad_cycle_map = dict(cycle_map)
    first_cycle, second_cycle = symmetric_pair
    bad_cycle_map[first_cycle], bad_cycle_map[second_cycle] = (
        bad_cycle_map[second_cycle], bad_cycle_map[first_cycle]
    )
    swapped_edges = tuple(sorted(
        (bad_cycle_map[cycle], cut_map[cut])
        for cycle, cut in binding_tree.edges
        if cycle in bad_cycle_map and cut in cut_map
    ))
    require(swapped_edges == projected_tree.edges,
            "cycle-map mutation witness is not incidence-symmetric")
    expect_rejected(lambda: verify_projection_binding(
        binding_signature, binding_tree, binding_geometries, projected_tree,
        bad_cycle_map, cut_map), "swapped incidence-symmetric cycle map")
    cut_sites = tuple(
        (geometry_index, vertex_index, vertex)
        for geometry_index, geometry in enumerate(binding_geometries)
        for vertex_index, vertex in enumerate(geometry.vertices)
        if vertex.cut is not None
    )
    first = cut_sites[0]
    second = next(site for site in cut_sites if site[2].cut != first[2].cut)
    bad_geometries = list(binding_geometries)
    replacements = {}
    for site, new_cut in ((first, second[2].cut), (second, first[2].cut)):
        geometry_index, vertex_index, vertex = site
        vertices = list(replacements.get(geometry_index,
                                         bad_geometries[geometry_index].vertices))
        vertices[vertex_index] = replace(vertex, cut=new_cut)
        replacements[geometry_index] = tuple(vertices)
    for geometry_index, vertices in replacements.items():
        geometry = bad_geometries[geometry_index]
        bad_geometries[geometry_index] = replace(
            geometry, vertices=vertices,
            edges=tuple((vertices[index], vertices[(index + 1) % len(vertices)])
                        for index in range(len(vertices)))
        )
    expect_rejected(lambda: verify_projection_binding(
        binding_signature, binding_tree, tuple(bad_geometries), projected_tree,
        cycle_map, cut_map), "swapped geometry cut labels")
    (expected_vertices, expected_edges, expected_attachment_domain,
     physical_vertices, physical_edges, physical_owners, attachment_owners,
     packet_owners, physical_c5, physical_connector, physical_plan,
     physical_tree, physical_geometries, physical_remote, physical_cycle_map,
     physical_cut_map, physical_row_id) = physical_fixture
    split_owners = list(physical_owners)
    split_vertex = physical_c5.vertices[1]
    split_index = next(index for index, (vertex, _) in enumerate(split_owners)
                       if vertex == split_vertex)
    split_owners[split_index] = (split_vertex,
                                 next(owner for owner in packet_owners
                                      if owner != split_owners[split_index][1]))
    expect_rejected(lambda: CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachment_domain,
        physical_vertices, physical_edges, tuple(split_owners),
        attachment_owners, packet_owners), "split C5 ownership")
    duplicated_cut_vertices = physical_vertices + (next(
        vertex for vertex in physical_vertices if isinstance(vertex, CORE.CutSite)),)
    expect_rejected(lambda: CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachment_domain,
        duplicated_cut_vertices, physical_edges, physical_owners,
        attachment_owners, packet_owners), "duplicated canonical cut")
    forged_edges = tuple(edge for edge in physical_edges
                         if CORE.undirected_edge(edge) != CORE.undirected_edge(
                             physical_connector.edges[1]))
    expect_rejected(lambda: CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachment_domain,
        physical_vertices, forged_edges, physical_owners, attachment_owners,
        packet_owners), "forged packet connectivity")
    remnant = physical_connector.remnant
    remnant_edge = CORE.undirected_edge(
        (physical_connector.remnant_anchor, remnant)
    )
    deleted_vertices = tuple(vertex for vertex in physical_vertices if vertex != remnant)
    deleted_edges = tuple(edge for edge in physical_edges
                          if CORE.undirected_edge(edge) != remnant_edge)
    deleted_owners = tuple(record for record in physical_owners if record[0] != remnant)
    deleted_attachments = tuple(record for record in attachment_owners
                                if record[0] != remnant)
    expect_rejected(lambda: CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachment_domain,
        deleted_vertices, deleted_edges, deleted_owners, deleted_attachments,
        packet_owners), "coordinated remnant deletion")
    private_signature, private_tree, private_certificate = private_router_fixture
    bouquet_signature, bouquet_tree, bouquet_certificate = private_bouquet_fixture
    expect_rejected(lambda: verify_private_certificate(
        bouquet_signature, bouquet_tree,
        replace(bouquet_certificate, open_vertex=next(
            vertex for vertex in expected_blocks(bouquet_signature, bouquet_tree)[0][
                bouquet_tree.colors.index("P")].vertices
            if vertex != bouquet_certificate.open_vertex))),
        "wrong distance/open vertex")
    private_connector_edge = next(
        edge for edge in private_certificate.edges
        if isinstance(edge[0], str) and ":path-root" in edge[0]
        or isinstance(edge[1], str) and ":path-root" in edge[1]
    )
    expect_rejected(lambda: verify_private_certificate(
        private_signature, private_tree,
        replace(private_certificate, edges=tuple(
            edge for edge in private_certificate.edges if edge != private_connector_edge))),
        "severed private connector")
    expect_rejected(lambda: verify_private_certificate(
        private_signature, private_tree,
        replace(private_certificate, two_p_cycles=tuple(range(8)))),
        "rank10+ private child")
    expect_rejected(lambda: verify_private_certificate(
        private_signature, private_tree,
        replace(private_certificate, strict_cycles=())),
        "empty private strict sibling")
    private_owners = dict(private_certificate.vertex_owners)
    private_p0 = expected_blocks(private_signature, private_tree)[0][
        private_tree.colors.index("P")]
    split_vertex = physical_vertex(private_p0.vertices[1])
    private_owners[split_vertex] = "strict"
    expect_rejected(lambda: verify_private_certificate(
        private_signature, private_tree,
        replace(private_certificate, vertex_owners=tuple(private_owners.items()))),
        "private C5 split")
    c0_vertex = next(
        physical_vertex(vertex)
        for vertex in expected_blocks(private_signature, private_tree)[0][0].vertices
        if dict(private_certificate.vertex_owners)[physical_vertex(vertex)] == "strict"
    )
    c0_owners = dict(private_certificate.vertex_owners)
    c0_owners[c0_vertex] = "two-P"
    expect_rejected(lambda: verify_private_certificate(
        private_signature, private_tree,
        replace(private_certificate, vertex_owners=tuple(c0_owners.items()))),
        "private C0 vertex moved from strict to two-P")
    private_attachments = dict(private_certificate.attachment_owners)
    attachment_vertex = next(vertex for vertex, owner in private_attachments.items()
                             if owner == "two-P")
    private_attachments[attachment_vertex] = "strict"
    expect_rejected(lambda: verify_private_certificate(
        private_signature, private_tree,
        replace(private_certificate,
                attachment_owners=tuple(private_attachments.items()))),
        "private attachment mismatch")
    split_args, split_certificate, split_repair = residual_split_fixture
    split_owners = dict(split_certificate.vertex_owners)
    split_vertex = split_certificate.interval_vertices[0][0]
    split_owners[split_vertex] = split_certificate.interval_owners[1]
    expect_rejected(lambda: verify_residual_certificate(
        *split_args, replace(split_certificate, vertex_owners=tuple(split_owners.items())),
        split_repair), "residual split owner mutation")
    expect_rejected(lambda: verify_residual_certificate(
        *split_args, replace(split_certificate,
                             interval_vertices=tuple(reversed(split_certificate.interval_vertices))),
        split_repair), "residual ordered interval mutation")
    open_args, open_certificate, open_repair = residual_open_fixture
    opened_owners = dict(open_certificate.vertex_owners)
    opened_vertex = open_certificate.interval_vertices[1][0]
    opened_owners[opened_vertex] = open_certificate.interval_owners[0]
    expect_rejected(lambda: verify_residual_certificate(
        *open_args, replace(open_certificate, vertex_owners=tuple(opened_owners.items())),
        open_repair), "residual C5 opening mutation")
    open_connector = open_args[7]
    severed = tuple(edge for edge in open_certificate.edges
                    if CORE.undirected_edge(edge) !=
                    CORE.undirected_edge(open_connector.edges[1]))
    expect_rejected(lambda: verify_residual_certificate(
        *open_args, replace(open_certificate, edges=severed), open_repair),
        "residual connector mutation")
    return 31


def main():
    blueprint_digest = file_digest(BLUEPRINT)
    require(blueprint_digest == EXPECTED_BLUEPRINT_DIGEST,
            "persisted K1--K17 repair blueprint digest changed")
    classes = INCIDENCE.enumerate_colors(tuple(sorted(("T",) * 9 + ("P",))), 0)
    projection_sources, triangular_physical = derive_triangular_source_domain(classes)
    all_by_cut = Counter()
    leaf_by_cut = Counter()
    all_signatures = []
    leaf_signatures = []
    triangular_rows = list(projection_sources)
    private_rows = []
    incidence_records = []
    triangular_connector_records = []
    private_connector_records = []
    private_physical = 0
    fixture = None
    binding_fixture = None
    a9_rows, _, _ = A9.enumerate_rows()
    a9_by_signature = unique_map(
        ((row.signature, row) for row in a9_rows),
        (row.signature for row in a9_rows), "A9 canonical row ledger"
    )
    projection_records = []
    projected_plan_records = []
    physical_certificate_records = []
    residual_certificate_records = []
    residual_source_rows = []
    private_certificate_records = []
    projected_plan_count = 0
    physical_fixture = None
    private_router_fixture = None
    private_bouquet_fixture = None
    residual_split_fixture = None
    residual_open_fixture = None

    require(tuple(signature for signature, _ in classes) ==
            tuple(sorted(signature for signature, _ in classes)),
            "incidence classes are not sorted")
    require(len({signature for signature, _ in classes}) == len(classes),
            "duplicate incidence signature")

    for signature, tree in classes:
        require(signature == INCIDENCE.signature(tree), "noncanonical incidence tree")
        adj = INCIDENCE.adjacency(tree)
        cuts = len(adj) - len(tree.colors)
        all_by_cut[cuts] += 1
        all_signatures.append(signature)
        geometries = incidence_geometry(signature, tree)
        verify_geometry_incidence_binding(signature, tree, geometries)
        expected_geometry_record = expected_incidence_geometry_text(signature, tree)
        require(expected_geometry_record == geometry_text(geometries),
                "submitted incidence geometry differs from independent stream")
        incidence_records.append(f"{signature}|{expected_geometry_record}")
        p0 = tree.colors.index("P")
        if len(adj[p0]) != 1:
            continue
        leaf_by_cut[cuts] += 1
        leaf_signatures.append(signature)
        clustered = geometries[p0]
        require(clustered.vertices[0].cut == adj[p0][0],
                "clustered pentagon root is not its unique incidence cut")

        remote = make_cycle(f"{signature}:remote-P1", 5, ())
        orbits = rooted_private_orbits(clustered)
        for root_code, mark, multiplicity in ROOTS.root_orbits(tree):
            row_id = f"T\t{signature}\t{root_code}"
            hull = hull_position_for_mark(geometries, mark)
            connector = connector_for_mark("P1", remote, hull, row_id)
            triangular_connector_records.append(expected_triangular_connector_text(
                signature, tree, row_id, mark
            ))
            projected_signature, projected_tree, projected_positions, cycle_map, cut_map = (
                triangular_projection(tree, mark)
            )
            verify_projection_binding(
                signature, tree, geometries, projected_tree, cycle_map, cut_map
            )
            if (binding_fixture is None and len(cut_map) >= 2 and
                    incidence_symmetric_triangle_pair(tree) is not None):
                binding_fixture = (
                    signature, tree, geometries, projected_tree,
                    dict(cycle_map), dict(cut_map)
                )
            projected_row = a9_by_signature.get(projected_signature)
            require(projected_row is not None,
                    f"triangular projection has no canonical A9 row: {row_id} -> "
                    f"{projected_signature}")
            require(A9.BASE.BASE.signature(projected_tree) == projected_row.incidence_signature,
                    "projected incidence tree disagrees with canonical A9 row")
            require(A9.BASE.marked_signature(projected_tree, projected_positions) ==
                    projected_row.signature,
                    "projected marked positions disagree with canonical A9 row")
            projection_records.append((row_id, projected_signature))
            concrete_projected_row = A9.BASE.Row(
                projected_signature,
                A9.BASE.BASE.signature(projected_tree),
                projected_tree,
                projected_positions,
                multiplicity,
            )
            plan = A9.choose_plan(concrete_projected_row)
            if plan is not None:
                A9.verify_plan(concrete_projected_row, plan)
                interval_records = verify_projected_plan(
                    plan, geometries, cycle_map, cut_map
                )
                projected_plan_records.append(
                    f"{row_id}|{projected_signature}|{'|'.join(interval_records)}"
                )
                physical_record, candidate_fixture = certify_projected_physical_plan(
                    row_id, plan, projected_tree, geometries, projected_positions,
                    clustered, remote, connector, cycle_map, cut_map,
                    signature, tree, mark
                )
                physical_certificate_records.append(physical_record)
                if physical_fixture is None:
                    physical_fixture = candidate_fixture
                projected_plan_count += 1
            else:
                require(residual_geometry(projected_tree, projected_positions) is not None,
                        f"unrecognized projected residual remains fail-closed: {row_id}")
                certificate, repair = make_residual_certificate(
                    row_id, concrete_projected_row, geometries, clustered, remote,
                    connector, cycle_map, cut_map
                )
                residual_args = (
                    signature, tree, mark, concrete_projected_row, geometries,
                    clustered, remote, connector, cycle_map, cut_map,
                )
                residual_certificate_records.append(verify_residual_certificate(
                    *residual_args, certificate, repair
                ))
                residual_source_rows.append((row_id, projected_signature,
                                             certificate.operation))
                fixture_value = (residual_args, certificate, repair)
                if certificate.operation == "split-router" and residual_split_fixture is None:
                    residual_split_fixture = fixture_value
                if certificate.operation == "open-clustered-P" and residual_open_fixture is None:
                    residual_open_fixture = fixture_value
            if fixture is None:
                fixture = (next(g for g in geometries if g.length == 3), remote, connector,
                           rooted_private_orbits(remote))

        for orbit in orbits:
            row_id = f"P\t{signature}\tdistance={orbit.distance}"
            private_rows.append(row_id)
            private_physical += len(orbit.positions)
            private_certificate, private_connector = make_private_certificate(
                signature, tree, geometries, remote, orbit
            )
            private_record, private_fixture = verify_private_certificate(
                signature, tree, private_certificate
            )
            private_certificate_records.append(private_record)
            if private_certificate.operation == "leaf-P-router" and private_router_fixture is None:
                private_router_fixture = private_fixture
            if private_certificate.operation == "distance-specific-open-P0" and \
                    private_bouquet_fixture is None:
                private_bouquet_fixture = private_fixture
            for physical in orbit.positions:
                connector = connector_for_mark("P1", remote, physical, row_id)
                private_connector_records.append(expected_private_connector_text(
                    signature, tree, row_id, physical.index
                ))

    triangular_rows.sort()
    private_rows.sort()
    combined_rows = tuple(sorted(triangular_rows + private_rows))
    projection = verify_projection_bijection(
        tuple(projection_records), projection_sources, a9_rows
    )
    projection_digest = digest(
        f"{source}|{projection[source]}" for source in sorted(projection)
    )
    projected_plan_digest = digest(sorted(projected_plan_records))
    physical_certificate_digest = digest(sorted(physical_certificate_records))
    private_certificate_digest = digest(sorted(private_certificate_records))
    residual_certificate_digest = digest(sorted(residual_certificate_records))
    row_digests = {
        "all-incidence": digest(all_signatures),
        "leaf-incidence": digest(leaf_signatures),
        "triangular-rows": digest(triangular_rows),
        "private-rows": digest(private_rows),
        "combined-rows": digest(combined_rows),
    }
    geometry_digests = {
        "incidence-geometry": digest(sorted(incidence_records)),
        "triangular-connectors": digest(sorted(triangular_connector_records)),
        "private-connectors": digest(sorted(private_connector_records)),
        "combined-geometry": digest(sorted(incidence_records + triangular_connector_records +
                                            private_connector_records)),
    }
    require(all_by_cut == EXPECTED_ALL_BY_CUT and leaf_by_cut == EXPECTED_LEAF_BY_CUT,
            "colored incidence census changed")
    require((len(classes), len(leaf_signatures), len(triangular_rows), triangular_physical,
             len(private_rows), private_physical, len(combined_rows)) ==
            (8011, 3624, 43151, 68856, 7248, 14496, 50399),
            "endpoint row or physical-position count changed")
    require(row_digests == EXPECTED_ROW_DIGESTS, "frozen endpoint row digest changed")
    require(fixture is not None, "hostile mutation fixture is absent")
    require(binding_fixture is not None, "projection-binding mutation fixture is absent")
    require(physical_fixture is not None, "physical-certificate mutation fixture is absent")
    require(private_router_fixture is not None and private_bouquet_fixture is not None,
            "private-certificate mutation fixtures are absent")
    require(residual_split_fixture is not None and residual_open_fixture is not None,
            "residual-certificate mutation fixtures are absent")
    require(projected_plan_count == 43145,
            "concrete projected interval plan count is not 43145")
    require(len(residual_certificate_records) == 6 and
            Counter(operation for _, _, operation in residual_source_rows) ==
            Counter({"split-router": 2, "open-clustered-P": 4}),
            "predicate-derived projected residual profile is not exact")
    mutation_count = mutation_self_tests(
        *fixture, (tuple(projection_records), projection_sources, a9_rows),
        binding_fixture, physical_fixture, private_router_fixture,
        private_bouquet_fixture, residual_split_fixture, residual_open_fixture
    )

    print("colored T^9P incidence trees:", dict(sorted(all_by_cut.items())), "total", len(classes))
    print("clustered-P incidence-leaf trees:", dict(sorted(leaf_by_cut.items())),
          "total", len(leaf_signatures))
    print("triangular-hull rows/placements:", len(triangular_rows), triangular_physical)
    print("private-P distance-orbit rows/physical vertices:", len(private_rows), private_physical)
    print("triangular-hull projection bijection:", len(projection))
    print("triangular-hull projection sha256:", projection_digest)
    print("concrete projected A9 plans:", projected_plan_count)
    print("concrete projected-plan sha256:", projected_plan_digest)
    print("physical owner certificates:", len(physical_certificate_records))
    print("physical owner-certificate sha256:", physical_certificate_digest)
    print("private physical owner certificates:", len(private_certificate_records))
    print("private owner-certificate sha256:", private_certificate_digest)
    print("residual physical owner certificates:", len(residual_certificate_records))
    print("residual owner-certificate sha256:", residual_certificate_digest)
    for index, source in enumerate(residual_source_rows, 1):
        print(f"projected residual source R{index}:", source)
    print("rooted C5 stabilizer:", rooted_c5_stabilizer())
    for label in sorted(row_digests):
        print(f"{label} sha256:", row_digests[label])
    for label in sorted(geometry_digests):
        print(f"{label} sha256:", geometry_digests[label])
    print("reported 17-row candidate frontier sha256:", REPORTED_SEVENTEEN_DIGEST[1])
    print("repair blueprint sha256:", blueprint_digest)
    print("rejected hostile geometry mutations:", mutation_count)

    require(geometry_digests == EXPECTED_GEOMETRY_DIGESTS,
            "frozen endpoint geometry digest changed")
    require(projection_digest == EXPECTED_PROJECTION_DIGEST,
            "triangular-hull projection digest changed")
    require(projected_plan_digest == EXPECTED_PROJECTED_PLAN_DIGEST,
            "concrete projected-plan digest changed")
    require(physical_certificate_digest == EXPECTED_PHYSICAL_CERTIFICATE_DIGEST,
            "physical owner-certificate digest changed")
    require(private_certificate_digest == EXPECTED_PRIVATE_CERTIFICATE_DIGEST,
            "private owner-certificate digest changed")
    if EXPECTED_RESIDUAL_CERTIFICATE_DIGEST is not None:
        require(residual_certificate_digest == EXPECTED_RESIDUAL_CERTIFICATE_DIGEST,
                "residual owner-certificate digest changed")
    require(mutation_count == 31, "hostile mutation count changed")
    print("theorem-certified endpoint rows:",
          projected_plan_count + len(residual_certificate_records) +
          len(private_certificate_records), "/", len(combined_rows))


if __name__ == "__main__":
    main()
