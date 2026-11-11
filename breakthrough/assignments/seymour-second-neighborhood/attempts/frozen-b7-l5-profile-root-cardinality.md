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

## Certificates and implication

Pinned CaDiCaL 1.7.3 produced 53 textual LRATs, and pinned `lrat-check` accepted
all 53. The raw proofs total 1,004,531,865 bytes; retained `xz -3` artifacts total
121,021,160 bytes, strictly below the exclusive 250,000,000-byte cap. The strict
ledger and verifier reciprocally pin their canonical forms, bind all direct and
transitive runtime sources, authenticate the exact artifact set, regenerate all
CNFs, decompress every proof, and rerun `lrat-check`.

The composition verifier independently reconstructs all 322 parents, 30 states,
1,920 parent/state incidences, 53 exact `S7(B)` profiles, and 3,387
parent/profile incidences. For every state it exhausts the intersection orbits
of both exact C-to-B rows. Since all 53 profile disjunctions are certified UNSAT,
the complete frozen clean `B7-l5` parent campaign is closed. This does not close
another residual group, order 18 generally, or Seymour's conjecture.
