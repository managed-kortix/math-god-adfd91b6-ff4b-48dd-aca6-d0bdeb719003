# Positive square energy of every connected rank-nine cactus

**Date:** 2026-07-26

## 1. Theorem and proof boundary

For a graph `G`, write

```text
s+(G) = sum_{lambda_i>0} lambda_i^2,
sigma(G) = s+(G)-|V(G)|,
T=C3, P=C5, delta=sqrt(5)-2<1/4.
```

**Theorem.** If `G` is a connected cactus of cyclomatic rank nine, then

```text
s+(G)>|V(G)|.
```

The proof is exhaustive. It uses the exact sharp-DNN residual calculation,
actual-bridge reductions, finite triangle-router certificates, the scalar
common-cut Schur--Sachs theorem, the one-hostile-cycle packing-one theorem, and
two explicit pentagon openings. It does **not** use the proposed two-pivot phase
theorem. That theorem remains open and is unnecessary because all of its
rank-nine target interfaces are closed by the finite certificates and openings
below.

The authoritative ingredients are:

| role | source |
|---|---|
| exact DNN frontier | `research/nonacyclic-dnn-residuals-2026-07-26.md` |
| disconnected color reduction and `T^8Q` closure | `research/rank-nine-cactus-octacyclic-attack-status-2026-07-26.md` |
| disconnected `T^7PP` closure | `research/nonacyclic-disconnected-t7pp-marked-interface-status-2026-07-26.md` |
| two-interface finite certificate | `research/nonacyclic-t7-two-interface-census-2026-07-26.md` |
| fully shared censuses | `research/nonacyclic-fully-shared-incidence-census-2026-07-26.md` |
| seven fully shared replacements | `research/nonacyclic-t7pp-seven-exceptions-resolution-2026-07-26.md` |
| scalar common-cut bounds | `research/common-cut-bouquet-rooted-schur-2026-07-26.md` |
| one-hostile-cycle packing-one bound | `research/octacyclic-packing-one-hostile-cycle-lemma-2026-07-26.md` |

The exploratory two-pivot reduction in
`research/two-pivot-schur-sachs-triangular-cactus-2026-07-26.md` is not a
dependency. In particular, no principal-argument, winding, matrix-cone, or
two-pivot integrated phase assertion is imported here.

## 2. General packet facts and ownership

Positive square energy is superadditive on induced vertex partitions. If
`V(G)` is partitioned into induced territories `G_1,...,G_j`, then

```text
sigma(G)>=sum_i sigma(G_i).                              (2.1)
```

We use the already established cactus bounds

```text
rank 2 or 3 connected cactus:             sigma>=0,
rank 4 through 8 connected cactus:        sigma>0,
P packet:                                 sigma>=-delta,
hostile Q=C_q, q=1 mod 4:                 sigma>=-delta_q,
delta_q=sec(pi/q)-1<1,
TP:                                       sigma>1-delta,
TQ:                                       sigma>0,
PP:                                       sigma>0,
TPP:                                      sigma>3/2.
```

For a connected shared-cut cluster `A_r` of `r` triangles, arbitrary attached
trees included,

```text
sigma(A_r)>b_r,
(b_1,...,b_7)=(0,1,2,3,2,1,0).                       (2.2)
```

The only analytic absorption estimates used in residual locked packets are

```text
packing-one, one hostile Q and a triangles:
  sigma>a-delta_q;

common-cut T^kQ:
  sigma>k-delta_q                    if q=1 mod 4,
  sigma>k                            otherwise;

common-cut T^kP:
  sigma>k-delta;

common-cut T^kPP:
  sigma>k+1-4/(3sqrt(13)).                         (2.3)
```

The packing-one theorem is used only after directly checking that no two
triangles in the packet are vertex-disjoint. In every use below all relevant
triangles contain one hub. The theorem permits either direct contact with `Q`
or an arbitrary positive joining path and permits arbitrary trees on the core
and path. No packing-one decomposition theorem is assumed.

The common-cut theorem is scalar and is used only when every named cycle in the
packet really contains one common cut vertex. It is not extended to two pivots.

A triangle router has two or three distinct marks. With two marks, one marked
vertex is a singleton and the complementary edge is the other interval; with
three marks, the three singleton intervals are forced. Each incidence branch,
connector remnant, and off-hull tree follows the owner of its mark or unique
hull attachment. A second split refines one already induced territory. Thus all
router territories are induced, disjoint, connected, and exhaustive. A naked
private interval is a nonempty tree and has exact surplus `-1`.

