#!/usr/bin/env python3
"""Fail-closed geometry-aware census for the rank-eleven T^9P | P endpoint.

No theorem closure is claimed. The executable materializes the abstract cyclic
geometry, projects the triangular-hull slice bijectively to the hardened
P | A_9 | P verifier, and realizes all of its 43145 ordinary plans on concrete
T^9P triangle vertices. It still exits with RuntimeError because private-P rows
and full graph-level ownership are not certified.
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
    "triangular-connectors": "e59ff052f88b00bbfaed46ad8d0fd4a6d6cb42302ad53bf321202066c2d76e8b",
    "private-connectors": "df3437148c879d78c0595331f3e9d5966e9edf037ea8a12fb5cd64d6df77b90f",
    "combined-geometry": "82387e52ea2ab4878de670377d9003c5a66297637abcf28778d223a2b3d39398",
}
REPORTED_SEVENTEEN_DIGEST = (
    17, "fcf002bb4150db6dc4c5b19f2e9d76b05de066898413b28ee11c4e0a9619747c"
)
BLUEPRINT = HERE / "rank-eleven-t9p-p-seventeen-repair-blueprint-2026-07-28.md"
EXPECTED_BLUEPRINT_DIGEST = "163d4c86bc373470f9d012bdb162937d4013ca345577222e3f26603a77b5f92e"
EXPECTED_PROJECTION_DIGEST = "9897c86b3e197ea3da1fbc2e0ef5ed4440e53bec0d8ac34d6024466c26ccf1a1"
EXPECTED_PROJECTED_PLAN_DIGEST = "c3fd37ebc47de29a7f49471c6ecd61a280581fe30c3fdf72905548345d814566"


CyclicVertex = CORE.CyclicVertex
CycleGeometry = CORE.CycleGeometry


@dataclass(frozen=True)
class Connector:
    label: str
    pentagon_root: CyclicVertex
    hull_position: CyclicVertex
    path_vertices: tuple[str, ...]
    remnant: str


@dataclass(frozen=True)
class PrivateOrbit:
    distance: int
    positions: tuple[CyclicVertex, ...]
    stabilizer_images: tuple[tuple[int, ...], ...]


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
    connector = Connector(label, root, hull_position, path, f"{row_id}:{label}:remnant")
    verify_connector(connector, pentagon, hull_position)
    return connector


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


def geometry_text(geometries):
    return repr(tuple((geometry.label,
                       tuple((vertex.index, vertex.role, vertex.cut)
                             for vertex in geometry.vertices))
                      for geometry in geometries))


def connector_text(row_id, connector):
    return repr((row_id, connector.label, connector.pentagon_root.index,
                 connector.hull_position.cycle, connector.hull_position.index,
                  connector.path_vertices, connector.remnant))


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
                        binding_fixture):
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
    return 15


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
    projected_plan_count = 0

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
        incidence_records.append(f"{signature}|{geometry_text(geometries)}")
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
            if mark.kind == "cut":
                candidates = tuple(vertex for geometry in geometries for vertex in geometry.vertices
                                   if vertex.cut == mark.vertex)
                require(candidates, "cut mark has no concrete cyclic position")
                hull = candidates[0]
            else:
                candidates = tuple(vertex for vertex in geometries[mark.vertex].vertices
                                   if vertex.role == "private")
                require(candidates, "private triangle mark has no concrete cyclic position")
                hull = candidates[0]
            connector = connector_for_mark("P1", remote, hull, row_id)
            triangular_connector_records.append(connector_text(row_id, connector))
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
                projected_plan_count += 1
            if fixture is None:
                fixture = (next(g for g in geometries if g.length == 3), remote, connector,
                           rooted_private_orbits(remote))

        for orbit in orbits:
            row_id = f"P\t{signature}\tdistance={orbit.distance}"
            private_rows.append(row_id)
            private_physical += len(orbit.positions)
            for physical in orbit.positions:
                connector = connector_for_mark("P1", remote, physical, row_id)
                private_connector_records.append(connector_text(row_id, connector))

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
    require(projected_plan_count == 43145,
            "concrete projected interval plan count is not 43145")
    mutation_count = mutation_self_tests(
        *fixture, (tuple(projection_records), projection_sources, a9_rows),
        binding_fixture
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
    require(mutation_count == 15, "hostile mutation count changed")
    raise RuntimeError(
        "fail-closed exact census frontier: the triangular-hull projection and "
        "43145 concrete router plans are certified, but private-P rows and full "
        "T9P graph-level final ownership are not theorem-certified"
    )


if __name__ == "__main__":
    main()
