# R21 adjacency-level semantic parent gate: design and proof obligations

Date: 2026-11-18. Status: **NONPROMOTIONAL / design + compact prototype**.
Branch artifact: `research/r21-adjacency-parent-gate-verifier.py` (this branch
only; the parent lane is not modified).

## 0. Verdict

The current R21 literal-cycle typing gate and the reduced block-cut hull
verifier do **not** compose by passing a `q` or a symbolic family name from one
to the other. The typing gate supplies an adjacency-authenticated
`D+4T+C_q` inventory, but it does not construct the cyclic hull, identify the
first actual `K2` bridges, isolate the hostile `C5` side, choose the least-depth
`D+T+T` anchor, or own a single physical vertex. The hull verifier consumes an
abstract `ReducedCase`; its `rootmost_cyclic_route_k2_deleted=True` is a free
witness, its `bridge_groups` are supplied rather than derived, and its
`payload_mass` is an aggregate quotient statistic.

The missing object is a **semantic parent gate**:

```text
finite simple adjacency
  -> Tarjan block inventory + arbitrary Theta(1,2,r) path typing
  -> actual cyclic hull and first/rootmost K2 bridge set
  -> (C5 row) actual bridge isolating the rank-one C5 side
  -> physical root shared-cut cluster with ports
  -> least-depth DTT anchor, cut closure, opened territories
  -> original-vertex + rooted-payload partition
  -> conditional credit ledger
```

This note specifies that gate, records the exact proof obligations, and
records the overbroad-composition counterexamples. The accompanying prototype
executes the adjacency, Tarjan, theta, C5-orientation, first-hull-bridge,
root-cluster, cut-closure, ownership, and ledger stages. It does **not** prove
any spectral packet inequality and does **not** claim a theorem.

The gate covers both DNN-open physical R21 rows:

1. `Theta(1,2,r)+T^5`, arbitrary `r>=2`; and
2. literal `D+T^4+C5`.

It fails closed on the DNN-closed rows, on a C5 that is not isolated by an
actual bridge, on a C5 side of rank greater than one, on arbitrary theta
blocks in the C5 row, and on every symbolic label without materialized
adjacency.

## 1. Why the existing two artifacts do not compose

### 1.1 The literal-cycle typing gate

`research/r21-literal-cycle-typing-verifier.py` (parent branch, commit
`ccb201ef`) correctly:

* accepts arbitrary finite simple adjacency;
* runs a Tarjan edge-stack decomposition;
* authenticates exactly one literal `D=Theta(1,2,2)=K4-e` and five literal
  cycle blocks;
* permits rank-zero bridge blocks and one-root acyclic attachments;
* classifies `q=3` as `D+T^5`, `q=5` as `D+T^4+P(C5)`, and every other `q` as
  DNN-closed.

It does **not**:

* reconstruct the cyclic hull spanning `D` and the four external triangles;
* distinguish a bridge on a `D`-to-triangle hull route from a bridge inside a
  rooted tree payload;
* identify the first/rootmost `K2` bridge or prove the no-second-cut rule;
* prove that the `C5` is on the far side of an actual bridge;
* derive the root shared-cut cluster, its ports, or the least-depth `D+T+T`
  anchor;
* assign an original vertex or a rooted acyclic component to a territory;
* reconstruct the `ReducedCase`, the ledger, or any packet inequality.

Its own `q=5` fixture `build_profile(5)` puts the `C5` in the same shared cut
as `D` and the four triangles. That graph is typing-valid but **outside** the
reduced hull theorem's scope, because no bridge isolates the `C5` side. This is
the first overbroad-composition counterexample (§6.1).

### 1.2 The reduced block-cut hull verifier

`research/r21-reduced-block-cut-hull-verifier.py` (parent branch, commit
`03ac2166`) correctly proves a finite combinatorial quotient lemma once the
following are supplied:

* a labelled root shared-cut cluster with injective physical ports;
* first-hull-bridge away triangle groups;
* a positive chain witness for each first bridge;
* exact destination labels for aggregate payload mass;
* literal triangle segment witnesses.

But:

* `derive(case)` reads `rootmost_cyclic_route_k2_deleted=True` as a supplied
  Boolean. It does not derive it from adjacency.
* `make_case(...)` manufactures `payload_mass` and the bridge groups from a
  caller-supplied cluster and partition.
* The 307 versus 606,783 census is a count of **labelled decorated abstract
  quotient states**, not of physical graphs. It does not reconstruct a graph
  from a state, and it does not prove that every physical `H` maps to exactly
  one state except in the accompanying prose.
* The connected/induced/disjoint/exhaustive original-vertex lift is prose, not
  adjacency-enumerated.
