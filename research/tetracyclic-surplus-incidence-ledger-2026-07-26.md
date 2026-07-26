# Quantitative tetracyclic surplus ledger for pentacyclic leaf deletion

## Purpose and conventions

Put `sigma(G)=s+(G)-|V(G)|`, write `T=C3`, `P=C5`, and let
`Q=Cq` with `q=1 mod 4`. Set

`delta_q=sec(pi/q)-1`, and `delta_5=sqrt(5)-2`.

This note extracts the strongest uniform margins supplied by the existing
tetracyclic proof ledger, incidence by incidence. These are certified proof
margins, not claims that the constants are optimal. All inequalities remain
valid with arbitrary connector trees and arbitrary trees attached at arbitrary
vertices.

The application is leaf deletion in a pentacyclic cactus. If the deleted
territory is a tree, then its surplus is `-1`. Thus every tetracyclic remainder
row with `sigma(R)>1` immediately gives

`sigma(G) >= sigma(R)-1 > 0`.

Bars separate shared-cut clusters. For a fully shared cluster, incidence means
the bipartite tree of cycle blocks and shared cut vertices. The ledger entries
used below are

- `sigma(T)>0`, `sigma(Q)>=-delta_q`;
- `sigma(TT)>1`, `sigma(TQ)>1-delta_q`;
- every bicyclic or tricyclic cactus has `sigma>=0`;
- `sigma(TTQ)>2-delta_q` when the two triangles share a cut;
- `sigma(TPP)>6-2sqrt(5)` in one shared-cut cluster;
- a favorable `r`-cyclic packet with cycle-packing number at most two has
  `sigma>r-1`.

## The `{TTTQ}` incidence table

Here `Q=Cq`, `q=1 mod 4`. The six disconnected cluster partitions and the two
fully shared incidence alternatives are exhaustive.

| Shared-cut incidence | Necessary refinement | Certified margin | Pays a tree cost of one? |
|---|---|---:|:---:|
| `T|T|T|Q` | a reduced-tree edge gives a `TQ / TT` two-two split | `sigma>2-delta_q=3-sec(pi/q)` | yes |
| `T|T|T|Q` | no such two-two split | `sigma>1-delta_q=2-sec(pi/q)` | no |
| `TT|T|Q` | none | `sigma>2-delta_q=3-sec(pi/q)` | yes |
| `TQ|T|T` | the path between the singleton triangles avoids the `TQ` node | `sigma>2-delta_q=3-sec(pi/q)` | yes |
| `TQ|T|T` | the `TQ` node lies on that path | `sigma>1-delta_q=2-sec(pi/q)` | no |
| `TTT|Q` | none | `sigma>1` | yes |
| `TT|TQ` | none | `sigma>2-delta_q=3-sec(pi/q)` | yes |
| `TTQ|T` | the two triangles in `TTQ` share a cut | `sigma>2-delta_q=3-sec(pi/q)` | yes |
| `TTQ|T` | incidence inside `TTQ` is `T-Q-T` at distinct cuts | `sigma>1` | yes |
| fully shared | some two designated triangles share a cut | `sigma>1` | yes |
| fully shared | no two triangles meet; `Q` has three triangle petals at distinct cuts | `sigma>0` | no |

### Derivation

For `TT|T|Q`, let `A=TT`, `B=T`, and `C=Q` in the reduced cluster tree. If
the `B-C` path avoids `A`, use the packets `TT` and `TQ`; their margins sum to
more than `2-delta_q`. If that path contains `A`, use the connected `A-C`
subtree as a shared-triangle `TTQ` packet and leave `B` triangular; the same
margin follows. The identical sum proves the `TT|TQ` row. The refined
`TTQ|T` row follows directly from the shared-triangle estimate.

For `TTT|Q`, delete a private non-connector vertex of `Q`. The remaining
three-triangle packet has cycle-packing number at most two and hence surplus
greater than two, while the deleted territory is a tree of surplus `-1`. This
gives `sigma>1`.

For four singleton clusters, a reduced-tree edge with two marked nodes on each
side necessarily separates `TQ` from `TT`; the packet sum is greater than
`2-delta_q`. Without such an edge, the general nearest-triangle construction
gives only `TQ`, `T`, and `T`, hence more than `1-delta_q`. Likewise, in
`TQ|T|T`, the two singleton triangles form a `TT` territory precisely when
their joining path avoids the marked `TQ` node; otherwise the direct ledger
only gives the weaker row.

For the distinct-cut `T-Q-T` incidence inside `TTQ|T`, apply the same cycle
sacrifice as in the middle-pentagon argument. If the connector from the remote
triangle enters `Q` at a private vertex, split that vertex from `Q`; this leaves
a `TT` territory on `Q-v` and a triangular territory on the connector side. If
the connector enters through one of the attached triangles, put that triangle
with the remote triangle and put `Q-x` with the other attached triangle. The
territories are again `TT` and `T`. Thus `sigma>1` in every entry position.

In a fully shared incidence, if two designated triangles share a cut, the
incidence-excess identity leaves at most two shared cuts on `Q`. Deleting a
private vertex of `Q` again leaves a favorable three-triangle packet, proving
`sigma>1`. If no triangles meet, incidence-tree acyclicity forces the three
distinct `Q`-petal cuts. Splitting `Q` into three paths gives three triangular
unicyclic territories. Their sum is strictly positive, but the triangular
unicyclic margin is not uniformly separated from zero, so the existing ledger
does not certify a positive constant in this row.

The remaining rows are direct packet sums. In particular, isolated triangular
packets contribute strictness but no fixed positive amount, so they cannot be
used to increase the displayed constants.

## The `{TTPP}` incidence table

