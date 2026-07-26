# Cycle 39: exact one-step radial recurrence

## 1. Coefficient update

Let

\[
 L_n=\log n,\qquad L_{n+1}=\log(n+1),\qquad
 \delta_n=L_{n+1}-L_n,
\]

\[
 h_n={1\over L_n}-{1\over L_{n+1}}
     ={\delta_n\over L_nL_{n+1}},\qquad
 w_n=h_nL_n={\delta_n\over L_{n+1}}.
\]

In

\[
 H=L^2([1,\infty),dt/t^2),\qquad \phi_a(t)=\{t/a\},
\]

put

\[
 c_a(n)=\mu(a){\log(n/a)_+\over L_n},\qquad
 F_n=1+\sum_{a\geq1}c_a(n)\phi_a,
 \qquad P_n=\|F_n\|_H^2.
\]

For every `a<=n`,

\[
 c_a(n+1)-c_a(n)=h_n\mu(a)\log a,
\]

while `c_(n+1)(n+1)=0`. Therefore, with

\[
 D_n=\sum_{a\leq n}\mu(a)\log a\,\phi_a,
\]

the exact coefficient update is

\[
 \boxed{F_{n+1}=F_n+h_nD_n.}                         \tag{39.1}
\]

Taking squared norms gives the exact one-step recurrence

\[
 \boxed{P_{n+1}=P_n+2h_n\langle F_n,D_n\rangle
                    +h_n^2\|D_n\|^2.}               \tag{39.2}
\]

Equivalently, if

\[
 Q_n=-\langle F_n,D_n\rangle,\qquad R_n=\|D_n\|^2,
 \qquad E_n=Q_n-{h_n\over2}R_n,
\]

then

\[
 \boxed{P_{n+1}=P_n-2h_nE_n.}                        \tag{39.3}
\]

## 2. Radial alignment scalar

For `P_n>0`, define the exact compensated radial alignment

\[
 \boxed{\kappa_n={E_n\over L_nP_n}
 ={-\langle F_n,D_n\rangle-(h_n/2)\|D_n\|^2
   \over L_n\|F_n\|^2}.}                             \tag{39.4}
\]

Then (39.3) is the scalar recurrence

\[
 \boxed{P_{n+1}=(1-2\kappa_nw_n)P_n.}                \tag{39.5}
\]

The uncompensated normalized radial cosine is

\[
 \alpha_n={-\langle F_n,D_n\rangle
 \over\|F_n\|\,\|D_n\|}
\]

when `D_n` is nonzero. It is related to the recurrence scalar by

\[
 \boxed{\kappa_n={1\over L_n}
 \left(\alpha_n\sqrt{R_n\over P_n}
       -{h_n\over2}{R_n\over P_n}\right).}           \tag{39.6}
\]

For any comparison constant `kappa`, the exact one-step defect is

\[
 \boxed{P_{n+1}-(1-2\kappa w_n)P_n
       =2w_nP_n(\kappa-\kappa_n).}                    \tag{39.7}
\]

Thus the one-step inequality with strength `kappa` is exactly
`kappa_n>=kappa`.

## 3. The exact simplification at `kappa=1/2`

Define the finite Mobius vectors

\[
 U_n=1+\sum_{a\leq n}\mu(a)\phi_a,
 \qquad D_n=\sum_{a\leq n}\mu(a)\log a\,\phi_a.
\]

At both endpoints of the `n`th scale cell,

\[
 F_n=U_n-{D_n\over L_n},\qquad
 F_{n+1}=U_n-{D_n\over L_{n+1}}.                     \tag{39.8}
\]

Consequently the mixed radial term cancels after multiplication by the
endpoint logarithm:

\[
 \boxed{L_{n+1}P_{n+1}-L_nP_n
 =\delta_n\|U_n\|^2-h_n\|D_n\|^2
 =\delta_n\left(\|U_n\|^2-{\|D_n\|^2\over L_nL_{n+1}}\right).} \tag{39.9}
\]

Since `1-w_n=L_n/L_(n+1)`, equations (39.5) and (39.9) also give

