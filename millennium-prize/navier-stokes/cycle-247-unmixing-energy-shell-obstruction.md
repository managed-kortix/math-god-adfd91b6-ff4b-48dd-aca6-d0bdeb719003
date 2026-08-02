# Cycle 247: unmixing must stay on the Euler energy shell

## Verdict

The proposed inverse-mixing mechanism has an exact obstruction in its stated
form. For every smooth mean-zero two-dimensional Euler solution,

\[
 \|\omega(t)\|_{\dot H^{-1}(\mathbb T^2)}
 =\|u(t)\|_{L^2(\mathbb T^2)}
 =\|u(0)\|_{L^2(\mathbb T^2)}.                         \tag{247.1}
\]

Consequently no dynamically accessible Euler rearrangement can strictly
increase the homogeneous Hilbert `dot H^-1` norm of vorticity. In particular,
a static area-preserving rearrangement that unmixes positive and negative
vorticity and strictly increases this energy norm fails the conserved-energy
gate and cannot be the endpoint of the same Euler orbit.

If `H^-1` instead denotes the inhomogeneous multiplier
`(1+|k|^2)^(-1/2)`, it is not identical to energy and need not be conserved.
Growth of that norm is not itself obstructed, but it still does not pass the
Euler gate unless the homogeneous quantity in (247.1) is exactly unchanged.

This does not obstruct the Cycle 211 target. The relevant identity there is

\[
 \|u\|_{L^3}\asymp\|\omega\|_{W^{-1,3}},               \tag{247.2}
\]

and `W^(-1,3)` is not conserved. Thus a factor-greater-than-two endpoint can
only come from a shape change of the Biot--Savart velocity on one fixed
`dot H^-1` energy sphere, not from growth of `dot H^-1` itself. No such Euler
orbit is constructed here, so `LA242` is not admitted.

## Exact energy-shell obstruction

Use normalized Haar measure and write the periodic Biot--Savart law as

\[
 u=\nabla^\perp\Delta^{-1}\omega,
 \qquad \widehat u(k)=-i\frac{k^\perp}{|k|^2}\widehat\omega(k)
 \quad(k\ne0),                                        \tag{247.3}
\]

up to the harmless sign convention for `Delta`. Parseval gives

\[
 \|u\|_2^2
 =\sum_{k\ne0}\frac{|\widehat\omega(k)|^2}{|k|^2}
 =\|\omega\|_{\dot H^{-1}}^2.                         \tag{247.4}
\]

Smooth 2D Euler conserves kinetic energy, proving (247.1). If `eta` is a smooth
area-preserving diffeomorphism and

\[
 \omega_1=\omega_0\circ\eta^{-1},                     \tag{247.5}
\]

then equimeasurability preserves all vorticity Casimirs. Euler accessibility
additionally requires the exact scalar condition

\[
 \mathcal D(\eta;\omega_0)
 :=\langle\omega_1,(-\Delta)^{-1}\omega_1\rangle
  -\langle\omega_0,(-\Delta)^{-1}\omega_0\rangle=0.  \tag{247.6}
\]

Therefore every proposed separated-sign endpoint with `mathcal D>0`, including one
 advertised as having larger `dot H^-1`, is rejected by one exact invariant before
any orbit construction. Equal Casimirs do not repair this failure.

The condition `mathcal D=0` is necessary but still not sufficient. A path
`eta(t)` with `eta(0)=id` is the Lagrangian map of the Euler solution from
`omega_0` exactly when it satisfies the self-consistency equation

\[
 \partial_t\eta(t,a)
 =K[\omega_0\circ\eta(t)^{-1}](\eta(t,a)),             \tag{247.7}
\]

where `K=grad^perp Delta^-1`. An arbitrary area-preserving isotopy is generated
by some divergence-free external velocity, but generally not by the velocity
induced by its transported scalar. Equation (247.7), not mere smooth
area-preservation, is the dynamical-accessibility gate.

## What time reversal does and does not supply

Suppose a rigorously constructed smooth Euler orbit satisfies

