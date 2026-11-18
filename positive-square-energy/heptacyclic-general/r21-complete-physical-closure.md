# Complete physical closure of the rank partition `R21`

## Scope and theorem

Status: **NONPROMOTIONAL_AUTHENTICATED_PROOF_NOTE**.  The mathematics below is
a human-checkable packet proof; the accompanying strict executable-promotion
gate remains fail-closed at the four explicitly named universal analytic
replays.  Nothing here updates a master, STATE, or publication ledger.

For a graph `X`, write

```text
sigma(X)=s+(X)-|V(X)|.
```

Here and below a named packet estimate is applied to the **induced territory**
that contains the named cyclic blocks together with whatever tree material the
territory construction assigns to them. The notation `A_j`, `D+T^t`, and `P`
never means the bare cyclic core unless explicitly stated.

**Theorem.** Let `G` be a finite simple connected graph of cyclomatic rank
seven whose positive-rank maximal vertex-biconnected blocks have ranks
`2+1+1+1+1+1`. Suppose `G` is in one of the two exact residual families of
the DNN sieve:

```text
Theta(1,2,r)+T^5,                  r>=2,
D+T^4+P,                           D=Theta(1,2,2), P=C5.
```

Here every `T` is a literal triangle. Arbitrary block-cut incidence, actual
bridge connectors, legal subdivisions, and arbitrary finite rooted trees are
allowed. Then

```text
sigma(G)>0.
```

Thus both exact post-DNN residual families are strict.  At the target
`s^+(G)>=|V(G)|` (equivalently `sigma>=0`), the whole `R21` block partition is
closed: profiles on the DNN boundary may supply only `sigma>=0`, not a strict
surplus.  This theorem is packet-specific; it neither proves nor uses a generic
rank-seven hull-bridge theorem.

### Authentication and executable-promotion boundary

The accompanying strict gate authenticates this corrected note and replays the
adjacency parent, literal typing, exact `D+T+T` packet, and finite `D+4T`
selector.  The following four analytic proof kernels are each classified as
`rigorous_prose_authenticated_not_executable_universal_replay`, not as merely
asserted prose:

1. **Uniform triangular-cactus strictness:** every connected cactus in which
   every cyclic block is `C3` has `sigma>0`; arbitrary bridge connectors and
   arbitrary finite attached trees are allowed.  The proof is the maximum
   vertex-disjoint-cycle Voronoi partition followed by the packing-one Sachs
   sign theorem.
2. **Six-triangle margin:** every connected six-triangle cactus has `sigma>1`,
   including the exact shared-cluster floors `sigma(A_5)>2` and
   `sigma(A_6)>1`.  The proof uses the explicit `A_4>3`
   central-triangle/three-petal matching injection, incidence-leaf openings,
   and arbitrary-connector territories.
3. **Hostile one-root `C5` bound:** a unicyclic `C5` territory with arbitrary
   rooted trees has `sigma>=-(sqrt(5)-2)>-1`.  The proof uses rooted-tree
   elimination, weighted-cycle phase domination, and the bare `C5` spectrum.
4. **Rank-uniform nonunicyclic-cactus strictness:** every finite simple
   connected cactus of cyclomatic rank at least two has `sigma>0`, with
   arbitrary shared cuts, bridge connectors, cactus incidence, and finite tree
   attachments.  The proof is the exact rank-uniform sharp-DNN frontier plus
   the two exhaustive all-rank residual closures.

Absence of executable universal replays for these kernels is not a mathematical
disproof.  It does, however, leave the deliberately stronger strict
executable-promotion mode fail-closed.  Accordingly this note and gate are
nonpromotional.  The older `r21-full-physical-first-k2-quotient.md` and its
verifier remain historical/nonpromotional OPEN artifacts and are not closure
inputs.

The arbitrary-`r` theta family comes from an adjacency-level physical
classification, not from extrapolating the literal `r=2` fixture. A maximal
simple rank-two vertex-biconnected block has exactly two degree-three vertices
and all other block degrees two, hence is a subdivision of three internally
disjoint paths between the branch vertices. The parent gate reconstructs these
paths from the Tarjan block. The exact DNN calculation then proves

```text
Delta(a,b,c)>1 iff (a,b,c)=(1,2,r) after sorting, r>=2.
```

