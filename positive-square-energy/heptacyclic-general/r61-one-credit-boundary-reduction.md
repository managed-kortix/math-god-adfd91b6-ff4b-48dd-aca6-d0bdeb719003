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

After applying these two gates, the exact R61 residual initially consists of the
non-DNN structural rank-six owner states at their canonical physical
realizations:

```text
R61-K110-0: all-unit K5 + Q;
R61-K110-1: exactly one long odd K5 path + Q;
R61-K223:   canonical all-unit K223 + Q.
```

Here `Q` may have any length and its shared cut may be any vertex of the
displayed rank-six realization, including the interior of the unique long path
in `R61-K110-1`. The K223 family is now closed by the exact two-orbit coupled
packet in `r61-k223-marked-cycle-packet.md`. The two K110 families are closed by
the shared-cut spectral packet below. Thus R61 has no remaining configuration.

## Exact shared-cut K110 packet

Use induced square-energy superadditivity. An actual attached `K4` has
`sigma>2`; a nonempty induced tree has `sigma=-1`; and a connected unicyclic
packet has `sigma>-1`. Hence an induced vertex partition into an actual
attached `K4` packet `A` and `r<=2` connected tree or unicyclic packets `U_i`
satisfies the exact shared-cut inequality

`sigma(G)>=sigma(A)+sum_i sigma(U_i)>2-r>=0`.                 (1)

The cut is assigned once, to one displayed territory. Crossing edges are
absent from the induced pieces, and each rooted tree follows its root.

### `R61-K110-0`

Let `x` be the marked cut. Assign `x`, all of `Q`, and their rooted trees to one
connected unicyclic territory. The other four K5 vertices induce an actual
attached `K4`. Formula (1), with `r=1`, closes the unique `Aut(K5)` cut orbit
for every cycle length.

### `R61-K110-1`

Write the long odd path as

`P: a=v_0,v_1,...,v_l=b`, with `l=2h+1>=3`,

and denote the other branch vertices by `c,d,e`. The long-edge stabilizer has
the following marked-cut orbits:

1. the endpoint orbit `{a,b}`;
2. the off-edge branch orbit `{c,d,e}`;
3. the internal distance orbits `min(j,l-j)=1,...,h`.

Thus canonical length three has one internal orbit, and each same-parity
lengthening merely adds the next distance orbit. The packet below is uniform
in `j` and `l`, so monotonicity leaves no additional minimal length case.

If `x` is an endpoint, the other four branch vertices induce an actual `K4`;
the omitted endpoint, the internal vertices of `P`, and `Q` induce one
connected unicyclic territory. If `x=v_j` is internal, omit `a`; then
`{b,c,d,e}` induces the actual `K4`, while `v_0,...,v_(l-1)` together with `Q`
induces one connected unicyclic territory. Formula (1) applies with `r=1`.

If `x` is off the long edge, retain the actual `K4` on `{b,c,d,e}`, including
`x`. The vertices `v_0,...,v_(l-1)` induce one nonempty tree, and `Q-x` induces
a second nonempty tree. Assign `x` and its rooted tree to the `K4`. Formula (1)
applies with `r=2`; strictness of the attached-`K4` inequality closes this
tight orbit.

These partitions exhaust all cut orbits, all odd long-path lengths, all cycle
lengths, and arbitrary rooted-tree attachments. They do not assert an
excess-five Gram for the one-long rank-six block.

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

## Why only the three structural keys arise

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
budget five. Thus relabeling `R61-K110-1` as DNN-owned is unavailable. The
shared-cut packet above instead spends the strict attached-`K4` credit against
the internal path territory and the external cycle territory simultaneously.

Likewise, the K223 structural proof partitions the rank-six block into an
attached K4 and one nonempty tree. Its `>2-1` accounting closes the rank-six
graph but does not expose a uniform additional unit after an arbitrary cycle
is attached at an arbitrary vertex. Applying the unmarked rank-six conclusion
and deleting `Q-x` would again charge a tree of credit `-1` without a proved
unit of margin.

## Completed exact obligation

The two K110 rows are closed by a shared-cut spectral packet with every rooted
tree assigned once. No step deletes `Q-x` and invokes only the nonstrict
rank-six theorem.

For completeness, `R61-K223` has exactly two marked-cut orbits,
`{0,1,2,3}` and `{4,5}`. In every orbit a marked actual `K4` can be retained;
the other two kernel vertices induce one edge. Retain the attached `K4`, and
boundary-open the cycle at the marked cut. The `K4` credit greater than two
pays the complementary kernel tree and the cycle-minus-cut tree strictly.

## Ledger update

The owner registry entry `R61-NDNN: B_6^struct+Q` is the disjoint union of the
three typed keys above. `R61-K223` is closed by its marked-cycle packet and both
K110 keys are closed by (1). All other physical R61 states are owned by the
bridge split or the shared-Gram DNN gate. Therefore the complete `R61` row is
closed.
