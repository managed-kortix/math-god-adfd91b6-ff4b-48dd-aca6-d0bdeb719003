# Cycle 48: canonical complete-prefix geometry and temporal Abel audit

## Status and scope

This note continues the Cycle 47 complete-prefix construction on the fixed
closed interval

\[
 I_0=[1,3/2].
\]

It records exact finite algebra, endpoint-safe temporal Abel identities, a
canonical orthogonalization of the two Cycle 47 generators, and hostile finite
and abstract no-go checks.  No claim of bibliographic priority or of a new
arithmetic theorem is made here.  The recombination \(B_a=Y_a+V_a\), its
orthogonal decomposition, the projection inequalities, and the finite Abel
identities are elementary consequences of the Cycle 47 construction.  The
unresolved arithmetic content is the lower bound in (8.1), or one of the
stronger sufficient targets (8.2) and (5.6).

This note does **not** prove

\[
 D_a(I_0)\gg (\log a)^{-3},
 \qquad
 \liminf_{a\to\infty}\log(a)\frac{D_a(I_0)}{\Delta_a(I_0)}>0,
\]

a moving-projection theorem, a completed-square budget upper bound, or the
Riemann hypothesis.  Every numerical statement below is a finite diagnostic
from the already certified Cycle 47 output.

Fix

\[
 a\in\mathbb Z,\qquad a\ge2,\qquad
 0<\theta<\frac12,\qquad C=2(1-\theta),\qquad \tau=C-1,
\]

put \(L=\log a\), \(M=2a-1\), \(L_n=\log n\), and retain the Cycle 47
definitions

\[
 \delta_n=\log\frac{n+1}{n},\quad
 w_n=1-\frac{L_n}{L_{n+1}},\quad
 A_n=C-w_n,\quad
 \eta_n=\frac{\tau}{A_n},
\]

\[
 b_q(n)=\frac{\log q}{L_n}-\eta_n,
 \qquad
 \alpha_{q,n}=w_nA_nb_q(n).
\]

For physical squarefree rows \(q\in S_a(I_0)\), the exact temporal
contraction is

\[
 \widehat c_a(q)=\sum_{n=q}^{M}\alpha_{q,n}\mathcal K_{q,n}.
 \tag{0.1}
\]

There is no \(n=2a\) term and no extra outer Möbius sign.

## 1. Reconstructed complete-prefix algebra

For \(q\in S_a(I_0)\) and \(q\le n<2a\), define

\[
 \mathcal B_{q,n}
 =\int_1^{n+1}\rho_q(t)Z_n(t)\frac{dt}{t^2}.
\]

Since \(q\ge a\), \(n<2a\le2q\), and hence \(n<2q\).  On every complete
half-open cell \([k,k+1)\), \(1\le k\le n\), the finite convolution
identities give

\[
 U_n(t)=m_nt,
 \qquad
 \mathscr D_n(t)=\ell_nt+\psi(k).
\]

Thus, with

\[
 s_n=\frac{\ell_n}{L_n}-\eta_nm_n,
 \qquad R_n=s_n+\frac1{L_n},
\]

one has the exact cell identity

\[
 \boxed{Z_n(t)=R_nt+\frac{\psi(k)-t}{L_n}.}
 \tag{1.1}
\]

The affine vector in \(U_n\) is essential for (1.1).  Put

\[
 \mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q},
\]

\[
 C_r=\sum_{m<r}\Lambda(m)\log\frac rm,
 \qquad E_r=C_r-(r-1),
\]

and

\[
 \mathfrak j_{q,n}
 =\log\frac{n+1}{q}
 -\sum_{k=q}^{n}\frac{\psi(k)}{k(k+1)}.
\]

Direct cell integration reproduces the Cycle 47 formula

\[
 \boxed{
 \mathcal B_{q,n}
 =\mathfrak a_{q,n}R_n
 +\frac1{L_n}\left(\frac{E_{n+1}}q+\mathfrak j_{q,n}\right).}
 \tag{1.2}
\]

Finite Abel summation gives the endpoint-safe equivalent

