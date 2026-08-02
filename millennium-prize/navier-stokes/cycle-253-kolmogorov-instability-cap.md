# Cycle 253: Kolmogorov instability is only a local departure mechanism

## Verdict: EXACT MODE ARCHITECTURE, FACTOR-TWO GATE NOT CROSSED

The classical unstable periodic Kolmogorov shear gives a deterministic smooth
Euler family and genuine self-induced nonlinear departure from a steady flow.
It does not presently give `ND251`. The spectral and nonlinear-instability
theorems amplify an arbitrarily small perturbation to a fixed positive
departure chosen within a sufficiently small neighborhood of the shear; they
do not control the orbit beyond that neighborhood. In any common relative velocity-`L^3` ball of
radius `rho<1/3`, every two-time norm ratio is strictly below two:

\[
 {\|u(t)\|_3\over\|u(s)\|_3}\le {1+\rho\over1-\rho}<2.       \tag{253.1}
\]

For an orbit launched arbitrarily close to the shear, a factor-two increase in
the directed orientation requires an order-one endpoint departure, not merely
the fixed small departure furnished by nonlinear instability. Thus the
local perturbative theorem is inherently capped as a proof mechanism. This is not a
global cap on Kolmogorov-flow evolution and not a proof that a large excursion
on its unstable manifold cannot occur.

## Frozen torus and steady state

Work on

\[
 \mathbb T^2=(\mathbb R/2\pi\mathbb Z)^2,
 \qquad k=3,\quad n_0=4,
 \qquad \alpha={k\over n_0}={3\over4},                    \tag{253.2}
\]

with normalized Haar measure. Fix

\[
 U_A(y)=(A\cos(4y),0),\qquad
 \Omega_A(y)=4A\sin(4y),\qquad A>0.                       \tag{253.3}
\]

The sign of `Omega_A` depends only on the curl convention and has no effect on
the conclusions. This is a smooth mean-zero stationary Euler solution. Its
norms are exact:

\[
 \|U_A\|_2={A\over\sqrt2},\qquad
 \|U_A\|_3=A\left({4\over3\pi}\right)^{1/3}.             \tag{253.4}
\]

The ratio `1/2<alpha<1` is the simplest classical unstable window: only the
central lattice point on the vertical rail lies strictly inside the base
Fourier circle. Choosing the integer pair `(k,n_0)=(3,4)` realizes that ratio
on the standard square torus required by `ND251`, with no rectangular-domain
change hidden in the setup.

## Exact linear mode setup

Write perturbation vorticity in the designated streamwise class as

\[
 q(t,x,y)=e^{\lambda t}e^{i3x}
             \sum_{j\in\mathbb Z}q_je^{i4jy}.             \tag{253.5}
\]

For velocity convention `v=nabla^perp Delta^{-1}q`, linearization about
`U_A` gives the bi-infinite tridiagonal recurrence

\[
 \lambda q_j+{3iA\over2}
 \left[
 \left(1-{16\over9+16(j-1)^2}\right)q_{j-1}
 +\left(1-{16\over9+16(j+1)^2}\right)q_{j+1}
 \right]=0.                                               \tag{253.6}
\]

Changing the curl or perpendicular-gradient convention conjugates signs but
does not change the growth rate. Equation (253.6), square summability, the
normalization `sum |q_j|^2=1`, the positive real eigenvalue, and the phase
condition `q_0>0` specify the unstable mode without a Galerkin projection.
Equivalently, its two half-line continued fractions must match at `j=0`. The
classical Kolmogorov-flow spectral theorem gives a positive real growth rate
for this rail because `0<k/n_0<1`; taking the real part of (253.5) gives a real
analytic divergence-free eigenmode `V`.

This infinite tail is indispensable. The three coefficients `j=-1,0,1` do not
form an invariant Euler system: (253.6) immediately couples them to `j=+-2`,
and the quadratic equation generates streamwise harmonics `mk` with
`m=0,+-2,+-3,...`.
Consequently a three-mode or any fixed Galerkin crossing is not an exact Euler
certificate.

## Exact fixed-energy launch

Normalize the real eigenvelocity by `\|V\|_2=1`; it is `L^2`-orthogonal to
`U_1` because its streamwise frequency is nonzero. For

\[
 0<\varepsilon<{A\over\sqrt2},\qquad
 a_\varepsilon=\sqrt{A^2-2\varepsilon^2},               \tag{253.7}
\]

set

\[
 u_0^\varepsilon=a_\varepsilon U_1+\varepsilon V.       \tag{253.8}
\]

Then, exactly,

\[
 \|u_0^\varepsilon\|_2^2={a_\varepsilon^2\over2}
 +\varepsilon^2={A^2\over2}=\|U_A\|_2^2.                \tag{253.9}
\]

The corresponding curl is a deterministic smooth mean-zero vorticity, and its
unique two-dimensional Euler solution is global and conserves (253.9). This
repairs the otherwise common error of adding an unstable eigenmode while
claiming that the energy still equals that of the unperturbed shear.

