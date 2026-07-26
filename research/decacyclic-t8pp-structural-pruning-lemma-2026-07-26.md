# Graph-level pruning of the ten disconnected `T^8PP` structural rows

**Date:** 2026-07-26

## 1. Statement and proof boundary

Write `T=C3`, `P=C5`, and `sigma(H)=s+(H)-|V(H)|`. Let the cyclic
blocks of a connected cactus `G` be `T^8PP`, and suppose its shared-cut graph
is disconnected. This note proves the graph-level reduction of every one of
the ten structural color partitions left by the exact rank-ten frontier
census. For every reduced cluster tree topology, each row either has a
positive induced packet split or reduces, with its real connector interfaces,
to one of

```text
T^8P_0 | P_1,             P_0 | A_8 | P_1.                 (1.1)
```

Here `A_r` is one shared-cut cluster of `r` triangles. The second expression
means that `A_8` lies between the two pentagons in the reduced tree; the two
interfaces are the two actual bridge directions at `A_8`. It does not mean
that an abstract connector is contracted or that a shared bridge stem is
given to two owners.

The quantitative inputs are

```text
sigma(T)>0,                 sigma(TP)>1-delta>0,
sigma(A_7)>0, sigma(A_8)>0,
sigma(H)>=0 for ranks 2,3,  sigma(H)>0 for ranks 4,...,9,
```

where `delta=sqrt(5)-2`, and all packet statements permit arbitrary bridge
connectors and attached trees. The two endpoint families in (1.1) are closed
by the exact marked-entry and marked-`A_8` interface certificates. This note
does not replace those finite certificates.

## 2. The actual reduced tree and ownership convention

Start with the block-cut tree and contract each shared-cut cluster to one
marked vertex. Take the minimal subtree spanning the marked vertices. Every
component outside that hull is an acyclic branch with a unique attachment to
the hull; assign it permanently to the owner of that attachment. Suppress
unmarked degree-two hull vertices only combinatorially. A resulting reduced
edge is therefore a record of a nonempty chain of actual bridge blocks, not an
edge that may be cut analytically.

Call the resulting marked/Steiner tree `R`. Its leaves are marked cluster
vertices. Whenever the proof separates two subtrees of `R`, choose an actual
bridge in each boundary bridge chain. Give both remnants of every cut chain,
all off-hull branches rooted on them, and the two endpoints of the cut bridge
to their respective sides. Thus the lifted territories are connected,
induced, disjoint, and exhaustive. No cyclic block is split in this pruning
lemma.

Two elementary consequences will be used repeatedly.

**Leaf cut.** If a singleton triangle cluster is a leaf of `R`, cut the first
actual bridge on its unique hull chain, walking away from the triangle. The
leaf territory is a connected triangular unicyclic cactus and has positive
surplus. Its complement is a connected rank-nine cactus and also has positive
surplus. This closes the row.

**Two-end path cut.** Suppose a row has at least one singleton triangle and,
apart from those singletons, exactly two marked clusters `B` and `P_1`. If no
singleton is a leaf, then the only possible leaves of `R` are `B` and `P_1`.
They are both leaves, and a finite tree with exactly two leaves is a path.
Let `T_*` be the singleton triangle nearest `P_1`. The terminal hull segment
from `T_*` through `P_1` contains no other marked cluster. Cut the first actual
bridge on the other side of `T_*`. The terminal territory is a connected `TP`
packet, while its complement is a connected rank-eight cactus. Both are
strictly positive. Connector lengths, suppressed vertices, and hanging trees
are already assigned by the preceding convention.

## 3. The ten rows

The complete row-by-row reduction is as follows. `sT` denotes `s` singleton
triangle clusters.

