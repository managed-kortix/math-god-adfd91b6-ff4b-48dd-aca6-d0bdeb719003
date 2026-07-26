# Cycle 41: finite-zero affine Gram form for the half-strength defect

## 1. Exact endpoint representation

Put

\[
 L=\log n,\qquad L_+=\log(n+1),\qquad C=LL_+,
 \qquad \lambda_k=\log(1+1/k),\qquad \tau_k={1\over k(k+1)}.
\]

In `L^2([1,infinity),dt/t^2)`, Cycle 40 defined

\[
 U_n(t)=1+\sum_{a\le n}\mu(a)\{t/a\},\qquad
 D_n(t)=\sum_{a\le n}\mu(a)(\log a)\{t/a\},
\]

and

\[
 \boxed{H_n=\|D_n\|^2-C\|U_n\|^2.}                              \tag{41.1}
\]

Let

\[
 m_n=\sum_{a\le n}{\mu(a)\over a},\qquad
 \ell_n=\sum_{a\le n}{\mu(a)\log a\over a},
\]

\[
 u_{n,k}=1-\sum_{a\le n}\mu(a)\lfloor k/a\rfloor,
 \qquad
 v_{n,k}=-\sum_{a\le n}\mu(a)(\log a)\lfloor k/a\rfloor.
\]

On `k<t<k+1`,

\[
 U_n(t)=m_nt+u_{n,k},\qquad D_n(t)=\ell_nt+v_{n,k}.                 \tag{41.2}
\]

The complete initial range has `u_(n,k)=0` and `v_(n,k)=psi(k)` for
`1<=k<=n`. For the tail `k>=n+1`, every divisor `a|k` satisfies `a<=k`, so

\[
 u_{n,k}-u_{n,k-1}=\sum_{\substack{a\mid k\\a>n}}\mu(a),
 \qquad
 v_{n,k}-v_{n,k-1}=\Lambda(k)+
       \sum_{\substack{a\mid k\\a>n}}\mu(a)\log a.               \tag{41.3}
\]

Thus, with the endpoint values `u_(n,n)=0`, `v_(n,n)=psi(n)`, define

\[
 M_{n,k}=\sum_{j=n+1}^{k}\sum_{\substack{a\mid j\\a>n}}\mu(a),
\]

\[
 Q_{n,k}=\sum_{j=n+1}^{k}\sum_{\substack{a\mid j\\a>n}}
                  \mu(a)\log a,
\]

where both sums are zero at `k=n`. Then the exact all-cell endpoint formula is

\[
 \boxed{u_{n,k}=M_{n,k},\qquad v_{n,k}=\psi(k)+Q_{n,k}\quad(k\ge n).} \tag{41.4}
\]

No tail cell has been discarded: the finite Mobius endpoint corrections
`M_(n,k),Q_(n,k)` are part of every formula below.

## 2. Finite symmetric zero coordinates

For integer `q>1`, use the right-continuous endpoint packet

\[
 B(q)=-\log(2\pi)-{1\over2}\log(1-q^{-2})+{1\over2}\Lambda(q).     \tag{41.5}
\]

Let `Z(T)` be the multiset of nontrivial zeros with `|Im rho|<=T`, counted
with multiplicity and closed under conjugation, where `T` is not a zero
ordinate. Define

\[
 Z_T(q)=\sum_{\rho\in Z(T)}{q^\rho\over\rho},\qquad
 r_T(q)=\psi(q)-q-B(q)+Z_T(q).                                     \tag{41.6}
\]

This is the exact finite identity

\[
 \psi(q)=q+B(q)-Z_T(q)+r_T(q).                                     \tag{41.7}
\]

Set `B(1)=-1`, `Z_T(1)=0`, and `r_T(1)=0`, so that (41.7) also agrees with
`psi(1)=0`. For `k>=1`, put

