# Cycle 103: structural portfolio gate

## RH: reciprocal mollifiers

For Dirichlet polynomials `M`, define
\[
 D(M)^2=\frac1{2\pi}\int_{\mathbf R}
 \frac{|1-\zeta(1/2+it)M(1/2+it)|^2}{1/4+t^2}\,dt.
\]
The assertion that the infimum over length-`N` polynomials tends to zero is
exactly the Dirichlet-polynomial Nyman--Beurling criterion, hence equivalent to
RH.  An off-line zero `rho=beta+i gamma` gives the coefficient-independent
Hardy-space obstruction
\[
 D(M)^2\ge(2\beta-1)|\rho-1|^2/|\rho|^4.
\]
Critical-line zeros instead force the optimal scale no better than order
`1/log N`.  Ordinary fixed-weight approximation to `1/zeta` is not the
criterion and is singular at critical zeros.

## Yang--Mills: local mixing and martingale gaps

For frustration-free local Hamiltonians, the Nachtergaele martingale criterion
converts uniform shell gaps and overlap bounds
\[
 \|G_{S_{n,r}}E_n\|\le\varepsilon_r,
 \qquad \sqrt r\,\varepsilon_r<1,
\]
into a volume-uniform gap.  Local strong spatial mixing could supply
`epsilon_r<=poly(r)e^{-r/xi}` without global TV mixing.  For gauge theory the
missing steps are conversion to physical Hilbert-space projector norms after
Gauss projection, exclusion of all superselection sectors, and cutoff scaling
\[
 a_t^{-1}\gamma_r d_r^{-1}(1-\sqrt r\varepsilon_r)^2>c>0.
\]
Static local mixing alone does not prove these properties.

## Navier--Stokes: phase hypergraph theorem

For oriented triads, collect phase equations into an integer incidence matrix
`A`.  Exact lock targets `beta` are simultaneously feasible on the phase torus
iff
\[
 z^T\beta=0\pmod{2\pi}
 \quad\text{for every }z\in\ker_{\mathbf Z}(A^T).
\]
This follows exactly from Smith normal form; integer left-kernel vectors are the
minimal frustration certificates.  The theorem extends to countable networks
by compactness.  It is kinematic: sign intervals, modal zeros, newly generated
modes, tangency of phase dynamics, and magnitude control remain outside it.
Overlap alone supplies no depletion.

## Hodge: smallest Weil-type production target

A very general abelian sixfold of Weil type for `Q(i)`, multiplicities `(3,3)`,
and nonsplit discriminant `-3` has a two-dimensional exceptional rational Weil
space in `H^6`.  Invariant theory algebraizes all contraction tensors but not
the determinant invariant.  Split discriminant `-1` sixfolds and Weil
fourfolds are covered by recent/special constructions; the nonsplit sixfold is
a clean remaining boundary.  The exact production target is two codimension-
three cycles whose projections span the Weil space, preferably in a relative
family.  No such cycles were constructed in this cycle, and recent-preprint
status requires a primary-source novelty audit before relying on the claimed
dimensional boundary.

## P versus NP: total search

Any explicit TFNP problem outside `FP` implies `P!=NP`, since under `P=NP`
witnesses can be recovered bit by bit.  Decision-tree separations for
`rwPHP(PLS)` do not transfer to white-box algorithms.  They are not hardness
magnification: the needed unrestricted lower bound is already target-level.
The only verified weak-resource magnification in this neighborhood remains the
CJSW constructive GapMaj theorem and its unresolved uniform-selector gate.

## BSD

The determinant/Bockstein repair scout returned no independently verified
report; no claim is recorded.

No Millennium result is claimed.
