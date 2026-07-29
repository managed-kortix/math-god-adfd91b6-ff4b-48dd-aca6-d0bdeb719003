# Cycle 91: helical-sector and cumulative-stretching audit

## Exact sector obstruction

Writing
\[
 \widehat u(k)=u_+(k)h_+(k)+u_-(k)h_-(k),\qquad
 ik\times h_s(k)=s|k|h_s(k),
\]
gives the signed helicity and critical magnitude
\[
 H/2=K_+-K_-,\qquad
 \|u\|_{\dot H^{1/2}}^2/2=K_++K_-.
\]
The nonlinear sector production rates satisfy `G_+=G_-`: opposite helicity
magnitudes can be created in equal amounts while signed helicity is conserved.
Thus energy and signed helicity do not control the critical norm.

The positive-homochiral cone is not invariant.  An exact certificate is
\[
 k=(1,0,0),\quad p=(0,1,1),\quad q=(1,1,1),
\]
with positive-helicity coefficients
\[
 a=2^{-1/2}(0,1,i),\qquad
 b=(2^{-1/2},i/2,-i/2).
\]
For the real field supported at `+-k,+-p`, the negative-helicity coefficient
of `B(u,u)` at `q` has imaginary part
\[
 \frac{\sqrt3+\sqrt2-3}{4\sqrt6}\ne0.
\]
Hence full Navier--Stokes immediately creates the opposite sector.  Positive
helicity becomes coercive only in the explicitly decimated equation.

## Cumulative shell gate

Assign every ordered stretching triad once to its largest dyadic shell and
write
\[
 S(t)=\int (\omega\cdot\nabla)u\cdot\omega=\sum_j\sigma_j(t),
 \qquad Z(t)=\|\nabla\omega\|_2^2=\sum_j z_j(t).
\]
The candidate estimate
\[
 \sup_{T<T_*}\sum_j\int_0^T
 [\sigma_j-\theta\nu z_j]_+dt<\infty,\qquad 0<\theta<1,
\]
implies a uniform enstrophy bound by the exact enstrophy identity, and hence
global regularity.

It is not an independently produced lemma.  If a smooth unforced periodic
solution is global, smoothness gives absolute triad summability on compact
time intervals, while eventual smallness and parabolic smoothing give
exponential decay of every Sobolev norm.  The displayed positive-excess
functional is therefore finite.  For arbitrary smooth data its finiteness is
equivalent to global regularity.

Positive-part shell functionals are also decomposition-sensitive.  Splitting
two components with energies `1+-sin(Nt)` counts positive variation `4N` over
`[0,2*pi]`, whereas merging them counts zero.  Thus norm equivalence does not
make shellwise positive variation intrinsic.

Finally, phase-blind spectra cannot supply pointwise depletion.  A phase flip
on one mode of a nondegenerate triad preserves every diagonal quadratic
spectral quantity but reverses the stretching contribution.  Scaling the
amplitude makes `S/(nu Z)` arbitrarily large.  Any viable route must add a
genuinely dynamical phase theorem; merely postulating integrated phase
depletion with an arbitrary data-dependent bound again restates the required
enstrophy control.

The helical cumulative-stretching tactic is therefore retired.  The exact
opposite-helicity creation certificate is retained as a reusable no-go.  No
regularity result is claimed.
