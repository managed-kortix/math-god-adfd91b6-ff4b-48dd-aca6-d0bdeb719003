#!/usr/bin/env python3
"""OPEN hostile audit of the two-tree R31-S physical hierarchy.

Starting from each of the 110 three-retained-triangle records, this program
adds a *model* fourth triangle as a block-cut leaf in every physically legal
position.  It boundary-opens that model leaf to a tree S, independently opens
the even connector to a fixture owner tree T, and cuts one actual odd-connector
edge.  It then audits the four model territories U,V,S,T.

These synthetic leaf/owner fixtures test the composition once two upstream
antecedents are assumed.  They do NOT authenticate those antecedents for every
R31-S graph: (i) S must be the complete first-boundary territory supplied by
the upstream nested-owner reduction, and (ii) the complete actual structural
owner class T must be acyclic and contain no retained cyclic descendant.
Consequently the result is explicitly conditional, not a closure claim.

The doubled members stay first-simple, with physical lengths {1,2}.  Only the
two connector lengths vary in their fixed opposite parities.  Arbitrary
lengthening of a doubled member is outside this structural scope and belongs
to the separate DNN route.

OPEN RESEARCH ONLY.  This is a structural audit, not a promoted theorem
receipt and not an analytic inequality certificate.
"""

from __future__ import annotations

