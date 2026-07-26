# Rank-ten `T^9Q` template closure: fully shared and disconnected

**Date:** 2026-07-26

## Verdict

Every fully shared or disconnected-shared-cut rank-ten cactus with cyclic
multiset

```text
T^9Q,  T=C_3,  Q=C_q,  q>=3,
```

has `sigma(G)=s+(G)-|V(G)|>0`. This includes arbitrary hostile
`Q=C_(4k+1)`, arbitrary connector lengths and arbitrary finite tree
attachments. The proof uses no two-pivot winding statement.

The exact verifier is
`research/rank-ten-t9q-template-closure-verifier.py`. It closes the previously
open disconnected obligation `A_9|Q`, independently rechecks the three hostile
fully shared census exceptions, verifies the finite split ownership data, and
is fail-closed under `python -O`.

This note closes the `T^9Q` half of the rank-ten residual frontier. It does not
close any `T^8PP` obligation and therefore does not prove the full rank-ten
cactus theorem.

## Inputs

Write

```text
delta_q=sec(pi/q)-1  for q=1 mod 4.
```

Only the following established inputs are used.

1. Every connected cactus of rank `2,...,9` is strict.
2. An isolated hostile `Q` satisfies `sigma(Q)>-1`; `TQ` is strict and `TTQ`
   is nonnegative.
3. The triangular margins used by the router ledger are

   ```text
   A_1>0, A_2>1, A_3>2, A_4>3,
   A_5>2, A_6>1, A_7>0, A_8>0.
   ```

4. The common-cut scalar theorem closes the common-cut `T^9Q` packet.
5. The rooted packing-one hostile-cycle lemma gives

   ```text
   sigma(H)>a-delta_q
   ```

   for one hostile cycle joined directly or by an arbitrary path to `a`
   triangles of vertex-packing number one, with arbitrary trees attached.

The last theorem is exactly
`research/octacyclic-packing-one-hostile-cycle-lemma-2026-07-26.md`. Its rank
parameter `a>=1` is unrestricted; only the triangular packing-one hypothesis is
required.

## Disconnected reduction

Contract maximal shared-cut cyclic clusters while retaining every actual
bridge connector. The cluster graph is a tree. The rank-nine theorem permits
the standard leaf and path pruning: a proper all-triangle leaf is strict and
its rank-at-least-two complement is strict; a triangle adjacent to `Q` may be
paired into a strict `TQ` terminal packet. The unique endpoint not removed by
this argument is

```text
A_9 | Q.                                                (D10-Q)
```

The bar is an actual bridge path. Mark its first cyclic-hull entry in the
nine-triangle cluster. Every entry is either a shared cut or one of the actual
private vertices of a triangle. Entries through off-hull rooted trees project
to that unique hull attachment, and all connector remnants stay with the
entry's territory.

## Exact marked `A_9|Q` census

The verifier enumerates all pure nine-triangle incidence trees and all marked
entry orbits:

```text
unmarked A_9 incidence trees:                 355
marked entries before automorphisms:         6745
canonical marked A_9|Q rows:                 3624
finite-router rows:                          3618
explicit replacement rows:                     6
```

The frozen digests are

```text
all marked rows:
8ecf4f9f27f2f8bf9c41e85576b398fc7b9f85211386ee9e8c19413e675a0ad7

six replacement rows:
071cc2cbfc800a95b7128043b654f87aecf6b490542deaac89ca33293684c2f1
```

For each accepted row, the verifier splits one triangle at its two or three
occupied cyclic marks. It checks that the resulting incidence branches are
disjoint and exhaustive and that the marked connector has one owner. If the
`Q` territory retains `k` triangles, the exact ledger is:

```text
k=0:  Q>-1; the other eight triangles occupy at most two branches,
      one of size at least four and hence of margin >3;
k=1:  TQ>0;
k=2:  TTQ>=0 and another triangular branch is strict;
3<=k<=8: the retained rank-(k+1) T^kQ packet is strict.
```

The uniform one-interface automaton accepts exactly the rows with triangular
credit at least one. Its exact credit census is

```text
credit 0:    6
credit 1:    4
credit 2:   28
credit 3:  171
credit 4:  879
credit 5: 1548
credit 6:  988.
```

