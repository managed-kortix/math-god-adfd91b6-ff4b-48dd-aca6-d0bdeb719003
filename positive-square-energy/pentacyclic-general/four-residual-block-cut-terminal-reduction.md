# Four residual templates: exact block-cut terminal reduction

This note does not modify the main manuscript. It resolves the incidence
ambiguity in the four multiblock templates left by the induced-territory
reduction:

1. `Theta(1,2,2)+C3+C3+C5`;
2. canonical doubled-triangle class `111` plus `C3+C3`;
3. canonical doubled-`C4` class `111` plus `C3+C3`;
4. one-long all-odd `K4` plus `C3+C3`.

The conclusion is that "no routed cycle" is only a restriction on the owner
vertex in the distinguished block. It does not force a cycle to share that
vertex directly. The exact dichotomy is instead between a positive bridge
somewhere in the minimal block-cut subtree and an entirely shared-cut subtree.
The positive-connector cases split into already proved lower-rank packets. The
zero-connector cases are exactly the concentrated analytic packet families
listed below.

## 1. Ownership lemma

Let `B` be the distinguished cyclic block. Delete the edges of `B`. Every
component `C` of the remainder meets `B` in at most one vertex. Otherwise a
path in `C` between two vertices of `B`, together with a path in the
2-connected block `B`, would put the connecting edges in the same cyclic block
as `B`. Denote the unique meeting vertex, or the first vertex of `B` on the
block-cut-tree route when the component is bridge-separated, by `o(C)`.

Thus every external cyclic block `Q` has a unique owner `o(Q)` in `V(B)`. The
component it belongs to has precisely one of the following forms at `B`.

- `D` (zero at the root): the first external cyclic block is incident with the
  cut node `o(Q)`. The particular block `Q` may occur farther down a chain of
  shared cuts; it need not itself meet `B`.
- `P` (positive at the root): the route leaves `o(Q)` through an actual bridge.
  The whole descendant side of that bridge is one connected induced territory.

More generally, root the minimal block-cut subtree containing `B` and all
external cyclic blocks. Any bridge node in that subtree separates its complete
descendant set of cyclic blocks as one connected induced territory. This
remains valid for a common connector stem and for nested blocks. Consequently
no cut vertex, connector remnant, or rooted branch is duplicated. If there is
no bridge node anywhere in the subtree, all its cyclic blocks form one
shared-cut cluster. This last alternative includes chains and is stronger than
merely saying that every external block is directly incident with `B`.

If `O` is the set of internal vertices allowed as structural openings, the
statement that no external cycle is routed through an admissible opening says
exactly

`o(Q) notin O`.                                               (1)

It says nothing about whether the route type is `D` or `P`. In particular,
attaching `Q` to any legal owner by one bridge is a positive-route realization
of (1). This supplies an immediate counterexample to any inference
"no-routing implies shared cut." Even after positive routes are excluded, a
cycle can be downstream from another external cycle in the shared-cut cluster;
one must retain the full block-cut incidence tree.

## 2. Exact legal terminal sets

The four templates have the following terminal sets. Interiors are physical
path interiors, so an unsubdivided path contributes no internal terminal.

| template | admissible opening set `O` | legal owners |
|---|---|---|
| diamond, with paths `xy,xay,xby` | `{a,b}` | `{x,y}` |
| doubled triangle, odd connector `c>=3` | `Int(c)` | `V(B)-Int(c)` |
| doubled triangle, direct connector `c=1` | the internal vertices of the two canonical even parallel paths | the three branch vertices |
| doubled `C4` class `111` | interiors of every openable single connector | the branch vertices and the interiors of the two canonical even doubled paths |
| one-long all-odd `K4` | interior of the unique long path `P` | the four branch vertices |

For the doubled `C4`, the canonical even connector is always openable and the
odd connector is also openable when it is long. Hence the legal-owner formula
excludes both connector interiors when both exist. For the one-long `K4`, the
stabilizer of `P` has two terminal orbits: endpoints of `P` and the other two
branch vertices. For the direct doubled triangle there are likewise two
terminal orbits, the central branch vertex and the two outer branch vertices.
These orbit reductions are optional; the displayed physical terminal sets are
the ownership-exact statement.

For two external triangles the positive connector data need not be expanded
into a large topology list. Root the minimal block-cut subtree at `B`. If an
actual bridge occurs, its descendant cyclic set is exactly `{T}` or `{T,T}` in
the rank-three templates, and one of

`{T}`, `{T,T}`, `{T,P}`, `{T,T,P}`                         (2)

when the diamond template is cut on a side containing a triangle. Formula (2)
includes separate arms, a common positive stem, and nested external blocks.
It is therefore the exact reduced positive-connector family; those apparent
topological variants do not create new packet inequalities. In the absence of
a bridge, the exact terminal datum is the rooted bipartite block-cut incidence
tree itself. For `B+T+T` it has only two block-level forms: both triangles are
incident with cut nodes of `B`, or one triangle is downstream from the other.
A cut node may have degree three, so the first form includes two triangles
sharing the same owner. For `D+T+T+P`, retain the corresponding rooted
incidence tree on four block nodes; every cut node adjacent to `D` is labelled
`x` or `y`. This formulation includes stars, chains, and branching without
inventing pairwise block adjacencies at a common cut.

## 3. The diamond template

Write `D=Theta(1,2,2)` and call the external blocks `T_1,T_2,P`.