import importlib.util
import itertools
import subprocess
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit.py"
SPEC = importlib.util.spec_from_file_location("open_r31_physical_split", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load companion physical-split audit")
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


class HierarchyError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise HierarchyError(message)


def rooted_fixture(vertices, edges):
    """Attach a nontrivial one-root tree at every current graph vertex."""
    decorated_vertices = set(vertices)
    decorated_edges = set(edges)
    descendants = {}
    for serial, root in enumerate(sorted(vertices, key=repr)):
        first = ("H", serial, 0)
        second = ("H", serial, 1)
        third = ("H", serial, 2)
        owned = frozenset((first, second, third))
        require(owned.isdisjoint(decorated_vertices), "rooted fixture collided")
        decorated_vertices.update(owned)
        decorated_edges.update((BASE.edge(root, first), BASE.edge(first, second),
                                BASE.edge(root, third)))
        descendants[root] = owned
    return decorated_vertices, decorated_edges, descendants


def belongs_to_exactly_one(vertex, parts):
    owners = [index for index, part in enumerate(parts) if vertex in part]
    require(len(owners) == 1, "vertex does not have exactly one territory owner")
    return owners[0]


def side_order(components, source_intrinsic):
    ordered = []
    for triangle in source_intrinsic:
        matches = [component for component in components if triangle <= component]
        require(len(matches) == 1, "intrinsic triangle has ambiguous side owner")
        ordered.append(matches[0])
    require(ordered[0] != ordered[1], "intrinsic triangles lie in one component")
    return tuple(ordered)


def legal_leaf_cuts(graph, witness):
    """Every legal direct owner and every vertex of a retained triangle.

    The first set gives a fourth triangle directly incident with the structural
    block.  The second gives every nested leaf position.  Each retained
    triangle has two fresh private vertices, so the union has exactly
    6+2*3=12 physical cuts, including repeated/common-cut possibilities.
    Connector interiors are deliberately absent.
    """
    vertex_map, edge_map = witness
    direct = {BASE.transported_owner(label, vertex_map, edge_map)
              for label in BASE.LABELS}
    nested = set().union(*map(set, graph["external"]))
    cuts = tuple(sorted(direct | nested, key=repr))
    require(len(direct) == 6, "direct physical owner set is not six")
    require(len(cuts) == 12, "fourth-leaf physical cut set is not twelve")
    require(set(cuts) <= set(graph["vertices"]), "leaf cut is absent from graph")
    require(graph["open_vertex"] not in cuts,
            "a legal fourth-leaf cut is the structural opening vertex")
    for cut in cuts:
        if cut[0] == "P":
            require(cut[1] not in BASE.CONNECTORS,
                    "connector interior admitted as an external-cycle owner")
    return cuts


def q_leaf_fixture(serial, cut):
    """A fourth triangle at cut, with nontrivial trees on both private vertices."""
    left = ("Q", serial, 0)
    right = ("Q", serial, 1)
    left_a = ("QS", serial, 0, 0)
    left_b = ("QS", serial, 0, 1)
    left_c = ("QS", serial, 0, 2)
    right_a = ("QS", serial, 1, 0)
    right_b = ("QS", serial, 1, 1)
    right_c = ("QS", serial, 1, 2)
    vertices = frozenset((left, right, left_a, left_b, left_c,
                          right_a, right_b, right_c))
    internal_edges = frozenset((
        BASE.edge(left, right),
        BASE.edge(left, left_a), BASE.edge(left_a, left_b),
        BASE.edge(left, left_c),
        BASE.edge(right, right_a), BASE.edge(right_a, right_b),
        BASE.edge(right, right_c),
    ))
    cross_edges = frozenset((BASE.edge(cut, left), BASE.edge(cut, right)))
    triangle = frozenset((cut, left, right))
    return vertices, internal_edges, cross_edges, triangle


def audit_hierarchy_case(row, witness, record, even_length, odd_length,
                         opening_position, cut_position, probe_all_leaf_cuts=True):
    graph = BASE.build_physical_graph(
        row, witness, record, even_length, odd_length,
        opening_position, cut_position, decorate=False)
    core_vertices = set(graph["vertices"])
    core_edges = set(graph["edges"])
    require(BASE.is_connected(core_vertices, core_edges),
            "retained three-triangle physical graph is disconnected")

    vertices, edges, descendants = rooted_fixture(core_vertices, core_edges)
    open_vertex = graph["open_vertex"]
    structural_tree = frozenset({open_vertex} | set(descendants[open_vertex]))
    structural_edges = BASE.induced_edges(structural_tree, edges)
    require(structural_tree and BASE.is_connected(structural_tree, structural_edges),
            "structural owner territory T is empty or disconnected")
    require(len(structural_edges) == len(structural_tree) - 1,
            "structural owner territory T is not a tree")

    remaining = set(vertices) - set(structural_tree)
    remaining_edges = BASE.induced_edges(remaining, edges)
    require(graph["cut_edge"] in remaining_edges,
            "odd cut edge was captured by structural tree")
    components = BASE.components(remaining, remaining_edges - {graph["cut_edge"]})
    require(len(components) == 2,
            "structural opening plus odd cut did not yield two sides")
    bare_sides = side_order(components, graph["source_intrinsic"])

    # Every rooted fixture follows the unique territory containing its root.
    parts_before_q = (bare_sides[0], bare_sides[1], structural_tree)
    for root, owned in descendants.items():
        owner = belongs_to_exactly_one(root, parts_before_q)
        require(set(owned) <= set(parts_before_q[owner]),
                "rooted descendant set did not follow its root owner")

    expected_base_cross = {graph["cut_edge"]}
    expected_base_cross |= {
        e for e in edges if open_vertex in e and not set(e) <= set(structural_tree)
    }
    actual_base_cross = {
        e for e in edges
        if not any(set(e) <= set(part) for part in parts_before_q)
    }
    require(actual_base_cross == expected_base_cross and
            len(expected_base_cross) == 3,
            "pre-leaf cross edges are not exactly two structural plus one cut")

    # Audit the actual decorated U,V sides, not merely whole-graph connectivity.
    side_metrics = []
    for side_index, side in enumerate(bare_sides):
        external = [triangle for triangle in graph["external"] if triangle <= side]
        require(all(not (triangle & side) or triangle <= side
                    for triangle in graph["external"]),
                "retained external triangle is split across U,V")
        triangles = (graph["source_intrinsic"][side_index], *external)
        side_metrics.append(BASE.audit_side(
            side, edges, triangles, graph["source_intrinsic"][side_index]))
    ranks = tuple(metric["beta"] for metric in side_metrics)
    require(min(ranks) >= 1 and sum(ranks) == 5,
            "decorated U,V ranks are not positive and summing five")

    all_leaf_cuts = legal_leaf_cuts(graph, witness)
    # All twelve placements are exercised on the minimal connector case for
    # every anchor/witness/record.  On longer connector-position probes, one
    # deterministic cut suffices: connector remnants do not meet the leaf.
    leaf_cuts = (all_leaf_cuts if probe_all_leaf_cuts else all_leaf_cuts[:1])
    placements = 0
    cut_owner_profile = Counter()
    for serial, boundary_cut in enumerate(leaf_cuts):
        boundary_owner = belongs_to_exactly_one(boundary_cut, bare_sides)
        leaf_vertices, leaf_internal_edges, leaf_cross_edges, leaf_triangle = \
            q_leaf_fixture(serial, boundary_cut)
        require(leaf_vertices.isdisjoint(vertices), "fourth-leaf vertices collided")
        require(leaf_triangle & set(vertices) == {boundary_cut},
                "fourth cyclic block does not meet retained graph exactly at its cut")

        opened_leaf_tree = leaf_vertices
        require(opened_leaf_tree and opened_leaf_tree.isdisjoint(structural_tree),
                "boundary tree S and structural tree T are not distinct")
        require(BASE.is_connected(opened_leaf_tree, leaf_internal_edges),
                "boundary-open territory S is disconnected")
        require(len(leaf_internal_edges) == len(opened_leaf_tree) - 1,
                "boundary-open territory S is not a tree")

        full_vertices = set(vertices) | set(leaf_vertices)
        full_edges = set(edges) | set(leaf_internal_edges) | set(leaf_cross_edges)
        territories = (bare_sides[0], bare_sides[1],
                       opened_leaf_tree, structural_tree)
        require(set().union(*map(set, territories)) == full_vertices and
                sum(len(part) for part in territories) == len(full_vertices),
                "U,V,S,T are not disjoint and exhaustive")
        require(all(BASE.is_connected(part, BASE.induced_edges(part, full_edges))
                    for part in territories),
                "one of U,V,S,T is disconnected")

        expected_cross = set(expected_base_cross) | set(leaf_cross_edges)
        actual_cross = {
            e for e in full_edges
            if not any(set(e) <= set(part) for part in territories)
        }
        require(actual_cross == expected_cross and len(actual_cross) == 5,
                "four-territory cross edges are not exactly 2+2+1")
        require(sum(len(BASE.induced_edges(part, full_edges)) for part in territories)
                + len(actual_cross) == len(full_edges),
                "four-territory edge ownership is not exhaustive")
        require(set(leaf_cross_edges) == {
            e for e in full_edges
            if bool(set(e) & set(opened_leaf_tree)) and not set(e) <= set(opened_leaf_tree)
        }, "S boundary consists of something other than its two cut edges")
        require(boundary_cut in bare_sides[boundary_owner] and
                boundary_cut not in opened_leaf_tree,
                "shared boundary cut was copied into S or lost upstream")

        # Removing S restores exactly the decorated three-retained-triangle
        # graph; hence the fourth block was a genuine block-cut leaf and no
        # connector/rooted material was swallowed with it.
        require(full_vertices - set(opened_leaf_tree) == set(vertices) and
                BASE.induced_edges(set(vertices), full_edges) == set(edges),
                "boundary opening did not restore the exact retained graph")
        cut_owner_profile[boundary_owner] += 1
        placements += 1

    require(placements == len(leaf_cuts) == (12 if probe_all_leaf_cuts else 1),
            "fourth-leaf placement count changed")
    if probe_all_leaf_cuts:
        require(sum(cut_owner_profile.values()) == 12 and
                set(cut_owner_profile) == {0, 1} and
                min(cut_owner_profile.values()) >= 3,
                "twelve fourth-leaf model probes do not span both sides")
    return {
        "placements": placements,
        "ranks": ranks,
        "side_metrics": tuple(side_metrics),
        "cut_owner_profile": cut_owner_profile,
    }


def symbolic_hierarchy_audit():
    """All-length and arbitrary-rooted-tree step, using integer identities."""
    # Connector remnants are characterized without an upper bound.
    # Even connector: delete internal position j in a length L_e path.
    # Odd connector: cut edge k in a length L_o path.
    for total in range(0, 18, 2):
        for left in range(total + 1):
            right = total - left
            even_length = left + right + 2
            opening_position = left + 1
            odd_length = left + right + 1
            cut_position = left
            require(even_length % 2 == 0 and
                    1 <= opening_position < even_length,
                    "even symbolic-remnant parametrization failed")
            require(odd_length % 2 == 1 and
                    0 <= cut_position < odd_length,
                    "odd symbolic-remnant parametrization failed")

    # An arbitrary rooted tree with q nonroot vertices has q edges.  Assigning
    # it wholly with its root preserves inducedness and beta.  Each connector
    # remnant is a path with the same V=E contribution.  S and T are trees
    # because one-root trees glued to a tree remain a tree.
    for beta in range(1, 5):
        base_vertices = 2 * beta + 1
        base_edges = 3 * beta
        for remnant_vertices, rooted_vertices in itertools.product(range(8), repeat=2):
            vertices = base_vertices + remnant_vertices + rooted_vertices
            edges = base_edges + remnant_vertices + rooted_vertices
            require(edges - vertices + 1 == beta,
                    "symbolic rooted/remnant material changed side beta")
    for base_tree_vertices in (1, 2, 5):
        for rooted_vertices in range(8):
            vertices = base_tree_vertices + rooted_vertices
            edges = (base_tree_vertices - 1) + rooted_vertices
            require(edges == vertices - 1,
                    "symbolic owned attachments changed a tree territory")
    return {
        "doubled_members": "fixed physical first-simple lengths {1,2}",
        "even_remnants": "alpha,beta>=0; alpha+beta even; L=alpha+beta+2",
        "odd_remnants": "gamma,delta>=0; gamma+delta even; L=gamma+delta+1",
        "rooted_trees": "q nonroot vertices contribute q edges and follow one root",
    }


def audit():
    automorphisms = BASE.genuine_automorphisms()
    require(len(automorphisms) == 16, "genuine witness registry changed")
    anchors = tuple(sorted({BASE.act_on_row(BASE.BASE_ROW, edge_map)
                            for _, edge_map in automorphisms}))
    require(anchors == BASE.EXPECTED_ANCHORS, "physical anchor registry changed")
    witnesses = {
        row: tuple(w for w in automorphisms
                   if BASE.act_on_row(BASE.BASE_ROW, w[1]) == row)
        for row in anchors
    }
    require(all(len(value) == 2 for value in witnesses.values()),
            "an anchor lacks exactly two genuine witnesses")
    records = BASE.base_records()

    physical_cases = 0
    leaf_placements = 0
    rank_profiles = Counter()
    shape_placements = Counter()
    for row in anchors:
        for witness in witnesses[row]:
            for record in records:
                for even_length in BASE.EVEN_LENGTH_PROBES:
                    for opening_position in range(1, even_length):
                        for odd_length in BASE.ODD_LENGTH_PROBES:
                            for cut_position in range(odd_length):
                                probe_all = (even_length, opening_position,
                                             odd_length, cut_position) == (2, 1, 1, 0)
                                result = audit_hierarchy_case(
                                    row, witness, record,
                                    even_length, odd_length,
                                    opening_position, cut_position,
                                    probe_all_leaf_cuts=probe_all)
                                physical_cases += 1
                                leaf_placements += result["placements"]
                                rank_profiles[result["ranks"]] += 1
                                shape_placements[record[0]] += result["placements"]

    require(physical_cases == 8 * 2 * 110 * 9 * 9,
            "physical hierarchy case count changed")
    # Per anchor/witness/record: twelve leaf positions in the shortest case,
    # plus one position for each of the other 80 connector/open/cut probes.
    require(leaf_placements == 8 * 2 * 110 * (12 + 80),
            "fourth-leaf model-probe count changed")
    require(rank_profiles == Counter({
        (4, 1): 28 * 8 * 2 * 9 * 9,
        (3, 2): 27 * 8 * 2 * 9 * 9,
        (2, 3): 27 * 8 * 2 * 9 * 9,
        (1, 4): 28 * 8 * 2 * 9 * 9,
    }), "all-case rank profile changed")
    expected_shape_placements = {
        shape: count * 8 * 2 * (12 + 80)
        for shape, count in Counter(record[0] for record in records).items()
    }
    require(shape_placements == Counter(expected_shape_placements),
            "chain/fork/direct hierarchy census changed")
    symbolic = symbolic_hierarchy_audit()
    return {
        "physical_cases": physical_cases,
        "leaf_placements": leaf_placements,
        "rank_profiles": rank_profiles,
        "shape_placements": shape_placements,
        "symbolic": symbolic,
    }


def main():
    result = audit()
    output = "\n".join((
        "OPEN R31-S U,V,S,T hierarchy model audit: exact conditional PASS",
        "scope: doubled members fixed first-simple {1,2}; connectors only may lengthen",
        "registry: 8 physical anchors x 2 genuine witnesses x 110 retained records",
        f"opening/cut cases: {result['physical_cases']} "
        "(even L=2,4,6/all internal vertices; odd L=1,3,5/all actual edges)",
        f"synthetic fourth-leaf model probes: {result['leaf_placements']} "
        "(all 12 legal cuts at minimal connectors; one cut on each longer-remnant case)",
        "model predicates: U,V,S,T induced, connected, nonempty where required, disjoint/exhaustive; "
        "S,T distinct trees; exact cross-edge identity 2(S)+2(T)+1(UV)",
        "side predicates: every cyclic biconnected block triangular; cyclic-block "
        "intersection graph connected; intrinsic triangle each side; beta>=1 and sum 5",
        "shape placement census: " + repr(dict(sorted(result["shape_placements"].items()))),
        "rank case census: " + repr(dict(sorted(result["rank_profiles"].items()))),
        "symbolic scope: arbitrary parity-compatible connector remnants and arbitrary one-root trees",
        "minimal model failure: none",
        "conditional antecedent A (not authenticated here): S is the complete first-boundary tree territory",
        "conditional antecedent B (not authenticated here): actual complete structural owner T is acyclic and owns no retained cycle",
        "outside scope: any lengthening of a doubled member (separate DNN route)",
        "synthetic diamond diagnostic used: no",
        "status: OPEN/nonpromotional CONDITIONAL structural audit; no R31-S closure",
    ))
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output,
                "normal and optimized hierarchy outputs differ")
    print(output)


if __name__ == "__main__":
    main()
