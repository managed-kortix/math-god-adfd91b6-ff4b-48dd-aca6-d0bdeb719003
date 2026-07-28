# Positive square energy of every connected octacyclic cactus

**Date:** 2026-07-26

## 1. Theorem and validity boundary

For a graph `G`, write

```text
s+(G)=sum_{lambda_i>0} lambda_i^2,
sigma(G)=s+(G)-|V(G)|,
T=C3, P=C5, delta=sqrt(5)-2<1/4.
```

**Theorem.** Every connected octacyclic cactus `G` satisfies

```text
s+(G)>|V(G)|.
```

This proof does not use the then-retracted, now restored, all-rank rooted
hostile-cycle guard. In particular, it does not depend on the now-verified
assertion that maximum triangle packing forces every nearest-cycle Voronoi
territory to have packing number one. The
only hostile-cycle packet used below is the standalone packing-one Sachs packet, and
its packing-one hypothesis is checked directly for a common-cut triangle
bouquet. The disconnected two-pentagon family is proved instead by the global
strict-last-bridge `877=861+16` certificate. The fully shared two-pentagon family is
proved by the independent `2116=2110+6` incidence census and the six replacement
resolutions.

### Theorem-source locator

The publication proof uses the following four provenance packages. The old
uncut `877=868+9` / E1--E9 artifacts and the all-rank guard are not
dependencies.

| proof role | authoritative source | scope used here |
|---|---|---|
| disconnected `G6PP` | `research/octacyclic-t6p-last-bridge-conservative-resolution-2026-07-26.md` | strict last-bridge `877=861+16`, `16/16` closure |
| bridge-separated hostile `G7Q` | `research/octacyclic-packing-one-hostile-cycle-lemma-2026-07-26.md` | one hostile cycle plus a triangular family of vertex-packing number one |
| fully shared common-pivot bouquets | `research/common-cut-bouquet-rooted-schur-2026-07-26.md` | common-cut `T^kQ` and `T^kPP` bounds |
| fully shared `T^6PP` | `research/octacyclic-fully-shared-incidence-census-2026-07-26.md` and `research/octacyclic-t6pp-six-exceptions-resolution-2026-07-26.md` | `2116=2110+6`, with six replacement packetizations |

In the strict certificate, `TTP` means a connected three-cycle packet containing
two triangles and one pentagon in which the two triangles share a cut. The
pentagon belongs to the same packet but need not share that triangle cut.
Accordingly, "shared-cut `TTP`" is not shorthand for a common-cut `T^2P`
bouquet. By contrast, "common-cut `T^kP`" or "common-cut `T^kPP`" means that
all named cycles share one pivot. This terminology is used consistently below.

All packet estimates used here allow arbitrary finite trees at arbitrary core
vertices. Every connector cut and cycle split below is also audited explicitly:
connector vertices, Steiner branches, and hanging trees always have one owner.

## 2. General inputs

Positive square energy is superadditive over induced vertex partitions. Thus,
if `V(G)` is partitioned into induced territories `G_1,...,G_j`, then

```text
sigma(G)>=sum_i sigma(G_i).
```

The established cactus estimates used in the packet ledgers are:

```text
rank 2 or 3:                       sigma>=0,
rank 4, 5, 6, or 7:               sigma>0,
pentagonal unicyclic packet P:     sigma>=-delta,
hostile C_q packet Q:              sigma>=-delta_q,
delta_q=sec(pi/q)-1<1,
TP:                                sigma>1-delta,
one shared cluster PP:             sigma>0,
TPP:                               sigma>3/2.
```

For a connected shared-cut cluster `A_r` of `r` triangles, with arbitrary
attached trees,

```text
sigma(A_r)>b_r,
(b_1,...,b_7)=(0,1,2,3,2,1,0).                  (2.1)
```

The rank-four value in (2.1) is the corrected matching-injection bound
`sigma(A_4)>3`; it is not based on a multiplicity-blind Sturm calculation.
Successive incidence-leaf openings give the stated `A_5,A_6,A_7` bounds.

Two further valid analytic packets are used:

```text
packing-one hostile packet:
  sigma(Q plus a>=1 triangles)>a-delta_q;

common-cut Schur-Sachs packets:
  sigma(common-cut T^kQ)>k-delta_q       if q=1 mod 4,
  sigma(common-cut T^kQ)>k               otherwise,
  sigma(common-cut T^kPP)>k+1-4/(3sqrt(13)).       (2.2)
```

