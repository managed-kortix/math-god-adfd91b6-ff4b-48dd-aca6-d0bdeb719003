# `R31-S`: physical shared-triangle structural closure

## Scope and notation

For a finite graph `X`, put

`sigma(X)=s+(X)-|V(X)|`,

where `s+(X)` is its positive square energy.  This note proves the physical
`R31-S` packet after the exact DNN sieve.  It is deliberately independent of
the historical labels `C4` and `D3`: those labels came from a rooted-record
classifier, not from the biconnected topology of the induced sides.

The physical input is a finite simple connected graph `G` of cyclomatic rank
seven whose positive-rank maximal vertex-biconnected blocks are exactly

* one rank-three doubled-`C4` block `B`; and
* four external triangle blocks.

Here `B` is the actual maximal vertex-biconnected physical block, not merely a
chosen kernel subgraph, and the four external `K3` blocks are all the other
positive-rank maximal blocks of `G`.

Write the four branch vertices of `B` cyclically as `A,B,C,D`.  Its doubled
fibres join `A` to `B` and `C` to `D`, while its single connectors join `B` to
`C` and `D` to `A`.  The doubled members are in the first-simple exceptional
orbit: each doubled fibre consists of paths of lengths one and two.  The two
single connector paths have opposite parity.  Call the even connector `E` and
the odd connector `O`; `Int(E)` is nonempty.  Their lengths are otherwise
arbitrary positive integers of the prescribed parity.  Arbitrary finite rooted
trees, repeated owners, multiway cuts, and nested triangle incidences are
allowed.

The theorem below is the structural disposition of this physical input.  The
other `R31-S` rows—non-first-simple doubled members and nonexceptional parity
rows—remain owned by the exact DNN/structural sieve that produces this input.

## A universal triangle-cluster lemma through rank four

A **shared-cut triangular cluster** is a connected cactus whose cyclic blocks
are triangles and whose triangle-intersection graph is connected; two triangle
nodes are adjacent exactly when their blocks share a cut vertex.  Arbitrary
finite trees may be attached at arbitrary vertices.

**Lemma 1 (universal small cluster).**  If `A_r` is a shared-cut triangular
cluster with `1<=r<=4` triangle blocks, then

`sigma(A_r)>r-1`.                                                (1)

This statement is about every such physical cluster.  It is not restricted to
the 28 records formerly labelled `C4`.

**Proof.**  For `r<=3`, the cycle-packing number is at most two: the only
possible exception would be three pairwise vertex-disjoint triangles when
`r=3`, but then their intersection graph would be disconnected.  Thus the
packing-two half-plane theorem gives

`D(A_r):=s+(A_r)-s-(A_r)>0`.

For `r=4` the same argument applies when the packing number is at most two.
Suppose instead that three triangle blocks `T1,T2,T3` are pairwise disjoint.
Connectivity of the triangle-intersection graph forces the fourth block `T0`
to meet all three: there is no other triangle through which any `Ti` could be
connected.  The three intersection vertices on `T0` are distinct, since a
coincidence would make the corresponding two petals meet.  Hence the only
packing-three incidence is a central triangle with three pairwise disjoint
petals, one at each central vertex.  This classification includes repeated or
multiway cuts: a shared cut involving two petals would contradict their
pairwise disjointness.

For `t>0`, let `Z_J(t)` be the signless matching polynomial and put

`F=A_4-(V(T1) union V(T2) union V(T3))`.

The only odd-cardinality collections of pairwise vertex-disjoint cycles are
the four singleton triangles and the collection of all three petals.  The
grouped Sachs expansion therefore gives

`Im Psi_(A_4)(t)=-2 sum_(j=0)^3 Z_(A_4-Tj)(t)+8 Z_F(t)`.         (2)

Deleting `T0` leaves the three independent private petal edges.  They are
pairwise disjoint and disjoint from `F`.  Given any matching counted by
`Z_F(t)`, adjoin an arbitrary subset of those three edges.  This is a
weight-preserving injection and gives the exact bound

`Z_(A_4-T0)(t)>=(1+t^2)^3 Z_F(t)>Z_F(t)`.                       (3)

For `i in {1,2,3}`, let `H_i` be the subgraph induced by

`U-V(Ti)`, where `U=V(T1) union V(T2) union V(T3)`.

It is a six-vertex core with a perfect matching: use the central edge opposite
`Ti` and the private edge in each of the other two petals.  Hence
`Z_(H_i)(t)>1` for every `t>0` (the perfect matching supplies a constant term
and the empty matching supplies the positive term `t^6`).  Taking the union of
a matching of `H_i` and a matching of `F` gives a weight-preserving product
injection, and therefore

