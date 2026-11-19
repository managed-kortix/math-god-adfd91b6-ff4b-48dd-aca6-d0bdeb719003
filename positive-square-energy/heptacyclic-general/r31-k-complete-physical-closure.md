# R31-K residual lane: authenticated physical sublane and fail-closed boundary

## Status, exact scope, and nonclaim

Status: **NONPROMOTIONAL R31-K PROOF NOTE**.  This note treats one residual
lane only.  It does not update a master, `STATE.md`, or a publication ledger.
It does **not** prove the connected rank-seven theorem, the full multiblock
theorem, or any statement outside the `R31-K` family.  Those global programs
remain open because other residual lanes still need physical bridge dispatches
(and the separate single-block program is not part of this note).  The
first-bridge hypothesis in the theorem below is explicit; consequently this is
an authenticated R31-K **sublane**, not a claim that every graph sharing only
the three cycle-length profiles is closed.

For a graph `X`, put

```text
sigma(X)=s+(X)-|V(X)|.
```

**Theorem (R31-K only).**  Let `G` be a finite simple connected graph of
cyclomatic rank seven.  Suppose its positive-rank maximal
vertex-biconnected blocks are one literal `K4` and four literal cycles, and
suppose this row survives the exact `R31-K` DNN test

```text
sum_(four cycles Q) epsilon(Q)>3,

epsilon(C_l)=0                         (l even),
epsilon(C_l)=l tan^2(pi/(2l))          (l odd).
```

Arbitrary shared cuts, physical bridge connectors of arbitrary positive
length, nested or repeated cuts, and arbitrary finite rooted-tree attachments
are allowed.  In a first-bridge realization, require (as in the accepted
physical reduction) that the root first-bridge component contain a triangle
directly shared-cut reachable from the `K4`; the verifier rejects the graph
rather than infer this condition from the profile.  Then

```text
sigma(G)>0.
```

The theorem concerns an actual unsubdivided `K4` block.  It does not silently
replace a subdivided `K4` kernel by `K4`.

## 1. Exact residual profiles

The sharp cycle facts are

```text
epsilon(C3)=1,
epsilon(C5)=5-2sqrt(5),
epsilon(C_l) strictly decreases through odd l>=3,
epsilon(C_l)=0 for even l.
```

Moreover

```text
3(5-2sqrt(5))<2,
(5-2sqrt(5))+epsilon(C7)<1.
```

These are the cycle arithmetic used by the exact rank-seven debit ledger.
Sort the four cycle lengths.  If an even cycle occurs, its zero contribution
leaves total excess at most three, so the strict residual test fails.  If all
four are odd, let `h` be the number of nontriangles.

* `h=0` gives `T4`, i.e. four triangles.
* `h=1` gives `T3+odd>=5`.
* `h=2` can exceed three only when both nontriangles are pentagons: if one is
  at least seven, its excess plus the pentagon excess is below one.  This is
  `T2+C5+C5`.
* If `h>=3`, the total is at most
  `1+3(5-2sqrt(5))<3` (and decreases when `h=4`).

Thus the adjacency-derived residual profiles are exactly

```text
T4,              T3+odd>=5,              T2+C5+C5.       (1)
```

In particular every physical residual contains at least two triangles.  No
profile name or threshold is accepted from a case record by the verifier.

## 2. Analytic packet contracts

Only the following previously proved estimates are used.

1. **Induced superadditivity.**  For disjoint vertex sets `V_i`,
   `s+(G)>=sum_i s+(G[V_i])`.
2. **Rooted actual `K4`.**  A territory whose unique positive-rank block is
   the actual `K4`, with arbitrary one-root trees, has `sigma>2`.
3. **Shared-cut actual `K4+T`.**  A bridge-free shared-cut packet consisting
   of the actual `K4` and one triangle, with arbitrary one-root tree material,
   has `sigma>3`.  This estimate is not applied across a positive connector
   or through an intermediate cycle.
4. **Boundary territories.**  A nonempty tree has `sigma=-1`; an intact
   unicyclic territory has `sigma>-1`; and a connected graph of cyclomatic
   rank two through six has `sigma>=0`.  The last contract is used only on
   adjacency-authenticated side ranks in that range, never on rank one or
   seven.

The executable uses the fixed semantic IDs

```text
R31K-INDUCED-SUPERADD-v1
R31K-K4-ROOTED-v1
R31K-K4-T-SHARED-v1
R31K-UNICYCLIC-LOWER-v1
R31K-CONNECTED-RANK2-6-v1
R31K-RESIDUAL-SIEVE-v1
```

