# Toward heptacyclic cacti by structural induction

## Status and objective

This is a proof-development note, not a theorem and not a claim that the
heptacyclic case is complete. The new black box is the verified hexacyclic
theorem:

`sigma(H)=s+(H)-|V(H)|>0`

for every connected hexacyclic cactus `H`, with arbitrary bridge connectors
and arbitrary attached trees. The aim is to turn that qualitative rank-six
input into a rank-seven induction driven by leaves of the reduced cluster tree
and the cycle-cut incidence tree, avoiding a brute-force census of all
seven-cycle incidences if possible.

The central accounting warning remains unchanged: strict hexacyclic positivity
has no known uniform margin. It may be added to a strict positive leaf packet,
but it cannot pay a tree opening of surplus `-1` or a hostile odd-cycle deficit.
Any induction that destroys a cycle must therefore expose a quantitative core.

Write `T=C3`, `P=C5`,

`epsilon_l=0` for even `l`, and `epsilon_l=l tan^2(pi/(2l))` for odd `l`,

and, when `q=1 mod 4`, write `delta_q=sec(pi/q)-1<1`. Put

`a=epsilon_5=5-2sqrt(5)=0.527864...`.

## 1. The DNN frontier is already narrow

For a connected heptacyclic cactus with cycle lengths `l1,...,l7`, block
counting and the sharp cactus DNN estimate give

`sigma(G)>=6-sum_i epsilon_li`.                                  (1)

Since the odd `epsilon` sequence decreases and every nontriangle odd cycle
contributes at most `a`, the number `t` of triangles gives

`sum_i epsilon_li <= t+(7-t)a`.

Consequently:

- `t<=4` is strictly safe, because `4+3a<6`;
- for `t=5`, the remaining pair reaches the threshold only at `P,P`, since
  `2a>1` while `epsilon_5+epsilon_7<1`;
- `t=6` leaves the family `T^6 Q`, with arbitrary seventh cycle `Q`;
- `t=7` is included in `T^6 Q` by taking `Q=T`.

Thus the exact structural frontier is

`T^6 Q={T,T,T,T,T,T,Q}`,                                      (R7a)

`T^5PP={T,T,T,T,T,P,P}`.                                      (R7b)

This is still narrow enough to make structural induction plausible, but the
two families behave differently. In (R7a) there is only one distinguished
cycle, so every proper cluster decomposition has an all-triangle leaf. In
(R7b), the two pentagons can occupy both leaves of a reduced tree, recreating
the pentagon-ended path obstruction from rank six.

For later use, (1) gives only `sigma(G)>=0` inside (R7a) when `Q` is even, not
the required strict inequality. If `Q` is odd, it gives
`sigma(G)>=-epsilon_q`; this coarse bound does not by itself interact safely
with qualitative packet strictness.

## 2. Reduced cluster tree leaves

Use the shared-cut graph and reduced cluster tree from the hexacyclic proof.
Every marked node is one shared-cut cluster, including singleton cycles. A
connected subtree of marked nodes expands to a connected induced territory by
cutting actual bridges, assigning every Steiner branch and every hanging tree
to one owner.

### Proposed Lemma R1 (triangle singleton leaf induction)

If a singleton triangular cluster is a leaf of the reduced cluster tree, cut
the first actual bridge toward the rest. The two induced territories are a
triangular unicyclic cactus `A` and a connected hexacyclic cactus `H`. Hence

`sigma(G)>=sigma(A)+sigma(H)>0`.

This is the ideal induction step: it spends no fixed margin. It applies with
arbitrary connector length, connector branching, entry vertex, and attached
trees.

### Proposed Lemma R2 (all-triangle leaf-cluster cut)

Let `A` be a leaf cluster consisting of `r` triangles, where `1<=r<=6`.
Cutting its unique external connector gives an `r`-cyclic all-triangle
territory `A` and a connected `(7-r)`-cyclic territory `B`. The following
bounds close every value of `r` (the last row occurs only in `T^6Q`):

| `r` | triangle side | remote side | conclusion |
|---:|---|---|---|
| 1 | `sigma(A)>0` | hexacyclic `>0` | positive |
| 2 | `sigma(A)>1` | pentacyclic `>0` | positive |
| 3 | `sigma(A)>2` | tetracyclic `>0` | positive |
| 4 | `sigma(A)>3` | tricyclic `>=0` | positive |
| 5 | `sigma(A)>2` | bicyclic `>=0` | positive |
| 6 | proposed `sigma(A)>1` | hostile unicyclic `>-1` | positive |

