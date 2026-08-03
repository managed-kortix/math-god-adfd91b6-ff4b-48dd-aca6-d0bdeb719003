# Canonical doubled-`C4` class `111` plus two triangles

## Theorem

Let `G` be the bridge-free shared-cut packet consisting of a canonical
doubled-`C4` block in switching class `111` and two triangular blocks. The two
triangles may both be incident with the doubled-`C4` block, with repetition of
the owner cut, or one may be downstream from the other. Arbitrary rooted trees
may be attached at arbitrary vertices. Then

`sigma(G)=s^+(G)-|V(G)|>1`.

Thus this packet pays one deleted-tree unit with strict positive residual. No
change to the main manuscript is made here.

The word **canonical** is a scope restriction: in the notation below, both
doubled pairs have physical lengths `{a,A}={c,C}={1,2}`. Connector lengths are
arbitrary subject to class `111`. If any member of a doubled pair is longer
than canonical, this theorem is not invoked; Section 5, equations (8)--(9), of
`tricyclic-general/doubled-c4-switching-sieve.md` closes that physical row by
the all-length DNN bounds `1862/1000<2` and `1662/1000<2`, including arbitrary
rooted-tree attachments. Thus the owner-exact argument in Sections 2--3 below
is canonical-only.

## 1. Rooted triangular-cluster estimate

We use the following attached Sachs packet. If `A_r` is one shared-cut cluster
of `r` triangular blocks, with arbitrary rooted trees at its vertices, then for
`1<=r<=3`,

`sigma(A_r)>r-1`.                                             (1)

Here connectors and branches outside the shared cuts are trees and are included
in the packet. To recall the proof, eliminate every rooted tree toward the
cyclic core. This extracts a common positive factor and replaces the core
variable at `v` by an activity

`a_v=t+sum 1/Q_(u->v)>=t>0`.

The same factor is present after cycle vertices are deleted, so the grouped
Sachs expansion may be read directly with these positive activities. Every
triangle contributes `-2i`. If the triangle packing number is at most two, the
zero- and two-cycle terms are real and every one-cycle term has negative
imaginary part. Hence `Im Psi(t)<0` for every `t>0`, and the signed Coulson
identity gives

`D(A_r)=s^+(A_r)-s^-(A_r)>0`.                                 (2)

Since an attached `r`-triangle cluster has cyclomatic rank `r`,

`s^+(A_r)=|E(A_r)|+D(A_r)/2`

and `|E(A_r)|-|V(A_r)|=r-1`. Equation (2) proves (1).

We also need the following established favorable-packet version of (1). Let
`J` be an attached diamond together with `k<=2` triangular blocks in one
bridge-free shared-cut incidence tree, and put `r=2+k`. Then

`sigma(J)>r-1`.                                               (2a)

For `k=0` this is the attached-diamond estimate. For `k=1` it is the
concentrated `D+T` favorable rank-three estimate, and for `k=2` it is the
favorable rank-four `D+T+T` estimate. In each case the grouped normalized Sachs
phase is negative for every positive activity assignment, so arbitrary rooted
trees and either direct or nested shared-cut incidence are included. Hence
`D(J)=s^+(J)-s^-(J)>0`; since `J` has rank `r`,
`sigma(J)=r-1+D(J)/2>r-1`. The strict credits supplied by (2a) are therefore
respectively `>1`, `>2`, and `>3`. This is the only noncactus side packet used
below.

## 2. Canonical opening and exact owners

Label the doubled sides cyclically by

`a,A': A--B`, `c,C': C--D`,

and the single connectors by `b:B--C` and `d:D--A`. In class `111`, normalize
the canonical physical row so that

`{a,A'}={1,2}`, `{c,C'}={1,2}`,

`b` is odd and `d` is even. The connector `d` therefore has an internal
vertex. Let `v` be any internal vertex of `d`. Let `T` consist of `v` and every
component owned by `v`; under the residual hypothesis these components are all
trees. Put

`H=G-V(T)`.

