# Arbitrary-r shared-triangle clusters: uniform surplus frontier

## Verdict

For a finite graph `X`, put

`sigma(X)=s+(X)-|V(X)|`,

where `s+(X)` is the sum of the squares of the positive adjacency
eigenvalues. Let `A_r` be a connected cactus whose cyclic blocks are exactly
`r>=1` triangles and whose triangles form one shared-cut cluster. Arbitrary
finite trees may be attached at arbitrary vertices.

The requested linear estimate does not follow from either proposed reset.
There are exact combinatorial obstructions to both decompositions:

1. a maximum-packing Voronoi partition can split triangles, so all cyclomatic
   credits cannot be summed; and
2. four-triangle packets cannot be packed as vertex-disjoint induced
   territories even in a common-cut bouquet.

What *is* proved for arbitrary `r` is the qualitative uniform statement

`sigma(A_r)>0`.                                                  (1)

Together with the small-packet and opening arguments, the strongest bound
certified by the present toolkit is

`sigma(A_r)>r-1` for `1<=r<=4`,

`sigma(A_r)>max(0,7-r)` for `r>=4`.                              (2)

The two formulas agree at `r=4`. This note proves (1), audits both proposed
resets, and identifies the additional kind of spectral input a linear theorem
would require. It does not assert that a linear inequality is false for the
graphs themselves.

The proof uses two established facts.

1. Positive square energy is superadditive on induced vertex partitions:

   `s+(G)>=sum_i s+(G[V_i])`.                                    (3)

2. If a connected cactus `H` has only triangular cyclic blocks and has cycle
   packing number at most one, then

   `s+(H)>s-(H)`.                                                (4)

Fact (4) is the packing-one case of the favorable-cycle Sachs phase theorem.
Its hypotheses allow arbitrary bridges and attached trees.

## 1. Maximum-packing Voronoi territories

Write `nu(G)` for the maximum number of pairwise vertex-disjoint cycles in
`G`. The following standard lemma is included to expose all bookkeeping.

**Lemma 2 (cycle territories).** Let `G` be connected and let
`C_1,...,C_k` be a maximum-cardinality collection of pairwise vertex-disjoint
cycles. Assign a vertex `v` to the lexicographically least pair

`(d_G(v,V(C_i)),i)`,

and let `G_i` be induced by the vertices assigned to `i`. Then the `G_i`
form an induced vertex partition, every `G_i` is connected and contains
`C_i`, and `nu(G_i)=1`.

**Proof.** The assignment is a partition. A vertex of `C_i` has distance zero
from `C_i` and positive distance from every disjoint `C_j`, so `C_i` is wholly
contained in `G_i`.

Let `v` be assigned to `i`, let `a=d_G(v,V(C_i))>0`, and choose a neighbor
`u` preceding `v` on a shortest path to `C_i`. Thus
`d_G(u,V(C_i))=a-1`. If `j<i`, assignment of `v` to `i` implies
`a<d_G(v,V(C_j))`; integrality and the one-Lipschitz property of distance give

`d_G(u,V(C_j))>=a>a-1`.

If `j>i`, then `a<=d_G(v,V(C_j))`, whence

`d_G(u,V(C_j))>=a-1=d_G(u,V(C_i))`,

and a tie is won by `i`. Therefore `u` is also assigned to `i`. Iteration
gives a path in `G_i` from every assigned vertex to `C_i`, proving
connectivity.

Finally, if `G_i` contained two vertex-disjoint cycles, those two together
with `C_j` for every `j!=i` would give `k+1` pairwise disjoint cycles in `G`.
This contradicts maximal cardinality of the chosen packing. Since `G_i`
contains `C_i`, its packing number is exactly one. QED.

The use of a *maximum* packing is essential. A merely maximal packing does not
justify the last paragraph.

## 2. What the Voronoi argument proves

Apply Lemma 2 to `A_r`, and write

`n_i=|V(G_i)|`, `m_i=|E(G_i)|`, `beta_i=m_i-n_i+1`.

Every cycle of an induced subgraph of a cactus is one of the original block
cycles: a new cycle would also be a cycle of `A_r`, and a cactus has no cycle
other than its cyclic blocks. Hence every cyclic block of `G_i` is a triangle.
The graph `G_i` is connected and has cycle packing number one, so (4) applies:

`s+(G_i)>s-(G_i)`.                                               (5)

Because `s+(G_i)+s-(G_i)=2m_i`, (5) gives

`s+(G_i)>m_i=n_i+beta_i-1`,

and therefore

`sigma(G_i)>beta_i-1`.                                          (6)

By (3) and the fact that the territories partition all vertices,

`sigma(A_r)>=sum_i sigma(G_i)>sum_i(beta_i-1)`.                  (7)