\[
 \boxed{
 \mathfrak j_{q,n}
 =\log\frac{n+1}{q}
 -\frac{\psi(q-1)}q
 -\sum_{m=q}^{n}\frac{\Lambda(m)}m
 +\frac{\psi(n)}{n+1}.}
 \tag{1.3}
\]

The final cell is \([n,n+1)\).  There is no half-weight, \(\psi(n+1)\),
\(\Lambda(n+1)\), or temporal \(n=2a\) summand.

The temporal coefficient also has the exact simplification

\[
 \boxed{
 A_nb_q(n)
 =(1-w_n)+A_n\frac{\log(q/n)}{L_n},}
 \tag{1.4}
\]

and hence

\[
 \alpha_{q,n}
 =w_n\left(1-w_n+A_n\frac{\log(q/n)}{L_n}\right).
 \tag{1.5}
\]

## 2. The canonical complete-prefix vector

Cycle 47 defined

\[
 Y_a(q)=\sum_{n=q}^{M}\alpha_{q,n}\frac{E_{n+1}}{qL_n},
\]

\[
 V_a(q)=\sum_{n=q}^{M}\alpha_{q,n}
 \left(\mathfrak a_{q,n}R_n+\frac{\mathfrak j_{q,n}}{L_n}\right),
\]

and the complete tail

\[
 H_a(q)=\sum_{n=q}^{M}\alpha_{q,n}
       (\mathcal K_{q,n}-\mathcal B_{q,n}).
\]

Define the canonical complete-prefix vector

\[
 \boxed{B_a:=Y_a+V_a.}
 \tag{2.1}
\]

Then

\[
 \boxed{
 B_a(q)=\sum_{n=q}^{M}\alpha_{q,n}\mathcal B_{q,n},
 \qquad
 \widehat{\mathbf c}_a=B_a+H_a.}
 \tag{2.2}
\]

This is a structural identity, not a new third generator.  It replaces the
coordinate-dependent split of the prefix by the actual integral over
\([1,n+1]\).

Let

\[
 \mathfrak h_n=1+\ell_n-L_nm_n.
\]

Since

\[
 R_n=\frac{1-w_n}{A_n}m_n+\frac{\mathfrak h_n}{L_n},
\]

(1.2) gives the exact arithmetic packet

\[
 \boxed{
 \begin{aligned}
 B_a(q)={}&\sum_{n=q}^{M}
 w_n(1-w_n)b_q(n)\mathfrak a_{q,n}m_n\\
 &+\sum_{n=q}^{M}\frac{w_nA_nb_q(n)}{L_n}
 \left(
   \mathfrak a_{q,n}\mathfrak h_n
   +\frac{E_{n+1}}q+\mathfrak j_{q,n}
 \right).
 \end{aligned}}
 \tag{2.3}
\]

Every displayed plus sign joins signed arithmetic packets; (2.3) is not a
positivity decomposition.

The tail in (2.2) remains literally

\[
 \mathcal K_{q,n}-\mathcal B_{q,n}
 =\int_{n+1}^{\infty}\rho_q(t)Z_n(t)\frac{dt}{t^2}.
 \tag{2.4}
\]

Equivalently, the complete contraction retains the Cycle 46 gcd formula

\[
 \boxed{
 \mathcal K_{q,n}
 =-\eta_ng_q-\frac{s_n}{q}
 +\sum_{h\mid q}\frac{\mu(h)}h
 \sum_{\substack{r\le\lfloor n/h\rfloor\\(r,q)=1}}
 \mu(r)b_{hr}(n)J(q/h,r).}
 \tag{2.5}
\]

Thus the affine term, restricted correction, exact condition \((r,q)=1\),
every Möbius sign, and full Vasyunin kernel remain present.

## 3. Endpoint-safe temporal Abel formulas

Define the suffix coefficient

\[
 \Sigma_{q,m}=\sum_{n=m}^{M}\frac{\alpha_{q,n}}{L_n},
 \qquad q\le m\le M.
 \tag{3.1}
\]

The exact finite difference

\[
 E_{n+1}-E_n=\psi(n)\delta_n-1
 \tag{3.2}
\]

gives

\[
 \boxed{
 Y_a(q)=\frac1q\left[
 E_q\Sigma_{q,q}
 +\sum_{m=q}^{M}(\psi(m)\delta_m-1)\Sigma_{q,m}
 \right].}
 \tag{3.3}
\]

