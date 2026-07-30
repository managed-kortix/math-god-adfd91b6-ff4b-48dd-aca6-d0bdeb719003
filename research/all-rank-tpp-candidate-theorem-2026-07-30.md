# All-rank `T^rPP`: Voronoi-first proof note

**Date:** 2026-07-30

## 1. Status and theorem

This is a proof note only. It does not modify `STATE` and makes no public
claim. Unlike the previous draft, the argument below does not assume a global
quantitative `T^aP` theorem. It first applies maximum-triangle Voronoi to the
original graph and thereafter uses only packing-one quantitative estimates.

For a finite graph `H`, put

```text
sigma(H)=s+(H)-|V(H)|,       delta=sqrt(5)-2.
```

Write `T=C3` and `P=C5`.

**Theorem.** Let `G` be a connected cactus whose complete cyclic blocks are
`r>=1` triangles and two pentagons. Shared cuts, bridge connectors, and finite
trees attached at arbitrary vertices are unrestricted. Then

```text
sigma(G)>0.
```

The proof uses the following established inputs, uniformly over arbitrary tree
attachments.

1. **Superadditivity.** For an induced vertex partition `V(H)=dot_union V_i`,
   `sigma(H)>=sum_i sigma(H[V_i])`.
2. **Triangular packing one.** A connected cactus with `b>=1` triangles, no two
   vertex-disjoint, and no other complete cycles satisfies
   `sigma>b-1>=0`.
3. **Pentagonal packets.** A connected unicyclic pentagonal cactus has
   `sigma>=-delta`; a connected `PP` cactus has `sigma>=0`.
4. **Common cut.** A common-cut `T^bPP` packet satisfies
   `sigma>b+1-4/(3sqrt(13))>0`.
5. **Small ranks.** Every connected tricyclic cactus has nonnegative surplus,
   and every `TPP` cactus is strict. The proved rank-four and rank-five
   `TTPP` and `TTTPP` packets are strict.
6. **Two-pentagon hinge.** If two pentagons share a cut and a nonempty
   triangular cactus enters at one vertex of one pentagon through one
   interface, the resulting cactus has positive surplus.

Section 3 proves the additional local estimate actually needed here. It is a
general packing-one one-pentagon lemma; it has no one-interface restriction.

## 2. Maximum-triangle Voronoi comes first

Choose a maximum-cardinality family `T_1,...,T_m` of pairwise vertex-disjoint
triangles of the original graph `G`. Assign each vertex `v` to the
lexicographically least pair

```text
(d_G(v,V(T_i)),i),
```

and let `G_i` be induced by the vertices assigned to `T_i`.

Every selected triangle lies wholly in its own territory. If `v` has owner
`i`, the predecessor of `v` on a shortest path to `T_i` has the same owner:
distance is one-Lipschitz, and the fixed priority resolves equality in favor of
the same center. Hence every `G_i` is connected and contains `T_i`.

If `G_i` contained two vertex-disjoint triangles `D,E`, then

```text
D,E,{T_j:j!=i}
```

would be a triangle packing larger than the selected maximum packing. Thus the
triangles retained in every territory have packing number one. This replacement
argument uses maximum, not merely maximal, cardinality.

An induced subgraph of a cactus contains no new cycle: every cycle in it is an
original cyclic block. Consequently a split triangle or pentagon contributes
only a forest. In particular, a proper pentagon fragment is a path and is not
counted as `P`. Such a path may be an off-hull attachment or may supply bridge
blocks on the minimal hull between retained cycles; both are allowed in the
packet statements below. Every original attached-tree component follows the
owner of its unique actual anchor. Thus no fragment is discarded or promoted
to a complete cycle.

Classify each territory by the number of complete pentagons it retains.

* **`0P`.** It is a connected triangular packing-one cactus containing its
  selected triangle. If it retains `b>=1` triangles, Input 2 gives
  `sigma>b-1>=0`. Thus every `0P` territory is strict.
* **`1P`.** It contains `a>=1` triangles, no two disjoint, and one pentagon.
  The local lemma in Section 3 gives `sigma>a-delta>0`, regardless of the
  pentagon's number of ports or the bridge incidence inside the territory.
* **`2P`.** It contains `a>=1` triangles, no two disjoint, and both pentagons.
  Sections 4--6 prove it has positive surplus.

The territories are induced, disjoint, and exhaustive. It therefore remains
only to establish the local one-pentagon lemma and positivity of a `2P`
territory.

## 3. Local packing-one one-pentagon lemma

