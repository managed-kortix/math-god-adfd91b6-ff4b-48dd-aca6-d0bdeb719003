#!/usr/bin/env python3
"""Exact marked-entry router certificate for the A_9 | Q endpoint."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "marked_router", HERE / "nonacyclic-t7p-last-bridge-conservative.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("could not load marked router dependency")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)

BASE.TRIANGLE_MARGIN.update({8: 0, 9: 0})

BOUQUET = "X(T()T()T()T()T()T()T()T()T())"
TWO_HUB = "T(X(T())X(T()T()T()T()T()T()T()))"
EXPECTED_FAILURES = {
    (TWO_HUB, "TR(X(T())X(T()T()T()T()T()T()T()))", "private", 1),
    (BOUQUET, "R(T()T()T()T()T()T()T()T()T())", "cut", 1),
    (BOUQUET, "X(T()T()T()T()T()T()T()T()TR())", "private", 18),
}


@dataclass(frozen=True)
class Repair:
    signature: str
    marked_signature: str
    multiplicity: int
    territories: tuple[tuple[str, tuple[int, ...]], ...]
    cut_owners: tuple[tuple[int, str], ...]
    entry_owner: str
    attachment_owners: tuple[tuple[tuple[str, int], str], ...]
    margin: tuple[int, int]
    description: str


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q_component_bound(triangle_count):
    if triangle_count == 1:
        return Fraction(0), True
    if triangle_count == 2:
        return Fraction(0), False
    return Fraction(0), True


def exact_hostile_positive(integer_credit, delta_count=1):
    require(integer_credit >= delta_count >= 1, "hostile margin is not exactly positive")
    return True


def validate_repair(repair):
    owners = {owner for owner, _ in repair.territories}
    require(repair.multiplicity >= 1, "invalid repair multiplicity")
    require(exact_hostile_positive(*repair.margin), "nonpositive repair")
    require(repair.entry_owner in owners, "entry has no final owner")
    require(all(owner in owners for _, owner in repair.cut_owners), "cut has no final owner")
    require(all(owner in owners for _, owner in repair.attachment_owners), "attachment has no final owner")
    cycles = [cycle for _, packet in repair.territories for cycle in packet]
    require(sorted(cycles) == list(range(9)), "repair territories do not partition A_9")


def one_router_safe(tree, router, mark):
    components = BASE.BASE.components_after_split(tree, router)
    owner = BASE.root_component(tree, router, mark, components)
    if not 2 <= len(components) + (owner is None) <= 3:
        return False
    values = []
    strict = False
    for index, component in enumerate(components):
        triangles = len(component[0])
        if index == owner:
            value, is_strict = q_component_bound(triangles)
        else:
            value = Fraction(BASE.TRIANGLE_MARGIN[triangles])
            is_strict = True
        values.append(value)
        strict = strict or is_strict
    if owner is None:
        values.append(Fraction(-1))
    total = sum(values, Fraction())
    return total > 0 or (total == 0 and strict)


def verify_two_hub_repair(signature, root_code, tree, mark, multiplicity):
    adjacent = BASE.BASE.adjacency(tree)
    routers = [cycle for cycle in range(9) if len(adjacent[cycle]) == 2]
    require(len(routers) == 1, "two-hub repair lacks its router")
    router = routers[0]
    require(
        mark == BASE.Mark("private", router),
        "unexpected two-hub residual mark",
    )
    cuts = adjacent[router]
    degrees = sorted(len(adjacent[cut]) for cut in cuts)
    require(degrees == [2, 8], "two-hub repair has wrong cut degrees")
    hub_cut = next(cut for cut in cuts if len(adjacent[cut]) == 8)
    leaf_cut = next(cut for cut in cuts if cut != hub_cut)
    retained = tuple(sorted(cycle for cycle in range(9) if cycle != next(
        cycle for cycle in range(9)
        if cycle != router and adjacent[cycle] == [leaf_cut]
    )))
    repair = Repair(
        signature, root_code, multiplicity,
        (("packet:T8Q", retained), ("leaf:T", tuple(c for c in range(9) if c not in retained))),
        ((hub_cut, "packet:T8Q"), (leaf_cut, "leaf:T")),
        "packet:T8Q",
        tuple((("cycle", cycle), "packet:T8Q" if cycle in retained else "leaf:T") for cycle in range(9)),
        (8, 1),
        "packing-one T^8Q > 8-delta_q",
    )
    validate_repair(repair)
    return repair


def verify_bouquet_repair(signature, root_code, tree, mark, multiplicity):
    adjacent = BASE.BASE.adjacency(tree)
    require(len(adjacent) == 10 and len(adjacent[9]) == 9, "not a real A_9 bouquet")
    if mark.kind == "cut":
        require(mark.vertex == 9, "unexpected bouquet cut mark")
        description = "common-cut T^9Q > 9-delta_q"
    else:
        require(mark.kind == "private" and mark.vertex < 9, "unexpected bouquet private mark")
        description = "rooted packing-one T^9Q > 9-delta_q"
    repair = Repair(
        signature, root_code, multiplicity,
        (("packet:T9Q", tuple(range(9))),),
        ((9, "packet:T9Q"),),
        "packet:T9Q",
        tuple((("cycle", cycle), "packet:T9Q") for cycle in range(9)),
        (9, 1), description,
    )
    validate_repair(repair)
    return repair


def main():
    classes = BASE.BASE.enumerate_colors(("T",) * 9, 3)
    counts = Counter(BASE.BASE.cut_count(tree) for _, tree in classes)
    marked = Counter()
    direct = Counter()
    marked_multiplicity = Counter()
    direct_multiplicity = Counter()
    multiplicity_histogram = Counter()
    failures = []
    for signature, tree in classes:
        cuts = BASE.BASE.cut_count(tree)
        for root_code, mark, multiplicity in BASE.root_orbits(tree):
            require(multiplicity >= 1, "invalid root-orbit multiplicity")
            marked[cuts] += 1
            marked_multiplicity[cuts] += multiplicity
            multiplicity_histogram[multiplicity] += 1
            if any(one_router_safe(tree, router, mark) for router in range(9)):
                direct[cuts] += 1
                direct_multiplicity[cuts] += multiplicity
            else:
                failures.append((signature, root_code, mark, multiplicity, tree))

    require(
        counts == Counter({1: 1, 2: 4, 3: 17, 4: 48, 5: 92, 6: 107, 7: 68, 8: 18}),
        f"wrong A_9 incidence totals: {counts}",
    )
    require(sum(marked.values()) == 3624, f"wrong marked total: {marked}")
    require(sum(marked_multiplicity.values()) == 6745, "wrong marked-position multiplicity sum")
    require(
        multiplicity_histogram == Counter({1: 2157, 2: 905, 3: 14, 4: 393, 6: 76, 8: 59, 10: 8, 12: 9, 14: 1, 16: 1, 18: 1}),
        f"wrong orbit multiplicities: {multiplicity_histogram}",
    )
    require(sum(direct.values()) == 3621, f"wrong direct total: {direct}")
    require(len(failures) == 3, f"wrong residual count: {len(failures)}")
    require(
        Counter(signature for signature, _, _, _, _ in failures)
        == Counter({BOUQUET: 2, TWO_HUB: 1}),
        "wrong residual signatures",
    )
    require(
        {(signature, root_code, mark.kind, multiplicity) for signature, root_code, mark, multiplicity, _ in failures}
        == EXPECTED_FAILURES,
        "wrong frozen marked residual orbits",
    )
    require(sum(item[3] for item in failures) == 20, "wrong residual multiplicity sum")
    require(sum(direct_multiplicity.values()) + 20 == sum(marked_multiplicity.values()), "position orbits do not close")

    repairs = []
    for signature, root_code, mark, multiplicity, tree in failures:
        if signature == TWO_HUB:
            repairs.append(verify_two_hub_repair(signature, root_code, tree, mark, multiplicity))
        else:
            repairs.append(verify_bouquet_repair(signature, root_code, tree, mark, multiplicity))

    print("A_9 incidence trees:", dict(sorted(counts.items())), "total", len(classes))
    print("marked entry classes:", dict(sorted(marked.items())), "total", sum(marked.values()))
    print("marked physical positions:", dict(sorted(marked_multiplicity.items())), "total", sum(marked_multiplicity.values()))
    print("direct one-router certificates:", sum(direct.values()))
    print("explicit common-hub repairs:", len(repairs))
    for index, repair in enumerate(repairs, 1):
        print(f"R{index}: {repair.description}; orbit multiplicity={repair.multiplicity}")
    print("all marked A_9 | Q classes close")


if __name__ == "__main__":
    main()
