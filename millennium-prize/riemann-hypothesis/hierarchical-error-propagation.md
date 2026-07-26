# Certifiable hierarchical error propagation for symmetric kernel forms

## 1. Scope

Let `I` be a finite index set, let `K=K^T` be a real symmetric kernel matrix,
and let

\[
Q(c)=c^TKc=\sum_{i,j\in I}c_ic_jK(x_i,x_j).
\]

This note gives deterministic error bounds for a hierarchical approximation of
`Q(c)`. The bounds are coefficient-aware: every admissible block uses the local
`l1` or `l2` norm of the coefficients actually meeting that block. They also
distinguish cancellation that can be certified from cancellation that is only
hoped for. The final section specializes the formulas to the reduced rational
Fourier coefficients of the logarithmically tapered Mobius vectors in this
project.

No asymptotic estimate for the Mobius sums is asserted here. This is a
certification theorem, not an RH-strength cancellation theorem.

## 2. Symmetric hierarchical block convention

Let `P+` be a collection of blocks `b=(A,B)` with the following properties.

1. Each block is either diagonal (`A=B`) or has a fixed canonical ordering
   `A<B`.
2. The sets `A x A` for diagonal blocks, together with both `A x B` and
   `B x A` for off-diagonal blocks, form a disjoint partition of `I x I`.
3. The approximation is symmetric: on the transpose block,
   `Ktilde_BA=Ktilde_AB^T`.

These are the leaf blocks of the hierarchy. Internal tree blocks are not
additional summands. This point matters when different levels overlap.

Put

\[
E_{AB}=K_{AB}-\widetilde K_{AB},\qquad
\kappa_{AB}=\begin{cases}1,&A=B,\\2,&A<B.\end{cases}
\]

Then the quadratic-form error has the exact identity

\[
\boxed{
Q(c)-\widetilde Q(c)
=\sum_{(A,B)\in P_+}\kappa_{AB}c_A^TE_{AB}c_B.}
\tag{2.1}
\]

Thus an off-diagonal block stored once receives a factor of two. A diagonal
block does not. Within a diagonal block, `c_A^TE_AAc_A` already counts its
internal off-diagonal entries twice; inserting another factor of two is an
error.

If the two orientations were approximated independently, (2.1) cannot be used
until they are symmetrized. A safe replacement is

\[
\widetilde K_{AB}^{sym}
=\tfrac12(\widetilde K_{AB}+\widetilde K_{BA}^T),
\]

with the rounding and approximation error of this operation included in the
certificate.

## 3. Sharp local norm bounds

For a block `A x B`, define

\[
L_1(A)=\|c_A\|_1,\qquad L_2(A)=\|c_A\|_2.
\]

Suppose a residual matrix `R_AB` has certified bounds

\[
\|R_{AB}\|_{max}\le\epsilon_{AB}^{(\infty)},
\qquad
\|R_{AB}\|_{2\to2}\le\epsilon_{AB}^{(2)},
\]

and optionally

\[
\max_{i\in A}\|R_{iB}\|_2\le\epsilon_{AB}^{(1,2)},
\qquad
\max_{j\in B}\|R_{Aj}\|_2\le\epsilon_{AB}^{(2,1)}.
\]

Holder and Cauchy--Schwarz give

\[
|c_A^TR_{AB}c_B|
\le \epsilon_{AB}^{(\infty)}L_1(A)L_1(B),
\tag{3.1}
\]

and

\[
|c_A^TR_{AB}c_B|
\le \epsilon_{AB}^{(2)}L_2(A)L_2(B).
\tag{3.2}
\]

The row and column bounds give the mixed estimates

\[
|c_A^TR_{AB}c_B|
\le \epsilon_{AB}^{(1,2)}L_1(A)L_2(B),
\qquad
|c_A^TR_{AB}c_B|
\le \epsilon_{AB}^{(2,1)}L_2(A)L_1(B).
\tag{3.3}
\]

If several bounds certify the same residual, one may take

\[
\boxed{
\beta_{AB}=\min\{\epsilon_{AB}^{(\infty)}L_1(A)L_1(B),
\epsilon_{AB}^{(2)}L_2(A)L_2(B),
\epsilon_{AB}^{(1,2)}L_1(A)L_2(B),
\epsilon_{AB}^{(2,1)}L_2(A)L_1(B)\}.}
\tag{3.4}
\]

A certified Frobenius bound may replace the spectral bound because
`||R||_2<=||R||_F`. Bounds for different pieces of a decomposition must be
added, not minimized.

Each of (3.1)--(3.3) is worst-case sharp from the corresponding information
alone.
In particular, signs in `c` do not improve (3.1) when every residual entry is
known only to lie in the symmetric interval `[-epsilon,epsilon]`: an adversarial
residual can choose the sign of `R_ij` to match `c_i c_j`.

