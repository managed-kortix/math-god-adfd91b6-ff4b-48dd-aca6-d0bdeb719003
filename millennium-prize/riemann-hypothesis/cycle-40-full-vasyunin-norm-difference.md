# Cycle 40: the full Vasyunin expansion of the half-strength norm difference

## 1. Exact object and its sign

Work in `H=L^2((0,1),dx)`. Put

\[
 \chi(x)=1,\qquad \rho_a(x)=\{1/(ax)\},\qquad
 L_n=\log n,
\]

\[
 U_n=\chi+\sum_{a\le n}\mu(a)\rho_a,
 \qquad D_n=\sum_{a\le n}\mu(a)(\log a)\rho_a,
\]

and define

\[
 \boxed{H_n=\|D_n\|^2-L_nL_{n+1}\|U_n\|^2.}       \tag{40.1}
\]

The Cycle 39 cancellation gives

\[
 L_{n+1}P_{n+1}-L_nP_n
 =-{(L_{n+1}-L_n)H_n\over L_nL_{n+1}}.              \tag{40.2}
\]

Consequently `H_n>=0` is exactly the half-strength singleton condition. It is
not true at every index: exact complete-Gram evaluation already gives `H_2<0`.
Thus the viable target is an averaged or adaptive-block sign, not pointwise
positivity.

## 2. Full Vasyunin Gram expansion

Write

\[
 g_a=\langle\chi,\rho_a\rangle={\log a+1-\gamma\over a}       \tag{40.3}
\]

and `G_(a,b)=<rho_a,rho_b>`. If `d=(a,b)`, `p=a/d`, `q=b/d`, and
`ell=lcm(a,b)`, then the complete restricted Gram entry is

\[
 G_{a,b}={
 (q-p)\log(p/q)+(p+q)(\log(2\pi)-\gamma)
 -\pi[V(p,q)+V(q,p)]
 \over2\ell}-{1\over ab},                            \tag{40.4}
\]

where

\[
 V(p,q)=\sum_{k=1}^{q-1}\{kp/q\}\cot(\pi k/q),\qquad V(p,1)=0.
\]

Set `C_n=L_nL_(n+1)` and

\[
 w_n(a)=\mu(a)^2\big((\log a)^2-C_n\big),
\]

\[
 W_n(a,b)=\mu(a)\mu(b)\big((\log a)(\log b)-C_n\big).
\]

Opening the two norms while retaining the symmetric pair correlation gives

\[
 \boxed{
 H_n=-C_n-2C_n\sum_{a\le n}\mu(a)g_a
 +\sum_{a\le n}w_n(a)G_{a,a}
 +2\sum_{1\le a<b\le n}W_n(a,b)G_{a,b}.}             \tag{40.5}
\]

The diagonal is elementary. Formula (40.4) with `p=q=1` gives

\[
 G_{a,a}={\log(2\pi)-\gamma\over a}-{1\over a^2}.    \tag{40.6}
\]

Hence

\[
\begin{aligned}
 H_n={}&-C_n
 -2C_n\sum_{a\le n}{\mu(a)(\log a+1-\gamma)\over a}\\
 &+\sum_{a\le n}\mu(a)^2\big((\log a)^2-C_n\big)
 \left({\log(2\pi)-\gamma\over a}-{1\over a^2}\right)\\
 &+2\sum_{a<b\le n}\mu(a)\mu(b)
 \big((\log a)(\log b)-C_n\big)G_{a,b}.             \tag{40.7}
\end{aligned}
\]

Equations (40.4) and (40.7) are a finite exact Vasyunin formula. They also show
why separating a putative positive diagonal main term is hazardous: the
diagonal has size comparable to individual off-diagonal channels, while the
final answer is their highly cancelled contraction.

## 3. Cancellation before expansion

Let

\[
 R_n=\sqrt{L_nL_{n+1}},\qquad
 e_n^-(a)=\mu(a)(\log a-R_n),\qquad
 e_n^+(a)=\mu(a)(\log a+R_n).
\]

Difference-of-squares polarization gives

\[
 \boxed{H_n=\langle D_n-R_nU_n,D_n+R_nU_n\rangle.}     \tag{40.8}
\]

Thus an explicitly cancellation-preserving finite Gram formula is

\[
\boxed{
 H_n=-C_n-R_n\sum_{b\le n}e_n^+(b)g_b
       +R_n\sum_{a\le n}e_n^-(a)g_a
       +\sum_{a,b\le n}e_n^-(a)e_n^+(b)G_{a,b}.}      \tag{40.9}
\]

This identifies the sign as the acute/obtuse orientation of the two polarized
vectors `D_n-R_nU_n` and `D_n+R_nU_n`. It is not implied by positive
semidefiniteness of `G`.

## 4. Mobius convolutions and exact cells

After the reciprocal change of variables, use

\[
 \phi_a(t)=\{t/a\},\qquad
 U_n(t)=1+\sum_{a\le n}\mu(a)\phi_a(t),\qquad
 D_n(t)=\sum_{a\le n}\mu(a)(\log a)\phi_a(t),
\]

in `L^2([1,infinity),dt/t^2)`. Define