* The C5 typing is explicitly marked "REQUIRED BUT NOT PROVED HERE."
* The hull verifier's `derive` does not check that the supplied `bridge_groups`
  correspond to actual first hull bridges of the supplied cluster.

The parent gate therefore has to do two things at once:

1. construct the exact `ReducedCase` data from physical adjacency (so the
   Boolean and the groups become derived, not assumed); and
2. produce an original-vertex ownership certificate that the hull verifier's
   prose currently asserts but does not execute.

## 2. Definitions used by the gate

### 2.1 Physical graph and Tarjan blocks

`G` is a finite, connected, undirected, simple graph. `D` is the Tarjan edge
decomposition; `block_rank(B)=|E(B)|-|V(B)|+1`. A rank-zero block is a single
physical bridge `K2`. Rank-one blocks are cycles. The graph rank is
`|E|-|V|+1`.

The R21 inventory is the positive-rank multiset `(2,1,1,1,1,1)` with graph
rank seven. Rank-zero bridges and one-root acyclic attachments are permitted.

### 2.2 Arbitrary rank-two theta typing

A rank-two block `B` is `Theta(1,2,r)`, `r>=2`, iff:

* `|E(B)|=|V(B)|+1` and the block is 2-connected;
* exactly two vertices have block degree 3; all others have block degree 2;
* the two branch vertices `x,y` are joined by a literal unit edge;
* deleting `x,y` leaves exactly two path components whose sizes are `1` and
  `r-1` (both `1` when `r=2`);
* the reconstructed path lengths are `(1,2,r)` and sum to the block's edge
  count.

No symbolic theta label is read. For `r=2`, the two length-two arms are
symmetric; the gate records both as legal long-arm candidates. For `r>=3`,
the unique long arm is reconstructed and its internal vertex sequence is kept
for the opening analysis.

### 2.3 Cyclic hull and first/rootmost hull bridges

Build the block-cut incidence tree of the D+4T side `H`: block nodes are all
Tarjan blocks, cut nodes are vertices belonging to at least two blocks. The
tree is rooted at the `D` block.

For each external triangle `T`, take the unique `D`-to-`T` path. The **first
hull bridge** is the first rank-zero block on that path. The set of first hull
bridges over all four triangles is an antichain: if `b2` lay beyond `b1` on a
`D`-to-`T` route, then `b1` would be the first bridge on that route, so `b2`
could not be first on any route through that prefix.

Delete all first hull bridges simultaneously. The away component beyond each
first bridge contains at least one triangle and no second cut is made inside
it. The `D`-side component is the root component; its retained triangles are
those with no bridge on their `D`-to-`T` path. This is the exact meaning of the
hull verifier's free Boolean.

Bridges not on a `D`-to-triangle path are payload bridges and are never cut.
This is the distinction that the typing gate's flat bridge inventory does not
make.

### 2.4 C5 orientation

For the `D+T^4+C5` row, the C5 must be isolated by an **actual bridge** of the
full rank-seven graph. The gate tests each Tarjan bridge `e`: remove `e`,
compute the two components, and require one side to have rank one with unique
positive-rank block exactly the literal `C5`, and the other side to have rank
six with positive-rank blocks exactly `D` plus four literal `C3`. It also
requires `e` to be the only crossing edge between the two sides.

If the C5 shares a cut vertex with `D+4T`, no bridge isolates it and the gate
fails closed. This is not a defect: it is the boundary of the reduced-hull
theorem.

If the C5 hangs behind a tree chain, several bridges may isolate a rank-one
C5 side: every bridge on the unique H-to-C5 path separates a rank-one side
containing the C5 plus a one-root tree prefix. All such splits are legal. The
gate records all candidates and chooses the one whose C5 side is smallest, so
that the H side keeps the maximal tree payload. Requiring uniqueness here
would over-reject a valid physical profile.

### 2.5 Root shared-cut cluster and ports

After the first-hull-bridge cuts, the root component contains `D` and `k`
triangles, `0<=k<=4` for the C5 row or `0<=k<=5` for `D+T^5`, with no bridge
between any retained block on a `D`-to-triangle route.

The physical root cluster records:

* one node per retained block (`D` plus the `k` triangles);
* one cut node per physical vertex that belongs to at least two retained
  blocks;
* an incidence edge for each containment;
* a port index at each incidence, equal to the vertex's canonical position in
  the block's vertex ordering.

The incidence graph must be a tree. A block's port at different cut nodes must
be distinct; two cut nodes may not reuse the same physical vertex. These are
exactly the abstract `valid_cluster` conditions, now derived from the actual
vertex labels.

### 2.6 Least-depth anchor and cut closure

