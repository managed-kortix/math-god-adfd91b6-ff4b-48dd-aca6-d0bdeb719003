# The `c=4` three-arm hub: a common rooted packet theorem

**Date:** 2026-07-26

## 1. Common structure and result

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sec(pi/5)-1=sqrt(5)-2.
```

The four final marked `G6PP` roots L13--L16 are not four different cores.
Their common `T^6P_0` incidence tree has four cut nodes and the following
form. There is a hub cut `x`, the pentagon `P_0` meets `x`, and for
`i=1,2,3` there is an arm

```text
x -- R_i -- y_i -- L_i,
```

where `R_i` and `L_i` are triangles, `R_i` is the router, and `y_i` is the
outer arm cut. Apart from the displayed cuts, the cyclic blocks are disjoint.
Thus the six triangles are `R_1,L_1,R_2,L_2,R_3,L_3`, and the four rooted
orbits are represented by

```text
x,  y_1,  a private vertex of L_1,  a private vertex of R_1.
```

Arbitrary finite rooted trees may be attached at every core vertex. A further
tree interface may be rooted at the marked vertex; this includes the clustered
side of a connector after its last bridge to a remote pentagon has been cut.

**Theorem 1 (root-carrying arm decomposition).** Choose an arm containing the
marked root; if the root is `x`, choose any arm. Keep `P_0` and that complete
arm, and open each of the other two router triangles at `x`. This gives an
induced vertex partition

```text
H_0 | H_1 | H_2
```

such that

1. `H_0` contains `P_0`, `x`, the root interface, and one complete two-triangle
   arm;
2. each `H_i`, `i=1,2`, is triangular unicyclic; and
3. uniformly over all attached trees,

```text
sigma(H_0)>2-delta,  sigma(H_1)>0,  sigma(H_2)>0.
```

Consequently the whole rooted `T^6P_0` hub satisfies

```text
sigma(T^6P_0 with the rooted interface)>2-delta.             (1.1)
```

If the remote side of the last bridge is a pentagonal unicyclic packet `P_1`,
then

```text
sigma(G)>2-2delta=6-2sqrt(5)>0.                              (1.2)
```

Thus one construction proves all four roots. It is stronger than the earlier
shared-pair ledger `7/4-delta`: the exact rooted phase of the retained arm gives
`2-delta`, while the other two arms contribute strictly positive packets.

## 2. The direct induced split

Assume the selected arm is arm 1. The packet `H_0` owns `x`, all vertices of
`P_0,R_1,L_1`, the marked interface, and every tree attached at one of those
owned vertices. For `i=2,3`, let `z_i` be the private vertex of the router
triangle

```text
R_i=x y_i z_i x.
```

The packet associated with arm `i` owns `y_i,z_i`, all vertices of `L_i`, and
all trees attached there. In the induced subgraph on this packet, the opened
router contributes only the edge `y_i z_i`. Hence this packet has exactly one
cyclic block, namely the triangle `L_i`; all its remaining material is a tree
attached to that triangle. The favorable triangular-unicyclic phase theorem
therefore gives

```text
sigma(H_i)>0.                                                (2.1)
```

This assignment is disjoint and exhaustive. It is induced because every
vertex is assigned once and each packet is replaced by the graph induced on
its assigned vertices. The two edges from `x` into each opened router cross
between packets and are discarded. Every off-core tree follows the unique
packet owning its root. In particular, no tree is split and no attachment is
specialized.

The marked interface lies in `H_0`: for the arm-cut, terminal-private, and
router-private roots this follows by choosing their arm, and for the hub root
it follows because `x` is always owned by `H_0`. This is the only point at
which the four rooted orbits differ.

## 3. Exact rooted Schur phase of the retained packet

It remains to prove the uniform estimate for `H_0`. Its cyclic spine consists
of a pentagon `P_0`, a router triangle `R`, and a terminal triangle `L`, with

```text
P_0 intersection R = {x},
R intersection L = {y},
P_0 intersection L = empty.
```

In particular, the two triangles intersect, so a vertex-disjoint Sachs
collection contains at most one triangle. The pentagon and `L` may occur
together; this contributes a positive real term and causes no phase loss.

For completeness, eliminate every rooted tree exactly on the positive
imaginary axis. If

```text
Z_F(t)=sum_M t^(|V(F)|-2|M|),
```

then a directed rooted-tree branch has message

```text
q_(u->v)(t)=t+sum_(w child of u) 1/q_(w->u)(t)>0.
```

Schur complementation replaces the activity at each spine vertex `v` by

```text
a_v(t)=t+y_v(t),  y_v(t)>=0,                                 (3.1)
```

and removes one common positive normalized determinant factor `K(t)`. Thus the
argument of the characteristic polynomial is exactly the argument of the
weighted grouped Sachs polynomial on the three-cycle spine; arbitrary trees
have not been approximated.

Let `S=V(P_0)`, and let `Z_J(a)` denote the signless matching partition of a
spine subgraph `J` with the activities (3.1). Since a pentagon has normalized
Sachs multiplier `+2i` and a triangle has multiplier `-2i`, the normalized
polynomial is

```text
Psi_(H_0)(t)/K(t)=A+2i(B-C),                                  (3.2)
```

where

```text
B=Z_(spine-S)(a)>0,
C=Z_(spine-V(R))(a)+Z_(spine-V(L))(a)>0,
A=Z_spine(a)+4 Z_(spine-(S union V(L)))(a)>0.                 (3.3)
```

The last term in `A` is exactly the admissible joint Sachs selection
`P_0+L`. There is no `R+L` term because the triangles meet at `y`, and no
`P_0+R` term because those cycles meet at `x`.

Let

```text
Z_5(t)=t^5+5t^3+5t
```

be the bare pentagon matching partition. There is a weight-dominating
injection

```text
Match(P_0) times Match(spine-S) -> Match(spine).
```

It sends `(M_0,M_1)` to `M_0 union M_1`. The two matchings use disjoint vertex
sets because `spine-S` omits the shared vertex `x`, so their union is a
matching. Restriction to the two vertex sets recovers the pair, so the map is
injective. Its source weight is computed with activity `t` on `P_0` and the
effective activities on `spine-S`; the image has the same unmatched vertices,
but uses `a_v>=t` on `P_0`. Therefore

```text
Z_spine(a)>=Z_5(t) B.                                      (3.4)
```

Using (3.3) and `C>0` now gives the exact strict comparison

```text
A-Z_5(t)(B-C)
 >=Z_5(t)C+4 Z_(spine-(S union V(L)))(a)>0.                 (3.5)
