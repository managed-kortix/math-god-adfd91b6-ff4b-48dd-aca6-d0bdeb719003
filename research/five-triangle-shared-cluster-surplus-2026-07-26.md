# Uniform surplus for a five-triangle shared-cut cluster

## Statement and scope

For a graph `X`, write

`sigma(X)=s+(X)-|V(X)|`.

The purpose of this note is to extract exactly what follows from the written
phase argument and the induced-territory argument in
`packing-two-square-energy/paper.tex`. In particular, it does not assume a
general quantitative strengthening of the triangular block-graph corollary.

The conclusion needed for the hexacyclic residual is available.

**Theorem 1 (five triangles in one shared-cut cluster).** Let `A` be a
connected cactus whose five cyclic blocks are triangles and form one
shared-cut cluster. Arbitrary trees may be attached at arbitrary vertices.
If `k` is the maximum number of pairwise vertex-disjoint triangular blocks,
then `k<=3` and

`sigma(A)>4` if `k<=2`, while `sigma(A)>2` in all cases.

In particular every such cluster has the uniform surplus `sigma(A)>2>1`.

The two bounds use different arguments. The first is the packing-two phase
theorem. The uniform bound is obtained by opening one leaf triangle and using
the proved four-triangle shared-cluster packet. The proof is given below.

## 1. Exact consequence of the phase theorem

**Lemma 2 (phase credit).** Let `H` be a connected cactus with `r` cyclic
blocks, all of whose lengths are `3 mod 4`. If its cycle-packing number is at
most two, then

`sigma(H)>r-1`.

**Proof.** In the grouped Sachs expansion on the imaginary axis, every single
cycle has phase `-2i`, every two-cycle term is real, and there are no terms
with three or more cycles. The imaginary part is therefore

`Im Psi_H(t)=-2 sum_C Z_{H-V(C)}(t)<0` for every `t>0`,

where every signless matching polynomial in the sum is positive. The
continuous-argument step in the Coulson identity gives `s+(H)>s-(H)`.
Since a connected `r`-cyclic cactus has

`|E(H)|=|V(H)|+r-1`

and `s+(H)+s-(H)=2|E(H)|`, it follows that

`s+(H)>|E(H)|=|V(H)|+r-1`.

Subtracting `|V(H)|` proves the claim. QED.

This is the full numerical credit supplied by the phase argument. It applies
to arbitrary attached trees because neither the Sachs sign nor the edge count
changes its form.

## 2. What the cycle-territory proof does not prove

It is tempting to combine a maximum packing of size `k` with the Voronoi
territories from the triangular block-graph proof and claim

`sigma(G)>r-k`.

That inference is invalid. A triangle not selected in the packing can be split
among several induced territories and then contributes no cyclomatic credit to
any territory. The territory proof establishes only

`sigma(G) >= sum_i sigma(G_i) > sum_i (beta(G_i)-1)`,

not `sum_i beta(G_i)=r`.

**Exact obstruction.** Take a central triangle `T0` and three petal triangles
`T1,T2,T3`, where `Ti` meets `T0` at the `i`-th vertex of `T0`; the petals are
otherwise pairwise disjoint. The maximum packing is `{T1,T2,T3}`, so `r=4`
and `k=3`. In the distance territories centered at the three petals, the three
vertices of `T0` have distance zero from three different selected cycles.
Consequently `T0` is split among the three territories. Each territory retains
only its selected petal, and

`sum_i beta(G_i)=3<4=r`.

Thus the exact territory calculation yields only strict positivity, not the
putative bound `sigma(G)>r-k`. The separate matching-injection argument for
this four-triangle incidence proves a stronger result, but that result cannot
be retroactively attributed to the territory decomposition.

## 3. Leaf opening in a shared-cut cluster

We first reproduce, rather than merely quote, the four-triangle input used
below.

**Lemma 3 (four-triangle shared cluster).** Let `B` be a connected cactus
whose four cyclic blocks are triangles in one shared-cut cluster. Then

`sigma(B)>3`.

**Proof.** Let `p` be the maximum number of pairwise vertex-disjoint triangle
blocks. The cluster condition excludes `p=4`, because four independent
vertices cannot induce a connected triangle-intersection graph. If `p<=2`,
Lemma 2 with `r=4` gives the result.

Suppose `p=3`, and choose disjoint triangles `T1,T2,T3`. The fourth triangle
`T0` must meet each `Ti`, since the intersection graph is connected and no two
of `T1,T2,T3` meet. Their three intersections with `T0` are distinct, since a
coincident intersection would make two petals meet. Thus `T0` is a central
triangle and `T1,T2,T3` are its three pairwise disjoint petals.

Let `U=V(T1) union V(T2) union V(T3)` and `F=B-U`. For the signless matching
polynomial `Z`, the only odd-cardinality collections of disjoint cycles are the
four singleton triangles and the collection of all three petals. Hence the
grouped Sachs identity is

`Im Psi_B(t)=-2 sum_{j=0}^3 Z_{B-V(Tj)}(t)+8 Z_F(t)`.             (2)

After deleting `T0`, each petal leaves its edge opposite the center. These
three edges are pairwise disjoint and disjoint from `F`. Adjoining any subset
of them to any matching counted by `Z_F` gives an injective family of matchings
of `B-V(T0)`, and therefore

