# Finite-zero Gram form for the recombined shell-square difference

## 1. Exact shell packet and conventions

Let `N` be even, put

\[
 n=N/2,\qquad m=N-1,\qquad L=\log N,\qquad L_2=\log(2N),
 \qquad w_k={N\over k(k+1)}\quad(n\leq k\leq m),
\]

and use the Hermitian inner product

\[
 \langle f,g\rangle_W=\sum_{k=n}^m w_k\overline{f_k}g_k.
\]

Define

\[
 \vartheta_k={k\over2k+1},\qquad
 E_k=\psi(k)-k,
 \qquad F_k=\psi(2k)+\vartheta_k\Lambda(2k+1)-2k,
\]

\[
 p_k=k\left(A_N-{1\over L}\right),
 \qquad
 (p+h)_k=2k\left(A_{2N}-{1\over L_2}\right)
                 +\vartheta_kA_{2N}.
\]

Thus `x_k=E_k/L`, `y_k=F_k/L_2`, and the invariant recombined
shell-square difference is

\[
 \boxed{D_N=\|p-x\|_W^2-\|p+h-y\|_W^2-R_{\rm jump}},                 \tag{1}
\]

where every odd-pair endpoint correction is retained in

\[
 \boxed{R_{\rm jump}=
 \sum_{k=n}^m {N\over(2k+1)^2}
 \left(A_{2N}-{\Lambda(2k+1)\over L_2}\right)^2.}                  \tag{2}
\]

In the established normalization, (1) is exactly `E_N-E_(2N)`. The sums
include both shell endpoints `k=n,m`; the bulk argument in `F_k` stops at
`2m=2N-2`, while the separate interpolation endpoint reaches `2m+1=2N-1`.

## 2. Endpoint-safe finite explicit formula

For integer `q>1`, let

\[
 \psi_0(q)=\psi(q)-{1\over2}\Lambda(q),
\]

the symmetric value at a prime-power discontinuity. For a cutoff `T>0` which
is not a zero ordinate, let `Z(T)` be the multiset of nontrivial zeros with
`|Im rho|<=T`, counted with multiplicity and closed under conjugation, and put

\[
 Z_T(q)=\sum_{\rho\in Z(T)}{q^\rho\over\rho}.
\]

This is a finite symmetric sum. Define the finite explicit-formula remainder
by the exact equality

\[
 \boxed{r_T(q)=\psi(q)-q-B(q)+Z_T(q)},                              \tag{3}
\]

where

\[
 \boxed{B(q)=-\log(2\pi)-{1\over2}\log(1-q^{-2})
                    +{1\over2}\Lambda(q).}                         \tag{4}
\]

Equivalently,

\[
 \psi(q)-q=B(q)-Z_T(q)+r_T(q).                                    \tag{5}
\]

Formula (4) contains all three non-oscillatory endpoint terms: the constant,
the complete trivial-zero contribution, and the half-`Lambda(q)` correction
which converts `psi_0(q)` back to the right-continuous `psi(q)`. No limiting
zero sum or infinite product occurs in (3)-(5).

The two shell errors are therefore

\[
 E_k=B(k)-Z_T(k)+r_T(k),                                           \tag{6}
\]

\[
 F_k=B(2k)+\vartheta_k\Lambda(2k+1)-Z_T(2k)+r_T(2k).               \tag{7}
\]

The half-`Lambda(2k)` term in `B(2k)` and the full interpolated
`vartheta_k Lambda(2k+1)` term in (7) are distinct and must not be merged.

## 3. Finite-zero affine Gram representation

For each retained zero define shell vectors

\[
 \phi_\rho(k)={k^\rho\over L\rho},
 \qquad
 \chi_\rho(k)={(2k)^\rho\over L_2\rho}.                            \tag{8}
\]

Put

\[
 d_{0,k}=p_k-{B(k)\over L},                                       \tag{9}
\]

\[
 d_{1,k}=(p+h)_k-
 {B(2k)+\vartheta_k\Lambda(2k+1)\over L_2}.                       \tag{10}
\]

The zero-truncated vectors are

