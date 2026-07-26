# Global synthesis for connected hexacyclic cacti

**Date:** 2026-07-26

## Status

This document assembles the current hexacyclic proof objects into one proof
candidate. The case split is exhaustive: the sharp DNN reduction leaves exactly
two cycle-multiset families; disconnected and fully shared shared-cut graphs are
both covered for each family; and every exception returned by the finite
incidence censuses has a separate induced-territory proof. Accordingly a theorem
is stated below.

The conclusion is conditional only on the lower-rank and spectral dependencies
listed in Section 9. Within those dependencies, no hexacyclic incidence or
connector-entry case remains open. Section 10 records the remaining
formalization and reproducibility gaps; none is presently a missing mathematical
case in the assembled argument.

All graphs are finite, simple, and undirected. For a graph `H`, write

```text
s+(H) = sum_{lambda_i>0} lambda_i^2,
s-(H) = sum_{lambda_i<0} lambda_i^2,
sigma(H) = s+(H)-|V(H)|.
```

Write `T=C3`, `P=C5`, and use a bar to separate shared-cut clusters, not
necessarily graph components.

## Theorem

**Theorem (connected hexacyclic cacti).** Let `G` be a connected cactus with
exactly six cyclic blocks and `n=|V(G)|`. Arbitrary bridge connectors and
arbitrary trees attached at arbitrary vertices are allowed. Then

```text
s+(G)>n,
```

or equivalently `sigma(G)>0`.

## 1. Territory infrastructure and accounting

Three operations are used throughout.

1. **Induced superadditivity.** If `V(G)=V1 dotcup ... dotcup Vk`, then
   `s+(G)>=sum_i s+(G[Vi])`, and therefore
   `sigma(G)>=sum_i sigma(G[Vi])`.
2. **Bridge territories.** Contract each shared-cut cluster to a marked node in
   the block-cut tree, retain the minimal tree spanning the marked nodes, and
   suppress only unmarked degree-two nodes. Pairwise disjoint connected
   subtrees covering the marked nodes expand, by cuts on actual bridges, to
   connected induced territories with exactly the assigned cyclic blocks.
   Unmarked Steiner branches, connector remnants, and every hanging tree are
   assigned wholly to one territory.
3. **Cycle intervals and openings.** Deleting an internal cycle node from its
   cycle-cut incidence tree gives branches attached at distinct marked vertices
   of the cycle. Assigning those marks to nonempty proper consecutive intervals
   partitions the cycle among induced path fragments and costs no separate
   surplus unit. Every marked vertex has one owner. By contrast, opening a cycle
   at a private vertex, together with all tree branches rooted there, creates a
   nonempty induced tree territory of surplus exactly `-1`.

These rules are the topology behind every symbolic packet sum below. In
particular, no argument duplicates a shared cut, relocates an attached tree, or
uses edge monotonicity.

The quantitative packet ledger needed by the proof is:

```text
sigma(T)>0,
sigma(P)>=-delta,                         delta=sqrt(5)-2<1/2,
sigma(Cq)>=-delta_q,                      delta_q=sec(pi/q)-1<1,
sigma(TT)>1,
sigma(TP)>1-delta,
sigma(TQ)>1-delta_q                       for hostile q=1 mod 4,
sigma(H)>=0                               for bicyclic and tricyclic cacti,
sigma(H)>0                                for tetracyclic and pentacyclic cacti,
sigma(TTT)>2                              for one triangular shared-cut cluster,
sigma(TTTT)>3                             for one four-triangle shared-cut cluster,
sigma(TTP)>2-delta                        when its two triangles share a cut,
sigma(TPP)>6-2sqrt(5)                     for one shared-cut cluster,
sigma(TTTP)>1                             when some two triangles share a cut.
```

All these estimates allow arbitrary attached trees; the mixed two-cycle bounds
allow arbitrary bridge connectors. Qualitative positivity is never charged
against a hostile pentagon or a tree opening.

## 2. Exact sharp-DNN frontier

Let the six cycle lengths be `l1,...,l6`, let `b` be the number of bridge
blocks, and put

```text
epsilon_l = 0                              if l is even,
epsilon_l = l tan^2(pi/(2l))               if l is odd.
```

Since `G` is hexacyclic, `|E(G)|=n+5` and

```text
b+sum_i li=n+5.
```

The sharp cactus DNN theorem gives

```text
s-(G)<=b+sum_i(li+epsilon_li)
      =n+5+sum_i epsilon_li.
```