`Z_{B-V(T0)}(t)>Z_F(t)` for `t>0`.                              (3)

For each `i`, the graph induced by `U-V(Ti)` has a perfect matching: use the
edge of `T0` joining the other two petal centers and the edge opposite the
center in each of those two petals. It consequently has signless matching
polynomial strictly greater than one. Taking the union of one of its matchings
with a matching of `F` gives a product injection into the matchings of
`B-V(Ti)`, so

`Z_{B-V(Ti)}(t)>Z_F(t)` for `i=1,2,3` and `t>0`.                 (4)

Extra forest edges between the displayed induced subgraphs are simply unused,
so arbitrary attached trees do not affect either injection. Equations (2)--(4)
give `Im Psi_B(t)<0` for all `t>0`. The same continuous-argument and Coulson
step as in Lemma 2 yields `s+(B)>s-(B)`. Since `B` is connected and
four-cyclic, `|E(B)|=|V(B)|+3`; hence

`s+(B)>|E(B)|=|V(B)|+3`,

which is `sigma(B)>3`. QED.

This proof identifies both places where shared-cut connectivity is used: it
rules out four disjoint triangles and forces the packing-three incidence to be
the central-triangle/three-petal graph. No classification beyond those two
elementary observations is assumed.

For a shared-cut cluster of triangular blocks, form its bipartite incidence
graph `I`: one class consists of triangle nodes, the other of vertices lying in
at least two triangular blocks, and incidence means containment. This is a
tree. Indeed, it is the corresponding subtree of the block-cut tree of the
cactus after irrelevant bridge structure is suppressed. Every cut node has
degree at least two, so every leaf of `I` is a triangle node.

**Lemma 4 (one leaf opening).** Let `A` have `r>=2` triangular blocks in one
shared-cut cluster. There is an exact induced vertex partition

`V(A)=V(H) disjoint union V(F)`

such that:

1. `F` is a nonempty tree and `sigma(F)=-1`;
2. `H` is connected;
3. the cyclic blocks of `H` are the other `r-1` triangles, and they remain in
   one shared-cut cluster;
4. arbitrary trees attached to the original cluster are assigned wholly to
   `H` or `F` by their unique attachment.

**Proof.** Choose a leaf triangle `T` of `I`. It contains exactly one shared
cyclic cut `x`, hence either of its other two vertices is private. Choose one
such private vertex `v`. Put in `F` the vertex `v` and every bridge-tree branch
rooted at `v`; put every other vertex in `H`.

The cactus property implies that every off-core tree has a unique attachment
to the cyclic hull, so this is an exact vertex partition and both named graphs
are induced. The graph `F` is a nonempty tree. Removing `v` changes `T` into
the edge joining its two remaining vertices, one of which is `x`; it creates no
cycle and does not remove any cyclic cut belonging to another triangle.
Deleting the leaf triangle node from `I` leaves the other `r-1` triangle nodes
connected. Hence `H` is connected and those triangles remain one shared-cut
cluster. Finally, every nonempty tree has `s+(F)=|V(F)|-1`, so
`sigma(F)=-1`. QED.

Combining induced-subgraph superadditivity with Lemma 4 gives the reusable
rule

`sigma(A)>=sigma(H)-1`.                                      (1)

Notice that the full unit in (1) is necessary: an attached tree can have any
order, but its surplus is always exactly `-1`.

## 4. Proof of Theorem 1

First, `k<=3`. If four of the five triangles were pairwise vertex-disjoint,
then the fifth triangle would have to meet all four. Indeed, the triangle
intersection graph is connected, the four selected vertices are independent,
and the fifth vertex is the only possible neighbor connecting them. The four
intersections would have to be four distinct vertices because the selected
triangles are pairwise disjoint. A triangle has only three vertices, a
contradiction.

If `k<=2`, apply Lemma 2 with `r=5` to obtain `sigma(A)>4`.

For the bound valid for every `k`, apply Lemma 4 once. The induced remainder
`H` has four triangular blocks in one shared-cut cluster. Lemma 3, including
its explicit packing-three matching argument, gives

`sigma(H)>3`.

The opened territory is a tree `F` with `sigma(F)=-1`. Therefore

`sigma(A)>=sigma(H)+sigma(F)>3-1=2`.

This proves Theorem 1. QED.

## 5. General form justified by the same ingredients

The argument gives the following limited, but rigorous, family of bounds for
one triangular shared-cut cluster with `r` blocks:

- if its packing number is at most two, `sigma>r-1` by Lemma 2;
- for `r=2,3`, shared-cut connectivity forces packing number at most two, so
  Lemma 2 gives `sigma>r-1`; for `r=4`, Lemma 3 gives the same bound;
- for `r>=4`, repeatedly opening `r-4` incidence leaves and retaining a
  four-triangle shared cluster gives `sigma>3-(r-4)=7-r`.

The last formula is useful at `r=5`, where it gives `>2`; it is not asserted to
be optimal for larger `r`. No bound `sigma>r-k` follows from the existing
Voronoi-territory proof without an additional theorem controlling cycles split
between territories. The central-triangle/three-petal example is the exact
obstruction to that deduction.