**Lemma L.** Let `H` be a connected cactus whose complete cyclic blocks are one
pentagon `Q=C5` and `a>=1` triangles. Suppose no two retained triangles are
vertex-disjoint. Bridges, shared cuts, the number of occupied vertices of `Q`,
and arbitrary finite tree attachments are unrestricted. Then

```text
s+(H)-s-(H)>-2delta,
sigma(H)>a-delta>0.                                  (L)
```

This is the packing-one hostile-packet argument with its actual algebraic
scope. The earlier one-interface formulation is sufficient for its original
application but is not used here.

**Proof.** Let the spine `S_H` be the union of all complete cyclic blocks and
the unique minimal paths joining them. Every component outside the spine is a
tree with one spine attachment. For an oriented branch edge `u->v`, eliminate
the branch below `u` using the signless matching message

```text
M_(u->v)(t)=Z_(T_(u->v))(t)/Z_(T_(u->v)-u)(t)
            =t+sum_w 1/M_(w->u)(t)>=t.
```

This extracts a common positive real factor `K(t)` from every Sachs carrier and
replaces the activity at each spine vertex by

```text
alpha_v(t)=t+y_v(t),       y_v(t)>=0.
```

For a graph `F` with these activities, let `Z_F(alpha)` be its weighted
signless matching partition. Put `S=V(Q)` and normalize

```text
Psi_H(t)=i^(-|V(H)|)det(itI-A(H)).
```

A triangle has normalized Sachs multiplier `-2i`, while `Q=C5` has multiplier
`+2i`. Since no two triangles are disjoint, every Sachs cycle collection
contains at most one triangle. A collection may contain `Q` and one triangle
when they are disjoint; that pair has multiplier `+4`. Thus, exactly,

```text
Psi_H(t)/K(t)=R+2i(B-A),                              (3.1)
```

where

```text
B=Z_(S_H-S)(alpha)>0,
A=sum_T Z_(S_H-V(T))(alpha)>0,
R=Z_(S_H)(alpha)
  +4 sum_(T disjoint from Q)
       Z_(S_H-(S union V(T)))(alpha)>0.               (3.2)
```

These formulas do not assume one port on `Q`. Retain every shared cut of `Q` in
`S`; every edge from such a cut into another block, and every first edge of a
bridge connector leaving `Q`, is then an edge between `S` and `S_H-S`.
Partition the matchings counted by `Z_(S_H)(alpha)` according to whether they
use any edge between those two vertex sets. Matchings using none factor into a
matching on `Q` and a matching on `S_H-S`; all remaining weights are
nonnegative. Hence

```text
Z_(S_H)(alpha)=Z_Q(alpha|S)B+E,       E>=0.            (3.3)
```

Because every activity is at least `t` and matching partitions have
nonnegative coefficients,

```text
Z_Q(alpha|S)=Z_5(t)+L,                L>=0,            (3.4)
```

where `Z_5(t)` is the bare `C5` matching partition. Combining (3.1)--(3.4),

```text
R-Z_5(t)(B-A)
 =E+LB+Z_5(t)A
  +4 sum_(T disjoint from Q)
       Z_(S_H-(S union V(T)))(alpha)>0.                (3.5)
```

Since `R>0`, the continuous phase is

```text
Theta_H(t)=atan(2(B-A)/R).
```

The bare pentagon has normalized polynomial `Z_5(t)+2i` and phase
`theta_5(t)=atan(2/Z_5(t))`. If `B-A<=0`, then
`Theta_H<=0<theta_5`. If `B-A>0`, (3.5) gives
`Theta_H<theta_5`. Therefore this strict comparison holds for every `t>0`.
The signed Coulson identity and the exact value

```text
s+(C5)-s-(C5)=-2delta
```

give the first inequality in (L). Finally `H` has `a+1` cyclic blocks, so
`|E(H)|=|V(H)|+a`; averaging the signed difference with
`s+(H)+s-(H)=2|E(H)|` proves `sigma(H)>a-delta`. QED.

The proof covers a pentagon sharing several distinct cuts with the packing-one
triangular part and a pentagon separated from it by an arbitrary bridge tree.
No common-cut or one-interface classification is needed.

## 4. Actual-bridge reduction inside a `2P` territory

Fix a `2P` Voronoi territory `K`. All its retained triangles have packing
number one. This property is inherited by every induced component obtained by
cutting an actual bridge.

Form shared-cut clusters of complete cyclic blocks and contract them in the
cactus block-cut tree. Between distinct cluster nodes there is a nonempty chain
of actual bridge blocks. Choose bridges only on the minimal subtree spanning
the cyclic clusters, so both sides contain a complete cycle. Cutting one such
actual bridge gives two connected induced components; connector remnants and
every off-hull tree remain on their actual side. Complete cycles are recomputed
after every cut.

