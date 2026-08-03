# Cycle 272: P3 finite-support admission audit

## Verdict: INITIAL INFINITE-SUPPORT REQUIREMENT REMOVED

`ND270-ADMISSION` incorrectly promoted a property of an Euler trajectory into
a property of its initial datum. Kishimoto--Yoneda excludes a real Euler
solution that remains in one fixed finite Fourier support and is nonstationary;
it does not exclude finitely supported initial data whose quadratic Euler
field launches exterior modes. The generated modes are precisely what the
full-PDE analytic majorant must control. Requiring infinite support at `t=0`
therefore rejects valid launch data without strengthening the trajectory
certificate.

Revised item 1 permits a finitely printed smooth real mean-zero
divergence-free datum with finite or infinite initial Fourier support. If the
initial support is finite, item 4 must provide a full-Euler analytic majorant
for every generated mode on the declared interval; a Galerkin truncation or a
bound only on the initial coefficients does not qualify. The
Kishimoto--Yoneda breaker remains unchanged: an asserted orbit confined to one
fixed finite support is stationary (up to Galilean translation when a mean is
present) and cannot be promoted.

## Audit of the P3 datum

The datum in `cycle-272-p3-example.json` passes the corrected architecture
tests.

1. It is an exact rational trigonometric polynomial. Every polarization is
   perpendicular to its wave vector, and it has zero mean.
2. Its support contains `(0,0,1)`, `(1,1,0)`, and `(1,1,1)`, which span
   `R^3`; hence it is genuinely three-dimensional in the support sense.
3. `cycle-272-p3-certificate.json` gives an outward-rounded lower endpoint
   greater than `15262` for
   `P3(u)=d/dt integral |u|^3` at `t=0`. In particular one may freeze the
   rational admission margin `P3(u)>15000`. This is a complete-field pressure
   flux, not a vorticity, component, projection, or Galerkin proxy.
   Moreover, normalized Haar measure and the componentwise Wiener bound give
   the exact companion estimate
   `integral |u|^3 <= (8119/15)^3=535189549159/3375`.
4. The same strict derivative excludes stationarity modulo translation:
   translations preserve `integral |u|^3`, so every relative equilibrium has
   zero derivative of that functional.
5. The field is not a Kida--Pelz datum, a `K-F(K)/32` tangent profile, or a
   Kida core with a decorative tail. Its printed low-frequency circular shear
   and five-wave interaction are the production architecture itself. The
   Cycle 272 Kida-tail deletion rule is therefore inapplicable; there is no
   tail whose deletion exposes a retired Kida driver.

The local certificate alone does not certify a factor-two endpoint and does
not authorize a Galerkin substitution. It establishes that this datum is a new
active architecture rather than `ND270-DUPLICATE`.

## Exact generated-scale majorant

Use the dimension-independent velocity Wiener estimate from Cycle 265,

\[
 D^+A_{q(t)}(u(t))
 \leq (A_{q(t)}(u(t))+q'(t)/q(t))D_{q(t)}(u(t)).
\]

For this datum freeze

\[
 q_0={33\over32},\qquad M=600,\qquad \alpha=600,
 \qquad T={1\over65536},\qquad q(t)=q_0(1-\alpha t).
\]

Regard the datum as a singleton rational family with parameter box `{0}` and
freeze the interval `[0,T]`; no witness or horizon is selected after output.

Using the component `l1` norm as an exact upper bound for each Euclidean
polarization gives

\[
 A_{q_0}(u_0)\leq {91652781\over163840}<600,
 \qquad q(T)={267861\over262144}>1.
\]

Thus the full Euler solution satisfies

\[
 A_{q(t)}(u(t))\leq600,
 \qquad
 \sum_{|k|_\infty=n}|u_k(t)|_2\leq600q(t)^{-n}
 \quad(0\leq t\leq T).
\]

This is a closed analytic majorant for all generated scales, including modes
absent at `t=0`. It is not the zero `analytic_tail` field in the local P3 JSON,
which only records that the initial datum has no unresolved tail.

## Revised disposition

The P3 datum passes corrected admission items 1--4 and the novelty
check. It must not be rejected for finite initial support. A full
`ND270-ADMIT` compute authorization still requires the independent items that
the P3 artifacts do not print: a promotion margin and outward endpoint rule,
finite resources, and the concrete
full-Euler/transfer replay interface. Until that manifest is written, the
precise state is

`P3 ARCHITECTURE ADMISSIBLE; COMPUTE MANIFEST NOT YET FROZEN.`

No factor-two Euler crossing, Navier--Stokes result, or Millennium result is
claimed.