The rows through five are established packet bounds. The last row is the only
new quantitative input and follows from the leaf-opening recurrence developed
in Section 3. Notice that it is stronger than needed against nonhostile `Q`;
its purpose is to absorb the worst unicyclic deficit `-delta_q>-1`.

### Consequence for proper `T^6Q` cluster partitions

If the shared-cut graph is disconnected, the minimal reduced cluster tree has
at least two leaves. At most one leaf cluster contains `Q`; therefore another
leaf is an all-triangle cluster. Lemma R2 would settle the entire disconnected
case in one argument, with no colored set-partition table and no reduced-tree
topology census.

This conclusion depends on the leaf cluster being separated across an actual
bridge, not merely on a triangle being a leaf of an incidence tree. It also
uses the fact that (R7a) has only one nontriangle. This is exactly where the
`T^6Q` frontier is simpler than `T^5PP` and the hexacyclic `TTTTPP` frontier.

### Proposed Lemma R3 (pentagon-ended reduction for `T^5PP`)

For a proper cluster partition of `T^5PP`, either an all-triangle leaf cluster
exists, or every reduced-tree leaf contains a pentagon. In the latter case
there are exactly two leaves, the reduced tree is a path, and each endpoint
cluster contains one pentagon. The target conclusion is an induced
packetization of one of the forms

`TP + TTT + TP`, `TP + TT + T + TP`, or `T + (hexacyclic)`.

The first two forms have fixed positive ledgers. Lemma R3 must be
entry-sensitive when an endpoint cluster is nontrivial: a pentagon and its
nearest triangle may share a cut, and an internal cluster may require a
consecutive-interval split before the abstract path packets become induced.
The smallest obstruction to direct use of R1 is the singleton path

`P-T-T-T-T-T-P`.

It is not an obstruction to the displayed packetization, only to deleting a
triangular reduced-tree leaf. A rooted endpoint-cluster audit appears
preferable to a census of all colored set partitions.

## 3. Quantitative all-triangle shared clusters

Let `A_r` denote an arbitrary connected cactus whose `r` triangular cyclic
blocks form one shared-cut cluster, with arbitrary attached trees. Define a
certified lower margin `m_r` by `sigma(A_r)>m_r`.

The verified inputs are

`m_2=1,  m_3=2,  m_4=3,  m_5=2`.

The first three are the favorable-cycle/four-triangle estimates, and `m_5=2`
is obtained by opening one incidence-leaf triangle and retaining a
four-triangle shared cluster.

### Proposed Lemma Q1 (incidence-leaf opening recurrence)

For every `r>=3`, an incidence leaf triangle has one shared cyclic cut and two
private vertices. Opening either private vertex yields an exact induced
partition into a nonempty tree `F` and a connected shared cluster `A_{r-1}`,
with

`sigma(F)=-1`, and therefore `m_r>=m_{r-1}-1`.                    (2)

The recurrence is not an asymptotic theorem; it is an accounting device. From
`m_4=3`, it gives

`m_5>=2,  m_6>=1,  m_7>=0`.

In particular:

### Proposed Lemma Q2 (six-triangle shared-cluster margin)

Every six-triangle shared-cut cluster satisfies

`sigma(A_6)>1`.                                                   (3)

Proof route: open one incidence-leaf triangle, retain a five-triangle shared
cluster, use `sigma(A_5)>2`, and add the tree cost `-1`. This is enough for the
`r=6` row of Lemma R2 because every hostile unicyclic `Q` has
`sigma(Q)>=-delta_q` with `delta_q<1`.

Equation (2) also explains the limit of naive induction. A seven-triangle
shared cluster receives `sigma>0`, which closes that subcase directly but
cannot pay even one additional opening. It must not be used as a positive
budget inside a larger sacrifice.

### Optional strengthening worth isolating

If the cycle-packing number of `A_r` is at most two, the Sachs half-plane
argument gives `sigma(A_r)>r-1`. Thus the weak recurrence is needed only when
three or more vertex-disjoint triangles occur. For `r=7`, a useful target is:

**Proposed Lemma Q3 (packing-three-or-more split).** Every seven-triangle
shared-cut incidence with packing number at least three admits an ordinary
cycle-interval split into at least two retained all-triangle packets, one of
which is strict, with positive total surplus.

