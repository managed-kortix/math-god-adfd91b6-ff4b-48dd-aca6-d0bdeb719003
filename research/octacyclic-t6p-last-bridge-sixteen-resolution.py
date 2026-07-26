#!/usr/bin/env python3
"""Exact packet verifier for all 16 conservative last-bridge failures."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


AUDIT = load("last_bridge_audit", "octacyclic-t6p-last-bridge-conservative.py")
CENSUS = AUDIT.CENSUS
X = "P1"
E = "entry-tree"


@dataclass(frozen=True)
class Recipe:
    split: tuple[int, ...]
    packets: tuple[tuple[object, ...], ...]
    expected: tuple[Fraction, int]


RECIPES = (
    Recipe((), ((0, 1, 2, 3, 4, 5, 6), (X,)), (Fraction(6), 2)),
    Recipe((), ((0, 1, 2, 3, 4, 5, 6), (X,)), (Fraction(6), 2)),
    Recipe((0,), ((2,), (1, 3, 4, 5, 6), (X,)), (Fraction(4), 2)),
    Recipe((0,), ((2,), (1, 3, 4, 5, 6), (X,)), (Fraction(4), 2)),
    Recipe((0,), ((2,), (1, 3, 4, 5, 6), (X,)), (Fraction(4), 2)),
    Recipe((0,), ((2,), (1, 3, 4, 5, 6), (X,)), (Fraction(4), 2)),
    Recipe((0,), ((2,), (1, 3, 4, 5, 6), (X,), (E,)), (Fraction(3), 2)),
    Recipe((0, 1), ((2,), (5,), (3, 4, 6), (X,)), (Fraction(2), 2)),
    Recipe((0, 1), ((2,), (5,), (3, 4, 6), (X,)), (Fraction(2), 2)),
    Recipe((0, 1), ((2,), (5,), (3, 4, 6), (X,)), (Fraction(2), 2)),
    Recipe((0, 1), ((2,), (5,), (3, 4, 6), (X,), (E,)), (Fraction(1), 2)),
    Recipe((0, 1), ((2,), (5,), (3, 4, 6), (X,)), (Fraction(2), 2)),
    Recipe((0, 1), ((2,), (4,), (3, 5, 6), (X,)), (Fraction(2), 2)),
    Recipe((1, 3), ((4,), (5,), (0, 2, 6), (X,)), (Fraction(2), 2)),
    Recipe((1, 3), ((4,), (5,), (0, 2, 6), (X,)), (Fraction(2), 2)),
    Recipe((1, 3), ((4,), (5,), (0, 2, 6), (X,)), (Fraction(2), 2)),
)


def connected(tree, cycles):
    if len(cycles) <= 1:
        return True
    adj = CENSUS.BASE.adjacency(tree)
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


def common_cut(tree, cycles):
    adj = CENSUS.BASE.adjacency(tree)
    return any(all(cut in adj[cycle] for cycle in cycles) for cut in adj[cycles[0]])


def packet_bound(tree, packet):
    """Return (a,b,source) for the strict lower bound sigma>a-b*delta."""
    if packet == (X,):
        return Fraction(0), 1, "P1"
    if packet == (E,):
        return Fraction(-1), 0, "acyclic private-entry interval"
    cycles = tuple(packet)
    assert connected(tree, cycles)
    triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
    pentagons = tuple(cycle for cycle in cycles if tree.colors[cycle] == "P")
    if not pentagons:
        return Fraction(CENSUS.TRIANGLE_MARGIN[len(triangles)]), 0, f"A_{len(triangles)}"
    assert len(pentagons) == 1 and triangles
    if common_cut(tree, cycles):
        return Fraction(len(triangles)), 1, f"common-cut T^{len(triangles)}P0"
    assert len(triangles) == 2 and common_cut(tree, triangles)
    return Fraction(2), 1, "shared-cut TTP0>2-delta"


def verify_ownership(tree, mark, recipe):
    adj = CENSUS.BASE.adjacency(tree)
    packet_of = {
        item: index for index, packet in enumerate(recipe.packets) for item in packet
    }
    expected = (set(range(7)) - set(recipe.split)) | {X}
    if mark.kind == "private" and mark.vertex in recipe.split:
        expected.add(E)
    assert set(packet_of) == expected
    assert len(packet_of) == sum(len(packet) for packet in recipe.packets)

    for cut in range(len(tree.colors), len(adj)):
        retained = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        assert len(retained) <= 1

    for router in recipe.split:
        owners = []
        for cut in adj[router]:
            retained = [cycle for cycle in adj[cut] if cycle in packet_of]
            assert retained
            side_owners = {packet_of[cycle] for cycle in retained}
            assert len(side_owners) == 1
            owners.extend(side_owners)
        if mark.kind == "private" and mark.vertex == router:
            owners.append(packet_of[E])
        assert len(owners) in (2, 3)
        assert len(owners) == len(set(owners))


def exact_positive(ledger):
    a, b = ledger
    # a-b*(sqrt(5)-2)>0 iff a+2b>b*sqrt(5); square only positive rationals.
    left = a + 2 * b
    return left > 0 and left * left > 5 * b * b


def main():
    _, _, failures = AUDIT.census()
    assert len(failures) == len(RECIPES) == 16
    assert Counter(row[0] for row in failures) == Counter({1: 2, 2: 5, 3: 5, 4: 4})
    trees = dict(CENSUS.BASE.enumerate_colors(("P",) + ("T",) * 6, 5))
    ledgers = Counter()

    for index, (failure, recipe) in enumerate(zip(failures, RECIPES), 1):
        _, signature, root_code, mark, positions, _ = failure
        tree = trees[signature]
        verify_ownership(tree, mark, recipe)
        bounds = tuple(packet_bound(tree, packet) for packet in recipe.packets)
        ledger = (sum(item[0] for item in bounds), sum(item[1] for item in bounds))
        assert ledger == recipe.expected and exact_positive(ledger)
        ledgers[ledger] += 1
        sources = " + ".join(item[2] for item in bounds)
        print(
            f"L{index}: c={failure[0]} root={mark.kind}:{mark.vertex} "
            f"positions={positions} split={recipe.split or 'none'}; {sources}; "
            f"sigma>{ledger[0]}-{ledger[1]}delta; code={root_code}"
        )

    assert ledgers == Counter(
        {
            (Fraction(6), 2): 2,
            (Fraction(4), 2): 4,
            (Fraction(3), 2): 1,
            (Fraction(2), 2): 8,
            (Fraction(1), 2): 1,
        }
    )
    print("closed conservative failures: 16/16")
    print("weakest exact margin: 1-2delta = 5-2sqrt(5) > 0")


if __name__ == "__main__":
    main()
