# Fully shared rank-eleven `T^9PP`: physical repair certificate note

**Date:** 2026-07-29

The companion verifier
`research/rank-eleven-t9pp-fully-shared-first-phase-verifier.py` now implements
physical certificates for the exact ten canonical residual signatures. The
repair list is keyed by signature and independently checked against the
ordinary residual set, so a reordered or substituted row cannot inherit a
recipe accidentally.

Every certificate contains named cyclic vertices, canonical shared-cut
vertices, concrete consecutive router intervals or rooted `C5` opening paths,
router remnants, exhaustive vertex and arbitrary-forest attachment owners, and
the nested refinement order. The verifier reconstructs those domains from the
incidence graph, invokes the shared physical owner checker, derives complete
owned cycles, and only then selects common-cut, packing-one, connected-rank, or
small-packet theorems. It independently rederives and compares the complete
packet: owner, cycles, theorem, hypothesis, and exact `Bound`. Common-cut and
pairwise-intersection predicates use complete physical cycle vertex sets, not
the original incidence adjacency.

Each declared router or opening interval is also an ownership obligation. The
verifier reconstructs the physical branch reached from that interval after
removing router boundary edges and requires both every interval vertex and the
whole branch to equal the declared final owner domain. Packet owner identities
and cycle sets are bound to the repair specification before theorem
reclassification; a theorem-valid packet under the wrong owner name is not
accepted.

The implemented operations and ledgers are exactly:

```text
U1  common-cut T^9PP                         >10-4/(3sqrt(13))
U2  open leaf P + common-cut T^9P            >8-delta
U3  P + common-cut T^8P                      >8-2delta
U4  A_8 + TP via a C5 interval               >3/4
U5  opening + packing-one T^9P               >8-delta
U6  P + T + common-cut T^7P                  >7-2delta
U7  corrected P + packing-one T^8P           >8-2delta
U8  degree-four C5: T + rank-nine T^8P       >0
U9  nested P + P + T + A_6                   >1-2delta
U10 nested P + P + T + T + A_5               >2-2delta
```

For `U4` and `U8`, the singleton is the named occupied `C5` position and the
other four physical vertices form its complementary path. For `U2` and `U5`,
the incidence cut remains with the retained packet while the other four `C5`
vertices form the opened tree territory. For `U9` and `U10`, the verifier
physically reconstructs the first-router children, proves that the second
router lies wholly in exactly one active child, and refines only that child.
Closed siblings cannot be retrieved, and final descendants must equal the
submitted owner domains. The grouped U4/U8 packets require connected
owner-induced physical graphs with cyclomatic number equal to the complete-cycle
count; U8's generic rank-nine theorem consumes that physical profile directly.

At a nested first stage, a closed interval binds directly to its terminal owner;
the active interval resolves explicitly as the disjoint union of second-stage
descendants. This prevents metadata-only refinement or later recovery of a
closed branch.

The hostile suite rejects coordinated U4/U7/U8 owner-domain swaps even when the
mutator rebuilds packets and the radical ledger, as well as forged hypotheses,
forged packet bounds, nested closed-sibling retrieval, and, in particular,
literal `U7` inheritance as
`P+P+A_7` and a wrong `C5` singleton. Thus the corrected one-router geometry
and the occupied-position predicate are executable obligations rather than
prose assumptions.

This closes all `115512` fully shared incidence types. It does not modify
`STATE`, prove R11, or claim the unrestricted rank-eleven theorem.
