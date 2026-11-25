# Moving Gram kernel audit and the Möbius anti-cancellation gate

## Status and scope

This is an audit/candidate dossier for the fixed-parameter moving-divisor
frontier after the Cycle 43 fixed-probe theorem and the Cycle 44 finite
boundary-envelope obstruction.  It separates exact finite identities and
proved asymptotic lemmas from conditional consequences and open arithmetic
targets.

The main conclusions are:

1. after squarefree sign conjugation, moving divisor Gram entries have a
   locally uniform Brownian-support Hadamard Vasyunin-kernel limit;
2. the corresponding continuum operator has an explicit lower spectral-tail
   bound, but this does not control the physical Möbius coefficient vector;
3. the physical correlations reduce exactly to one signed rectangular-matrix
   action; and
4. positivity, entrywise positivity, normal-diagonal mass, continuum
   noncompression, literal self-pairs, gcd grouping, and thin endpoint layers
   do not imply the needed anti-cancellation.

The surviving open checkpoint is a quantitative theorem about the actual
Möbius signs.  Nothing here proves a moving projection limit, a completed-square
budget, or any consequence for the Riemann hypothesis.

Throughout, fix

\[
 0<\theta<\frac12,\qquad C=2(1-\theta),\qquad
 \tau=1-2\theta=C-1,
\]

let \(a\) be a positive integer, and put

\[
 L=\log a,\qquad \lambda=\log2,
\]

\[
 w_n=1-\frac{\log n}{\log(n+1)},\qquad
 A_n=C-w_n,\qquad \eta_n=\frac{\tau}{A_n}
 \quad(a\le n<2a).
\]

In

\[
 H=L^2\!\left([1,\infty),\frac{dt}{t^2}\right)
\]

write \(\chi(t)=1\), \(\rho_d(t)=\{t/d\}\), and

\[
 b_d(n)=\frac{\log d}{\log n}-\eta_n.
\]

Only squarefree divisor labels are physical.  Put

\[
 \mathcal D_a=\{1\le d<2a:\mu(d)^2=1\}.
\]

## 1. Exact signed/unsigned dictionary

For auxiliary unsigned estimates it is useful to define a column at every
integer label, even though only squarefree labels are physical.  In the direct
sum of one copy of \(H\) for every \(a\le n<2a\), define

\[
 f_d(n)=\mathbf1_{d\le n}\sqrt{w_nA_n}\,b_d(n)\rho_d
 \quad(1\le d<2a),
\]

and

\[
 f_0(n)=-\sqrt{w_nA_n}\,\eta_n\chi.
\]

The physical probes are

\[
 p_0=f_0,\qquad p_d=\mu(d)f_d.
\]

The completed-square vector is exactly

\[
 X=f_0+\sum_{d\in\mathcal D_a}\mu(d)f_d
   =p_0+\sum_{d\in\mathcal D_a}p_d.
 \tag{1.1}
\]

Define the unsigned entries

\[
 W_a(q,d)=\langle f_q,f_d\rangle,
 \qquad \beta_a(q)=\langle f_q,f_0\rangle.
 \tag{1.2}
\]

If \(\Gamma\) is the signed Gram matrix used by the finite verifier, then

\[
 \Gamma_{q0}=\mu(q)\beta_a(q),\qquad
 \Gamma_{qd}=\mu(q)\mu(d)W_a(q,d).
 \tag{1.3}
\]

Consequently the code-level row sum

\[
 c_q=\langle X,p_q\rangle
     =\Gamma_{q0}+\sum_{d\in\mathcal D_a}\Gamma_{qd}
 \tag{1.4}
\]

already contains every Möbius sign.  Multiplying a signed
`probe_gram(q,d)` by another \(\mu(d)\) is a double-signing error.  For a
squarefree row, de-signing gives the exact formula

\[
 \boxed{
 \widehat c_a(q):=\mu(q)c_q
 =\beta_a(q)+\sum_{d\in\mathcal D_a}\mu(d)W_a(q,d).}
 \tag{1.5}
\]

No such orthogonal sign conjugation is asserted on all integer labels:
\(\operatorname{diag}(\mu(q))\) has zero entries at nonsquarefree labels.

For later use, put

\[
 H_a(q,d)=\sum_{\max(a,q,d)\le n<2a}
 w_nA_nb_q(n)b_d(n),
 \tag{1.6}
\]

\[
 H_a^0(q)=\sum_{\max(a,q)\le n<2a}
 w_nA_n\eta_nb_q(n).
 \tag{1.7}
\]

Then, exactly,

\[
 W_a(q,d)=\langle\rho_q,\rho_d\rangle H_a(q,d),
 \qquad
 \beta_a(q)=-g_qH_a^0(q),
 \tag{1.8}
\]

where

\[
 g_q=\langle\chi,\rho_q\rangle
 =\frac{\log q+1-\gamma}{q}.
 \tag{1.9}
\]

## 2. The temporal support kernel

Let \(q,r\) be labels proportional to \(a\), and set

\[
 \alpha_a=\log(q/a),\qquad \beta_a'=\log(r/a),\qquad
 \xi_a=\log\frac{\max(a,q,r)}a.
\]