These are local finite operations. We do not invoke the unproved census-free
separator Lemma S from the rank-uniform router note.

## 3. Exact sharp-DNN reduction

Let the nine cyclic blocks of `G` have lengths `l_1,...,l_9`. Since `G` has
cyclomatic rank nine,

```text
|E(G)|=|V(G)|+8.
```

Put

```text
epsilon_l=0                              if l is even,
epsilon_l=l tan^2(pi/(2l))               if l is odd.
```

The sharp cactus DNN estimate and cactus block counting give

```text
sigma(G)>=8-sum_i epsilon_(l_i).                       (3.1)
```

The odd sequence is strictly decreasing, and

```text
epsilon_3=1,
epsilon_5=5-2sqrt(5)=:a,
3a<2,
2a>1,
epsilon_5+epsilon_7<1.                                (3.2)
```

All comparisons are exact. For example, `3a<2` reduces after positive-side
squaring to `169<180`, and `2a>1` reduces to `80<81`.

If there are at most six triangles, then

```text
sum epsilon_i<=6+3a<8.
```

With exactly seven triangles, the two remaining cycles contribute at least one
only when both are pentagons: an even cycle contributes zero, and every other
odd pair is bounded by `epsilon_5+epsilon_7<1`. With at least eight triangles,
the multiset is `T^8Q`, allowing `Q=T`. Hence the complete DNN residual list is

```text
T^8Q={3,3,3,3,3,3,3,3,q}, q>=3,
T^7PP={3,3,3,3,3,3,3,5,5}.                            (3.3)
```

Every other rank-nine cactus has `sigma(G)>0` directly from (3.1). It remains
only to prove the two families in (3.3).

## 4. Shared-cut cluster dichotomy

Contract each maximal shared-cut cyclic cluster while retaining every actual
bridge connector. The reduced cluster graph is a tree. There are two exhaustive
possibilities:

1. it has more than one cluster, the **disconnected shared-cut** case; or
2. all nine cyclic blocks lie in one shared-cut cluster, the **fully shared**
   case.

Separations in the first case are made at actual bridge edges. No connector is
silently shortened to one edge. Every connector remnant and every branch on it
is assigned to one endpoint territory.

The exact colored cluster-partition census gives

| residual | all partitions | proper partitions | direct packet rows | structural rows |
|---|---:|---:|---:|---:|
| `T^8Q` | 67 | 66 | 63 | 3 |
| `T^7PP` | 118 | 117 | 109 | 8 |

The direct rows have positive exact packet ledgers. Reduced-tree leaf and path
pruning closes every structural row containing a usable singleton triangle: a
triangle leaf leaves a strict rank-eight complement, while a triangle next to a
distinguished end cycle forms a positive `TP` or `TQ` packet and leaves a
strict lower-rank complement. The only endpoint families requiring separate
work are the ones treated in Sections 5 and 6.

## 5. Every disconnected `T^8Q` cactus

After the exact color and reduced-tree reduction, the only endpoint is

```text
A_8 | Q.                                                (5.1)
```

Mark the first cyclic-hull entry of the actual connector to `Q`.

If the eight-triangle incidence is not locked at one common cut, a legal
triangle router has at most three marks: its incidence marks and, when present,
the private connector entry. Split it into proper intervals. If the `Q`
territory retains `k` triangles, then:

```text
k=1:       TQ is strict positive;
k=2:       TTQ is nonnegative and another triangular branch is strict;
3<=k<=7:  the retained rank-(k+1) packet is strict positive;
k=0:       the other seven triangles occupy at most two branches, so one
           branch has at least four triangles and surplus >3, absorbing Q>-1.
```

If the incidence is locked, all eight triangles contain one hub. Their packing
number is one, whether the connector enters at the hub or through a private
bouquet vertex. The one-hostile-cycle packing-one theorem applies to the actual
joining path and gives

```text
sigma(G)>8-delta_q>0.                                  (5.2)
```

For even or `3 mod 4` `Q`, the ordinary bridge packet is already nonnegative;
`Q=T` is included. Thus every disconnected `T^8Q` cactus is proved using only
finite routing or the directly checked packing-one packet.

## 6. Every disconnected `T^7PP` cactus