For the reciprocal-Möbius part put

\[
 u_{q,n}
 =\frac{\alpha_{q,n}\mathfrak a_{q,n}(1-\eta_n)}{\delta_n}
 =\mathfrak a_{q,n}b_q(n)\frac{L_n}{L_{n+1}^2},
 \tag{3.4}
\]

\[
 \omega_{q,q}=u_{q,q}
 +\frac{\alpha_{q,q}\mathfrak a_{q,q}}{L_q},
 \tag{3.5}
\]

and, for \(q<n\le M\),

\[
 \omega_{q,n}=u_{q,n}-u_{q,n-1}
 +\frac{\alpha_{q,n}\mathfrak a_{q,n}}{L_n}.
 \tag{3.6}
\]

Using

\[
 \mathfrak h_n-\mathfrak h_{n+1}=\delta_nm_n
\]

and

\[
 \mathfrak j_{q,n}-\mathfrak j_{q,n-1}
 =\delta_n-\frac{\psi(n)}{n(n+1)},
 \qquad \mathfrak j_{q,q-1}=0,
\]

finite Abel summation gives

\[
 \boxed{
 \begin{aligned}
 V_a(q)={}&
 \sum_{m=q}^{M}
 \left(\delta_m-\frac{\psi(m)}{m(m+1)}\right)\Sigma_{q,m}\\
 &+\sum_{n=q}^{M}\omega_{q,n}\mathfrak h_n
 -u_{q,M}\mathfrak h_{2a}.
 \end{aligned}}
 \tag{3.7}
\]

The terminal sign is minus.  The \(\mathfrak h_{2a}\) value is generated by
Abel summation and is not an \(n=2a\) temporal term.

Combining (3.3) and (3.7),

\[
 \boxed{
 \begin{aligned}
 B_a(q)={}&\frac{E_q}{q}\Sigma_{q,q}\\
 &+\sum_{m=q}^{M}
 \left[
 \frac{\psi(m)\delta_m-1}{q}
 +\delta_m-\frac{\psi(m)}{m(m+1)}
 \right]\Sigma_{q,m}\\
 &+\sum_{n=q}^{M}\omega_{q,n}\mathfrak h_n
 -u_{q,M}\mathfrak h_{2a}.
 \end{aligned}}
 \tag{3.8}
\]

These are exact finite identities.  They do not continue \(1/\zeta\) into
the critical strip.

For completeness, define

\[
 \mathfrak p_{q,n}
 =\frac{C_{n+1}}q
 -\sum_{k=q}^{n}\frac{\psi(k)}{k(k+1)}.
 \tag{3.9}
\]

Then

\[
 \mathfrak p_{q,n}
 =\mathfrak a_{q,n}+\frac{E_{n+1}}q+\mathfrak j_{q,n},
 \tag{3.10}
\]

and

\[
 \boxed{
 \mathfrak p_{q,n}
 =\frac{C_q}{q}
 +\sum_{r=q}^{n}\psi(r)
 \left(\frac{\delta_r}{q}-\frac1{r(r+1)}\right).}
 \tag{3.11}
\]

Every coefficient in the last sum is positive.  Nevertheless, the actual
prefix cell is

\[
 \boxed{
 \mathcal B_{q,n}
 =\mathfrak a_{q,n}s_n+\frac{\mathfrak p_{q,n}}{L_n}.}
 \tag{3.12}
\]

The signed \(s_n\) term cannot be discarded, so (3.11) supplies no lower
bound by itself.

## 4. Canonical orthogonal geometry

Suppress the index \(a\) temporarily.  Let

\[
 \mathsf G=
 \begin{pmatrix}
 \langle Y,Y\rangle&\langle Y,V\rangle\\
 \langle Y,V\rangle&\langle V,V\rangle
 \end{pmatrix},
 \qquad
 z=\binom{\langle Y,\widehat{\mathbf c}\rangle}
              {\langle V,\widehat{\mathbf c}\rangle}.
\]

Put

\[
 B=Y+V,
 \qquad p=\|B\|^2,
 \qquad e=\langle Y,B\rangle.
 \tag{4.1}
\]

Define

