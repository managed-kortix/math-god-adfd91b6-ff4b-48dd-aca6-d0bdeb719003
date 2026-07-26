# The six fully shared octacyclic `T^6PP` census exceptions: replacement audit

**Date:** 2026-07-26

## 1. Corrected verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2.
```

This note replaces the previous resolution of the six canonical exceptions
returned by `research/octacyclic-fully-shared-incidence-census.py`. The previous
argument for U2--U6 invoked the rooted hostile-cycle guard theorem. No part of
the replacement audit uses that theorem.

All six exceptions are nevertheless **PROVED**. U1 and the large packets in U2
and U3 use only the exact common-cut Schur--Sachs theorem. U4--U6 admit direct
induced packetizations. The weakest case, U6, has the strict ledger

```text
sigma(G)>1-2delta=5-2sqrt(5)>0.                 (1.1)
```

The complete status is:

| code | replacement operation | certified surplus |
|---|---|---:|
| U1 | common-cut `T^6PP` theorem | `>7-4/(3sqrt(13))` |
| U2 | `P +` common-cut `T^5P` | `>5-2delta` |
| U3 | `P + T +` common-cut `T^4P` | `>4-2delta` |
| U4 | `P + P + A_4` | `>3-2delta` |
| U5 | `P + P + T + A_3` | `>2-2delta` |
| U6 | `P + P + T + T + A_2` | `>1-2delta` |

Here `A_r` denotes one connected shared-cut cluster of `r` triangles. These
statements are uniform over arbitrary finite trees attached at arbitrary core
vertices.

## 2. Inputs and exact splitting operation

Only the following established estimates are used:

```text
sigma(P)>=-delta;
sigma(A_r)>r-1 for 1<=r<=4;
sigma(common-cut T^kP)>k-delta for k>=1;
sigma(common-cut T^kPP)>k+1-4/(3sqrt(13)) for k>=1.
                                                               (2.1)
```

The last two inequalities are the scalar common-pivot Schur--Sachs theorem,
not a rooted guard statement. The `A_r` inequalities include arbitrary attached
trees. Positive square energy is superadditive over induced vertex partitions,
so the packet surpluses in (2.1) may be added.

The packetizations below use the following exact operation. Let a triangle
router `R` have cyclic cut marks `z_1,...,z_d`, where `d=2` or `3`. Partition
`V(R)` into nonempty proper consecutive intervals, one interval owning each
mark, and give that interval the entire component of the cycle-cut incidence
tree on the corresponding side of `I-R`.

For `d=2`, one may assign the pentagon-side marked vertex as a singleton and
the other two vertices, including the second mark, as the complementary edge.
For `d=3`, the three marks occupy the three triangle vertices, so the three
singleton vertices are the required intervals. Every hanging tree follows the
owner of its core attachment. Thus the territories are disjoint, exhaustive,
and induced; the router cycle is retained by no territory, and there is no
tree-opening charge. The operation depends only on cyclic order and therefore
works for every realization represented by a canonical incidence code.

Several cases split a second router inside the territory produced by the first
split. A refinement of an induced partition by an induced partition is again
an induced partition of the original graph. This justifies the sequential
descriptions without assigning any shared cut twice.

## 3. The six canonical codes

Cycle nodes `0,...,5` are triangles, nodes `6,7` are pentagons, and cut nodes
start at `8`.

### U1: common-cut bouquet -- PROVED

```text
signature: X(P()P()T()T()T()T()T()T())
edges:     ((0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8))
```

All eight cycles share cut `8`. Apply the common-cut `T^kPP` theorem with
`k=6` directly; no ownership split at cut `8` is attempted:

```text
sigma(G)>7-4/(3sqrt(13))>0.                     (3.1)
```

### U2: six-triangle hub and one `TP` tail -- PROVED

```text
signature: T(X(P())X(P()T()T()T()T()T()))
edges:     ((0,8),(0,9),(1,8),(2,8),(3,8),(4,8),(5,8),(6,9),(7,8))
```

Split router `T0` at its two marks: the singleton at cut `9` owns `P6`, and
the complementary two-vertex interval owns the cut-`8` side. The first packet
is one `P`. In the second packet, cycles `T1,...,T5,P7` all contain cut `8`;
the remnant of `T0` is only an attached tree. Hence the second packet is a
common-cut `T^5P` packet. By (2.1),

```text
sigma(G)>=sigma(P)+sigma(common-cut T^5P)
        >-delta+(5-delta)=5-2delta>0.            (3.2)