\[
 b_{n,T}(k)=k+B(k)+Q_{n,k}+r_T(k),\qquad
 z_\rho(k)={k^\rho\over\rho},                                     \tag{41.8}
\]

with `M_(n,k)=Q_(n,k)=0` on `k<=n`. Then

\[
 u_{n,k}=M_{n,k},\qquad
 v_{n,k}=b_{n,T}(k)-\sum_{\rho\in Z(T)}z_\rho(k).                  \tag{41.9}
\]

Equation (41.9) is exact at every integer endpoint. In particular, the
constant, trivial-zero logarithm, half-`Lambda(k)` jump, Mobius tail endpoint,
and finite-cutoff remainder all remain in the affine coordinate.

## 3. Full affine Gram matrix

Introduce the Hermitian cell form

\[
 \mathcal I_k((a,b),(c,d))
 =\overline a c+(\overline a d+\overline b c)\lambda_k
   +\overline b d\tau_k.                                           \tag{41.10}
\]

Let

\[
 X_k=(\ell_n,b_{n,T}(k)),\qquad Y_k=(m_n,M_{n,k}),
 \qquad Z_{\rho,k}=(0,z_\rho(k)).                                 \tag{41.11}
\]

For a finite cutoff `K>=n`, define the complete-cell prefix

\[
 H_{n,T,K}=\sum_{k=1}^{K}
 \left\{\mathcal I_k\left(X_k-\sum_\rho Z_{\rho,k},
                            X_k-\sum_\rho Z_{\rho,k}\right)
             -C\mathcal I_k(Y_k,Y_k)\right\}.                     \tag{41.12}
\]

Adjoin an affine index `star` and set every coordinate `a_star=a_rho=1`.
Then

\[
 \boxed{H_{n,T,K}=a^*\mathcal K^{(n,T,K)}a}                        \tag{41.13}
\]

for the Hermitian matrix

\[
 \mathcal K_{\star\star}^{(n,T,K)}
 =\sum_{k=1}^{K}\{\mathcal I_k(X_k,X_k)-C\mathcal I_k(Y_k,Y_k)\}, \tag{41.14}
\]

\[
 \mathcal K_{\star\rho}^{(n,T,K)}
 =-\sum_{k=1}^{K}\mathcal I_k(X_k,Z_{\rho,k})
 =-\sum_{k=1}^{K}z_\rho(k)\{\ell_n\lambda_k+b_{n,T}(k)\tau_k\}, \tag{41.15}
\]

\[
 \mathcal K_{\rho\star}^{(n,T,K)}
 =\overline{\mathcal K_{\star\rho}^{(n,T,K)}},                   \tag{41.16}
\]

and

\[
 \boxed{\mathcal K_{\rho\sigma}^{(n,T,K)}
 =\sum_{k=1}^{K}\tau_k\overline{z_\rho(k)}z_\sigma(k)
 = {1\over\overline\rho\sigma}
   \sum_{k=1}^{K}{k^{\overline\rho+\sigma}\over k(k+1)}.}       \tag{41.17}
\]

The zero-zero block is positive semidefinite: it comes only from `||D_n||^2`.
All negative `-C||U_n||^2` mass is in the affine entry because `U_n` is an
exact finite Mobius vector, not a zero expansion. The half-strength mixed-term
cancellation therefore does not simplify, subtract, or sign-change the pure
zero kernel. It only removes the `U-D` cross channel before zero coordinates
are introduced.

The full norm defect is recovered in the ordered endpoint-safe limit

\[
 \boxed{H_n=\lim_{K\to\infty}H_{n,T,K}}                            \tag{41.18}
\]

for every fixed finite `T`, because `r_T` was defined by exact equality.
Formula (41.18) is independent of `T`; changing `T` only moves content between
the affine coordinate and the finite zero coordinates. One must not let the
individual entries in (41.14)--(41.17) tend to infinity separately: their
large-`k` cancellation occurs only after the affine contraction (41.13).

