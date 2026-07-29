# Cycle 102: structural portfolio gate

## BSD: explicit rank-two determinant feasibility

For `E=389a1`, `p=5`, the test field `K=Q(sqrt(-31))` preserves rank two:
the twist has rank zero, while the rational points `(0,0)` and `(1,0)` give
independent mod-`5` Kummer classes and a nonzero exterior product.  Nevertheless
the proposed unobstructed determinant lemma fails at three exact gates.

First, `389` is inert in `K`; the Heegner sign setup is unavailable and the
corresponding quaternion algebra is definite.  Second, the two split `5`-adic
localization rows are conjugate on rational points, so a determinant made from
their scalar ordinary localizations vanishes.  Third, self-dual Poitou--Tate
duality makes the relevant finite `H^2` nonzero (dimension two in the calibrated
Selmer situation), so an `H^2=0` determinant-lifting hypothesis is impossible.
Any viable rank-two construction must absorb `H^2` in a determinant line and
use derived/Bockstein heights rather than two ordinary scalar localizations.

## Yang--Mills: slab minorization

A global Doeblin estimate for a Wilson slab gives at best
\[
 \varepsilon\gtrsim\exp[-c\beta N_{\rm plaquette}(\text{slab})],
\]
which collapses exponentially in transverse volume and catastrophically in the
continuum cutoff.  A volume-uniform Poincare constant can control equilibrium
`L^2` contraction but not uniform mixing from arbitrary boundary states.
Tensor-product two-state channels have a fixed `L^2` gap while their global
Doeblin and total-variation contraction constants tend to one exponentially in
the number of boundary variables.  Conditional slab Poincare estimates can
also leave an untouched complement eigenfunction exactly invariant.

## Navier--Stokes: overlapping phase locks

Triad overlap does not force phase frustration.  An exact five-mode Galerkin
cluster with triads
\[
 (1,0,0)+(0,1,0)=(1,1,0),
 \qquad (0,0,1)+(1,1,-1)=(1,1,0)
\]
admits a common purely imaginary phase assignment.  Explicit integer
polarizations make every triad and conjugate contribution to vortex stretching
positive, with total normalized stretching `12`.  The odd-parity Fourier
subspace is Galerkin-invariant, so positivity persists for a nonzero interval.
Frustration requires an inconsistent signed cycle, not merely shared modes.

## Hodge: mixed abelian summands

The precise closure theorem is formal: if `h(X)` is a rational Chow-motive
retract of Tate twists of mixed products of abelian varieties, and Hodge is
known for those mixed products, then Hodge holds for `X`.  Chow correspondences
push algebraic representatives through the retraction.  Motivated, numerical,
or cohomological summands do not suffice.  Separate knowledge for each generator
also does not control exceptional cross-product tensors.  No novelty-verified
new class was found.

## P versus NP: proof compression

Under `P=NP`, a deliberately semantic Cook--Reckhow system has linear proofs:
the formula itself is accepted after deciding tautologicity.  This gives no
near-linear verifier and no compression inside natural systems.  Forced-padding
systems retain arbitrarily high polynomial minimum lengths, and time hierarchy
blocks a general near-linear translator from proof alone.  Thus existential
compression is vacuous, while junk-robust natural-system compression is an
unsupported extra theorem.

## RH

The reciprocal-mollifier scout returned no independently verified report; no
claim is recorded.

All returned routes met explicit gates.  No Millennium result is claimed.