If `k>=2`, choose the two retained triangle block nodes of least depth from
`D`, breaking ties by label. Their minimal incidence hull `K0` contains no
third triangle: a third triangle on the union of the two root paths would be a
proper ancestor of one endpoint and hence have strictly smaller depth.

Let `S` be the cut closure: `K0` plus every cut node incident with `D`, `Ta`,
or `Tb`. Every edge from `S` to an unselected triangle is a frontier
`c -> T`. The far-side block-cut component of that edge, translated to original
vertices with `c` removed, is one opened territory. A nested unselected
triangle is part of the first boundary's far side; it is never a second cut.
If two unselected triangles leave the same cut `c`, their far-side components
are separate opened territories.

This is the exact combinatorial content of the hull verifier's
`cut_closed_ownership`. The gate derives it from the physical incidence tree.

### 2.7 Original-vertex and rooted-payload ownership

For `H` (the D+4T or D+5T side), the gate constructs:

* `A0`: the root component's upstream core (`D` plus the anchor triangles for
  `k>=2`; `D` for `k=0`; `D+T` for `k=1`) plus every acyclic off-core component
  whose unique physical root lies in `A0`;
* `W`: one opened territory per frontier, consisting of the far-side block
  vertices excluding the upstream cut, plus every acyclic off-core component
  rooted in it;
* `B_i`: one first-hull-bridge away territory per first bridge, consisting of
  the complete component beyond the bridge (including every K2-chain remnant,
  connector branch point, nested triangle, and rooted tree).

For the C5 row, `P` is the complete rank-one C5-side component beyond the
isolating bridge.

The gate verifies:

* pairwise disjoint vertex sets;
* exhaustive union equal to `V(H)` (and `V(G)` after adding `P`);
* each territory is connected in its induced subgraph;
* every acyclic off-core component has exactly one neighbor in the core (rank
  and block-inventory force this; the gate checks it rather than assuming it);
* every boundary cut is owned by `A0` and excluded from the opened territory;
* each opened/bridge territory's positive-rank blocks are literal triangles;
* `A0`'s positive-rank blocks are exactly `D` (`k=0`), `D+T` (`k=1`), or
  `D+Ta+Tb` (`k>=2`), and the relevant paths in `A0`'s block-cut tree are
  bridge-free (the narrow attached D/D+T/D+T+T scope).

The induced subgraphs are the pieces to which induced square-energy
superadditivity applies. Crossing edges (bridge edges and frontier edges at a
cut) are discarded.

## 3. Minimal gate stages

The prototype's `run()` is organised as follows.

### Stage 0: source and inventory authentication

* Pin exact bytes, SHA-256, and unique semantic tokens for the analytic
  sources (§7).
* Type the graph: connected, simple, rank seven, cyclic ranks
  `(2,1,1,1,1,1)`.
* Authenticate the rank-two theta as `Theta(1,2,r)`.
* Authenticate all rank-one blocks as literal cycles.
* Accept only `(3,3,3,3,3)` (theta + five triangles) or
  `(3,3,3,3,5)` (D + four triangles + C5).
* Check the final exact integer brackets: the literal `D` row uses `17>9`
  (`Delta(1,2,2)>1`); the `q=5` row uses `425>361`
  (`sqrt(17)+5>4sqrt(5)` after two squarings). For `Theta(1,2,r)+T^5` with
  `r>=3`, the pinned exact `Delta`-classification gives `Delta(1,2,r)>1`
  directly; there is no single `D`-form integer bracket. The radical
  identities and the classification are pinned analytic inputs; only the
  displayed brackets are recomputed.

### Stage 1: family dispatch

* `THETA_PLUS_T5`: arbitrary theta, five literal triangles.
* `D_PLUS_T4_C5`: require the theta to be literal `D=Theta(1,2,2)`; isolate
  the C5 side.

### Stage 2: C5 orientation (C5 row only)

As in §2.4. Fail closed if no bridge isolates a rank-one C5 side, if the C5
side has rank greater than one, or if the H side is not `D+4T`. If several
bridges isolate a rank-one side (a C5 behind a tree chain), choose the one with
the smallest C5 side and record all candidates.

### Stage 3: first-hull-bridge split (H side)

As in §2.3. The output is:

```text
HullSplit(
  theta_block,
  triangles,
  root_triangles,
  bridge_groups = [(bridge, away_side, triangles), ...],
  root_side
)
```

The gate checks that the first bridges are an antichain, each away component's
positive-rank blocks are exactly its mapped triangles, and no away component
overlaps another.

### Stage 4: physical root cluster

