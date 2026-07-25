# Routes

## Active route: explicit discrete Nyman--Beurling approximants

For `N >= 3`, put

\[
c_a=\mu(a)\frac{\log(N/a)}{\log N},\qquad
F_N(x)=1_{(0,1)}(x)+\sum_{a\le N}c_a\{1/(ax)\}.
\]

Candidate lemma: there are absolute `C,N0` such that

\[
 \|F_N\|_{L^2(0,\infty)}^2\le C/\log N\quad(N\ge N_0).
\]

By Báez-Duarte's discrete Nyman--Beurling criterion this implies RH. The route
is knowingly RH-strength. The proof may not use critical-line convergence of
`sum mu(n)n^-s`, an RH-level Mertens bound, or an RH-conditional mollifier
estimate.

Primary route references: Báez-Duarte, arXiv:math/0202141 and
arXiv:math/0205003; Burnol, arXiv:math/0103058; Bettin--Conrey--Farmer,
arXiv:1211.5191.

## Current sharpened bottleneck

Elementary pair-period estimates give polynomial-cost rigorous tail
certification, and the periodic gcd variance admits an unconditional
`14N/log^2 N` bound. These do not produce the required cancellation in the
full weighted Gram form. The active next step is the exact rational
fractional-part autocorrelation formula and its finite Vasyunin cotangent sum;
the target is a sufficient signed Möbius--Vasyunin cancellation lemma, not an
absolute pairwise estimate.

The Estermann operator has now been converted to an exact double Perron
integral, but its arithmetic diagonal vanishes and contour shifts meet the full
reciprocal-zeta zero set. A weaker positive target is also active: prove
`liminf P_N=0`, where `P_N` is the restricted `(0,1)` energy of the same fixed
approximants. Any off-critical zero gives an explicit uniform positive floor
for every `P_N`, so this condition implies RH. It is not known to follow from
RH for this exact logarithmic taper.