The prime on \(\beta_a'\) distinguishes this scalar from the affine Gram
entry \(\beta_a(q)\).  The unsigned temporal factor is

\[
 T_a(q,r)=\sum_{\max(a,q,r)\le n<2a}
 w_nA_nb_q(n)b_r(n).
 \tag{2.1}
\]

### Proposition 2.1: floor-exact expansion

Uniformly when \(q/a,r/a\) remain in a fixed compact subset of \((0,2)\),

\[
 \boxed{
 \begin{aligned}
 T_a(q,r)
 ={}&\frac{\lambda-\xi_a}{CL}\\
 &+\frac{(\alpha_a+\beta_a')(\lambda-\xi_a)
 -\left(1+\frac1{2C}\right)(\lambda^2-\xi_a^2)}{L^2}\\
 &+O_{\theta,K}\!\left(L^{-3}+\frac1{aL^2}\right).
 \end{aligned}}
 \tag{2.2}
\]

In particular, for literal floors \(q=\lfloor au\rfloor\),
\(r=\lfloor av\rfloor\), with \((u,v)\) in such a compact set, define

\[
 d(u,v)=\log\frac2{\max(1,u,v)}.
 \tag{2.3}
\]

Then

\[
 T_a(q,r)=\frac{d(u,v)}{CL}
 +\frac{Q_\theta(u,v)}{L^2}
 +O_{\theta,K}\!\left(L^{-3}+\frac1{aL}\right),
 \tag{2.4}
\]

where

\[
 \boxed{
 Q_\theta(u,v)
 = (\log u+\log v)d(u,v)
 -\left(1+\frac1{2C}\right)
 \left(\lambda^2-\log^2\max(1,u,v)\right).}
 \tag{2.5}
\]

There is no additional factor \(1/C\) in the first term of \(Q_\theta\).

#### Proof

Put \(x_n=\log(n/a)\) and
\(\delta_n=x_{n+1}-x_n=\log(1+1/n)\).  Exactly,

\[
 w_n=\frac{\delta_n}{L+x_{n+1}},
 \tag{2.6}
\]

and

\[
 b_q(n)=\frac{1-w_n}{C-w_n}
        +\frac{\alpha_a-x_n}{L+x_n}.
 \tag{2.7}
\]

Equivalently, direct algebra gives

\[
 \begin{aligned}
 w_nA_nb_q(n)b_r(n)
 ={}&Cw_n
 \left(\frac{\log q}{\log n}-\frac\tau C\right)
 \left(\frac{\log r}{\log n}-\frac\tau C\right)\\
 &+w_n^2\left(
 \frac{\tau^2}{CA_n}
 -\frac{\log q\log r}{(\log n)^2}\right).
 \end{aligned}
 \tag{2.8}
\]

The sum of the \(w_n^2\) remainder is
\(O_{\theta,K}(a^{-1}L^{-2})\).  The principal sum is a logarithmic-mesh
Riemann sum, yielding

\[
 \begin{aligned}
 T_a(q,r)
 =\int_{\xi_a}^{\lambda}\left[
 &\frac1{C(L+x)}
 +\frac{\alpha_a+\beta_a'-2x}{(L+x)^2}\\
 &+\frac{C(\alpha_a-x)(\beta_a'-x)}{(L+x)^3}
 \right]dx
 +O_{\theta,K}\!\left(\frac1{aL^2}\right).
 \end{aligned}
 \tag{2.9}
\]

Expanding the integrand through order \(L^{-2}\) proves (2.2).  Replacing
the lattice endpoints by \(u,v\) changes the leading support endpoint by
\(O(a^{-1}L^{-1})\), proving (2.4).  This is an expansion for the unsigned temporal factor.  A physical divisor
Gram entry vanishes when a label is nonsquarefree.  Uniformity as
\(u\downarrow0\) or relative uniformity as \(u\uparrow2\) is not claimed.
\(\square\)

The leading factor

\[
 \frac1C d(u,v)
 =\frac1C\min\left\{
 \log\frac2{\max(1,u)},\log\frac2{\max(1,v)}
 \right\}
 \tag{2.10}
\]

is precisely a reversed-log Brownian covariance kernel.

## 3. Exact spatial dilation and the moving kernel

Define

\[
 J(u,v)=\int_0^\infty
 \left\{\frac yu\right\}
 \left\{\frac yv\right\}\frac{dy}{y^2}
 \qquad(u,v>0).
 \tag{3.1}
\]

### Proposition 3.1: dilation, regularity, and positivity

For every positive integer \(a,q,r\),

\[
 \boxed{
 a\langle\rho_q,\rho_r\rangle_H
 =J(q/a,r/a)-\frac{a}{qr}.}
 \tag{3.2}
\]

The kernel \(J\) is symmetric, positive semidefinite, continuous, locally
uniformly continuous on \((0,\infty)^2\), and homogeneous:

\[
 J(su,sv)=s^{-1}J(u,v).
 \tag{3.3}
\]

#### Proof

After \(t=ay\), the restricted spatial product becomes the integral in
(3.1) over \([1/a,\infty)\).  On \(0<y<1/a\), both fractional parts are
linear and the omitted integral equals

\[
 \int_0^{1/a}\frac{y^2}{uv}\frac{dy}{y^2}
 =\frac1{auv}=\frac a{qr},
\]

which proves (3.2), including the negative sign of the restricted correction.
Symmetry and homogeneity are immediate.  Positive semidefiniteness follows by
writing a finite quadratic form as the integral of a square.  On
\(u,v\in[\delta,M]\), dominated convergence applies with majorant

\[
 \delta^{-2}\mathbf1_{(0,\delta)}(y)
 +y^{-2}\mathbf1_{[\delta,\infty)}(y),
\]

which proves continuity and local uniform continuity. \(\square\)

Writing

\[
 C_V=\log(2\pi)-\gamma,
 \tag{3.4}
\]

one has

\[
 J(u,u)=\frac{C_V}{u}.
 \tag{3.5}
\]

For \(u=\sigma p\), \(v=\sigma s\), with \((p,s)=1\), the exact rational
formula is

\[
 J(u,v)=
 \frac{(s-p)\log(p/s)+(p+s)C_V
 -\pi\bigl(V(p,s)+V(s,p)\bigr)}{2\sigma ps},
 \tag{3.6}
\]

where our Vasyunin-sum normalization is

\[
 V(p,s)=\sum_{j=1}^{s-1}
 \left\{\frac{jp}{s}\right\}\cot\frac{\pi j}{s}.
 \tag{3.6a}
\]

Formula (3.2), rather than reduced-ratio data alone, also shows why the moving
spatial kernel is continuous; a proposed arithmetic-discontinuity obstruction
is false.

Define the limiting moving kernel

\[
 \boxed{
 K_\theta(u,v)=\frac1C d(u,v)J(u,v).}
 \tag{3.7}
\]

### Corollary 3.2: locally uniform squarefree sign-stripped limit

For every compact \(K\Subset(0,2)^2\),

\[
 \boxed{
 \sup_{\substack{q,r\in\mathcal D_a\\(q/a,r/a)\in K}}
 \left|aL\,\mu(q)\mu(r)G_{qr}-K_\theta(q/a,r/a)\right|
 =
 \sup_{\substack{q,r\in\mathcal D_a\\(q/a,r/a)\in K}}
 \left|aL\,W_a(q,r)-K_\theta(q/a,r/a)\right|
 \longrightarrow0.}
 \tag{3.8}
\]

Here \(G\) is the physical signed divisor Gram.  The limit is literally the
Hadamard product of the reversed-log Brownian support kernel and the spatial
Vasyunin Gram kernel.

The entrywise normalization is \(aL\).  For an \(O(a)\)-node mesh, the
operator normalization is \(L\), because

\[
 LG_{qr}\sim \frac1aK_\theta(q/a,r/a)
 \tag{3.9}
\]

after sign conjugation.

The diagonal is

\[
 K_\theta(u,u)=\frac{C_V}{Cu}
 \log\frac2{\max(1,u)}.
 \tag{3.10}
\]

For \(q=2a-k\) with fixed \(k\ge1\),

\[
 W_a(q,q)\sim\frac{C_Vk}{4Ca^2L},
 \tag{3.11}
\]

while at \(q=2a\) the temporal support is empty.  These are pointwise
boundary-layer statements, not a relative endpoint-uniform theorem.

## 4. Affine scaling and fixed-finite-rank decoupling

The exact affine entries are

\[
 G_{00}=\tau^2\sum_{a\le n<2a}\frac{w_n}{C-w_n},
 \tag{4.1}
\]

\[
 G_{0q}=-\mu(q)g_q\tau
 \sum_{\max(a,q)\le n<2a}w_nb_q(n).
 \tag{4.2}
\]

For squarefree \(q_a/a\to u\in(0,2)\),

\[
 \boxed{
 LG_{00}\longrightarrow\frac{\tau^2\lambda}{C},
 \qquad
 a\mu(q_a)G_{0q_a}
 \longrightarrow-\frac{\tau}{Cu}
 \log\frac2{\max(1,u)}.}
 \tag{4.3}
\]

Thus, for squarefree bulk sequences \(q_a/a\to u\) and
\(r_a/a\to v\), with fixed \(u,v\in(0,2)\) and nonzero limiting kernel
entries, the three entry scales in magnitude are

\[
 G_{00}\asymp L^{-1},\qquad
 |G_{0q_a}|\asymp a^{-1},\qquad
 |G_{q_ar_a}|\asymp(aL)^{-1}.
 \tag{4.4}
\]

This statement does not include fixed old labels or endpoint layers.  For any
fixed finite family of bulk divisor labels, the anisotropic
congruence

\[
 D_a=\operatorname{diag}(\sqrt L,\sqrt{aL},\ldots,\sqrt{aL})
 \tag{4.5}
\]

makes every affine/divisor cross-entry tend to zero:

\[
 (D_aGD_a)_{0q}=O_\theta(L/\sqrt a)\to0.
 \tag{4.6}
\]

This is fixed-finite-rank decoupling only.  For \(m_a\) uniformly bulk
labels, the cross-row bound is

\[
 O_\theta\!\left(L\sqrt{m_a/a}\right),
 \tag{4.7}
\]

so this argument yields decay only when \(m_a=o(a/L^2)\).  It does not prove
growing-rank inverse or Schur-complement convergence.

Cycle 43, equations (43.73)--(43.84), established the corrected affine
correlation expansion

\[
 \boxed{
 c_0=\tau(1+\gamma)\sum_{a\le n<2a}\frac{w_n}{\log n}
 +O_\theta(L^{-3})
 =\frac{\tau(1+\gamma)\lambda}{L^2}+O_\theta(L^{-3}).}
 \tag{4.8}
\]

There is no factor \(1/C\) in (4.8).  Consequently the affine-only projection
has leading size

\[
 \Pi_{\mathrm{aff}}
 \sim\frac{C(1+\gamma)^2\lambda}{L^3}.
 \tag{4.9}
\]

## 5. Measure-aware continuum spectral statement

Restrict now to \([1,2]\), and let \(T_\theta\) be the integral operator on
\(L^2([1,2],du)\) with kernel \(K_\theta\).

### Proposition 5.1: lower spectral-tail bound

For every \(k\ge1\),

\[
 \boxed{
 \lambda_k(T_\theta)\ge
 \frac{\lambda^2}{2C\pi^2(k-\tfrac12)^2}.}
 \tag{5.1}
\]

Moreover,

\[
 \operatorname{tr}T_\theta=\frac{C_V\lambda^2}{2C},
 \tag{5.2}
\]

and, for every rank-\(r\) operator \(R\),

\[
 \boxed{
 \|T_\theta-R\|_1
 \ge\sum_{k>r}\lambda_k(T_\theta)
 \ge\frac{\lambda^2}{2C\pi^2(r+\tfrac12)}.}
 \tag{5.3}
\]

#### Proof

On \([1,2]\), split

\[
 J(u,v)=\frac1{uv}+J_+(u,v),
 \tag{5.4}
\]

where \(J_+\) is positive semidefinite.  The support kernel \(d\) is also
positive semidefinite, so the Schur product theorem makes \(dJ_+\) positive
semidefinite.  Hence

\[
 T_\theta\succeq \frac1C M_{1/u}T_BM_{1/u},
 \tag{5.5}
\]

where \(T_B\) has the reversed-log Brownian kernel \(d(u,v)\).  Put
\(t=\log(2/u)\), so \(u(t)=2e^{-t}\) and \(du=u(t)\,dt\).  The unitary
map \((Uf)(t)=\sqrt{u(t)}f(u(t))\) gives

\[
 UT_BU^{-1}=M_{\sqrt u}T_{\min}M_{\sqrt u},
 \qquad
 UM_{1/u}U^{-1}=M_{1/u}.
 \tag{5.6}
\]

Thus the comparator in (5.5) is unitarily equivalent to
\(C^{-1}M_{u^{-1/2}}T_{\min}M_{u^{-1/2}}\).  If \(A\ge0\) is compact and \(M=M^*>0\) is boundedly invertible, then the
nonzero spectra of \(MAM=(MA^{1/2})(A^{1/2}M)\) and
\((A^{1/2}M)(MA^{1/2})\) agree, so

\[
 \lambda_k(MAM)=s_k(A^{1/2}M)^2
 \ge \|M^{-1}\|^{-2}\lambda_k(A).
\]

The last inequality follows from
\(s_k(A^{1/2})=s_k((A^{1/2}M)M^{-1})\le
s_k(A^{1/2}M)\|M^{-1}\|\).

Here \(\|M_{u^{1/2}}\|^2=2\), and

\[
 \lambda_k(T_{\min})
 =\frac{\lambda^2}{\pi^2(k-\tfrac12)^2}.
 \tag{5.7}
\]

This proves (5.1).  It is a spectral comparison; it should not be replaced by
the generally false Loewner implication
\(M_fTM_f\succeq(\inf f)^2T\).  Formula (5.2) follows by
integrating (3.10).  The first inequality in (5.3) is the Schatten-\(1\)
Eckart--Young--Mirsky, equivalently Ky Fan, best-rank inequality; the final
bound follows by summing (5.1). \(\square\)

This noncompression statement belongs to the continuum operator, or to a
finite full-mesh Gram only after the correct normalization and a separately
proved spectral transfer.  The raw moving sub-Gram restricted to
\(a\le q<2a\) has trace \(O(L^{-1})\), so rank zero already has vanishing
unnormalized trace error.  This sentence does not apply to the full family of
old labels \(1\le d<a\).

Squarefree meshes also change the reference measure.  With

\[
 \delta_{\rm sf}=\frac6{\pi^2},\qquad
 \nu_a=\frac1a\sum_{\substack{a\le q<2a\\\mu(q)^2=1}}
 \delta_{q/a},
 \tag{5.8}
\]

one has \(\nu_a\Rightarrow\delta_{\rm sf}\,du\).  Thus a measure-aware
Nyström statement, if proved, would identify the sign-stripped \(LG_a\) with
\(K_\theta\) acting against \(\delta_{\rm sf}du\), or with
\(\delta_{\rm sf}T_\theta\) after identification with ordinary
\(L^2(du)\).  A measure-free claim of convergence to \(T_\theta\) misses this
factor.  No finite-mesh spectral transfer is claimed here.

## 6. Bulk trace and normal-diagonal normalization

Let \(I\Subset(0,2)\) be a nondegenerate compact interval and

\[
 S_a(I)=\{q\in\mathcal D_a:q/a\in I\}.
 \tag{6.1}
\]

The locally uniform limit and the squarefree Riemann-sum theorem give the
proved bulk trace normalization

\[
 \boxed{
 L\,\operatorname{tr}G_{S_a(I)}
 \longrightarrow
 \delta_{\rm sf}\int_IK_\theta(u,u)\,du.}
 \tag{6.2}
\]

In particular, \(\lambda_{\max}(G_{S_a(I)})=O_{\theta,I}(L^{-1})\).

For the rectangular unsigned matrix with affine column and every squarefree
divisor column,

\[
 (M_a)_{q0}=\beta_a(q),\qquad
 (M_a)_{qd}=W_a(q,d),
 \tag{6.3}
\]

put

\[
 \Delta_a(I)=\|M_a\|_F^2
 =\sum_{q\in S_a(I)}\left(
 \beta_a(q)^2+\sum_{d\in\mathcal D_a}W_a(q,d)^2
 \right).
 \tag{6.4}
\]

The affine contribution is \(O_{\theta,I}(a^{-1})\), hence it is
\(o(L^{-2})\).  To control the left boundary, use

\[
 \sum_{\max(a,q,d)\le n<2a}|w_nA_nb_q(n)b_d(n)|
 \ll_{\theta,I}L^{-1}
\]

and, for \(q/a\in I\) and \(v=d/a\le1\),

\[
 0\le a\langle\rho_q,\rho_d\rangle
 \le J(q/a,v)\ll_I1+\log(1/v).
\]

They give

\[
 |W_a(q,d)|\ll_{\theta,I}
 \frac{1+\log(a/d)}{aL}
 \quad(q/a\in I,\ d\le a),
 \tag{6.5}
\]

and therefore

\[
 \limsup_{a\to\infty}L^2\sum_{q\in S_a(I)}
 \sum_{\substack{d\in\mathcal D_a\\d\le\varepsilon a}}
 W_a(q,d)^2
 \ll_{\theta,I}
 \varepsilon\bigl(1+\log^2(1/\varepsilon)\bigr).
 \tag{6.6}
\]

Indeed, the corresponding unrestricted integer sum is bounded by

\[
 \frac1a\sum_{d\le\varepsilon a}
 \bigl(1+\log(a/d)\bigr)^2
 \ll \varepsilon\bigl(1+\log^2(1/\varepsilon)\bigr)
      +\frac{\log^2 a}{a}.
\]

At the other endpoint, take
\(0<\varepsilon<2-\sup I\), write \(d=2a-k\), and use

\[
 |H_a(q,2a-k)|\ll_{\theta,I}\frac{k}{aL},
 \qquad
 \langle\rho_q,\rho_{2a-k}\rangle\ll_I\frac1a.
\]

Thus \(|W_a(q,d)|\ll_{\theta,I}(2-d/a)/(aL)\), and

\[
 \limsup_{a\to\infty}L^2\sum_{q\in S_a(I)}
 \sum_{\substack{d\in\mathcal D_a\\d\ge(2-\varepsilon)a}}
 W_a(q,d)^2\ll_{\theta,I}\varepsilon^3.
\]

On each remaining rectangle
\(I\times[\varepsilon,2-\varepsilon]\), (3.8) and

\[
 \left(\frac1a\sum_{q\in S_a(I)}\delta_{q/a}\right)
 \otimes
 \left(\frac1a\sum_{d\in\mathcal D_a}\delta_{d/a}\right)
 \Longrightarrow
 \delta_{\rm sf}^2\mathbf1_I(u)\,du\,dv
\]

give the product Riemann-sum limit.  First letting \(a\to\infty\) with
\(\varepsilon\) fixed, and then letting \(\varepsilon\downarrow0\), yields

\[
 \boxed{
 L^2\Delta_a(I)\longrightarrow
 A_{\theta,I}:=\delta_{\rm sf}^2
 \int_I\int_0^2K_\theta(u,v)^2\,dv\,du,}
 \tag{6.7}
\]

where \(0<A_{\theta,I}<\infty\).  The density is
\(\delta_{\rm sf}^2\), since both the row and column labels are squarefree.
Near \(v=0\),

\[
 K_\theta(u,v)=O_{\theta,I}(1+|\log v|),
 \tag{6.8}
\]

which is square-integrable.

Three diagonal quantities must not be conflated:

1. the normal-matrix diagonal is (6.7);
2. the literal self-pairs satisfy
   \[
   aL^2\sum_{q\in S_a(I)}W_a(q,q)^2
   \longrightarrow
   \delta_{\rm sf}\int_IK_\theta(u,u)^2\,du,
   \tag{6.9}
   \]
   and therefore contribute only \(\asymp(aL^2)^{-1}=o(L^{-3})\);
3. the moving-probe Gram trace is (6.2).

## 7. Projection inequality and its exact range qualification

Let \(P_S\) synthesize a finite selected probe family, let
\(G_S=P_S^*P_S\ne0\), and let \(c_S=P_S^*X\).  Since
\(c_S\in\operatorname{Range}(G_S)\),

\[
 G_S^+\succeq
 \lambda_{\max}(G_S)^{-1}P_{\operatorname{Range}(G_S)}.
 \tag{7.1}
\]

Therefore

\[
 \boxed{
 \Pi_S=c_S^TG_S^+c_S
 \ge\frac{\|c_S\|_2^2}{\lambda_{\max}(G_S)}.}
 \tag{7.2}
\]

The range projector in (7.1) is essential when \(G_S\) is singular.  If
\(G_S=0\), then \(c_S=0\) and \(\Pi_S=0\); the displayed quotient is simply
not used.  For the
bulk moving family, (6.2) gives a constant \(C_{\theta,I}>0\) such that

\[
 \Pi_{S_a(I)}\ge
 \frac{L}{C_{\theta,I}}
 \sum_{q\in S_a(I)}|\widehat c_a(q)|^2
 \tag{7.3}
\]

for all sufficiently large \(a\).

This is only a one-sided sufficient route to a projection budget.  It does not
identify the projection asymptotically and cannot be reversed using trace
alone.

## 8. The exact dispersion problem

Set

\[
 x_a=(1,(\mu(d))_{d\in\mathcal D_a}).
 \tag{8.1}
\]

By (1.5) and (6.3), the physical moving-row dispersion is exactly

\[
 \boxed{
 D_a(I)=\sum_{q\in S_a(I)}|\widehat c_a(q)|^2
       =\|M_ax_a\|_2^2.}
 \tag{8.2}
\]

Expanding by coefficient index gives

\[
 D_a(I)=\Delta_a(I)+\mathcal O_a(I),
 \tag{8.3}
\]

where

\[
 \begin{aligned}
 \mathcal O_a(I)={}&
 2\sum_{q\in S_a(I)}\beta_a(q)
   \sum_{d\in\mathcal D_a}\mu(d)W_a(q,d)\\
 &+\sum_{q\in S_a(I)}
   \sum_{\substack{d,e\in\mathcal D_a\\d\ne e}}
   \mu(d)\mu(e)W_a(q,d)W_a(q,e).
 \end{aligned}
 \tag{8.4}
\]

The normal diagonal \(\Delta_a\) is exactly the second moment obtained by
replacing the divisor signs with independent Rademacher signs while retaining
the deterministic affine column.  It is not a lower bound for the fixed
Möbius vector.

Assuming the proved normalization (6.7),

\[
 \boxed{
 D_a(I)\gg L^{-3}
 \quad\Longleftrightarrow\quad
 \frac{D_a(I)}{\Delta_a(I)}\gg\frac1L.}
 \tag{8.5}
\]

Thus the target is an \(\Omega(1/L)\) retention theorem, not an
\(O(1/L)\) upper bound.

## 9. Exact generic obstructions

The following models rule out every inference based only on generic
positivity, positive entries, trace tails, or diagonal mass.  They are not
counterexamples to the physical Möbius--Vasyunin matrix.

### 9.1 Positive-entry Gram cancellation

For \(0<\varepsilon<1\), let

\[
 W_\varepsilon=s
 \begin{pmatrix}1&1-\varepsilon\\1-\varepsilon&1\end{pmatrix},
 \qquad \sigma=\binom1{-1}.
 \tag{9.1}
\]

Then \(W_\varepsilon\) is positive definite with positive entries, but

\[
 W_\varepsilon\sigma=s\varepsilon\sigma,
 \tag{9.2}
\]

\[
 D=2s^2\varepsilon^2,
 \qquad
 \Delta=2s^2\bigl(1+(1-\varepsilon)^2\bigr).
 \tag{9.3}
\]

Taking \(s\asymp L^{-1}\) and \(\varepsilon=o(L^{-1/2})\) gives
\(\Delta\asymp L^{-2}\) but \(D=o(L^{-3})\).

### 9.2 Scale-matched spectral countermodel

Let \(N=2^m\), let \(H_N\) be an unnormalized Sylvester Hadamard matrix with
columns \(h_1,\ldots,h_N\), \(h_1=\mathbf1\), and put \(\sigma=h_N\).  Define

\[
 W_{N,L}=\frac1{NL}H_N
 \operatorname{diag}\left(2,\frac1{2^2},\ldots,\frac1{N^2}\right)H_N^T.
 \tag{9.4}
\]

Its eigenvalues are

\[
 \frac2L,\frac1{2^2L},\ldots,\frac1{N^2L},
 \tag{9.5}
\]

and every entry satisfies

\[
 \frac{1+1/N}{NL}<(W_{N,L})_{ij}<\frac3{NL}.
 \tag{9.6}
\]

Nevertheless,

\[
 \|W_{N,L}\|_F^2
 =\frac1{L^2}\left(4+\sum_{k=2}^N\frac1{k^4}\right),
 \tag{9.7}
\]

while

\[
 W_{N,L}\sigma=\frac1{N^2L}\sigma,
 \qquad
 \|W_{N,L}\sigma\|^2=\frac1{N^3L^2}.
 \tag{9.8}
\]

For \(2r\le N\), it also has the trace tail

\[
 \inf_{\operatorname{rank}R\le r}\|W_{N,L}-R\|_1
 \ge\frac1L\sum_{k=r+1}^{2r}\frac1{k^2}
 \ge\frac1{4rL}.
 \tag{9.9}
\]

Thus trace noncompression does not locate the selected sign vector in a large
singular mode.

### 9.3 Complete augmented-Gram positivity

Let \(W>0\), choose any sign vector \(\sigma\), put
\(\beta=-W\sigma\), and for \(\zeta>0\) define

\[
 \mathcal G=
 \begin{pmatrix}
 \sigma^TW\sigma+\zeta&-\sigma^TW\\
 -W\sigma&W
 \end{pmatrix}.
 \tag{9.10}
\]

Then

\[
 (t,z)^T\mathcal G(t,z)
 =(z-t\sigma)^TW(z-t\sigma)+\zeta t^2>0
 \tag{9.11}
\]

for nonzero \((t,z)\), while \(\beta+W\sigma=0\).  Hence even a positive
definite complete augmented Gram and nonzero total energy do not force a
moving-divisor correlation.

### 9.4 A positive continuum kernel with near-null sign vectors

For the Brownian kernel \(B(x,y)=\min(x,y)\) on \([0,1]\), let \(f_n\), for
\(4\mid n\), repeat the signs

\[
 +1,-1,-1,+1
\]

on cells of length \(1/n\).  A direct rational integration gives

\[
 \boxed{
 \|T_Bf_n\|_2^2=\frac{23}{60n^4},
 \qquad \|f_n\|_2=1.}
 \tag{9.12}
\]

Infinite rank and positivity therefore do not give sign-vector coercivity.

### 9.5 Positive blocks cannot be discarded monotonically

Let

\[
 B=\begin{pmatrix}0&0\\0&1\end{pmatrix},\quad
 C'=\begin{pmatrix}1&-1\\-1&1\end{pmatrix},\quad
 A=B+C',\quad x=\binom{-3}{-2}.
 \tag{9.13}
\]

Both \(B,C'\succeq0\), hence \(A\succeq B\), but

\[
 \|Bx\|^2=4,\qquad \|Ax\|^2=2.
 \tag{9.14}
\]

The map \(A\mapsto A^2\) is not operator monotone.  A favorable historical,
moving, gcd, or endpoint Gram block cannot be retained as a lower bound after
the other positive Gram components are restored.

## 10. Historical and endpoint limitations

For every fixed squarefree \(d\) and \(q/a\to u\in I\),

\[
 aW_a(q,d)\longrightarrow
 -\frac{\tau}{2Cu}\log\frac2{\max(1,u)},
 \tag{10.1}
\]

whereas

\[
 a\beta_a(q)\longrightarrow
 -\frac{\tau}{Cu}\log\frac2{\max(1,u)}.
 \tag{10.2}
\]

Indeed, Cycle 43, equations (43.45)--(43.48), gives for fixed \(d\)

\[
 \langle\rho_q,\rho_d\rangle
 =\frac{\log q}{2q}+O_d(q^{-1}),
 \qquad
 H_a(q,d)=-\frac{\tau}{CL}
 \log\frac2{\max(1,u)}+O_{\theta,I,d}(L^{-2}),
 \tag{10.3}
\]

which proves (10.1); the analogous expansion of \(H_a^0(q)\) proves (10.2).
For a fixed finite old-divisor family \(F\), the squared norm of the summed
old-column contribution is \(O_{\theta,I,F}(a^{-1})=o(L^{-3})\), in agreement
with the stronger Cycle 43 fixed-family projection theorem.

For every integer label \(d\), write
\[
 W_{\bullet d}:=(W_a(q,d))_{q\in S_a(I)}\in\ell^2(S_a(I)).
\]
For a growing old cutoff \(h=o(a)\), the absolute estimate

\[
 \left\|\sum_{\substack{d\le h\\\mu(d)^2=1}}
 \mu(d)W_{\bullet d}\right\|_2
 \ll_{\theta,I}
 \frac{h[1+\log(a/h)]}{\sqrt a\,L}
 \tag{10.4}
\]

removes every range \(d\le a^{1/2-\varepsilon}\) at norm scale
\(L^{-3/2}\), but it does not control the remaining mesoscopic range.

For fixed \(k\ge1\), \(d=2a-k\), and \(q/a\to u\in I\),
\[
 H_a(q,2a-k)\sim\frac{k}{2CaL},
 \qquad
 a\langle\rho_q,\rho_{2a-k}\rangle\longrightarrow J(u,2),
\]
so

\[
 \frac{a^2L}{k}W_a(q,2a-k)
 \longrightarrow\frac{J(u,2)}{2C}.
 \tag{10.5}
\]

Uniformly for \(1\le k\le h=o(a)\),
\(|W_a(q,2a-k)|\ll_{\theta,I}k/(a^2L)\).  Summing the
column norms gives the right-end estimate

\[
 \left\|\sum_{\substack{2a-h\le d<2a\\\mu(d)^2=1}}
 \mu(d)W_{\bullet d}\right\|_2
 \ll_{\theta,I}\frac{h^2}{a^{3/2}L}.
 \tag{10.6}
\]

Fix \(0<\varepsilon<1/2\) and set

\[
 h_-(a)=\lfloor a^{1/2-\varepsilon}\rfloor,
 \qquad
 h_+(a)=\lfloor a^{3/4-\varepsilon}\rfloor,
\]

\[
 \beta_\bullet=(\beta_a(q))_{q\in S_a(I)},
 \qquad
 \widehat c_\bullet=(\widehat c_a(q))_{q\in S_a(I)},
 \qquad
 Y_a=\sum_{\substack{d\in\mathcal D_a\\
 h_-(a)<d<2a-h_+(a)}}\mu(d)W_{\bullet d}.
\]

Using \(\|\beta_\bullet\|_2=O_{\theta,I}(a^{-1/2})\), (10.4), and
(10.6),

\[
 \begin{aligned}
 \|\widehat c_\bullet-Y_a\|_2
 &\ll_{\theta,I}
 a^{-1/2}+a^{-\varepsilon}+\frac{a^{-2\varepsilon}}L\\
 &=o(L^{-3/2}).
 \end{aligned}
\]

The reverse triangle inequality therefore gives only

\[
 \left|\sqrt{D_a(I)}-\|Y_a\|_2\right|=o(L^{-3/2}).
 \tag{10.7}
\]

It cannot be squared into a difference \(o(L^{-3})\) without a separate upper
bound for the sum of the two norms.

For an ordered squarefree triple, the canonical pairwise-coprime factorization

\[
 q=txyu,\qquad d=txzv,\qquad e=tyzw
 \tag{10.8}
\]

gives

\[
 \mu(d)\mu(e)=\mu(xyvw).
 \tag{10.9}
\]

The common factors \(t,z\) disappear from the sign, leaving an uncontrolled
four-factor Möbius sign.  Common-gcd positivity is therefore a normal-diagonal
fact, not an off-diagonal anti-cancellation theorem.

## 11. Conditional consequence and open arithmetic checkpoint

Define

\[
 A_{de}^{(a,I)}=
 \sum_{q\in S_a(I)}W_a(q,d)W_a(q,e),
 \qquad
 r_d^{(a,I)}=
 \sum_{q\in S_a(I)}\beta_a(q)W_a(q,d).
 \tag{11.1}
\]

Then the exact expansion is

\[
 D_a(I)=\Delta_a(I)
 +2\sum_d\mu(d)r_d^{(a,I)}
 +\sum_{d\ne e}\mu(d)\mu(e)A_{de}^{(a,I)}.
 \tag{11.2}
\]

A target-scale arithmetic theorem is

\[
 \boxed{
 2\sum_d\mu(d)r_d^{(a,I)}
 +\sum_{d\ne e}\mu(d)\mu(e)A_{de}^{(a,I)}
 \ge-\Delta_a(I)+\frac\kappa{L^3}}
 \tag{11.3}
\]

for some \(\kappa>0\) and all sufficiently large \(a\).  By (6.7), this is
equivalent to

\[
 \boxed{
 \liminf_{a\to\infty}
 L\frac{D_a(I)}{\Delta_a(I)}>0.}
 \tag{11.4}
\]

Equations (11.3)--(11.4) are open targets, not proved statements.  A stronger
sufficient estimate would make the two Möbius sums in (11.2) jointly
\(o(L^{-2})\), which would imply \(D_a\sim\Delta_a\).  Fixed-shift Chowla
does not directly control this full family of support, ratio, gcd, and
Vasyunin weights.

Combining (7.3) with a proved lower bound of the form (11.3) would give a
moving projection lower bound of order \(L^{-2}\).  Paying the physical
negative budget requires constants and an upper bound of the appropriate
order for that budget.  Cycle 43, equations (43.30) and (43.88)--(43.89),
together with Burnol's Theorem 1.3 and the full-to-restricted rank-one
correction, supplies the unconditional lower bound

\[
 \liminf_{a\to\infty}L^2N_\theta(a,2a)
 \ge \frac{C_{\rm B}\lambda}{C}>0,
 \tag{11.5}
\]

where

\[
 C_{\rm B}=
 \sum_{\substack{\rho:\,\Re\rho=1/2\\
                  \rho\ \mathrm{distinct}}}
 \frac{m(\rho)^2}{|\rho|^2}>0.
\]

The cited source is J.-F. Burnol, *A lower bound in an approximation problem
involving the zeros of the Riemann zeta function*, Advances in Mathematics
**170** (2002), 56--70, Theorem 1.3.  This is not a two-sided asymptotic and
does not give the upper bound \(N_\theta(a,2a)\ll L^{-2}\).
Therefore \(D_a\gg L^{-3}\) is a necessary scale checkpoint for this
trace-based route, but it is not by itself a sufficient physical budget
theorem.  Nor is it necessary for every conceivable projection proof, since
the trace inequality is only a sufficient lower bound.

## 12. Audit boundary

The following are proved or algebraically derived in this dossier:

- the exact signed/unsigned dictionary and de-signed row-sum formula;
- the temporal support expansion through its \(L^{-2}\) coefficient;
- exact spatial dilation, local continuity, homogeneity, and positive
  semidefiniteness;
- the locally uniform squarefree sign-stripped entrywise moving-kernel limit;
- elementary anisotropic scaling estimates;
- the measure-aware continuum spectral lower bound and trace tail;
- the squarefree-density bulk trace and normal-diagonal normalizations;
- the range-qualified projection inequality; and
- exact generic countermodels showing why sign-blind coercivity fails.

Standard imported facts are (1.9), (3.5)--(3.6), the Brownian eigenvalues
(5.7), the Schur product theorem, the multiplier singular-value inequality,
the Schatten-\(1\) Eckart--Young--Mirsky theorem, and squarefree Riemann sums
from \(\sum_{n\le x}\mu(n)^2=(6/\pi^2)x+O(\sqrt x)\).  The cotangent-sum
normalization used in (3.6) is defined explicitly in (3.6a).  The affine
correlation (4.8)--(4.9), the fixed-divisor spatial asymptotic
(10.3), the fixed-family projection theorem, and the budget lower bound
(11.5) are inherited from Cycle 43 as cited above.

The following are conditional, open, or deliberately omitted:

- any unconditional asymptotic for the moving coefficients \(c_q\);
- inserting the entrywise kernel limit into a Möbius row sum without a
  discrepancy theorem;
- any moving projection limit or completed-square budget theorem;
- any assertion \(N_\theta\sim L^{-2}\) or \(N_\theta\asymp L^{-2}\);
- a measure-free Nyström limit;
- unnormalized finite-Gram noncompression;
- growing-rank inverse, Schur-complement, or affine-decoupling convergence;
- de-signing at nonsquarefree labels;
- relative endpoint uniformity or uniformity down to fixed old divisors; and
- every consequence for the Riemann hypothesis.

The next arithmetic object is the finite mean square in (8.2), equivalently
the weighted two-point Möbius packet in (11.3).  Generic kernel geometry has
reached its limit; progress requires a theorem that sees the actual Möbius
signs.
