#!/usr/bin/env python3
"""Direct replacement audit for the seven fully shared T^7PP exceptions.

The audit regenerates the exceptions from the rank-nine census, checks exact
edge representatives, and verifies every proposed router refinement and packet
ledger. All seven rows close; the pentagon-router row uses a leaf-pentagon
opening rather than its insufficient direct split.
"""

from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def load_census():
    name = "nonacyclic_fully_shared_incidence_census"
    spec = spec_from_file_location(
        name, HERE / "nonacyclic-fully-shared-incidence-census.py"
    )
    module = module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CENSUS = load_census()


@dataclass(frozen=True)
class Exact:
    rational: Fraction = Fraction(0)
    sqrt5: Fraction = Fraction(0)
    sqrt13: Fraction = Fraction(0)

    def __add__(self, other):
        return Exact(
            self.rational + other.rational,
            self.sqrt5 + other.sqrt5,
            self.sqrt13 + other.sqrt13,
        )

    def __str__(self):
        terms = [str(self.rational)] if self.rational else []
        for coefficient, radical in ((self.sqrt5, "sqrt(5)"), (self.sqrt13, "sqrt(13)")):
            if not coefficient:
                continue
            sign = "+" if coefficient > 0 else "-"
            magnitude = abs(coefficient)
            factor = "" if magnitude == 1 else f"{magnitude}*"
            terms.append(f"{sign}{factor}{radical}")
        return "".join(terms) or "0"


@dataclass(frozen=True)
class Packet:
    name: str
    cycles: tuple[int, ...]
    kind: str


@dataclass(frozen=True)
class Step:
    router: int
    active: tuple[int, ...]
    intervals: tuple[tuple[int, int], ...]
    branches: tuple[tuple[int, tuple[int, ...]], ...]


@dataclass(frozen=True)
class Recipe:
    code: str
    closed: bool
    signature: str
    edges: tuple[tuple[int, int], ...]
    steps: tuple[Step, ...]
    packets: tuple[Packet, ...]
    expected: Exact


def q(*values):
    return tuple(values)


