# Seventeen candidate repairs for the `T^9P|P` endpoint

**Date:** 2026-07-28

## Status

This file preserves the earlier 17-row design history. The physical-owner census
in `research/rank-eleven-t9p-p-endpoint-frontier-verifier.py` now certifies the
actual six projected residuals by transporting the hardened `A9` repairs into
the explicit `T9P` graph. The unrelated K1--K17 recipes below are not used for
dispatch or endpoint closure.

## Physical six-row closure

The source rows are derived by incidence and mark predicates, not by matching
their signatures. Exactly two rows have two cuts, one degree-two triangle
router, one degree-eight hub, and marks at the router private position and hub.
Their concrete `(2,1)` C3 split gives `TP + packing-one A7P`, with exact bound
`8-2delta>0`. Exactly four rows are common-cut bouquets with one of the three
allowed mark geometries (cut/cut, cut/private, or private/private on distinct
triangles). Their rooted clustered C5 is split into the connector-root singleton
and complementary four-vertex path; the retained graph is packing-one `A9P`
with exact bound `8-delta>0`.

Every repair certificate includes all C3/C5 vertices and edges, canonical shared
cuts, the complete remote-P connector and remnant, exact attachment owners,
connected induced owner territories, independently recovered complete packet
profiles, and theorem-derived bounds. Unknown or mismatched residual geometry
still fails closed.

The private-row theorem used by the same endpoint verifier is stated and proved
separately in
`research/rank-eleven-t9p-p-private-router-lemma-2026-07-29.md`.

Write `delta=sqrt(5)-2`. The 17 rows have geometry `1+1+15`.

## K1: complete-profile coalescence

The clustered pentagon lies beyond one cut of a transition triangle, the eight
other triangles lie beyond its hub cut, and the remote pentagon enters at the
private triangle vertex. Destroy the transition triangle into:

```text
singleton hub interval                  -> A_8,
two-vertex clustered-P/private-demand   -> PP.
```

The second territory owns the complete clustered-pentagon incidence branch,
the complete remote connector and remote pentagon, and the router edge joining
their two ports. There is no separate connector for the clustered pentagon.
The clustered branch must contain exactly its pentagonal block and no triangle;
under this checked hypothesis the complete profile is `PP`, not `TPP`. The
ledger is `A_8+PP>0`.

## K2: remote-pentagon opening

All nine triangles and the clustered pentagon have one common cut; the remote
entry is that cut. Materialize the remote pentagon as rooted cycle
`v0v1v2v3v4v0`. Keep `v0`, the complete remote connector, `A_9`, and the clustered
pentagon in packing-one `A_9P`; give `v1,v2,v3,v4` and their attachments to one
induced path. The ledger is

```text
(9-delta)-1=8-delta>0.
```

## K3--K17: two-arm family

These are indexed by positive `a,b,c` with `a+b+c=7`. Their invariant
incidence shape has one common hub, a marked router `R` carrying the remote
private entry and an outer `b`-triangle arm, a second router `U` carrying the
clustered pentagon and an outer `a`-triangle arm, and `c` bare hub petals.

First split `R`:

```text
two-vertex interval {outer-b cut, private remote mark} -> A_b P_remote,
singleton hub interval                                 -> active hub child.
```

Inside that hub child split `U`:

```text
two-vertex interval {outer-a cut, clustered-P cut} -> A_a P_clustered,
singleton hub interval                              -> A_c.
```

The second split refines only the active hub child and may not retrieve the
closed remote arm. Final owners must give each cut, router vertex, connector
remnant, pentagon vertex, and attachment exactly one descendant. The packet
verifier must derive that each outer arm is connected and common-cut (hence
packing one), owns exactly one complete pentagon interface, and contains no
cycle from a sibling. The final hub owner contains the `c` bare petals and the
inherited singleton router positions, but no hostile-arm branch. The packet ledger is

```text
sigma > (a-delta)+(b-delta)+0 = a+b-2delta >0.
```

The 15 pairs are

```text
(1,1);
(1,2),(2,1);
(1,3),(2,2),(3,1);
(1,4),(2,3),(3,2),(4,1);
(1,5),(2,4),(3,3),(4,2),(5,1).
```

The weakest row is `TP+TP+A_5>2-2delta`.

## Historical gate (now implemented for the six residuals)

A theorem verifier must not recognize repaired rows by signature alone. It must
derive the geometry from incidence neighborhoods, bind cuts to actual cyclic
vertices, realize the ordered intervals, retain complete connector paths and
pentagons, recursively resolve the hub adhesion, independently classify each
terminal theorem, sum exact bounds, and reject duplicate or incomplete owner
domains. The endpoint verifier now applies those standards to all 50399 rows;
the K1--K17 historical family remains outside the accepted dispatch.