\[
 \|u(T)\|_3<\frac12\|u(0)\|_3.                        \tag{247.8}
\]

Then

\[
 u^R(t,x)=-u(T-t,x),\qquad
 \omega^R(t,x)=-\omega(T-t,x)                         \tag{247.9}
\]

is an exactly accessible smooth Euler orbit with endpoint ratio greater than
two. No separate realization of the reversed diffeomorphism is needed. This is
the clean positive implication requested by the inverse mechanism.

However, no smooth Euler orbit can satisfy a corresponding strict decay of the
full homogeneous `dot H^-1` vorticity norm, because (247.1) is constant in both
time directions. Rigorous statements called Euler mixing must therefore
concern an inhomogeneous or projected norm, a passive scalar, a perturbation, a
weak topology, a positive-order quantity, or a component relative to a
background. None implies (247.8) without a same-norm estimate for the complete
velocity.

There is also a quantitative background obstruction. If a mixing theorem
decomposes both endpoints as

\[
 u(j)=U+v_j,\qquad \|v_j\|_3\leq\varepsilon\|U\|_3,
 \quad j=0,T,
\]

with `0<=epsilon<1`, then the triangle inequality gives

\[
 \frac{\|u(T)\|_3}{\|u(0)\|_3}
 \leq\frac{1+\varepsilon}{1-\varepsilon}.             \tag{247.10}
\]

A factor above two requires `epsilon>1/3`. Hence perturbative mixing around a
dominant steady shear or vortex cannot reach the gate while its perturbative
parameter is at most `1/3`; the background contribution cannot be discarded
from either endpoint norm.

## Necessary geometry of any surviving endpoint pair

Let `Q=||u(t)||_2`, which is fixed. On the normalized torus,
`||u||_3>=||u||_2`. Therefore

\[
 \frac{\|u(T)\|_3}{\|u(0)\|_3}>2
 \quad\Longrightarrow\quad
 \frac{\|u(T)\|_3}{Q}>2.                              \tag{247.11}
\]

The high-`L^3` endpoint must thus be genuinely concentrated relative to its
fixed energy; merely moving vorticity to lower frequencies is insufficient.
Combining (247.11) with the Cycle 216 Gagliardo--Nirenberg estimate gives the
necessary screen

\[
 2<C_{\mathbb T^2}
 \left(\frac{Z}{\kappa_0^2E}\right)^{1/6},            \tag{247.12}
\]

where `E=Q^2` and the conserved enstrophy is `Z=||omega||_2^2`. Any declared
family whose certified right side is at most two is rejected independently of
its proposed squeezing geometry.

## Corrected finite admission object

A viable continuation may use separated coherent signs only after replacing
the false `H^-1` growth objective by the following fixed-energy-shell packet.

1. Give a deterministic smooth real mean-zero `omega_0` and a smooth
   area-preserving endpoint map `eta` for which (247.6) is exactly zero.
2. Prove by directed Biot--Savart cubature that
   `||K(omega_0 o eta^-1)||_3>(2+eta_*)||K omega_0||_3` for explicit
   `eta_*>0`. This is a static screen, not yet an Euler orbit.
3. Supply a path satisfying the self-induced equation (247.7), or equivalently
   a full Euler enclosure with zero vorticity residual. Prescribing a passive
   mixer fails this item.
4. Control every generated scale and then attach the Cycle 211 inviscid-limit,
   amplitude-scaling, and three-dimensional embedding constants.

For a finite parameter box, interval exclusion of zero from `mathcal D` is an exact
breaker for item 1. If item 1 passes, interval exclusion of the factor-two
ratio rejects item 2. If both pass, any nonzero enclosed residual in (247.7)
rejects the proposed path, though proving nonexistence of every alternative
Euler path would require more than checking one parametrization.

The durable conclusion is therefore an obstruction and a correction, not a
construction: growth of the full-vorticity homogeneous `H^-1` energy norm is
impossible along Euler, while fixed-`dot H^-1`, variable-`W^(-1,3)` unmixing
remains exactly the open mechanism. No Navier--Stokes or Millennium result is
claimed.
