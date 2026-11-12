#!/usr/bin/env python3
"""Exact exhaustive certificate audit for all 64 doubled-C4 parity rows.

A parity row is ordered as ``(a,A,b,c,C,d)`` for the doubled sides
``a,A:01`` and ``c,C:23`` and the connectors ``b:12,d:30``.  Its first
simple lengths are even -> 2 and odd -> 1, except that an odd/odd parallel
pair is represented by the unordered simple pair {1,3}; the deterministic
label convention below assigns 1 to the lower-case path and 3 to the
upper-case path.

The old census discarded the 28 rows containing an odd/odd parallel pair.
This verifier enumerates all 64 rows, derives the genuine multigraph
automorphism group (without switching), and proves every one of those 28
omitted rows by an exact planar cosine Gram certificate.  Arithmetic is only
integer/Fraction arithmetic.  Strict tangent bounds use alternating Taylor
enclosures and 333/106 < pi < 355/113.

This is a finite-certificate audit.  It assumes the separately established
path-reduction formula and fixed-parity monotonicity.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
import json


PI_LO = F(333, 106)
PI_HI = F(355, 113)

# Path order a,A,b,c,C,d.
ENDPOINTS = ((0, 1), (0, 1), (1, 2), (2, 3), (2, 3), (3, 0))
DOUBLED_PAIRS = ((0, 1), (3, 4))

# One representative for each genuine-kernel-automorphism orbit omitted from
# the old 36-row census.  The angle tuple k means planar vectors at angles
# pi*k_v/3.  The final field is the exact rational upper bound audited below.
OMITTED_ORBIT_CERTIFICATES = (
    ("000110", (0, 1, 2, 5), "72/125"),
    ("000111", (0, 0, 0, 3), "0"),
    ("001111", (0, 1, 5, 2), "358/375"),
    ("010110", (0, 2, 2, 5), "143/125"),
    ("010111", (0, 2, 1, 4), "554/375"),
    ("011111", (0, 2, 0, 3), "4/3"),
    ("110110", (0, 3, 3, 0), "0"),
    ("110111", (0, 2, 1, 4), "68/75"),
    ("111111", (0, 3, 0, 3), "0"),
)

# tan^2(pi/12) < 9/125, tan^2(pi/6)=1/3 exactly, and
# tan^2(pi/18) < 4/125.  The last bound is needed only when a length-three
# member of an OO pair has a nonzero transformed angle.
TANGENT_BOUNDS = ((1, 12, "9/125"), (1, 18, "4/125"))

EXPECTED_PAYLOAD_SHA256 = "2c1efbbf65b2c11f563f0f32cf7c1d70057d0aeb6d4d657ac6f0fe353f3b339c"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ftext(value):
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def alternating_sum(x, powers, last_power):
    total = F(0)
    factorial = 1
    first = min(powers)
    for power in range(last_power + 1):
        if power:
            factorial *= power
        if power in powers:
            sign = -1 if ((power - first) // 2) % 2 else 1
            total += sign * x**power / factorial
    return total


def tan_sq_upper_pi_multiple(numerator, denominator):
    """Certified rational upper bound for tan^2(numerator*pi/denominator)."""
    require(type(numerator) is int and type(denominator) is int,
            "nonintegral tangent angle")
    require(0 <= 2 * numerator < denominator,
            "tangent angle is outside [0,pi/2)")
    if numerator == 0:
        return F(0)
    x = F(numerator, denominator) * PI_HI
    sin_upper = alternating_sum(x, {1, 3, 5, 7, 9, 11, 13}, 13)
    cos_lower = alternating_sum(x, {0, 2, 4, 6, 8, 10, 12, 14}, 14)
    require(sin_upper > 0 and cos_lower > 0,
            "Taylor tangent enclosure lost positivity")
    return (sin_upper / cos_lower) ** 2


def prove_tan_bound(numerator, denominator, bound):
    require(tan_sq_upper_pi_multiple(numerator, denominator) < F(bound),
            f"tan^2({numerator}pi/{denominator}) bound failed")


def all_rows():
    return tuple("".join(bits) for bits in product("01", repeat=6))


def old_simple_rows():
    """The old 36 rows: no parallel pair is odd/odd."""
    return tuple(row for row in all_rows()
                 if row[0:2] != "11" and row[3:5] != "11")


def first_simple_lengths(row):
    require(len(row) == 6 and set(row) <= {"0", "1"}, "malformed parity row")
    lengths = [1 if bit == "1" else 2 for bit in row]
    for lower, upper in DOUBLED_PAIRS:
        if row[lower] == row[upper] == "1":
            lengths[lower], lengths[upper] = 1, 3
    return tuple(lengths)


def adjacency_multiplicities():
    adjacency = [[0] * 4 for _ in range(4)]
    for u, v in ENDPOINTS:
        adjacency[u][v] += 1
        adjacency[v][u] += 1
    return adjacency


def genuine_kernel_automorphisms():
    """Derive all edge permutations induced by doubled-C4 automorphisms.

    Parallel edges are distinct kernel edges, so each admissible vertex
    permutation has all compatible bijections between the two parallel fibers.
    No parity switching operation occurs here.
    """
    adjacency = adjacency_multiplicities()
    records = set()
    for vertex_map in permutations(range(4)):
        if not all(adjacency[u][v] == adjacency[vertex_map[u]][vertex_map[v]]
                   for u in range(4) for v in range(4)):
            continue
        targets = []
        for u, v in ENDPOINTS:
            image_pair = sorted((vertex_map[u], vertex_map[v]))
            targets.append(tuple(index for index, edge in enumerate(ENDPOINTS)
                                 if sorted(edge) == image_pair))
        for edge_map in product(*targets):
            if len(set(edge_map)) == 6:
                records.add((tuple(vertex_map), tuple(edge_map)))
    return tuple(sorted(records))


def act_on_row(row, edge_map):
    image = [None] * 6
    for old_edge, new_edge in enumerate(edge_map):
        image[new_edge] = row[old_edge]
    require(all(bit is not None for bit in image), "edge map is not a permutation")
    return "".join(image)


def transform_angles(angles, vertex_map):
    image = [None] * 4
    for old_vertex, new_vertex in enumerate(vertex_map):
        image[new_vertex] = angles[old_vertex]
    shift = image[0]
    return tuple((angle - shift) % 6 for angle in image)


def automorphism_orbits(rows, automorphisms):
    universe = set(rows)
    unseen = set(rows)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {act_on_row(representative, edge_map)
                 for _, edge_map in automorphisms}
        require(orbit <= universe, "row family is not automorphism invariant")
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    return tuple(orbits)


def principal_cos_index(index, period):
    index %= 2 * period
    return min(index, 2 * period - index)


def exact_tan_sq(numerator, denominator):
    value = F(numerator, denominator)
    if value == 0:
        return F(0)
    if value == F(1, 6):
        return F(1, 3)
    return None


def certificate_terms(row, angles):
    """Return exact angle terms for the planar Gram R_uv=cos(pi(ku-kv)/3)."""
    lengths = first_simple_lengths(row)
    terms = []
    for length, (u, v) in zip(lengths, ENDPOINTS):
        # acos((-1)^length R_uv) is represented by adding pi for odd length.
        q = principal_cos_index(angles[u] - angles[v] +
                                (3 if length % 2 else 0), 3)
        numerator, denominator = q, 6 * length
        terms.append((length, numerator, denominator))
    return tuple(terms)


def term_upper(term):
    coefficient, numerator, denominator = term
    exact = exact_tan_sq(numerator, denominator)
    if exact is not None:
        return coefficient * exact
    lookup = {(n, d): F(bound) for n, d, bound in TANGENT_BOUNDS}
    require((numerator, denominator) in lookup,
            f"unregistered tangent angle {numerator}pi/{denominator}")
    return coefficient * lookup[numerator, denominator]


def audit(expected_digest=EXPECTED_PAYLOAD_SHA256):
    rows = all_rows()
    old_rows = old_simple_rows()
    old_set = set(old_rows)
    omitted = tuple(row for row in rows if row not in old_set)

    require(len(rows) == 64 and len(set(rows)) == 64, "64-row enumeration failed")
    require(len(old_rows) == 36, "old census is not exactly 36 rows")
    require(len(omitted) == 28, "old-census complement is not exactly 28 rows")
    require(all((row[0:2] == "11") or (row[3:5] == "11") for row in omitted),
            "omitted-row characterization failed")
    require(all(first_simple_lengths(row)[upper] == 3
                for row in rows for lower, upper in DOUBLED_PAIRS
                if row[lower] == row[upper] == "1"),
            "OO pair did not receive first simple lengths {1,3}")

    automorphisms = genuine_kernel_automorphisms()
    require(len(automorphisms) == 16, "genuine kernel automorphism order changed")
    vertex_maps = {vertex_map for vertex_map, _ in automorphisms}
    require(len(vertex_maps) == 4, "doubled-C4 vertex automorphism order changed")

    all_orbits = automorphism_orbits(rows, automorphisms)
    old_orbits = automorphism_orbits(old_rows, automorphisms)
    omitted_orbits = automorphism_orbits(omitted, automorphisms)
    require(len(all_orbits) == 18, "64-row genuine-automorphism orbit count changed")
    require(len(old_orbits) == 9 and len(omitted_orbits) == 9,
            "old/omitted genuine-automorphism orbit count changed")
    require(not any((set(orbit) & old_set) and (set(orbit) - old_set)
                    for orbit in all_orbits),
            "a genuine automorphism mixed old and omitted rows")

    for n, d, bound in TANGENT_BOUNDS:
        prove_tan_bound(n, d, bound)

    records = {row: (angles, F(bound))
               for row, angles, bound in OMITTED_ORBIT_CERTIFICATES}
    require(len(records) == len(OMITTED_ORBIT_CERTIFICATES) == 9,
            "omitted certificate representative count changed")
    require(set(records) == {orbit[0] for orbit in omitted_orbits},
            "certificate representatives are not the nine canonical orbits")

    covered = set()
    expanded = []
    for orbit in omitted_orbits:
        representative = orbit[0]
        angles, displayed_bound = records[representative]
        require(len(angles) == 4 and angles[0] == 0 and
                all(type(value) is int for value in angles),
                f"{representative}: malformed planar angles")
        representative_terms = certificate_terms(representative, angles)
        representative_bound = sum(map(term_upper, representative_terms), F(0))
        require(representative_bound == displayed_bound,
                f"{representative}: displayed rational bound changed")
        require(representative_bound <= 2,
                f"{representative}: certified excess exceeds two")

        orbit_records = []
        for row in orbit:
            witnesses = []
            for vertex_map, edge_map in automorphisms:
                if act_on_row(representative, edge_map) == row:
                    transformed = transform_angles(angles, vertex_map)
                    terms = certificate_terms(row, transformed)
                    bound = sum(map(term_upper, terms), F(0))
                    witnesses.append((transformed, terms, bound))
            require(witnesses, f"{representative}->{row}: no genuine automorphism")
            require(all(bound == displayed_bound for _, _, bound in witnesses),
                    f"{representative}->{row}: automorphism did not preserve cost")
            transformed, terms, bound = min(witnesses)
            require(row not in covered, f"duplicate omitted-row coverage: {row}")
            covered.add(row)
            orbit_records.append({
                "row": row,
                "lengths": list(first_simple_lengths(row)),
                "angles_mod_6": list(transformed),
                "terms": [list(term) for term in terms if term[1]],
                "upper_bound": ftext(bound),
            })
        expanded.append({
            "representative": representative,
            "orbit_size": len(orbit),
            "upper_bound": ftext(displayed_bound),
            "rows": orbit_records,
        })
    require(covered == set(omitted), "the 28 omitted rows were not covered exactly")

    payload = {
        "model": {
            "path_order": ["a", "A", "b", "c", "C", "d"],
            "endpoints": [list(edge) for edge in ENDPOINTS],
            "first_simple_rule": "even=2; odd=1; each OO parallel pair={1,3}",
            "planar_vectors": "u_v=(cos(pi*k_v/3),sin(pi*k_v/3))",
        },
        "counts": {
            "all_rows": len(rows),
            "old_rows": len(old_rows),
            "omitted_rows": len(omitted),
            "kernel_automorphisms": len(automorphisms),
            "all_orbits": len(all_orbits),
            "old_orbits": len(old_orbits),
            "omitted_orbits": len(omitted_orbits),
        },
        "pi_enclosure": [ftext(PI_LO), ftext(PI_HI)],
        "tangent_bounds": [[n, d, bound] for n, d, bound in TANGENT_BOUNDS],
        "omitted_certificates": expanded,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    digest = sha256(canonical.encode("ascii")).hexdigest()
    if expected_digest is not None:
        require(digest == expected_digest,
                f"certificate payload digest changed: {digest}")
    return payload, digest


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, ValueError, TypeError, ZeroDivisionError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    global OMITTED_ORBIT_CERTIFICATES, TANGENT_BOUNDS
    mutations = 0

    original_certificates = OMITTED_ORBIT_CERTIFICATES
    try:
        OMITTED_ORBIT_CERTIFICATES = original_certificates[:-1]
        expect_rejected(lambda: audit(expected_digest=None), "missing orbit record")
        mutations += 1
    finally:
        OMITTED_ORBIT_CERTIFICATES = original_certificates

    try:
        changed = list(original_certificates)
        row, angles, bound = changed[4]
        changed[4] = (row, (0, 0, 0, 0), bound)
        OMITTED_ORBIT_CERTIFICATES = tuple(changed)
        expect_rejected(lambda: audit(expected_digest=None), "wrong Gram angles")
        mutations += 1
    finally:
        OMITTED_ORBIT_CERTIFICATES = original_certificates

    try:
        changed = list(original_certificates)
        row, angles, _ = changed[0]
        changed[0] = (row, angles, "2")
        OMITTED_ORBIT_CERTIFICATES = tuple(changed)
        expect_rejected(lambda: audit(expected_digest=None), "wrong rational bound")
        mutations += 1
    finally:
        OMITTED_ORBIT_CERTIFICATES = original_certificates

    original_tangent_bounds = TANGENT_BOUNDS
    try:
        TANGENT_BOUNDS = ((1, 12, "7/100"), original_tangent_bounds[1])
        expect_rejected(lambda: audit(expected_digest=None), "false tangent bound")
        mutations += 1
    finally:
        TANGENT_BOUNDS = original_tangent_bounds

    return mutations


def main():
    payload, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 4, "hostile mutation count changed")
    counts = payload["counts"]
    print("doubled-C4 64-row exact audit passed")
    print("rows: {all_rows}; old census: {old_rows}; omitted and certified: {omitted_rows}".format(**counts))
    print("genuine kernel automorphisms: {kernel_automorphisms}; row orbits: "
          "{all_orbits} = {old_orbits} old + {omitted_orbits} omitted".format(**counts))
    print("omitted-orbit excess bounds: " + ", ".join(
        record["representative"] + "<=" + record["upper_bound"]
        for record in payload["omitted_certificates"]))
    print("certificate_payload_sha256: " + digest)
    print(f"rejected_hostile_mutations: {mutations}")
    print("scope: finite exact Gram audit; no switching quotient and no theorem promotion")


if __name__ == "__main__":
    main()
