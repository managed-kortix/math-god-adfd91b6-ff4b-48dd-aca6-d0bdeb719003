# Physical `R21` first-`K2` quotient and exact residual (nonpromotional)

## Status and scope

Status: **NONPROMOTIONAL_R21_PARTIAL**.  This packet-local note repairs the
actual-bridge reduction for the `R21` block-rank partition `2+1^5` and closes
the physically typed `D+T^4+C5` row in the exact scope below.  It deliberately
returns the arbitrary-`r` bridge-free `Theta(1,2,r)+T^5` endpoint as **OPEN**.
It does not edit a master/STATE/closed-key ledger, prove another packet, or
promote the full heptacyclic theorem.

For a graph `X`, write

```text
sigma(X)=s^+(X)-|V(X)|.
```

The exact adjacency typing gate
`research/r21-literal-cycle-typing-verifier.py`, cherry-picked from commit
`8c7f2409ea4e4ab5f8f5d19b1124cee8d47f0337`, reconstructs physical blocks
before reading symbolic labels.  Together with the exact DNN sieve it leaves
precisely two physical `R21` families:

```text
Theta(1,2,r)+T^5,                  r>=2,
D+T^4+P,                           D=Theta(1,2,2), P=C5.
```

Every displayed `T` is a literal `C3`.  The typing gate's `q=3` adjacency
fixture authenticates only the literal `r=2` graph `D+T^5`; it proves no packet
and does **not** type or close arbitrary `Theta(1,2,r)`.  Its `q=5` fixture is
the unique nontriangle survivor and authenticates `P=C5`.  Equality in the
DNN predicate is already closed; no other cycle typing enters this note.

## Authenticated inputs

The verifier pins the exact source bytes supporting the following inputs.

1. Every connected graph of cyclomatic rank two is strict positive; connected
   graphs of ranks three through six have nonnegative credit.  Arbitrary
   rooted-tree attachments are included.
2. A connected cactus containing a triangle, with all other cyclic blocks
   triangles and optionally one `C5`, has positive credit, uniformly over
   arbitrary bridge connectors and rooted trees.  A territory containing only
   `P=C5` has credit greater than `-(sqrt(5)-2)>-1`.
3. In the narrow bridge-free shared-cut scope, with arbitrary one-root tree
   branches,

   ```text
   sigma(D)>1,   sigma(D+T)>2,   sigma(D+T+T)>3.
   ```

   In particular, this input excludes a hidden acyclic multi-interface router.
4. Induced square-energy superadditivity applies to vertex-disjoint induced
   territories.

The historical nested induced-piece note is **not** an authenticated input for
arbitrary-`r` theta ownership.  In particular, its R21 sentence and Boolean
verifier receipt do not reconstruct the maximal-block owner fibres or resolve
the `r=2` two-arm choice.

## 1. Simultaneous first-`K2` ownership

Let `H` be the minimal physical block-cut subtree spanning the displayed
cyclic block nodes, rooted at the distinguished rank-two block `B` (`B=Theta`
or `B=D`).  A `K2` block in `H` is an actual bridge edge.  Let `C_0` be the
maximal connected `K2`-free cyclic cluster containing `B`.  Define `E_0` as
the **deduplicated root-boundary antichain**: the physical hull bridges with
one endpoint-side incident with `C_0` and the other pointing away from it.
Equivalently, these are the distinct first `K2` blocks on all root-to-external-
cycle routes.  If several routes share their first bridge, it occurs once.

The members of `E_0` are pairwise incomparable.  Delete only those physical
hull bridge edges simultaneously.  The residual component containing `B` is
the **root group**; every other component is the complete descendant side of
one member of `E_0`, an **away group**.  Later `K2` blocks stay inside their
away group.

This is an original-vertex partition, not just a block-label partition.
Deleting bridges partitions `V(G)` into connected components.  Each component
is induced: an omitted edge between two vertices of one component would still
join them, while an edge between distinct components would contradict that
these are components after deleting exactly the crossing bridges.  Hence the
groups are connected, vertex-disjoint, induced, and exhaustive.  Each bridge
endpoint remains on its own vertex side; every suppressed connector vertex,
off-hull rooted branch, and descendant follows its unique component.  A shared
cut is an ordinary vertex and is never copied.

At label level, the external labels are partitioned into a distinguished root
part and nonempty away parts.  Conversely, every such labelled set partition
is realized: realize each part by a shared-cut tree and attach each away tree
to `B` through one positive-length `K2`.  Therefore the coarse quotient is
exact.  It suppresses internal later-bridge topology only because the cited
territory estimates are uniform over arbitrary connectors.

