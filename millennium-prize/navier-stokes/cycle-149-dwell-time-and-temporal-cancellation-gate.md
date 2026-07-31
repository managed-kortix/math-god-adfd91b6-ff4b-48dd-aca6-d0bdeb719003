# Cycle 149: the exact dwell-time ledger and its temporal-cancellation failure

The relative-rate idea has one exact phase-robust identity, but it does not
close against the Navier--Stokes energy budget.  Large forcing on a tiny Fourier
mode can persist through rapid temporal rotation or cheap high-frequency
viscous absorption.

For one mode write

\[
\dot u+\lambda u=F,
\qquad\lambda=\nu|k|^2.
\]

If on an interval `I` one has

\[
|F|\ge f,
\qquad |u|\le\varepsilon,
\]

then the reverse triangle inequality gives

\[
|\dot u|\ge(f-\lambda\varepsilon)_+.
\]

The exact action identity is

\[
\boxed{
\int_I\left(\frac{|\dot u|^2}{\lambda}+\lambda|u|^2\right)dt
=\int_I\frac{|F|^2}{\lambda}dt-|u(b)|^2+|u(a)|^2.
}
\]

Thus tiny amplitude under large forcing pays either ordinary viscous
dissipation or the temporal action `|du/dt|^2/lambda`.  The second term is
indispensable: energy controls the dissipation but not this temporal action.

Indeed, in a two-dimensional real plane take

\[
u(t)=A(\cos\omega t,\sin\omega t),
\qquad F=\dot u+\lambda u.
\]

Choosing

\[
A=\frac f{\sqrt{\lambda^2+\omega^2}}
\]

gives `|F|=f` and arbitrarily small `|u|` for arbitrarily long intervals.  As
`omega` grows, ordinary viscous dissipation tends to zero while the temporal
action carries the entire cost.  A rapidly detuned quadratic Fourier triad
realizes the same mechanism exactly: order-one nonlinear forcing rotates at
frequency `O(N^2)` and creates only an `O(N^-2)` response.

Viscosity provides a second loophole.  A quasi-steady high-frequency mode under
fixed forcing satisfies

\[
u_k\simeq\frac{F_k}{\nu|k|^2},
\qquad
\nu|k|^2|u_k|^2\simeq\frac{|F_k|^2}{\nu|k|^2}.
\]

Thus order-one forcing can be absorbed at energy cost tending to zero as
`|k| -> infinity`.  Such a mode is dissipated rather than efficiently
transferred onward; nevertheless it defeats a forcing-magnitude dwell tax.

There is an exact globally budgetable Duhamel norm.  On `I=[s,T]`, let

\[
(K_\lambda F)(t)=\int_s^t e^{-\lambda(t-r)}F(r)dr.
\]

For a mode generated from zero,

\[
\|K_\lambda F\|_{L^2(I)}^2=\int_I|u(t)|^2dt.
\]

Hence the energy inequality gives

\[
\sum_k\nu|k|^2\|K_{\nu|k|^2}F_k\|_{L^2(I)}^2
\le\frac12\|u(s)\|_2^2.
\]

This budget sees only dynamically effective, heat-filtered forcing.  It does
not control the unsigned integral of `|F_k|`; rapid temporal oscillations are
correctly discounted.  Therefore the remaining gate is an exact-symbol
temporal-coherence theorem, not another pointwise forcing estimate.

The binary promotion criterion is now precise.  Every efficient shell transfer
must force a coherent Duhamel response and a nonsummable charge in a known
finite positive spacetime budget, with scale-independent constants and bounded
interval overlap.  A theorem charging uncontrolled temporal action or higher
dissipation does not count.

No such coherence theorem is currently established.  This closes forcing
magnitude, relative rate, and nominal dwell time as standalone regularity
mechanisms.  It does not prove regularity or blowup.