The parent gate checks the unit edge and the two remaining path lengths
directly and rejects every other theta (including `Theta(2,2,2)`).

The separate literal typing gate has narrower scope: its `q=3` fixture is only
`D+T^5` (`r=2`), while its `q=5` fixture authenticates `D+T^4+P`. No finite
fixture is extrapolated to arbitrary `r`.

## 1. Quantitative six-triangle cactus lemma

**Lemma.** If `H` is a connected cactus whose positive-rank maximal blocks are
exactly six triangles, with arbitrary bridge connectors and arbitrary attached
trees, then

```text
sigma(H)>1.                                             (1)
```

Partition the triangles into maximal shared-cut clusters. Contract every such
cluster to one marked node in the reduced cluster tree. The arbitrary-connector
territory lemma is the following elementary tree construction. In the physical
block-cut tree, begin with pairwise disjoint connected **expanded incidence
subtrees**: each source contains the full block/cut incidence subtree of its
named cyclic cluster, not merely a contracted marked block node. Contract each
expanded labelled subtree. Assign every remaining unlabelled tree node to one
label by multi-source breadth-first search, with a fixed tie-break by label.
Along the unique path from an assigned node to its chosen source, the distance
to that source decreases, so every label class is connected. Cut only tree
edges whose endpoints have different labels. Translating those cuts back to
the physical graph cuts actual bridge blocks between classes, never a shared
cut vertex. Thus each physical cut vertex, connector vertex, and rooted branch
is assigned exactly once. This construction produces
connected induced, vertex-disjoint, exhaustive territories and assigns every
connector remnant, Steiner branch, entry vertex, and off-hull tree exactly
once. In particular, we do not cut every bridge incident with a chosen path;
that could isolate an uncharged acyclic Steiner territory.

For an induced territory whose cyclic blocks form one shared-cut cluster
`A_j` of `j<=6` triangles, with arbitrary trees assigned wholly to their unique
attachment vertices, the established strict floors are

```text
j                 1    2    3    4    5    6
sigma(A_j) >      0    1    2    3    2    1.           (2)
```

The values through four are the favorable-cycle and exact four-triangle
packets. The values for five and six follow from one and two incidence-leaf
openings from `A_4`, each opening charging exactly one nonempty tree of credit
`-1`. These are piecewise floors; no claim `sigma(A_j)>j-1` is made for
`j=5,6`.

If some maximal shared-cut cluster has size at least two, make every cluster a
labelled subtree and apply the construction above. The selected territory has
exactly that cluster as its cyclic blocks, so it has credit `>1` by (2); every
other resulting territory is a connected triangular block graph and has credit
`>0`. Hence (1) follows by induced superadditivity.

If all six clusters are singletons, choose two marked nodes at minimum distance
in the reduced cluster tree. Their unique path has no other marked node. Use
the whole reduced-tree path, including its connector nodes, as one labelled
subtree and the other four marks as singleton labelled subtrees. Applying the
construction above yields one connected induced arbitrary-connector bicyclic
cactus with exactly two triangular blocks and four other triangular
territories. The two-triangle territory has credit `>1`, and each other
territory has credit `>0`. Again (1) follows. Every off-hull tree follows its
unique attachment; it is not globally assigned to the two-triangle piece.

## 2. Uniform theta owner-fibre theorem

Assume the first residual family. Write the maximal theta block as three paths

```text
xy,     x-a-y,     Q,
```

where `Q` has length `r`. When `r=2`, designate either one of the two
length-two arms as `Q` and call the other `x-a-y`. Choose an internal vertex
`v` of `Q`.

Delete all and only the edges of the maximal block `B`. Every component of
`G-E(B)` meets `B` in exactly one vertex. It meets `B` at least once by
connectedness. If a component met distinct vertices `u,w` of `B`, a shortest
`u-w` path through that component, together with the 2-connected block `B`,
would be a nontrivial open ear of `B`; adjoining an ear to a 2-connected graph
is 2-connected. This would contradict maximality of `B` as a
vertex-biconnected block.

Let `U` be the component of `G-E(B)` containing `v`, and put

```text
F=G[V(G)\V(U)].
```