The packing-one packet, proved in
`research/octacyclic-packing-one-hostile-cycle-lemma-2026-07-26.md`, permits a
common vertex or an arbitrary positive joining path and arbitrary attached
trees. It follows from the exact grouped Sachs
formula with at most one triangular cycle in a Sachs collection. No extension
from packing one to arbitrary rank is made. The common-cut theorem is a separate
scalar Schur-Sachs result and is used only when all named cyclic blocks really
share one pivot.

Every cycle split in this proof partitions the split cycle into nonempty proper
consecutive intervals, one interval for each distinct mark. The whole incidence
branch at a mark follows that mark's owner. An off-hull cactus component has a
unique hull attachment and follows its owner's territory. A second router split
only refines one territory from the first split, so inducedness and unique
ownership persist.

## 3. Exact DNN reduction

Let the eight cyclic blocks have lengths `l_1,...,l_8`. Since an octacyclic
connected graph has `m=n+7`, cactus block counting and the sharp cactus DNN
estimate give

```text
sigma(G)>=7-sum_i epsilon_(l_i),
epsilon_l=0                         for even l,
epsilon_l=l tan^2(pi/(2l))          for odd l.             (3.1)
```

The odd sequence is decreasing, `epsilon_3=1`, and, with
`a=epsilon_5=5-2sqrt(5)`, the exact comparisons

```text
3a<2, 2a>1, epsilon_5+epsilon_7<1                  (3.2)
```

give the exhaustive classification. At most five triangles imply
`sum epsilon<=5+3a<7`. With exactly six triangles, the remaining pair reaches
one only for two pentagons. At least seven triangles gives the family `T^7Q`.
Consequently (3.1) is strictly positive outside exactly

```text
T^7Q={3,3,3,3,3,3,3,q}, q>=3,
T^6PP={3,3,3,3,3,3,5,5}.                         (3.3)
```

It remains to prove these two residual families.

## 4. Disconnected shared-cut graph: exact partition census

Contract each shared-cut cycle cluster and retain the actual bridge connections
between clusters. The resulting reduced cluster graph is a tree. Cutting an
edge of this tree means cutting an actual bridge of `G`, not deleting an
arbitrary connector vertex. All vertices on each resulting connector remnant,
including every branch off it, remain with one endpoint territory.

The exact colored cluster-partition census gives:

| residual | all partitions | proper partitions | direct packet rows |
|---|---:|---:|---:|
| `T^7Q` | 45 | 44 | 42 |
| `T^6PP` | 77 | 76 | 70 |

The two `T^7Q` structural rows are

```text
Q|T|T|T|T|T|T|T,  Q|T^7.                         (4.1)
```

The six `T^6PP` structural rows are

```text
P|P|T|T|T|T|T|T,
P|T|T|T|T|T^2P,
P|T|T|T|T^3P,
P|T|T|T^4P,
P|T|T^5P,
P|T^6P.                                           (4.2)
```

The census uses exact `Fraction` arithmetic. Every omitted proper partition has
a positive packet ledger, with strictness recorded rather than inferred from a
numerical approximation.

### 4.1 Disconnected `T^7Q`

In the all-singleton row of (4.1), some singleton triangle is a leaf of the
finite reduced tree. Cutting its first bridge gives a strict triangular packet
and a connected heptacyclic complement, so this row is positive.

Consider `T^7|Q`. If the seven-triangle incidence tree is not a bouquet, split
an internal triangle at its cyclic marks and at a private connector-entry mark
when one is present. If the `Q` territory retains `r` triangles, then `r>=3` is
strict by rank, `r=2` is nonnegative with another strict triangular branch, and
`r=1` is a positive `TQ` packet. If `r=0`, the entry consumes one of the at most
three triangle marks, so the other six triangles occupy at most two branches;
one branch contains at least three triangles and has surplus `>2`, which pays
the isolated hostile bound `>-1`. These are legal proper interval splits and
cover every nonbouquet incidence.

If the triangle cluster is a bouquet but the connector enters at a private
triangle vertex, splitting that triangle at the common cut and entry yields
`A_6+Q`, with surplus `>1-delta_q>0`. The sole locked case is therefore:

```text
seven triangles share x, and Q is joined to x by an arbitrary positive
connector, possibly with arbitrary trees on the connector and core.   (G7Q)
```

For hostile `Q`, the seven triangles in this packet are pairwise intersecting
at `x`; hence their vertex-packing number is exactly one. Apply the valid
packing-one hostile packet directly, with `a=7`. It gives

```text
sigma(G7Q)>7-delta_q>0.                              (4.3)
```

This is not an application of the all-rank theorem: the hypothesis of
the retained packing-one lemma is verified on the packet itself, and that lemma
already allows the arbitrary joining path and all attached trees. If `Q` is
even or `3 mod 4` (including `Q=T`), its unicyclic packet is nonnegative and
`A_7` is strict, so the bridge partition also closes the case. Thus every
disconnected `T^7Q` cactus is proved.

