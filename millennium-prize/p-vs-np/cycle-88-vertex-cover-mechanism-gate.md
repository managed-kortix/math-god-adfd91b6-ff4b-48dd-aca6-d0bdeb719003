# Cycle 88: small-Vertex-Cover mechanism gate

The Oliveira--Santhanam implication remains correct, but the proposed
extraction mechanisms do not survive the post-Buss audit.

Exact self-reduction recovers a minimum cover using at most

\[
k+\lceil\log_2(k+1)\rceil
\]

decision calls. At `k=2^sqrt(log n)` this is only an `m^o(1)` multiplier. It is
an upper bound, not a forced adaptive lower bound for arbitrary RAMs.

The kernel can be stored completely in `m^o(1)` workspace after one near-linear
scan. Thereafter a solver may perform arbitrary charged computation without
further input access. Consequently:

* query counts and hidden-kernel location cannot produce superlinear time;
* ordinary communication tops out at extraction/retention costs;
* read-`k`, oblivious branching-program, pebbling, and resolution lower bounds
  do not transfer without a reverse normalization theorem;
* such normalization is falsified by repeated reads, adaptive addresses, and
  arbitrary kernel computation.

A useful rejection test is junk robustness. If `A` is a valid solver and `J` is
any computation on the stored kernel fitting the resource allowance, then the
wrapper that runs `J` and discards its result before returning `A(x)` is still a
valid solver. Any syntax-sensitive extractor can therefore be defeated by
irrelevant computation. A semantic extractor would have to simplify arbitrary
kernel computation from correctness alone, which carries the separation
burden.

Direct transfer from known SAT time--space lower bounds also fails. Standard
SAT-to-Vertex-Cover reductions square the input under adjacency-matrix encoding
and use a linear cover parameter. Padding to the fixed subpolynomial parameter
is quasipolynomial and changes the threshold unless additional forced-cover
gadgets are added. Nondeterministic cover verification has the wrong quantifier
for a deterministic SAT contradiction.

Thus the full-reach target remains valid but has no live intermediate mechanism.
The extraction tactic is retired at the rotation gate. No RAM lower bound or
`P!=NP` result is claimed.
