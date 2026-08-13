# Heptacyclic multiblock theorem: complete owner-exact ledger

## Theorem and exact scope

For a connected graph `X`, put

`sigma(X)=s^+(X)-|V(X)|`.

**Theorem.** Let `G` be a finite simple connected graph of cyclomatic rank
seven with at least two positive-rank cyclic blocks. Then

`s^+(G)>=|V(G)|`.

The statement includes arbitrary legal subdivisions, arbitrary block-cut
incidence, arbitrary bridge connectors, repeated or nested attachment cuts,
and arbitrary finite rooted-tree attachments. It is only the multiblock
theorem. The partition `(7)`, and hence any claim about all connected
heptacyclic graphs, is outside its scope.

## Block split and ownership contract

Cyclomatic rank is additive over positive-rank blocks: adjoining a block at
one cut vertex adds `|E(B)|-|V(B)|+1`. Thus the positive block ranks form one
of the fifteen integer partitions of seven. Exactly fourteen have at least two
parts; `(7)` is disjoint from the theorem.

If the cyclic hull contains an actual bridge, deletion of that bridge gives
two connected induced sides of ranks between one and six. The complete
lower-rank theorems give nonnegative credit on both sides. Otherwise the cyclic
hull is bridge-free and all incidences below occur through shared cuts.

Every packet uses the following owner assignment before credit is charged.

1. A shared boundary cut belongs to the upstream territory only.
2. A boundary-open block contributes its cut-deleted downstream side, all path
   remnants there, and every descendant rooted away from the cut.
3. A structural opening takes the opened internal vertex and its complete
   physical owner class; endpoint remnants remain retained unless its cited
   structural theorem explicitly assigns them otherwise.
4. Nested demands remain one complete first-boundary territory until an
   explicit later opening; an intermediate cut is never copied.
5. Every rooted tree, connector remnant, and deeper descendant follows its
   unique first physical owner. Positive connectors occur only in the preceding
   actual-bridge branch.

These rules make the bridge, DNN, and packet-owner dispositions disjoint and
exhaustive.

## Complete fourteen-partition ledger

The exact DNN sieve and its arithmetic are those of
`rank-seven-multiblock-debit-ledger.md`: for `k` positive-rank blocks the debit
allowance is `k-1`, equality is DNN-closed, and only the displayed physical
residuals pass to packet owners. The final ledger is:

| partition | bridge-free disposition after the exact DNN gate |
|---|---|
| `1^7` | rank-uniform cactus theorem; no packet residual |
| `2+1^5` | `R21` |
| `2+2+1^3` | `R221` |
| `2+2+2+1` | DNN, since `3alpha+1<3` |
| `3+1^4` | `R31-S`, `R31-K` |
| `3+2+1+1` | `R321` |
| `3+2+2` | `R322` |
| `3+3+1` | `R331-S`, `R331-K` |
| `4+1^3` | `R41` |
| `4+2+1` | `R421` |
| `4+3` | `R43` |
| `5+1+1` | `R511-K5e`, `R511-K22`, `R511-K71` |
| `5+2` | `R52-K22`, `R52-K71` |
| `6+1` | `R61-K110-0`, `R61-K110-1`, `R61-K223` |

There are no other packet-owner keys. The first DNN sieve is exact on actual
certificate excesses, not on an inferred spectral margin. In particular,
structural K22, K71, S3, S4, and rank-six states are never silently promoted to
DNN owners.

## Packet closure

The two-debit induced-piece theorem closes

`R331-S, R331-K, R43, R52-K22, R52-K71`.

Its owner ledger regenerates the four K22 and nine K71 structural targets and
covers separate, repeated-cut, nested, opened-owner, and retained-owner routes.

The nested induced-piece theorem closes

`R21, R221, R31-K, R321, R322, R41, R421, R511-K5e, R511-K71`.

It regenerates the `53+640` all-odd K5-e targets and all nine K71 targets. Its
historical returned set is exactly `R31-S, R511-K22`; no conclusion for those
two keys is imported from that theorem.

The subsequent marked packets close both returned keys. For `R31-S`, the
canonical doubled-`C4` census has exactly 110 marked records: 54 balanced, 28
one-sided `C4`, and 28 one-sided `D3`. The balanced records and the independently
proved marked four-triangle and diamond territories leave no residual. For
`R511-K22`, the four exact structural targets have 178 labeled marked two-cycle
orbits. A strict `e_22<21/5` Gram closes every profile containing a
nontriangle, and the remaining two-triangle packet gives `>3-1-1>0` (or the
stronger routed-owner ledger `>2+0-1>0`).

Finally, `R61` has exactly three structural keys after the actual-bridge and
shared-Gram gates. The two K110 rows are closed by the marked shared-cut
attached-`K4` partitions in `r61-one-credit-boundary-reduction.md`, uniformly
over every odd long-path length and every cycle length. The canonical K223 row
has exactly two marked-cut orbits and is closed by its dedicated packet. Hence
all nineteen packet-owner keys are closed.

Combining the actual-bridge branch, every exact DNN row, and these disjoint
packet owners proves the theorem.

## Fail-closed audit

From the repository root run

```text
python3 research/heptacyclic-multiblock-master-verifier.py
python3 -O research/heptacyclic-multiblock-master-verifier.py
```

The master regenerates all fifteen partitions, requires exactly the fourteen
non-`(7)` rows, checks the nineteen-key owner ledger and the empty final
residual, locks every source and child verifier, and invokes every packet
verifier separately in normal and optimized mode. It accepts only each child's
exact scoped output and rejects scope widening, omitted owners, overlaps,
changed partitions, reopened residuals, or an all-heptacyclic promotion.
