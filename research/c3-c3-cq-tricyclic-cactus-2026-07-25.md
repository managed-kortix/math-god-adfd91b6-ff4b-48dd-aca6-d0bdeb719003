# The `C3,C3,Cq` tricyclic cactus family

## Theorem

Let `G` be a connected cactus of order `n` whose three cyclic blocks have
lengths `3,3,q`, where `q>=5` is odd.  Bridge blocks, the incidence of the
three cyclic blocks in the block-cut tree, and all attached trees are
arbitrary.  Then

`s^+(G)>n`.

In particular, the AKMPZ inequality holds for this family.  In fact the proof
below gives stronger bounds in most incidence classes.

Write

`D(H)=s^+(H)-s^-(H)`

and put

`delta_q=sec(pi/q)-1` when `q=1 mod 4`.  Notice that `0<delta_q<1`.
Since `G` is tricyclic, `|E(G)|=n+2` and

`s^+(G)=n+2+D(G)/2`.                                      (1)

We use three established inputs.

1. Induced-subgraph superadditivity:

   `s^+(H)>=sum_i s^+(H[V_i])`

   for every vertex partition `(V_i)`.
2. A connected cactus all of whose cycles are `3 mod 4`, with cycle-packing
   number at most two, has `D>0`.  Thus a triangular unicyclic packet of order
   `h` has `s^+>h`, and a bicyclic packet with two `3 mod 4` cycles has
   `s^+>h+1`.
3. For a connected bicyclic cactus with blocks `C3,Cq`, `q=1 mod 4`,

   `s^+>h+1-delta_q`.                                      (2)

   For a unicyclic `Cq` cactus with arbitrary trees,

   `s^+>=h-delta_q`.                                       (3)

The last estimate follows from tree elimination:

`Psi_H=K[Z_Cq(a)+2i]`, with every `a_v>=t`.

Hence its continuous phase is at most the phase of the bare `Cq`; Coulson
integration gives `D(H)>=D(Cq)=-2 delta_q`, which is (3).

## A partition fact for disjoint cyclic blocks

If selected cyclic blocks are vertex-disjoint, suppress all acyclic hanging
branches and look at the minimal block-tree joining the cycle-block nodes.
Cutting suitable bridge blocks partitions the vertices into connected induced
territories.  Every hanging tree is assigned to the territory containing its
attachment.  In particular:

- three vertex-disjoint cycles can be put into three unicyclic territories;
- an adjacent pair in the reduced three-node cycle tree can be put into one
  bicyclic territory and the remaining cycle into one unicyclic territory.

Here "adjacent" means that the path between the two cycle-block nodes contains
no third cyclic block.  Cutting a bridge edge creates vertex sets with exactly
that property, so the resulting territories really are induced; no spectral
edge-monotonicity is being used.

## Case `q=3 mod 4`

If the three cycles are not pairwise vertex-disjoint, their cycle-packing
number is at most two.  Every cycle has length `3 mod 4`, so the packing-two
Sachs theorem gives

`D(G)>0`, and consequently `s^+(G)>n+2` by (1).

If the three cycles are pairwise vertex-disjoint, partition `G` into three
connected induced unicyclic territories, one around each cycle.  Every packet
has a `3 mod 4` cycle, hence has positive asymmetry and positive square energy
strictly larger than its order.  Superadditivity gives

`s^+(G)>sum_i |V(G_i)|=n`.                                  (4)

This is why the apparently hostile packing-three Sachs term causes no gap.
Its multiplier is `(-2i)^3=8i`, opposite to the singleton terms, but it occurs
only when the three cycles are pairwise disjoint, exactly when the induced
unicyclic partition is available.

## Case `q=1 mod 4`: the easy partitions

First suppose all three cyclic blocks are vertex-disjoint.  Choose an adjacent
pair in their reduced block tree.

- If the pair consists of the two triangles, its bicyclic territory has
  `s^+>h+1`, while the `Cq` territory has `s^+>=h-delta_q`.
- If the pair consists of a triangle and `Cq`, (2) gives
  `s^+>h+1-delta_q`, while the remaining triangular territory has `s^+>h`.

In either case superadditivity yields

`s^+(G)>n+1-delta_q>n`.                                    (5)

The same argument applies if one triangle is disjoint from the union of the
other triangle and `Cq`: cut the bridge territory separating it, use (2) on
the mixed packet, and use the triangular unicyclic estimate on the singleton
packet.

