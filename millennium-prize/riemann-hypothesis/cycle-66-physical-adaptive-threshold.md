# Cycle 66: the physical adaptive threshold

## Exact endpoint identity

Fix `M>=3`, `1<=r<=12`, and `B=M+r`. Put

\[
A_{M,r}=\sum_{n=M}^{B-1}\beta_n,
\qquad
Z_{M,r}=\operatorname{span}\{U_{M-1},\rho_M,\ldots,\rho_{B-1}\}.
\]

Let `D=D_(M-1)`, let `bar T_(M,r)` be the `beta`-weighted mean of the new
`D` increments, and let `V_(D,M,r)` and `N_(U,M,r)` be the exact Cycle 52
new-row variance and weighted `U` cost. Since `bar T` belongs to `Z`,

\[
\begin{aligned}
S_M(r)={}&V_{D,M,r}
+A_{M,r}\|\Pi_{Z_{M,r}}(D+\bar T_{M,r})\|^2\\
&+A_{M,r}\|(I-\Pi_{Z_{M,r}})D\|^2-N_{U,M,r}.       \tag{66.1}
\end{aligned}
\]

Extract the optimal below-`M` staircase `g_M`, of squared norm `W_M`, and
define the physical post-staircase residual

\[
R_{M,r}=\|(I-\Pi_{Z_{M,r}\oplus\langle g_M\rangle})D\|^2.
\]

Define the endpoint demand

\[
\boxed{
\Theta_{M,r}={N_{U,M,r}-V_{D,M,r}\over A_{M,r}}
-\|\Pi_{Z_{M,r}}(D+\bar T_{M,r})\|^2-W_M.}          \tag{66.2}
\]

Then the exact, non-artificial adaptive factorization is

\[
\boxed{S_M(r)=A_{M,r}(R_{M,r}-\Theta_{M,r}).}       \tag{66.3}
\]

This is the correct endpoint threshold. A formal identity obtained by defining
`Theta=1-S/A` from the already known budget is tautological and is not (66.2).
A proposed verifier using that normalization was rejected before commit.

## Complete tail and boundary realization

Cycles 62--63 give

\[
\boxed{R_{M,r}=\Omega_{\infty,M,r}
+{\delta_{M,r}^2\over(M-1)^{-1}+\|u_{M,r}\|^2}.}   \tag{66.4}
\]

Thus the additive-12 statement is exactly

\[
\boxed{
\forall M\ge3\quad\exists r\le12:\quad
\Omega_{\infty,M,r}
+{\delta_{M,r}^2\over(M-1)^{-1}+\|u_{M,r}\|^2}
\ge\Theta_{M,r}.}                                  \tag{66.5}
\]

Unlike the auxiliary centered covariance, every term in (66.5) comes from the
same complete Vasyunin Gram and boundary channel.

## Nested endpoint update

As `r` increases, the probe spaces are nested. If

\[
q_r={ (I-\Pi_{Z_{M,r}})\rho_{M+r}
\over\|(I-\Pi_{Z_{M,r}})\rho_{M+r}\|},
\]

then

\[
\boxed{R_{M,r+1}=R_{M,r}-|\langle D,q_r\rangle|^2.}              \tag{66.6}
\]

Thus reserve decreases by one exact Schur payment as demand changes in a
separate endpoint-dependent way. For every look-ahead `k`,

\[
R_{M,r}-R_{M,r+k}
=\sum_{j=r}^{r+k-1}|\langle D,q_j\rangle|^2.         \tag{66.7}
\]

A stopping theorem must compare these cumulative losses with the corresponding
change in `Theta`; one-step monotonicity is unavailable without additional
arithmetic input.

## Finite diagnostics and selector warning

Independent Arb diagnostics through the Cycle 51 frontier found that minimizing
the physical demand (66.2) selected a successful endpoint at every tested
start, with the weakest selected surplus at `[219,231)`. This is finite evidence
only and needs a durable independent implementation before being treated as a
certificate family.

Threshold minimization is not a generic Hilbert-space theorem. Two endpoints
can have demands `(1,2)` and available certified reserves `(0,3)`, so the
minimum-demand endpoint fails while the other succeeds. The constructive
certificate selector must instead maximize certified slack

\[
L_{M,r}(N)-\Theta_{M,r},                             \tag{66.8}
\]

where `L_(M,r)(N)` is a finite tail-plus-boundary lower certificate. Nested
finite supports satisfy `L(N)` increasing to `R`; therefore every endpoint with
strict surplus has a finite certificate. Equality may have no finite strict
certificate.

## Exact floor-cell representation

There is also a direct complete floor-cell formula

\[
S_M(r)=\sum_{k\ge1}q_{M,r}(k),                      \tag{66.9}
\]

where each `q` recombines its signed slope, intercept, and affine cross terms.
For a nonintegral truncation `X=K+theta`, the three partial-cell metrics scale
respectively as `theta^3`, `theta^2`, and `theta`; replacing the partial cell by
`theta q(K)` is false. The general tail is only `O_(M,r)(1/K)` without new
cancellation. This representation is the same budget, not an independent
reserve.

Likewise, a moving-endpoint centered Chebyshev covariance can be defined, with
a leading triangular local von-Mangoldt impulse over `2r-1` indices. It is an
auxiliary selector diagnostic unless embedded into an explicit physical dual
witness. Abstract PNT-quality models can defeat all twelve covariance tests
simultaneously while leaving the unobserved physical Gram reserve arbitrary.

The next target is therefore a physical comparison of the nested Schur payments
in (66.7) with the demand changes in (66.2), or a demand-aware finite dual
witness proving (66.8). No additive-12 theorem or RH result is claimed.
