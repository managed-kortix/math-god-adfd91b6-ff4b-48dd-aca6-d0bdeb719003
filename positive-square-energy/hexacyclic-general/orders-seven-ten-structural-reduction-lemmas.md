# Rank-six kernels of orders seven through ten: structural reduction lemmas

## Scope

This note records reductions that can replace a large direct parity census. It
does not assert the still-missing order-seven through order-ten rank-six kernel
theorem. The input is a loopless, no-cut-vertex multigraph `K` of cyclomatic
rank six and minimum degree at least three. A simple realization replaces each
edge `e` by an internally disjoint path `P_e` of length `l_e>=1`; arbitrary
rooted trees may be attached at every resulting vertex.

Write

`sigma(X)=s^+(X)-|V(X)|`.

We use induced-partition superadditivity of `s^+`, so that
`sigma(X)>=sum_i sigma(X[V_i])` for every vertex partition. A nonempty tree has
credit `-1`.

## Lemma 1 (top-order degree rigidity)

For an order-`n` rank-six kernel,

`sum_v (deg_K(v)-3)=10-n`.                                      (1)

Consequently the degree multisets at orders seven through ten are exactly

```text
n=7:  6,3,3,3,3,3,3;  5,4,3,3,3,3,3;  4,4,4,3,3,3,3,
n=8:  5,3,3,3,3,3,3,3;  4,4,3,3,3,3,3,3,
n=9:  4,3,3,3,3,3,3,3,3,
n=10: 3,3,3,3,3,3,3,3,3,3.
```

In particular these orders contain respectively at least `4,6,8,10` cubic
vertices. Thus the high-order branch is not an arbitrary sparse family: it is
cubic apart from total degree excess at most three.

### Proof

Rank six gives `|E(K)|=n+5`, hence

`sum_v (deg(v)-3)=2(n+5)-3n=10-n`.

Every summand is a nonnegative integer. Listing the partitions of `10-n`
gives the displayed rows.                                                   `□`

## Lemma 2 (physical edge opening and rank drop)

Let `e=ab` be a kernel edge with `l_e>=2`, and let `x` be any internal vertex
of `P_e`. Put in `T_x` the vertex `x` and the complete rooted tree based at
`x`, and put `H=G-V(T_x)`. Then:

1. `T_x` is a nonempty induced tree and `sigma(T_x)=-1`;
2. `H` is connected;
3. every component of `P_e-x` is a rooted tree attached at `a` or `b`;
4. the cyclic core of `H` is the realization of `K-e`, with degree-two
   vertices suppressed, and has cyclomatic rank five.

Therefore

`sigma(G)>=sigma(H)-1`.                                        (2)

In particular, any attachment-uniform lower-rank packet proving
`sigma(H)>=1` closes the original rank-six realization.

### Proof

The first and third claims are immediate from path ownership. Since `K` has no
cut vertex it is 2-vertex-connected, hence it has no bridge; thus `K-e` is
connected. Replacing its edges by paths and adding the two remnants of `P_e`
and rooted trees preserves connectivity, proving the second claim. Deleting an
internal path vertex removes one vertex and two edges, so `|E|-|V|+1` drops by
one. Suppressing degree-two vertices preserves cyclomatic rank. Finally apply
induced-partition superadditivity to `V(G)=V(H) dot_union V(T_x)`.             `□`

## Lemma 3 (uniform DNN deletion transfer)

In the setting of Lemma 2, let the cyclic part of `H` have `M` edges after all
subdivision lengths are retained. If it has a DNN certificate

`kappa(H)<=M+4+t`,                                             (3)

where `t` is the number of attached-tree edges in `H`, then `sigma(H)>=0`.
This alone does **not** pay the opened tree. If instead either

```text
kappa(H)<=M+3+t,                                               (4)
```

or an independent structural packet gives `sigma(H)>=1`, then the deletion
proves `sigma(G)>=0`.

