# Weighted drift-free Mobius kernel

Let `L=log N`, let `M=2N`, and sum complete drift-free endpoint
coefficients with

\[
w_k={1\over k(k+1)}.
\]

This note expands the range `N<k<=2N` before applying any bounds. Endpoint
cell conventions may instead use `N<=k<2N`; the same formulas hold after
changing the terminal index, and the `k=N` term has zero fresh transform.

## 1. Exact cancellation in one cell

Put

\[
p_k=kA-{\psi(k)\over L},\qquad q_k=kD-{\psi(k)\over L},
\]

and, for `N<k<=2N`,

\[
T_k=T_N(k)={1\over L}\sum_{N<n\le k}\mu(n)\log(N/n).
\]

The exact endpoint formulas are

\[
r_k=p_k+T_k,\qquad s_k=q_k+{T_k\over\alpha}.
\]

Expanding `g_k=2r_ks_k-alpha s_k^2` gives the useful cancellation

\[
\boxed{
g_k=g_k^{(0)}+{2p_kT_k+T_k^2\over\alpha},\qquad
g_k^{(0)}=2p_kq_k-\alpha q_k^2.
}
\]

In particular, every term involving `q_k T_k` cancels. Equivalently,

\[
g_k={r_k^2-(r_k-\alpha s_k)^2\over\alpha},\qquad
r_k-\alpha s_k=p_k-\alpha q_k,
\]

so the fresh transform changes only the first square.

## 2. Sum first: exact linear and quadratic kernels

Write

\[
\ell_n=\log(N/n)<0\quad(N<n\le M).
\]

Then

\[
\sum_{N<k\le M}w_kg_k
=\sum_{N<k\le M}w_kg_k^{(0)}+\mathcal L_{N,M}+\mathcal Q_{N,M},
\]

where the exact fresh linear form is

\[
\boxed{
\mathcal L_{N,M}={2\over\alpha L}
\sum_{N<n\le M}\mu(n)\ell_n R_n^{(M)},
\qquad
R_n^{(M)}=\sum_{k=n}^M{p_k\over k(k+1)},
}
\]

and the exact fresh quadratic form is

\[
\boxed{
\mathcal Q_{N,M}={1\over\alpha L^2}
\sum_{N<n,m\le M}\mu(n)\mu(m)\ell_n\ell_m
K_M(n,m),
}
\]

with

\[
\boxed{
K_M(n,m)=\sum_{k=\max(n,m)}^M{1\over k(k+1)}
={1\over\max(n,m)}-{1\over M+1}.
}
\]

Thus the requested max-index weights telescope exactly; no absolute value or
endpoint estimate is needed.

The linear coefficient also has a fully telescoped arithmetic expression. If
`H_j=sum_(a<=j)1/a`, then

\[
R_n^{(M)}=A(H_{M+1}-H_n)-{1\over L}\Sigma_n^{(M)},
\]

where

\[
\boxed{
\Sigma_n^{(M)}=
\psi(n-1)\left({1\over n}-{1\over M+1}\right)
+\sum_{d=n}^M\Lambda(d)
\left({1\over d}-{1\over M+1}\right).
}
\]

This follows by opening `psi(k)=sum_(d<=k)Lambda(d)` only after summing in
`k`. It is preferable to bounding `psi(k)` cell by cell.

## 3. Positivity and signs

For arbitrary real `x_n`,

\[
\sum_{n,m}x_nx_mK_M(n,m)
=\sum_{k=N+1}^M w_k\left(\sum_{N<n\le k}x_n\right)^2\ge0.
\]

Hence `K_M` is a Gram kernel, and in fact is positive definite on the full
index set `N<n<=M`: if `B_(k,n)=1_(n<=k)`, then

\[
K_M=B^T\operatorname{diag}(w_{N+1},\ldots,w_M)B.
\]

The triangular cumulative-sum matrix `B` is invertible and every `w_k` is
positive. Its inverse form is correspondingly tridiagonal: if
`y_N=0` and indices run through `N<n<=M`, then

