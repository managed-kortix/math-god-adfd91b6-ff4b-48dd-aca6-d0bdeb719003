# Cycle 128: temporal regularization under reflection positivity

The Cycle 127 electric contact divergence is not repaired by a universal linear
temporal smoother that also preserves reflection positivity.  Under standard
analytic assumptions, every universal reflection-positive multiplier is
polynomial and hence cannot improve ultraviolet decay.  The correct surviving
topology is distributional: the spatially smeared free electric field has sharp
local temporal regularity `H^{-s}` exactly above `s=1/2`.

## Universal multiplier classification

Put `x=p_0^2`.  Let `q` be entire, real on the real axis, and such that for
every `a>0`

\[
F_a(p_0)=\frac{q(p_0^2)}{p_0^2+a}
\]

is an even tempered distribution.  Test Osterwalder--Schrader positivity with
functions compactly supported in the open positive half-line, so distributions
supported at reflection time zero are invisible.

Then `F_a` is reflection positive modulo contact terms for every `a>0` if and
only if `q=P` is a real polynomial satisfying

\[
P(-a)\ge0\qquad(a>0).
\]

Indeed, reflection positivity gives a positive Stieltjes spectral
representation.  Since `q(z)/(z+a)` is meromorphic with no possible nonlocal
singularity except `z=-a`, uniqueness forces the noncontact spectral measure to
be supported only at that mass.  Hence

\[
\frac{q(z)}{z+a}=P_a(z)+\frac{c_a}{z+a},\qquad c_a\ge0,
\]

where `P_a` is a contact polynomial.  It follows that `q` is polynomial and
`c_a=q(-a)`.  Conversely, polynomial division gives

\[
\frac{P(z)}{z+a}
=\frac{P(-a)}{z+a}+\frac{P(z)-P(-a)}{z+a},
\]

with the second term polynomial and therefore supported at time zero.

If contact terms are not quotiented out and the covariance itself must be a
positive Stieltjes function for every mass, the polynomial must be a
nonnegative constant.  Thus no nonzero entire, tempered multiplier decaying at
large temporal momentum can universally preserve free reflection positivity.

Analyticity is essential.  Reflection positivity only samples `q(x)` for
`x>=0`; without a specified entire continuation, values `q(-a)` are not even
defined by the covariance and the polynomial conclusion is false.

## Distributional alternative

For the spatially heat-smeared free Maxwell electric field, the temporal
spectral density tends to a positive constant at large frequency.  In the
traced convention of Cycle 127,

\[
Q_\sigma(\omega)\longrightarrow
A_\sigma=\frac{2}{(4\pi\sigma)^{3/2}}>0.
\]

Therefore, on every bounded temporal interval,

\[
\mathbf E\|E_\sigma\|_{H^{-s}}^2<\infty
\quad\Longleftrightarrow\quad s>\frac12.
\]

The threshold follows from

\[
\int_{\mathbb R}\frac{d\omega}{2\pi}
(1+\omega^2)^{-s}
=\frac{\Gamma(s-1/2)}{2\sqrt\pi\,\Gamma(s)},
\qquad s>\frac12.
\]

At `s=1/2` the temporal lattice norm diverges logarithmically; below it the
divergence is a power.  Thus the contact term is ordinary white-noise-order
temporal structure, not a failure of distribution theory or reflection
positivity.

For the interacting gauge-invariant action density, power counting predicts a
much rougher temporal threshold above `5/2`.  Standard Wilson one-plaquette
expectation bounds do not imply the required negative-Sobolev covariance bound:
they contain no temporal spectral localization, and an RP constant-in-time
countermodel can satisfy the same one-point bounds while diverging in every
`H^{-s}` norm after physical normalization.

## Half-space-flow audit

Half-space heat flow gives the standard fixed-collar image estimate
`exp(-delta^2/(ct))`, but it is not yet a gauge-covariant Yang--Mills regulator.
Fixed-reference DeTurck flow is background-covariant rather than gauge
equivariant as a map of the physical connection, and its boundary gauge domain
is problematic around nonflat backgrounds.  Moreover fixed-distance estimates
are not uniform for observables approaching the reflection plane.  This route
is therefore retained only as a bounded scout.

No Yang--Mills or Millennium solution is claimed.
