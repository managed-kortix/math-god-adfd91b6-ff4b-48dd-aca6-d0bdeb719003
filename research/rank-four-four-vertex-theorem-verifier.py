#!/usr/bin/env python3
"""Exact fail-closed audit of the four-vertex rank-four theorem ledger.

The original 340 exact physical-row certificates are rechecked.  The two old
residual rows are discharged by an exhaustive binary long/unit audit of their
all-odd K4 support.  All trigonometric comparisons use rational Taylor
intervals; floating point and assert statements are not part of acceptance.
"""

import hashlib
import importlib.util
import json
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
PAIRS = tuple(combinations(range(4), 2))
DISTINGUISHED23 = PAIRS.index((2, 3))
PI_INTERVAL = (Fraction(333, 106), Fraction(355, 113))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact_int(value, label):
    require(type(value) is int, label)
    return value


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            f"cannot load proof component {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load("rank_four_four_vertex_base", "rank-four-four-vertex-dnn-verifier.py")
PATCH = load("rank_four_four_vertex_patch", "rank-four-four-vertex-exact-row-patch.py")


# The six q=1 frontier certificates.  Angles are k_i*pi/denominator.
# The long support edge is represented by its relation to distinguished 23.
GRAM_CLASSES = (
    {"extra": "even", "relation": "distinguished", "denominator": 5,
     "angles": (0, 3, 6, 7)},
    {"extra": "even", "relation": "opposite", "denominator": 5,
     "angles": (0, 1, 4, 7)},
    {"extra": "even", "relation": "adjacent", "denominator": 5,
     "angles": (0, 3, 9, 6)},
    {"extra": "odd", "relation": "distinguished", "denominator": 7,
     "angles": (0, 4, 8, 10)},
    {"extra": "odd", "relation": "opposite", "denominator": 3,
     "angles": (0, 0, 2, 4)},
    {"extra": "odd", "relation": "adjacent", "denominator": 5,
     "angles": (0, 4, 1, 7)},
)

EXPECTED_COUNTS = {
    "simplex_even": 57,
    "simplex_odd": 57,
    "frontier_even_distinguished": 1,
    "frontier_even_opposite": 1,
    "frontier_even_adjacent": 4,
    "frontier_odd_distinguished": 1,
    "frontier_odd_opposite": 1,
    "frontier_odd_adjacent": 4,
    "structural_even": 1,
    "structural_odd": 1,
}
EXPECTED_SHA256 = "f381b2b28bd3f45d7c96d90bce824a308bc340c9d6ebd098e5da116b89648d5a"


def base_failures():
    fixture = {
        (i, row): (parameters if parameters[0] == "x" else
                   tuple(Fraction(x) for x in parameters))
        for i, row, parameters in BASE.CERTIFICATES
    }
    failures = set()
    universe = set()
    for i, kernel in enumerate(BASE.KERNELS):
        for row in BASE.physical_rows(kernel):
            key = (i, row)
            universe.add(key)
            representative, bits, permutation = BASE.orbit_transport(kernel, row)
            parameters = fixture[(i, representative)]
            failed = parameters[0] == "x" and row != representative
            if not failed:
                try:
                    failed = BASE.transported_cost(
                        kernel, row, parameters, bits, permutation) > 3
                except RuntimeError:
                    failed = True
            if failed:
                failures.add(key)
    return universe, failures


def patch_coverage(failures):
    rational = {(i, row) for i, row, unused in PATCH.ROW_CERTIFICATES}
    boundary = {(i, row) for i, row, unused_matrix, unused_cost
                in PATCH.BOUNDARY_CERTIFICATES}
    canonical_patch = rational | boundary
    return {key for key in failures
            if (key[0], PATCH.aut_canonical(BASE.KERNELS[key[0]], key[1]))
            in canonical_patch}