For pure norm certificates, (2.1) immediately yields

\[
|Q-\widetilde Q|
\le \sum_{(A,B)\in P_+}\kappa_{AB}
\beta_{AB}.
\tag{3.5}
\]

This can be much smaller than
`max_AB epsilon_AB * ||c||_1^2`, especially when difficult near-diagonal
blocks meet little coefficient mass.

## 4. Rigorous uses of signed cancellation

### 4.1 Entry intervals

Suppose every independent residual entry is enclosed. For `A<B`, let
`E_ij in [ell_ij,u_ij]`. Then exact interval evaluation gives

\[
c_A^TE_{AB}c_B\in
\sum_{i\in A,j\in B}c_ic_j[\ell_{ij},u_{ij}].
\tag{4.1}
\]

For `A=A`, symmetry gives instead

\[
c_A^TE_{AA}c_A\in
\sum_{i\in A}c_i^2[\ell_{ii},u_{ii}]
+2\sum_{i<j\atop i,j\in A}c_ic_j[\ell_{ij},u_{ij}].
\tag{4.2}
\]

Equations (4.1)--(4.2) are the strongest elementary entrywise certificates and
make the diagonal/off-diagonal multiplicities explicit. They are generally too
expensive for a large compressed block, but are appropriate for dense near
leaves.

### 4.2 Certified separated error structure

The main cancellation mechanism for compressed blocks is a rigorous separated
description of the error. Suppose

\[
E_{AB}=Z_{AB}+
\sum_{\nu=1}^s\theta_\nu f_\nu g_\nu^T+R_{AB},
\qquad \theta_\nu\in[\underline\theta_\nu,\overline\theta_\nu],
\tag{4.3}
\]

where `Z_AB` is exactly known or interval-enclosed and `R_AB` satisfies one or
more bounds from Section 3. Define the signed local moments

\[
X_\nu(A)=\sum_{i\in A}c_i f_\nu(x_i),
\qquad
Y_\nu(B)=\sum_{j\in B}c_j g_\nu(x_j).
\tag{4.4}
\]

Outward-rounded interval arithmetic gives

\[
\boxed{
c_A^TE_{AB}c_B\in
c_A^TZ_{AB}c_B+
\sum_{\nu=1}^s
[\underline\theta_\nu,\overline\theta_\nu]X_\nu(A)Y_\nu(B)
+[-\beta_{AB},\beta_{AB}].}
\tag{4.5}
\]

Formula (4.5) preserves cancellation inside each signed moment and between the
known centers of the separated terms. Examples include exact cancellation of a
constant residual mode when `sum_(i in A)c_i=0`, or of polynomial modes when
the corresponding signed moments vanish. Such cancellation is valid only when
the error representation (4.3) proves that the residual lies in those modes
plus the certified remainder.

For a diagonal block, the separated representation should itself be symmetric,
or be replaced by its symmetric part. A term `f g^T` then contributes through
the symmetric combination `(f g^T+g f^T)/2`; its quadratic form is the product
of the two signed moments.

### 4.3 What cannot be cancelled

Unknown residual intervals from different blocks may be perfectly correlated
and may all attain their adverse endpoints. Consequently:

- do not use root-sum-square accumulation without a proved probabilistic model;
- do not cancel symmetric radii because neighboring block centers have
  opposite signs;
- do not infer small error from `sum c_i`, unless the residual is certified to
  be constant or nearly constant in the relevant variable;
- do not treat floating-point SVD singular values as spectral error bounds.

## 5. Global certification theorem

### Theorem 5.1 (coefficient-aware symmetric hierarchy)

Assume the symmetric leaf partition of Section 2. For every stored leaf block
`b=(A,B)`, let interval arithmetic certify

\[
\delta_b:=c_A^T(K_{AB}-\widetilde K_{AB})c_B\in I_b.
\]

The interval `I_b` may be obtained from (3.4), (4.1), (4.2), (4.5), or the
intersection of any independently certified enclosures. Then

\[
\boxed{
Q(c)\in \widetilde Q(c)+
\sum_{b\in P_+}\kappa_b I_b.}
\tag{5.1}
\]

All sums in (5.1) are outward-rounded interval sums. In particular, if

\[
I_b=[m_b-r_b,m_b+r_b],
\]

then

\[
Q(c)-\widetilde Q(c)\in[M-R,M+R],
\quad
M=\sum_b\kappa_bm_b,
\quad
R=\sum_b\kappa_br_b,
\tag{5.2}
\]

and hence