With five external labels, adjoining a marker `R` for the root part identifies
these states with set partitions of six labelled objects.  Thus the exact
coarse census is

```text
sum_(S subset of [5]) Bell(5-|S|)=Bell(6)=203.
```

A `K2` means one physical edge.  A zero-length “bridge” is a shared cut and is
not a member of `E_0`.

## 2. The theta family: exact bridge reduction and open endpoint

For `Theta(1,2,r)+T^5`, every away group from the deduplicated root-boundary
antichain contains at least one triangle and is therefore a positive all-
triangle cactus.  If at least one root-boundary `K2` exists, the connected root
group contains the theta and `k` triangles, where `0<=k<=4`, and has rank
`2+k<=6`.  For `k=0` it is strict by the all-bicyclic theorem; for `1<=k<=4`
it is nonnegative by the completed rank-three-through-rank-six theorems.  One
strict-positive away group plus the nonnegative root group makes the full graph
strict.  This closes every theta state having an actual root-boundary bridge.

If there is no root-boundary bridge, all five external triangles remain in the
root (`k=5`) and the cyclic hull is bridge-free.  This rank-seven endpoint is
**OPEN** here.  Neither the literal typing gate (whose `q=3` fixture is only the
literal `r=2` diamond) nor the historical nested-packet Boolean establishes an
owner-exact theorem for arbitrary `r`.  The exact returned key is

```text
OPEN_THETA_BRIDGE_FREE = bridge-free Theta(1,2,r)+T^5, r>=2,
```

with arbitrary repeated/nested shared cuts and rooted-tree payloads.  No empty
residual or full-R21 closure is claimed.

## 3. A narrow `D+T^k` root lemma

**Lemma.**  Every narrow bridge-free shared-cut cluster `D+T^k`, with arbitrary
one-root tree branches and `0<=k<=4`, has `sigma>1`.

For `k=0,1,2`, use the three pinned bounds above.  Let `k=3` or `4`.  In the
rooted bipartite block-cut incidence tree, select two triangles whose minimal
subtree with `D` contains no other triangle block.  One way to do this is to
repeatedly prune a triangle leaf not needed for the final pair; equivalently,
choose a least-depth branching pair.  The finite selector verifier separately
authenticates the `k=4` case on all 307 canonical incidence skeletons.

Retain that connector-free `D+T+T` hull as an anchor.  At each component
boundary outside the anchor, keep the boundary cut in the anchor and take the
complete first-boundary side without that cut.  Nested omitted triangles stay
in the same complete side unless a later explicit opening is made.  There are
at most `k-2` such sides.  Each has credit at least `-1`: it is a nonempty tree
if all its cycles are opened, greater than `-1` if unicyclic, and nonnegative
at rank at least two.  The boundary-cut convention gives connected induced,
disjoint, exhaustive territories on the original vertices.  Therefore

```text
sigma(D+T^k)>3-(k-2),
```

which is `>2` for `k=3` and `>1` for `k=4`.  No monotonicity under adding a
triangle is assumed.

## 4. The diamond family when `P` is away

Every away group containing at least one `T` (with or without `P`) is positive.
There is at most one `P`-only away group, and it has credit greater than `-1`.
The root group is a narrow bridge-free `D+T^t` cluster for some `0<=t<=4`, so
Section 3 gives credit greater than one.  Hence it pays a possible `P`-only
away group strictly; every other away group adds positive credit.

If `P` belongs to a triangle-containing away group, no negative away group
exists and the same root bound is more than enough.

## 5. The diamond family when `P` is retained

Work now in the residual `D`-component after deleting `E_0`; its cyclic hull
is bridge-free.  Root its block-cut incidence tree at `D`.  Since `P` is not
the root block, its block node has a unique parent cut node, represented by a
unique physical vertex `c in V(P)`.

Delete the five edges of `P`, retaining all vertices.  For each `v in V(P)`,
let `F_v` be the component of `G-E(P)` containing `v`.  These five owner
classes are well-defined and partition the vertices of the root group.  Every
component meets `P` by stopping a shortest path at its first pentagon vertex.
No component can meet two distinct pentagon vertices: a path between them,
together with a pentagon arc, would enlarge the 2-connected block `P`.

Keep **all** of `F_c` upstream, including every sibling block sharing `c`,
every payload rooted at `c`, and the unique route to `D`.  Put the residual
`P`-side subtree minus `c` downstream: the other four pentagon vertices and
all four owner classes `F_v` (`v!=c`):

