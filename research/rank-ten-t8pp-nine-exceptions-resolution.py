#!/usr/bin/env python3
"""Exact replacement audit for all nine fully shared rank-ten T^8PP rows."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations, product
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_ten_shared", HERE / "rank-ten-fully-shared-incidence-census.py"
)
CENSUS = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("rank-ten census dependency has no import loader")
sys.modules[SPEC.name] = CENSUS
SPEC.loader.exec_module(CENSUS)
BASE = CENSUS.BASE

EXPECTED_CLASS_DIGEST = "9aa6813cb87e1db0748faf441b8941145fbedb5af55386404bd9cfcbe10a6e3b"
EXPECTED_WITNESS_DIGEST = "1c54195dd78960ab03645f152ded55e0b35aaf898aefda9dbbd1237ea6822958"
EXPECTED_ALL_BY_CUT = Counter({1: 1, 2: 19, 3: 204, 4: 1155, 5: 3990, 6: 8135, 7: 9615, 8: 5843, 9: 1424})
EXPECTED_SAFE_BY_CUT = Counter({2: 17, 3: 200, 4: 1154, 5: 3989, 6: 8135, 7: 9615, 8: 5843, 9: 1424})


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Recipe:
    code: str
    signature: str
    routers: tuple[int, ...]
    opened: tuple[int, ...]
    packets: tuple[tuple[str, tuple[int, ...]], ...]
    credit: Fraction
    deficits: int
    steps: tuple["Step", ...] = ()


@dataclass(frozen=True)
class Step:
    router: int
    active: tuple[int, ...]
    intervals: tuple[tuple[tuple[int, ...], int, int], ...]


@dataclass(frozen=True)
class GraphCertificate:
    placement: tuple[tuple[int, tuple[tuple[int, int], ...]], ...]
    interval_owners: tuple[tuple[int, int, int], ...]
    cut_owners: tuple[tuple[int, int], ...]
    connectors: tuple[tuple[int, int, int], ...]
    attachments: tuple[tuple[tuple[object, ...], int], ...]


@dataclass(frozen=True)
class PacketHypothesis:
    value: Fraction
    strict: bool
    source: str


@dataclass(frozen=True)
class OrdinaryOwner:
    port: int
    interval: tuple[int, ...]
    cycles: tuple[int, ...]
    cuts: tuple[int, ...]
    hypothesis: PacketHypothesis


@dataclass(frozen=True)
class OrdinaryWitness:
    signature: str
    sacrificed: int
    owners: tuple[OrdinaryOwner, ...]
    cycle_owners: tuple[tuple[int, int], ...]
    cut_owners: tuple[tuple[int, int], ...]
    final_owners: tuple[tuple[tuple[object, ...], int], ...]
    ledger: Fraction
    strict: bool


def stream_digest(lines):
    return sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


def local_adjacency(tree):
    cycle_count = len(tree.colors)
    cut_count = len(tree.edges) + 1 - cycle_count
    require(cut_count >= 1, "canonical row has no cut")
    adjacency = [[] for _ in range(cycle_count + cut_count)]
    for edge in tree.edges:
        require(len(edge) == 2, "canonical row has a malformed edge")
        cycle, cut = edge
        require(0 <= cycle < cycle_count <= cut < len(adjacency),
                "canonical row has a non-incidence edge")
        adjacency[cycle].append(cut)
        adjacency[cut].append(cycle)
    return tuple(tuple(sorted(neighbors)) for neighbors in adjacency)


def local_signature(tree, adjacency):
    degrees = [len(neighbors) for neighbors in adjacency]
    leaves = [vertex for vertex, degree in enumerate(degrees) if degree <= 1]
    remaining = len(adjacency)
    while remaining > 2:
        require(leaves, "canonical center search stalled")
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            for neighbor in adjacency[leaf]:
                degrees[neighbor] -= 1
                if degrees[neighbor] == 1:
                    new_leaves.append(neighbor)
        leaves = new_leaves

    def rooted(vertex, parent):
        label = tree.colors[vertex] if vertex < len(tree.colors) else "X"
        children = sorted(rooted(child, vertex) for child in adjacency[vertex]
                          if child != parent)
        return label + "(" + "".join(children) + ")"

    require(leaves, "canonical row has no center")
    return min(rooted(center, -1) for center in leaves)


def validate_canonical_rows(classes):
    require(len(classes) == 30386, "canonical class total changed")
    signatures = tuple(signature for signature, _ in classes)
    require(signatures == tuple(sorted(signatures)), "canonical rows are not sorted")
    require(len(set(signatures)) == len(signatures), "canonical signatures repeat")
    counts = Counter()
    for stored_signature, tree in classes:
        require(Counter(tree.colors) == Counter(T=8, P=2),
                "canonical row has incorrect colors")
        require(len(set(tree.edges)) == len(tree.edges), "canonical row repeats an edge")
        adjacency = local_adjacency(tree)
        require(len(tree.edges) == len(adjacency) - 1,
                "canonical incidence representative is not a tree")
        require(all(len(adjacency[cut]) >= 2 for cut in range(10, len(adjacency))),
                "canonical row has a redundant cut leaf")
        require(all(1 <= len(adjacency[cycle]) <= (3 if color == "T" else 5)
                    for cycle, color in enumerate(tree.colors)),
                "canonical row violates cycle capacity")
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(len(seen) == len(adjacency), "canonical row is disconnected")
        require(stored_signature == local_signature(tree, adjacency),
                "stored signature is not independently canonical")
        counts[len(adjacency) - 10] += 1
    require(counts == EXPECTED_ALL_BY_CUT, "canonical cut-count stream changed")
    digest = stream_digest(signatures)
    require(digest == EXPECTED_CLASS_DIGEST, "canonical class digest changed")
    return digest


def split_components(tree, sacrificed, adjacency):
    components = []
    seen = {sacrificed}
    for port in adjacency[sacrificed]:
        require(port not in seen, "two sacrificed-cycle ports enter one component")
        stack = [port]
        seen.add(port)
        vertices = set()
        cycles = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            if vertex < 10:
                cycles.add(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components.append((port, tuple(sorted(cycles)), tuple(sorted(
            vertex for vertex in vertices if vertex >= 10
        ))))
    return tuple(components)


def packet_hypothesis(tree, cycles, cuts, adjacency):
    triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
    triangles = len(triangle_set)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    margins = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0}
    internal_cuts = tuple(cut for cut in cuts
                          if sum(cycle in cycles for cycle in adjacency[cut]) >= 2)
    if pentagons == 0:
        require(triangles in margins, "all-triangle packet has unsupported rank")
        return PacketHypothesis(Fraction(margins[triangles]), True, f"A_{triangles}")
    if rank == 1:
        require((triangles, pentagons) == (0, 1), "singleton packet is not P")
        return PacketHypothesis(Fraction(-1, 4), True, "P>-1/4")
    if (triangles, pentagons) == (1, 1):
        return PacketHypothesis(Fraction(3, 4), True, "TP>3/4")
    if (triangles, pentagons) == (0, 2):
        return PacketHypothesis(Fraction(0), True, "PP>0")
    if (triangles, pentagons) == (2, 1) and any(
            triangle_set <= set(adjacency[cut]) for cut in internal_cuts):
        return PacketHypothesis(Fraction(7, 4), True, "common-cut-TTP>7/4")
    if (triangles, pentagons) == (1, 2):
        return PacketHypothesis(Fraction(3, 2), True, "TPP>3/2")
    if rank == 3:
        return PacketHypothesis(Fraction(0), False, "generic-rank-3>=0")
    if (triangles, pentagons) == (3, 1) and any(
            len(triangle_set & set(adjacency[cut])) >= 2 for cut in internal_cuts):
        return PacketHypothesis(Fraction(1), True, "shared-pair-TTTP>1")
    require(4 <= rank <= 8, f"unrecognized retained packet rank {rank}")
    return PacketHypothesis(Fraction(0), True, f"generic-rank-{rank}>0")


def ordinary_witness(signature, tree, sacrificed):
    adjacency = local_adjacency(tree)
    components = split_components(tree, sacrificed, adjacency)
    if len(components) < 2:
        return None
    cycle_length = 3 if tree.colors[sacrificed] == "T" else 5
    require(len(components) <= cycle_length, "split has too many occupied ports")
    sizes = (1,) * (len(components) - 1) + (cycle_length - len(components) + 1,)
    require(all(0 < size < cycle_length for size in sizes),
            "split does not use proper nonempty intervals")
    owners = []
    cycle_owners = {}
    cut_owners = {}
    final_owners = {}
    cursor = 0
    for owner, ((port, cycles, cuts), size) in enumerate(zip(components, sizes)):
        hypothesis = packet_hypothesis(tree, cycles, cuts, adjacency)
        interval = tuple(range(cursor, cursor + size))
        cursor += size
        owners.append(OrdinaryOwner(port, interval, cycles, cuts, hypothesis))
        for cycle in cycles:
            require(cycle not in cycle_owners, "retained cycle has two owners")
            cycle_owners[cycle] = owner
            for slot in range(3 if tree.colors[cycle] == "T" else 5):
                final_owners[("cycle", cycle, slot)] = owner
        for cut in cuts:
            require(cut not in cut_owners, "cut has two final owners")
            cut_owners[cut] = owner
            final_owners[("cut", cut)] = owner
        for slot in interval:
            final_owners[("cycle", sacrificed, slot)] = owner
    require(cursor == cycle_length, "split intervals do not exhaust sacrificed cycle")
    require(set(cycle_owners) == set(range(10)) - {sacrificed},
            "split does not own every retained cycle")
    require(set(cut_owners) == set(range(10, len(adjacency))),
            "split does not own every cut")
    expected_sites = len(adjacency) - 10 + sum(3 if color == "T" else 5
                                               for color in tree.colors)
    require(len(final_owners) == expected_sites, "split final ownership is not exhaustive")
    for owner, item in enumerate(owners):
        require(final_owners[("cycle", sacrificed, item.interval[0])] == owner,
                "split port interval has wrong owner")
        require(cut_owners[item.port] == owner, "split port cut has wrong owner")
        for cycle in item.cycles:
            for cut in adjacency[cycle]:
                require(cut_owners[cut] == owner, "retained connector crosses owners")
    ledger = sum((item.hypothesis.value for item in owners), Fraction(0))
    strict = any(item.hypothesis.strict for item in owners)
    if not (ledger > 0 or (ledger == 0 and strict)):
        return None
    return OrdinaryWitness(
        signature, sacrificed, tuple(owners), tuple(sorted(cycle_owners.items())),
        tuple(sorted(cut_owners.items())), tuple(sorted(final_owners.items())),
        ledger, strict,
    )


def witness_line(witness):
    owners = ";".join(
        f"{item.port}:{','.join(map(str, item.interval))}:"
        f"{','.join(map(str, item.cycles))}:{','.join(map(str, item.cuts))}:"
        f"{item.hypothesis.value.numerator}/{item.hypothesis.value.denominator}:"
        f"{int(item.hypothesis.strict)}:{item.hypothesis.source}"
        for item in witness.owners
    )
    cycle_owners = ",".join(f"{cycle}:{owner}"
                            for cycle, owner in witness.cycle_owners)
    cut_owners = ",".join(f"{cut}:{owner}" for cut, owner in witness.cut_owners)
    final_owners = ",".join(
        f"{':'.join(map(str, site))}:{owner}"
        for site, owner in witness.final_owners
    )
    return (f"{witness.signature}|s={witness.sacrificed}|{owners}|"
            f"cycles={cycle_owners}|cuts={cut_owners}|final={final_owners}|"
            f"ledger={witness.ledger.numerator}/{witness.ledger.denominator}|"
            f"strict={int(witness.strict)}")


def validate_ordinary_stream(classes):
    witnesses = []
    residuals = []
    safe_by_cut = Counter()
    for signature, tree in classes:
        candidates = tuple(filter(None, (
            ordinary_witness(signature, tree, cycle) for cycle in range(10)
        )))
        if candidates:
            witness = candidates[0]
            witnesses.append(witness)
            safe_by_cut[len(local_adjacency(tree)) - 10] += 1
        else:
            residuals.append((signature, tree))
    require(len(witnesses) == 30377, "ordinary-safe witness total changed")
    require(len(residuals) == 9, "ordinary residual total changed")
    require(safe_by_cut == EXPECTED_SAFE_BY_CUT, "ordinary-safe cut counts changed")
    digest = stream_digest(witness_line(witness) for witness in witnesses)
    require(digest == EXPECTED_WITNESS_DIGEST, "ordinary witness digest changed")
    return tuple(witnesses), tuple(residuals), digest


RECIPES = (
    Recipe("N1", "X(P()P()T()T()T()T()T()T()T()T())", (), (), (("common_tpp", tuple(range(10))),), 1, 0),
    Recipe("N2", "P(X(P())X(T()T()T()T()T()T()T()T()))", (), (9,), (("common_tp", tuple(range(9))),), 7, 1),
    Recipe("N3", "T(X(P())X(P()T()T()T()T()T()T()T()))", (0,), (), (("P", (8,)), ("common_tp", tuple(range(1, 8)) + (9,))), 7, 2, (Step(0, tuple(range(10)), (((10,), 2, 1), ((11,), 1, 0))),)),
    Recipe("N4", "P(X(P())X(T())X(T()T()T()T()T()T()T()))", (0,), (), (("A", (1,) + tuple(range(3, 9))), ("TP", (2, 9))), Fraction(3, 4), 0, (Step(0, tuple(range(10)), (((10,), 1, 0), ((11, 12), 4, 1))),)),
    Recipe("N5", "T(X(P())X(P())X(T()T()T()T()T()T()T()))", (), (8,), (("packing_one_tp", tuple(range(8)) + (9,)),), 7, 1),
    Recipe("N6", "T(X(P())X(P()T()T()T()T()T()T())X(T()))", (0,), (), (("P", (8,)), ("A", (2,)), ("common_tp", (1,) + tuple(range(3, 8)) + (9,))), 6, 2, (Step(0, tuple(range(10)), (((10,), 1, 2), ((11,), 1, 1), ((12,), 1, 0))),)),
    Recipe("N7", "X(T()T()T()T()T()T()T(X(P()))T(X(P())))", (0, 1), (), (("P", (8,)), ("P", (9,)), ("A", tuple(range(2, 8)))), 1, 2, (Step(0, tuple(range(10)), (((10,), 2, 2), ((11,), 1, 0))), Step(1, (1, 2, 3, 4, 5, 6, 7, 9), (((10,), 2, 2), ((12,), 1, 1))))),
    Recipe("N8", "X(T()T()T()T()T()T(X(P()))T(X(P())X(T())))", (0, 1), (), (("P", (8,)), ("P", (9,)), ("A", (2,)), ("A", tuple(range(3, 8)))), 2, 2, (Step(0, tuple(range(10)), (((10,), 1, 3), ((11,), 1, 2), ((12,), 1, 0))), Step(1, (1, 3, 4, 5, 6, 7, 9), (((10,), 2, 3), ((13,), 1, 1))))),
    Recipe("N9", "X(T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))", (0, 1), (), (("P", (8,)), ("P", (9,)), ("A", (2,)), ("A", (7,)), ("A", tuple(range(3, 7)))), 3, 2, (Step(0, tuple(range(10)), (((10,), 1, 4), ((11,), 1, 2), ((13,), 1, 0))), Step(1, (1, 3, 4, 5, 6, 7, 9), (((10,), 1, 4), ((12,), 1, 3), ((14,), 1, 1))))),
)


def connected(tree, cycles):
    if len(cycles) <= 1:
        return True
    adj = local_adjacency(tree)
    allowed = set(cycles)
    seen = {cycles[0]}
    todo = [cycles[0]]
    while todo:
        cycle = todo.pop()
        for cut in adj[cycle]:
            for neighbor in adj[cut]:
                if neighbor in allowed and neighbor not in seen:
                    seen.add(neighbor)
                    todo.append(neighbor)
    return seen == allowed


def shared_cut(tree, cycles):
    adj = local_adjacency(tree)
    return any(all(cut in adj[cycle] for cycle in cycles) for cut in adj[cycles[0]])


def positive(credit, deficits):
    rational = credit + 2 * deficits
    return rational > 0 and rational * rational > 5 * deficits * deficits


def common_tpp_positive(tree, cycles):
    colors = Counter(tree.colors[cycle] for cycle in cycles)
    require(colors == Counter(T=8, P=2), "common-cut TPP positivity received the wrong packet")
    rational = colors["T"] + 1
    return rational > 0 and (3 * rational) ** 2 * 13 > 4**2


def components_after_router_deletion(tree, routers, opened):
    adj = local_adjacency(tree)
    blocked = set(routers) | set(opened)
    seen = set(blocked)
    components = []
    for start in range(len(adj)):
        if start in seen:
            continue
        todo = [start]
        seen.add(start)
        cycles = set()
        while todo:
            vertex = todo.pop()
            if vertex < 10:
                cycles.add(vertex)
            for neighbor in adj[vertex]:
                if neighbor not in seen and neighbor not in blocked:
                    seen.add(neighbor)
                    todo.append(neighbor)
        if cycles:
            components.append(frozenset(cycles))
    return Counter(components)


def branch_cycles(tree, active, removed, ports):
    adj = local_adjacency(tree)
    allowed = set(active) - set(removed)
    seen = set(ports)
    todo = list(ports)
    cycles = set()
    while todo:
        vertex = todo.pop()
        for neighbor in adj[vertex]:
            if neighbor < 10 and neighbor not in allowed:
                continue
            if neighbor not in seen:
                seen.add(neighbor)
                todo.append(neighbor)
                if neighbor < 10:
                    cycles.add(neighbor)
    return frozenset(cycles)


def step_placements(tree, step):
    marks = local_adjacency(tree)[step.router]
    size = 3 if tree.colors[step.router] == "T" else 5
    return tuple(
        tuple(zip(marks, slots))
        for slots in permutations(range(size), len(marks))
    )


def interval_slot_owners(recipe, step, placement):
    mark_slot = dict(placement)
    size = sum(interval_size for _, interval_size, _ in step.intervals)
    owners = {}
    if recipe.code == "N4":
        singleton_ports, singleton_size, singleton_owner = step.intervals[0]
        require(singleton_size == 1 and len(singleton_ports) == 1, "N4 singleton interval is malformed")
        singleton_slot = mark_slot[singleton_ports[0]]
        owners[singleton_slot] = singleton_owner
        for slot in range(size):
            if slot != singleton_slot:
                owners[slot] = step.intervals[1][2]
    elif len(step.intervals) == 2:
        small = next(item for item in step.intervals if item[1] == 1)
        large = next(item for item in step.intervals if item[1] == 2)
        owners[mark_slot[small[0][0]]] = small[2]
        for slot in range(size):
            if slot not in owners:
                owners[slot] = large[2]
    else:
        for ports, interval_size, owner in step.intervals:
            require(interval_size == 1 and len(ports) == 1, f"{recipe.code} non-singleton three-way interval")
            owners[mark_slot[ports[0]]] = owner
    require(set(owners) == set(range(size)), f"{recipe.code} router intervals do not cover its cycle")
    return owners


def materialize_graph_certificates(tree, recipe):
    adj = local_adjacency(tree)
    packet_of = {
        cycle: index
        for index, (_, cycles) in enumerate(recipe.packets)
        for cycle in cycles
    }
    opened_owner = {
        cycle: len(recipe.packets) + index
        for index, cycle in enumerate(recipe.opened)
    }
    cut_owner = {}
    for cut in range(10, len(adj)):
        owners = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        require(len(owners) == 1, f"{recipe.code} cut {cut} does not have exactly one retained owner")
        cut_owner[cut] = next(iter(owners))

    choices = tuple(step_placements(tree, step) for step in recipe.steps)
    combinations = product(*choices) if choices else ((),)
    certificates = []
    for combination in combinations:
        vertex_owner = {("cut", cut): owner for cut, owner in cut_owner.items()}
        interval_owners = []
        mark_slots = {}
        for step, placement in zip(recipe.steps, combination):
            slots = interval_slot_owners(recipe, step, placement)
            mark_slots[step.router] = dict(placement)
            for slot, owner in sorted(slots.items()):
                vertex_owner[("cycle", step.router, slot)] = owner
                interval_owners.append((step.router, slot, owner))

        for cycle, color in enumerate(tree.colors):
            if cycle in recipe.routers:
                continue
            size = 3 if color == "T" else 5
            if cycle in opened_owner:
                incident = adj[cycle][0]
                incident_slot = 0
                vertex_owner[("cycle", cycle, incident_slot)] = cut_owner[incident]
                for slot in range(1, size):
                    vertex_owner[("cycle", cycle, slot)] = opened_owner[cycle]
            else:
                owner = packet_of[cycle]
                for slot in range(size):
                    vertex_owner[("cycle", cycle, slot)] = owner

        connectors = []
        for cycle in range(10):
            for offset, cut in enumerate(adj[cycle]):
                slot = mark_slots.get(cycle, {}).get(cut, offset)
                cycle_owner = vertex_owner[("cycle", cycle, slot)]
                require(cycle_owner == cut_owner[cut], f"{recipe.code} connector {cycle}-{cut} crosses owners")
                connectors.append((cycle, cut, cycle_owner))

        attachments = tuple(sorted((site, owner) for site, owner in vertex_owner.items()))
        expected_vertices = (len(adj) - 10) + sum(3 if color == "T" else 5 for color in tree.colors)
        require(len(attachments) == expected_vertices, f"{recipe.code} attachment sites are not exhaustive")
        require(len(dict(attachments)) == len(attachments), f"{recipe.code} attachment site has multiple owners")
        certificates.append(GraphCertificate(
            tuple((step.router, placement) for step, placement in zip(recipe.steps, combination)),
            tuple(interval_owners), tuple(sorted(cut_owner.items())),
            tuple(connectors), attachments,
        ))
    expected = 1
    for step in recipe.steps:
        marks = len(adj[step.router])
        size = 3 if tree.colors[step.router] == "T" else 5
        factor = 1
        for value in range(size - marks + 1, size + 1):
            factor *= value
        expected *= factor
    require(len(certificates) == expected, f"{recipe.code} cyclic-placement census changed")
    return tuple(certificates)


def packet_ledger(tree, recipe):
    margins = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0}
    credit = -len(recipe.opened)
    deficits = 0
    for kind, cycles in recipe.packets:
        colors = Counter(tree.colors[cycle] for cycle in cycles)
        triangles = colors["T"]
        if kind == "P":
            deficits += 1
        elif kind == "A":
            credit += margins[triangles]
        elif kind == "TP":
            credit += Fraction(3, 4)
        elif kind in ("common_tp", "packing_one_tp"):
            credit += triangles
            deficits += 1
        else:
            require(kind == "common_tpp", f"{recipe.code} unknown ledger packet")
    return credit, deficits


def verify(recipe, tree):
    adj = local_adjacency(tree)
    require(local_signature(tree, adj) == recipe.signature, f"{recipe.code} signature mismatch")
    removed = set(recipe.routers) | set(recipe.opened)
    retained = set().union(*(set(cycles) for _, cycles in recipe.packets))
    require(retained == set(range(10)) - removed, f"{recipe.code} cycle coverage mismatch")
    require(sum(len(cycles) for _, cycles in recipe.packets) == len(retained), f"{recipe.code} packets overlap")

    for router in recipe.routers:
        color = tree.colors[router]
        require(color in ("T", "P"), f"{recipe.code} router is not cyclic")
        require(2 <= len(adj[router]) <= (3 if color == "T" else 5), f"{recipe.code} router has invalid mark count")
    for cycle in recipe.opened:
        require(len(adj[cycle]) == 1, f"{recipe.code} opened cycle is not an incidence leaf")

    require(tuple(step.router for step in recipe.steps) == recipe.routers, f"{recipe.code} router steps disagree with routers")
    for step in recipe.steps:
        marks = set(adj[step.router])
        ports = [cut for cuts, _, _ in step.intervals for cut in cuts]
        require(set(ports) == marks and len(ports) == len(set(ports)), f"{recipe.code} router ports are not partitioned")
        size = 3 if tree.colors[step.router] == "T" else 5
        require(sum(interval_size for _, interval_size, _ in step.intervals) == size, f"{recipe.code} intervals do not total the router cycle")
        require(all(0 < interval_size < size for _, interval_size, _ in step.intervals), f"{recipe.code} has an improper router interval")
        for ports, _, owner in step.intervals:
            require(0 <= owner < len(recipe.packets), f"{recipe.code} interval has no packet owner")
            actual = branch_cycles(tree, step.active, recipe.routers, ports)
            expected = frozenset(set(recipe.packets[owner][1]) & set(step.active))
            require(actual == expected, f"{recipe.code} interval at {ports} is not owned by packet {owner}")

    expected_components = Counter(frozenset(cycles) for _, cycles in recipe.packets if cycles)
    if recipe.code == "N4":
        expected_components = Counter((frozenset(recipe.packets[0][1]), frozenset((2,)), frozenset((9,))))
    require(
        components_after_router_deletion(tree, recipe.routers, recipe.opened) == expected_components,
        f"{recipe.code} router/opening components do not match materialized packets",
    )

    strict = False
    for kind, cycles in recipe.packets:
        require(connected(tree, cycles) or (recipe.code == "N4" and kind == "TP"), f"{recipe.code} has a disconnected packet")
        colors = Counter(tree.colors[cycle] for cycle in cycles)
        if kind == "P":
            require(colors == Counter(P=1), f"{recipe.code} P packet mismatch")
        elif kind == "A":
            require(set(colors) == {"T"} and shared_cut(tree, cycles), f"{recipe.code} A packet mismatch")
            strict = True
        elif kind == "TP":
            require(colors == Counter(T=1, P=1), f"{recipe.code} TP packet mismatch")
            strict = True
        elif kind == "common_tp":
            require(colors["P"] == 1 and colors["T"] == len(cycles) - 1, f"{recipe.code} TP packet mismatch")
            require(shared_cut(tree, cycles), f"{recipe.code} TP packet has no common cut")
            strict = True
        elif kind == "packing_one_tp":
            require(colors == Counter(T=8, P=1), f"{recipe.code} packing-one packet mismatch")
            triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
            require(shared_cut(tree, triangles), f"{recipe.code} triangles do not have packing number one")
            strict = True
        else:
            require(kind == "common_tpp", f"{recipe.code} unknown packet kind")
            require(colors == Counter(T=8, P=2) and shared_cut(tree, cycles), f"{recipe.code} TPP packet mismatch")
            strict = True

    if recipe.code == "N1":
        require(
            common_tpp_positive(tree, recipe.packets[0][1]),
            "common-cut radical ledger is not positive",
        )
    else:
        require(
            packet_ledger(tree, recipe) == (recipe.credit, recipe.deficits),
            f"{recipe.code} packet ledger does not match its claimed margin",
        )
        require(positive(recipe.credit, recipe.deficits), f"{recipe.code} radical ledger is not positive")
    require(strict, f"{recipe.code} has no strict packet")

    certificates = materialize_graph_certificates(tree, recipe)
    if recipe.code == "N4":
        require(len(certificates) == 60, "N4 does not materialize all 60 cyclic placements")
        for certificate in certificates:
            slots = dict(certificate.placement)[0]
            mark_slot = dict(slots)
            owners = {(router, slot): owner for router, slot, owner in certificate.interval_owners}
            require(owners[(0, mark_slot[10])] == 0, "N4 cut 10 is not attached to A_7")
            require(owners[(0, mark_slot[11])] == owners[(0, mark_slot[12])] == 1, "N4 actual TP cuts do not lie in the complementary interval")
            require(sum(owner == 1 for router, _, owner in certificate.interval_owners if router == 0) == 4, "N4 TP owner does not receive four pentagon vertices")
    return certificates


def main():
    classes = BASE.enumerate_colors(("P", "P") + ("T",) * 8, 0)
    class_digest = validate_canonical_rows(classes)
    witnesses, residual_rows, witness_digest = validate_ordinary_stream(classes)
    unresolved = {signature: tree for signature, tree in residual_rows}
    require(set(unresolved) == {recipe.signature for recipe in RECIPES},
            "recipe signatures do not exhaust residuals")
    for recipe in RECIPES:
        certificates = verify(recipe, unresolved[recipe.signature])
        if recipe.code == "N1":
            ledger = ">9-4/(3sqrt(13))"
        elif recipe.deficits == 0:
            ledger = f">{recipe.credit}"
        else:
            ledger = f">{recipe.credit}-{recipe.deficits}delta"
        print(f"{recipe.code} CLOSED: routers={recipe.routers or 'none'} opened={recipe.opened or 'none'} placements={len(certificates)} ledger={ledger}")
    print(f"independent canonical stream: {len(classes)} sha256={class_digest}")
    print(f"materialized ordinary witnesses: {len(witnesses)} sha256={witness_digest}")
    print("verified exact canonical exceptions: 9/9")
    print("all 30386 fully shared T^8PP incidence types close")


if __name__ == "__main__":
    main()