As in §2.5. The output is a `PhysicalCluster` with the actual labels, cut
vertices, port tuples, and depths. The gate checks the incidence tree,
connectedness, port injectivity, and that the cluster uses exactly the retained
blocks.

### Stage 5: anchor, cut closure, opened groups

As in §2.6. For `k>=2`, `select_anchor_pair` and `derive_opened_groups` produce
the upstream core, the opened core territories (with their block names), and
the frontier. For `k<2`, the whole root cluster is upstream.

### Stage 6: ownership

As in §2.7. `payload_assignments` folds every maximal acyclic off-core
component into the unique territory containing its physical root. The gate
verifies the partition, connectedness, block classes, and bridge-free packet
paths.

### Stage 7: ledger

Conservative per-territory credits:

| territory | credit | strict? |
|---|---:|---|
| upstream `k=0` | `1` | yes (`sigma(D)>1`) |
| upstream `k=1` | `2` | yes (`sigma(D+T)>2`) |
| upstream `k>=2` | `3` | yes (`sigma(D+Ta+Tb)>3`) |
| opened `W` | `-1` | no (complete first boundary floor) |
| first-hull bridge `B_i` | `0` | no (all-triangle cactus is stronger) |
| C5 side `P` | `-1` | no (`sigma(P)>-delta_5>-1`) |

The hull ledger is strictly above the threshold:

* C5 row (`D+4T`): threshold `>1`, because the C5 side costs `-1`.
* `D+5T`: threshold `>0`, because there is no separate C5 side.

For `k>=2` and `m` opened territories, `m<=k-2`, so the ledger is
`>3-m >= 3-(k-2) = 5-k`; for `k=4` this is `>1`, and for `k=5` this is `>0`.

### Stage 8: report

The report records the adjacency fingerprint, block inventory, theta path
lengths, the chosen bridge or opening, every territory's vertex count and
fingerprint, the ledger, the pinned source receipts, and the external analytic
inputs. It is explicitly conditional and nonpromotional.

## 4. Arbitrary `Theta(1,2,r)+T^5`

### 4.1 Long-arm opening

Let the theta arms be `xy` (length 1), `x-a-y` (length 2), and `P` (length
`r`). Choose an internal vertex `v` of `P`; for `r=2`, either length-two arm is
legal, and the other length-two arm supplies the intrinsic triangle.

Let `R` be the component of `G - E(theta)` containing `v`. Then:

* `R` is connected and induced;
* `R` contains exactly one theta vertex, namely `v` (otherwise an off-theta
  path between two theta vertices would add a cycle and exceed rank seven);
* the only edges crossing `R | (V-R)` are the two theta edges at `v`;
* every external triangle is wholly in `R` or wholly in `H=G-R`;
* `R`'s positive-rank blocks are literal `C3` blocks (or `R` is a tree);
* `H` is connected, and its positive-rank blocks are the intrinsic triangle
  plus the external triangles not in `R`, all literal `C3`.

The gate verifies each of these from adjacency.

### 4.2 Case split

Let `k` be the number of external triangles in `R`.

**`k=0`.** `R` is a nonempty tree, so `sigma(R)=-1`. `H` is a connected
six-triangle cactus (the intrinsic triangle plus all five external triangles).
The six-triangle lemma (§5) gives `sigma(H)>1`. Total `>1-1=0`.

**`k>=1`.** `R` is a connected triangular block graph with `k` literal `C3`
blocks; `H` is a connected triangular block graph with `6-k` literal `C3`
blocks (it always retains the intrinsic triangle). The packing-two
triangular-block corollary gives `sigma(R)>0` and `sigma(H)>0`. Total `>0`.

This eliminates the nested induced-piece theorem's "rank-at-most-six
complement is nonnegative" branch. That branch depended on the completed
connected rank-two-through-six theorem, which in the current tree is available
as a committed execution attestation rather than a fresh exact replay. The
gate does not use it.

### 4.3 Ownership

`R` and `V-R` partition `V(G)`. `R` receives `v` and every off-theta component
rooted at `v`; `H` receives every other theta vertex, the long-arm remnants,
the intrinsic triangle, and every external triangle not rooted at `v`. The two
theta edges at `v` cross and are discarded. No vertex, tree branch, connector
remnant, or nested triangle is unassigned.

### 4.4 Legal opening vertices

The gate accepts only internal vertices of the unique long arm for `r>=3`, and
either length-two arm's internal vertex for `r=2`. It rejects:

* branch vertices `x,y` (removing one turns the theta into a spider and loses
  the six-triangle count);
* the internal vertex `a` of the short length-two arm for `r>=3` (the intact
  long arm then forms a cycle of length `r+1>3`, so the complement is not a
  triangular block graph).

## 5. The six-triangle cactus `>1` lemma, sourced carefully