The sets are vertex-disjoint and exhaustive, and both displayed subgraphs are
induced by definition. The fibre `U` is connected. The complement `F` is
connected: `B-v` is connected, every other first-`B` fibre meets it at its
unique owner, and the two remnants of `Q-v` attach at `x` or `y`. Every nested
cyclic block, connector payload, and rooted tree follows one complete fibre.
The direct edge `xy` and path `x-a-y` leave exactly one intrinsic triangle in
`F`; the remnants of `Q-v` are acyclic.

Let `k` be the number of the five external triangles in `U`.

* If `k>=1`, then `U` is a connected triangular block graph with `k`
  triangles. The complement `F` is a connected triangular block graph with
  `6-k>=1` triangles, counting the intrinsic triangle. Therefore

  ```text
  sigma(U)>0,   sigma(F)>0.
  ```

  This includes `k=5`; no generic lower-rank theorem is invoked on the
  rank-one complement.

* If `k=0`, then `U` has only bridge blocks. It is a nonempty tree and
  `sigma(U)=-1`. The complement `F` is a connected six-triangle cactus with
  arbitrary connectors and trees, so Section 1 gives `sigma(F)>1`.

In either case induced superadditivity gives

```text
sigma(G)>=sigma(U)+sigma(F)>0.                         (3)
```

This proves the theta family uniformly for every `r>=2`, every repeated or
nested owner pattern, every actual bridge connector, and every rooted-tree
payload. The finite `r=2,3` adjacency executable is only a semantic regression
of the physical owner definition; the general quantifier is the theorem just
proved.

## 3. Simultaneous first-bridge quotient for the `P` row

Assume now `D+T^4+P`. Root the minimal physical block-cut subtree spanning the
six displayed cyclic blocks at `D`. Let `C_0` be the maximal `K2`-free cyclic
cluster containing `D`, and let `E_0` be the deduplicated antichain of distinct
first actual bridge blocks on routes from `C_0` to an external cyclic block.
Delete all edges in `E_0` simultaneously.

The component containing `D` is the root group; every other component is the
complete descendant side of one first bridge. These are connected induced,
vertex-disjoint, exhaustive original-vertex territories. Shared cuts are not
copied. Every later bridge, connector vertex, rooted branch, and descendant
stays in one component.  Separate the unique away group containing `P`, if
one exists, from all other away groups.  Every `P`-free away group contains at
least one triangle and is an all-triangle cactus, so its credit is strictly
positive.  Let `q` be the number of triangles in the `P`-containing away group.
If `q=0`, that group is a unicyclic `C5` territory and has credit strictly
greater than `-(sqrt(5)-2)>-1`.  If `q>=1`, it is a connected cactus of rank
`q+1 in {2,3,4,5}` and therefore has strictly positive credit by the proved
rank-uniform theorem that every connected cactus of cyclomatic rank at least
two has `sigma>0`.  Thus no mixed `P`-plus-triangle away group is ever called
triangular or charged by the one-root `C5` floor.

For reference, the exact coarse quotient has `Bell(6)=203` labelled states.
The finer root-incidence quotient, which records the root `D`, `k` retained
triangles, and whether `P` is retained, has

```text
N(k,0)=[1,1,4,29,307],
N(k,1)=[1,4,29,308,4322],
```

and 6,768 states after choosing root labels and partitioning away labels.
These counts are reproducibility checks, not the proof of ownership.

## 4. Narrow root packets

For `0<=t<=4`, every bridge-free shared-cut root cluster `D+T^t`, allowing
arbitrary one-root tree branches, satisfies

```text
sigma(D+T^t)>1.                                         (4)
```

For `t=0,1,2`, the exact diamond packets give respectively credits `>1`, `>2`,
and `>3`. For `t=3,4`, root the expanded block-cut incidence subtree at `D`
and choose the two triangle block nodes of least depth (with a fixed tie-break).
Their minimal connector-free shared-cut hull with `D` contains no third
triangle: such a third triangle would be a proper ancestor of one selected
node and hence have smaller depth. Retain this exact `D+T+T` anchor and take
its **cut closure**: every physical cut vertex incident with `D` or either
anchor triangle stays upstream. At each first incidence edge from that closed
set to an unselected triangle, open the complete far-side expanded incidence
subtree once. Thus a nested omitted triangle belongs to the first boundary
side; it is never charged by a second cut. Every omitted complete
first-boundary side has credit at least `-1`:
it is a nonempty tree if acyclic, greater than `-1` if unicyclic, and
nonnegative at rank at least two. There are at most `t-2` such sides, so