\[
 g_{0,T}=d_0+\sum_{\rho\in Z(T)}\phi_\rho,
 \qquad
 g_{1,T}=d_1+\sum_{\rho\in Z(T)}\chi_\rho.                      \tag{11}
\]

Define the finite weighted power sum

\[
 S_N(z)=\sum_{k=n}^m {N k^z\over k(k+1)}.                          \tag{12}
\]

Then the required Hermitian zero kernel is

\[
 \boxed{K^{(N)}_{\rho\sigma}=
 {S_N(\overline\rho+\sigma)\over L^2\overline\rho\sigma}
 -{2^{\overline\rho+\sigma}S_N(\overline\rho+\sigma)
       \over L_2^2\overline\rho\sigma}.}                         \tag{13}
\]

The finite linear coefficient and zero-free constant are

\[
 q^{(N)}_\rho=\langle d_0,\phi_\rho\rangle_W
                    -\langle d_1,\chi_\rho\rangle_W,             \tag{14}
\]

\[
 c_N=\|d_0\|_W^2-\|d_1\|_W^2-R_{\rm jump}.                       \tag{15}
\]

Consequently the completely finite zero Gram value is

\[
 \boxed{D_{N,T}=c_N+2\Re\sum_{\rho\in Z(T)}q^{(N)}_\rho
 +\sum_{\rho,\sigma\in Z(T)}K^{(N)}_{\rho\sigma}
 =\|g_{0,T}\|_W^2-\|g_{1,T}\|_W^2-R_{\rm jump}.}                \tag{16}
\]

Equation (16), rather than a product over zeros, is the desired finite
affine Gram representation. The matrix is a difference of two positive
semidefinite Gram matrices and is not itself asserted to be positive.

Equivalently, adjoining an affine index `star`, let `a_star=1` and
`a_rho=1` for every retained zero, and define the Hermitian matrix

\[
 \mathcal K^{(N)}_{\star\star}=c_N,
 \qquad \mathcal K^{(N)}_{\star\rho}=q^{(N)}_\rho,
 \qquad \mathcal K^{(N)}_{\rho\star}=\overline{q^{(N)}_\rho},
 \qquad \mathcal K^{(N)}_{\rho\sigma}=K^{(N)}_{\rho\sigma}.         \tag{16a}
\]

Then `D_(N,T)=a^* mathcal K^(N) a`. This augmented matrix includes the
deterministic, trivial-zero, half-`Lambda`, odd interpolation, and jump-square
terms; the zero-by-zero block is exactly (13).

## 4. Diagonal and off-diagonal ordinates under RH

Under RH write `rho_gamma=1/2+i gamma`. For retained ordinates `gamma,eta`,

\[
 \boxed{K^{(N)}_{\gamma\eta}=
 {S_N(1+i(\eta-\gamma))\over
   (1/2-i\gamma)(1/2+i\eta)}
 \left({1\over L^2}-{2^{1+i(\eta-\gamma)}\over L_2^2}\right).}    \tag{17}
\]

The diagonal is explicit:

\[
 \boxed{K^{(N)}_{\gamma\gamma}=
 {N(H_N-H_n)\over 1/4+\gamma^2}
 \left({1\over L^2}-{2\over L_2^2}\right).}                     \tag{18}
\]

For `gamma != eta`, (17) is the off-diagonal lag kernel. Its arithmetic
content is the finite Mellin shell sum `S_N(1+i(eta-gamma))`; its dyadic phase
is exactly

\[
 2^{i(\eta-\gamma)}=e^{i(\eta-\gamma)\log2}.                       \tag{19}
\]

Thus the only new phase introduced by recombination is the zero-ordinate
difference sampled at lag `log 2`. The factors `1/rho`, the unequal
normalizations `L,L_2`, and the finite shell sum prevent replacement of this
kernel by a translation-invariant cosine matrix. Since `Z(T)` contains both
signs of every ordinate, (16) is real; one may fold to positive ordinates only
after combining all four sign pairs explicitly.

## 5. Exact finite truncation correction

From (3), (6), and (7), define