The nested induced-piece theorem states the needed conclusion in prose:

> A connected cactus with at least two triangular blocks has credit greater
> than one. ... In particular it applies to six triangles.

The old supporting sentence is not enough. The quantitative proof is in three
existing notes, used together:

### 5.1 Small shared-cut clusters

`positive-square-energy/heptacyclic-general/r31-s-physical-shared-triangle-closure.md`
Lemma 1 (and `research/five-triangle-shared-cluster-surplus-2026-07-26.md`
Lemma 3) prove, for a shared-cut triangular cluster `A_r` with `1<=r<=4`:

```text
sigma(A_r) > r-1.
```

The proof handles the packing-three central-triangle/three-petal incidence by
an explicit matching injection. Arbitrary rooted trees are allowed.

### 5.2 Five and six triangles

`research/five-triangle-shared-cluster-surplus-2026-07-26.md` proves
`sigma(A_5)>2` by opening one leaf triangle and retaining a four-triangle
cluster of credit `>3`; the opened territory is a nonempty tree of credit
exactly `-1`.

`research/arbitrary-r-shared-triangle-uniform-surplus-2026-07-26.md` iterates
the same leaf opening. For `r>=4`,

```text
sigma(A_r) >= sigma(A_{r-1}) - 1,
```

because removing one private vertex of a leaf triangle leaves a nonempty tree
of credit `-1` (not credit `0`: `s^+(K2)=1`, so `sigma(K2)=-1`). Iterating from
`A_4`:

```text
sigma(A_r) > 3 - (r-4) = 7-r.
```

Thus `sigma(A_5)>2` and `sigma(A_6)>1`. This is exactly the parent's
"incidence-leaf recurrence from `A4>3` giving `>2,>1`." The recurrence is
**decreasing by one per leaf**, not nondecreasing; removing both private
vertices of the leaf triangle would leave a `K2` of credit `-1`, not `0`, so
the one-vertex opening is the correct operation.

### 5.3 Two-triangle cactus

`positive-square-energy/tricyclic-general/theta-cycle-completion.md`, credit 2,
proves that a connected bicyclic cactus whose two cyclic blocks are triangles
has `sigma>1`, with arbitrary connectors and trees. The Sachs expansion has
only singleton-triangle imaginary terms and a possible real double-triangle
term; the determinant stays in the open lower half-plane, so `s^+>s^-` and
`sigma=1+D/2>1`.

### 5.4 Assembling the six-triangle lemma

Let `W` be a connected cactus whose six cyclic blocks are triangles, with
arbitrary bridges and rooted trees. Form maximal shared-cut clusters
`C_1,...,C_s`; the reduced graph whose nodes are the clusters and whose edges
are the actual bridge paths is a tree.

* If some cluster has `r_i>=2`, then `sigma(C_i)>1` by §5.1–5.2. Every other
  cluster has `sigma>0` (a singleton triangle by the triangular-block
  corollary; a larger cluster by the same bounds). Assign every bridge/tree
  remnant to an adjacent cluster; the cluster bounds are attachment-uniform,
  so the total is `>1`.
* If all six clusters are singleton triangles, choose two adjacent marked
  nodes in the reduced tree and retain the full bridge path between them as a
  two-triangle cactus territory of credit `>1` (§5.3). Cut every off-path
  marked branch at its first actual bridge; each remainder is a connected
  triangular cactus with at least one triangle, hence `>0` by the
  triangular-block corollary. Tree remnants are assigned to an adjacent
  positive-rank territory. The total is `>1`.

This proves the six-triangle `>1` lemma from the named notes. It does not rely
on the nested theorem's unsupported single sentence, and it does not use the
rank-six theorem.

## 6. Counterexamples to overbroad composition

Each item was checked by the prototype; the rejection message is the gate's
own.

### 6.1 The typing gate's own `q=5` fixture

`build_profile(5)` (or `d_plus_t4_c5_shared`) has `D`, four triangles, and the
`C5` all sharing one cut vertex. The typing gate accepts it as
`D+T^4+P(C5)`. No bridge isolates the C5 side, so the reduced hull theorem's
prior certificate is false. The parent gate rejects:

```text
no actual bridge isolates a rank-one side whose unique cycle is the C5
```

A naive composition `if typing.q == 5: apply hull theorem` is unsound here.

### 6.2 C5 side of rank two

`d_plus_t3_c5_plus_t_isolated` has `H=D+3T`, and the far side of the bridge is
`C5+T`, rank two. The full inventory is still `D+4T+C5`, so the typing gate
accepts it. The parent gate rejects because no bridge isolates a rank-one C5
side. A naive "orient the bridge" gate that only checks that one side contains
a C5 would accept and then wrongly apply the hostile unicycle bound to a
rank-two side.