Q3 is deliberately a structural target, not an asserted fact. A countershape
to test first is a saturated central triangle with three petal branches, each
branch itself carrying further triangles; short-cycle capacity and coincident
multiway cuts make this the plausible obstruction to a one-cycle split.

## 4. Fully shared incidence and a leaf-opening recurrence

Assume all seven cycles form one shared-cut cluster. Let `I` be the bipartite
cycle-cut incidence tree. With seven cycle nodes and `c` shared-cut nodes,

`|E(I)|=c+6`, and `sum_x(deg_I(x)-1)=6`,                        (4)

so `1<=c<=6`. Every leaf of `I` is a cycle node.

In `T^6Q`, `I` necessarily has a triangular leaf. In `T^5PP`, both incidence
leaves may be pentagons; the alternating path

`P-x-T-x-T-x-T-x-T-x-T-x-P`

is the smallest example. Thus the first family presents a quantitative
triangle-opening problem, while the second also presents genuine leaf
avoidance.

Let `T` be a leaf triangle with shared cut `x` and private vertices `u,v`.
There are two canonical operations.

1. **Split inward.** Delete an internal neighboring cycle node into proper
   consecutive intervals. One interval may retain `T`, but the split cycle is
   destroyed, so the output is a collection of packets of total rank six, not
   `T` plus a hexacyclic remainder.
2. **Open `T`.** Remove a private vertex, assign its rooted branch to a tree
   territory of surplus `-1`, and retain the other six cycles in one shared
   cluster. This gives only

   `sigma(G)>=sigma(H_6)-1`,                                    (5)

   so the qualitative hexacyclic theorem is insufficient.

The needed recurrence must choose between these operations according to the
local degree and the six-cycle remainder.

### Proposed Lemma F1 (quantitative leaf-opening alternative for `T^6Q`)

For a fully shared `T^6Q` incidence tree and a triangular leaf `T` at `x`, at
least one of the following holds:

- **inward split:** a cycle-interval split at the neighbor of `x` yields
  retained lower-rank packets with positive total surplus;
- **paid opening:** opening `T` leaves a hexacyclic shared cluster `H_6` with a
  certified margin `sigma(H_6)>1`;
- **ordinary split:** some cycle node has a consecutive-interval split whose
  retained branch packets have positive total surplus;
- **common-cut core:** all failed choices force one of the explicit obstruction
  families in Section 6.

F1 is the main missing induction lemma. Its useful feature is that it asks only
for a local reduction to the already classified rank-six packet ledger, not a
canonical enumeration of every seven-cycle tree.

### Proposed Lemma F2 (when the paid opening is automatic)

After opening a triangular leaf, the six retained cycles are `T^5Q`. The cost
in (5) is paid in either of these checkable situations:

- the remainder is six triangles in one shared cluster, by (3);
- the remainder has cycle-packing number at most two and all cycles are
  `3 mod 4`, giving margin `>5`;
- an ordinary split of the remainder has certified packet sum `>1`;
- opening `Q` and one additional triangle leaves a four-triangle shared cluster
  of margin `>3`, provided the total number of opened tree territories is at
  most three and strictness is retained.

The third bullet should be implemented as a symbolic rank-six ledger, reusing
the verified `TTTTTQ` incidence certificates rather than re-enumerating
rank-seven objects. The fourth bullet is a last-resort sacrifice and needs
exact ownership of all common cuts.

### Proposed Lemma F3 (two-pentagon endpoint alternative)

For a fully shared `T^5PP` incidence tree, at least one of the following holds:

- a triangular incidence leaf has an inward split with positive packet sum;
- deleting an internal cycle node and assigning consecutive intervals gives
  `TP+TTT+TP` or a positive refinement;
- both pentagons have admissible private openings and the five retained
  triangles remain one shared-cut cluster, giving `>2-2=0`;
- a saturated pentagon hub admits a cyclic split of type `TP+TT+T+T` or
  `TP+T+T+T+T`;
- failure is confined to a two-hub ownership core.

The concentration clause in the third bullet is essential. Opening both
pentagons may leave a connected induced remainder while dispersing the five
triangles into several shared-cut clusters, in which case the quantitative
five-triangle bound is unavailable. Likewise, a pentagon using all five
vertices as cyclic cuts has no private opening vertex. These are the two
specific hostile mechanisms F3 must distinguish.