\[
 \epsilon_{0,T}(k)=-{r_T(k)\over L},
 \qquad
 \epsilon_{1,T}(k)=-{r_T(2k)\over L_2}.                            \tag{20}
\]

Then no limiting argument is needed:

\[
 p-x=g_{0,T}+\epsilon_{0,T},
 \qquad p+h-y=g_{1,T}+\epsilon_{1,T},                              \tag{21}
\]

and hence

\[
\boxed{\begin{aligned}
 D_N-D_{N,T}={}&2\Re\langle g_{0,T},\epsilon_{0,T}\rangle_W
                 +\|\epsilon_{0,T}\|_W^2\\
 &-2\Re\langle g_{1,T},\epsilon_{1,T}\rangle_W
                 -\|\epsilon_{1,T}\|_W^2.
\end{aligned}}                                                    \tag{22}
\]

If validated pointwise enclosures `|r_T(q)|<=R_T(q)` are available, set

\[
 \eta_0^2=\sum_{k=n}^m w_k{R_T(k)^2\over L^2},
 \qquad
 \eta_1^2=\sum_{k=n}^m w_k{R_T(2k)^2\over L_2^2}.                 \tag{23}
\]

A simple certificate enclosure is

\[
 \boxed{|D_N-D_{N,T}|\leq
 2\|g_{0,T}\|_W\eta_0+\eta_0^2
 +2\|g_{1,T}\|_W\eta_1+\eta_1^2.}                               \tag{24}
\]

For a sharper certificate, interval-evaluate the four terms in (22) using
the individual signed balls for `r_T(k)` and `r_T(2k)`; (24) should be only a
fallback norm bound.

There are two rigorous ways to supply these remainder balls.

1. **Finite arithmetic remainder.** Evaluate `psi(q)=sum_(a<=q) Lambda(a)`
   with exact prime-power endpoints, evaluate the certified finite zero sum,
   and use (3) directly. This gives an identity-level finite certificate and
   requires no estimate for omitted zeros.
2. **Analytic tail remainder.** Use a stated effective truncated explicit-
   formula theorem, with its numerical constants, endpoint convention, and
   hypotheses, to enclose each `r_T(q)`. A bare
   `O(q log^2(qT)/T)` is not certificate data. The certificate must store the
   resulting numerical balls `R_T(q)` (or stronger signed intervals) for all
   `q` in `{n,...,m} union {2n,2n+2,...,2m}`.

The first route is preferable for auditing a fixed finite `N`; the second is
needed only when the certificate is intended to derive a uniform consequence
without directly summing `Lambda` through `2N`.

## 6. Data required for a rigorous certificate

A checkable finite certificate must include:

1. `N`, the exact definitions or certified balls for `A_N,A_(2N)`, and the
   exact `Lambda(k),Lambda(2k),Lambda(2k+1)` endpoint values used in
   (2), (4), and (10).
2. A cutoff `T` separated from every zero ordinate, isolating complex balls
   for every retained zero with multiplicity, and a zero-count/completeness
   certificate proving that the symmetric list is exactly `Z(T)`. Under an
   RH-conditional certificate, it must additionally certify `Re rho=1/2` for
   every retained zero or explicitly declare this as an assumption.
3. Directed-rounding evaluations of the finite sums (12)-(16), including
   conjugate closure. Zero-coordinate uncertainty must be propagated through
   `q^rho/rho=exp(rho log q)/rho`, using the real logarithm of positive `q`;
   midpoint ordinates alone are insufficient. The resulting interval matrix
   need not be tested for positive semidefiniteness: its two constituent Gram
   blocks should instead be evaluated from their finite vector factors.
4. Pointwise remainder intervals from (3), or from one identified effective
   explicit-formula theorem, followed by the exact correction (22) or the
   weaker enclosure (24).
5. A final interval for `D_N` whose relevant endpoint has the strict desired
   sign. Neither a numerically positive eigenvalue of one Gram block nor the
   diagonal (18) alone certifies the sign of the difference (16).

All objects in this construction are finite sums. In particular, no Hadamard
product, formal product over ordinates, interchange of an unbounded zero sum
with the shell square, or unquantified truncation is used.
