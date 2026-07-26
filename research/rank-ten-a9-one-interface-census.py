#!/usr/bin/env python3
"""Exact marked one-interface census for disconnected rank-ten A_9 | Q.

The mark ranges over every shared cut and actual private triangle vertex.  A
private router interval keeps its connector and Q, so it is not charged as a
naked tree.  The uniform hostile ledger accepts triangular credit at least one;
the six remaining marked rows are closed by packing one or one leaf-triangle
opening.
"""

from __future__ import annotations

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
    raise RuntimeError("router dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)
BASE.TRIANGLE_MARGIN[8] = 0
BASE.TRIANGLE_MARGIN[9] = 0


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class ExactLedger:
    credit: Fraction
    hostile_deficits: int
    tree_costs: int
    strict: bool

    def positive(self):
        # Every hostile deficit delta_q is strictly less than one.
        floor = self.credit - self.hostile_deficits - self.tree_costs
        return floor >= 0 and (floor > 0 or self.strict)


@dataclass(frozen=True)
class ResidualPacket:
    name: str
    kind: str
    cycles: tuple[int, ...]
    contains_q: bool
    hypothesis: str
    strict: bool


@dataclass(frozen=True)
class OpeningCertificate:
    triangle: int
    retained_cut: int
    opened_position: object
    interval_sizes: tuple[int, ...]
    interval_owners: tuple[str, ...]


@dataclass(frozen=True)
class ResidualCertificate:
    code: str
    terminal: str
    packets: tuple[ResidualPacket, ...]
    opening: OpeningCertificate | None
    cut_owners: tuple[tuple[int, str], ...]
    root_owner: str
    q_owner: str
    attachment_owner: str
    ledger: ExactLedger


def enumerate_rows():
    classes = BASE.BASE.enumerate_colors(("T",) * 9, 0)
    rows = {}
    placements = 0
    for incidence_signature, tree in classes:
        positions = BASE.position_universe(tree)
        placements += len(positions)
        for position in positions:
            # Duplicate labels encode one geometric mark while reusing the
            # complete center-rooted marked-tree canonicalizer.
            pair = (position, position)
            signature = BASE.marked_signature(tree, pair)
            rows.setdefault(
                signature,
                BASE.Row(signature, incidence_signature, tree, pair, 1),
            )
    return tuple(rows[key] for key in sorted(rows)), len(classes), placements


def verify_owner(row, plan):
    BASE.verify_interval_realization(row, plan)
    position = row.positions[0]
    removed = set(plan.routers)
    realized = {
        marked
        for step in plan.steps
        for marked, _ in step.owners
    }
    if position.kind == "private" and position.vertex in removed:
        require(position in realized, "private Q connector has no router interval")
    elif position.kind == "private":
        require(
            any(position.vertex in packet for packet in plan.packet_cycles),
            "private Q connector has no retained packet owner",
        )
    else:
        require(
            position in realized
            or any(
                cycle in packet
                for packet in plan.packet_cycles
                for cycle in BASE.BASE.adjacency(row.tree)[position.vertex]
            ),
            "cut Q connector has no owner",
        )


def repair_residual(row, plan, code="R?"):
    verify_owner(row, plan)
    tree = row.tree
    adj = BASE.BASE.adjacency(tree)
    cuts = BASE.BASE.cut_count(tree)
    mark = row.positions[0]
    require(plan.credit == 0, "one-interface residual unexpectedly has credit")
    if cuts == 1:
        hub = len(tree.colors)
        require(all(hub in adj[cycle] for cycle in range(9)), "bouquet has no common hub")
        return ResidualCertificate(
            code, "packing-one-A9Q",
            (ResidualPacket("A9Q", "packing-one", tuple(range(9)), True,
                            "all nine triangles meet the common cut", True),),
            None, ((hub, "A9Q"),), "A9Q", "A9Q", "A9Q",
            ExactLedger(Fraction(9), 1, 0, True),
        )

    require(cuts == 2, "unknown one-interface residual shape")
    router = next(cycle for cycle in range(9) if len(adj[cycle]) == 2)
    leaf_cut = next(cut for cut in adj[router] if len(adj[cut]) == 2)
    leaf = next(cycle for cycle in adj[leaf_cut] if cycle != router)
    hub = next(cut for cut in adj[router] if cut != leaf_cut)
    require(
        sum(hub in adj[cycle] for cycle in range(9)) == 8,
        "two-cut residual has no eight-triangle hub",
    )
    remainder = tuple(cycle for cycle in range(9) if cycle != leaf)
    if mark.kind == "private" and mark.vertex == leaf:
        return ResidualCertificate(
            code, "leaf-TQ+A8",
            (
                ResidualPacket("TQ", "lower-rank", (leaf,), True,
                               "the marked private interval retains T and Q", True),
                ResidualPacket("A8", "common-cut", remainder, False,
                               "the eight remainder triangles meet the hub", True),
            ),
            OpeningCertificate(leaf, leaf_cut, mark, (1, 2), ("TQ", "A8")),
            ((hub, "A8"), (leaf_cut, "A8")), "TQ", "TQ", "TQ",
            ExactLedger(Fraction(0), 0, 0, True),
        )
    private_slots = 3 - len(adj[leaf])
    require(private_slots >= 1, "opened leaf has no private root")
    opened = BASE.Position("private", leaf, 0)
    return ResidualCertificate(
        code, "open-leaf-T+packing-one-A8Q",
        (
            ResidualPacket("opened-tree", "opened-tree", (), False,
                           "one nonempty private triangle interval", False),
            ResidualPacket("A8Q", "packing-one", remainder, True,
                           "the eight retained triangles meet the hub", True),
        ),
        OpeningCertificate(leaf, leaf_cut, opened, (1, 2),
                           ("opened-tree", "A8Q")),
        ((hub, "A8Q"), (leaf_cut, "A8Q")), "opened-tree", "A8Q", "A8Q",
        ExactLedger(Fraction(8), 1, 1, True),
    )


def verify_residual_certificate(row, certificate):
    tree = row.tree
    adj = BASE.BASE.adjacency(tree)
    cuts = tuple(range(9, len(adj)))
    packets = {packet.name: packet for packet in certificate.packets}
    require(len(packets) == len(certificate.packets), f"{certificate.code}: duplicate packet")
    require({certificate.root_owner, certificate.q_owner,
             certificate.attachment_owner} <= set(packets),
            f"{certificate.code}: root/Q/attachment owner is missing")
    require(sum(packet.contains_q for packet in certificate.packets) == 1,
            f"{certificate.code}: Q is not assigned exactly once")
    require(all(packet.hypothesis for packet in certificate.packets),
            f"{certificate.code}: packet hypothesis is missing")
    require(certificate.ledger.strict == any(packet.strict for packet in certificate.packets),
            f"{certificate.code}: packet and ledger strictness disagree")
    require(packets[certificate.q_owner].contains_q,
            f"{certificate.code}: declared Q owner omits Q")
    require(certificate.q_owner == certificate.attachment_owner,
            f"{certificate.code}: joining attachment is separated from Q")
    retained = [cycle for packet in certificate.packets for cycle in packet.cycles]
    opened_cycles = (
        {certificate.opening.triangle}
        if certificate.opening is not None
        and any(packet.kind == "opened-tree" for packet in certificate.packets)
        else set()
    )
    require(Counter(retained) == Counter(set(range(9)) - opened_cycles),
            f"{certificate.code}: triangle packet ledger is not exact")
    cut_owner = dict(certificate.cut_owners)
    require(len(cut_owner) == len(certificate.cut_owners) and set(cut_owner) == set(cuts),
            f"{certificate.code}: cut-owner ledger is not exact")
    require(set(cut_owner.values()) <= set(packets),
            f"{certificate.code}: cut owner has no packet")
    mark = row.positions[0]
    attachment_packet = packets[certificate.attachment_owner]
    mark_owned = mark == (certificate.opening.opened_position if certificate.opening else None)
    if mark.kind == "private":
        mark_owned |= mark.vertex in attachment_packet.cycles
    else:
        mark_owned |= any(cycle in attachment_packet.cycles for cycle in adj[mark.vertex])
        mark_owned |= cut_owner.get(mark.vertex) == certificate.attachment_owner
    require(mark_owned, f"{certificate.code}: marked attachment has no final owner")

    if certificate.opening is not None:
        opening = certificate.opening
        require(opening.triangle in range(9), f"{certificate.code}: invalid opened triangle")
        require(opening.retained_cut in adj[opening.triangle],
                f"{certificate.code}: opening cut is not incident")
        require(sorted(opening.interval_sizes) == [1, 2] and sum(opening.interval_sizes) == 3,
                f"{certificate.code}: opening has illegal triangle intervals")
        require(len(opening.interval_owners) == 2 and set(opening.interval_owners) <= set(packets),
                f"{certificate.code}: opening interval owner is missing")
        require(certificate.root_owner in opening.interval_owners,
                f"{certificate.code}: opening root has no interval owner")
        require(opening.opened_position.kind == "private" and
                opening.opened_position.vertex == opening.triangle,
                f"{certificate.code}: opening root is not a private triangle vertex")
    require(certificate.ledger.positive(), f"{certificate.code}: exact ledger is not strict positive")

    kinds = {packet.kind for packet in certificate.packets}
    if certificate.terminal == "packing-one-A9Q":
        require(kinds == {"packing-one"} and certificate.ledger == ExactLedger(Fraction(9), 1, 0, True),
                f"{certificate.code}: A9Q packing ledger mismatch")
    elif certificate.terminal == "leaf-TQ+A8":
        require(kinds == {"lower-rank", "common-cut"} and
                certificate.ledger == ExactLedger(Fraction(0), 0, 0, True),
                f"{certificate.code}: TQ+A8 strict ledger mismatch")
    elif certificate.terminal == "open-leaf-T+packing-one-A8Q":
        require(kinds == {"opened-tree", "packing-one"} and
                certificate.ledger == ExactLedger(Fraction(8), 1, 1, True),
                f"{certificate.code}: opened A8Q ledger mismatch")
    else:
        require(False, f"{certificate.code}: unknown terminal")


def main():
    rows, incidence_count, placements = enumerate_rows()
    scores = Counter()
    routers = Counter()
    residuals = []
    plans = {}
    for row in rows:
        plan = BASE.best_plan(row)
        plans[row.signature] = plan
        # The marked connector is retained with Q; private marked intervals are
        # not naked trees.  Only certified triangular credit is tested here.
        scores[plan.credit] += 1
        routers[len(plan.routers)] += 1
        if plan.credit < 1:
            residuals.append(row)
        else:
            verify_owner(row, plan)
    repairs = tuple(repair_residual(row, plans[row.signature], f"R{index}")
                    for index, row in enumerate(residuals, 1))
    for row, repair in zip(residuals, repairs):
        verify_residual_certificate(row, repair)
    row_digest = sha256(("\n".join(row.signature for row in rows) + "\n").encode("ascii")).hexdigest()
    residual_digest = sha256(("\n".join(row.signature for row in residuals) + "\n").encode("ascii")).hexdigest()

    print("nine-triangle incidence trees:", incidence_count)
    print("labelled interface placements before automorphisms:", placements)
    print("canonical marked one-interface rows:", len(rows))
    print("router accepted:", len(rows) - len(residuals))
    print("explicit packing/opening repairs:", len(repairs))
    print("credit distribution:", dict(sorted(scores.items())))
    print("router distribution:", dict(sorted(routers.items())))
    print("repair types:", dict(sorted(Counter(item.terminal for item in repairs).items())))
    print("canonical-row sha256:", row_digest)
    print("canonical-residual sha256:", residual_digest)

    require(incidence_count == 355, "incidence count changed")
    require(placements == 6745, "placement count changed")
    require(len(rows) == 3624, "canonical marked count changed")
    require(scores == Counter({0: 6, 1: 4, 2: 28, 3: 171, 4: 879, 5: 1548, 6: 988}), "credit census changed")
    require(routers == Counter({0: 6, 1: 3062, 2: 551, 3: 5}), "router census changed")
    require(Counter(item.terminal for item in repairs) == Counter({"packing-one-A9Q": 2, "leaf-TQ+A8": 1, "open-leaf-T+packing-one-A8Q": 3}), "repair census changed")
    require(len(residuals) == 6, "residual total changed")
    print("exact closure: 3624 = 3618 + 6")


if __name__ == "__main__":
    main()
