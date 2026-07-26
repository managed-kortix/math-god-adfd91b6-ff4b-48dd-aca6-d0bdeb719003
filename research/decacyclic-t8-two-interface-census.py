#!/usr/bin/env python3
"""Exact marked two-interface certificate for an eight-triangle cluster."""

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


spec = spec_from_file_location("rank9_two_interface", HERE / "nonacyclic-t7-two-interface-census.py")
base = module_from_spec(spec)
require(spec.loader is not None, "cannot load marked-census dependency")
sys.modules[spec.name] = base
spec.loader.exec_module(base)


EXPECTED_ROW_DIGEST = "77468da6a473a52ece68d6e4319f78337feb17941e615e2a0ae65032f826cc86"
EXPECTED_RESIDUAL_DIGEST = "1f41279dad404a97627da24f1fa67e720f6a0d2ffc67b3c28bf1521ebeb11ca0"


@dataclass(frozen=True)
class RepairCertificate:
    signature: str
    operation: str
    routers: tuple[int, ...]
    splits: tuple[base.Split, ...]
    packets: tuple[tuple[str, tuple[int, ...], int, bool], ...]
    connector_owners: tuple[tuple[str, base.Position, str], ...]
    openings: tuple[tuple[str, int], ...]
    credit: int
    deficits: int


def split_at(row, router, active):
    adj = base.BASE.adjacency(row.tree)
    branches = base.component_cycle_sets(row.tree, frozenset(active), router)
    marks = base.marks_by_position(row.positions)
    owners = []
    for cut, cycles in branches:
        position = base.Position("cut", cut)
        if cycles or position in marks:
            owners.append((position, tuple(sorted(cycles))))
    for position in sorted(marks):
        if position.kind == "private" and position.vertex == router:
            owners.append((position, ()))
    require(len(owners) in (2, 3), "repair router does not expose two or three marked intervals")
    intervals = (2, 1) if len(owners) == 2 else (1, 1, 1)
    return base.Split(router, tuple(sorted(active)), tuple(owners), intervals)


def component_packets(row, removed):
    adj = base.BASE.adjacency(row.tree)
    retained = set(range(8)) - set(removed)
    packets = []
    while retained:
        start = min(retained)
        seen = {start}
        stack = [start]
        while stack:
            cycle = stack.pop()
            for cut in adj[cycle]:
                for neighbor in adj[cut]:
                    if neighbor in retained and neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
        retained -= seen
        common = set(adj[next(iter(seen))])
        for cycle in seen:
            common &= set(adj[cycle])
        hub = min(common) if common else -1
        packets.append((f"K{len(packets)}", tuple(sorted(seen)), hub, False))
    return tuple(packets)


def structural_repair(row):
    operation, credit, deficits = repair_kind(row, None)
    adj = base.BASE.adjacency(row.tree)
    cuts = len(adj) - 8
    routers = ()
    openings = ()
    packing = "packing-one" in operation
    if cuts == 2:
        routers = (next(cycle for cycle in range(8) if len(adj[cycle]) == 2),)
    elif operation.startswith("split the private-entry triangle"):
        routers = (next(position.vertex for position in row.positions if position.kind == "private"),)
    elif operation == "split once: A_7 + PP":
        routers = (row.positions[0].vertex,)
    elif operation == "split twice: A_6 + PA + PB":
        routers = tuple(sorted({position.vertex for position in row.positions}))
    elif operation.startswith("open PA"):
        openings = (("PA", -1),)

    remaining = tuple(range(8))
    splits = []
    for router in routers:
        splits.append(split_at(row, router, remaining))
        remaining = tuple(cycle for cycle in remaining if cycle != router)
    packets = list(component_packets(row, routers))
    if packing:
        candidates = [index for index, (_, cycles, hub, _) in enumerate(packets)
                      if hub >= 0 and len(cycles) >= 6]
        require(len(candidates) == 1, "packing-one repair does not identify one retained common-hub packet")
        packet_index = candidates[0]
        name, cycles, hub, _ = packets[packet_index]
        packets[packet_index] = (name, cycles, hub, True)

    packet_names = tuple(name for name, _, _, _ in packets)
    require(packet_names, "repair has no retained packet")
    connector_owners = []
    for label, position in zip(base.LABELS, row.positions):
        if openings and label == "A":
            owner = "opened-PA"
        else:
            incident = []
            for name, cycles, _, _ in packets:
                if position.kind == "private" and position.vertex in cycles:
                    incident.append(name)
                elif position.kind == "cut" and set(adj[position.vertex]) & set(cycles):
                    incident.append(name)
            owner = min(incident) if incident else f"P{label}"
        connector_owners.append((label, position, owner))
    return RepairCertificate(row.signature, operation, routers, tuple(splits), tuple(packets),
                             tuple(connector_owners), openings, credit, deficits)


