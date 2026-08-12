# R61 one-credit boundary reduction

## Exact result

Let `G` be a finite simple connected graph whose positive cyclic blocks are a
rank-six block `B` and one cycle `Q`. Write

`sigma(X)=s^+(X)-|V(X)|`.

The rank-six theorem closes `G` in either of the following two cases.

1. The cyclic hull contains an actual bridge.
2. The hull is bridge-free, `B` and `Q` meet at a shared cut `x`, and the
   complete rank-six owner of `B` supplies a DNN certificate

   `kappa(B)<=|E(B)|+5`.

In case 2 the certificate and the sharp cycle Gram glue at `x`; no vertex is
deleted. Consequently

`kappa(B vee_x Q)<=|E(B vee_x Q)|+6`,

and arbitrary rooted trees can then be attached at every vertex. Thus

`s^+(G)>=|V(G)|`.

After applying these two gates, the exact R61 residual consists only of the
non-DNN structural rank-six owner states at their canonical physical
realizations:

```text
R61-K110-0: all-unit K5 + Q;
R61-K110-1: exactly one long odd K5 path + Q;
R61-K223:   canonical all-unit K223 + Q.
```

Here `Q` may have any length and its shared cut may be any vertex of the
displayed rank-six realization, including the interior of the unique long path
in `R61-K110-1`. This is a sharp interface reduction, not closure of these
three families.

## Shared-Gram proof

For a graph `H`, use

`kappa(H)=min sum_(uv in E(H)) 2/(1-R_uv)`,

where `R` ranges over correlation matrices. If two graphs meet in one vertex,
their feasible Grams can be glued by identifying the common unit vector and
putting the orthogonal complements in perpendicular subspaces. Hence `kappa`
is additive under a one-vertex sum.

Let `q=|E(Q)|`. The sharp cycle certificate has

`kappa(Q)<=q+epsilon(Q)<=q+1`.

If the rank-six owner is DNN with excess at most five, then

```text
kappa(B vee_x Q)
 <= kappa(B)+kappa(Q)
 <= |E(B)|+5+q+1
  = |E(B vee_x Q)|+6.
```

The rank is seven, so the core has `|V|=|E|-6`. The DNN/trace inequality gives
`s^+>=|V|`. A rooted tree with `t` edges adds exactly `t` to `kappa`, to the
edge count, and to the vertex count, so the same conclusion survives arbitrary
rooted-tree attachments. The shared cut is represented once in the glued Gram;
it is neither deleted nor charged as a tree vertex.

This argument spends the cycle's one allowed unit directly in the Gram budget.
It is therefore valid even when both block certificates are at equality. It is
not the invalid induced-deletion argument `sigma(G)>=sigma(B)-1`, which would
require one full unit of rank-six spectral credit.

## Why only the three structural keys remain

The complete rank-six owner partition has the following relevant form.

- Kernel orders two through four are uniformly DNN-owned.
- Orders seven through ten are uniformly DNN-owned; their symbolic equality
  rows are exact cost-five Grams, not non-DNN structural owners.
- Order eight likewise has only rational or symbolic exact-cost-five owners.
- At order five, the only non-DNN owner is the all-odd K110 (`K5`) family. Its
  structural scope is exactly the canonical all-unit target and the ten
  one-coordinate targets. The canonical target is `R61-K110-0`. Every
  one-coordinate target is an odd length-three subdivision of one K5 edge,
  and `Aut(K5)` is transitive on edges, giving `R61-K110-1`. If at least two
  K5 paths are long, the order-five theorem uses one of two strict DNN
  certificates and fixed-parity lengthening, so the shared-Gram gate applies.
- At order six, the only non-DNN owner is the single canonical all-unit K223
  target, giving `R61-K223`. Every noncanonical same-parity K223 realization
  chooses a DNN-owned one-coordinate frontier, so it is already closed.

The order-five one-long DNN obstruction is numerically very tight but is not a
proof input: its reported optimum is about `5.00582080171`, above the rank-six
budget five. Thus relabeling `R61-K110-1` as DNN-owned is unavailable, while
the theorem's structural deletion uses an attached K4 only to pay the internal
path tree. It records no spare unit for the external cycle boundary.

Likewise, the K223 structural proof partitions the rank-six block into an
attached K4 and one nonempty tree. Its `>2-1` accounting closes the rank-six
graph but does not expose a uniform additional unit after an arbitrary cycle
is attached at an arbitrary vertex. Applying the unmarked rank-six conclusion
and deleting `Q-x` would again charge a tree of credit `-1` without a proved
unit of margin.

## Remaining exact obligation

The present reduction leaves the following sufficient closing alternatives for
each of `R61-K110-0`, `R61-K110-1`, and `R61-K223`, uniformly over the marked
cut orbit and the cycle length:

1. a coupled Gram for `B vee_x Q` of total excess at most six; or
2. a shared-cut spectral packet with nonnegative total credit, with all rooted
   trees assigned once.

For `R61-K110-1`, the marked-cut orbits must distinguish a K5 branch vertex
from an internal vertex of the long path (and may refine branch vertices by
their incidence with the long edge). No argument may delete `Q-x` and invoke
only the nonstrict rank-six theorem.

## Ledger update

The owner registry entry `R61-NDNN: B_6^struct+Q` should therefore be read
exactly as the disjoint union of the three keys above. All other physical R61
states are owned by the bridge split or the shared-Gram DNN gate.
