# Exact sacrifice and splitting lemmas for the heptacyclic residuals

## Scope

Write

`sigma(H)=s+(H)-|V(H)|`, `T=C3`, `P=C5`,

and let `Q=Cq`, `q>=3`. This note treats one fully shared cycle cluster with
cycle multiset

`T^6Q={T,T,T,T,T,T,Q}` or `T^5PP={T,T,T,T,T,P,P}`.

It gives exact induced-territory lemmas for the three local mechanisms most
likely to appear as exceptions to an ordinary heptacyclic census:

1. a common-cut lock;
2. a saturated hub;
3. triangles dispersed among several hub branches.

The main point is that these are not three unrelated exceptions. For `T^6Q`,
opening a leaf `Q` and splitting an internal `Q` form an exhaustive dichotomy.
For `T^5PP`, opening both pentagons when both are incidence leaves and splitting
an internal pentagon form an exhaustive dichotomy. Thus no color-preserving
incidence census is needed for a single fully shared cluster once the stated
packet inputs are admitted.

This note does not treat a disconnected shared-cut graph, a nontrivial reduced
cluster tree, or the entry-sensitive release of a leaf cluster across bridges.
It therefore does not prove the heptacyclic theorem.

## 1. Inputs and conventions

For `r>=1`, let `A_r` denote a connected cactus whose cyclic blocks are exactly
`r` triangles in one shared-cut cluster, with arbitrary trees attached. The
shared triangular recurrence gives

`sigma(A_r)>b_r`, where

| `r` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `b_r` | 0 | 1 | 2 | 3 | 2 | 1 | 0 |

For `r<=4`, this is the established `>r-1` packet margin. For `r>=4`, it is
the exact certified recurrence

`b_4=3`, `b_r=b_(r-1)-1=7-r`.

We also use the existing lower-rank margins

`sigma(P)>=-delta`, `sigma(TP)>1-delta`, `sigma(TT)>1`,

where `delta=sqrt(5)-2<1`, together with generic nonnegativity for tricyclic
cacti and strict positivity for tetracyclic and pentacyclic cacti.

Let `I` be the bipartite cycle-cut incidence tree of the fully shared cluster.
Deleting a cycle node `C` of incidence degree `d` leaves exactly `d` incidence
branches. Each branch contains at least one other cycle node: the cut node next
to `C` has degree at least two. The cycles in one branch form one shared-cut
cluster.

Two standard induced operations will be used.

- **Private opening.** If `v` is a non-cut vertex of `C`, put `v` and every
  off-core branch rooted at `v` into a nonempty tree territory `F`. Then
  `sigma(F)=-1`; the path `C-v` remains with the complementary territory and
  contains every cyclic cut of `C`.
- **Hub split.** If `deg_I(C)=d>=2`, assign the `d` cyclic marks, in cyclic
  order, to `d` nonempty proper consecutive intervals of `C`, one interval per
  mark. The interval at a mark and the corresponding branch of `I-C` form a
  connected induced territory. Every mark has exactly one owner, `C` is
  retained by no territory, and there is no separate tree cost.

The one-mark-per-interval form is always available when `d>=2`: cut one cycle
edge in each gap selected between successive marked vertices, assigning any
unmarked vertices in that gap to either adjacent interval. All hanging trees
follow their unique cycle attachment.

## 2. The `T^6Q` leaf-or-split lemma

**Lemma 2.1 (distinguished-cycle dichotomy).** Let the seven cycles of a
connected cactus form one shared-cut cluster of type `T^6Q`. Then
`sigma(G)>0`. More precisely, exactly one of the following two constructions
applies to the distinguished node `Q`.

1. If `deg_I(Q)=1`, open one private vertex of `Q`. The remainder is an
   `A_6` territory and

   `sigma(G)>=sigma(A_6)-1>1-1=0`.

2. If `deg_I(Q)=d>=2`, split `Q` into one proper consecutive interval per
   branch of `I-Q`. If branch `j` contains `r_j` triangles, then

   `r_1+...+r_d=6`, `r_j>=1`,

   and the resulting exact induced territories are `A_(r_1),...,A_(r_d)`.
   Hence

   `sigma(G)>=sum_j sigma(A_(r_j))>sum_j b_(r_j)>=0`.

**Proof.** If `Q` is an incidence leaf, it has one cyclic cut and therefore at
least `q-1>=2` private vertices. Opening one of them costs exactly one. Removing
a leaf cycle node from an incidence tree leaves the other cycle nodes connected
after an irrelevant binary cut node, if any, is suppressed. Thus the six
triangles remain one shared-cut cluster, and the `A_6` recurrence pays the
opening strictly.