def verify_structural_repair(row, certificate):
    require(certificate.signature == row.signature, "repair exact signature mismatch")
    require(base.marked_signature(row.tree, row.positions) == row.signature, "marked incidence signature is not canonical")
    adj = base.BASE.adjacency(row.tree)
    require(all(cost == -1 for _, cost in certificate.openings), "opening does not have exact tree cost -1")
    require(len({name for name, _ in certificate.openings}) == len(certificate.openings), "opening is repeated")
    removed = set(certificate.routers)
    require(len(removed) == len(certificate.routers), "router is repeated")

    previous_active = set(range(8))
    for split, router in zip(certificate.splits, certificate.routers):
        require(split.router == router and set(split.active) == previous_active, "router active set is not sequential")
        require(len(split.owners) == len(split.interval_sizes) and sum(split.interval_sizes) == 3,
                "router marks/intervals do not cover its triangle")
        require(sorted(split.interval_sizes) == ([1, 2] if len(split.owners) == 2 else [1, 1, 1]),
                "router interval lengths are invalid")
        require(len({position for position, _ in split.owners}) == len(split.owners), "router marks repeat")
        branches = [set(cycles) for _, cycles in split.owners]
        require(set().union(*branches) == previous_active - {router}, "router branches do not cover retained cycles")
        require(sum(map(len, branches)) == len(set().union(*branches)), "router branches overlap")
        previous_active.remove(router)

    retained = set(range(8)) - removed
    packet_cycles = [cycle for _, cycles, _, _ in certificate.packets for cycle in cycles]
    require(set(packet_cycles) == retained and len(packet_cycles) == len(set(packet_cycles)),
            "retained packets are not a partition")
    packet_of = {}
    for name, cycles, hub, packing_one in certificate.packets:
        require(cycles == tuple(sorted(cycles)) and cycles, f"packet {name} is empty or noncanonical")
        for cycle in cycles:
            packet_of[cycle] = name
        seen = {cycles[0]}
        stack = [cycles[0]]
        while stack:
            cycle = stack.pop()
            for cut in adj[cycle]:
                for neighbor in adj[cut]:
                    if neighbor in cycles and neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
        require(seen == set(cycles), f"packet {name} is disconnected")
        if hub >= 0:
            require(all(hub in adj[cycle] for cycle in cycles), f"packet {name} does not have its declared common hub")
        if packing_one:
            require(hub >= 0 and all(hub in adj[cycle] for cycle in cycles),
                    f"packet {name} packing-one claim lacks one common triangle hub")

    final_cut_owners = []
    for cut in range(8, len(adj)):
        owners = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        require(len(owners) <= 1, f"cut {cut} has competing final packet owners")
        require(owners or set(adj[cut]) & removed, f"cut {cut} has no final owner")
        final_cut_owners.append((cut, next(iter(owners)) if owners else "router"))
    require(tuple(label for label, _, _ in certificate.connector_owners) == base.LABELS,
            "connector ownership omits or reorders an interface")
    require(tuple(position for _, position, _ in certificate.connector_owners) == row.positions,
            "connector ownership does not match the marked entries")
    valid_owners = {name for name, _, _, _ in certificate.packets} | {"PA", "PB", "opened-PA"}
    require(all(owner in valid_owners for _, _, owner in certificate.connector_owners),
            "connector has no final packet/opening owner")
    if certificate.deficits:
        require(exact_positive(certificate.credit, certificate.deficits), "repair ledger is not positive")
    else:
        require(certificate.operation in {"split router: A_6 + T + PP", "split once: A_7 + PP"},
                "zero-deficit repair has no strict packet")
    return tuple(final_cut_owners)


def exact_positive(credit, deficits):
    left = credit + 2 * deficits
    return left > 0 and left * left > 5 * deficits * deficits


