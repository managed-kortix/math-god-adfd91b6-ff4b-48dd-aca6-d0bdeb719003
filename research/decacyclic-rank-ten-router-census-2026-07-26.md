# Rank-ten marked router census: proof boundary

**Date:** 2026-07-26

Write `T=C3`, `P=C5`, `delta=sqrt(5)-2`, and
`sigma(G)=s+(G)-|V(G)|`. This extension treats the decacyclic residual
`T^8PP` at the two disconnected endpoints

```text
T^8P | P,
P | A_8 | P,
```

and regenerates the fully shared ordinary-split census. It uses triangle
routers, scalar common-cut packets, the one-hostile-cycle packing-one theorem,
and explicit pentagon openings. It does not use a two-pivot phase or winding
claim.

## Disconnected endpoint `T^8P|P`

The exact marked-entry census gives

```text
2392 T^8P incidence trees,
1105 with the clustered P as an incidence leaf,
11689 canonical marked-entry classes,
11586 direct one-router certificates,
100 finite replacement certificates,
3 explicit repairs/openings.
```

The replacement split counts are `2,9,73,16` for zero through three routers.
The three residual marks occur on one two-cut kernel: a router triangle joins a
common-cut `A_7` fan to the clustered pentagon. They close respectively as

```text
A_7+PP                                      >0,
P + packing-one A_7P                       >7-2delta,
open remote P; retain packing-one T^8P     >7-delta.
```

Thus all `11689` marked classes close.

## Disconnected endpoint `P|A_8|P`

The exact two-interface census gives

```text
126 unmarked eight-triangle incidence trees,
36414 ordered labelled placements before automorphisms,
11689 canonical marked-interface classes,
11674 ordinary-router certificates,
15 explicit replacements.
```

The best router count distribution is `0:6, 1:10844, 2:838, 3:1`. Nine
residuals are the same two-cut `A_7`-plus-leaf kernel with different labelled
entry positions. Their five surgeries produce `A_6+T+PP`, `A_6+TP+P`,
common-cut `T^6P+T+P`, or packing-one `T^6P+T+P`, with respective lower
ledgers `>1`, `>2-2delta`, or `>6-2delta`. The six bouquet orbits close by the
same interface-aware operations as at rank nine, with `A_7`, `A_6`, and
packing-one margins. Hence all `11689` classes close.

The frozen canonical digests are

```text
rows:      77468da6a473a52ece68d6e4319f78337feb17941e615e2a0ae65032f826cc86
residuals: 1f41279dad404a97627da24f1fa67e720f6a0d2ffc67b3c28bf1521ebeb11ca0
```

The repair executable now materializes a structural ownership certificate for
each of the 15 signatures rather than accepting a repair name alone. Each row
contains its concrete incidence edges and labelled `A,B` positions, sequential
router active sets, marked owner ports and interval lengths `(2,1)` or
`(1,1,1)`, connected retained cycle packets, any displayed common hub and
packing-one flag, exact `-1` opening costs, connector owners, and one final
owner for every retained incidence cut. Verification fails closed if packets
overlap or disconnect, a router interval is missing, a common hub is false, an
opening cost changes, or any cut/connector has no unique final owner.

## Fully shared `T^8PP`

The exact color-preserving incidence census is

| cuts | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 19 | 204 | 1155 | 3990 | 8135 | 9615 | 5843 | 1424 | 30386 |
| ordinary safe | 0 | 17 | 200 | 1154 | 3989 | 8135 | 9615 | 5843 | 1424 | 30377 |
| exceptions | 1 | 2 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 9 |

All nine have exact replacements: common-cut `T^8PP`; leaf openings retaining
common-cut `T^8P` or `T^7P`; the continuing router ladder ending in
`P+P+T+T+A_4`; and one packing-one opening for the apparent new row

```text
signature: T(X(P())X(P())X(T()T()T()T()T()T()T()))
cuts:      (T,P), (T,P), (8T)
```

The ordinary split of this row gives only `P+P+A_7`, with ledger `>-2delta`.
Instead open either leaf pentagon at exact cost `-1`. The retained graph has the
central router triangle and the seven hub triangles, all containing the hub,
plus one pentagonal arm at the router's other vertex. Its eight triangles have
packing number one, so the established one-hostile-cycle theorem gives
`>8-delta`; after the opening the ledger is `>7-delta>0`. This is a one-hostile
packet and not a two-pivot estimate.

The other three-cut row is closed by opening its leaf pentagon and the leaf
triangle on the second private pivot, each at exact tree cost `-1`, leaving a
common-cut `T^7P` packet. Its ledger is `>7-delta-2=5-delta>0`.

Therefore the requested disconnected rank-ten endpoints are proved, and the
fully shared census is exact with all `9/9` exceptions closed. A complete
rank-ten cactus theorem is not claimed because the global rank-ten DNN and
disconnected cluster-partition exhaustion are outside this artifact.

The nine-exception executable likewise freezes the exact ordered signature set
and digest

```text
461351660aa2d8e23d36ca54441275acfd022ebfec80ba599698ffcbb86cb35a
```

and reconstructs every certificate from the concrete colored incidence tree.
It checks selected routers and openings, exact opening costs, connected and
disjoint retained packets, common-cut hubs, the E5 packing-one hub for all eight
retained triangles, positive exact ledgers, and final ownership of every cut.
Thus a signature prefix can no longer fall through to a verbal recipe.

## Reproduction

Run from the repository root:

```bash
python3 research/decacyclic-t8p-last-bridge-census.py
python3 research/decacyclic-t8-two-interface-census.py
python3 -O research/decacyclic-t8-two-interface-census.py
python3 research/decacyclic-fully-shared-nine-exceptions.py
python3 -O research/decacyclic-fully-shared-nine-exceptions.py
```

All three scripts use the Python standard library and exact integer or
`Fraction` arithmetic. The two strengthened executables produce identical
normal and optimized output and use explicit `require` checks for certificate
invariants. They fail closed on totals, exact signatures/digests, incidence
structures, router marks and intervals, packet connectivity and hubs, packing
one, opening costs, exact ledgers, and final ownership.