If `Q` is internal, every component of `I-Q` contains at least one triangle and
contains no nontriangle. The hub split gives one induced territory per
component. Its retained cycles are precisely the triangles in that incidence
component, so it is an `A_(r_j)` packet after the proper path interval of `Q`
and all attached trees are absorbed as tree attachments. Every `b_r` in the
table is nonnegative and every packet inequality is strict. Therefore the
packet sum is strictly positive, even when all `r_j=1`. QED.

The lemma is uniform in the length and parity of `Q`. In particular, no hostile
singleton `Q` is retained in the split case, and no DNN deficit for `Q` is
charged in the opening case.

## 3. Exact common-cut consequences

**Corollary 3.1 (`T^6Q` common-cut sacrifice).** Suppose all seven cycles share
one cyclic cut `x`. Open any vertex of `Q` other than `x`, together with all
tree branches rooted there. The six triangles remain an `A_6` bouquet, so the
exact partition satisfies

`sigma(G)>=sigma(A_6)-1>0`.

Only one sacrifice is needed. This is stronger than opening `Q` and two
triangles and retaining an `A_4` packet; both ledgers end strictly positive,
but the one-opening form spends less of the triangular margin.

**Lemma 3.2 (`T^5PP` common-cut sacrifice).** Suppose all five triangles and
both pentagons share one cyclic cut `x`. Open one private vertex on each
pentagon. The rooted opening territories are disjoint nonempty trees, the path
remnants retain `x`, and the five triangles remain an `A_5` bouquet. Hence

`sigma(G)>=sigma(A_5)-2>2-2=0`.

**Proof.** Each pentagon has four vertices different from `x`, so the two
private choices exist. Distinct cyclic blocks intersect only at `x`, hence the
two rooted territories are disjoint. The private-opening lemma gives two exact
tree costs, while the triangular recurrence gives the strict `A_5` margin.
QED.

These statements also explain the common-cut ownership rule. All retained
triangles belong to one territory containing `x`; no attempted partition gives
`x` to two retained packets. The sacrificed cycles leave paths through `x` but
are retained by none.

## 4. The `T^5PP` leaf-or-split lemma

**Lemma 4.1 (two-pentagon dichotomy).** Let the seven cycles of a connected
cactus form one shared-cut cluster of type `T^5PP`. Then `sigma(G)>0` by one of
the following exact constructions.

1. If both pentagon nodes are leaves of `I`, open one private vertex on each.
   The five triangles remain one `A_5` cluster and

   `sigma(G)>=sigma(A_5)-2>0`.

2. Otherwise choose an internal pentagon `P_0`, of incidence degree
   `2<=d<=5`, and split it into one proper consecutive interval per branch of
   `I-P_0`. Let `B` be the unique branch containing the other pentagon `P_1`,
   and let `a` be the number of triangles in `B`.

   - If `a>=1`, then `1<=a<=4`. The `B` packet is `T^aP`: it is positive for
     `a=1`, nonnegative for `a=2`, and positive for `a=3,4`. At least one other
     branch is an all-triangle packet and is strictly positive. The total split
     is therefore positive.
   - If `a=0`, then `B` is a singleton pentagon with surplus at least `-delta`.
     The five triangles occupy at most `d-1<=4` other nonempty branches. One
     branch consequently contains at least two triangles and has surplus
     `>1`; every remaining all-triangle branch is strict. Thus the total is

     `>1-delta>0`.

**Proof.** If both pentagons are leaves, each has four private vertices. Delete
the two leaf cycle nodes successively. A tree remains connected after leaf
deletion, so the retained triangle nodes form one shared-cut incidence tree.
The two private openings are disjoint and cost exactly two; `A_5` pays them.

Otherwise an internal pentagon exists. The hub split is an exact induced vertex
partition and incurs no opening cost. There is exactly one branch containing
`P_1`; all other branches contain only triangles. Every branch is nonempty in
cycle nodes. Therefore, if `B` contains `a>=1` triangles, at least one triangle
lies outside `B`, proving `a<=4` and supplying a separate strict all-triangle
packet. The stated lower-rank estimates for `TP`, generic tricyclic `TTP`,
tetracyclic `TTTP`, and pentacyclic `T^4P` give the first ledger.

If `a=0`, distribute five triangles among at most four nonempty branches. The
pigeonhole principle gives a branch with at least two triangles. Its shared-cut
cluster is `A_r` for some `r>=2`, and hence has margin at least the strict
`A_2` margin `>1` (for `r=2,3,4,5` the table gives a bound no smaller than one).
This absorbs `-delta`, while every other branch remains strict. QED.

The proof deliberately splits an internal pentagon rather than opening it.
Opening an internal pentagon can preserve ordinary connectivity while
dispersing the retained triangles; the interval split turns that dispersion
into useful packet territories and pays no tree cost.

