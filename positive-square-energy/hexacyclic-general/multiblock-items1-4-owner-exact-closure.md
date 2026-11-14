# Hexacyclic multiblock items 1--4: owner-exact closure

This note proves four owner-exact packet templates used by the exhaustive
rank-six multiblock ledger:

1. `Theta(1,2,r)+T^4`, `r>=2`;
2. `D+T^3+P`, where `D=Theta(1,2,2)`;
3. `D+D+T^2`;
4. `S_3+T^3`, where `S_3` is one of the structural rank-three blocks
   left after the all-length gate (first-simple doubled triangle class `111`,
   the exceptional doubled-`C4` eight-row automorphism orbit with first-simple
   doubled pairs, or one-long all-odd `K4`).

Here `T=C3`, `P=C5`, and arbitrary bridge connectors and arbitrary rooted
trees are allowed. For a graph `X`, put

`sigma(X)=s^+(X)-|V(X)|`.

The conclusion is `sigma(G)>0` in every one of the four families. In
particular, their owner-sensitive residual is empty.

## 1. Inputs and the owner convention

We use induced square-energy superadditivity and the following established
attachment-uniform facts.

1. Every connected graph of cyclomatic rank two through five has nonnegative
   credit.
2. A nonempty tree has credit `-1`; a triangular territory has positive
   credit; a territory containing only triangles and one pentagon, and at
   least one triangle, has positive credit.
3. `sigma(TT)>1` and `sigma(D)>1`.  More narrowly, a bridge-free
   shared-cut `D+T` packet with arbitrary one-root tree branches has
   `sigma(D+T)>2`, and the exact bridge-free shared-cut `D+TT` packet has
   `sigma(D+TT)>3`.  These statements do **not** allow an acyclic connector
   meeting several cyclic cores.  The `D+TT` input is the exact weighted-core
   theorem in
   `pentacyclic-general/diamond-two-triangle-exact-packet.md`; its direct and
   nested incidence forms and its arbitrary one-root branches are part of that
   theorem's stated scope.
4. A connected four-triangle shared-cut packet has credit greater than three.
5. The canonical opening of a doubled triangle or a one-long all-odd `K4`
   deletes one physical internal path vertex and its owned descendants as a
   tree. With two retained external triangles, the retained anchor has credit
   greater than three: it is respectively a four-triangle packet or `D+TT`.
6. An exceptional doubled-`C4`-orbit block with first-simple doubled pairs,
   together with two triangles in arbitrary bridge-free direct/direct or
   direct/nested incidence, has credit greater than one. This is the
   owner-exact retained-packet theorem proved in
   `pentacyclic-general/doubled-c4-111-two-triangles-retained-packet.md`: a
   genuine kernel isomorphism first transports the packet to normalized anchor
   `010011`; opening its even connector and cutting the opposite connector
   separates the two doubled sides, and the two side credits total greater
   than two before the structural tree is charged. The inverse isomorphism
   transports the legal-owner set and induced territories to all eight
   anchors, four in class `110` and four in class `111`. It includes
   opposite-side owners and an interior owner whose side is a diamond rather
   than a cactus; no switching operation is used.

For the two doubled families in item 4, the all-length DNN gate is applied
first. If a member of a doubled pair is longer than first-simple, the exact
excess bounds `229/120`, `31/20`, `1862/1000`, and `1662/1000`, together with
the three external triangle excesses, put the row at or below the rank-six DNN
budget five. Thus the structural argument below is invoked only after both
doubled pairs have their first-simple physical lengths. For doubled `C4`, the
two connectors remain arbitrary in their fixed opposite parities. No
switching operation is used to alter a physical length.

Fix a distinguished cyclic block `B`. Delete its edges. Every remaining
component meets `B` in at most one vertex; otherwise a route in that component
and a route in the 2-connected block `B` would belong to a larger cyclic
block. The first vertex of `B` on the block-cut route is the unique owner of
the component. Whenever a vertex is opened, it and all descendants owned by it
are assigned together. A boundary-open cycle keeps its boundary cut on the
upstream side and assigns the cycle minus that cut, with all descendants rooted
away from the cut, to the downstream territory.

These rules define the vertex partition before any credit is charged. Each
connector remnant and rooted branch follows exactly one owner, and a shared cut
is never copied.

## 2. Five-triangle packet lemma

### Lemma 2.1 (five triangular blocks)

Every connected cactus whose cyclic blocks are exactly five triangles, with
arbitrary connectors and rooted trees, has

`sigma>1`.                                                     (1)