## 5. Hostile residual mixes after opening

In `T^6Q`, local splitting can isolate `Q` or place it in a small packet. In
`T^5PP`, it can isolate one or both pentagons. The dangerous configurations are
determined by margin, not merely by cycle count.

### Safe local packets

- `TQ` has `sigma>1-delta_q>0` for hostile `q=1 mod 4`.
- `TTQ` is nonnegative as a generic tricyclic cactus; it becomes useful only
  when another branch is strict.
- `T^kQ` is positive for `k=3,4,5` by the verified lower-rank theorems, but
  this qualitative positivity cannot pay a tree opening.
- An isolated hostile `Q` costs at most `delta_q<1`; it is safely absorbed by
  `TT` with margin `>1`, by a six-triangle cluster with margin `>1`, or by any
  explicitly larger packet margin.

### Proposed Lemma H1 (hostile singleton absorption)

If a cycle-interval split isolates `Q`, and the six triangles occupy at most
five other nonempty branches, then either some branch contains `TT`, giving
total `>1-delta_q>0`, or every triangular branch is a singleton. In the latter
case the split has six strict triangular territories plus `Q`; strictness alone
does not uniformly absorb `delta_q`, so the cycle owning the intervals must
merge the `Q` mark with one adjacent triangular mark to form `TQ`.

This cyclic-neighbor merge is always available when the split cycle has a
proper interval containing the two marks. It must be checked separately when
the marks coincide at a multiway cut or when the split cycle is a triangle and
has only three vertices.

### Proposed Lemma H2 (hostile branch promotion)

If `Q` lies in a branch with at least one triangle, keep the smallest connected
initial segment containing `TQ` as one territory. Its positive margin removes
the only hostile deficit. Partition all remaining branches into lower-rank
nonnegative packets, requiring at least one strict all-triangle packet if any
generic `TTQ` branch is used only at zero.

The obstruction is not spectral but geometric: the initial `TQ` segment may
share the splitting-cycle vertex needed by another branch. A precise proof
must phrase H2 in terms of consecutive intervals around one cycle, not paths in
the abstract incidence tree alone.

### Proposed Lemma H3 (no qualitative payment)

Any reduction with `k` opened cycles must exhibit retained packets with total
certified margin strictly greater than `k`. A qualitative hexacyclic,
pentacyclic, or tetracyclic theorem may supply strictness after a nonnegative
ledger, but it may not be counted as any positive numerical amount.

H3 is an accounting rule rather than a spectral statement. Making it explicit
prevents the most likely false induction step.

### Proposed Lemma H4 (two-pentagon pairing)

In every `T^5PP` split, each isolated pentagon must be merged with an adjacent
triangular mark to form a positive `TP` packet, paired with the other pentagon
using a proved shared-`PP` bound, or opposed by an explicitly larger
triangle-cluster margin. Two qualitative strict terms do not pay `-2delta`.
If both pentagons are leaves of a path, simultaneous pairing should produce
`TP+X+TP`, where `X` is an all-triangle packetization with nonnegative total.

## 6. Smallest obstruction cores

The following are obstructions to particular induction moves, not candidate
counterexamples to positive square energy.

### O1. Seven-cycle bouquet: smallest common-cut lock

All six triangles and `Q` share one cut vertex `x`. The incidence tree has one
cut node and seven leaf cycles. No retained triangle can be separated from a
retained hexacyclic remainder because both require `x`.

A quantitative repair is nevertheless available for `T^6Q`. Open `Q` and two
designated triangles at private vertices. The other four triangles remain one
shared-cut cluster, so

`sigma(G)>3-3=0`.

This is strict and includes `Q=T`. It uses three tree territories, each of
surplus exactly `-1`. The bouquet is minimal in number of shared cut nodes and
is the first mandatory exception to an inward-split-only recurrence.

For the `T^5PP` bouquet, open both pentagons. The five triangles remain one
shared-cut cluster and give `>2-2=0`. Thus the same incidence core has two
different quantitative repairs.

### O2. Saturated `Q` hub with six triangular petals

If `q>=6`, let `Q` meet six triangles at six distinct cuts. Splitting `Q`
around its six marks gives six strict triangular territories and destroys `Q`.
This has positive total with no hostile deficit because `Q` is not retained.

