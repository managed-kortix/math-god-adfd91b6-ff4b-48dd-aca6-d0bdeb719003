# Positive square energy of every connected rank-ten cactus

**Date:** 2026-07-26

## 1. The theorem and proof firewall

For a graph `G`, put

```text
s+(G)=sum_(lambda_i>0) lambda_i^2,
sigma(G)=s+(G)-|V(G)|,
T=C3, P=C5, delta=sqrt(5)-2<1/4.
```

**Theorem.** Every connected cactus `G` of cyclomatic rank ten satisfies

```text
s+(G)>|V(G)|.
```

The proof is exhaustive. It combines the exact sharp-DNN frontier, the exact
colored cluster-partition audit, three exact marked-interface censuses, two
exact fully shared incidence censuses, and explicit repairs for every finite
exception. Global separations use actual bridges; local separations use proved
proper-interval triangle routers. The proof uses neither the open two-pivot
winding assertion nor the false candidate separator Lemma S.

The exact finite ingredients are:

| role | artifact |
|---|---|
| sharp-DNN frontier | `research/rank-ten-cactus-dnn-residual-frontier-2026-07-26.md` |
| disconnected partition audit | `research/rank-ten-cactus-residual-partition-audit.py` |
| marked `A_9|Q` closure | `research/rank-ten-t9q-template-closure-verifier.py` |
| entry-locked `T^8P|P` closure | `research/rank-ten-t8p-entry-locked-census.py` |
| marked `P|A_8|P` closure | `research/rank-ten-a8-two-interface-census.py` |
| fully shared censuses | `research/rank-ten-fully-shared-incidence-census.py` |
| nine `T^8PP` replacements | `research/rank-ten-t8pp-nine-exceptions-resolution.py` |

## 2. Proved packet inputs and ownership

Positive square energy is superadditive on induced vertex partitions. Thus, if
`V(G)` is partitioned into induced territories `V_1,...,V_r`, then

```text
sigma(G)>=sum_i sigma(G[V_i]).                         (2.1)
```

We use the proved rank-two-through-nine cactus theorems and the following
consequences, all uniform over arbitrary trees attached at packet vertices:

```text
connected cactus of rank 2 or 3:       sigma>=0,
connected cactus of rank 4,...,9:      sigma>0,
P:                                     sigma>=-delta,
hostile Q=C_q, q=1 mod 4:              sigma>=-delta_q,
delta_q=sec(pi/q)-1<1,
TP:                                    sigma>3/4,
TQ:                                    sigma>0,
PP:                                    sigma>0,
TPP:                                   sigma>3/2.
```

For a connected shared-cut cluster `A_r` of `r` triangles,

```text
sigma(A_r)>b_r,
(b_1,...,b_9)=(0,1,2,3,2,1,0,0,0).                  (2.2)
```

The entries through `r=8` are the proved triangular-cluster margins. The
`r=9` entry follows from the rank-nine cactus theorem. Only strict positivity,
not a numerical margin, is used for `A_8` and `A_9`.

Two analytic inputs close locked one-pivot packets. The common-cut scalar
Schur--Sachs theorem gives

```text
common-cut T^kQ:   sigma>k-delta_q  for hostile Q,
                   sigma>k          for nonhostile Q,
common-cut T^kP:   sigma>k-delta,
common-cut T^kPP:  sigma>k+1-4/(3sqrt(13)).           (2.3)
```

The rooted packing-one theorem says that one hostile `Q`, joined directly or
by an arbitrary path to `a>=1` triangles no two of which are vertex-disjoint,
has

```text
sigma>a-delta_q.                                      (2.4)
```

Arbitrary trees may occur on the cycles and joining path. Every use of (2.4)
below has a displayed common triangular hub, so packing number one is checked
directly. Formula (2.3) is used only when all named cycles have one actual
common cut. Neither input is a two-pivot theorem.

Contracting maximal shared-cut cyclic clusters while retaining every actual
bridge path gives a tree. Cutting an actual bridge realizes any connected
subtree assignment as connected induced territories. At a triangle router,
two distinct marks induce a singleton and a complementary two-vertex interval;
three marks induce three singleton intervals. Each incidence branch and
connector remnant follows its mark, and every off-hull tree follows its unique
hull attachment. A later router split refines one existing territory. Hence
all final territories are connected, induced, disjoint, and exhaustive. A
private interval with no retained cycle is a nonempty tree and has exact
surplus `-1`. This is the proved local router theorem; no global separator
claim is used.

## 3. Exact sharp-DNN reduction

Let the ten cyclic blocks have lengths `l_1,...,l_10`. A connected rank-ten
cactus has `m=n+9`. Put

