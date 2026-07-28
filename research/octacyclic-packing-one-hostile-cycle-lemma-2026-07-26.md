# Rooted packing-one hostile-cycle lemma for octacyclic provenance

**Date:** 2026-07-26

## Theorem and exact scope

For a graph `F`, write

```text
s+(F)=sum_{lambda>0} lambda^2,
s-(F)=sum_{lambda<0} lambda^2,
sigma(F)=s+(F)-|V(F)|.
```

Let `Q=C_q`, where `q=4k+1>=5`, and put

```text
delta_q=sec(pi/q)-1.
```

**Rooted packing-one hostile-cycle lemma.** Let `H` be a connected cactus whose cyclic
blocks are `Q` and `a>=1` triangles. Assume that no two triangular blocks are
vertex-disjoint. The hostile cycle `Q` may meet the triangular part at a
designated root cut vertex or may be joined to a designated root of that part
by a path of positive length. Arbitrary finite
trees may be attached at arbitrary vertices, including internal vertices of the
joining path. Then

```text
s+(H)-s-(H)>-2 delta_q,
sigma(H)>a-delta_q>=1-delta_q>0.                 (1.1)
```

The designated root records the unique interface to `Q`; it imposes no
restriction on where trees attach. Here "packing one" refers only to the family
of triangular blocks: every Sachs
collection contains at most one triangle. It does not require `Q` to intersect
the triangles. The hypothesis is automatic for a common-cut triangle bouquet,
but the lemma is not restricted to bouquets. It makes no assertion for a
triangular lobe containing two vertex-disjoint triangles, for two hostile
cycles, or for an arbitrary-rank decomposition into packing-one territories.
In particular, this theorem is independent of the all-rank Voronoi argument in
`research/rooted-hostile-cycle-guard-absorption-2026-07-26.md`.  That argument
was temporarily retracted on 2026-07-26 and restored after hostile audit on
2026-07-28; no part of the present proof depends on either status.

## Proof

Let `S=V(Q)`. Take as the spine the union of all cyclic blocks and the minimal
paths joining them. Every component off the spine is a tree with one attachment.
For a branch directed toward the spine, define its signless matching message by

```text
M_(u->v)(t)=Z_(T_(u->v))(t)/Z_(T_(u->v)-u)(t),
```

where `Z` is the signless matching partition with unmatched-vertex activity
`t`. Splitting matchings at `u` gives

```text
M_(u->v)(t)=t+sum_w 1/M_(w->u)(t)>=t.             (2.1)
```

Eliminating every off-spine branch therefore gives each spine vertex a positive
effective activity

```text
alpha_v(t)=t+y_v(t),  y_v(t)>=0,                  (2.2)
```

and contributes a common positive real factor `K(t)`. For a graph `F` with
positive activities, write

```text
Z_F(alpha)=sum_M product_(v unmatched by M) alpha_v.
```

Normalize the characteristic polynomial by

```text
Psi_H(t)=i^(-|V(H)|) det(itI-A(H))
        =product_j(t+i lambda_j).
```

In the grouped Sachs expansion, a triangle has multiplier `-2i`, whereas
`Q=C_(4k+1)` has multiplier `+2i`. The packing-one hypothesis excludes every
term containing two triangles. A term may contain both `Q` and one triangle
only when those cycles are disjoint. Consequently

```text
Psi_H(t)/K(t)=R+2i(B-A),                            (2.3)
```

where

```text
B=Z_(spine-S)(alpha)>0,
A=sum_T Z_(spine-V(T))(alpha)>0,                   (2.4)
R=Z_spine(alpha)
  +4 sum_(T disjoint from Q)
       Z_(spine-(S union V(T)))(alpha)>0.           (2.5)
```

The first sum in (2.4) ranges over all triangular blocks. Formula (2.3) follows
equally from rooted coalescence and bridge formulas: the singleton triangle and
hostile-cycle terms have opposite imaginary signs, while every admissible
two-cycle term is positive real.

Let `Z_q(t)` be the bare signless matching partition of `C_q`. Partition the
matchings counted by `Z_spine(alpha)` according to whether they use an edge
between `S` and its complement. The matchings using no such edge factor, so

```text
Z_spine(alpha)=Z_Q(alpha|S)B+E,  E>=0.             (2.6)
```

By (2.2) and coefficientwise positivity,

```text
Z_Q(alpha|S)=Z_q(t)+L,  L>=0.                      (2.7)
```

Combining (2.4)--(2.7) yields the strict comparison

```text
R-Z_q(t)(B-A)
 =E+LB+Z_q(t)A
  +4 sum_(T disjoint from Q)
       Z_(spine-(S union V(T)))(alpha)>0.           (2.8)
```

Because `R>0`, the continuous argument of `Psi_H(t)` tending to zero at
infinity is the principal value

```text
Theta_H(t)=arctan(2(B-A)/R).                        (2.9)
```

For the isolated hostile cycle,

```text
Psi_Q(t)=Z_q(t)+2i,
theta_q(t)=arctan(2/Z_q(t)).                        (2.10)
```

If `B-A<=0`, then `Theta_H(t)<=0<theta_q(t)`. If `B-A>0`, divide (2.8) by the
positive quantity `R Z_q(t)`. In either case,

```text
Theta_H(t)<theta_q(t)  for every t>0.               (2.11)
```

The signed Coulson identity is

```text
s+(F)-s-(F)=-(4/pi) integral_0^infinity t Theta_F(t) dt.  (2.12)
```

Direct evaluation of the eigenvalues of `C_q`, for `q=1 mod 4`, gives

```text
s+(Q)-s-(Q)=-2(sec(pi/q)-1)=-2 delta_q.             (2.13)
```

Integrating the strict pointwise comparison (2.11) proves the first inequality
in (1.1). Since `H` has cyclomatic number `a+1`,

```text
|E(H)|=|V(H)|+a,
s+(H)+s-(H)=2|E(H)|.
```

Together with the first inequality, this gives

```text
s+(H)>|V(H)|+a-delta_q,
```

and hence the second inequality in (1.1). This proves the lemma.

## Publication-use boundary

For the octacyclic proof this lemma is used only for the bridge-separated
`G7Q` packet: seven triangles share one cut and an arbitrary joining path leads
to one hostile `Q`. The common-cut `T^kQ` theorem used for fully shared
configurations is a different theorem with a different hypothesis. No claim
from the all-rank extension is needed or inherited here.