Using `s+(G)+s-(G)=2n+10` yields

```text
sigma(G)>=5-sum_i epsilon_li.                         (2.1)
```

For odd lengths, `epsilon_l` is strictly decreasing, with

```text
epsilon_3=1,
epsilon_5=5-2sqrt(5),
3epsilon_5<2,
2epsilon_5>1,
epsilon_5+epsilon_7<1.
```

Let `t` be the number of triangles. If `t<=3`, then

```text
sum_i epsilon_li <= 3+3epsilon_5<5.
```

If `t=4`, the two other cycles contribute less than one unless both are
pentagons: an even cycle contributes zero, and any other odd pair is bounded by
`epsilon_5+epsilon_7<1`. The pair `P,P` does survive because
`4+2epsilon_5>5`. If `t>=5`, the multiset is `{3,3,3,3,3,q}` for some `q>=3`
and (2.1) is not strict.

Thus the complete DNN residual frontier is exactly

```text
TTTTTQ = {T,T,T,T,T,Q},  Q=Cq and q>=3,
TTTTPP = {T,T,T,T,P,P}.                              (2.2)
```

Every other cycle-length multiset already has `sigma(G)>0` by (2.1).

## 3. Exhaustive structural split

Join two cyclic blocks when they share a cut vertex. Its connected components
are the shared-cut clusters. For either residual family in (2.2), exactly one
of the following holds.

1. The shared-cut graph is disconnected, so its six cycle nodes form at least
   two clusters joined only through bridge structure.
2. The shared-cut graph is connected, so all six cycles form one cluster and
   have a bipartite cycle-cut incidence tree.

This dichotomy is literal and exhaustive. Sections 4 and 5 settle the first
alternative; Sections 6 and 7 settle the second.

## 4. Disconnected `TTTTTQ`

If `q=3`, every cyclic block is triangular, so the triangular block-graph
theorem gives `sigma(G)>0` directly. Assume `q!=3` and let `R` be the reduced
cluster tree. Since `R` has at least two leaves and at most one leaf cluster can
contain `Q`, choose a `Q`-free leaf cluster `A`. It consists of `r` triangles,
where `1<=r<=5`. Cut the first actual bridge from `A` toward the rest.

If `r<=4`, the triangular side has strict positive surplus. The complementary
side is respectively penta-, tetra-, tri-, or bicyclic as `r=1,2,3,4`; it has
positive surplus in the first two cases and nonnegative surplus in the last
two. Hence the total is strict positive.

The only margin-sensitive case is `r=5`. The five triangles form one shared-cut
cluster. Its cycle-cut incidence tree has a leaf triangle. Open one private
vertex of that triangle. The opened tree costs one, while the remaining four
triangles stay in one shared-cut cluster and have surplus `>3`. Therefore

```text
sigma(A)>3-1=2.                                      (4.1)
```

The remote `Q` territory is nonnegative unless `q=1 mod 4`; in the hostile
case it has surplus at least `-delta_q`, with `delta_q<1`. Thus

```text
sigma(G)>2-delta_q>1>0.
```

This argument includes packing-three five-triangle clusters: the four-triangle
input explicitly includes the central-triangle/three-petal incidence. The
opening is internal to `A`, so the external connector may enter anywhere.
Consequently every disconnected `TTTTTQ` cactus is settled.

## 5. Disconnected `TTTTPP`

### 5.1 Complete colored cluster partition audit

Up to permutations of the four triangles and two pentagons, there are exactly
28 proper colored set partitions of `(4,2)`. The recursion choosing a first
nonzero pair `(t,p)` and requiring the remaining pairs to be nondecreasing gives
29 partitions including the one-cluster partition, hence 28 proper partitions.

The packet ledger settles 23 proper partitions directly, independently of the
reduced-tree topology. The five topology-sensitive rows are

```text
T|T|T|T|P|P,
TTP|T|T|P,
TTTP|T|P,
TTTTP|P,
TTP|TTP.                                             (5.1)
```

They are all resolved as follows.

### 5.2 All singletons and `TTP|TTP`

For `T|T|T|T|P|P`, a triangular leaf gives a strict triangular territory plus
a positive pentacyclic remainder. If there is no triangular leaf, the two
pentagons are the only leaves, so the reduced tree is a path. In path order,
form territories

```text
TP + TT + TP,
```

whose total surplus is `>2(1-delta)+1>0`.