Thus the proved rank-five kernel theorem, whose general guarantee is only
excess four and hence credit zero, cannot be cited by itself as a deletion
induction. A valid induction needs one unit of DNN slack beyond the rank-five
budget, or one explicit unit of spectral credit.

### Proof

A connected rank-five core with `M` edges has `M-4` vertices. From (3),

`s^+(H)>=2(M+t)-(M+4+t)=M-4+t=|V(H)|`.

Under (4), the same calculation gives `sigma(H)>=1`, exactly the unit needed
in (2). The stated structural alternative follows directly from (2).          `□`

## Lemma 4 (subdivision-or-canonical dichotomy)

Fix a kernel `K`. Every realization falls into exactly one of these branches:

1. some physical path has length at least two, so Lemma 2 gives a physical
   rank-five opening; or
2. every physical path has length one, so `K` is simple and the realization is
   the actual simple graph `K` (apart from rooted-tree attachments).

Consequently a deletion-induction proof needs lower-rank marked-edge packets
only for subdivided realizations. Its zero-subdivision base consists only of
the simple kernels, not all multigraph kernels.

In the frozen rank-six census, the numbers of simple kernels at orders
`7,8,9,10` are respectively

`17,33,25,18`.                                                (5)

The remaining `297,292,137,48` kernels contain parallel edges, and every
simple realization of such a multigraph necessarily subdivides all but at most
one member of each parallel bundle. Hence Lemma 2 is always available there.

### Proof

The dichotomy is tautological. In a simple graph, two parallel kernel edges
cannot both be realized as the same branch-to-branch edge, so in every bundle
of multiplicity at least two at least one member has an internal vertex. The
counts in (5) are an exact projection of the canonical fixture.               `□`

## Lemma 5 (marked-edge reduction is the right finite object)

Let `(K,e)` be a rank-six kernel with a chosen edge. Delete one copy of `e` and
suppress every resulting degree-two vertex. The output is a connected
rank-five multigraph, but it need not remain no-cut-vertex. Its block-cut tree
has total cyclic rank five, and all opened path remnants and all original
attachments occur only as rooted trees on that block-cut tree.

Therefore the induction target is not merely one of the 118 2-connected
rank-five kernels. It is a **marked rank-five block tree with two distinguished
attachment roots**, namely the endpoints of the opened path after suppression.
Any proposed reduction directly to the unmarked 118-kernel theorem omits this
interface data and is invalid unless it separately proves that `K-e` remains
2-connected.

### Proof

Connectivity and rank five are Lemma 2. Suppression can merge an endpoint into
an adjacent branch but does not remove the two path-remnant roots. Deleting an
edge from a 2-connected graph can create cut vertices, so the resulting cyclic
part must in general be decomposed into its blocks. Cyclomatic rank is additive
over those blocks.                                                             `□`

## Lemma 6 (rank-uniform equality template on a signed cycle quotient)

Suppose a kernel realization has the following quotient data for some `q>=3`:

1. there are `q` doubled bundles forming a cycle on quotient classes
   `X_0,...,X_{q-1}`;
2. each doubled bundle contains one odd path and one even path;
3. every other physical path joins two branch vertices assigned to the same
   signed quotient vector, so its transformed endpoint correlation is one.

Let `S` be the signed adjacency matrix of that quotient cycle and assume

`Q=I-(1/2)S` is positive semidefinite.                         (6)

Assign branch vectors by the signed quotient map. Then every singleton path
has zero cost and every doubled bundle has canonical cost

`1/3+2/3=1`.

The total canonical DNN excess is exactly `q`, and it is at most `q` for all
fixed-parity lengthenings. Hence this is an equality-budget template exactly
when the target rank has excess budget `q`.

For an ordinary unsigned cycle, (6) holds because the eigenvalues are
`1-cos(2 pi j/q)>=0`. More generally (6) holds for every signing: switching
reduces it to either the balanced cycle or the cycle with one negative edge,
whose eigenvalues are again `1-cos(theta_j)>=0` for the corresponding periodic
or antiperiodic angles.

### Proof