`Z_(A_4-Ti)(t)>=Z_(H_i)(t)Z_F(t)>Z_F(t)` for `i=1,2,3`.          (4)

Additional edges from the displayed subgraphs to arbitrary one-root forests
are simply ignored; they cannot destroy an injected matching.  Thus no forest
elimination or monotonicity assertion is being used.  Equations (2)--(4) imply
`Im Psi_(A_4)(t)<0` for every `t>0`.  The continuous argument and signed
Coulson identity give `D(A_4)>0`.

We have proved `D(A_r)>0` in every case.  Since a connected cactus with `r`
cyclic blocks satisfies

`|E(A_r)|=|V(A_r)|+r-1`

and `s+(A_r)+s-(A_r)=2|E(A_r)|`, it follows that

`sigma(A_r)=r-1+D(A_r)/2>r-1`.

This proves (1).  QED.

## Physical owner fibres

For `x in V(B)`, define the **first-`B` owner fibre** `F_x` to be the vertex
set of the component containing `x` in `G-E(B)`, where only the edges of the
block `B` are deleted.

**Lemma 2 (owner fibres).**  Every component of `G-E(B)` meets `B` in exactly
one vertex.  Consequently the sets `F_x`, `x in V(B)`, partition `V(G)`;
each `G[F_x]` is connected and induced.  Moreover `G-F_x` is connected, and
if `F_x` contains no positive-rank maximal block, then `G[F_x]` is a nonempty
tree.

**Proof.**  A component meets `B` because `G` is connected.  Suppose a
component `K` met `B` in distinct vertices.  Take a path in `K` whose endpoints
`a,b` are two consecutive visits to `B` and whose internal vertices lie
outside `B`.  This is a nontrivial `B`-ear.  Two internally disjoint `a`--`b`
paths in the vertex-biconnected block `B`, together with that ear, lie in one
larger vertex-biconnected subgraph.  This contradicts the maximality of the
physical block `B`.  Hence every component meets `B` exactly once.  This
proves uniqueness, the partition, and induced connectedness.  Since `B` is
2-connected, `B-x` is connected; every other fibre stays attached at its
unique vertex of `B-x`, so `G-F_x` is connected.  Finally a connected fibre
with no positive-rank maximal block is acyclic and nonempty because it
contains `x`; hence it is a tree.  QED.

The complete fibre in Lemma 2 is the only object called an owner fibre below.
A boundary-open triangle territory is different: its entry cut remains on the
upstream side and is not part of the opened territory.

## The three-way physical disposition

Let the **cyclic hull** be the minimal block-cut subtree containing `B` and the
four external triangle blocks.

**Theorem 3 (physical `R31-S` closure).**  Every graph in the scope above
satisfies

`sigma(G)>0`.

More precisely, exactly the following structural dispatch is needed.

### Case A: an actual bridge lies in the cyclic hull

Root the full block--cut tree at `B` and orient an actual hull bridge away from
`B`.  Let `q` be the number of external triangle blocks on its away side.  By
definition of the cyclic hull, `1<=q<=4`.  That away side is a connected cactus
whose `q` positive-rank blocks are triangles; actual bridge blocks and arbitrary
rooted trees may occur between or beyond them.  The all-rank triangular-cactus
corollary therefore gives this side strictly positive credit.

The side containing `B` has rank

`3+(4-q)=7-q in {3,4,5,6}`.                               (A1)

It is connected and induced and hence has nonnegative credit by the completed
connected rank-three through rank-six theorems.  Induced square-energy
superadditivity closes the row strictly.  Notice that this is an oriented,
`R31-S`-specific argument.  It does **not** assert generic nonnegativity for an
arbitrary positive rank-one side; for example, a pentagon has negative credit.

Hence the residual may be assumed to have a bridge-free cyclic hull: all
successive positive blocks meet through shared cut vertices.

### Case B: a connector-interior fibre contains a triangle

Let

`I=Int(E) union Int(O)`.

Suppose some `x in I` has `q>=1` external triangle blocks in its complete fibre
`F_x`, counting all nested descendants.  The induced graph `G[F_x]` is a
connected triangular block graph containing a triangle, with arbitrary rooted
trees, and hence

`sigma(G[F_x])>0`.                                              (5)

The connector-interior vertex `x` has degree two in `B`.  Deleting it breaks
one connector but leaves its endpoints joined by the other connector and the
two doubled fibres.  Thus `B-x` is connected and has cyclomatic rank two.  The
induced complement is connected by Lemma 2 and has rank

`beta(G-F_x)=2+(4-q)=6-q in {2,3,4,5}`.                         (6)

