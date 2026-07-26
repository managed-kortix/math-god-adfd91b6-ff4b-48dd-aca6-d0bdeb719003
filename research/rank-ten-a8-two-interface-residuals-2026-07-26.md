# Marked `A_8` two-interface residual certificates

**Date:** 2026-07-26

## Scope

This note resolves only the fifteen zero-score rows of the marked abstract
`P|A_8|P` census. It classifies their two canonical unmarked templates and
records explicit proper-interval packetizations, connector owners, common-cut
owners, terminal packet inputs, and exact symbolic margins. It does not close
the other rank-ten endpoint censuses, the fully shared `T^8PP` exceptions, or
the final graph-level exhaustion. No rank-ten theorem is claimed.

Write `delta=sqrt(5)-2`. The verifier uses integer or `Fraction` arithmetic and
checks positivity of `a-b*delta` by the exact comparison

```text
(a+2b)^2 > 5b^2.
```

## Canonical templates

The frozen fifteen rows have exactly two unmarked incidence templates.

1. `S`: a saturated router triangle `T0` meets the six-triangle common-cut
   branch at cut `8` and a singleton triangle `T2` at cut `9`. There are nine
   marked orbits, `R1`--`R9`.
2. `B`: all eight triangles share cut `8`. There are six marked orbits,
   `R10`--`R15`.

For `S`, split `T0` into its three singleton vertices. The cut-8 interval owns
the six-triangle branch, the cut-9 interval owns `T2`, and the private interval
owns the connector entering `T0`. This is the forced three-port realization;
it is not the old naked-interval ledger because each private interval is
rejoined to its actual pentagon packet.

## Saturated-router rows

| rows | marks on `T0` and its cuts | final packets | exact margin |
|---|---|---|---:|
| `R1` | both entries at the same private vertex | `A_6 + T + PP` | `>1` |
| `R2,R4` and reversals `R6,R8` | one private entry; other entry at cut `9` or private on `T2` | `A_6 + TP + P` | `>2-2delta` |
| `R3` and reversal `R7` | one private entry; other entry at cut `8` | common-cut `T^6P + T + P` | `>6-2delta` |
| `R5` and reversal `R9` | private entry on `T0`; other private entry on a cut-8 branch triangle | packing-one `T^6P + T + P` | `>6-2delta` |

The `PP` terminal in `R1` is the connected two-pentagon packet carried by the
single private interval. The `TP` terminals in `R2,R4,R6,R8` use the singleton
triangle at cut `9` and its assigned pentagon. The last four rows retain the
other pentagon with the six-triangle arm, using respectively the scalar
common-cut or one-hostile-cycle packing-one certificate.

No `TPP` terminal is needed by these nine rows. The verifier distinguishes
bounded-rank terminal packet kinds from ordinary deficit packets; here the
bounded mixed terminals are `TP` and `PP`, while the canonical `TPP` count is
exactly zero. Thus no destroyed router triangle is silently reused in `TPP`.

## Bouquet rows

| row | marked profile | operation and final packets | exact margin |
|---|---|---|---:|
| `R10` | hub, hub | open `P_A`; retain the packing-one `A_8+P_B` arm | `>7-delta` |
| `R11,R12` | hub, private (either order) | split the private triangle: common-cut `T^7P + P` | `>7-2delta` |
| `R13` | coincident private entries | split once: strict `A_7 + PP` | `>0` |
| `R14` | two private vertices of one triangle | open `P_A`; retain the packing-one `A_8+P_B` arm | `>7-delta` |
| `R15` | private entries on distinct triangles | open `P_A`; retain the packing-one `A_8+P_B` arm | `>7-delta` |

For `R10,R14,R15`, opening the remote pentagon contributes the exact tree cost
`-1`, while packing one gives `>8-delta` for the retained arm. For `R13`, `PP`
is nonnegative and `A_7` is strict, so `>0` is a strict-zero ledger, not a
positive rational credit. Among the radical ledgers the smallest displayed
lower bound is

```text
2-2delta = 6-2sqrt(5) > 0,
```

whose exact certificate follows already from `3>sqrt(5)`, or `9>5` after
squaring positive sides.

## Verifier

`research/rank-ten-a8-two-interface-census.py` materializes every repair. For
each row it checks the frozen template, proper intervals, nested active sets,
disjoint exhaustive cycle coverage, unique cut owners, connector and pentagon
owners, terminal kind, and exact positivity without floating point.

```text
terminal: PP 2, direct packetization 4, common-cut 4,
          packing-one 2, opening 3;

margin:   >0 1, >1 1, >2-2delta 4, >6-2delta 4,
          >7-2delta 2, >7-delta 3.
```

Run

```bash
python3 research/rank-ten-a8-two-interface-census.py
python3 research/rank-ten-a8-two-interface-census.py --list-residuals
```

The first command reruns all `11689` marked rows and verifies all fifteen
repairs. The second prints each canonical code, split, interval owner, packet,
connector owner, cut owner, terminal classification, and exact margin.
