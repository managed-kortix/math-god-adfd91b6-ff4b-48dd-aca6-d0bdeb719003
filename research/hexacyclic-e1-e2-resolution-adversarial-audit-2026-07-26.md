# Adversarial audit of the E1 and E2 resolution notes

## Verdict

**ACCEPT.** I found no counterexample, ownership conflict, missing incidence
row, packet-hypothesis violation, or strictness gap in

- `hexacyclic-ttttpp-e1-resolution-2026-07-26.md`, or
- `hexacyclic-e2-tttp-two-entry-resolution-2026-07-26.md`.

This verdict concerns exactly the E1 and E2 families stated in those notes. It
does not extend either result to another hexacyclic family.

## E2 verifier and independent interval test

I ran

```bash
python research/hexacyclic-e2-tttp-entry-census.py
```

successfully. It reproduced the incidence counts `1,3,4`, classified seven of
the eight `TTTP` incidence trees as containing a shared triangle pair, found the
unique three-petal hub, and certified all 26 ordered-entry dihedral orbits. The
certificate split was `20` of type `TP+TTT` and `6` of type `TTP+TT`.

I also tested the interval claim independently, without dihedral reduction and
without using the verifier's certificate selection. For each of the ten
three-mark subsets of `C5`, I tested all 25 ordered pairs `(b,c)`, including
coincident entries and every coincidence with a petal mark. All 250 raw
configurations admit a nonempty proper cyclic interval containing `c` for which

`number of internal petal marks in J + indicator(b in J)`

is one or two. Of these configurations, 170 have a one-vertex certificate and
80 first require a two-vertex certificate. No configuration requires an
interval of length three or four, and none fails.

The projection of a branch or triangle entry to its pentagon attachment does
not create an ownership error. An arm entering through a triangle is connected
to the territory containing that whole triangle, and the triangle is assigned
by its unique petal mark. Thus a root coincident with a petal cut, two entries
through the same petal, and `b=c` all force the relevant objects to the same
territory exactly as the interval count assumes. If the two reduced-tree arms
shared a connector segment before reaching `A`, the `B-C` path would meet at
that exterior Steiner point and would not pass through `A`; hence the E2
path-through hypothesis also justifies treating the arms separately up to
their entries in `A`.

For the seven non-hub incidences, no interval construction is needed:
`sigma(A)>1`, `sigma(B)>0`, and `sigma(C)>=-delta` give a strict total greater
than `1-delta`. For the hub, the packet hypotheses used by the certificates are
only generic tricyclic nonnegativity together with either `sigma(TP)>1-delta`
or `sigma(TT)>1`. Consequently the possibly disconnected shared-triangle
pattern inside the three-cycle packet is not being silently charged a strong
`TTT` bound.

## E1 incidence and interval audit

I independently enumerated the color-preserving bipartite incidence trees for
one pentagon and four triangles. There are 25 canonical trees. Their component
partitions after deleting the pentagon node are

```text
(4):       14
(3,1):      5
(2,2):      3
(2,1,1):    2
(1,1,1,1):  1
```

The last tree is the excluded pairwise-disjoint four-petal hub. In every other
tree, every component of the deleted-pentagon incidence graph has exactly one
pentagon attachment cut, and distinct components have distinct attachment
cuts. This remains true for multiway cuts. Marking the component containing the
external entry gives exactly the six rows in the E1 note and no additional
row:

```text
((4),4), ((3,1),3), ((3,1),1),
((2,2),2), ((2,1,1),2), ((2,1,1),1).
```

I separately enumerated actual vertex assignments on `C5` for every placement
of two or three distinct attachment marks. Every placement admits a partition
into respectively two or three nonempty proper consecutive intervals, each
owning exactly one prescribed mark. This includes adjacent marks and all two
cyclic gap patterns. Therefore the short length of the pentagon causes no
hidden feasibility failure.

Connector and branch ownership is also consistent. The entry lies in one
unique deleted-pentagon component, so its whole connector can be assigned to
that component's interval. Every other off-core tree has one core attachment
in a cactus and is assigned wholly with that attachment. Boundary cycle edges
are the only omitted edges between territories, so the resulting territories
are induced as well as connected. A multiway attachment cut is a single vertex
owned by its unique interval, not duplicated among packets.

## Six-row packet and strictness check

The packet arithmetic is valid row by row.

| E1 row | Required hypotheses and resulting strictness |
|---|---|
| `(4), r=4` | Opening private non-entry vertices of both pentagons costs exactly two tree units; the surviving connected four-triangle shared cluster has `sigma>3`, so the total is `>1`. |
| `(3,1), r=3` | The entry territory is a generic tetracyclic `TTTP`, hence strict positive; the singleton `T` is also strict positive. |
| `(3,1), r=1` | `TP>1-delta`; the other component is one connected shared three-triangle cluster and has `TTT>2`. |
| `(2,2), r=2` | Generic `TTP>=0` is sufficient because the other packet has `TT>1`. |
| `(2,1,1), r=2` | Generic `TTP>=0` plus two strict singleton-triangle terms gives a strict positive sum; no uniform triangular credit is charged. |
| `(2,1,1), r=1` | `TP>1-delta`, `TT>1`, and a strict singleton `T` give a strict positive sum. |

For the `(4)` row, incidence-tree acyclicity implies that `P0` has exactly one
shared cyclic cut. A private opening vertex distinct from it therefore exists.
The remote pentagon likewise has a private vertex distinct from its connector
attachment. Removing those rooted tree territories leaves both pentagon path
remnants and the connector in the four-triangle territory; it neither deletes
a triangle shared cut nor introduces another cycle. Thus the concentrated
`TTTT>3` hypothesis is genuinely present.

## Non-mathematical consistency note

The older disconnected audit still describes E1 as unresolved in its status
section. That is stale cross-document status, not a flaw in the new E1 proof.
Any later roll-up should cite the E1 resolution note and update that status
before claiming the complete disconnected `TTTTPP` row.