For `q<6`, six distinct marks are impossible; multiway cuts identify petals
and lead toward bouquet/hybrid cases. Thus the obstruction is not the saturated
hub itself but the short-hub version with coincident marks.

### O3. Saturated triangle hub with three compound branches

A triangle hub uses all three vertices as shared cuts, with two triangles
distributed in each of three branches and `Q` lying in one branch (or with one
multiway cut carrying `Q`). No private vertex is available on the hub. A naive
hub opening is impossible, and independent branch cuts may allocate a hub
vertex twice.

This is the smallest capacity obstruction: a triangle has only three vertices,
yet all six incidence-excess units can be concentrated through three multiway
cuts. It is the first shape to test for failure of Q3 and F1.

### O4. Double hub with an ownership cut

Two internal cycle nodes meet at a cut `x`; triangular branches occur on both
sides and `Q` lies on one side. Splitting both hubs independently can assign
`x` to two territories. The desired outcome is one of

`TQ + TT + T + T`, `TTQ + TT + T`, `T + (hexacyclic)`,

or a paid opening with retained margin `>1`.

This is the smallest obstruction to composing local interval splits. It calls
for a two-hub compatibility lemma, not a global incidence census.

### O5. Pentagon-ended paths and dispersed sacrifice

In `T^5PP`, both leaves can be pentagons, in either the reduced cluster tree or
the fully shared incidence tree. The singleton/degree-two model is

`P-T-T-T-T-T-P`.

No triangular leaf induction is available. The packet `TP+TTT+TP` repairs the
bare path, but endpoint clusters and multiway cuts require rooted interval
versions. A separate fully shared obstruction occurs when opening both
pentagons leaves the five triangles in several shared-cut components; ordinary
connectivity of the path remnants does not restore the concentrated
five-triangle margin.

### O6. All-seven-triangle recurrence floor

Opening three incidence leaves until four triangles remain gives exactly

`sigma>3-3=0`.

Thus it proves positivity for a shared seven-triangle cluster, but leaves no
budget for another operation. The obstruction is quantitative rather than
topological: the recurrence reaches zero at rank seven. Any proposed global
induction that first pays an external tree cost and only then invokes this
bound is invalid.

## 7. Precise lemma package to pursue

The proposed proof can be organized around the following statements.

1. **DNN residual lemma.** Equation (1) is strict unless the cycle multiset is
   `T^6Q` or `T^5PP`.
2. **All-triangle leaf-cluster lemma.** Lemma R2, using the six-triangle margin
   `>1`, settles every disconnected `T^6Q` shared-cut graph and every `T^5PP`
   partition having an all-triangle leaf.
3. **Triangular recurrence lemma.** Q1 and Q2, including arbitrary attached
   trees and exact induced ownership.
4. **Inward leaf-split lemma.** At a degree-two leaf cut, specify sufficient
   local incidence conditions for a positive rank-six packetization after the
   neighboring cycle is split.
5. **Paid leaf-opening lemma.** Classify the rank-six remainders after opening
   a triangular leaf for which the verified hexacyclic proof supplies margin
   `>1`, not merely positivity.
6. **Hostile-mark merge lemma.** On a split cycle, either absorb singleton `Q`
   with a `TT` branch or merge its mark with an adjacent triangle to form `TQ`.
7. **Short-hub lemma.** Resolve saturated triangle hubs and coincident
   multiway-cut marks under the degree cap three.
8. **Two-hub compatibility lemma.** Give the common cut one owner and produce
   one of the positive packetizations listed in O4.
9. **Common-cut sacrifice lemma.** If every ordinary split fails because all
   retained cycles require one cut, sacrifice exactly enough cycles to leave a
   four-triangle shared cluster; the total number of tree costs must be at most
   three.
10. **Seven-triangle split lemma.** Establish Q3 or replace it by a direct
    finite list of short-hub exceptions.
11. **Pentagon-ended path lemma.** Prove R3 for reduced-tree and incidence-tree
    paths with nontrivial endpoint clusters and arbitrary entries.
12. **Two-pentagon concentration lemma.** Prove F3, separating private opening,
    saturation, and dispersion.

Items 1--3 are immediate extensions or recombinations of verified ingredients.
Items 4--12 are the proposed new structural work; item 10 may be unnecessary
because the recurrence already proves the isolated all-seven-triangle case,
but a split form could simplify mixed local reductions.

