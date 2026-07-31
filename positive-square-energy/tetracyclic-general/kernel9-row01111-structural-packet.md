# Kernel 9, row `(0,1,1,1,1)`: structural deletion packet

## Statement

Use the nonzero-bundle order

`03,04,12,14,23`.

Kernel 9 has multiplicities

`m=(1,2,1,2,2)`,

and the physical row in this note is

`q=(0,1,1,1,1)`.

Thus `P_03` is even, `P_12` is odd, and each of the doubled bundles
`04,14,23` has one odd and one even member. This packet covers the two hard
first-length realizations:

1. the all-`l1/l2` row
   `l_03=2`, `l_12=1`, and lengths `{1,2}` in each doubled bundle;
2. the same row with `l_12=3`.

Arbitrary rooted trees may be attached at arbitrary vertices. In both cases,

`s^+(G)>|V(G)|`.

In fact, after the deletion below the connected tricyclic remainder `H`
satisfies

`D(H)=tr(A(H)|A(H)|)=s^+(H)-s^-(H)>0`,

which is stronger than the requested `D(H)>-2`.

## The deletion

Use the row-adapted open path:

- in the all-`l1/l2` row, let `v` be the unique internal vertex of the
  length-two path `P_03`;
- in the `l_12=3` row, let `v` be either internal vertex of `P_12`.

Thus the two requested operations are respectively deletion on an internal
even path and deletion on the specified length-three path. Let `T` consist of
`v` and all rooted-tree branches attached at `v`, and put

`H=G-V(T)`.

The two sets are induced and partition `V(G)`. The graph `T` is a nonempty
tree, including the possibility `T={v}`, and hence

`sigma(T):=s^+(T)-|V(T)|=-1`.                                (1)

The remainder `H` is connected. In the first row, connectivity between `0`
and `3` is retained by

`0--4--1--2--3`.

In the second row, connectivity between `1` and `2` is retained by

`1--4--0--3--2`.

In each case the opened path remnants are rooted trees at its endpoints.

Deleting `v` removes one vertex and two core edges. Therefore the cyclomatic
rank drops from four to three. The same count remains true after all rooted
trees are included, so

`beta(H)=3`.                                                  (2)

## Classification of the remainder

The cyclic-block kernel of `H` is not one of the four 2-connected rank-three
kernels. In the all-`l1/l2` row it is the block chain

`D_04 vee D_14 -- P_12 -- D_23`,                              (3)

where `D_ij` denotes the two-path dipole in bundle `ij`, `D_04` and `D_14`
share the cut vertex `4`, and `P_12` is a bridge path from the second dipole to
the third. In the `l_12=3` row it is

`D_14 vee D_04 -- P_03 -- D_23`,                              (4)

where the surviving length-two `P_03` is now the bridge path. Equivalently,
after each two-path dipole is suppressed to one cyclic block, either remainder
is a tricyclic cactus with three cyclic blocks.

For the all-`l1/l2` row these three cycles have lengths

`1+2=3, 1+2=3, 1+2=3`.                                      (5)

Opening `P_12` in the second row removes that path from the cyclic core, while
the even `P_03` takes over as the bridge in (4). The opened path remnants and
every original rooted attachment are trees. Consequently (3)--(5) are the
complete cyclic classification in both requested rows: `H` has exactly three
cycles, all triangles.

The cycle-packing number of `H` is at most two. Indeed, the `04` and `14`
triangles share vertex `4`, so the three cycles cannot be pairwise
vertex-disjoint. No additional cycle can use the bridge path `P_12` or an
attached tree; in the second row the same statement holds with bridge path
`P_03`.

## Phase bound

The favorable packing-two phase argument applies with arbitrary attached
trees. For completeness, normalize the characteristic polynomial on the
positive imaginary axis by

`Psi_H(t)=i^(-|H|) det(itI-A(H))`.

In its grouped Sachs expansion, every matching partition is positive. Every
cycle has length `3 mod 4`, so a singleton cycle contributes a strictly
negative imaginary term. Since the cycle-packing number is at most two, a
Sachs subgraph contains zero, one, or two cycles. The zero- and two-cycle terms
are real. Hence, for every `t>0`,

`Im Psi_H(t)<0`.                                               (6)

The continuous Coulson phase therefore lies in the open lower half-plane, and
the signed Coulson identity gives

`D(H)=s^+(H)-s^-(H)>0>-2`.                                    (7)

This is the zero-hostile attached phase channel. The general attached-theta
estimate `D>=-4(sqrt(5)-2)>-2` would have enough numerical strength, but it
does not apply literally because the remainder in (3) has three cyclic blocks
rather than one theta 2-core. Equation (6) is the applicable, stronger phase
bound and avoids that scope error.

## Surplus ledger

For every connected graph `X`,

`s^+(X)=|E(X)|+D(X)/2`.

Using `beta(H)=3`, so `|E(H)|=|V(H)|+2`, equation (7) gives

`sigma(H)=s^+(H)-|V(H)|=2+D(H)/2>2`.                          (8)

Induced square-energy superadditivity, (1), and (8) now yield

`sigma(G)>=sigma(H)+sigma(T)>2-1=1>0`.                        (9)

Thus both the canonical all-`l1/l2` realization and its `l_12=3` mutation are
closed strictly, with arbitrary rooted trees. Every vertex, opened path
remnant, and attached branch is assigned exactly once; no unquantified use of
the tricyclic theorem and no physical-parity switching occurs.

## Boundary of this packet

The proof uses that the three doubled bundles have first-simple lengths
`{1,2}`. If one of those paths is increased by two, its dipole cycle can change
from `3 mod 4` to `1 mod 4`, and (6) no longer follows from the favorable
packing-two sign argument. The deletion remains structurally valid, but those
long doubled-bundle mutations require a separate mixed-phase or DNN packet.
