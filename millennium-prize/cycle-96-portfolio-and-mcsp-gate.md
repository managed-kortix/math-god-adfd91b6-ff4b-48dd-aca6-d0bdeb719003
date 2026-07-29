# Cycle 96: portfolio audit and average-case MCSP gate

## P versus NP: exact MCSP magnification

Oliveira--Santhanam's Theorem 27 and Corollary 28 give a valid full-reach
statement.  Let `N=2^n` and `n<=s(n)<=2^o(n)`.  If zero-error average-case
`MCSP[s]` requires unrestricted circuits of size `Omega(N^delta)` for one
constant `delta>0`, then an NP language on length
\[
 m=\Theta(ns(n)\log s(n))
\]
requires circuits of size `2^Omega(n)`.  For `s(n)=n^c`, one fixed `c>=1`
and one fixed exponent suffice to imply `P!=NP`.

The formal average-case model is ternary, never wrong, and decisive on at least
`1-1/n` of uniform truth tables for every sufficiently large `n`.  The proof
uses a stronger one-sided rejector, based on inconsistency of
`Theta(s log s)` canonical samples, which rejects a random table with probability
at least `1-2^-n` and never rejects a size-`s` table.

Ruling out one-sided rejectors of even constant density is sufficient, but is
not equivalent to ruling out arbitrary ternary solvers: an arbitrary solver may
answer only on easy YES tables.  This corrects the initial scout's claimed
equivalence and its informal `1/2` coverage normalization.

The local fitting barrier remains exact.  Any `q` labeled points can be fitted
by a compressed decision tree expanded into at most
\[
 3(q-1)+\min(n,q-1)
\]
fan-in-two De Morgan gates.  Therefore query, transcript, sampled-antichecker,
and local-consistency methods cannot soundly reject before the sample is large
enough to exceed the size budget.  Ordinary random restrictions are likewise
misaligned: after fixing many truth-table coordinates, the surviving subcube
typically contains no small-circuit truth table, making one-sided usefulness
vacuous.  The unresolved operation is global recognition of whether an
`O(s log s)` labeled sample is fit by any size-`s` circuit.

Average-case MCSP is therefore preserved as a correct full-reach theorem but
not promoted as the main funnel.  Its required advance is an architecture-
sensitive lower bound that charges sample fitting and does not survive replacing
that computation by a local oracle.

## Other five scouts

- **RH.** Mayer's exact Fredholm determinant represents modular Selberg zeta,
  while Riemann xi appears through a unitary scattering quotient.  A positive
  trace-class determinant
  \[
  \Xi(t)/\Xi(0)=\det(I-t^2A)
  \]
  exists exactly under RH by taking eigenvalues `gamma^-2`; constructing it
  independently is the Hilbert--Polya problem, not a transfer-operator corollary.

- **BSD.** Adelic openness and height lower bounds prove large-prime
  nondivisibility when the initial Kolyvagin class is a unit multiple of the
  Kummer image of one normalized point.  They do not control integral Euler-
  system content, congruence factors, Tamagawa factors, or Sha.  Multiplying an
  Euler system by an integer preserves the representation and changes
  primitivity at its prime divisors.

- **Hodge.** The BFNP normal-function singularity conjecture is equivalent to
  the rational Hodge conjecture.  A singularity detects nonzero restriction to
  a singular hyperplane section; the reverse implication obtains cycles only by
  lower-dimensional Hodge induction.  It is a cohomological detector, not an
  independent algebraic seed.

- **Navier--Stokes.** Backward uniqueness requires a tangent that is
  simultaneously nonzero, terminal-zero, strongly compact, and globally or
  exteriorly critical-tight.  Energy supplies none of these jointly.  A finite
  dissipation measure can have annular costs `2^-j`, leaving normalized local
  concentration order one at every dyadic scale.

- **Yang--Mills.** The center-vortex scout returned no independently verified
  production theorem.  No claim is recorded from the empty report.

No Millennium result is claimed.