**Proof.** Form the shared-cut clusters and their reduced bridge tree. If one
cluster contains `k>=2` triangles, take that complete cluster as one induced
territory. For `k=2,3,4` its credit is greater than `1,2,3`, respectively; for
`k=5`, the incidence-leaf opening theorem gives credit greater than two. Cut
all incident actual bridges and assign every bridge-only branch to an adjacent
cyclic territory. Every other resulting territory has positive cyclic rank at
most three and nonnegative credit. The total is therefore greater than one.

It remains that all five clusters are singletons. Choose a marked leaf of the
reduced tree and the nearest other marked node. Keep the path between them and
cut every other incident bridge. This is an attached two-triangle territory,
of credit greater than one. Assign every unmarked Steiner branch wholly to an
adjacent cyclic territory; each remaining cyclic component contains at least
one triangle and has nonnegative credit. The territories are connected,
induced, disjoint, and exhaustive, so superadditivity proves (1). QED.

## 3. Item 1: `Theta(1,2,r)+T^4`

Write the theta paths as the edge `xy`, the length-two path `xay`, and a path
`Q` of length `r`. Choose an internal vertex `v` of `Q`; for `r=2`, either
length-two arm may be designated as `Q`. Let `U` consist of `v` and its
complete owned descendant set, and retain both path remnants with the endpoint
side.

If `U` contains an external triangle, then `U` is an all-triangle cactus and
has positive credit. The connected complement has rank at most five and has
nonnegative credit. Hence `sigma(G)>0`.

Otherwise `U` is a nonempty tree, so `sigma(U)=-1`. The complement is a
connected five-triangle cactus: the intrinsic triangle `xyax` and all four
external triangles remain, and the remnants of `Q` are trees. Lemma 2.1 gives
credit greater than one. The two owner classes are induced, disjoint, and
exhaustive, and therefore

`sigma(G)>=sigma(G-U)+sigma(U)>1-1=0`.                         (3)

This includes repeated owners, nested triangles, and every positive connector.

## 4. Item 2: `D+T^3+P`

Root the minimal block-cut subtree at `D`. If an actual bridge has a triangle
on its descendant side, cut the farthest such bridge. Its complete descendant
suffix contains at least one triangle and at most the pentagon in addition, so
it is a positive triangular or triangle--pentagon cactus territory. The
connected complement has rank at most five and nonnegative credit. This closes
the graph. Notice that this formulation includes a pentagon lying between `D`
and a triangle: the suffix at the bridge then contains both blocks. It is not
legitimate merely to select a farthest bridge and call its suffix pentagonal.

We may therefore assume that no actual bridge has a triangle on its descendant
side. In particular, the complete hull from `D` to all three triangles is
bridge-free. If an actual bridge separates `P`, its descendant cyclic suffix
contains only `P`; cut off that complete side as a unicyclic territory `U`,
with `sigma(U)>-1`. In the remaining bridge-free `D+T^3` incidence, retain `D`
and two triangles and boundary-open a triangle leaf not needed to connect
them. The retained `D+TT` anchor has credit greater than three and the opened
territory is one tree. Thus this remaining side has credit greater than two,
and adding `U` is strict. Consequently it remains only to treat the completely
bridge-free cyclic hull.

We use the following elementary selection in its block-cut incidence tree.
Choose two triangles `T_1,T_2` so that the third triangle `T_3` is not an
internal block on either route from `D` to a selected triangle; equivalently,
prune a triangle leaf and retain two triangle nodes in the root component.
Let `K` be the minimal incidence subtree containing `D,T_1,T_2`.

If `P` is not a block of `K`, retain `K` as an attached `D+TT` anchor `A`.
At each component boundary outside `K`, keep the boundary cut in `A`. The only
outside cyclic demands are `P` and `T_3`. If they occur in separate components,
each component is boundary-opened once (or kept intact), and each has credit at
least `-1`. If they are nested in one component, open its first boundary cycle;
the resulting territory is either a tree or has one intact cycle, and has
credit at least `-1`; no second charge is needed. Hence there are at most two
units of boundary loss against `sigma(A)>3`.

If `P` is a block of `K`, do not retain `P-z` as a connector. Delete the five
edges of `P`, but retain all vertices, and for each `v in V(P)` let `F_v` be
the component of `G-E(P)` containing `v`. These five components are well
defined and partition `V(G)`. Indeed, every component of `G-E(P)` meets `P`,
because a shortest route from any of its vertices to `P`, stopped at its first
vertex of `P`, uses no edge of `P`. No component can meet `P` in two distinct
vertices `x,y`: choose an `x-y` path in that component with no internal vertex
on `P`; adjoining this ear (a chord is allowed) to the 2-connected block `P`
produces a strictly larger 2-connected subgraph, contradicting maximality of
the block `P`. Thus every component has one unique owner in `V(P)`.

