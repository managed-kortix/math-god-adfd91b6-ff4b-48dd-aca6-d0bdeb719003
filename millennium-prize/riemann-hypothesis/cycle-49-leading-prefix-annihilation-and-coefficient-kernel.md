# Cycle 49: leading annihilation of the complete-prefix packets

## Status and scope

This note continues the Cycle 48 canonical complete-prefix construction on

\[
 I_0=[1,3/2].
\]

It proves an exact positive/signed packet decomposition of the complete prefix,
an unconditional leading-order cancellation between those two packets, and an
exact common-source coefficient-kernel representation.  The cancellation is a
no-go result for estimating the positive packet before combining it with its
reciprocal-Möbius partner.  It is **not** a counterexample to the desired
complete-prefix lower bound.

Nothing here proves

\[
 \|B_a\|^2\gg(\log a)^{-3},\qquad
 \mathcal Q_a^{\rm cp}\gg(\log a)^{-3},\qquad
 D_a(I_0)\gg(\log a)^{-3},
\]

a completed-square budget upper bound, or the Riemann hypothesis.  In
particular, the estimate \(\|B_a\|^2=o(a/\log^4a)\) below is much too weak to
decide any of these targets.

Fix

\[
 a\ge2,\qquad 0<\theta<\frac12,\qquad
 C=2(1-\theta),\qquad \tau=C-1,
\]

put \(M=2a-1\), \(L_n=\log n\), and retain

\[
 \delta_n=\log\frac{n+1}{n},\quad
 w_n=1-\frac{L_n}{L_{n+1}},\quad
 A_n=C-w_n,\quad
 \eta_n=\frac{\tau}{A_n},
\]

\[
 b_q(n)=\frac{\log q}{L_n}-\eta_n,
 \qquad \alpha_{q,n}=w_nA_nb_q(n).
\]

Rows always mean physical squarefree rows

\[
 q\in S_a(I_0)=\{q:\mu(q)^2=1,\ a\le q\le3a/2\}.
\]

There is no outer Möbius sign and every temporal sum ends at \(M=2a-1\).

## 1. Exact positive packet and signed partner

Use the Cycle 48 quantities

\[
 \mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q},
 \qquad
 s_n=\frac{\ell_n}{L_n}-\eta_nm_n,
\]

where

\[
 m_n=\sum_{d\le n}\frac{\mu(d)}d,
 \qquad
 \ell_n=\sum_{d\le n}\frac{\mu(d)\log d}{d}.
\]

Also put

\[
 C_r=\sum_{m<r}\Lambda(m)\log\frac rm,
 \qquad
 \mathfrak p_{q,n}
 =\frac{C_{n+1}}q-\sum_{k=q}^{n}\frac{\psi(k)}{k(k+1)}.
 \tag{1.1}
\]

The exact complete-prefix cell identity from Cycle 48 is

\[
 \boxed{\mathcal B_{q,n}
 =\mathfrak a_{q,n}s_n+\frac{\mathfrak p_{q,n}}{L_n}.}
 \tag{1.2}
\]

Define

\[
 P_a^+(q)=\sum_{n=q}^{M}\frac{\alpha_{q,n}}{L_n}\mathfrak p_{q,n},
 \qquad
 S_a^\mu(q)=\sum_{n=q}^{M}
 \alpha_{q,n}\mathfrak a_{q,n}s_n.
 \tag{1.3}
\]

Then, exactly,

\[
 \boxed{B_a=P_a^++S_a^\mu.}
 \tag{1.4}
\]

### 1.1 Every temporal weight is positive

For every \(a\ge2\), \(q\ge a\), \(q\le n\le2a-1\), and
\(0<\theta<1/2\),

\[
 \boxed{\alpha_{q,n}>0.}
 \tag{1.5}
\]

Here neither squarefreeness nor the upper physical-row restriction is needed.
Put

\[
 r=\frac{\log2}{\log3}>\frac58.
\]

