# Rank-eleven `T^9PP` ladder inheritance with final owners

**Date:** 2026-07-26

## Scope and verdict

This note closes Gap G3 in
`research/rank-eleven-structural-pruning-and-router-endpoints-2026-07-26.md`.
It proves positive surplus for all ten fully shared `T^9PP` incidence shapes
left by the ordinary one-cycle split ledger. It does **not** prove global router
reachability R11, close the marked disconnected endpoints, or prove the
rank-eleven cactus theorem.

Write `sigma(G)=s+(G)-|V(G)|`, `T=C3`, `P=C5`, and
`delta=sqrt(5)-2<1/4`. The rank-ten final-owner proof and verifier are
`research/rank-ten-t8pp-nine-exceptions-resolution-2026-07-26.md` and its
companion `.py` file. They materialize all cyclic placements used below,
including sixty labelled placements at the inherited pentagon router and every
nested triangle-router owner. Every extended ledger below is recomputed; no
qualitative strictness is treated as numerical credit.

## Owner-preserving leaf extension

**Lemma.** Suppose a cycle--cut incidence tree has a final-owner induced
partition, a cut `x` has owner `H`, and a new leaf triangle is adjoined at `x`.
Enlarge `H` by the two private vertices of the new triangle and every off-hull
tree whose first hull attachment is one of them. Keep every old owner unchanged.
The enlarged territories remain connected, induced, disjoint, and exhaustive,
and the new triangle is retained by `H`.

**Proof.** The leaf triangle meets the old hull only at `x`. Its two private
vertices form an edge and are both adjacent to `x`; adjoining them and their
uniquely rooted off-hull components to the territory owning `x` preserves
connectivity. Every new edge either lies in one rooted component or has both
ends in the enlarged territory. No old territory changes, and every new vertex
follows exactly one private hull vertex. All three triangle vertices have owner
`H`. QED.

The lemma preserves ownership, not a surplus margin. The packet containing the
new triangle must supply its displayed numerical bound.

## The ten repairs

The signatures `U1`--`U10` are those in Section 7 of the structural pruning
note. `U8` is already closed there by Proposition 7.1. The complete ledger is:

| row | final packet certificate | lower bound for `sigma(G)` |
|---|---|---:|
| `U1` | common-cut `T^9PP` | `>10-4/(3sqrt(13))` |
| `U2` | common-cut `T^9P` + opened tree | `>8-delta` |
| `U3` | `P` + common-cut `T^8P` | `>8-2delta` |
| `U4` | `A_8+TP` | `>3/4` |
| `U5` | packing-one `T^9P` + opened tree | `>8-delta` |
| `U6` | `P+T+` common-cut `T^7P` | `>7-2delta` |
| `U7` | `P+` packing-one `T^8P` | `>8-2delta` |
| `U8` | `T+` connected rank-nine `T^8P` | `>0` |
| `U9` | `P+P+T+A_6` | `>1-2delta` |
| `U10` | `P+P+T+T+A_5` | `>2-2delta` |

All bounds are positive. Here `A_k` is the common-cut cluster of `k`
triangles.

### `U1`--`U3`

For `U1`, all named cycles contain one cut, and the common-cut theorem gives
`>10-4/(3sqrt(13))`. For `U2`, open the outer leaf pentagon at its incidence
cut: that cut stays with common-cut `T^9P`, while the other four vertices and
their rooted trees form a nonempty tree of surplus `-1`. Thus the total is
`>(9-delta)-1=8-delta`.

For `U3`, the outer triangle has one mark leading to a leaf pentagon and one
leading to common-cut `T^8P`. Give the former a singleton interval and the
latter the complementary edge. The destroyed router leaves `P+T^8P`, with
surplus `>-delta+(8-delta)=8-2delta`.

### `U4`--`U6`

At `U4`, the central pentagon branches have profiles `P,T,A_8`. Isolate the
vertex carrying `A_8`; the other four vertices are one path containing the
other two marks in every cyclic placement. The packets are `A_8+TP`, giving
`>3/4`. The rank-ten verifier checks all sixty labelled placements.

At `U5`, open one leaf pentagon, paying one tree unit. The retained eight fan
triangles and router triangle all contain the displayed hub; the other
pentagon joins through the router. The rooted packing-one theorem gives
`>9-delta`, hence total `>8-delta`.

At `U6`, the three router marks lead to `P`, `T`, and common-cut `T^7P`.
The three singleton intervals are forced, and the ledger is
`>-delta+0+(7-delta)=7-2delta`.

### `U7`: corrected, non-inherited numerical repair

There is a central cut with seven bare triangles and two router triangles,
each leading to a pentagon. Sacrifice only one router. Give its pentagon mark a
singleton interval and give the complementary edge containing the central cut
to the retained packet. The separate territory is `P`. The retained territory
contains the seven bare triangles, the other router triangle, and its
pentagon. Its eight triangles all contain the central cut, so the rooted
packing-one theorem applies to `T^8P`. Therefore

```text
sigma(G)>-delta+(8-delta)=8-2delta>0.
```

Literal N7 extension would instead produce `P+P+A_7`. The available bound
`A_7>0` would yield only `>-2delta`, not positivity. This is why qualitative
strictness cannot be substituted for an integer margin.

### `U8`--`U10`

For `U8`, Proposition 7.1 isolates either singleton-triangle branch of the
central pentagon and gives its complementary four-vertex path to the other
branches. The packets are a strict triangle and a strict connected rank-nine
`T^8P` cactus.

For `U9`, apply the N8 nested order: the first split produces `P`, `T`, and one
active territory, which the second router refines. The final packets are
`P+P+T+A_6`; the leaf-extension lemma gives the new triangle to the final
common-cut owner. Since `A_6>1`, the total is `>1-2delta`.

For `U10`, the analogous N9 refinement gives `P+P+T+T+A_5`. Since `A_5>2`,
the total is `>2-2delta`.

## Final-owner closure and boundary

At every opening, the incidence cut stays with the retained packet and the
private path has the opened-tree owner. At every triangle router, each branch
and connector remnant follows the proper interval containing its mark. At
`U4` and `U8`, each pentagon branch follows the displayed singleton or
complementary path. A nested split refines exactly one active territory, so
every old cut has exactly one descendant owner. Every off-hull tree follows its
unique first hull attachment. The packetizations are therefore connected,
induced, disjoint, exhaustive, and valid with arbitrary attached trees.

All ten fully shared `T^9PP` ordinary-ledger exceptions are positive: the nine
inherited rows close G3, and `U8` is the separate G6 repair. The rank-eleven
theorem remains open because the global existential claim that every marked
endpoint reaches an ordinary certificate or one of these terminals is precisely
Gap G4/R11.
