# Rank-seven removable-ear census theorem and exact audit

## Definitions

All multigraphs here are finite and loopless; parallel edges are distinct
physical edges. A multigraph is 2-connected when it has at least two vertices,
is connected, and deletion of any one vertex leaves a connected graph (a graph
with at most one remaining vertex is connected). Its rank is
`beta(G)=|E(G)|-|V(G)|+1`.

An open ear relative to a subgraph `H` is a path whose distinct endpoints are
in `H` and whose internal vertices are outside `H`. A one-edge ear is allowed.
A pair of parallel edges is a cycle of length two. These conventions are
essential at order two and in the presence of parallel edges.

## Lemma 1 (removable physical edge)

Let `K` be a loopless 2-connected multigraph with minimum degree at least three.
Then some physical edge `e` has `K-e` 2-connected.

### Proof

First suppose `|V(K)|>=3`. The standard open-ear theorem, with physical edge
copies distinguished, applies verbatim to loopless multigraphs: start with a
cycle and repeatedly add an open ear until all physical edges are present.
Equivalently, apply the usual proof to the incidence structure; a cycle may
have length two, and an unused edge between two old vertices is a one-edge ear.
Thus

`K=C union P_1 union ... union P_t`,

and every prefix is 2-connected. Since every vertex on `C` initially has
degree two, while every vertex introduced internally by an ear has degree two
when introduced, minimum degree at least three implies `t>=1`. The internal
vertices of the last ear occur in no later ear and consequently have degree two
in `K`. There are none. Hence `P_t` is one physical edge `e`, and the preceding
prefix `K-e` is 2-connected.

If `|V(K)|=2`, looplessness and 2-connectivity say that `K` consists of `m`
parallel edges. Minimum degree at least three gives `m>=3`; deleting any one
physical copy leaves at least two parallel edges and hence a 2-connected
multigraph under the stated convention. This also exhibits explicitly the
order-two base excluded by formulations of the ear theorem that require three
vertices. `QED`

## Lemma 2 (suppression and the inverse augmentation)

Let `e=xy` be supplied by Lemma 1, put `J=K-e`, and suppress every degree-two
vertex of `J`. The resulting multigraph `H` is loopless, 2-connected, has
minimum degree at least three, and satisfies `beta(H)=beta(K)-1`. Moreover `K`
is produced from `H` by exactly one augmentation emitted by
`research/rank-seven-kernel-frontier-census.py`.

### Proof

Only `x` and `y` can have degree two in `J`, because all other degrees are
unchanged and were at least three. Suppressing a degree-two vertex replaces
its two incident physical edges by one edge. It preserves `|E|-|V|`, and it
preserves 2-connectivity: deleting the suppressed vertex from the subdivision
model is the same as deleting an interior point of an edge, while deletion of
any other vertex has the same connected components before and after contracting
the resulting path.

No suppression creates a loop. Such a loop would mean that a degree-two vertex
has both incident edges to one vertex `z`. If another vertex existed, deleting
`z` would isolate it, contrary to 2-connectivity of `J`. If no other vertex
existed, `J` would have order two and both its vertices would have degree two,
so its rank would be one; this cannot be the rank-six graph arising below.
After all suppressions, every remaining degree is at least three. Also

`beta(J)=beta(K)-1`

and suppression preserves beta, proving the rank assertion.

It remains to match the code, including all parallel cases. If neither endpoint
is suppressed, `e` is an ear between two branch vertices of `H`. If exactly one
endpoint is suppressed, it is the interior of one physical edge of `H`, and
`e` joins that location to a branch vertex. If both are suppressed and lie on
distinct resulting physical edges, `e` joins their two interiors. Physical
parallel copies remain distinct locations because the generator indexes the
expanded physical-edge list.

The only remaining case is that `J` contains an `xy` edge and suppression puts
both endpoints in one resulting physical edge. Degree two in `J` forces the
local path to be `a-x-y-b`; restoring `e` gives two parallel `xy` copies. This
is precisely the generator's same-physical-edge branch, which replaces `ab` by
`a-x`, two copies of `xy`, and `y-b`. More than one retained `xy` copy would
use both incidences at each endpoint and disconnect this pair from any other
vertex, so there is no omitted parallel subcase. These cases exhaust the
endpoint degrees and are exact inverses of lines 70--103 of the generator.
`QED`

