# Rank-six orders 2--10 master architecture (promotion-gated skeleton)

## Boundary

This is architecture for an implication verifier. It records no theorem claim
and does not modify project state. The verifier is intentionally red until
separate order-nine and order-ten theorem-promotion owners exist, perform full
exact replay, and have frozen source and canonical-output identities.

The scope is exactly the loopless 2-connected rank-six kernel universe with
minimum degree at least three. If a kernel has order `n`, then it has `n+5`
edges, and the degree bound gives `2<=n<=10`. The frozen census partition is

```text
order:   2  3   4   5    6    7    8    9   10
count:   1  4  26  84  216  314  325  162  66
kernel: K1----------------------------------K1198
```

The exact owner partition is:

| owner | orders | kernel interval | count | replay contract |
|:--|:--|:--|--:|:--|
| existing orders-2--7 implication owner | `2,...,7` | `K1--K645` | 645 | canonical child manifest and exact transitive audits |
| existing order-8 theorem owner | `8` | `K646--K970` | 325 | mandatory `--full` exact replay |
| future order-9 promotion owner | `9` | `K971--K1132` | 162 | mandatory full exact replay, not a coverage status |
| future order-10 promotion owner | `10` | `K1133--K1198` | 66 | mandatory full exact replay, not a coverage status |

These order sets and intervals are disjoint, contiguous, and exhaustive. The
master rejects omission, duplication, overlap, changed counts, or any endpoint
other than `K1` and `K1198`.

## Promotion interface

Every direct owner entry binds its source SHA-256, canonical full-replay output
SHA-256, child schema, exact order set, exact kernel interval, fixture identity,
and conclusion. A missing owner or an unset digest closes the gate. A green
coverage verifier, `ready_for_theorem_promotion` field, receipt aggregate, or
acceptance substring is not an owner.

The independent kernel-census verifier is a fifth direct dependency. Its source
and canonical output are pinned, and its regenerated order partition must agree
with both the frozen fixture and all four owner intervals.

The existing orders-2--7 owner is consumed through its canonical
`--print-manifest` interface and exact count/scope/conclusion adapter. The
order-eight owner is invoked with `--full --print-manifest`; an invocation
without `--full` cannot enter the registry. Future order-nine and order-ten
owners must expose the same machine-readable theorem interface and must inherit
or cause a fresh complete exact replay. Their current coverage gates remain
non-theorem dependencies and cannot be registered directly.

## Encoded implication

Only after all four owners pass does the master construct a canonical
implication manifest. Its finite premise is

```text
kappa(B) <= |E(B)|+5
```

for every positive simple subdivision `B` in all 1,198 kernel families. The
owner contracts include arbitrary positive subdivision lengths, obtained from
the exact canonical-plus-coordinate frontier and fixed-parity monotonicity, and
arbitrary finite rooted trees attached at branch or subdivision vertices.

For a subdivided rank-six block with `L` edges, `|V(B)|=L-5`. If attached rooted
trees have `t` edges in total, one-vertex-sum additivity gives
`kappa(G)<=L+5+t`. Combining this premise with the DNN trace identity yields the
encoded conditional conclusion `s+(G)>=|V(G)|` for the owned single-block
families. This implication is not emitted while any owner gate is closed.

Multiblock graphs and an all-connected hexacyclic result are outside the scope.
The master must reject either widening.

## Current fail-closed behavior

Run from the repository root:

```sh
python3 research/rank-six-order2-10-master-verifier.py
python3 -O research/rank-six-order2-10-master-verifier.py
```

Both commands currently exit nonzero. In particular, absent or unregistered
order-nine/order-ten promotion owners are reported as blockers before expensive
child replay. Promotion requires adding those owners and freezing all four
canonical child-output identities; it does not permit weakening this skeleton
or substituting completion status for exact ownership.