## 8. How to avoid a seven-cycle census

A complete proof need not enumerate all bipartite incidence trees satisfying
(4). A smaller obstruction-driven audit should be run separately on `T^6Q`
and `T^5PP` and proceed as follows.

1. Choose a triangular incidence leaf minimizing distance to `Q`.
2. Test the local inward-split condition at its incident cut and neighboring
   cycle.
3. If the inward split fails, open the leaf and query a symbolic database of the
   already verified rank-six `T^5Q` certificates for margin `>1`.
4. If the rank-six certificate is only qualitative, search for one ordinary
   split cycle using branch color counts and retained-cut predicates.
5. Normalize failures by the local degree sequence around the leaf-neighbor:
   private vertex available, saturated triangle, saturated longer hub, or
   multiway cut.
6. Recurse across at most one adjacent internal cycle. If ownership conflicts,
   invoke the two-hub lemma.
7. Send the remaining common-cut lock to the sacrifice lemma.
8. For `T^5PP`, first test pentagon-ended path packetization, then distinguish
   concentrated two-opening sacrifice from saturated or dispersed failures.

The computational proof object, if needed, should enumerate only unresolved
local rooted neighborhoods `(leaf T, incident cut, neighboring cycle, next
cut)`, with colors `T/Q` or `T/P/P`, cyclic mark coincidences, and capacities. It should
not canonicalize complete seven-cycle trees. The output should be explicit
rooted obstruction tuples and a witness for inward split, paid opening, ordinary
split, double-hub reduction, or sacrifice.

There is one legitimate fallback census: enumerate the residual rooted
neighborhoods after all structural lemmas are encoded and assert that every
unresolved object embeds in O1, O3, O4, or the pentagon-ended/dispersed family
O5. This is materially smaller and more explanatory than a census of all
seven-cycle incidences.

## 9. Verification targets and stopping rules

Before any theorem statement is attempted, the following checks are required.

- Prove the six-triangle margin (3) in manuscript form from the verified
  five-triangle bound and the exact leaf-opening partition.
- Extract quantitative, not merely qualitative, margins from each rank-six
  `T^5Q` ordinary-split certificate.
- Formalize the inward leaf-split operation with one-owner rules for the shared
  cut, connector entry, and hanging trees.
- Test H1 when singleton `Q` and all six triangle marks occupy distinct
  intervals, especially on short split cycles.
- Prove the saturated triangle-hub and double-hub lemmas with cyclic order and
  coincident-root cases explicit.
- Prove the pentagon-ended path packetization with nontrivial endpoint clusters,
  then audit saturated and dispersing two-pentagon openings separately.
- Independently audit every sacrifice: each opened territory is a nonempty
  tree of surplus exactly `-1`, and the retained four triangles remain one
  connected shared-cut cluster.
- Run a rooted local obstruction search and print canonical unresolved
  neighborhoods, not just counts.

Stop if an argument asks qualitative hexacyclic positivity to pay `1`, asks
unspecified triangular strictness to pay `delta_q`, assigns a shared cut to two
territories, or treats an incidence leaf as a bridge leaf. Each such event
signals a missing quantitative or ownership lemma.

## 10. Current assessment

The rank-seven problem appears structurally more favorable than a direct
seven-cycle census suggests. The DNN frontier has only `T^6Q` and `T^5PP`.
For `T^6Q`, every proper shared-cluster partition has an all-triangle
reduced-tree leaf, and the new margin `sigma(A_6)>1` follows from the verified
rank-four and rank-five triangular cluster bounds; this would dispose of that
entire disconnected family. For `T^5PP`, the remaining disconnected work is
concentrated in pentagon-ended paths and nontrivial endpoint clusters rather
than arbitrary colored partitions.

The fully shared work has two branches. In `T^6Q`, a triangular incidence leaf
always exists, but opening it costs one and the hexacyclic theorem is only
qualitative. In `T^5PP`, triangular leaves can be avoided and opening both
pentagons can fail through saturation or dispersion. The plausible route is an
adaptive recurrence plus endpoint pairing: split inward when possible, pay a
leaf opening only from a quantitative rank-six certificate, pair hostile
pentagons with triangles, and prove that failures collapse to common-cut,
short-hub, dispersed-hub, or double-hub cores. Whether those local lemmas are
exhaustive remains to be verified. No heptacyclic theorem is claimed here.