\[
 \boxed{L_{n+1}P_{n+1}-L_nP_n
 =\delta_nP_n(1-2\kappa_n),}                          \tag{39.10}
\]

and hence

\[
 \boxed{\kappa_n={1\over2}
 \left[1-{\|U_n\|^2-\|D_n\|^2/(L_nL_{n+1})\over P_n}\right].} \tag{39.11}
\]

The sharp half-strength statements are therefore exactly equivalent:

\[
 \boxed{\kappa_n\geq{1\over2}
 \iff L_{n+1}P_{n+1}\leq L_nP_n
 \iff \|D_n\|^2\geq L_nL_{n+1}\|U_n\|^2.}           \tag{39.12}
\]

At equality they reduce to

\[
 \boxed{\kappa_n={1\over2}
 \iff P_{n+1}={L_n\over L_{n+1}}P_n
 \iff L_{n+1}P_{n+1}=L_nP_n
 \iff \|D_n\|^2=L_nL_{n+1}\|U_n\|^2.}               \tag{39.13}
\]

## 4. Exact Mobius--Chebyshev cell form

For `k>=1`, set

\[
 m_n=\sum_{a\leq n}{\mu(a)\over a},\qquad
 \ell_n=\sum_{a\leq n}{\mu(a)\log a\over a},
\]

\[
 u_{n,k}=1-\sum_{a\leq n}\mu(a)\lfloor k/a\rfloor,
 \qquad
 v_{n,k}=-\sum_{a\leq n}\mu(a)\log a\lfloor k/a\rfloor.
\]

On `k<t<k+1`, exactly,

\[
 U_n(t)=m_nt+u_{n,k},\qquad
 D_n(t)=\ell_nt+v_{n,k},                              \tag{39.14}
\]

and

\[
 F_n(t)=\left(m_n-{\ell_n\over L_n}\right)t
        +u_{n,k}-{v_{n,k}\over L_n}.                  \tag{39.15}
\]

Write

\[
 \lambda_k=\log(1+1/k),\qquad \tau_k={1\over k(k+1)},
\]

\[
 \mathcal I_k(a,b)=a^2+2ab\lambda_k+b^2\tau_k.
\]

Then the complete norms are

\[
 \boxed{P_n=\sum_{k\geq1}\mathcal I_k
 \left(m_n-{\ell_n\over L_n},
       u_{n,k}-{v_{n,k}\over L_n}\right),}           \tag{39.16}
\]

\[
 \boxed{\|U_n\|^2=\sum_{k\geq1}\mathcal I_k(m_n,u_{n,k}),
 \qquad
 \|D_n\|^2=\sum_{k\geq1}\mathcal I_k(\ell_n,v_{n,k}).} \tag{39.17}
\]

Thus the half-strength recurrence has the exact cell expansion

\[
 \boxed{L_{n+1}P_{n+1}-L_nP_n
 =\delta_n\sum_{k\geq1}
 \left[\mathcal I_k(m_n,u_{n,k})
 -{\mathcal I_k(\ell_n,v_{n,k})\over L_nL_{n+1}}\right].} \tag{39.18}
\]

For `1<=k<=n`, the two finite convolution identities give

\[
 u_{n,k}=0,\qquad v_{n,k}=\psi(k).
\]

Therefore on the complete initial Chebyshev range,

\[
 \boxed{U_n(t)=m_nt,\qquad
 D_n(t)=\ell_nt+\psi(k),
 \qquad
 F_n(t)=\left(m_n-{\ell_n\over L_n}\right)t
             -{\psi(k)\over L_n}.}                   \tag{39.19}
\]

The corresponding `k`th summand in (39.17) is exactly

\[
 \boxed{m_n^2-{\ell_n^2+2\ell_n\psi(k)\lambda_k
                    +\psi(k)^2\tau_k
                  \over L_nL_{n+1}}.}                 \tag{39.20}
\]

All sums in (39.16)--(39.18) are limits of complete unit-cell prefixes; no
Chebyshev substitution is made for `k>n`.
