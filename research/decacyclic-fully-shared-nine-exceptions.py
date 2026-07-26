#!/usr/bin/env python3
"""Fail-closed structural certificates for the nine fully shared T^8PP rows."""

from collections import Counter, deque
from dataclasses import dataclass
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


spec = spec_from_file_location("rank9_shared", HERE / "nonacyclic-fully-shared-incidence-census.py")
base = module_from_spec(spec)
require(spec.loader is not None, "cannot load fully shared dependency")
sys.modules[spec.name] = base
spec.loader.exec_module(base)


EXPECTED_SIGNATURES = (
    "X(P()P()T()T()T()T()T()T()T()T())",
    "P(X(P())X(T()T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T()T()))",
    "P(X(P())X(T())X(T()T()T()T()T()T()T()))",
    "T(X(P())X(P())X(T()T()T()T()T()T()T()))",
    "T(X(P())X(P()T()T()T()T()T()T())X(T()))",
    "X(T()T()T()T()T()T()T(X(P()))T(X(P())))",
    "X(T()T()T()T()T()T(X(P()))T(X(P())X(T())))",
    "X(T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))",
)
EXPECTED_SIGNATURE_DIGEST = "461351660aa2d8e23d36ca54441275acfd022ebfec80ba599698ffcbb86cb35a"


@dataclass(frozen=True)
class Packet:
    name: str
    cycles: tuple[int, ...]
    hub: int = -1
    packing_one: bool = False


@dataclass(frozen=True)
class Certificate:
    code: str
    signature: str
    operation: str
    routers: tuple[int, ...]
    openings: tuple[tuple[int, int], ...]
    packets: tuple[Packet, ...]
    credit: int
    deficits: int
    special_margin: bool = False


def exact_positive(credit, deficits):
    left = credit + 2 * deficits
    return left > 0 and left * left > 5 * deficits * deficits


def connected_packet(adj, cycles):
    allowed = set(cycles)
    if not allowed:
        return False
    seen = {next(iter(allowed))}
    queue = deque(seen)
    while queue:
        cycle = queue.popleft()
        for cut in adj[cycle]:
            for neighbor in adj[cut]:
                if neighbor in allowed and neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
    return seen == allowed


def hub_packet(tree, cut, excluded=()):
    adj = base.adjacency(tree)
    cycles = tuple(sorted(cycle for cycle in adj[cut] if cycle not in set(excluded)))
    return cycles


def leaf_across(tree, router, color):
    adj = base.adjacency(tree)
    candidates = []
    for cut in adj[router]:
        others = [cycle for cycle in adj[cut] if cycle != router]
        if len(others) == 1 and tree.colors[others[0]] == color:
            candidates.append(others[0])
    require(len(candidates) == 1, f"router {router} does not have one {color} leaf")
    return candidates[0]


