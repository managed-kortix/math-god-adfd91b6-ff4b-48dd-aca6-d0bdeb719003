# Cycle 162: composite kernel incidence and primitive image classes

Cycle 161's four-orbit count is finite-field linear algebra.  It applies to
prime torsion, not to `p^e`-torsion: already in a symplectic
`(Z/4Z)^2`, the six cyclic self-dual subgroups and the subgroup `2M` give seven
Lagrangians, whereas a symplectic plane over `F_4` has five Lagrangian lines.
Thus elementary-divisor data are indispensable at composite level.

Let `f:A -> B=A/K` be a polarized isogeny of principally polarized abelian
sixfolds with

\[
f^*M=mL,
\qquad |K|=m^6,
\]

and suppose at the good primes under consideration that

\[
A[m]=G\perp H,
\qquad G=\Gamma[m],
\]

where `Gamma` is the seed abelian threefold.  Put

\[
A_K=K\cap G,\qquad B_K=K\cap H,
\qquad\delta=|A_K|.
\]

Projection to either equal-order factor and the Lagrangian identity
`K=K^perp` give

\[
|A_K|=|B_K|,
\]

and the residual part of `K` is the graph of an anti-symplectic isomorphism

\[
A_K^\perp/A_K\simeq B_K^\perp/B_K.
\]

This remains true over every `Z/p^e Z`, without freeness of the intersections:
the two projections of `K` are exactly `A_K^perp` and `B_K^perp`.  A detailed
nonfree-module proof and the necessity of the equal-order hypothesis are given
in Cycle 163.

Consequently, with

\[
\eta_m(K)={m^3\over\delta},
\]

one has the exact order identity

\[
\boxed{|K/(A_K\oplus B_K)|=\eta_m(K)^2.}
\]

Thus `eta` is the square root of the residual coupled graph, not merely a
prime-level intersection codimension.  Chinese remaindering factors `eta` over
the prime powers dividing `m`.  In particular, bounded `eta` does not bound
`m`: multiplication kernels can have arbitrarily high level while remaining
completely adapted.

## Exact cycle denominator

The restriction of `f` to `Gamma` has scheme-theoretic degree

\[
\delta=|K\cap\Gamma[m]|,
\]

so for the reduced image `Y=f(Gamma)`,

\[
f_*[\Gamma]=\delta[Y],
\qquad
m^{-3}f_*[\Gamma]={1\over\eta_m(K)}[Y].
\]

The displayed denominator in the free group on reduced integral cycles is
therefore exactly `eta_m(K)`.

There is no hidden cancellation from divisibility of `[Y]`.  On integral
homology, `H_1(Y,Z)` is the saturation of the image lattice inside
`H_1(B,Z)`.  Its top exterior generator is primitive, hence the fundamental
class `[Y]` and its Poincare dual are primitive.  Divisibility in integral Chow
would imply divisibility of this cohomology class.  Therefore

\[
\boxed{[Y]\text{ is primitive in integral cohomology and is not divisible
in integral Chow,}}
\]

and the actual integral denominator of the normalized class is exactly `eta`,
not merely a divisor of it.

If the restricted seed polarization `L|_Gamma` has type
`(e_1,e_2,e_3)` and the induced polarization on `Y` has type
`(d_1,d_2,d_3)`, then projection gives

\[
\boxed{d_1d_2d_3={m^3\over\delta}e_1e_2e_3.}
\]

Thus `eta=m^3/delta` is the ratio of the two polarization volumes, not in
general the absolute polarization volume of the image.  For the Cycle 151
diagonal, the restricted alternating form has blocks `2J,2J,4J`, so this
qualification is essential.

## Scope corrections

For the Cycle 151 polarization type `(1,1,1,1,1,3)`, the decomposition into
two nondegenerate symplectic six-spaces is valid only for primes `p>=5`.
At `p=3` the ambient pairing and the orthogonal complement are degenerate; at
`p=2` the graph `Gamma[2]` is Lagrangian.  Moreover the graph is `K`-antilinear,
so this symplectic decomposition is not a decomposition by PEL
`O_K/p`-submodules.

A bounded `eta` gives bounded-degree isogenies or algebraic correspondences
between quotient varieties after passing through a common cover.  When both
kernels are polarized `m`-isogeny kernels from the same source, compatibility
of the descended polarizations is automatic on that cover: both pull back to
`mL`.  The two cover legs have degree at most `eta^2`, and the resulting
rational polarized isogeny has denominator at most `eta^2`.  Arbitrary level
structures or kernels not arising from this same-source construction still
require separate compatibility.  In all cases, finite incidence rarity alone
does not prove that the adapted locus is proper or Zariski nondense.

No generic algebraicity theorem or Hodge-conjecture result is claimed.
