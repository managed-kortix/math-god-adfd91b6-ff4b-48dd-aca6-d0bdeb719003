# Exact packet audit of the nine fully shared `T^8PP` exceptions

**Date:** 2026-07-26

## Scope and verdict

This note concerns only the fully shared rank-ten `T^8PP` incidence census. It
does not claim the rank-ten cactus theorem and does not address the three
disconnected marked-interface families.

The exact census has `30386=30377+9` canonical color-preserving incidence
trees. Explicit common-cut, opening, and router packetizations close all nine
ordinary-ledger exceptions. In particular, the seven rows previously left as
replacement targets now have exact positive packet ledgers.

Cycle labels and cut labels are those emitted by the verifier. A router entry
`cut:size -> cycles` gives a proper consecutive interval and its incidence
branch. Write `delta=sqrt(5)-2`.

## Nine packetizations

### C1: common-cut bouquet

```text
signature: X(P()P()T()T()T()T()T()T()T()T())
split:     none
packets:   common-cut T^8PP
ledger:    >9-4/(3sqrt(13))
```

### O2: leaf-pentagon opening

```text
signature: P(X(P())X(T()T()T()T()T()T()T()T()))
opening:   private vertices of leaf P9 at cut 11
packets:   common-cut T^8P8 + opened tree
ledger:    >(8-delta)-1=7-delta=9-sqrt(5)
```

### R3: one triangle router

```text
signature: T(X(P())X(P()T()T()T()T()T()T()T()))
router T0: cut 10:2 -> (T1,T2,T3,T4,T5,T6,T7,P9)
           cut 11:1 -> (P8)
packets:   P8 + common-cut T^7P9
ledger:    >7-2delta=11-2sqrt(5)
```

### R4: pentagon opening/router

```text
signature: P(X(P())X(T())X(T()T()T()T()T()T()T()))
router P0: isolate its cut-10 vertex; the other four vertices form one path
packets:   A_7 at cut 10 + TP connector packet from T2 to P9
ledger:    >0+3/4=3/4
```

The verifier materializes all `5*4*3=60` injections of the actual marks
`(cut 10,cut 11,cut 12)` into the five vertices of `P0`. In every certificate,
the vertex carrying cut `10` is owned by `A_7`; the other four pentagon vertices
are owned by `TP`; and the connector edges to the actual cuts `11` and `12`
have that same `TP` owner. Thus the check is tied to the incidence graph and
packet owners rather than merely counting three distinct abstract positions.

### O5: leaf opening plus packing one

```text
signature: T(X(P())X(P())X(T()T()T()T()T()T()T()))
opening:   private vertices of leaf P8 at cut 11
packets:   packing-one T^8P9 + opened tree
ledger:    >(8-delta)-1=7-delta=9-sqrt(5)
```

Here all eight triangles contain hub cut `10`; `P9` is joined through router
triangle `T0`. This is exactly the established packing-one packet shape.

### R6: one three-way triangle router

```text
signature: T(X(P())X(P()T()T()T()T()T()T())X(T()))
router T0: cut 10:1 -> (T1,T3,T4,T5,T6,T7,P9)
           cut 11:1 -> (T2)
           cut 12:1 -> (P8)
packets:   P8 + T2 + common-cut T^6P9
ledger:    >6-2delta=10-2sqrt(5)
```

### R7: two nested triangle routers

```text
signature: X(T()T()T()T()T()T()T(X(P()))T(X(P())))
router T0: cut 10:2 -> (T1,T2,T3,T4,T5,T6,T7,P9); cut 11:1 -> (P8)
router T1: cut 10:2 -> (T2,T3,T4,T5,T6,T7);    cut 12:1 -> (P9)
packets:   P8 + P9 + A_6
ledger:    >1-2delta=5-2sqrt(5)
```

### R8: two nested routers and one triangle packet