```text
A=G[V(F_c)],
B=G[ union_(v!=c) V(F_v) ].
```

Here the notation is within the already isolated root group.  `A` is connected
and contains `D`.  `B` is connected because `P-c` is a four-vertex path
joining its four owner classes.  Both are induced by definition.  Their vertex
sets are disjoint and exhaustive.  The only crossing edges are the two
pentagon edges incident with `c`; no parent cut or descendant is duplicated.
A triangle follows the unique `F_v` containing its block: a triangle at `c`
stays upstream, while one owned at `v!=c` moves downstream.  This is the
required original-vertex lift of the quotient ownership rule.

Let `r` be the number of root triangles in `B`, and let `t` be the number in
the root group before opening `P`.  Then `A` is a narrow `D+T^(t-r)` packet and
has credit greater than one by Section 3.  If `r=0`, `B` is a nonempty tree
(the path `P-c` with one-root tree branches), so `sigma(B)=-1`.  If `r>=1`,
`B` is a cactus containing a triangle and optionally only acyclic remnants of
`P`, so it has positive credit.  Thus

```text
sigma(A)+sigma(B)>0.
```

All first-`K2` away groups remain disjoint from `A union B`; triangle-containing
ones are positive.  A `P`-only away group cannot coexist with retained `P`.
This closes every retained-`P` state.

The tempting phrase “`P-c` plus descendants is a tree” is false when triangles
exit through nonparent pentagon vertices.  The exact statement is: it is a tree
only when `r=0`, and otherwise it is a positive triangular cactus.  The owner
classes above are essential.

## 6. Fine finite quotient

For a root part containing `D`, `k` labelled triangles, and a bit `p` recording
whether `P` is retained, let `N(k,p)` be the number of rooted colour-preserving
isomorphism classes of its bridge-free incidence skeleton.  For `m=1+k+p`
block nodes and `c` indistinguishable cut nodes, enumerate every connected
`(m+c-1)`-edge subset of `K_(m,c)` subject to

```text
cut degree >=2,
deg(D)<=4, deg(T_i)<=3, deg(P)<=5.
```

Since a connected graph with `|V|-1` edges is a tree, this is complete.  Since
the sum of cut degrees is `m+c-1` and every cut has degree at least two,
`c<=m-1`; hence the search is finite.  Rooted AHU coding, with unique colours
for labelled cyclic blocks and one common cut colour, quotients exactly the
cut-node relabellings.

The exact arrays are

```text
N(k,0) = [1, 1, 4, 29, 307],
N(k,1) = [1, 4, 29, 308, 4322],       k=0,...,4.
```

The one-state difference `N(3,1)-N(4,0)=1` is the degree-four `P`-centred
incidence star, permitted by the pentagon's five physical ports but forbidden
at a triangle.  It is not a relabelling accident.

Choose which `k` of the four labelled triangles are in the root, choose `p`,
and partition the remaining `5-k-p` labels into away groups.  The fine census
is therefore

```text
sum_(k=0)^4 sum_(p=0)^1 binom(4,k) N(k,p) Bell(5-k-p)=6768.
```

Its ten row contributions `(k,p)` are

```text
52,15,60,80,120,348,232,1232,307,4322.
```

This fine quotient records the complete root incidence skeleton and the exact
coarse away grouping.  It intentionally does not enumerate cyclic-block port
assignments, off-hull payload shapes, bridge lengths beyond positivity, or
later bridges inside away groups: the proof never distinguishes them, and the
pinned packet bounds are uniform over precisely those data.

## 7. Exact conclusion and nonclaims

The physically typed `D+T^4+C5` row is closed under arbitrary shared cuts,
actual `K2` hull bridges, connector lengths, and rooted-tree attachments.  In
the theta row, every state with a nonempty root-boundary bridge antichain is
closed, but the bridge-free `Theta(1,2,r)+T^5` endpoint for arbitrary `r>=2`
is returned **OPEN**.  Therefore the status is `NONPROMOTIONAL_R21_PARTIAL`,
not `R21 closed`.

The coarse first-bridge quotient has 203 labelled states per five-label
family; the P-row root-incidence refinement has 6,768 states.  Ownership is
defined on original vertices before any credit is charged.

The verifier is fail-closed: it authenticates the literal P-row typing,
regenerates both censuses independently, checks quotient ownership invariants,
runs normal/optimized replay, rejects hostile mutations, and requires the open
theta residual verbatim.  It does not treat a Boolean or synthetic receipt as
an arbitrary-`r` packet proof.  No master, STATE, publication, or closed-key
artifact is modified.
