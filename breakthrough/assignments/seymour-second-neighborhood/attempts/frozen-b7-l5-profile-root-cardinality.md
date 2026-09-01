# Frozen B7-l5 profile root cardinality

## Exact scope

The clean `B7-l5` parent group contains 322 frozen parents. Splitting by the
exact two-C state and then by the `S7(B)` orbit of the two C-to-B rows gives 30
states, 1,920 state/parent incidences, 53 profiles, and 3,387 profile/parent
incidences. The producer and independent checker both derive these totals from
the committed clean-sink inputs.

## Root strengthening

Six holes leave 147 arcs, so exactly three of the 18 vertices have outdegree
nine. With `A={1,...,8}` and `B={9,...,15}`, root normalization forbids arcs
from A to the root or C. Therefore

`e(A,B)=36+H(A)+high(A)`.

Each profile receives fresh unary counters for global highs, A-to-B arcs, and
`H(A)+high(A)`. This adds exactly 2,433 variables and 9,571 clauses. The checker
reconstructs the frozen base, state/profile units, parent disjunction, and fresh
counters without importing the producer. Its semantic audit checks all 262,144
degree vectors and 261 root-cut arithmetic cases.

## Current status

This is a campaign freeze only. The manifest and every emitted CNF explicitly
record `certificate-status=not-started`. The scout entrypoint is pinned to the
same CaDiCaL 1.7.3 identity and options as the committed B7-l6 campaign, but no
LRATs, certificate ledger, certificate verifier, or closure claim is included.