```text
signature: X(T()T()T()T()T()T(X(P()))T(X(P())X(T())))
router T0: cut 10:1 -> (T1,T3,T4,T5,T6,T7,P9)
           cut 11:1 -> (T2); cut 12:1 -> (P8)
router T1: cut 10:2 -> (T3,T4,T5,T6,T7); cut 13:1 -> (P9)
packets:   P8 + P9 + T2 + A_5
ledger:    >2-2delta=6-2sqrt(5)
```

### R9: two three-way nested routers

```text
signature: X(T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))
router T0: cut 10:1 -> (T1,T3,T4,T5,T6,T7,P9)
           cut 11:1 -> (T2); cut 13:1 -> (P8)
router T1: cut 10:1 -> (T3,T4,T5,T6)
           cut 12:1 -> (T7); cut 14:1 -> (P9)
packets:   P8 + P9 + T2 + T7 + A_4
ledger:    >3-2delta=7-2sqrt(5)
```

## Arbitrary attached trees

Every graph certificate assigns exactly one owner to every cut vertex and every
cycle vertex. It also records every cycle--cut connector edge and checks that
its two endpoints have the same owner. At a triangle router, each nonempty
proper consecutive interval has an explicit packet owner and is checked against
the incidence branch reached through its recorded cut or cuts. The second split
in R7--R9 refines one already active branch. At the R4 pentagon, the singleton
interval belongs to `A_7` and the four-vertex complementary path belongs to the
`TP` packet. At O2 and O5, the incidence vertex of the opened pentagon remains
with the retained packet while its four private vertices belong to the opened
tree.

The executable emits the complete attachment-site map used for arbitrary
off-hull trees: each cut or cycle vertex has one final packet/opening owner. An
off-hull tree has a unique first attachment to the cyclic hull, so its whole
rooted tree receives that materialized owner. This preserves connected,
induced, disjoint, exhaustive territories. No extra tree charge appears: only
each explicit leaf opening contributes the exact nonempty-tree surplus `-1`.

## Exact verification

Run from the repository root:

```bash
python3 research/rank-ten-t8pp-nine-exceptions-resolution.py
python3 -O research/rank-ten-t8pp-nine-exceptions-resolution.py
```

The standard-library verifier uses the recurrence only to emit candidate rows;
it does not trust or invoke the dependency's census, SAFE classification,
split certificates, component profiles, bounds, or assertions. For every one
of the `30386` emitted rows it independently rebuilds the incidence graph and
checks bipartiteness, labels, colors, capacities, cut degrees, tree size,
connectivity, uniqueness, center-rooted canonical signature, sorted order, and
the complete cut-count distribution. The frozen canonical signature stream is

```text
sha256 9aa6813cb87e1db0748faf441b8941145fbedb5af55386404bd9cfcbe10a6e3b
```

For each of the `30377` ordinary-safe rows, the verifier independently tries
all ten sacrificed cycles and chooses the first legal one. It materializes the
nonempty proper cyclic intervals, component packets, packet hypotheses, cycle
owners, cut owners, and every final cut/cycle-vertex owner. It then recomputes
the exact `Fraction` ledger and strictness and accepts only a positive ledger,
or a zero ledger with a strict packet. The canonical-order stream of these
fully materialized selected witnesses is frozen as

```text
sha256 1c54195dd78960ab03645f152ded55e0b35aaf898aefda9dbbd1237ea6822958
```

Exactly nine rows have no such independently accepted witness. Their signatures
must equal the nine recipes in this note. The replacement audit then checks
router activity, nesting, interval sizes, actual branch owners, and components;
all cyclic placements (including the 60 pentagon placements in R4); packet
connectivity and common-cut or packing-one hypotheses; exhaustive unique cut,
cycle-vertex, connector, and attachment ownership; and exact radical ledgers.
Every invariant uses the fail-closed `require` helper, so normal and `-O` runs
perform the same checks rather than losing checks to optimized assertions.

This is a case-level fully shared `T^8PP` packet audit only. No global rank-ten
claim is made.
