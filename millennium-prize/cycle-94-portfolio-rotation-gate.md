# Cycle 94: six-problem portfolio rotation gate

This bounded portfolio wave required a structural production lemma rather than
another equivalent criterion.  Every candidate met an exact obstruction.

## Riemann hypothesis: Jensen heat hierarchy

For
\[
 J_t^{d,n}(X)=\sum_{j=0}^d\binom dj\gamma_{n+j}(t)X^j,
 \qquad \dot\gamma_n=-\gamma_{n+1},
\]
the exact evolution is
\[
 \partial_tJ_t^{d,n}=-J_t^{d,n+1}
 =-\frac1{d+1}\partial_XJ_t^{d+1,n}.
\]
Thus no fixed-degree Jensen system closes.  In degree two, if
`J=a+2bX+cX^2`, then
\[
 D=4(b^2-ac),\qquad \dot D=4(ae-bc),
\]
where `e` is the next coefficient.  The discriminant derivative has no sign
from degree-two hyperbolicity.  Root-repulsion/discriminant monotonicity starts
only after all roots are real, so it preserves the hyperbolic phase but cannot
prove entry at `t=0`.  Uniform positivity of every Hermite matrix is the full
Jensen criterion.

## BSD: cyclotomic versus complex leading terms

Cyclotomic main conjectures and sufficiently strong `p`-adic BSD statements can
control one `p`-primary Selmer group.  For positive rank there is no
interpolation identity comparing the cyclotomic derivative with
`L^(r)(E,1)`: the `p`-adic and Neron--Tate regulators are different
realizations.  Infinitely many finite `p`-primary components do not imply
global finiteness of `Sha`, since unexamined primes and infinitely many finite
nonzero components remain possible.  Rank zero is exceptional because the
value itself is interpolated.  A genuinely productive arithmetic target would
be uniform large-prime primitivity of a higher-rank Euler system, but it still
would not provide the archimedean rank bridge.

## Hodge: absolute and motivated classes

Principle B propagates absolute Hodgeness in a flat family; it does not produce
algebraic cycles.  Deligne's abelian-variety theorem produces absolute tensors
at CM points via invariant theory and transports them, but does not prove those
tensors algebraic.  Andre motivated cycles formally install inverse Lefschetz
operations and yield absolute-Hodge classes, not algebraic representatives.
The missing reverse implications remain standard/Hodge-conjectural.

## Navier--Stokes: Lagrangian deformation

For the common-noise stochastic flow,
\[
 \dot F=(\nabla u)(X_t,t)F,\qquad \det F=1,
\]
and the stochastic Cauchy formula averages `F omega_0` over inverse trajectories.
Energy controls only label/noise-averaged squared strain exposure.  Exact shear
solutions
\[
 u=(e^{\nu t\Delta_{y,z}}U_0(y,z),0,0)
\]
have
\[
 F=\begin{pmatrix}1&\nabla H_t\\0&I_2\end{pmatrix},
 \qquad H_t=\int_0^t e^{\nu s\Delta}U_0ds.
\]
Unit-energy trigonometric polynomials can make `|grad H_t(0)|` grow like
`sqrt(log N)/nu` at fixed positive time.  Hence energy and unit determinant do
not control the largest deformation singular value, even for global exact
solutions.

## P versus NP: resolution automatability polarity

Atserias--Muller prove that polynomial-time automatability of Resolution implies
`P=NP`; equivalently, `P!=NP` implies non-automatability.  An unconditional
lower bound on a proof-search heuristic therefore does not imply `P!=NP`.
Restricted proof systems, proof length, and bounded-arithmetic unprovability do
not transfer to arbitrary decision algorithms.  The proposed separation route
had the implication in the wrong direction.

## Yang--Mills: weak-coupling character expansion

For Wilson `SU(2)`,
\[
 c_j(\beta)=\frac{I_{2j+1}(\beta)}{I_1(\beta)}
 =\exp\!\left(-\frac{2j(j+1)}\beta+O(\beta^{-2})\right)
\]
at fixed spin.  Every nontrivial fixed-spin activity approaches one as
`beta -> infinity`, while spins through order `sqrt(beta)` remain populated.
Thus a vacuum/trivial-representation polymer expansion loses its small
parameter on the continuum trajectory.  Positive character coefficients and
positive link projectors do not give scalar termwise positivity after
recoupling, and absolute representation norms diverge.  A viable expansion
would need a collective Gaussian high-spin background and ultraviolet
renormalization, not a conventional dilute spin foam.

All six tactics are retired at these gates.  No Millennium result is claimed.