For `TTP|TTP`, if either cluster contains intersecting triangles, its
`>2-delta` bound plus nonnegativity of the other cluster settles the graph.
Otherwise each cluster is the distinct-cut chain `T-P-T`. Split each central
pentagon into two intervals, assigning the common bridge connector to the
interval containing its actual entry at each end. Join the selected intervals
through that connector. The exact induced territories are

```text
TT + T + T,
```

with total surplus `>1` plus two strict terms.

### 5.3 The row `TTP|T|T|P`

Intersecting triangles inside `TTP` give a direct positive total. Otherwise
the cluster is the chain `T-P-T`. Reduced-tree edge tests first settle every
topology admitting a `TP` versus tetracyclic split or a `TT` versus `TPP`
split. If neither singleton triangle is a leaf and neither edge test applies,
the reduced tree has only the `TTP` cluster and remote pentagon as leaves; it
is therefore their path, with the two singleton triangles internal.

Split the chain pentagon according to its actual connector entry. Join one
interval to one internal singleton triangle, leave the other interval as a
strict triangle, and join the remaining singleton triangle to the remote
pentagon. This gives

```text
TT + T + TP,
```

with positive total. Thus this row is complete for arbitrary connector entry.

### 5.4 E2: `TTTP|T|P` with two labelled entries

If the singleton `T-P` path avoids the `TTTP` cluster, it is a `TP` territory
and the cluster is a positive tetracyclic territory. Otherwise two labelled
connector arms enter the `TTTP` cluster.

There are exactly eight colored `TTTP` incidence trees by cut count:

```text
c=1,2,3: 1,3,4.
```

Seven have an intersecting triangle pair, so their cluster surplus is `>1` and
absorbs the remote pentagon deficit. The eighth is a pentagon with three
pairwise disjoint triangular petals. Project each labelled entry to one of the
five pentagon vertices; entries through a petal project to and travel with its
petal mark. Modulo pentagon dihedral symmetry there are exactly 26 ordered
entry orbits, including coincident entries and entries at petal cuts.

The exact interval census gives, in every orbit, a proper interval containing
the remote-pentagon entry and owning one or two of the four triangles after the
remote singleton triangle is assigned by its labelled entry. The resulting
certificates are

```text
20 orbits: TP + TTT,
 6 orbits: TTP + TT.
```

Their totals are respectively `>(1-delta)+0` and `>0+1`. The verifier asserts
both interval and complement are nonempty consecutive sets and that the
remote-pentagon root has one owner. Hence E2 is closed.

### 5.5 E1: `TTTTP|P` with an intersecting triangle pair

Let `P0` lie in the five-cycle cluster and `P1` be remote. Delete `P0` from the
cluster incidence tree. Every resulting component contains triangles, meets
`P0` at exactly one distinct cut, and is exactly one connected component of the
triangle shared-cut graph. Since some triangles intersect, the component-size
partition and marked entry-component size are exactly the following six rows:

```text
(4),       entry 4;
(3,1),     entry 3 or 1;
(2,2),     entry 2;
(2,1,1),   entry 2 or 1.                              (5.2)
```

For at least two components, split `P0` at one gap between each consecutive
pair of attachment marks. Give the whole external connector and `P1` to the
interval owning the entry component. Every cyclic order then gives one of

```text
TTTP+T,  TP+TTT,  TTP+TT,  TTP+T+T,  TP+TT+T,
```

all with positive packet sum. This construction covers entry through a private
triangle vertex, a triangle-triangle cut, a multiway attachment cut on `P0`, or
a branch rooted at any such point.

For the one-component row `(4)`, open private vertices of both pentagons away
from the connector route. Their two tree territories cost two. The four
triangles remain one shared-cut cluster with surplus `>3`, so

```text
sigma(G)>3-2=1.
```

Pairwise-disjoint four-petal incidences, excluded from E1, were already settled
by a `TP` plus nonnegative all-triangle interval split for every entry. Thus E1
is closed.

Combining Sections 5.1--5.5 settles all 28 proper colored partitions, every
reduced-tree topology needed by the five exceptional rows, and every retained
entry orbit. Therefore every disconnected `TTTTPP` cactus is settled.

## 6. Fully shared `TTTTTQ`

Let `I` be the bipartite incidence tree on the six cycle nodes and `c` shared
cut nodes. Then