def make_certificate(index, signature, tree):
    adj = base.adjacency(tree)
    cuts = range(len(tree.colors), len(adj))
    hubs = sorted(cuts, key=lambda cut: (-len(adj[cut]), cut))
    hub = hubs[0]
    triangles = tuple(i for i, color in enumerate(tree.colors) if color == "T")
    pentagons = tuple(i for i, color in enumerate(tree.colors) if color == "P")

    if index == 1:
        return Certificate("E1", signature, "common-cut T^8PP", (), (),
                           (Packet("T^8PP", tuple(range(10)), hub),), 9, 0, True)
    if index == 2:
        opened = next(cycle for cycle in pentagons if hub not in adj[cycle])
        return Certificate("E2", signature, "open leaf P; retain common-cut T^8P", (), ((opened, -1),),
                           (Packet("T^8P", hub_packet(tree, hub), hub),), 7, 1)
    if index == 3:
        router = next(cycle for cycle in triangles if len(adj[cycle]) == 2)
        leaf = leaf_across(tree, router, "P")
        return Certificate("E3", signature, "P + common-cut T^7P", (router,), (),
                           (Packet("P", (leaf,)), Packet("T^7P", hub_packet(tree, hub, (router,)), hub)), 7, 2)
    if index == 4:
        router = next(cycle for cycle in pentagons if len(adj[cycle]) == 3)
        leaf_p = leaf_across(tree, router, "P")
        leaf_t = leaf_across(tree, router, "T")
        return Certificate("E4", signature, "open leaf P and leaf T; retain common-cut T^7P", (),
                           ((leaf_p, -1), (leaf_t, -1)),
                           (Packet("T^7P", tuple(sorted(set(range(10)) - {leaf_p, leaf_t})), hub),), 5, 1)
    if index == 5:
        router = next(cycle for cycle in triangles if len(adj[cycle]) == 3)
        # There are two symmetric P leaves; canonical labels are irrelevant, but
        # the certificate chooses the lower cycle and retains the other arm.
        leaves = tuple(sorted(cycle for cut in adj[router] for cycle in adj[cut]
                              if cycle != router and tree.colors[cycle] == "P"))
        require(len(leaves) == 2, "E5 does not have two pentagon leaves")
        opened, retained_p = leaves
        retained = tuple(sorted(set(triangles) | {retained_p}))
        return Certificate("E5", signature, "open one P; retain packing-one T^8P", (), ((opened, -1),),
                           (Packet("T^8P", retained, hub, True),), 7, 1)
    if index == 6:
        router = next(cycle for cycle in triangles if len(adj[cycle]) == 3)
        leaf_p = leaf_across(tree, router, "P")
        leaf_t = leaf_across(tree, router, "T")
        return Certificate("E6", signature, "P + T + common-cut T^6P", (router,), (),
                           (Packet("P", (leaf_p,)), Packet("T", (leaf_t,)),
                            Packet("T^6P", hub_packet(tree, hub, (router,)), hub)), 6, 2)

    routers = tuple(sorted(cycle for cycle in triangles if len(adj[cycle]) > 1 and hub in adj[cycle]
                           and any(cut != hub and any(tree.colors[other] == "P" for other in adj[cut])
                                   for cut in adj[cycle])))
    require(len(routers) == 2, f"E{index} does not have the two marked hub routers")
    leaf_packets = []
    for router in routers:
        for color in ("P", "T"):
            matches = [cycle for cut in adj[router] for cycle in adj[cut]
                       if cycle != router and tree.colors[cycle] == color and hub not in adj[cycle]]
            for cycle in sorted(set(matches)):
                leaf_packets.append(Packet(color, (cycle,)))
    retained_a = tuple(cycle for cycle in triangles if cycle not in routers and hub in adj[cycle])
    packets = tuple(leaf_packets) + (Packet(f"A_{len(retained_a)}", retained_a, hub),)
    operations = {7: "P + P + A_6", 8: "P + P + T + A_5", 9: "P + P + T + T + A_4"}
    credits = {7: 1, 8: 2, 9: 3}
    return Certificate(f"E{index}", signature, operations[index], routers, (), packets, credits[index], 2)