Induct on the number of complete cyclic blocks in the active connected `2P`
component, with the number of shared-cut clusters as a secondary parameter.
Every bridge used below lies on the minimal subtree spanning cyclic clusters,
so each side contains a complete cyclic block. If one side is terminal and the
other remains a `T^bPP` component, that recursive component is missing every
complete cycle on the terminal side and therefore has strictly fewer complete
cyclic blocks. A bridge cut has one of the following exhaustive distributions
of the two pentagons.

1. **No pentagon on one side.** That side is a nonempty triangular packing-one
   cactus and has nonnegative surplus, strict when needed. If the opposite side
   still has a triangle, it is a smaller `T^bPP` instance. If it has none, it
   is a `PP` packet with nonnegative surplus, while the triangular side is
   strict.
2. **One bare `P` side.** The exact partition is

   ```text
   P + T^bP.
   ```

   The second component has `b>=1` packing-one triangles. Lemma L applies to
   its complete arbitrary incidence, not merely to a marked interface. Thus

   ```text
   sigma(K)>=-delta+(b-delta)=b-2delta>0.              (4.1)
   ```

3. **A pure `PP` side.** Keep it as one connected `PP` packet with surplus at
   least zero. The other side is a nonempty triangular packing-one cactus and
   is strict. The pentagons are not split into two adverse singleton packets.
4. **One pentagon and at least one triangle on each side.** Both components
   satisfy Lemma L and hence are positive.

The alternatives `0+2`, `1+1`, and their symmetric forms exhaust the pentagon
distribution. Recursion terminates by the complete-cyclic-block induction just
stated; connector-only branches are never selected because bridges are cut only
on the minimal cyclic-cluster hull. A side called `P` or `PP` has no hidden triangle: its complete cycles
are read from the actual bridge component before a packet theorem is selected.

It remains to treat a single shared-cut cluster.

## 5. Structure of a packing-one shared-cut `T^aPP` cluster

Let `K` now be one shared-cut cluster with `a>=1` triangles and two pentagons.
Its cycle-cut incidence graph `I` is a tree. Indeed, an incidence cycle would
give either a cycle traversing several blocks or two blocks meeting in more than
one vertex, both impossible in a cactus.

If `a=1`, `K` is tricyclic and is strict by the complete tricyclic theorem,
including the incidence path `P-x-T-y-P`. Assume `a>=2`.

Choose two triangles `T_1,T_2`. They meet because the triangle packing number
is one; call their common vertex `x`. Every third triangle `T` meets both. If
`T` met `T_1` away from `x` and `T_2` away from `x`, the corresponding paths
in `I` would form an incidence cycle. If it met one away from `x` and the other
at `x`, it would share two vertices with that triangle. Both are impossible.
Thus every triangle contains `x`.

After deleting the pentagon nodes and cuts used only by them, the triangular
incidence is therefore the star centered at `x`. A non-`x` cut belongs to at
most one triangle, since two such triangles would share it and `x`.

Restore the pentagons. A pentagon independent of the other can attach to the
triangular star at only one cut; two attachments would close an incidence
cycle. That cut is `x` or a private vertex of one triangle. If one pentagon lies
between the other and the star, the pentagons form a serial pair and the first
attaches at `x` or at a private triangle vertex. Up to exchanging the two
pentagons and the triangle petals, the exact possibilities are

```text
H1  both pentagons attach at x;
H2  both attach at the same private cut y of one triangle;
H3  one attaches at x and one at a private cut y;
H4  they attach at private cuts on two distinct triangles;
H5  a serial P-P pair whose first pentagon attaches at x;
H6  a serial P-P pair whose first pentagon attaches at a private cut y;
H7  they attach at the two distinct private cuts y,z of one triangle.
```

This list follows from the tree `I`: same private port gives `H2`, distinct
ports of one petal give `H7`, ports on distinct petals give `H4`, and dependence
of the pentagon nodes gives exactly the two serial cases. There is no hidden
triangle below a pentagonal port, because every triangle is already a petal at
`x`.

## 6. `H1`--`H7`: physical partitions and margins

Every router operation below partitions actual cycle vertices into consecutive
intervals. The incidence component at a port follows the interval containing
that port. Every connector remnant and arbitrary attachment follows its actual
anchor. Hence the displayed owners are connected, induced, disjoint, and
exhaustive.