```

No relation among the attachment activities other than (3.1) is used.

Because `A>0`, the continuous phase tending to zero at infinity remains in the
principal right-half-plane chart:

```text
Theta_(H_0)(t)=atan(2(B-C)/A).
```

The isolated pentagon phase is

```text
theta_5(t)=atan(2/Z_5(t)).
```

If `B-C<=0`, then `Theta_(H_0)<=0<theta_5`. If `B-C>0`, divide
(3.5) by the positive quantity `A Z_5(t)` to get the same strict comparison.
Hence, for every `t>0`,

```text
Theta_(H_0)(t)<theta_5(t).                                  (3.6)
```

The signed Coulson identity and the exact pentagon value now give

```text
D(H_0)=s+(H_0)-s-(H_0)
      >D(C5)=-2delta.                                      (3.7)
```

The packet has three cyclic blocks, so `|E(H_0)|=|V(H_0)|+2`. Since
`s+(H_0)+s-(H_0)=2|E(H_0)|`, equation (3.7) yields

```text
sigma(H_0)=2+D(H_0)/2>2-delta.                             (3.8)
```

This proves the only spectral assertion in Theorem 1 with fully arbitrary
attachments.

## 4. The four roots and the final `G6PP` ledger

The same rule specializes as follows.

| rooted orbit | selected arm | opened routers |
|---|---|---|
| hub cut `x` | any arm | the other two |
| arm cut `y_i` | arm `i` | the other two |
| private vertex of `L_i` | arm `i` | the other two |
| private vertex of `R_i` | arm `i` | the other two |

After the strict last-bridge cut, the remote component containing `P_1` is
pentagonal unicyclic, with arbitrary attached trees, and satisfies

```text
sigma(P_1 packet)>=-delta.                                  (4.1)
```

Positive square energy is superadditive over induced vertex partitions.
Combining (2.1), (3.8), and (4.1) therefore gives

```text
sigma(G)
 >=sigma(H_0)+sigma(H_1)+sigma(H_2)+sigma(P_1 packet)
 > (2-delta)+0+0-delta
  =2-2delta
  =6-2sqrt(5)>0.                                           (4.2)
```

This argument simultaneously handles L13--L16 and every realization of their
attached trees. It neither opens a pentagon nor invokes a free multivariable
phase assertion for the full `T^6P_0` core. The finite incidence input is only
the common three-arm normal form; the attachment-uniform analytic input is the
three-cycle rooted Schur comparison (3.5).

## 5. Relation to the existing certificates

In canonical labels from the conservative last-bridge census, the hub is cut
`7`, the routers are `0,1,3`, their terminals are `2,4,5`, and `P_0=6`.
For L13 one may retain arm `(3,5)` and open routers `0,1`. For L14--L16 one may
retain arm `(0,2)` and open routers `1,3`. These are exactly the ownership
patterns in the existing sixteen-row verifier.

The earlier verifier credits the retained packet only by the established
weaker bound `sigma(TTP_0)>7/4`. The present theorem identifies why all four
rows have one proof: the retained `TTP_0` is always a rooted packing-one
three-cycle spine, so its exact Schur--Sachs phase gives the sharper uniform
bound `2-delta`. The router split is therefore the combinatorial half of the
certificate, and (3.5) is its attachment-uniform analytic half.
