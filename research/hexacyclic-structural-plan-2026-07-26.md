# Structural proof plan for connected hexacyclic cacti

## Status and target

This is a proof-development plan, not a theorem or a claim that the hexacyclic
case is complete. The intended target is to prove positive surplus

`sigma(G)=s+(G)-|V(G)|>0`

for every connected cactus with six cyclic blocks. The new permitted black box
is the verified pentacyclic theorem:

`sigma(H)>0` for every connected pentacyclic cactus `H`, with arbitrary bridge
connectors and arbitrary attached trees.

The central issue is quantitative. A pentacyclic remainder has strict positive
surplus, but no known uniform positive margin. It therefore combines safely
with a separated triangle, but not with a tree territory of surplus `-1` or an
isolated hostile odd cycle of negative surplus. Every reduction below is
organized to avoid silently spending more margin than the proved ledger gives.

Write `T=C3`, `P=C5`, and, for odd `q`,

`epsilon_q=q tan^2(pi/(2q))`.

Thus `epsilon_3=1`, `epsilon_5=5-2sqrt(5)=0.527864...`, the odd sequence is
strictly decreasing, and even cycles have epsilon zero. For a hostile
`q=1 mod 4` cycle it is also convenient to write

`delta_q=sec(pi/q)-1<1`,

so a unicyclic `Cq` territory has surplus at least `-delta_q`.

## 1. Independent DNN residual derivation

For a connected hexacyclic cactus with cycle lengths `l1,...,l6`, block
counting gives

`b+sum_i li=n+5`.

The exact cactus DNN estimate and
`s+(G)+s-(G)=2|E(G)|=2(n+5)` give

`sigma(G)>=5-sum_i epsilon_li`.                                    (1)

Only odd cycles contribute. Since every nontriangle odd cycle contributes at
most `epsilon_5`, the number `t` of triangles gives

`sum_i epsilon_li <= t+(6-t)epsilon_5`.

Consequently:

- `t<=3` is strictly safe, because `3+3epsilon_5<5`;
- `t=4` can be hostile only if both remaining cycles are odd and their epsilon
  sum is at least one;
- `t>=5` is not decided uniformly by (1).

For `t=4`, monotonicity and
`epsilon_5+epsilon_7<1` show that the threshold can be reached only by two
pentagons. If either cycle is even, or one odd cycle has length at least seven,
the total epsilon is strictly below five. Thus the exact structural residuals
left by (1) are

`TTTTTQ = {T,T,T,T,T,Q}`, with arbitrary `Q=Cq`, `q>=3`,            (R1)

`TTTTPP = {T,T,T,T,P,P}`.                                         (R2)

The value `Q=T` in (R1) is the all-six-triangle case. The two families are
disjoint: (R1) has at least five triangles, while (R2) has exactly four.

This is the complete DNN frontier. In particular, no family with exactly four
triangles other than `TTTTPP` survives.

## 2. Structural language and safe induced territories

Use exactly the shared-cut graph and reduced cluster tree from the
pentacyclic proof. Its marked nodes are shared-cut clusters, including
singletons. Pairwise disjoint connected subtrees covering the marked nodes can
be expanded into vertex-disjoint connected induced territories by cutting
actual bridge edges. A Steiner branch is assigned to one territory, and every
hanging tree is assigned wholly by its unique attachment to the cyclic hull.

Two further principles must remain explicit.

**Intersection-component constraint.** Retained cycles in one connected
component of the shared-cut graph must lie in one territory. A common cut
vertex cannot be allocated to two induced parts. Thus a proposal to make a
triangle into a separate territory is valid only when that triangle is a
singleton shared-cut cluster or when an incident cycle is opened to release
the common cut.

**Cycle-interval split.** If an internal cycle node is deleted from a
cycle-cut incidence tree, its branches may be assigned nonempty consecutive
intervals of the cycle, one or more adjacent branch marks per interval. Every
interval is a proper path, so the split cycle disappears. This is the basic
operation for converting a fully shared six-cycle incidence into lower-cyclic
packets.