| type | physical terminal packets | surplus |
|---|---|---:|
| `H1` | common-cut `T^aPP` | `>a+1-4/(3sqrt(13))` |
| `H2` | rooted common-cut `PP` hinge entered by the triangular cactus at `y` | `>0` |
| `H3` | split its marked triangle as singleton `y` plus the complementary two-vertex interval: `P+T^(a-1)P` | `>(a-1)-2delta` |
| `H4` | split either pentagon-bearing petal in the same way: `P+T^(a-1)P` | `>(a-1)-2delta` |
| `H5` | rooted `PP` hinge, triangular cactus entering the first pentagon at `x` | `>0` |
| `H6` | rooted `PP` hinge, triangular cactus entering the first pentagon at `y` | `>0` |
| `H7` | valid `1+2` split of the three ports `x,y,z`: one bare `P` and one `T^(a-1)P` owner | `>(a-1)-2delta` |

In `H3`, `H4`, and `H7`, the `T^(a-1)P` owner retains a subfamily of the
original packing-one triangles. Lemma L therefore applies and gives the stated
margin after the bare pentagon charge. Since `a>=2`,

```text
(a-1)-2delta>=1-2delta=5-2sqrt(5)>0.                  (6.1)
```

Here a ``singleton `y`'' is a singleton interval of the router triangle, not a
singleton-vertex final territory. Its owner receives `y`, all four other
vertices of the pentagon incident at `y`, and every remnant or tree anchored in
that branch. Thus it retains the whole pentagon. The complementary owner gets
the other two triangle vertices and every remaining vertex. The router triangle
is destroyed, its complementary edge keeps the other owner connected through
`x`, and that owner retains exactly `a-1` triangles and the other complete
pentagon. In `H7` either private port can be chosen symmetrically. This assigns
each shared cut once and proves the stated induced physical profiles rather than
merely assigning abstract demands.

The `H7` row is not an abstract table lookup. It is valid precisely when the
chosen singleton is an occupied private vertex, the other two triangle
vertices form one consecutive interval containing `x` and the other occupied
private port, and every incidence branch follows its actual port. Those
conditions hold in the unmarked one-cluster object classified in Section 5.

For an externally marked refinement, do not inherit `H7` if an entry makes an
owner disconnected or assigns one port twice. At total ranks four and five use
the proved connected `TTPP` or `TTTPP` terminal. At larger rank an opening is
valid only after checking that deleting the occupied cut of a leaf pentagon
leaves its four private vertices, remnants, and attachments in one connected
acyclic owner and leaves a connected packing-one `T^aP` complement. The opening
then has ledger

```text
-1+(a-delta)>0
```

by Lemma L. If that physical predicate fails, the opening is unavailable; no
formal `H7` row is asserted.

Thus every one-cluster packing-one `T^aPP` territory is positive.

## 7. Completion and scope

Apply maximum-triangle Voronoi to the original `G` before making any bridge
cut. Every territory contains a selected triangle and has triangle-packing
number one. Its `0P`, `1P`, or `2P` classification is exhaustive. The first is
strict triangular, the second is positive by Lemma L, and the third is positive
by the actual-bridge reduction followed by `H1`--`H7`. Superadditivity gives
`sigma(G)>0`.

Accordingly the theorem in this note is unconditional relative to the listed
proved packet inputs. In particular, it has no dependency on an unrestricted
global estimate `sigma(T^aP)>a-delta`: every quantitative `T^aP` invocation is
inside a Voronoi territory or one of its induced bridge/router descendants, so
its triangles retain packing number one and Lemma L applies.

This proof covers finite simple connected cacti with exactly `r>=1` triangles
and two pentagons, arbitrary shared cuts, arbitrary bridge lengths and
branching, and arbitrary finite forest attachments. Voronoi pentagon fragments
are forests and remain with their physical owners. The proof does not cover
three pentagons, non-cactus block intersections, or a merely maximal triangle
packing.

Dependencies are `all-rank-triangle-hostile-cacti/paper.tex` for
superadditivity, the packing-one phase calculation, and triangular territories;
`research/common-cut-bouquet-rooted-schur-2026-07-26.md` for `H1`;
`research/rooted-two-pentagon-hinge-theorem-2026-07-28.md` for `H2,H5,H6`;
`all-tricyclic-cacti/paper.tex` for `a=1`;
`all-tetracyclic-cacti/paper.tex` and `all-pentacyclic-cacti/paper.tex` for the
marked low-rank fallback; and
`research/physical-c5-interval-router-lemma-2026-07-29.md` for physical interval
ownership. Lemma L is proved in Section 3 rather than imported as a global
one-hostile theorem.
