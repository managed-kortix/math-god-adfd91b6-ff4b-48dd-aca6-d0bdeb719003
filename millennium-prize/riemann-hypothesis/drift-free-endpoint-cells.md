# Drift-free complete endpoint cells

On `I_k=(k,k+1)`, write `t=k+x` and define the actual endpoint values

\[
r_k=f(k+)=Ak+b_k,\qquad s_k=d(k+)=Dk+e_k.
\]

For `q=2fd-alpha d^2`, put

\[
c_2=2AD-\alpha D^2,
\quad \widehat z_k=2Dr_k+2(A-\alpha D)s_k,
\quad g_k=2r_ks_k-\alpha s_k^2.
\]

Then exactly

\[
\boxed{J_k=c_2R_k+\widehat z_kV_k+g_kw_k,}
\]

where

\[
R_k=\int_0^1\frac{x^2}{(k+x)^2}dx,
\quad V_k=\int_0^1\frac{x}{(k+x)^2}dx,
\quad w_k=\frac1{k(k+1)}.
\]

All three weights are positive and decreasing, with asymptotics
`1/(3k^2),1/(2k^2),1/k^2`. This removes the artificial linear drift in the
intercept-based Abel form, but `zhat_k,g_k` remain signed.

For cumulative primitives `zhatZ_m=sum_(K<=k<=m) zhat_k` and
`G_m=sum_(K<=k<=m)g_k`, finite Abel summation gives

\[
\begin{aligned}
\sum_{K\le k<T}J_k={}&c_2\sum_{K\le k<T}R_k
+\widehat Z_{T-1}V_{T-1}
+\sum_{m=K}^{T-2}\widehat Z_m(V_m-V_{m+1})\\
&+G_{T-1}w_{T-1}
+\sum_{m=K}^{T-2}G_m(w_m-w_{m+1}).
\end{aligned}
\]

Every Abel weight is positive. The missing estimate is a correlated lower bound
for the combined `zhat V+g w` tail.

## Initial reserve cancellation

For `k<=N`, let `L=log N`, `C=2-alpha`, and `psi_k=psi(k)`. Since
`b_k=e_k=-psi_k/L`, define

\[
B=A+(1-\alpha)D,
\quad S_1=\sum_{k\le N}\psi(k)\log(1+1/k),
\quad S_2=\sum_{k\le N}\frac{\psi(k)^2}{k(k+1)}.
\]

The exact complete initial sum is

\[
R_N=ND(2A-\alpha D)-2BS_1/L+CS_2/L^2.
\]

If `m_N=S_1/(NL)`, `V_N=S_2/L^2-S_1^2/(NL^2)>=0`, and
`G=(2A-alpha D)/(2-alpha)`, then

\[
\boxed{R_N=(2-\alpha)[V_N+N(D-m_N)(G-m_N)].}
\]

Thus a lower bound on `psi^2` alone is misleading: three terms of natural size
`N/log^2 N` cancel at leading order. Coarse Chebyshev bounds cannot control the
remaining slope-position term.

## Exact post-reserve transform

The endpoint values satisfy

\[
r_{k+1}-r_k=A-x_{k+1},\qquad s_{k+1}-s_k=D-y_{k+1}.
\]

For `k<=N`,

\[
r_k=kA-\psi(k)/\log N,\qquad s_k=kD-\psi(k)/\log N.
\]

For `N<k<=2N`, define

\[
T_N(k)=\frac1{\log N}\sum_{N<n\le k}\mu(n)\log(N/n).
\]

Then

\[
r_k=kA-\psi(k)/\log N+T_N(k),
\qquad s_k=kD-\psi(k)/\log N+T_N(k)/\alpha.
\]

The post-reserve obstruction is therefore exactly a signed truncated Möbius
correlation inside `g_k`.
