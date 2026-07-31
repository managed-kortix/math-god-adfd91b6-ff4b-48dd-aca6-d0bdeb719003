# Cycle 158: shrinking spatial smoothing does not produce the local electric square

Cycle 157's collar-positive composite cannot be promoted by simply shrinking
the constituent spatial smoothing.  In free Maxwell theory, the equal-time
constituent-smoothed square develops positive low-external-momentum fluctuations
that diverge in every Sobolev topology.

Let `F_rho=e^(rho Delta_x)F` and

\[
Q_\rho=:F_\rho F_\rho:.
\]

At equal time, field-strength covariance scales as `|k|`.  Hence the spatial
covariance of the quadratic composite is

\[
\widehat C_{Q_\rho}(k)=\rho^{-5/2}\Phi(\sqrt\rho k),
\qquad\Phi(0)>0.
\]

Thus even pairing with a fixed smooth low-frequency test function has variance
of order `rho^(-5/2)`.  Additive Wick subtraction removes the one-point
divergence `rho^-2` but does not alter this connected fluctuation.

The unique power normalization preserving nonzero fixed-test variance is

\[
Z_\rho\asymp\rho^{5/4}.
\]

It yields a spatial white-noise limit, tight only in `H^-s` for `s>3/2`.
This is an emergent ultralocal noise, not the canonical Maxwell composite.
Stronger normalization collapses fixed tests; weaker normalization diverges.

The temporal lattice obstruction is sharper.  For a centered spatially
smoothed electric square, the internal temporal-frequency sum contains a
positive contact plateau.  At every fixed external spacetime frequency,

\[
\widehat K_{a,\rho}(\nu,p)
\sim\frac{b(0)}{a_\tau\rho^3},
\qquad b(0)>0.
\]

For heat smoothing in the convention of Cycle 131, the pointwise spatial
coefficient is

\[
\frac1{96\pi^3a_\tau\sigma^3}.
\]

The divergent mass sits at bounded external frequency.  Therefore no finite
negative-Sobolev exponent can suppress it:

\[
\boxed{
\text{the spatially smoothed, temporally sampled centered square is not tight
in }H^{-s}_{\rm loc}\text{ for any finite }s.
}
\]

This is actual non-tightness, not only failure of a second-moment method:
second-chaos hypercontractivity and Paley--Zygmund give a uniform positive
probability of excursions at the diverging variance scale.

Deterministic identity subtraction cannot help because connected covariance is
unchanged.  Contact counterterms can choose a coincident-time distributional
extension but cannot remove the positive low-output-momentum contact-contact
fluctuation while retaining the original lattice operator and reflection-
positive spectral interpretation.

The threshold `s>4` belongs to a different object: a genuinely renormalized
four-dimensional local composite formed before restricting to equal time.  Its
covariance has scaling `|q|^4` up to logarithms and is compatible with local
`H^-s` exactly for `s>4`.  Spatial-only smoothing followed by squaring does not
converge to that object.

At finite Wilson cutoff, one can define a gauge-invariant positive-time
point-split plaquette bilocal with a spatial Wilson line.  Reflection positivity
is exact, and a chessboard estimate reduces exponential moments to a tiled
pressure increment.  But proving a cutoff-uniform pressure estimate while the
physical split shrinks is construction-level weak-coupling work; fixed split or
flow time only gives a nonlocal observable.

Thus the shrinking-spatial-composite route is retired.  A viable local
Yang--Mills composite must be defined through a genuinely four-dimensional,
reflection-compatible renormalization or small-flow-time expansion with
interacting uniform control.  No such estimate is obtained here.
