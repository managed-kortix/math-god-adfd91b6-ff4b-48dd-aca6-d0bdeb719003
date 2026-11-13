# Exceptional doubled-`C4` orbit plus two triangles

## Theorem

Let `G` be the bridge-free shared-cut packet consisting of a doubled-`C4`
block in the exceptional eight-row kernel-automorphism orbit, with both doubled
pairs at their first-simple physical lengths, and two triangular blocks. The
two triangles may both be incident with the doubled-`C4` block, with repetition
of the owner cut, or one may be downstream from the other. Their legal first
owners are the four branch vertices and the interiors of the two even members
of the doubled pairs; in the nested form the downstream owner may be any
vertex of the upstream triangle. The two single connector paths may have
arbitrary lengths in their fixed opposite parities, and arbitrary rooted trees
may be attached at arbitrary vertices. Then

`sigma(G)=s^+(G)-|V(G)|>1`.

Thus this packet pays one deleted-tree unit with strict positive residual.
The result is uniform over all eight parity anchors: four lie in switching
class `110` and four in switching class `111`.

The phrase **first-simple doubled pairs** is a scope restriction, not a
switching-class label. In the notation below, each doubled pair has physical
lengths `{1,2}`. If a doubled
member is longer than first-simple, this theorem is not invoked; Section 6,
equations (8)--(9), of
`tricyclic-general/doubled-c4-switching-sieve.md` closes the physical row by
the all-length DNN bounds `1862/1000<2` and `1662/1000<2`, including arbitrary
rooted-tree attachments. Connector lengths are not restricted to their
shortest representatives.

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
Sachs expansion may be read directly with these positive activities.  Because
every cyclic block in `A_r` is a triangle, each selected cycle contributes
`-2i`. If the triangle packing number is at most two, the zero- and two-cycle
terms are real and every one-cycle term has negative imaginary part. Hence
`Im Psi(t)<0` for every `t>0`, and the signed Coulson identity gives

`D(A_r)=s^+(A_r)-s^-(A_r)>0`.                                 (2)

Since an attached `r`-triangle cluster has cyclomatic rank `r`,

`s^+(A_r)=|E(A_r)|+D(A_r)/2`

and `|E(A_r)|-|V(A_r)|=r-1`. Equation (2) proves (1).

We also need the following favorable-packet version of (1). Let `J` be a
diamond together with `k<=2` triangular blocks in one bridge-free shared-cut
incidence tree, with arbitrary one-root tree branches, and put `r=2+k`. Then

`sigma(J)>r-1`.                                               (2a)

The scope excludes an acyclic connector meeting several cyclic cores.  For
`k=0`, the positive-activity diamond state is `Psi_D=R+iI`, with `R>0` and
`I=-2(r+s)<0`, so the lower-half-plane/Coulson argument gives the attached-
diamond estimate.  For `k=1`, if the triangle has private activities `a,b` at
physical shared cut `u`, put `d=ab+1` and `e=a+b`.  The exact one-sum identity
is

`Psi_(D+T)=d Psi_D+(e-2i)Psi_(D-u)`.

Writing `Psi_(D-u)=R_u+iI_u`, the explicit deleted-diamond states have
`R_u>0`, `I_u<=0`, and hence

`Im Psi_(D+T)=dI+eI_u-2R_u<0`.

For `k=2`, the aggregate direct/direct and direct/nested formulas---not a
triangle-packing shortcut in the presence of the diamond's four-cycle---are
the exact theorem in
`diamond-two-triangle-exact-packet.md`.  That theorem proves strict negative
imaginary part for every positive core activity and covers arbitrary one-root
branches.  In all three cases the signed Coulson identity gives
`D(J)=s^+(J)-s^-(J)>0`; since `J` has rank `r`,
`sigma(J)=r-1+D(J)/2>r-1`. The strict credits supplied by (2a) are therefore
respectively `>1`, `>2`, and `>3`. This is the only noncactus side packet used
below.

## 2. Exact exceptional orbit and normalized opening

Label the doubled sides and single connectors by

`a,A': A--B`, `b:B--C`, `c,C': C--D`, `d:D--A`.

Record path parities in the order `(a,A',b,c,C',d)`, with `1` meaning odd.
The exceptional parity anchors are

`010011, 010101, 011010, 011100,`

`100011, 100101, 101010, 101100`.                             (3)

They form one orbit under genuine automorphisms of the physical doubled-`C4`
kernel, together with the compatible exchanges inside the two parallel-edge
fibres. The kernel has four vertex automorphisms and sixteen induced incidence
permutations. The orbit (3) splits into four switching-class-`110` anchors and
four switching-class-`111` anchors; no switching operation is used here.

Normalize the representative `010011` to the first-simple physical lengths

`(a,A',b,c,C',d)=(2,1,2,2,1,1)`.                            (4)

Thus `b` is the even connector, `d` is the odd connector, and `a,c` are the
even members of the doubled pairs. In a same-parity descendant, `b` has any
even length at least two, `d` has any odd length at least one, and the doubled
pairs remain exactly `{1,2}`. Choose an internal vertex `v` of `b`. Let `T`
consist of `v` and every component owned by `v`; under the residual hypothesis
these components are all trees. Put

