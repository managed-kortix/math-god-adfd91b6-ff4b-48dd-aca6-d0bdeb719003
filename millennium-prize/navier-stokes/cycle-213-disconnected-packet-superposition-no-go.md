# Cycle 213: disconnected packet superposition versus the factor-two gate

## Verdict

Genuine nonlinear decoupling cannot turn many subcritical transient-growth
packets into a factor-two counterexample. At the two endpoint times, the cube
of the `L^3` norm is additive for disjoint packets. More generally, asymptotic
endpoint additivity makes the aggregate amplification the cubic weighted mean
of the packet amplifications. It is bounded by the best packet ratio, up to the
decoupling error.

This is a no-go for the proposed amplification mechanism, not a proof of the
universal factor-two lemma. Frequency separation alone is not endpoint
additivity and does not nonlinearly decouple Navier--Stokes at critical `L^3`.
A construction using cancellation, packet collision, or a sequential cascade
would leave the hypotheses of the no-go and remains logically possible, but it
would require strong cross-packet interaction rather than decoupling.

## Endpoint aggregation lemma

Let `v_1,...,v_N` be nonzero packet trajectories on a common interval `[0,T]`.
Write

\[
 a_j=\|v_j(0)\|_3,\qquad b_j=\|v_j(T)\|_3,
 \qquad A=\left(\sum_j a_j^3\right)^{1/3}.
\]

Suppose an exact solution `u` and the packet sum `V=sum_j v_j` obey

\[
 \left|\|V(s)\|_3^3-\sum_j\|v_j(s)\|_3^3\right|
 \leq \delta_s A^3,\qquad s=0,T,                       \tag{213.1}
\]

and

\[
 \|u(s)-V(s)\|_3\leq\varepsilon_s A,
 \qquad s=0,T.                                         \tag{213.2}
\]

If `b_j<=R a_j` for every `j`, then the triangle inequality and (213.1) give

\[
 \frac{\|u(T)\|_3}{\|u(0)\|_3}
 \leq
 \frac{(R^3+\delta_T)^{1/3}+\varepsilon_T}
      {(1-\delta_0)^{1/3}-\varepsilon_0},              \tag{213.3}
\]

provided the denominator is positive. In the exact disjoint and exact-sum
case this reduces to

\[
 \left(\frac{\|u(T)\|_3}{\|u(0)\|_3}\right)^3
 =\frac{\sum_j a_j^3(b_j/a_j)^3}{\sum_j a_j^3}
 \leq \max_j(b_j/a_j)^3.                               \tag{213.4}
\]

Thus adding any number of packets with individual ratio at most two cannot
produce a ratio above two. If the errors tend to zero in a many-packet or
scale-separation limit, (213.3) rules out a crossing by any fixed margin. The
argument is independent of how large `N` is and whether the individual peaks
have been synchronized.

The same calculation applies to spatially separated copies, scale-separated
localized bubbles whose endpoint `L^3` masses decouple, and profiles separated
by translations in a decompactification limit. It also shows that replication
of one known transient-growth packet merely reproduces its ratio.

## Compatibility with endpoint mild-solution theory

For three-dimensional data in `L^3`, Kato's mild theory gives local existence,
uniqueness, and continuous dependence for each fixed datum. It does not give a
lifespan uniform on an `L^3` ball. A standard endpoint construction supplements
`L^3` by, for some `q>3`,

\[
 \sup_{0<t<T}t^{(1-3/q)/2}\|u(t)\|_q.
\]

The corresponding heat profile tends to zero as `T` tends to zero for each
fixed datum, but not uniformly over a critical `L^3` ball. Critical
concentration can preserve the norm while driving the required time to zero.
Consequently endpoint theory has exactly the following implications here.

1. A finite packet sum can be promoted from an approximate solution to an
   exact one if its Kato norm is controlled and the full cross-interaction
   residual is small in the matching forcing norm.
2. The perturbation theorem then supplies (213.2), so it preserves rather than
   defeats the aggregation no-go.
3. It gives no scale-uniform theorem saying that an arbitrarily large packet
   family decouples. The stability constants depend on the aggregate critical
   profile, and the endpoint bilinear kernel cannot be bounded using only
   `L^infinity_t L^3_x`.

The endpoint continuation theorem is consistent with this conclusion. A
uniform bound in `L^infinity_t L^3_x` prevents a finite-time singularity, so a
universal factor-two estimate would imply global continuation. The theorem's
converse supplies no numerical multiplier and does not constrain finite-time
transient amplification along a regular solution.

For an approximate sum `V=sum_j v_j`, even when each `v_j` solves
Navier--Stokes separately, its residual contains

\[
 {\cal R}={\mathbb P}\nabla\mathbin\cdot
 \sum_{i\ne j}v_i\otimes v_j.                          \tag{213.5}
\]

Smallness of (213.5), not merely disjoint Fourier support at time zero, is the
nonlinear decoupling gate.

## Why disconnected scales do not provide a loophole for free

Dyadic Fourier separation gives the Littlewood--Paley equivalence

\[
 \left\|\sum_j f_j\right\|_3
 \asymp
 \left\|\left(\sum_j|f_j|^2\right)^{1/2}\right\|_3,   \tag{213.6}
\]

with constants independent of the number of scales. This is neither cubic
additivity nor a sharp constant-one identity. It therefore cannot prove the
factor-two bound. Conversely, it does not produce a counterexample: the full
heat semigroup is an `L^3` contraction, and nonlinear high--low and high--high
terms remain in (213.5). At the critical scaling, a low--high paraproduct is not
automatically small merely because the frequency ratio is large.

There are only three ways for superposition to beat (213.4).

1. **Initial cancellation.** Arrange a packet sum whose initial norm is much
   smaller than its component mass and later undo the cancellation. Then
   (213.1) fails at time zero. Frequency separation controls this only up to
   Littlewood--Paley constants; no Navier--Stokes phase-unwinding construction
   is supplied by that fact.
2. **Final collision or concentration.** Initially separated packets may be
   transported into a common region so that their final fields reinforce.
   Endpoint additivity then fails at time `T`, and the cross terms become large
   precisely near the proposed amplification event.
3. **Sequential nonlinear transfer.** An earlier packet can seed a later scale
   so that gains compose rather than average. This makes (213.5) the main term,
   not an error. It is a coupled cascade and must be analyzed as one solution,
   not as a decoupled packet superposition.

Scale synchronization is an additional practical obstruction. A critically
rescaled localized packet evolves on its own parabolic time scale. Geometrically
separated scales therefore reach copies of the same transient-growth event at
different physical times unless the profiles are separately tuned. Even if all
peaks are tuned to a common time, (213.4) still bounds the aggregate by the best
peak.

## Consequence for the hostile test

Known endpoint `L^3` mild theory neither proves the universal factor two nor
supports amplification by arbitrarily many decoupled packets. The rigorous
conclusion is narrower and decisive:

\[
 \boxed{\text{decoupled packet gains average in }L^3\text{; they do not
 multiply or add.}}
\]

Accordingly, a many-packet campaign is useful only if it deliberately searches
for failure of endpoint additivity through cancellation, collision, or a
coupled inverse cascade. Such a hit must certify the full cross-scale residual
and the exact solution. If every packet remains nonlinearly decoupled and no
single packet crosses two, increasing the number of packets cannot refute the
lemma.

No universal factor-two estimate, factor-two crossing, or Navier--Stokes
regularity result is claimed.
