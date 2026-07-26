# Connected rank-10 cacti: router/interface attack and exact status

**Date:** 2026-07-26

## Verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

The rank-nine theorem and the rank-uniform router/interface machinery reduce
the connected rank-ten problem to a finite list, but they do not yet prove the
rank-ten theorem.

The exact sharp-DNN residuals are

```text
T^9Q,  q>=3,                 T^8PP.                    (1)
```

All disconnected-cluster cases reduce to three marked endpoint kernels:

```text
A_9 | Q,
T^8P_0 | P_1,
P_0 | A_8 | P_1.                                      (2)
```

The third kernel has now been enumerated exactly at the abstract marked-
incidence level. Its rank-nine router automaton accepts `11674` of `11689`
canonical marked classes and leaves `15` new interface residuals. Promoting
those accepted rows to graph certificates uses the proved local interface
theorem and still requires a final connector/owner audit. The first two
kernels have not yet received their
required marked-interface censuses. On the fully shared side, the ordinary
split census leaves at most three `T^9Q` types, all of which close by existing
one-pivot machinery, and nine `T^8PP` types, of which two immediate scalar
repairs are recorded below. Seven fully shared two-pentagon replacement rows
remain to be certified.

Thus the exact status is **reduced, finite, and still open**. No rank-ten
theorem is claimed in this note.

## 1. DNN reduction

For a connected rank-ten cactus with cycle lengths `l_1,...,l_10`, the sharp
cactus DNN estimate gives

```text
sigma(G) >= 9-sum_i epsilon_(l_i),
epsilon_l=0                              for even l,
epsilon_l=l tan^2(pi/(2l))               for odd l.    (3)
```

Using

```text
epsilon_3=1,
epsilon_5=5-2sqrt(5)=a,
3a<2,  2a>1,  epsilon_5+epsilon_7<1,
```

the same all-rank argument used at rank nine is exact: at most two cycles can
be nontriangular; with two, only the pair `(5,5)` remains. Hence (1) is the
complete failure set of (3). Every other cycle multiset is already strict.

The symbolic derivation is recorded in
`research/rank-ten-cactus-dnn-residual-frontier-2026-07-26.md`.

## 2. Disconnected shared-cut clusters

Contract maximal shared-cut cyclic clusters while retaining actual bridge
connectors. The reduced cluster graph is a tree. Every separation below is at
an actual bridge, so connector remnants and arbitrary attached trees remain
owned by one induced territory.

The rank-nine theorem supplies the decisive induction input: every connected
cactus of rank `2,...,9` is strict. Therefore an all-triangle leaf cluster can
be removed whenever its complement has rank at least two. The leaf territory
is triangular and strict; the complement is strict by the lower-rank theorem.

### `T^9Q`

Repeated leaf pruning closes every reduced tree except the concentrated
endpoint

```text
A_9 | Q.                                                (D10-Q)
```

Indeed, if a non-`Q` leaf contains fewer than all nine triangles, its
complement has rank at least two and pruning applies. If all nine triangles
are concentrated opposite a singleton `Q`, qualitative positivity of `A_9`
cannot pay a hostile unicyclic deficit. This is a genuine one-interface
kernel, not a gap that the rank-nine theorem alone removes.

Its cyclic-hull entry may be a shared cut or an actual private triangle
vertex. The required next certificate is therefore a marked one-interface
census on all nine-triangle incidence trees, followed by router repairs of its
locked rows. The common-cut bouquet is already analytically harmless by the
packing-one hostile-cycle theorem, but the nonbouquet marked rows have not yet
been exhaustively certified.

### `T^8PP`

After the same pruning, either all triangles are concentrated with one
pentagon opposite the other, or the two pentagon-containing ends are joined by
a reduced path. The endpoint reduction is exactly

```text
T^8P_0 | P_1,                                          (D10-P1)
P_0 | A_8 | P_1.                                       (D10-P2)
```

