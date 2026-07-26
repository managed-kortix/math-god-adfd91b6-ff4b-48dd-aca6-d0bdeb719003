# The seven fully shared nonacyclic `T^7PP` exceptions

**Date:** 2026-07-26

## Verdict

The exact fully shared census has `8004=7997+7` color-preserving incidence
types. Direct replacement closes all seven exceptions. The seventh, `F9`, has
a pentagon router. Splitting that router gives only

```text
sigma(G)>sigma(A_7)+sigma(P)>0-delta=2-sqrt(5)<0.
```

Instead, opening the leaf pentagon retains a common-cut `T^7P` packet and gives
the positive ledger `6-delta=8-sqrt(5)`. Thus this audit proves `7/7`
replacement closure for the fully shared census. It makes no claim about all
rank-nine cacti or other disconnected and interface-bearing families.

Cycle nodes `0,...,6` are triangles, nodes `7,8` are pentagons, and cut nodes
start at `9`. For a router row, `cut:size -> cycles` records the consecutive
router interval size and the incidence branch assigned to it.

## Exact representatives and replacements

### N1 -- closed

```text
signature: X(P()P()T()T()T()T()T()T()T())
edges:     ((0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9))
split:     none
packets:   common-cut T^7PP
ledger:    >8-4/(3sqrt(13))
```

### F9 -- closed by leaf-pentagon opening

```text
signature: P(X(P())X(T()T()T()T()T()T()T()))
edges:     ((0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(7,10),(8,10))
opening:   remove the four private vertices of leaf P8; retain its cut 10
packets:   common-cut T^7P7 + tree (P8-cut 10)
ledger:    >(7-delta)-1=6-delta=8-sqrt(5)>0
```

The common packet owns cuts `9` and `10`, all of `P7`, and all seven triangles.
Its cycles share cut `9`. The other territory contains the four private
vertices of `P8` and their attached branches; it is a nonempty tree with exact
surplus `-1`. This avoids the insufficient `A_7+P8` router split.

### N2 -- closed

```text
signature: T(X(P())X(P()T()T()T()T()T()T()))
edges:     ((0,9),(0,10),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,10),(8,9))
router T0: cut 9:2 -> (T1,T2,T3,T4,T5,T6,P8)
           cut 10:1 -> (P7)
packets:   P7 + common-cut T^6P8
ledger:    >6-2delta=10-2sqrt(5)>0
```

### N3 -- closed

```text
signature: T(X(P())X(P()T()T()T()T()T())X(T()))
edges:     ((0,9),(0,10),(0,11),(1,9),(2,10),(3,9),(4,9),(5,9),(6,9),(7,11),(8,9))
router T0: cut 9:1 -> (T1,T3,T4,T5,T6,P8)
           cut 10:1 -> (T2)
           cut 11:1 -> (P7)
packets:   P7 + T2 + common-cut T^5P8
ledger:    >5-2delta=9-2sqrt(5)>0
```

### N4 -- closed

```text
signature: X(T()T()T()T()T()T(X(P()))T(X(P())))
edges:     ((0,9),(0,10),(1,9),(1,11),(2,9),(3,9),(4,9),(5,9),(6,9),(7,10),(8,11))
router T0: cut 9:2 -> (T1,T2,T3,T4,T5,T6,P8); cut 10:1 -> (P7)
router T1: cut 9:2 -> (T2,T3,T4,T5,T6); cut 11:1 -> (P8)
packets:   P7 + P8 + A_5
ledger:    >2-2delta=6-2sqrt(5)>0
```

### N5 -- closed

```text
signature: X(T()T()T()T()T(X(P()))T(X(P())X(T())))
edges:     ((0,9),(0,10),(0,11),(1,9),(1,12),(2,10),(3,9),(4,9),(5,9),(6,9),(7,11),(8,12))
router T0: cut 9:1 -> (T1,T3,T4,T5,T6,P8); cut 10:1 -> (T2); cut 11:1 -> (P7)
router T1: cut 9:2 -> (T3,T4,T5,T6); cut 12:1 -> (P8)
packets:   P7 + P8 + T2 + A_4
ledger:    >3-2delta=7-2sqrt(5)>0
```

### N6 -- closed

```text
signature: X(T()T()T()T(X(P())X(T()))T(X(P())X(T())))
edges:     ((0,9),(0,10),(0,12),(1,9),(1,11),(1,13),(2,10),(3,9),(4,9),(5,9),(6,11),(7,12),(8,13))
router T0: cut 9:1 -> (T1,T3,T4,T5,T6,P8); cut 10:1 -> (T2); cut 12:1 -> (P7)
router T1: cut 9:1 -> (T3,T4,T5); cut 11:1 -> (T6); cut 13:1 -> (P8)
packets:   P7 + P8 + T2 + T6 + A_3
ledger:    >2-2delta=6-2sqrt(5)>0
```

## Arbitrary attached trees

Each split partitions the router cycle into nonempty proper consecutive
intervals, one per incidence mark. Each incidence branch follows its marked
interval. Every off-hull tree has a unique first attachment to the cyclic hull
and follows the owner of that attachment. Therefore the territories remain
induced, disjoint, exhaustive, and connected for arbitrary finite trees
attached at arbitrary core vertices. A second router split only refines one
already induced territory. No tree-opening charge is introduced.

For `F9`, every tree attached at a private vertex of `P8` follows the opened
tree territory. Trees attached at cut `10` or elsewhere stay with the common
packet. This makes the leaf opening equally uniform over arbitrary trees.

## Reproduction

Run:

```bash
python3 research/nonacyclic-t7pp-seven-exceptions-resolution.py
```

The standard-library verifier regenerates all `8004` incidence types and the
exact seven exceptions. It checks every signature and edge set, router mark,
interval size, sequential branch refinement, retained packet, shared-cut
hypothesis, and unique cut ownership. Exact arithmetic confirms all seven
positive ledgers, including the exact `-1` charge for the opened leaf.