Suppose first that the minimal subtree contains a bridge having a triangle on
its descendant side. Its descendant territory has one of the four profiles in
(2). The established packet bounds give

- `sigma(T)>0`;
- `sigma(TT)>1`;
- `sigma(TP)>0`;
- `sigma(TTP)>0`.

The complementary territory is connected, contains `D`, has cyclic rank
between two and four, and therefore has nonnegative credit by the already
proved lower-rank theorems. This closes every positive-triangle connector
shape, including common-stem and nested shapes.

It remains either that the subtree is bridge-free or that every bridge cuts
off only the pentagon. In the latter case cut off that pentagonal unicyclic
territory, whose credit is greater than `-1`; the complementary `D+T+T`
territory is a favorable rank-four packet of credit `>3`, and the row closes.

In the bridge-free case, choose a triangle `T_1` whose block node is a leaf of
the rooted incidence tree after suppressing the pentagon side. The minimal
subtree from `D` to `T_1` contains no bridge. If `T_1` is incident with `D` at
`x` or `y`, the concentrated block `D+T_1` is the favorable rank-three packet:
all three of its odd cycles are triangles, and its normalized Sachs phase gives

`sigma(D+T_1 packet)>2`.                                    (3)

Root the remaining incidence tree at this packet. Delete its root cut from each
component on the other side. A component containing one remaining cyclic block
has rank zero or one and credit at least `-1`; a component containing both has
rank at most two and can either be kept whole or split at its next cut, again
with total credit at least `-2`. There are only two remaining cyclic demands,
so the total boundary loss is at most two. Thus (3) pays every possible loss
strictly, without assigning a shared cut twice. This includes the case in which
one demand is nested beyond the other: the boundary cycle is opened by the root
cut and the downstream cycle remains intact.

If no triangle is incident with `D`, the pentagon is the first external block
on the route from `D`; both triangles lie downstream from it. This is the
genuinely nested bridge-free incidence and cannot be relabelled as a direct
`D+T` anchor. The single analytic family for this template should therefore be
stated as the whole bridge-free `D+T+T+P` incidence packet, uniformly over its
rooted block-cut trees and the labels `x,y` on cuts adjacent to `D`. Its members
with a direct `D+T` subpacket are already discharged by (3); only the members
rooted `D-P` need new analysis.

## 4. The three rank-three templates

Let `B` be any of the three canonical rank-three blocks and let `T_1,T_2` be
the external triangles. If the minimal subtree contains a bridge, cut a bridge
farthest from `B`. The descendant cyclic set is `{T}` or `{T,T}`. Its credit is
respectively positive or greater than one, while the connected complement has
rank four or three and nonnegative credit. Hence every case with a positive
connector is strict. This argument also covers a common connector stem and one
triangle lying beyond the other.

The sole remaining connector family is therefore genuinely bridge-free. The
entire cyclic core is one shared-cut cluster, so connector splitting has done
all it can do. For each rank-three template there are two exact incidence
families: both triangles are incident with legal owner cuts of `B`, or one
triangle is downstream from the other. What remains is one analytic packet,
uniform over those two incidence families, for each rank-three template:

| rank-three template | bridge-free analytic packet |
|---|---|
| doubled triangle class `111` | doubled triangle plus two triangles in one shared-cut incidence tree |
| doubled `C4` class `111` | doubled `C4` plus two triangles in one shared-cut incidence tree |
| one-long all-odd `K4` | one-long `K4` plus two triangles in one shared-cut incidence tree |

In the first incidence family, each packet must be proved uniformly over every
pair, with repetition, from the legal-owner set in Section 2. In the second,
only the first triangle has a terminal in `B`; the second terminal is an
arbitrary vertex of the first triangle. Arbitrary rooted trees are part of the
packet.
There is no deleted-tree payment and no duplicated shared cut. Notice that the
existing structural opening gives only a favorable bicyclic remainder of
credit `>1`; after two direct triangle attachments that estimate cannot simply
be promoted to a rank-five margin. A valid closure must therefore analyze the
displayed whole shared-cut packet (for example by its grouped Sachs phase), not
reuse the opening ledger formally.

## 5. Reduced ledger

The exact connector ledger is consequently:

| residual template | positive-route packet | bridge-free analytic packet |
|---|---|---|
| `D+T+T+P` | one of (2), plus a rank-at-most-four complement | one bridge-free four-block incidence packet; direct-`D+T` members close by (3) |
| doubled triangle `111` plus `TT` | `T` or `TT`, plus a lower-rank complement | one shared-cut packet, direct/direct and nested incidences |
| doubled `C4` `111` plus `TT` | `T` or `TT`, plus a lower-rank complement | one shared-cut packet, direct/direct and nested incidences |
| one-long all-odd `K4` plus `TT` | `T` or `TT`, plus a lower-rank complement | one shared-cut packet, direct/direct and nested incidences |

Thus no-routing does not itself force direct attachment. Block-cut ownership
instead gives a complete dichotomy: a positive first bridge supplies an
induced lower-rank packet split, while absence of such a bridge forces one
shared-cut incidence packet. These alternatives exhaust the connector geometry
of the four templates and retain every connector vertex, shared cut, and rooted
tree exactly once. There is one bridge-free analytic packet family per
residual template. The direct `D+T` rank-three anchor closes part of the diamond
packet; its nested members and the other three shared-cut packet families are
the exact new analytic ledger.