```text
|E(I)|=c+5,
sum_x(deg_I(x)-1)=5,
1<=c<=5.                                             (6.1)
```

Every cut has degree at least two, triangle degree is at most three, and
`Q=Cq` has degree at most `q`. The capacity regimes `q=3`, `q=4`, and `q>=5`
are exhaustive because (6.1) permits at most five cut nodes.

The color-preserving census, fixing `Q` and quotienting by permutations of the
five triangles and cut nodes, gives:

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | total |
|---|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 6 | 20 | 27 | 14 | 68 |
| `q=4` | 1 | 6 | 20 | 28 | 15 | 70 |
| `q>=5` | 1 | 6 | 20 | 28 | 16 | 71 |

Keeping `Q` distinguished when `q=3` may overcount uncolored six-triangle
trees but cannot omit one.

Every non-bouquet tree has a safe ordinary one-cycle split: respectively
`67`, `69`, and `70` trees are resolved. The acceptance ledger is exhaustive
for the branch created by a split:

1. Splitting `Q` leaves nonempty all-triangle branches, each strict positive.
2. Splitting a triangle leaves one `Q`-branch. A `TQ` branch is positive; a
   generic `TTQ` branch is nonnegative and another triangle branch is strict;
   larger `T^kQ` branches are lower-rank positive.
3. If `Q` is singleton, the other four triangles occupy at most two branches,
   so one branch contains `TT` and its surplus `>1` absorbs the hostile loss
   `delta_q<1`.

The unique exception in every regime is the one-cut six-cycle bouquet. Open a
private vertex of `Q` and a private vertex of one designated triangle. Their
path remnants retain the common cut. The other four triangles remain one
shared-cut cluster of surplus `>3`, while the two rooted tree territories cost
two. Hence the bouquet has surplus `>1`. This also covers `Q=T` by arbitrary
designation. Therefore every fully shared `TTTTTQ` cactus is settled.

## 7. Fully shared `TTTTPP`

The same incidence identity (6.1), now with triangle capacities three and
pentagon capacities five, gives the exact color-preserving census:

| cut count `c` | incidence trees | SAFE ordinary split | exceptions |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 1 |
| 2 | 9 | 9 | 0 |
| 3 | 40 | 40 | 0 |
| 4 | 62 | 62 | 0 |
| 5 | 38 | 37 | 1 |
| **total** | **150** | **148** | **2** |

For all `900` cycle choices, the executable deletes the candidate cycle,
computes the retained incidence components, and applies only the packet bounds
whose hypotheses hold inside those components. It checks, rather than infers
from colors, a shared triangle cut in `TTP`, an intersecting triangle pair in
`TTTP`, and connected shared-cut hypotheses for `TTT`, `TTTT`, `TPP`, and
`PP`. Generic tri-, tetra-, and pentacyclic bounds are not used to cancel a
negative singleton pentagon. Thus each of the 148 accepted trees has an actual
positive branch sum after a legal interval split.

The two exceptions are exact.

1. **Six-cycle bouquet.** Open private vertices on both pentagons. Their path
   remnants retain the common cut, the four triangles remain one shared-cut
   bouquet, and `sigma(G)>3-2=1`.
2. **Saturated pentagon hub.** One pentagon uses all five vertices at distinct
   degree-two cuts, with four triangular petals and the other pentagon as the
   fifth petal. It has no private opening vertex. In cyclic order, merge the
   pentagonal petal mark with either adjacent triangular mark and give the
   other three triangle marks separate proper intervals. This produces

   ```text
   TP + T + T + T,
   ```

   with total surplus `>1-delta>0`. Both neighbors of the unique pentagonal
   mark are triangular, so no cyclic-order subcase is omitted.

No double hub or hybrid remains outside the SAFE set. Therefore every fully
shared `TTTTPP` cactus is settled.

## 8. Completion of the proof

Let `G` be any connected hexacyclic cactus.

- If its cycle multiset is not one of the two families in (2.2), the strict DNN
  bound (2.1) proves `sigma(G)>0`.
- If its multiset is `TTTTTQ`, disconnected shared-cut graph is covered by
  Section 4 and connected shared-cut graph by Section 6.
- If its multiset is `TTTTPP`, disconnected shared-cut graph is covered by
  Section 5 and connected shared-cut graph by Section 7.

These alternatives exhaust all cycle lengths and all shared-cut incidences.
The bridge-territory and cycle-interval constructions include arbitrary
connectors, Steiner branches, coincident connector roots where permitted, and
arbitrary attached trees. Every use of superadditivity is on an explicit
vertex partition into induced subgraphs. This proves the theorem.