The completed connected theorem through rank six gives
`sigma(G-F_x)>=0`.  Superadditivity with (5) closes the row strictly:

`sigma(G)>=sigma(G[F_x])+sigma(G-F_x)>0`.                       (7)

This dispatch applies to every internal vertex of **both** connectors.  One
must not strip a cyclic descendant from `F_x`, call the remainder a tree, and
continue; the whole graph is closed in this case.

### Case C: the bridge-free, connector-clean residual

Assume no `F_x`, `x in I`, contains a positive-rank block.

Root the full block-cut tree at `B` and choose an external triangle block `Q`
of maximum depth.  Let `c` be its parent cut.  Define `S` to be the complete
component beyond the oriented incidence `c--Q`, omitting `c`: equivalently,
take `Q-c`, all branches rooted at its two private vertices, and every further
descendant away from `c`.  Maximal depth ensures that no positive-rank block
lies below `Q`.  Therefore `G[S]` is a connected nonempty induced tree and

`sigma(S)=-1`.                                                  (8)

The cut `c`, every branch rooted at `c`, and every sibling block remain
upstream.  Thus `G-S` remains connected.  This is a boundary-open downstream
territory, **not** the complete owner fibre `F_c`.

Choose any `v in Int(E)` and put

`T=F_v`.

The connector-clean assumption and Lemma 2 make `G[T]` a connected nonempty
induced tree, so

`sigma(T)=-1`.                                                  (9)

The first `B`-owner of `Q` is not in `I`, for otherwise its fibre would contain
`Q` and Case B would apply.  Hence `S` lies in a fibre different from `T`; in
particular `S cap T` is empty.  Lemma 2 and the boundary construction show
that

`R=G-(S union T)`

is connected.  The two remnants of `E` remain in `R`, not in `T`.

Now choose any actual edge `e` of the odd connector `O`.  In `R`, the two
remnants of `E` end at `v` and hence no longer join its endpoint sides.  Thus
`O` is the sole route in `B-v` between the two doubled fibres.  No off-`B`
component supplies another route, by Lemma 2.  Therefore `e` is a bridge of
`R`.  Delete `e` only to identify its two vertex components and call their
induced subgraphs `U_0,U_1`.  We obtain an exact induced vertex partition

`V(G)=S disjoint union T disjoint union U_0 disjoint union U_1`. (10)

All connector remnants, rooted trees, and nested descendants follow their
unique first owner.  Edges across (10) are discarded only in applying induced
superadditivity; no edge-monotonicity claim is used.

Each first-simple doubled fibre is exactly

`A--B` together with `A--x--B`,

and hence is one physical triangle, not a diamond.  Each `U_i` contains one
such intrinsic triangle.  The three external triangles left after opening
`S` have first owners outside connector interiors.  They therefore lie on one
of the two intrinsic triangles (at a branch vertex or the unique interior of
a length-two doubled member), and every nested descendant stays on that same
side.

Each `U_i` is a cactus whose cyclic blocks are exactly its intrinsic triangle
and its assigned external triangles.  Indeed, after deleting `v` and cutting
`e`, the part of `B` on that side is the intrinsic triangle with connector
remnants attached at one root each.  Lemma 2 makes every off-`B` component a
one-root attachment, so it cannot create another route between vertices of
that triangle.  The only other positive-rank blocks are the external
triangles; everything else is a bridge or a rooted tree.

These triangle blocks form one shared-cut cluster.  Since Case A has been
excluded, the block-cut path from `B` to any top external triangle contains no
bridge block: that triangle shares its first-owner cut directly with `B`.
After the split, this owner lies on exactly one intrinsic triangle, so the top
triangle intersects that intrinsic triangle.  Every nested child triangle
shares its entry cut with its parent triangle.  Induction down each incidence
subtree therefore connects every assigned triangle to the intrinsic triangle
in the triangle-intersection graph.  Repeated owners merely give multiway
shared cuts, while forks and chains give branching and path incidence
subtrees.  Connector remnants are one-root paths and introduce no cyclic
block.  This proves both cactus structure and shared-cut connectedness for all
repeated and nested owner patterns; ordinary connectedness alone would not
have sufficed.

Let `k_i` be the number of retained external triangles in `U_i`, and put
`r_i=beta(U_i)`.  Then

`r_i=1+k_i>=1`, and `r_0+r_1=2+(k_0+k_1)=2+3=5`.                (11)

Thus the only possible ordered rank pairs are

`(1,4), (2,3), (3,2), (4,1)`.

Lemma 1 applies to both sides, including either rank-four side, and yields

