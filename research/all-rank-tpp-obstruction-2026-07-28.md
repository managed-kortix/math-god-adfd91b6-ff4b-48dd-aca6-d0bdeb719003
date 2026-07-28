# All-rank `T^rPP`: exact remaining hinge obstruction

**Date:** 2026-07-28

## Verdict

The all-rank one-hostile theorem removes the complete `T^rQ` frontier, but the
same structural packetization does not close `T^rPP`.  A proposed path proof
was rejected by four hostile audits.  Its smallest rank-uniform obstruction is
the two-cut hinge

```text
A -- y -- P1 -- x -- P2,       x != y,
```

where `A` is an arbitrary nonempty connected triangular cactus, `P1,P2` are
pentagons, and arbitrary trees may be attached throughout.  In the sharp
locked version all triangles of `A` share the root `y`.

For one triangle this is a proved `TPP` base.  For arbitrary triangular rank it
is not covered by the rooted one-hostile theorem, common-cut `T^rPP`, bare
two-pentagon theorems, or demand coalescence.

## Exact method deficit

Put `delta=sqrt(5)-2`.  Every known natural move reaches only `>-delta`.

1. Split `P1` between its cuts `x,y`: the territories have complete profiles
   `P2` and `A`; their available ledger is `-delta + qualitative strict`.
2. Open leaf `P2`: the opened tree costs exactly `-1`, while the rooted
   one-hostile remainder gives only `>1-delta`.
3. Put `x,y` in one proper `P1` interval: the retained `A+P2` packet gives
   `>1-delta`, but the complementary nonempty tree costs `-1`.
4. Open `P1` while retaining `P2`: the packets are triangular plus bare
   pentagonal, again `>-
   delta`.
5. Maximum-packing Voronoi may select a triangle of `A` and `P2`, splitting
   `P1`; it again yields only qualitative triangular strictness minus `delta`.

No unspecified strict triangular margin may pay this fixed deficit.

## Why the first structural proof failed

The false step asserted that splitting any endpoint pentagon of incidence
degree at least two leaves the path-side component guarded by a triangle.  In
the hinge, deleting `P1` leaves a bare `P2` component at `x` and the entire
triangular component at `y`.  Cyclic interval choices cannot move a retained
cycle across those incidence components.

Other path-case claims must likewise use complete branch profiles.  The bare
`P-T-P` path splits into two naked pentagons, not two `TP` packets; it survives
only as the bounded `TPP` terminal.  A restricted coalescence gives `PP+T`
only when both hostile branches have complete profile exactly one pentagon.

## Remaining theorem target

Prove the rooted two-pentagon hinge theorem:

> Let `A` be an arbitrary nonempty connected triangular cactus rooted at `y`.
> Let two pentagons share a cut `x`, and choose `y` as a distinct vertex of the
> first pentagon.  Identify or bridge the root of `A` to `y`, with exactly one
> interface.  With arbitrary attached trees, the resulting cactus has
> `sigma>0`.

A sufficient analytic route is a packing-one version followed by a maximum-
triangle-packing Voronoi decomposition rooted at `y`.  The exact two-hostile
packing-one Sachs polynomial has real/imaginary parts

```text
R = Z + 4 C - 4 D,
I = 2(B-A) + 8 E,
```

where the negative `PP` real term and positive triple-cycle imaginary term
prevent the coefficientwise one-hostile comparison.  A pointwise comparison
with isolated `PP` would suffice, but its naive cross product has negative
coefficients on independent activities.  Connector/actual-tree message
structure or a rooted Schur correction is required.

No all-rank `T^rPP` theorem is claimed.