It remains to count the cycles retained by the territories. Since the `G_i`
are pairwise vertex-disjoint induced subgraphs, every original triangle is
retained by at most one territory. Some triangles can be split among several
territories, so only

`sum_i beta_i<=r`                                                (8)

is automatic. This is exactly where a direct attempt to prove (1) from (7)
fails.

The missing reverse inequality in (8) cannot be recovered from shared-cut
connectivity. Instead use the weaker consequence of (5) that does not count
all cycles:

`s+(G_i)>m_i>=n_i`,                                              (9)

because `G_i` is connected and contains a cycle. Summing (9) directly gives

`s+(A_r)>=sum_i s+(G_i)>sum_i n_i=|V(A_r)|`.                    (10)

Equation (10) proves (1), but gives no numerical margin depending on `r`.
Consequently the Voronoi method supplies a rank-independent sign theorem, not
a linear lower bound.

## 3. Exact obstruction to both proposed resets

The preceding calculation isolates the obstruction rather than hiding it.

Take a central triangle `T_0` and three triangles `T_1,T_2,T_3`, where `T_i`
meets `T_0` at its `i`-th vertex and the petals are otherwise disjoint. A
maximum packing consists of the three petals. In the Voronoi partition their
three shared vertices belong to three different territories, so `T_0` is
split. Thus

`sum_i beta_i=3<4=r`.                                           (11)

The four-triangle example alone invalidates the equality needed in (8), even
when the centers are a maximum packing. Thus no theorem summing *all* `r`
cyclomatic credits follows from the Voronoi lemma. The territory proof has no
conserved quantity that charges a split cycle to one owner. Its rigorous
universal output is (10), namely strict positivity. The strict inequalities in
(9) have no quantitative value in the cited phase theorem that can be summed
into a function growing with `r`.

There is a simpler exact obstruction to a universal four-triangle packet
partition. Let all `r` triangles share one cut vertex `x` and be otherwise
disjoint. This is a valid cactus and one shared-cut cluster; its incidence tree
is a star with center `x`. Any induced territory retaining a triangle must own
`x`. Since a vertex partition gives `x` to exactly one territory, at most one
territory can retain any triangle at all. In particular, when `r>=8` there is
no partition into two vertex-disjoint induced four-triangle packets. Grouping
four cycle nodes in the incidence tree does not produce graph territories,
because all groups demand the same cut vertex.

The central-triangle/three-petal gadget gives the complementary boundary
obstruction: a four-triangle packet can have three distinct cut vertices
leading to the rest of the incidence tree. Detaching it by private openings
can cost three tree territories, exactly consuming its certified credit `>3`.
Thus neither multiway nor binary-cut incidence trees admit the desired packet
reset from the existing unrooted `A_4` estimate.

## 4. Strongest conclusion currently justified

The investigation therefore yields the following rigorous verdict.

**Theorem 1.** For every `r>=1` and every connected `r`-triangle shared-cut
cluster with arbitrary attached trees,

`sigma(A_r)>0`.                                                  (12)

For `1<=r<=4`, the favorable-cycle and exceptional four-triangle arguments
give the stronger bound `sigma(A_r)>r-1`. For every `r>=4`, incidence-leaf
opening gives

`sigma(A_r)>7-r`.                                                (13)

Combining the two independent arguments gives the certified bound

`sigma(A_r)>max(0,7-r)` for `r>=4`.                              (14)

Here strict positivity persists at every larger rank. Formula (14), together
with `sigma(A_r)>r-1` for `r<=4`, is the strongest general uniform statement
justified by the available packet, phase, superadditivity, and Voronoi inputs.

No explicit positive constant independent of `r`, and no linear lower bound
in `r`, follows from these inputs: the Voronoi loss (11), the common-cut
bouquet, and the three-boundary four-packet gadget are exact obstructions to
the proposed deductions. This is an obstruction to the methods, not a graph
counterexample to a stronger spectral inequality. Establishing a linear bound
requires genuinely new information, for example either

1. a packing-one estimate retaining quantitative credit for cycles split by
   Voronoi boundaries; or
2. a rooted/boundary four-triangle inequality whose credit survives detaching
   up to three incidence branches.

## Conclusion

The decreasing recurrence is reset beyond rank seven only qualitatively: maximum-
packing Voronoi territories prove `sigma(A_r)>0` for every `r`. They cannot be
summed to a linear surplus because nonselected triangles may be split, already
in the central-triangle/three-petal incidence. Four-triangle packetization has
the same obstruction in boundary form. Hence the presently certified
arbitrary-r bound is (14), not a linear positive margin; a linear theorem
remains open and needs a boundary-sensitive spectral input absent from the
current toolkit.
