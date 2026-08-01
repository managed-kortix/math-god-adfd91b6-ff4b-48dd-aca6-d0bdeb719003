# Cycle 206: seed-amplitude parametric obstruction

## Result

The Cycle 205 three-row contradiction persists when the two seed families are
given independent, scale-dependent amplitudes `A=A(R,Y,nu)` and
`B=B(R,Y,nu)`, provided both amplitudes and both frequency scales are nonzero.
The viscosity again drops out.  The exact locus where the displayed unit-ideal
certificate loses its nonzero constant is

\[
 ABY=0.
\]

On the bounded nondegenerate Navier scout (`R Y != 0`) it reduces to `A B=0`.
Both components delete one of the two interacting seed families and make the
prescribed seed-to-terminal first derivative `i A B Y` vanish.  They are
degenerate boundary cases, not nonzero-amplitude evasions of the obstruction.

Use physical wavevectors

\[
  (m,n,0)\longmapsto (mR,nY,0)
\]

with horizontal seed coefficients `A e_2` and oblique seed coefficients
`+/- B e_3`, in the Cycle 177 sign pattern, and with the Cycle 204 first
completion support and terminal policy.  Treat `A` and `B` as fixed parameter
values at each chosen scale; no derivatives of these parameter functions enter
the time-jet equations.  Nineteen selected independent
exterior-closure rows give
the same planar zero relations as at `R=Y=1`, together with

\[
 q1\_o9\_planar\_re=c/2,
\]

\[
 q1\_o4\_vertical={BR\over A}(-c/2,-a),\quad
 q1\_o5\_vertical={BR\over A}(0,2a-b),\quad
 q1\_o6\_vertical={BR\over A}(c/2,-a),
\]

where

\[
 a=q1\_o9\_planar\_im,\qquad
 b=q1\_o10\_planar\_im,\qquad
 c=q1\_o10\_planar\_re.
\]

Three directly recomputed nonlinear rows then reduce to

\[
 f={BR^2Y\over4A}(c^2-4a^2),
\]

\[
 g={BY^2\over4}(4A^2+8R^2ab-3R^2c^2-4R^2a^2),
\]

\[
 h={BR^2Y\over2A}(4ab-c^2-4a^2).
\]

They satisfy the exact identity

\[
 AYf+g-AYh=A^2BY^2.
\]

Thus `f=g=h=0` has no common real or complex solution whenever `A B Y != 0`.
The displayed linear parametrization uses `A != 0`; the exceptional cases are
handled before that division.  If `A=0` or `B=0`, direct seed convolution gives
the prescribed seed-to-terminal first derivative `i A B Y=0`; the selected
certificate no longer decides the resulting lower-seed systems.  Those cases
delete a seed family and therefore are outside the requested two-family
nonzero-amplitude generalization.  If `R=0` or `Y=0`, the physical wavevector
map and polarization basis degenerate and lie outside the bounded nonzero-scale
scout.  Notice that `R=0` is a domain degeneration, not a zero of the
certificate's right-hand side.

For an elimination check, clear the harmless nonzero monomial factors and put

\[
 F=c^2-4a^2,\qquad
 G=4A^2+8R^2ab-3R^2c^2-4R^2a^2,\qquad
 H=4ab-c^2-4a^2.
\]

Keeping the common seed factor `B`, exact iterated resultants are

\[
 \operatorname{Res}_b(BG,BH)
 =-4B^2a(4A^2+4R^2a^2-R^2c^2),
\]

\[
 \operatorname{Res}_c\!\left(BF,
 \operatorname{Res}_b(BG,BH)\right)
 =256A^4B^6a^2.
\]

The residual `a=0` branch is not an exceptional parameter component: `F=0`
then gives `c=0`, while `G=0` gives `A=0`.  Hence the projected exceptional
amplitude locus is exactly `A B=0`.  Algebraically the certificate-exceptional
locus is `A B Y=0`; independently, `R=0` is excluded because the Fourier model
degenerates there.

Consequently no nonzero scale-dependent choice of the two seed amplitudes
evades this frozen finite-support, second-order tangency obstruction.  The claim
does not cover other supports, altered relative amplitudes within either seed
family, approximate leakage, infinite-mode mechanisms, or Navier--Stokes
regularity.

## Verification

Run

```sh
PYTHONPATH=.cycle206-sympy python3 \
  millennium-prize/navier-stokes/verify_cycle206_parametric_obstruction.py
```

The verifier constructs the amplitude-weighted Fourier field and
Leray-projected Navier vector field from the support, checks all 19 selected
linear rows under the displayed substitution, independently recomputes the
three nonlinear rows and terminal seed derivative, checks their closed forms,
and verifies the identity and both resultants symbolically. These rows are a
sufficient subsystem, not the complete exterior linear closure: the full
closure at the original nonzero seed has rank 27 and only strengthens the
obstruction. SymPy 1.13.3 was used for the recorded run.
