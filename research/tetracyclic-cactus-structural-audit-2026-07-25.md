# Tetracyclic cactus structural audit: exact frontier and relocation obstruction

This note adversarially audits the proposed extension of the all-tricyclic
cactus theorem to tetracyclic cacti. It records what the existing packet lemmas
do prove, the precise remaining incidence classes, a coverage defect in the
reconnaissance driver, and an exact counterexample to a tempting tree
concentration reduction. It does **not** claim the tetracyclic theorem.

## Exact DNN residual reduction

For four cycle blocks of lengths `l1,...,l4`, the cactus identity and sharp DNN
constant give

`s+(G)-n >= 3-sum epsilon_li`,

where `epsilon_3=1`, `epsilon_5=5-2sqrt(5)`, even cycles contribute zero, and
the odd sequence strictly decreases. Thus the only residual families are

`{3,3,3,q}` for odd `q`, and `{3,3,5,5}`.

This part is exact. The second family is unique with only two triangles because
`2 epsilon_5>1` while `epsilon_5+epsilon_7<1`.

## Packet surplus ledger

Write `sigma(H)=s+(H)-|H|` and, for `q=1 mod 4`,
`delta_q=sec(pi/q)-1<1`. Existing audited papers prove, with arbitrary tree
attachments,

- triangular unicyclic: `sigma>0`;
- `C_q` unicyclic: `sigma>=-delta_q`;
- mixed `{3,q}` bicyclic: `sigma>1-delta_q`;
- arbitrary bicyclic or tricyclic cactus: `sigma>=0`;
- two `3 mod 4` cycles: `sigma>1`;
- shared-triangle `{3,3,q}` tricyclic: `sigma>2-delta_q`;
- one-cluster `{3,5,5}` tricyclic: `sigma>6-2sqrt(5)`.

The strict positive surplus of a triangular unicyclic packet is not uniformly
bounded away from zero: a growing star at a triangle vertex drives it to zero.
Therefore strict inequalities cannot silently pay a fixed pentagonal deficit.

## Exact shared-cut incidence classifications

Use the bipartite block-cut incidence tree whose two node classes are cycle
blocks and cut vertices belonging to at least two cycle blocks.

For one connected shared-cut cluster of type `{3,3,3,q}`, either two triangles
share a cut vertex, or the three triangles are leaves meeting the `q`-cycle at
three distinct cut vertices. This follows because any second incidence between
one triangle and the `q`-cycle would create a cycle in the block-cut tree.

For one connected shared-cut cluster of type `{3,3,5,5}`, either some triangle
is a leaf cycle node (deleting it leaves the other three cycle nodes connected),
or the incidence tree is forced to be the alternating path

`C5 - T - T - C5`,

with three distinct pairwise cut vertices. Indeed, if neither triangle is a
leaf, degree counting in the bipartite tree forces both triangles to have
degree two, both pentagons degree one, and all three cut nodes degree two.

These combinatorial classifications are valid, but they do not by themselves
produce vertex-disjoint induced cyclic packets: two blocks sharing a cut vertex
cannot both retain that vertex in a vertex partition.

## What bridge packet accounting leaves open

Bridge cuts do yield genuine induced territories. Most cluster-tree splits are
settled by the surplus ledger, but the following cannot be certified from the
existing quantitative bounds alone:

1. fully bridge-separated `{3}|{3}|{3}|{q}` for `q=1 mod 4`;
2. fully bridge-separated `{3}|{3}|{5}|{5}`;
3. a connected shared `{3,3,5}` cluster in which the pentagon meets two
   disjoint triangles at distinct cuts, plus a bridge-separated `C5` packet.

In (1) and (2), singleton triangle surpluses can tend to zero while singleton
hostile cycles retain fixed deficits. In (3), the all-tricyclic theorem supplies
only `sigma({3,3,5})>0`, not the needed uniform `sqrt(5)-2`.

The fully shared `{3,3,5,5}` phase route also remains open: there are 20
quotient-isomorphism types, and the naive two-pentagon comparison polynomial is
coefficientwise positive for only one. Negative coefficients do not disprove
positivity on the activity orthant, but they invalidate that certificate.

## Coverage defect in the reconnaissance driver

`tetracyclic_cactus_residual_search.py` varies the attachment position on the
parent cycle but always attaches every child at its locally labelled vertex
zero. Hence an internal cycle's parent/child cut vertices do not range over all
relative cyclic positions. The claim that the driver enumerates every
shared-cut position for connector lengths zero or one is too strong. Its
reported examples remain valid reconnaissance, not a complete core census.

## Exact relocation obstruction

No proof may concentrate arbitrary connector leaves at the connector middle.
Take `C5--P5--C5`, wedge two triangles at the left pentagon endpoint, and add
two leaves. Let `G_split` put one leaf at each of the first and last internal
connector vertices; let `G_middle` put both at the middle internal vertex.
Both are 19-vertex tetracyclic cacti.

Exact characteristic polynomials factor as

`chi_split = x(x-1)(x+1)^2(x^2+x-1)^2 f_split`,

where

`f_split=x^11-3x^10-13x^9+41x^8+49x^7-183x^6-42x^5`
`        +306x^4-40x^3-168x^2+36x+12`,

and

`chi_middle = x(x-1)(x+1)^2(x^2+x-1)^2 f_middle`,

where

`f_middle=x^11-3x^10-13x^9+41x^8+48x^7-180x^6-29x^5`
`         +269x^4-69x^3-65x^2+2x+2`.

Rational Sturm isolation and interval squaring certify

`3.99322941587477321 < s+(G_split)-19 < 3.99322941587490311`,

`3.99874061650129984 < s+(G_middle)-19 < 3.99874061650143203`.

Thus `s+(G_split)<s+(G_middle)` with a certified gap exceeding `0.00551`.
Moving the leaves to the connector middle increases, rather than decreases,
the target. Reproduce with

```bash
uv run --with sympy python positive-square-energy/experiments/tetracyclic_relocation_obstruction.py
```

## Next exact targets

The cleanest remaining targets are:

1. a uniform `sigma>=delta_5` bound for the pentagon-middle shared
   `{3,3,5}` tricyclic packet;
2. an actual-lobe connector phase inequality that merges hostile singleton
   cycles with neighboring triangular lobes without assuming leaf relocation;
3. positivity on the activity orthant for all fully shared core incidences,
   using substitutions/Bernstein certificates rather than raw coefficients;
4. a genuine multi-root tree-allocation theorem, if one exists, stated weakly
   enough to survive the exact relocation obstruction above.
