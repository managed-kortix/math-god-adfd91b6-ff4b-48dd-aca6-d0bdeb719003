# Hostile audit

Interpolation gives twisted central values, not complex `s`-derivatives.
Exclude exceptional zeros, supersingular primes, reducible residual
representations, analytic rank used circularly in rank certification, and
finite `p`-adic precision presented as exact vanishing.

For Cycle 215, distinguish an explicit coordinate witness from an exact
existence/localization certificate. Kim's localization isomorphism alone does
not identify the rational line, but rank one and trivial rational 7-torsion
make `A(Q)/7A(Q)` one-dimensional. Its Kummer injection into the
one-dimensional Selmer group is therefore surjective, so the rational line
localizes nontrivially without choosing a generator. This argument would fail
if the rank, rational torsion, Selmer dimension, or localization isomorphism
were only bounded rather than exact.

For the Cycle 193 approximate functional equation, do not cite the good-prime
form of Deligne's bound as though it automatically covered bad primes.  The
normalized weight-two newform has exact level equal to the arithmetic
conductor `433*1499^2`.  Its local coefficients must be checked separately:
the multiplicative prime `433` has `|a_433|=1`, while the additive prime `1499`
has trivial local factor and `a_(1499^r)=0`.  Together with Deligne at good
primes and multiplicativity, this proves `|a_n|<=d(n)*sqrt(n)` for every `n`.
PARI's `ellan` returns the classical Fourier/L-series coefficients `a_n`, not
unitarily normalized coefficients.  The completed function is
`N^(s/2)*(2*pi)^(-s)*Gamma(s)*L(s)`; the split is at `1/sqrt(N)`, even when
`N` is nonsquarefree.
