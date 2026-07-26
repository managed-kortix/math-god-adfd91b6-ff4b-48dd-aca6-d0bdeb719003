#!/usr/bin/env python3
"""SUPERSEDED restricted uncut census for the disconnected T^6P | P gap.

This reproduces the historical 877=868+9 ledger only. It is not a completeness
certificate; use the strict-last-bridge 877=861+16 artifacts instead.

The root is a cyclic-hull vertex of the T^6P cluster.  We retain only rows in
which the clustered pentagon is an incidence leaf, but enumerate all 226
unrooted T^6P incidence trees as a completeness check.  A certificate uses an
ordinary triangle interval split and packet bounds through rank seven; it does
not use the rooted hostile-cycle guard.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import argparse


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "octacyclic_incidence", HERE / "octacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BASE)


@dataclass(frozen=True)
class Mark:
    kind: str
    vertex: int


@dataclass(frozen=True)
class Bound:
    value: Fraction
    strict: bool
    source: str


TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1}


def marked_signature(tree, mark):
    """Canonical colored-tree code with either a cut or private-vertex mark."""
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)

    def code(vertex, parent):
        if vertex < cycle_count:
            color = tree.colors[vertex]
            if mark.kind == "private" and mark.vertex == vertex:
                color += "R"
        else:
            color = "R" if mark.kind == "cut" and mark.vertex == vertex else "X"
        children = sorted(code(neighbor, vertex) for neighbor in adj[vertex] if neighbor != parent)
        return color + "(" + "".join(children) + ")"

    return min(code(center, -1) for center in BASE.tree_centers(adj))


def root_orbits(tree):
    """Return all cyclic-hull root orbits in the triangular component.

    A triangle of incidence degree d has 3-d private vertices.  For d=1 its
    two private vertices are exchanged by the reflection fixing its cut, so a
    single private mark suffices.  For d=2 there is one private vertex, and for
    d=3 there is none.  This accounts for every cyclic position of a triangle.
    """
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    pentagon = tree.colors.index("P")
    p_cut = adj[pentagon][0]
    candidates = [(Mark("cut", cut), 1) for cut in range(cycle_count, len(adj))]
    candidates += [
        (Mark("private", cycle), 3 - len(adj[cycle]))
        for cycle, color in enumerate(tree.colors)
        if color == "T" and len(adj[cycle]) < 3
    ]
    # The unique P cut is included; private P vertices are intentionally not.
    assert p_cut in [mark.vertex for mark, _ in candidates if mark.kind == "cut"]
    answer = {}
    for mark, positions in candidates:
        signature = marked_signature(tree, mark)
        if signature in answer:
            representative, old_positions = answer[signature]
            answer[signature] = representative, old_positions + positions
        else:
            answer[signature] = mark, positions
    return tuple((signature, *value) for signature, value in sorted(answer.items()))


def profile_bound(triangles, pentagons, topology=None):
    rank = triangles + pentagons
    if pentagons == 0:
        return Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    if rank == 1:
        return Bound(Fraction(-1, 4), True, "P>-1/4")
    if (triangles, pentagons) == (1, 1):
        return Bound(Fraction(3, 4), True, "TP>3/4")
    if (triangles, pentagons) == (0, 2):
        return Bound(Fraction(0), False, "connected rank-2 PP>=0")
    if (triangles, pentagons) == (1, 2):
        return Bound(Fraction(3, 2), True, "TPP>3/2")
    if pentagons == 1 and topology is not None:
        base = BASE.tpp_bound(topology[0], topology[1])
        return Bound(base.value, base.strict, base.source)
    if rank in (2, 3):
        return Bound(Fraction(0), False, f"generic rank-{rank}>=0")
    assert 4 <= rank <= 7
    return Bound(Fraction(0), True, f"generic rank-{rank}>0")


def component_counts(tree, component):
    colors = Counter(tree.colors[cycle] for cycle in component[0])
    return colors["T"], colors["P"]


def root_component(tree, sacrificed, mark, components):
    if mark.kind == "private" and mark.vertex == sacrificed:
        return None
    adj = BASE.adjacency(tree)
    if mark.kind == "private":
        target = mark.vertex
    else:
        target = mark.vertex
    for index, component in enumerate(components):
        vertices = set(component[0]) | set(component[1])
        # A boundary cut of the deleted triangle is omitted from internal_cuts.
        if target in vertices:
            return index
        if mark.kind == "cut" and any(target in adj[cycle] for cycle in component[0]):
            return index
    raise AssertionError((sacrificed, mark, components))


def split_certificate(tree, sacrificed, mark):
    """Certify a split with the uncut connector joined to its root interval.

    If the root is not on the sacrificed triangle, ``owner`` is the incidence
    component whose interval contains the root, and P1 is added to that
    component's cycle profile.  If the root is private on the sacrificed
    triangle, its interval, the connector, and P1 form a pentagonal unicyclic
    packet; the sacrificed router contributes no retained cycle in that case.
    """
    if tree.colors[sacrificed] != "T":
        return None
    components = BASE.components_after_split(tree, sacrificed)
    owner = root_component(tree, sacrificed, mark, components)
    mark_count = len(components) + (owner is None)
    if mark_count < 2 or mark_count > 3:
        return None

    bounds = []
    profiles = []
    for index, component in enumerate(components):
        triangles, pentagons = component_counts(tree, component)
        external = index == owner
        profiles.append((triangles, pentagons + external))
        if external:
            bounds.append(profile_bound(triangles, pentagons + 1))
        else:
            bounds.append(profile_bound(triangles, pentagons, (tree, component)))
    if owner is None:
        profiles.append((0, 1))
        bounds.append(profile_bound(0, 1))

    total = sum((bound.value for bound in bounds), Fraction(0))
    strict = any(bound.strict for bound in bounds)
    if total > 0 or (total == 0 and strict):
        return tuple(sorted(profiles)), tuple(bounds), total, strict
    return None


def connector_repair_audit():
    """Identify the old cut-before-P1 rows and verify their uncut repair."""
    classes = BASE.enumerate_colors(("P",) + ("T",) * 6, 5)
    invalid_rows = []
    repaired_counts = Counter()
    certificate_counts = Counter()
    private_router_rows = Counter()
    private_router_certificates = Counter()
    private_router_only = Counter()

    for signature, tree in classes:
        adj = BASE.adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            continue
        cuts = BASE.cut_count(tree)
        for root_signature, mark, _ in root_orbits(tree):
            certificates = []
            for router, color in enumerate(tree.colors):
                if color != "T":
                    continue
                certificate = split_certificate(tree, router, mark)
                if certificate is None:
                    continue
                components = BASE.components_after_split(tree, router)
                owner = root_component(tree, router, mark, components)
                profiles = certificate[0]
                assert sum(pentagons for _, pentagons in profiles) == 2
                assert sum(pentagons > 0 for _, pentagons in profiles) in (1, 2)
                if owner is None:
                    assert mark == Mark("private", router)
                    assert (0, 1) in profiles
                    private_router_certificates[cuts] += 1
                else:
                    triangles, pentagons = component_counts(tree, components[owner])
                    assert (triangles, pentagons + 1) in profiles
                certificates.append(owner)
                certificate_counts[cuts] += 1

            if not certificates:
                continue

            # Under the old instruction to cut the final connector bridge, P1
            # is disconnected from the root component to which its cycle was
            # charged. Thus every formerly accepted rooted row was invalid as
            # written. Keeping that bridge repairs every one with no type loss.
            row_id = f"{cuts}\t{signature}\t{root_signature}"
            invalid_rows.append(row_id)
            repaired_counts[cuts] += 1
            if any(owner is None for owner in certificates):
                private_router_rows[cuts] += 1
            if all(owner is None for owner in certificates):
                private_router_only[cuts] += 1

    invalid_rows.sort()
    digest = sha256(("\n".join(invalid_rows) + "\n").encode("ascii")).hexdigest()
    expected_rows = Counter({2: 21, 3: 123, 4: 302, 5: 316, 6: 106})
    assert repaired_counts == expected_rows
    assert len(invalid_rows) == 868
    assert certificate_counts == Counter({2: 21, 3: 194, 4: 653, 5: 841, 6: 327})
    assert private_router_certificates == Counter({2: 4, 3: 19, 4: 46, 5: 47, 6: 17})
    assert private_router_rows == Counter({2: 4, 3: 19, 4: 46, 5: 47, 6: 17})
    assert private_router_only == Counter({2: 4, 3: 3, 4: 2})
    return (
        tuple(invalid_rows),
        digest,
        repaired_counts,
        certificate_counts,
        private_router_rows,
        private_router_only,
    )


def census():
    classes = BASE.enumerate_colors(("P",) + ("T",) * 6, 5)
    all_counts = Counter(BASE.cut_count(tree) for _, tree in classes)
    leaf_trees = []
    internal_trees = []
    marked_counts = Counter()
    position_counts = Counter()
    resolved_counts = Counter()
    exceptions = []

    for signature, tree in classes:
        adj = BASE.adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            internal_trees.append((signature, tree))
            continue
        leaf_trees.append((signature, tree))
        for root_signature, mark, positions in root_orbits(tree):
            cuts = BASE.cut_count(tree)
            marked_counts[cuts] += 1
            position_counts[cuts] += positions
            certificates = []
            for cycle, color in enumerate(tree.colors):
                if color == "T":
                    certificate = split_certificate(tree, cycle, mark)
                    if certificate is not None:
                        certificates.append((cycle, certificate))
            if certificates:
                resolved_counts[cuts] += 1
            else:
                exceptions.append(
                    (cuts, signature, root_signature, mark, positions, tree.edges)
                )

    expected_all = Counter({1: 1, 2: 8, 3: 33, 4: 73, 5: 78, 6: 33})
    expected_leaf = Counter({1: 1, 2: 5, 3: 20, 4: 38, 5: 36, 6: 11})
    assert all_counts == expected_all
    assert Counter(BASE.cut_count(tree) for _, tree in leaf_trees) == expected_leaf
    assert len(classes) == 226 and len(leaf_trees) == 111 and len(internal_trees) == 115
    assert sum(marked_counts.values()) == sum(resolved_counts.values()) + len(exceptions)
    assert marked_counts == Counter({1: 2, 2: 24, 3: 126, 4: 303, 5: 316, 6: 106})
    assert position_counts == Counter({1: 13, 2: 65, 3: 260, 4: 494, 5: 468, 6: 143})
    assert resolved_counts == Counter({2: 21, 3: 123, 4: 302, 5: 316, 6: 106})
    assert Counter(item[0] for item in exceptions) == Counter({1: 2, 2: 3, 3: 3, 4: 1})
    exceptions.sort(key=lambda item: (item[0], item[2]))
    return (
        all_counts,
        expected_leaf,
        marked_counts,
        position_counts,
        resolved_counts,
        exceptions,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--list-invalid-rows",
        action="store_true",
        help="print canonical IDs of all rows invalid under the cut-before-P1 wording",
    )
    args = parser.parse_args()
    (
        all_counts,
        leaf_counts,
        marked_counts,
        position_counts,
        resolved_counts,
        exceptions,
    ) = census()
    print("all T^6P incidence trees by cut count:", dict(sorted(all_counts.items())))
    print("P-leaf incidence trees by cut count:", dict(sorted(leaf_counts.items())))
    print("marked-root orbits by cut count:", dict(sorted(marked_counts.items())))
    print("labelled cyclic root positions by cut count:", dict(sorted(position_counts.items())))
    print("packet-resolved marked roots by cut count:", dict(sorted(resolved_counts.items())))
    print("exact conservative exceptions:", len(exceptions))
    for cuts, signature, root_signature, mark, positions, edges in exceptions:
        print(
            f"  c={cuts} root={mark.kind}:{mark.vertex} positions={positions} "
            f"{root_signature}"
        )
        print(f"    incidence={signature}")
        print(f"    edges={edges}")

    (
        invalid_rows,
        digest,
        repaired,
        certificates,
        private_router,
        private_only,
    ) = connector_repair_audit()
    print("old cut-before-P1 invalid accepted rows:", len(invalid_rows))
    print("repaired uncut-connector rows by cut count:", dict(sorted(repaired.items())))
    print("repaired router certificates by cut count:", dict(sorted(certificates.items())))
    print("rows admitting a private-root router:", dict(sorted(private_router.items())))
    print("rows requiring a private-root router:", dict(sorted(private_only.items())))
    print("canonical invalid-row sha256:", digest)
    if args.list_invalid_rows:
        for row_id in invalid_rows:
            print("INVALID-OLD\t" + row_id)


if __name__ == "__main__":
    main()