### 6.3 Chorded C5

`add_chord(d_plus_t4_c5_isolated(), "c1", "c3")` turns the C5 block into a
rank-two block. The graph rank becomes eight; `authenticate_r21` rejects. A
label-based gate that trusts the claimed `P` would accept.

### 6.4 Subdivided required triangle

`subdivide_edge(..., edge("T0:u","T0:v"), "subT")` turns a required `C3` into a
`C4` block. The cycle inventory becomes `(3,3,3,4,5)`, which is DNN-closed and
outside the two rows; the gate rejects.

### 6.5 Extra cycle behind a bridge

Attaching a triangle behind a bridge to a private vertex of `T0` makes rank
eight; the gate rejects. The hull verifier's abstract bridge groups have no way
to represent this: the physical graph is outside its rank-seven scope. The
typing gate would also reject on rank, but the parent gate must not rely on the
typing label alone.

### 6.6 C5 joined to H by a second edge

`add_chord(..., "c2", "x")` creates a second crossing edge between the C5 side
and `H`. The C5 side is no longer isolated by one bridge and the graph rank
changes; the gate rejects. A gate that only checks "there is a bridge incident
to the C5 side" would accept.

### 6.7 Arbitrary theta in the C5 row

`Theta(1,2,3)+T^4+C5` still has rank seven and five external triangles, so a
naive inventory gate might accept it. But the DNN excess is
`Delta(1,2,3)+4+epsilon_5 < 4/3+4+2/3 = 6`, so the row is DNN-closed; the
reduced hull theorem also requires literal `D`. The gate rejects:

```text
the D+T^4+C5 row requires the literal diamond D
```

### 6.8 Theta opening at a branch vertex

`verify_theta_parent(..., preferred_opening="x")` rejects because `x` is not an
internal long-arm vertex. Opening a branch would destroy the intrinsic
triangle and change the six-triangle count.

### 6.9 Theta opening on the short length-two arm for `r>=3`

`preferred_opening="a"` rejects. The intact long arm plus the unit edge forms a
cycle of length `r+1>3`, so the complement is not a triangular block graph;
the triangular-block corollary and the six-triangle lemma do not apply.

### 6.10 Theta `(2,2,2)`

A simple theta with three length-two arms has no literal unit edge. The gate
rejects. A gate that only checks rank two and degree pattern would accept and
then misclassify a non-`(1,2,r)` block.

### 6.11 First hull bridge versus all bridges

`d_plus_5t_chain` is `D` with a bridge chain carrying all five triangles. The
correct first-hull-bridge split cuts only the first bridge and books one
complete away group of five triangles. Cutting **every** bridge would create
middle acyclic segments with no triangle; those segments have credit `-1`, not
the nonnegative credit booked for a hull group, and the hull verifier's
nonempty-group rule would be violated. The gate's `first_hull_bridges` records
one group and verifies the antichain.

### 6.12 Payload bridge mistaken for a hull bridge

`with_leaf(d_plus_5t_shared(), "x")` attaches a leaf to `D` by a bridge that is
not on any `D`-to-triangle route. The gate does not cut it; the leaf is an
upstream payload. A naive "cut every Tarjan bridge" gate would cut it, book a
group with no triangle, and misassign the leaf.

### 6.13 Nested unselected triangles

In `d_plus_5t_nested`, the first boundary cut leads to a component containing a
nested triangle. The gate opens the whole far-side block component once; it
does not make a second cut inside it. A gate that loops over every unselected
triangle and requires an independent boundary cut would reject or double-cut.

### 6.14 Multiway cut

`d_plus_5t_shared` puts `D` and all five triangles at one cut. The anchor pair
is two of the triangles, and the other three leave the same cut as three
separate opened territories. The ledger is `3-3=0` strict, hence `>0`. A gate
that requires distinct boundary cuts would wrongly reject.

### 6.15 C5 or H tree payload

`c5_tree_payload()` and `h_tree_payload()` attach leaves to the C5 side and the
H side. The gate accepts; the rank-one C5 side and the D+4T side both allow
arbitrary rooted trees. This checks that the gate is not over-restricting
payloads.

### 6.16 C5 bridge attached inside a bridge group

`d_plus_t4_c5_with_hull_bridge` has `H=D+T0` and a bridge chain `T1-T2-T3`;
the C5 bridge attaches at `a` in the upstream D. The gate handles `k=1`, one
bridge group of three triangles, ledger `2`, total `1>0`. The C5 bridge's
H-side endpoint need not be in the upstream territory; the C5 side is still
rank one. A gate that requires the C5 attachment point to be upstream would
wrongly reject.