\[
 R=
 \begin{cases}
 Y-\dfrac{\langle Y,B\rangle}{\|B\|^2}B,&p=\|B\|^2>0,\\[7pt]
 Y,&p=0,
 \end{cases}
 \qquad r=\|R\|^2.
 \tag{4.2}
\]

When \(p>0\), also put \(\sigma=e/p\).  When \(p=0\), one has \(B=0\)
and \(V=-Y\), so the second branch of (4.2) retains the possible rank-one
span.  In every case,

\[
 B\perp R,
 \qquad
 \operatorname{span}(B,R)=\operatorname{span}(Y,V).
\]

When \(p>0\),

\[
 \boxed{\det\mathsf G=pr.}
 \tag{4.3}
\]

and writing \(Y=\sigma B+R\) and \(V=(1-\sigma)B-R\) gives

\[
 \boxed{
 \operatorname{tr}\mathsf G
 =2r+[\sigma^2+(1-\sigma)^2]p.}
 \tag{4.4}
\]

This displays the coordinate dependence of the Cycle 47 trace criterion.  A
common scaling of the two generators changes both \(\operatorname{tr}\mathsf
G\) and \(\|z\|^2\) while leaving the span and projection energy unchanged.

Define

\[
 u=\langle B,\widehat{\mathbf c}\rangle=z_Y+z_V,
 \qquad
 v=\langle R,\widehat{\mathbf c}\rangle.
\]

Since \(\widehat{\mathbf c}=B+H\),

\[
 \boxed{
 u=p+\langle B,H\rangle,
 \qquad
 v=\langle R,H\rangle.}
 \tag{4.5}
\]

Define the zero-safe quotient

\[
 \Phi(x,d)=
 \begin{cases}
 |x|^2/d,&d>0,\\
 0,&d=0.
 \end{cases}
 \tag{4.6}
\]

The corresponding numerator is automatically zero when its denominator
vanishes.  Orthogonal projection now gives, in every rank,

\[
 \boxed{
 Q_a^{(2)}=\Phi(u,p)+\Phi(v,r).}
 \tag{4.7}
\]

In the full-rank case, if

\[
 \xi=pz_Y-e(z_Y+z_V),
\]

then \(\xi=pv\) and

\[
 \boxed{
 Q_a^{(2)}
 =\frac{(z_Y+z_V)^2}{p}
 +\frac{\xi^2}{p\det\mathsf G}.}
 \tag{4.8}
\]

Only in this full-rank case are both orthogonal-basis projection coefficients
uniquely given by

\[
 \lambda_B=\frac up,
 \qquad
 \lambda_R=\frac vr=\frac{\xi}{\det\mathsf G}.
 \tag{4.9}
\]

The coefficient of \(B\) in the nonorthogonal basis \(\{B,Y\}\) is different;
confusing it with \(u/p\) is a coordinate error.

Finally, in every rank,

\[
 \boxed{
 \begin{aligned}
 D_a(I_0)={}&
 \Phi(p+\langle B,H\rangle,p)
 +\Phi(\langle R,H\rangle,r)\\
 &+\|H-\operatorname{Proj}_{\operatorname{span}(Y,V)}H\|^2.
 \end{aligned}}
 \tag{4.10}
\]

Thus

\[
 D_a(I_0)-Q_a^{(2)}
 =\|H-\operatorname{Proj}_{\operatorname{span}(Y,V)}H\|^2.
 \tag{4.11}
\]

A small residual means only that the perpendicular component of the tail is
small.  It does not mean that \(H\) itself is small.

## 5. Canonical complete-prefix projection

Define

\[
 \mathcal Q_a^{\rm cp}=
 \begin{cases}
 0,&B_a=0,\\[3pt]
 \displaystyle
 \frac{|\langle B_a,\widehat{\mathbf c}_a\rangle|^2}
      {\|B_a\|^2},&B_a\ne0.
 \end{cases}
 \tag{5.1}
\]

Equations (2.2) and (4.7) give the exact rank-safe chain