`H=G-V(T)`.

The sets are induced, `T` is a nonempty tree, and

`sigma(T)=-1`.                                                (5)

The remnants of `b` are rooted trees. The two doubled sides have triangular
cyclic support, while `d` becomes the unique bridge path between them. Both
external triangles are retained: the residual hypothesis excludes owners in
the interior of an admissible connector opening.

For the normalized representative, the legal-owner set is

`L={A,B,C,D} union Int(a) union Int(c)`.                       (6)

There are exactly two bridge-free block-cut incidence types.

1. **Direct/direct.** The two triangle roots are an arbitrary ordered pair
   `(q_1,q_2) in L^2`; equality is allowed.
2. **Nested.** The first triangle has root `q in L`, and the second triangle
   has root at an arbitrary vertex of the first triangle.

These alternatives are exhaustive for a bridge-free block-cut tree with two
external block nodes. An owner in `Int(a)` or `Int(c)` is legal. Keeping that
owner and its complete descendant set on its side can make the induced side a
diamond rather than a cactus; the proof therefore uses (2a) in precisely that
case.

Every other anchor in (3) has the transported data: its even connector, odd
connector, and two even doubled members are the images of `b,d,a,c` under a
genuine kernel automorphism. The same automorphism sends (6) to its exact legal
owner set and transports the chosen opening and every owner class. This is a
physical graph-isomorphism transport, not a switching transport and not a
change of any path length.

## 3. Owner-exact structural split

Cut any actual edge `e` of the odd connector path `d`. The components of
`H-e` determine the two base sides. Assign every off-core component to the side
containing its unique owner. In a nested incidence, the complete first triangle
and all of its descendants follow its owner in `L`. Assign the two remnants of
`b` to their endpoint sides. This gives an induced vertex partition

`V(H)=V(H_1) disjoint union V(H_2)`

such that each `H_i` is connected. The two external triangles are distributed
between the sides. Write `rho_i` for the cyclomatic rank of `H_i`. Opening `b`
lowers the total rank by one, while cutting the bridge edge `e` does not lower
the sum of the side ranks. Therefore

`rho_1>=0`, `rho_2>=0`, and `rho_1+rho_2=4`.                  (7)

There are two structural possibilities. If neither side acquires the second
route through an interior doubled-side owner, each positive-rank `H_i` is a
triangular cactus and (1) gives `sigma(H_i)>rho_i-1`; a rank-zero side is a
nonempty tree and has `sigma(H_i)=-1=rho_i-1`.

If an interior owner creates the second route, one side is an attached diamond
with `k` of the two external triangles, for some `0<=k<=2`. Its rank is `2+k`
and (2a) gives credit `>1+k`. The opposite side is an attached triangular
cactus with the remaining `2-k` triangles, interpreted as a nonempty tree when
`k=2`; by (1) its credit is `>1-k` for `k<2`, and is `-1` for `k=2`. Hence in
all three cases the two side credits total strictly more than two:

`k=0: >1 + >1`, `k=1: >2 + >0`, `k=2: >3 + (-1)`.            (8)

The ordinary triangular-cactus case gives the same conclusion from (7), with
at least one positive-rank side strict. Thus induced square-energy
superadditivity gives

`sigma(H)>=sigma(H_1)+sigma(H_2)>2`.                          (9)

Finally apply induced superadditivity to
`V(G)=V(H) disjoint union V(T)`. Equations (5) and (9) yield

`sigma(G)>=sigma(H)+sigma(T)>2-1=1`.                         (10)

The partition is owner-exact. The vertex `v` and every descendant owned by it
occur only in `T`. Every other branch or internal-path owner lies in exactly
one component of `H-e`, and its complete descendant set follows it. A shared
cut is not copied. Each vertex of both even-connector remnants follows its
endpoint side. Thus `T,H_1,H_2` are pairwise disjoint and exhaustive, and every
territory is induced and connected.

## 4. Transport and all-length boundary

A genuine kernel automorphism sends every physical path in the normalized
proof to the corresponding physical path of any target anchor in (3). It
therefore transports:

- the even-connector opening and odd-connector cut;
- the two even doubled members and legal-owner set;
- direct/direct and nested incidence, including repeated owners;
- all connector vertices, rooted trees, shared cuts, and the three induced
  territories.

Square energy and vertex count are graph-isomorphism invariants, so (10) holds
for all eight anchors. Arbitrary connector-only lengthening causes no change in
the proof: the even connector remains openable, the other connector remains a
bridge path after the opening, and the two intrinsic cycle lengths remain
`a+A'=c+C'=3`. If a doubled member is lengthened instead, the separate DNN
bounds `1862/1000<2` or `1662/1000<2`, relabelling, and fixed-parity
monotonicity close that row before this packet theorem is used.

Consequently there is no owner, incidence, connector-length, or rooted-tree
residual for the exceptional doubled-`C4` orbit plus two triangles.