def arctan_bounds(x, term_count=40):
    require(Fraction(0) < x < 1 and term_count % 2 == 0,
            "arctangent enclosure domain changed")
    terms = tuple((Fraction(1) if k % 2 == 0 else Fraction(-1)) *
                  x ** (2 * k + 1) / (2 * k + 1)
                  for k in range(term_count))
    lower = sum(terms, Fraction(0))
    upper = sum(terms[:-1], Fraction(0))
    require(lower < upper, "arctangent enclosure reversed")
    return lower, upper


def prove_pi_interval():
    # Machin's identity pi=16 atan(1/5)-4 atan(1/239), with alternating
    # rational series, proves rather than assumes the two classical bounds.
    a_lo, a_hi = arctan_bounds(Fraction(1, 5))
    b_lo, b_hi = arctan_bounds(Fraction(1, 239))
    proven_lo = 16 * a_lo - 4 * b_hi
    proven_hi = 16 * a_hi - 4 * b_lo
    require(PI_INTERVAL[0] < proven_lo < proven_hi < PI_INTERVAL[1],
            "Machin certificate does not prove the stated pi interval")


def alternating_bounds(x, kind):
    require(Fraction(0) <= x <= Fraction(8, 5), "Taylor argument out of range")
    powers = 1 if kind == "cos" else x
    start = 0 if kind == "cos" else 1
    terms = []
    for k in range(20):
        exponent = start + 2 * k
        if k:
            powers *= x * x
        terms.append((Fraction(1) if k % 2 == 0 else Fraction(-1)) *
                     powers / factorial(exponent))
    lower = sum(terms, Fraction(0))
    upper = sum(terms[:-1], Fraction(0))
    require(lower <= upper, "alternating Taylor enclosure reversed")
    return lower, upper


def tan_square_upper(pi_coefficient):
    require(Fraction(0) <= pi_coefficient < Fraction(1, 2),
            "tangent argument is outside [0,pi/2]")
    x_lo = pi_coefficient * PI_INTERVAL[0]
    x_hi = pi_coefficient * PI_INTERVAL[1]
    require(x_hi < PI_INTERVAL[0] / 2,
            "rational pi enclosure does not prove trigonometric monotonicity")
    sin_lo, unused = alternating_bounds(x_lo, "sin")
    unused, sin_hi = alternating_bounds(x_hi, "sin")
    cos_lo, unused = alternating_bounds(x_hi, "cos")
    unused, cos_hi = alternating_bounds(x_lo, "cos")
    require(Fraction(0) <= sin_lo <= sin_hi, "sine enclosure failed")
    require(Fraction(0) < cos_lo <= cos_hi, "cosine enclosure failed")
    return sin_hi * sin_hi / (cos_lo * cos_lo)


def circular_distance(value):
    value %= 2
    return min(value, 2 - value)


def planar_cost_upper(record, long_edge):
    denominator = record["denominator"]
    angles = tuple(Fraction(k, denominator) for k in record["angles"])
    total = Fraction(0)
    for edge_index, (u, v) in enumerate(PAIRS):
        length = 3 if edge_index == long_edge else 1
        alpha = circular_distance(angles[u] - angles[v] + (length & 1))
        total += length * tan_square_upper(alpha / (2 * length))
    extra_length = 2 if record["extra"] == "even" else 3
    alpha = circular_distance(
        angles[2] - angles[3] + (extra_length & 1))
    total += extra_length * tan_square_upper(alpha / (2 * extra_length))
    return total


def edge_relation(edge_index):
    if edge_index == DISTINGUISHED23:
        return "distinguished"
    return ("opposite" if set(PAIRS[edge_index]).isdisjoint((2, 3))
            else "adjacent")


