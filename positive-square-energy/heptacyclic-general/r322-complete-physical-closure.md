# R322 complete physical closure — packet theorem and proof

## Status, exact scope, and nonclaim

Status: **PROVED R322 PACKET THEOREM**, conditional only on the pinned analytic
results listed in §1 and on the exact DNN sieve that identifies the packet.
This note supplies the universal block-cut proof. It does not prove the full
multiblock statement, the connected rank-seven theorem, or any single-block
case. No publication claim follows from this packet alone. The companion
Python program is finite corroboration and an adjacency-only semantic gate;
it is not the universal proof.

For a finite graph `H`, put

```text
sigma(H) = s+(H) - |V(H)|.
```

### Theorem (complete physical R322 lane)

Let `G` be a finite simple connected graph.  Reconstruct its maximal
vertex-biconnected blocks from its physical adjacency, counting every bridge
as a `K2` block.  Suppose that its positive-rank blocks are exactly

* one literal, unsubdivided `K4` block `B`; and
* two literal diamond blocks `D1,D2`, each
  `D=Theta(1,2,2)=K4-e`.

Consequently, the positive block ranks are `3+2+2=7`.  Allow arbitrary actual
`K2` bridge connectors, arbitrary connector lengths and branching, arbitrary
block-cut nesting, repeated articulation vertices, and arbitrary finite
rooted-tree attachments at any physical vertex.  Then

```text
sigma(G) > 0.
```

The conclusion is only for this adjacency-derived inventory.  It does not
cover a subdivided `K4`, a theta other than the literal diamond, another
rank-three block, another block-rank partition, a single-block graph, or the
global connected rank-seven problem.

### Why this is exactly the R322 residual inventory

This paragraph identifies the post-DNN packet; the physical theorem above may
also be read simply with its displayed inventory as a hypothesis.  For a
rank-two biconnected block `Theta(a,b,c)`, write `Delta(a,b,c)` for its exact
DNN excess.  The pinned theta classification gives

```text
Delta <= d := (sqrt(17)-1)/2,
Delta=d exactly at Theta(1,2,2),
and every other theta with Delta>1 has Delta<4/3.
```

The rank-seven debit rule for the partition `3+2+2` closes a
`K4+Theta_1+Theta_2` row exactly when

```text
Delta_1 + Delta_2 <= 3.                                  (0.1)
```

Indeed, the three debits are `1, Delta_1-1, Delta_2-1` and the
three-block allowance is `2`.  If either theta is not the literal diamond,
then

```text
Delta_1+Delta_2 < 4/3+d < 3,
```

where the last inequality is `sqrt(17)<13/3`.  If both are diamonds, then

```text
Delta_1+Delta_2 = 2d = sqrt(17)-1 > 3.
```

The same exact rank-three ledger closes every non-`K4` rank-three owner before
this step.  Thus equality in (0.1) is DNN-closed and the strict residual is
literally `K4+D+D`, not a packet-label interpretation of a different physical
graph.

## 1. Independently pinned analytic inputs

The universal topology proof uses only the following estimates.

1. **Induced superadditivity.**  For every original-vertex partition
   `V(G)=dot_union_i V_i`,

   ```text
   sigma(G) >= sum_i sigma(G[V_i]).
   ```

2. **Trees.**  Every nonempty tree `T` has `sigma(T)=-1`.

3. **Fixed connected ranks.**  For a finite simple connected graph `H`,

   ```text
   beta(H)=2  => sigma(H)>0,
   beta(H)=3  => sigma(H)>=0,
   beta(H)=4  => sigma(H)>=0.
   ```

4. **Triangular unicycle.**  If the unique positive block of connected `H` is
   a literal triangle (arbitrary bridge trees allowed), then `sigma(H)>0`.

5. **Rooted literal K4.**  If the unique positive block of connected `H` is a
   literal `K4` (arbitrary bridge trees allowed), then

   ```text
   sigma(H)>2.
   ```

No rank-one side is assumed nonnegative.  The only rank-one induced side that
will occur is reconstructed explicitly as a triangular unicycle and receives
item 4.  The strictness in the final worst-case ledger comes from item 5.

On source snapshot `origin/main=98e0040c36fe2bf86c39148fa79cdae0319254d6`,
the exact source pins are:

| use | source | SHA-256 | location |
|---|---|---|---|
| induced superadditivity; connected rank 3; tree identity | `all-tricyclic-graphs/paper.tex` | `4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02` | lines 61–100 |
| connected rank 2 | `all-bicyclic-graphs/paper.tex` | `56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da` | lines 56–62 |
| connected rank 4 | `all-tetracyclic-graphs/paper.tex` | `70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f` | lines 65–71 |
| triangular block graphs; rooted literal `K4` | `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` | lines 394–450 |
| exact theta excess classification | `positive-square-energy/tricyclic-general/theta-cycle-dnn-reduction.md` | `b1e40ec3f9f4ba5ecaf1de44284c9fba63d65fc3da59023d05eab488087e7c71` | lines 7–31 |
| rank-seven debit rule and `R322` row | `positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md` | `3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5` | lines 57–86 and 96–122 |

The last ledger is a fail-closed reduction note, not by itself a global
rank-seven theorem.  Here it is used only to identify the displayed residual;
the proof below starts again from physical adjacency.

## 2. Physical block-cut reconstruction

Run an edge-stack Tarjan decomposition on `G`.  Include each physical bridge
edge as its own `K2` block node and build the full block-cut incidence tree
`T`.  Root `T` at the literal `K4` block node `B`.  The two diamond block nodes
are the only other marked positive nodes.

All ancestry, bridge selection, and ownership below refer to this physical
tree.  No input packet label supplies a route, owner, cut, or nesting
relation.

Cyclomatic rank is additive over the positive blocks in a block tree.  In
particular, deleting bridge edges leaves every positive block intact, and a
component containing `q` of the two diamonds and not `B` has rank exactly
`2q`.

## 3. Simultaneous first-bridge split

For each diamond `D_i`, inspect the unique `B`-to-`D_i` route in `T`.  If the
route contains a `K2` block, select the first such block encountered from
`B`.  Deduplicate the selections before deleting anything.

### Lemma 3.1 (first bridges are an antichain)

Distinct selected `K2` blocks are incomparable in the rooted incidence tree.

**Proof.**  If a selected bridge `e` were strictly above another selected
bridge `f`, then every route reaching `f`, including the route for which `f`
was selected, would encounter `e` first.  Thus `f` could not be the first
`K2` on that route.  This is a contradiction.  ∎

Delete the selected physical bridge edges simultaneously.  The resulting
original-vertex components are:

* one root component `R` containing `B`; and
* one complete away component `A_e` beyond each selected bridge `e`.

They are connected, pairwise disjoint, exhaustive, and induced when regarded
as `G` on their vertex sets.  Each selected bridge edge merely crosses two
parts.  Every other connector edge and vertex, every connector branch, every
later bridge, and every rooted payload remains in exactly one complete
component.  Moreover, any edge of `G` between two different components would
reconnect them after the selected edges were deleted; hence there is no such
edge other than a selected bridge.  Thus each component is exactly the graph
induced by its original-vertex set.

Every `A_e` contains at least one diamond.  Let `q_e` be the number of the two
original diamonds in it.  Because the selected bridges are an antichain,
`q_e` is either one or two and

```text
beta(A_e)=2q_e.
```

Hence the exact away receipts are

| physical away inventory | rank | authenticated floor |
|---|---:|---:|
| one intact diamond | 2 | `sigma(A_e)>0` |
| both intact diamonds behind one shared first bridge | 4 | `sigma(A_e)>=0` |

Thus every actual-bridge away component is nonnegative.  This is the
packet-specific bridge dispatch missing from the old generic hull-bridge
sentence.  In particular, no rank-one side and no potentially negative
unicycle is hidden here.

A diamond remains in `R` if and only if its route from `B` in `R` contains no
`K2` block.

## 4. The bridge-free root frontier

Let `M` be the set of diamonds retained in `R`.  Define the physical frontier

```text
F = {X in M : no other diamond of M lies strictly on the B-to-X route}.
```

Thus `F` is the ancestor-minimal antichain of retained diamonds.  Every
retained diamond is either in `F` or is below exactly one member of `F`.
Since there are only two diamonds, `|F|<=2`.

