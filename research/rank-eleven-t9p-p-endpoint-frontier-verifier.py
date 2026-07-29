#!/usr/bin/env python3
"""Fail-closed geometry-aware census for the rank-eleven T^9P | P endpoint.

No theorem closure is claimed. The executable materializes the abstract cyclic
geometry that a future owner certificate must use and freezes the exact 50399
row universe. It also pins the persisted K1--K17 repair blueprint, but exits
with RuntimeError because those recipes have not been integrated into one
uniform graph-level owner verifier for all ordinary and private-P rows.
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
EXPECTED_BLUEPRINT_DIGEST = "c56b1830ada29d5b6887d9ddb95a12ddd950052a23854e39e7a4cd92664ecf5d"


@dataclass(frozen=True, order=True)
class CyclicVertex:
    cycle: str
    index: int
    role: str
    cut: int | None = None


@dataclass(frozen=True)
class CycleGeometry:
    label: str
    length: int
    vertices: tuple[CyclicVertex, ...]
    edges: tuple[tuple[CyclicVertex, CyclicVertex], ...]


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
    keys = [key for key, _ in records]
    require(len(keys) == len(set(keys)), f"{label} has duplicate owner keys")
    require(set(keys) == set(expected_domain), f"{label} has an inexact owner domain")
    return dict(records)


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
    require(len(geometry.vertices) == geometry.length and
            len(set(geometry.vertices)) == geometry.length,
            "cycle does not have distinct named vertices")
    require(geometry.edges == tuple(
        (geometry.vertices[index], geometry.vertices[(index + 1) % geometry.length])
        for index in range(geometry.length)), "cycle edges are not in named cyclic order")
    require(len({frozenset(edge) for edge in geometry.edges}) == geometry.length,
            "cycle repeats an undirected edge")
    cut_vertices = tuple(vertex for vertex in geometry.vertices if vertex.role == "cut")
    private_vertices = tuple(vertex for vertex in geometry.vertices if vertex.role == "private")
    require(tuple(vertex.cut for vertex in cut_vertices) == tuple(cut_bindings),
            "cycle cut vertices do not match incidence bindings")
    require(all(vertex.cut is None for vertex in private_vertices),
            "private cyclic vertex carries a cut")


def consecutive_intervals(geometry):
    """Enumerate every ordered two- and three-part cyclic interval partition."""
    answer = []
    n = geometry.length
    for start in range(n):
        rotated = geometry.vertices[start:] + geometry.vertices[:start]
        for first in range(1, n):
            answer.append((rotated[:first], rotated[first:]))
        if n == 3:
            answer.append(((rotated[0],), (rotated[1],), (rotated[2],)))
    for partition in answer:
        verify_intervals(geometry, partition)
    return tuple(answer)


def verify_intervals(geometry, intervals):
    flat = tuple(vertex for interval in intervals for vertex in interval)
    require(Counter(flat) == Counter(geometry.vertices),
            "cyclic intervals are not an exact vertex partition")
    require(all(0 < len(interval) < geometry.length for interval in intervals),
            "cyclic interval is empty or improper")
    edge_set = {frozenset(edge) for edge in geometry.edges}
    for interval in intervals:
        require(all(frozenset((left, right)) in edge_set
                    for left, right in zip(interval, interval[1:])),
                "interval is not consecutive in the named cycle")


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


def expect_rejected(action, label):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def mutation_self_tests(triangle, pentagon, connector, orbits):
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
    return 9


def main():
    blueprint_digest = file_digest(BLUEPRINT)
    require(blueprint_digest == EXPECTED_BLUEPRINT_DIGEST,
            "persisted K1--K17 repair blueprint digest changed")
    classes = INCIDENCE.enumerate_colors(tuple(sorted(("T",) * 9 + ("P",))), 0)
    all_by_cut = Counter()
    leaf_by_cut = Counter()
    all_signatures = []
    leaf_signatures = []
    triangular_rows = []
    private_rows = []
    incidence_records = []
    triangular_connector_records = []
    private_connector_records = []
    triangular_physical = 0
    private_physical = 0
    fixture = None

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
            triangular_rows.append(row_id)
            triangular_physical += multiplicity
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
    mutation_count = mutation_self_tests(*fixture)

    print("colored T^9P incidence trees:", dict(sorted(all_by_cut.items())), "total", len(classes))
    print("clustered-P incidence-leaf trees:", dict(sorted(leaf_by_cut.items())),
          "total", len(leaf_signatures))
    print("triangular-hull rows/placements:", len(triangular_rows), triangular_physical)
    print("private-P distance-orbit rows/physical vertices:", len(private_rows), private_physical)
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
    require(mutation_count == 9, "hostile mutation count changed")
    raise RuntimeError(
        "fail-closed exact census frontier: no endpoint row is theorem-certified; "
        "the persisted K1--K17 blueprint is not yet integrated with uniform "
        "graph-level final-owner certificates for all 50399 rows"
    )


if __name__ == "__main__":
    main()