## Theorem 3 (formal rank induction)

For every integer `r>=2`, every loopless 2-connected multigraph of rank `r`
and minimum degree at least three is obtained from the order-two multigraph of
three parallel edges by `r-2` iterations of the following topological open-ear
operation: first subdivide zero, one, or two physical edges to create the chosen
endpoint locations, then join the two distinct locations by one physical edge;
when both locations lie in one physical edge, use the two-internal-vertex case
of Lemma 2. Retain only outcomes of minimum degree at least three. In the inverse
direction, delete a removable physical edge and suppress the resulting
degree-two vertices.

### Proof

Induct on `r`. If `r=2`, the degree sum gives

`3|V|<=2(|V|+1)`,

so `|V|<=2`; 2-connectivity requires `|V|>=2`, and rank two then forces exactly
three parallel physical edges. This is the order-two base.

Let `r>=3` and assume the assertion at rank `r-1`. Apply Lemma 1, delete its
edge, and suppress as in Lemma 2. The result is a loopless 2-connected
minimum-degree-three multigraph of rank `r-1`. (The exceptional order-two
degree-two graph considered in Lemma 2 has rank one, whereas `r-1>=2`.) By the
induction hypothesis it descends to the base. Reversing the final suppression
and edge deletion is exactly one of the endpoint-location ear augmentations
classified in Lemma 2, including the same-physical-edge and parallel-copy
cases. This appends one operation to the inductive construction. `QED`

## Theorem 4 (exhaustive rank-seven census)

Every loopless 2-connected multigraph `K` of rank seven and minimum degree at
least three occurs, up to isomorphism, in
`research/fixtures/rank-seven-kernel-frontier-census.json`.

### Proof

The degree sum gives

`3|V(K)| <= 2|E(K)| = 2(|V(K)|+6)`,

so `2<=|V(K)|<=12`. Choose `e` by Lemma 1 and form `H` by Lemma 2. Then `H` is
loopless and 2-connected, has minimum degree at least three, and has rank six.
The exact rank-six verifier independently regenerates every such `H` on orders
two through ten and requires literal equality with
`research/fixtures/rank-six-kernels.json`; this is the exhaustion checked by
`R6.audit()` in `research/rank-six-kernel-census-verifier.py`.

The rank-seven generator now applies every endpoint-location augmentation to
every row returned by that exact audit. Theorem 3 and Lemma 2 say one of those labelled
augmentations reconstructs `K`. The generator tests the defining predicates,
computes an exact canonical multiplicity code, and deduplicates canonical
codes. Therefore the regenerated set contains the isomorphism class of every
`K`. Conversely, every retained row is checked directly to have rank seven,
minimum degree at least three, and no cut vertex, so the generated set is exact,
not merely a superset. Literal canonical-byte equality then links that set to
the committed fixture. `QED`

## Verifier linkage and audit result

`research/rank-seven-kernel-frontier-census.py` calls the rank-six `R6.audit()`;
it does not trust or merely count rank-six fixture rows. That audit regenerates
the complete rank-six set, checks canonical forms and graph predicates, and
requires literal fixture equality. The rank-seven verifier then:

1. emits all four inverse cases in Lemma 2, with physical parallel copies
   separately indexed;
2. rejects loops and rows with wrong rank, order, degree, or vertex connectivity;
3. canonicalizes each multiplicity vector and takes exact set equality;
4. requires the order ledger
   `1,6,47,233,914,2270,4015,4495,3396,1391,365` (total `17,133`);
5. requires canonical byte equality with the committed fixture in both normal
   and optimized Python modes.

The fixture status is consequently
`complete-proved-removable-ear-exhaustion`. This theorem concerns only kernel
census completeness; it does not promote the rank-seven spectral frontier or
authorize any `STATE` change.

Run from the repository root:

```text
python3 research/rank-seven-kernel-frontier-census.py
python3 -O research/rank-seven-kernel-frontier-census.py
```
