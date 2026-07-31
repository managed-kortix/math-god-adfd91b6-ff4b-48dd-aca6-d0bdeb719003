# Cycle 177: cubic-flux parity and budget gate

The Cycle 176 Laurent filter does not immediately become a stronger cascade
mechanism when its quadratic boundary output is renamed cubic energy flux.  On
the field constructed there the physical cubic flux is identically zero.  If a
receiver is added to make that flux nonzero, its signed time integral is the
ordinary shell-energy ledger.  A new route therefore needs a uniform
one-sided/coherent-flux theorem; neither parity nor energy bookkeeping supplies
one.

## The unaugmented filter has zero cubic flux

Use the Fourier convention

\[
 N_q(u)=iP_q\sum_{p+r=q}(u_p\mathbin\cdot r)u_r.
\]

Cycle 176 constructs a real divergence-free field whose nonzero coefficients
are real vectors and whose complete algebraic convolution before the common
factor `i` is supported only at the terminal quartet

\[
 Q_D=\{(\pm R_D,\pm Y,0)\}.
\]

None of those terminal modes is occupied by the input field.  Consequently

\[
 \operatorname{Re}(\overline{u_q}\cdot N_q(u))=0
 \qquad(q\in\mathbb Z^3)
\]

for two independent reasons: `u_q=0` on `Q_D`, while away from `Q_D` the
complete convolution vanishes.  Even if a real receiver coefficient is merely
inserted at a terminal mode, its pairing with the purely imaginary forcing is
still zero at that instant.  Thus quadratic boundary-output norm and physical
cubic flux are not interchangeable observables.

A nonzero terminal flux requires a relative phase, for example an imaginary
receiver paired with the `i` times real boundary forcing.  Its size is then
linear in the receiver amplitude and quadratic in the two input families.  It
is therefore subject to an additional normalization freedom absent from the
Cycle 176 product identity.  The receiver also becomes part of the full field,
so all of its new quadratic interactions must be included; the four-mode
output statement cannot simply be reused unchanged.

## Parity does not supply irreversibility

The checkerboard Fourier phase class from Cycles 113 and 146 is invariant under
Euler and Navier--Stokes evolution.  It can contain phase-locked nonzero triad
transfer when the receiver lies in the imaginary checkerboard class.  Hence a
nonzero cubic flux does not force departure from that parity class, phase
dispersion, or exterior launch.  Conversely the all-real Cycle 176 slice sits
at a zero-flux phase.  Moving from the slice to a flux-carrying receiver is an
extra phase hypothesis, not a consequence of the Laurent cancellation.

This is the exact parity decision: the cubic route is not pointwise equivalent
to the quadratic-output route, because the latter may be nonzero while the
former is zero; after a receiver phase is imposed, invariant parity still does
not give a one-sided sign or prevent reversal.

## The signed flux is the existing energy budget

Let `A` be any fixed symmetric set of Fourier modes and define

\[
 E_A(t)={1\over2}\sum_{q\in A}|u_q(t)|^2,
 \qquad
 D_A(t)=\nu\sum_{q\in A}|q|^2|u_q(t)|^2.
\]

For a smooth solution, with forcing omitted, the exact projected energy
identity is

\[
 {d\over dt}E_A(t)+D_A(t)
 =-\sum_{q\in A}\operatorname{Re}
   (\overline{u_q}\cdot N_q(u))
 =:\Pi_A(t).
\]

Therefore

\[
 \int_s^t\Pi_A(r)\,dr
 =E_A(t)-E_A(s)+\int_s^tD_A(r)\,dr.
\]

For `A` or its complement this is exactly the ordinary energy-transfer ledger.
Global cubic energy transfer sums to zero.  The identity controls signed net
transfer, not

\[
 \int_s^t|\Pi_A(r)|\,dr,
 \qquad
 \int_s^t(\Pi_A(r))_+\,dr,
\]

nor a sum over moving or overlapping shell boundaries.  Repeated forward and
backward transfers can have a small signed total.  Treating every positive
instantaneous cubic event as a separately spendable charge would therefore
double count the same energy unless bounded overlap and suppressed reverse
flux are proved.  This is the same temporal-coherence obstruction isolated in
Cycle 149, now written in the physical cubic observable.

## Falsification gate

The cubic-flux route is promoted only if it proves the following statement for
the exact unaveraged Leray evolution, with constants independent of scale and
cascade depth.

> For every efficient depth-`L` transfer circuit, there are fixed shell sets
> `A_j` and time intervals `I_j` of uniformly bounded overlap such that the
> physical fluxes satisfy a one-sided coherent lower bound
> \[
> \sum_j\int_{I_j}(\Pi_{A_j})_+\,dt\ge cL-C,
> \]
> while reverse flux and boundary-motion errors are bounded by a fixed fraction
> of the left side, and the resulting charge is dominated by one declared
> finite positive Navier--Stokes budget.

The gate is falsified by any arbitrary-depth exact-symbol family with efficient
designated transfers but bounded charge in that same budget, including a
phase-locked parity family with oscillatory/reversible flux or a completed
family whose heat-filtered receiver response tends to zero.  Testing raw
quadratic output, one instant, one chosen phase, or unsigned flux without a
budget domination does not pass the gate.

## Strategic verdict

**Rotate.**  The immediate cubic reinterpretation fails: it is zero on the
Cycle 176 field, and after adding a receiver its signed integral is the existing
energy budget.  Continuing is justified only as a bounded adversarial scout for
the displayed one-sided temporal-coherence inequality.  It should not remain
the main funnel without either that exact lemma or an exact arbitrary-depth
counterexample.  No Navier--Stokes regularity or blowup result is claimed.