The first variation of the cubic norm at the shear also vanishes for this
launch. Indeed,

\[
 D\!\left(\int|u|^3\right)_{U_A}[V]
 =3\int |U_A|U_A\mathbin\cdot V=0,                       \tag{253.10}
\]

because `V` has nonzero streamwise frequency. The base-amplitude correction in
(253.7) is quadratic as well. Thus the initial velocity-`L^3` shape change is
`O(epsilon^2)`, not `O(epsilon)`.

## Quantitative perturbative cap

Let `M=\|U_A\|_3` and suppose two times belong to the same relative ball

\[
 \|u(r)-U_A\|_3\le\rho M,\qquad r=s,t,
 \quad 0\le\rho<1.                                      \tag{253.11}
\]

The triangle and reverse-triangle inequalities give

\[
 (1-\rho)M\le\|u(r)\|_3\le(1+\rho)M,
\]

and hence (253.1). In particular, a theorem controlling the entire comparison
inside any ball with `rho<1/3` cannot prove a factor-two ratio.

There is a stronger one-sided requirement for (253.8). If
`\delta_\varepsilon=\|u_0^\varepsilon-U_A\|_3/M`, then

\[
 \|u(T)-U_A\|_3
 >\bigl(1-2\delta_\varepsilon\bigr)M                    \tag{253.12}
\]

is necessary for `\|u(T)\|_3>2\|u_0^\varepsilon\|_3`.
Thus, as `epsilon` tends to zero, the required endpoint must leave essentially
the full `L^3` size of the background shear. A small fixed nonlinear departure
cannot approach this requirement.

For `s>2`, standard Euler energy estimates for
`z=u-U_A` have the schematic explicit comparison form

\[
 {dX\over dt}\le a_sX+b_sX^2,
 \qquad X=\|z\|_{H^s},                                  \tag{253.13}
\]

where `a_s=C_s\|U_A\|_{H^{s+1}}` and `b_s=C_s` after fixing
the Fourier Sobolev algebra constant on the standard torus. Therefore

\[
 X(t)\le {X(0)e^{a_st}\over
  1-(b_sX(0)/a_s)(e^{a_st}-1)}                           \tag{253.14}
\]

while the denominator is positive. Sobolev embedding turns (253.14) into
(253.11). This is only an upper enclosure. The unstable eigenvalue supplies
linear growth `epsilon e^{lambda t}`, while nonlinear-instability theorems
justify departure at a time of order

\[
 T_\varepsilon\sim\lambda^{-1}\log(\delta/\varepsilon) \tag{253.15}
\]

for a sufficiently small fixed `delta`. Their bootstrap deliberately closes
inside a local Sobolev neighborhood. It neither continues the unstable
manifold to the order-one threshold (253.12) nor gives directed endpoint
`L^3` enclosures there.

## What is and is not capped

Energy alone does not cap velocity `L^3` on its sphere. A smooth localized
divergence-free bump of diameter `ell`, rescaled to fixed `L^2`, has `L^3` of
order `ell^(-1/3)` in two dimensions. Hence there is no universal fixed-energy
factor-two obstruction. Such bumps need not be equimeasurable in vorticity with
(253.3) and need not lie on its Euler orbit, so this observation is not an
`ND251` construction.

The exact conclusion is narrower:

1. linear Kolmogorov instability is real and its full infinite mode is given by
   (253.5)--(253.6);
2. the energy-corrected launch (253.7)--(253.9) is an actual smooth Euler datum;
3. local nonlinear instability yields only a small, usually unspecified,
   departure and is blocked from factor two by (253.1) or, for a near-shear
   launch, by (253.12);
4. no theorem used here bounds a later global excursion of the unstable
   manifold, so the Kolmogorov architecture is not globally retired.

To promote this architecture, one must rigorously continue one branch beyond
the local instability regime and enclose the complete Euler solution until
(253.12), including all generated streamwise classes. A numerical Rayleigh
eigenvalue, a Galerkin trajectory, or the abstract word "instability" is not
such a packet.

## Sources

1. L. D. Meshalkin and Ya. G. Sinai, *Investigation of the stability of a
   stationary solution of a system of equations for the plane movement of an
   incompressible viscous liquid*, J. Appl. Math. Mech. 25 (1961), 1700--1705.
2. S. Friedlander, W. Strauss, and M. Vishik, *Nonlinear instability in an
   ideal fluid*, Ann. Inst. H. Poincare Anal. Non Lineaire 14 (1997), 187--209.
3. Z. Lin, *Instability of some ideal plane flows*, SIAM J. Math. Anal. 35
   (2003), 318--356, DOI `10.1137/S0036141002406266`.

The cited instability results must be used with their stated function-space
and spectral hypotheses; they do not assert a factor-two norm excursion. No
Navier--Stokes regularity result or Millennium solution is claimed.