### 4.2 Preliminary disconnected `T^6PP` rows

For the first five rows of (4.2), a singleton-triangle leaf gives `T` and a
heptacyclic complement. If no singleton triangle is a leaf, the two nontriangle
endpoint clusters are the leaves and the reduced tree is their path. Pair the
singleton triangle nearest the singleton pentagon with that pentagon; this
gives a positive `TP` terminal packet and a strict hexacyclic complement.

The separate row `P_0|T^6|P_1` is also positive. Cut its two actual bridge
interfaces, assign every connector remnant to one of the three territories,
and use

```text
sigma(G)>sigma(A_6)-2delta>1-2delta=5-2sqrt(5)>0.   (4.4)
```

Only `T^6P_0|P_1` remains. If `P_0` is internal in its cluster, split it into
proper intervals, one per incidence branch. The branch receiving `P_1` is a
mixed lower-rank packet and another triangular branch is strict. If `P_0` is an
incidence leaf but the connector entry projects to a private vertex of `P_0`,
split between that entry and its unique cyclic cut to obtain
`A_6+P_1>1-delta>0`. The remaining entry-locked family is `(G6PP)`.

### 4.3 Strict-last-bridge `G6PP`: `877=861+16`

Cut the last actual connector bridge before the remote pentagon `P_1`. Its
territory is pentagonal unicyclic and contributes at least `-delta`. The entire
connector remnant on the `T^6P_0` side becomes a tree rooted at its marked first
cyclic-hull entry. No connector or branch vertex is discarded.

The color-preserving incidence census contains

```text
all T^6P_0 incidence trees:        226,
P_0-leaf incidence trees:          111,
marked cyclic-entry root classes:  877.                    (4.5)
```

The root classes include every shared cut and every private cyclic triangle
position modulo colored automorphism. Connector lengths and hanging trees are
not finite parameters because each follows its unique marked owner.

For each class, the exact verifier first tries the conservative one-router
ledger after the bridge to `P_1` has been cut. It proves 861 classes and leaves
16, distributed by cut number as

```text
c=1,2,3,4,5,6: 2,5,5,4,0,0.                       (4.6)
```

All 16 replacement resolutions are verified independently:

| classes | operation | clustered-side packets | total including `P_1` |
|---|---|---|---:|
| L1--L2 | no split | common-cut `T^6P_0` | `>6-2delta` |
| L3--L6 | one router | `T+` common-cut `T^4P_0` | `>4-2delta` |
| L7 | one router plus entry tree | `T+` common-cut `T^4P_0+E` | `>3-2delta` |
| L8--L10, L12 | two routers | `T+T+` common-cut `T^2P_0` | `>2-2delta` |
| L11 | two routers plus entry tree | `T+T+` common-cut `T^2P_0+E` | `>1-2delta` |
| L13--L16 | two routers | `T+T+` shared-cut `TTP_0` | `>2-2delta` |

Here `E` is the acyclic private-entry interval with surplus at least `-1`.
Common-cut means every cycle in the packet shares one cut. Shared-cut `TTP`
has the locator-table meaning: the two retained triangles share a cut, while
`P_0` may meet that lobe at a different cut; its bound in the strict certificate
is `>2-delta`. Each incidence side,
entry remnant, and attached tree has exactly one owner for every cyclic order.

The weakest row is L11:

```text
T+T+common-cut T^2P_0+P_1+E,
sigma(G)>0+0+(2-delta)-delta-1
        =1-2delta=5-2sqrt(5)>0.                    (4.7)
```

This proves all `877=861+16` marked classes without a rooted theorem and with
no residual. The defective uncut E1--E9 completeness claim is superseded; its
connector ownership is not used. Hence every
disconnected `T^6PP` cactus is proved.

## 5. Fully shared `T^7Q`

For one shared-cut cluster, the exact color-preserving incidence-tree counts are:

| `Q` capacity | counts by cut number `c=1,...,7` | total |
|---|---|---:|
| `q=3` | `1,9,49,142,236,191,60` | 688 |
| `q=4` | `1,9,49,145,243,202,66` | 715 |
| `q=5` | `1,9,49,145,245,205,69` | 723 |
| `q=6` | `1,9,49,145,245,206,70` | 725 |
| `q>=7` | `1,9,49,145,245,206,71` | 726 |

The exact ordinary-split ledger proves every nonbouquet incidence. The unique
exception in every capacity regime is the one-cut bouquet in which all seven
triangles and `Q` share one vertex. Apply the common-cut theorem (2.2) directly:

```text
sigma(T^7Q)>7-delta_q>6     for hostile Q,
sigma(T^7Q)>7               otherwise.             (5.1)
```

This use is within the theorem's scalar common-pivot scope. Arbitrary rooted
trees are absorbed by its exact matching-message Schur reduction. Thus every
fully shared `T^7Q` cactus is proved.

## 6. Fully shared `T^6PP`: `2116=2110+6`

The exact color-preserving census gives:

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 14 | 106 | 377 | 728 | 657 | 233 | 2116 |
| ordinary-split safe | 0 | 13 | 104 | 376 | 727 | 657 | 233 | 2110 |
| exceptions | 1 | 1 | 2 | 1 | 1 | 0 | 0 | 6 |

The 2110 safe types have an exact legal ordinary cycle split with a positive
packet ledger. The six replacement resolutions are:

| code | replacement packetization | certified surplus |
|---|---|---:|
| U1 | common-cut `T^6PP` | `>7-4/(3sqrt(13))` |
| U2 | `P +` common-cut `T^5P` | `>5-2delta` |
| U3 | `P + T +` common-cut `T^4P` | `>4-2delta` |
| U4 | `P + P + A_4` | `>3-2delta` |
| U5 | `P + P + T + A_3` | `>2-2delta` |
| U6 | `P + P + T + T + A_2` | `>1-2delta` |

U1 is exactly the common-cut `(6,2)` bouquet and uses the two-pentagon
Schur-Sachs inequality without splitting its common vertex. U2 splits one
binary router, leaving one isolated pentagon and an actual common-cut `T^5P`
packet. U3 splits one saturated router into `P`, `T`, and an actual common-cut
`T^4P` packet. U4 splits two binary routers, leaving `P+P+A_4`. U5 first splits
a saturated router and then a binary router, leaving `P+P+T+A_3`. U6 splits
two saturated routers successively, leaving `P+P+T+T+A_2`.

For degree two, the marked pentagon-side vertex is a singleton and the other
two router vertices form the complementary interval. For degree three, all
three marks occupy distinct triangle vertices and the singleton intervals are
forced. Every pentagon's unique cut stays with that pentagon; every common hub
cut has one owner; router remnants are trees; and every off-hull tree follows
its unique core attachment. Therefore these packetizations work for every
cyclic mark order and every assignment of attached trees, not merely for one
drawn representative of each incidence code.

The weakest case is U6:

```text
sigma(G)>-delta-delta+0+0+1
        =1-2delta=5-2sqrt(5)>0.                    (6.1)
```

Hence all `2116=2110+6` fully shared `T^6PP` types are proved without the
rooted hostile-cycle guard.

## 7. Exhaustion and connector/tree audit

Every connected octacyclic cactus is now covered:

1. The DNN inequality proves every nonresidual cycle multiset.
2. The exact disconnected partition census, reduced-tree argument, valid
   packing-one treatment of `(G7Q)`, and strict `877=861+16` certificate prove
   both residual families when the shared-cut graph is disconnected.
3. The fully shared `T^7Q` census plus the common-cut theorem proves all fully
   shared `T^7Q` incidences.
4. The fully shared `T^6PP` census and six replacement resolutions prove all
   `2116` fully shared `T^6PP` incidences.

No arbitrary connector is replaced by a single edge without an ownership
argument. Reduced-tree separations occur at actual bridges. The remote `P_1`
cut in `(G6PP)` keeps every remaining connector vertex on the marked cluster
side. In `(G7Q)`, the valid packing-one packet itself permits every positive
joining-path length and trees on its internal vertices. Router refinements
partition actual triangle vertices into proper intervals and assign all
incidence branches uniquely. Every component outside the cyclic hull has one
hull attachment in a cactus and is assigned whole to that attachment's owner.

Thus all territories used for superadditivity are induced, disjoint, and
exhaustive; all packet bounds retain their arbitrary-tree hypotheses; and no
retracted rooted all-rank theorem remains in the proof. Therefore

```text
sigma(G)>0,
```

which proves the theorem.

## 8. Exact certificates

Run from the repository root:

```bash
python research/octacyclic-disconnected-partition-census.py
python research/octacyclic-t6p-last-bridge-conservative.py
python research/octacyclic-g6pp-last-bridge-census.py
python research/octacyclic-t6p-last-bridge-sixteen-resolution.py
python research/octacyclic-g6pp-last-bridge-four-resolution.py
python research/octacyclic-fully-shared-incidence-census.py
python positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

The census and packet verifiers use exact integer or rational arithmetic. The
last script verifies the finite positive-coefficient inequality used by the
two-pentagon common-cut Schur-Sachs theorem.
