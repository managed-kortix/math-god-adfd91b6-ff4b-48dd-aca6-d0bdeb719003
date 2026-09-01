# Frozen clean B6-l6 root cardinality

## Exact scope

This certificate applies only to the 220 parents in the committed clean-sink
group `B6-l6`. It uses one grouped selector CNF and imports no witness or later
residual refinement units.

## Authoritative identity

Six holes leave `C(18,2)-6=147` arcs. Every vertex has outdegree eight or nine,
so exactly three vertices are high. With `A={1,...,8}`, `B={9,...,14}`, and
`C={15,16,17}`, root normalization forbids arcs from `A` to the root or `C`.
Therefore

`sum_(a in A) d+(a)=64+high(A)`, `e(A,A)=28-H(A)`, and
`e(A,B)=36+H(A)+high(A)`.

Fresh unary counters enforce exactly three global highs and every threshold
consequence of the root identity. The extension adds 2,013 variables and 7,899
clauses. The independent checker reconstructs all 220 selectors, the frozen B6
base, and the counters. Its semantic audit checks 262,144 degree vectors and
all 261 `(H(A),high(A))` arithmetic cases.

## Certificate and implication

Pinned CaDiCaL 1.7.3 produced one textual LRAT, accepted by pinned `lrat-check`.
Strict replay regenerates and structurally checks the grouped CNF, authenticates
the compressed and raw proof, and reruns `lrat-check`. Thus the exact frozen
clean `B6-l6` parent group is UNSAT. This does not close another clean group,
residual B6 generally, order 18 generally, or Seymour's conjecture.
