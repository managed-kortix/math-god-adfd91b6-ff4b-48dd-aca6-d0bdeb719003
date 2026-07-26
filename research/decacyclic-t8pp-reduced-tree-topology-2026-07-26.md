# Reduced-tree topology for the ten structural `T^8PP` rows

**Date:** 2026-07-26

## Result

The companion certificate

```bash
python3 research/decacyclic-t8pp-reduced-tree-topology.py
python3 -O research/decacyclic-t8pp-reduced-tree-topology.py
```

enumerates every reduced colored cluster tree realizing each of the ten
structural `T^8PP` partitions. Cluster interiors, connector lengths, and
hanging bridge trees are abstracted. The topology lemma is:

**Lemma.** Let `R` be the reduced cluster tree of one of the ten structural
rows. Exactly one of the following ordered alternatives applies.

1. `R` has an all-triangle leaf cluster whose deletion leaves rank at least
   two. Cutting the first actual bridge gives a strict triangular territory and
   a strict lower-rank complement (rank at most nine).
2. `R` has no such leaf, is a path whose two leaves contain the two pentagons,
   and a singleton triangle adjacent to a singleton-pentagon end gives a strict
   `TP` terminal territory and a strict lower-rank complement.
3. `R=P|A_8|P`, the marked two-interface endpoint kernel.
4. `R=T^8P|P`, the marked last-bridge endpoint kernel.

The alternatives are ordered because some trees satisfying (1) also contain a
terminal `TP`. With priority `(1),(2),(3),(4)`, the exhaustive counts are:

| row | reduced shapes | colored trees | leaf | terminal `TP` | `P|A_8|P` | `T^8P|P` |
|---|---:|---:|---:|---:|---:|---:|
| `P|P|T|T|T|T|T|T|T|T` | 5995 | 142805 | 142804 | 1 | 0 | 0 |
| `P|P|T|T^7` | 5 | 19 | 18 | 1 | 0 | 0 |
| `P|P|T^8` | 2 | 3 | 2 | 0 | 1 | 0 |
| `P|T|T|T|T|T|T|T^2P` | 412 | 10727 | 10726 | 1 | 0 | 0 |
| `P|T|T|T|T|T|T^3P` | 116 | 2156 | 2155 | 1 | 0 | 0 |
| `P|T|T|T|T|T^4P` | 37 | 439 | 438 | 1 | 0 | 0 |
| `P|T|T|T|T^5P` | 12 | 90 | 89 | 1 | 0 | 0 |
| `P|T|T|T^6P` | 5 | 19 | 18 | 1 | 0 | 0 |
| `P|T|T^7P` | 2 | 4 | 3 | 1 | 0 | 0 |
| `P|T^8P` | 1 | 1 | 0 | 0 | 0 | 1 |
| **total** | | **156263** | **156253** | **8** | **1** | **1** |

Thus the structural census has no further reduced-tree topology kernel. The
two marked kernels are exactly those already covered by
`decacyclic-t8-two-interface-census.py` and
`decacyclic-t8p-last-bridge-census.py`.

## Why arbitrary bridge degree is finite

Start in the block-cut tree, mark the shared-cut clusters, take the minimal
subtree spanning them, and suppress only unmarked degree-two vertices. Delete
unmarked leaves, which lie outside the spanning subtree. Every remaining
unmarked vertex is therefore a Steiner vertex of degree at least three, and
every leaf is a marked cluster.

If there are `k` clusters and `s` Steiner vertices, the tree degree identity
gives

```text
k+s-2 = sum_v(deg(v)-1) >= 2s,
```

so `s<=k-2`. Also every degree is at most the number `k` of marked branches.
Connector subdivisions, arbitrarily high degrees in the original bridge tree,
and hanging unmarked branches therefore create no new reduced type. They are
assigned to an adjacent territory when the proof cuts actual bridge edges.

The generator mirrors this reduction. From a reduced tree on `k-1` marked
vertices, add the final marked leaf either directly at an existing vertex or
by subdividing an edge with a degree-three Steiner vertex. Conversely, delete
any marked leaf and suppress its Steiner neighbor if that neighbor becomes
degree two. This proves generation completeness by induction. Center-rooted
colored-tree codes quotient all graph and equal-color automorphisms.

## Counterexample to the narrower claim

The tempting dichotomy

```text
singleton triangle leaf with strict rank-nine complement,
or one of the two marked endpoint kernels
```

is false. Its smallest displayed counterexample is the ten-cluster path

```text
P-T-T-T-T-T-T-T-T-P.
```

Neither endpoint is a triangle, so there is no singleton-triangle leaf; it is
neither `P|A_8|P` nor `T^8P|P`. It is nevertheless strict: take either endpoint
pentagon together with its adjacent singleton triangle as a `TP` territory.
The complement is a connected rank-eight cactus and is strict. More generally,
the same issue accounts for the one terminal-path class in eight of the rows.

There are further failures if “rank-nine complement” is read literally as
deleting only a singleton triangle: for example `P|T^8|P` has an all-triangle
leaf of rank eight, whose deletion leaves a strict rank-two `PP` complement.
The correct statement is therefore the lemma above: an all-triangle leaf with
a strict lower-rank complement, or a terminal `TP` path reduction, or one of
the two endpoint kernels.

## Analytic boundary

This certificate proves only the finite tree-combinatorial exhaustion and the
cycle-type ledgers attached to its four outcomes. It does not enumerate a
cluster's internal cycle-cut incidence, because the only outcomes needing that
data are deliberately isolated as marked kernels. Their existing certificates
enumerate all connector entries (shared cuts and private cycle ports), validate
cyclic interval ownership, and close every residual surgery. Arbitrary
connector remnants and off-hull trees follow the unique reduced-tree owner and
do not alter the topology classification.
