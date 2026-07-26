#!/usr/bin/env python3
"""SUPERSEDED audit of proposed packets for nine marked T^6P exceptions.

The uncut E1--E9 construction is not a complete proof. This script retains its
history and rejects six rows; use the strict-last-bridge 877=861+16 verifier.

The script reuses the exhaustive census, checks explicit zero-, one-, and
two-router cycle profiles, evaluates their symbolic a-b*delta ledgers, checks
whether the uncut connector realizes the displayed separate P1 packet, and
compares the rooted triangular kernels with the four residuals.
"""

from collections import Counter
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = spec_from_file_location(name, HERE / filename)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CENSUS = load("t6p_marked_census", "octacyclic-t6p-marked-root-incidence-census.py")
ROOTED = load("rooted_t6_certificate", "octacyclic-rooted-six-triangle-certificate.py")


@dataclass(frozen=True)
class Recipe:
    split: tuple[int, ...]
    packets: tuple[tuple[object, ...], ...]
    expected_ledger: tuple[int, int]


X = "P1"
RECIPES = (
    Recipe((), ((0, 1, 2, 3, 4, 5, 6), (X,)), (6, 2)),
    Recipe((), ((0, 1, 2, 3, 4, 5, 6), (X,)), (6, 2)),
    Recipe((0,), ((6,), (1, 2, 3, 4, 5), (X,)), (2, 2)),
    Recipe((0,), ((6,), (1, 2, 3, 4, 5), (X,)), (2, 2)),
    Recipe((0,), ((2,), (1, 3, 4, 5, 6), (X,)), (4, 2)),
    Recipe((0,), ((2,), (6,), (1, 3, 4, 5), (X,)), (3, 2)),
    Recipe((0,), ((2,), (6,), (1, 3, 4, 5), (X,)), (3, 2)),
    Recipe((0, 1), ((2,), (6,), (3, 4, 5), (X,)), (2, 2)),
    Recipe((0, 1), ((2,), (5,), (6,), (3, 4), (X,)), (1, 2)),
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
    """Return (constant, delta coefficient, source), meaning sigma > a-b*delta."""
    cycles = tuple(item for item in packet if isinstance(item, int))
    has_external = X in packet
    triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
    pentagons = sum(tree.colors[cycle] == "P" for cycle in cycles) + has_external
    assert connected(tree, cycles)
    if pentagons == 0:
        assert triangles
        margin = CENSUS.TRIANGLE_MARGIN[len(triangles)]
        return margin, 0, f"A_{len(triangles)}"
    if not triangles:
        assert pentagons == 1
        return 0, 1, "P"
    assert pentagons == 1 and common_cut(tree, cycles)
    return len(triangles), 1, f"common-cut T^{len(triangles)}P"


def verify_ownership(tree, mark, recipe):
    adj = CENSUS.BASE.adjacency(tree)
    packet_of = {item: index for index, packet in enumerate(recipe.packets) for item in packet}
    assert set(packet_of) == (set(range(7)) - set(recipe.split)) | {X}
    assert len(packet_of) == sum(len(packet) for packet in recipe.packets)

    for cut in range(len(tree.colors), len(adj)):
        retained_owners = {packet_of[cycle] for cycle in adj[cut] if cycle in packet_of}
        assert len(retained_owners) <= 1

    # This exceptional-row abstraction does not by itself certify a connector
    # join: X records only the remote cycle profile, not the marked root
    # interval or the intervening connector vertices. Connector legality is
    # audited separately by the marked-census script.
    assert recipe.packets[packet_of[X]] == (X,)

    for router in recipe.split:
        marks = adj[router]
        assert 2 <= len(marks) <= 3
        owners = []
        for cut in marks:
            retained = [cycle for cycle in adj[cut] if cycle in packet_of]
            if retained:
                owner_set = {packet_of[cycle] for cycle in retained}
                assert len(owner_set) == 1
                owners.extend(owner_set)
            elif mark.kind == "cut" and mark.vertex == cut:
                owners.append(packet_of[X])
        if mark.kind == "private" and mark.vertex == router:
            owners.append(packet_of[X])
        assert len(owners) in (2, 3) and len(owners) == len(set(owners))


def triangular_kernel(tree, mark):
    """Delete P0 and canonically mark the unchanged external entry vertex."""
    adj = CENSUS.BASE.adjacency(tree)
    triangles = [cycle for cycle, color in enumerate(tree.colors) if color == "T"]
    relabel = {cycle: index for index, cycle in enumerate(triangles)}
    shared_cuts = [
        cut
        for cut in range(len(tree.colors), len(adj))
        if sum(cycle in triangles for cycle in adj[cut]) >= 2
    ]
    relabel.update({cut: 6 + index for index, cut in enumerate(shared_cuts)})
    edges = tuple(
        sorted(
            (relabel[cycle], relabel[cut])
            for cycle in triangles
            for cut in adj[cycle]
            if cut in shared_cuts
        )
    )
    kernel = ROOTED.Tree(edges)
    if mark.kind == "private":
        root = ("private", relabel[mark.vertex])
    elif mark.vertex in shared_cuts:
        root = ("cut", relabel[mark.vertex])
    else:
        incident = [cycle for cycle in adj[mark.vertex] if cycle in triangles]
        assert len(incident) == 1
        root = ("private", relabel[incident[0]])
    return ROOTED.signature(kernel, 6, root)


def separate_p1_packet_is_legal(mark, recipe):
    """The root interval can join singleton P1 iff its router is sacrificed."""
    return mark.kind == "private" and mark.vertex in recipe.split


def residual_codes():
    answer = []
    for _, tree in ROOTED.enumerate_trees(6):
        for root_code, root in ROOTED.root_orbits(tree, 6):
            certificate = ROOTED.certificate(tree, 6, root)
            if certificate is None or certificate[0] < 1:
                answer.append(root_code)
    assert len(answer) == 4
    return tuple(answer)


def main():
    exceptions = CENSUS.census()[-1]
    trees = dict(CENSUS.BASE.enumerate_colors(("P",) + ("T",) * 6, 5))
    residual = residual_codes()
    ledgers = Counter()
    overlap = []
    connector_valid = []
    assert len(exceptions) == len(RECIPES) == 9

    for index, (exception, recipe) in enumerate(zip(exceptions, RECIPES), 1):
        _, signature, _, mark, _, _ = exception
        tree = trees[signature]
        verify_ownership(tree, mark, recipe)
        bounds = tuple(packet_bound(tree, packet) for packet in recipe.packets)
        ledger = (sum(item[0] for item in bounds), sum(item[1] for item in bounds))
        assert ledger == recipe.expected_ledger
        assert 4 * ledger[0] - ledger[1] > 0  # delta=sqrt(5)-2 < 1/4
        ledgers[ledger] += 1
        if separate_p1_packet_is_legal(mark, recipe):
            connector_valid.append(index)
        kernel = triangular_kernel(tree, mark)
        matches = tuple(i + 1 for i, code in enumerate(residual) if code == kernel)
        overlap.extend((index, item) for item in matches)
        sources = " + ".join(item[2] for item in bounds)
        print(
            f"E{index}: split={recipe.split or 'none'} packets={sources}; "
            f"sigma>{ledger[0]}-{ledger[1]}delta; "
            f"connector-valid={index in connector_valid}; "
            f"residual-overlap={matches or 'none'}"
        )

    assert ledgers == Counter({(6, 2): 2, (2, 2): 3, (3, 2): 2, (4, 2): 1, (1, 2): 1})
    assert overlap == []
    assert connector_valid == [5, 8, 9]
    print("connector-valid displayed resolutions: E5, E8, E9 (3/9)")
    print("invalid separate-P1 rows: E1, E2, E3, E4, E6, E7")
    print("overlap with R1--R4: empty")
    print("weakest connector-valid ledger: 1-2delta = 5-2sqrt(5) > 0")


if __name__ == "__main__":
    main()
