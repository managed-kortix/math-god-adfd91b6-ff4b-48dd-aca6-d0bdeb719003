# Cycle 130: formal closure and the convergence wall

Infinite recursive completion has an exact coefficientwise closure theorem, but
it does not presently define an analytic Fourier field.  Exact computation
through depth eight shows rapidly accelerating norms consistent with
factorial-scale growth; no asymptotic divergence theorem is claimed.

For the Cycle 129 recursion

\[
Q_m=\sum_{a+b=m}B(V_a,V_b),\qquad
V_{m+1}=\mathbf1_{S_m^c}Q_m,
\]

let

\[
S_\infty=\bigcup_{m\ge0}S_m.
\]

Then, unconditionally, for every `m`,

\[
\operatorname{supp}Q_m\subseteq S_\infty.
\]

Indeed, if `n` is outside `S_infty`, then it is outside `S_m` and outside the
support of `V_(m+1)`.  By definition,

\[
0=V_{m+1}(n)=Q_m(n).
\]

Thus the formal series

\[
\widehat U(\epsilon)=\sum_{j\ge0}\epsilon^jV_j
\]

satisfies the coefficientwise identity

\[
\mathbf1_{S_\infty^c}B(\widehat U,\widehat U)=0.
\]

This closes the graded sums `Q_m`; it need not close every individual
`B(V_a,V_b)`, because exterior terms can cancel at a fixed total degree.

The conclusion passes to an actual field only if the series converges in a
space where the Euler bilinear map is continuous and the Cauchy products
converge to `B(U,U)`.  Convergence merely in the critical `H^(1/2)` norm would
not suffice for this nonlinear interchange.

Exact rational computation gives generation sizes

```text
6, 4, 14, 24, 28, 34, 40, 46, 52
```

through depth eight, cumulative support size `248`, and approximate weighted
norms

```text
4.060, 4.436, 15.384, 44.550, 128.769,
581.354, 3555.685, 25653.252, 210486.410.
```

The successive late ratios are approximately `4.51, 6.12, 7.21, 8.21`, while
the factorial-normalized norms stabilize near `5`.  This is evidence consistent
with Gevrey-1 growth, not a proof of zero convergence radius.  The basic
convolution majorant loses one derivative and naturally permits factorial
growth; it does not prove a matching lower bound for the actual coefficients.

The recursion also discards large internal coefficients
`1_(S_j) Q_j`.  Hence it is not a Picard, Duhamel, or fixed-point expansion for
Euler or Navier--Stokes.  It closes support order by order without correcting
higher-order amplitudes on modes already present.

Recursive completion is therefore retired as a standalone regularity funnel.
If the series diverges, it defines no field.  If it converges strongly enough,
the complement leakage is zero by construction while all hard dynamics remain
inside `S_infty`.  A revival requires an all-depth convergence theorem, a
closed coefficient formula, an internal coercive estimate, or an actual
time-dependent Navier--Stokes recurrence.

Reproduce the finite-depth evidence with

```sh
python3 millennium-prize/navier-stokes/verify_cycle130_formal_completion_growth.py
```

No Navier--Stokes or Millennium solution is claimed.