```

### U3: five-triangle hub, one `TP` tail, and one `TT` petal -- PROVED

```text
signature: T(X(P())X(P()T()T()T()T())X(T()))
edges:     ((0,8),(0,9),(0,10),(1,8),(2,9),(3,8),(4,8),(5,8),(6,10),(7,8))
```

Router `T0` has marks `8,9,10`. Split it into the three singleton intervals.
The cut-`10` packet contains only `P6`; the cut-`9` packet contains only `T2`;
and the cut-`8` packet contains `T1,T3,T4,T5,P7`. Every cycle in the last list
contains cut `8`, so it is a common-cut `T^4P` packet. Therefore

```text
sigma(G)>=sigma(P)+sigma(T)+sigma(common-cut T^4P)
        >-delta+0+(4-delta)=4-2delta>0.           (3.3)
```

The strict `0` for the `T` packet is the `A_1` case of (2.1).

### U4: six-triangle hub with two `TP` tails -- PROVED

```text
signature: X(T()T()T()T()T(X(P()))T(X(P())))
edges:     ((0,8),(0,9),(1,8),(1,10),(2,8),(3,8),(4,8),(5,8),(6,9),(7,10))
```

Split `T0` between cuts `9` and `8`, isolating `P6`, and then split `T1`
between cuts `10` and `8`, isolating `P7`. The common owner of cut `8` retains
exactly `T2,T3,T4,T5`; the two router remnants are attached trees. Thus the
final induced packets are `P6`, `P7`, and one common-cut `A_4`, giving

```text
sigma(G)>-2delta+3=3-2delta>0.                   (3.4)
```

### U5: five-triangle hub with one decorated and one plain arm -- PROVED

```text
signature: X(T()T()T()T(X(P()))T(X(P())X(T())))
edges:     ((0,8),(0,9),(0,10),(1,8),(1,11),(2,9),(3,8),(4,8),(5,8),(6,10),(7,11))
```

First split saturated router `T0` at cuts `8,9,10`. This yields a `P6` packet,
a `T2` packet, and the cut-`8` territory containing `T1,T3,T4,T5,P7`. Inside
that last territory split `T1` between cuts `11` and `8`. This yields `P7` and
leaves the common-cut cluster `T3,T4,T5=A_3`. The exact final packet list is

```text
P6 + P7 + T2 + A_3,
```

and hence

```text
sigma(G)>-2delta+0+2=2-2delta>0.                 (3.5)
```

### U6: four-triangle hub with two decorated arms -- PROVED

```text
signature: X(T()T()T(X(P())X(T()))T(X(P())X(T())))
edges:     ((0,8),(0,9),(0,11),(1,8),(1,10),(1,12),(2,9),(3,8),(4,8),(5,10),(6,11),(7,12))
```

Split `T0` at cuts `8,9,11`. The first refinement gives `P6`, `T2`, and the
cut-`8` territory containing `T1,T3,T4,T5,P7`. Split saturated router `T1` in
that territory at cuts `8,10,12`. This gives `P7`, `T5`, and the common-cut
two-triangle packet `T3,T4=A_2`. Therefore

```text
sigma(G)>-2delta+0+0+1
        =1-2delta
        =5-2sqrt(5)>0.                           (3.6)
```

The last inequality is exact because `sqrt(5)<5/2`.

## 4. Ownership, attachments, and scope

Each listed pentagon is an incidence leaf. In every split above, its unique
cyclic cut is assigned to the same interval as that pentagon, so the resulting
pentagon packet is connected and unicyclic. A binary router leaves a path in
the complementary packet; a saturated router leaves no internal router edge,
but each incidence branch already meets its owning marked vertex. Thus every
named packet is connected and has exactly the cyclic blocks claimed.

A cactus component outside the cyclic hull has a unique hull attachment.
Assigning it to the owner of that attachment makes the partition exhaustive
for arbitrary attached trees and introduces neither overlap nor an extra
territory. Cuts `8` retained through two sequential splits always have one
owner: the later split merely refines the territory that already owned them.

The six objects are color-preserving incidence types rather than six individual
graphs. The interval argument covers every cyclic mark order compatible with
each type. Consequently all six canonical ordinary-split exceptions are
closed without the rooted hostile-cycle guard theorem. This remains a local
fully shared `T^6PP` result; it does not by itself resolve any disconnected or
entry-locked octacyclic family.
