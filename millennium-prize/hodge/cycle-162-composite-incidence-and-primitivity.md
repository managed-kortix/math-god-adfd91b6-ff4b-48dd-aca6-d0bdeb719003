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

Projection to either factor and symplectic orthogonality give

\[
|A_K|=|B_K|,
\]

and the residual part of `K` is the graph of an anti-symplectic isomorphism

\[
A_K^\perp/A_K\simeq B_K^\perp/B_K.
\]

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
\boxed{[Y]\text{ is primitive in integral cohomology and Chow,}}
\]

and the actual integral denominator of the normalized class is exactly `eta`,
not merely a divisor of it.

Equivalently, if the induced polarization on `Y` has type
`(d_1,d_2,d_3)`, then projection gives

\[
\boxed{{m^3\over\delta}=d_1d_2d_3.}
\]

The denominator is the polarization volume of the reduced image; it equals one
exactly when that induced polarization is principal.

## Scope corrections

For the Cycle 151 polarization type `(1,1,1,1,1,3)`, the decomposition into
two nondegenerate symplectic six-spaces is valid only for primes `p>=5`.
At `p=3` the ambient pairing and the orthogonal complement are degenerate; at
`p=2` the graph `Gamma[2]` is Lagrangian.  Moreover the graph is `K`-antilinear,
so this symplectic decomposition is not a decomposition by PEL
`O_K/p`-submodules.

A bounded `eta` does give bounded-degree unpolarized isogenies or algebraic
correspondences between quotient varieties after passing through a common
cover.  It does not automatically give a bounded Hecke correspondence between
the original polarized moduli points: compatibility of the descended
polarizations and level structures is additional data.  Hence finite incidence
rarity does not prove Zariski non-density.

No generic algebraicity theorem or Hodge-conjecture result is claimed.
