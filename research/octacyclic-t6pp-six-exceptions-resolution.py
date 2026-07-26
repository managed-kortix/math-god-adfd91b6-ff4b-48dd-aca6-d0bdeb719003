#!/usr/bin/env python3
"""Exact structural and symbolic verifier for the six T^6PP exceptions.

This standard-library audit regenerates U1--U6 from the authoritative fully
shared incidence census and checks the replacement packetizations in
octacyclic-t6pp-six-exceptions-resolution-2026-07-26.md.
"""

from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def load_census():
    name = "octacyclic_fully_shared_incidence_census"
    spec = spec_from_file_location(
        name, HERE / "octacyclic-fully-shared-incidence-census.py"
    )
    module = module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CENSUS = load_census()


@dataclass(frozen=True)
class Exact:
    """An exact element rational + sqrt5*sqrt(5) + sqrt13*sqrt(13)."""

    rational: Fraction = Fraction(0)
    sqrt5: Fraction = Fraction(0)
    sqrt13: Fraction = Fraction(0)

    def __add__(self, other):
        return Exact(
            self.rational + other.rational,
            self.sqrt5 + other.sqrt5,
            self.sqrt13 + other.sqrt13,
        )

    def __sub__(self, other):
        return Exact(
            self.rational - other.rational,
            self.sqrt5 - other.sqrt5,
            self.sqrt13 - other.sqrt13,
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
    signature: str
    edges: tuple[tuple[int, int], ...]
    steps: tuple[Step, ...]
    packets: tuple[Packet, ...]
    expected: Exact


def q(*values):
    return tuple(values)


RECIPES = (
    Recipe(
        "U1",
        "X(P()P()T()T()T()T()T()T())",
        q((0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8)),
        (),
        (Packet("T^6PP", q(0, 1, 2, 3, 4, 5, 6, 7), "common_tpp"),),
        Exact(Fraction(7), sqrt13=Fraction(-4, 39)),
    ),
    Recipe(
        "U2",
        "T(X(P())X(P()T()T()T()T()T()))",
        q((0, 8), (0, 9), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 9), (7, 8)),
        (Step(0, q(0, 1, 2, 3, 4, 5, 6, 7), q((8, 2), (9, 1)), q((8, q(1, 2, 3, 4, 5, 7)), (9, q(6)))),),
        (Packet("P6", q(6), "P"), Packet("T^5P", q(1, 2, 3, 4, 5, 7), "common_tp")),
        Exact(Fraction(9), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "U3",
        "T(X(P())X(P()T()T()T()T())X(T()))",
        q((0, 8), (0, 9), (0, 10), (1, 8), (2, 9), (3, 8), (4, 8), (5, 8), (6, 10), (7, 8)),
        (Step(0, q(0, 1, 2, 3, 4, 5, 6, 7), q((8, 1), (9, 1), (10, 1)), q((8, q(1, 3, 4, 5, 7)), (9, q(2)), (10, q(6)))),),
        (Packet("P6", q(6), "P"), Packet("T2", q(2), "A"), Packet("T^4P", q(1, 3, 4, 5, 7), "common_tp")),
        Exact(Fraction(8), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "U4",
        "X(T()T()T()T()T(X(P()))T(X(P())))",
        q((0, 8), (0, 9), (1, 8), (1, 10), (2, 8), (3, 8), (4, 8), (5, 8), (6, 9), (7, 10)),
        (
            Step(0, q(0, 1, 2, 3, 4, 5, 6, 7), q((8, 2), (9, 1)), q((8, q(1, 2, 3, 4, 5, 7)), (9, q(6)))),
            Step(1, q(1, 2, 3, 4, 5, 7), q((8, 2), (10, 1)), q((8, q(2, 3, 4, 5)), (10, q(7)))),
        ),
        (Packet("P6", q(6), "P"), Packet("P7", q(7), "P"), Packet("A_4", q(2, 3, 4, 5), "A")),
        Exact(Fraction(7), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "U5",
        "X(T()T()T()T(X(P()))T(X(P())X(T())))",
        q((0, 8), (0, 9), (0, 10), (1, 8), (1, 11), (2, 9), (3, 8), (4, 8), (5, 8), (6, 10), (7, 11)),
        (
            Step(0, q(0, 1, 2, 3, 4, 5, 6, 7), q((8, 1), (9, 1), (10, 1)), q((8, q(1, 3, 4, 5, 7)), (9, q(2)), (10, q(6)))),
            Step(1, q(1, 3, 4, 5, 7), q((8, 2), (11, 1)), q((8, q(3, 4, 5)), (11, q(7)))),
        ),
        (Packet("P6", q(6), "P"), Packet("P7", q(7), "P"), Packet("T2", q(2), "A"), Packet("A_3", q(3, 4, 5), "A")),
        Exact(Fraction(6), sqrt5=Fraction(-2)),
    ),
    Recipe(
        "U6",
        "X(T()T()T(X(P())X(T()))T(X(P())X(T())))",
        q((0, 8), (0, 9), (0, 11), (1, 8), (1, 10), (1, 12), (2, 9), (3, 8), (4, 8), (5, 10), (6, 11), (7, 12)),
        (
            Step(0, q(0, 1, 2, 3, 4, 5, 6, 7), q((8, 1), (9, 1), (11, 1)), q((8, q(1, 3, 4, 5, 7)), (9, q(2)), (11, q(6)))),
            Step(1, q(1, 3, 4, 5, 7), q((8, 1), (10, 1), (12, 1)), q((8, q(3, 4)), (10, q(5)), (12, q(7)))),
        ),
        (Packet("P6", q(6), "P"), Packet("P7", q(7), "P"), Packet("T2", q(2), "A"), Packet("T5", q(5), "A"), Packet("A_2", q(3, 4), "A")),
        Exact(Fraction(5), sqrt5=Fraction(-2)),
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
    if packet.kind == "A":
        assert colors and set(colors) == {"T"}
        assert 1 <= len(colors) <= 4
        assert shared_cut(tree, packet.cycles) is not None
        return Exact(Fraction(len(colors) - 1)), True, f"A_{len(colors)}>{len(colors) - 1}"
    if packet.kind == "common_tp":
        assert colors.count("P") == 1 and colors.count("T") == len(colors) - 1
        assert shared_cut(tree, packet.cycles) is not None
        triangles = colors.count("T")
        return Exact(Fraction(triangles + 2), sqrt5=Fraction(-1)), True, f"common-cut T^{triangles}P>{triangles}-delta"
    assert packet.kind == "common_tpp"
    assert colors.count("P") == 2 and colors.count("T") == 6
    assert shared_cut(tree, packet.cycles) is not None
    return Exact(Fraction(7), sqrt13=Fraction(-4, 39)), True, "common-cut T^6PP>7-4/(3sqrt(13))"


def verify_recipe(recipe, tree):
    assert tree.edges == recipe.edges
    assert CENSUS.signature(tree) == recipe.signature
    adj = CENSUS.adjacency(tree)
    split = tuple(step.router for step in recipe.steps)
    assert len(split) == len(set(split))

    previous_branches = None
    removed = set()
    for step in recipe.steps:
        assert tree.colors[step.router] == "T"
        assert step.router in step.active and step.router not in removed
        if previous_branches is not None:
            assert step.active in previous_branches
        marks = tuple(adj[step.router])
        intervals = dict(step.intervals)
        branches = dict(step.branches)
        assert tuple(sorted(intervals)) == tuple(sorted(marks))
        assert tuple(sorted(branches)) == tuple(sorted(marks))
        assert len(marks) in (2, 3)
        assert sorted(intervals.values()) == ([1, 2] if len(marks) == 2 else [1, 1, 1])
        assert sum(intervals.values()) == 3
        removed.add(step.router)
        for cut in marks:
            assert component_cycles(tree, step.active, removed, cut) == branches[cut]
        branch_union = set().union(*(set(cycles) for cycles in branches.values()))
        assert branch_union == set(step.active) - {step.router}
        assert sum(len(cycles) for cycles in branches.values()) == len(branch_union)
        previous_branches = tuple(branches.values())

    retained = set().union(*(set(packet.cycles) for packet in recipe.packets))
    assert retained == set(range(8)) - set(split)
    assert sum(len(packet.cycles) for packet in recipe.packets) == len(retained)
    packet_of = {
        cycle: index
        for index, packet in enumerate(recipe.packets)
        for cycle in packet.cycles
    }

    cut_owner = {}
    for cut in range(8, len(adj)):
        owners = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        assert len(owners) == 1
        cut_owner[cut] = owners.pop()
    for step in recipe.steps:
        assert len({cut_owner[cut] for cut, _ in step.intervals}) == len(step.intervals)

    bounds = tuple(packet_bound(tree, packet) for packet in recipe.packets)
    ledger = sum((bound[0] for bound in bounds), Exact())
    assert ledger == recipe.expected
    assert any(bound[1] for bound in bounds)
    return ledger, tuple(bound[2] for bound in bounds)


def main():
    result = CENSUS.census(("T",) * 6 + ("P",) * 2, 0, CENSUS.tpp_bound)
    assert sum(result[0].values()) == 2116
    assert sum(result[1].values()) == 2110
    assert len(result[-1]) == 6
    unresolved = {signature: edges for _, signature, edges in result[-1]}
    assert set(unresolved) == {recipe.signature for recipe in RECIPES}

    trees = dict(CENSUS.enumerate_colors(("P", "P") + ("T",) * 6, 0))
    ledgers = []
    for recipe in RECIPES:
        assert unresolved[recipe.signature] == recipe.edges
        tree = trees[recipe.signature]
        ledger, sources = verify_recipe(recipe, tree)
        ledgers.append(ledger)
        source_text = " + ".join(sources)
        print(f"{recipe.code}: {source_text}; ledger={ledger}")

    weakest = Exact(Fraction(5), sqrt5=Fraction(-2))
    assert ledgers[-1] == weakest
    assert all(
        ledger == weakest or (ledger - weakest).rational > 0
        for ledger in ledgers[1:]
    )
    assert ledgers[0].rational - Fraction(4, 3) > weakest.rational
    assert Fraction(5, 2) ** 2 > 5
    print("verified canonical exceptions: 6/6")
    print("weakest strict margin: 1-2delta = 5-2sqrt(5) > 0")


if __name__ == "__main__":
    main()
