# Uniform margins for an arbitrary shared triangular cluster

## Statement

For a graph `X`, write

`sigma(X)=s+(X)-|V(X)|`.

Let `A_r` be a connected cactus whose cyclic blocks are exactly `r` triangles,
all in one shared-cut cluster. Arbitrary finite trees may be attached at
arbitrary vertices. The proved four-triangle packet and incidence-leaf opening
give the following uniform result.

**Theorem 1.** For every `r>=4`,

`sigma(A_r)>7-r`.                                                (1)

Equivalently, the certified lower-bound sequence is

`L_4=3`, and `L_r=L_(r-1)-1` for `r>=5`,                         (2)

so exactly

`L_r=7-r`.                                                       (3)

Here "exactly" refers to the recurrence for the bounds produced by this
argument. It does not assert that the infimum of `sigma(A_r)` equals `7-r`, or
that one-unit loss at every opening is sharp for the original unsplit graph.

The values relevant through rank seven are

| `r` | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|
| proved margin | `>3` | `>2` | `>1` | `>0` |

For completeness, the established packing-two argument gives `sigma(A_r)>r-1`
for `r=1,2,3`, and the four-triangle base gives the same formula at `r=4`.
Thus the piecewise bound furnished by the packing-two, base-four, and opening
inputs is

`sigma(A_r)>B_r`, where `B_r=r-1` for `1<=r<=4` and `B_r=7-r` for `r>=4`.

The two expressions agree at `r=4`. The downward branch for `r>=4`, rather
than the small-r upward branch, is the incidence-opening recurrence studied
here.

Thus the method by itself reaches strict positivity at seven triangles and no
farther. The general triangular block-graph theorem separately gives
`sigma>0` at every rank, but that qualitative theorem is not an improvement in
the positive budgets needed for sacrifices.

## 1. The incidence tree

Form the bipartite graph `I_r` with one node for each triangular block and one
node for each vertex contained in at least two triangular blocks; incidence is
containment. This is a tree. It is the subtree of the cactus block-cut tree
spanned by the triangular block nodes, with bridge-only structure omitted.

Every cut node of `I_r` has degree at least two. This includes a multiway cut
shared by any number of triangles. Consequently every leaf of `I_r` is a
triangle node. A leaf triangle `T` is incident with exactly one shared cyclic
cut `x`, and its other two vertices are private with respect to every cyclic
block.

The word "private" does not prohibit hanging tree branches. It says only that
the vertex lies in no other cyclic block.

## 2. One incidence-leaf opening

**Lemma 2.** Let `r>=2`. From `A_r` one can obtain an exact induced partition

`V(A_r)=V(A_(r-1)) disjoint union V(F)`                           (4)

with the following properties:

1. `F` is a nonempty tree and `sigma(F)=-1`;
2. `A_(r-1)` is connected;
3. its cyclic blocks are exactly the other `r-1` triangles;
4. those triangles still form one shared-cut cluster;
5. every hanging tree is assigned wholly to one side.

**Proof.** Choose a leaf triangle `T` of `I_r`, let `x` be its unique shared
cyclic cut, and choose either private vertex `v` of `T`. Put into `F` the
vertex `v` and every off-core tree branch rooted at `v`. Put all other vertices
into `A_(r-1)`.

A component outside the cyclic hull has a unique attachment to that hull. If
it had two, the two hull routes together with the component route would create
an additional cyclic block, contrary to the assumed cactus block structure.
Hence (4) assigns every vertex once, both named graphs are induced, and no
hanging tree is split.

The graph `F` is a tree: it consists of `v` with zero or more bridge-tree
branches rooted there. It is nonempty even if no branch is present. Therefore
`s+(F)=|V(F)|-1` and `sigma(F)=-1`.

In the other part, `T-v` is the edge joining `x` to the other private vertex.
It is now a tree branch attached at `x`; it creates no cycle. Since `v` was
private, no vertex shared by two retained triangles was removed. Deleting the
leaf triangle node and its incident edge from `I_r` leaves a connected tree on
the other triangle nodes (possibly with the now-irrelevant cut node `x` as a
pendant node). Removing such irrelevant cut nodes leaves precisely the
incidence tree of the retained triangles. Thus the retained triangles remain
one shared-cut cluster. Their incidence realization, together with the path
`T-v`, is connected, proving that `A_(r-1)` is connected. QED.

Induced-subgraph superadditivity now gives the one-step inequality

`sigma(A_r)>=sigma(A_(r-1))+sigma(F)=sigma(A_(r-1))-1`.           (5)

The full unit in (5) cannot be replaced by a smaller uniform opening charge:
every nonempty tree, independent of its order or shape, has surplus exactly
`-1`.

## 3. Iteration and the recurrence

Apply Lemma 2 successively to a leaf of the current retained incidence tree.
After `j` openings, where `0<=j<=r-4`, there is an exact induced partition

`V(A_r)=V(H_(r-j)) disjoint union V(F_1) disjoint union ... disjoint union V(F_j)`,

where every `F_i` is a nonempty tree and `H_(r-j)` is connected with exactly
`r-j` triangular blocks in one shared-cut cluster. Earlier opened triangle
remnants are merely hanging tree branches at later stages, so the arbitrary-
tree clause of Lemma 2 applies inductively.