For `X in F`, let `c_X` be the articulation immediately upstream of `X` on
the rooted block-cut route.  There is no `K2` between `B` and `X`; if no other
diamond intervenes, the incidence route is literally `B-c_X-X`.

### Exact boundary-open territory

Work in the current root vertex set `U=V(R)`.  Delete only the five edges of
the intact diamond `X` from `G[U]` and compute the resulting components.  A
standard maximal-block property says that every such component meets `V(X)`
in exactly one vertex.  Indeed, an outside component meeting two vertices of
`X` would provide an outside ear between those vertices and would contradict
maximality of the biconnected block `X`.

For `x in V(X)`, let `C_x` be the component meeting `X` at `x`, and put

```text
W_X = union_{x in V(X)\{c_X}} V(C_x).                     (4.1)
```

The induced graph charged is always `G[W_X]`; (4.1) is an ownership rule, not
a noninduced edge deletion in the final partition.  It consists of `X-c_X`
and every complete descendant owner attached through a vertex other than
`c_X`.  The cut `c_X` stays upstream exactly once.

Because a diamond is 2-connected, `X-c_X` is connected.  It joins all the
components in (4.1), so `G[W_X]` is nonempty and connected.  Frontier nodes
are an antichain, hence the `W_X` are pairwise disjoint.  Define

```text
C = V(R) \ dot_union_{X in F} W_X.                        (4.2)
```

Then `G[C]` is connected and contains `B`: in the rooted incidence tree,
removing every strict descendant branch through `X-c_X` leaves the connected
root-side subtree containing `B`, while any tree branch incident at `c_X`
remains there.  The sets in (4.2) are induced, disjoint, and exhaustive in
`R`.  All deeper diamonds and all path remnants follow the unique first
frontier owner.  A nested diamond is therefore not opened a second time.

## 5. Exact ranks of the opened diamond territories

The entry orbit matters, so it is reconstructed from the degree inside the
literal diamond, not from total graph degree.  A diamond has two degree-three
terminals and two degree-two internal vertices.  Set

```text
delta_X = 0  if c_X has degree 3 inside X,
delta_X = 1  if c_X has degree 2 inside X.
```

Direct inspection gives

```text
X-c_X is a three-vertex tree when delta_X=0,
X-c_X is a literal triangle when delta_X=1.               (5.1)
```

Let `eta_X` be the number of the other retained diamonds strictly below `X`.
Here `eta_X` is zero or one.  All descendant diamonds are intact in `W_X` and
all remaining material is acyclic, so block-rank additivity and (5.1) give the
exact formula

```text
beta(G[W_X]) = delta_X + 2 eta_X.                          (5.2)
```

The complete receipt table is therefore:

| `delta_X` | `eta_X` | physical content/rank | authenticated credit |
|---:|---:|---|---:|
| 0 | 0 | nonempty tree, rank 0 | `sigma=-1` exactly |
| 1 | 0 | one literal triangle plus bridge trees, rank 1 | `sigma>0` |
| 0 | 1 | one intact descendant diamond plus tree material, rank 2 | `sigma>0` |
| 1 | 1 | residual triangle plus intact descendant diamond, rank 3 | `sigma>=0` |

This table handles both cut orbits of the outer diamond in a nested pair.  It
does not infer a rank from a packet label or assume all rank-one graphs are
nonnegative.

After every frontier territory is removed, `G[C]` has the full literal `K4`
`B` as its unique positive block.  Every other retained edge belongs to a
bridge tree.  Therefore

```text
sigma(G[C]) > 2.                                          (5.3)
```

## 6. Exact strict ledger

Let

```text
t = |{X in F : delta_X=0 and eta_X=0}|.
```

By the table in §5, these and only these frontier territories can be negative,
and each has the exact value `-1`.  Thus `0<=t<=|F|<=2`.  Every first-bridge
away component is nonnegative by §3; every other frontier territory is
nonnegative by §5; and the anchor is strict by (5.3).

The final sets

```text
C,  {W_X : X in F},  {A_e : e selected first bridge}
```

form one original-vertex, induced, connected, pairwise disjoint, exhaustive
partition of `G`.  Induced superadditivity gives the exact integer ledger

```text
sigma(G)
 >= sigma(G[C]) + sum_X sigma(G[W_X]) + sum_e sigma(G[A_e])
 > 2 - t
 >= 0.
```

