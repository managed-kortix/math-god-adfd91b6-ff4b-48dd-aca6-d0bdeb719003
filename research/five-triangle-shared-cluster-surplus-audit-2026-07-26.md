# Adversarial audit: five-triangle shared-cluster surplus

## Verdict

**ACCEPT.** Let `A` be a connected cactus whose five cyclic blocks are
triangles in one shared-cut cluster, with arbitrary trees attached at arbitrary
vertices. The argument in
`research/five-triangle-shared-cluster-surplus-2026-07-26.md` validly proves

`sigma(A)=s+(A)-|V(A)|>2`.

No counterexample occurs from a multiway cut, a non-core attachment, packing
three, or the exceptional four-triangle incidence. The proof uses the exact
four-triangle estimate `sigma>3`; strict positivity alone would not suffice.

## 1. Incidence tree and the leaf claim

Form the bipartite incidence graph `I` with a node for each triangle and a node
for each vertex contained in at least two triangles. This is the subtree of the
block-cut tree induced by the five cyclic blocks and their shared cut vertices,
so it is a tree. A cut node incident with `d` triangles has degree `d>=2`,
including a genuine multiway cut. Therefore no cut node is a leaf, and every
leaf of `I` is a triangle node.

If a leaf triangle is `T`, its node has degree one, so `T` contains exactly one
shared cyclic cut `x`. Its other two vertices are private with respect to all
cyclic blocks. This remains true when `x` is multiway: the degree of the cut
node changes, but the leaf triangle still has only the one incidence edge.

Thus the assertion "a leaf triangle always has a private vertex" is correct;
in fact it has two private cyclic vertices.

## 2. Opening a leaf

Choose a private vertex `v` of `T`. Put `v` and every hanging tree branch whose
unique core attachment is `v` into `F`, and put all other vertices into `H`.
Then:

- `F` is a nonempty induced tree, hence `s+(F)=|F|-1` and `sigma(F)=-1`;
- `T-v` is the edge joining the other private vertex to `x`, so it introduces
  no cycle and keeps the attachment at `x` in `H`;
- deleting the leaf triangle node and its incidence edge from `I` leaves a
  connected incidence tree on the other four triangle nodes;
- consequently `H` is connected and its four cyclic blocks are exactly the
  retained triangles, still in one shared-cut cluster.

Arbitrary attachments cause no leak between the two territories. In a cactus,
every component outside the cyclic hull has one core attachment; two would
create a second block-tree route. Attachments at `v` go wholly to `F`, and all
others go wholly to `H`. Edges from `v` to the two retained vertices of `T`
cross the partition, which is allowed because only induced-subgraph
superadditivity is used.

This proves the exact bookkeeping inequality

`sigma(A) >= sigma(H)+sigma(F)=sigma(H)-1`.

## 3. Exact four-triangle dependency

For four triangles in one shared-cut cluster, packing four is impossible: four
pairwise disjoint triangle nodes would give four isolated vertices in the
triangle-intersection graph. If the packing number is at most two, the
packing-two phase theorem gives

`sigma(H)>4-1=3`.

If the packing number is three, choose three pairwise disjoint triangles
`T1,T2,T3`. The fourth triangle `T0` must meet each of them because the
intersection graph is connected and there is no other possible intermediate
triangle. The three intersections on `T0` are distinct; if two coincided, the
corresponding petals would intersect each other. Hence the only packing-three
incidence is a central triangle with three pairwise disjoint petals. This
classification also covers multiway cuts: a multiway intersection involving
two petals would contradict their disjointness.

For this exceptional incidence, the grouped Sachs expansion has exactly the
four singleton odd-cycle collections and the collection of all three petals:

`Im Psi_H(t) = -2 sum_(j=0)^3 Z_(H-V(Tj))(t) + 8 Z_F(t)`.

The matching injections are sufficient and survive arbitrary attached trees:

- deleting `T0` leaves the three opposite petal edges, which are pairwise
  disjoint and disjoint from `F`; adjoining their subsets gives
  `Z_(H-V(T0))(t) >= (1+t^2)^3 Z_F(t) > Z_F(t)`;
- after deleting a petal `Ti`, the six vertices in the other two petals and
  the remaining part of `T0` have a perfect matching; product with any
  matching of `F` gives `Z_(H-V(Ti))(t)>Z_F(t)` for each `i=1,2,3`.

Unused attachment edges cannot invalidate an injected matching. Therefore the
negative singleton terms strictly dominate the positive three-petal term for
every `t>0`. The continuous-argument/Coulson step gives `s+(H)>s-(H)`. Since a
connected four-cyclic cactus has `|E(H)|=|V(H)|+3`, this is precisely

`sigma(H)>3`.

The stronger estimate is essential: the universal triangular block-graph
result only gives `sigma(H)>0`, which would leave `sigma(A)>-1` after paying
for the opened tree.

## 4. Five-triangle packing coverage

The five-triangle cluster has packing number at most three. If four triangles
were pairwise disjoint, the fifth would be the only remaining node capable of
connecting them in the triangle-intersection graph. It would have to meet all
four at distinct vertices, since a common intersection would make two of the
four selected triangles intersect. A triangle has only three vertices.

This excludes packing four and five. Packing at most two separately gives the
stronger phase bound `sigma(A)>4`. Packing three needs no additional
five-triangle incidence classification: opening any incidence-tree leaf
reduces to a four-triangle shared cluster, and the preceding dichotomy covers
both possible packing numbers of that remainder. In particular, the remainder
may be the central-triangle/three-petal configuration; it is not silently
assumed to have packing at most two.

Finally,

`sigma(A) >= sigma(H)-1 > 3-1=2`.

All inequalities and partitions are uniform over arbitrary tree attachments
and all binary or multiway shared cuts. The lemma is accepted as stated.