Taking `j=r-4` leaves a four-triangle shared cluster `H_4`. The established
four-triangle theorem, including the central-triangle/three-disjoint-petals
incidence, gives

`sigma(H_4)>3`.

Therefore

`sigma(A_r)>=sigma(H_4)+sum_(i=1)^(r-4) sigma(F_i)`

`             >3-(r-4)=7-r`,

which proves Theorem 1. At the level of certified bounds, each opening changes
`L_(r-1)` to `L_(r-1)-1`; hence (2) and (3) are the exact recurrence and its
solution.

Strictness is preserved: superadditivity is weak, but its four-triangle input
is strict, while every tree charge is an equality.

## 4. Connectivity and shared-cut audit

The opening argument needs two different preservation statements, and neither
should be replaced by the other.

**Ordinary connectivity.** The opened triangle leaves the edge `T-v` in the
remainder. This edge contains the unique attachment cut `x`, so it stays
attached to the retained cyclic hull. Deleting `v` cannot disconnect two
retained incidence branches because a leaf triangle has only one such branch.

**Shared-cut connectivity.** The path remnant `T-v` is not used to claim that
two retained triangles share a cut. Instead, deleting a leaf triangle from the
incidence tree leaves the other triangle nodes connected through their own
shared cut nodes. Thus their shared-cut graph remains connected. If `x` was a
binary cut, it ceases to be a shared cyclic cut after `T` is opened and is
discarded from the retained incidence tree. If `x` was multiway, it remains a
shared cut of the other incident triangles. Both cases preserve the claim.

**Arbitrary attachments.** A branch rooted at `v` belongs to the opened tree;
a branch rooted anywhere else belongs to the remainder. Cycle edges incident
with `v` cross the vertex partition and are discarded when induced subgraphs
are taken. This is legitimate because the proof uses induced-subgraph
superadditivity, not edge monotonicity.

**Repeated openings.** At each stage the leaf is selected in the incidence
tree of the triangles still retained, not in the original tree. The preceding
lemma then re-establishes both kinds of connectivity. No simultaneous choice
of pairwise separated original leaves is required.

## 5. The heptacyclic sacrifice budget

The inequality needed for a rank-seven sacrifice argument with `r>=4` is not
`sigma(A_r)>r`. If a heptacyclic cactus can be partitioned into an `r`-triangle
shared cluster and `7-r` opened tree territories, then the exact requirement is

`sigma(A_r)>7-r`.                                                (6)

Theorem 1 supplies (6) for every `4<=r<=7`. Consequently

`sigma(G)>=sigma(A_r)-(7-r)>0`.                                  (7)

This is an exact budget match: the `r-4` leaf openings hidden in the proof of
Theorem 1 and the `7-r` additional sacrifices total three tree charges, which
are paid by the strict `>3` four-triangle base packet. More generally, the same
ledger at total cycle rank `c` gives

`sigma(G)>3-(r-4)-(c-r)=7-c`.                                   (8)

Thus this base-four opening mechanism closes rank seven strictly, but at rank
eight it gives only `>-1`, not positivity.

For `r<=3`, the available bound `sigma(A_r)>r-1` does not pay `7-r`
sacrifices: it would require `r-1>=7-r`, which first holds at `r=4`. Hence a
heptacyclic proof based only on one small triangular packet and one-unit
openings needs at least four retained triangles, or some additional positive
packet margin elsewhere.

Equation (7) is conditional on a valid induced partition. For each of the
`7-r` external sacrifices one must verify:

1. an admissible private opening vertex exists;
2. its rooted tree territory is disjoint from the other opened territories;
3. the remainder is connected;
4. the `r` retained triangles still form one shared-cut cluster.

These conditions are automatic for successive incidence-leaf triangles in a
pure triangular cluster. They are not automatic for arbitrary internal
nontriangular cycles: a private opening can preserve ordinary connectivity
while the retained triangles remain dispersed among several shared-cut
components. In that situation Theorem 1 cannot be applied to their union.

Finally, a hypothetical estimate `sigma(A_r)>r` would be enough against
`7-r` tree sacrifices exactly when `2r-7>=0`, hence for integral `r>=4`, since
it would give `sigma(G)>r-(7-r)=2r-7`. But `sigma(A_r)>r` is neither needed nor
supplied by this proof. Even the natural stronger-looking pattern
`sigma(A_r)>r-1`, known for packing number at most two and for `r<=4`, does not
follow under repeated leaf opening: the recurrence loses one unit when `r`
increases by one. The rigorous uniform conclusion from the stated base and
opening is exactly (1).

## Conclusion

Incidence-leaf opening is uniform over all binary and multiway shared cuts and
over arbitrary attached trees. Starting from the proved strict base
`sigma(A_4)>3`, it yields the certified recurrence `L_r=L_(r-1)-1` and hence
`sigma(A_r)>7-r`. This is precisely enough to absorb the complementary
`7-r` one-unit tree sacrifices in a heptacyclic argument, provided the explicit
connectivity, concentration, private-vertex, and disjointness checks for those
sacrifices are made.