## 5. Saturated-hub lemmas

The preceding dichotomies contain the saturated cases, but the following forms
are convenient as named census repairs.

**Corollary 5.1 (saturated `Q` hub).** In `T^6Q`, suppose `Q` is incident with
`d>=2` distinct cyclic cuts, possibly all `q` vertices when `d=q`. Split `Q`
at its marked vertices. Every branch packet is an `A_r` with `r>=1`; therefore
the total surplus is positive. In the six-petal case the visible packetization
is

`T+T+T+T+T+T`.

No private vertex of `Q` is required. If several triangles lie in one branch,
the corresponding symbol is `A_r`, not a collection of illegally separated
cycles sharing a cut.

**Corollary 5.2 (saturated pentagon hub).** In `T^5PP`, suppose a pentagon
`P_0` uses all five vertices as distinct cyclic cuts. Split `P_0` into five
one-mark intervals.

- If the `P_1` branch contains a triangle, that branch is nonnegative or
  positive and another triangular branch is strict.
- If `P_1` is a singleton petal, the five triangles occupy the other four
  branches, so one is an `A_r` packet with `r>=2`. The resulting ledger is at
  least

  `P + A_r +` strict triangular packets `> -delta+1>0`.

For the smallest simple petal model, exactly one triangular mark is multiway
and the visible pattern is

`P+TT+T+T+T`,

whose fixed part has surplus `>1-delta`. Unlike the rank-six `T^4PP`
saturated hub, no adjacent-mark merge into `TP` is needed: the extra fifth
triangle forces the `TT` branch which pays the singleton pentagon deficit.

## 6. Dispersed-triangle splitting

**Lemma 6.1 (dispersed `T^6Q` branches).** Suppose deleting the `Q` node leaves
`d>=2` triangle-bearing incidence components of sizes
`r_1,...,r_d`. Regardless of how small their individual margins are, splitting
`Q` gives

`A_(r_1)+...+A_(r_d)`

with a strictly positive total. In particular the three-arm obstruction

`TT+TT+TT`

has surplus `>3`, while the maximally dispersed pattern of six singleton
triangles is still strict positive, though it has no certified uniform margin.

**Lemma 6.2 (dispersed `T^5PP` branches).** Suppose `P_0` is internal and is
split. Dispersion is harmless under the exact alternatives in Lemma 4.1:

- a branch containing `P_1` and at least one triangle is nonnegative and is
  accompanied by a strict all-triangle branch;
- a singleton `P_1` is accompanied by at most four all-triangle branches whose
  sizes sum to five, forcing one branch with margin `>1`.

Thus the two potentially hostile phenomena cannot coincide at rank seven:
`P_1` cannot be a singleton branch while all five triangles are singleton
branches, because that would require six branches on the five-vertex hub
`P_0`.

**Proof of both lemmas.** These are the branch ledgers in Lemmas 2.1 and 4.1.
Their topological content is the consecutive-interval construction: each
incidence component receives exactly one hub mark and one proper path interval,
so no shared cut or hub vertex has two owners. QED.

## 7. A separate margin audit for two-pentagon opening

The concentrated opening in Lemma 4.1 is the clean operation. For comparison,
suppose some other construction legally opens both pentagons and then produces
interval-compatible induced all-triangle territories with shared-cut component
sizes forming a partition `lambda` of five. The recurrence gives the following
exact proof credits before the two tree costs:

| `lambda` | certified sum of `b_r` |
|---|---:|
| `5` | 2 |
| `4+1` | 3 |
| `3+2` | 3 |
| `3+1+1` | 2 |
| `2+2+1` | 2 |
| `2+1+1+1` | 1 |
| `1+1+1+1+1` | 0 |

Because every packet estimate is strict, the first five rows pay two openings
and leave strict positivity. The last two rows do not pay two costs from the
triangular recurrence alone. This table sharpens the warning that
"dispersion loses the five-triangle margin": some dispersed partitions are
better than the concentrated `A_5` bound, while only `2+1+1+1` and `1^5`
remain uncertified by this ledger.

The table is conditional on an actual compatible induced partition. Ordinary
connectivity through two opened pentagon path remnants does not by itself make
the triangle components interval-compatible, and it does not assign ownership
at both remnants.

## 8. Exact census targets and what happens to them

The independent ordinary-split censuses provide a useful check on the two
dichotomies.

For fully shared `T^6Q`, the census has exactly one unresolved type in every
capacity regime `q=3,4,5,6,>=7`: the seven-cycle bouquet. Corollary 3.1 closes
it by one opening. Every nonbouquet type already has an ordinary positive
split; Lemma 2.1 supplies the simpler uniform distinguished-`Q` construction.

