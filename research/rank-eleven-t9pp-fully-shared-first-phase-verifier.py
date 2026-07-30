#!/usr/bin/env python3
"""Fail-closed physical verifier for fully shared rank-eleven T^9PP.

The verifier regenerates the complete color-preserving incidence universe and
searches ordinary one-cycle splits.  Every accepted split is then rebuilt on a
concrete C3/C5 geometry, given exhaustive physical final owners, and classified
again from the owned terminal packets.  The ten nonordinary rows are closed by
separately reconstructed physical opening/router certificates.
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
EXPECTED_REPAIR_DIGEST = "eedc3bebd64e4711849115b3846db2eee2a93cd7ffee628e49f7a3133f73c324"
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


@dataclass(frozen=True)
class RadicalLedger:
    credit: Fraction
    deficits: int
    sqrt13_charge: Fraction
    strict: bool

    def positive(self):
        if self.sqrt13_charge:
            require(self.deficits == 0,
                    "mixed sqrt(5)/sqrt(13) repair ledger is unsupported")
            return (self.credit > 0 and
                    13 * self.credit * self.credit >
                    self.sqrt13_charge * self.sqrt13_charge)
        return Bound(self.credit, self.deficits, self.strict).positive()


@dataclass(frozen=True)
class RepairPacket:
    owner: str
    cycles: tuple[int, ...]
    theorem: str
    hypothesis: str
    bound: Bound


@dataclass(frozen=True)
class RepairCertificate:
    code: str
    signature: str
    operation: str
    routers: tuple[int, ...]
    opened: tuple[int, ...]
    nesting: tuple[int, ...]
    router_splits: tuple[tuple[int, tuple[tuple[object, ...], ...],
                               tuple[str, ...]], ...]
    opening_splits: tuple[tuple[int, tuple[tuple[object, ...], ...],
                                tuple[str, str]], ...]
    geometry_vertices: tuple[tuple[object, ...], ...]
    vertices: tuple[object, ...]
    edges: tuple[tuple[object, object], ...]
    remnant_anchors: tuple[tuple[RouterRemnant, object], ...]
    vertex_owners: tuple[tuple[object, str], ...]
    attachment_owners: tuple[tuple[ForestAttachment, str], ...]
    packets: tuple[RepairPacket, ...]
    ledger: RadicalLedger


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


REPAIR_SIGNATURES = (
    "X(P()P()T()T()T()T()T()T()T()T()T())",
    "P(X(P())X(T()T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T()T()T()))",
    "P(X(P())X(T())X(T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P())X(T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T()T())X(T()))",
    "X(T()T()T()T()T()T()T()T(X(P()))T(X(P())))",
    "P(X(P())X(T())X(T())X(T()T()T()T()T()T()T()))",
    "X(T()T()T()T()T()T()T(X(P()))T(X(P())X(T())))",
    "X(T()T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))",
)


def repair_spec(code):
    specs = {
        "U1": ("common-cut-T9PP", (), (), (), (),
               (("all", tuple(range(11)), "common-cut-T9PP"),),
               RadicalLedger(Fraction(10), 0, Fraction(4, 3), True)),
        "U2": ("open-leaf-P+common-cut-T9P", (), (10,), (), (),
               (("retained", tuple(range(10)), "common-cut-T9P"),),
               RadicalLedger(Fraction(8), 1, 0, True)),
        "U3": ("P+common-cut-T8P", (0,), (), (0,),
               ((0, ((12,), (11,)), ("P", "retained")),),
               (("P", (9,), "P"),
                ("retained", tuple(range(1, 9)) + (10,), "common-cut-T8P")),
               RadicalLedger(Fraction(8), 2, 0, True)),
        "U4": ("A8+TP-via-C5", (0,), (), (0,),
               ((0, ((11,), (12, 13)), ("A8", "TP")),),
               (("A8", (1,) + tuple(range(3, 10)), "common-cut-A8"),
                ("TP", (2, 10), "TP-quantitative")),
               RadicalLedger(Fraction(3, 4), 0, 0, True)),
        "U5": ("opening+packing-one-T9P", (), (9,), (), (),
               (("retained", tuple(range(9)) + (10,), "packing-one-T9P"),),
               RadicalLedger(Fraction(8), 1, 0, True)),
        "U6": ("P+T+common-cut-T7P", (0,), (), (0,),
               ((0, ((11,), (12,), (13,)), ("retained", "T", "P")),),
               (("P", (9,), "P"), ("T", (2,), "T"),
                ("retained", (1,) + tuple(range(3, 9)) + (10,),
                 "common-cut-T7P")),
               RadicalLedger(Fraction(7), 2, 0, True)),
        "U7": ("one-router-P+packing-one-T8P", (0,), (), (0,),
               ((0, ((12,), (11,)), ("P", "retained")),),
               (("P", (9,), "P"),
                ("retained", tuple(range(1, 9)) + (10,), "packing-one-T8P")),
               RadicalLedger(Fraction(8), 2, 0, True)),
        "U8": ("degree4-C5-T+rank9-T8P", (0,), (), (0,),
               ((0, ((12,), (11, 13, 14)), ("T", "rank9")),),
               (("T", (2,), "T"),
                ("rank9", (1,) + tuple(range(3, 11)), "connected-rank9-T8P")),
               RadicalLedger(Fraction(0), 0, 0, True)),
        "U9": ("nested-P+P+T+A6", (0, 1), (), (0, 1),
               ((0, ((11,), (12,), (13,)), ("active", "T", "P1")),
                (1, ((14,), (11,)), ("P2", "A6"))),
               (("P1", (9,), "P"), ("P2", (10,), "P"),
                ("T", (2,), "T"), ("A6", tuple(range(3, 9)), "common-cut-A6")),
               RadicalLedger(Fraction(1), 2, 0, True)),
        "U10": ("nested-P+P+T+T+A5", (0, 1), (), (0, 1),
                ((0, ((11,), (12,), (14,)), ("active", "T1", "P1")),
                 (1, ((11,), (13,), (15,)), ("A5", "T2", "P2"))),
                (("P1", (9,), "P"), ("P2", (10,), "P"),
                 ("T1", (2,), "T"), ("T2", (8,), "T"),
                 ("A5", tuple(range(3, 8)), "common-cut-A5")),
                RadicalLedger(Fraction(2), 2, 0, True)),
    }
    return specs[code]


def repair_graph(geometries, routers):
    vertices, edges, remnants = physical_graph(geometries)
    vertices, edges, remnants = list(vertices), list(edges), list(remnants)
    for router in routers:
        for vertex in geometries[router].vertices:
            if vertex.role == "private":
                remnant = RouterRemnant(router, vertex.index)
                anchor = physical_vertex(vertex)
                vertices.append(remnant)
                edges.append((anchor, remnant))
                remnants.append((remnant, anchor))
    return tuple(vertices), tuple(edges), tuple(remnants)


def intervals_for_ports(geometry, port_groups):
    vertices = tuple(physical_vertex(vertex) for vertex in geometry.vertices)
    position = {vertex.cut: index for index, vertex in enumerate(geometry.vertices)
                if vertex.cut is not None}
    claimed = {}
    for group_index, ports in enumerate(port_groups):
        for port in ports:
            require(port in position and position[port] not in claimed,
                    "repair interval names an absent or repeated port")
            claimed[position[port]] = group_index
    require(set(position.values()) == set(claimed),
            "repair intervals do not partition occupied router ports")
    if len(port_groups) == 2 and len(port_groups[0]) == 1:
        singleton = position[port_groups[0][0]]
        order = tuple(vertices[(singleton + offset) % len(vertices)]
                      for offset in range(len(vertices)))
        return ((order[0],), order[1:])
    require(len(port_groups) == len(vertices),
            "nonbinary repair must use forced singleton intervals")
    return tuple((vertices[position[group[0]]],) for group in port_groups)


def make_repair_certificate(code, signature, tree):
    operation, routers, opened, nesting, split_specs, packet_specs, ledger = repair_spec(code)
    require(signature == REPAIR_SIGNATURES[int(code[1:]) - 1],
            f"{code}: exact residual signature changed")
    adjacency = local_adjacency(tree)
    geometries = incidence_geometry(signature, tree, adjacency)
    vertices, edges, remnants = repair_graph(geometries, routers)
    packet_cycle_owner = {cycle: owner for owner, cycles, _ in packet_specs for cycle in cycles}
    require(len(packet_cycle_owner) == sum(len(cycles) for _, cycles, _ in packet_specs),
            f"{code}: repair packets overlap")
    require(set(packet_cycle_owner) == set(range(CYCLE_COUNT)) - set(routers) - set(opened),
            f"{code}: retained cycle domain is inexact")
    split_cut_owners = {}
    for _, groups, group_owners in split_specs:
        for group, owner in zip(groups, group_owners):
            terminal_owner = owner
            if owner == "active":
                terminal_owner = "A6" if code == "U9" else "A5"
            for cut in group:
                old = split_cut_owners.setdefault(cut, terminal_owner)
                require(old == terminal_owner,
                        f"{code}: nested routers disagree on a cut owner")
    cut_owners = {}
    for cut in range(CYCLE_COUNT, len(adjacency)):
        candidates = {packet_cycle_owner[cycle] for cycle in adjacency[cut]
                      if cycle in packet_cycle_owner}
        if cut in split_cut_owners:
            require(split_cut_owners[cut] in candidates,
                    f"{code}: router cut owner does not retain an incident branch")
            cut_owners[cut] = split_cut_owners[cut]
        else:
            require(len(candidates) == 1, f"{code}: cut has no unique terminal owner")
            cut_owners[cut] = next(iter(candidates))
    router_splits = []
    router_vertex_owners = {}
    for router, groups, owners in split_specs:
        intervals = intervals_for_ports(geometries[router], groups)
        physical_geometry = CORE.CycleGeometry(
            geometries[router].label, geometries[router].length,
            tuple(physical_vertex(vertex) for vertex in geometries[router].vertices),
            tuple((physical_vertex(left), physical_vertex(right))
                  for left, right in geometries[router].edges),
        )
        if physical_geometry.length == 5:
            CORE.verify_c5_router_owner_split(physical_geometry, intervals, owners)
        else:
            CORE.verify_router_owner_split(physical_geometry, intervals, owners)
        router_splits.append((router, intervals, owners))
        for interval, owner in zip(intervals, owners):
            terminal_owner = owner
            if owner == "active":
                terminal_owner = "A6" if code == "U9" else "A5"
            for vertex in interval:
                router_vertex_owners[vertex] = terminal_owner
    opening_splits = []
    opening_vertex_owners = {}
    for cycle in opened:
        require(len(adjacency[cycle]) == 1, f"{code}: opened pentagon is not a leaf")
        cut = adjacency[cycle][0]
        root = CORE.CutSite(cut)
        cycle_vertices = tuple(physical_vertex(vertex) for vertex in geometries[cycle].vertices)
        start = cycle_vertices.index(root)
        order = tuple(cycle_vertices[(start + offset) % 5] for offset in range(5))
        retained_owner = cut_owners[cut]
        opened_owner = f"opened-{cycle}"
        intervals = ((root,), order[1:])
        physical_geometry = CORE.CycleGeometry(
            geometries[cycle].label, 5, cycle_vertices,
            tuple((physical_vertex(left), physical_vertex(right))
                  for left, right in geometries[cycle].edges),
        )
        CORE.verify_c5_router_owner_split(
            physical_geometry, intervals, (retained_owner, opened_owner), (1, 4)
        )
        opening_splits.append((cycle, intervals, (retained_owner, opened_owner)))
        opening_vertex_owners.update({root: retained_owner})
        opening_vertex_owners.update({vertex: opened_owner for vertex in order[1:]})
    owners = {}
    for cycle, geometry in enumerate(geometries):
        for vertex in geometry.vertices:
            physical = physical_vertex(vertex)
            if cycle in routers:
                owner = router_vertex_owners[physical]
            elif cycle in opened:
                owner = opening_vertex_owners[physical]
            else:
                owner = packet_cycle_owner[cycle]
            old = owners.setdefault(physical, owner)
            require(old == owner, f"{code}: shared physical cut has competing owners")
    for remnant, anchor in remnants:
        owners[remnant] = owners[anchor]
    attachments, attachment_anchors = expected_attachment_specification(vertices, remnants)
    certificate = RepairCertificate(
        code, signature, operation, routers, opened, nesting,
        tuple(router_splits), tuple(opening_splits),
        tuple(tuple(physical_vertex(vertex) for vertex in geometry.vertices)
              for geometry in geometries), vertices, edges, remnants,
        tuple(owners.items()),
        tuple((site, owners[anchor]) for site, anchor in attachment_anchors),
        (), ledger,
    )
    edge_keys = tuple(CORE.undirected_edge(edge) for edge in edges)
    owned = {
        owner: frozenset(vertex for vertex, assigned in owners.items()
                         if assigned == owner)
        for owner in dict.fromkeys(owners.values())
    }
    complete = complete_repair_cycles(certificate, owners)
    packet_owners = tuple(owner for owner, _, _ in packet_specs)
    packets = derive_physical_repair_packets(
        tree, certificate, owners, edge_keys, owned, complete, packet_owners
    )
    certificate = replace(certificate, packets=packets)
    verify_repair_certificate(tree, certificate)
    return certificate


def complete_repair_cycles(certificate, owner_map):
    complete = {owner: [] for owner in dict.fromkeys(owner_map.values())}
    for cycle, vertices in enumerate(certificate.geometry_vertices):
        cycle_owners = {owner_map[vertex] for vertex in vertices}
        if len(cycle_owners) == 1:
            complete[next(iter(cycle_owners))].append(cycle)
    return {owner: tuple(cycles) for owner, cycles in complete.items()}


def physical_common_vertex(cycles, geometry_vertices):
    common = set(geometry_vertices[cycles[0]])
    for cycle in cycles[1:]:
        common &= set(geometry_vertices[cycle])
    return min(common, key=repr) if common else None


def physical_pairwise_intersecting(cycles, geometry_vertices):
    return all(set(geometry_vertices[first]) & set(geometry_vertices[second])
               for index, first in enumerate(cycles)
               for second in cycles[index + 1:])


def derive_physical_repair_packet(tree, certificate, owner, cycles,
                                  edge_keys, domain):
    cycles = tuple(sorted(cycles))
    require(cycles, "repair terminal carrier is empty")
    require(domain, "repair terminal physical domain is empty")
    internal_edges = sum(edge <= domain for edge in edge_keys)
    cyclomatic = internal_edges - len(domain) + 1
    require(cyclomatic == len(cycles),
            "repair terminal physical graph has the wrong complete-cycle rank")
    triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
    pentagons = tuple(cycle for cycle in cycles if tree.colors[cycle] == "P")
    t, p = len(triangles), len(pentagons)
    if (t, p) == (9, 2):
        hub = physical_common_vertex(cycles, certificate.geometry_vertices)
        require(hub is not None, "T9PP repair packet lacks its common cut")
        theorem = "common-cut-T9PP"
        hypothesis = f"all eleven complete physical cycles share {hub!r}"
        bound = Bound(Fraction(10), 0, True)
    elif p == 1 and t >= 2:
        hub = physical_common_vertex(cycles, certificate.geometry_vertices)
        if hub is not None:
            theorem = f"common-cut-T{t}P"
            hypothesis = f"all complete physical cycles share {hub!r}"
            bound = Bound(Fraction(t), 1, True)
        elif physical_pairwise_intersecting(triangles,
                                            certificate.geometry_vertices):
            theorem = f"packing-one-T{t}P"
            hypothesis = "every pair of complete physical triangles intersects"
            bound = Bound(Fraction(t), 1, True)
        else:
            require(t + p == 9,
                    "one-hostile physical packet has no applicable theorem")
            theorem = "connected-rank9-T8P"
            hypothesis = ("owner-induced physical cactus is connected with "
                          "cyclomatic rank 9 and profile T8P")
            bound = Bound(0, 0, True)
    elif (t, p) == (1, 1):
        theorem, hypothesis = "TP-quantitative", "complete connected TP cactus"
        bound = Bound(Fraction(3, 4), 0, True)
    elif (t, p) == (0, 1):
        theorem, hypothesis = "P", "one complete pentagon"
        bound = Bound(0, 1, False)
    elif p == 0 and t == 1:
        theorem, hypothesis = "T", "one complete triangle"
        bound = Bound(0, 0, True)
    elif p == 0 and t in (5, 6, 8):
        hub = physical_common_vertex(triangles, certificate.geometry_vertices)
        require(hub is not None, "triangular repair cluster lacks its common cut")
        theorem = f"common-cut-A{t}"
        hypothesis = f"all complete physical triangles share {hub!r}"
        bound = Bound(Fraction(TRIANGLE_MARGIN[t]), 0, True)
    else:
        raise UnprovedPacket(f"unproved repair packet T^{t}P^{p}")
    return RepairPacket(owner, cycles, theorem, hypothesis, bound)


def derive_physical_repair_packets(tree, certificate, owner_map, edge_keys,
                                   owned, complete, packet_owners):
    return tuple(
        derive_physical_repair_packet(
            tree, certificate, owner, complete[owner], edge_keys, owned[owner]
        )
        for owner in packet_owners
    )


def derive_repair_ledger(certificate, packets):
    credit = sum((packet.bound.credit for packet in packets),
                 Fraction(-len(certificate.opened)))
    deficits = sum(packet.bound.deficits for packet in packets)
    sqrt13_charge = Fraction(0)
    strict = any(packet.bound.strict for packet in packets)
    for packet in packets:
        theorem = packet.theorem
        if theorem == "common-cut-T9PP":
            sqrt13_charge += Fraction(4, 3)
        elif not (theorem.startswith("common-cut-T") or
                  theorem.startswith("packing-one-T") or theorem == "P" or
                  theorem == "TP-quantitative" or
                  theorem.startswith("common-cut-A") or theorem in
                  ("T", "connected-rank9-T8P")):
            raise UnprovedPacket(f"repair ledger has unknown theorem {theorem}")
    return RadicalLedger(credit, deficits, sqrt13_charge, strict)


def physical_interval_children(domain, edge_keys, geometry_vertices, intervals):
    """Split one current physical domain only along its router boundaries."""
    domain = set(domain)
    interval_of = {
        vertex: index for index, interval in enumerate(intervals)
        for vertex in interval
    }
    require(set(geometry_vertices) == set(interval_of),
            "nested replay intervals do not exhaust the current router")
    router_edges = {
        frozenset((geometry_vertices[index],
                   geometry_vertices[(index + 1) % len(geometry_vertices)]))
        for index in range(len(geometry_vertices))
    }
    boundaries = set()
    for edge in router_edges:
        left, right = tuple(edge)
        if interval_of[left] != interval_of[right]:
            boundaries.add(edge)
    adjacency = {vertex: set() for vertex in domain}
    for edge in edge_keys:
        if edge <= domain and edge not in boundaries:
            left, right = tuple(edge)
            adjacency[left].add(right)
            adjacency[right].add(left)
    components = []
    covered = set()
    for interval in intervals:
        start = interval[0]
        require(start in domain, "nested replay interval leaves its parent domain")
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(set(interval) <= seen,
                "nested replay interval is disconnected inside its child")
        require(not covered & seen,
                "nested replay retrieves a previously closed sibling")
        covered |= seen
        components.append(frozenset(seen))
    require(covered == domain,
            "nested replay children do not exhaust their physical parent")
    return tuple(components)


def verify_nested_refinement(certificate, edge_keys, owned, owner_map):
    if len(certificate.nesting) <= 1:
        return
    require(certificate.nesting == tuple(router for router, _, _
                                         in certificate.router_splits),
            "nested refinement order differs from physical split order")
    current = frozenset(certificate.vertices)
    closed = {}
    active_parents = []
    for step_index, (router, intervals, child_names) in enumerate(
            certificate.router_splits):
        require(set(certificate.geometry_vertices[router]) <= current,
                "nested router is not wholly inside the active parent")
        children = physical_interval_children(
            current, edge_keys, certificate.geometry_vertices[router], intervals
        )
        if step_index + 1 < len(certificate.router_splits):
            next_router = certificate.router_splits[step_index + 1][0]
            next_vertices = set(certificate.geometry_vertices[next_router])
            active_indices = tuple(index for index, child in enumerate(children)
                                   if next_vertices <= child)
            require(len(active_indices) == 1,
                    "next nested router is not wholly inside exactly one child")
            active_index = active_indices[0]
            require(child_names[active_index] == "active",
                    "physical active child disagrees with submitted refinement")
            for index, (name, child) in enumerate(zip(child_names, children)):
                if index != active_index:
                    require(name in owned and child == owned[name],
                            "closed first-stage sibling differs from final owner domain")
                    require(all(owner_map[vertex] == name for vertex in intervals[index]),
                            "closed interval vertices disagree with their declared owner")
                    closed[name] = child
            active_parents.append(children[active_index])
            current = children[active_index]
            require(not any(current & domain for domain in closed.values()),
                    "active refinement retrieves a closed sibling")
        else:
            require("active" not in child_names,
                    "last nested split leaves an unresolved active child")
            for name, child in zip(child_names, children):
                require(name in owned and child == owned[name],
                        "final nested descendant differs from final owner map")
                interval = intervals[child_names.index(name)]
                require(all(owner_map[vertex] == name for vertex in interval),
                        "final nested interval vertices disagree with their descendant")
                closed[name] = child
    require(set(closed) == set(owned),
            "sequential refinement descendants do not equal final owners")
    require(set().union(*(set(domain) for domain in closed.values())) ==
            set(certificate.vertices),
            "sequential refinement descendants do not exhaust the graph")
    for parent in active_parents:
        descendants = tuple(domain for domain in closed.values() if domain <= parent)
        require(descendants and set().union(*(set(domain) for domain in descendants)) ==
                set(parent),
                "first-stage active interval does not resolve exactly to later descendants")


def verify_repair_owner_bindings(certificate, edge_keys, owned, owner_map):
    """Bind every declared interval and its physical branch to final owners."""
    if len(certificate.nesting) > 1:
        verify_nested_refinement(certificate, edge_keys, owned, owner_map)
    else:
        for router, intervals, owner_names in certificate.router_splits:
            children = physical_interval_children(
                certificate.vertices, edge_keys,
                certificate.geometry_vertices[router], intervals
            )
            for interval, name, child in zip(intervals, owner_names, children):
                require(name in owned and child == owned[name],
                        "router interval branch differs from its declared final owner")
                require(all(owner_map[vertex] == name for vertex in interval),
                        "router interval vertex differs from its declared final owner")
    for cycle, intervals, owner_names in certificate.opening_splits:
        children = physical_interval_children(
            certificate.vertices, edge_keys,
            certificate.geometry_vertices[cycle], intervals
        )
        for interval, name, child in zip(intervals, owner_names, children):
            require(name in owned and child == owned[name],
                    "opening branch differs from its declared final owner")
            require(all(owner_map[vertex] == name for vertex in interval),
                    "opening interval vertex differs from its declared final owner")


def verify_repair_certificate(tree, certificate):
    code = certificate.code
    require(certificate.signature == REPAIR_SIGNATURES[int(code[1:]) - 1],
            f"{code}: submitted residual signature changed")
    operation, routers, opened, nesting, split_specs, packet_specs, _ = repair_spec(code)
    require((certificate.operation, certificate.routers, certificate.opened,
             certificate.nesting) == (operation, routers, opened, nesting),
            f"{code}: repair operation ledger changed")
    adjacency = local_adjacency(tree)
    require(local_signature(tree, adjacency) == certificate.signature,
            f"{code}: repair is attached to the wrong incidence graph")
    geometries = incidence_geometry(certificate.signature, tree, adjacency)
    expected_vertices, expected_edges, expected_remnants = repair_graph(geometries, routers)
    expected_attachments, attachment_anchors = expected_attachment_specification(
        expected_vertices, expected_remnants
    )
    require(certificate.geometry_vertices == tuple(
                tuple(physical_vertex(vertex) for vertex in geometry.vertices)
                for geometry in geometries),
            f"{code}: physical cycle geometry changed")
    require(certificate.remnant_anchors == expected_remnants,
            f"{code}: connector-remnant domain changed")
    require(tuple(router for router, _, _ in certificate.router_splits) == routers,
            f"{code}: router split order changed")
    for submitted, expected in zip(certificate.router_splits, split_specs):
        router, groups, owner_names = expected
        intervals = intervals_for_ports(geometries[router], groups)
        require(submitted == (router, intervals, owner_names),
                f"{code}: concrete router intervals changed")
        physical_geometry = CORE.CycleGeometry(
            geometries[router].label, geometries[router].length,
            tuple(physical_vertex(vertex) for vertex in geometries[router].vertices),
            tuple((physical_vertex(left), physical_vertex(right))
                  for left, right in geometries[router].edges),
        )
        if physical_geometry.length == 5:
            CORE.verify_c5_router_owner_split(
                physical_geometry, intervals, owner_names
            )
        else:
            CORE.verify_router_owner_split(physical_geometry, intervals, owner_names)
    require(tuple(cycle for cycle, _, _ in certificate.opening_splits) == opened,
            f"{code}: physical opening domain changed")
    for cycle, intervals, owner_names in certificate.opening_splits:
        require(len(adjacency[cycle]) == 1 and tuple(map(len, intervals)) == (1, 4),
                f"{code}: opening is not the exact rooted C5 singleton/four-path")
        root = CORE.CutSite(adjacency[cycle][0])
        require(intervals[0] == (root,),
                f"{code}: opening singleton is not the incidence vertex")
        retained_owner = next(packet.owner for packet in certificate.packets
                              if cycle not in packet.cycles and
                              root in certificate.geometry_vertices[next(
                                  retained for retained in packet.cycles
                                  if root in certificate.geometry_vertices[retained]
                              )])
        require(owner_names == (retained_owner, f"opened-{cycle}"),
                f"{code}: opening owners do not bind root and four-path")
        physical_geometry = CORE.CycleGeometry(
            geometries[cycle].label, 5,
            tuple(physical_vertex(vertex) for vertex in geometries[cycle].vertices),
            tuple((physical_vertex(left), physical_vertex(right))
                  for left, right in geometries[cycle].edges),
        )
        CORE.verify_c5_router_owner_split(
            physical_geometry, intervals, owner_names, (1, 4)
        )
    final_owners = tuple(dict.fromkeys(owner for _, owner in certificate.vertex_owners))
    owner_map, edge_keys, owned = CORE.verify_physical_owner_certificate(
        expected_vertices, expected_edges, expected_attachments,
        certificate.vertices, certificate.edges, certificate.vertex_owners,
        certificate.attachment_owners, final_owners, attachment_anchors,
    )
    verify_repair_owner_bindings(certificate, edge_keys, owned, owner_map)
    complete = complete_repair_cycles(certificate, owner_map)
    packet_owners = tuple(owner for owner, _, _ in packet_specs)
    expected_packet_cycles = tuple((owner, tuple(sorted(cycles)))
                                   for owner, cycles, _ in packet_specs)
    require(tuple((packet.owner, packet.cycles) for packet in certificate.packets) ==
            expected_packet_cycles,
            f"{code}: packet owner identities differ from the repair specification")
    require(set(complete) - set(packet_owners) ==
            {f"opened-{cycle}" for cycle in opened},
            f"{code}: unexpected physical terminal owner")
    require(all(not complete[f"opened-{cycle}"] for cycle in opened),
            f"{code}: opened tree retains a complete cycle")
    derived_packets = tuple(
        derive_physical_repair_packet(
            tree, certificate, owner, complete[owner], edge_keys, owned[owner]
        ) for owner in packet_owners
    )
    require(certificate.packets == derived_packets,
            f"{code}: full packet was not rederived from the physical owner graph")
    derived_ledger = derive_repair_ledger(certificate, derived_packets)
    require(certificate.ledger == derived_ledger,
            f"{code}: radical ledger is not the exact theorem/opening sum")
    require(derived_ledger.positive(), f"{code}: exact radical ledger is not positive")


def expect_rejected(action, label):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def coordinated_owner_domain_swap(tree, certificate, first, second):
    """Relabel two complete owner domains and rebuild packet/ledger claims."""
    def swapped(owner):
        if owner == first:
            return second
        if owner == second:
            return first
        return owner

    vertex_owners = tuple((vertex, swapped(owner))
                          for vertex, owner in certificate.vertex_owners)
    attachment_owners = tuple((site, swapped(owner))
                              for site, owner in certificate.attachment_owners)
    owner_map = dict(vertex_owners)
    edge_keys = tuple(CORE.undirected_edge(edge) for edge in certificate.edges)
    owned = {
        owner: frozenset(vertex for vertex, assigned in owner_map.items()
                         if assigned == owner)
        for owner in dict.fromkeys(owner_map.values())
    }
    mutated = replace(certificate, vertex_owners=vertex_owners,
                      attachment_owners=attachment_owners, packets=())
    complete = complete_repair_cycles(mutated, owner_map)
    packet_owners = tuple(packet.owner for packet in certificate.packets)
    packets = derive_physical_repair_packets(
        tree, mutated, owner_map, edge_keys, owned, complete, packet_owners
    )
    mutated = replace(mutated, packets=packets)
    return replace(mutated, ledger=derive_repair_ledger(mutated, packets))


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


def repair_mutation_self_tests(repairs):
    tests = 0
    tree7, repair7 = repairs["U7"]
    literal_packets = (
        RepairPacket("P-left", (9,), "P", "P", Bound(0, 0, True)),
        RepairPacket("P-right", (10,), "P", "P", Bound(0, 0, True)),
        RepairPacket("A7", tuple(range(2, 9)), "common-cut-A7", "A7", Bound(0, 0, True)),
    )
    expect_rejected(lambda: verify_repair_certificate(
        tree7, replace(repair7, operation="literal-N7-P+P+A7",
                       packets=literal_packets,
                       ledger=RadicalLedger(Fraction(0), 2, 0, True))),
        "invalid literal U7 extension",
    )
    tests += 1
    tree3, repair3 = repairs["U3"]
    router, intervals, owners = repair3.router_splits[0]
    expect_rejected(lambda: verify_repair_certificate(
        tree3, replace(repair3,
                       router_splits=((router, intervals, tuple(reversed(owners))),))),
        "U3 swapped interval owners",
    )
    tests += 1
    tree4, repair4 = repairs["U4"]
    forged4 = replace(repair4.packets[1], theorem="forged-TP")
    expect_rejected(lambda: verify_repair_certificate(
        tree4, replace(repair4, packets=(repair4.packets[0], forged4))),
        "U4 forged TP theorem",
    )
    tests += 1
    forged_hypothesis = replace(
        repair4.packets[0], hypothesis="all triangles share a forged vertex"
    )
    expect_rejected(lambda: verify_repair_certificate(
        tree4, replace(repair4,
                       packets=(forged_hypothesis,) + repair4.packets[1:])),
        "U4 forged physical hypothesis",
    )
    tests += 1
    expect_rejected(lambda: verify_repair_certificate(
        tree4, coordinated_owner_domain_swap(tree4, repair4, "A8", "TP")),
        "U4 coordinated owner-domain swap",
    )
    tests += 1
    tree5, repair5 = repairs["U5"]
    cycle, intervals, owners = repair5.opening_splits[0]
    expect_rejected(lambda: verify_repair_certificate(
        tree5, replace(repair5,
                       opening_splits=((cycle, intervals, tuple(reversed(owners))),))),
        "U5 swapped opening owners",
    )
    tests += 1
    tree6, repair6 = repairs["U6"]
    router, intervals, owners = repair6.router_splits[0]
    expect_rejected(lambda: verify_repair_certificate(
        tree6, replace(repair6,
                       router_splits=((router, intervals[:-1], owners[:-1]),))),
        "U6 omitted forced singleton",
    )
    tests += 1
    tree8, repair8 = repairs["U8"]
    router, intervals, owners = repair8.router_splits[0]
    wrong_intervals = (intervals[1][:1], intervals[0] + intervals[1][1:])
    expect_rejected(lambda: verify_repair_certificate(
        tree8, replace(repair8,
                       router_splits=((router, wrong_intervals, owners),))),
        "wrong C5 singleton",
    )
    tests += 1
    forged_bound = replace(repair8.packets[1],
                           bound=Bound(Fraction(1), 0, True))
    expect_rejected(lambda: verify_repair_certificate(
        tree8, replace(repair8,
                       packets=(repair8.packets[0], forged_bound))),
        "U8 forged physical packet bound",
    )
    tests += 1
    expect_rejected(lambda: verify_repair_certificate(
        tree8, coordinated_owner_domain_swap(tree8, repair8, "T", "rank9")),
        "U8 coordinated owner-domain swap",
    )
    tests += 1
    tree9, repair9 = repairs["U9"]
    expect_rejected(lambda: verify_repair_certificate(
        tree9, replace(repair9, nesting=tuple(reversed(repair9.nesting)))),
        "reversed nested repair order",
    )
    tests += 1
    expect_rejected(lambda: verify_repair_certificate(
        tree7, coordinated_owner_domain_swap(tree7, repair7, "P", "retained")),
        "U7 coordinated owner-domain swap",
    )
    tests += 1
    owner_map9 = dict(repair9.vertex_owners)
    edge_keys9 = tuple(CORE.undirected_edge(edge) for edge in repair9.edges)
    owned9 = {
        owner: frozenset(vertex for vertex, assigned in owner_map9.items()
                         if assigned == owner)
        for owner in dict.fromkeys(owner_map9.values())
    }
    owned9["A6"] = owned9["A6"] | owned9["T"]
    expect_rejected(lambda: verify_nested_refinement(
        repair9, edge_keys9, owned9, owner_map9),
                    "U9 closed sibling retrieval")
    tests += 1
    tree2, repair2 = repairs["U2"]
    cycle, intervals, owners = repair2.opening_splits[0]
    expect_rejected(lambda: verify_repair_certificate(
        tree2, replace(repair2,
                       opening_splits=((cycle, tuple(reversed(intervals)), owners),))),
        "reversed physical opening",
    )
    tests += 1
    tree1, repair1 = repairs["U1"]
    expect_rejected(lambda: verify_repair_certificate(
        tree1, replace(repair1,
                       ledger=RadicalLedger(Fraction(10), 0, Fraction(3, 2), True))),
        "forged common-cut radical charge",
    )
    tests += 1
    tree10, repair10 = repairs["U10"]
    forged10 = replace(repair10.packets[-1], theorem="common-cut-A6")
    expect_rejected(lambda: verify_repair_certificate(
        tree10, replace(repair10,
                        packets=repair10.packets[:-1] + (forged10,))),
        "U10 forged nested cluster rank",
    )
    tests += 1
    owner_map10 = dict(repair10.vertex_owners)
    edge_keys10 = tuple(CORE.undirected_edge(edge) for edge in repair10.edges)
    owned10 = {
        owner: frozenset(vertex for vertex, assigned in owner_map10.items()
                         if assigned == owner)
        for owner in dict.fromkeys(owner_map10.values())
    }
    owned10["A5"] = owned10["A5"] | owned10["P1"]
    expect_rejected(lambda: verify_nested_refinement(
        repair10, edge_keys10, owned10, owner_map10),
        "U10 closed sibling retrieval")
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
    residual_by_signature = dict(residuals)
    require(set(residual_by_signature) == set(REPAIR_SIGNATURES),
            "repair signatures do not exactly exhaust the ordinary residual stream")
    repairs = {}
    repair_hasher = sha256()
    repair_theorems = Counter()
    for number, signature in enumerate(REPAIR_SIGNATURES, 1):
        code = f"U{number}"
        tree = residual_by_signature[signature]
        repair = make_repair_certificate(code, signature, tree)
        repairs[code] = (tree, repair)
        repair_theorems.update(packet.theorem for packet in repair.packets)
        repair_hasher.update(repr(repair).encode("ascii") + b"\n")
    repair_mutations = repair_mutation_self_tests(repairs)
    repair_digest = repair_hasher.hexdigest()
    degree4_digest = stream_digest(router_degree_signatures[4])
    degree5_digest = stream_digest(router_degree_signatures[5])

    print("fully shared T^9PP rows:", len(classes))
    print("ordinary physical-owner SAFE:", sum(safe_by_cut.values()))
    print("physical theorem certificates for abstract SAFE candidates:",
          physical_candidate_count)
    print("ordinary residual rows repaired physically:", len(repairs))
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
    print("repair-proof sha256:", repair_digest)
    print("repair theorem uses:", dict(sorted(repair_theorems.items())))
    print("rejected hostile mutations:", mutation_count + repair_mutations)
    for code, (_, repair) in repairs.items():
        print(f"{code} CLOSED: {repair.signature} operation={repair.operation} ledger={repair.ledger}")
    print(f"FULLY SHARED CLOSED: {len(classes)}/{len(classes)} = {sum(safe_by_cut.values())} ordinary + {len(repairs)} repairs")

    require(safe_by_cut == EXPECTED_SAFE_BY_CUT, "ordinary SAFE cut-count census changed")
    require(sum(safe_by_cut.values()) == 115502, "ordinary physical-owner SAFE total changed")
    require(len(residuals) == 10, "exact fail-closed residual count changed")
    require(len(repairs) == 10 and all(repair.ledger.positive()
                                      for _, repair in repairs.values()),
            "physical repair closure count changed")
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
    require(repair_mutations == 17, "repair hostile mutation count changed")
    require(repair_digest == EXPECTED_REPAIR_DIGEST,
            "physical repair-certificate digest changed")


if __name__ == "__main__":
    main()
