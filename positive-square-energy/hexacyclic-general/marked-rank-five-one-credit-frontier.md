# Marked rank-five one-credit packet: rigorous frontier

## Question

Put

`sigma(X)=s^+(X)-|V(X)|`.

The physical edge-opening lemma for an order-eight rank-six block deletes an
internal vertex and its rooted tree. The retained graph `H` is a connected
rank-five block tree with two marked path-remnant interfaces. Since the deleted
territory is a nonempty tree of credit `-1`, the desired induction requires

`sigma(H)>=1`.                                                (1)

This note records exactly what follows from the complete pentacyclic theorem
and its certificates. The conclusion is a failure characterization, not a
claim that (1) is false.

## Theorem (marked deletion dichotomy)

Let `H` be any connected graph of cyclomatic rank five, with arbitrary rooted
trees and with any two vertices marked. Write its cyclic-core edge count as
`M` and its attached-tree edge count as `t`. Then:

1. `sigma(H)>=0`.
2. If `H` has a DNN correlation certificate satisfying

   `kappa(H)<=M+3+t`,                                         (2)

   then `sigma(H)>=1`.
3. More generally, if `Pi_+` is the positive spectral projector of `A(H)` and
   one can exhibit any positive semidefinite trial matrix `X` for which

   `2 tr(A(H)X)-tr(X^2)>=|V(H)|+1`,                           (3)

   then `sigma(H)>=1`.
4. The complete all-pentacyclic certificate library establishes item 1 for
   every `H`, but it does not establish item 2 or item 3 uniformly. Thus the
   existing pentacyclic theorem alone cannot pay the opened tree.

### Proof

The marks do not affect the adjacency spectrum. Item 1 is the complete
connected pentacyclic theorem.

Rank five gives `|V(H)|=M-4+t`. The trace identity and the DNN estimate give

```text
s^+(H) = 2(M+t)-s^-(H)
       >= 2(M+t)-kappa(H).
```

Under (2), the right side is `M-3+t=|V(H)|+1`, proving item 2.

For every real symmetric matrix `A`,

`tr(A_+^2)=max_{X>=0} (2 tr(AX)-tr(X^2))`.

Consequently (3) proves item 3. Item 4 follows by inspecting the exact scope of
the pentacyclic master theorem: its universal DNN budget is excess four, not
three, and several structural branches are not DNN claims at all.             `square`

## Exact failure classes of the existing certificate system

The complete rank-five master has three kinds of records.

1. A strict DNN record with certified excess `E<4`. It pays the opening only
   when the exact recorded inequality is strong enough to give `E<=3`.
   Merely having `E<4` gives a positive but possibly subunit bound and cannot
   be rounded to one.
2. A symbolic budget record with displayed cost exactly four. It proves only
   `sigma(H)>=0` through the DNN route. The order-eight K118 ledger alone has
   30 such signed-cycle records: six physical rows at the canonical target and
   the four singleton-coordinate frontiers `0,5,6,11`.
3. A structural induced-territory record. Its conclusion is the unmarked
   inequality `sigma(H)>=0`; no DNN margin may be inferred from it.

These are failures of the **available implication**, not spectral
counterexamples to (1). In particular, a displayed DNN cost of four is an
upper bound on `kappa`; without a matching lower bound it does not prove that a
cost-three certificate is impossible.

## Why the K118 rows occur in the order-eight opening interface

The obstruction is not irrelevant to the deletion ledger. K118 has support

```text
single: 01,26,35,47
double: 02,17,36,45.
```

Adding one copy of any support or nonsupport pair and canonicalizing gives an
order-eight rank-six kernel. For example, adding one copy of `01` gives K756.
Conversely, deleting the corresponding copy from K756 gives K118. A simple
physical realization uses one direct member and one subdivided member of the
parallel `01` bundle. Opening the internal vertex of the subdivided member
leaves the direct member and therefore a marked K118 realization. The K118
signed-cycle equality ledger contains both singleton parities and the
singleton `+2` frontiers, so this interface cannot be discarded by a simplicity
or parity argument.

The finite combinatorial deletion census therefore genuinely reaches a
rank-five family for which the committed proof object supplies only the
four-unit DNN budget.

## The deletion-edge/projector route

Let `G` be the rank-six graph, let `T` be the opened nonempty tree, and let
`H=G-V(T)`. Induced superadditivity gives

`sigma(G)>=sigma(H)-1`.                                      (4)

There are exactly two valid ways to close this branch without completing the
full rank-six frontier:

1. **DNN slack:** prove (2) for the marked deletion packet.
2. **Projector slack:** construct a trial matrix satisfying (3), possibly by
   starting from `A(H)_+` and exploiting the two marked interfaces or the
   deleted edge.

An argument involving the deleted edge must produce an inequality of size one
in (3). Edge addition by itself is not monotone for `s^+`, and a positive but
unquantified projector gain does not suffice in (4).

## Conclusion

The rigorous result is the dichotomy above. The universal marked spectral
statement (1) is **not proved** by the complete pentacyclic theorem, and the
current certificates do not provide a counterexample to it. The precise
certificate failures are:

- every DNN record with certified excess in `(3,4]`;
- the exact-budget symbolic families, including the 30 K118 order-eight keys;
- every structural record lacking an independent one-unit territory margin.

Accordingly, the order-eight rank-six edge-opening program remains open on
exactly those marked deletions unless a new one-unit projector lemma, a genuine
excess-three DNN certificate, or a direct rank-six frontier certificate is
supplied. Citing the unmarked pentacyclic theorem as `sigma>=1` would be an
invalid strengthening.
