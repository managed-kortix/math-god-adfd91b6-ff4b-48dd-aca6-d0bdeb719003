# Cycle 258: velocity-L3 two-jet and analytic-Wiener persistence audit

## Verdict

Let `u` be a smooth, nonzero, mean-zero two-dimensional Euler solution on the
normalized-Haar square torus, put

\[
 F=\int |u|^3,\qquad N=\int |u|u\cdot u_t,\qquad
 \ell=\log\|u\|_3.
\]

Then

\[
 \boxed{\ell''={1\over F}\int\left[
 |u||u_t|^2+{(u\cdot u_t)^2\over |u|}+|u|u\cdot u_{tt}
 \right]-3\left({N\over F}\right)^2.}                 \tag{258.1}
\]

The quotient is assigned its continuous value zero at `u=0`. If
`omega=curl u`, `u=K omega`, and

\[
 f=-u\cdot\nabla\omega,\qquad b=Kf=u_t,
\]

then the exact second Euler jet is

\[
 \omega_{tt}=-b\cdot\nabla\omega-u\cdot\nabla f,
 \qquad u_{tt}=K\omega_{tt}.                           \tag{258.2}
\]

Thus (258.1)--(258.2) are directly interval-evaluable from one initial datum;
they require no time integration.

There is also a simple explicit persistence bound. Define the unweighted
Wiener seminorms

\[
 a_j(t)=\sum_{k\ne0}|k|_1^j|\widehat\omega_k(t)|,
 \qquad j=0,1,2.
\]

Also set `m=||u||_2`, which is positive and conserved by Euler. With
normalized Haar measure and the Cycle 257 convention for `K`,

\[
 |\ell''(t)|\le L(t):=
 {5[a_0(t)a_1(t)]^2\over m^2}
 +{a_0(t)a_1(t)^2+a_0(t)^2[a_1(t)+a_2(t)]\over m}.     \tag{258.3}
\]

Consequently `ell'` is Lipschitz on every interval on which the right side is
bounded. This estimate is deliberately elementary and non-sharp, but all its
constants are explicit.

## Exact differentiation

The map `Phi(z)=|z|z` is continuously differentiable, with

\[
 D\Phi(z)h=|z|h+{z\cdot h\over|z|}z
\]

and continuous value zero at `z=0`. Since `F'=3N`, differentiation gives

\[
 N'=\int\left[|u||u_t|^2+{(u\cdot u_t)^2\over|u|}
                  +|u|u\cdot u_{tt}\right].           \tag{258.4}
\]

As `ell'=N/F`, equations (258.1) and (258.4) follow. Differentiating
`omega_t=-u dot grad omega` proves (258.2). Equivalently,

\[
 u_t=-\mathbb P(u\cdot\nabla u),
 \qquad
 u_{tt}=-\mathbb P(u_t\cdot\nabla u+u\cdot\nabla u_t), \tag{258.5}
\]

where `P` is the Leray projector.

## Wiener proof of the Lipschitz constant

Write `||g||_A=sum_k |g_hat_k|`, componentwise for vectors, and use the
corresponding `A^1` norm with multiplier `|k|_1`. The Fourier symbols give

\[
 \|u\|_A\le a_0,
 \quad \|\nabla u\|_A\le a_0,
 \quad \|\nabla\omega\|_A=a_1,
 \quad \|\nabla^2\omega\|_A\le a_2.                  \tag{258.6}
\]

The Wiener algebra property and `|k|_2^{-1}<=1` for nonzero integer modes give

\[
 \|u_t\|_A\le\|u\cdot\nabla\omega\|_A\le a_0a_1.     \tag{258.7}
\]

From `f=-u dot grad omega`,

\[
 \|f\|_A\le a_0a_1,
 \qquad
 \|\nabla f\|_A\le a_0a_1+a_0a_2.                    \tag{258.8}
\]

Equations (258.2), (258.7), and (258.8) imply

\[
 \|u_{tt}\|_A
 \le a_0a_1^2+a_0^2(a_1+a_2).                         \tag{258.9}
\]