```text
sigma(D+T^t)>3-(t-2),
```

which is `>2` for `t=3` and `>1` for `t=4`. The finite selector independently
checks all 307 canonical `t=4` incidence skeletons. No monotonicity under
adding a triangle is used.

If `P` is away after Section 3, (4) pays the unique possible negative side
when its `P`-containing group has no triangle.  When that group also contains
one or more triangles, it is instead strict by the rank-uniform nonunicyclic
cactus theorem.  Every other, `P`-free away group is a strict all-triangle
cactus.  Hence the root credit `>1` closes every away-`P` state.

## 5. Retained-pentagon opening

Suppose `P` remains in the root group.  Let `R` be the induced subgraph on
that root group's vertices, before any opening of `P`; all first-bridge away
groups are outside `R`.  The block node of `P` in `R` has a unique parent cut,
a physical vertex `c in V(P)`.  Delete the five pentagon edges from `R`.  For
each `w in V(P)`, let `F_w` be the component of `R-E(P)` containing `w`.  The
same maximal-block ear argument shows that these five owner classes partition
`V(R)` and that each meets `P` exactly at its owner.

Keep the whole parent class `F_c` upstream, including the route to `D`, all
siblings at `c`, and all payload rooted at `c`.  Put the four other owner
classes downstream:

```text
A=R[V(F_c)],
B'=R[union_(w!=c) V(F_w)].
```

The downstream pentagon remnant `P-c` is a four-vertex path joining its four
owner classes. Hence `A` and `B'` are connected induced, disjoint, and
exhaustive within the root group. The only crossing edges are the two pentagon
edges incident with `c`.

If `q` retained triangles lie downstream, then `A` is a narrow
`D+T^(t-q)` packet and has credit `>1` by (4). If `q=0`, `B'` is a nonempty
tree and has credit `-1`; if `q>=1`, every cyclic block of `B'` is a triangle.
The four-vertex remnant `P-c` and all other material are only bridge/tree
attachments, so `B'` is a connected triangular block graph and has positive
credit. Thus

```text
sigma(A)+sigma(B')>0.                                   (5)
```

After this split, add back the already separated first-bridge away groups;
they remain disjoint from `A union B'`.  Because `P` is retained here, each of
those groups is `P`-free and hence a strict all-triangle cactus.  Equations
(4)--(5) close every retained-`P` state, while the preceding paragraph closes
every away-`P` state. Therefore `D+T^4+P` is strict.

## 6. Conclusion and provenance boundary

Sections 2 and 3--5 prove both exact post-DNN residual families strict, so the
physical `R21` post-DNN residual is empty.  Together with the DNN-closed and
DNN-boundary profiles, this closes the whole `R21` block partition at the
target `s^+(G)>=|V(G)|`; it does not assert a strict surplus on a boundary
profile.  The proof authenticates its sources as follows:

* the Tarjan/degree/path reconstruction in the parent gate supplies the physical
  rank-two theta classification, while the exact theta DNN calculation supplies
  the analytic survivor `(1,2,r)`;
* the literal adjacency gate is used only for its narrow `D+T^4+P` typing and
  `r=2` regression scope;
* the six-triangle theorem uses the explicit multi-source territory construction
  above and the exact piecewise cluster floors;
* the diamond row uses the exact `D+T+T` packet and its physical first-boundary
  selector;
* a mixed `P`-plus-triangle away group is authenticated as a connected cactus
  of rank `2` through `5` and is handled by the pinned rank-uniform
  nonunicyclic-cactus theorem, never by the triangular-cactus or `P`-only bound;
* all partitions are on original vertices before induced superadditivity is
  charged.

No symbolic closed flag, fixture extrapolation, generic bridge projector, or
unoriented rank-seven bridge theorem is used.  As a mathematical proof note,
this establishes only `R21`; it is not itself a promotion receipt.  Other
rank-seven packet families still require their own physical actual-bridge
dispatches before a global multiblock theorem can be promoted.