The six non-router rows are exactly:

1. the common-cut `A_9` bouquet entered at its hub;
2. the same bouquet entered at a private triangle vertex;
3. four marked-entry orbits on one two-cut saturated extension.

In the first two rows all nine triangles have packing number one, regardless
of the entry position. Apply the packing-one theorem to the actual joining path
and `Q` to get `sigma>9-delta_q>0`.

On one extension orbit the marked connector follows the opened leaf interval;
this gives a strict `TQ` packet and a strict common-cut `A_8` remainder. In the
other three extension orbits, open the unique leaf triangle opposite the
eight-triangle common-hub lobe. The opened private territory is one nonempty
tree and costs exactly `-1`. The retained eight triangles have packing number
one and carry the actual joining path to `Q`, so

```text
sigma(G)>(8-delta_q)-1=7-delta_q>0.
```

This proves every marked `A_9|Q` row. No assumption is made about connector
length, entry coincidence with a shared cut, or attached trees.

## Fully shared census

The hostile ordinary-split census is exhaustive. At `q=5` it has `8011`
canonical incidence trees, and at saturated capacity nine it has `8049`. In
both hostile regimes exactly three rows survive ordinary splitting. The
verifier independently reruns every one-cycle split, checks that retained cuts
have unique owners, matches the three frozen canonical signatures, and checks
the following replacements.

### Q1: common cut

All ten cycles share one cut. The common-cut scalar theorem closes this row. In
the hostile ledger its integer triangular margin is nine before the hostile
deficit.

### Q2: packing-one tail

All nine triangles share one hub; `Q` is attached through one router triangle
at its other cut. Hence the triangular family has packing number one. The
packing-one theorem applies to the joining segment through the router and gives

```text
sigma(G)>9-delta_q>0.
```

### Q3: leaf opening

The verifier identifies a unique leaf triangle whose removal leaves eight
triangles on one common hub. It also checks that the common-hub lobe and the
leaf meet through a unique saturated router and that `Q` is outside the hub.
Open that leaf at its cut with the router. Its private vertices and all branches
rooted there form one nonempty tree of exact surplus `-1`. The retained eight
triangles have packing number one and retain the complete joining path to `Q`.
Therefore

```text
sigma(G)>(8-delta_q)-1=7-delta_q>0.
```

These are the three census exceptions requested in the hostile regime. For
nonhostile `Q`, the ordinary ledger is stronger and leaves only Q1, already
closed by the scalar theorem. The census stabilizes at capacity nine because
`Q` can meet at most the nine other cycle nodes in an incidence tree.

## Ownership and arbitrary trees

Every global disconnected separation is at an actual bridge. Connector
vertices and branches on them remain in one endpoint territory. At a triangle
router, two marks induce intervals of sizes `1+2`, while three marks induce
three singleton intervals. Each incidence branch, connector entry and off-hull
tree follows its unique mark owner. Opening a leaf triangle assigns its two
private vertices and every tree rooted there to one opened tree territory and
retains the shared cut with the cyclic packet.

The verifier checks cycle coverage, branch disjointness, legal triangle degree,
unique marked-entry ownership, connected incidence representatives and unique
retained-cut ownership. The cited interface theorem upgrades these finite
owners to connected induced, disjoint and exhaustive graph territories. The
common-cut and packing-one inputs are already uniform over arbitrary rooted
trees and arbitrary joining paths.

## Reproduction

Run from the repository root:

```bash
python3 research/rank-ten-t9q-template-closure-verifier.py
python3 -O research/rank-ten-t9q-template-closure-verifier.py
```

Both commands must report `3624=3618+6` on the disconnected marked kernel and
three closed exceptions in each hostile fully shared regime. All classifications
use integer or `Fraction` arithmetic; no floating-point sign decision occurs.

## Conclusion

The disconnected and fully shared cases exhaust the `T^9Q` residual family.
The marked census closes every disconnected endpoint, and the independently
checked ordinary-split census plus Q1--Q3 replacements closes every fully
shared incidence. Therefore every connected rank-ten `T^9Q` cactus is strict,
for every `q>=3`, including arbitrary hostile `q=1 mod 4`.