```text
epsilon_l=0                              if l is even,
epsilon_l=l tan^2(pi/(2l))               if l is odd.
```

The sharp cactus DNN theorem and block counting give

```text
sigma(G)>=9-sum_i epsilon_(l_i).                       (3.1)
```

The odd sequence decreases strictly. With
`a=epsilon_5=5-2sqrt(5)`, exact squared comparisons give

```text
epsilon_3=1,  3a<2,  2a>1,  epsilon_5+epsilon_7<1.    (3.2)
```

If at most seven cycles are triangles, then
`sum epsilon_i<=7+3a<9`. With exactly eight triangles, the two remaining
cycles contribute at least one only when both are pentagons: an even cycle
contributes zero, and every other odd pair is at most
`epsilon_5+epsilon_7<1`. At least nine triangles gives `T^9Q`, allowing
`Q=T`. Therefore the exact DNN residual frontier is

```text
T^9Q={3,3,3,3,3,3,3,3,3,q}, q>=3,
T^8PP={3,3,3,3,3,3,3,3,5,5}.                         (3.3)
```

Every other cycle multiset is strict directly from (3.1).

## 4. Shared-cut dichotomy and disconnected partition audit

For a residual graph, the reduced shared-cut cluster tree either has one node
or more than one node. The former is the fully shared case. In the latter,
the exact colored integer-partition audit is

| residual | all partitions | proper | direct packet rows | structural rows |
|---|---:|---:|---:|---:|
| `T^9Q` | 97 | 96 | 92 | 4 |
| `T^8PP` | 181 | 180 | 170 | 10 |

For each direct row, summing (2.2) and the packet bounds above is positive, or
zero with a strict summand. The structural rows are printed and frozen by the
partition verifier. They reduce as follows.

For `T^9Q`, the four rows are

```text
Q + T+...+T (nine singleton triangles),
Q + T + T + A_7,
Q + T + A_8,
Q + A_9.
```

In the first row a leaf triangle can be removed, leaving a connected strict
rank-nine cactus. In `Q+T+T+A_7`, a leaf singleton triangle leaves a strict
rank-nine complement; if neither singleton is a leaf, the four cluster nodes
form a path with `Q` and `A_7` at its ends, so the singleton adjacent to `Q`
forms a strict `TQ` packet and the other singleton with `A_7` is a strict
rank-eight cactus. In `Q+T+A_8`, either the singleton is a leaf and leaves a
strict rank-nine complement, or it is the middle of the three-node path and
pairs with `Q`, leaving strict `A_8`. The only endpoint not removed is

```text
A_9 | Q.                                               (D10-Q)
```

For `T^8PP`, the ten structural color rows consist of the three rows

```text
P+P+T+...+T,  P+P+T+A_7,  P+P+A_8,
```

and the seven rows `P+T+...+T+(T^kP)`, `2<=k<=8`, with the displayed singleton
count making eight triangles in total. Here is the complete tree reduction.
Any singleton-triangle leaf is strict and leaves a connected rank-nine
complement, so remove it. In the first row, if no singleton is a leaf, the two
pentagons are the only leaves and the reduced tree is a path; its first
pentagon--triangle edge gives a strict `TP` territory and a strict rank-eight
remainder. In `P+P+T+A_7`, a leaf `T` is already covered, a leaf `A_7` leaves a
strict `TPP` complement, and otherwise the four-node tree has a terminal `TP`
and a strict rank-eight `A_7P` remainder. In `P+P+A_8`, a pentagon in the
middle gives a strict `PP` territory plus strict `A_8`; the only unreduced
order is `P|A_8|P`. Finally consider
`P+T+...+T+(T^kP)`. If `k<8` and no singleton is a leaf, the bare `P` and the
`T^kP` cluster are the only leaves, so the reduced tree is a path. Its bare
pentagon and adjacent singleton form a strict `TP`, leaving a connected
rank-eight cactus. For `k=8` there is no singleton and the row is
`T^8P|P`. Thus the only endpoints are

```text
T^8P_0 | P_1,                                         (D10-P1)
P_0 | A_8 | P_1.                                      (D10-P2)
```

This reduction uses only leaf/path moves on the actual reduced tree and the
rank-nine theorem. It does not assert that an arbitrary incidence tree has a
good router.

## 5. Disconnected `A_9|Q`: `3624=3618+6`

Mark the first cyclic-hull entry of the actual connector from `Q` into `A_9`.
It is either a shared cut or an actual private triangle vertex. The exact
one-interface census contains

```text
355 unmarked A_9 incidence trees,
6745 marked placements before automorphisms,
3624 canonical marked rows,
3618 accepted finite-router rows,
6 explicit repairs.
```