For endpoint correlation `-1/2`, an odd unit path costs `1/3`; the canonical
even path of length two has a PSD midpoint with endpoint-midpoint correlations
`1/2` and costs `2/3`. A transformed correlation of one gives zero path cost.
Summing gives `q`. Fixed-parity path monotonicity proves the all-length claim.
The spectral assertion follows from diagonalizing the balanced and unbalanced
signed cycle matrices.                                                         `□`

## Corollary 7 (the only budget-five cycle-quotient candidates)

At rank six, Lemma 6 can be an equality template only for `q=5`. A direct
structural projection of the frozen order-seven through order-ten fixture finds
exactly six kernels whose support contracts along singleton forests to a
five-cycle of doubled bundles:

```text
order 7:  K534, K548,
order 8:  K744, K756,
order 9:  K971,
order 10: K1133.
```

Their singleton and doubled supports are:

```text
K534:  singles 03,12;          doubles 06,16,25,34,45
K548:  singles 03,12;          doubles 06,15,23,45,46
K744:  singles 05,14,23;       doubles 07,16,27,36,45
K756:  singles 05,14,23;       doubles 07,16,25,34,67
K971:  singles 07,16,25,34;    doubles 08,18,27,36,45
K1133: singles 08,17,29,35,46; doubles 09,18,26,37,45.
```

For every physical row in which each doubled bundle is mixed odd/even and the
singleton signs are compatible with a signed contraction to the quotient,
Lemma 6 gives DNN excess exactly five at canonical lengths and at most five at
all same-parity descendants. These are natural equality rows and should be
removed symbolically before any numerical frontier search.

The sign compatibility condition is essential: contracting singleton edges
with signs requires that the sign product around every singleton cycle be
positive. Here the listed singleton supports are forests, so compatibility is
automatic for arbitrary singleton parities.

For order eight this projection has now been expanded into an exact finite
packet ledger in
`hexacyclic-general/order-eight-rank-six-structural-packets.md`. In particular,
K744 and K756 give twelve physical-row equality orbits, and all 3,594 supported
edge openings fall into nineteen exact marked block profiles. Among the 429
marked edges of the 33 simple excess-two kernels, 420 deletions remain
2-connected and only nine explicitly listed edges split into multiple cyclic
blocks. The accompanying verifier checks these statements directly from the
frozen kernel fixture. The ledger remains a reduction: it does not supply the
unit spectral credit required in Lemma 3.

## Lemma 8 (frontier reduction after deletion packets)

Fix a physical parity row. Assume:

1. its canonical shortest realization is covered by a DNN or structural
   certificate;
2. for each coordinate `e`, either its one-coordinate `+2` realization has a
   DNN certificate of excess at most five, or opening `P_e` invokes a marked
   rank-five packet with credit at least one.

Then every realization in the parity row satisfies `sigma(G)>=0`.

### Proof

If no coordinate grows, use (1). Otherwise choose a grown coordinate `e`. In
the DNN branch, the actual length vector is a coordinatewise same-parity
descendant of the `e` frontier, so path monotonicity applies. In the structural
branch, opening an internal vertex of `P_e` and Lemma 2 apply at its actual
length; the marked packet pays the deleted tree.                               `□`

## Consequences for a proof strategy

The lemmas suggest a proof ledger substantially smaller than a direct census
of all parity orbits and all coordinate frontiers:

1. prove marked rank-five deletion packets with one unit of credit for the
   block-tree outputs of `(K,e)`;
2. apply them to every noncanonical coordinate through Lemma 8;
3. remove the six signed-five-cycle equality families by Lemma 6;
4. handle the all-unit canonical bases of the `93` simple kernels in (5), then
   use the marked packets or ordinary DNN frontiers for their noncanonical
   parity/length rows, together with any marked-edge residuals whose rank-five
   remainder has no unit-credit packet.

This is a reduction, not a closure claim. In particular, the existing general
rank-five theorem gives nonnegative credit but not the unit credit required by
Lemma 2; that quantitative gap is the principal induction obligation.