def repair_kind(row, plan):
    adj = base.BASE.adjacency(row.tree)
    cuts = len(adj) - len(row.tree.colors)
    if cuts == 2:
        router = next(cycle for cycle in range(8) if len(adj[cycle]) == 2)
        private = base.Position("private", router, 0)
        require(private in row.positions, "two-cut residual lacks its router-private demand")
        other = row.positions[1] if row.positions[0] == private else row.positions[0]
        hub_cut = max(adj[router], key=lambda cut: len(adj[cut]))
        leaf_cut = min(adj[router], key=lambda cut: len(adj[cut]))
        leaf_triangle = next(cycle for cycle in adj[leaf_cut] if cycle != router)
        if other == private:
            return "split router: A_6 + T + PP", 1, 0
        if other == base.Position("cut", leaf_cut):
            return "split router: A_6 + TP + P", 2, 2
        if other == base.Position("cut", hub_cut):
            return "split router: common-cut T^6P + T + P", 6, 2
        require(other.kind == "private", "unexpected two-cut residual demand")
        if other.vertex == leaf_triangle:
            return "split router: A_6 + TP + P", 2, 2
        require(hub_cut in adj[other.vertex], "private demand is not on a hub petal")
        return "split router: packing-one T^6P + T + P", 6, 2

    require(cuts == 1, "residual is neither the two-cut kernel nor the bouquet")
    first, second = row.positions
    if first.kind == second.kind == "cut":
        return "open PA; retain packing-one T^8+PB", 7, 1
    if {first.kind, second.kind} == {"cut", "private"}:
        return "split the private-entry triangle: P + common-cut T^7P", 7, 2
    if first == second:
        return "split once: A_7 + PP", 0, 0
    if first.vertex == second.vertex:
        return "open PA; retain packing-one T^7+PB", 6, 1
    return "split twice: A_6 + PA + PB", 1, 2


def main():
    rows, incidence_count, labelled_positions = base.enumerate_rows(8)
    plans, scores, states, routers, packets, residuals = base.classify(rows)
    for row in rows:
        base.verify_interval_realization(row, plans[row.signature])

    row_digest = sha256(("\n".join(row.signature for row in rows) + "\n").encode("ascii")).hexdigest()
    residual_digest = sha256(("\n".join(row.signature for row in residuals) + "\n").encode("ascii")).hexdigest()
    repairs = []
    ownership_certificates = []
    for row in residuals:
        operation, credit, deficits = repair_kind(row, plans[row.signature])
        if deficits:
            require(exact_positive(credit, deficits), (operation, credit, deficits))
        else:
            require(
                (credit > 0 and operation == "split router: A_6 + T + PP")
                or operation == "split once: A_7 + PP",
                "zero-deficit ledger lacks strict packet closure",
            )
        repairs.append((operation, credit, deficits))
        certificate = structural_repair(row)
        require((certificate.operation, certificate.credit, certificate.deficits) == repairs[-1],
                "structural repair and ledger classification disagree")
        owners = verify_structural_repair(row, certificate)
        ownership_certificates.append((certificate, owners))

    require(incidence_count == 126, incidence_count)
    require(labelled_positions == 36414, labelled_positions)
    require(len(rows) == 11689, len(rows))
    require(scores == Counter({5: 5176, 4: 4817, 3: 1378, 2: 283, 1: 20, 0: 15}), scores)
    require(routers == Counter({1: 10844, 2: 838, 0: 6, 3: 1}), routers)
    require(len(residuals) == len(repairs) == 15, len(residuals))
    require(len(ownership_certificates) == 15, "structural ownership certificate count changed")
    require(sum(len(base.BASE.adjacency(row.tree)) - 8 == 2 for row in residuals) == 9, "two-cut residual count changed")
    require(row_digest == EXPECTED_ROW_DIGEST, row_digest)
    require(residual_digest == EXPECTED_RESIDUAL_DIGEST, residual_digest)

    print("eight-triangle incidence trees:", incidence_count)
    print("labelled placements before automorphisms:", labelled_positions)
    print("canonical marked rows:", len(rows))
    print("ordinary router accepted:", len(rows) - len(residuals))
    print("residual repairs:", len(repairs), "of", len(residuals))
    print("best scores:", dict(sorted(scores.items())))
    print("router counts:", dict(sorted(routers.items())))
    print("canonical-row sha256:", row_digest)
    print("canonical-residual sha256:", residual_digest)
    for index, ((operation, credit, deficits), row, (certificate, owners)) in enumerate(
            zip(repairs, residuals, ownership_certificates), 1):
        margin = "strict >0" if not deficits else f">{credit}-{deficits}delta"
        print(f"R{index}: {operation}; {margin}; {row.signature}")
        print("  incidence:", row.tree.edges)
        print("  marks:", tuple(position.text() for position in row.positions))
        print("  routers/intervals:", tuple((step.router, step.interval_sizes, step.owners) for step in certificate.splits) or "none")
        print("  retained-packets:", certificate.packets, "openings:", certificate.openings or "none")
        print("  connectors:", certificate.connector_owners, "final-cut-owners:", owners)


if __name__ == "__main__":
    main()
