# Cycle 206: parametric frozen-support obstruction

## Result

The Cycle 205 three-row contradiction persists for every real nonzero horizontal
frequency scale `R`, transverse scale `Y`, and viscosity `nu`.  The viscosity
drops out of these rows.  This is a symbolic extension of the same frozen
completion obstruction, not a new Navier--Stokes result.

Use physical wavevectors

\[
  (m,n,0)\longmapsto (mR,nY,0)
\]

with the Cycle 177 seed amplitudes left fixed and with the Cycle 204 first
completion support and terminal policy.  Nineteen selected independent
exterior-closure rows give
the same planar zero relations as at `R=Y=1`, together with

\[
 q1\_o9\_planar\_re=c/2,
\]

\[
 q1\_o4\_vertical=R(-c/2,-a),\quad
 q1\_o5\_vertical=R(0,2a-b),\quad
 q1\_o6\_vertical=R(c/2,-a),
\]

where

\[
 a=q1\_o9\_planar\_im,\qquad
 b=q1\_o10\_planar\_im,\qquad
 c=q1\_o10\_planar\_re.
\]

Three directly recomputed nonlinear rows then reduce to

\[
 f={R^2Y\over4}(c^2-4a^2),
\]

\[
 g={Y^2\over4}(4+8R^2ab-3R^2c^2-4R^2a^2),
\]

\[
 h={R^2Y\over2}(4ab-c^2-4a^2).
\]

They satisfy the exact Laurent-coefficient identity

\[
 {f\over Y}+{g\over Y^2}-{h\over Y}=1.
\]

Because `Y` is nonzero, the equations `f=g=h=0` have no common real or complex
solution.  No division by an amplitude or case exclusion is used.  The claim is
only about the declared anisotropically rescaled seed and frozen finite-support,
second-order tangency architecture.  It does not cover zero or degenerate
frequency scales, scale-dependent seed amplitudes, other supports, approximate
leakage, infinite-mode mechanisms, or Navier--Stokes regularity.

## Verification

Run

```sh
PYTHONPATH=.cycle206-sympy python3 \
  millennium-prize/navier-stokes/verify_cycle206_parametric_obstruction.py
```

The verifier constructs the Fourier field and Leray-projected Navier vector
field from the support, checks all 19 selected linear rows under the displayed
substitution, independently recomputes the three nonlinear rows, checks their
closed forms, and verifies the unit identity symbolically. These rows are a
sufficient subsystem, not the complete exterior linear closure: the full
closure has rank 27 and only strengthens the obstruction. SymPy 1.13.3 was used
for the recorded run.
