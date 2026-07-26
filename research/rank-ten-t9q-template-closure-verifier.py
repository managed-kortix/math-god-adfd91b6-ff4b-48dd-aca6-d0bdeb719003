#!/usr/bin/env python3
"""Exact audit of all disconnected and fully shared rank-ten T^9Q templates."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load verifier dependency {filename}")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


A9 = load_module("rank_ten_a9_for_t9q_audit", "rank-ten-a9-one-interface-census.py")
SHARED = load_module(
    "rank_ten_shared_for_t9q_audit", "rank-ten-fully-shared-incidence-census.py"
)
BASE = SHARED.BASE


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


EXPECTED_SHARED_SIGNATURES = (
    "X(Q()T()T()T()T()T()T()T()T()T())",
    "T(X(Q())X(T()T()T()T()T()T()T()T()))",
    "T(X(Q())X(T())X(T()T()T()T()T()T()T()))",
)


@dataclass(frozen=True)
class SplitOwner:
    port: int
    interval_size: int
    cycles: tuple[int, ...]
    cuts: tuple[int, ...]
    bound: object


@dataclass(frozen=True)
class OrdinarySplit:
    sacrificed: int
    color: str
    minimum_cycle_length: int
    extensible: bool
    slack_owner: int | None
    owners: tuple[SplitOwner, ...]
    cycle_owners: tuple[tuple[int, int], ...]
    cut_owners: tuple[tuple[int, int], ...]
    total: Fraction
    strict: bool


def digest(signatures):
    return sha256(("\n".join(signatures) + "\n").encode("ascii")).hexdigest()


def audit_disconnected():
    rows, incidence_count, placements = A9.enumerate_rows()
    scores = Counter()
    routers = Counter()
    residuals = []
    repairs = []
    for row in rows:
        plan = A9.BASE.best_plan(row)
        scores[plan.credit] += 1
        routers[len(plan.routers)] += 1
        if plan.credit >= 1:
            A9.verify_owner(row, plan)
        else:
            residuals.append(row)
            repair = A9.repair_residual(row, plan, f"R{len(residuals)}")
            A9.verify_residual_certificate(row, repair)
            repairs.append(repair)

    repair_types = Counter(item.terminal for item in repairs)
    row_digest = digest(row.signature for row in rows)
    residual_digest = digest(row.signature for row in residuals)
    require(incidence_count == 355, "A_9 incidence count changed")
    require(placements == 6745, "A_9 marked placement count changed")
    require(len(rows) == 3624, "A_9 canonical marked count changed")
    require(len(residuals) == 6, "A_9 residual count changed")
    require(
        scores == Counter({0: 6, 1: 4, 2: 28, 3: 171, 4: 879, 5: 1548, 6: 988}),
        "A_9 exact credit distribution changed",
    )
    require(
        routers == Counter({0: 6, 1: 3062, 2: 551, 3: 5}),
        "A_9 router distribution changed",
    )
    require(
        repair_types
        == Counter(
            {
                "packing-one-A9Q": 2,
                "leaf-TQ+A8": 1,
                "open-leaf-T+packing-one-A8Q": 3,
            }
        ),
        "A_9 repair templates changed",
    )
    require(
        row_digest == "8ecf4f9f27f2f8bf9c41e85576b398fc7b9f85211386ee9e8c19413e675a0ad7",
        "A_9 canonical-row digest changed",
    )
    require(
        residual_digest == "071cc2cbfc800a95b7128043b654f87aecf6b490542deaac89ca33293684c2f1",
        "A_9 residual digest changed",
    )
    return {
        "incidences": incidence_count,
        "placements": placements,
        "rows": len(rows),
        "router": len(rows) - len(residuals),
        "repairs": len(residuals),
        "repair_types": dict(sorted(repair_types.items())),
        "row_digest": row_digest,
        "residual_digest": residual_digest,
    }


def common_cut(tree, cycles):
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    return tuple(
        cut
        for cut in range(cycle_count, len(adj))
        if set(cycles) <= set(adj[cut])
    )


def validate_incidence(tree, q_capacity):
    adj = BASE.adjacency(tree)
    require(len(tree.edges) == len(adj) - 1, "incidence representative is not a tree")
    require(all(len(adj[cut]) >= 2 for cut in range(10, len(adj))),
            "incidence representative has a unary cut")
    require(all(1 <= len(adj[cycle]) <= (3 if color == "T" else q_capacity)
                for cycle, color in enumerate(tree.colors)),
            "incidence representative violates cycle capacity")


def materialize_split(tree, sacrificed, certificate, cycle_length, extensible=False):
    components = BASE.components_after_split(tree, sacrificed)
    require(len(components) >= 2, "accepted shared split has fewer than two parts")
    cycle_sets = [set(component[0]) for component in components]
    require(
        set().union(*cycle_sets) == set(range(10)) - {sacrificed},
        "accepted shared split misses a cycle",
    )
    require(sum(map(len, cycle_sets)) == 9, "accepted shared split overlaps")
    adj = BASE.adjacency(tree)
    ports = tuple(adj[sacrificed])
    require(len(ports) == len(components), "split ports and components disagree")
    require(2 <= len(ports) <= cycle_length, "split cycle has illegal occupied ports")
    interval_sizes = (1,) * (len(ports) - 1) + (cycle_length - len(ports) + 1,)
    require(all(size >= 1 for size in interval_sizes) and sum(interval_sizes) == cycle_length,
            "split intervals are not a legal cyclic partition")
    if tree.colors[sacrificed] == "T":
        require(sorted(interval_sizes) == ([1, 2] if len(ports) == 2 else [1, 1, 1]),
                "triangle split intervals are illegal")

    profiles, bounds, total = certificate
    require(tuple(BASE.component_profile(tree, item) for item in components) == profiles,
            "materialized split profiles disagree with accepted certificate")
    strict = any(bound.strict for bound in bounds)
    require(total == sum((bound.value for bound in bounds), Fraction(0)),
            "ordinary split ledger is not exact")
    require(total > 0 or (total == 0 and strict), "ordinary split is not strict positive")

    cycle_owner = {}
    cut_owner = {}
    owners = []
    for index, (port, interval_size, component, bound) in enumerate(
        zip(ports, interval_sizes, components, bounds)
    ):
        cycles = tuple(component[0])
        owned_cuts = tuple(
            cut for cut in range(10, len(adj))
            if any(cycle in cycles for cycle in adj[cut])
        )
        require(port in owned_cuts, "split port has no final component owner")
        for cycle in cycles:
            require(cycle not in cycle_owner, "retained cycle has multiple final owners")
            cycle_owner[cycle] = index
        for cut in owned_cuts:
            require(cut not in cut_owner or cut_owner[cut] == index,
                    "retained shared cut has multiple final owners")
            cut_owner[cut] = index
        owners.append(SplitOwner(port, interval_size, cycles, owned_cuts, bound))
    require(set(cycle_owner) == set(range(10)) - {sacrificed},
            "ordinary split lacks a final owner for a retained cycle")
    require(set(cut_owner) == set(range(10, len(adj))),
            "ordinary split lacks a final owner for a shared cut")
    return OrdinarySplit(
        sacrificed, tree.colors[sacrificed], cycle_length, extensible,
        len(owners) - 1 if extensible else None, tuple(owners),
        tuple(sorted(cycle_owner.items())), tuple(sorted(cut_owner.items())),
        total, strict,
    )


def verify_shared_exception(tree, index):
    adj = BASE.adjacency(tree)
    q = tree.colors.index("Q")
    triangles = set(range(10)) - {q}
    if index == 0:
        require(len(common_cut(tree, range(10))) == 1, "Q1 is not common-cut")
        return "common-cut", Fraction(9)
    if index == 1:
        hubs = common_cut(tree, triangles)
        require(len(hubs) == 1, "Q2 triangles do not have packing one")
        require(q not in adj[hubs[0]], "Q2 hostile cycle meets the triangle hub")
        return "packing-one", Fraction(9)

    candidates = []
    for leaf in triangles:
        if len(adj[leaf]) != 1:
            continue
        hubs = common_cut(tree, triangles - {leaf})
        if len(hubs) == 1:
            candidates.append((leaf, hubs[0]))
    require(len(candidates) == 1, "Q3 lacks a unique leaf-opening certificate")
    leaf, hub = candidates[0]
    require(q not in adj[hub], "Q3 hostile cycle meets the retained hub")
    routers = set(adj[hub]) & set(adj[adj[leaf][0]])
    require(len(routers) == 1, "Q3 lacks a unique saturated router")
    router = next(iter(routers))
    require(router in triangles and len(adj[router]) == 3, "Q3 router is not saturated")
    return "leaf-open+packing-one", Fraction(7)


def audit_fully_shared():
    closures = {}
    totals = {}
    for label, capacity, expected_label in (
        ("q=5", 5, "q=5"),
        ("q>=9", 9, "q=9"),
    ):
        classes = dict(
            BASE.enumerate_colors(tuple(sorted(("T",) * 9 + ("Q",))), capacity)
        )
        result = BASE.census(
            ("T",) * 9 + ("Q",),
            capacity,
            lambda tree, component: SHARED.tq_bound(label, tree, component),
        )
        require(
            result[0] == Counter(SHARED.EXPECTED_TQ[expected_label]),
            f"{label} shared universe changed",
        )
        unresolved = []
        materialized = []
        for signature, tree in classes.items():
            validate_incidence(tree, capacity)
            require(BASE.signature(tree) == signature,
                    "canonical incidence signature disagrees with representative")
            accepted = False
            for cycle in range(10):
                certificate = BASE.split_certificate(
                    tree,
                    cycle,
                    lambda candidate, component: SHARED.tq_bound(
                        label, candidate, component
                    ),
                )
                if certificate is not None:
                    length = 3 if tree.colors[cycle] == "T" else capacity
                    split = materialize_split(
                        tree, cycle, certificate, length,
                        extensible=tree.colors[cycle] == "Q" and label == "q>=9",
                    )
                    require(split.color != "Q" or split.minimum_cycle_length == capacity,
                            "Q split was not materialized at the audited capacity")
                    require(split.color != "Q" or label != "q>=9" or
                            split.slack_owner is not None,
                            "unbounded Q split has no owner for excess interval vertices")
                    materialized.append(split)
                    accepted = True
            if not accepted:
                unresolved.append(signature)
        require(
            tuple(sorted(unresolved)) == tuple(sorted(EXPECTED_SHARED_SIGNATURES)),
            f"{label} exception signatures changed",
        )
        for index, signature in enumerate(EXPECTED_SHARED_SIGNATURES):
            closures[(label, index + 1)] = verify_shared_exception(
                classes[signature], index
            )
        totals[label] = len(classes)
        require(materialized, f"{label} has no materialized ordinary splits")
    require(
        all(margin >= 7 for _, margin in closures.values()),
        "hostile shared replacement has insufficient integer margin",
    )
    return totals, closures


def main():
    disconnected = audit_disconnected()
    totals, closures = audit_fully_shared()
    print("disconnected A_9|Q:", disconnected)
    print("fully-shared hostile universes:", totals)
    print("fully-shared exception closures:", closures)
    print("exact T^9Q closure: disconnected 3624=3618+6; shared exceptions 3/3")


if __name__ == "__main__":
    main()