and no caller-supplied numeric bound.  Their exact source paths and SHA-256
pins are listed in Section 7 and enforced by the verifier.

## 3. Original-vertex ownership

Let `B` be the actual `K4`.  Run Tarjan on `G`; singleton edge blocks are the
physical bridges.  The full block--cut graph, including all bridge-block nodes
and articulation nodes, is a tree.  Root it at the block node `B`.

All cuts below are made on original adjacency and produce original vertex
sets before any credit is charged.

* **First bridge.**  On each root-to-cycle route containing a bridge block,
  choose the first bridge.  The distinct chosen bridges form an antichain.
  Delete their physical edges simultaneously.  Their complete away
  components and the one root component are connected, induced, pairwise
  disjoint, and exhaustive.  A later bridge, connector remnant, nested cycle,
  or rooted payload stays in its first away component.
* **Shared boundary.**  If a cycle `Q` is opened at its upstream articulation
  `c`, delete `E(Q)`.  Maximality of the block implies that each component of
  `G-E(Q)` meets `Q` in exactly one vertex: two contacts would furnish an open
  ear and enlarge the biconnected block.  Keep the owner component at `c`
  upstream and put the owner components at `V(Q)-{c}` downstream.  The
  downstream set is connected through `Q-c`, induced, and does not copy `c`.
* **Nesting.**  A complete first-boundary side is never opened a second time
  merely because it contains another demand.  Hence an intermediate cut is
  owned once, long connector vertices stay together with one side, and a
  repeated physical cut is never duplicated.
* **Remaining rank-zero material.**  Each off-hull component has one first
  physical root in the block--cut tree.  It follows that owner.  This covers
  arbitrary finite rooted trees, not a bounded list of decorations.

These facts establish connectedness, inducedness, disjointness, exhaustive
union, and unique articulation/payload ownership for every partition used
below.

## 4. First-bridge cascade

Perform the simultaneous first-bridge split of Section 3.  In the presently
proved R31-K bridge sublane, the root component contains a triangle directly
reachable from `B` with no intermediate positive block.  Retain the cut-closed
actual `K4+T` packet `A`.  Every other component at its first boundary is kept
complete.  There are at most three such territories, each with credit at least
`-1`; nested cycles are one territory, not several charges.  Therefore

```text
sigma(G) > 3-1-1-1 = 0.                              (2)
```

This is packet-specific.  It does not assert that every positive-rank side of
an arbitrary rank-seven bridge has nonnegative credit; an isolated `C5` side
can have negative credit.  In particular, adjacency realizations in which all
four cycles sit in four separate first-bridge away components are deliberately
rejected by the verifier.  Thus this artifact does not encode the asserted
independent acceptance as a trusted flag: it requires the direct root triangle
from adjacency before making the first-bridge charge.  Without that condition,
the bare `K4` margin `>2` cannot pay four arbitrary rank-one sides.  This
fail-closed boundary is also listed in Section 8.

## 5. First-nontriangle cascade

Assume the cyclic hull has no physical bridge.  If a triangle is directly
reachable from `B` without an intermediate positive block, Section 6 applies.
Otherwise the first positive block on every `B`-to-triangle route is a
nontriangle.  Select every distinct first such nontriangle.  These block nodes
form an antichain in the rooted block--cut tree.  Boundary-open each once at
its upstream port.

Every complete downstream side contains at least one intact triangle in
addition to the opened nontriangle remnant.  In profile `T3+odd>=5` there is
only one nontriangle.  In profile `T2+C5+C5`, distinct first pentagons give
two disjoint sides, each with an intact triangle; if one pentagon is nested
behind the other, only the first is opened and the whole nested side remains
one territory.  Consequently every downstream territory is a cactus of rank
at least two after the opening and has positive credit.  The retained root
territory has the actual `K4` and only one-root tree material, hence credit
`>2`.  Therefore

```text
sigma(G)>2+sum_(downstream S) sigma(S)>0.               (4)
```

This is the **first-nontriangle cascade**.  It prevents the invalid operation
of calling a triangle beyond a pentagon part of a narrow shared `K4+T` packet.

## 6. The `K4+kT` core

It remains that a triangle `T` is directly reachable from `B` in the
bridge-free block--cut tree.  There is no bridge block and no positive block
inside the `B`--`T` route, so the two blocks meet at one physical articulation.
Take their cut closure, together with all rank-zero material whose first owner
is `B` or `T`, as the anchor `A`.  This is exactly the shared actual `K4+T`
contract, not a string profile, and

