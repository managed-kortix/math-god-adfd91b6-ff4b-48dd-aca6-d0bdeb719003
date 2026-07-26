# SUPERSEDED: uncut-connector attempt for disconnected `G6PP`

**Date:** 2026-07-26

## 1. Verdict

> **SUPERSEDED -- NOT A PROOF DEPENDENCY.** The `877=868+9` / E1--E9 narrative
> is retained as audit history only. It must not be used to prove `(G6PP)`.

**Superseded.** The `868+9` uncut-connector narrative is not a complete proof.
The E1--E9 follow-up validates only E5, E8, and E9; E1--E4 and E6--E7
incorrectly separate `P_1` from a root owner retaining clustered cycles. No
completeness claim in this note is authoritative. The complete replacement is
the strict-last-bridge certificate `877=861+16`, with `16/16` closure and no
residual, in
`research/octacyclic-t6p-last-bridge-conservative-resolution-2026-07-26.md`.

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

**Historical withdrawn claim (do not cite):** The disconnected entry-locked row

```text
T^6P_0 | P_1                                             (G6PP)
```

was claimed to be proved without a rooted guard. The attempted proof treats the connector entry as a
marked cyclic-hull position, keeps the connector to the remote pentagon `P_1`
uncut, and partitions the entire `T^6P_0` side by connector-aware
cycle intervals. Ordinary one-triangle splits prove 868 of 877 exact marked
incidence classes. The nine exceptions are closed by common-cut packets and at
most two successive triangle-router splits. The weakest ledger is

```text
sigma(G)>1-2delta=5-2sqrt(5)>0.                          (1.1)
```

This includes entry at the unique `P_0` cut, every remote entry in the
triangular component, private triangle entries, entries through rooted trees,
arbitrary connector length, Steiner branches, and arbitrary attached trees.

No rooted `T^6P` inequality and no `9/4` six-triangle kernel theorem is needed.
The latter would also suffice after opening both pentagons, but it is not an
available input and is not part of this proof.

## 2. Exact normal form

Let `A` be the connected shared-cut cluster of six triangles. The clustered
pentagon `P_0` is an incidence leaf, meeting `A` at its unique cyclic cut. The
remote pentagon `P_1` is joined by an arbitrary positive connector whose first
cyclic-hull entry is a vertex of the triangular component. The entry may equal
the `P_0` cut.

The cycle-cut incidence object on `A+P_0` is a bipartite tree with six
interchangeable triangle nodes, one distinguished pentagon node, and cut nodes.
Triangle degree is at most three, pentagon degree is at most five, and every cut
has degree at least two. The exact color-preserving census gives

```text
all T^6P_0 incidence trees:       226,
P_0-leaf incidence trees:         111,
marked cyclic-entry root classes: 877.                  (2.1)
```

The marked count includes every shared cut and every private cyclic triangle
vertex, modulo the automorphism group of the colored incidence tree. A degree
one triangle contributes one private orbit representing its two symmetric
private vertices; a degree two triangle contributes its unique private vertex.
Thus (2.1) covers the locked cut roots as well as all private roots. Connector
lengths and hanging trees are not census parameters because they follow their
unique entry owner.

## 3. Global connector partition

Keep the connector to `P_1` uncut and assign its whole territory to the marked
root interval. When that interval retains no clustered cycle, the resulting
packet is a pentagonal unicyclic cactus and therefore

```text
sigma(H_1)>=-delta.                                     (3.1)
```

When the root interval retains clustered cycles, its packet profile instead
contains those cycles and `P_1`, exactly as charged in the marked census.
Every Steiner branch and hanging subtree follows its unique first attachment.

Choose a triangle router `R`. Deleting its cycle node separates its incidence
sides. Their marks occupy distinct vertices of `R`; a private connector entry
on `R` is an additional mark. Partition `R` into nonempty proper consecutive
intervals, one owner for each side and for the connector when it is marked on
`R`. Every incidence branch, connector remnant, and off-core tree follows the
interval owning its attachment. The resulting territories are connected,
induced, disjoint, and exhaustive.

Two-stage intervals are legal. A second router is split only inside the
territory produced by the first split. Refinement of an induced partition by an
induced partition remains induced; a shared cut already has one owner, and the
second split only refines that owner's territory. A split-router remnant is a
tree and retains no cyclic block.