## 9. Dependency ledger

### 9.1 External mathematical dependencies in the repository

The proof candidate depends on the following results, not reproved globally in
this synthesis.

1. **Induced-subgraph superadditivity for `s+`.** Stated in
   `all-pentacyclic-cacti/paper.tex` and attributed there to Akbari, Kumar,
   Mohar, and Pragada.
2. **Sharp cactus DNN theorem.** The block-additive formula for `kappa(G)` and
   `s-(G)<=kappa(G)` is proved in `sharp-cactus-dnn/paper.tex`.
3. **Unicyclic and mixed bicyclic packet bounds.** The `T`, hostile `Q`, `TT`,
   `TP`, and `TQ` bounds are supplied by `all-bicyclic-cacti/paper.tex`,
   `all-tricyclic-cacti/paper.tex`, and their cited one-cycle inputs.
4. **All bicyclic and tricyclic cacti.** Nonnegative surplus is proved in
   `all-bicyclic-cacti/paper.tex` and `all-tricyclic-cacti/paper.tex`.
5. **All tetracyclic cacti.** Strict positive surplus is proved in
   `all-tetracyclic-cacti/paper.tex`.
6. **All pentacyclic cacti.** Strict positive surplus, including arbitrary
   connector and interval territory infrastructure, is proved in
   `all-pentacyclic-cacti/paper.tex`.
7. **Packing-two phase theorem and triangular block graphs.** The phase bound
   `sigma>r-1` at packing number at most two and strict positivity for every
   connected triangular block graph are in
   `packing-two-square-energy/paper.tex`.
8. **Concentrated triangle margins.** The shared `TTT` margin `>2` and shared
   `TTTT` margin `>3`, including the packing-three central-triangle case, are
   recorded and sourced in `all-pentacyclic-cacti/paper.tex`; the latter's
   direct matching injection is reproduced in
   `research/five-triangle-shared-cluster-surplus-2026-07-26.md`.
9. **Other concentrated packets.** Shared `TTP`, `TPP`, and `TTTP` margins used
   by the SAFE ledgers are consequences of the lower-rank manuscripts and the
   explicit opening argument in `all-pentacyclic-cacti/paper.tex`.

### 9.2 Hexacyclic proof objects integrated here

1. `research/hexacyclic-dnn-residuals-2026-07-26.md`: exact residual
   inequality, symbolic threshold comparisons, and residual classification.
2. `research/hexacyclic-tttttq-disconnected-2026-07-26.md`: reduced-tree proof
   for disconnected `TTTTTQ`.
3. `research/five-triangle-shared-cluster-surplus-2026-07-26.md`: the new
   uniform `sigma(TTTTT)>2` margin, including packing three.
4. `research/hexacyclic-ttttpp-disconnected-audit-2026-07-26.md`: all 28
   proper colored partitions, direct rows, and exact E1/E2 boundary.
5. `research/hexacyclic-ttttpp-e1-resolution-2026-07-26.md`: six-row
   component-and-entry classification and E1 closure.
6. `research/hexacyclic-e2-tttp-two-entry-resolution-2026-07-26.md`: eight
   `TTTP` incidences, 26 ordered hub-entry orbits, and E2 closure.
7. `research/hexacyclic-e2-tttp-entry-census.py`: executable E2 proof object.
8. `research/hexacyclic-tttttq-incidence-census.py` and
   `research/hexacyclic-tttttq-incidence-census-2026-07-26.md`: fully shared
   `TTTTTQ` enumeration, SAFE split ledger, and bouquet exception.
9. `research/hexacyclic-ttttpp-incidence-census.py` and
   `research/hexacyclic-ttttpp-census-2026-07-26.md`: fully shared `TTTTPP`
   enumeration, retained-incidence SAFE ledger, and two exceptions.
10. `research/hexacyclic-common-cut-sacrifice-2026-07-26.md`: exact private
    opening, common-cut ownership, and four-triangle sacrifice lemma.
11. `research/hexacyclic-fully-shared-verdict-2026-07-26.md`: independent
    replay and acceptance-ledger audit of both full shared-cut censuses.
12. `research/hexacyclic-packet-ledger-2026-07-26.md`: strictness and opening
    cost ledger used to prevent unsupported margin transfers.