Reduced-tree pruning leaves two finite interface families:

```text
T^7P_0 | P_1,                                          (D9b)
P_0 | A_7 | P_1.                                       (D9a)
```

### 6.1 Entry-locked `T^7P_0|P_1`

Cases with internal `P_0`, or a leaf `P_0` entered privately, split by the
ordinary pentagon interval argument. In the remaining entry-locked family the
exact incidence-and-entry census has

| cut count | 1 | 2 | 3 | 4 | 5 | 6 | 7 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all `T^7P` incidences | 1 | 9 | 49 | 145 | 245 | 205 | 69 | 723 |
| `P`-leaf incidences | 1 | 6 | 30 | 79 | 120 | 86 | 23 | 345 |
| marked-entry classes | 2 | 29 | 195 | 661 | 1144 | 909 | 248 | 3188 |
| direct one-router certificates | 0 | 24 | 186 | 649 | 1134 | 909 | 248 | 3150 |
| finite replacements | 2 | 5 | 9 | 12 | 10 | 0 | 0 | 38 |

The 38 replacements use zero routers in two common-cut rows, one router in nine
rows, two routers in 22 rows, and three routers in five rows. The exact verifier
checks a legal split order, connected retained incidence components, every
common-cut or shared-cut hypothesis, each pentagonal deficit, each private
entry cost, and unique ownership. There is no failed row. The weakest ledger is

```text
1-2delta=5-2sqrt(5)>0.                                 (6.1)
```

Thus all 3188 entry-locked marked classes close by finite routing and scalar
packets.

### 6.2 Two arbitrary interfaces on `A_7`

For `P_0|A_7|P_1`, the two labelled connector entries may be cuts, private
triangle vertices, or coincident. The exact marked-interface census enumerates

```text
48 unmarked seven-triangle incidence trees,
10800 ordered labelled placements before automorphisms,
3188 canonical marked-interface classes.
```

The finite router automaton accepts 3182 classes: 3134 best certificates use one
router and 52 use two successive routers. Every accepted state has an integer
credit score at least one, hence

```text
sigma(G)>1-2delta>0.                                   (6.2)
```

The six residual marked classes all lie on the common-cut seven-triangle
bouquet. They close as follows:

| interfaces | finite replacement | ledger |
|---|---|---:|
| both at the hub | open one remote `P`; retain the other arm with the packing-one `A_7` bouquet | `>6-delta` |
| one hub, one private, either label order | split the privately entered triangle, giving `P +` common-cut `T^6P` | `>6-2delta` |
| coincident private entries | split once, giving `A_6+PP` | `>1` |
| distinct private vertices of one triangle | split into three singleton ports, giving `A_6+P+P` | `>1-2delta` |
| private vertices on two triangles | split twice, giving `A_5+P+P` | `>2-2delta` |

In the hub-hub row, opening four private vertices of one remote pentagon gives
one nonempty tree of surplus `-1`. The retained territory has seven pairwise
intersecting triangles and one hostile pentagonal arm, so the packing-one
theorem gives `>7-delta` before the opening cost. This is a one-hostile-cycle
packet, not a two-pivot argument.

Consequently all 3188 canonical two-interface classes close, and every
disconnected `T^7PP` cactus is proved.

## 7. Every fully shared `T^8Q` cactus

The exact color-preserving incidence census, by number `c` of shared cuts, is

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 11 | 68 | 253 | 572 | 742 | 493 | 127 | 2267 |
| `q=4` | 1 | 11 | 68 | 258 | 586 | 774 | 525 | 142 | 2365 |
| `q=5` | 1 | 11 | 68 | 258 | 589 | 781 | 536 | 148 | 2392 |
| `q=6` | 1 | 11 | 68 | 258 | 589 | 783 | 539 | 151 | 2400 |
| `q=7` | 1 | 11 | 68 | 258 | 589 | 783 | 540 | 152 | 2402 |
| `q>=8` | 1 | 11 | 68 | 258 | 589 | 783 | 540 | 153 | 2403 |

The ordinary exact split ledger leaves only the common-cut bouquet for even
`Q`. For the hostile odd ledger it can also leave one two-cut type: seven
triangles share one hub with a router triangle, and `Q` meets the router at its
other cut. In both types all eight triangles contain the same hub, so their
packing number is one.