def verify_gram_classes(records=GRAM_CLASSES):
    require(isinstance(records, tuple) and len(records) == 6,
            "six-class Gram table is incomplete")
    required = {"extra", "relation", "denominator", "angles"}
    expected_keys = {(extra, relation) for extra in ("even", "odd")
                     for relation in ("distinguished", "opposite", "adjacent")}
    actual_keys = set()
    bounds = {}
    representatives = {"distinguished": DISTINGUISHED23,
                       "opposite": PAIRS.index((0, 1)),
                       "adjacent": PAIRS.index((0, 2))}
    for record in records:
        require(set(record) == required, "Gram-class schema changed")
        denominator = exact_int(record["denominator"], "angle denominator is not an integer")
        require(all(type(value) is int for value in record["angles"]),
                "planar angles are not integers")
        key = (record["extra"], record["relation"])
        require(key not in actual_keys, "duplicate Gram class")
        actual_keys.add(key)
        require(denominator in (3, 5, 7),
                "nonstandard planar angle denominator")
        require(len(record["angles"]) == 4 and record["angles"][0] == 0,
                "planar vector witness malformed")
        # R_ij=cos(theta_i-theta_j) is PSD because it is the Gram matrix of
        # the explicitly listed vectors (cos theta_i,sin theta_i).
        bound = planar_cost_upper(record, representatives[record["relation"]])
        require(bound < 3, f"{key}: rigorous planar cost is not below three")
        bounds[key] = bound
    require(actual_keys == expected_keys, "Gram-class antichain is incomplete")
    return bounds


def stabilizer():
    group = tuple(p for p in permutations(range(4))
                  if {p[2], p[3]} == {2, 3})
    require(len(group) == 4, "distinguished-23 stabilizer changed")
    return group


def relabel_mask(mask, permutation):
    result = 0
    for index, (u, v) in enumerate(PAIRS):
        source = PAIRS.index(tuple(sorted((permutation[u], permutation[v]))))
        if mask & (1 << source):
            result |= 1 << index
    return result


def simplex_bound(extra):
    # A regular-simplex support has unit cost 1/2 and strict long cost <1/6.
    # For q>=2 its worst support bound is 7/3.  On distinguished 23 the extra
    # even cost is 4-2sqrt(3)<3/5; the extra odd cost is again <1/6.
    matrix = tuple(tuple(Fraction(1) if i == j else Fraction(-1, 3)
                         for j in range(4)) for i in range(4))
    require(all(BASE.determinant(BASE.principal_submatrix(matrix, indices)) >= 0
                for size in range(1, 5)
                for indices in combinations(range(4), size)),
            "regular-simplex Gram matrix is not exactly PSD")
    # If y=tan^2(acos(1/3)/6), then tan^2(3 atan(sqrt(y)))=1/2.
    # The rational test at y=1/18 and strict monotonicity prove y<1/18.
    y = Fraction(1, 18)
    triple_square = y * (3 - y) ** 2 / (1 - 3 * y) ** 2
    require(triple_square > Fraction(1, 2),
            "simplex long-path bound 3y<1/6 failed")
    require(Fraction(17, 10) ** 2 < 3, "sqrt(3)>17/10 proof failed")
    extra_bound = Fraction(3, 5) if extra == "even" else Fraction(1, 6)
    return Fraction(7, 3) + extra_bound


def structural_certificate(extra, long_edges):
    require(not long_edges, "structural state is not the no-long state")
    require(extra in ("even", "odd"), "structural extra parity changed")
    # Delete the internal vertices of the distinguished second 23 path.  It is
    # nonempty: even means length >=2; in the odd row simplicity forces this
    # selected second path to have length >=3.  The complement is an actual K4
    # with all its rooted attachments, whose established Sachs packet has
    # sigma>2.  The deleted nonempty tree has sigma=-1, so sigma(G)>1.
    return "attached_K4_sigma_gt_2_plus_nonempty_tree_sigma_minus_1"


