# Heptacyclic multiblock program: fail-closed reduction with a bridge blocker

## Current status and scope

For a connected graph `X`, put

`sigma(X)=s^+(X)-|V(X)|`.

The target statement is:

> If `G` is a finite simple connected graph of cyclomatic rank seven with at
> least two positive-rank cyclic blocks, then `s^+(G)>=|V(G)|`.

The intended scope includes arbitrary legal subdivisions, arbitrary block-cut
incidence, arbitrary bridge connectors, repeated or nested attachment cuts,
and arbitrary finite rooted-tree attachments.  The partition `(7)` is outside
this multiblock program.

**Status: open.**  The physical `R31-S` packet is now closed by
`r31-s-physical-shared-triangle-closure.md` and its full-parent adjacency gate.
The old `D3` obstruction was a synthetic topology and is not used.  However,
the global reduction still contains an invalid generic hull-bridge sentence:
a positive rank-one side need not have nonnegative credit (`C5` has
`sigma(C5)=2-sqrt(5)<0`).  Until every other packet's hull-bridge case receives
an oriented or packet-specific repair, this note makes no all-multiblock or
all-heptacyclic conclusion.

## Block split and ownership contract

Cyclomatic rank is additive over positive-rank blocks, so their ranks form one
of the fifteen integer partitions of seven.  Exactly fourteen have at least
two parts.  An actual bridge in the cyclic hull always gives two connected induced
sides, but positive rank alone does not certify both credits: rank one is the
unicyclic exception.  A packet may discard its bridge row only after orienting
the bridge and proving that any rank-one side is strict positive (as the
triangular away side is in `R31-S`) or after supplying another exact debit
argument.  Otherwise all retained incidences are through shared cuts.

Every packet assigns vertices before charging credit:

1. a shared boundary cut belongs to the upstream territory only;
2. a boundary-open block contributes its cut-deleted downstream side, all path
   remnants there, and all descendants rooted away from the cut;
3. a structural opening takes the opened internal vertex and its complete
   physical owner class;
4. nested demands remain one complete first-boundary territory until an
   explicit later opening; an intermediate cut is never copied; and
5. every rooted tree, connector remnant, and deeper descendant follows its
   unique first physical owner.

## Exact fourteen-partition ledger

The exact DNN sieve is recorded in
`rank-seven-multiblock-debit-ledger.md`.  The bridge-free packet registry is:

| partition | disposition after the exact DNN gate |
|---|---|
| `1^7` | rank-uniform cactus theorem |
| `2+1^5` | `R21` |
| `2+2+1^3` | `R221` |
| `2+2+2+1` | DNN |
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

There are nineteen packet keys.  The two-debit theorem closes

`R331-S, R331-K, R43, R52-K22, R52-K71`.

The nested induced-piece theorem closes

`R21, R221, R31-K, R321, R322, R41, R421, R511-K5e, R511-K71`.

The later exact packets close `R511-K22` and all three `R61` keys.  In `R31-S`, the historical balanced/`C4`/`D3` labels are superseded by
physical adjacency reconstruction.  The ordered hull-bridge, connector-fibre,
and two-shared-cut-cactus dispatch closes that packet.  The conservative
machine ledger still records `{R31-S}` as its global fail-closed residual until
the upstream bridge cascade is repaired; it must not be interpreted as a
remaining `D3` analytic obligation.

## Why the global master is still open

The physical `R31-S` closure reconstructs the full parent graph before making
any debit.  If a hull bridge occurs, it is oriented away from the rank-three
block; the away side is a strict-positive triangular cactus of rank `q`, while
the root side has rank `7-q in {3,4,5,6}`.  If a connector-interior complete
fibre contains `q` triangles, it is strict positive and its complement has rank
`6-q in {2,3,4,5}`.  Only after both dispatches are excluded are the two exact
tree charges and the rank-sum-five triangular split used.

That argument is specific to `R31-S`.  The previous master sentence treated
*every* actual hull bridge as two nonnegative positive-rank sides.  This is
false when one side has rank one: for example `C5` has negative credit.  The
other packet proofs were developed downstream of that sentence and have not
all been audited with an oriented strict-positive rank-one side.  Promoting the
master now would therefore overclaim beyond the passing `R31-S` gate.

## Fail-closed audit

From the repository root run

```text
python3 research/heptacyclic-multiblock-master-verifier.py
python3 -O research/heptacyclic-multiblock-master-verifier.py
```

Both invocations authenticate the exact fourteen-partition ledger, run every
closed packet and finite prerequisite (including the passing physical `R31-S`
gate) in normal and optimized mode, reject hostile scope/ownership mutations,
and exit with status `1`.  The output names the global hull-bridge repair as
the blocker.  The nonzero exit is intentional; a global `COMPLETE` receipt
would currently overclaim.