The common-cut bouquet is closed by the scalar common-cut theorem. The two-cut
type is closed by the one-hostile-cycle packing-one theorem, which permits the
joining segment from the hub through the router to `Q`. In either case

```text
sigma(G)>8-delta_q>0                                   (7.1)
```

for hostile `Q`; the nonhostile cases have at least as strong a packet ledger.
Hence every fully shared `T^8Q` incidence is proved. The census is finite and
stabilizes because at most eight distinct cuts can meet `Q`.

## 8. Every fully shared `T^7PP`: `8004=7997+7`

The exact color-preserving census gives

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 17 | 150 | 699 | 1856 | 2714 | 1998 | 569 | 8004 |
| ordinary-split safe | 0 | 15 | 148 | 698 | 1855 | 2714 | 1998 | 569 | 7997 |
| exceptions | 1 | 2 | 2 | 1 | 1 | 0 | 0 | 0 | 7 |

Every one of the 7997 safe rows has an exact legal cycle split and positive
packet ledger. The seven exceptions have these replacements:

| code | replacement | certified surplus |
|---|---|---:|
| N1 | common-cut `T^7PP` | `>8-4/(3sqrt(13))` |
| F9 | open the leaf pentagon; retain common-cut `T^7P` | `>6-delta` |
| N2 | `P +` common-cut `T^6P` | `>6-2delta` |
| N3 | `P+T+` common-cut `T^5P` | `>5-2delta` |
| N4 | `P+P+A_5` | `>2-2delta` |
| N5 | `P+P+T+A_4` | `>3-2delta` |
| N6 | `P+P+T+T+A_3` | `>2-2delta` |

N2--N6 use one or two legal triangle-router refinements. N1 is an actual
single-pivot bouquet and uses only the scalar common-cut theorem.

For F9, seven triangles and `P_0` share `x`, while leaf pentagon `P_1` meets
`P_0` at a second cut `y`. Splitting the router pentagon would leave the
insufficient ledger `A_7+P_1>-delta`; that split is not used. Instead open
`P_1` by assigning its four private vertices and all trees rooted there to a
nonempty tree `E`. Keep `y`, `P_0`, all seven triangles, and all other branches
in `H`. Then

```text
sigma(E)=-1,
sigma(H)>7-delta                       (common-cut T^7P_0),
sigma(G)>=sigma(H)+sigma(E)>6-delta>0.                  (8.1)
```

This opening preserves the scalar pivot `x` and uses no two-pivot estimate.
Therefore all seven exceptions close and the exact resolution is
`8004=7997+7` with `7/7` positive replacements.

## 9. Exhaustion

Every connected rank-nine cactus now occurs in exactly one covered class:

1. A nonresidual cycle multiset is strict by the exact DNN inequality.
2. A residual `T^8Q` or `T^7PP` cactus with more than one shared-cut cluster is
   covered by the disconnected partition reduction and Sections 5--6.
3. A fully shared `T^8Q` cactus is one of the exact finite incidence types in
   Section 7.
4. A fully shared `T^7PP` cactus is one of the 8004 exact incidence types in
   Section 8.

Every bridge separation is at an actual bridge. Every router partitions actual
cycle vertices into proper intervals. Every shared cut, incidence branch,
connector remnant, and attached tree has exactly one owner. The analytic packet
hypotheses are checked on the retained packets: common-cut estimates only at a
real common pivot, and packing one only for a real common-hub triangular
family. The only openings have their exact nonempty-tree cost `-1` recorded.

There is no residual family and no appeal to the unsupported two-pivot phase
theorem. Thus `sigma(G)>0`, proving the theorem.

## 10. Exact reproduction

Run from the repository root with Python 3.10 or newer:

```bash
python3 research/rank-nine-cactus-residual-census.py
python3 research/nonacyclic-fully-shared-incidence-census.py
python3 research/nonacyclic-t7p-last-bridge-conservative.py
python3 research/nonacyclic-t7-two-interface-census.py
python3 research/nonacyclic-t7pp-seven-exceptions-resolution.py
python3 positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

The first five scripts use the Python standard library and exact integer or
`Fraction` arithmetic. The last script uses SymPy and checks the finite
positive-coefficient inequality behind the common-cut two-pentagon bound. The
scripts certify their finite enumerations, canonical digests, router recipes,
ownership data, and exact ledgers; the analytic packet inequalities are proved
in the cited Schur--Sachs and packing-one notes.
