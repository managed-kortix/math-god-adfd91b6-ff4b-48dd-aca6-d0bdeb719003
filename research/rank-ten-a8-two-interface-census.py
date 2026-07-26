#!/usr/bin/env python3
"""Exact marked two-interface experiment for an eight-triangle cluster.

The two labelled marks range over shared cuts and actual private triangle
vertices and may coincide.  The router objective is an exact Fraction credit
minus exact private-interval charges.  Acceptance at score >= 1 is a
conservative rational surrogate for subtracting two pentagonal deficits.  This
is a finite interface census, not a theorem claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_nine_two_interface", HERE / "nonacyclic-t7-two-interface-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("rank-nine interface dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)
BASE.TRIANGLE_MARGIN[8] = Fraction(0)


@dataclass(frozen=True)
class ExactMargin:
    credit: Fraction
    deficits: int
    strict_zero: bool = False

    def text(self):
        if not self.deficits:
            return "> 0" if self.credit == 0 else f"> {self.credit}"
        suffix = "delta" if self.deficits == 1 else f"{self.deficits}delta"
        return f"> {self.credit}-{suffix}"

    def positive(self):
        if self.credit == 0:
            return self.deficits == 0 and self.strict_zero
        rational = self.credit + 2 * self.deficits
        return rational > 0 and rational * rational > 5 * self.deficits**2


@dataclass(frozen=True)
class Owner:
    positions: tuple
    cycles: tuple[int, ...]
    packet: str


@dataclass(frozen=True)
class RepairSplit:
    router: int
    active: tuple[int, ...]
    interval_sizes: tuple[int, ...]
    owners: tuple[Owner, ...]


@dataclass(frozen=True)
class RepairPacket:
    name: str
    kind: str
    cycles: tuple[int, ...]
    pentagons: tuple[str, ...]


@dataclass(frozen=True)
class ResidualRepair:
    code: str
    template: str
    terminal: str
    splits: tuple[RepairSplit, ...]
    packets: tuple[RepairPacket, ...]
    connector_owners: tuple[str, str]
    cut_owners: tuple[tuple[int, str], ...]
    margin: ExactMargin
    opened_pentagon: str = ""


def enumerate_rows():
    classes = BASE.BASE.enumerate_colors(("T",) * 8, 0)
    rows = {}
    labelled_positions = 0
    for incidence_signature, tree in classes:
        positions = BASE.position_universe(tree)
        labelled_positions += len(positions) ** 2
        local = {}
        for first in positions:
            for second in positions:
                pair = (first, second)
                signature = BASE.marked_signature(tree, pair)
                if signature in local:
                    old_pair, multiplicity = local[signature]
                    local[signature] = old_pair, multiplicity + 1
                else:
                    local[signature] = pair, 1
        for signature, (pair, multiplicity) in local.items():
            BASE.require(signature not in rows, f"duplicate canonical row: {signature}")
            rows[signature] = BASE.Row(
                signature, incidence_signature, tree, pair, multiplicity
            )
    return tuple(rows[key] for key in sorted(rows)), len(classes), labelled_positions


def exact_classify(rows):
    scores = Counter()
    routers = Counter()
    residuals = []
    plans = {}
    for row in rows:
        plan = BASE.best_plan(row)
        score = Fraction(plan.credit) - Fraction(plan.naked)
        BASE.require(score == plan.score, "router score is not exact")
        plans[row.signature] = plan
        scores[score] += 1
        routers[len(plan.routers)] += 1
        if score < 1:
            residuals.append(row)
    return plans, scores, routers, residuals


def residual_shapes(residuals):
    answer = Counter()
    for row in residuals:
        positions = tuple(
            sorted(
                (
                    position.kind,
                    len(BASE.BASE.adjacency(row.tree)[position.vertex])
                    if position.kind == "private"
                    else sum(
                        cycle < len(row.tree.colors)
                        for cycle in BASE.BASE.adjacency(row.tree)[position.vertex]
                    ),
                )
                for position in row.positions
            )
        )
        answer[(BASE.BASE.cut_count(row.tree), row.incidence_signature, positions)] += 1
    return answer


def residual_repairs(residuals):
    """Classify and materialize the fifteen finite replacement certificates."""
    BASE.require(len(residuals) == 15, "repair table requires fifteen residuals")
    repairs = []
    for index, row in enumerate(residuals, 1):
        all_cycles = tuple(range(8))
        if index <= 9:
            BASE.require(
                row.incidence_signature == "T(X(T())X(T()T()T()T()T()T()))",
                f"R{index} is not on the two-cut template",
            )
            big = (1, 3, 4, 5, 6, 7)
            small = (2,)
            big_cut = BASE.Position("cut", 8)
            small_cut = BASE.Position("cut", 9)
            private = BASE.Position("private", 0, 0)
            if index == 1:
                owners = (Owner((big_cut,), big, "A6"), Owner((small_cut,), small, "T"), Owner((private,), (), "PP"))
                packets = (RepairPacket("A6", "triangular", big, ()), RepairPacket("T", "triangular-strict", small, ()), RepairPacket("PP", "PP", (), ("PA", "PB")))
                connector_owners = ("PP", "PP")
                terminal, margin = "PP", ExactMargin(Fraction(1), 0)
            elif index in (2, 6):
                private_p = "PA" if index == 2 else "PB"
                small_p = "PB" if index == 2 else "PA"
                owners = (Owner((big_cut,), big, "A6"), Owner((small_cut,), small, "TP"), Owner((private,), (), private_p))
                packets = (RepairPacket("A6", "triangular", big, ()), RepairPacket("TP", "TP", small, (small_p,)), RepairPacket(private_p, "P", (), (private_p,)))
                connector_owners = (private_p, "TP") if index == 2 else ("TP", private_p)
                terminal, margin = "packetization", ExactMargin(Fraction(2), 2)
            elif index in (3, 7):
                private_p = "PA" if index == 3 else "PB"
                big_p = "PB" if index == 3 else "PA"
                owners = (Owner((big_cut,), big, "T6P"), Owner((small_cut,), small, "T"), Owner((private,), (), private_p))
                packets = (RepairPacket("T6P", "common-cut", big, (big_p,)), RepairPacket("T", "triangular-strict", small, ()), RepairPacket(private_p, "P", (), (private_p,)))
                connector_owners = (private_p, "T6P") if index == 3 else ("T6P", private_p)
                terminal, margin = "common-cut", ExactMargin(Fraction(6), 2)
            elif index in (4, 8):
                private_p = "PA" if index == 4 else "PB"
                small_p = "PB" if index == 4 else "PA"
                owners = (Owner((big_cut,), big, "A6"), Owner((small_cut,), small, "TP"), Owner((private,), (), private_p))
                packets = (RepairPacket("A6", "triangular", big, ()), RepairPacket("TP", "TP", small, (small_p,)), RepairPacket(private_p, "P", (), (private_p,)))
                connector_owners = (private_p, "TP") if index == 4 else ("TP", private_p)
                terminal, margin = "packetization", ExactMargin(Fraction(2), 2)
            else:
                BASE.require(index in (5, 9), f"unexpected two-cut residual R{index}")
                private_p = "PA" if index == 5 else "PB"
                big_p = "PB" if index == 5 else "PA"
                owners = (Owner((big_cut,), big, "packing-one-T6P"), Owner((small_cut,), small, "T"), Owner((private,), (), private_p))
                packets = (RepairPacket("packing-one-T6P", "packing-one", big, (big_p,)), RepairPacket("T", "triangular-strict", small, ()), RepairPacket(private_p, "P", (), (private_p,)))
                connector_owners = (private_p, "packing-one-T6P") if index == 5 else ("packing-one-T6P", private_p)
                terminal, margin = "packing-one", ExactMargin(Fraction(6), 2)
            repairs.append(ResidualRepair(
                f"R{index}", "two-cut", terminal,
                (RepairSplit(0, all_cycles, (1, 1, 1), owners),), packets,
                connector_owners, ((8, owners[0].packet), (9, owners[1].packet)), margin,
            ))
            continue

        BASE.require(
            row.incidence_signature == "X(T()T()T()T()T()T()T()T())",
            f"R{index} is not on the bouquet template",
        )
        hub = BASE.Position("cut", 8)
        if index == 10:
            repairs.append(ResidualRepair(
                "R10", "bouquet", "opening", (),
                (RepairPacket("opened-PA", "opened-pentagon", (), ("PA",)), RepairPacket("packing-one-A8P", "packing-one", all_cycles, ("PB",))),
                ("opened-PA", "packing-one-A8P"), ((8, "packing-one-A8P"),),
                ExactMargin(Fraction(7), 1), "PA",
            ))
        elif index in (11, 12):
            router = row.positions[1].vertex if index == 11 else row.positions[0].vertex
            private_position = row.positions[1] if index == 11 else row.positions[0]
            remainder = tuple(cycle for cycle in all_cycles if cycle != router)
            private_p = "PB" if index == 11 else "PA"
            common_p = "PA" if index == 11 else "PB"
            repairs.append(ResidualRepair(
                f"R{index}", "bouquet", "common-cut",
                (RepairSplit(router, all_cycles, (1, 2), (Owner((hub,), remainder, "T7P"), Owner((private_position,), (), private_p))),),
                (RepairPacket("T7P", "common-cut", remainder, (common_p,)), RepairPacket(private_p, "P", (), (private_p,))),
                (("T7P", private_p) if index == 11 else (private_p, "T7P")), ((8, "T7P"),),
                ExactMargin(Fraction(7), 2),
            ))
        elif index == 13:
            router = row.positions[0].vertex
            remainder = tuple(cycle for cycle in all_cycles if cycle != router)
            private_positions = tuple(dict.fromkeys(row.positions))
            repairs.append(ResidualRepair(
                f"R{index}", "bouquet", "PP",
                (RepairSplit(router, all_cycles, (1, 2), (Owner((hub,), remainder, "A7"), Owner(private_positions, (), "PP"))),),
                (RepairPacket("A7", "triangular-strict", remainder, ()), RepairPacket("PP", "PP", (), ("PA", "PB"))),
                ("PP", "PP"), ((8, "A7"),), ExactMargin(Fraction(0), 0, True),
            ))
        else:
            BASE.require(index in (14, 15), f"unexpected bouquet residual R{index}")
            repairs.append(ResidualRepair(
                f"R{index}", "bouquet", "opening", (),
                (RepairPacket("opened-PA", "opened-pentagon", (), ("PA",)), RepairPacket("packing-one-A8P", "packing-one", all_cycles, ("PB",))),
                ("opened-PA", "packing-one-A8P"), ((8, "packing-one-A8P"),),
                ExactMargin(Fraction(7), 1), "PA",
            ))
    return tuple(repairs)


def verify_residual_repair(row, repair):
    packet_names = {packet.name for packet in repair.packets}
    packet_by_name = {packet.name: packet for packet in repair.packets}
    BASE.require(len(packet_names) == len(repair.packets), f"{repair.code}: duplicate packet name")
    BASE.require(set(repair.connector_owners) <= packet_names, f"{repair.code}: connector has no packet owner")
    assigned_pentagons = tuple(pentagon for packet in repair.packets for pentagon in packet.pentagons)
    BASE.require(Counter(assigned_pentagons) == Counter(("PA", "PB")), f"{repair.code}: pentagons are not assigned exactly once")
    for pentagon, packet_name in zip(("PA", "PB"), repair.connector_owners):
        BASE.require(pentagon in packet_by_name[packet_name].pentagons, f"{repair.code}: connector owner omits {pentagon}")
    BASE.require(sum(len(packet.cycles) for packet in repair.packets) == len({cycle for packet in repair.packets for cycle in packet.cycles}), f"{repair.code}: packet cycles overlap")

    adj = BASE.BASE.adjacency(row.tree)
    removed = set()
    previous_branches = []
    for split in repair.splits:
        BASE.require(split.router in split.active and split.router not in removed, f"{repair.code}: inactive or repeated router")
        if previous_branches:
            BASE.require(set(split.active) in previous_branches, f"{repair.code}: nonnested second split")
        BASE.require(len(split.owners) in (2, 3), f"{repair.code}: invalid owner count")
        BASE.require(sorted(split.interval_sizes) == ([1, 2] if len(split.owners) == 2 else [1, 1, 1]), f"{repair.code}: invalid proper triangle intervals")
        branch_sets = [set(owner.cycles) for owner in split.owners]
        BASE.require(set().union(*branch_sets) == set(split.active) - {split.router}, f"{repair.code}: split branches are not exhaustive")
        BASE.require(sum(map(len, branch_sets)) == len(set().union(*branch_sets)), f"{repair.code}: split branches overlap")
        BASE.require(all(owner.packet in packet_names for owner in split.owners), f"{repair.code}: split owner has no packet")
        positions = tuple(position for owner in split.owners for position in owner.positions)
        BASE.require(len(positions) == len(set(positions)), f"{repair.code}: split position has two owners")
        for position in positions:
            if position.kind == "cut":
                BASE.require(position.vertex in adj[split.router], f"{repair.code}: cut owner is not incident with router")
            else:
                BASE.require(position.vertex == split.router, f"{repair.code}: private owner belongs to another router")
        removed.add(split.router)
        previous_branches = branch_sets

    retained = {cycle for packet in repair.packets for cycle in packet.cycles}
    BASE.require(retained == set(range(8)) - removed, f"{repair.code}: packets do not cover retained triangles")
    BASE.require(dict(repair.cut_owners).keys() == ({8} if repair.template == "bouquet" else {8, 9}), f"{repair.code}: cut-owner domain mismatch")
    BASE.require(set(dict(repair.cut_owners).values()) <= packet_names, f"{repair.code}: cut has no packet owner")
    split_position_owner = {
        position: owner.packet
        for split in repair.splits
        for owner in split.owners
        for position in owner.positions
    }
    for position, packet_name in zip(row.positions, repair.connector_owners):
        packet = packet_by_name[packet_name]
        entry_is_owned = packet.kind == "opened-pentagon"
        if position.kind == "private":
            entry_is_owned |= position.vertex in packet.cycles
        else:
            entry_is_owned |= any(cycle in packet.cycles for cycle in adj[position.vertex])
        entry_is_owned |= split_position_owner.get(position) == packet_name
        BASE.require(entry_is_owned, f"{repair.code}: marked entry is not owned by its connector packet")
    for cut, packet_name in repair.cut_owners:
        incident_retained = {cycle for cycle in adj[cut] if cycle in retained}
        BASE.require(incident_retained <= set(packet_by_name[packet_name].cycles), f"{repair.code}: retained cut cycles have another owner")
    BASE.require(repair.margin.positive(), f"{repair.code}: exact margin is not positive")

    kinds = {packet.kind for packet in repair.packets}
    if repair.terminal == "packetization":
        BASE.require("TP" in kinds and repair.margin == ExactMargin(Fraction(2), 2), f"{repair.code}: direct packet ledger mismatch")
    elif repair.terminal in ("common-cut", "packing-one"):
        expected = ExactMargin(Fraction(7), 2) if repair.template == "bouquet" else ExactMargin(Fraction(6), 2)
        BASE.require(repair.margin == expected, f"{repair.code}: mixed packet ledger mismatch")
    elif repair.terminal == "opening":
        BASE.require(repair.opened_pentagon == "PA" and repair.margin == ExactMargin(Fraction(7), 1), f"{repair.code}: opening ledger mismatch")
    elif repair.terminal == "PP":
        BASE.require("PP" in kinds and (repair.margin.strict_zero or repair.margin == ExactMargin(Fraction(1), 0)), f"{repair.code}: PP strict terminal mismatch")
    else:
        BASE.require(False, f"{repair.code}: unknown terminal {repair.terminal}")


def verify_residual_repairs(residuals):
    repairs = residual_repairs(residuals)
    for row, repair in zip(residuals, repairs):
        verify_residual_repair(row, repair)
    return repairs


def compact(counter):
    return dict(sorted(counter.items(), key=lambda item: repr(item[0])))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-residuals", action="store_true")
    args = parser.parse_args()

    rows, incidence_count, labelled_positions = enumerate_rows()
    plans, scores, routers, residuals = exact_classify(rows)
    for row in rows:
        BASE.verify_interval_realization(row, plans[row.signature])
    repairs = verify_residual_repairs(residuals)

    row_digest = sha256(
        ("\n".join(row.signature for row in rows) + "\n").encode("ascii")
    ).hexdigest()
    residual_digest = sha256(
        ("\n".join(row.signature for row in residuals) + "\n").encode("ascii")
    ).hexdigest()
    print("eight-triangle incidence trees:", incidence_count)
    print("labelled interface placements before automorphisms:", labelled_positions)
    print("canonical marked two-interface rows:", len(rows))
    print("accepting rows at exact Fraction score >= 1:", len(rows) - len(residuals))
    print("canonical residuals:", len(residuals))
    print("explicit residual repairs:", len(repairs))
    print("repair terminals:", compact(Counter(repair.terminal for repair in repairs)))
    print("exact repaired margins:", compact(Counter(repair.margin.text() for repair in repairs)))
    print("best exact Fraction scores:", compact(scores))
    print("split-router counts:", compact(routers))
    print("residual shape templates:", compact(residual_shapes(residuals)))
    print("canonical-row sha256:", row_digest)
    print("canonical-residual sha256:", residual_digest)

    BASE.require(sum(scores.values()) == len(rows), "score census is incomplete")
    BASE.require(sum(routers.values()) == len(rows), "router census is incomplete")
    BASE.require(incidence_count == 126, "eight-triangle incidence count changed")
    BASE.require(labelled_positions == 36414, "labelled placement count changed")
    BASE.require(len(rows) == 11689, "marked canonical count changed")
    BASE.require(len(residuals) == 15, "marked residual count changed")
    BASE.require(len(repairs) == 15, "marked repairs are incomplete")
    BASE.require(Counter(repair.terminal for repair in repairs) == Counter({"packetization": 4, "common-cut": 4, "packing-one": 2, "opening": 3, "PP": 2}), "repair profile changed")
    BASE.require(
        scores == Counter({Fraction(0): 15, Fraction(1): 20, Fraction(2): 283, Fraction(3): 1378, Fraction(4): 4817, Fraction(5): 5176}),
        "exact score distribution changed",
    )
    BASE.require(
        routers == Counter({0: 6, 1: 10844, 2: 838, 3: 1}),
        "router distribution changed",
    )
    BASE.require(row_digest == "77468da6a473a52ece68d6e4319f78337feb17941e615e2a0ae65032f826cc86", "canonical row digest changed")
    BASE.require(residual_digest == "1f41279dad404a97627da24f1fa67e720f6a0d2ffc67b3c28bf1521ebeb11ca0", "canonical residual digest changed")
    BASE.require(
        all(plans[row.signature].score < 1 for row in residuals),
        "residual set contains an accepting score",
    )

    if args.list_residuals:
        for row, repair in zip(residuals, repairs):
            print(BASE.row_description(int(repair.code[1:]), row, plans[row.signature]))
            print(f"  canonical-template={repair.template} terminal={repair.terminal}")
            for split in repair.splits:
                owners = ", ".join(
                    f"{'/'.join(position.text() for position in owner.positions)}->{owner.packet}:{owner.cycles or 'connector'}"
                    for owner in split.owners
                )
                print(f"  repair-split=T{split.router} active={split.active} intervals={split.interval_sizes} owners={owners}")
            packet_text = tuple((packet.name, packet.kind, packet.cycles, packet.pentagons) for packet in repair.packets)
            print(f"  repair-packets={packet_text}")
            print(f"  connector-owners=PA->{repair.connector_owners[0]}, PB->{repair.connector_owners[1]}")
            print(f"  cut-owners={repair.cut_owners}")
            print(f"  exact-margin={repair.margin.text()}")


if __name__ == "__main__":
    main()