## 4. RH diagonal and the conjugate-diagonal sign

Under RH write `rho_gamma=1/2+i gamma`. Equation (41.17) becomes

\[
 \mathcal K_{\gamma\eta}^{(n,T,K)}
 ={1\over(1/2-i\gamma)(1/2+i\eta)}
   \sum_{k=1}^{K}{k^{i(\eta-\gamma)}\over k+1}.                    \tag{41.19}
\]

Its Hermitian diagonal is strictly positive:

\[
 \boxed{\mathcal K_{\gamma\gamma}^{(n,T,K)}
 ={H_{K+1}-1\over1/4+\gamma^2}>0.}                                \tag{41.20}
\]

In the original bilinear expansion of the real zero sum, (41.20) is exactly
the conjugate pair `rho_gamma+rho_(-gamma)=1`: complex conjugation in the
Hermitian convention turns that conjugate pair into the ordinary matrix
diagonal. Its sign is therefore positive, not negative.

There is a different object produced by the anti-diagonal of the Hermitian
matrix. Pairing the coordinate indexed by `rho_gamma` with that indexed by
`rho_(-gamma)=bar(rho_gamma)` gives

\[
 \boxed{\mathcal K_{\gamma,-\gamma}^{(n,T,K)}
 ={1\over(1/2-i\gamma)^2}
   \sum_{k=1}^{K}{k^{-2i\gamma}\over k+1}.}                         \tag{41.21}
\]

Its real contribution is

\[
 2\Re\mathcal K_{\gamma,-\gamma}^{(n,T,K)},                       \tag{41.22}
\]

which has no fixed sign. Thus the true conjugate-zero diagonal is the positive
Hermitian diagonal (41.20); the Hermitian anti-diagonal represents same-sign
pairs in the original bilinear expansion and is oscillatory. This is the
opposite sign from the earlier dyadic shell decrement, whose pure zero kernel
is a difference of two scale Grams and has an eventually negative conjugate
diagonal. The distinction is caused by the observable, not by a
zero-conjugation convention.

## 5. Relation to the second coefficient

The exact recurrence gives

\[
 L_+P_{n+1}-LP_n=-{(L_+-L)H_n\over LL_+}.                           \tag{41.23}
\]

If

\[
 P_n={C_0\over L}+{D_{\rm restricted}\over L^2}+o(L^{-2}),         \tag{41.24}
\]

with sufficient regularity to difference the remainder, then direct expansion
of (41.23) yields

\[
 \boxed{H_n=D_{\rm restricted}+o(1).}                              \tag{41.25}
\]

Cycle 40 found `D_restricted=D_full-1`, so equivalently

\[
 \boxed{\lim_{n\to\infty}H_n=D_{\rm full}-1}                     \tag{41.26}
\]

conditionally on existence of the scalar second coefficient and a
difference-stable remainder. Hence eventual positivity of `H_n` would demand
`D_full>1`, exactly the second-order critical-tail target. If persistent
nonzero-frequency zero pairs prevent a scalar coefficient, (41.26) must be
replaced by a pointwise/liminf statement for `H_n`; neither the positive
finite zero kernel nor half-strength cancellation supplies that sign by
itself.

## 6. Verdict

The full endpoint-safe finite-zero representation is the augmented affine
Gram form (41.13)--(41.17). Half-strength cancellation simplifies the norm
defect before expansion, but it does not simplify the pure zero-zero kernel:
that kernel is the ordinary positive Gram (41.17). Its
conjugate-zero/Hermitian diagonal is positive, while its Hermitian
anti-diagonal (the original same-sign pairing) is sign-indefinite. The desired
asymptotic sign resides in the cancellation of this positive zero block against
the affine row and endpoint packet; conditionally, the surviving finite part
is precisely the restricted second coefficient `D_full-1` through (41.25).
No positivity theorem or RH result is claimed.