The first inequality may be weak, but the displayed conclusion is strict
because the rooted-`K4` receipt is strict.  Hence `sigma(G)>0`, proving the
theorem.

## 7. Exhaustion of hostile physical topologies

The following are not extra cases assumed by a fixture; they are consequences
of the rooted physical incidence tree.

1. **Shared first-bridge prefix.**  If both diamond routes begin
   `B ... e ...` and branch only after the same first `K2`, deduplication cuts
   `e` once.  One complete away component owns both diamonds, has recomputed
   rank four, and receives the rank-four nonnegative theorem.  Treating it as
   two rank-two packet-label sides would duplicate vertices.

2. **Separate first bridges.**  Two incomparable first bridges give two
   complete rank-two away components.  Their connector prefixes, branch
   vertices, and payloads are not suppressed.

3. **Bridge after an outer diamond.**  In a route
   `B-c-D1-...-e-...-D2`, the selected bridge for `D2` sends only its complete
   far component away.  `D1` remains in the root and is opened once.  The
   connector stump on the `D1` side follows its physical owner.

4. **Nested diamonds with no bridge.**  For
   `B-c-D1-x-D2` with `x!=c` in the incidence tree, the frontier is `{D1}`.
   Its single territory contains `D1-c`, the cut `x`, the intact `D2`, and all
   descendants.  Formula (5.2) gives rank two or three, so this side is
   nonnegative.  Opening `D2` separately would overlap the first territory and
   is forbidden.

5. **All three positive blocks share one articulation.**  If `B,D1,D2` are
   all incident with the same physical cut `c`, the two diamonds are siblings,
   not nested.  Both are frontier nodes; each side excludes `c`; and `c`
   belongs once to the `K4` anchor.  In the worst entry orbit both sides are
   trees and the strict ledger is `>2-1-1=0`.

6. **The diamonds share the upstream cut.**  A diamond meeting the other at
   its upstream cut is likewise a sibling in the block-cut tree.  It is nested
   only when its block node lies beyond a different cut of the first diamond.
   This distinction is recovered from adjacency and defeats a common
   label-based misclassification.

7. **Repeated cuts and branching.**  Any number of block nodes may be incident
   with the same articulation node.  Every opened side excludes its upstream
   cut; the retained component owns that original vertex once.  Unmarked tree
   branches at the cut remain upstream, while branches through another
   diamond vertex follow that diamond territory.

8. **K2-chain expansion and rooted-tree growth.**  Subdividing a selected
   bridge replaces it by a chain whose first physical edge is selected; all
   later new vertices remain in one away component.  Subdividing any other
   bridge or adding a rooted tree only adds rank-zero material to its existing
   physical owner.  No positive block, rank receipt, frontier relation, or
   debit changes.

These checks expose the two genuine counterexamples to a *naive proof*:
shared first-bridge prefixes invalidate one-side-per-label ownership, and a
nested pair invalidates opening both diamonds independently.  They do not
counterexample the theorem because the deduplicated antichain split and the
ancestor-minimal frontier group those vertices exactly once.

## 8. Relation to existing packet notes and implementation gate

The sentence for `R322` in
`nested-induced-piece-packet-theorem.md` is only a bridge-free two-debit
template and its persisted verifier is a Boolean typed-manifest check.  The
generic hull-bridge reduction preceding that template was later correctly
marked open because a rank-one away side can be negative.  Neither that
sentence nor the manifest is cited as a universal physical theorem here.  The
present proof repairs exactly the missing physical lane: an `R322`
first-bridge away side contains one or two intact diamonds and therefore has
rank two or four, never rank one.

Likewise, `two-debit-induced-piece-theorem.md` supplies an abstract arithmetic
rule only after induced ownership and actual-bridge dispatch have already been
proved.  It does not reconstruct the full physical `R322` adjacency.  Sections
2–6 above establish those obligations directly.

The companion adjacency-only semantic verifier reconstructs the physical
inventory, split, frontier, ownership, exact ranks, and integer ledger from
finite input adjacency while authenticating the pinned source bytes.  Its
fixture suite is finite corroboration and a fail-closed implementation gate;
it does not replace the universal proof.  No conclusion for any other packet
or for the global rank-seven theorem follows.