There is one further incidence with vertex-disjoint triangles.  The long
cycle can meet both triangles, at necessarily distinct cut vertices `x_1`
and `x_2`.  Give `x_1` and the first triangle to one territory, and give the
remaining vertices to the other.  Assign every component hanging at `x_1`
off the long-cycle side to the first territory.  The two edges of `Cq`
incident with `x_1` are then the only cross edges.  The first induced territory
is connected and has only its triangle as a cycle.  The second is connected:
`Cq-x_1` is a path, and it has only the second triangle as a cycle.  Thus both
territories are triangular unicyclic cacti, and (4) again proves `s^+(G)>n`.

It remains only the incidence in which the two triangle blocks meet.  This is
the case naturally handled by product-subpartition phase domination.

## Two favorable triangles versus one bad cycle

Let the cycles be `T_1,T_2,Q`, where `Q=Cq`, and suppose `T_1` and `T_2`
share a cut vertex.  They therefore cannot occur together in a Sachs
subgraph.  Let `H` be the union of the cycle blocks and the unique block-tree
paths joining them.  Eliminate every tree off `H` by matching belief
propagation.  This gives a common positive factor `K(t)` and activities
`a_v=t+y_v`, `y_v>=0`, on `H`.

For a cycle collection `J`, write

`D_J=Z_{H-V(J)}(a)`

when the cycles in `J` are vertex-disjoint, and put `D_J=0` otherwise.  Set

`B=D_Q`, `A_j=D_{T_j}`.  Grouping Sachs terms gives

`Psi_G/K=R+iI`,                                             (6)

where

`R=Z_H+4D_{T_1,Q}+4D_{T_2,Q}`,                             (7)

`I=2(B-A_1-A_2)`.                                          (8)

There is no `-4D_{T_1,T_2}` term and no triple term, precisely because the
triangles meet.  Formulae (7)--(8) remain valid when one or both triangles
also meet `Q`, under the zero convention above.

Let `Z_q(t)=Z_Cq(t)`.  Partition the matchings counted by `Z_H(a)` according
as they use an edge between `V(Q)` and its complement.  The no-boundary-edge
class factors, including when a triangle shares a cut vertex with `Q`:

`Z_H(a)=Z_Q(a|_Q) B+E`, with `E>=0`.                        (9)

Since all activities on `Q` are `t+y_v`, coefficientwise monotonicity gives

`Z_Q(a|_Q)=Z_q(t)+L`, with `L>=0`.                          (10)

Combining (7)--(10),

`R-Z_q(t) I/2`
` =E+LB+4D_{T_1,Q}+4D_{T_2,Q}+Z_q(t)(A_1+A_2)>0`.          (11)

Every displayed summand is nonnegative, and the last term is strictly
positive.  If `theta_q(t)=Arg(Z_q(t)+2i)`, equation (11) says

`Im((Psi_G/K) conjugate(Z_q+2i))<0`.                        (12)

Indeed the left side of (12) is `Z_q I-2R`.  Both continuous arguments tend
to zero at infinity.  The strict inequality prevents their difference from
crossing a multiple of `pi`; its sign near infinity is negative by (11).
Consequently

`Theta_G(t)<theta_q(t)` for every `t>0`.                    (13)

Coulson integration reverses (13), giving

`D(G)>D(Cq)=-2 delta_q`.                                   (14)

Using (1),

`s^+(G)>n+2-delta_q>n`.                                    (15)

This is the requested product-subpartition domination: the isolated bad
`Cq` supplies the comparison phase, while each triangle contributes only
favorable terms in (11).  The potentially negative double-triangle real Sachs
term is absent exactly in this residual incidence; whenever it is present,
the preceding induced-territory partitions apply instead.

## Exhaustion of incidences

For `q=3 mod 4`, cycle packing is either at most two or all three blocks are
vertex-disjoint, covered respectively by the phase theorem and the three-way
partition.

For `q=1 mod 4`, either the triangles meet, covered by (6)--(15), or they are
vertex-disjoint.  In the latter case, `Q` meets both triangles, meets at most
one triangle, or meets neither.  The first alternative is the two-triangular-
territory partition; in the other alternatives a bridge cut separates a
single triangle from an adjacent bicyclic packet, or all cyclic blocks are
disjoint and the reduced cycle-tree adjacent-pair argument applies.  These
possibilities exhaust the block-cut tree of a cactus.

Thus every incidence and every attached-tree configuration is covered.
