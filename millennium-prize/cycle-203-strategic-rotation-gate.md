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

Freeze the small Cycle 177 seed at `R=Y=nu=1`, with `e_2=(0,1,0)` and
`e_3=(0,0,1)`.  Its nonzero coefficients are

\[
\begin{array}{c|c}
k&u_k\\ \hline
(-2,1,0),\ (2,-1,0)&e_3\\
(2,1,0),\ (-2,-1,0)&-e_3\\
(\pm2,0,0),\ (\pm6,0,0)&e_2.
\end{array}
\]

Thus `K_0` is this eight-frequency support.  These values, rather than merely
their support or scale, are pinned throughout the feasibility problem.  A
general Fourier-real completion is not restricted to real Fourier
coefficients: on one representative of every conjugacy orbit use independent
real variables for the real and imaginary parts of a complex polarization,
impose `k dot u_k=0`, and set `u_{-k}=conj(u_k)`.

For finite sets `A,B`, write `A+B={a+b:a in A,b in B}`.  Freeze the candidate
initial support and the two jet-support envelopes as

\[
 S=\bigl(K_0\cup(K_0+K_0)\bigr)\setminus\{0\},
 \qquad
 U_2=(S+S)\setminus\{0\},
 \qquad
 U_3=(S+U_2)\setminus\{0\}.
\]

The terminal quartet is

\[
 Q=\{(-8,1,0),(8,1,0),(-8,-1,0),(8,-1,0)\}.
\]

It is **two**, not one, Fourier-reality orbits:

\[
 Q_- =\{(-8,1,0),(8,-1,0)\},\qquad
 Q_+ =\{(8,1,0),(-8,-1,0)\}.
\]

Both are absent in the Cycle 177 initial seed.  Accordingly every coefficient
on `Q` is fixed to zero at time zero; terminal receiver coefficients are not
completion variables.  Introduce the complex-polarization variables described
above only on `(S\setminus K_0)\setminus Q`.  Set every mode outside `S`, and
the mean mode, to zero.  No time-dependent control or Galerkin deletion of a
genuine interaction is allowed.

For the unforced periodic Navier--Stokes Fourier vector field `N`, form the
two-jet polynomials

\[
 P_{k,0}=u_k(0),\qquad
 P_{k,1}=N_k(u(0)),\qquad
 P_{k,2}=DN_k(u(0))[N(u(0))]
 \quad(k\in S\cup U_2\cup U_3).
\]

Here `N_k(u)=-\nu|k|^2u_k-iP_k\sum_{a+b=k}(u_a\mathbin\cdot b)u_b`, up to the
single globally fixed Fourier-sign convention, and `P_k` is the exact Leray
projector.  Pressure is not an extra variable.  The support formulas above are
exhaustive: `P_1` is supported in `S union U_2`, while `P_2` is supported in
`S union U_2 union U_3`; no `U_4` terms occur in a two-jet because the
direction in `DN(u)[N(u)]` has support only in `S union U_2`.

Require each terminal orbit to be genuinely seeded at first order.  This is a
nonvanishing condition, not permission to rescale the pinned seed.  If `J_+`
and `J_-` are the sums of squares of the real and imaginary components of
`P_{q,1}` for one representative `q` of `Q_+` and `Q_-`, respectively, impose

\[
 P_{q,0}=0\quad(q\in Q),\qquad hJ_+J_--1=0
\]

with one real slack variable `h`.  Equivalently, work on the component charts
where a component of each terminal first derivative is invertible.  For a
complex Groebner obstruction, use those component charts (or saturation by
the two component ideals), rather than the sum-of-squares equation, which can
have nonzero isotropic complex points.

The exterior closure equations are precisely

\[
 P_{k,1}=0\quad(k\in U_2\setminus S),\qquad
 P_{k,2}=0\quad(k\in(U_2\cup U_3)\setminus S).
\]

The pinned seed equations are initial-value substitutions, not stationarity
conditions: do not impose `P_{k,1}=P_{k,2}=0` on `K_0`.  Thus the full vector
field and its first directional derivative are tangent through quadratic time
order to the declared finite support; nonterminal helper modes inside
`S\setminus K_0` may be nonzero initially, but no generated mode outside `S`
is suppressed.

There are exactly two acceptable computational outcomes.

1. **Completion:** exhibit an exact rational or algebraic coefficient point
   satisfying all equations, and verify by the full untruncated ordered
   convolution followed by exact Leray projection that
   every mode in `U_2\cup U_3` has been included in the test.
2. **Obstruction:** exhibit a reproducible Groebner-basis, resultant, or
   rational Positivstellensatz certificate showing that `1` belongs to the
   normalized constraint ideal (or real infeasibility certificate, if the
   complex variety is nonempty but has no Fourier-real point).

A floating-point failure, a search over selected polarizations, or cancellation
only after projecting away leakage does not pass the gate.

## Scope of either outcome

A completion proves only quadratic-order tangency of this declared support for
this pinned seed and helper-mode class.  It does not provide an invariant
manifold, a critical budget, global regularity, or blowup.  If a completion
exists, the next gate is cubic-order tangency on the same support.

An exact infeasibility certificate has a different but still meaningful bounded
conclusion: **no Fourier-real choice of the allowed helper coefficients on this
particular support `S`, with the seed and terminal normalization fixed above,
makes the unforced Navier--Stokes vector field tangent to the coordinate
subspace through second time order.**  Equivalently, this fixed first-completion
architecture cannot realize its proposed exact two-jet sequential filter.  It
is then legitimate to retire that architecture as a route to an exact
finite-dimensional cascade and rotate the funnel.

That obstruction must not be enlarged by changing its quantifiers.  It says
nothing about larger or different finite supports, different seeds, helper
modes outside `S`, approximate closure with controlled leakage, time-dependent
or infinite-mode mechanisms, or actual Navier--Stokes trajectories not confined
to the coordinate subspace.  In particular, exact invariant Fourier support is
not a necessary condition for finite-time blowup: a hypothetical singular
solution may continually generate new modes.  Therefore infeasibility cannot
be called a blowup obstruction, a regularity criterion, or evidence that all
finite-Fourier blowup mechanisms fail; its force is solely the falsification of
the stated exact-filter ansatz.

No Millennium problem is claimed solved.
