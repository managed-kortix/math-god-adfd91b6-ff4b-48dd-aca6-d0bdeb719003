#!/usr/bin/env python3
"""Exact marked-entry census for the disconnected rank-ten T^8P | P family.

The rank-nine machinery supplies the incidence generator and certificate
constructors.  This file independently rechecks every generated incidence
tree and every field of all 11586 direct, 100 replacement, and three locked
certificates: packets, router order and intervals, final owners, cuts,
attachments, the opened tree, and exact strict radical ledgers.
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
    "rank_nine_entry_locked", HERE / "nonacyclic-t7p-last-bridge-conservative.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("rank-nine entry-locked dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)

BASE.TRIANGLE_MARGIN[8] = 0
OLD_PROFILE_BOUND = BASE.profile_bound


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def profile_bound(tree, component):
    triangles, pentagons = BASE.component_counts(tree, component)
    if pentagons and triangles + pentagons == 8:
        return BASE.Bound(Fraction(0), True, "input generic rank-8 > 0")
    return OLD_PROFILE_BOUND(tree, component)


BASE.profile_bound = profile_bound


@dataclass(frozen=True)
class OpeningCertificate:
    router: int
    hub: int
    p_cut: int
    opened_owner: str
    retained_owner: str
    opened_vertices: tuple[str, ...]
    p_assignments: tuple[tuple[str, str], ...]
    connector_parts: tuple[tuple[str, str], ...]
    connector_owner: str
    cut_owners: tuple[tuple[int, str], ...]
    ledger: tuple[int, int]
    strict: bool


def validate_incidence_tree(signature, tree):
    """Reject malformed or noncanonical generator output without assertions."""
    adj = BASE.BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    require(BASE.BASE.signature(tree) == signature, "incidence signature mismatch")
    require(len(tree.edges) == len(adj) - 1, "incidence graph is not a tree")
    require(len(set(tree.edges)) == len(tree.edges), "duplicate incidence edge")
    require(all(left < cycle_count <= right for left, right in tree.edges), "non-bipartite incidence edge")
    require(all(len(adj[cut]) >= 2 for cut in range(cycle_count, len(adj))), "degenerate cut vertex")
    require(all(1 <= len(adj[cycle]) <= (3 if color == "T" else 5)
                for cycle, color in enumerate(tree.colors)), "cycle capacity violation")
    seen = {0}
    todo = [0]
    while todo:
        vertex = todo.pop()
        for neighbor in adj[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                todo.append(neighbor)
    require(len(seen) == len(adj), "disconnected incidence graph")


def expected_cut_owners(tree, cycle_owner, steps):
    adj = BASE.BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    interval_owner = {}
    for step in steps:
        for interval in step.intervals:
            if interval.port[0] == "cut":
                cut = interval.port[1]
                require(cut not in interval_owner or interval_owner[cut] == interval.owner,
                        "inconsistent interval owner for cut")
                interval_owner[cut] = interval.owner
    result = []
    for cut in range(cycle_count, len(adj)):
        owners = {cycle_owner[cycle] for cycle in adj[cut] if cycle in cycle_owner}
        require(len(owners) <= 1, f"cut {cut} meets multiple final packets")
        if owners:
            owner = next(iter(owners))
            require(cut not in interval_owner or interval_owner[cut] == owner,
                    f"cut {cut} disagrees with its interval owner")
        else:
            require(cut in interval_owner, f"deleted cut {cut} has no final owner")
            owner = interval_owner[cut]
        result.append((cut, owner))
    return tuple(result)


def validate_attachments(certificate, mark, cycle_owner):
    steps = certificate.steps if hasattr(certificate, "steps") else (certificate.step,)
    expected = tuple(
        [(('cut', cut), owner) for cut, owner in certificate.cut_owners]
        + [(('private', cycle), cycle_owner[cycle]) for cycle in cycle_owner]
        + [
            ((f"router-{step.router}-interval", index), interval.owner)
            for step in steps
            for index, interval in enumerate(step.intervals)
        ]
        + [(('root', mark.vertex), certificate.root_owner),
           (('remote', 1), certificate.remote_owner)]
    )
    require(certificate.attachment_owners == expected, "attachment-owner ledger mismatch")


def validate_direct_certificate(tree, mark, certificate):
    """Independently check every field of a one-router certificate."""
    adj = BASE.BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    step = certificate.step
    router = step.router
    require(tree.colors[router] == "T", "direct router is not triangular")
    require(step.active_cycles == tuple(range(cycle_count)), "direct active territory mismatch")
    components = BASE.BASE.components_after_split(tree, router)
    cycle_owner = {
        cycle: f"packet:{index}"
        for index, component in enumerate(components)
        for cycle in component[0]
    }
    require(len(cycle_owner) == cycle_count - 1, "direct packets do not partition retained cycles")
    owner_index = BASE.root_component(tree, router, mark, components)
    expected_bounds = tuple(profile_bound(tree, component) for component in components)
    expected_bounds += (BASE.Bound(Fraction(-1, 4), True, "remote P>-1/4"),)
    private_deleted = mark == BASE.Mark("private", router)
    if private_deleted and not certificate.keep_connector:
        expected_bounds += (BASE.Bound(Fraction(-1), False, "private-entry tree>=-1"),)
    require(certificate.packet_bounds == expected_bounds, "direct packet hypotheses mismatch")
    require(all(BASE.connected_cycles(tree, component[0]) for component in components),
            "direct certificate has a disconnected packet")

    remote_owner = "remote:P1"
    require(not certificate.keep_connector or private_deleted,
            "direct certificate keeps a nonprivate connector")
    expected_root = (remote_owner if certificate.keep_connector else BASE.NAKED_TREE_OWNER
                     if owner_index is None else f"packet:{owner_index}")
    ports = [("cut", cut) for cut in adj[router]]
    if private_deleted:
        ports.append(("private", router))
    require(tuple(interval.port for interval in step.intervals) == tuple(ports),
            "direct router ports do not match its intervals")
    require(tuple(interval.size for interval in step.intervals) ==
            ((1, 2) if len(ports) == 2 else (1, 1, 1)), "improper direct router intervals")
    for interval in step.intervals:
        if interval.port[0] == "private":
            require(interval.owner == expected_root, "private connector has the wrong owner")
        else:
            owners = {cycle_owner[cycle] for cycle in adj[interval.port[1]] if cycle != router}
            require(owners == {interval.owner}, "direct interval does not lead to its packet")
    require(len({interval.owner for interval in step.intervals}) == len(step.intervals),
            "direct router intervals do not have distinct final owners")

    cuts = expected_cut_owners(tree, cycle_owner, (step,))
    if mark.kind == "cut":
        expected_root = dict(cuts)[mark.vertex]
    elif mark.vertex != router:
        expected_root = cycle_owner[mark.vertex]
    require(certificate.cut_owners == cuts, "direct cut ownership mismatch")
    require(certificate.root_owner == expected_root, "direct entry owner mismatch")
    require(certificate.remote_owner == remote_owner, "direct remote-P owner mismatch")
    packet_owners = set(cycle_owner.values()) | {remote_owner, BASE.NAKED_TREE_OWNER}
    require(all(owner in packet_owners for _, owner in certificate.cut_owners), "direct cut has no final owner")
    validate_attachments(certificate, mark, cycle_owner)

    total = sum((bound.value for bound in expected_bounds), Fraction())
    strict = any(bound.strict for bound in expected_bounds)
    positive = total > 0 or (total == 0 and strict)
    require((certificate.total, certificate.strict, certificate.positive) ==
            (total, strict, positive), "direct exact ledger mismatch")
    require(strict and positive, "direct ledger is not strictly positive")


def validate_replacement(tree, mark, certificate):
    """Verify split order, intervals, packets, owners, and radical ledger."""
    adj = BASE.BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    require(certificate.order == tuple(step.router for step in certificate.steps),
            "replacement order/step mismatch")
    require(len(set(certificate.order)) == len(certificate.order), "replacement repeats a router")
    require(all(tree.colors[router] == "T" for router in certificate.order),
            "replacement deletes a nontriangle")
    components = BASE.deleted_components(tree, certificate.order)
    expected_packets = []
    cycle_owner = {}
    for index, (_, cycles) in enumerate(components):
        owner = f"packet:{index}"
        require(BASE.connected_cycles(tree, cycles), "replacement packet is disconnected")
        bound = BASE.packet_bound(tree, cycles)
        expected_packets.append(BASE.Packet(owner, cycles, bound))
        for cycle in cycles:
            require(cycle not in cycle_owner, "replacement packets overlap")
            cycle_owner[cycle] = owner
    expected_packets.append(BASE.Packet("remote:P1", (), (Fraction(), 1, True, "remote P>-delta")))
    private_deleted = mark.kind == "private" and mark.vertex in certificate.order
    if private_deleted and not certificate.keep_connector:
        expected_packets.append(BASE.Packet(BASE.NAKED_TREE_OWNER, (),
                                            (Fraction(-1), 0, False, "private-entry tree=-1")))
    require(certificate.packets == tuple(expected_packets), "replacement packet hypotheses mismatch")
    require(set(cycle_owner) == set(range(cycle_count)) - set(certificate.order),
            "replacement packets do not cover exactly the retained cycles")
    require(not certificate.keep_connector or private_deleted,
            "replacement keeps a connector not incident with a deleted router")

    private_owner = "remote:P1" if certificate.keep_connector else (
        BASE.NAKED_TREE_OWNER if private_deleted else None)
    active = set(range(len(adj)))
    for step in certificate.steps:
        require(step.router in active, "replacement router is not active")
        territory = BASE.active_territory(adj, active, step.router)
        expected_active = tuple(sorted(vertex for vertex in territory if vertex < cycle_count))
        require(step.active_cycles == expected_active, "replacement active territory mismatch")
        active.remove(step.router)
        ports = [("cut", cut) for cut in adj[step.router] if cut in territory]
        if mark == BASE.Mark("private", step.router):
            ports.append(("private", step.router))
        require(tuple(interval.port for interval in step.intervals) == tuple(ports),
                "replacement interval ports mismatch")
        require(tuple(interval.size for interval in step.intervals) ==
                ((1, 2) if len(ports) == 2 else (1, 1, 1)),
                "replacement interval is not a proper triangle interval partition")
        require(len({interval.owner for interval in step.intervals}) == len(step.intervals),
                "replacement router interval owners are not distinct")
        for interval in step.intervals:
            if interval.port[0] == "private":
                require(interval.owner == private_owner, "replacement private connector owner mismatch")
            else:
                cut = interval.port[1]
                owners = {cycle_owner[cycle] for cycle in adj[cut] if cycle in cycle_owner}
                require(owners == {interval.owner}, "replacement interval has no unique final packet")

    cuts = expected_cut_owners(tree, cycle_owner, certificate.steps)
    require(certificate.cut_owners == cuts, "replacement cut ownership mismatch")
    expected_root = (dict(cuts)[mark.vertex] if mark.kind == "cut" else
                     private_owner if private_deleted else cycle_owner[mark.vertex])
    require(certificate.root_owner == expected_root, "replacement entry owner mismatch")
    require(certificate.remote_owner == "remote:P1", "replacement remote-P owner mismatch")
    validate_attachments(certificate, mark, cycle_owner)
    BASE.validate_deletion_owners(certificate)

    bounds = tuple(packet.bound for packet in expected_packets)
    ledger = (sum((bound[0] for bound in bounds), Fraction()), sum(bound[1] for bound in bounds))
    strict = any(bound[2] for bound in bounds)
    sign = BASE.exact_sign(*ledger)
    positive = sign > 0 or (sign == 0 and strict)
    require(certificate.ledger == ledger, "replacement radical ledger mismatch")
    require(certificate.entry_cost == int(private_deleted and not certificate.keep_connector),
            "replacement entry cost mismatch")
    require((certificate.strict, certificate.positive) == (strict, positive),
            "replacement strictness/positivity mismatch")
    require(strict and positive, "replacement ledger is not strictly positive")


def locked_repair(tree, mark):
    """Check the unique new shape and its uniform remote-P opening."""
    adj = BASE.BASE.adjacency(tree)
    pentagon = tree.colors.index("P")
    require(len(adj[pentagon]) == 1, "clustered pentagon is not an incidence leaf")
    router = next(
        cycle
        for cycle, color in enumerate(tree.colors)
        if color == "T" and len(adj[cycle]) == 2 and adj[pentagon][0] in adj[cycle]
    )
    p_cut = adj[pentagon][0]
    hub = next(cut for cut in adj[router] if cut != p_cut)
    triangles = tuple(cycle for cycle, color in enumerate(tree.colors) if color == "T")
    require(len(triangles) == 8, "locked repair does not contain eight triangles")
    require(
        all(hub in adj[cycle] for cycle in triangles),
        "locked repair triangles do not have packing number one at the hub",
    )
    require(
        mark in (BASE.Mark("cut", p_cut), BASE.Mark("cut", hub), BASE.Mark("private", router)),
        "unexpected marked orbit on the locked repair shape",
    )

    # H contains all eight hub triangles, P0, both connector remnants, and all
    # trees rooted there.  Packing one gives sigma(H)>8-delta.  Opening the four
    # private vertices of remote P1 gives one nonempty tree E with sigma(E)=-1.
    certificate = OpeningCertificate(
        router, hub, p_cut, "opened:P1-private-tree", "packet:T8P0",
        ("P1-private-1", "P1-private-2", "P1-private-3", "P1-private-4"),
        (("P0", "packet:T8P0"), ("P1-entry", "packet:T8P0"),
         ("P1-private-tree", "opened:P1-private-tree")),
        (("P0-side-remnant", "packet:T8P0"),
         ("P1-side-remnant", "packet:T8P0")),
        "packet:T8P0", tuple((cut, "packet:T8P0") for cut in range(9, len(adj))),
        (7, 1), True,
    )
    require(certificate.opened_vertices == tuple(f"P1-private-{i}" for i in range(1, 5)),
            "opened tree is not exactly the four private remote-P vertices")
    require(certificate.opened_owner != certificate.retained_owner, "opened and retained territories overlap")
    require(certificate.p_assignments ==
            (("P0", certificate.retained_owner), ("P1-entry", certificate.retained_owner),
             ("P1-private-tree", certificate.opened_owner)), "locked pentagon assignment mismatch")
    require(certificate.connector_parts ==
            (("P0-side-remnant", certificate.retained_owner),
             ("P1-side-remnant", certificate.retained_owner)),
            "locked connector-remnant assignment mismatch")
    require(certificate.connector_owner == certificate.retained_owner,
            "remote-P connector was incorrectly charged to the opened tree")
    require(dict(certificate.cut_owners) == {cut: certificate.retained_owner for cut in range(9, len(adj))},
            "locked repair does not own every incidence cut")
    require(certificate.strict, "packing-one packet is not strict")
    require(BASE.exact_sign(*certificate.ledger) > 0, "7-delta is not positive")
    return certificate


def census():
    classes = BASE.BASE.enumerate_colors(("P",) + ("T",) * 8, 5)
    all_counts = Counter(BASE.BASE.cut_count(tree) for _, tree in classes)
    leaf_counts = Counter()
    marked_counts = Counter()
    position_counts = Counter()
    direct_counts = Counter()
    replacement_counts = Counter()
    replacement_sizes = Counter()
    locked_counts = Counter()
    row_ids = []
    classified_ids = []
    locked_ids = []

    for signature, tree in classes:
        validate_incidence_tree(signature, tree)
        adj = BASE.BASE.adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            continue
        cuts = BASE.BASE.cut_count(tree)
        leaf_counts[cuts] += 1
        for root_code, mark, multiplicity in BASE.root_orbits(tree):
            row_id = f"{cuts}\t{signature}\t{root_code}"
            row_ids.append(row_id)
            marked_counts[cuts] += 1
            position_counts[cuts] += multiplicity
            certificates = tuple(
                BASE.conservative_split(tree, cycle, mark)
                for cycle, color in enumerate(tree.colors)
                if color == "T"
            ) + tuple(
                BASE.private_entry_uncut_split(tree, cycle, mark)
                for cycle, color in enumerate(tree.colors)
                if color == "T"
            )
            direct = tuple(item for item in certificates if item is not None)
            if direct:
                for certificate in direct:
                    validate_direct_certificate(tree, mark, certificate)
                direct_counts[cuts] += 1
                classified_ids.append(row_id)
                continue
            replacement = BASE.best_deletion_certificate(tree, mark)
            if replacement is not None:
                validate_replacement(tree, mark, replacement)
                replacement_counts[cuts] += 1
                replacement_sizes[len(replacement.order)] += 1
                classified_ids.append(row_id)
                continue
            locked_repair(tree, mark)
            locked_counts[cuts] += 1
            classified_ids.append(row_id)
            locked_ids.append(row_id)

    row_ids.sort()
    classified_ids.sort()
    locked_ids.sort()
    row_digest = sha256(("\n".join(row_ids) + "\n").encode("ascii")).hexdigest()
    locked_digest = sha256(("\n".join(locked_ids) + "\n").encode("ascii")).hexdigest()

    require(all_counts == Counter({1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 781, 7: 536, 8: 148}), "all-incidence census changed")
    require(leaf_counts == Counter({1: 1, 2: 7, 3: 42, 4: 142, 5: 301, 6: 354, 7: 212, 8: 46}), "P-leaf census changed")
    require(marked_counts == Counter({1: 2, 2: 34, 3: 279, 4: 1226, 5: 3019, 6: 3997, 7: 2550, 8: 582}), "marked census changed")
    require(position_counts == Counter({1: 17, 2: 119, 3: 714, 4: 2414, 5: 5117, 6: 6018, 7: 3604, 8: 782}), "labelled-position census changed")
    require(direct_counts == Counter({2: 25, 3: 263, 4: 1201, 5: 2988, 6: 3977, 7: 2550, 8: 582}), "direct census changed")
    require(replacement_counts == Counter({1: 2, 2: 6, 3: 16, 4: 25, 5: 31, 6: 20}), "replacement census changed")
    require(replacement_sizes == Counter({0: 2, 1: 9, 2: 73, 3: 16}), "replacement-size census changed")
    require(locked_counts == Counter({2: 3}), "locked residual census changed")
    require(len(row_ids) == len(set(row_ids)), "canonical marked rows are not unique")
    require(classified_ids == row_ids, "certificate classes do not exactly partition marked rows")
    require(sum(marked_counts.values()) == 11689, "marked total changed")
    require(sum(direct_counts.values()) == 11586, "direct total changed")
    require(sum(replacement_counts.values()) == 100, "replacement total changed")
    require(len(locked_ids) == 3, "locked repair total changed")
    require(row_digest == "002685d1e5662e8890ae8d067dee2963ffbbd3388a00e9491427797420b14cf7",
            "canonical marked-row digest changed")
    require(locked_digest == "f9f898a13fceb6b4fa3c5d50d1cc83ea9e22324b64c999b37c0b6d263add0dc1",
            "locked-row digest changed")
    return (
        all_counts, leaf_counts, marked_counts, position_counts, direct_counts,
        replacement_counts, replacement_sizes, locked_counts, row_digest,
        locked_digest,
    )


def main():
    result = census()
    labels = (
        "all T^8P incidence trees", "P-leaf incidence trees",
        "marked entry orbits", "labelled entry positions",
        "direct one-router certificates", "finite replacements",
        "replacement router counts", "packing-one opening repairs",
    )
    for label, counter in zip(labels, result[:8]):
        print(f"{label}:", dict(sorted(counter.items())), "total", sum(counter.values()))
    print("canonical-row sha256:", result[8])
    print("locked-row sha256:", result[9])
    print("exact closure: 11689 = 11586 + 100 + 3")
    print("weakest new repair: 7-delta = 9-sqrt(5) > 0")


if __name__ == "__main__":
    main()
