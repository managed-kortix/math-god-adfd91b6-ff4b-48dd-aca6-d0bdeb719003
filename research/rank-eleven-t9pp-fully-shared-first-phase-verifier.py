#!/usr/bin/env python3
"""Fail-closed first-phase verifier for fully shared rank-eleven T^9PP.

The verifier regenerates the complete color-preserving incidence universe and
searches ordinary one-cycle splits.  Every accepted split is then rebuilt on a
concrete C3/C5 geometry, given exhaustive physical final owners, and classified
again from the owned terminal packets.  The ten nonordinary rows remain
explicitly unresolved here; this executable makes no full-closure claim.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class UnprovedPacket(RuntimeError):
    pass


def load_module(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {filename}")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BASE = load_module(
    "rank_eleven_t9pp_incidence_base",
    "nonacyclic-fully-shared-incidence-census.py",
)
CORE = load_module("geometry_router_owner_core", "geometry_router_owner_core.py")

COLORS = ("P", "P") + ("T",) * 9
CYCLE_COUNT = 11
EXPECTED_ALL_BY_CUT = Counter({
    1: 1, 2: 22, 3: 264, 4: 1790, 5: 7560, 6: 20080,
    7: 33154, 8: 32369, 9: 16775, 10: 3497,
})
EXPECTED_SAFE_BY_CUT = Counter({
    2: 20, 3: 260, 4: 1788, 5: 7559, 6: 20080,
    7: 33154, 8: 32369, 9: 16775, 10: 3497,
})
EXPECTED_CLASS_DIGEST = "65f4d845ff0ef17ce7880992810de149fd2108927e2ef03b8fac57032ac72ce2"
EXPECTED_ACCEPTED_DIGEST = "f9c743de601ca11eb03bf687ad020475f8a087a4f62af56e58726a3510b30c2b"
EXPECTED_PHYSICAL_DIGEST = "5d134b875d7ff369c74f361f4fd58a2ee7262c8bfdaba0453987f46f3391b70e"
EXPECTED_RESIDUAL_DIGEST = "37da45267e16a5c98610ff3a733dbcaeee000c3b089dc16de253e2fbf2feb25c"
EXPECTED_ROUTER_DEGREES = Counter({2: 65586, 3: 43202, 4: 5334, 5: 1380})
EXPECTED_DEGREE4_DIGEST = "1724a7155021b740373957fbcc81eee7dea4d9bc8892d4e9e2ccd6fa9a887af4"
EXPECTED_DEGREE5_DIGEST = "e9049b58c3212b15fb3892367822ed1051aa0663e58828b771658fa8544f020c"
EXPECTED_CANDIDATE_COUNT = 517923
EXPECTED_CANDIDATE_DIGEST = "071df2e10153eb21a8153cc3e45de6768e350a2257a692b0b03979227bc37a0f"
TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0, 9: 0}


@dataclass(frozen=True)
class Bound:
    credit: Fraction
    deficits: int
    strict: bool

    def __add__(self, other):
        return Bound(
            self.credit + other.credit,
            self.deficits + other.deficits,
            self.strict or other.strict,
        )

    def positive(self):
        """Check credit-deficits*(sqrt(5)-2)>0 exactly."""
        shifted = self.credit + 2 * self.deficits
        if shifted < 0:
            return False
        square = shifted * shifted - 5 * self.deficits * self.deficits
        return square > 0 or square == 0 and self.strict


ZERO = Bound(Fraction(0), 0, False)


@dataclass(frozen=True)
class Packet:
    owner: int
    cycles: tuple[int, ...]
    theorem: str
    hypothesis: str
    bound: Bound


@dataclass(frozen=True, order=True)
class RouterRemnant:
    cycle: int
    slot: int


@dataclass(frozen=True, order=True)
class ForestAttachment:
    anchor: object


@dataclass(frozen=True)
class Certificate:
    signature: str
    sacrificed: int
    geometry_vertices: tuple[tuple[object, ...], ...]
    interval_vertices: tuple[tuple[object, ...], ...]
    interval_owners: tuple[int, ...]
    vertices: tuple[object, ...]
    edges: tuple[tuple[object, object], ...]
    remnant_anchors: tuple[tuple[RouterRemnant, object], ...]
    vertex_owners: tuple[tuple[object, int], ...]
    attachment_owners: tuple[tuple[ForestAttachment, int], ...]
    packets: tuple[Packet, ...]
    bound: Bound


def stream_digest(records):
    digest = sha256()
    for record in records:
        digest.update(record.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def local_adjacency(tree):
    cut_count = len(tree.edges) + 1 - CYCLE_COUNT
    require(cut_count >= 1, "incidence row has no shared cut")
    adjacency = [[] for _ in range(CYCLE_COUNT + cut_count)]
    for cycle, cut in tree.edges:
        require(0 <= cycle < CYCLE_COUNT <= cut < len(adjacency),
                "incidence row has a non-bipartite edge")
        adjacency[cycle].append(cut)
        adjacency[cut].append(cycle)
    return tuple(tuple(sorted(row)) for row in adjacency)


def local_signature(tree, adjacency):
    degrees = [len(row) for row in adjacency]
    leaves = [vertex for vertex, degree in enumerate(degrees) if degree <= 1]
    remaining = len(adjacency)
    while remaining > 2:
        require(leaves, "canonical center search stalled")
        remaining -= len(leaves)
        next_leaves = []
        for leaf in leaves:
            for neighbor in adjacency[leaf]:
                degrees[neighbor] -= 1
                if degrees[neighbor] == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves

    def rooted(vertex, parent):
        label = tree.colors[vertex] if vertex < CYCLE_COUNT else "X"
        children = sorted(rooted(child, vertex) for child in adjacency[vertex]
                          if child != parent)
        return label + "(" + "".join(children) + ")"

    require(leaves, "canonical row has no center")
    return min(rooted(center, -1) for center in leaves)


def validate_classes(classes):
    require(len(classes) == 115512, "canonical class total changed")
    signatures = tuple(signature for signature, _ in classes)
    require(signatures == tuple(sorted(signatures)), "canonical rows are not sorted")
    require(len(signatures) == len(set(signatures)), "canonical signatures repeat")
    counts = Counter()
    for signature, tree in classes:
        require(Counter(tree.colors) == Counter(T=9, P=2),
                "canonical row has wrong cycle colors")
        require(len(tree.edges) == len(set(tree.edges)), "incidence edge repeats")
        adjacency = local_adjacency(tree)
        require(len(tree.edges) == len(adjacency) - 1,
                "incidence representative is not a tree")
        require(all(len(adjacency[cut]) >= 2
                    for cut in range(CYCLE_COUNT, len(adjacency))),
                "incidence representative has a redundant cut leaf")
        require(all(1 <= len(adjacency[cycle]) <= (3 if color == "T" else 5)
                    for cycle, color in enumerate(tree.colors)),
                "cycle incidence capacity changed")
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(len(seen) == len(adjacency), "incidence representative is disconnected")
        require(signature == local_signature(tree, adjacency),
                "stored signature is not independently canonical")
        counts[len(adjacency) - CYCLE_COUNT] += 1
    require(counts == EXPECTED_ALL_BY_CUT, "canonical cut-count census changed")
    digest = stream_digest(signatures)
    require(digest == EXPECTED_CLASS_DIGEST, "canonical signature digest changed")
    return digest


def physical_vertex(vertex):
    if isinstance(vertex, CORE.CyclicVertex) and vertex.cut is not None:
        return CORE.CutSite(vertex.cut)
    return vertex


def incidence_geometry(signature, tree, adjacency):
    geometries = []
    for cycle, color in enumerate(tree.colors):
        cuts = adjacency[cycle]
        length = 3 if color == "T" else 5
        vertices = tuple(
            CORE.CyclicVertex(
                f"{signature}:C{cycle}:{color}", index,
                "cut" if index < len(cuts) else "private",
                cuts[index] if index < len(cuts) else None,
            )
            for index in range(length)
        )
        geometry = CORE.make_cycle(f"{signature}:C{cycle}:{color}", vertices)
        require(tuple(vertex.cut for vertex in geometry.vertices if vertex.cut is not None)
                == cuts, "concrete cyclic cuts disagree with incidence order")
        geometries.append(geometry)
    bound_edges = Counter(
        (cycle, vertex.cut)
        for cycle, geometry in enumerate(geometries)
        for vertex in geometry.vertices if vertex.cut is not None
    )
    require(bound_edges == Counter(tree.edges),
            "concrete positions do not bind exactly to incidence edges")
    return tuple(geometries)


def physical_graph(geometries, sacrificed=None):
    vertices = []
    edges = []
    for geometry in geometries:
        vertices.extend(physical_vertex(vertex) for vertex in geometry.vertices)
        edges.extend((physical_vertex(left), physical_vertex(right))
                     for left, right in geometry.edges)
    remnant_anchors = ()
    if sacrificed is not None:
        remnant_anchors = tuple(
            (RouterRemnant(sacrificed, vertex.index), physical_vertex(vertex))
            for vertex in geometries[sacrificed].vertices
            if vertex.role == "private"
        )
        vertices.extend(remnant for remnant, _ in remnant_anchors)
        edges.extend((anchor, remnant) for remnant, anchor in remnant_anchors)
    vertices = tuple(dict.fromkeys(vertices))
    expected_hull_count = 9 * 3 + 2 * 5 - sum(
        len(positions) - 1 for positions in (
            tuple(vertex for geometry in geometries for vertex in geometry.vertices
                  if vertex.cut == cut)
            for cut in {vertex.cut for geometry in geometries
                        for vertex in geometry.vertices if vertex.cut is not None}
        )
    )
    require(len(vertices) == expected_hull_count + len(remnant_anchors),
            "physical cut/remnant vertex count is incorrect")
    return vertices, tuple(edges), remnant_anchors


def expected_attachment_specification(vertices, remnant_anchors):
    """Reconstruct symbolic arbitrary-forest domains from physical anchors."""
    anchors = tuple(vertices)
    domain = tuple(ForestAttachment(anchor) for anchor in anchors)
    records = tuple(zip(domain, anchors))
    require(len(domain) == len(set(domain)), "reconstructed forest domain aliases")
    require(set(remnant for remnant, _ in remnant_anchors) <= set(anchors),
            "router remnant is missing from reconstructed forest anchors")
    return domain, records


def components_after_deletion(adjacency, sacrificed):
    components = []
    seen = {sacrificed}
    for port in adjacency[sacrificed]:
        require(port not in seen, "two sacrificed ports enter one component")
        stack = [port]
        seen.add(port)
        vertices = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        cycles = tuple(sorted(vertex for vertex in vertices if vertex < CYCLE_COUNT))
        require(cycles, "ordinary split creates a cycle-free port component")
        components.append((port, frozenset(vertices), cycles))
    require(set().union(*(set(component) for _, component, _ in components))
            == set(range(len(adjacency))) - {sacrificed},
            "ordinary components are not exhaustive")
    return tuple(components)


def connected_cycles(tree, cycles, adjacency):
    cycles = set(cycles)
    seen = {min(cycles)}
    stack = list(seen)
    while stack:
        cycle = stack.pop()
        for cut in adjacency[cycle]:
            for neighbor in adjacency[cut]:
                if neighbor in cycles and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return seen == cycles


def pairwise_intersecting(cycles, adjacency):
    return all(set(adjacency[first]) & set(adjacency[second])
               for index, first in enumerate(cycles)
               for second in cycles[index + 1:])


def common_cut(cycles, adjacency):
    common = set(adjacency[cycles[0]])
    for cycle in cycles[1:]:
        common &= set(adjacency[cycle])
    return min(common) if common else None


def terminal_packet(tree, owner, cycles, adjacency):
    cycles = tuple(sorted(cycles))
    require(cycles, "ordinary terminal has no complete cycle")
    require(connected_cycles(tree, cycles, adjacency),
            "ordinary terminal cycle carrier is disconnected")
    triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
    pentagons = tuple(cycle for cycle in cycles if tree.colors[cycle] == "P")
    t, p = len(triangles), len(pentagons)
    rank = t + p
    if p == 0:
        require(t in TRIANGLE_MARGIN, "pure triangular packet rank is unsupported")
        hub = common_cut(triangles, adjacency)
        theorem = "common-cut-triangular-margin" if hub is not None else "rank-triangular-margin"
        hypothesis = (f"all retained triangles contain cut {hub}" if hub is not None
                      else f"complete connected triangular cactus of rank {t}")
        return Packet(owner, cycles, theorem, hypothesis,
                      Bound(Fraction(TRIANGLE_MARGIN[t]), 0, True))
    if t == 0 and p == 1:
        return Packet(owner, cycles, "P-deficit", "one complete pentagon",
                      Bound(Fraction(0), 1, False))
    if t == 0 and p == 2:
        return Packet(owner, cycles, "PP-nonnegative",
                      "complete connected two-pentagon cactus", ZERO)
    if t == 1 and p == 1:
        return Packet(owner, cycles, "TP-quantitative", "complete connected TP cactus",
                      Bound(Fraction(1), 1, True))
    if t == 1 and p == 2:
        return Packet(owner, cycles, "TPP-strict", "complete connected TPP cactus",
                      Bound(Fraction(3, 2), 0, True))
    if t == 2 and p == 1 and common_cut(cycles, adjacency) is not None:
        hub = common_cut(cycles, adjacency)
        return Packet(owner, cycles, "common-cut-TTP-quantitative",
                      f"both triangles and the pentagon contain cut {hub}",
                      Bound(Fraction(7, 4), 0, True))
    if t == 3 and p == 1:
        shared_pairs = tuple(
            cut for cut in range(CYCLE_COUNT, len(adjacency))
            if len(set(triangles) & set(adjacency[cut])) >= 2
        )
        if shared_pairs:
            return Packet(owner, cycles, "shared-pair-T3P-quantitative",
                          f"two retained triangles contain cut {min(shared_pairs)}",
                          Bound(Fraction(1), 0, True))
    if p == 1 and pairwise_intersecting(triangles, adjacency):
        hub = common_cut(triangles, adjacency)
        theorem = "one-hostile-common-cut" if hub is not None else "one-hostile-packing-one"
        hypothesis = (f"all retained triangles contain cut {hub}" if hub is not None
                      else "every pair of retained triangles intersects")
        return Packet(owner, cycles, theorem, hypothesis, Bound(Fraction(t), 1, True))
    if 2 <= rank <= 3:
        return Packet(owner, cycles, "connected-rank-2/3-nonnegative",
                      f"complete connected cyclic rank {rank}", ZERO)
    if 4 <= rank <= 10:
        return Packet(owner, cycles, "connected-rank-4..10-strict",
                      f"complete connected cyclic rank {rank}", Bound(0, 0, True))
    raise UnprovedPacket(f"unproved owned terminal profile T^{t}P^{p}")


def canonical_intervals(geometry, components):
    ports = tuple(CORE.CutSite(port) for port, _, _ in components)
    vertices = tuple(physical_vertex(vertex) for vertex in geometry.vertices)
    require(vertices[:len(ports)] == ports,
            "canonical concrete port positions are not in component order")
    intervals = tuple((port,) for port in ports[:-1]) + (vertices[len(ports) - 1:],)
    owners = tuple(range(len(components)))
    physical_geometry = CORE.CycleGeometry(
        geometry.label, geometry.length, vertices,
        tuple((physical_vertex(left), physical_vertex(right))
              for left, right in geometry.edges),
    )
    if len(intervals) <= 3:
        CORE.verify_router_owner_split(physical_geometry, intervals, owners)
    else:
        CORE.verify_c5_router_owner_split(
            physical_geometry, intervals, owners
        )
    return intervals, owners


def make_certificate(signature, tree, sacrificed):
    adjacency = local_adjacency(tree)
    components = components_after_deletion(adjacency, sacrificed)
    if len(components) < 2:
        return None
    geometries = incidence_geometry(signature, tree, adjacency)
    vertices, edges, remnant_anchors = physical_graph(geometries, sacrificed)
    intervals, interval_owners = canonical_intervals(geometries[sacrificed], components)
    owners = {}

    def own(vertex, owner):
        old = owners.setdefault(vertex, owner)
        require(old == owner, "physical vertex receives competing ordinary owners")

    component_owner = {
        vertex: owner
        for owner, (_, component, _) in enumerate(components)
        for vertex in component
    }
    for cycle, geometry in enumerate(geometries):
        if cycle == sacrificed:
            continue
        for vertex in geometry.vertices:
            incidence_vertex = vertex.cut if vertex.cut is not None else cycle
            own(physical_vertex(vertex), component_owner[incidence_vertex])
    for owner, interval in zip(interval_owners, intervals):
        for vertex in interval:
            own(vertex, owner)
    for remnant, anchor in remnant_anchors:
        own(remnant, owners[anchor])
    require(set(owners) == set(vertices), "ordinary physical owner domain is incomplete")
    attachment_domain, attachment_anchors = expected_attachment_specification(
        vertices, remnant_anchors
    )
    attachment_owners = tuple(
        (site, owners[anchor]) for site, anchor in attachment_anchors
    )
    packets = tuple(
        terminal_packet(tree, owner, cycles, adjacency)
        for owner, (_, _, cycles) in enumerate(components)
    )
    bound = sum((packet.bound for packet in packets), ZERO)
    if not bound.positive():
        return None
    certificate = Certificate(
        signature, sacrificed,
        tuple(tuple(physical_vertex(vertex) for vertex in geometry.vertices)
              for geometry in geometries),
        intervals, interval_owners, vertices, edges,
        remnant_anchors, tuple(owners.items()), attachment_owners, packets, bound,
    )
    verify_certificate(tree, certificate)
    return certificate if bound.positive() else None


def ordinary_candidate(tree, sacrificed, adjacency):
    components = components_after_deletion(adjacency, sacrificed)
    if len(components) < 2:
        return False
    total = Fraction(0)
    strict = False
    for _, component, cycles in components:
        triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
        pentagons = tuple(cycle for cycle in cycles if tree.colors[cycle] == "P")
        t, p = len(triangles), len(pentagons)
        rank = t + p
        internal_cuts = tuple(
            cut for cut in component if cut >= CYCLE_COUNT
            and len(set(cycles) & set(adjacency[cut])) >= 2
        )
        if p == 0:
            value, flag = Fraction(TRIANGLE_MARGIN[t]), True
        elif rank == 1:
            value, flag = Fraction(-1, 4), True
        elif (t, p) == (1, 1):
            value, flag = Fraction(3, 4), True
        elif (t, p) == (0, 2):
            value, flag = Fraction(0), True
        elif (t, p) == (2, 1) and any(
                set(triangles) <= set(adjacency[cut]) for cut in internal_cuts):
            value, flag = Fraction(7, 4), True
        elif (t, p) == (1, 2):
            value, flag = Fraction(3, 2), True
        elif rank == 3:
            value, flag = Fraction(0), False
        elif (t, p) == (3, 1) and any(
                len(set(triangles) & set(adjacency[cut])) >= 2
                for cut in internal_cuts):
            value, flag = Fraction(1), True
        elif 4 <= rank <= 10:
            value, flag = Fraction(0), True
        else:
            raise UnprovedPacket(f"ordinary ledger has unknown T^{t}P^{p} profile")
        total += value
        strict = strict or flag
    return total > 0 or total == 0 and strict


def complete_owned_cycles(tree, certificate, owner_map):
    answer = {owner: [] for owner in certificate.interval_owners}
    for cycle, vertices in enumerate(certificate.geometry_vertices):
        cycle_owners = {owner_map[vertex] for vertex in vertices}
        if len(cycle_owners) == 1:
            answer[next(iter(cycle_owners))].append(cycle)
    return {owner: tuple(cycles) for owner, cycles in answer.items()}


def verify_owned_cactus_profiles(certificate, owner_map, edge_keys, owned,
                                 complete, attachment_map, attachment_anchors):
    """Check connected cactus cores and tree-uniform forest attachment scope."""
    anchor_map = dict(attachment_anchors)
    require(set(attachment_map) == set(anchor_map),
            "forest attachment domain differs from independent reconstruction")
    for owner, domain in owned.items():
        internal_edges = sum(edge <= domain for edge in edge_keys)
        cyclomatic = internal_edges - len(domain) + 1
        require(cyclomatic == len(complete[owner]),
                "owner-induced graph is not a cactus with exactly its complete cycles")
        remnants = {remnant for remnant, _ in certificate.remnant_anchors
                    if remnant in domain}
        for remnant in remnants:
            anchor = dict(certificate.remnant_anchors)[remnant]
            require(owner_map[anchor] == owner_map[remnant] == owner,
                    "private router remnant drifted from its interval owner")
            incident = sum(remnant in edge for edge in edge_keys)
            require(incident == 1, "private router remnant is not a forest leaf")
        owner_attachments = {site for site, assigned in attachment_map.items()
                             if assigned == owner}
        require(all(anchor_map[site] in domain for site in owner_attachments),
                "forest attachment is outside its owner-induced cactus")
        require(owner_attachments,
                "owner-induced cactus has no reconstructed tree-uniform forest domain")


def verify_certificate(tree, certificate):
    adjacency = local_adjacency(tree)
    geometries = incidence_geometry(certificate.signature, tree, adjacency)
    expected_vertices, expected_edges, expected_remnant_anchors = physical_graph(
        geometries, certificate.sacrificed
    )
    expected_attachment_domain, expected_attachment_anchors = (
        expected_attachment_specification(expected_vertices, expected_remnant_anchors)
    )
    components = components_after_deletion(adjacency, certificate.sacrificed)
    expected_intervals, expected_interval_owners = canonical_intervals(
        geometries[certificate.sacrificed], components
    )
    require(certificate.geometry_vertices == tuple(
                tuple(physical_vertex(vertex) for vertex in geometry.vertices)
                for geometry in geometries),
            "submitted concrete cycle positions differ from incidence geometry")
    require(certificate.interval_vertices == expected_intervals and
            certificate.interval_owners == expected_interval_owners,
            "submitted ordinary intervals differ from canonical concrete intervals")
    require(certificate.remnant_anchors == expected_remnant_anchors,
            "submitted router-remnant anchors differ from reconstructed anchors")
    owner_map, edge_keys, owned = CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachment_domain,
        certificate.vertices, certificate.edges, certificate.vertex_owners,
        certificate.attachment_owners, expected_interval_owners,
        expected_attachment_anchors,
    )
    attachment_map = CORE.exact_owner_map(
        certificate.attachment_owners, expected_attachment_domain,
        "submitted forest attachment owners"
    )
    for interval, owner in zip(certificate.interval_vertices,
                               certificate.interval_owners):
        require(all(owner_map[vertex] == owner for vertex in interval),
                "concrete interval vertex does not have its declared interval owner")
    for owner, (port, component, _) in enumerate(components):
        require(owner_map[CORE.CutSite(port)] == owner,
                "ordinary port cut does not follow its interval owner")
        for vertex in component:
            if vertex >= CYCLE_COUNT:
                require(owner_map[CORE.CutSite(vertex)] == owner,
                        "shared cut does not follow its incidence component")
        require(owned[owner], "ordinary final owner has an empty physical domain")
    complete = complete_owned_cycles(tree, certificate, owner_map)
    verify_owned_cactus_profiles(
        certificate, owner_map, edge_keys, owned, complete,
        attachment_map, expected_attachment_anchors,
    )
    derived_packets = tuple(
        terminal_packet(tree, owner, complete[owner], adjacency)
        for owner in expected_interval_owners
    )
    require(certificate.packets == derived_packets,
            "terminal packet theorem was not reclassified after physical ownership")
    derived_bound = sum((packet.bound for packet in derived_packets), ZERO)
    require(certificate.bound == derived_bound,
            "ordinary ledger is not the exact post-ownership packet sum")
    require(certificate.bound.positive(), "ordinary post-ownership ledger is not positive")


def certificate_text(certificate):
    intervals = tuple(tuple(repr(vertex) for vertex in interval)
                      for interval in certificate.interval_vertices)
    owners = tuple(sorted((repr(vertex), owner)
                          for vertex, owner in certificate.vertex_owners))
    attachments = tuple(sorted((repr(site), owner)
                               for site, owner in certificate.attachment_owners))
    packets = tuple((packet.owner, packet.cycles, packet.theorem,
                     packet.hypothesis, packet.bound)
                    for packet in certificate.packets)
    return repr((certificate.signature, certificate.sacrificed,
                 certificate.geometry_vertices, intervals,
                 certificate.interval_owners, certificate.remnant_anchors,
                 owners, attachments, packets, certificate.bound))


def expect_rejected(action, label):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def mutation_self_tests(fixtures):
    tree, certificate = fixtures[2]
    tests = 0
    first = certificate.interval_vertices[0][0]
    bad_intervals = ((certificate.interval_vertices[0] +
                      (certificate.interval_vertices[1][0],)),) + certificate.interval_vertices[1:]
    expect_rejected(lambda: verify_certificate(
        tree, replace(certificate, interval_vertices=bad_intervals)),
        "overlapping concrete interval",
    )
    tests += 1
    owner_map = dict(certificate.vertex_owners)
    drift = certificate.interval_vertices[0][0]
    owner_map[drift] = certificate.interval_owners[1]
    attachments = dict(certificate.attachment_owners)
    attachments[ForestAttachment(drift)] = certificate.interval_owners[1]
    expect_rejected(lambda: verify_certificate(
        tree, replace(certificate, vertex_owners=tuple(owner_map.items()),
                      attachment_owners=tuple(attachments.items()))),
        "coordinated interval/attachment owner drift",
    )
    tests += 1
    owner_map = dict(certificate.vertex_owners)
    owner_map[first] = (owner_map[first] + 1) % len(certificate.interval_owners)
    expect_rejected(lambda: verify_certificate(
        tree, replace(certificate, vertex_owners=tuple(owner_map.items()))),
        "changed physical vertex owner",
    )
    tests += 1
    forged = replace(certificate.packets[0], theorem="forged-rank-ten-theorem")
    expect_rejected(lambda: verify_certificate(
        tree, replace(certificate, packets=(forged,) + certificate.packets[1:])),
        "forged terminal theorem",
    )
    tests += 1
    expect_rejected(lambda: verify_certificate(
        tree, replace(certificate, attachment_owners=certificate.attachment_owners[:-1])),
        "missing attachment owner",
    )
    tests += 1

    tree4, certificate4 = fixtures[4]
    geometry4 = CORE.CycleGeometry(
        f"mutation:C5:d4", 5,
        certificate4.geometry_vertices[certificate4.sacrificed],
        tuple((certificate4.geometry_vertices[certificate4.sacrificed][index],
               certificate4.geometry_vertices[certificate4.sacrificed][(index + 1) % 5])
              for index in range(5)),
    )
    expect_rejected(lambda: CORE.verify_router_owner_split(
        geometry4, certificate4.interval_vertices,
        certificate4.interval_owners, allowed_owner_counts=(2, 3)),
        "unsupported four-owner arity at old-call defaults",
    )
    tests += 1

    tree5, certificate5 = fixtures[5]
    expect_rejected(lambda: verify_certificate(
        tree5, replace(certificate5,
                       interval_vertices=certificate5.interval_vertices[:-1],
                       interval_owners=certificate5.interval_owners[:-1])),
        "fifth C5 interval omission",
    )
    tests += 1
    remnant, _ = certificate4.remnant_anchors[0]
    deleted_vertices = tuple(vertex for vertex in certificate4.vertices
                             if vertex != remnant)
    deleted_edges = tuple(edge for edge in certificate4.edges if remnant not in edge)
    deleted_owners = tuple(record for record in certificate4.vertex_owners
                           if record[0] != remnant)
    deleted_attachments = tuple(record for record in certificate4.attachment_owners
                                if record[0] != ForestAttachment(remnant))
    deleted_anchors = tuple(record for record in certificate4.remnant_anchors
                            if record[0] != remnant)
    expect_rejected(lambda: verify_certificate(
        tree4, replace(certificate4, vertices=deleted_vertices,
                       edges=deleted_edges, vertex_owners=deleted_owners,
                       attachment_owners=deleted_attachments,
                       remnant_anchors=deleted_anchors)),
        "coordinated remnant cycle/domain deletion",
    )
    tests += 1
    return tests


def main():
    classes = BASE.enumerate_colors(tuple(sorted(COLORS)), 0)
    class_digest = validate_classes(classes)
    safe_by_cut = Counter()
    theorem_counts = Counter()
    residuals = []
    proof_hasher = sha256()
    accepted_hasher = sha256()
    candidate_hasher = sha256()
    physical_candidate_count = 0
    fixtures = {}
    router_degrees = Counter()
    router_degree_signatures = {4: [], 5: []}
    for index, (signature, tree) in enumerate(classes, 1):
        adjacency = local_adjacency(tree)
        physical_candidates = []
        for sacrificed in range(CYCLE_COUNT):
            try:
                accepted = ordinary_candidate(tree, sacrificed, adjacency)
            except UnprovedPacket:
                accepted = False
            if accepted:
                certificate = make_certificate(signature, tree, sacrificed)
                require(certificate is not None,
                        f"abstract SAFE candidate failed physical certification: "
                        f"{signature} cycle={sacrificed}")
                verify_certificate(tree, certificate)
                physical_candidates.append(certificate)
                physical_candidate_count += 1
                candidate_hasher.update(
                    certificate_text(certificate).encode("ascii") + b"\n"
                )
        if not physical_candidates:
            residuals.append((signature, tree))
        else:
            certificate = min(physical_candidates, key=lambda item: item.sacrificed)
            degree = len(certificate.interval_owners)
            router_degrees[degree] += 1
            if degree in router_degree_signatures:
                router_degree_signatures[degree].append(signature)
            safe_by_cut[len(local_adjacency(tree)) - CYCLE_COUNT] += 1
            theorem_counts.update(packet.theorem for packet in certificate.packets)
            line = certificate_text(certificate).encode("ascii") + b"\n"
            proof_hasher.update(line)
            accepted_hasher.update(signature.encode("ascii") + b"\n")
            fixtures.setdefault(degree, (tree, certificate))
        if index % 10000 == 0:
            print(f"checked {index}/{len(classes)}", flush=True)

    proof_digest = proof_hasher.hexdigest()
    candidate_digest = candidate_hasher.hexdigest()
    accepted_digest = accepted_hasher.hexdigest()
    residual_digest = stream_digest(signature for signature, _ in residuals)
    require(set((2, 4, 5)) <= set(fixtures),
            "missing degree-2/4/5 mutation fixtures")
    mutation_count = mutation_self_tests(fixtures)
    degree4_digest = stream_digest(router_degree_signatures[4])
    degree5_digest = stream_digest(router_degree_signatures[5])

    print("fully shared T^9PP rows:", len(classes))
    print("ordinary physical-owner SAFE:", sum(safe_by_cut.values()))
    print("physical theorem certificates for abstract SAFE candidates:",
          physical_candidate_count)
    print("fail-closed residual rows:", len(residuals))
    print("all by cut:", dict(sorted(EXPECTED_ALL_BY_CUT.items())))
    print("SAFE by cut:", dict(sorted(safe_by_cut.items())))
    print("post-ownership theorem uses:", dict(sorted(theorem_counts.items())))
    print("selected router degrees:", dict(sorted(router_degrees.items())))
    print("degree-4 signatures:", len(router_degree_signatures[4]),
          "sha256=" + degree4_digest)
    print("degree-5 signatures:", len(router_degree_signatures[5]),
          "sha256=" + degree5_digest)
    require(router_degree_signatures[5], "degree-five signature stream is empty")
    print("degree-5 first signature:", router_degree_signatures[5][0])
    print("canonical-row sha256:", class_digest)
    print("ordinary-signature sha256:", accepted_digest)
    print("physical-proof sha256:", proof_digest)
    print("all-candidate physical-proof sha256:", candidate_digest)
    print("residual sha256:", residual_digest)
    print("rejected hostile mutations:", mutation_count)
    for number, (signature, _) in enumerate(residuals, 1):
        print(f"U{number}: {signature}")
    print(f"FIRST-PHASE ONLY: {len(classes)}={sum(safe_by_cut.values())}+{len(residuals)}; residuals remain fail-closed")

    require(safe_by_cut == EXPECTED_SAFE_BY_CUT, "ordinary SAFE cut-count census changed")
    require(sum(safe_by_cut.values()) == 115502, "ordinary physical-owner SAFE total changed")
    require(len(residuals) == 10, "exact fail-closed residual count changed")
    require(accepted_digest == EXPECTED_ACCEPTED_DIGEST,
            "ordinary accepted-signature digest changed")
    require(proof_digest == EXPECTED_PHYSICAL_DIGEST,
            "ordinary physical-proof digest changed")
    require(residual_digest == EXPECTED_RESIDUAL_DIGEST,
            "fail-closed residual digest changed")
    require(router_degrees == EXPECTED_ROUTER_DEGREES,
            "selected physical router-degree census changed")
    require(degree4_digest == EXPECTED_DEGREE4_DIGEST,
            "degree-four selected-signature digest changed")
    require(degree5_digest == EXPECTED_DEGREE5_DIGEST,
            "degree-five selected-signature digest changed")
    require(physical_candidate_count == EXPECTED_CANDIDATE_COUNT,
            "abstract SAFE physical-certificate count changed")
    require(candidate_digest == EXPECTED_CANDIDATE_DIGEST,
            "all abstract SAFE physical-certificate digest changed")
    require(mutation_count == 8, "hostile mutation count changed")


if __name__ == "__main__":
    main()
