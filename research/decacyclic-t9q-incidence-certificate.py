#!/usr/bin/env python3
"""Exact fully shared incidence certificate for the rank-ten T^9Q frontier."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "nonacyclic_incidence", HERE / "nonacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("could not load incidence generator")
SPEC.loader.exec_module(BASE)

TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0, 9: 0}

BOUQUET = "X(Q()T()T()T()T()T()T()T()T()T())"
TWO_CUT = "T(X(Q())X(T()T()T()T()T()T()T()T()))"
THREE_CUT = "T(X(Q())X(T())X(T()T()T()T()T()T()T()))"
HOSTILE_SIGNATURES = frozenset({BOUQUET, TWO_CUT, THREE_CUT})

EXPECTED_TOTALS = {
    3: {1: 1, 2: 12, 3: 91, 4: 406, 5: 1178, 6: 2115, 7: 2250, 8: 1246, 9: 275},
    4: {1: 1, 2: 12, 3: 91, 4: 412, 5: 1203, 6: 2187, 7: 2361, 8: 1340, 9: 306},
    5: {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2201, 7: 2393, 8: 1372, 9: 321},
    6: {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2400, 8: 1383, 9: 327},
    7: {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1386, 9: 330},
    8: {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 331},
    9: {1: 1, 2: 12, 3: 91, 4: 412, 5: 1208, 6: 2204, 7: 2402, 8: 1387, 9: 332},
}


@dataclass(frozen=True)
class Repair:
    signature: str
    territories: tuple[tuple[str, tuple[int, ...]], ...]
    cut_owners: tuple[tuple[int, str], ...]
    attachment_owners: tuple[tuple[tuple[str, int], str], ...]
    margin: tuple[int, int]
    strict: bool


def require(condition, message):
    """Fail closed under both normal Python and python -O."""
    if not condition:
        raise RuntimeError(message)


def exact_hostile_positive(integer_credit, delta_count=1):
    """Prove a-delta_count*delta_q>0 using the exact fact 0<delta_q<1."""
    require(integer_credit >= delta_count >= 1, "invalid hostile margin")
    return integer_credit >= delta_count


def validate_tree(tree, capacity):
    adjacent = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    require(len(tree.edges) == len(adjacent) - 1, "incidence graph is not a tree")
    require(
        all(len(adjacent[cut]) >= 2 for cut in range(cycle_count, len(adjacent))),
        "incidence cut has degree below two",
    )
    require(
        all(
            1 <= len(adjacent[cycle]) <= (capacity if color == "Q" else 3)
            for cycle, color in enumerate(tree.colors)
        ),
        "cycle capacity violation",
    )


def materialize_repair(signature, tree):
    adjacent = BASE.adjacency(tree)
    neighbors = cut_neighbors(tree)
    triangles = {i for i, color in enumerate(tree.colors) if color == "T"}
    q_cycle = next(i for i, color in enumerate(tree.colors) if color == "Q")

    if signature == BOUQUET:
        verify_bouquet(tree)
        hub = next(cut for cut, cycles in neighbors.items() if cycles == triangles | {q_cycle})
        repair = Repair(
            signature,
            (("packet:T9Q", tuple(sorted(triangles | {q_cycle}))),),
            ((hub, "packet:T9Q"),),
            tuple((("cycle", cycle), "packet:T9Q") for cycle in sorted(triangles | {q_cycle})),
            (9, 1),
            True,
        )
    elif signature == TWO_CUT:
        verify_two_cut(tree)
        router = next(cycle for cycle in triangles if len(adjacent[cycle]) == 2)
        repair = Repair(
            signature,
            (("packet:T9Q", tuple(sorted(triangles | {q_cycle}))),),
            tuple((cut, "packet:T9Q") for cut in sorted(adjacent[router])),
            tuple((("cycle", cycle), "packet:T9Q") for cycle in sorted(triangles | {q_cycle})),
            (9, 1),
            True,
        )
    else:
        require(signature == THREE_CUT, f"unknown repair signature: {signature}")
        verify_three_cut_opening(tree)
        router = next(cycle for cycle in triangles if len(adjacent[cycle]) == 3)
        leaf = next(
            cycle for cycle in triangles
            if cycle != router and len(adjacent[cycle]) == 1
            and neighbors[adjacent[cycle][0]] == {router, cycle}
        )
        retained = tuple(sorted((triangles - {leaf}) | {q_cycle}))
        repair = Repair(
            signature,
            (("packet:T8Q", retained), ("opened-tree:E", (leaf,))),
            tuple((cut, "packet:T8Q") for cut in sorted(adjacent[router])),
            tuple(
                (("private" if cycle == leaf else "cycle", cycle),
                 "opened-tree:E" if cycle == leaf else "packet:T8Q")
                for cycle in sorted(triangles | {q_cycle})
            ),
            (7, 1),
            True,
        )

    owners = {name for name, _ in repair.territories}
    require(repair.strict, "repair margin is not strict")
    require(exact_hostile_positive(*repair.margin), "repair margin is not positive")
    require(all(owner in owners for _, owner in repair.cut_owners), "unowned cut")
    require(all(owner in owners for _, owner in repair.attachment_owners), "unowned attachment")
    covered = [cycle for _, cycles in repair.territories for cycle in cycles]
    require(sorted(covered) == list(range(10)), "repair territories do not partition cycles")
    return repair


def component_bound(hostile, tree, component):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    triangles, q_count = counts["T"], counts["Q"]
    if q_count == 0:
        return BASE.Bound(
            Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}"
        )
    if triangles == 0:
        if hostile:
            return BASE.Bound(Fraction(-1), True, "hostile Q > -1")
        return BASE.Bound(Fraction(0), False, "nonhostile Q >= 0")
    if triangles == 1:
        return BASE.Bound(Fraction(0), True, "TQ > 0")
    if triangles == 2:
        return BASE.Bound(Fraction(0), False, "TTQ >= 0")
    return BASE.Bound(
        Fraction(0), True, f"rank-{triangles + 1} theorem"
    )


def cut_neighbors(tree):
    adjacent = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    return {
        cut: {cycle for cycle in adjacent[cut] if cycle < cycle_count}
        for cut in range(cycle_count, len(adjacent))
    }


def verify_bouquet(tree):
    neighbors = cut_neighbors(tree)
    triangles = {i for i, color in enumerate(tree.colors) if color == "T"}
    q_cycle = next(i for i, color in enumerate(tree.colors) if color == "Q")
    if not any(cycles == triangles | {q_cycle} for cycles in neighbors.values()):
        raise AssertionError("bouquet does not have one real common cut")


def verify_two_cut(tree):
    adjacent = BASE.adjacency(tree)
    neighbors = cut_neighbors(tree)
    triangles = {i for i, color in enumerate(tree.colors) if color == "T"}
    q_cycle = next(i for i, color in enumerate(tree.colors) if color == "Q")
    hubs = [cut for cut, cycles in neighbors.items() if cycles == triangles]
    if len(hubs) != 1:
        raise AssertionError("two-cut repair lacks a unique nine-triangle hub")
    routers = [cycle for cycle in triangles if len(adjacent[cycle]) == 2]
    if len(routers) != 1:
        raise AssertionError("two-cut repair lacks its triangle router")
    router = routers[0]
    if not any(neighbors[cut] == {router, q_cycle} for cut in adjacent[q_cycle]):
        raise AssertionError("Q is not joined at the router's second cut")


def verify_three_cut_opening(tree):
    adjacent = BASE.adjacency(tree)
    neighbors = cut_neighbors(tree)
    triangles = {i for i, color in enumerate(tree.colors) if color == "T"}
    q_cycle = next(i for i, color in enumerate(tree.colors) if color == "Q")
    routers = [cycle for cycle in triangles if len(adjacent[cycle]) == 3]
    if len(routers) != 1:
        raise AssertionError("three-cut repair lacks its saturated router")
    router = routers[0]
    leaf_triangles = [
        cycle
        for cycle in triangles
        if cycle != router
        and len(adjacent[cycle]) == 1
        and neighbors[adjacent[cycle][0]] == {router, cycle}
    ]
    if len(leaf_triangles) != 1:
        raise AssertionError("three-cut repair lacks its openable leaf triangle")
    retained_triangles = triangles - {leaf_triangles[0]}
    hubs = [
        cut for cut, cycles in neighbors.items() if retained_triangles <= cycles
    ]
    if len(hubs) != 1 or router not in neighbors[hubs[0]]:
        raise AssertionError("opened complement lacks its eight-triangle hub")
    if not any(neighbors[cut] == {router, q_cycle} for cut in adjacent[q_cycle]):
        raise AssertionError("Q is not rooted at the retained router")


def main():
    regimes = (
        ("q=3", 3, False),
        ("q=4", 4, False),
        ("q=5", 5, True),
        ("q=6", 6, False),
        # q=7 is nonhostile; this deliberately audits a conservative weakening.
        ("capacity 7 (conservative; q=7 is nonhostile)", 7, True),
        ("q=8", 8, False),
        ("capacity >=9 (conservative hostile ledger)", 9, True),
    )
    for label, capacity, hostile in regimes:
        result = BASE.census(
            ("T",) * 9 + ("Q",),
            capacity,
            lambda tree, component, hostile=hostile: component_bound(
                hostile, tree, component
            ),
        )
        totals, resolved, _, _, _, unresolved = result
        require(totals == Counter(EXPECTED_TOTALS[capacity]), f"wrong {label} incidence totals")
        signatures = {row[1] for row in unresolved}
        expected = HOSTILE_SIGNATURES if hostile else {BOUQUET}
        require(
            signatures == expected and len(unresolved) == len(expected),
            f"wrong {label} frontier: {sorted(signatures)}",
        )

        trees = {sig: tree for sig, tree in BASE.enumerate_colors(("Q",) + ("T",) * 9, capacity)}
        require(len(trees) == sum(totals.values()), f"wrong {label} canonical orbit sum")
        for tree in trees.values():
            validate_tree(tree, capacity)
        repairs = (materialize_repair(BOUQUET, trees[BOUQUET]),)
        if hostile:
            repairs = tuple(materialize_repair(sig, trees[sig]) for sig in sorted(HOSTILE_SIGNATURES))
            require({repair.signature for repair in repairs} == HOSTILE_SIGNATURES, "repair orbit mismatch")

        total = sum(totals.values())
        safe = sum(resolved.values())
        print(
            f"T^9Q {label}: {total}={safe}+{len(unresolved)}; "
            f"cuts={dict(sorted(totals.items()))}; repairs={len(repairs)}"
        )

    print("all fully shared T^9Q incidences close")
    print("hostile repairs: common cut; packing-one two-cut; open leaf T then packing-one")


if __name__ == "__main__":
    main()