\[
|Q(c)-\widetilde Q(c)|\le |M|+R.
\tag{5.3}
\]

The center `M` is summed before taking its absolute value. This retains all
rigorously resolved signed cancellation across blocks. The radii are summed
absolutely, which is unavoidable without additional dependence information.

*Proof.* Identity (2.1) is exact. Scalar multiplication of each certified block
interval by the positive integer `kappa_b`, followed by interval addition,
preserves inclusion. Equations (5.2)--(5.3) are the center-radius form of the
resulting interval. QED.

### Corollary 5.2 (one-sided decision certificate)

If the target is to prove `Q(c)<=T`, it suffices that the outward-rounded upper
endpoint in (5.1) is at most `T`. There is no need to certify a small relative
error when `Q` is close to zero; an absolute one-sided enclosure is the correct
object.

### Optional global `l2` check

When a fixed disjoint cluster partition `C_1,...,C_s` is used and
`||R_rs||_2<=eta_rs=eta_sr`, put `z_r=||c_(C_r)||_2`. Then

\[
|c^TRc|\le z^T\eta z
\le \rho(\eta)||c||_2^2.
\tag{5.4}
\]

A completely elementary upper bound for the last spectral radius is the
weighted Schur bound

\[
\rho(\eta)\le
\max_r\frac1{w_r}\sum_s\eta_{rs}w_s
\quad(w_r>0).
\tag{5.5}
\]

This is useful as an independent audit. For a genuinely nonuniform H-matrix
leaf partition, (3.5) is the direct bound and does not require forcing all
leaves onto one level.

## 6. Reduced rational Mobius coefficients

Let

\[
\beta_a(t)=\{t/a\}-\tfrac12,
\qquad
g_u(t)=m_u+\sum_{a\le N}u_a\beta_a(t),
\]

and define the exact divisor aggregate

\[
U_q(u)=\sum_{j\le N/q}\frac{u_{qj}}j.
\tag{6.1}
\]

At the reduced positive frequency `lambda=p/q`, `(p,q)=1`, the sine amplitude
is

\[
\boxed{a_{p,q}(u)=-\frac{U_q(u)}{\pi p}.}
\tag{6.2}
\]

If a finite realization uses a certified multiplier `w_(p,q)` depending only
on the reduced mode, define the weighted amplitude

\[
a^{(w)}_{p,q}(u)=-\frac{w_{p,q}U_q(u)}{\pi p}.
\tag{6.2a}
\]

This factorization is not valid for a multiplier imposed on the original
unreduced harmonic. For example, an Abel factor `r^(pj)` gives instead

\[
-\frac1{\pi p}\sum_{j\le N/q}\frac{u_{qj}}j r^{pj}.
\]

Duplicate representations may be combined only after their actual multipliers
have been included.

For the logarithmic Mobius taper

\[
u_a^{(N)}=\mu(a)\frac{\log(N/a)}{\log N},
\tag{6.3}
\]

one has the exact finite formula

\[
U_q=
\begin{cases}
\displaystyle
\frac{\mu(q)}{\log N}
\sum_{j\le N/q\atop(j,q)=1}
\frac{\mu(j)}j\log\frac{N}{qj},&q\text{ squarefree},\\[3mm]
0,&q\text{ not squarefree}.
\end{cases}
\tag{6.4}
\]

Thus nonsquarefree denominator clusters carry no oscillatory coefficient for
this Mobius vector. They may be removed only after every channel sharing the
hierarchy has been checked.

For any frequency block `A`, its exact local masses are

\[
\boxed{
L_1(A)=\frac1\pi\sum_{(p,q)\in A}
\frac{|w_{p,q}U_q|}{p},
\qquad
L_2(A)^2=\frac1{\pi^2}\sum_{(p,q)\in A}
\frac{|w_{p,q}U_q|^2}{p^2}.}
\tag{6.5}
\]

These are the quantities to insert into (3.4), not a global upper bound such as
`sum |u_a|`. They can be enclosed using directed intervals for logarithms and
`pi`. One may alternatively absorb `1/pi^2` into the kernel and retain
rational coefficient numerators whenever the chosen multipliers are rational.

The signed moments in (4.4) take the denominator-aggregated form

\[
\boxed{
\sum_{(p,q)\in A}a^{(w)}_{p,q}(u)f(p/q)
=-\frac1\pi\sum_qU_q
\sum_{\substack{p\ge1:(p,q)\in A\\(p,q)=1}}
\frac{w_{p,q}}p f(p/q).}
\tag{6.6}
\]

Equation (6.6) is the rigorous place to exploit Mobius cancellation. The inner
and outer signed sums must be evaluated, with outward rounding, before an
absolute value is taken. In contrast, the final unstructured remainder in
(3.1) still requires the local `L1(A)L1(B)` product.

