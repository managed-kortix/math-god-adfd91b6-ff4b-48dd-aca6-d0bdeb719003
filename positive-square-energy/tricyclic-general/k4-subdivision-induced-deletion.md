# K4 subdivisions: the induced-deletion reduction

This note isolates exactly what the proposed induced deletion proves. It does
not use the false inequality `s^+(G) >= MaxCut(G)`, and it does not claim an
unverified DNN classification.

## Setup

Let `B` be a subdivision of `K4`, with branch vertices `1,2,3,4`. Write
`P_ij` for the six branch paths and `l_ij >= 1` for their lengths. Arbitrary
rooted trees may be attached at vertices of `B`. Put

`sigma(H) = s^+(H) - |V(H)|`.

We use induced superadditivity and the following established attached-theta
credits.

1. A nonempty tree `T` has `sigma(T) = -1`.
2. A bipartite attached theta has `sigma = 1`.
3. If both odd cycles of an attached nonbipartite theta have length `3 mod 4`,
   then `sigma > 1`. Indeed, every imaginary singleton-cycle term in the
   normalized Sachs expansion is negative, while the even-cycle term is real;
   hence `D=s^+-s^->0` and `sigma=1+D/2>1`.

The third statement is the zero-hostile channel of the attached-theta proof.

## Induced-deletion lemma

Choose an edge `ab` of the suppressed `K4` for which `l_ab >= 2`, and choose
any internal vertex `v` of `P_ab`. Let `T` consist of `v` and the entire rooted
tree attached at `v`. Put `H=G-V(T)`.

The sets `V(T)` and `V(H)` partition `V(G)` and induce their respective
graphs. The graph `T` is a nonempty tree. The graph `H` is connected: deleting
`v` opens `P_ab`, and its two remnants become trees attached at `a` and `b`.
Its unique cyclic block is the theta between the other two branch vertices
`c,d`, with path lengths

`x = l_cd`,

`y = l_ca + l_ad`,

`z = l_cb + l_bd`.                                      (1)

All other vertices of `H` lie in rooted trees attached to this theta.
Consequently, if this theta has `sigma(H) >= 1`, then

`sigma(G) >= sigma(H) + sigma(T) >= 1-1 = 0`.             (2)

The inequality is strict whenever `sigma(H)>1`.

Thus every such deletion proves `s^+(G)>=|V(G)|` when the three numbers in
(1) have one of the following two parity types:

- `x,y,z` have the same parity (the theta is bipartite);
- they do not have the same parity, and both odd members among
  `x+y,x+z,y+z` are `3 mod 4` (the theta has no hostile odd cycle).

This criterion is exact for what follows from the three credits above. In the
second line, exactly two of the three pair sums are odd.

There is a useful intrinsic classification of the first line. Call one of the
four branch triangles even or odd according to the parity of the sum of its
three path lengths. The number of odd branch triangles is even, since every
edge occurs in exactly two of them. For deletion on `P_ab`, the theta in (1) is
bipartite exactly when the two branch triangles containing the complementary
edge `cd` are even. Hence:

- if all four branch triangles are even, deletion on every subdivided path
  leaves a bipartite theta;
- if exactly two branch triangles are even, they share a unique edge `cd`, and
  the only bipartite-theta deletion is on the opposite path `P_ab` (provided
  that path is subdivided);
- if all four branch triangles are odd, no one-path deletion leaves a
  bipartite theta.

These are all parity patterns. The refinement from parity to residues modulo
four decides whether a nonbipartite deletion is favorable: its two odd cycle
lengths must both be `3 mod 4`.

## Residual condition

The induced-deletion argument leaves precisely the subdivisions satisfying the
following finite congruence obstruction:

> For every pair `ab` with `l_ab>=2`, let `{c,d}` be its complementary pair
> and form the triple in (1). The triple is not constant modulo `2`, and at
> least one of its two odd pair sums is `1 mod 4`.

This is a condition only on the six lengths modulo four together with the
distinction `l_ij=1` versus `l_ij>1` for residue-one paths. It is therefore a
legitimate finite parity sieve before any DNN estimate. It includes, for
example, the all-length-three subdivision: deleting any path leaves
`Theta(3,6,6)`, whose two odd cycles have length nine and are both hostile.
Hence induced deletion alone does not close every subdivision.

At the other extreme, if five paths are unsubdivided and the sixth has any
length at least two, deleting an internal vertex of the sixth path leaves an
attached `Theta(1,2,2)`. Its two triangles are favorable, so its margin is
strictly greater than one and (2) closes the subdivision strictly. This covers
both the one-edge-length-two and one-edge-length-three cases, and in fact every
one-edge subdivision length.

If all six lengths are one, the graph has a unique `K4` cyclic block. The
standalone `K4` packet lemma gives

`s^+(G) > |E(G)| = |V(G)|+2`,

also with arbitrary rooted-tree attachments.

## Why branch-vertex deletion is weaker

Deleting a branch vertex does leave a subdivided triangle on the other three
branch vertices, but the three opened incident paths become pendant trees.
Thus the complement is unicyclic, not bicyclic. The deleted branch territory
is a tree of credit `-1`, while a general attached odd cycle can have negative
`sigma`; there is no uniform margin capable of paying this loss. Deleting an
internal path vertex is the useful operation because it preserves a bicyclic
theta core.

## What remains to complete the K4-subdivision theorem

The complete theorem follows from this note plus either of the following
missing statements.

1. Prove the sharp K4-subdivision DNN bound on every congruence-obstruction row
   above; or
2. give an additional induced packet with enough credit for every obstruction
   row (the all-length-three row shows that the zero-hostile theta packet is
   insufficient).

The proposed assertion that DNN fails only for `K4` and one edge of length
three is not presently established and is unnecessary for those two residuals:
the `K4` packet closes the former, while the induced `Theta(1,2,2)` deletion
closes the latter. A complete proof must display and verify the DNN certificates
for all remaining congruence rows rather than cite that classification.
