# Cycle 105: nonsplit Weil mechanism rotation gate

The bounded discriminant-`-3` Weil-sixfold target is genuine, but every tested
seed mechanism met an exact obstruction.

## Secant and Fourier--Mukai modifications

For Markman's model `A=X x X^`, with `X` an abelian threefold and polarization
type `(d_1,d_2,d_3)`, put `D=d_1d_2d_3`.  The induced `Q(i)`-Hermitian
determinant is
\[
 \det_K H=-D^2,
\]
so its norm class is always `[-1]`.  More invariantly, every metabolic model
has Gram matrix
\[
 \begin{pmatrix}0&B\\\bar B^t&0\end{pmatrix}
\]
and determinant `-N(det B)`.  Changing polarization type, taking `K`-linear
isogenies or quotients, replacing the dual by an isogenous nonprincipal dual,
and Brauer/`B`-field/Fourier--Mukai transport all change the determinant only by
a norm.  The target ratio is `3`, which is not a norm from `Q(i)`.  Reaching
`-3` therefore requires destroying the metabolic decomposition, at which point
the inherited secant and semiregularity construction no longer applies.

## Unitary special cycles

Nonzero Kudla--Rapoport special homomorphisms cut out proper codimension-three
special subvarieties of the nine-dimensional `U(3,3)` base.  Their universal
cycles cannot dominate the generic Weil component.  The zero datum exists over
the full base but produces only contraction tensors.  Representation-theoretic
weights make the dichotomy exact: polarization, Poincare, endomorphism, and
special-homomorphism contractions lie in the balanced
`wedge^3 W tensor wedge^3 Wbar` sector, while the exceptional classes lie in
`wedge^6 W` and its conjugate.  Pair contractions cannot create the determinant
tensor.

The same no-go applies to every cycle generated solely from divisors,
homomorphism graphs, diagonals, and pull-push operations.  Endomorphisms can
separate an already existing determinant seed, but cannot create the first one.

## Deformation correction

For an lci threefold `Z` in an abelian sixfold, the ambient obstruction map is
\[
 \rho_Z:T_S\longrightarrow H^1(Z,N_{Z/A}),
\]
and semiregularity satisfies
\[
 \sigma_Z\rho_Z(\kappa)=\kappa\lrcorner[Z].
\]
Dominance over the chosen nine-dimensional Weil Shimura component means
`rho_Z` vanishes on its tangent space, together with all-order effectivity.  If
one instead works in the full `21`-dimensional polarized moduli space, the Weil
component has codimension `12`; the infinitesimal Hodge map must therefore have
rank `12`, not rank `9`.  This corrects a possible ambiguity in the preceding
production gate: "rank nine" referred to the projection onto the nine-
dimensional base, not the rank of the ambient Hodge obstruction map.

## Rotation decision

No explicit CM or geometric codimension-three cycle with nonzero pure `W^6`
projection was produced.  CM algebraicity neither guarantees nor forbids
generization; the decisive condition remains a dominating, formally effective
relative Chow component.  The route is retired as a production funnel until a
genuinely nonmetabolic determinant-bearing seed is exhibited.  No Hodge result
is claimed.