`sigma(U_0)+sigma(U_1)`
`  > (r_0-1)+(r_1-1)=5-2=3`.                                  (12)

Using (8)--(10) and induced square-energy superadditivity,

`sigma(G)`
` >= sigma(S)+sigma(T)+sigma(U_0)+sigma(U_1)`
` > -1-1+3=1>0`.                                               (13)

Equivalently, for `H=G-S`, one first gets `sigma(H)>2`, not merely the
frontier target `sigma(H)>1`, and then `sigma(G)>1`.  The weak
superadditivity inequalities do not destroy strictness because the side input
(12) is strict while both tree charges are exact.  This proves Theorem 3.
QED.

## Verification contract

Run

```text
python3 research/r31-s-physical-parent-verifier.py
python3 -O research/r31-s-physical-parent-verifier.py
```

The executable starts from physical adjacency.  It reconstructs Tarjan edge
blocks, the unique rank-three block and four actual triangle blocks, the full
block--cut tree, the cyclic hull, complete first-`B` fibres, the deepest
boundary-open `S`, the complete even-connector fibre `T`, and the two components
`U,V` of an actual odd-connector bridge after `T` is opened.  It explicitly generates the 423 canonical no-hull-bridge four-triangle
parent incidences over the six clean physical owners, applies the deterministic
deepest-`Q` opening, and recomputes the 110 outputs and their preimage
multiplicities.  It then realizes every output on all eight physical anchors,
reruns Tarjan on those adjacencies, transports actual rooted-tree probes, and
checks arbitrary connector remnants.  Its hostile adjacency
fixtures force Case A and Case B before Case C and distinguish the rank formulas
`7-q` and `6-q`.

This theorem closes the physical `R31-S` packet.  It does not by itself repair
or certify generic hull-bridge sentences elsewhere in the rank-seven
multiblock reduction, and therefore is not a global `COMPLETE` receipt.

## Dependencies

The proof uses exactly the following established inputs.

1. The physical `R31-S` DNN/structural gate: outside the routed rows, `B` is a
   first-simple exceptional doubled-`C4` block and the other four positive
   blocks are triangles; the two connectors have opposite parity.
2. Maximal-block and block-cut-tree facts, including Lemma 2 and additivity of
   cyclomatic rank over positive-rank blocks.
3. Induced square-energy superadditivity and `sigma(tree)=-1` for every
   nonempty tree.
4. The completed connected nonnegativity theorem through cyclomatic rank six.
5. Positive credit for a connected triangular block graph containing a
   triangle (used in the two early dispatches).
6. The packing-two half-plane theorem, grouped Sachs expansion, continuous
   argument, and signed Coulson identity used in Lemma 1.  The exact
   packing-three matching injections are the ones proved in
   `packing-two-square-energy/paper.tex` (SHA-256
   `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791`), equations
   `central-deletion-bound` through `petal-deletion-bound`; the universal
   formulation here uses those injections directly rather than the narrower
   record statement in `r31-s-c4-marked-four-triangle-theorem.md`.

For exact comparison provenance, that narrower note has SHA-256
`78344337226ae5c5b42645dd563390eec9eb462824e78fd4e42d7fa54051309d`.
The proof above imports no 28-record scope restriction and no unsupported
common-forest-factor sentence from it.

No diamond determinant, `D3` phase inequality, switching-class quotient, or
historical 28-record `C4` restriction is a dependency.

## False steps excluded

The proof specifically does **not** make any of the following inferences.

* An interior owner of a length-two doubled member does not create
  `Theta(1,2,2)`: the physical fibre has one length-one and one length-two
  path, hence exactly one triangle.  There is no second internal vertex
  `z` and no edges `Az,Bz`.
* Bridge-free ordinary connectedness alone does not imply shared-cut
  connectedness.  The proof uses the actual block-cut path, unique first-owner
  fibres, and absence of bridge blocks in the cyclic hull.
* The boundary territory `S` is not `F_c`: `c` stays upstream.  By contrast
  `T=F_v` is a complete physical owner fibre.
* The tree status of `T` is not unconditional.  A connector fibre containing
  even one triangle is positive-rank; it is dispatched in Case B before `T` is
  charged as a tree.
* The two side ranks do not sum to four.  They sum to five because opening `S`
  and `T` removes two units from total rank seven, while cutting the bridge
  edge of `O` only separates the retained rank: `7-1-1=5`.
* The universal rank-four estimate is not inferred from the old `C4` label.
  It follows from the physical hypotheses in Lemma 1 and includes every former
  `D3` owner pattern.
* Strict `>3` in (12) must not be weakened to `>=3`; the two exact tree charges
  require the strict side margin to obtain (13).
