# The final four strict-last-bridge `G6PP` classes

**Date:** 2026-07-26

## Verdict

The final four rows L13--L16 of
`research/octacyclic-g6pp-last-bridge-census-2026-07-26.md` are closed by
explicit induced packetizations. They are the four marked-root orbits of one
unrooted incidence tree, and no direct whole-graph spectral calculation is
needed. In every row the packet ledger is

```text
sigma(G) > 2-2delta = 6-2sqrt(5) > 0,
delta=sqrt(5)-2.                                      (1)
```

This is uniform over arbitrary finite trees attached at arbitrary vertices.
It is the same corrected shared-cut ledger used by the 16-row resolution.

## Common incidence and labels

Use triangle labels `T_0,...,T_5`, clustered pentagon `P_0=6`, and cuts
`7,...,10`. The common incidence tree is

```text
edges = ((0,7),(0,8),(1,7),(1,9),(2,8),
         (3,7),(3,10),(4,9),(5,10),(6,7)).           (2)
```

Thus cut `7` is the pentagon hub. Its three arms are

```text
T_0--8--T_2,   T_1--9--T_4,   T_3--10--T_5.         (3)
```

The remote pentagon `P_1` has already been separated at the strict last
bridge. The four roots are, respectively,

```text
L13: cut 7;   L14: an outer cut (represented by 8);
L15: a terminal private vertex (represented on T_2);
L16: a router private vertex (represented on T_0).   (4)
```

The positional multiplicities are `1,3,6,3`, agreeing exactly with the census.

## Packet input

Only induced-partition superadditivity and the following established estimates
are used:

```text
sigma(triangular unicyclic territory) > 0,            (5)
sigma(pentagonal unicyclic territory) >= -delta,      (6)
sigma(TTP territory) > 2-delta                        (7)
```

In (7), the two triangles share an actual cut vertex; the pentagon may meet the
triangular lobe or be joined to it by a bridge path. All three statements allow
arbitrary attached trees. Estimate (7) is the intersecting-triangle
product-subpartition/Sachs packet, so it is not the generic nonnegative
tricyclic bound used by the first census search.

Splitting a binary router triangle at its two incidence marks assigns one mark
to one nonempty proper consecutive path and the other mark to the complementary
path. This gives two induced pieces in either cyclic order. Every off-core tree
has a unique core attachment and follows the owner of that attachment. A second
router split only refines one existing territory. Consequently all packets
below are connected, induced, pairwise disjoint, and exhaustive.

## L13

Split routers `T_0,T_1`. The retained cyclic components are

```text
T_2 | T_4 | (T_3,T_5,P_0) | P_1.                    (8)
```

The two triangles in the mixed packet share cut `10`; `P_0` meets `T_3` at hub
cut `7`. The marked entry is cut `7`, owned by this mixed packet. In particular,
the strict-last-bridge convention creates no acyclic entry packet. From
(5)--(7),

```text
sigma(G) > 0+0+(2-delta)-delta = 2-2delta.           (9)
```

## L14--L16

Split routers `T_1,T_3`. The retained cyclic components are

```text
T_4 | T_5 | (T_0,T_2,P_0) | P_1.                   (10)
```

Here the mixed packet's triangles share cut `8`, while `P_0` meets `T_0` at
cut `7`. In L14 the outer-cut root `8` belongs to the mixed packet. In L15 the
terminal private root on `T_2` belongs to it, and in L16 the router-orbit root
is represented by a private vertex of retained `T_0`. None of the marked roots
lies on a split router, so again there is no separate acyclic `-1` territory.
The same calculation as (9) proves (1) for all three rows.

The other two arms are symmetric. Therefore the representative proof covers
all `3`, `6`, and `3` labelled positions in L14, L15, and L16, respectively,
not just the displayed labels.

## Crosscheck with the 16-row resolution

The packet choices agree exactly with the L13--L16 rows of
`research/octacyclic-t6p-last-bridge-conservative-resolution-2026-07-26.md`:

| rows | split routers | singleton packets | mixed packet |
|---|---|---|---|
| L13 | `T_0,T_1` | `T_2,T_4` | `T_3T_5P_0` |
| L14--L16 | `T_1,T_3` | `T_4,T_5` | `T_0T_2P_0` |

The independent classifier now recognizes exactly the same shared-cut `TTP`
bound (7). Positivity in (1) is exact because `6>2sqrt(5)`, equivalently
`36>20`.

The earlier generic-rank classification that left these rows open is
superseded; it omitted the established shared-cut `TTP` case.

## Exact verifier

Run

```bash
python research/octacyclic-g6pp-last-bridge-four-resolution.py
```

The verifier independently reads the four residual rows from the `G6PP`
census, asserts their common incidence and root multiplicities, removes the
listed routers, and checks:

1. the retained cyclic components are exactly (8) or (10);
2. every retained cut has at most one packet owner;
3. each split triangle is a binary router whose two sides have distinct owners;
4. every root is retained by the mixed packet, so no entry-tree charge occurs;
5. the mixed packet has exactly two triangles and one pentagon, with a genuine
   shared cut between the triangles;
6. `2-2delta>0` holds by exact rational squaring.

Its terminal certificate is

```text
closed independent final classes: 4/4
uniform strict margin: 2-2delta = 6-2sqrt(5) > 0
shared-cut TTP ledger crosscheck: 4/4
```
