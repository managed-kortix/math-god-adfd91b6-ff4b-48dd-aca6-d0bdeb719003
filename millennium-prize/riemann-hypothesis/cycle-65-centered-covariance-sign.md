# Cycle 65: centered covariance sign and route correction

## Exact endpoint-safe identity

For even `N>=4`, set `n=N/2`, `m=N-1`,

\[
E_k=\psi(k)-k,
\]

\[
F_k=\psi(2k)+{k\over2k+1}\Lambda(2k+1)-2k,
\qquad \rho_N={\log(2N)\over\log N}.
\]

Define

\[
A_N=\sum_{k=n}^m{E_k^2\over k(k+1)},\qquad
C_N=\sum_{k=n}^m{E_kF_k\over k(k+1)},
\]

and

\[
\boxed{T_N=C_N-\rho_NA_N.}                         \tag{65.1}
\]

Writing `H_k=F_k-rho_N E_k`, finite Abel summation gives

\[
\boxed{
T_N={E_nH_n\over n}-{E_mH_m\over m+1}
+\sum_{k=n+1}^m{E_kH_k-E_{k-1}H_{k-1}\over k}.}    \tag{65.2}
\]

The increment of `F` is

\[
\begin{aligned}
f_k={}&(\Lambda(2k-1)-1)+(\Lambda(2k)-1)\\
&+{k\over2k+1}\Lambda(2k+1)
-{k-1\over2k-1}\Lambda(2k-1),
\end{aligned}
\]

so every interior packet retains the odd endpoint and cross-window information
together:

\[
E_kH_k-E_{k-1}H_{k-1}
=(\Lambda(k)-1)H_{k-1}+E_k(f_k-\rho_N(\Lambda(k)-1)).             \tag{65.3}
\]

There is no generic endpoint cancellation.

## Indefinite square decomposition

Completing the square yields

\[
\boxed{
T_N={1\over4\rho_N}\sum_{k=n}^m{F_k^2\over k(k+1)}
-\rho_N\sum_{k=n}^m
{(E_k-F_k/(2\rho_N))^2\over k(k+1)}.}              \tag{65.4}
\]

Thus the covariance is intrinsically indefinite. Its sign is an arithmetic
alignment statement, not a consequence of positive squares.

## Certified finite sign

`verify_cycle65_centered_covariance.py` computes `A_N,C_N,T_N` with exact
rational weights and Arb values, and independently checks both Abel and square
identities. It certifies:

| `N` | `A_N` | `C_N` | `T_N` |
|---:|---:|---:|---:|
| 4 | `0.406297814` | `0.297686110` | `-0.311760611` |
| 64 | `0.0575420792` | `-0.00228709252` | `-0.0694195183` |
| 220 | `0.0353687701` | `-0.00368615445` | `-0.0436002445` |
| 8192 | `0.0238572362` | `-0.0106453498` | `-0.0363377581` |

A broader 128-bit Arb scan certifies `T_N<0` at every dyadic scale through
`2^21`. The cross-window rectangle is eventually the dominant component; at
`2^21` it supplies about `96.7%` of the covariance magnitude. The positive odd
prime-power diagonal does not dominate it.

Abstract bounded-increment models satisfying PNT-quality summatory control can
realize either sign, and can make the odd diagonal zero while `T_N` remains
nonzero. Therefore positivity, near-diagonal dominance, PNT, and absolute use of
pointwise RH-scale errors cannot prove the needed signed estimate.

## Explicit-formula form

At one symmetric zero cutoff, the Hermitian zero block has kernel

\[
\mathcal K_{\rho\sigma}^{C,N}
={S_N(\bar\rho+\sigma)\over\bar\rho\sigma}
\left[-{1\over\log^2N}
+{2^{\bar\rho}+2^\sigma\over2\log N\log(2N)}\right].             \tag{65.5}
\]

Its diagonal already has a dyadic ordinate phase and no fixed sign. Known pair
correlation and standard large-sieve estimates omit the required finite Mellin
weights, affine row, odd endpoint, or cancellation-scale error. They do not
currently imply a useful one-sided bound.

## Strategic correction

In the exact shell decrement, this centered covariance enters with the opposite
sign. Hence observed negative `T_N` is favorable; it does not kill the renewal
route. What is decisively falsified is the attempted lower-alignment theorem
`T_N>=0` and every proof that replaces `T_N` by its absolute value.

The next exact target must be window-adaptive. For each `1<=r<=12`, derive

\[
S_M(r)=\sum_{n=M}^{M+r-1}\beta_nH_n
=R_{M,r}-\kappa_{M,r}T_{M,r},\qquad \kappa_{M,r}>0,               \tag{65.6}
\]

with all boundary and odd-endpoint packets retained, then prove

\[
\max_{1\le r\le12}S_M(r)\ge0.
\]

This changes the direction of attack from a lower bound on covariance to a
joint upper-threshold theorem for at least one adaptive endpoint. No additive-
12 theorem or RH result is claimed.
