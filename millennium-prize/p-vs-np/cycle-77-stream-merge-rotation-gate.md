# Cycle 77: Stream-Merge rotation gate

The MMW relation and its local canonical-merge implementation must be kept
distinct. Feasibility, minimum size, and lexicographic output have the expected
`NP^A/coNP^A` Boolean structure, with adaptive canonical output in
`FP^(NP^A)`. For `A=SAT`, transcript expansion places the bits at the
corresponding higher PH level. These are upper bounds, not hardness results.

Three mechanisms fail. The current circuit is a semantic summary of every old
block, so merge is Markovian and has no extra many-block consistency burden. A
proof-complexity route needs a missing algorithm-to-proof compiler certifying
universal minimality. A pseudorandom reachable antichecker must already know
that every bounded streamer has a nonempty error set, which is the desired
lower bound.

Most decisively, canonical merge belongs to the MMW upper-bound construction,
whereas the hardness-magnification hypothesis concerns relational
`search-MCSP`: a solver may output any valid size-bounded circuit. A lower bound
for an artificially canonicalized problem does not imply a lower bound for the
easier original relation.

The MMW implication remains valid, but no intermediate non-tautological lemma
survives the residual-entropy, locality, and relation-identity audits. This
tactic is retired. No circuit lower bound or `P!=NP` result is claimed.