\[
 \boxed{
 \mathcal Q_a^{\rm cp}
 =\begin{cases}
 \dfrac{|\|B_a\|^2+\langle B_a,H_a\rangle|^2}{\|B_a\|^2},
 &\|B_a\|^2>0,\\[8pt]
 0,&\|B_a\|^2=0,
 \end{cases}
 \le Q_a^{(2)}\le D_a(I_0).}
 \tag{5.2}
\]

This removes the arbitrary internal normalization of \(Y_a,V_a\).  It retains
the complete prefix, complete tail, and signed cross term.

A sufficient split is

\[
 \|B_a\|^2\ge c_0L^{-3},
 \qquad
 \left|1+\frac{\langle B_a,H_a\rangle}{\|B_a\|^2}\right|
 \ge\varepsilon,
 \tag{5.3}
\]

which would imply

\[
 D_a(I_0)\ge\varepsilon^2c_0L^{-3}.
 \tag{5.4}
\]

The square on \(\varepsilon\) is mandatory.  Neither premise in (5.3) is
proved.

The intrinsic one-inequality target is

\[
 \boxed{
 \mathcal Q_a^{\rm cp}\gg L^{-3}}
 \tag{5.5}
\]

for every sufficiently large integer \(a\).  If its first channel cancels,
the exact rank-two fallback remains

\[
 \mathcal Q_a^{\rm cp}
 +\frac{|\langle R_a,H_a\rangle|^2}{\|R_a\|^2}
 \gg L^{-3},
 \tag{5.6}
\]

with the second quotient interpreted as zero when \(R_a=0\).  Equation (5.6)
is exactly \(Q_a^{(2)}\gg L^{-3}\), rewritten in canonical channels.

## 6. Sharp geometric limitations

The identities above do not create an arithmetic lower bound.

### 6.1 Norm-only tail bound

Put \(b=\|B_a\|\) and \(h=\|H_a\|\).  Projection onto the line spanned by
\(B_a\) gives

\[
 \boxed{Q_a^{(2)}\ge(b-h)_+^2.}
 \tag{6.1}
\]

This is sharp from separate norm information alone.  If \(h\le b\), take
\(H=-(h/b)B\).  If \(h\ge b\) and an orthogonal complement is available,
take \(H=-B+R_\perp\) with \(\|R_\perp\|^2=h^2-b^2\).  In the latter case
the full selected projection can vanish.

Thus full rank, the complete \(2\times2\) Gram matrix, and separate prefix and
tail energies do not force retention without a signed correlation theorem.

### 6.2 Trace and full rank

For \(L>1\), take

\[
 Y=L^{-3/2}e_1,
 \qquad V=L^{-3/2}e_2,
 \qquad H=-Y-V+L^{-2}e_3.
\]

Then

\[
 \operatorname{tr}\mathsf G=2L^{-3},
 \qquad \det\mathsf G=L^{-6}>0,
\]

but \(z=0\), \(Q^{(2)}=0\), and \(D=L^{-4}\).  This is an abstract
countermodel, not a physical Möbius example.

Conversely, the Cycle 47 sufficient pair is not necessary.  Taking

\[
 \widehat{\mathbf c}=L^{-3/2}e_1,
 \quad Y=L^{-2}e_1,
 \quad V=L^{-2}e_2,
 \quad H=\widehat{\mathbf c}-Y-V
\]

gives \(Q^{(2)}=L^{-3}\) while \(\|z\|^2=L^{-7}=o(L^{-6})\).

### 6.3 High capture does not make the tail negligible

From (4.10), high \(Q^{(2)}/D\) controls only the perpendicular tail.  A tail
of large norm may lie almost entirely inside the generator span.  Therefore no
finite high-capture ratio justifies dropping \(H_a\) or its parallel cross
terms.

### 6.4 Fixed-cutoff zero packets

A fixed finite conjugate-closed set of distinct simple critical-line modes has
a positive finite Gram floor on the fixed log interval: distinct exponential
modes are linearly independent.  This prevents internal cancellation inside
that fixed packet.  It does not control cancellation by the common signed
affine remainder, omitted zeros, off-line zeros, or the physical tail.
Moreover the least frame eigenvalue cannot remain uniform as the cutoff grows,
because the number of critical-line modes up to height \(T\) is superlinear in
\(T\) on a fixed interval of length at most \(\log2\).  Hence a generic frame
argument does not prove (5.5).

