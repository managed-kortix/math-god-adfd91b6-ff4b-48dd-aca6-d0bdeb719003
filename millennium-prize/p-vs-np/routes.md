# Routes

Scout lemma: polynomial-cardinality anticheckers for dense-encoded 3-COLOR
against unrestricted fan-in-two circuits of size `N^2`. This gives only a
quadratic lower bound; a separate all-exponents amplification theorem would
be required for `P != NP`. First exact test: finite circuit/hitting-set
enumeration at six graph vertices.

Cycle 180 bounded prospect: state an exact random-order MCSP model and prove a
query or streaming lower bound there. This remains a restricted-model theorem
unless it applies to relational `search-MCSP^SAT` at
`s(n)=2^(n/log^* n)` and preserves exactness, oracle access, space, and per-item
update time strongly enough to trigger the McKay--Murray--Williams implication.
Decision MCSP, canonical output, average-order success, or a near-linear query
bound alone does not imply `P != NP`.

Cycle 182 calibration: a lower bound for exact `pi`-OBDD size on most random
orders is a genuine residual-state strengthening of query depth. It gives a
random-partition deterministic one-way communication bound and, for a matched
fixed-order exact decision streamer, space at least `log L-log(N+1)`. It does
not cover best-order or adaptive/repeated-read branching programs, does not
charge update time, and does not transfer from Boolean decision MCSP to the MMW
search relation. Novelty remains conditional on a primary-source audit.

Cycle 182 hostile audit: midpoint splice packing is valid for exact all-order
decision MCSP only after conditioning on the number of disagreements in the
prefix; the candidate splice has support `binom(d,k)`, not `2^N`, and balance
alone does not imply hardness. More decisively, a code of easy tables has
`log|C|<=O(s log(n+s))=N^o(1)` at the MMW value of `s`, so the resulting width
argument cannot force fixed-power space. Average-order correctness also does
not give one permutation correct on all pairwise splices, and decision-state
distinguishability supplies neither relational-search nor update-time hardness.

Cycle 182 gives an exact affine-plane order family: transverse slope blocks
meet in one point, so balanced block prefixes have exact product intersections
up to one boundary block. Equality has width at least `2^((q^2-1)/2)` in every
one of these `q(q-1)` designated orders, by an exact split-pair count. This does
not cover an adversarial OBDD order (the paired order has width two), and no
reverse simulation transfers OBDD hardness to exact relational
`search-MCSP^SAT`. The live obstruction is quantifier order: one efficiently
computable function must hide a family of matchings so that every variable
order leaves one matching with `Omega(N)` independent cross-cut bits, without
letting the program read a selector first.