The function \(f(x)=\log x/\log(2x-1)\) is increasing on \([2,\infty)\):
the numerator of \(f'(x)\), after multiplication by the positive denominator
and by \(2x-1\), is

\[
 (2x-1)\log(2x-1)-2x\log x,
\]

whose derivative is \(2\log((2x-1)/x)>0\) and whose value at \(x=2\) is
positive.  Consequently

\[
 \frac{L_q}{L_n}\ge\frac{\log a}{\log(2a-1)}\ge r.
 \tag{1.6}
\]

Also

\[
 1-w_n=\frac{L_n}{L_{n+1}}\ge r,
 \qquad A_n=\tau+(1-w_n)\ge\tau+r.
\]

Since \(r^2+r>1\), for \(0<\tau<1\),

\[
 \eta_n=\frac{\tau}{A_n}
 \le\frac{\tau}{\tau+r}<r;
\]

the last strict inequality is equivalent to
\(\tau(1-r)<r^2\), whose worst case is \(\tau=1\).  Thus
\(b_q(n)=L_q/L_n-\eta_n>0\).  Since \(w_n,A_n>0\), (1.5) follows.

### 1.2 The prime packet is strictly positive

Finite differencing (1.1) gives

\[
 \boxed{
 \mathfrak p_{q,n}
 =\frac{C_q}{q}
 +\sum_{r=q}^{n}\psi(r)
 \left(\frac{\delta_r}{q}-\frac1{r(r+1)}\right).}
 \tag{1.7}
\]

Here \(C_q\ge0\), and

\[
 \delta_r=\log(1+1/r)>\frac1{r+1}.
\]

For \(r\ge q\), therefore,

\[
 \frac{\delta_r}{q}-\frac1{r(r+1)}
 >\frac{r-q}{qr(r+1)}\ge0.
\]

The inequality is still strict for \(r=q\), and \(\psi(r)>0\) for
\(r\ge2\).  Thus

\[
 \boxed{\mathfrak p_{q,n}>0,\qquad P_a^+(q)>0.}
 \tag{1.8}
\]

The second packet in (1.3) is signed and is of the same leading size.  It
cannot be discarded or bounded absolutely without destroying the relevant
cancellation.

## 2. Endpoint-safe Abel pair

Let

\[
 \Sigma_{q,m}=\sum_{n=m}^{M}\frac{\alpha_{q,n}}{L_n}.
 \tag{2.1}
\]

Swapping only finite sums in (1.7) gives the manifestly positive identity

\[
 \boxed{
 P_a^+(q)=\frac{C_q}{q}\Sigma_{q,q}
 +\sum_{m=q}^{M}\psi(m)
 \left(\frac{\delta_m}{q}-\frac1{m(m+1)}\right)\Sigma_{q,m}.}
 \tag{2.2}
\]

For the signed partner define

\[
 \mathfrak h_n=1+\ell_n-L_nm_n,
 \qquad
 u_{q,n}=\frac{\alpha_{q,n}\mathfrak a_{q,n}(1-\eta_n)}{\delta_n},
 \tag{2.3}
\]

\[
 \omega_{q,q}=u_{q,q}
 +\frac{\alpha_{q,q}\mathfrak a_{q,q}}{L_q},
 \tag{2.4}
\]

and, for \(q<n\le M\),

\[
 \omega_{q,n}=u_{q,n}-u_{q,n-1}
 +\frac{\alpha_{q,n}\mathfrak a_{q,n}}{L_n}.
 \tag{2.5}
\]

The identities

\[
 s_n=-\frac1{L_n}+(1-\eta_n)m_n+\frac{\mathfrak h_n}{L_n},
 \qquad
 \mathfrak h_n-\mathfrak h_{n+1}=\delta_nm_n,
\]

and

\[
 \mathfrak a_{q,n}-\mathfrak a_{q,n-1}=\frac1q-\delta_n,
 \qquad
 \mathfrak a_{q,q-1}=1-\frac1q,
\]

give the exact finite Abel identity

\[
 \boxed{
 \begin{aligned}
 S_a^\mu(q)={}&-\left(1-\frac1q\right)\Sigma_{q,q}
 +\sum_{m=q}^{M}\left(\delta_m-\frac1q\right)\Sigma_{q,m}\\
 &+\sum_{n=q}^{M}\omega_{q,n}\mathfrak h_n
 -u_{q,M}\mathfrak h_{2a}.
 \end{aligned}}
 \tag{2.6}
\]

The terminal sign is minus.  The value \(\mathfrak h_{2a}\) is an Abel
endpoint and is not a temporal \(n=2a\) summand.  Adding (2.2) and (2.6)
reproduces Cycle 48 equation (3.8), because
\(C_q=E_q+q-1\).  Neither \(\omega_{q,n}\) nor \(\mathfrak h_n\) has a
fixed sign in the required range.

For reference, the initial Abel coefficient has the positive exact form

\[
 \omega_{q,q}=\mathfrak a_{q,q}b_q(q)
 \left[
 \frac{L_q}{L_{q+1}^2}
 +\frac{\delta_q(C-\delta_q/L_{q+1})}{L_qL_{q+1}}
 \right]>0.
 \tag{2.7}
\]

## 3. Unconditional leading-order annihilation

The estimates in this section use the classical unconditional quantitative
zero-free-region PNT, not merely the qualitative PNT.  The classical bound

\[
 M(x)=\sum_{d\le x}\mu(d)
 \ll x\exp(-c\sqrt{\log x})
\]

(after harmlessly reducing \(c\) to absorb powers of \(\log x\)) and partial
summation give

\[
 m(x)=O(\!\sqrt{\log x}\,e^{-c\sqrt{\log x}}),
 \qquad
 \ell(x)=-1+O(\operatorname{poly}(\log x)e^{-c\sqrt{\log x}}).
\]

Equivalently, these are the quantitative reciprocal-Möbius estimates already
used in Cycle 47.  They imply the required dyadic suprema

\[
 \sup_{a\le n\le2a}|L_nm_n|=o(1),
 \qquad
 \sup_{a\le n\le2a}|1+\ell_n|=o(1).
 \tag{3.1}
\]

The bare equivalence between the qualitative PNT and \(m(x)=o(1)\) would not
suffice for the first limit in (3.1).  In particular, one must not infer it
from formal substitution into \(1/\zeta(s)\) at \(s=1\).

The prime packet needs only the qualitative PNT.  If
\(e_k=\psi(k)-k\), then

\[
 E_x=\int_1^x\frac{\psi(t)-t}{t}\,dt=o(x)
\]

and exact subtraction of the model \(\psi_0(k)=k\) gives

\[
 \mathfrak j_{q,n}
 =\sum_{k=q}^{n}\left(\delta_k-\frac1{k+1}\right)
  -\sum_{k=q}^{n}\frac{e_k}{k(k+1)}.
\]

The first sum is \(O(a^{-1})\), since
\(0<\delta_k-1/(k+1)<1/[k(k+1)]\).  Therefore, uniformly for
\(a\le q\le n<2a\),

\[
 \sup\frac{|E_{n+1}|}{q}=o(1),
 \qquad
 \sup|\mathfrak j_{q,n}|
 \le O(a^{-1})+
 \sup_{a\le k\le2a}\frac{|e_k|}{k}
      \sum_{k=q}^{n}\frac1{k+1}=o(1).
 \tag{3.2}
\]

Put \(L=\log a\), \(u=q/a\), and let \(q\) range over the closed physical
row set.  On the closed triangular domain \(a\le q\le3a/2\),
\(q\le n<2a\), elementary expansion gives

\[
 \sup_{q,n}\left|\frac{nL^2\alpha_{q,n}}{L_n}-1\right|
 =O(L^{-1}).
 \tag{3.3}
\]

Indeed, \(n\delta_n=1+O(a^{-1})\), \(L_n=L+O(1)\), and
\(A_nb_q(n)=A_nL_q/L_n-\tau=1+O(L^{-1})\), uniformly.  Equations
(3.1)--(3.2) then give

\[
 \mathfrak p_{q,n}=\mathfrak a_{q,n}+o(1),
 \qquad
 L_ns_n=\ell_n-\eta_nL_nm_n=-1+o(1)
 \tag{3.4}
\]

uniformly; \(\eta_n\) is uniformly bounded.  Finally,
\(\mathfrak a_{q,n}=v/u-\log(v/u)+O(a^{-1})\) for \(v=n/a\), uniformly.
Uniform Riemann summation now yields

\[
 \boxed{L^2P_a^+(q)=F(q/a)+o(1),}
 \qquad
 \boxed{L^2S_a^\mu(q)=-F(q/a)+o(1),}
 \tag{3.5}
\]

uniformly over the physical rows, where

\[
 \boxed{
 F(u)=\int_u^2\left(\frac vu-\log\frac vu\right)\frac{dv}{v}
 =\frac{2-u}{u}-\frac12\log^2\frac2u.}
 \tag{3.6}
\]

The integrand \(v/u-\log(v/u)\) is at least one for \(v\ge u\), so \(F\)
is continuous and bounded away from zero on \([1,3/2]\).  In particular,

\[
 \frac{S_a^\mu(q)}{P_a^+(q)}\longrightarrow-1
 \tag{3.7}
\]

uniformly over physical rows.  Thus both packets are much larger than their
surviving difference at leading order.

The weighted squarefree equidistribution lemma

\[
 \frac1a\sum_{a\le q\le3a/2}\mu(q)^2g(q/a)
 \longrightarrow\frac6{\pi^2}\int_1^{3/2}g(u)\,du
 \tag{3.8}
\]

holds for every continuous \(g\); it follows from
\(\mu^2(n)=\sum_{d^2\mid n}\mu(d)\) and uniform Riemann sums.  Applying it
to \(F^2\) gives

\[
 \boxed{
 \begin{aligned}
 \|P_a^+\|_2^2&\sim\|S_a^\mu\|_2^2
 \sim c_+\frac{a}{L^4},\\
 \langle P_a^+,S_a^\mu\rangle&\sim-c_+\frac{a}{L^4},
 \qquad
 c_+=\frac6{\pi^2}\int_1^{3/2}F(u)^2\,du>0.
 \end{aligned}}
 \tag{3.9}
\]

By (1.4) and the uniform limits above, only

\[
 \boxed{\|B_a\|_2^2=o(a/L^4)}
 \tag{3.10}
\]

follows.  The right side of (3.10) is far larger than the desired
\(L^{-3}\) scale, so (3.10) proves neither a lower bound nor a useful upper
bound at the target scale.  It proves that positivity of (2.2), even with its
sharp asymptotic constant, is strategically irrelevant unless it is combined
with (2.6) before estimation.

## 4. The exact second-order residual

Define

\[
 \mathcal R_{q,n}
 =\mathfrak p_{q,n}+L_n\mathfrak a_{q,n}s_n.
 \tag{4.1}
\]

Then (1.2) gives the cancellation-preserving identity

\[
 \boxed{
 B_a(q)=\sum_{n=q}^{M}\frac{\alpha_{q,n}}{L_n}\mathcal R_{q,n}.}
 \tag{4.2}
\]

Using
\(\mathfrak p_{q,n}=\mathfrak a_{q,n}+E_{n+1}/q+\mathfrak j_{q,n}\),
this residual is exactly

\[
 \boxed{
 \mathcal R_{q,n}
 =\frac{E_{n+1}}q+\mathfrak j_{q,n}
 +\mathfrak a_{q,n}
 \bigl(1+\ell_n-\eta_nL_nm_n\bigr).}
 \tag{4.3}
\]

Equivalently,

\[
 \mathcal R_{q,n}
 =\frac{E_{n+1}}q+\mathfrak j_{q,n}
 +\mathfrak a_{q,n}
 \bigl(\mathfrak h_n+(1-\eta_n)L_nm_n\bigr).
 \tag{4.4}
\]

There is also a useful exact centering by the deterministic profile
\(\psi_0(k)=k\).  Put \(e_k=\psi(k)-k\), and define

\[
 \mathcal D_{q,n}
 =\frac{n\log(n+1)-\log(n!)-n}{q}
 -\sum_{k=q}^{n}\frac1{k+1}+\log\frac{n+1}{q},
 \tag{4.5}
\]

\[
 \mathcal P_{q,n}
 =\frac1q\sum_{k=1}^{n}e_k\delta_k
 -\sum_{k=q}^{n}\frac{e_k}{k(k+1)}.
 \tag{4.6}
\]

Since

\[
 C_{n+1}=\sum_{k=1}^{n}\psi(k)\delta_k,
\]

equations (4.1) and (4.3) give

\[
 \boxed{
 \mathcal R_{q,n}=\mathcal D_{q,n}+\mathcal P_{q,n}
 +\mathfrak a_{q,n}
 \bigl(1+\ell_n-\eta_nL_nm_n\bigr).}
 \tag{4.7}
\]

The deterministic term is already small: Stirling's formula and harmonic
summation give \(\mathcal D_{q,n}=O((\log a)/a)\) uniformly for
\(a\le q\le n<2a\).  (The logarithm is present, for example, in the
\(-\tfrac12\log n/q\) Stirling correction.)  Thus the surviving scale is governed by a joint
Chebyshev-error/reciprocal-Möbius packet, not by the deterministic continuum
profile.

A sharper exact form exposes its sources without changing that conclusion.
Put

\[
 c_{q,n}=\frac{\alpha_{q,n}}{L_n},\qquad
 v_n=L_n(1-\eta_n)m_n=\frac{L_n^2}{A_nL_{n+1}}m_n,
\]

\[
 \mathcal D^*_{q,n}=\frac{E_{n+1}}q+\mathfrak j_{q,n}.
\]

Then

\[
 \boxed{\mathcal R_{q,n}=\mathcal D^*_{q,n}
 +\mathfrak a_{q,n}(\mathfrak h_n+v_n).}
 \tag{4.8}
\]

Its first source has the endpoint-preserving recurrence

\[
 \mathcal D^*_{q,q-1}=\frac{E_q}{q},
\]

\[
 \mathcal D^*_{q,r}-\mathcal D^*_{q,r-1}
 =d_{q,r}+e_r\kappa_{q,r},
 \tag{4.9}
\]

where

\[
 e_r=\psi(r)-r,
 \quad
 \kappa_{q,r}=\frac{\delta_r}{q}-\frac1{r(r+1)}>0,
\]

\[
 d_{q,r}=\left(1+\frac rq\right)\delta_r-\frac1q-\frac1{r+1}<0.
 \tag{4.10}
\]

For the last sign, write
\(d=(\delta_r-1/(r+1))+(r\delta_r-1)/q\).  Since
\(r\delta_r-1<0\), this is maximal at \(q=r\); strict trapezoid convexity
of \(1/t\), equivalently
\(2\log(1+1/r)<1/r+1/(r+1)\), gives \(d_{r,r}<0\).
Consequently, with \(\Sigma_{q,r}=\sum_{n=r}^Mc_{q,n}\),

\[
 \boxed{
 \begin{aligned}
 B_a(q)={}&\frac{E_q}{q}\Sigma_{q,q}
 +\sum_{r=q}^M(d_{q,r}+e_r\kappa_{q,r})\Sigma_{q,r}\\
 &+\sum_{n=q}^Mc_{q,n}\mathfrak a_{q,n}(\mathfrak h_n+v_n).
 \end{aligned}}
 \tag{4.11}
\]

The exact identity
\(\mathfrak h_n-\mathfrak h_{n+1}=\delta_nm_n\) turns the last line into
Cycle 48's endpoint-safe Abel form with

\[
 u_{q,n}=\frac{\alpha_{q,n}\mathfrak a_{q,n}(1-\eta_n)}{\delta_n};
\]

its coefficient of \(\mathfrak h_n\) is
\(c_{q,n}\mathfrak a_{q,n}+u_{q,n}
 -\mathbf1_{n>q}u_{q,n-1}\), and its terminal term is
\(-u_{q,M}\mathfrak h_{2a}\).  Notice carefully that
\(v_n=L_n^2m_n/(A_nL_{n+1})\), not \(\delta_nm_n\).

Equations (4.2)--(4.11) locate all surviving prefix mass in a correlated
Chebyshev/reciprocal-Möbius residual.  The quantitative estimates of Section 3
give only \(\mathcal R_{q,n}=o(1)\) uniformly.  A lower bound for the weighted
row square in (4.2) is a new two-source anti-cancellation theorem; separate
one-point PNT bounds and the negative deterministic curvature do not imply it.

## 5. Exact common-source coefficient kernels

The residual also has a finite coefficient-space representation that retains
every affine, endpoint, and Möbius term.  Adjoin the affine label \(0\), and
write

\[
 x_0=1,\quad \phi_0=\chi,\quad b_0(n)=-\eta_n,
\]

\[
 x_d=\mu(d),\quad \phi_d=\rho_d,\quad
 b_d(n)=\frac{\log d}{L_n}-\eta_n\quad(d\ge1).
\]

Thus

\[
 Z_n=\sum_{d=0}^{n}x_db_d(n)\phi_d,
\]

where the affine label is always active.  Define the prefix and tail spatial
entries

\[
 P_n(q,d)=\left\langle\rho_q,
  \mathbf1_{[1,n+1]}\phi_d\right\rangle_H,
 \qquad
 T_n(q,d)=\left\langle\rho_q,
  \mathbf1_{[n+1,\infty)}\phi_d\right\rangle_H.
 \tag{5.1}
\]

For \(d=0\), since \(n<2q\),

\[
 P_n(q,0)=\frac{\log(n+1)-1}{q}+\frac1{n+1},
 \qquad T_n(q,0)=g_q-P_n(q,0).
 \tag{5.2}
\]

For \(d\ge1\), literal complete-cell integration gives

\[
 \boxed{
 \begin{aligned}
 P_n(q,d)=\sum_{k=1}^{n}\bigg[&\frac1{qd}
 -\left(\frac{\lfloor k/d\rfloor}{q}
       +\frac{\lfloor k/q\rfloor}{d}\right)
       \log\frac{k+1}{k}\\
 &+\lfloor k/q\rfloor\lfloor k/d\rfloor
 \left(\frac1k-\frac1{k+1}\right)\bigg].
 \end{aligned}}
 \tag{5.3}
\]

Moreover,

\[
 P_n(q,d)+T_n(q,d)=G(q,d),
\]

where \(G(q,d)\) is the restricted \(H=L^2([1,\infty),dt/t^2)\)
Vasyunin Gram entry: it is the full \((0,\infty)\) value minus exactly
\(1/(qd)\).  This correction belongs to \(G\), not to the finite prefix
(5.3).

Use the active augmented set

\[
 \mathcal D_a^+=\{0\}\cup\{1\le d\le M:\mu(d)^2=1\}.
\]

The affine column is active for every \(n\), whereas a divisor column is
active only for \(d\le n\).  Thus define, without an ambiguous artificial
threshold,

\[
 W_a^B(q,0)=\sum_{n=q}^{M}\alpha_{q,n}b_0(n)P_n(q,0),
 \qquad
 W_a^H(q,0)=\sum_{n=q}^{M}\alpha_{q,n}b_0(n)T_n(q,0),
 \tag{5.4}
\]

and, for \(d\ge1\),

\[
 W_a^B(q,d)=\sum_{n=\max(q,d)}^{M}
 \alpha_{q,n}b_d(n)P_n(q,d),
 \quad
 W_a^H(q,d)=\sum_{n=\max(q,d)}^{M}
 \alpha_{q,n}b_d(n)T_n(q,d).
 \tag{5.5}
\]

Finite expansion gives, exactly,

\[
 \boxed{B_a=W_a^Bx,\qquad H_a=W_a^Hx,
 \qquad\widehat{\mathbf c}_a=(W_a^B+W_a^H)x.}
 \tag{5.6}
\]

No limit interchange is used.  The row-space coefficient kernels

\[
 K_{BB}=(W_a^B)^TW_a^B,
 \quad K_{BH}=(W_a^B)^TW_a^H,
 \quad K_{HH}=(W_a^H)^TW_a^H
 \tag{5.7}
\]

therefore satisfy

\[
 \|B_a\|^2=x^TK_{BB}x,
 \qquad
 \langle B_a,H_a\rangle=x^TK_{BH}x
 =x^T\operatorname{sym}(K_{BH})x,
 \tag{5.8}
\]

and

\[
 \langle B_a,\widehat{\mathbf c}_a\rangle
 =x^T[K_{BB}+\operatorname{sym}(K_{BH})]x.
 \tag{5.9}
\]

The nonsymmetric matrix
\((W_a^B)^T(W_a^B+W_a^H)\) is algebraically valid inside the scalar
quadratic form, but is not itself a Gram or PSD kernel.  Finally,

\[
 \|\widehat{\mathbf c}_a\|^2
 =x^T(K_{BB}+K_{BH}+K_{BH}^T+K_{HH})x.
 \tag{5.10}
\]

The delta pairing of equal physical rows is essential in (5.7).  These are
row-space Gram kernels, not spatial \(H\)-inner products of source functions.

The normal diagonal

\[
 \Delta_B=\|W^B_{\cdot,0}\|_2^2
 +\sum_{\substack{1\le d\le M\\\mu(d)^2=1}}
 \|W^B_{\cdot,d}\|_2^2
 \tag{5.11}
\]

is positive, but it is not a lower bound for \(x^TK_{BB}x\).  The omitted
terms are the selected affine/Möbius off-diagonal correlations, precisely the
terms capable of cancellation.  Positive semidefiniteness, trace mass,
entrywise positivity, full rank, and continuum spectral tails do not control
this selected sign vector.

For orientation only, let \(q/a\to u\), \(d/a\to v>0\), with \(u,v\)
in compact bulk sets separated from support and discontinuity thresholds.
Then the local ingredients suggest

\[
 aL\alpha_{q,n}\to\frac1s,
 \qquad b_d(n)\to\frac1C,
 \qquad aP_n(q,d)\to J_{\le s}(u,v),
\]

and the Riemann increment is \(ds/a\).  Hence the entrywise candidate is

\[
 aL\,W_a^B(q,d)\rightsquigarrow
 \frac1C\int_{\max(u,v)}^2J_{\le s}(u,v)\frac{ds}{s},
 \tag{5.12}
\]

where

\[
 J_{\le s}(u,v)=\int_0^s
 \left\{\frac yu\right\}\left\{\frac yv\right\}\frac{dy}{y^2}.
\]

The analogous tail replaces \(J_{\le s}\) by \(J-J_{\le s}\); their sum is
\(C^{-1}\log(2/\max(u,v))J(u,v)\), matching the Cycle 45 bulk normalization
(and using \(\max(1,u,v)\) beyond the present range \(u\ge1\)).

The affine label \(d=0\) is excluded from (5.12).  It has mixed scalings:
\(W_a^B(q,0)\) and the full affine column are of order \(a^{-1}\), while
\(W_a^H(q,0)\) is of order \((aL)^{-1}\).  More precisely,

\[
 aW_a^B(q,0)\to-\frac{\tau}{Cu}\log\frac2u,
\]

whereas \(aL W_a^H(q,0)\) has a finite, generally nonzero limit.  Thus no
prefix-tail leading cancellation makes the full affine column smaller than
order \(a^{-1}\).  The finite affine factorization remains exact.

Equation (5.12) is only a local moving-divisor normalization guide.  No
finite-matrix Nyström limit, endpoint tightness, selected-Möbius-vector limit,
or affine-column limit under this normalization is claimed.

## 6. Correlation reformulation and limitations

Let

\[
 p_a=\|B_a\|^2,\qquad h_a=\|H_a\|^2,
 \qquad D_a=\|B_a+H_a\|^2.
\]

When \(p_a>0\), the complete-prefix projection has the exact energy form

\[
 \boxed{
 \mathcal Q_a^{\rm cp}
 =\frac{(D_a+p_a-h_a)^2}{4p_a}.}
 \tag{6.1}
\]

When \(p_a=0\), it is defined to be zero.

This follows from

\[
 \langle B_a,B_a+H_a\rangle
 =\frac{D_a+p_a-h_a}{2}.
\]

Thus retention is exactly an arithmetic separation of the three energies,
not a consequence of separate norm bounds.  In symmetric coefficient form,

\[
 \langle B_a,\widehat{\mathbf c}_a\rangle
 =x^T[K_{BB}+\operatorname{sym}(K_{BH})]x.
\]

A generic positive-definite countermodel already shows why diagonal arguments
cannot suffice.  Given any positive-definite divisor block \(W>0\), a selected
sign vector \(\sigma\), and \(\zeta>0\), the augmented Gram matrix

\[
 \begin{pmatrix}
 \sigma^TW\sigma+\zeta&-\sigma^TW\\
 -W\sigma&W
 \end{pmatrix}
\]

is positive definite, while its divisor-part affine vector
\(\beta=-W\sigma\) satisfies \(\beta+W\sigma=0\).  For merely semidefinite
\(W\), the same construction is generally only semidefinite.  This abstract
model is not a physical Möbius counterexample, but it rules out generic PSD,
trace, entry-positivity, and diagonal reasoning.

## 7. Surviving exact frontier

The strongest intrinsic target remains

\[
 \boxed{
 \mathcal Q_a^{\rm cp}=
 \frac{\bigl(x^T[K_{BB}+\operatorname{sym}(K_{BH})]x\bigr)^2}
      {x^TK_{BB}x}\gg(\log a)^{-3},}
 \tag{7.1}
\]

on the positive-denominator branch, with value zero when \(B_a=0\).  A
sufficient two-part version is

\[
 \|B_a\|^2\ge c_0(\log a)^{-3},
 \qquad
 |\langle B_a,\widehat{\mathbf c}_a\rangle|
 \ge\varepsilon\|B_a\|^2.
 \tag{7.2}
\]

By (4.2), the first assertion is the explicit weighted two-point residual
estimate

\[
 \sum_{q\in S_a(I_0)}
 \left|\sum_{n=q}^{2a-1}
 \frac{\alpha_{q,n}}{L_n}\mathcal R_{q,n}\right|^2
 \gg(\log a)^{-3}.
 \tag{7.3}
\]

The second assertion requires the complete signed tail or, equivalently, the
three-energy separation in (6.1).  Fixed-shift Chowla estimates, one-point PNT
upper bounds, the positive packet (2.2), generic operator positivity, and the
sign-stripped continuum spectrum do not imply either statement.

At \(\theta=2/5\), a fail-closed 192-bit finite certificate checks every
physical row at \(a=218,301\), verifies (1.4), both Abel identities, and all
31,847 declared temporal cells against the certified bound
\(\alpha_{q,n}>10^{-6}\).  At \((a,q)=(218,327)\), it certifies

\[
 B_a(q)<0<H_a(q),\qquad \widehat c_a(q)>0,
\]

so rowwise acuteness, same sign, and \(|H_a(q)|\le|B_a(q)|\) fail.  The ratio
\(|\widehat c_a(q)/B_a(q)|\approx0.019943\) does not refute a smaller or
eventual rowwise magnitude constant.  At \(a=301\), it certifies
\(\langle B_a,H_a\rangle<0\), refuting aggregate cross nonnegativity at that
scale only; the certified retention factor is about \(0.9898\), so this is not
evidence against absolute retention.  These are finite mechanism
counterexamples, not asymptotics.  The verifier is documented in
`cycle-49-exact-finite-prefix-certificate.md`.

Even a proof of (7.1) would establish only the current moving-retention
checkpoint.  Completed-square closure would still require the separate
physical budget upper bound with explicit constants.  No RH conclusion is
established.