13. `research/five-triangle-shared-cluster-surplus-audit-2026-07-26.md`:
    adversarial check of incidence leaves, multiway cuts, packing three, tree
    attachments, and the strict `>2` budget.
14. `research/hexacyclic-e1-e2-resolution-adversarial-audit-2026-07-26.md`:
    independent enumeration of 25 E1 incidences and all 250 raw E2 hub-entry
    placements, before quotienting the latter to 26 dihedral orbits.
15. `research/hexacyclic-fully-shared-verdict-2026-07-26.md`,
    `research/hexacyclic-cactus-complete-hostile-audit-2026-07-26.md`, and
    `research/hexacyclic-independent-reconstruction-2026-07-26.md`: successive
    independent audits of the full shared censuses, cumulative hostile
    completeness, and the complete theorem proof tree.

The earlier `research/hexacyclic-structural-plan-2026-07-26.md` and
`research/hexacyclic-naive-obstructions-2026-07-26.md` are planning and
adversarial-audit documents. Their proposed gaps H1--H11 are superseded by the
disconnected resolutions, the two exact fully shared censuses, and the explicit
bouquet/hub repairs assembled here. They are not independent proof inputs.

## 10. Gap and risk ledger

### 10.1 Mathematical case gaps

**None currently identified.** More specifically:

- the DNN frontier has no unclassified cycle multiset;
- disconnected `TTTTTQ` has no remaining cluster partition, including the
  formerly marginal `TTTTT|Q` row;
- disconnected `TTTTPP` has no remaining colored partition or entry family:
  E1 and E2 are both resolved;
- fully shared `TTTTTQ` has only the bouquet outside the ordinary split census,
  and it is resolved;
- fully shared `TTTTPP` has only the bouquet and saturated pentagon hub outside
  the SAFE census, and both are resolved.

### 10.2 Formalization and verification gaps

These do not presently expose an omitted mathematical family, but they should
be closed before treating this synthesis as a publication-ready proof.

1. **Computer-assisted census reliance.** The two fully shared classifications
   and the E2 entry classification rely on Python enumerators with internal
   assertions. The fully shared counts have an independent audit recorded in
   the verdict note. All 250 unquotiented E2 hub placements were also checked
   independently, but there is no proof-assistant certificate or committed
   second E2 implementation.
2. **E1 has no committed verifier.** Its six rows follow from a short
   incidence-tree invariant, and the adversarial audit independently enumerates
   all 25 internal incidences and reproduces the six marked-component rows, but
   that independent checker is not retained as a repository script.
3. **The 28-row disconnected partition audit has no dedicated verifier.** The
   count and row set were independently regenerated in both the hostile audit
   and independent reconstruction, but there is no committed script asserting
   all 28 rows together with their assigned certificates.
4. **The global theorem is not integrated into a TeX manuscript.** The argument
   is distributed across Markdown notes and lower-rank papers. Definitions,
   numbering, and cross-references should be consolidated before submission.
5. **Dependency status is manuscript-local.** Several lower-rank results are
   repository manuscripts rather than imported, formally published theorems.
   The hexacyclic theorem inherits any error in those dependencies.
6. **Scripts certify abstract incidence, not graph spectra.** This is intended:
   spectral positivity comes from proved packet theorems. The bridge-territory
   and interval realization lemmas must remain adjacent to the census results
   in any final manuscript so abstract branch tuples are not mistaken for
   vertex partitions by themselves.

### 10.3 Reproduction

From the repository root, run:

```bash
python research/hexacyclic-e2-tttp-entry-census.py
python research/hexacyclic-tttttq-incidence-census.py
python research/hexacyclic-ttttpp-incidence-census.py
```

The asserted outputs are:

```text
E2 TTTP incidences by c:             1, 3, 4
E2 hub ordered-entry orbits:         26 = 20 TP+TTT + 6 TTP+TT

TTTTTQ totals:
q=3:                                 1, 6, 20, 27, 14 = 68
q=4:                                 1, 6, 20, 28, 15 = 70
q>=5:                                1, 6, 20, 28, 16 = 71
ordinary-split exceptions:           one bouquet in each regime

TTTTPP totals:                       1, 9, 40, 62, 38 = 150
SAFE ordinary-split resolutions:     0, 9, 40, 62, 37 = 148
ordinary-split exceptions:           bouquet, saturated pentagon hub
all recorded cycle choices:          900
```

The three scripts were rerun successfully while preparing this synthesis.