The accounting primitives currently available are:

- `sigma(T)>0`, `sigma(P)>=-delta`, and `sigma(Cq)>=-delta_q` for hostile
  `q=1 mod 4`;
- `sigma(TT)>1`, `sigma(TQ)>1-delta_q`, and `sigma(TP)>1-delta`;
- every bicyclic or tricyclic cactus has nonnegative surplus;
- favorable all-`3 mod 4` packets of packing number at most two have
  `sigma>r-1`;
- every tetracyclic cactus has positive surplus;
- every pentacyclic cactus has positive surplus;
- the quantitative tetracyclic margins recorded in
  `research/tetracyclic-surplus-incidence-ledger-2026-07-26.md`.

The last ledger is essential whenever a construction opens one cycle and pays
a tree cost of one. Merely invoking the tetracyclic or pentacyclic theorem does
not pay that cost.

## 3. First use of the pentacyclic theorem: a triangle-leaf reduction

The cleanest new decomposition is the following.

**Proposed Lemma H1 (bridge-leaf triangle).** If a singleton triangular
shared-cut cluster is a leaf of the minimal reduced cluster tree spanning the
six cyclic clusters, cut the first actual bridge toward the rest. The leaf
territory is a triangular unicyclic cactus and the remainder is a connected
pentacyclic cactus. Hence

`sigma(G)>=sigma(T-territory)+sigma(pentacyclic remainder)>0`.

This lemma is already justified by the proved packet theorems and the arbitrary
connector-territory lemma; what remains is careful formulation. It immediately
settles every disconnected cluster partition whose reduced tree has a
singleton triangle leaf.

It is not enough to say that a proper cluster partition contains a triangle.
The triangle cluster can be internal in the reduced tree, and a triangle inside
a larger shared-cut cluster cannot be detached without opening another cycle.
The hostile disconnected analysis therefore has to classify the configurations
in which H1 is unavailable.

## 4. Disconnected shared-cut graph: reduction rather than a 31-row table

For six cycles, listing all colored set partitions is possible but not the
right first invariant. The reduced-tree leaf types expose the actual
obstruction.

### 4.1 The `TTTTTQ` family

If H1 does not apply, every reduced-tree leaf cluster is either:

1. the singleton `Q` cluster;
2. a nontrivial cluster containing one or more triangles; or
3. when `Q=T`, a triangle hidden by the designation but not necessarily a
   singleton triangle cluster.

There is only one possibly nontriangular cycle. Therefore, if all six cycles
are singleton clusters, a finite reduced tree necessarily has a triangular
leaf and H1 applies. Every obstruction in this residual family must hide a
triangle in a nontrivial shared-cut leaf cluster (or put all six cycles in one
cluster). The following decompositions should be proved as structural lemmas.

**Proposed Lemma H2 (nontrivial triangular leaf release).** Suppose a leaf
cluster contains at least one triangle. Audit the unique external connector
entry into that cluster. One can choose a bridge cut or split an internal entry
cycle so as to produce either:

- a pentacyclic territory plus a strict triangular territory; or
- one mixed `TQ` territory plus an all-triangle packet; or
- one `TTQ`/`TTTQ` territory with a certified margin and lower-cyclic
  nonnegative territories.

The statement must be split by whether the connector enters through a private
cycle vertex, a shared cut, or an attached triangle. The proof template is the
entry-sensitive `TTTP|P` repair from the pentacyclic argument, now with five
triangles available across the two sides.

**Proposed Lemma H3 (hostile singleton against a triangular cluster).** If one
leaf is the singleton `Q` and another leaf is a nontrivial all-triangle or mixed
cluster, then either the latter has enough certified margin to absorb the
hostile singleton, or an internal cycle can be split to release a strict
triangle and leave a pentacyclic territory. Required packet instances include
`TTTTQ`, `TTTQ`, `TTQ`, and all-triangle shared clusters.