For an accepted row, the verifier checks legal proper intervals, disjoint and
exhaustive incidence branches, and one final owner for the marked connector.
If the `Q` territory retains `k` triangles, the ledger is: `TQ>0` for `k=1`;
`TTQ>=0` plus another strict branch for `k=2`; the lower-rank theorem for
`3<=k<=8`; and, for `k=0`, a triangular branch of size at least four and margin
`>3`, which absorbs `Q>-1`.

The six exceptions are two entry orbits on the common-cut `A_9` bouquet and
four entry orbits on one two-cut saturated extension. The bouquet has packing
one and gives `>9-delta_q`. On one extension orbit, the leaf triangle and `Q`
form a strict `TQ` packet and the common-cut `A_8` remainder is strict. On the
other three, open the leaf triangle. The opened private territory costs `-1`;
the retained eight hub triangles and the actual path to `Q` satisfy (2.4), so

```text
sigma(G)>(8-delta_q)-1=7-delta_q>0.                  (5.1)
```

Thus every `A_9|Q` endpoint closes. Nonhostile `Q`, including `Q=T`, has the
same or a stronger ledger.

## 6. Disconnected `T^8P|P`: `11689=11586+100+3`

The ordinary pentagon interval argument handles an internal clustered
pentagon and a privately entered leaf pentagon. The remaining entry-locked
family has

```text
2392 colored T^8P incidence trees,
1105 incidences with the clustered P as an incidence leaf,
11689 canonical marked-entry rows.
```

Exact final-owner certificates close `11586` rows directly and `100` by finite
replacement sequences. The replacements use zero, one, two, and three routers
in respectively `2,9,73,16` rows. They verify every split order, interval,
retained component, packet hypothesis, radical ledger, and final owner; no
provisional territory label survives.

The three remaining marked orbits lie on one two-cut shape: a router triangle
joins the clustered leaf pentagon to a common-hub fan of eight triangles. Open
the remote pentagon `P_1`. Its four private vertices and rooted trees form one
nonempty tree of surplus `-1`; the retained packet contains all eight hub
triangles, clustered `P_0`, both actual connector remnants, and their trees.
Packing one gives `>8-delta`, hence

```text
sigma(G)>(8-delta)-1=7-delta>0.                       (6.1)
```

This proves all `11689=11586+100+3` entry-locked rows.

## 7. Disconnected `P|A_8|P`: `11689=11674+15`

The two labelled connector entries may be shared cuts, private triangle
vertices, or coincident. The exact census has

```text
126 unmarked A_8 incidence trees,
36414 ordered labelled placements before automorphisms,
11689 canonical marked rows,
11674 accepted router rows,
15 explicit repairs.
```

Each accepted row has exact integer credit at least one after private-interval
charges. The two pentagonal deficits therefore leave
`>1-2delta>0`. Its checked router intervals and successive refinements assign
both actual connectors, cuts, branches, and attached trees to final packets.

The fifteen exceptions occupy only two incidence shapes. Six are marked orbits
on the common-cut `A_8` bouquet. Their repairs are: hub--hub or suitable private
profiles, open one remote pentagon and retain a packing-one `T^8P` arm, giving
`>7-delta`; hub--private, split to `P+` common-cut `T^7P`, giving
`>7-2delta`; coincident private entries, use strict `A_7+PP`; the remaining
private profiles use the same checked opening or proper triangle intervals.

The other nine lie on a saturated router between a singleton triangle and a
six-triangle common-cut branch. Splitting its three singleton ports gives,
according to the marked orbit,

```text
A_6+T+PP,               >1,
A_6+TP+P,               >2-2delta,
common-cut T^6P+T+P,    >6-2delta,
packing-one T^6P+T+P,   >6-2delta.
```

The verifier materializes every row, distinguishes `TP` and `PP` terminals,
and checks that no destroyed router triangle is reused. Hence all
`11689=11674+15` classes close.

## 8. Fully shared `T^9Q`

The exact color-preserving incidence census stabilizes when `Q` has capacity
nine. At capacity nine its cut-count distribution is

```text
c:      1   2  3   4     5     6     7     8    9
count:  1  12  91  412  1208  2204  2402  1387  332
total: 8049.
```

Ordinary exact splits close every nonhostile row except the common-cut bouquet.
In each hostile regime they leave exactly three rows:

1. All nine triangles and `Q` share one cut. Apply (2.3): `>9-delta_q`.
2. All nine triangles contain one hub and `Q` joins through a router triangle.
   Apply (2.4) along the actual joining segment: `>9-delta_q`.
3. Open the unique leaf triangle opposite an eight-triangle common-hub lobe.
   The opening costs `-1`; the retained eight hub triangles and path to `Q`
   satisfy (2.4), giving `>7-delta_q` in total.

