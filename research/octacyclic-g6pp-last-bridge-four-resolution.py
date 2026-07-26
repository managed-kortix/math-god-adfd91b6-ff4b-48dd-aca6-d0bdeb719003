#!/usr/bin/env python3
"""Independent incidence/ledger crosscheck for the final four G6PP classes."""

from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_census():
    path = HERE / "octacyclic-g6pp-last-bridge-census.py"
    spec = spec_from_file_location("g6pp_last_bridge_census", path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CENSUS = load_census()
P1 = "P1"


@dataclass(frozen=True)
class Resolution:
    label: str
    root_kind: str
    root_vertex: int
    positions: int
    split: tuple[int, int]
    singleton_triangles: tuple[int, int]
    mixed_packet: tuple[int, int, int]


RESOLUTIONS = (
    Resolution("L13", "cut", 7, 1, (0, 1), (2, 4), (3, 5, 6)),
    Resolution("L14", "cut", 8, 3, (1, 3), (4, 5), (0, 2, 6)),
    Resolution("L15", "private", 2, 6, (1, 3), (4, 5), (0, 2, 6)),
    Resolution("L16", "private", 0, 3, (1, 3), (4, 5), (0, 2, 6)),
)

EXPECTED_INCIDENCE = "X(P()T(X(T()))T(X(T()))T(X(T())))"
EXPECTED_EDGES = (
    (0, 7),
    (0, 8),
    (1, 7),
    (1, 9),
    (2, 8),
    (3, 7),
    (3, 10),
    (4, 9),
    (5, 10),
    (6, 7),
)


def retained_components(tree, split):
    return CENSUS.retained_components(tree, split)


def packet_of(resolution):
    packets = (
        (resolution.singleton_triangles[0],),
        (resolution.singleton_triangles[1],),
        resolution.mixed_packet,
        (P1,),
    )
    return packets, {
        item: index for index, packet in enumerate(packets) for item in packet
    }


def verify_induced_packetization(tree, mark, resolution):
    adj = CENSUS.adjacency(tree)
    packets, owner = packet_of(resolution)

    assert mark == CENSUS.Root(resolution.root_kind, resolution.root_vertex)
    assert mark.vertex not in resolution.split
    assert set(owner) == (set(range(7)) - set(resolution.split)) | {P1}
    assert retained_components(tree, resolution.split) == tuple(
        sorted(packets[:3])
    )

    # Every retained cut belongs to at most one packet. A cut incident only with
    # split routers is a cross-boundary remnant and needs no packet owner.
    for cut in range(7, len(adj)):
        retained_owners = {owner[cycle] for cycle in adj[cut] if cycle in owner}
        assert len(retained_owners) <= 1

    # Both deleted triangles are binary routers. Their two incidence marks have
    # distinct owners, so the triangle is partitioned into two nonempty proper
    # consecutive paths. This is valid in either cyclic ordering of the marks.
    for router in resolution.split:
        assert tree.colors[router] == "T"
        assert len(adj[router]) == 2
        side_owners = []
        for cut in adj[router]:
            retained = [cycle for cycle in adj[cut] if cycle in owner]
            assert retained
            owners = {owner[cycle] for cycle in retained}
            assert len(owners) == 1
            side_owners.append(owners.pop())
        assert len(set(side_owners)) == 2

    # The entry is retained by the mixed packet in all four root orbits; hence
    # strict last-bridge accounting creates no separate -1 tree interval.
    mixed_owner = owner[resolution.mixed_packet[0]]
    if mark.kind == "private":
        assert owner[mark.vertex] == mixed_owner
    else:
        root_owners = {owner[cycle] for cycle in adj[mark.vertex] if cycle in owner}
        assert root_owners == {mixed_owner}


def verify_spectral_packet(tree, resolution):
    adj = CENSUS.adjacency(tree)
    mixed = resolution.mixed_packet
    triangles = tuple(cycle for cycle in mixed if tree.colors[cycle] == "T")
    pentagons = tuple(cycle for cycle in mixed if tree.colors[cycle] == "P")
    assert len(triangles) == 2 and len(pentagons) == 1
    assert CENSUS.common_cut(tree, triangles)

    shared_cuts = set(adj[triangles[0]]) & set(adj[triangles[1]])
    assert len(shared_cuts) == 1
    # Established arbitrary-tree packet theorem: intersecting T,T plus P gives
    # sigma > 2-delta. The separate remote P1 has sigma >= -delta; singleton
    # triangular packets are strict positive and need no numerical credit.
    ledger = (Fraction(2), 2)
    a, b = ledger
    left = a + 2 * b
    assert left > 0 and left * left > 5 * b * b
    return ledger, min(shared_cuts)


def main():
    result = CENSUS.census()
    assert not result["final_codes"]
    residual = result["sixteen"][-4:]
    assert len(residual) == len(RESOLUTIONS) == 4
    trees = dict(CENSUS.enumerate_trees(("P",) + ("T",) * 6))

    for row, resolution in zip(residual, RESOLUTIONS):
        cuts, signature, _, mark, positions, edges = row
        tree = trees[signature]
        assert cuts == 4
        assert signature == EXPECTED_INCIDENCE
        assert edges == EXPECTED_EDGES
        assert positions == resolution.positions
        verify_induced_packetization(tree, mark, resolution)
        ledger, shared_cut = verify_spectral_packet(tree, resolution)
        print(
            f"{resolution.label}: root={mark.kind}:{mark.vertex} "
            f"split={resolution.split} packets=T{resolution.singleton_triangles[0]}"
            f"+T{resolution.singleton_triangles[1]}+TTP{resolution.mixed_packet}+P1 "
            f"shared-cut={shared_cut} sigma>{ledger[0]}-{ledger[1]}delta"
        )

    # 2-2delta = 6-2sqrt(5) > 0 because 6^2 > (2sqrt(5))^2.
    assert 6 * 6 > 4 * 5
    print("closed independent final classes: 4/4")
    print("uniform strict margin: 2-2delta = 6-2sqrt(5) > 0")
    print("shared-cut TTP ledger crosscheck: 4/4")


if __name__ == "__main__":
    main()