\[
 m_n=\sum_{a\le n}{\mu(a)\over a},\qquad
 \ell_n=\sum_{a\le n}{\mu(a)\log a\over a},
\]

\[
 u_{n,k}=1-\sum_{a\le n}\mu(a)\lfloor k/a\rfloor,
 \qquad
 v_{n,k}=-\sum_{a\le n}\mu(a)(\log a)\lfloor k/a\rfloor. \tag{40.11}
\]

On the unit cell `k<t<k+1`,

\[
 U_n(t)=m_nt+u_{n,k},\qquad D_n(t)=\ell_nt+v_{n,k}.   \tag{40.12}
\]

For

\[
 \lambda_k=\log(1+1/k),\qquad \tau_k={1\over k(k+1)},
\]

the exact cell contribution to (40.1) is

\[
\begin{aligned}
 h_{n,k}={}&(\ell_n^2-C_nm_n^2)
 +2(\ell_nv_{n,k}-C_nm_nu_{n,k})\lambda_k\\
 &+(v_{n,k}^2-C_nu_{n,k}^2)\tau_k,                  \tag{40.13}
\end{aligned}
\]

and

\[
 \boxed{H_n=\sum_{k\ge1}h_{n,k}.}                   \tag{40.14}
\]

For `k<=n`, the complete divisor convolutions are

\[
 \sum_{a\mid j}\mu(a)=\mathbf1_{j=1},\qquad
 \sum_{a\mid j}\mu(a)\log a=-\Lambda(j).
\]

Summing over `j<=k` yields

\[
 u_{n,k}=0,\qquad v_{n,k}=\psi(k),
\]

so the exact initial Chebyshev cells are

\[
 \boxed{h_{n,k}=\ell_n^2+2\ell_n\psi(k)\lambda_k
                    +\psi(k)^2\tau_k-C_nm_n^2,
        \qquad 1\le k\le n.}                         \tag{40.15}
\]

The safest cancellation-preserving cell form is obtained directly from
(40.8). Define

\[
 A_n^-=\ell_n-R_nm_n,\qquad A_n^+=\ell_n+R_nm_n,
\]

\[
 E_{n,k}^-=v_{n,k}-R_nu_{n,k},\qquad
 E_{n,k}^+=v_{n,k}+R_nu_{n,k}.
\]

Then

\[
 \boxed{h_{n,k}=A_n^-A_n^+
 +(A_n^-E_{n,k}^++A_n^+E_{n,k}^-)\lambda_k
 +E_{n,k}^-E_{n,k}^+\tau_k.}                          \tag{40.16}
\]

For `k<=n`, this reduces to

\[
 h_{n,k}=A_n^-A_n^++(A_n^-+A_n^+)\psi(k)\lambda_k
                       +\psi(k)^2\tau_k,              \tag{40.17}
\]

which is algebraically identical to (40.15). No Chebyshev substitution is
valid for `k>n`; those tail cells retain the truncated divisor floors in
(40.11). In particular, proving a sign for only the initial cells does not
prove a sign for `H_n`.

## 5. Averaging and block sign

The singleton sign fails, but the exact block residual has a clean positive-
weight representation. Let

\[
 \eta_n={L_{n+1}-L_n\over L_nL_{n+1}^2}>0.
\]

Using (40.2) in the half-strength summation-by-parts identity gives

\[
\boxed{
 P_a-P_b-\sum_{n=a}^{b-1}\left(1-{L_n\over L_{n+1}}\right)P_n
 =\sum_{n=a}^{b-1}\eta_nH_n.}                         \tag{40.18}
\]

Therefore the exact surviving sign target is

\[
 \boxed{\text{the block }[a,b)\text{ succeeds at }\kappa=1/2
 \iff \sum_{n=a}^{b-1}\eta_nH_n\ge0.}                \tag{40.19}
\]

Equivalently, if `A_n=L_nP_n`, then

\[
 H_n={L_nL_{n+1}\over L_{n+1}-L_n}(A_n-A_{n+1}),
 \qquad \eta_nH_n={A_n-A_{n+1}\over L_{n+1}}.         \tag{40.20}
\]

This weighted average is the correct place to seek compensation. An unweighted
mean of `H_n`, a mean of the diagonal part of (40.7), or a Chebyshev-only
prefix all alter the exact block functional and need not preserve its sign.

## 6. Certified finite diagnostic

`analyze_cycle40_h.py` evaluates (40.1) with the complete restricted Vasyunin
Gram matrix and outward-rounded Arb arithmetic. At 256-bit precision through
`n=512`, it certifies 499 positive and 12 negative values. The negative indices
are

\[
 2,39,40,95,96,99,100,219,220,221,222,226.
\]

Every start through 512 has a nonnegative weighted block within the available
range; the longest first-passage block is `[219,231)`, of length 12. The
command is

```text
uv run --with python-flint python analyze_cycle40_h.py --max-n 512 --bits 256
```

These are finite certificates only. They prove that pointwise positivity is
false and that weighted compensation occurs in this range. They do not imply
an eventual sign density, a uniform block length, an endpoint from every
arbitrarily large start, or RH. The remaining theorem would have to control the
complete Mobius contraction, including the off-diagonal Vasyunin terms or,
equivalently, the full tail of the divisor-floor cells.