Mark `v` when `F_v` contains at least one of the four other cyclic blocks
`D,T_1,T_2,T_3`. If several cyclic blocks use the same cut of `P`, or are
nested beyond one another from that cut, they lie in the same `F_v` and give
one mark; their triangle counts are aggregated. Let the distinct marked
vertices, in cyclic order, be `c_0,...,c_(q-1)`, where `F_(c_0)` contains `D`.
Let `k` be the number of triangular blocks in `F_(c_0)`, and for `i>0` let
`r_i>=1` be the number in `F_(c_i)`. Since there are only the four blocks
`D,T_1,T_2,T_3`, `q<=4`, and

`k+sum_(i=1)^(q-1) r_i=3`.                                  (4a)

Moreover, `P in K` makes `P` an internal block on a route from `D` to at least
one selected triangle. Deleting the block node `P` therefore separates `D`
from that selected triangle. Hence `q>=2` and `0<=k<=2`.

Choose one edge of `P` in each of the `q` cyclic edge-arcs from `c_i` to
`c_(i+1)` (indices modulo `q`) and cut those `q` edges. The remaining graph on
`V(P)` has `q` nonempty consecutive path intervals `I_0,...,I_(q-1)`, each
containing exactly one marked vertex, say `c_i in I_i`. Put

`W_i=union_(v in I_i) V(F_v),        A_i=G[W_i]`.             (4b)

The sets `W_i` are disjoint and exhaustive. Each `A_i` is connected: every
`F_v` is connected and contains `v`, and the internal edges of the path
`P[I_i]` join their owners. Each is induced by definition. More explicitly,
an edge outside `E(P)` cannot join two different `F_v`, while the edges of `P`
with both ends in `I_i` are exactly the internal path edges of `A_i`; every
`P`-edge crossing two intervals has its endpoints in different territories
and is omitted automatically. Thus every unmarked `P` vertex and every rooted
branch owned by it occurs in exactly one territory, and no shared cut or
connector remnant is copied.

Let `H` be the minimal block-cut subtree on `D,P,T_1,T_2,T_3`. The present
case has no bridge between cyclic blocks. Deleting the block node `P` from `H`
shows that the cyclic blocks in each marked `F_(c_i)` form one bridge-free
shared-cut incidence subtree; any bridge on a route between two of them would
already be a bridge of `H` between cyclic blocks. Every displayed cyclic block
stays whole inside the unique sector containing its owner mark, even when
several blocks share that mark. All other material in `A_i`---including
`P[I_i]` and components based at its unmarked vertices---is a forest attached
to that shared-cut packet at individual roots.  Indeed, a component outside
the displayed cyclic packet cannot meet two of its core vertices: together
with a path inside the packet it would make a cycle and hence enlarge a
positive-rank block.  Bridges internal to those one-root trees are harmless
and are not being excluded by the cyclic-hull assumption.

Consequently `A_0` lies in the *narrow* bridge-free shared-cut `D+T^k` scope,
with arbitrary one-root tree branches, for `0<=k<=2`. There is no retained
multi-interface `P-z` router. For clarity, the three inputs are authenticated
separately and the first two are rederived here.  Orient every off-core tree
branch toward its root.  Its positive matching-partition ratio satisfies
`Q=t+sum 1/Q_child>0`; extracting all branch partitions leaves one common
positive real factor and replaces each core diagonal variable by an
independent positive activity.  Thus it is enough to analyze the weighted
core.

Label the diamond by edges `pq,pr,qr,ps,qs`, with `r,s` of degree two. Its
weighted normalized determinant and any one-root deletion have the forms

`Psi_D=R+iI,             Psi_(D-u)=R_u+iI_u`,

where

`R=pqrs+pr+ps+qr+qs+rs>0,       I=-2(r+s)<0`,

and, for every physical vertex `u`, `R_u>0` and `I_u<=0` (the four states are
`qrs+r+s`, `prs+r+s`, `pqs+p+q+s-2i`, and
`pqr+p+q+r-2i`).  For `k=0`, therefore, the weighted diamond curve remains in
the open lower half-plane.  Its continuous argument tends to zero at infinity;
the signed Coulson identity gives `Delta=s^+-s^->0`.  Since the diamond sector
has cyclomatic rank two, `sigma(A_0)=1+Delta/2>1`.

