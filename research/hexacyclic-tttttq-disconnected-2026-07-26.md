# Hexacyclic `TTTTTQ` with disconnected shared-cut graph

## Scope and conclusion

Let `G` be a connected cactus whose six cyclic blocks are five designated
triangles `T1,...,T5` and one cycle `Q=Cq`, `q>=3`. Put

`sigma(H)=s+(H)-|V(H)|`.

**Theorem.** If the shared-cut graph of the six cyclic blocks is disconnected,
then `sigma(G)>0`.

This includes arbitrary bridge connectors, arbitrary connector entry vertices,
unmarked Steiner branches, multiway cuts, and arbitrary trees attached at
arbitrary vertices. It also includes `q=3`, when all six blocks are triangles.

The last previously unresolved family was a single shared-cut cluster of five
triangles separated by bridges from a hostile `Q=Cq`, `q=1 mod 4`. It is closed
by the uniform estimate `sigma(TTTTT)>2` proved in
`research/five-triangle-shared-cluster-surplus-2026-07-26.md`.

## Inputs

We use the following established facts.

1. **Induced superadditivity.** For a vertex partition into induced subgraphs,
   `sigma(G)>=sum_i sigma(G[Vi])`.
2. **Lower-cyclic cactus bounds.** Connected pentacyclic and tetracyclic cacti
   have positive surplus; connected tricyclic and bicyclic cacti have
   nonnegative surplus.
3. **Triangular block-graph theorem.** A connected cactus with at least one
   cycle and only triangular cyclic blocks has positive surplus.
4. **Hostile unicyclic bound.** If a unicyclic territory has cycle `Cq` with
   `q=1 mod 4`, then its surplus is at least
   `-delta_q`, where `delta_q=sec(pi/q)-1<1`.
5. **Five-triangle shared-cluster margin.** A connected cactus whose five
   cyclic blocks are triangles in one shared-cut cluster has surplus greater
   than `2`, with arbitrary attached trees. This includes packing three.

We also use the standard reduced-tree territory lemma. Contract each shared-cut
cluster to a marked node in the block-cut tree, take the minimal tree spanning
the marked nodes, and suppress unmarked degree-two nodes. Cutting an edge of
this reduced tree can be realized by cutting an actual bridge. Every hanging
tree and unmarked Steiner branch can be assigned wholly to one side, producing
two connected induced territories with exactly the designated cyclic blocks.

## Triangular bridge sides

**Lemma 1.** Suppose an actual bridge separates a connected territory `A`
containing exactly `r` cyclic blocks, all triangles, from the complementary
connected territory `B`. If `1<=r<=4`, then `sigma(G)>0`. If `r=5` and the
five triangles form one shared-cut cluster, then `sigma(G)>0` as well.

**Proof.** For `r=1`, `B` is pentacyclic and has positive surplus. For `r=2`,
`B` is tetracyclic and has positive surplus. For `r=3,4`, `B` is respectively
tricyclic or bicyclic and has nonnegative surplus. In each case `A` has strict
positive surplus by the triangular block-graph theorem, so superadditivity is
strict.

For `r=5`, `B` is unicyclic. Nonhostile parity is immediate. If
`q=1 mod 4`, then

`sigma(G)>=sigma(A)+sigma(B)>2-delta_q>1`.

QED.

## Reduced-tree proof

Assume first that `q=3`. Then every cyclic block of `G` is a triangle, and the
triangular block-graph theorem proves `sigma(G)>0` without using
disconnectedness.

Now assume `q!=3`. Let `R` be the reduced tree spanning the shared-cut
clusters. Since the shared-cut graph is disconnected, `R` has at least two
marked nodes and therefore at least two leaves. Every leaf of the minimal
spanning tree is marked. At most one leaf cluster contains `Q`; choose another
leaf cluster `A`. It is `Q`-free and hence consists of exactly `r` designated
triangles for some `1<=r<=5`.

Cut the first actual bridge on the unique reduced edge from `A` toward the
rest of `R`, and use the territory lemma to assign all side branches. This
gives a vertex partition into connected induced territories: the leaf side
contains exactly the `r` triangles of `A`, and the other side contains all
remaining cyclic blocks. If `r<=4`, Lemma 1 applies. If `r=5`, the leaf is by
definition one shared-cut cluster, so the last clause of Lemma 1 applies.
Thus `sigma(G)>0` in every case.

## Exact audit of `TTTTT|Q`

Let `A` be the five-triangle leaf territory and `B` the remote unicyclic
`Q` territory. The proof of the five-triangle margin chooses a leaf triangle
in the cycle-cut incidence tree of `A`, opens one of its private vertices, and
partitions `A` into:

- one tree territory of surplus `-1`; and
- one connected four-triangle shared-cut territory of surplus `>3`.

Hence `sigma(A)>2`. This move is internal to `A`, so it is independent of the
vertex at which the external bridge connector enters `A`.

No packing-at-most-two assumption is made. Packing three can occur in `A`.
After the incidence-leaf opening, the four-triangle remainder either has
packing at most two or is exactly the central-triangle/three-petal incidence.
The latter has `s+>s-` by the direct grouped-Sachs matching injection, and thus
also has surplus `>3`. Packing four cannot occur in a one-cluster
five-triangle cactus: a fifth triangle connecting four pairwise disjoint
triangles would have to meet them at four distinct vertices.

For hostile `q=1 mod 4`, therefore,

`sigma(G)>=sigma(A)+sigma(B)>2-delta_q>1>0`.

This closes disconnected `TTTTT|Q` with all incidence types, including packing
three. There is no remaining disconnected shared-cut case in `TTTTTQ`.
