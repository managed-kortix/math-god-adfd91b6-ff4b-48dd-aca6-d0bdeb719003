# Frozen B7-l4 profile root cardinality

## Exact scope

The clean `B7-l4` parent group contains 1,649 frozen parents. Splitting by the
exact two-C state and then by the `S7(B)` orbit of the two C-to-B rows gives 28
states, 10,036 state/parent incidences, 40 profiles, and 14,464 profile/parent
incidences. The producer and independent checker derive these totals from the
committed clean-sink inputs frozen at `e0419f0`.

## Certificates and implication

Six holes leave 147 arcs, so exactly three vertices have outdegree nine, and
root normalization gives `e(A,B)=36+H(A)+high(A)`. Each profile receives fresh
unary counters adding exactly 2,433 variables and 9,571 clauses.

Pinned CaDiCaL 1.7.3 produced 40 textual LRATs, and pinned `lrat-check` accepted
all 40. The CNFs total 462,367,384 bytes, raw proofs total 1,713,258,694 bytes,
and retained `xz -3` artifacts total 242,442,740 bytes. The push-friendly
package ledger splits the artifacts into contiguous 90,679,000-byte,
85,516,660-byte, and 66,247,080-byte packages, each strictly below the exclusive
250,000,000-byte cap.

The strict ledger and verifier reciprocally pin their canonical forms, bind all
direct and transitive runtime sources, authenticate the exact artifact set,
regenerate all CNFs, decompress every proof, and rerun `lrat-check`. Hostile
tests reject profile/order, path, counter, and transitive-runtime mutations.

The composition verifier independently reconstructs all 1,649 parents, 28
states, 10,036 parent/state incidences, 40 exact `S7(B)` profiles, and 14,464
parent/profile incidences. This closes the complete frozen clean `B7-l4` parent
campaign, but no other residual group, order 18 generally, or Seymour's
conjecture.
