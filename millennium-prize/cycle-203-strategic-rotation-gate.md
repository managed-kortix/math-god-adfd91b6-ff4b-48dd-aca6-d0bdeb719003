# Cycle 203: Hodge linkage rotation and Navier quadratic-order gate

## Decision

Rotate the main funnel from Hodge to Navier--Stokes if the minimal
Ferrand/link family has the semiregularity behavior found in Cycle 202.  More
precisely, suppose every member of that family is obtained from a nonunit graph
component by a finite generic thickening, a common horizontal complete-
intersection envelope, or a decomposition-preserving residual construction.
Then its relative tangent image is contained in the graph kernel:

\[
 \operatorname {im}(dp)\subseteq\ker\rho_k,
 \qquad \rho_k(B)=Q^{-1}B^t-5^kB,
 \qquad Q=\operatorname {diag}(1,1,3).
\]

For every nonunit graph, `rho_k` is injective.  Positive generic lengths cannot
cancel under semiregularity, and replacing a graph by its complete-intersection
residual negates rather than removes its cycle-class variation.  Thus either
effective endpoint has zero PEL tangent image.  This fails the required
rank-nine production gate before any higher obstruction calculation.  The
failure closes this named minimal Ferrand/link family, not arbitrary liaison or
singular non-Hilbert Chow branches.  Those broader possibilities remain open,
but no finite local equation or bounded support currently makes one an exact
next target.

## Scout-wave comparison

The Navier scout supplies the best next bounded obstruction problem.  The
Cycle 176 Laurent packet has exact instantaneous cancellation, while Cycle 177
computes two independent failures of dynamic closure: unequal heat weights and
terminal--pump interaction.  In the smallest packet,

\[
 F=z^{-2}-z^2,
 \qquad G=z^{-6}+z^{-2}+z^2+z^6,
 \qquad FG=z^{-8}-z^8,
\]

and the first leakage coefficients include

\[
 [\dot C(0)]_4=-32,
 \qquad [\dot C(0)]_6=i,
 \qquad C=GF.
\]

This is preferable to the other live scouts because the next question is a
finite polynomial feasibility problem over exact coefficients.  BSD still
requires a rank-two explicit-reciprocity or generalized Perrin--Riou bridge;
the random-order MCSP route has an exponent and model-transfer gap; the RH
residual estimate is not yet separated from a near-RH-strength coercivity
statement; and the Yang--Mills connected-tail target presently repackages the
uniform mass-gap and continuum-existence requirements.

## Exact Navier gate

Freeze the Cycle 177 real Fourier seed, including its conjugate modes, at
`R=Y=nu=1`.  Let `K_0` be its occupied wavevectors and freeze the
first-completion support

\[
 S=\bigl(K_0\cup(K_0+K_0)\bigr)\setminus\{0\},
 \qquad
 U_2=(S+S)\setminus\{0\},
 \qquad
 U_3=(S+U_2)\setminus\{0\}.
\]

No mode outside `S`, no time-dependent control, and no Galerkin deletion of a genuine interaction is
allowed.  Introduce exact real variables for a divergence-free polarization at
each conjugate orbit in `S\K_0`, except that the initially absent terminal
orbit remains zero.  Pin the seed coefficients and impose Fourier reality.

For the unforced periodic Navier--Stokes Fourier vector field `N`, form the
two-jet polynomials

\[
 P_{k,0}=u_k(0),\qquad
 P_{k,1}=N_k(u(0)),\qquad
 P_{k,2}=DN_k(u(0))[N(u(0))]
 \quad(k\in S\cup U_2\cup U_3).
\]

Pressure is not an extra variable: use the exact Leray projector at every
nonzero `k`.  Let `T` be the designated terminal conjugate orbit corresponding
to exponents `+8` and `-8`.  Require `P_(T,0)=0` and normalize its nonzero first
derivative.  The closure equations are

\[
 P_{k,1}=P_{k,2}=0
 \quad(k\in(U_2\cup U_3)\setminus S),
\]

together with preservation of the pinned seed equations.  Thus the full vector
field and its first directional derivative are tangent through quadratic time
order to the declared finite support; helper modes inside `S\setminus K_0` may
be nonzero initially, but no generated mode outside `S` is suppressed.

There are exactly two acceptable outcomes.

1. **Completion:** exhibit an exact rational or algebraic coefficient point
   satisfying all equations, and verify by full unprojected convolution that
   every mode in `U_2\cup U_3` has been included in the test.
2. **Obstruction:** exhibit a reproducible Groebner-basis, resultant, or
   rational Positivstellensatz certificate showing that `1` belongs to the
   normalized constraint ideal (or real infeasibility certificate, if the
   complex variety is nonempty but has no Fourier-real point).

A floating-point failure, a search over selected polarizations, or cancellation
only after projecting away leakage does not pass the gate.  Conversely, a
completion proves only quadratic-order closure of this declared finite packet;
it does not provide an invariant manifold, a critical budget, global
regularity, or blowup.  If a completion exists, the next gate is cubic-order
closure on the same support.  If the exact ideal is infeasible, retire this
Laurent first-completion architecture and rotate again.

No Millennium problem is claimed solved.
