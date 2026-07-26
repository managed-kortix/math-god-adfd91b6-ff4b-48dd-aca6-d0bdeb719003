# Fully shared pentacyclic residual `{T,T,T,T,Q}`

## Theorem

Let `G` be a connected cactus on `n` vertices whose five cyclic blocks are four
triangles `T1,T2,T3,T4` and one cycle `Q=Cq`, where `q>=3`. Suppose the five
blocks form one shared-cut cluster. Then

`s+(G)>n`.

Arbitrary bridge blocks and arbitrary trees attached at arbitrary vertices are
allowed.

The proof uses only induced-subgraph superadditivity, cycle territories, and
these existing packet bounds (all allowing arbitrary tree attachments):

1. every triangular unicyclic cactus `U` has `s+(U)>|U|`;
2. an intersecting `TT` bicyclic packet has surplus greater than `1`;
3. an all-`3 mod 4` cactus with at most two vertex-disjoint cycles has
   surplus greater than `r-1`, where `r` is its cyclomatic number;
4. a one-cluster four-triangle cactus with packing number three has surplus
   greater than `3`.

The fourth assertion is the central-triangle/three-petal case of the existing
tetracyclic block-graph theorem. Its direct Sachs proof gives `s+(H)>s-(H)`,
and `s+(H)+s-(H)=2|E(H)|=2(|H|+3)`.

## Incidence classification

Let `I` be the bipartite incidence tree whose nodes are the five cyclic blocks
and the cut vertices belonging to at least two cyclic blocks. If `c` is the
number of cut nodes, then `I` has `c+5` vertices and `c+4` edges. Hence

`sum_x (deg_I(x)-1)=4`,

where the sum is over cut nodes. This formula remains exact at a multiway cut:
a cut incident with `d` cyclic blocks contributes `d-1`.

There are exactly two cases.

### 1. The four triangles are pairwise disjoint

Every cut node incident with a triangle must also be incident with `Q`, because
it has degree at least two and cannot be incident with another triangle. A
triangle cannot meet `Q` at two cut vertices, since the two triangle--cut--`Q`
routes would form a cycle in `I`. Connectedness therefore forces each triangle
to meet `Q` exactly once. The four attachment cuts are distinct, since two
triangles using the same cut would intersect. Thus `I` is the subdivided star
with center `Q` and four triangular leaves: `Q` is central and the triangles
are four pairwise disjoint petals.

In particular this case forces `q>=4`. List the four attachment vertices in
cyclic order and partition `V(Q)` into four nonempty consecutive cyclic
intervals, each containing exactly one attachment. Equivalently, choose one
boundary edge in each of the four arcs between consecutive attachments. Each
interval induces a proper path, including when two attachments are adjacent;
for `q=4` all four intervals are singletons.

Adjoin to each interval its triangular petal. Every component outside this
five-cycle core is a tree with a unique core attachment, so assign it wholly to
the territory containing that attachment. This gives a vertex partition into
four connected induced triangular unicyclic cacti `G1,...,G4`. Therefore

`s+(G) >= sum_i s+(Gi) > sum_i |Gi| = n`.

This construction is unaffected by branching connector trees or trees attached
at any core vertex.

### 2. Some two triangles intersect

Let `k` be the number of shared cut vertices lying on `Q`. The corresponding
cut nodes contribute at least `k` to the incidence excess. An intersecting
triangle pair contributes at least one further unit. Indeed, if its common cut
does not lie on `Q`, it is an additional cut node of contribution at least one;
if it lies on `Q`, that cut has degree at least three and contributes at least
two, one more than the unit already included in `k`. Consequently

`k+1 <= 4`, and hence `k<=3`.

Assume first `q>=4`. There is a vertex `v` of `Q` which is not a shared cyclic
cut. Let `F` consist of `v` and all components of `G-E(Q)` attached to `Q` only
at `v`, and let `H=G-F`. Since `v` is not a shared cyclic cut, `F` is a tree,
so

`s+(F)=|F|-1`.

The graph `Q-v` is a path containing every shared cut on `Q`. Replacing the
`Q` node of `I` by this path leaves all four triangular blocks connected.
Thus `H` is connected, induced, and its only cyclic blocks are the four
triangles.

Partition `H` along the bridge connectors between its shared-cut clusters.
Let `A` be a cluster containing an intersecting triangle pair. If `A` contains
exactly two triangles, it is a `TT` packet and has surplus greater than `1`.
If it contains three triangles, connectedness of its triangle-intersection
graph makes its cycle packing number at most two, so its surplus is greater
than `2`. If it contains all four triangles and has packing number at most two,
its surplus is greater than `3`; if its packing number is three, it is exactly
the central-triangle/three-petal cluster covered by packet bound 4, again with
surplus greater than `3`. Every other cluster is either a singleton triangular
packet, with positive surplus, or contains an intersecting pair and has one of
the same positive bounds. Connector territories assign every internal path,
Steiner branch, and hanging tree to one packet without changing its cyclic
blocks. Consequently

`s+(H)>|H|+1`.

Induced-subgraph superadditivity now yields

`s+(G) >= s+(H)+s+(F) > |H|+1+|F|-1 = n`.

This is the clean cycle sacrifice: opening `Q` costs exactly one tree unit,
while the cluster containing an intersecting triangle pair supplies strictly
more than one unit; all other triangular packets have positive surplus. It
also gives the exact induced realization of the suggested `TT`-plus-triangles
argument without trying to allocate a shared cut vertex to two packets.

### The case `q=3`

Here all five cyclic blocks are triangles, regardless of which block was
initially named `Q`. Relabeling is therefore harmless. The connected triangular
block-graph theorem applies directly and gives `s+(G)>n`. This also covers all
multiway cuts. The four-petal alternative cannot occur with a designated
triangle as center, because four pairwise disjoint triangular petals would
require four distinct vertices on that center.

The two incidence alternatives are exhaustive, completing the proof.

## Exact status

There is no remaining fully shared incidence in the family `{T,T,T,T,Q}`.
Pairwise disjoint triangles force the central-four-petal partition; any
triangle intersection forces at most three shared cuts on `Q`, hence a private
vertex for `q>=4` and the four-triangle sacrifice. The exceptional notation
`q=3`, arbitrary multiway cuts, and arbitrary attached trees are all covered
above.
