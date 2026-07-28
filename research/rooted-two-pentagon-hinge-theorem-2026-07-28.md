# Rooted two-pentagon hinge theorem

**Date:** 2026-07-28

## Theorem

Let `A` be a nonempty connected triangular cactus rooted at `y`. Let
`P1,P2` be pentagons sharing one cut `x`, and let `y` be a distinct vertex of
`P1`. Attach `A` to `y` through exactly one interface, either by identifying
the roots or by one internally disjoint connector path. Allow arbitrary finite
trees everywhere. Then the resulting cactus `G` satisfies

```text
sigma(G)=s+(G)-|V(G)|>0.
```

If the triangular part has triangle-packing number one (no two retained
triangles are vertex-disjoint) and retains `a` triangles, the
stronger bound is

```text
sigma(G)>a+1-4/(3 sqrt(13))>0.                         (1)
```

The arbitrary-rank conclusion follows from rooted maximum-packing Voronoi
territories.

## 1. Triangle-packing-one packet

Eliminate every off-spine tree by the exact signless-matching recursion

```text
q_(u->v)=t+sum_w 1/q_(w->u)>=t.
```

This extracts one positive real factor `K(t)` from every grouped Sachs term and
gives every retained spine vertex a real activity at least `t`. Keep the root
connector inside `A`.

For the weighted triangular side put

```text
L=Z_(A-y)>0,       alpha=Z_A/Z_(A-y)>=t.               (2)
```

The inequality follows by splitting matchings at `y`: the unmatched term is
`a_y Z_(A-y)` with `a_y>=t`, and every matched-root term is nonnegative.

Replace the activity at `y` in the common-cut `P1P2` core by `alpha`. Rooted
matching coalescence gives

```text
Z_G                         = L Z_PP(alpha),
Z_(G-V(P1))                 = L Z_(PP-V(P1))(alpha),
Z_(G-V(P2))                 = L Z_(PP-V(P2))(alpha).    (3)
```

Deleting `P1` deletes both `x` and `y`, leaving `A-y` and `P2-x`; deleting
`P2` retains `y`, and (2) applies to the remaining `P1-x` path. Thus the empty
Sachs term and both singleton-pentagon terms are exactly

```text
K L Psi_PP^w = K L (R0+i I0),                           (4)
```

the weighted common-cut two-pentagon bouquet polynomial. Here `R0,I0>0`.

Triangle-packing one means a Sachs collection contains at most one triangle.
It does not say that a triangle is forced to meet a pentagon; triangle--
pentagon pairs are retained explicitly below. Since the pentagons share `x`, a
Sachs collection contains at most one pentagon. Therefore all terms not
in (4) are exactly:

* one triangle, multiplier `-2i`;
* one triangle and one disjoint pentagon, multiplier `+4`.

After dividing their positive matching carriers by `L`, write their sums as
`Acal>0` and `Ccal>=0`. The complete exact polynomial is

```text
Psi_G/(K L)=(R0+4 Ccal)+i(I0-2 Acal).                  (5)
```

No negative two-pentagon real term exists: `P1,P2` share `x`. No triple-cycle
term exists for the same reason.

The real part in (5) is positive, so its continuous phase has no winding. If
`I0-2 Acal<=0`, its phase is already below the positive phase of the weighted
`PP` bouquet. Otherwise

```text
(I0-2 Acal)/(R0+4 Ccal) < I0/R0.
```

Hence, pointwise for every `t>0`,

```text
Theta_G(t)<Theta_PP^w(t).                               (6)
```

The exact 1290-term weighted bouquet certificate proves, for all nine core
activities at least `t`,

```text
2 R0 >= t(t^4+7t^2+9)(A1+A2),
I0=2(A1+A2),
Theta_PP^w(t)<=4/[t(t^4+7t^2+9)].                      (7)
```

Its verifier is
`positive-square-energy/experiments/c5_bouquet_matching_certificate.py`;
the canonical coefficient stream has 1290 positive integer terms, coefficient
range 1--22, and SHA-256
`4c436cac772395d2a8edfdd81408ffe426759d3e94d66df2e4ab0235a3343110`.

The signed Coulson identity and

```text
integral_0^infinity 4/(t^4+7t^2+9) dt=2 pi/(3 sqrt(13))
```

give

```text
s+(G)-s-(G)>-8/(3 sqrt(13)).                            (8)
```

Since a cactus with `a` triangles and two pentagons has
`|E|=|V|+a+1`, equation (1) follows.

## 2. Arbitrary triangular root

Choose a maximum-cardinality family of vertex-disjoint triangles in `A`,
prioritizing a selected triangle nearest `y`, and make fixed-priority nearest-
cycle induced territories. The standard shortest-path argument makes each
territory connected, and replacing one selected center by two cycles proves
that every territory has cycle-packing number one. Root priority puts `y` in
the distinguished territory.

Put the complete `PP` lobe and every internal vertex of the unique connector
into that root territory.  Assign every tree attached to the lobe or connector
wholly to the root territory, and every other off-hull tree to the territory
owning its unique attachment.  The resulting sets are connected induced,
disjoint, and exhaustive: a cactus connector has no second attachment, and
cross-territory edges are simply omitted from the induced pieces.

The retained triangles of the enlarged root territory still have triangle-
packing number one, because they are precisely the retained triangles of the
root Voronoi territory.  They need not be disjoint from, or intersect, either
pentagon; Section 1 allowed all such triangle--pentagon intersections via
`Ccal`.  Thus the packet just proved applies and gives positive surplus.
Every other territory is a nonempty triangle-packing-one triangular cactus and
has positive surplus by the favorable Sachs phase theorem. Every split
triangle contributes only forest fragments. Induced-partition superadditivity
proves the theorem.

## 3. Audit status

Independent analytic reconstructions checked (2)--(8), including all
triangle/pentagon intersection patterns, cycle-deletion factors, connector
ownership, phase branch, and use of the weighted bouquet certificate. Exact
symbolic scouting found no contradiction; no finite graph census is used in
the theorem.

The theorem is specific to pentagons sharing `x`. For separated pentagons the
negative two-pentagon Sachs carrier and positive triple-cycle carrier can both
occur, so formula (5) is false there.
