# Cycle 38: exact consecutive-block coefficient and Gram kernels

## Setup

Write

\[
 x_n={1\over\log n},\qquad h_n=x_n-x_{n+1},\qquad
 \rho_n=h_n\log n={\log(1+1/n)\over\log(n+1)},
\]

and, for `q>=1`,

\[
 c_q(n)=\mu(q){\log(n/q)_+\over\log n},\qquad
 \phi_q(t)=\{t/q\},\qquad
 f_n=1+\sum_qc_q(n)\phi_q.
\]

Thus `P_n=||f_n||_H^2` in
`H=L^2([1,infinity),dt/t^2)`.  Put

\[
 g_q=\langle1,\phi_q\rangle_H,
 \qquad G_{q,r}=\langle\phi_q,\phi_r\rangle_H.
\tag{38.1}
\]

These fixed physical Gram entries are themselves explicit.  One has

\[
 \boxed{g_q={\log q+1-\gamma\over q}.}
\tag{38.1a}
\]

For completeness, let `d=(q,r)`, `p=q/d`, `s=r/d`, and
`ell=lcm(q,r)`.  With the Vasyunin sum

\[
 V(p,s)=\sum_{k=1}^{s-1}\left\{{kp\over s}\right\}
 \cot {\pi k\over s},\qquad V(p,1)=0,
\]

the exact fractional-part Gram kernel is

\[
 \boxed{G_{q,r}={
 (s-p)\log(p/s)+(p+s)[\log(2\pi)-\gamma]
 -\pi[V(p,s)+V(s,p)]
 \over2\ell}-{1\over qr}.}
\tag{38.1b}
\]

The expression is symmetric despite its displayed oriented form (interchanging
`p,s` gives the same value).  It is the standard full Vasyunin kernel with the
rank-one `t<1` tail removed after the reciprocal-variable change.  Equations
(38.1a)--(38.1b) make every kernel in this note finite and explicit.

The convention at `q=n` is harmless: `c_n(n)=0`.  All sums below can
therefore use `q<=n` instead of `q<n`.

## Complete consecutive decrement

For integers `2<=a<b`, exact telescoping gives

\[
 \mathcal D_{a,b}:=\sum_{n=a}^{b-1}(P_n-P_{n+1})=P_a-P_b.
\tag{38.2}
\]

Its correlation-preserving coefficient expansion is

\[
 \boxed{\mathcal D_{a,b}=2\sum_{q<b}D_{a,b}(q)g_q
 +\sum_{q,r<b}K_{a,b}(q,r)G_{q,r},}
\tag{38.3}
\]

where

\[
 \boxed{D_{a,b}(q)=\sum_{n=a}^{b-1}[c_q(n)-c_q(n+1)]
 =c_q(a)-c_q(b),}
\tag{38.4}
\]

\[
 \boxed{K_{a,b}(q,r)=\sum_{n=a}^{b-1}
 [c_q(n)c_r(n)-c_q(n+1)c_r(n+1)]
 =c_q(a)c_r(a)-c_q(b)c_r(b).}
\tag{38.5}
\]

The common `n` in each product in (38.5) is essential.  In particular,
`K_(a,b)` is not `D_(a,b) tensor D_(a,b)`.

There is also an exact local form.  Direct calculation gives

\[
 d_{n,q}:=c_q(n)-c_q(n+1)
 =-h_n\mu(q)\log q\,\mathbf1_{q\leq n}.
\tag{38.6}
\]

Hence

\[
 K_{a,b}(q,r)={1\over2}\sum_{n=a}^{b-1}
 \left\{d_{n,q}[c_r(n)+c_r(n+1)]
 +d_{n,r}[c_q(n)+c_q(n+1)]\right\}.
\tag{38.7}
\]

This is the symmetric first-difference kernel before telescoping.  It keeps the
two coefficients at the same scale and exposes the one-prefix von Mangoldt
vector in (38.6), without replacing a same-`n` product by products of separate
averages.

## Exact weighted dissipation kernel

The weighted block functional required by the variable-block theorem is

\[
 \mathcal R_{a,b}:=\sum_{n=a}^{b-1}\rho_nP_n.
\tag{38.8}
\]

Define

\[
 W_{a,b}=\sum_{n=a}^{b-1}\rho_n,
 \quad L_{a,b}(q)=\sum_{n=a}^{b-1}\rho_nc_q(n),
 \quad Q_{a,b}(q,r)=\sum_{n=a}^{b-1}\rho_nc_q(n)c_r(n).
\tag{38.9}
\]

Then

