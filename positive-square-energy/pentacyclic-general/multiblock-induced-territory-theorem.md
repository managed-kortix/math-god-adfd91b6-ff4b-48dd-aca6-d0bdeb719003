# Pentacyclic multiblock induced-territory reduction

## Result

Let `G` be a finite simple connected graph of cyclomatic rank five. The
induced-territory argument below closes every multiblock DNN residual except
the following exact block/physical-row families:

1. `Theta(1,2,2)+C3+C3+C5`;
2. a canonical structural rank-three block plus `C3+C3`, namely canonical
   doubled triangle class `111`, canonical doubled-`C4` class `111`, or
   all-odd `K4` with exactly one long path.                 (R)

Thus the block-rank partitions

`1^5, 2+1^3, 2+2+1, 3+1+1, 3+2, 4+1`

are complete except for (R), which lies in `2+1^3` and `3+1+1`. The all-cycle
case `1^5` is the established pentacyclic cactus theorem. Bridges, connector
remnants, and rooted trees are arbitrary.

Write `sigma(H)=s^+(H)-|V(H)|`. For a vertex partition into induced
territories, pinching gives

`sigma(G) >= sum sigma(H_i)`.                              (1)

A nonempty tree has credit `-1`. We use the attachment-uniform packets already
proved in the bicyclic, tricyclic, tetracyclic, and cactus arguments:

| packet | credit |
|---|---:|
| connected bicyclic graph | `>=0` |
| two-triangle cactus or `Theta(1,2,2)` | `>1` |
| connected tricyclic graph | `>=0` |
| favorable tricyclic packet with `D>0` | `>2` |
| connected tetracyclic graph | `>=0` |
| attached `K4` | `>2` |
| triangular unicyclic cactus | `>0` |
| pentagonal unicyclic cactus | `>=2-sqrt(5)>-1` |
| triangle-pentagon cactus | `>3-sqrt(5)>0` |

Here a favorable rank-`r` packet with negative normalized Sachs phase has
`sigma>r-1`. In particular, a triangular packet with cycle-packing number at
most two has this credit. If its triangles are more dispersed, actual bridges
split them into lower-rank triangular territories. Every cut below is either
at an actual bridge or opens one specified block path; hence every territory
is induced and connected.

## Exact DNN residual sieve

For a cycle put

`epsilon_q=0` for even `q`, and
`epsilon_q=q tan^2(pi/(2q))` for odd `q`.

Thus `epsilon_3=1`, `epsilon_5=5-2sqrt(5)<2/3`, and
`epsilon_q<2/5` for odd `q>=7`. For a theta use its exact excess
`Delta(a,b,c)`. The established classification says

`Delta>1` exactly for `Theta(1,2,r)`,

the maximum is `Delta(1,2,2)=(sqrt(17)-1)/2`, and every other exceptional
theta has `Delta<4/3`.

The pentacyclic excess budget is four. Block additivity therefore leaves the
following rows and no others before structural packets are used:

| block ranks | residual after the exact available DNN ledgers |
|---|---|
| `2+1+1+1` | `Theta(1,2,r)+C3+C3+C3`; and `Theta(1,2,2)+C3+C3+C5` |
| `2+2+1` | `Theta(1,2,2)+Theta(1,2,2)+C3` |
| `3+1+1` | the canonical doubled-triangle, doubled-`C4`, and one-long all-odd `K4` structural rows with two triangles; and `K4+Q_1+Q_2`, where `epsilon(Q_1)+epsilon(Q_2)>1` |
| `3+2` | `K4+Theta(1,2,r)` |
| `4+1` | only the structural rank-four rows from the tetracyclic theorem, with one cycle |

For `2+1+1+1`, three cycle excesses can cross `4-Delta` only when all three
are triangles, or when the theta is the unique maximum diamond and the cycle
multiset is `C3,C3,C5`. For `2+2+1`, both theta excesses must be maximal and
the cycle must be a triangle. For `3+1+1`, every nonstructural rank-three row
has excess at most two. The sharper canonical bounds show that only two
triangles can accompany a structural row. For `3+2`, all canonical structural
rows other than the unsubdivided `K4` have excess below `12/5`, so even the
maximum theta keeps the sum below four. Every direct rank-four row has excess
at most three, and hence `4+1` is direct unless the rank-four proof itself is
structural.

## Territory convention

Delete the edges of a selected cyclic block. Every remaining component has a
unique first vertex on its block-cut-tree route to that block and is owned by
that vertex. When an internal path vertex is opened, its territory receives
that vertex, all components it owns, and all rooted branches based there. The
other paths in the 2-connected block keep the complement connected. A path
remnant is acyclic and stays whole with its endpoint territory.

When favorable cyclic blocks in a retained territory are vertex-disjoint, cut
actual bridges in their reduced block tree. Group two triangles whenever one
tree payment remains; the two-triangle territory has credit `>1`, while every
remaining triangle territory is strict. If a pentagon is present, group it
with a triangle, giving credit `>3-sqrt(5)>0`, and group two remaining
triangles to pay the opened tree. If the relevant cycles are not separated by
actual bridges, their packing number drops and the favorable Sachs packet has
the stronger credit `>r-1`. This is the induced-territory reinforcement rule
used in every row below.

## Closure of `2+1+1+1`

For `Theta(1,2,r)+C3+C3+C3`, write the theta paths as the edge `xy`, the
length-two path `xay`, and the path `P` of length `r`. Open an internal vertex
of `P`. The complement retains the intrinsic triangle `xayx`.