For nonhostile `Q` parities the ledger simplifies: even-cycle singleton
territories have zero surplus, while `3 mod 4` packets are favorable. A final
proof should separate this easy parity layer before analyzing the one hostile
`1 mod 4` cycle.

### 4.2 The `TTTTPP` family

Again H1 handles every singleton triangle leaf. If no such leaf exists, all
reduced-tree leaves are pentagons or nontrivial clusters. The two-pentagon
path obstruction from the pentacyclic proof reappears with one extra triangle,
but the proved pentacyclic theorem creates a useful option: release one strict
triangle and keep all five other cycles connected.

The target decomposition hierarchy is:

1. `T + (pentacyclic)` whenever a triangle can be released across an actual
   bridge or by splitting an entry cycle;
2. `TP + TTT` or `TP + TT + T`, with positive packet total;
3. `TP + TP + TT`, with lower surplus `>2(1-delta)+1`;
4. a four-cycle packet with a margin greater than one plus a tree opening;
5. a fully shared local lemma when common cuts prevent all of the preceding
   separations.

**Proposed Lemma H4 (pentagon-ended reduced tree).** If every reduced-tree leaf
is a singleton pentagon, then the reduced tree has exactly those two leaves and
is a path. Along that path, either a bridge cut releases a triangle and leaves
a connected pentacyclic territory, or two path cuts give `TP`, a middle
all-triangle packet, and `TP`. The latter has positive total even if the middle
packet is only nonnegative. The proof must allow nontrivial triangle-containing
clusters at internal marked nodes; if a common cut blocks the path packets, H4
must invoke an entry-cycle interval split rather than assign the cut twice.

**Proposed Lemma H5 (mixed nontrivial leaf absorption).** A leaf cluster of
type `TT...` or `TP...` either contributes a certified margin against a remote
pentagon or admits a split producing `T + pentacyclic`. This is where the exact
pentacyclic `TTTTQ` and `TTTPP` proofs should be mined for entry-sensitive
versions, not merely their qualitative final theorem.

An exact colored set-partition census should still be run after H1--H5 are
formalized. Its purpose is to certify that the leaf/path alternatives cover
every proper partition, not to substitute raw packet addition for topology.

## 5. Fully shared incidence: general census framework

For one shared-cut cluster, let `I` be the bipartite incidence tree on six cycle
nodes and the cut vertices belonging to at least two cycles. If there are `c`
cut nodes, then

`|E(I)|=c+5`, and `sum_x(deg_I(x)-1)=5`.                       (2)

Hence `1<=c<=5`. Cycle degrees are bounded by cycle lengths. Modulo equal-cycle
permutations and cut permutations, the fully shared cases are finite for each
colored residual family.

The first computational proof object should enumerate every admissible colored
incidence tree and, for each cycle node `C`, record the colored branch multisets
after deleting `C`. Unlike the pentacyclic census, the acceptance test should
have three levels:

1. direct positive packet sum for the branch multisets;
2. one branch certified by the pentacyclic theorem and another by a strict
   triangle packet;
3. a two-stage split: split `C`, then apply an entry-sensitive split inside one
   branch.

The script must output canonical unresolved edge sets, not just counts. Each
unresolved tree then receives a named structural lemma and a hand-checkable
territory construction.

## 6. Fully shared `TTTTTQ`: predicted hard bouquets and hubs

Several configurations are already forced as hard before running a census.

### 6.1 Universal six-cycle bouquet

All six cycles share one cut vertex `x`. Every retained cycle contains `x`, so
all retained cycles belong to one territory. No decomposition into several
retained `T`, `TT`, or `TQ` packets is possible. This is the minimal common-cut
obstruction.

Open `Q` and one designated triangle at private vertices. This costs two tree
units and leaves a connected four-triangle bouquet. The known all-triangle
shared packet has surplus greater than three, so this route would yield
`>3-2>0`. It also covers `Q=T` after arbitrary re-designation. The exact lemma
is:

**Proposed Lemma H6 (two-cycle sacrifice at a common cut).** In a six-cycle
bouquet containing at least five triangles, opening a private vertex on `Q` and
on one triangle leaves a connected four-triangle packet of surplus `>3`; the
two tree territories cost exactly two.

The proof must specify attached branches at the chosen private vertices and
verify that each opened cycle minus that vertex still contains `x`.

### 6.2 `Q` hub with five triangular petals

The cycle `Q` meets the five triangles at five distinct degree-two cuts. This
saturates (2). A raw split of `Q` leaves branch type

`T + T + T + T + T`.

If the five marks fit on `Q`, split the hub into five proper consecutive
intervals, one per triangle mark. The territories are five triangular
unicyclic cacti and their total surplus is strict positive. This predicts:

**Proposed Lemma H7 (five-triangle hub split).** A hub cycle with five
triangular petals at distinct cuts admits a consecutive-interval partition
into five triangular territories.

The degree constraint is important: a triangular hub cannot carry five
distinct marks, so short hub lengths force multiway cuts and fall into bouquet
or hybrid cases.

### 6.3 Four-triangle hub with a `TQ` tail

A cycle or multiway cut supports four triangles, while the fifth triangle and
`Q` lie on a tail through one internal triangle or through `Q`. These are
analogues of the pentacyclic `(4,2)` and `(3,2,2)` exceptions. A single cycle
split may leave a hostile singleton plus a cluster whose qualitative surplus
is positive but not uniformly large enough.

**Proposed Lemma H8 (four-triangle core plus `TQ` tail).** If opening the tail
triangle and `Q` leaves one connected shared-cut four-triangle cluster, then
the cluster margin `>3` pays the two tree costs. More generally, split the
intervening internal cycle to obtain either `TQ + T + T + T` or
`TT + TQ + T`.

### 6.4 Double hub

Two internal cycles joined through a cut or through one intermediate cycle may
divide the five triangles between them, with `Q` attached on one side. Neither
internal cycle alone need have a positive raw branch partition;
the obstruction is simultaneous entry ownership at the joining cut.

**Proposed Lemma H9 (double-hub interval compatibility).** For two adjacent
internal cycle nodes, there are compatible interval splits assigning their
common cut to one side only and producing one of

`TQ + TT + T + T`, `TTQ + TT + T`, or `pentacyclic + T`.

This needs a finite cyclic-order check with coincident entries and short cycles.
It is a likely source of genuine census exceptions.

## 7. Fully shared `TTTTPP`: predicted hard bouquets and hubs

### 7.1 Six-cycle bouquet

Four triangles and two pentagons share one cut. Opening a private vertex on
each pentagon leaves the connected four-triangle bouquet. Its surplus `>3`
pays the two tree costs. This extends the pentacyclic `TTTPP` bouquet repair
and should be isolated as a lemma rather
than hidden in a census.

### 7.2 Pentagon hub with five petals

One pentagon meets four triangles and the other pentagon at its five distinct
vertices. Splitting the hub into four intervals, merging the other pentagon
with an adjacent triangle, gives

`TP + T + T + T`,

whose surplus is `>1-delta>0`. This is a separate saturated-hub lemma, denoted
H7P below; it is expected to be the unique five-cut hub type up to color.

**Proposed Lemma H7P (pentagon five-mark hub).** A pentagon hub with four
triangular petals and one pentagonal petal admits a consecutive-interval split
of type `TP+T+T+T`.

### 7.3 Triangle hub with multiway cuts

A triangle can have at most three distinct incidence vertices, so degree four,
five, or six behavior must use multiway cuts. Typical hard types are:

- one cut carrying the triangle hub, several other triangles, and one or both
  pentagons;
- cut-degree sequences `(5,2)`, `(4,3)`, `(4,2,2)`, and `(3,3,2)` whose excess
  totals five;
- two pentagons as leaf cycle nodes with the four triangles remaining one
  shared cluster after both are opened.

