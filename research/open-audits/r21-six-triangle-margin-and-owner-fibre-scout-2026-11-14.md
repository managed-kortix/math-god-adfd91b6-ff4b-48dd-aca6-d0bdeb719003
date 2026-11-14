# R21 six-triangle margin and owner-fibre scout

Date: 2026-11-14. Status: **NONPROMOTIONAL / independent scout**.

## Verdict on the six-triangle question

Let `H` be a connected triangular block graph whose positive-rank maximal
blocks are exactly six literal triangles; bridge blocks and arbitrary finite
rooted trees are allowed. Then

```text
sigma(H)=s+(H)-|V(H)| > 1.
```

This is not a claim that the qualitative triangular-block theorem by itself
has margin one. The proof is a separate induced-territory decomposition using
the established quantitative `TT` packet and shared-cluster inputs.

Form maximal shared-cut clusters and contract their full supports in the
block-cut tree. Every reduced edge between cluster nodes contains an actual
bridge. If some cluster contains at least two triangles, cut every incident
reduced-tree edge on an actual bridge and retain that complete cluster as one
induced territory. For a cluster of size `2`, the arbitrary-incidence
bicyclic all-triangle theorem gives `sigma>1`; for sizes `3,4,5,6`, the
established shared-cluster floors are respectively `>2,>3,>2,>1`. Every
other resulting territory contains a triangle and is a connected triangular
block graph, so it has strict positive credit. Superadditivity gives total
credit greater than one.

If all six clusters are singletons, choose a marked leaf and the nearest other
marked node. Retain their unique reduced-tree path, which has no third marked
node, and cut every other incident reduced
edge on an actual bridge. Assign every off-path bridge-only branch wholly to
one adjacent owner. The retained territory is an arbitrary-connector
bicyclic cactus with two triangular blocks, hence has `sigma>1`. Every other
cyclic territory is triangular and strict positive. This again gives total
credit greater than one.

Thus there is no six-triangle counterexample and no long-connector limiting
obstruction to the strict `>1` statement. The decomposition is topology
uniform. The relevant quantitative source chain is

* `all-bicyclic-cacti/paper.tex`, equation `common-phase`: two triangles with
  arbitrary incidence and arbitrary attached trees have `s+>n+1`;
* `all-heptacyclic-cacti/paper.tex`, the shared-triangle recurrence:
  `A_3>2`, `A_4>3`, `A_5>2`, `A_6>1` (and `A_2>1`);
* `packing-two-square-energy/paper.tex`, Corollary
  `cor:triangular-block`: every connected triangular block graph containing a
  triangle has positive credit, including bridge blocks and arbitrary trees;
* its induced-subgraph superadditivity input.

The present conclusion is intentionally limited to exactly six triangles. It
does not extrapolate the finite shared-cluster recurrence to arbitrary rank.
`positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md`
contains a broader observation, but this scout independently establishes only
the six-triangle specialization from the quantitative inputs listed above.

## Exact and numerical scout

Run

```text
python3 research/six-triangle-margin-scout.py
python3 -O research/six-triangle-margin-scout.py
```

The executable checks all 11 integer partitions of six into shared-cluster
sizes. It also realizes the 19 unlabelled six-triangle shared-cut incidence
trees from physical adjacency. For each bare realization it computes the
integer characteristic polynomial and isolates every positive root with
multiplicity by rational Sturm arithmetic. The smallest bare surplus is the
six-triangle bouquet, with certified interval approximately `8`; every one of
the 19 exact rows is far above one.

The numerical probes are explicitly nonproof evidence. Six disjoint triangles
joined in a path by connector lengths `1,2,3,5,10,20,50` had observed surplus
between about `9.70` and `10.23`. Starting from the direct-connector chain and
attaching `k` leaves to every base vertex gave

```text
k=0:   10.2299502312
k=10:   6.3596460845
k=50:   5.6303222008
k=100:  5.4478327634
```

No numerical extrapolation is used in the proof.

## Physical theta owner-fibre theorem and fixture test

The analytic family does **not** come from extrapolating the literal `r=2`
fixture. The exact theta DNN classification in
`all-tricyclic-graphs/paper.tex`, equation `Delta-classification`, proves

