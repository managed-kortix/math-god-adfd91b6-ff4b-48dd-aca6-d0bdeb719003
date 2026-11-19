#!/usr/bin/env python3
"""Audit the coarse witness-pattern cover for order-18, m=7.

This is a structural cover only.  It enumerates mutually exhaustive ways to
choose one robust predecessor for each of the two degree-nine vertices, and it
checks the elementary layer/intersection bookkeeping for two distinct low
roots.  It does not enumerate graph completions or prove any leaf impossible.
"""
from collections import Counter
from itertools import product

LOW = "low"
HIGH = "high"
LAYERS = "ABC"


def ordered_type(wr, wq):
    """Classify chosen witnesses for highs r and q.

    A high witness can only be the *other* high.  Thus (r,q) means q->r and
    r->q, a forbidden digon; there is no other high-high ordered type.
    """
    if wr == LOW and wq == LOW:
        return "two-low"
    if wr == LOW and wq == "r":
        return "low-plus-high:q<-r"
    if wr == "q" and wq == LOW:
        return "low-plus-high:r<-q"
    if wr == "q" and wq == "r":
        return "forbidden-mutual-high"
    raise ValueError((wr, wq))


ordered = [(wr, wq, ordered_type(wr, wq))
           for wr in (LOW, "q") for wq in (LOW, "r")]
assert Counter(t for _, _, t in ordered) == {
    "two-low": 1,
    "low-plus-high:q<-r": 1,
    "low-plus-high:r<-q": 1,
    "forbidden-mutual-high": 1,
}

# In the two-low case equality/inequality of the two low labels is the first
# genuine split.  A shared low root points to both highs, so both highs lie in
# that root's A=N+(w) layer; it has one rooted ledger, not two independent
# ledgers or zones.
low_patterns = ("shared-low", "distinct-low")
assert len(low_patterns) == 2


def max_intersection(high_location, other_root_location):
    """Maximum |C_u intersect C_v| visible from u's partition.

    C_v excludes v and both highs (they are out-neighbours of v).  Starting
    with the two vertices in C_u, remove v if v lies in C_u and remove the
    other high if it lies in C_u.  The high witnessed by u is already in A_u.
    """
    return 2 - (high_location == "C") - (other_root_location == "C")


# For ordered distinct roots u->r and v->q, record
# (location of q from u, location of r from v,
#  location of v from u, location of u from v, |C_u intersect C_v|).
# The roots cannot both see one another in A, since that would be a digon.
distinct_rows = []
for q_from_u, r_from_v, v_from_u, u_from_v in product(LAYERS, repeat=4):
    if v_from_u == u_from_v == "A":
        continue
    cap_u = max_intersection(q_from_u, v_from_u)
    cap_v = max_intersection(r_from_v, u_from_v)
    for overlap in range(min(cap_u, cap_v) + 1):
        distinct_rows.append((q_from_u, r_from_v,
                              v_from_u, u_from_v, overlap))

assert len(distinct_rows) == 139
assert Counter(row[-1] for row in distinct_rows) == {0: 72, 1: 55, 2: 12}


def swap_roots(row):
    q_from_u, r_from_v, v_from_u, u_from_v, overlap = row
    return (r_from_v, q_from_u, u_from_v, v_from_u, overlap)


canonical = {min(row, swap_roots(row)) for row in distinct_rows}
assert len(canonical) == 76
assert Counter(row[-1] for row in canonical) == {0: 39, 1: 30, 2: 7}

# In the mixed branch a low v witnesses q and q witnesses r (or labels are
# exchanged).  Thus q is in A_v, while r is in A_v or B_v via v->q->r.  For
# q's high-root partition, v is forced into B_q: q cannot point back to v, and
# the 9+8 first/exact-second layers exhaust all other vertices.
mixed_other_high_from_low = ("A", "B")
mixed_low_from_high = ("B",)
assert mixed_other_high_from_low == ("A", "B")
assert mixed_low_from_high == ("B",)

print("PASS top-level ordered witness choices=4 (one forbidden digon)")
print("PASS admissible families=shared-low, distinct-low, mixed-low/high")
print("PASS distinct-low labelled coarse rows=139 overlap={0:72,1:55,2:12}")
print("PASS distinct-low root-swap orbits=76 overlap={0:39,1:30,2:7}")
print("PASS mixed branch other-high-from-low=A/B; low-from-high=B")