For `k=1`, if the triangle private activities are positive and `d=ab+1`,
`e=a+b`, the exact one-sum identity gives

`Psi_(D+T)=d Psi_D+(e-2i)Psi_(D-u)`,

and hence

`Im Psi_(D+T)=dI+eI_u-2R_u<0`

for every physical shared cut `u`.  The same branch compression and continuous
lower-half-plane Coulson argument gives `Delta>0`; rank three now yields
`sigma(A_0)=2+Delta/2>2`.  Because the sector hull is bridge-free, no hidden
path joins `D` to `T`: this is a shared-cut calculation, not the disputed use
of the same name for a graph joined through `P-z`.  For `k=2`, the exact
attached-`D+T+T` theorem cited in input 3 gives `sigma(A_0)>3`.  Thus in all
three cases

`sigma(A_0)>1+k`.                                             (4c)

For `i>0`, `A_i` is a bridge-free shared-cut cluster of `r_i` triangles with
arbitrary one-root tree branches.  Here `1<=r_i<=3`.  Eliminating those
branches gives independent positive activities and a positive common factor.
Every selected triangle contributes `-2i`; packing is at most two, so every
one-cycle term is negative imaginary while the zero- and two-cycle terms are
real.  The same lower-half-plane/Coulson argument therefore yields

`sigma(A_i)>r_i-1`.                                           (4d)

Set `h=q-1`.  Thus `h`, unlike an empty-sector count, is exactly the number of
non-`D` cyclic owner marks.  There are no empty sectors and no separate tree
charges: every one of the `q` cyclic intervals is nonempty and contains one
mark. Induced square-energy superadditivity and (4a)--(4d) now give

`sigma(G)>=sum_(i=0)^h sigma(A_i)`

`        >(1+k)+sum_(i=1)^h(r_i-1)=4-h=5-q>=1>0`.             (4)

Here `h in {1,2,3}`; the respective strict lower bounds are `>3`, `>2`, and
`>1`.  This includes repeated exits, several cyclic blocks at one cut,
direct or nested triangles, the pentagon-between-triangles configuration, and
the case in which `D` and `P` share their entry cut. In the last case that
physical cut and `D` simply belong to the single component `F_(c_0)`. Every
pentagon vertex, including a shared cut, is assigned to exactly one interval;
all edges between distinct sectors are precisely the selected boundary edges
of `P`; and every off-`P` component has its unique owner in one sector.

The rejected alternative is worth recording.  Retaining `P-z` produces an
acyclic graph with several cyclic-core interfaces, not a one-root tree
attachment.  The proposed universal lower-half-plane router extension is
false: a corrected all-subsets exact determinant expansion finds positive
independent-activity imaginary coefficients in 36 of the 84 bare router
isomorphism types (63 positive versus 9,010 negative coefficients); after
`z_v=t+y_v`, 81 positive coefficients survive.  Fifteen cores have a positive
activity-free constant (twelve `+6i`, three `+4i`).  Concretely, for the path
`P_4=x_0x_1x_2x_3`, identify the diamond degree-two vertex `r` with `x_0` and
attach one triangle at each of `x_0,x_3`.  At equal activity `t`, exact
expansion gives

`Im Psi(t)=6-86t^2-150t^4-66t^6-8t^8`,

whose activity-free term is `+6i` and whose sign changes.  This refutes that
proposed phase certificate, not by itself the router's square-energy
inequality.  Neither this proof nor any cited packet uses the false extension;
the sector partition is essential.

## 5. Item 3: `D+D+T^2`

If an actual bridge occurs in the minimal subtree on the four cyclic blocks,
cut a farthest one. A descendant all-triangle suffix is strict and its
rank-at-most-five complement is nonnegative. A suffix containing a diamond and
`k` triangles has credit greater than `1+k`, for `0<= k<=2`; its complement
contains the other diamond and the remaining triangles and is nonnegative
(indeed strict unless it has no remaining triangle). Hence every positive-route
incidence is strict.

Assume the four blocks form one shared-cut incidence tree. Root it at one
diamond `D_1`, and let `c` be the first cut on the route into the other diamond
`D_2`. Keep `c` upstream. Boundary-open `D_2` at `c`: if `c` has
diamond-degree three, `D_2-c` is a path; if it has diamond-degree two, transfer
one adjacent degree-three vertex, its edge to `c`, and its rooted branches to
the upstream side, and the two vertices left from `D_2` induce an edge. This is
the standard two-diamond opening, applied at the physical boundary of `D_2`.

