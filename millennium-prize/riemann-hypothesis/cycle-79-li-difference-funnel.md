# Cycle 79: Li first-difference funnel

Define the classical Li coefficients by

\[
\log\xi\left({1\over1-z}\right)-\log\xi(1)
=\sum_{n\ge1}{\lambda_n\over n}z^n,
\qquad D_n=\lambda_{n+1}-\lambda_n.
\]

The conjecture

\[
D_n>0\quad(n\ge1)
\]

is strictly stronger than Li positivity, but it is unconditional in statement
and has full reach: since `lambda_1>0`, it implies every Li coefficient is
positive and hence RH. Functional equation and critical-line location alone do
not imply monotonicity; a single symmetric critical-line zero pair gives signed
oscillating differences.

An exact arithmetic decomposition is

\[
D_n=A_n+P_n,
\]

where

\[
A_n=-{\log(4\pi)+\gamma\over2}
+\sum_{k=2}^{n+1}\binom n{k-1}(-1)^k(1-2^{-k})\zeta(k)
\]

and the prime term has the grouped Abel regularization

\[
P_n=\lim_{\epsilon\downarrow0}\left[
{1\over\epsilon}\left(1-{1\over\epsilon}\right)^n
-\sum_{m\ge2}{\Lambda(m)\over m^{1+\epsilon}}L_n(\log m)
\right].
\]

Equivalently, with `R(x)=psi(x)-x`, one obtains an absolutely convergent
fixed-`n` integral after an effective PNT estimate:

\[
P_n=-1-\int_1^\infty {R(x)\over x^2}
[L_n(\log x)-L_n'(\log x)]\,dx.
\]

The Laguerre kernel changes sign and grows exponentially across its oscillatory
range. Pointwise PNT remainders control only an astronomically remote tail and
do not provide the signed transform cancellation. This is the precise analytic
bottleneck.

`verify_cycle79_li_differences.py` provides outward-rounded finite
certification. With python-flint `0.9.0` at 256 bits it certifies
`D_n>0` for `1<=n<=100`; the weakest certified ball is at `n=1`,
`[0.0692500262619256 +/- 4.02e-17]`. Finite verification is reconnaissance only; the full target is
a uniform one-sided bound on the signed prime transform. No RH result is
claimed.