## 7. Finite diagnostics and their boundary

The stored Cycle 47 certificate

- `cycle47_complete_prefix_census.py`, SHA-256
  `49f128e0e411f03e6d646ddbee5e4b2a13a4da2bc11bc5e6705e356404625928`,
- `cycle47-complete-prefix-census.out`, SHA-256
  `d15e404fd584b62a778156eea00e66d2cbb1b7eb7770028228dff6be2f6001ef`,

already prints all scalar products needed to reconstruct \(B_a=Y_a+V_a\).
No new physical computation is used here.

For \(\theta=2/5\), \(I_0=[1,3/2]\), and the six certified starts
\(a=32,64,128,256,512,1024\), the one-generator ratio
\(\mathcal Q_a^{\rm cp}/D_a\), computed from the stored outward intervals, is
approximately

\[
 0.99837,\ 0.99882,\ 0.99787,\ 0.99516,\ 0.95808,\ 0.97976.
 \tag{7.1}
\]

These are postprocessed finite diagnostics, not new outward certificates.  At
the same six starts, the stored certificate gives

\[
 \frac{Q_a^{(2)}}{D_a}
 =0.999925\ldots,
 0.999938\ldots,
 0.999776\ldots,
 0.999626\ldots,
 0.997459\ldots,
 0.997895\ldots,
 \tag{7.2}
\]

and

\[
 (\log a)^3Q_a^{(2)}
 =0.013519\ldots,
 0.010927\ldots,
 0.004182\ldots,
 0.004753\ldots,
 0.001159\ldots,
 0.001514\ldots.
 \tag{7.3}
\]

Thus the scaled projection is already nonmonotone.  The normalized Gram angles,
projection coefficients, and signs of mixed scalar products are also
nonmonotone in the six-row sample.  Postprocessing the certified intervals
further gives

\[
 13.1<\frac{\|H_a\|^2}{D_a-Q_a^{(2)}}<173.0
 \tag{7.4}
\]

across the six starts.  Hence near-total capture controls only the
perpendicular tail; it does not make the complete tail small.

In particular:

1. six positive determinants prove rank two only at those six starts;
2. high capture gives no interscale recurrence or eventual rank theorem;
3. the tail norm may greatly exceed the perpendicular residual;
4. no individual \(Y\), \(V\), endpoint, prime, or Chebyshev square is a lower
   bound for the physical energy;
5. projection coefficients and mixed signs give no coordinate-invariant or
   local sign rule;
6. even infinitely many favorable dyadic starts would require a separate
   all-integer interscale theorem.

Exact Euclidean countermodels show that each forbidden extrapolation can fail
after any prescribed finite prefix, even under perfect projection capture.
They do not rule out a future Möbius-specific arithmetic theorem.

## 8. Surviving frontier

The original arithmetic checkpoint remains

\[
 \boxed{
 \exists\kappa>0,\ a_0:\quad
 D_a(I_0)\ge\frac{\kappa}{(\log a)^3}
 \quad(a\ge a_0).}
 \tag{8.1}
\]

This coordinate rewrite singles out the following stronger, still-open
sufficient target for (8.1):

\[
 \boxed{
 \mathcal Q_a^{\rm cp}
 =\frac{|\langle B_a,\widehat{\mathbf c}_a\rangle|^2}
        {\|B_a\|^2}
 \gg(\log a)^{-3},}
 \tag{8.2}
\]

with the quotient zero when \(B_a=0\), and the exact two-channel fallback
(5.6).  The temporal Abel formulas (3.3), (3.7), and (3.8) make the first
channel an explicit finite arithmetic correlation while preserving every
endpoint and signed packet.

No standard PNT upper bound proves the lower energy or signed retention in
(5.3).  No generic positivity, finite-frame, full-rank, trace, or high-capture
argument supplies it.  Progress now requires an arithmetic theorem controlling
the actual signed complete-prefix/tail correlation.

Even a proof of (8.1) would only establish the trace-based moving-retention
checkpoint.  Completed-square closure would still require an upper bound for
the physical negative budget with explicit constants and a strict comparison.
Burnol's cited theorem gives a lower budget bound, which has the wrong
direction for that final step.  No RH conclusion is established.