The last condition is favorable: a connected four-triangle cluster has the
required `>3` margin. The danger is a hybrid in which opening the two pentagons
disconnects the triangles into packets whose known margins total only two.
That hybrid must be found explicitly by the census.

**Proposed Lemma H10 (two-pentagon sacrifice criterion).** If both pentagons
are leaf cycle nodes and deleting private vertices from them leaves a connected
four-triangle shared-cut cluster, then the total surplus is positive. If the
four triangles split into several shared clusters, the lemma must instead give
an exact cluster-margin criterion; two disjoint `TT` clusters provide `>2`,
which does not by itself strictly pay two tree costs unless both inequalities
are strict enough in aggregate. They are (`>1+>1`), but every other partition
must be checked separately.

### 7.4 Pentagon--pentagon double hub

Each pentagon may be internal, with two triangles attached on each side and a
shared route between the pentagons. A naive split can produce `TT+TT` and lose
both pentagons, which gives only `>2` against two opening costs and is actually
sufficient if the strict packet bounds are retained. However, ownership of the
pentagon--pentagon entry cut can prevent those two `TT` territories from being
induced simultaneously.

**Proposed Lemma H11 (pentagon double hub).** Two adjacent internal pentagons
supporting four triangular branches admit compatible consecutive-interval
splits yielding either two `TT` territories with two tree/path territories, or
`TP+TP+TT`. The lemma must state which side owns the common cut and cover
coincident attachment roots.

## 8. Exact lemmas needed before a theorem proof can be written

The following list separates already available infrastructure from genuinely
new work.

### 8.1 Infrastructure to restate, not reprove

1. Induced-subgraph superadditivity for `s+`.
2. Arbitrary connector territories on the reduced cluster tree, including
   Steiner branches and arbitrary attached trees.
3. Consecutive-interval splitting of a cycle node.
4. The exact hexacyclic DNN reduction (1) and residual classification (R1)--(R2).
5. The verified qualitative pentacyclic theorem.
6. Existing quantitative packet bounds through four cycles, including the
   tetracyclic incidence ledger.

### 8.2 New structural lemmas

1. H1: singleton bridge-leaf triangle plus connected pentacyclic remainder.
2. H2--H5: reduced-tree entry lemmas for the no-triangle-leaf disconnected
   residuals, with explicit ownership of shared cuts and connector entries.
3. H6: two-cycle sacrifice leaving a four-triangle cluster, including bouquets
   and leaf-cycle variants.
4. H7 and H7P: saturated five-triangle and pentagon-hub interval splits.
5. H8: four-triangle core with a `TQ` tail.
6. H9 and H11: compatible two-cycle splits for double hubs.
7. H10: exact accounting when two pentagons are opened and the four triangles
   remain connected or split into several shared-cut clusters.

### 8.3 New quantitative lemmas likely required by census output

1. **Four-triangle cluster margin.** A clean reusable statement that every
   connected one-cluster four-triangle cactus has `sigma>3`, with the
   packing-three central-triangle case included.
2. **Split four-triangle ledger.** Classify exactly which shared-cut partitions
   of four triangles left after opening two cycles have total certified margin
   greater than two. The partitions `TTTT`, `TTT|T`, and `TT|TT` do; partitions
   containing at most one intersecting pair generally do not. This prevents an
   invalid appeal to qualitative triangular strictness.
3. **Entry-sensitive pentacyclic release.** Conditions under which splitting
   one cycle in a six-cycle cluster yields a strict triangular territory plus
   a connected pentacyclic territory. The qualitative pentacyclic theorem then
   closes the split with no uniform-margin demand.
4. **One-tree-cost pentacyclic subclasses, if unavoidable.** If a census
   exception only opens one cycle and leaves a pentacyclic remainder, a new
   quantitative bound `sigma(remainder)>1` for that exact incidence is needed.
   The global pentacyclic theorem alone is insufficient. The first candidates
   should be extracted from the existing `TTTTQ` and `TTTPP` proofs by tracking
   their displayed packet margins.