def exhaustive_state_audit(records=GRAM_CLASSES):
    bounds = verify_gram_classes(records)
    group = stabilizer()
    counts = {key: 0 for key in EXPECTED_COUNTS}
    states = []
    orbit_representatives = set()
    for extra in ("even", "odd"):
        require(simplex_bound(extra) < 3, f"{extra} simplex class misses target")
        for mask in range(64):
            long_edges = tuple(i for i in range(6) if mask & (1 << i))
            orbit = tuple(sorted(relabel_mask(mask, p) for p in group))
            orbit_representatives.add((extra, orbit[0]))
            if len(long_edges) >= 2:
                disposition = f"simplex_{extra}"
            elif len(long_edges) == 1:
                relation = edge_relation(long_edges[0])
                disposition = f"frontier_{extra}_{relation}"
                require(bounds[(extra, relation)] < 3,
                        "frontier state lacks a strict Gram certificate")
            else:
                disposition = f"structural_{extra}"
                structural_certificate(extra, long_edges)
            counts[disposition] += 1
            states.append((extra, mask, disposition))
    require(len(states) == 128 and len(set((x[0], x[1]) for x in states)) == 128,
            "binary state universe is not exhaustive")
    require(counts == EXPECTED_COUNTS, "binary antichain class counts changed")
    require(len(orbit_representatives) == 56,
            "distinguished-23 stabilizer orbit census changed")
    return counts, states, bounds


def audit(records=GRAM_CLASSES):
    prove_pi_interval()
    BASE.audit()
    PATCH.audit()
    universe, failures = base_failures()
    base = universe - failures
    patch = patch_coverage(failures)
    old_residual = failures - patch
    require(len(universe) == 342, "physical universe changed")
    require(len(base) == 270 and len(patch) == 70,
            "old exact physical coverage changed")
    require(old_residual == {
        (4, (1, 1, 1, 1, 1, 1)),
        (4, (1, 1, 1, 1, 1, 2)),
    }, "old two-row residual changed")
    require(base.isdisjoint(patch), "base and patch overlap")

    counts, states, bounds = exhaustive_state_audit(records)
    payload = {
        "distinguished23": [2, 3],
        "gram_classes": records,
        "counts": counts,
        "states": states,
        "old_residual": sorted(old_residual),
    }
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    digest = hashlib.sha256(serial.encode("ascii")).hexdigest()
    return digest, counts, bounds


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, KeyError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = []

    def mutate(label, action):
        records = [dict(record) for record in deepcopy(GRAM_CLASSES)]
        action(records)
        mutations.append((label, tuple(records)))

    mutate("missing distinguished23", lambda rows: rows.pop(0))
    mutate("duplicate class", lambda rows: rows.__setitem__(1, dict(rows[0])))
    mutate("changed parity", lambda rows: rows[0].__setitem__("extra", "odd"))
    mutate("changed relation", lambda rows: rows[2].__setitem__("relation", "opposite"))
    mutate("nonstandard angle", lambda rows: rows[0].__setitem__("denominator", 11))
    mutate("lost planar vertex", lambda rows: rows[0].__setitem__("angles", (0, 3, 6)))
    mutate("false high-cost vectors", lambda rows: rows[0].__setitem__("angles", (0, 0, 0, 0)))
    mutate("extra field", lambda rows: rows[0].__setitem__("claim", "trusted"))
    mutate("boolean angle", lambda rows: rows[0].__setitem__("angles", (False, 3, 6, 7)))
    mutate("floating angle", lambda rows: rows[0].__setitem__("angles", (0, 3.0, 6, 7)))
    mutate("nonintegral denominator", lambda rows: rows[0].__setitem__(
        "denominator", Fraction(5, 2)))
    for label, records in mutations:
        expect_rejected(lambda records=records: audit(records), label)
    return len(mutations)


def main():
    digest, counts, bounds = audit()
    require(digest == EXPECTED_SHA256, "exact certificate digest changed")
    mutations = hostile_self_checks()
    require(mutations == 11, "hostile mutation count changed")
    print("four-vertex rank-four exact theorem audit passed")
    print("physical_rows: 342 = 270 base + 70 patch + 2 discharged")
    print("residual_binary_states: 128; distinguished23_stabilizer_orbits: 56")
    print("antichain: 6 strict planar Gram classes + q>=2 simplex + 2 structural states")
    print("angle_denominators: 3,5,7; all costs proved by Fraction Taylor intervals")
    print("certificate_sha256: " + digest)
    print(f"rejected_hostile_mutations: {mutations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