The first family requires the rank-ten analogue of the entry-locked
`T^7P|P` certificate: one labelled entry on a colored `T^8P` incidence tree,
including the cases where the clustered pentagon is an incidence leaf and the
entry is locked at its cyclic cut. No exact census for this kernel has yet
been run.

For `(D10-P2)`, both labelled interfaces range over every shared cut and every
actual private triangle vertex and may coincide. Exact enumeration gives

```text
eight-triangle incidence trees:                    126
ordered labelled placements before automorphisms: 36414
canonical marked classes:                         11689
router score at least 1:                          11674
router residuals:                                    15
```

The exact best-score distribution is

```text
score 0:    15
score 1:    20
score 2:   283
score 3:  1378
score 4:  4817
score 5:  5176.
```

Best plans use zero, one, two, and three routers in respectively

```text
6, 10844, 838, 1
```

classes. Every accepted score is an integer credit after private-interval tree
costs. Once the labelled connectors and their remote pentagons are assigned by
the proved interface theorem, score at least one gives

```text
sigma(G)>1-2delta=5-2sqrt(5)>0.                       (4)
```

The fifteen residuals occupy only two unmarked incidence shapes:

1. the common-cut `A_8` bouquet, with six marked-interface orbits;
2. one two-cut shape consisting of a router triangle between a singleton
   triangle branch and a common-cut six-triangle branch, with nine marked
   orbits.

Their finer mark-profile counts are

```text
bouquet:
  hub-hub 1, hub-private 2, private-private 3;

two-cut shape:
  cut/private profiles 2+2,
  private/private profiles 4+1.
```

This is the first genuinely new rank-ten interface kernel. The fifteen rows
need explicit connector ownership and packet repairs; a zero router score is
not evidence of a nonpositive graph.

The reproducer is `research/rank-ten-a8-two-interface-census.py`. Its frozen
digests are

```text
all rows: 77468da6a473a52ece68d6e4319f78337feb17941e615e2a0ae65032f826cc86
residuals: 1f41279dad404a97627da24f1fa67e720f6a0d2ffc67b3c28bf1521ebeb11ca0
```

## 3. Fully shared `T^9Q`

The color-preserving incidence census stabilizes once `Q` has capacity nine.
At capacity nine it contains exactly `8049` canonical trees, distributed by
cut count as

```text
c:      1   2   3    4     5     6     7     8    9
count:  1  12  91  412  1208  2204  2402  1387  332.
```

For an even or otherwise nonhostile `Q`, the ordinary ledger leaves only the
common-cut bouquet. Under the conservative hostile ledger it leaves exactly
three types:

```text
Q1: all nine triangles and Q share one cut x;
Q2: a router triangle joins Q at x to eight triangles sharing y;
Q3: a three-cut router triangle joins Q, one leaf triangle, and a
    seven-triangle common-cut bouquet.                         (5)
```

All three close with existing rank-nine analytic machinery:

* `Q1` is the scalar common-cut `T^9Q` packet, with surplus
  `>9-delta_q` in the hostile case.
* In `Q2`, all nine triangles contain `y`; the packing-one theorem, including
  the joining segment through the router to `Q`, gives `>9-delta_q`.
* In `Q3`, open the leaf triangle at its cut with the router. Its two private
  vertices and all branches rooted there form one nonempty tree of surplus
  `-1`. The retained eight triangles all contain the bouquet hub, while `Q`
  is joined through the router, so packing one gives `>8-delta_q`. The total
  is therefore `>7-delta_q>0`.

Thus no fully shared `T^9Q` row remains, conditional only on the already proved
scalar common-cut and packing-one theorems used in the rank-nine proof.

## 4. Fully shared `T^8PP`

The exact colored incidence census contains `30386` canonical trees:

```text
c:      1   2    3     4     5     6     7     8     9
count:  1  19  204  1155  3990  8135  9615  5843  1424.
```

