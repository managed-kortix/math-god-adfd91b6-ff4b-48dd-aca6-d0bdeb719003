# Cycle 211: Euler reversal as the factor-two breaker

## Decision

The high-variance route should search first for a two-dimensional Euler orbit,
not directly for seven Navier--Stokes viscosities. One smooth Euler trajectory
with

\[
  \|v(T)\|_{L^3(\mathbb T^2)}>(2+\eta)\|v(0)\|_{L^3(\mathbb T^2)},
  \qquad \eta>0,                                      \tag{211.1}
\]

rigorously transfers to a smooth periodic Navier--Stokes counterexample to the
Cycle 210 factor-two lemma. Arbitrarily large amplification would be stronger
than needed.

Time reversal makes decay and growth equivalent. If `v` solves Euler on
`[0,T]`, then

\[
  v^R(t,x)=-v(T-t,x), \qquad p^R(t,x)=p(T-t,x)
\]

also solves Euler. Thus a forward orbit on which the `L^3` norm falls by a
factor greater than two gives (211.1) after reversal.

This does not make the factor-two lemma obviously false. Reversibility alone
only says that a hypothetical Euler bound would imply

\[
 {1\over2}\leq {\|v(t)\|_3\over\|v(s)\|_3}\leq2
 \quad\hbox{for every pair }s,t\hbox{ on one orbit}.  \tag{211.2}
\]

There is no contradiction in a reversible Hamiltonian flow having a bounded
observable. A genuine orbit with oscillation greater than two is still needed.

## Exact viscosity and amplitude transfer

Fix a smooth mean-zero two-dimensional Euler datum `v_0` and a finite time
`T`. Let `w_mu` solve two-dimensional Navier--Stokes with the same datum and
viscosity `mu`. Standard fixed-time inviscid-limit stability gives

\[
 \sup_{0\leq t\leq T}\|w_\mu(t)-v(t)\|_{L^3}\longrightarrow0
 \quad(\mu\downarrow0).                               \tag{211.3}
\]

For a certificate this must not be used qualitatively. Subtract the equations,
estimate the difference in `H^{s-1}` with `s>3`, retain `mu Delta v` as the
forcing, and apply Gronwall. Bounds for the certified Euler orbit in `H^{s+1}`
then produce an explicit `mu_0(T,v,eta)>0` such that (211.1) implies

\[
 \|w_\mu(T)\|_3>2\|v_0\|_3 \qquad(0<\mu<\mu_0).       \tag{211.4}
\]

For physical viscosity `nu>0`, set

\[
 u_\lambda(t,x)=\lambda w_{\nu/\lambda}(\lambda t,x).
\]

Then `u_lambda` solves Navier--Stokes with viscosity `nu`, starts from
`lambda v_0`, and at physical time `T/lambda` has exactly the same norm ratio
as `w_(nu/lambda)` at time `T`. Choosing `lambda>nu/mu_0` proves the strict
factor-two crossing. Extending the field independently of `x_3` preserves the
ratio on `T^3`. Amplitude scaling therefore removes viscosity after an Euler
crossing is known; it cannot create a crossing by itself.

## What mixing would have to prove

For mean-zero two-dimensional vorticity,

\[
 v=\nabla^\perp\Delta^{-1}\omega,
 \qquad \|v\|_3\asymp\|\omega\|_{W^{-1,3}},           \tag{211.5}
\]

with constants fixed by the torus. Euler transports `omega` by an
area-preserving flow. Hyperbolic filamentation can therefore lower the
negative Sobolev norm of vorticity, and reversal turns that mixing into velocity
amplification. This is the correct conceptual mechanism.

Three obstructions prevent rearrangement from being a proof.

1. Euler conserves kinetic energy `||v||_2^2`, so `||v||_3` has a fixed
   orbit-dependent lower bound on the finite torus. Mixing cannot drive the
   full velocity norm to zero.
2. Equimeasurability preserves all vorticity Casimirs but not kinetic energy.
   Two attractive rearrangements with different `H^{-1}` energies cannot be
   endpoints of one Euler orbit.
3. Even equal energy and equal Casimirs do not show dynamical accessibility by
   the self-induced Euler flow. A prescribed passive-scalar mixer is not an
   Euler construction. In a perturbative background-plus-scalar argument, the
   background velocity enters both endpoint `L^3` norms and can suppress the
   desired ratio.

Consequently, static rearrangement is useful only as a design screen. To get
arbitrary amplification one would need a sequence of actual smooth Euler
orbits whose `L^3/L^2` concentration is large at one endpoint and nearly
relaxed at another while energy is unchanged. No such theorem is established
here.

## Rigorous production route

Optimize the full two-dimensional Euler equation over the frozen five-frequency
family and modest enlargements, with objective

\[
  J(v_0,T)=\log\|v(T)\|_3-\log\|v_0\|_3.
\]

Search both signs of time and prioritize vorticity packets stretched near
hyperbolic stagnation regions. A numerical hit should have substantial margin,
for example `exp(J)>2.2`, before certification.

A passing certificate has four parts:

1. directed Fourier or analytic-norm enclosures for the full Euler solution on
   `[0,T]`, including the unresolved tail;
2. a uniform high-Sobolev bound sufficient for the explicit inviscid-limit
   Gronwall estimate;
3. directed cubature proving the two endpoint `L^3` inequalities and a strict
   margin above two;
4. the explicit `mu_0` and amplitude threshold `lambda_0=nu/mu_0`, followed by
   the exact two-dimensional embedding in three dimensions.

This route is stronger and cleaner than separately certifying a grid of small
viscosities. Failure to find a crossing is only a finite-family exclusion. A
Galerkin crossing, passive-scalar rearrangement, positive initial derivative,
or qualitative appeal to the inviscid limit does not refute the factor-two
lemma.

No arbitrary-amplification theorem, Navier--Stokes counterexample, regularity
result, or Millennium solution is claimed.