RECIPES = (
    Recipe(
        "N1", True,
        "X(P()P()T()T()T()T()T()T()T())",
        q((0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9)),
        (),
        (Packet("T^7PP", q(0, 1, 2, 3, 4, 5, 6, 7, 8), "common_tpp"),),
        Exact(Fraction(8), sqrt13=Fraction(-4, 39)),
    ),
    Recipe(
        "F9", True,
        "P(X(P())X(T()T()T()T()T()T()T()))",
        q((0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (7, 10), (8, 10)),
        (),
        (Packet("T^7P7", q(0, 1, 2, 3, 4, 5, 6, 7), "common_tp"), Packet("P8-y", q(8), "opened_leaf")),
        Exact(Fraction(8), sqrt5=Fraction(-1)),
    ),
    Recipe(
        "N2", True,
        "T(X(P())X(P()T()T()T()T()T()T()))",
        q((0, 9), (0, 10), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 10), (8, 9)),
        (Step(0, q(0, 1, 2, 3, 4, 5, 6, 7, 8), q((9, 2), (10, 1)), q((9, q(1, 2, 3, 4, 5, 6, 8)), (10, q(7)))),),
        (Packet("P7", q(7), "P"), Packet("T^6P", q(1, 2, 3, 4, 5, 6, 8), "common_tp")),
        Exact(Fraction(10), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "N3", True,
        "T(X(P())X(P()T()T()T()T()T())X(T()))",
        q((0, 9), (0, 10), (0, 11), (1, 9), (2, 10), (3, 9), (4, 9), (5, 9), (6, 9), (7, 11), (8, 9)),
        (Step(0, q(0, 1, 2, 3, 4, 5, 6, 7, 8), q((9, 1), (10, 1), (11, 1)), q((9, q(1, 3, 4, 5, 6, 8)), (10, q(2)), (11, q(7)))),),
        (Packet("P7", q(7), "P"), Packet("T2", q(2), "A"), Packet("T^5P", q(1, 3, 4, 5, 6, 8), "common_tp")),
        Exact(Fraction(9), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "N4", True,
        "X(T()T()T()T()T()T(X(P()))T(X(P())))",
        q((0, 9), (0, 10), (1, 9), (1, 11), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 10), (8, 11)),
        (
            Step(0, q(0, 1, 2, 3, 4, 5, 6, 7, 8), q((9, 2), (10, 1)), q((9, q(1, 2, 3, 4, 5, 6, 8)), (10, q(7)))),
            Step(1, q(1, 2, 3, 4, 5, 6, 8), q((9, 2), (11, 1)), q((9, q(2, 3, 4, 5, 6)), (11, q(8)))),
        ),
        (Packet("P7", q(7), "P"), Packet("P8", q(8), "P"), Packet("A_5", q(2, 3, 4, 5, 6), "A")),
        Exact(Fraction(6), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "N5", True,
        "X(T()T()T()T()T(X(P()))T(X(P())X(T())))",
        q((0, 9), (0, 10), (0, 11), (1, 9), (1, 12), (2, 10), (3, 9), (4, 9), (5, 9), (6, 9), (7, 11), (8, 12)),
        (
            Step(0, q(0, 1, 2, 3, 4, 5, 6, 7, 8), q((9, 1), (10, 1), (11, 1)), q((9, q(1, 3, 4, 5, 6, 8)), (10, q(2)), (11, q(7)))),
            Step(1, q(1, 3, 4, 5, 6, 8), q((9, 2), (12, 1)), q((9, q(3, 4, 5, 6)), (12, q(8)))),
        ),
        (Packet("P7", q(7), "P"), Packet("P8", q(8), "P"), Packet("T2", q(2), "A"), Packet("A_4", q(3, 4, 5, 6), "A")),
        Exact(Fraction(7), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "N6", True,
        "X(T()T()T()T(X(P())X(T()))T(X(P())X(T())))",
        q((0, 9), (0, 10), (0, 12), (1, 9), (1, 11), (1, 13), (2, 10), (3, 9), (4, 9), (5, 9), (6, 11), (7, 12), (8, 13)),
        (
            Step(0, q(0, 1, 2, 3, 4, 5, 6, 7, 8), q((9, 1), (10, 1), (12, 1)), q((9, q(1, 3, 4, 5, 6, 8)), (10, q(2)), (12, q(7)))),
            Step(1, q(1, 3, 4, 5, 6, 8), q((9, 1), (11, 1), (13, 1)), q((9, q(3, 4, 5)), (11, q(6)), (13, q(8)))),
        ),
        (Packet("P7", q(7), "P"), Packet("P8", q(8), "P"), Packet("T2", q(2), "A"), Packet("T6", q(6), "A"), Packet("A_3", q(3, 4, 5), "A")),
        Exact(Fraction(6), sqrt5=Fraction(-2)),
    ),
)


def component_cycles(tree, active, removed, start_cut):
    adj = CENSUS.adjacency(tree)
    cycle_count = len(tree.colors)
    allowed_cycles = set(active) - set(removed)
    seen = {start_cut}
    todo = [start_cut]
    cycles = set()
    while todo:
        vertex = todo.pop()
        for neighbor in adj[vertex]:
            if neighbor < cycle_count and neighbor not in allowed_cycles:
                continue
            if neighbor not in seen:
                seen.add(neighbor)
                todo.append(neighbor)
                if neighbor < cycle_count:
                    cycles.add(neighbor)
    return tuple(sorted(cycles))


def connected(tree, cycles):
    if len(cycles) <= 1:
        return True
    adj = CENSUS.adjacency(tree)
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
    adj = CENSUS.adjacency(tree)
    return next(
        (cut for cut in adj[cycles[0]] if all(cut in adj[cycle] for cycle in cycles)),
        None,
    )


def packet_bound(tree, packet):
    colors = tuple(tree.colors[cycle] for cycle in packet.cycles)
    assert connected(tree, packet.cycles)
    if packet.kind == "P":
        assert colors == ("P",)
        return Exact(Fraction(2), sqrt5=Fraction(-1)), False, "P>=-delta"
    if packet.kind == "opened_leaf":
        assert colors == ("P",)
        assert len(CENSUS.adjacency(tree)[packet.cycles[0]]) == 1
        return Exact(Fraction(-1)), False, "opened leaf P-y tree=-1"
    if packet.kind == "A":
        margins = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0}
        assert colors and set(colors) == {"T"}
        assert shared_cut(tree, packet.cycles) is not None
        margin = margins[len(colors)]
        return Exact(Fraction(margin)), True, f"A_{len(colors)}>{margin}"
    if packet.kind == "common_tp":
        assert colors.count("P") == 1 and colors.count("T") == len(colors) - 1
        assert shared_cut(tree, packet.cycles) is not None
        triangles = colors.count("T")
        return Exact(Fraction(triangles + 2), sqrt5=Fraction(-1)), True, f"common-cut T^{triangles}P>{triangles}-delta"
    assert packet.kind == "common_tpp"
    assert colors.count("P") == 2 and colors.count("T") == 7
    assert shared_cut(tree, packet.cycles) is not None
    return Exact(Fraction(8), sqrt13=Fraction(-4, 39)), True, "common-cut T^7PP>8-4/(3sqrt(13))"


def verify_recipe(recipe, tree):
    assert tree.edges == recipe.edges
    assert CENSUS.signature(tree) == recipe.signature
    adj = CENSUS.adjacency(tree)
    split = tuple(step.router for step in recipe.steps)
    assert len(split) == len(set(split))
    previous_branches = None
    removed = set()
    for step in recipe.steps:
        assert step.router in step.active and step.router not in removed
        if previous_branches is not None:
            assert step.active in previous_branches
        marks = tuple(adj[step.router])
        intervals = dict(step.intervals)
        branches = dict(step.branches)
        assert set(intervals) == set(marks) == set(branches)
        cycle_size = 3 if tree.colors[step.router] == "T" else 5
        assert all(0 < size < cycle_size for size in intervals.values())
        assert sum(intervals.values()) == cycle_size
        if tree.colors[step.router] == "T":
            assert sorted(intervals.values()) == ([1, 2] if len(marks) == 2 else [1, 1, 1])
        else:
            assert recipe.code == "F9" and sorted(intervals.values()) == [1, 4]
        removed.add(step.router)
        for cut in marks:
            assert component_cycles(tree, step.active, removed, cut) == branches[cut]
        branch_union = set().union(*(set(cycles) for cycles in branches.values()))
        assert branch_union == set(step.active) - {step.router}
        assert sum(map(len, branches.values())) == len(branch_union)
        previous_branches = tuple(branches.values())

    retained = set().union(
        *(set(packet.cycles) for packet in recipe.packets if packet.kind != "opened_leaf")
    )
    opened = {
        cycle
        for packet in recipe.packets
        if packet.kind == "opened_leaf"
        for cycle in packet.cycles
    }
    assert retained | opened == set(range(9)) - set(split)
    assert retained.isdisjoint(opened)
    packet_of = {
        cycle: index
        for index, packet in enumerate(recipe.packets)
        for cycle in packet.cycles
    }
    cut_owner = {}
    for cut in range(9, len(adj)):
        owners = {
            packet_of[cycle]
            for cycle in adj[cut]
            if cycle in packet_of and cycle not in opened
        }
        assert len(owners) == 1
        cut_owner[cut] = owners.pop()
    for step in recipe.steps:
        assert len({cut_owner[cut] for cut, _ in step.intervals}) == len(step.intervals)

    bounds = tuple(packet_bound(tree, packet) for packet in recipe.packets)
    ledger = sum((bound[0] for bound in bounds), Exact())
    assert ledger == recipe.expected and any(bound[1] for bound in bounds)
    return ledger, tuple(bound[2] for bound in bounds)


def main():
    result = CENSUS.census(("T",) * 7 + ("P",) * 2, 0, CENSUS.tpp_bound)
    assert sum(result[0].values()) == 8004
    assert sum(result[1].values()) == 7997
    assert len(result[-1]) == 7
    unresolved = {signature: edges for _, signature, _, edges in result[-1]}
    assert set(unresolved) == {recipe.signature for recipe in RECIPES}
    trees = dict(CENSUS.enumerate_colors(("P", "P") + ("T",) * 7, 0))

    closed = 0
    for recipe in RECIPES:
        assert unresolved[recipe.signature] == recipe.edges
        ledger, sources = verify_recipe(recipe, trees[recipe.signature])
        status = "CLOSED" if recipe.closed else "OPEN"
        print(f"{recipe.code} {status}: {' + '.join(sources)}; ledger={ledger}")
        closed += recipe.closed

    assert closed == 7
    assert RECIPES[1].expected == Exact(Fraction(8), sqrt5=Fraction(-1))
    assert Fraction(3) ** 2 > 5
    print("verified exact canonical exceptions: 7/7")
    print("replacement closures: 7/7")
    print("F9 leaf opening: 6-delta = 8-sqrt(5) > 0")
    print("all fully shared T^7PP incidence types close; no broader theorem asserted")


if __name__ == "__main__":
    main()
