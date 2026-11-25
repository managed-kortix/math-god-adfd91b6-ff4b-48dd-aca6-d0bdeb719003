# Heptacyclic multiblock program: fail-closed reduction with authenticated physical-hull overlays

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

**Status: open.**  The physical `R31-S` packet and universal exactly-two-
positive-block `(4,3)/(5,2)` hull--`K2` slice remain closed.  Two later
physical-hull theorems now close additional nontrivial-hull rows:
`PHYSICAL-UNIT-STAR-DNN` closes every hostile reduced unit-star whose center
component has rank `c<=4`, and the `c=5` row unless both arm cycles are `C5`;
`R61-PHYSICAL-SINGLE-BLOCK` closes the `c=6` one-arm row when the rank-six
center has exactly one positive cyclic block.  Both imported theorems allow
their stated physical bridge chains and finite tree payloads.

Within the nontrivial-positive-hull domain, the resulting open multiblock rows
are `c=5` with arm pair `(C5,C5)` and an arbitrary bridge-free rank-five center
having at least two positive-rank cyclic blocks, and `c=6` with a multiblock
center.  These are outer row types, not a finite graph, center-profile, or port
census.  The first cannot be closed by the same universal all-center DNN
threshold: the allowed multiblock center `K4 vee C3 vee C3`, whose positive-
block profile is `(3,1,1)`, has exact DNN excess five, while that route requires
at most `4sqrt(5)-4`.  This is a certificate-route obstruction, not a graph
counterexample.

The separate one-vertex-positive-hull multiblock lane remains **OPEN,
UNAUTHENTICATED**.  Its unique rank-seven bridge-free component may still
carry actual bridges to rank-zero components.  The nineteen-key equality
below authenticates only a bridge-free packet pass after a registered
packet-specific bridge dispatch; no theorem and verifier currently transport
all such physical bridge forests through all nineteen owners.  The generic
phrase “arbitrary finite rooted-tree attachments” is not that missing global
dispatch.  Partition `(7)` remains outside the multiblock target.  Thus this
note makes no all-multiblock or all-heptacyclic conclusion.

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

The later exact packets close `R511-K22` and all three bridge-free `R61`
keys.  In `R31-S`, the historical balanced/`C4`/`D3` labels are superseded by
physical adjacency reconstruction.  The ordered hull-bridge,
connector-fibre, and two-shared-cut-cactus dispatch closes that packet.

The machine ledger records an empty bridge-free packet residual.  It records
four separate physical overlays without assigning them packet keys: the
physical `R31-S` dispatch, the universal exactly-two-positive `(4,3)/(5,2)`
hull--`K2` slice, `PHYSICAL-UNIT-STAR-DNN`, and
`R61-PHYSICAL-SINGLE-BLOCK`.  In the nontrivial-positive-hull domain, the last
two reduce the unit-star complement to `c=5` with arms `(C5,C5)` and an
arbitrary multiblock rank-five center, and `c=6` with a multiblock center.  The
ledger separately retains the one-positive-hull
multiblock lane as `OPEN`, census `UNAUTHENTICATED`: empty bridge-free packet
residual does not authenticate unregistered physical bridge-forest transport.

## Why the global master is still open

The quotient-component rank `c` and the partition of seven into positive
**block** ranks are different axes.  A physical unit-star center is one
bridge-free component but may contain several positive blocks.  Therefore the
unit-star and physical `R61` theorems are overlays on the fourteen block-rank
partitions; they are not new packet keys and do not change the nineteen-key
bridge-free equality.

For a nontrivial positive hull, the weighted-tree theorem gives a balanced
`2|5` or `3|4` dispatch or a reduced unit-star.  The authenticated physical
owners then leave exactly the two outer unit-star rows stated above, subject to any later
narrower authenticated c5/c6 owner.  This is
an exact residual only inside that nontrivial-hull domain.

A one-vertex positive hull has no positive-hull edge, so it lies outside that
reduction.  Although every off-core all-bridge component has rank zero, the
physical graph can still contain arbitrarily many bridges and attachment
ports.  HEAD's packet notes expressly require packet-specific bridge dispatch
before the bridge-free pass, and the available owners have heterogeneous
contracts: for example, physical `R31-S` proves its own bridge dispatch,
`R511-K22` states only a bridge-free row, `R61` expressly excludes a physical
bridge between its positive sides, and the two-debit theorem begins only after
all actual bridges have been cut.  No present theorem verifies the missing
all-owner transport.  Consequently this lane cannot be called closed merely
from intended rooted-tree scope.

Thus the global blocker is a disjoint union of (i) two authenticated outer row
types for nontrivial positive hulls and (ii) an unauthenticated one-positive-
hull multiblock bridge-forest lane with no accepted finite census.  Promoting
the master before all three obligations are closed would overclaim.

## Fail-closed audit

From the repository root run

```text
python3 research/heptacyclic-multiblock-master-verifier.py
python3 -O research/heptacyclic-multiblock-master-verifier.py
```

Both invocations authenticate the exact fourteen-partition ledger, run every
closed packet and finite prerequisite, and also run the physical unit-star and
physical `R61` theorem gates in normal and optimized mode.  They reject hostile
scope/ownership mutations and exit with status `1`.  The output names the two
nontrivial-hull rows and the separate one-positive-hull unauthenticated lane.
The nonzero exit is intentional; a global `COMPLETE` receipt would currently
overclaim.
