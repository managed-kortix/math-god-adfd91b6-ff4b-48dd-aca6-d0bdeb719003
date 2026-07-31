# The tetracyclic `2+1+1` residuals

## Proposition

Let `G` be connected, with one bicyclic block and two unicyclic blocks, and
allow arbitrary bridge trees and arbitrary rooted trees at every core vertex.
The following two residual rows have positive surplus:

1. `Theta(1,2,r)+C3+C3`, for `r>=2`;
2. `Theta(1,2,2)+C3+C5`.

Thus `s+(G)>|V(G)|` in both rows. No restriction is imposed on the block tree,
on shared cut vertices, or on the lengths and branches of connector trees.

Write `sigma(H)=s+(H)-|V(H)|`. We use induced superadditivity and the following
already proved attachment-uniform packet credits:

| induced packet | credit |
|---|---:|
| nonempty tree | `-1` |
| `C3` cactus | `>0` |
| `C5` cactus | `>=-delta`, `delta=sqrt(5)-2<1` |
| two-`C3` cactus | `>1` |
| `C3+C5` cactus | `>1-delta` |
| `Theta(1,2,2)` | `>1` |
| `C3+C3+C5`, with the two triangles sharing a cut | `>2-delta>1` |

Every row permits arbitrary trees attached anywhere. The last row is the
shared-triangle phase bound, not merely the unquantified tricyclic theorem.
We also use the completed `2+1` statements that every attached
`Theta(1,2,r)+C3` and every attached `Theta(1,2,2)+C5` has positive surplus.

## Territory convention

Delete the theta edges and regard every component hanging from a theta vertex
as owned by that vertex. Equivalently, in the block-cut tree every block
outside the theta has a unique first theta cut on its route to the theta. For a
theta vertex `v`, its opened territory consists of `v`, all off-theta
components owned by `v`, and all rooted branches based at `v`.

After an internal vertex of one theta arm is opened, the other two theta arms
still connect the endpoints. Consequently the complementary territory is
connected. Both territories are induced. Any further separation below is made
at an actual bridge. At every cut, the cut vertex is assigned to exactly one
territory; all components on the other side follow their unique block-cut-tree
route. Hence these constructions partition every vertex and every attached
tree, including branches based at cuts and at internal connector vertices.

## Two external triangles

Write the theta paths as the edge `xy`, the length-two path `xay`, and an
`x-y` path `P` of length `r`. Choose any internal vertex `v` of `P`, and let
`R` be its opened territory. The complement `H=G-R` is connected and retains
the intrinsic triangle `xayx`; the two remnants of `P-v` are only trees.

Let `k` be the number of external triangle blocks in `R`. The block-cut tree
makes the following list exhaustive.

- If `k=1`, then `R` is a triangular unicyclic cactus, so `sigma(R)>0`.
  The complement is a two-triangle cactus, so `sigma(H)>1`.
- If `k=2`, then `R` is a two-triangle cactus, so `sigma(R)>1`.
  The complement is a triangular unicyclic cactus, so `sigma(H)>0`.
- Suppose `k=0`. Then `R` is a nonempty tree and `sigma(R)=-1`. If the two
  external triangles share a cut, all three triangles in `H` have packing
  number at most two. The favorable-cycle phase theorem gives
  `sigma(H)>2`, and hence `sigma(G)>1`.
- Finally suppose `k=0` and the external triangles do not share a cut. If the
  three retained triangles have packing number at most two, the same favorable-
  cycle theorem gives `sigma(H)>2`, so the tree is paid. If their packing
  number is three, they are
  pairwise vertex-disjoint. The reduced tree joining them then has actual
  bridges; cut one edge so that one side contains two triangles and the other
  contains one. Call the singleton territory `L`. The other retained territory
  is a two-triangle cactus, while `R` is a tree. Therefore

  `sigma(G) >= sigma(L) + sigma(H-L) + sigma(R) > 0+1-1=0`.

This proves `Theta(1,2,r)+C3+C3` for every cut incidence. Notice that no
internal vertex was assumed to avoid both external routes: the cases `k=1,2`
are precisely the cases in which the chosen vertex carries one or both routes.

## One triangle and one pentagon

Now the theta is `Theta(1,2,2)`. Denote its two degree-two internal vertices by
`a,b`, the external triangle by `T`, and the pentagon by `Q`. Join cyclic
blocks in the shared-cut graph when they have a common cut vertex. Contracting
each shared-cut component and every acyclic connector between components gives
a tree. We first exhaust its disconnected cases and then the connected
three-block incidences.

### More than one shared-cut component

Actual bridge cuts separate the components, with each whole connector branch
assigned to one side.

- For three singleton components, use the three territories theta, `T`, and
  `Q`. Their total credit is `>1+0-delta>0`.
- For a `theta+Q` component and singleton `T`, the completed `2+1` theorem
  gives positive credit on the first territory and the triangle is strict.
- For a `T+Q` component and singleton theta, the credits are respectively
  `>1-delta` and `>1`.
- It remains that theta and `T` share a cut `w`, while `Q` lies outside that
  shared-cut component. Choose `v` in `{a,b}` with `v!=w` and open `v`.
  Deleting `v` leaves the other intrinsic theta triangle, and it shares `w`
  with `T`. If the route to `Q` is owned by `v`, the opened territory is a
  pentagonal unicyclic cactus and the complement is a two-triangle cactus;
  the total is `>1-delta`. If that route is not owned by `v`, the opened
  territory is a tree and the complement is a `C3+C3+C5` cactus whose two
  triangles share `w`; the total is `>(2-delta)-1=1-delta`.

These are all `2+1` distributions, according to which pair lies in the
two-block shared-cut component.

### One shared-cut component

The block-cut incidence restricted to the three cyclic blocks is a tree. Thus
either all three blocks use one common cut, or there are two distinct cuts and
exactly one of theta, `T`, and `Q` is the central cyclic block. These four
possibilities are exhaustive.

- If theta is central, let `w` be its cut with `T`; its cut with `Q` may equal
  `w`. Choose `v` in `{a,b}` with `v!=w` and open `v`. If `v` is the cut with
  `Q`, the opened territory is a pentagonal unicyclic cactus and the complement
  is a two-triangle cactus sharing `w`, for total `>1-delta`. Otherwise the
  opened territory is a tree and the complement is a `C3+C3+C5` cactus with
  its triangles sharing `w`, again giving `>(2-delta)-1>0`. This also covers
  the common-cut case.
- If `T` is central, let `w` be its cut with theta and `z!=w` its cut with
  `Q`. Give `w` and the intact theta to one territory. Give `T-w`, `z`, the
  intact pentagon, and all branches on that side to the other. Since `T-w` is
  an edge containing `z`, the second territory is a pentagonal unicyclic
  cactus. The total credit is `>1-delta>0`.
- If `Q` is central, let `w` be its cut with theta and `z!=w` its cut with
  `T`. Again keep `w` with the intact theta. The path `Q-w` contains `z`, so
  the other territory, consisting of `Q-w`, the intact triangle, and its
  assigned branches, is a triangular unicyclic cactus. The total credit is
  `>1+0>0`.

The connected and disconnected lists exhaust the shared-cut graph, and the
territory convention assigns every actual connector, cut, and hanging tree
exactly once. Induced superadditivity now proves positive surplus for
`Theta(1,2,2)+C3+C5` in every block-tree incidence.
