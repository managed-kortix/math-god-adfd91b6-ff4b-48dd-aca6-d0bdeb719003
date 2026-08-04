# Hexacyclic multiblock items 1--4: owner-exact closure

This note proves four owner-exact packet templates used by the exhaustive
rank-six multiblock ledger:

1. `Theta(1,2,r)+T^4`, `r>=2`;
2. `D+T^3+P`, where `D=Theta(1,2,2)`;
3. `D+D+T^2`;
4. `S_3+T^3`, where `S_3` is one of the canonical structural rank-three
   blocks (canonical doubled triangle class `111`, canonical doubled-`C4`
   class `111`, or one-long all-odd `K4`).

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
3. `sigma(TT)>1`, `sigma(D)>1`, `sigma(D+T)>2`, and
   `sigma(D+TT)>3` for the corresponding connected attached packets. The last
   two bounds include direct and nested shared-cut incidence.
4. A connected four-triangle shared-cut packet has credit greater than three.
5. The canonical opening of a doubled triangle or a one-long all-odd `K4`
   deletes one physical internal path vertex and its owned descendants as a
   tree. With two retained external triangles, the retained anchor has credit
   greater than three: it is respectively a four-triangle packet or `D+TT`.
6. A canonical doubled-`C4` class `111` block together with two triangles in
   arbitrary bridge-free direct/direct or direct/nested incidence has credit
   greater than one. This is the owner-exact retained-packet theorem proved in
   `pentacyclic-general/doubled-c4-111-two-triangles-retained-packet.md`: after
   opening the even connector, cutting the opposite connector separates the
   two doubled sides, and the two side credits total greater than two before
   the structural tree is charged. It includes opposite-side owners and an
   interior owner whose side is a diamond rather than a cactus.

For the two doubled families in item 4, the all-length DNN gate is applied
first. If a member of a doubled pair is noncanonical, the exact excess bounds
`229/120`, `31/20`, `1862/1000`, and `1662/1000`, together with the three
external triangle excesses, put the row at or below the rank-six DNN budget
five. Thus the structural argument below is invoked only after both doubled
pairs have their canonical physical lengths. No switching operation is used
to alter a physical length.

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

If `P` is a block of `K`, orient `P` away from `D`. Its entry cut and the first
exit cuts on the routes to `T_1,T_2` occupy at most three vertices of `P`.
Choose a fourth vertex `z`. Delete `z` with its complete owner class and retain
the path `P-z` in `A`. If the owner class of `z` contains `T_3`, it is a strict
triangular territory. Otherwise it is a nonempty tree `R`, with
`sigma(R)=-1`, and `T_3` is boundary-opened at its first cut from `A` as one
further tree `S`. In both alternatives `A` is an attached `D+TT` packet: the
pentagon has been replaced by an acyclic connector joining the selected
triangles to `D`. Therefore

`sigma(G)>3-1-1>0`.                                           (4)

This also covers the pentagon-between-triangles configuration. Only the entry
and the two selected exits are forbidden; there is no need to forbid the owner
of `T_3`, because if it equals `z` the opened territory improves from a tree to
a triangular territory. Repeated exits share their cut only in `A`. Every
boundary cut, connector remnant, and rooted descendant follows exactly one
owner, so all territories used above are induced, disjoint, and exhaustive.

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
induced. If it contains no triangle, it is a nonempty tree and has credit
`-1`. If it contains one or two triangles, its only cyclic blocks after the
opening are those triangles, so it has nonnegative credit (indeed it is
strict). Therefore

`k=0: sigma(A)+sigma(U)>1-1=0`,

while for `k=1,2` the sum is already strict from `sigma(A)>1+k` and
`sigma(U)>=0`. This proves

`sigma(G)>0`.                                                  (5)

The argument also covers a triangle lying between the diamonds or one triangle
nested beyond the other. The boundary cut occurs only in `A`; every other
vertex of the opened diamond, every complete downstream suffix, and every
rooted branch occurs only in `U`.

## 6. Item 4: `S_3+T^3`

After the noncanonical DNN gate in Section 1, first inspect the minimal subtree
from `S_3` to the triangles. If it contains an actual bridge, choose a farthest
one before making any structural opening. Its complete descendant suffix is a
nonempty all-triangle territory and is strict; its connected complement has
rank at most five and is nonnegative. Hence every positive-route incidence is
closed without paying a structural tree.

Now the subtree is bridge-free. Inspect the owner class of a canonical physical
opening of `S_3`. If it contains a triangle, performing that opening makes the
class a strict triangular territory and leaves a connected rank-at-most-five
nonnegative complement. Thus we may assume that no external triangle is owned
by an admissible structural opening.

The remaining incidence is bridge-free. Its block-cut incidence tree has
three external triangle nodes. Choose a triangle leaf `T_3` whose deletion
leaves the other two triangle nodes connected to `S_3`. Boundary-open `T_3`,
keeping its boundary cut upstream. The remainder of `T_3`, with every branch
rooted away from that cut, is a nonempty tree `S` with `sigma(S)=-1`.

For the canonical doubled triangle and the one-long all-odd `K4`, now perform
the canonical structural opening. The opened vertex and its complete
descendant set form a nonempty tree `R`; physical path remnants stay with the
retained side. The retained anchor `A` is respectively a four-triangle packet
or a `D+TT` packet, so `sigma(A)>3`. Thus

`sigma(G)>=sigma(A)+sigma(R)+sigma(S)>3-1-1>0`.                (6)

The doubled-`C4` requires a different partition. Two retained triangles can
have owners on opposite doubled sides. After the even connector is opened, the
result is then neither one four-triangle shared-cut cluster nor one `D+TT`
anchor; its available side estimate is only greater than two and cannot be
charged for two trees a second time. Instead, before making the structural
opening, let `H=G-S`. The graph `H` is exactly a canonical doubled-`C4` class
`111` block plus two triangles in bridge-free direct/direct or direct/nested
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