| no. | structural color row | no singleton-triangle leaf | conclusion |
|---:|---|---|---|
| 1 | `P_0|P_1|8T` | two-end path, `B=P_0` | `TP +` rank eight, positive |
| 2 | `P_0|P_1|T|A_7` | the singleton `T` is internal | positive split from Section 4 |
| 3 | `P_0|P_1|A_8` | leaf/path dichotomy at `A_8` | positive, or `P_0|A_8|P_1` |
| 4 | `P_1|6T|T^2P_0` | two-end path, `B=T^2P_0` | `TP +` rank eight, positive |
| 5 | `P_1|5T|T^3P_0` | two-end path, `B=T^3P_0` | `TP +` rank eight, positive |
| 6 | `P_1|4T|T^4P_0` | two-end path, `B=T^4P_0` | `TP +` rank eight, positive |
| 7 | `P_1|3T|T^5P_0` | two-end path, `B=T^5P_0` | `TP +` rank eight, positive |
| 8 | `P_1|2T|T^6P_0` | two-end path, `B=T^6P_0` | `TP +` rank eight, positive |
| 9 | `P_1|T|T^7P_0` | two-end path, `B=T^7P_0` | `TP +` rank eight, positive |
| 10 | `P_1|T^8P_0` | two marked clusters | endpoint `T^8P_0|P_1` |

In rows 1 and 4--9, the leaf cut applies first; if it does not, the stated
two-end path cut applies. Row 10 has a unique reduced-tree path and hence a
single real last-bridge interface on the `T^8P_0` cluster. It is exactly the
marked-entry endpoint, including arbitrary entry at a shared cut, a private
cycle port, or a branch projecting to either kind of port.

## 4. The exceptional four-mark row

Consider row 2 and assume its singleton triangle `T_*` is not a leaf. Delete
its marked vertex from `R`. Minimality of the hull implies that every resulting
component contains at least one of `A_7,P_0,P_1`. There are only three other
marks, so the reduced degree `d` of the nonleaf `T_*` is two or three. This
argument allows arbitrarily many bridge branches at the same triangle vertex;
unmarked branches are off-hull trees and already follow that vertex's owner.

If `d=2`, the three remaining marks are distributed `1+2` between the two
components. Let `C` be the component containing the single mark.

* If that mark is a pentagon, retain `T_*` with `C`. This gives a positive
  connected `TP` packet. The other territory is a connected rank-eight cactus
  containing `A_7` and the other pentagon, and is positive.
* If that mark is `A_7`, retain `T_*` with `C`. This is a connected rank-eight
  cactus and is positive. The other territory is a connected rank-two cactus
  containing the two pentagons and is nonnegative.

In either case cut one actual bridge in each boundary chain between `T_*` and
the territory not retained with it. Exactly two connected induced territories
result, and at least one is strict.

If `d=3`, the three components contain `A_7`, `P_0`, and `P_1`, one each.
Cut the actual bridge chain toward `A_7` and retain `T_*` with both pentagonal
branches. The retained territory is a connected rank-three cactus and is
nonnegative; the other territory is `A_7` and has positive surplus. (The
stronger shared-cut `TPP` bound is neither needed nor invoked.) Thus row 2 is
positive for every path or three-arm topology.

## 5. The three-mark row and its interfaces

Consider row 3. If `A_8` is a leaf of `R`, cut its first actual bridge. Its
territory has surplus `sigma(A_8)>0`. The complementary territory is a
connected rank-two cactus containing both pentagons and has nonnegative
surplus. Hence this case is positive, including a three-leaf Steiner topology
and a path having a pentagon as its middle mark.

If `A_8` is not a leaf, minimality of the hull and the presence of only two
other marks force `deg_R(A_8)=2`; deleting it leaves two components, one
containing `P_0` and one containing `P_1`. Consequently `A_8` is genuinely on
the `P_0`--`P_1` path. The two incident reduced directions determine two
distinct actual bridge chains. Project each chain to its first cyclic-hull
entry in `A_8`, retaining its complete connector remnant and all branches.
The entries may coincide as vertices of the cluster, but the two external
owners remain labelled. This is exactly the certified endpoint

```text
P_0 | A_8 | P_1.
```

There is no hidden Y-shaped connector in this endpoint: if the two pentagons
branch together before reaching `A_8`, then `A_8` is a reduced-tree leaf and
the preceding positive split applies.

## 6. Exhaustion

The exact colored census says that the table contains all ten structural
proper partitions. Rows with a singleton triangle are exhausted by the leaf
cut, the forced two-end path cut, and the `A_7` four-mark analysis. Of the two
rows without a singleton, row 3 is either positive or the two-interface
endpoint, and row 10 is the one-interface last-bridge endpoint. Every boundary
used above is an actual bridge; all remnants and attached trees have one owner;
and no cycle interval, shared cut, or connector stem is duplicated. Therefore
the ten structural rows reduce exactly to the two certified families in
(1.1) or to positive packet splits.