The exact one-router verifier applies this operation to all 877 marked classes,
using only established unrooted packet bounds. It resolves 868 and leaves nine
classes E1--E9. Their distribution by number of cut nodes is

```text
c=1,2,3,4,5,6:  2,3,3,1,0,0.                           (3.2)
```

Thus all high-cut and generic entry incidences are already settled; only the
five low-cut structural forms represented by E1--E9 require explicit joint
packetizations.

## 4. The nine entry-locked forms

The complete replacement packet ledger is:

| classes | connector-side operation | final clustered-side packets | total surplus |
|---|---|---|---:|
| E1--E2 | retain common-cut hub | common-cut `T^6P_0` | `>6-2delta` |
| E3--E4 | split hub-tail router | `P_0+A_5` | `>2-2delta` |
| E5 | split pentagon-hub router | `T+` common-cut `T^4P_0` | `>4-2delta` |
| E6--E7 | split saturated router | `T+P_0+A_4` | `>3-2delta` |
| E8 | split two binary routers | `T+P_0+A_3` | `>2-2delta` |
| E9 | saturated split, then binary split | `T+T+P_0+A_2` | `>1-2delta` |

In every row the separate remote packet `P_1` contributes the second
`-delta`; it is included in the displayed total. The clustered-side bounds are

```text
sigma(P_0)>=-delta,
sigma(A_r)>r-1 for 1<=r<=4,
sigma(A_5)>2,
sigma(common-cut T^kP_0)>k-delta.                        (4.1)
```

E1--E2 are the two common-cut marked roots. They require no split: the exact
common-cut theorem absorbs `P_0` into the six-triangle bouquet, regardless of
whether the connector remnant is rooted at the common cut or privately on a
triangle.

E3--E7 use one router split. E8 uses two binary routers. E9 first splits a
saturated router into its three marked singleton intervals and then splits a
binary router inside the hub-owning territory. The final E9 packets are exactly

```text
T + T + P_0 + A_2 + P_1,
```

so (4.1) and (3.1) give

```text
sigma(G)>0+0-delta+1-delta
        =1-2delta
        =5-2sqrt(5)>0.                                  (4.2)
```

This was the claimed weakest row. The assertion that all nine exceptional
marked roots are positive is withdrawn by the superseding verdict above.

## 5. Relation to separate pentagon pairing and `9/4` kernels

A literal universal partition into two retained packets `TP_0` and `TP_1` is
not available when both interfaces meet the same articulation: both connected
packets would have to own that vertex. The successful proof therefore pairs
the pentagons separately only at the level actually permitted by ownership:
`P_1` is a remote unicyclic territory, while `P_0` is either absorbed by a
common-cut triangle packet or isolated by one or two triangle-router splits.
This is the connector-side joint partition used in Section 4.

There is an alternative conditional reduction. Opening one private vertex on
each pentagon leaves a connected six-triangle cactus with arbitrary attached
trees and incurs two exact `-1` territories. Therefore a universal kernel bound

```text
sigma(K)>9/4
```

would imply `sigma(G)>1/4`. The established recurrence gives only
`sigma(K)>1`, so that route cannot currently be used as a proof. More
importantly, it is unnecessary: the common-cut and two-stage interval packets
retain enough cycle structure to obtain the stronger ledgers in Section 4.

## 6. Exact status and reproduction

The proof is universal over all disconnected `(G6PP)` graphs because the
incidence census is exhaustive in the only finite parameters, the root mark is
exhaustive up to colored automorphism, and all noncyclic material follows a
unique interval or connector owner. No numerical spectrum or arbitrary-tree
approximation is used.

Run the exact certificates from the repository root:

```bash
python research/octacyclic-t6p-marked-root-incidence-census.py
python research/octacyclic-t6p-nine-exceptions-resolution.py
```

The first reproduces the restricted `877=868+9` list. The second now rejects
six E1--E9 ownership partitions; it is an erratum check, not a completeness
certificate.

Consequently the displayed E1--E9 packet list must not be cited as a complete
proof. The strict-last-bridge replacement, not this uncut construction, proves
that `(G6PP)` has no residual marked kernel.