### 6.17 C5 behind a tree chain: several isolating bridges

`d_plus_t4_c5_behind_tree_chain` is `H=D+4T`, then a two-bridge tree chain
`x-b1-t-w`, then the C5 at `w`. Both `b1` and `t-w` isolate a rank-one C5
side. The gate records both candidates and chooses `t-w`, the one with the
smallest C5 side; the H side keeps `b1,t` as upstream payload. A gate that
requires exactly one isolating bridge would over-reject this legal profile.
The same choice is sound for any one-root tree prefix: the chosen H side is
still rank six with positive blocks `D+4T`, and the C5 side is the literal C5
with its one-root trees.

## 7. Pinned analytic inputs and their status

The gate pins exact bytes, SHA-256, and uniquely occurring semantic tokens for:

| source | statement used | status |
|---|---|---|
| `all-tricyclic-graphs/paper.tex` | `Delta(1,2,2)`, `Delta>1` exactly for `Theta(1,2,r)`, cycle excesses | pinned prose; no replay |
| `packing-two-square-energy/paper.tex` | `cor:triangular-block`: connected triangular block graph has `s^+>n` | pinned prose; no replay |
| `research/five-triangle-shared-cluster-surplus-2026-07-26.md` | `A_5>2`, `A_4>3`, leaf opening | pinned prose; no replay |
| `research/arbitrary-r-shared-triangle-uniform-surplus-2026-07-26.md` | `A_6>1` via `7-r`, incidence-leaf recurrence | pinned prose; no replay |
| `positive-square-energy/tricyclic-general/theta-cycle-completion.md` | two-triangle cactus `sigma>1` | pinned prose; no replay |
| `positive-square-energy/pentacyclic-general/doubled-c4-111-two-triangles-retained-packet.md` | attached `D`, `D+T` credits, one-root tree scope | pinned prose; no replay |
| `positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md` | `D+T+T` credit `>3`, bridge-free scope | pinned prose + executable child on parent branch |
| `all-tricyclic-cacti/paper.tex` | hostile C5 `delta_5`, `s^+(U_5)>=u-delta_5` | pinned prose; no replay |

The prototype's `--strict-analytics` mode **fails closed** for every required
input that is prose-only or not replayed. The default mode emits a conditional
certificate and lists the inputs. The gate never treats a source hash or token
as adjacency evidence; the hashes are change detectors and the tokens are
statement receipts.

The following are explicitly **not** used:

* the nested induced-piece theorem's R21 sentence as a proof;
* the rank-six all-connected theorem (committed execution attestation);
* the symbol `P` in the rank-seven ledger as a physical C5;
* any `STATE`, theorem-master, publication, or lane-control artifact.

## 8. Proof obligations

### 8.1 Discharged by adjacency / executable in the prototype

1. Tarjan edge decomposition, rank, bridge/cycle/theta block typing.
2. Arbitrary `Theta(1,2,r)` path reconstruction and branch/arm ownership.
3. Family dispatch and DNN-open cycle inventory.
4. C5 isolation by at least one actual bridge, minimal-C5-side selection when
   several bridges isolate, rank-one/rank-six split, unique positive-rank C5
   block.
5. First-hull-bridge selection, antichain, no-second-cut, away-triangle
   partition.
6. Physical root cluster, cut nodes, ports, incidence tree, depths.
7. Least-depth anchor, cut closure, frontier, opened group components.
8. Original-vertex partition, connectedness, inducedness, disjointness,
   exhaustiveness, unique-root payload assignment, boundary-cut ownership.
9. `A0` block classes and bridge-free `D`/`D+T`/`D+T+T` paths.
10. Conservative ledger thresholds and strictness.

### 8.2 External analytic inputs (not rederived)

1. attached `D` `sigma>1`; attached `D+T` `sigma>2`; attached `D+T+T`
   `sigma>3` (pinned notes; DTT child executable on the parent branch);
2. connected triangular block graph `sigma>0`;
3. two-triangle cactus `sigma>1`;
4. shared-cut `A_r` small-cluster bounds and the leaf recurrence;
5. six-triangle cactus `sigma>1`;
6. hostile C5 `sigma>=-delta_5>-1`.

### 8.3 Open / not claimed

1. No executable replay of the prose packet inequalities; `--strict-analytics`
   fails closed.
2. No 5-triangle decorated block-cut census. The per-graph gate computes the
   `D+T^5` hull dispatch directly; a finite exhaustive receipt would need new
   expected counts and a new `derive` mode with threshold `>0`.
