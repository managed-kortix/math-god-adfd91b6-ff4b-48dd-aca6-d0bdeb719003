#!/usr/bin/env python3
"""Exact orbit and marked-cut transport audit for the doubled-C4 R31-S frontier.

This verifier deliberately separates three claims.

* The canonical structural scope is exactly the eight first-simple exceptional
  parity rows, one genuine doubled-C4 multigraph-automorphism orbit (not a
  switching class).
* Every physical owner, connector opening/cut and fully decorated rooted
  block-cut record is transported recordwise through each genuine witness.
* A non-first-simple doubled member is routed to one of the two exact DNN
  certificate bounds; it is never canonicalized by switching.

The script authenticates this finite transport prerequisite only.  It does not
by itself prove either analytic C4 or D3 packet inequality.
"""

from __future__ import annotations

import hashlib
import itertools
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


ROOT = Path(__file__).resolve().parents[1]
# Path order a,A,b,c,C,d on branch vertices 0,1,2,3.
ENDPOINTS = ((0, 1), (0, 1), (1, 2), (2, 3), (2, 3), (3, 0))
DOUBLED_FIBRES = ((0, 1), (3, 4))
CONNECTORS = (2, 5)
BASE = "010011"
EXPECTED_ANCHORS = (
    "010011", "010101", "011010", "011100",
    "100011", "100101", "101010", "101100",
)
BRANCH_LABELS = ("A", "B", "C", "D")
OWNER_LABELS = ("A", "B", "C", "D", "x", "y")
BASE_LABEL_TO_TOKEN = {
    "A": ("branch", 0), "B": ("branch", 1),
    "C": ("branch", 2), "D": ("branch", 3),
    "x": ("interior", 0), "y": ("interior", 3),
}
BASE_SIDE = {"A": 0, "B": 0, "x": 0, "C": 1, "D": 1, "y": 1}
BASE_INTERIOR = {"x", "y"}
LONG_REPRESENTATIVE = "011010"
LONG_VECTORS = {
    "even": (4, 1, 1, 2, 1, 2),
    "odd": (2, 3, 1, 2, 1, 2),
}
LONG_BOUNDS = {"even": (1862, 1000), "odd": (1662, 1000)}
FOUNDATION_SOURCES = {
    "positive-square-energy/tricyclic-general/doubled-c4-switching-sieve.md":
        "7d2b77857c9f90514ceda84e6acb01d4c752a7aecf39a1f553601b5376164d84",
    "research/doubled-c4-64-row-exact-verifier.py":
        "3849b3aef7ded9ed9abfe046f08b4e1ba292068232000172be9fee6ee646d9e8",
    "research/tricyclic-finite-rational-certificates-verifier.py":
        "37aa5b45f98d1a6f0848d578e2f345609be4bc42af940d63ad7b0d0428c1f300",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_foundation_sources():
    for relative, expected in FOUNDATION_SOURCES.items():
        path = ROOT / relative
        require(path.is_file() and sha256(path) == expected,
                f"foundation source changed: {relative}")


def first_simple_lengths(row):
    require(type(row) is str and len(row) == 6 and set(row) <= {"0", "1"},
            "malformed parity row")
    # Exceptional rows have no odd--odd doubled fibre, so this is the complete
    # first-simple rule in the structural branch.
    return tuple(1 if bit == "1" else 2 for bit in row)


def switching_invariant(row):
    parity = tuple(map(int, row))
    switches = [0] * 4
    switches[1] = parity[0]
    switches[2] = parity[2] ^ switches[1]
    switches[3] = parity[3] ^ switches[2]
    normalized = tuple(bit ^ switches[u] ^ switches[v]
                       for bit, (u, v) in zip(parity, ENDPOINTS))
    require(normalized[0] == normalized[2] == normalized[3] == 0,
            "switching normalization failed")
    return "".join(str(normalized[index]) for index in (1, 4, 5))


def adjacency_multiplicities():
    adjacency = [[0] * 4 for _ in range(4)]
    for left, right in ENDPOINTS:
        adjacency[left][right] += 1
        adjacency[right][left] += 1
    return adjacency


def genuine_kernel_automorphisms():
    adjacency = adjacency_multiplicities()
    records = set()
    for vertex_map in itertools.permutations(range(4)):
        if not all(adjacency[u][v] == adjacency[vertex_map[u]][vertex_map[v]]
                   for u in range(4) for v in range(4)):
            continue
        targets = []
        for u, v in ENDPOINTS:
            image_pair = sorted((vertex_map[u], vertex_map[v]))
            targets.append(tuple(index for index, edge in enumerate(ENDPOINTS)
                                 if sorted(edge) == image_pair))
        for edge_map in itertools.product(*targets):
            if len(set(edge_map)) == 6:
                records.add((tuple(vertex_map), tuple(edge_map)))
    return tuple(sorted(records))


def authenticate_automorphism(vertex_map, edge_map):
    require(tuple(sorted(vertex_map)) == tuple(range(4)),
            "branch-vertex map is not bijective")
    require(tuple(sorted(edge_map)) == tuple(range(6)),
            "kernel-edge map is not bijective")
    for old_edge, (u, v) in enumerate(ENDPOINTS):
        image_pair = sorted((vertex_map[u], vertex_map[v]))
        require(sorted(ENDPOINTS[edge_map[old_edge]]) == image_pair,
                "edge map is not endpoint-compatible")
    source_multiplicities = Counter(tuple(sorted(edge)) for edge in ENDPOINTS)
    image_multiplicities = Counter(tuple(sorted((vertex_map[u], vertex_map[v])))
                                   for u, v in ENDPOINTS)
    require(source_multiplicities == image_multiplicities,
            "edge multiplicities were not preserved")


def act_on_row(row, edge_map):
    image = [None] * 6
    for old_edge, new_edge in enumerate(edge_map):
        image[new_edge] = row[old_edge]
    require(all(bit is not None for bit in image), "edge action is incomplete")
    return "".join(image)


def act_on_vector(vector, edge_map):
    require(len(vector) == 6, "malformed edge vector")
    image = [None] * 6
    for old_edge, new_edge in enumerate(edge_map):
        image[new_edge] = vector[old_edge]
    require(all(value is not None for value in image), "vector action is incomplete")
    return tuple(image)


def unique_even_edges(row):
    doubled = tuple(next(edge for edge in fibre if row[edge] == "0")
                    for fibre in DOUBLED_FIBRES)
    require(all(sum(row[edge] == "0" for edge in fibre) == 1
                for fibre in DOUBLED_FIBRES),
            "a canonical doubled fibre is not odd/even")
    connector = next(edge for edge in CONNECTORS if row[edge] == "0")
    require(sum(row[edge] == "0" for edge in CONNECTORS) == 1,
            "canonical connectors are not opposite parity")
    odd_connector = next(edge for edge in CONNECTORS if edge != connector)
    return doubled, connector, odd_connector


def fibre_index(edge):
    for index, fibre in enumerate(DOUBLED_FIBRES):
        if edge in fibre:
            return index
    raise AuditError("edge is not in a doubled fibre")


def target_geometry(row):
    doubled_even, even_connector, odd_connector = unique_even_edges(row)
    token_to_label = {
        ("branch", index): BRANCH_LABELS[index] for index in range(4)
    }
    token_to_label[("interior", doubled_even[0])] = "x"
    token_to_label[("interior", doubled_even[1])] = "y"
    legal_tokens = set(token_to_label)
    # Anchor-relative sides: the first doubled fibre and its branch endpoints
    # form side 0; the second forms side 1.  A witness may exchange them.
    side_by_token = {
        ("branch", 0): 0, ("branch", 1): 0,
        ("interior", doubled_even[0]): 0,
        ("branch", 2): 1, ("branch", 3): 1,
        ("interior", doubled_even[1]): 1,
    }
    interior_tokens = {("interior", edge) for edge in doubled_even}
    return {
        "row": row,
        "lengths": first_simple_lengths(row),
        "doubled_even": doubled_even,
        "open_connector": even_connector,
        "cut_connector": odd_connector,
        "token_to_label": token_to_label,
        "legal_tokens": legal_tokens,
        "side_by_token": side_by_token,
        "interior_tokens": interior_tokens,
    }


def transport_token(token, vertex_map, edge_map):
    kind, index = token
    if kind == "branch":
        return (kind, vertex_map[index])
    require(kind == "interior", "unknown physical owner token")
    return (kind, edge_map[index])


def transport_symbolic_paths(row, vertex_map, edge_map):
    """Transport exact connector paths, orientations and cut/open positions.

    A connector is not a parity bit.  Give source connector e an arbitrary
    positive integer length L_e of the prescribed parity, orient its positions
    0,...,L_e from ENDPOINTS[e][0] to ENDPOINTS[e][1], and transport that
    exact path to edge_map[e].  Endpoint compatibility decides whether a
    position j maps to j or L_e-j.  The internal opening position on the even
    connector and the actual cut position on the odd connector are therefore
    carried symbolically, together with both path-remnant lengths.
    """
    source_geometry = target_geometry(BASE)
    target = target_geometry(row)
    symbolic = {}
    for source_edge in CONNECTORS:
        target_edge = edge_map[source_edge]
        require(target_edge in CONNECTORS,
                "a connector path did not map to a connector path")
        length_symbol = f"L{source_edge}"
        expected_parity = int(BASE[source_edge])
        require(expected_parity == int(row[target_edge]),
                "connector length parity was not preserved")
        source_u, source_v = ENDPOINTS[source_edge]
        target_u, target_v = ENDPOINTS[target_edge]
        image_endpoints = (vertex_map[source_u], vertex_map[source_v])
        if image_endpoints == (target_u, target_v):
            orientation = "forward"
            position_image = ("j",)
            remnants = (("j",), (length_symbol, "-j"))
        else:
            require(image_endpoints == (target_v, target_u),
                    "connector endpoint orientation is incompatible")
            orientation = "reverse"
            position_image = (length_symbol, "-j")
            remnants = ((length_symbol, "-j"), ("j",))
        role = ("open" if source_edge == source_geometry["open_connector"]
                else "cut")
        require((target_edge == target["open_connector"]) == (role == "open"),
                "connector opening/cut role did not transport")
        symbolic[source_edge] = {
            "target_edge": target_edge,
            "length_symbol": length_symbol,
            "parity": expected_parity,
            "orientation": orientation,
            "position_image": position_image,
            "remnants": remnants,
            "role": role,
        }
    require(set(record["target_edge"] for record in symbolic.values()) ==
            set(CONNECTORS), "symbolic connector transport is not bijective")
    require({record["role"] for record in symbolic.values()} == {"open", "cut"},
            "symbolic connector roles are incomplete")
    return symbolic


def owner_transport(target_row, vertex_map, edge_map):
    target = target_geometry(target_row)
    mapping = {}
    physical_mapping = {}
    for source_label, source_token in BASE_LABEL_TO_TOKEN.items():
        image_token = transport_token(source_token, vertex_map, edge_map)
        require(image_token in target["legal_tokens"],
                "physical owner left the target legal-owner set")
        mapping[source_label] = target["token_to_label"][image_token]
        physical_mapping[source_token] = image_token
    require(set(mapping) == set(OWNER_LABELS) and
            set(mapping.values()) == set(OWNER_LABELS),
            "owner-label transport is not bijective")
    require(set(physical_mapping) == set(BASE_LABEL_TO_TOKEN.values()) and
            set(physical_mapping.values()) == target["legal_tokens"],
            "physical owner transport is not bijective")
    return mapping, physical_mapping, target


def base_records():
    direct = {("direct3", roots)
              for roots in itertools.combinations_with_replacement(OWNER_LABELS, 3)}
    chain2_direct = {("chain2+direct", upstream, direct_root)
                     for upstream in OWNER_LABELS for direct_root in OWNER_LABELS}
    fork = {("fork", upstream, occupancy)
            for upstream in OWNER_LABELS for occupancy in ("same", "split")}
    chain3 = {("chain3", upstream) for upstream in OWNER_LABELS}
    records = direct | chain2_direct | fork | chain3
    require(len(records) == sum(map(len, (direct, chain2_direct, fork, chain3))),
            "incidence-shape collision")
    return records, Counter(record[0] for record in records)


def decorate_record(record, label_to_token):
    kind = record[0]
    if kind == "direct3":
        return (kind, tuple(sorted((label_to_token[root] for root in record[1]),
                                   key=repr)))
    if kind == "chain2+direct":
        # The child is rooted at a distinguished fresh vertex of the upstream
        # triangle.  This is parent/child data, not a second kernel owner.
        return (kind, label_to_token[record[1]], ("fresh", "first"),
                label_to_token[record[2]])
    if kind == "fork":
        require(record[2] in {"same", "split"}, "malformed fork occupancy")
        return (kind, label_to_token[record[1]], ("children", record[2]))
    require(kind == "chain3", "unknown incidence shape")
    return (kind, label_to_token[record[1]],
            ("fresh", "first"), ("fresh", "first"))


def transport_decorated_record(decorated, vertex_map, edge_map):
    def transport_field(value):
        if (type(value) is tuple and len(value) == 2 and
                value[0] in {"branch", "interior"} and type(value[1]) is int):
            return transport_token(value, vertex_map, edge_map)
        if type(value) is tuple:
            return tuple(transport_field(item) for item in value)
        return value
    result = transport_field(decorated)
    if result[0] == "direct3":
        result = (result[0], tuple(sorted(result[1], key=repr)))
    return result


def transport_record(record, owner_map):
    kind = record[0]
    if kind == "direct3":
        return (kind, tuple(sorted(owner_map[root] for root in record[1])))
    if kind == "chain2+direct":
        return (kind, owner_map[record[1]], owner_map[record[2]])
    if kind == "fork":
        return (kind, owner_map[record[1]], record[2])
    require(kind == "chain3", "unknown incidence shape")
    return (kind, owner_map[record[1]])


def top_roots(record):
    if record[0] == "direct3":
        return record[1]
    if record[0] == "chain2+direct":
        return record[1:3]
    return (record[1],)


def classify(record, side_by_label, interior_labels):
    roots = top_roots(record)
    if len({side_by_label[root] for root in roots}) == 2:
        return "balanced"
    if interior_labels & set(roots):
        return "D3"
    return "C4"


def source_classification(record):
    return classify(record, BASE_SIDE, BASE_INTERIOR)


def target_label_geometry(target):
    side_by_label = {target["token_to_label"][token]: side
                     for token, side in target["side_by_token"].items()}
    interior_labels = {target["token_to_label"][token]
                       for token in target["interior_tokens"]}
    return side_by_label, interior_labels


def recordwise_transport_audit(records, target_row, vertex_map, edge_map,
                               owner_map_override=None):
    owner_map, _, target = owner_transport(target_row, vertex_map, edge_map)
    if owner_map_override is not None:
        owner_map = dict(owner_map_override)
    side_by_label, interior_labels = target_label_geometry(target)
    image_records = set()
    classification_counts = Counter()
    for record in records:
        image = transport_record(record, owner_map)
        image_records.add(image)
        require(image[0] == record[0], "record shape changed under transport")
        if record[0] == "fork":
            require(image[2] == record[2], "fork same/split flag changed")
        # Authenticate every direct owner, upstream owner, direct sibling and
        # every fresh parent/child marker through the physical vm/em action.
        physical_expected = transport_decorated_record(
            decorate_record(record, BASE_LABEL_TO_TOKEN), vertex_map, edge_map)
        target_label_to_token = {label: token
                                 for token, label in target["token_to_label"].items()}
        physical_actual = decorate_record(image, target_label_to_token)
        require(physical_actual == physical_expected,
                "decorated rooted block-cut record did not commute")
        source_class = source_classification(record)
        target_class = classify(image, side_by_label, interior_labels)
        require(target_class == source_class,
                "recordwise side/interior classification did not commute")
        classification_counts[target_class] += 1
    require(len(image_records) == len(records), "record transport collided")
    require(classification_counts == Counter({"balanced": 54, "C4": 28, "D3": 28}),
            "recordwise classification counts changed")
    return image_records, classification_counts


def all_length_routes(anchors, automorphisms):
    """Authenticate every one-member-long structural escape exactly.

    For each physical anchor and each of its four doubled members, there is
    exactly one genuine automorphism taking the anchor to 011010 and the
    selected member to canonical slot 0 (even) or 1 (odd).  Transporting the
    *full* first-long vector must give the corresponding published DNN vector.
    Larger additions by two, including connector lengthening, are then only
    componentwise fixed-parity monotonicity; no switching quotient is used.
    """
    routes = []
    for row in anchors:
        base_lengths = first_simple_lengths(row)
        for selected_edge in DOUBLED_FIBRES[0] + DOUBLED_FIBRES[1]:
            route = "odd" if row[selected_edge] == "1" else "even"
            canonical_slot = 1 if route == "odd" else 0
            candidates = []
            for vertex_map, edge_map in automorphisms:
                if (act_on_row(row, edge_map) == LONG_REPRESENTATIVE and
                        edge_map[selected_edge] == canonical_slot):
                    candidates.append((vertex_map, edge_map))
            require(len(candidates) == 1,
                    f"{row}/edge{selected_edge}: long-route witness is not unique")
            vertex_map, edge_map = candidates[0]
            authenticate_automorphism(vertex_map, edge_map)
            first_long = list(base_lengths)
            first_long[selected_edge] += 2
            transported = act_on_vector(tuple(first_long), edge_map)
            require(transported == LONG_VECTORS[route],
                    f"{row}/edge{selected_edge}: full first-long vector mismatch")
            require(all(transported[index] == first_simple_lengths(
                        LONG_REPRESENTATIVE)[index]
                        for index in DOUBLED_FIBRES[0] + DOUBLED_FIBRES[1]
                        if index != canonical_slot),
                    f"{row}/edge{selected_edge}: another doubled member changed")
            bound = LONG_BOUNDS[route]
            require(bound[0] < 2 * bound[1], "long DNN bound is not below two")

            # Model independent +2 increments on all six physical paths.  The
            # genuine edge permutation carries each coefficient to the image
            # path, so every image length is its canonical long-vector entry
            # plus an even nonnegative increment.  In particular connectors
            # stay symbolic physical paths; they are not reset to length 1/2.
            increment_coefficients = tuple(range(6))
            image_coefficients = act_on_vector(increment_coefficients, edge_map)
            require(tuple(sorted(image_coefficients)) == tuple(range(6)),
                    "fixed-parity increment coefficients did not transport")
            require({edge_map[index] for index in CONNECTORS} == set(CONNECTORS),
                    "connector path did not transport to a connector")
            for source_connector in CONNECTORS:
                target_connector = edge_map[source_connector]
                require(row[source_connector] ==
                        LONG_REPRESENTATIVE[target_connector],
                        "symbolic connector parity changed under transport")
            routes.append((row, selected_edge, route, vertex_map, edge_map,
                           transported, bound))
    require(len(routes) == 8 * 4, "all-length doubled-member route count changed")
    require(Counter(route[2] for route in routes) == Counter({"even": 16, "odd": 16}),
            "even/odd long-route split changed")
    return routes


def expect_rejection(action, label):
    try:
        action()
    except (AuditError, KeyError, TypeError, ValueError):
        return
    raise AuditError(f"hostile mutation accepted: {label}")


def audit(run_hostile=True):
    audit_foundation_sources()
    automorphisms = genuine_kernel_automorphisms()
    require(len(automorphisms) == 16, "genuine automorphism-pair count changed")
    require(len({vertex_map for vertex_map, _ in automorphisms}) == 4,
            "branch-vertex automorphism count changed")
    for witness in automorphisms:
        authenticate_automorphism(*witness)

    anchors = tuple(sorted({act_on_row(BASE, edge_map)
                            for _, edge_map in automorphisms}))
    require(anchors == EXPECTED_ANCHORS, "exceptional anchor set changed")
    require(Counter(switching_invariant(row) for row in anchors) ==
            Counter({"110": 4, "111": 4}),
            "exceptional switching split changed")
    require(all("11" not in row[0:2] and "11" not in row[3:5]
                for row in anchors), "exceptional orbit contains an OO fibre")

    records, shape_counts = base_records()
    require(len(records) == 110 and shape_counts == Counter({
        "direct3": 56, "chain2+direct": 36, "fork": 12, "chain3": 6,
    }), "base marked census changed")
    require(Counter(source_classification(record) for record in records) ==
            Counter({"balanced": 54, "C4": 28, "D3": 28}),
            "base marked classification changed")

    base_geometry = target_geometry(BASE)
    witnesses = {}
    for row in anchors:
        row_witnesses = tuple((vertex_map, edge_map)
                              for vertex_map, edge_map in automorphisms
                              if act_on_row(BASE, edge_map) == row)
        require(len(row_witnesses) == 2,
                f"{row}: orbit-stabilizer witness multiplicity changed")
        row_witnesses = tuple(sorted(row_witnesses))
        witness_side_maps = []
        for vertex_map, edge_map in row_witnesses:
            require(act_on_vector(base_geometry["lengths"], edge_map) ==
                    target_geometry(row)["lengths"],
                    f"{row}: first-simple length vector was not transported")
            require(edge_map[base_geometry["open_connector"]] ==
                    target_geometry(row)["open_connector"],
                    f"{row}: even opening connector was not transported")
            require(edge_map[base_geometry["cut_connector"]] ==
                    target_geometry(row)["cut_connector"],
                    f"{row}: odd cut connector was not transported")
            for source_fibre in DOUBLED_FIBRES:
                image_fibre = {edge_map[edge] for edge in source_fibre}
                require(image_fibre in tuple(map(set, DOUBLED_FIBRES)),
                        f"{row}: doubled fibre was not transported as a fibre")
                require(sorted(target_geometry(row)["lengths"][edge]
                               for edge in image_fibre) == [1, 2],
                        f"{row}: transported doubled fibre is not first-simple")
            symbolic_paths = transport_symbolic_paths(row, vertex_map, edge_map)
            require(len(symbolic_paths) == 2,
                    f"{row}: symbolic connector path ledger changed")
            owner_map, physical_map, target = owner_transport(row, vertex_map, edge_map)
            source_to_target_side = {}
            for source_label, source_token in BASE_LABEL_TO_TOKEN.items():
                image_token = physical_map[source_token]
                source_to_target_side[BASE_SIDE[source_label]] = \
                    target["side_by_token"][image_token]
            require(set(source_to_target_side) == {0, 1} and
                    set(source_to_target_side.values()) == {0, 1},
                    f"{row}: side map is not one global preserve/swap")
            witness_side_maps.append(tuple(source_to_target_side[index]
                                           for index in (0, 1)))
            recordwise_transport_audit(records, row, vertex_map, edge_map)
        require(set(witness_side_maps) == {(0, 1), (1, 0)},
                f"{row}: the two witnesses are not preserve/global-swap")
        witnesses[row] = row_witnesses

    routes = all_length_routes(anchors, automorphisms)

    hostile_count = 0
    if run_hostile:
        # A<->C is an abstract six-symbol permutation that maps the generated
        # 110-record universe onto itself and preserves aggregate counts, but
        # no doubled-C4 vm/em induces it.  Recordwise physical commutation must
        # reject it (e.g. direct roots A,B,B become C,B,B).
        bad_owner_map = {label: label for label in OWNER_LABELS}
        bad_owner_map["A"], bad_owner_map["C"] = "C", "A"
        identity = ((0, 1, 2, 3), (0, 1, 2, 3, 4, 5))
        expect_rejection(
            lambda: recordwise_transport_audit(
                records, BASE, *identity, owner_map_override=bad_owner_map),
            "abstract A/C owner swap")
        hostile_count += 1

        bad_edge_map = (0, 1, 3, 2, 4, 5)
        expect_rejection(lambda: authenticate_automorphism(identity[0], bad_edge_map),
                         "non-endpoint-compatible edge map")
        hostile_count += 1

        mutated_anchors = list(anchors)
        mutated_anchors[-1] = "111111"
        expect_rejection(lambda: require(tuple(mutated_anchors) == EXPECTED_ANCHORS,
                                         "mutated exceptional row"),
                         "nonexceptional anchor")
        hostile_count += 1

        wrong_lengths = list(base_geometry["lengths"])
        wrong_lengths[0] += 2
        expect_rejection(lambda: require(
            act_on_vector(tuple(wrong_lengths), identity[1]) ==
            target_geometry(BASE)["lengths"], "untransported first-simple lengths"),
            "silently lengthened structural member")
        hostile_count += 1

        wrong_vertex_map = (1, 0, 2, 3)
        expect_rejection(lambda: transport_symbolic_paths(
            BASE, wrong_vertex_map, identity[1]),
            "connector endpoint orientation mismatch")
        hostile_count += 1

    return {
        "automorphisms": automorphisms,
        "anchors": anchors,
        "witnesses": witnesses,
        "records": records,
        "shape_counts": shape_counts,
        "routes": routes,
        "hostile_count": hostile_count,
    }


def main():
    result = audit()
    split = Counter(switching_invariant(row) for row in result["anchors"])
    output = (
        "R31-S doubled-C4 orbit transport verifier: exact audit passed\n"
        f"physical anchors: {len(result['anchors'])} = class110:{split['110']} + "
        f"class111:{split['111']}; no OO row\n"
        "genuine automorphism pairs: 16; witnesses per anchor: 2 "
        "(side-preserving/global-swap)\n"
        "transported marked records per anchor: 110 = balanced:54 + C4:28 + D3:28\n"
        "all-length doubled-member routes: 32 = even-long:16 + odd-long:16; "
        "bounds 1862/1000 and 1662/1000\n"
        "arbitrary connector paths: exact symbolic lengths, orientations, positions and remnants transported\n"
        f"hostile transport mutations rejected: {result['hostile_count']}\n"
        "scope: finite physical-orbit prerequisite only; analytic C4/D3 packet bounds not asserted"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