\[
 \boxed{\mathcal R_{a,b}=W_{a,b}+2\sum_{q<b}L_{a,b}(q)g_q
 +\sum_{q,r<b}Q_{a,b}(q,r)G_{q,r}.}
\tag{38.10}
\]

Again, `Q` is the average of the same-`n` outer products, not the outer product
of `L` with itself.

All coefficients have short exact finite-sum forms.  For `m>=1` and
`j=0,1,2`, put

\[
 S_j(m)=\sum_{n=\max(a,m)}^{b-1}\rho_nx_n^j,
\tag{38.11}
\]

with an empty sum interpreted as zero.  Then

\[
 \boxed{L_{a,b}(q)=\mu(q)[S_0(q)-(\log q)S_1(q)],}
\tag{38.12}
\]

and, with `m=max(q,r)`,

\[
 \boxed{Q_{a,b}(q,r)=\mu(q)\mu(r)
 [S_0(m)-(\log q+\log r)S_1(m)
 +(\log q)(\log r)S_2(m)].}
\tag{38.13}
\]

These formulas include the changing support at `n=q` and `n=r`; no endpoint
correction is missing because the newly entering coefficient is zero.

Since `P_n-P_(n+1)=2h_nE_n`, the desired block estimate

\[
 \sum_{n=a}^{b-1}h_nE_n\geq
 \kappa\sum_{n=a}^{b-1}h_n(\log n)P_n
\tag{38.14}
\]

is exactly

\[
 \boxed{\mathcal D_{a,b}\geq2\kappa\mathcal R_{a,b}.}
\tag{38.15}
\]

Thus (38.3) and (38.10), with the factor `2 kappa`, are the exact two sides of
the complete consecutive-block problem.

## Positivity and completion after summing the scale

The weighted side has an exact covariance completion.  Let

\[
 \bar c_q={L_{a,b}(q)\over W_{a,b}},\qquad
 H_{a,b}(q,r)=Q_{a,b}(q,r)
 -{L_{a,b}(q)L_{a,b}(r)\over W_{a,b}}.
\tag{38.16}
\]

Because every `rho_n>0`,

\[
 H_{a,b}(q,r)=\sum_{n=a}^{b-1}\rho_n
 [c_q(n)-\bar c_q][c_r(n)-\bar c_r]
\tag{38.17}
\]

is positive semidefinite as a coefficient-space Gram matrix.  In physical
space this gives the exact completion

\[
 \boxed{\begin{aligned}
 \mathcal R_{a,b}={}&W_{a,b}
 \left\|1+\sum_q\bar c_q\phi_q\right\|_H^2\\
 &+\sum_{n=a}^{b-1}\rho_n
 \left\|\sum_q[c_q(n)-\bar c_q]\phi_q\right\|_H^2.
 \end{aligned}}
\tag{38.18}
\]

Equivalently, the second line is
`sum_(q,r) H_(a,b)(q,r)G_(q,r)>=0`.  This is the full algebraic positivity
created by summing `n`: a positive mean square plus a positive scale-variance
square.  Dropping the variance is valid but loses exactly the common-scale
correlations that survive smoothing.

No analogous sum-of-squares completion exists for the decrement alone.  With
the augmented coefficient vector

\[
 u_n=(1,(c_q(n))_{q<b}),
\]

its scale-side kernel is

\[
 B_{a,b}=u_au_a^T-u_bu_b^T.
\tag{38.19}
\]

Unless `u_a=u_b`, this difference of two rank-one positive kernels is
indefinite on `span(u_a,u_b)`: a vector orthogonal to `u_a` but not to `u_b`
has a negative quadratic form, and the reversed choice has a positive one.
For the combined target the coefficient kernel is

\[
 B_{a,b}-2\kappa\sum_{n=a}^{b-1}\rho_nu_nu_n^T,
\tag{38.20}
\]

so subtracting the weighted Gram kernel cannot produce coefficient-space
positivity.  Equation (38.18) therefore supplies a useful exact RHS
completion, but no purely algebraic proof of (38.15).  Any favorable sign must
use special arithmetic interaction with the fixed fractional-part Gram matrix
`G`, rather than Gram positivity or scale summation alone.

## Verdict

Consecutive summation completely telescopes the decrement kernel while the
weighted RHS retains a genuine same-scale covariance kernel.  The latter has
the positive completion (38.18).  The endpoint difference remains an
indefinite rank-two scale kernel, and moving any positive multiple of the RHS
to its left only adds negative Gram directions.  Thus Cycle 38 isolates the
remaining task sharply: prove an arithmetic lower bound for the contraction of
(38.3) with the fixed fractional-part Gram data strong enough to dominate the
mean and covariance terms in (38.18).  There is no missing algebraic
completion after the `n`-sum.