For the tail kernel already derived in the notebook,

\[
K_Q(\omega,\nu)=\int_Q^\infty
\sin(\omega t)\sin(\nu t)t^{-2}\,dt,
\]

the frequency locations are `omega=2 pi p/q`. Dense overlapping or near blocks
can use (4.1)--(4.2) with interval evaluation of the exact kernel. Separated
blocks can use the certified analytic expansion from Lemma 9 of the notebook,
arranged in the form (4.3). Polynomial, Chebyshev, or inverse-power basis
moments should be accumulated by (6.6).

## 7. Direct endpoint functional

The oscillatory--oscillatory part of the endpoint integrand uses two
coefficient vectors, say `a(u)` and `a(d)`, in

\[
2a(u)^TKa(d)-\alpha a(d)^TKa(d).
\tag{7.1}
\]

It is important to certify (7.1) directly rather than separately enclosing
three large terms. Introduce a two-channel coefficient vector and the channel
matrix

\[
H_\alpha=\begin{pmatrix}0&1\\1&-\alpha\end{pmatrix}.
\]

Then (7.1) is the symmetric quadratic form with kernel `H_alpha tensor K`.
Theorem 5.1 applies verbatim on the augmented index set. In a separated error
expansion on `A x B`, evaluate the channel combination

\[
X_\nu(A;u)Y_\nu(B;d)+X_\nu(A;d)Y_\nu(B;u)
-\alpha X_\nu(A;d)Y_\nu(B;d)
\tag{7.2}
\]

inside one interval expression before taking absolute values. For a symmetric
rank-one term on the full index set, the first two products coincide and give
`2X_nu(u)X_nu(d)`. This preserves
the exact absence of the large `U_s^2` term identified in the reduced-frequency
mean. Certifying the two quadratic pieces independently would discard that
cancellation.

The constant--constant and constant--oscillatory terms of the full endpoint
tail are separate finite expressions and must also be included in a complete
certificate; (7.1) is not by itself the entire tail functional.

Write the constant terms of the two fields as `m,n` and their sine amplitudes
as `A_lambda,B_lambda`. The complete tail is

\[
\begin{aligned}
\mathcal T_Q={}&\frac{2mn-\alpha n^2}{Q}\\
&+2\sum_\lambda[nA_\lambda+(m-\alpha n)B_\lambda]S_Q(\omega_\lambda)\\
&+2\sum_{\lambda,\mu}A_\lambda B_\mu K_Q(\omega_\lambda,\omega_\mu)
-\alpha\sum_{\lambda,\mu}B_\lambda B_\mu K_Q(\omega_\lambda,\omega_\mu),
\end{aligned}
\tag{7.3}
\]

where

\[
S_Q(\omega)=\int_Q^\infty\sin(\omega t)t^{-2}\,dt
=\frac{\sin(Q\omega)}Q-\omega\operatorname{Ci}(Q\omega).
\tag{7.4}
\]

Thus the constant--sine term is a linear reduced-frequency sum. With
unweighted aggregates it is exactly

\[
-\frac2\pi\sum_q\sum_{\substack{p\ge1\\(p,q)=1}}
\frac{nU_q+(m-\alpha n)D_q}{p}S_Q(2\pi p/q).
\tag{7.5}
\]

It can be enclosed using `Ci` or the imaginary projection of the endpoint
expansion. The constant--sine period mean is zero, while equal-frequency sine
products have mean `1/2`; hence (7.3) recovers the exact reduced period mean.

## 8. Minimal certificate payload

A reproducible hierarchy certificate should record:

1. the sorted reduced frequencies and outward enclosures of their locations;
2. the coefficient aggregates `U_q` and local masses (6.5);
3. the leaf block list, canonical orientation, and multiplicity `kappa_b`;
4. for each dense leaf, its entrywise error interval or exact kernel interval;
5. for each compressed leaf, the separated center, signed moments, and a
   proved max-norm or spectral residual bound;
6. the outward-rounded approximate form, global center `M`, radius `R`, and
   final one-sided endpoint.

The hostile clustered-rational tests remain essential, but they validate an
implementation rather than replace any item in this payload.

## 9. Consequence for the active program

The error-propagation problem itself is now reduced to a precise local target:
for every geometrically separated frequency block, produce a rigorously
outward-rounded decomposition (4.3) whose residual radius, after multiplication
by the local masses (6.5), is affordable in (5.2). The theorem handles
hierarchical accumulation, symmetry, and signed reduced-frequency moments. It
does not prove that the available analytic expansion attains affordable ranks
at `N=8192`; that remains the computational and approximation-theoretic step.
