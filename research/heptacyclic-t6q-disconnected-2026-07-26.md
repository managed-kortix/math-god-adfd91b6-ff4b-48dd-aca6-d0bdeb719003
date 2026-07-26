# The disconnected shared-cut case for the heptacyclic residual `T^6 Q`

## Scope and status

This note proves one structural proposition for connected heptacyclic cacti. It
does not claim the heptacyclic theorem, does not address the other sharp-DNN
residual `T^5PP`, and does not address the case in which all seven cycles lie in
one shared-cut cluster.

For a graph `X`, write

`sigma(X)=s+(X)-|V(X)|`,

and write `T=C3`. Let `G` be a connected cactus whose seven cyclic blocks are
six designated triangles `T1,...,T6` and one cycle `Q=Cq`, where `q>=3`. The
designation is retained when `q=3`.

**Proposition.** If the shared-cut graph of the seven cyclic blocks is
disconnected, then

`sigma(G)>0`.

The statement permits arbitrary bridge connectors, arbitrary unmarked Steiner
branches, arbitrary connector lengths and entries, multiway cyclic cuts, and
arbitrary finite trees attached at arbitrary vertices.

## Inputs

Only the following established results are used.

1. **Induced superadditivity.** If `V(G)=V1 disjoint union ... disjoint union
   Vk`, then

   `sigma(G)>=sum_i sigma(G[Vi])`.

2. **Lower-rank cactus results.** Every connected tetra-, penta-, or
   hexacyclic cactus has positive surplus. Every connected bi- or tricyclic
   cactus has nonnegative surplus.

3. **Small shared triangular packets.** A connected cactus whose `r` cyclic
   blocks are triangles in one shared-cut cluster satisfies

   `sigma(T)>0`, `sigma(TT)>1`, and `sigma(TTT)>2`.

4. **Uniform shared triangular margin.** If `4<=r<=7` and the `r` triangular
   cyclic blocks of a connected cactus form one shared-cut cluster, then

   `sigma(T^r)>7-r`.                                      (1)

   Arbitrary attached trees are allowed. This follows by repeatedly opening an
   incidence-leaf triangle at a private vertex until four shared triangles
   remain: the four-triangle packet has surplus `>3`, and each opened nonempty
   tree has surplus exactly `-1`.

5. **Unicyclic hostile bound.** A connected unicyclic cactus with cycle `Cq`
   has nonnegative surplus unless `q=1 mod 4`. In the latter case

   `sigma(Cq-territory)>=-delta_q`,
   `delta_q=sec(pi/q)-1<1`.                               (2)

   This bound also permits arbitrary trees attached to the cycle.

6. **Arbitrary connector territories.** Contract every shared-cut cluster to
   a marked node in the block-cut tree, take the minimal subtree spanning the
   marked nodes, and suppress only unmarked degree-two nodes. If a leaf marked
   node is separated from the other marked nodes, the separation can be made
   on an actual bridge. All intervening connector vertices, unmarked Steiner
   branches, and hanging trees can be assigned wholly to one of the two sides.
   The result is a vertex partition into two connected induced territories,
   retaining exactly the prescribed cyclic blocks.

For clarity, (1) is the quantitative input only for `r=4,5,6` below. The
small-rank bounds in item 3 are not being inferred by extrapolating (1).

## Reduced-cluster-leaf proof

Let `R` be the reduced cluster tree. Since the shared-cut graph is disconnected,
there are at least two shared-cut clusters, hence at least two marked nodes in
`R`. Every leaf of the minimal marked subtree is marked, and a finite tree with
at least two vertices has at least two leaves. At most one leaf cluster contains
the designated block `Q`. Therefore `R` has a leaf cluster `A` not containing
`Q`.

All cyclic blocks in `A` are among `T1,...,T6`. Write their number as `r`, so
`1<=r<=6`. Because `A` is, by definition, a shared-cut cluster (represented by
one marked node of `R`), these `r` triangles form one shared-cut cluster.

Cut the first actual bridge from `A` toward the rest of the reduced tree and
apply the arbitrary-connector territory lemma. This gives an exact partition

`V(G)=V(A*) disjoint union V(B*)`                           (3)

into connected induced territories such that:

- `A*` has exactly the `r` triangular cyclic blocks of `A`, still in one
  shared-cut cluster;
- `B*` has exactly the other `7-r` cyclic blocks, including `Q`;
- every connector entry, connector remnant, Steiner branch, and hanging tree
  has exactly one owner.

In particular, `A*` is an admissible shared-triangular packet with arbitrary
attached trees, and `B*` is a connected `(7-r)`-cyclic cactus. Induced
superadditivity gives

`sigma(G)>=sigma(A*)+sigma(B*)`.                           (4)

The complete rank ledger is:

| `r` | bound for the all-triangle leaf `A*` | rank and bound for `B*` | result from (4) |
|---:|---|---|---|
| 1 | `sigma(A*)>0` | hexacyclic, `sigma(B*)>0` | `>0` |
| 2 | `sigma(A*)>1` | pentacyclic, `sigma(B*)>0` | `>1` |
| 3 | `sigma(A*)>2` | tetracyclic, `sigma(B*)>0` | `>2` |
| 4 | `sigma(A*)>3` by (1) | tricyclic, `sigma(B*)>=0` | `>3` |
| 5 | `sigma(A*)>2` by (1) | bicyclic, `sigma(B*)>=0` | `>2` |
| 6 | `sigma(A*)>1` by (1) | unicyclic with cycle `Q` | treated below |

Only the last row can contain a negative remote term. If `Q` is nonhostile,
item 5 gives `sigma(B*)>=0`, hence (4) is positive. If `q=1 mod 4`, then (2)
and the strict six-triangle margin give

`sigma(G)>=sigma(A*)+sigma(B*)>1-delta_q>0`.               (5)

This proves the proposition. No colored cluster partition or reduced-tree
topology census is used: the argument selects one `Q`-free reduced-tree leaf
and depends only on its triangle count.

## Exact connector and entry audit

The proof does not cut at an abstract cluster edge. The reduced edge leaving
`A` expands in the block-cut tree through bridge blocks only. Cutting one actual
bridge on that route separates the cyclic blocks of `A` from every other
cyclic block. If the expanded route contains a branch vertex, choose one side
as its owner and cut an actual bridge on each route assigned to the other side.
Every component outside the cyclic hull has a unique hull attachment, since two
attachments would create another cyclic block. Assign that component wholly to
the territory owning its attachment.

Consequently (3) is a genuine vertex partition, both parts are induced and
connected, and no connector vertex or entry is duplicated. An entry into `A`
may occur at a private triangle vertex, at a binary or multiway cyclic cut, on
a bridge-tree branch, or through another triangle of the leaf cluster. None of
these possibilities changes the cycles retained by `A*` or the fact that they
form one shared-cut cluster. They merely change the arbitrary tree structure
allowed in the margin (1). The argument therefore needs no entry-sensitive
subcase.

## Hostile self-audit

The following are the plausible failure points; each is discharged explicitly.

1. **A reduced-cluster leaf is not confused with an incidence leaf.** The cut
   is made outside the whole leaf cluster on an actual bridge. No individual
   triangle is asserted to be separable from the other cycles sharing its cut.

2. **A `Q`-free leaf always exists.** A nontrivial reduced tree has at least two
   leaves, while the single designated block `Q` belongs to exactly one
   cluster. This remains valid when `Q=T`: the designation distinguishes that
   block from `T1,...,T6`.

3. **The leaf side is concentrated.** Its `r` triangles comprise one
   shared-cut cluster by the definition of the marked node. Ordinary
   connectedness is not substituted for shared-cut connectedness.

4. **The complementary rank is exact.** Cutting bridge blocks destroys no
   cycle. Thus `B*` retains exactly `7-r` cyclic blocks and is connected by the
   territory construction, so the cited lower-rank theorem has the stated
   rank.

5. **Qualitative positivity pays no fixed loss.** For `r<=5`, the remote side
   is nonnegative or positive, so no hostile deficit is present. In the sole
   potentially negative row `r=6`, the numerical margin `sigma(A*)>1`, not an
   unspecified strict surplus, pays the explicit deficit `delta_q<1`.

6. **The unicyclic bound applies to the actual territory.** `B*` may contain
   arbitrary bridge trees and connector remnants, but item 5 is stated for the
   actual unicyclic graph with arbitrary attached trees, not for the bare cycle.

7. **Strictness survives.** Superadditivity in (4) is weak, but every row has a
   strict triangular input. In the hostile row the strict inequalities
   `sigma(A*)>1` and `delta_q<1` give the strict conclusion in (5).

8. **No vertex or tree is used twice.** The territory construction assigns
   every actual bridge segment, Steiner branch, entry vertex, and hanging tree
   to one owner before induced subgraphs are taken. Shared cyclic cuts internal
   to `A` remain wholly in `A*`; none is allocated to both sides.

9. **No hidden packing assumption occurs.** The margins `>3`, `>2`, and `>1`
   for four, five, and six shared triangles come from the uniform
   incidence-leaf opening theorem, whose four-triangle base includes the
   packing-three central-triangle/three-petal incidence.

10. **The conclusion is local in scope.** This note settles only the
    disconnected shared-cut case of the residual multiset `T^6Q`. It says
    nothing about fully shared `T^6Q`, disconnected or fully shared `T^5PP`, or
    nonresidual heptacyclic cycle multisets.

The hostile audit therefore leaves no connector, entry, concentration,
strictness, or fixed-deficit gap in the stated proposition.