Since `||g||_infinity<=||g||_A`, normalized Haar measure gives
`F>=||u||_2^3`. Parseval gives `||u||_2=||omega||_{H^{-1}}`. More usefully,
the first two terms of (258.4) are at most
`2 ||u||_3 ||u_t||_3^2`, while the last is at most
`||u||_3^2 ||u_tt||_3`. Therefore

\[
 {|N'|\over F}
 \le2{\|u_t\|_3^2\over\|u\|_3^2}
       +{\|u_{tt}\|_3\over\|u\|_3}
 \le{2(a_0a_1)^2\over m^2}
       +{a_0a_1^2+a_0^2(a_1+a_2)\over m}.             \tag{258.10}
\]

Also `|ell'|<=||u_t||_3/||u||_3<=a_0a_1/m`, so the final term in
(258.1) is at most `3(a_0a_1/m)^2`. This proves (258.3).

For a shrinking analytic enclosure

\[
 A_{q(t)}(\omega(t))\le M,\qquad q(t)>1,
\]

put `kappa_j(q)=max_(n>=1) n^j/q^n`. Then

\[
 a_0\le M,\qquad a_j\le M\kappa_j(q(t)),
\]

and hence

\[
 \boxed{L(t)\le
 {5M^4\kappa_1(q(t))^2\over m^2}
 +{M^3[\kappa_1(q(t))^2+\kappa_1(q(t))+\kappa_2(q(t))]\over m}.} \tag{258.11}
\]

This is the requested analytic-Wiener Lipschitz bound for `ell'`.

## What a positive initial derivative certifies

Suppose interval arithmetic proves `ell'(0)>=c>0` and `L(t)<=L` on `[0,T]`.
Then

\[
 \ell'(t)\ge c-Lt,
 \qquad
 \ell(t)-\ell(0)\ge ct-{L\over2}t^2.                  \tag{258.12}
\]

Thus the best lower bound available before the derivative may change sign is

\[
 \sup_{t\ge0}\left(ct-{L\over2}t^2\right)
 ={c^2\over2L},                                       \tag{258.13}
\]

provided `c/L<=T`; otherwise use `cT-LT^2/2`. A factor two requires

\[
 L\le {c^2\over2\log2}                                \tag{258.14}
\]

and enough analytic lifespan to reach the smaller root of
`ct-Lt^2/2=log 2`.

## Cycle 257 candidate audit

For the `rho=20` candidate in
`cycle257-initial-l3-candidates.json`, the doubled-grid floating value is

\[
 c_{\rm float}=0.30527111116241978.
\]

Interpreting its listed cosine/sine streamfunction coefficients exactly as in
the optimizer gives the floating diagnostic Wiener sums

\[
 a_0=38.0804420881,\qquad
 a_1=247.8575280913,\qquad
 a_2=1822.5559289531.                                  \tag{258.15}
\]

These are not interval-certified because the candidate coefficients are not
exact data. Substitution in (258.3) gives

\[
 L_{\rm diag}\approx4.5092\,10^8,
 \qquad {c_{\rm float}^2\over2L_{\rm diag}}
 \approx1.03\,10^{-10}.                               \tag{258.16}
\]

By contrast, (258.14) would require

\[
 L\le0.06722270098.                                   \tag{258.17}
\]

The bound is therefore too large by about `6.7*10^9` even before accounting
for interval margins. The positivity guarantee for `ell'` lasts only about
`c/L=6.77*10^-10`, whereas constant-rate accumulation of `log 2` would take
about `2.27`.

The Cycle 255 shrinking-radius enclosure is no rescue for this candidate.
Its initial finite-support analytic norm is

\[
 M(q_0)=\sum_{k\ne0}q_0^{|k|_1}|\widehat\omega_k|.
\]

Under the required choice `alpha>=M(q0)`, the available interval satisfies
`T<(1-1/q0)/M(q0)`. A floating one-dimensional optimization gives a largest
such lifespan of only about `1.31*10^-3`, near `q0=1.139`, while (258.11)
becomes still worse as the terminal radius approaches one.

Hence the Cycle 257 constants cannot possibly certify `log 2` through this
global analytic-Wiener Lipschitz argument. This rejects the bound as a
persistence mechanism for the recorded candidate, not the candidate orbit:
the exact value of `ell''(0)` and a short rigorous orbit enclosure could be far
smaller than the global Wiener majorant.