Let `k` be the number of external triangles on the upstream side, so
`0<=k<=2`. The upstream territory `A` is an attached `D_1+T^k` packet and has
credit greater than `1+k`. The downstream territory `U` is connected and
induced and contains exactly `2-k` external triangles after the diamond is
opened. If `k=2`, it contains no triangle, so it is a nonempty tree and has
credit `-1`. If `k=1`, it contains one triangle and is strict. If `k=0`, it
contains two triangles and has nonnegative credit. The exact ledger is

| `k` | `sigma(A)` | `sigma(U)` | total |
|---:|---:|---:|---:|
| 0 | `>1` | `>=0` | `>0` |
| 1 | `>2` | `>0` | `>0` |
| 2 | `>3` | `-1` | `>2` |

Thus in every case

`sigma(G)>0`.                                                  (5)

The argument also covers a triangle lying between the diamonds or one triangle
nested beyond the other. The boundary cut occurs only in `A`; every other
vertex of the opened diamond, every complete downstream suffix, and every
rooted branch occurs only in `U`.

## 6. Item 4: `S_3+T^3`

After the longer-doubled-member DNN gate in Section 1, first inspect the minimal subtree
from `S_3` to the triangles. If it contains an actual bridge, choose a farthest
one before making any structural opening. Its complete descendant suffix is a
nonempty all-triangle territory and is strict; its connected complement has
rank at most five and is nonnegative. Hence every positive-route incidence is
closed without paying a structural tree.

Now the subtree is bridge-free. Inspect the owner class of the prescribed
physical opening of `S_3`. If it contains a triangle, performing that opening makes the
class a strict triangular territory and leaves a connected rank-at-most-five
nonnegative complement. Thus we may assume that no external triangle is owned
by an admissible structural opening.

The remaining incidence is bridge-free. Its block-cut incidence tree has
three external triangle nodes. Choose a triangle leaf `T_3` whose deletion
leaves the other two triangle nodes connected to `S_3`. Boundary-open `T_3`,
keeping its boundary cut upstream. The remainder of `T_3`, with every branch
rooted away from that cut, is a nonempty tree `S` with `sigma(S)=-1`.

For the first-simple doubled triangle and the one-long all-odd `K4`, now
perform the prescribed structural opening. The opened vertex and its complete
descendant set form a nonempty tree `R`; physical path remnants stay with the
retained side. The retained anchor `A` is respectively a four-triangle packet
or a `D+TT` packet, so `sigma(A)>3`. Thus

`sigma(G)>=sigma(A)+sigma(R)+sigma(S)>3-1-1>0`.                (6)

The doubled-`C4` requires a different partition. Two retained triangles can
have owners on opposite doubled sides. After the even connector is opened, the
result is then neither one four-triangle shared-cut cluster nor one `D+TT`
anchor; its available side estimate is only greater than two and cannot be
charged for two trees a second time. Instead, before making the structural
opening, let `H=G-S`. The graph `H` is exactly an exceptional-orbit
doubled-`C4` block with first-simple doubled pairs and arbitrary fixed-parity
connectors, plus two triangles in bridge-free direct/direct or direct/nested
incidence. The owner-exact retained-packet theorem in input 6 applies to the
whole induced territory and gives

`sigma(H)>1`.

Its proof internally opens the even connector, partitions at the opposite
connector, and charges the structural tree only once; opposite-side owners and
interior doubled-side owners are included. Therefore

`sigma(G)>=sigma(H)+sigma(S)>1-1=0`.                           (7)

For repeated direct owners, the common cut stays only in the retained
territory. For nested incidence, the upstream triangle, including the cut
leading to its child, stays retained; choosing an incidence leaf for `T_3`
ensures that no retained triangle is captured by `S`. The residual hypothesis
also ensures that neither retained triangle is captured by the internal
opening used in the doubled-`C4` packet theorem. Hence all territories in
(6)--(7) are connected, induced, disjoint, and exhaustive.

## 7. Theorem and exact residual

**Theorem.** Every connected rank-six graph in one of items 1--4 above
satisfies

`s^+(G)>|V(G)|`.

The proof is uniform over all physical path lengths in the stated rows, all
legal owners (including repeated and nested owners), arbitrary bridge
connectors, and arbitrary rooted-tree attachments.

**Packet residual statement.** Each of the four displayed templates contributes
no remaining owner, connector, incidence, or physical-length case. This is a
packet theorem, not an exhaustion of the rank-six DNN sieve. The complete
pre-sieve and residual accounting is in
`multiblock-items1-7-combined-theorem-audit.md`.
