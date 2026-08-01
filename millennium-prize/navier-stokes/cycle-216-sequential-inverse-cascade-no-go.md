# Cycle 216: conservation obstruction to a separated sequential inverse cascade

## Verdict

Energy and enstrophy do impose a uniform endpoint `L^3` ratio on a
two-dimensional Euler orbit, provided the initial velocity is confined to a
finite frequency annulus. The bound depends on the initial frequency cap and
on the lowest nonzero torus frequency, but not on the number of
triads, cascade stages, packet gaps, elapsed time, phases, or Hamiltonian
realization:

\[
 \frac{\|u(t)\|_3}{\|u(0)\|_3}
 \leq C_{\mathbb T^2}\left(\frac{K_+}{\kappa_0}\right)^{1/3}.
                                                               \tag{216.1}
\]

Here `kappa_0` is the smallest nonzero frequency, the initial Fourier support
lies in `|k|<=K_+`, and the `L^p` norms use normalized Haar measure. The
dimensionless constant `C_T` is the constant in (216.6) after rescaling the
torus so its spectral gap is one. Thus a factor above two is rigorously
impossible whenever the right side of (216.1) is at most two. More generally,
no finite sequential high-to-low cascade from a fixed launch annulus can have
unbounded amplification.

This is not a universal factor-two theorem. If the launch frequency is allowed
to grow, (216.1) grows like `K_+^(1/3)`. Conservation therefore obstructs
unbounded gain at fixed launch scale but does not rule out one carefully coupled
orbit crossing two.

## Conservation interpolation theorem

Let `u` be a smooth, mean-zero solution of two-dimensional incompressible Euler
on a fixed flat torus, and put

\[
 E=\|u(t)\|_2^2,\qquad Z=\|\omega(t)\|_2^2,
 \qquad \omega=\partial_1u_2-\partial_2u_1.             \tag{216.2}
\]

Both `E` and `Z` are independent of time. There is a torus-dependent constant
`C_T` such that every time slice satisfies

\[
 \|u(t)\|_3\leq C_T\kappa_0^{-1/3}E^{1/3}Z^{1/6}.     \tag{216.3}
\]

Indeed, Sobolev and Biot--Savart give

\[
 \|u\|_6\leq C_T\|\nabla u\|_2=C_T\|\omega\|_2,
                                                               \tag{216.4}
\]

where the equality follows by Fourier expansion for a divergence-free,
mean-zero field. Interpolation between `L^2` and `L^6` then yields

\[
 \|u\|_3\leq\|u\|_2^{1/2}\|u\|_6^{1/2}
 \leq C_T E^{1/4}Z^{1/4}.                              \tag{216.5}
\]

A sharper exponent follows from the two-dimensional
Gagliardo--Nirenberg inequality applied componentwise,

\[
 \|u\|_3\leq C_T\kappa_0^{-1/3}
                 \|u\|_2^{2/3}\|\nabla u\|_2^{1/3}
 =C_T\kappa_0^{-1/3}E^{1/3}Z^{1/6},                    \tag{216.6}
\]

which proves (216.3). Since normalized Haar measure is a probability measure,
`||u(0)||_3>=||u(0)||_2=E^(1/2)`. Therefore

\[
 \boxed{\displaystyle
 \frac{\|u(t)\|_3}{\|u(0)\|_3}
 \leq C_T\left(\frac{Z}{\kappa_0^2E}\right)^{1/6}.}  \tag{216.7}
\]

The invariant inside the sixth root is the dimensionless squared rms wave
number. It is finite for every fixed smooth orbit and is completely insensitive
to how a finite triad network orders its transfers.

## Annular launch and packet leakage

Suppose first that

\[
 \operatorname{supp}\widehat u(0)\subset
 \{k:K_-\leq |k|\leq K_+\}.                            \tag{216.8}
\]

Parseval gives

\[
 K_-^2E\leq Z\leq K_+^2E.                              \tag{216.9}
\]

Substitution in (216.7) proves (216.1). Notice that the lower launch edge
`K_-` is irrelevant to the upper bound; only the largest initially occupied
frequency can fund enstrophy.

The exact-support assumption has a stable replacement. Let `P_>` project onto
`|k|>K_+`, and assume only

\[
 \|\nabla P_>u(0)\|_2^2\leq L E.                      \tag{216.10}
\]

The complementary modes contribute at most `K_+^2E`, so

\[
 Z\leq(K_+^2+L)E,
 \qquad
 \frac{\|u(t)\|_3}{\|u(0)\|_3}
 \leq C_T\left(\frac{K_+^2+L}{\kappa_0^2}\right)^{1/6}.
                                                               \tag{216.11}
\]

Thus small packet leakage measured in enstrophy, rather than merely in energy,
preserves the obstruction. Small high-frequency energy alone is insufficient:
an arbitrarily small energy tail can carry arbitrarily large enstrophy and make
(216.11) vacuous.

## Geometry of a sequential high-to-low transfer