```text
Delta(a,b,c)>1 iff (a,b,c)=(1,2,r) after sorting, r>=2.
```

Applied in the rank-seven `2+1^5` debit row, this supplies the
`Theta(1,2,r)+T^5` residual family uniformly in `r`. This is an analytic
classification of a physically given theta block; the symbolic residual label
alone remains no adjacency receipt.

The owner-fibre statement then takes the following physical input as a
hypothesis: `G` has a specified maximal vertex-biconnected block
`B=Theta(1,2,r)`, `r>=2`, and its other five positive-rank maximal blocks are
literal triangles. It does not need to rediscover arbitrary `r` from finitely
many fixtures. Under that hypothesis, the maximal-block ear argument below is
uniform for every `r>=2` and every block-cut incidence.

Run

```text
python3 research/r21-theta-owner-fibre-scout.py
python3 -O research/r21-theta-owner-fibre-scout.py
```

This second executable starts from materialized adjacency, runs Tarjan,
authenticates one maximal rank-two theta block and five literal external
`K3` blocks, and independently recovers theta path lengths. It tests `r=2`
and `r=3` fixtures in three owner patterns:

1. all five external triangles repeat one theta owner while the designated
   internal-arm fibre is acyclic;
2. all five form a nested descendant chain while that fibre is acyclic; and
3. two external triangles share the designated internal-arm fibre, while the
   remaining three occupy other theta owners.

For the authenticated maximal theta block `B`, it defines the physical
first-`B` fibre `F_x` as the component containing `x` in `G-E(B)`. The fixtures
verify on original vertices that these fibres are connected, induced,
disjoint, and exhaustive; that every fibre meets `B` exactly at its owner;
and that `G-F_x` is connected. They also reject a partial edge deletion in
place of `G-E(B)` and a symbolic profile without adjacency.

For a clean designated fibre, `F_x` is a nonempty tree and its complement
contains the intrinsic triangle from the untouched `1`- and `2`-arms plus all
five external triangles. Hence the complement is a six-triangle cactus and
the exact ledger is

```text
sigma(G) >= sigma(G-F_x)+sigma(F_x) > 1-1 = 0.
```

For a designated fibre containing `q>=1` external triangles, the whole fibre
is a connected triangular block graph and is strict positive. Deleting an
internal vertex from the `r`-arm lowers the theta rank from two to one, so the
connected complement has rank

```text
1+(5-q)=6-q in {1,2,3,4,5}.
```

For `q<=4`, a rank-at-most-five connected theorem supplies nonnegative credit.
For `q=5`, the complement is the retained intrinsic triangular unicycle and
is itself strict positive. Thus this branch is also strict. In particular, the
complete cyclic fibre must never be stripped and relabelled as a tree.

## Exact uniform owner-fibre theorem and provenance boundary

The owner-fibre lemma is general: if `B` is a maximal
vertex-biconnected block, every component of `G-E(B)` meets `B` once; otherwise
an outside path gives an open `B`-ear and contradicts maximality. Since
`B-x` is connected for every `x`, the complement of a complete fibre is
connected. For the physically given block `B=Theta(1,2,r)`, an internal vertex
of the designated `r`-arm exists for every `r>=2`; when `r=2`, designate one
of the two symmetric length-two arms explicitly. The tree/cyclic-fibre ledger
above therefore proves the owner split uniformly for all `r`, repeated owners,
and nested descendants. No finite-fixture extrapolation enters this theorem.

The `r=2,3` executable remains a semantic regression suite: it verifies the
physical definitions and catches partial-edge deletion, duplicated ownership,
and symbolic-label substitution. It is not the source of the arbitrary-`r`
quantifier. Conversely, the DNN residual classification supplies the analytic
family but does not itself materialize adjacency or prove the owner partition.
The two roles must not be conflated.

This scout neither changes `STATE` nor promotes a master theorem. Its exact
conditional conclusion is: **given** the stated physical maximal-block
inventory, the six-triangle margin and maximal-block fibre theorem close the
`Theta(1,2,r)+T^5` packet for every `r>=2`. Any integration into a larger
all-connected theorem must separately preserve the provenance that supplies
that physical block inventory and the surrounding bridge dispatch.
