# Abel identities for complete endpoint unit cells

Let

\[
x_n=\sum_{a\mid n}u_a,\qquad y_n=\sum_{a\mid n}d_a,
\]

and let `b_k,e_k` be the affine intercepts of the endpoint channels on
`(k,k+1)`. Then

\[
b_n=b_{n-1}-x_n,\qquad e_n=e_{n-1}-y_n.
\]

Put

\[
z_k=2Db_k+2(A-\alpha D)e_k,
\qquad h_k=2b_ke_k-\alpha e_k^2.
\]

The exact cell functional is

\[
J_k=c_2+z_kL_k+h_kw_k,
\quad L_k=\log((k+1)/k),\quad w_k=1/[k(k+1)].
\]

## Cumulative Abel form

For `K<=m<T`, define

\[
Z_m=\sum_{k=K}^m z_k,\qquad H_m=\sum_{k=K}^m h_k.
\]

Since both `L_k` and `w_k` decrease, finite Abel summation gives

\[
\boxed{\begin{aligned}
\sum_{K\le k<T}J_k={}&c_2(T-K)+Z_{T-1}L_{T-1}\\
&+\sum_{m=K}^{T-2}Z_m\log\left(1+\frac1{m(m+2)}\right)\\
&+H_{T-1}w_{T-1}
+\sum_{m=K}^{T-2}\frac{2H_m}{m(m+1)(m+2)}.
\end{aligned}}
\]

Every weight multiplying `Z_m,H_m` is positive. Therefore

\[
\sum_{K\le k<T}J_k
\ge c_2(T-K)+L_K\min_{K\le m<T}Z_m
+w_K\min_{K\le m<T}H_m.
\]

This identifies the exact analytic target: lower envelopes for the cumulative
linear and signed-quadratic divisor-impulse primitives. In particular,
`H_m` must retain `2b_ke_k-alpha e_k^2`; separate absolute bounds destroy the
needed correlation.

## Boundary--impulse form

Let

\[
s_n=2Dx_n+2(A-\alpha D)y_n
\]

and

\[
\rho_n=h_{n-1}-h_n
=2\bar e_nx_n+2(\bar b_n-\alpha\bar e_n)y_n,
\]

where `bar b_n=b_(n-1)-x_n/2` and `bar e_n=e_(n-1)-y_n/2`. Then

\[
\boxed{\begin{aligned}
\sum_{K\le k<T}J_k={}&c_2(T-K)
+z_{T-1}\log T-z_K\log K\\
&+\sum_{n=K+1}^{T-1}s_n\log n
+\frac{h_K}{K}-\frac{h_{T-1}}T
-\sum_{n=K+1}^{T-1}\frac{\rho_n}{n}.
\end{aligned}}
\]

This is streamable after a divisor sieve, but has larger boundary cancellation
than the cumulative form.

## Cross-scale telescope and obstruction

For dyadic scales `M_r=2^rN`, the natural weights telescope pointwise:

\[
\sum_{r=0}^{L-1}\alpha_{M_r}q_{M_r}(t)
=F_N(t)^2-F_{2^LN}(t)^2.
\]

Thus longer alpha-weighted blocks remove all intermediate scales but do not
create positivity. General weights `lambda_r`, with
`beta_r=lambda_r/alpha_r`, satisfy

\[
\sum_{r<L}\lambda_rq_{M_r}
=\beta_0F_N^2+\sum_{1\le j<L}(\beta_j-\beta_{j-1})F_{2^jN}^2
-\beta_{L-1}F_{2^LN}^2.
\]

Nonconstant weights leave mixed-sign intermediate squares. The missing result
is therefore not another telescope, but a lower-envelope estimate for the
aggregated cumulative primitives before absolute values.

## Classical initial-range simplification

For the logarithmic Möbius taper and `1<=k<=N`, convolution identities give

\[
\sum_{a\le k}\mu(a)\lfloor k/a\rfloor=1,
\qquad
\sum_{a\le k}\mu(a)\log a\lfloor k/a\rfloor=-\psi(k).
\]

Consequently

\[
b_k=e_k=-\psi(k)/\log N\qquad(1\le k\le N),
\]

and

\[
h_k=(2-\alpha)\psi(k)^2/(\log N)^2\ge0
\]

on this initial range. Beyond `N`, an explicit truncated Möbius tail enters;
bounding it at useful strength is again the arithmetic obstruction.