The closure verifier independently regenerates the `q=5` universe of `8011`
types and the stabilized universe of `8049`, reruns every ordinary split,
checks unique retained-cut ownership, and matches all three frozen exception
signatures. Thus every fully shared `T^9Q` cactus is strict.

## 9. Fully shared `T^8PP`: `30386=30377+9`

The exact census is

| shared cuts `c` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 19 | 204 | 1155 | 3990 | 8135 | 9615 | 5843 | 1424 | 30386 |
| ordinary safe | 0 | 17 | 200 | 1154 | 3989 | 8135 | 9615 | 5843 | 1424 | 30377 |
| exceptions | 1 | 2 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 9 |

Every ordinary-safe row has a checked legal split and positive exact packet
ledger. The nine exceptions and their replacement margins are

| code | replacement | margin |
|---|---|---:|
| N1 | common-cut `T^8PP` | `>9-4/(3sqrt(13))` |
| N2 | open leaf `P`; retain common-cut `T^8P` | `>7-delta` |
| N3 | `P+` common-cut `T^7P` through one router | `>7-2delta` |
| N4 | `A_7+TP` through a pentagon router | `>3/4` |
| N5 | open one `P`; retain packing-one `T^8P` | `>7-delta` |
| N6 | `P+T+` common-cut `T^6P` | `>6-2delta` |
| N7 | `P+P+A_6` through two routers | `>1-2delta` |
| N8 | `P+P+T+A_5` through two routers | `>2-2delta` |
| N9 | `P+P+T+T+A_4` through two routers | `>3-2delta` |

For N4 the verifier checks all `5*4*3=60` placements of the three marks on
the router pentagon. Removing the designated singleton always leaves one
four-vertex path containing the other two marks, so the `A_7` and `TP`
territories are genuine intervals. In N7--N9 the second triangle-router split
refines one territory from the first. In N2 and N5 precisely the four private
vertices of the opened pentagon, with trees rooted there, incur the `-1` cost;
the entry cut and connector remnants remain in the retained packet.

The nine-row verifier regenerates all `30386` incidence types and checks the
frozen signatures and labelled edges, router activity and nesting, every
packet's connectivity and common-cut or packing-one hypothesis, cycle coverage,
unique cut ownership, and exact radical sign. Therefore
`30386=30377+9` is a complete closure.

## 10. Exhaustion

Every connected rank-ten cactus belongs to exactly one covered class:

1. A nonresidual cycle multiset is strict by (3.1).
2. A disconnected residual cluster tree is one of the `96` or `180` proper
   colored partitions. Direct rows have positive packet ledgers; structural
   rows reduce by proved leaf/path moves to `A_9|Q`, `T^8P|P`, or `P|A_8|P`,
   all closed in Sections 5--7.
3. A fully shared `T^9Q` cactus is one of the exact capacity-dependent census
   rows and is closed in Section 8.
4. A fully shared `T^8PP` cactus is one of the `30386` rows and is closed in
   Section 9.

Every bridge cut is actual; no connector is contracted. Every local router is
a proved proper-interval split, and later splits refine one owner. Every shared
cut, connector remnant, incidence branch, private interval, and attached tree
has one final owner. Common-cut estimates are used only at one real pivot;
packing one is used only when all retained triangles contain one displayed hub;
each opening records its exact nonempty-tree cost. There is no appeal to a
two-pivot phase estimate or to candidate Lemma S. Thus `sigma(G)>0` in every
case, proving the theorem.

## 11. Exact reproduction

Run from the repository root with Python 3.10 or newer:

```bash
python3 research/rank-ten-cactus-residual-partition-audit.py
python3 research/rank-ten-a9-one-interface-census.py
python3 research/rank-ten-t9q-template-closure-verifier.py
python3 research/rank-ten-t8p-entry-locked-census.py
python3 research/rank-ten-a8-two-interface-census.py
python3 research/rank-ten-fully-shared-incidence-census.py
python3 research/rank-ten-t8pp-nine-exceptions-resolution.py
```

The first script fail-closed verifies `97/96/92/4`, `181/180/170/10`, and the
exact frozen structural rows in ordinary and optimized Python. The next five
independent families reproduce `3624=3618+6`, the hostile fully shared `T^9Q`
exceptions, `11689=11586+100+3`, `11689=11674+15`, and the fully shared census
tables. The final script verifies all nine `T^8PP` replacements and the closure
`30386=30377+9`. The hardened endpoint and replacement verifiers fail closed
under `python -O`; all finite classifications use integers or `Fraction`, and
radical signs are decided by exact squared comparisons.
