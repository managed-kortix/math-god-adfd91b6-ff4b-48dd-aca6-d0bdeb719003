# Rank-ten cactus residuals: completed structural cases

**Date:** 2026-07-26

## Verdict

Write `sigma(G)=s+(G)-|V(G)|`, `T=C3`, `P=C5`, and
`delta=sqrt(5)-2`. The sharp-DNN frontier is exactly `T^9Q` and `T^8PP`.
The disconnected reduction has exactly the three marked kernels

```text
A_9|Q,  T^8P|P,  P|A_8|P.
```

All three are now closed by exact marked censuses and explicit residual
repairs. The nine fully shared `T^8PP` rows are also closed. Together with the
previously completed fully shared `T^9Q` census, no rank-ten structural row
remains.

## Exact censuses

| family | canonical marked rows | ordinary/router rows | replacements | locked repairs |
|---|---:|---:|---:|---:|
| `A_9|Q` | 3624 | 3618 | 0 | 6 |
| entry-locked `T^8P|P` | 11689 | 11586 | 100 | 3 |
| `P|A_8|P` | 11689 | 11674 | 0 | 15 |

The entry-locked census is newly built. It starts from 2392 colored `T^8P`
incidence trees, of which 1105 have the clustered pentagon as an incidence
leaf. Marking every shared cut and actual private triangular vertex gives
11689 canonical rows. Exact final-owner certificates close

```text
11689 = 11586 direct + 100 finite replacements + 3 locked openings.
```

The executable verifier does not merely recount those classes. For every one
of the 11586 direct rows it reconstructs and checks the packet partition,
router ports and proper interval sizes, connector assignment, cut and root
owners, attachment ledger, packet hypotheses, and exact strict-positive
margin. It performs the same independent reconstruction for all 100 finite
replacements, including each sequential active territory and final resolution
of every interval owner. For each of the three openings it checks that the
opened tree is exactly the four private vertices of the remote pentagon with
their rooted trees, while the entry cut and both connector remnants remain
owned by the retained packing-one packet. Canonical row digests and an exact
disjoint partition check prevent skipped or duplicated rows.

The three locked rows are the three entry orbits on one two-cut shape: a
router triangle joins the clustered leaf pentagon to a common-cut
eight-triangle fan. Open the remote pentagon. Its four private vertices and
all trees rooted there form a nonempty tree of surplus `-1`; the retained
territory has eight pairwise intersecting triangles and the clustered hostile
pentagon, including both actual connector remnants. Packing one gives
`>8-delta`, so the total is `>7-delta>0`.

For `A_9|Q`, the one-interface router census accepts 3618 rows. Its six
residuals are two marked common-cut bouquets and four marked orbits on the
two-cut saturated-router shape. The bouquets use packing one directly. On the
two-cut shape, either the leaf triangle and `Q` form a strict `TQ` territory
with strict `A_8` remainder, or opening that leaf costs one while packing one
on the retained eight-triangle hostile arm gives `>8-delta_q`; hence
`>7-delta_q>0`.

For `P|A_8|P`, the fixed router ledger accepts 11674 rows. The six bouquet
residuals close uniformly: open one remote pentagon and retain all eight
pairwise intersecting triangles with the other hostile arm, giving
`(8-delta)-1=7-delta>0`. In each of the nine two-cut residuals, the ordinary
score charged private connector intervals as naked trees. Keeping the actual
connectors with their pentagons removes precisely those charges. The retained
triangular credit is one or two, so the exact ledgers are respectively
`1-2delta` or `2-2delta`, both positive.

## Fully shared rows

The `T^9Q` census was already complete: 8049 stabilized incidence types, with
its common-cut and two saturated-router hostile rows closed by common-cut,
packing-one, and one leaf-triangle opening packets.

The `T^8PP` census has 30386 types. Ordinary splitting accepts 30377. The nine
residuals now close as follows:

```text
N1 common-cut scalar packet                         >9-4/(3sqrt(13))
N2 leaf-P opening                                   >7-delta
N3 one router: P + common-cut T^7P                  >7-2delta
N4 pentagon router: A_7 + TP                         >3/4
N5 one P opening + packing-one T^8P                 >7-delta
N6 one router: P + T + common-cut T^6P              >6-2delta
N7 two routers: P + P + A_6                         >1-2delta
N8 two routers: P + P + T + A_5                     >2-2delta
N9 two routers: P + P + T + T + A_4                 >3-2delta.
```

Thus the exact fully shared closure is `30386=30377+9`.

## Connectors, trees, and ownership

Every global separation is made at an actual bridge; no arbitrary connector
is shortened to one edge. At a router, each incidence branch or private
connector follows its marked proper interval. Successive splits refine one
induced territory, and the entry-locked verifier resolves every provisional
owner to a final packet owner. Every off-hull tree follows the owner of its
unique hull attachment. For a pentagon opening, only the four private
pentagon vertices and trees rooted there enter the opened tree territory; the
entry cut and connector remnants stay with the retained cyclic packet.

Consequently the certificates cover arbitrary connector lengths, branching
connector trees, coincident entries, and arbitrary finite trees attached at
any core or connector vertex.

## Reproduction and exact status

Run:

```bash
python3 research/rank-ten-a9-one-interface-census.py
python3 research/rank-ten-t8p-entry-locked-census.py
python3 research/rank-ten-a8-two-interface-census.py
python3 research/rank-ten-fully-shared-incidence-census.py
python3 research/rank-ten-t8pp-nine-exceptions-resolution.py
```

All arithmetic classifications use integers or `Fraction`; radical signs use
exact squared comparisons. Every invariant uses an explicit exception-raising
check rather than `assert`, so the full census and certificate audit fails
closed under both ordinary Python and `python3 -O`.
Given the already proved rank-two-through-nine cactus theorems, the sharp DNN
reduction, the common-cut scalar estimates, and the packing-one hostile-cycle
theorem, these certificates prove `sigma(G)>0` for every connected rank-ten
cactus. No two-pivot winding claim or unproved census-free separator is used.