The ordinary one-cycle split ledger accepts `30377` and leaves nine canonical
types, by cut count

```text
c=1: 1,  c=2: 2,  c=3: 4,  c=4: 1,  c=5: 1.          (6)
```

Two rows have immediate exact repairs.

1. The `c=1` row is the common-cut `T^8PP` bouquet. The established scalar
   theorem gives
   `sigma>9-4/(3sqrt(13))>0`.
2. In the `c=2` row where one pentagon `P_0` contains the eight-triangle hub
   and a second cut leading to leaf pentagon `P_1`, open `P_1` at that cut.
   The opened territory is a nonempty tree of surplus `-1`; the retained
   common-cut `T^8P_0` packet has surplus `>8-delta`. Hence the total is
   `>7-delta>0`.

The other seven rows are finite replacement targets. Several visibly admit
rank-nine-style router plans, but no exact interval-order, final-owner, packet-
hypothesis, and radical-ledger certificate has yet been written. They remain
open in this status rather than being promoted from a suggestive incidence
split.

The reproducer is `research/rank-ten-fully-shared-incidence-census.py`. It
regresses the rank-nine generator counts before producing the rank-ten tables.
The program is a structural experiment: the analytic packet inequalities and
the seven replacement proofs remain separate mathematical obligations.

## 5. Does the finite state scale?

Yes for the arithmetic state, no for the raw orbit count, and not yet as a
census-free structural theorem.

The proved router ledger uses

```text
(p,e,c,t),
p in {0,1,2}, e in {0,1,2}, c in {0,1,2,3}, t in {0,1},
```

so it has at most `72` states. Credit truncates at three because at most two
interfaces can become naked and at most two pentagonal deficits occur. This
state bound is independent of the number of triangles. Rank ten introduces no
new arithmetic coordinate and no third interface.

What grows is the topology presented to that fixed automaton:

```text
two-interface A_7:  48 incidence trees,  3188 marked classes,  6 residuals;
two-interface A_8: 126 incidence trees, 11689 marked classes, 15 residuals;

fully shared T^7PP:  8004 incidence classes, 7 ordinary residuals;
fully shared T^8PP: 30386 incidence classes, 9 ordinary residuals.
```

Therefore the finite-state mechanism scales exactly, but exhaustive orbit
enumeration grows substantially. The rank-uniform note's structural Lemma S is
still unproved: the `72`-state ledger does not guarantee that an accepting
router exists. The new `A_8` residuals and the seven unrepaired fully shared
rows are concrete rank-ten instances of that distinction.

## 6. Exact remaining obligations

The connected rank-ten theorem will follow from the established lower-rank and
analytic inputs once all of the following finite obligations are discharged:

```text
R10-1  marked one-interface A_9|Q census and all residual repairs;
R10-2  marked entry-locked T^8P|P census and all residual repairs;
R10-3  explicit repairs for the 15 P|A_8|P marked residuals;
R10-4  exact replacement certificates for the seven unrepaired fully
       shared T^8PP rows;
R10-5  final graph-level exhaustion and ownership audit.
```

`T^9Q` is complete on the fully shared side. `T^8PP` is not. The disconnected
side is reduced to (2), but none of its three endpoint families should be
called complete until `R10-1`--`R10-3` are certified. In particular, the open
two-pivot winding theorem is neither proved nor needed by the present plan;
every proposed closure must use finite routers, scalar common-cut packets,
packing one, or an explicit cycle opening with its exact tree cost.

## 7. Reproduction

From the repository root, run

```bash
python3 research/rank-ten-a8-two-interface-census.py
python3 research/rank-ten-fully-shared-incidence-census.py
```

Both scripts use exact integer or `Fraction` arithmetic. The first verifies the
abstract incidence realization of every selected router interval; it does not
by itself certify remote connector ownership. The second validates the color-
preserving incidence recurrence and regresses selected rank-nine census tables
before printing the rank-ten output.
