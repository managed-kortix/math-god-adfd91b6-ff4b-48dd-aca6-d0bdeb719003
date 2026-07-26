# Resolution of E1 for the disconnected hexacyclic `TTTTP|P` row

## 1. Scope and result

Let `G` be a connected cactus with cyclic blocks

`T1,T2,T3,T4,P0,P1`,

where every `Ti` is a triangle and `P0,P1` are pentagons. Assume that

1. `A={T1,T2,T3,T4,P0}` is one shared-cut cluster;
2. some two triangles in `A` share a cyclic cut;
3. `P1` is bridge-separated from `A`; and
4. the unique connector from `P1` first meets the cyclic core of `A` on a
   triangle or at a shared cyclic cut.

These are exactly the configurations called E1 in
`hexacyclic-ttttpp-disconnected-audit-2026-07-26.md`. Entries at a private
vertex of `P0`, and the pairwise-disjoint four-petal incidence, are outside
E1.

Write

`sigma(H)=s+(H)-|V(H)|` and `delta=sqrt(5)-2`.

This note proves `sigma(G)>0` for every E1 configuration. The proof gives a
complete six-row incidence-and-entry classification. Five rows use a legal
consecutive-interval split of `P0`; the remaining row opens both pentagons and
uses the concentrated four-triangle estimate. No assertion is made about E2,
the connected shared-cut `TTTTPP` case, or any broader hexacyclic family.

## 2. The attachment-component invariant

Let `I` be the bipartite cycle-cut incidence tree of the five-cycle cluster
`A`. Delete the cycle node `P0` from `I`. Let

`D1,...,Dk`

be the resulting components, recorded only by the triangles they contain, and
put `ri=|V(Di) intersection {T1,T2,T3,T4}|`.

**Lemma 2.1.** The following statements hold.

1. Every component `Di` contains at least one triangle.
2. Each `Di` meets `P0` at exactly one cut vertex `xi`.
3. The vertices `x1,...,xk` are distinct vertices of `P0`.
4. The sets of triangles in the `Di` are exactly the connected components of
   the triangle shared-cut graph.

**Proof.** Every neighbor of `P0` in `I` is a cut node incident with at least
one other cycle, and that other cycle must be a triangle. Thus every component
of `I-P0` contains a triangle. If two distinct neighbors of `P0` belonged to
the same component of `I-P0`, their path in that component together with the
two edges to `P0` would form a cycle in `I`. Hence every component has exactly
one neighbor of `P0`. Distinct cut nodes on one cactus block are distinct
vertices of that block. Finally, after `P0` is removed, two triangles lie in
the same incidence component exactly when they are joined by a chain of
triangle-triangle shared cuts. QED.

Because some two triangles intersect, at least one `ri` is at least two.
Consequently the unordered component-size partition is one of

```text
(4),  (3,1),  (2,2),  (2,1,1).
```

In particular `1<=k<=3`. This conclusion includes multiway cuts: if `P0` and
several triangles share one cut, all those triangles lie in the single
component attached at that cut.

## 3. Entry localization

Let `e` be the first point at which the connector from `P1` meets the cyclic
core of `A`. The E1 hypothesis makes `e` one of the following.

1. A private vertex of a triangle, or a tree branch rooted there.
2. A triangle-triangle shared cut not on `P0`.
3. The attachment cut `xi` on `P0`, possibly a multiway cut incident with
   several triangles.

In every case `e` belongs to a unique component `Dj` of `I-P0`. In the third
case the cut node `xi` itself remains in `Dj`; in the first two cases uniqueness
is immediate. Call `Dj` the entry component and write `r= rj`.

Thus, modulo triangle relabeling, permutation of equal-sized components, and
all internal incidence choices that do not change the packet bound, E1 has the
following complete finite classification.

| component sizes `(r1,...,rk)` | entry size `r` | certificate |
|---|---:|---|
| `(4)` | 4 | two-pentagon sacrifice |
| `(3,1)` | 3 | `TTTP + T` |
| `(3,1)` | 1 | `TP + TTT` |
| `(2,2)` | 2 | `TTP + TT` |
| `(2,1,1)` | 2 | `TTP + T + T` |
| `(2,1,1)` | 1 | `TP + TT + T` |

Here the `P` in the packet containing the entry component is the remote
pentagon `P1`. The displayed packets do not retain `P0`; its vertices are
distributed among proper path intervals. The three entry modes above require
no further rows because all of them force the connector into the same uniquely
owned entry territory.

The table is exhaustive: Lemma 2.1 gives all component partitions of four with
a nonsingleton part, and `r` distinguishes exactly the orbits of a marked part
under permutations of equal-sized parts. Cyclic order of the `xi` on `P0` does
not refine the classification because the interval construction below works in
every cyclic order. Equivalently, every E1 incidence has the normal form
obtained by taking connected all-triangle incidence subtrees of orders `ri`
and attaching each subtree once to `P0`; the entry marks one subtree. The
internal shape and the exact entry vertex remain arbitrary within that normal
form and are covered uniformly below.

## 4. Legal interval certificates for `k>=2`

List `x1,...,xk` in their actual cyclic order on `P0`. Choose one boundary edge
in each open arc between consecutive marked vertices. Cutting those boundary
edges partitions `V(P0)` into `k` nonempty consecutive intervals