```text
sigma(A)>3.                                              (5)
```

Delete `V(A)` and take the connected components of the induced complement.
They are precisely the complete first-boundary territories of the other three
cycle demands.  A common cut gives three cycle-minus-cut trees; repeated cuts
still give three disjoint original-vertex sides because the common cut stays
in `A`; nesting coalesces several demands into one component and cannot
increase the number of charges.  Long connectors and every rooted payload
remain with their unique component.  Hence there are at most three pieces,
each with credit at least `-1`, and

```text
sigma(G)>=sigma(A)+sum_i sigma(S_i)>3-3=0.              (6)
```

This is the advertised `K4+kT` core argument (`k>=1` at selection time): one
actual triangle is retained with `K4`; any further triangles are either in a
complete boundary territory or nested in a higher-rank strict territory.
Equations (2), (4), and (6) exhaust the accepted physical first-bridge,
first-nontriangle, and direct-core branches for all profiles in (1), proving
the stated R31-K theorem in its explicit direct-root-triangle bridge scope.

## 7. Quotient/expansion invariance and authentication

The verifier suppresses nothing when deciding acceptance: it reconstructs
every physical K2 bridge and every original vertex.  Its finite generated
suite is only branch authentication.  Arbitrary size follows from these two
invariance lemmas.

**K2-chain expansion.**  Subdividing a physical bridge replaces one bridge
block by a path of bridge blocks and degree-two routing cuts in the full
block--cut tree.  It creates no positive block and changes no cyclic order or
port.  On any root-to-demand route the first new bridge is selected; all later
inserted vertices lie in that same complete away component.  Thus the derived
profile, dispatch, piece ranks, and credit contract are unchanged.

**Rooted-tree expansion.**  Adding a finite one-root tree adds rank-zero leaf
blocks below one existing physical owner.  Removing a leaf returns the smaller
instance without changing any positive block, first bridge, first
nontriangle, or boundary port.  Induction on the number of tree edges assigns
every added vertex to the owner's piece and preserves connectedness and
inducedness.

Together these prove invariance under arbitrary connector lengths, arbitrary
finite rooted payloads, and arbitrary nesting depth.  Repeated cuts and
positive-block nesting are retained in the unsuppressed block--cut tree, so no
extra extrapolation is involved.

The executable artifact is

```text
research/r31-k-adjacency-semantic-verifier.py
```

Its analytic pins are:

| contract use | source | SHA-256 |
|---|---|---|
| induced superadditivity; rooted `K4` packet | `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` |
| shared-cut actual `K4+T` packet | `positive-square-energy/hexacyclic-general/multiblock-items5-7-owner-exact-closure.md` | `1c5722565e874ebf04533e908c5bf335f7be0b56a5665f5b607cfdef14ac8c67` |
| rooted hostile unicycle lower bound | `all-tricyclic-cacti/paper.tex` | `d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8` |
| connected rank-two-through-six nonnegativity used on authenticated side ranks | `positive-square-energy/heptacyclic-general/complete-multiblock-theorem.md` | `27c6a4736125d821f21fd1ebc7a30580068535826c8fcc6f72ea172cbb6a7399` |
| exact `R31-K` residual sieve | `positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md` | `3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5` |

Run

```text
python3 research/r31-k-adjacency-semantic-verifier.py
python3 -O research/r31-k-adjacency-semantic-verifier.py
```

The program accepts adjacency only; reruns Tarjan; authenticates exact block
types, full block--cut topology, bridges, ports, profile, dispatch, and the
original-vertex partition; checks fixed contract IDs; independently generates
fixtures for all three profiles and all dispatch branches; exercises long
connectors, nesting, repeated cuts, and rooted payloads; rejects hostile
rewires; and requires normal/optimized output to be byte-identical.

## 8. Promotion boundary

Passing this gate authenticates only the physical `R31-K` residual lane in the
scope above.  A graph with four independently bridge-separated cycle demands
and no root-side triangle is rejected: neither the `>2` rooted-`K4` contract
nor any source pinned here pays four rank-one losses.  Therefore a parent
master may promote R31-K only if its upstream physical reduction proves the
direct-root-triangle condition used in Section 4, or if a stronger analytic
packet is separately proved and pinned.  This is the residual promotion
blocker exposed by the fail-closed gate, not a counterexample to the spectral
inequality.

The other global rank-seven bridge lanes and the single-block program also lie
outside this artifact and remain open.  No global theorem is claimed.