The sets are induced, `T` is a nonempty tree, and

`sigma(T)=-1`.                                                (3)

The remnants of `d` are rooted trees. The two doubled sides have triangular
cyclic support, while `b` becomes the unique bridge path between them. Both
external triangles are retained: the residual hypothesis excludes owners in
the interior of an admissible connector opening.

For completeness, the legal-owner set is

`L={A,B,C,D} union Int(a_even) union Int(c_even)`,             (4)

where `a_even` and `c_even` are the physical length-two members of the two
canonical doubled pairs. There are exactly two block-cut incidence types.

1. **Direct/direct.** The two triangle roots are an arbitrary ordered pair
   `(q_1,q_2) in L^2`; equality is allowed.
2. **Nested.** The first triangle has root `q in L`, and the second triangle
   has root at an arbitrary vertex of the first triangle.

These alternatives are exhaustive for a bridge-free block-cut tree with two
external block nodes: both are children of the distinguished block node, or
one is the child of the other. Notice in particular that an owner in
`Int(a_even)` or `Int(c_even)` is legal. Keeping that owner and its complete
descendant set on its side can make the induced side a diamond rather than a
cactus. The proof below therefore uses (2a), not (1), in precisely that case.

## 3. Owner-exact structural split

Cut any actual edge `e` of the bridge path `b`. The components of `H-e`
determine the two base sides. Assign every off-core component to the side
containing its unique owner. In a nested incidence, the complete first
triangle and all of its descendants follow its owner in `L`. Assign the two
remnants of `d` to their endpoint sides. This gives an induced vertex partition

`V(H)=V(H_1) disjoint union V(H_2)`

such that each `H_i` is connected. The two external triangles are distributed
between the sides. Write `rho_i` for the cyclomatic rank of `H_i`. Opening `d`
lowers the total rank by one, while cutting the bridge `e` does not lower the
sum of the side ranks. Therefore

`rho_1>=0`, `rho_2>=0`, and `rho_1+rho_2=4`.                  (5)

There are now two structural possibilities. If neither side acquires the
second route through an interior doubled-side owner, each positive-rank `H_i`
is a triangular cactus and (1) gives `sigma(H_i)>rho_i-1`; a rank-zero side is
a nonempty tree and has `sigma(H_i)=-1=rho_i-1`.

If an interior owner creates the second route, one side is an attached diamond
with `k` of the two external triangles, for some `0<=k<=2`. Its rank is `2+k`
and (2a) gives credit `>1+k`. The opposite side is an attached triangular
cactus with the remaining `2-k` triangles, interpreted as a nonempty tree when
`k=2`; by (1) its credit is `>1-k` for `k<2`, and is `-1` for `k=2`. Hence in
all three cases the two side credits total strictly more than two:

`k=0: >1 + >1`, `k=1: >2 + >0`, `k=2: >3 + (-1)`.            (6)

The ordinary triangular-cactus case gives the same conclusion from (5), with
at least one positive-rank side strict. Thus induced square-energy
superadditivity gives

`sigma(H)>=sigma(H_1)+sigma(H_2)`

`        >2`.                                                 (7)

Finally apply induced superadditivity to `V(G)=V(H) disjoint union V(T)`.
Equations (3) and (7) yield

`sigma(G)>=sigma(H)+sigma(T)>2-1=1`.                          (8)

The partition is owner-exact. The vertex `v` and every descendant owned by it
occur only in `T`. Every other branch or internal-path owner lies in exactly
one component of `H-e`, and its complete descendant set follows it. A shared
cut is not copied: it remains in the same `H_i` as every block rooted there.
Each vertex of both `d` remnants follows its endpoint side. Thus `T,H_1,H_2`
are pairwise disjoint and exhaustive, and every territory is induced and
connected. Equation (8) is uniform over every direct/direct owner pair, every
nested owner, and arbitrary rooted-tree attachments. There is no residual case
for the canonical doubled-`C4` class `111` plus two triangles.