`J1,...,Jk`,

where `Ji` contains exactly `xi`. Adjacent marks cause no problem: their common
cycle edge is a permissible boundary edge. Since `2<=k<=3`, every `Ji` is a
proper interval of the five-cycle `P0`.

For each `i`, form a territory `Hi` from

1. the interval `Ji`;
2. every triangle and incidence branch in `Di`; and
3. every off-core tree whose unique core attachment lies in this set.

For the entry index `j`, also include the whole bridge connector to `P1`, the
cycle `P1`, and all trees attached along that connector or to `P1`. At a branch
point of the connector, assign every irrelevant hanging subtree wholly to
`Hj`. This does not change its cyclic blocks.

**Lemma 4.1.** The sets `V(H1),...,V(Hk)` form an exact vertex partition into
connected induced territories. Territory `Hi` retains exactly the `ri`
triangles of `Di`, and `Hj` additionally retains `P1`. The cycle `P0` is not
retained.

**Proof.** Lemma 2.1 gives exactly one `P0` attachment `xi` for each incidence
component. Hence `Ji` joins all of `Di` and no other incidence component.
Every marked vertex `xi`, including a multiway cut, has one owner. The entry
point `e` lies in `Dj`, so the entire external connector can be assigned to
`Hj` without meeting another territory. The intervals partition `P0`, and a
cactus component outside the cyclic core has a unique core attachment, so the
stated branch assignment covers every vertex once.

Each `Hi` is connected. It is induced because all vertices of every retained
triangle and of `P1` are included, each interval is consecutive, and omitted
edges of `P0` run only between endpoints of two different intervals. No `Hi`
contains all of `P0`, so `P0` is destroyed without creating a separate tree
territory or a one-unit opening cost. QED.

We now check all five interval rows using only established packet bounds:

```text
sigma(T)>0,       sigma(TT)>1,      sigma(TTT)>2,
sigma(TP)>1-delta,
sigma(TTP)>=0,    sigma(TTTP)>0.
```

The `TTT` estimate applies because `Di` is one connected triangular shared-cut
cluster. The last two estimates are the generic tricyclic nonnegativity and
tetracyclic positivity theorems; they are not charged against a separate
pentagon deficit because `P1` is retained inside the named packet.

The resulting sums are:

```text
(3,1), r=3:  sigma(G) >= sigma(TTTP)+sigma(T) > 0;
(3,1), r=1:  sigma(G) > (1-delta)+2 > 0;
(2,2), r=2:  sigma(G) > 0+1 > 0;
(2,1,1), r=2:
               sigma(G) >= sigma(TTP)+sigma(T)+sigma(T) > 0;
(2,1,1), r=1:
               sigma(G) > (1-delta)+1+0 > 0.
```

In the fourth row, the two strict triangular terms make the sum strict even
though the `TTP` term is only nonnegative. In the fifth row the displayed final
`0` denotes only the unused lower endpoint of a strict triangular term; no
uniform triangular credit is being spent. Induced-subgraph superadditivity and
Lemma 4.1 prove every `k>=2` case.

## 5. The `(4)` sacrifice certificate

It remains to consider `k=1`. By Lemma 2.1 all four triangles form one
shared-cut cluster, and `P0` has exactly one shared cyclic cut `x1`. Choose

1. a private vertex `v0` of `P0`, distinct from `x1`; and
2. a private vertex `v1` of `P1`, distinct from its connector attachment.

Both choices exist because the cycles are pentagons. Let `F0` and `F1` be the
rooted tree territories removed when `P0` and `P1` are opened at `v0` and `v1`,
including every tree branch rooted at the selected vertex. Their rooted sets
are disjoint and

`sigma(F0)=sigma(F1)=-1`.

Let `H=G-(V(F0) union V(F1))`. The path `P0-v0` still contains `x1`, while
`P1-v1` still contains the connector attachment. Therefore these two path
remnants and the whole connector remain with `H`; they connect to the four
triangles and introduce no cycle. Thus `H` is connected and induced, its only
cyclic blocks are `T1,T2,T3,T4`, and those blocks remain one shared-cut
cluster. The established four-triangle estimate gives

`sigma(H)>3`.

The exact induced partition `V(G)=V(H) dotcup V(F0) dotcup V(F1)` now yields

`sigma(G) >= sigma(H)+sigma(F0)+sigma(F1) > 3-1-1=1>0`.

This argument is entry-safe. If the connector enters at `x1`, at another
shared cut of the triangular component, or through a triangle branch, neither
selected opening vertex lies on the connector route. Every shared cut remains
owned by `H`.

## 6. Conclusion and boundary

Every E1 incidence reduces to the marked component data `(r1,...,rk;r)` in the
six-row table. For `k>=2`, splitting `P0` at the gaps between its distinct
component marks gives legal induced intervals and a positive packet sum. For
`k=1`, opening both pentagons leaves one concentrated four-triangle packet and
costs exactly two tree units, giving the stronger conclusion `sigma(G)>1`.

Hence E1 contains no canonical obstruction. This closes only the E1 family as
stated in Section 8 of the disconnected `TTTTPP` audit. It does not resolve E2
and does not imply the full disconnected or connected hexacyclic theorem.
