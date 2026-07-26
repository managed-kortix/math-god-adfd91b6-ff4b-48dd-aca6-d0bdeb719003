# Rank-eleven residual colored-partition audit

**Date:** 2026-07-26

## Status and boundary

This note generalizes the exact rank-ten colored integer-partition audit to the
expected rank-eleven sharp-DNN residuals

```text
T^10Q, q>=3 (including Q=T),    T^9PP.
```

It uses the proved packet bounds for connected cactus territories of rank at
most ten. It is a conditional finite audit, not a rank-eleven theorem claim.
In particular, it does not certify endpoint closure, marked-interface
ownership, connector remnants, fully shared clusters, or a global cactus
decomposition.

Run the fail-closed exact checker with and without optimization:

```bash
python3 research/rank-eleven-residual-partition-audit.py
python3 -O research/rank-eleven-residual-partition-audit.py
```

The program uses `Fraction` arithmetic and explicit `RuntimeError` guards. It
freezes every structural row, checks color mass and component ranks, and does
not rely on `assert`.

## Exact lower-rank ledger

Write `T=C3`, `P=C5`, and `A_k=T^k` for an all-triangle shared-cut cluster.
The audit enters only the already proved rank-at-most-ten bounds:

```text
A_1,...,A_10:       margins 0,1,2,3,2,1,0,0,0,0, all strict;
Q:                  >= -1;
TQ:                 > 0;
rank 2 or 3 cactus: >= 0;
rank 4,...,10:      > 0;
P:                  > -1/4;
TP:                 > 3/4;
PP:                 > 0;
TPP:                > 3/2.
```

A colored partition is direct when its exact rational lower bounds have
positive sum, or zero sum with at least one strict packet. No rank-eleven
connected packet is entered: every proper part has rank at most ten.

## Exact counts and direct rows

| residual | all partitions | proper | direct | structural |
|---|---:|---:|---:|---:|
| `T^10Q` | 139 | 138 | 133 | 5 |
| `T^9PP` | 267 | 266 | 253 | 13 |

Thus the direct ledgers are exactly `138=133+5` and `266=253+13` after the
one-cluster row is removed.

The five `T^10Q` structural rows are

```text
Q|10T
Q|3T|A_7
Q|2T|A_8
Q|T|A_9
Q|A_10
```

The thirteen `T^9PP` structural rows are

```text
P|P|9T
P|P|2T|A_7
P|P|T|A_8
P|P|A_9
P|7T|T^2P
P|6T|T^3P
P|5T|T^4P
P|4T|T^5P
P|3T|T^6P
P|2T|T^7P
P|T|T^8P
P|T^2P|A_7
P|T^9P
```

Here `kT` means `k` singleton-triangle clusters, not one `A_k` cluster.

## Minimal structural endpoints

The same elementary reduced-tree operations used at rank ten suggest the next
minimal targets: remove a singleton-triangle leaf, use the forced path when two
nonsingleton marks are the only possible leaves, and group a terminal `TP`
against a connected complementary territory of rank at most ten. The candidate
endpoint forms are:

```text
A_10|Q,
T^9P_0|P_1,
P_0|A_9|P_1,
P_0|A_7|T^2P_1.
```

The scalar and elementary reductions motivating this list are transparent in
the frozen rows. In `Q|10T`, some singleton triangle must be a leaf. In
`P|P|9T` and every `P|sT|T^kP` row with `s>0`, a singleton leaf gives a strict
triangle and strict rank-ten complement; if no singleton is a leaf, the two
nonsingleton marks are the only leaves, forcing a path and a terminal `TP`
split. The short rows ending in `A_7`, `A_8`, or `A_9` admit the analogous
leaf/path tests, while `Q|A_10` and `P|T^9P` already have only two marks. In
`P|P|A_9`, the scalar-unresolved order has `A_9` between the pentagons. This
identifies the first three candidate forms. A separate graph-level topology
audit is still required to prove that every branching arrangement in the
short rows reduces legally; the executable deliberately does not claim that
exhaustion.

The first three are the direct rank-eleven analogues of the rank-ten endpoint
ladder. The fourth is new. It comes from `P|T^2P|A_7`: if `A_7` is a reduced-
tree leaf, its complement is a strict connected rank-four packet; if either
mixed mark is internal, that mark can be grouped toward the other mixed mark,
again producing lower-rank strict packets. The only scalar-unresolved order is

```text
P_0|A_7|T^2P_1,
```

with component ranks `(1,7,3)` and ordinary ledger `-1/4+0+0`. As with
`P_0|A_9|P_1`, the bars record reduced-tree order and therefore two actual
interfaces at the middle all-triangle cluster; they do not contract or assign
a connector.

For `Q|A_10` and `P|T^9P`, the component ranks are `(1,10)`. For
`P|A_9|P`, they are `(1,9,1)`. The executable checks that every endpoint rank
sum is exactly eleven and every individual component lies within the proved
rank-at-most-ten input. It also checks that each listed source row is among the
frozen structural rows and that their exact ordinary ledgers are respectively
`-1`, `-1/4`, `-1/2`, and `-1/4`.

## What remains unchecked

The endpoint list is a target list for later topology and marked censuses, not
an exhaustive graph reduction or a closure result. A theorem-level argument
would still need the graph-level structural pruning audit, exact one- and
two-interface certificates with arbitrary attached trees, legal ownership of
every bridge remnant, and treatment of fully shared rank-eleven incidence
trees. None of those claims is made here.