\[
y^TK_M^{-1}y=\sum_{n=N+1}^M { (y_n-y_{n-1})^2\over w_n}.
\]

Taking `x_n=mu(n)ell_n` proves

\[
\mathcal Q_{N,M}\ge0.
\]

This positivity is order/cumulative positivity, not gcd positivity. The kernel
depends only on `max(n,m)`, not on `gcd(n,m)` or divisibility. Regrouping pairs
by gcd does not preserve the Gram squares, and individual gcd classes have no
forced sign because of `mu(n)mu(m)`. Thus there is no hidden positive gcd
kernel on the first dyadic block.

The complete fresh correction is not nonnegative. Its cellwise form is

\[
{(p_k+T_k)^2-p_k^2\over\alpha},
\]

so the positive `T_k^2` term competes with `2p_kT_k`. In the summed form the
same obstruction is the signed linear form `\mathcal L_{N,M}`. Neither
`\mu(n)\ell_n` nor `R_n^{(M)}` has a uniform sign. Completing the square merely
returns

\[
\mathcal L_{N,M}+\mathcal Q_{N,M}
={1\over\alpha}\sum_{N<k\le M}w_k
\bigl[(p_k+T_k)^2-p_k^2\bigr],
\]

which is exact but indefinite.

## 4. Extension beyond `2N`

For any scale `B`, define the exact floor transform

\[
U_B(k)={1\over\log B}\sum_{B<n\le k}
\mu(n)\log(B/n)\left\lfloor{k\over n}\right\rfloor.
\]

The classical convolution identity gives, for every `k`,

\[
b_k^{(B)}=-{\psi(k)\over\log B}+U_B(k).
\]

For the `N -> 2N` endpoint channels, set `X_k=U_N(k)` and
`Y_k=U_(2N)(k)`. Using

\[
\alpha={\log2\over\log(2N)},\qquad
{1\over\log(2N)}={1-\alpha\over\log N},
\]

one obtains for all `k`

\[
r_k=p_k+X_k,\qquad
s_k=q_k+{X_k-Y_k\over\alpha}.
\]

Therefore the exact all-range expansion is

\[
\boxed{
g_k=g_k^{(0)}+{2p_kX_k-2(p_k-\alpha q_k)Y_k+X_k^2-Y_k^2\over\alpha}.
}
\]

For `k<=2N`, `Y_k=0` and `floor(k/n)=1` in `X_k`, recovering the preceding
formula. On a finite later range, each square separately has a PSD floor
kernel

\[
K_{B;K,T}(n,m)=\sum_{k=K}^T{1\over k(k+1)}
\left\lfloor{k\over n}\right\rfloor
\left\lfloor{k\over m}\right\rfloor,
\]

because it is again a Gram matrix. But the endpoint expression contains the
difference `X_k^2-Y_k^2`; it is a difference of two PSD forms, with no general
Loewner ordering. Moreover these floor kernels depend on the full pair
`(n,m)`, not only on `gcd(n,m)`. A gcd kernel can arise after averaging
fractional parts over common periods, but that is a different representation
and does not turn this exact finite weighted floor kernel into a positive gcd
form.

Finally, the transforms `X_k,Y_k` separately contain growing floor pieces.
Extending either isolated square to infinity before recombining the two scales
loses the endpoint cancellations. The safe exact statement beyond `2N` is
therefore the finite-horizon identity above, followed by recombination, and
only then any limiting argument or bound.

## Conclusion

The first dyadic block has one genuinely favorable structure: its fresh
quadratic Mobius kernel is an exact positive-definite max kernel. The remaining
obstruction is sharply localized in the linear functional with coefficients
`R_n^(2N)`. There is no gcd dependence to exploit at this stage. Beyond `2N`,
each scale still supplies a PSD floor Gram form, but the cross-scale endpoint
telescope subtracts the `2N` form and restores indefiniteness.
