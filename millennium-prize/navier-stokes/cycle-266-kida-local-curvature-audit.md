# Cycle 266: local curvature audit for the directed Kida datum

This note concerns only the time jet at

\[
 u_*=K-{1\over32}F(K),\qquad F(u)=-\mathbb P((u\cdot\nabla)u).
\]

It makes no trajectory, persistence, or amplification claim.

## Exact second derivative

Put `a=F(u)` and `b=DF(u)a`, where

\[
 DF(u)h=-\mathbb P((h\cdot\nabla)u+(u\cdot\nabla)h).
\]

For `C(t)=int |u(t)|^3` and `L(t)=log ||u(t)||_3=(1/3)log C(t)`, direct
differentiation gives

\[
 C''(0)=3\int\left
 \{(u\cdot a)^2\over |u|}+|u||a|^2+|u|u\cdot b\right),                 \tag{266.13}
\]

with the quotient assigned its continuous value zero at `u=0`, and

\[
 \boxed{L''(0)={C''(0)\over3C(0)}-{C'(0)^2\over3C(0)^2}}.             \tag{266.14}
\]

These are exact Euler time derivatives. The fields `u`, `a`, and `b` are
finite Fourier polynomials with Gaussian-rational coefficients; only the
displayed integrals involving Euclidean magnitude require cubature.

The independent grids `64,96,128` give, respectively,

| grid | `C` | `C'` | `C''` | `L'` | `L''` |
|---:|---:|---:|---:|---:|---:|
| 64 | 0.9051492780 | 0.0356600016 | -1.1318037614 | 0.0131322727 | -0.4173192495 |
| 96 | 0.9051474833 | 0.0356443375 | -1.1317220837 | 0.0131265303 | -0.4172895445 |
| 128 | 0.9051473044 | 0.0356418018 | -1.1317415115 | 0.0131255991 | -0.4172967081 |

Thus the finite-cubature signal is not merely concave: its curvature scale is
about 32 times its initial positive slope.

## Rigorous Taylor interface

Let outward cubature and coefficient arithmetic provide

\[
 C_0\in[c_-,c_+],\quad C'_0\in[g_-,g_+],\quad C''_0\in[h_-,h_+],
 \qquad c_->0.
\]

Interval evaluation of (266.14) provides `ell_1` and `ell_2` enclosing `L'(0)`
and `L''(0)`. If an analytic Euler existence enclosure on `0<=t<=tau` gives
`|L'''(t)|<=M_3` almost everywhere (equivalently, `L''` is Lipschitz with
constant `M_3`), Taylor's theorem yields the local lower bound

\[
 \boxed{L(t)-L(0)\ge \ell_1^-t+{1\over2}\ell_2^-t^2-{M_3\over6}t^3}
 \quad(0\le t\le\tau).                                                   \tag{266.15}
\]

It also proves continued positive growth only while

\[
 \ell_1^-+\min(\ell_2^-,0)t-{M_3\over2}t^2>0.                            \tag{266.16}
\]

A convenient analytic-norm remainder follows from `phi(v)=|v|^3`, whose second
derivative is Lipschitz even at `v=0`. If a
validated slab bounds, pointwise, `|u|<=U`, `|u_t|<=A`, `|u_tt|<=B`, and
`|u_ttt|<=D`, then the bounded third differential of `phi` gives

\[
 |C'''(t)|\le12A^3+18UAB+3U^2D.                                          \tag{266.17}
\]

The corresponding `M_3` is obtained exactly from

\[
 L'''={C'''\over3C}-{C'C''\over C^2}+{2(C')^3\over3C^3},                 \tag{266.18}
\]

using a positive slab lower bound for `C`. Fourier Wiener norms bound the four
pointwise quantities in (266.17), including the complete analytic tail. This
is the required interface: endpoint jets alone cannot supply `M_3`.

## What the present finite bounds prove

For auditability, the replay also computes a deliberately crude analytic
periodic rectangle-rule remainder. For an `N^3` grid it uses the rigorous
inequality

\[
 |\langle f\rangle-Q_Nf|\le {\pi\over N}\sum_{j=1}^3
 \|\partial_jf\|_\infty,
\]

and bounds every sup norm by the finite Fourier `l1` norm. At `N=128` the
floating replay gives candidate radii `(33.58,219.60,2463.86)` for
`(C,C',C'')`. Even after outward rounding these are far too wide to retain
`C>0`, much less certify the signs of `L'` and `L''`. The script does not claim
directed interval arithmetic. A useful rigorous interval requires exact or
outward-rounded Fourier coefficients and cellwise interval cubature
(exploiting local ranges and symmetry), followed by the analytic slab/tail
remainder (266.17)--(266.18).

The converged cubature values give a clear diagnostic. The quadratic jet turns
at

\[
 t_{quad}=-L'(0)/L''(0)\simeq0.03145
\]

and predicts a maximum logarithmic gain only

\[
 -{L'(0)^2\over2L''(0)}\simeq2.06\,10^{-4},
\]

or about `0.0206%` in the velocity `L3` norm. Therefore positive growth appears
to turn quickly and is not meaningful for factor-scale amplification. The
current global analytic/cubature remainder is vacuous, so even that short
persistence is a numerical local-jet conclusion, not a certified trajectory
statement.
