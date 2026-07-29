# Seventeen candidate repairs for the `T^9P|P` endpoint

**Date:** 2026-07-28

## Status

This is a proof blueprint, not a certificate. The geometry-aware census in
`research/rank-eleven-t9p-p-endpoint-frontier-verifier.py` deliberately accepts
no theorem rows. The operations below were independently reconstructed from the
17-row candidate frontier and must still be integrated with exact graph-level
owners for the entire 50399-row universe.

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

## Required future gate

A theorem verifier must not recognize these rows by signature alone. It must
derive the geometry from incidence neighborhoods, bind cuts to actual cyclic
vertices, realize the ordered intervals, retain complete connector paths and
pentagons, recursively resolve the hub adhesion, independently classify each
terminal theorem, sum exact bounds, and reject duplicate or incomplete owner
domains. The same standards must also be applied to every ordinary and private-
pentagon row before an endpoint theorem is claimed.