3. No theorem claim, no rank-seven closure, no publication promotion.
4. The prototype does not import the parent branch's files; it copies the
   Tarjan/typing primitives verbatim and records the intended import-once
   composition. The parent branch must decide whether to share a module.

## 9. Integration plan for the parent lane

Minimal, ordered, no mutation of the parent lane from this branch:

1. **Share the primitives.** Move `PhysicalGraph`, `adjacency`,
   `biconnected_edge_blocks`, `block_rank`, `authenticate_literal_cycle`, and
   `authenticate_theta` to a small shared module, or import them from the
   literal-cycle typing gate. The prototype's copies are byte-compatible in
   behaviour.
2. **Replace the free Boolean.** In the reduced hull verifier, replace
   `rootmost_cyclic_route_k2_deleted: bool` with a `HullSplit` record derived by
   `first_hull_bridges`. `derive` should reject a `ReducedCase` whose
   `bridge_groups` do not equal the `HullSplit` groups.
3. **Add `from_adjacency`.** Construct the `ReducedCase` fields from the
   physical `HullSplit` and `PhysicalCluster`: `root_cluster` from the actual
   cut/port data, `bridge_groups` from the first-hull-bridge away components,
   `chain_lengths` from the positive bridge chains, `payload_mass` from the
   per-destination aggregate, `segment_lengths` from the literal `(1,1,1)`
   triangle witnesses.
4. **Add the ownership certificate.** Attach a `PhysicalOwnership` object with
   the actual vertex sets, connectedness, inducedness, unique roots, boundary
   cuts, and fingerprints. The hull verifier's prose lift becomes executable.
5. **Supply the C5 prior.** `orient_c5_side` supplies the prior physical
   typed-row certificate that the hull note explicitly says is "REQUIRED BUT
   NOT PROVED HERE."
6. **Keep the theta row separate.** Do not route `Theta(1,2,r)+T^5` through the
   D+4T hull verifier. Use the long-arm opening (`verify_theta_parent`). This
   avoids the rank-six branch and the wrong four-triangle census.
7. **Optional `D+T^5` hull mode.** If the five-triangle hull dispatch is wanted
   as a second route for `r=2`, add a `threshold=0` mode and a five-triangle
   census. The prototype already computes the per-graph audit; only the finite
   exhaustive receipt is missing.

## 10. Reproduction

```text
python3 research/r21-adjacency-parent-gate-verifier.py
python3 -O research/r21-adjacency-parent-gate-verifier.py
```

The program checks that the normal and `-O` outputs are byte-identical, that
there are no Python `assert` statements, and that the pinned sources have the
expected bytes and tokens.

Selected prototype results:

| fixture | result |
|---|---|
| `d_plus_t4_c5_isolated` | C5 bridge `x-w`, C5 side 5, H 12, `k=4`, opened T2/T3, H ledger 1 strict, total 0 strict |
| `d_plus_t4_c5_with_hull_bridge` | C5 bridge isolated, H `k=1`, one bridge group of 3 triangles, H ledger 2, total 1 |
| `d_plus_t4_c5_behind_tree_chain` | two isolating bridges; choose `t-w` (C5 side 5), H 14, H ledger 1, total 0 strict |
| `d_plus_5t_shared` | `k=5`, three opened frontier edges at one cut, ledger 0 strict |
| `d_plus_5t_chain` | `k=0`, one away group of 5 triangles, ledger 1 |
| `d_plus_5t_two_chains_and_shared` | `k=1`, two away groups of 2, ledger 2 |
| `d_plus_5t_nested` | `k=5`, one opened group containing nested triangles, ledger 2 |
| `Theta(1,2,r)+5T`, `r=2,3,4,5,7` | `k_R=0`, H six triangles, ledger 0 strict |
| `Theta(1,2,4)+1T@p2+4T@x` | `k_R=1`, H five triangles, two `>0` credits, ledger 0 strict |

Hostile mutations rejected by the prototype (11): C5 sharing the D cut; C5
side rank two; chorded C5; subdivided triangle; extra cycle behind a bridge;
C5 joined to H by a second edge; arbitrary theta in the C5 row; theta opening
at a branch vertex; theta opening on the short arm; C5 row passed to theta
mode; theta `(2,2,2)`.

## 11. Trust boundary

The prototype closes the **semantic gap** between adjacency and the reduced
hull quotient. It does not close the spectral gap. Every packet credit in §7 is
an external analytic input; the six-triangle and triangular-block lemmas are
prose proofs, not executable replays; the DTT child is executable only on the
parent branch and is not replayed here. The gate is therefore a conditional,
fail-closed composition certificate, not a theorem and not a publication
artifact. No parent lane state, `STATE` file, theorem-master, or publication
file is read or modified.