5. **Short-hub cyclic-order lemma.** Multiway cuts on a triangle or pentagon
   must be handled when distinct incidence marks cannot all be placed at
   distinct vertices. The statement must distinguish distinct marks from
   several cycle branches sharing one cut node.

## 9. Required exact censuses

Two independent scripts should be produced.

### 9.1 Fully shared colored incidence census

For `TTTTTQ` (with `Q` specialized by parity/length role as needed)
and `TTTTPP`, enumerate bipartite trees satisfying (2), minimum cut degree two,
cycle degree caps, and color-preserving isomorphism. For every cycle node,
record:

- branch color multisets after deletion;
- whether a positive one-cycle packet partition exists;
- whether one branch is a single triangle and the complement is pentacyclic;
- whether `Q` and one triangle can be opened while four triangles retain the
  required shared-cluster structure;
- whether the tree is a bouquet, saturated hub, core-with-two-leaves, or double
  hub.

The output must include canonical unresolved edge sets and witness splits for
resolved trees. Counts alone are not a proof certificate.

### 9.2 Disconnected cluster-partition and reduced-tree census

Enumerate proper colored set partitions of each residual multiset, then attach
abstract reduced-tree topologies on the parts. Test H1 first, followed by
two-leaf path decompositions and H2--H5. This second stage is necessary because
the same set partition can be easy or hard depending on whether the path
between two singleton cycles avoids or passes through a nontrivial cluster.

The census may quotient equal cycles, but it must retain the labels “hostile
`1 mod 4`”, “even”, and “favorable `3 mod 4`” for `Q`; packet positivity
depends on these roles.

## 10. Proof workflow and stopping rules

1. Formalize (1), verify the numerical threshold, and freeze (R1)--(R2).
2. State H1 and the connector/interval infrastructure in manuscript-ready
   form.
3. Build the fully shared censuses and classify the unresolved trees into the
   named bouquet/hub families.
4. Prove H6, H7, and H10 first; they are structurally forced and reuse known
   four-triangle margins.
5. Build the disconnected reduced-tree census and prove H2--H5 only for the
   surviving topologies.
6. Address double hubs H9/H11 with explicit cyclic-order tables.
7. If an exception requires a tree cost against a pentacyclic remainder, stop
   and prove the exact quantitative pentacyclic subclass lemma; do not replace
   it by the qualitative theorem.
8. Re-run both censuses with assertions that the unresolved set is empty and
   independently audit every generated territory for connectedness,
   inducedness, cycle multiset, and surplus strictness.

## 11. Main logical hazards

- A pentacyclic theorem with `sigma>0` cannot absorb `sigma=-1` from an opened
  cycle and cannot offset a hostile singleton cycle.
- A triangle present in a cluster partition is not automatically separable;
  shared-cut components are indivisible unless another cycle is split.
- A reduced cluster tree is not generally a path. Path language is valid only
  after proving there are exactly two leaves.
- Two compatible interval splits must assign their common cut to exactly one
  territory. Independent local splits can overlap at that vertex.
- A strict triangle surplus has no known uniform positive lower bound under
  arbitrary tree attachments; it supplies strictness, not a fixed budget.
- Multiway cuts consume incidence excess but use only one vertex on a hub
  cycle. A census based solely on ordinary degree-two cuts would miss the most
  hostile bouquets.
- Cycle designation is bookkeeping: in `TTTTTQ`, `Q` may itself be a triangle.
  Arguments must be invariant under re-designation in the six-triangle case.

## 12. Deliverable criterion

A future theorem proof is ready only when all of the following exist:

1. a checked exact residual derivation;
2. complete disconnected reduced-tree certificates;
3. complete fully shared colored incidence certificates;
4. hand proofs for every canonical bouquet/hub exception;
5. explicit quantitative bounds for every paid tree cost;
6. an induced-territory audit covering connector entries, shared-cut ownership,
   hanging trees, coincident roots, short cycles, and multiway cuts.

At present this document identifies a finite structural program and the likely
hard configurations. It deliberately makes no hexacyclic theorem claim.
