# Cycle 106: structural portfolio gate

## Navier--Stokes: dynamic phase frustration

Kinematic phase compatibility does not imply dynamic residence.  For a triad
system with phase-incidence matrix `A`, amplitudes `r`, interaction matrix `C`,
and triad products `R_e`, the exact phase velocity is
\[
 A\dot\phi=-A\,\operatorname{diag}(r_j^{-2})C
 \operatorname{diag}(R_e)\sin(A\phi).
\]
Thus an exact target lock `A phi=beta` is dynamically tangent only if the
amplitude-dependent right side vanishes.  Smith-normal-form compatibility of
`beta` gives no such identity.

An exact conservative six-mode, three-triad loose hypercycle demonstrates the
failure.  At unit amplitudes and simultaneous maximizing phases
`A phi=(pi/2,pi/2,pi/2)`, suitable energy-conserving integer edge coefficients
give
\[
 A\dot\phi=(1,1,1)\ne0.
\]
The maximizing lock is left immediately.  Diagonal Navier damping has no direct
phase term and does not repair tangency.  This is a finite Galerkin logical
counterexample, not a full invariant Navier cluster or a regularity result.

## Yang--Mills: martingale criterion mismatch

The Kogut--Susskind Hamiltonian is not frustration free.  Link Casimirs and
plaquette multiplication operators do not share a nonzero local kernel; in
particular, the zero set of the Wilson plaquette potential has Haar measure
zero.  Subtracting the global vacuum energy, truncating representations,
blocking, or replacing terms by support projectors does not create nested local
ground spaces with a uniform spectral comparison.  Hence the standard
Nachtergaele/detectability setup cannot be applied directly.

Conditional-expectation heat-bath projectors do form a coherent
frustration-free auxiliary dynamics.  But transferring its gap to physical
time requires the uniform Dirichlet-form comparison
\[
 \langle f,(I-T^{\lceil r_0/a\rceil})f\rangle
 \ge c\langle f,L_{HB}f\rangle
\]
on every physical sector.  Static spatial mixing does not provide this bridge;
it is another form of the missing physical-slab contraction.

## BSD: rank-two Bockstein determinant

When specialized Selmer `H^1` and `H^2` both have dimension two, the first
Bockstein
\[
 \beta:H^1\to H^2\otimes I/I^2
\]
has a determinant in the cohomological determinant line.  Nonzero Kummer wedges
and Poitou--Tate dual wedges merely orient source and target; they do not imply
`det(beta)!=0`.  Nonvanishing is exactly nondegeneracy of the derived height,
or equivalently absence of a first-order lift/universal-norm radical.  Thus
absorbing `H^2` repairs the formulation but not the missing arithmetic input.

## P versus NP: PCP proof magnification

Under `P=NP`, a polynomial-time TAUT verifier can ignore all proofs.  A lower
bound over every polynomial-time verifier would therefore imply `P!=NP`, but is
already a decision lower bound in disguise.  A lower bound for one proof system
or one fixed verifier exponent does not suffice.  Linear or nearly linear PCPs
are linear in the encoded computation/witness size, not necessarily the
original formula length, so they do not compress an unknown `n^k` collapse
algorithm to near-linear proofs.

## Hodge bounded scout

A possible different bounded target occurs in a quartic-CM genus-four Jacobian
secant-sheaf construction where a normalized Chern class reportedly already
has nonzero determinant projection and the remaining issue is equivariant
semiregularity.  The scout report was incomplete and relied on a recent preprint
citation without a full theorem/hypothesis audit.  It is recorded only as a
future literature-verification target, not a mathematical claim.

## RH

The Nyman--Beurling frame scout returned no independently verified report; no
claim is recorded.

No Millennium result is claimed.