If the opened territory owns at least one external triangle, it is a strict
triangular territory rather than a tree. The complement is triangular and is
split, if necessary, into triangular territories. If it owns no external
triangle, it costs one tree. The complement contains four triangles. Packing
number at most three gives credit greater than one. Packing number four gives
actual bridge cuts; group two triangles and leave the other two as strict
unicyclic territories. In either case the tree is paid strictly.

The same opening does not uniformly close
`Theta(1,2,2)+C3+C3+C5`. If the opened territory is a tree, the complement has
profile `C3+C3+C3+C5` and must supply credit greater than one. This is valid
when an actual-bridge split realizes `TT+TP`, or when a shared packet gives the
same quantitative margin. It is not supplied by the presently quoted general
tetracyclic theorem, which gives only nonnegative credit. In particular, a
connected `T-P-T` subcluster plus the remaining triangle cannot be assigned
the formal ledger `TT+TP` without proving compatible cut ownership. Therefore
the whole block family (R), with arbitrary incidence, is retained fail-closed;
no topology row is silently discarded.

## Closure of `2+2+1`

Only two diamonds and a triangle remain. If an actual bridge separates the
diamonds, cut there. The two territories have profiles `diamond` and
`diamond+C3` in some order, hence credits `>1` and `>=0`. If the diamonds share
a cut, apply the complete two-diamond opening there. It gives an attached
diamond territory of credit `>1` and one nonempty tree. If the external
triangle follows the tree side, that side is a strict triangular territory and
there is no negative payment. If it follows the retained side, the retained
side has the diamond's two favorable triangles and the external triangle. At a
shared cut their packing number is at most two, so its credit is `>2`; when
dispersed, an actual bridge separates a two-triangle packet of credit `>1` from
a strict triangle. Either version pays the tree strictly.

## Closure of `3+1+1`

For the canonical doubled-triangle, doubled-`C4`, and one-long all-odd `K4`
rows, use the same internal path opening as in the tricyclic proof. It produces
one tree and a favorable bicyclic remainder of credit `>1`. If an external
triangle follows the opened side, that side becomes strict and the remaining
side is a connected tetracyclic or tricyclic graph, so this incidence closes.
If both external triangles follow the retained side, however, the available
general tetracyclic theorem gives that side only nonnegative credit. The base
credit `>1` is not known to survive the two attachments with the quantitative
margin needed to pay the opened tree. Formal regrouping into a two-triangle
packet can duplicate a shared cut. Therefore exactly these three canonical
physical families, in their no-routed-triangle incidences, remain fail-closed.

The no-long rows have an unsubdivided `K4` and two external cycles. Root the
reduced block tree at the `K4`. Keep the complete attached `K4` packet. Each
component away from it contains one or two of the external cycles. A
one-cycle component, after assigning its boundary cut to the `K4` side when
necessary, is either a unicyclic packet of credit greater than `-1` or a tree
of credit `-1`. A two-cycle component is either bicyclic with nonnegative
credit, or its boundary cycle is opened by ownership of the root cut and the
remaining side is unicyclic with credit greater than `-1`. There are at most
two components, so the attached-`K4` credit `>2` pays them strictly. This
covers every `K4+Q_1+Q_2` residual, including triangles, pentagons, common cuts,
and a cycle lying between the `K4` and the other cycle.

## Closure of `3+2`

Only `K4+Theta(1,2,r)` is residual. Across an actual bridge, the attached `K4`
has credit `>2` and the theta is a connected bicyclic graph of nonnegative
credit. At a shared cut `z`, keep `z`, the complete `K4`, and its branches in
one territory. The graph `Theta-z` is connected and has rank at most one: if
`z` is a theta endpoint it is a tree, and if `z` is internal to an arm it is
unicyclic. Assign all theta-side branches to it. Its credit is greater than
`-1`, so together with the attached-`K4` credit `>2` the total is positive.

## Closure of `4+1`

Every direct rank-four certificate absorbs the cycle because its excess is at
most three and `epsilon_q<=1`. In a structural rank-four row, the tetracyclic
proof opens one path and leaves either an attached all-odd `K4` packet or a
three-favorable-triangle packet, in both cases with credit `>2`, against one
tree.

If the external cycle lies on the opened side, that side is unicyclic and has
credit greater than `-1`, while the retained packet has credit `>2`. If it lies
on the retained side and can be bridge-separated, split it off; its credit is
greater than `-1`, so `>2-1-1>=0` is strict because both displayed packet
bounds are strict. If it shares a cut `z` with the retained packet, open the
cycle at `z`. The cycle-minus-`z` territory is a second nonempty tree, while
the favorable rank-three packet remains intact. Its credit `>2` pays both
trees strictly. This covers the two four-vertex structural states and the
kernel-9 structural subfamily; all other rank-four rows were direct.

## Exact residual

The DNN rows and induced-territory repairs close `2+2+1`, `3+2`, and `4+1`;
close the `Theta(1,2,r)+C3+C3+C3` branch of `2+1^3`; and close every direct row
and the unsubdivided-`K4` row of `3+1+1`. Together with the established `1^5`
theorem, the exact fail-closed multiblock residual is (R):

`Theta(1,2,2)+C3+C3+C5`, with arbitrary block-cut incidence, connectors, and
rooted trees; and the three canonical structural rank-three rows plus two
triangles when neither triangle is routed into an admissible opened territory.

Consequently the full pentacyclic frontier consists of these multiblock rows
and the single rank-five block program represented after suppression by the
118 classified kernels. Closing (R) requires quantitative retained-territory
credits `>1`: for `C3+C3+C3+C5` in the diamond tree-payment incidence, and for
the tetracyclic packets obtained by adjoining two triangles to the three
canonical favorable bicyclic remainders. A direct opening that always routes
one external triangle to the opened side would also close the latter rows.