def verify_certificate(tree, certificate):
    require(base.signature(tree) == certificate.signature, f"{certificate.code} signature/tree mismatch")
    adj = base.adjacency(tree)
    cycle_count = len(tree.colors)
    opened = {cycle for cycle, _ in certificate.openings}
    routers = set(certificate.routers)
    require(len(opened) == len(certificate.openings), f"{certificate.code} repeats an opening")
    require(opened.isdisjoint(routers), f"{certificate.code} opens a router")
    require(all(cost == -1 for _, cost in certificate.openings), f"{certificate.code} has a non-exact opening cost")
    require(all(0 <= cycle < cycle_count for cycle in opened | routers), f"{certificate.code} references a bad cycle")
    retained = set(range(cycle_count)) - opened - routers
    packet_cycles = [cycle for packet in certificate.packets for cycle in packet.cycles]
    require(set(packet_cycles) == retained and len(packet_cycles) == len(set(packet_cycles)),
            f"{certificate.code} packets do not partition retained cycles")

    packet_of = {}
    for packet in certificate.packets:
        require(packet.cycles == tuple(sorted(packet.cycles)), f"{certificate.code}/{packet.name} cycles are not canonical")
        require(connected_packet(adj, packet.cycles), f"{certificate.code}/{packet.name} is disconnected")
        for cycle in packet.cycles:
            packet_of[cycle] = packet.name
        if packet.hub >= 0:
            require(packet.hub >= cycle_count, f"{certificate.code}/{packet.name} hub is not a cut")
            if not packet.packing_one:
                require(all(packet.hub in adj[cycle] for cycle in packet.cycles),
                        f"{certificate.code}/{packet.name} is not a common-hub packet")
        if packet.packing_one:
            triangle_cycles = [cycle for cycle in packet.cycles if tree.colors[cycle] == "T"]
            require(packet.hub >= 0 and triangle_cycles,
                    f"{certificate.code}/{packet.name} packing-one has no displayed triangle hub")
            require(all(packet.hub in adj[cycle] for cycle in triangle_cycles),
                    f"{certificate.code}/{packet.name} triangles do not have packing number one")

    # Every retained incidence cut has at most one final packet owner. Cuts left
    # only on opened/router cycles are owned by that exact operation.
    final_owners = []
    for cut in range(cycle_count, len(adj)):
        owners = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        require(len(owners) <= 1, f"{certificate.code} cut {cut} has competing final owners")
        if owners:
            owner = next(iter(owners))
        else:
            operation_cycles = sorted(set(adj[cut]) & (opened | routers))
            require(operation_cycles, f"{certificate.code} cut {cut} has no final owner")
            owner = "operation:" + ",".join(map(str, operation_cycles))
        final_owners.append((cut, owner))
    require(len(final_owners) == len(adj) - cycle_count, f"{certificate.code} ownership is incomplete")
    if not certificate.special_margin:
        require(exact_positive(certificate.credit, certificate.deficits), f"{certificate.code} ledger is not positive")
    return tuple(final_owners)


def main():
    result = base.census(("T",) * 8 + ("P",) * 2, 0, base.tpp_bound)
    totals, safe, _, _, _, unresolved = result
    signatures = tuple(item[1] for item in unresolved)
    digest = sha256(("\n".join(signatures) + "\n").encode("ascii")).hexdigest()
    require(sum(totals.values()) == 30386, totals)
    require(sum(safe.values()) == 30377, safe)
    require(Counter(item[0] for item in unresolved) == Counter({1: 1, 2: 2, 3: 4, 4: 1, 5: 1}), unresolved)
    require(signatures == EXPECTED_SIGNATURES, "exact exception signature set or order changed")
    require(digest == EXPECTED_SIGNATURE_DIGEST, digest)

    classes = dict(base.enumerate_colors(tuple(sorted(("T",) * 8 + ("P",) * 2)), 0))
    certificates = []
    for index, (_, signature, profile, edges) in enumerate(unresolved, 1):
        tree = classes[signature]
        require(tree.edges == edges and base.cut_profile(tree) == profile, f"E{index} concrete incidence row changed")
        certificate = make_certificate(index, signature, tree)
        owners = verify_certificate(tree, certificate)
        certificates.append(certificate)
        margin = ">9-4/(3sqrt(13))" if certificate.special_margin else f">{certificate.credit}-{certificate.deficits}delta"
        print(f"{certificate.code}: c={base.cut_count(tree)}; {certificate.operation}; {margin}")
        print("  signature:", signature)
        print("  incidence:", tree.edges)
        print("  routers:", certificate.routers or "none", "openings:", certificate.openings or "none")
        print("  packets:", certificate.packets)
        print("  final-cut-owners:", owners)

    require(len(certificates) == 9, "certificate count changed")
    print("canonical-exception sha256:", digest)
    print("closed structural ownership certificates: 9/9")
    print("remaining fully shared exception gaps: 0")


if __name__ == "__main__":
    main()
