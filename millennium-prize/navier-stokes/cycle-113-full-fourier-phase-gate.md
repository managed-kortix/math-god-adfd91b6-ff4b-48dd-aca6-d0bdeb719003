# Cycle 113: full-Fourier phase gate

## Correct observable

Support leakage is not phase escape.  For a physical oriented triad
`k+p=q`, define the translation- and polarization-gauge-invariant interaction
scalar

\[
 \Xi_{kpq}=\overline{u_q}\cdot
 ((u_k\cdot p)u_p+(u_p\cdot k)u_k).
\]

Its argument measures the phase of the complete physical interaction.  Modes
born from zero have no phase derivative at birth; their Fourier launch vectors
must instead enter the full second jet of `Xi`.

## Exact packet and failed escape

On the normalized `2 pi` torus take

\[
k=(1,0,0),\quad p=(0,1,0),\quad q=(1,1,0),
\]
\[
u_k=(0,1,1),\quad u_p=(1,0,1),\quad
u_q=-i(1,-1,1),\qquad u_{-n}=\overline{u_n}.
\]

The full Euler convolution, with no Galerkin projection, gives positive vortex
stretching `S=4`.  The interaction is maximized since `Xi(0)=2i`.  Four modes
outside the initial support are generated, with total squared launch velocity
`44/5`.  Nevertheless exact differentiation including all those launch modes
gives

\[
 \Xi(t)=2i+2it-\frac{52}{5}it^2+O(t^3).
\]

Thus its phase has zero first and second derivatives.  More strongly, the
parity class

\[
u_n\in\mathbb R^3\ (n_1+n_2\text{ odd}),\qquad
u_n\in i\mathbb R^3\ (n_1+n_2\text{ even})
\]

is invariant under Euler and Navier--Stokes evolution.  Consequently `Xi`
remains purely imaginary, and while its sign remains positive its maximizing
phase remains exactly `pi/2`.  Full support leakage therefore does not imply
departure from a maximizing physical triad phase.

The dependency-free verifier reconstructs the complete first convolution and
second derivative over exact Gaussian rationals:

```sh
python millennium-prize/navier-stokes/verify_cycle113_phase_packet.py
```

## Strategic consequence

Qualitative packet transversality could not yield regularity even if it held.
Near invariant triad faces, arbitrarily small connector amplitudes preserve
order-one stretching while making any transverse defect tend to zero.  Integer
Navier scaling replicates the same dimensionless defect at arbitrary shells.
A regularity argument would require a uniform coercive ratio, telescoping
critical flux, or irreversible phase-dispersion identity; local leakage gives
none of these.  The amplitude-coupled phase-escape funnel is retired.

No regularity theorem or Millennium solution is claimed.