Conservation quantitatively restricts simultaneous low- and high-frequency
packets. Fix `0<L<H` and write

\[
 E_{\leq L}=\sum_{0<|k|\leq L}|\widehat u_k|^2,
 \qquad
 E_{\geq H}=\sum_{|k|\geq H}|\widehat u_k|^2.          \tag{216.12}
\]

Since the intermediate band has `|k|^2>=L^2`,

\[
 Z\geq L^2(E-E_{\leq L})+(H^2-L^2)E_{\geq H}.         \tag{216.13}
\]

Consequently

\[
 E_{\leq L}
 \geq E-\frac Z{L^2}
      +\left(\frac{H^2}{L^2}-1\right)E_{\geq H},       \tag{216.14}
\]

or, equivalently,

\[
 E_{\geq H}
 \leq\frac{Z-L^2(E-E_{\leq L})}{H^2-L^2}.             \tag{216.15}
\]

These inequalities are an exact shell budget: once the low-frequency energy is
specified, they cap the energy that can lie beyond `H`. They do not by
themselves lower-bound the high packet, because arbitrarily small energy at
arbitrarily large frequency may carry fixed enstrophy. Any stronger claimed
leakage lower bound therefore needs an upper support cap or another moment.
Packet separation alone supplies neither.

At the level of one isolated Euler triad `k+p+q=0`, the quadratic interaction
conserves the triad energy and enstrophy. If `|k|<|p|<|q|` and `delta E_j`
denotes a triad energy increment, then

\[
 \delta E_k+\delta E_p+\delta E_q=0,
 \qquad
 |k|^2\delta E_k+|p|^2\delta E_p+|q|^2\delta E_q=0,    \tag{216.16}
\]

and hence

\[
 \delta E_q
 =\frac{|p|^2-|k|^2}{|q|^2-|p|^2}\,\delta E_k,
 \qquad
 \delta E_p=-(\delta E_k+\delta E_q).                 \tag{216.17}
\]

Thus, in an isolated triad, energy delivered to the lowest leg is accompanied
by energy on the highest leg and is paid for by the middle leg. In an
overlapping triad network this stagewise statement need not survive because a
mode can participate in several transfers; only the global `E,Z` budget is
automatic. The invariant estimate (216.7) already includes all overlaps,
mirror modes, simultaneous triads, and phase choices, so Hamiltonian or triad
geometry cannot evade that bound.

## A packetwise variant

If the endpoint packets are spatially disjoint, or asymptotically disjoint with
vanishing endpoint error, the Cycle 213 cubic-additivity argument remains
available. Let `u=sum_j u_j` at both endpoints, with exact disjointness, and
suppose packet `j` launches below frequency `K_{j,+}` with energy `E_j` and
enstrophy `Z_j`. Then

\[
 \|u(t)\|_3^3=\sum_j\|u_j(t)\|_3^3
 \leq C_T^3\kappa_0^{-1}\sum_j E_j Z_j^{1/2}.         \tag{216.18}
\]

In particular, if each packet is itself an exact Euler subsystem and
`Z_j<=K_{j,+}^2E_j`, its gain is bounded by
`C_T(K_{j,+}/kappa_0)^(1/3)` and endpoint aggregation cannot exceed the largest
packet gain. For a genuinely sequential
cascade, however, packets interact strongly and their individual energies and
enstrophies are not conserved. One must then use the global bound (216.7), not
assign fictitious invariant budgets to the stages.

## Sharp logical boundary

The following no-go is rigorous.

> Fix a torus, a launch cap `K_+`, and an enstrophy-leakage cap `L`. No smooth
> mean-zero 2D Euler solution satisfying (216.10) can achieve endpoint `L^3`
> amplification larger than
> `C_T((K_+^2+L)/kappa_0^2)^(1/6)`, regardless of the finite
> sequential triad cascade proposed to produce it. In particular, if this
> constant is at most two, amplification above two is impossible in that class.

The following stronger statements do not follow.

1. There is no torus-independent or launch-scale-independent constant two in
   (216.7).
2. Taking `K_+` arbitrarily large leaves room for ratios above two; the estimate
   then weakens rather than closes.
3. Energy/enstrophy conservation does not control `L^3` by energy alone. Smooth
   fields with fixed energy and increasing enstrophy can have increasing
   concentration bounds.
4. Packet separation only yields the sharper aggregation no-go when endpoint
   additivity is proved. A sequential cascade deliberately violates nonlinear
   decoupling.
5. The estimate proves no universal Euler factor-two bound, no Navier--Stokes
   factor-two bound, and no Millennium result.

The hostile conclusion is therefore bounded but decisive: a fixed-band finite
inverse-cascade architecture cannot amplify `L^3` without limit, and any claimed
factor-two crossing must explicitly beat the computable invariant threshold in
(216.11). To escape, the construction must inject an increasingly high initial
enstrophy-to-energy ratio or exploit a non-separated coupled orbit; merely
adding stages or widening packet gaps cannot do so.
