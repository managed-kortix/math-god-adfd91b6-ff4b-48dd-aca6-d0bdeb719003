#!/usr/bin/env python3
"""Exact replacement audit for all nine fully shared rank-ten T^8PP rows."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
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
    adj = BASE.adjacency(tree)
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
    adj = BASE.adjacency(tree)
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
    adj = BASE.adjacency(tree)
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
    adj = BASE.adjacency(tree)
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
    marks = tuple(BASE.adjacency(tree)[step.router])
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
    adj = BASE.adjacency(tree)
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
    require(BASE.signature(tree) == recipe.signature, f"{recipe.code} signature mismatch")
    removed = set(recipe.routers) | set(recipe.opened)
    retained = set().union(*(set(cycles) for _, cycles in recipe.packets))
    require(retained == set(range(10)) - removed, f"{recipe.code} cycle coverage mismatch")
    require(sum(len(cycles) for _, cycles in recipe.packets) == len(retained), f"{recipe.code} packets overlap")
    adj = BASE.adjacency(tree)

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
    result = BASE.census(("T",) * 8 + ("P",) * 2, 0, CENSUS.tpp_bound)
    require(sum(result[0].values()) == 30386, "full census total changed")
    require(sum(result[1].values()) == 30377, "ordinary accepted total changed")
    require(len(result[-1]) == 9, "ordinary residual total changed")
    unresolved = {signature: edges for _, signature, _, edges in result[-1]}
    require(set(unresolved) == {recipe.signature for recipe in RECIPES}, "recipe signatures do not exhaust residuals")
    trees = dict(BASE.enumerate_colors(("P", "P") + ("T",) * 8, 0))
    for recipe in RECIPES:
        require(trees[recipe.signature].edges == unresolved[recipe.signature], f"{recipe.code} representative mismatch")
        certificates = verify(recipe, trees[recipe.signature])
        if recipe.code == "N1":
            ledger = ">9-4/(3sqrt(13))"
        elif recipe.deficits == 0:
            ledger = f">{recipe.credit}"
        else:
            ledger = f">{recipe.credit}-{recipe.deficits}delta"
        print(f"{recipe.code} CLOSED: routers={recipe.routers or 'none'} opened={recipe.opened or 'none'} placements={len(certificates)} ledger={ledger}")
    print("verified exact canonical exceptions: 9/9")
    print("all 30386 fully shared T^8PP incidence types close")


if __name__ == "__main__":
    main()