The eight disconnected cluster partitions, together with the indicated
internal/reduced-tree refinements and the two fully shared alternatives, are
exhaustive.

| Shared-cut incidence | Necessary refinement | Certified margin | Pays a tree cost of one? |
|---|---|---:|:---:|
| `TTP|P` | the two triangles share a cut | `sigma>2-2delta_5=6-2sqrt(5)` | yes |
| `TTP|P` | incidence inside `TTP` is `T-P-T` at distinct cuts | `sigma>1-delta_5=3-sqrt(5)` | no |
| `TPP|T` | none | `sigma>6-2sqrt(5)` | yes |
| `TT|PP` | none | `sigma>1` | yes |
| `TP|TP` | none | `sigma>2(1-delta_5)=6-2sqrt(5)` | yes |
| `TT|P|P` | the path between the pentagons avoids the `TT` node | `sigma>1` | yes |
| `TT|P|P` | the `TT` node lies on that path | `sigma>2-2delta_5=6-2sqrt(5)` | yes |
| `PP|T|T` | the path between the triangles avoids the `PP` node | `sigma>1` | yes |
| `PP|T|T` | the `PP` node lies on that path | `sigma>0` | no |
| `TP|T|P` | the singleton `T-P` path avoids the `TP` node | `sigma>2(1-delta_5)=6-2sqrt(5)` | yes |
| `TP|T|P` | the `TP` node lies on that path | `sigma>1-2delta_5=5-2sqrt(5)` | no |
| `T|T|P|P` | a reduced-tree edge gives a mixed `TP / TP` split | `sigma>2(1-delta_5)=6-2sqrt(5)` | yes |
| `T|T|P|P` | a reduced-tree edge gives the split `TT / PP` | `sigma>1` | yes |
| `T|T|P|P` | no two-two split | `sigma>0` | no |
| fully shared | a triangle is a leaf cycle node of the incidence tree | `sigma>5-2sqrt(5)` | no |
| fully shared | neither triangle is a leaf; forced incidence path `P-T-T-P` | `sigma>1-delta_5=3-sqrt(5)` | no |

Numerically, the three recurring constants are

- `6-2sqrt(5)=1.527864045...`;
- `3-sqrt(5)=0.763932022...`;
- `5-2sqrt(5)=0.527864045...`.

### Derivation

For `TTP|P` with a shared triangle cut, add the shared-triangle packet margin
`2-delta_5` to the remote pentagon margin `-delta_5`. If the pentagon is instead
the middle block at two distinct cuts, sacrifice it into path fragments. The
resulting induced territories are either `TT` plus `P`, or `T` plus `TP`; both
give more than `1-delta_5`.

The `TPP|T` row is the one-cluster `TPP` bound plus a triangular packet. The
`TT|PP` row uses `sigma(TT)>1` and the nonnegative bicyclic bound for `PP`.
The `TP|TP` row adds two mixed bicyclic margins. Adaptive reduced-tree
packetization improves all three-cluster rows when the relevant path avoids the
third marked node. In `TT|P|P`, if the pentagon-to-pentagon path avoids `TT`,
it forms a nonnegative `PP` territory and the `TT` territory gives more than
one. If the path contains `TT`, join `TT` to one pentagon as a shared-triangle
`TTP` territory and leave the other pentagon separate; the sum is greater than
`2-2delta_5`. In `PP|T|T`, if the triangle-to-triangle path avoids `PP`, it
forms a `TT` territory while `PP` remains nonnegative, proving `sigma>1`. In
`TP|T|P`, if the path joining the singleton cycles avoids `TP`, it forms a
second `TP` territory, proving `sigma>6-2sqrt(5)`.

For four singleton clusters, any reduced-tree edge with two marked nodes on
each side gives either `TP / TP`, with margin `6-2sqrt(5)`, or `TT / PP`, with
margin greater than one. If there is no such edge, a leaf-triangle cut gives
one strictly positive triangular territory and one nonnegative tricyclic
territory; no uniform positive constant follows from the ledger. This includes
the earlier path argument: if neither triangle is a reduced-tree leaf, the
forced order is `P-T-T-P`, whose middle edge is a mixed two-two split.

For a fully shared cluster, a leaf triangle can be opened at tree cost one,
leaving a one-cluster `TPP` packet. Hence

`sigma>-1+(6-2sqrt(5))=5-2sqrt(5)`.

If neither triangle is a leaf, incidence-tree degree counting forces the
alternating path `P-T-T-P`. Opening a private vertex of a leaf pentagon costs
one and leaves a shared-triangle `TTP` packet, so

`sigma>-1+(2-delta_5)=1-delta_5=3-sqrt(5)`.

## Leaf-deletion-ready subclasses

Using only the audited ledger, the tetracyclic remainders that uniformly absorb
a deleted tree territory are exactly the rows marked `yes` above:

- `{TTTQ}`: the two-two-split subclass of `T|T|T|Q`; `TT|T|Q`; the
  triangle-path-avoids-`TQ` subclass of `TQ|T|T`; `TTT|Q`; `TT|TQ`; every
  `TTQ|T` incidence; and fully shared incidence containing a
  triangle-triangle cut;
- `{TTPP}`: every shared-triangle `TTP|P`; `TPP|T`; `TT|PP`; `TP|TP`; every
  `TT|P|P`; the path-avoidance subclasses of `PP|T|T` and `TP|T|P`; and every
  four-singleton incidence having a two-two split.

“Exactly” here refers to what follows from the present proof ledger. A `no` row
is not asserted to have actual surplus at most one; it means that the available
uniform packet estimates do not prove a margin greater than one. In particular,
strict triangular surplus cannot pay any fixed missing amount because it tends
to zero under growing star attachments.