For fully shared `T^5PP`, the conservative ordinary ledger resolves `557` of
`560` color-preserving incidence trees. Its three canonical exceptions are:

1. the seven-cycle bouquet;
2. a six-cycle common-cut core `T^5P` with a `TP` tail;
3. a five-triangle common-cut core with two separate pentagon tails.

In all three, both pentagon nodes are incidence leaves. Lemma 4.1(1) therefore
opens private vertices on both pentagons. Deleting those two leaf nodes leaves
the five triangle nodes connected in the retained incidence tree: at the common
cut in the bouquet, at the six-cycle common cut in the second type, and at the
five-triangle common cut in the third. Thus each exception has one `A_5`
territory and two disjoint tree territories, with exact ledger `>2-2=0`.

The following table also records the anticipated local repair for the broader
structural cores which motivated the lemmas.

| rooted core | residual | exact repair |
|---|---|---|
| universal common-cut bouquet | `T^6Q` | open `Q`; retain `A_6`; net `>0` |
| universal common-cut bouquet | `T^5PP` | open both `P`; retain `A_5`; net `>0` |
| saturated `Q` hub | `T^6Q` | split `Q` into all-triangle branch packets |
| three-arm dispersed `Q` router | `T^6Q` | `TT+TT+TT` |
| saturated pentagon hub with singleton `P` petal | `T^5PP` | `P+A_r+...`, some `r>=2`; net `>1-delta` |
| internal pentagon with mixed `P` branch | `T^5PP` | split hub; mixed branch nonnegative plus a strict triangle branch |
| both pentagons incidence leaves | `T^5PP` | simultaneous two-opening sacrifice |

The rank-seven `T^5PP` census has no unresolved saturated hub; Lemma 4.1(2)
explains why its ordinary split is automatically accepted. At rank six, the
analogous `T^4PP` saturated pentagon hub has four triangles
in four non-pentagonal branches and therefore needs an adjacent interval merge
to form `TP`. At rank seven, five triangles in at most four such branches force
`TT`; this is the precise reason the likely saturated exception becomes an
ordinary positive split.

Likewise, the dispersed `Q` router should not be sent to a private-opening
test. Splitting `Q` destroys the only possibly hostile cycle and turns every
incidence branch into a positive all-triangle packet.

## 9. Limitations and stopping rules

1. **Fully shared only.** The proofs assume one cycle-cut incidence tree. If
   the shared-cut graph is disconnected, use the reduced cluster tree and cut
   actual bridges; none of the leaf-or-split dichotomies alone assigns Steiner
   connector territories.
2. **A shared-cut component is essential.** An abstract set of `r` triangles
   receives the `A_r` margin only when its retained incidence is connected.
   The components of `I-C` have this property; arbitrary color packets need not.
3. **No uniform singleton-triangle credit.** A sum of strict `T` packets is
   positive but may approach zero under arbitrary tree attachments. It closes
   a cost-free hub split but cannot pay a later opening.
4. **No reuse of split credit.** A hub split has no separate cost, but its
   packet margin may be used only once. In particular, the qualitative
   positivity proved here cannot pay an external tree territory.
5. **Opening and splitting are different.** Opening a private vertex creates
   one tree territory of surplus exactly `-1`. Splitting a cycle distributes
   proper path intervals among branch territories and creates no such cost.
6. **Ownership is part of every statement.** A common cut belongs to one
   retained packet. A split hub mark belongs to one interval. Independent
   local splits cannot be composed across a second hub without checking their
   common vertex.
7. **Lower-rank inputs are assumed.** The proof uses the shared triangular
   recurrence and the existing `P`, `TP`, `TT`, tricyclic, tetracyclic, and
   pentacyclic packet bounds. It is not an independent spectral proof of those
   estimates.
8. **No global heptacyclic claim.** Proper cluster partitions, pentagon-ended
   reduced paths, arbitrary bridge entries, and two-hub compatibility remain
   separate structural tasks.

## Conclusion

The shared triangular recurrence changes the rank-seven local picture. A
fully shared `T^6Q` cluster is settled by opening `Q` when it is an incidence
leaf and splitting `Q` when it is internal. A fully shared `T^5PP` cluster is
settled by opening both pentagons when both are leaves and splitting an internal
pentagon otherwise. Common-cut locks, saturated hubs, and dispersed triangle
branches are exact subcases of these two dichotomies.

The decisive rank-seven pigeonhole is that a pentagon hub has at most five
incidence branches. If the other pentagon is a hostile singleton branch, five
triangles occupy at most four remaining branches, forcing an `A_2`-or-larger
packet whose margin `>1` absorbs `delta<1`. This removes the saturated-hub
exception present in the rank-six `T^4PP` census. The remaining limitations are
global connector and reduced-tree problems, not fully shared incidence
exceptions.
