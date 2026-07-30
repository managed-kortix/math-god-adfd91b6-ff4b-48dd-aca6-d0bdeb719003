# Cycle 124: bare Wilson-loop modulus compactness gate

The proposed loop-modulus route fails its first ultraviolet gate.

For two loops differing by one adjacent plaquette insertion, write their based
holonomies as `A` and `AP`.  For the normalized fundamental `SU(2)` trace
`w(U)=Tr(U)/2`, the exact pointwise estimate is

\[
 |w(AP)-w(A)|^2\le 2(1-w(P)).
\]

Thus weak coupling gives only

\[
 \mathbf E|\Delta W|^2=O(1/\beta).
\]

Along four-dimensional asymptotically free scaling,
`beta=Theta(log(1/a))`, so this is logarithmic rather than a positive power of
the geometric displacement `a`.  The microscopic plaquette versus trivial
backtracking loop gives the lower calibration

\[
 \mathbf E(1-W_p)^2\ge(\mathbf E(1-W_p))^2
 \asymp \beta^{-2},
\]

conditional on the standard weak-coupling plaquette asymptotic.  No
cutoff-uniform Hölder estimate `C a^eta` can accommodate this rate.

The Gaussian continuum calibration is sharper.  For a fixed physical edge of
length `L` displaced by `h`, with ultraviolet regulator `a`,

\[
 \mathbf E|W_a(C)-W_a(C_h)|^2=2(1-e^{-S_a(h)}),
\]

where, up to a regulator-dependent positive constant,

\[
 S_a(h)\asymp\frac{g^2(a)L}{a}
 \left(1-\frac1{\sqrt{1+(h/a)^2}}\right).
\]

For fixed physical `h>0`, or even `h=a`, this diverges along asymptotic
freedom.  Nearby resolved bare contours decorrelate rather than become
continuous.  Continuity would require

\[
 h\ll a^{3/2}\sqrt{\log(1/a)/L},
\]

which is much smaller than one lattice spacing.

Bare normalized loops remain bounded and reflection positive but suffer
perimeter/cusp ultraviolet noise.  Multiplicatively renormalized loops may have
finite correlation functions, yet the inverse counterterms diverge, destroying
automatic boundedness/tightness; cusp and intersection mixing also do not
automatically preserve reflection positivity.  Fixed-positive-flow-time
holonomies evade the bare-loop calculation but define a different smeared
observable problem and still do not alone produce local OS Yang--Mills.

Even a successful modulus plus nonzero variance for macroscopic loops would be
insufficient for the Clay existence statement without joint consistency,
Euclidean restoration, reflection positivity on a complete algebra, shrinking-
loop/local-field renormalization, temperedness, locality, and identification of
the Yang--Mills dynamics.  The loop criterion was therefore both ultraviolet-
false for bare observables and logically too weak as stated.

The route is retired.  No Yang--Mills or Millennium result is claimed.
