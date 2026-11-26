# Cycle 46: finite-prime grouping and initial-block audit

## Status and scope

This note records two exact reorganizations of the Cycle 45 moving-row
correlation:

1. finite-prime inclusion-exclusion grouping of its squarefree divisor
   columns; and
2. an initial non-wrapped interval decomposition of each temporal row
   contraction.

Both packages were reconstructed through several exact paths and attacked
adversarially.  They expose new normalizations and exact cancellation channels,
but they do **not** prove the
Cycle 45 checkpoint

\[
 D_a(I)\gg (\log a)^{-3},
 \qquad
 \liminf_{a\to\infty}\log(a)\frac{D_a(I)}{\Delta_a(I)}>0,
\]

a moving-projection theorem, the required completed-square budget, or the
Riemann hypothesis.  In particular, grouped normal diagonals and the separate
initial/tail energies are not lower bounds for the physical selected-vector
energy.

Fix throughout

\[
 0<\theta<\frac12,\qquad C=2(1-\theta),\qquad L=\log a,
\]

and a nondegenerate compact interval \(I\Subset(0,2)\).  Retain the Cycle 45
notation

\[
 \mathcal D_a=\{1\le d<2a:\mu(d)^2=1\},\qquad
 S_a(I)=\{q\in\mathcal D_a:q/a\in I\},
\]

\[
 \widehat c_a(q)=\beta_a(q)+
  \sum_{d\in\mathcal D_a}\mu(d)W_a(q,d),
 \qquad
 D_a(I)=\sum_{q\in S_a(I)}|\widehat c_a(q)|^2.
\]

Here \(\widehat c_a(q)=\mu(q)c_q\) is the de-signed row only for physical
squarefree \(q\).  No sign conjugation is asserted at nonsquarefree labels.

## 1. Exact finite-prime grouping

Let \(P\ge1\) be squarefree.  Define

\[
 \mathcal R_{P,a}=
 \{1\le r<2a:\mu(r)^2=1,\ (r,P)=1\},
\]

\[
 B_{P,r}^{(a)}=
 \sum_{\substack{s\mid P\\sr<2a}}
 \mu(s)W_{\bullet,sr},
 \qquad
 W_{\bullet,d}=(W_a(q,d))_{q\in S_a(I)},
\]

and the grouped normal diagonal

\[
 \Delta_{P,a}(I)=\|\beta_\bullet\|_2^2+
 \sum_{r\in\mathcal R_{P,a}}\|B_{P,r}^{(a)}\|_2^2.
\]

### Theorem 1.1: exact grouping

For every finite squarefree \(P\),

\[
 \boxed{
 \sum_{d\in\mathcal D_a}\mu(d)W_{\bullet,d}
 =
 \sum_{r\in\mathcal R_{P,a}}\mu(r)B_{P,r}^{(a)}.}
 \tag{1.1}
\]

Consequently,

\[
 \boxed{
 D_a(I)=\left\|
 \beta_\bullet+
 \sum_{r\in\mathcal R_{P,a}}\mu(r)B_{P,r}^{(a)}
 \right\|_2^2.}
 \tag{1.2}
\]

For \(P=1\), one recovers \(B_{1,r}=W_{\bullet,r}\) and
\(\Delta_{1,a}=\Delta_a\).

#### Proof

Every squarefree \(d\) has the unique factorization

\[
 s=(d,P),\qquad r=d/s,
\]

with

\[
 s\mid P,\quad \mu(r)^2=1,\quad (r,P)=1,
 \quad \mu(d)=\mu(s)\mu(r).
\]

Conversely every such pair with \(sr<2a\) gives a squarefree \(d=sr\).
Reindexing the finite sum proves (1.1), and insertion into the physical row
formula proves (1.2).  No Möbius sign may be added inside or outside
\(B_{P,r}\).

The immediate comparison

\[
 0\le \Delta_{P,a}-\|\beta\|_2^2
 \le 2^{\omega(P)}
       (\Delta_{1,a}-\|\beta\|_2^2)
 \tag{1.3}
\]

follows from Cauchy--Schwarz within each group.  There is no converse lower
comparison.

## 2. Fixed-\(P\) continuum normalizer

Put

\[
 \delta=\frac6{\pi^2},\qquad
 \rho_P=\delta\prod_{p\mid P}\frac p{p+1}.
 \tag{2.1}
\]

Then

\[
 \#\{r\le x:\mu(r)^2=1,\ (r,P)=1\}
 =\rho_Px+O_P(\sqrt x).
 \tag{2.2}
\]

The row mesh has density \(\delta\), while the rough-column mesh has density
\(\rho_P\).  Thus the product density is \(\delta\rho_P\), not \(\rho_P^2\).

Extend the Cycle 45 kernel by zero:

\[
 \overline K_\theta(u,x)=
 \begin{cases}
 \displaystyle
 \frac1C\log\frac2{\max(1,u,x)}J(u,x),&0<x<2,\\[1ex]
 0,&x\ge2,
 \end{cases}
 \tag{2.3}
\]

where

\[
 J(u,v)=\int_0^\infty
 \left\{\frac yu\right\}\left\{\frac yv\right\}
 \frac{dy}{y^2}.
\]

Define

\[
 \boxed{
 F_{P,\theta}(u,v)=
 \sum_{s\mid P}\mu(s)\overline K_\theta(u,sv).}
 \tag{2.4}
\]

### Theorem 2.1: fixed-\(P\) grouped kernel and diagonal

For every fixed squarefree \(P\) and every fixed \(0<\varepsilon<2\),

\[
 \sup_{\substack{q\in S_a(I),\ r\in\mathcal R_{P,a}\\
                  \varepsilon\le r/a<2}}
 \left|aL B_{P,r}^{(a)}(q)
       -F_{P,\theta}(q/a,r/a)\right|\longrightarrow0.
 \tag{2.5}
\]

The convergence includes every threshold \(sr/a=2\): at equality the finite
summand is absent and the zero-extended limiting summand is zero.  The Cycle 45
right-end estimate supplies the uniform passage through these thresholds.

Moreover,

\[
 \boxed{
 L^2\Delta_{P,a}(I)\longrightarrow A_{P,\theta,I},}
 \tag{2.6}
\]

where

\[
 \boxed{
 A_{P,\theta,I}=\delta\rho_P
 \int_I\int_0^2F_{P,\theta}(u,v)^2\,dv\,du>0.}
 \tag{2.7}
\]

The affine column is retained in the exact finite definition, but
\(\|\beta_\bullet\|_2^2=O(a^{-1})=o(L^{-2})\).

#### Boundary at \(v=0\)

Uniform discrete convergence is not asserted down to fixed old labels.  The
required tightness is instead

\[
 \lim_{\varepsilon\downarrow0}\limsup_{a\to\infty}
 L^2\sum_{q\in S_a(I)}
 \sum_{\substack{r\in\mathcal R_{P,a}\\r\le\varepsilon a}}
 |B_{P,r}^{(a)}(q)|^2=0.
 \tag{2.8}
\]

Uniformly for \(u\in I\),

\[
 \boxed{
 J(u,v)=
 \frac{\log(1/v)+\log u+1+\log(2\pi)-\gamma}{2u}
 +o_I(1)\qquad(v\downarrow0).}
 \tag{2.9}
\]

Writing \(d_0(u)=\log(2/\max(1,u))\), this yields

\[
 F_{p,\theta}(u,v)\longrightarrow
 \frac{d_0(u)\log p}{2Cu}
 \quad(P=p\text{ prime}),
 \tag{2.10}
\]

and

\[
 F_{P,\theta}(u,v)\longrightarrow0
 \quad(\omega(P)\ge2).
 \tag{2.11}
\]

For \(P=1\) the logarithmic singularity from (2.9) remains, but is square
integrable.  Positivity in (2.7) is immediate on \(1<v<2\), where every
\(s>1\) term vanishes and \(F_{P,\theta}=K_\theta>0\).

For fixed \(P\), (2.6) implies the exact checkpoint equivalence

\[
 D_a(I)\gg L^{-3}
 \quad\Longleftrightarrow\quad
 \frac{D_a(I)}{\Delta_{P,a}(I)}\gg\frac1L,
 \tag{2.12}
\]

and

\[
 \liminf_{a\to\infty}L\frac{D_a}{\Delta_{P,a}}
 =\frac1{A_{P,\theta,I}}
   \liminf_{a\to\infty}L^3D_a.
 \tag{2.13}
\]

These are equivalences of open statements, not proofs that the liminfs are
positive.

## 3. Adjoining a prime and nonmonotonicity

Let \(p\nmid P\) be prime and \(Q=Pp\).  With the convention
\(B_{P,t}=0\) for \(t\ge2a\),

\[
 \boxed{B_{Q,r}=B_{P,r}-B_{P,pr}.}
 \tag{3.1}
\]

The rough labels for \(P\) split into the labels rough for \(Q\), and their
\(p\)-multiples.  Hence the square terms cancel exactly and

\[
 \boxed{
 \Delta_{Q,a}-\Delta_{P,a}
 =-2\sum_{\substack{r\in\mathcal R_{Q,a}\\pr<2a}}
 \langle B_{P,r},B_{P,pr}\rangle.}
 \tag{3.2}
\]

At the continuum level,

\[
 F_Q(u,v)=F_P(u,v)-F_P(u,pv),
 \qquad \rho_Q=\frac p{p+1}\rho_P,
\]

and therefore

\[
 \boxed{
 A_Q-A_P=-2\delta\rho_Q
 \int_I\int_0^{2/p}F_P(u,v)F_P(u,pv)\,dv\,du.}
 \tag{3.3}
\]

For \(P=1\), both factors are positive, so \(A_p<A_1\).  For general
\(P\), the displayed formula supplies no fixed sign for the cross integral.

Finite monotonicity fails in both directions in the physical matrix.  At
\(\theta=2/5\), \(a=64\), and \(I=[1,3/2]\), the accompanying verifier certifies

\[
 \Delta_{6,64}<\Delta_{2,64}<\Delta_{10,64},
 \tag{3.4}
\]

with

\[
 \begin{aligned}
 \Delta_{2,64}&=
 [0.0004915417361726970319139637097073533373331
   \mathbin{+/-}3.49\cdot10^{-44}],\\
 \Delta_{6,64}&=
 [0.0004887517173623030171600341041881708432743
   \mathbin{+/-}3.65\cdot10^{-44}],\\
 \Delta_{10,64}&=
 [0.0005069480456057754382915997890928778967797
   \mathbin{+/-}2.91\cdot10^{-44}].
 \end{aligned}
 \tag{3.5}
\]

Thus adjoining \(3\) to \(P=2\) decreases the grouped diagonal, while
adjoining \(5\) increases it.

## 4. Growing \(P\): a quantitative bookkeeping theorem

The exact grouping (1.1) holds for every finite squarefree \(P=P(a)\), but the
fixed-\(P\) limit may not be interchanged with a growing \(P\).  The proof of
the theorem in this section is given in Appendix A, with every dependence on
\(P,T,L\), and \(a\) explicit.  Let

\[
 T=2^{\omega(P)},\qquad
 \rho_P=\delta\prod_{p\mid P}\frac p{p+1},\qquad
 H=\log(2PL^4).
\]

A uniform elementary sieve estimate is

\[
 \#\{r\le x:\mu(r)^2=1,(r,P)=1\}
 =\rho_Px+O(T\sqrt x),
 \tag{4.1}
\]

and

\[
 \frac{T^2}{P}=\prod_{p\mid P}\frac4p\le\frac83.
 \tag{4.2}
\]

### Theorem 4.1: admissible growing range

Assume \(H\le L/4\) eventually and put

\[
 \begin{aligned}
 \mathcal E_a(P)={}&T^2\left(
 \frac{H^3}{L}+\frac{H^2PL^4}{a}
 +\frac{H^2}{PL^4}+\frac{L^2}{a}\right)\\
 &+\frac{T^2HP^{5/2}L^{17/2}}{a^{1/8}}
 +\frac{T^3H^2}{a^{1/4}}+\frac{L^2}{a}.
 \end{aligned}
 \tag{4.3}
\]

Then

\[
 \boxed{
 L^2\Delta_{P,a}(I)=A_{P,\theta,I}
 +O_{\theta,I}(\mathcal E_a(P)),}
 \tag{4.4}
\]

where \(A_{P,\theta,I}\) is the instantaneous expression (2.7).  In
particular, the two conditions

\[
 \frac{T^2H^3}{L}\to0,
 \qquad
 \frac{T^3P^3L^{10}}{a^{1/8}}\to0
 \tag{4.5}
\]

imply an absolute asymptotic.  If also

\[
 \mathcal E_a(P)\log\log(3P)\to0,
 \tag{4.6}
\]

then

\[
 L^2\Delta_{P,a}(I)=A_{P,\theta,I}(1+o(1)).
 \tag{4.7}
\]

The proof combines the Cycle 45 temporal and endpoint estimates, (4.1), the
left cutoff \(1/(PL^4)\), and a product-mesh Riemann sum.  A safe explicit
range is

\[
 P(a)\le L^{1-\eta}\qquad(\eta>0).
 \tag{4.8}
\]

For the primorial \(P(z)=\prod_{p\le z}p\), an explicit sufficient range is

\[
 z\le\left(\frac1{2\log2}-\eta\right)
       \log L\,\log\log L,
 \qquad 0<\eta<\frac1{2\log2}.
 \tag{4.9}
\]

The exact first primorial condition is

\[
 4^{\pi(z)}\bigl(\vartheta(z)+4\log L+\log2\bigr)^3=o(L).
 \tag{4.10}
\]

Equation (4.9) follows from the prime number theorem.  No uniformity beyond
these displayed conditions is asserted.

For fixed \(u\), Mellin--Plancherel gives the exact normalizer

\[
 \boxed{
 A_{P,\theta,I}=\frac{\delta^2}{2\pi}
 \int_I\int_{\mathbb R}|\widehat k_u(t)|^2
 \prod_{p\mid P}\left(
 1-\frac{2\sqrt p}{p+1}\cos(t\log p)
 \right)dt\,du,}
 \tag{4.11}
\]

where \(k_u(v)=\overline K_\theta(u,v)\) and

\[
 \widehat k_u(t)=\int_0^\infty k_u(v)v^{-1/2-it}\,dv.
\]

This is a specialization of standard Mellin scaling and Plancherel, not a new
Mellin identity.  Each factor can be below or above one, so product
differencing is not a contraction.

Under (4.7), the exact finite identity

\[
 L^3D_a=(L^2\Delta_{P,a})
 \left(L\frac{D_a}{\Delta_{P,a}}\right)
 \tag{4.12}
\]

becomes

\[
 L^3D_a=A_{P,\theta,I}
 \left(L\frac{D_a}{\Delta_{P,a}}\right)(1+o(1)).
 \tag{4.13}
\]

Thus a growing-\(P\) retention target must include \(A_P\); a bare
\(1/L\) fraction is not invariant.

The nonuniform extreme is decisive.  If
\(P_a=\prod_{p<2a}p\), then \(\mathcal R_{P_a,a}=\{1\}\) and

\[
 B_{P_a,1}=\sum_{d\in\mathcal D_a}\mu(d)W_{\bullet,d}.
 \tag{4.14}
\]

Grouping has merely moved all unresolved cancellation into one column.  The
resulting retention statement is tautological, while the fixed-\(P\) density
prediction fails badly.  Therefore finite-prime grouping is useful
bookkeeping, not coercivity.

## Appendix A. Proof of Theorem 4.1

Write

\[
 \ell(u,x)=\left(\log\frac2{\max(1,u,x)}\right)_+,
 \qquad k(u,x)=\frac{\ell(u,x)}C J(u,x),
\]

so that \(k=\overline K_\theta\), and put

\[
 m=\frac1{PL^4},\qquad h=a^{-1/4}.
 \tag{A.1}
\]

All constants in this appendix depend only on \(\theta\) and \(I\).  We may
assume \(a\) is large enough that \(L\ge2\) and \(H\ge1\).  Since
\(e^H=2PL^4\), the hypothesis \(H\le L/4\) gives

\[
 2PL^4\le a^{1/4},\qquad m\ge2h,
 \qquad Ph\le\frac1{2L^4}.
 \tag{A.2}
\]

In particular, every integer \(d\ge am\) satisfies

\[
 \log d\ge L-H+\log2\ge\frac{3L}{4}.
 \tag{A.3}
\]

### A.1. Rough squarefree counting

Uniformly in squarefree \(P\ge1\) and \(x\ge1\),

\[
 R_P(x):=\#\{r\le x:\mu(r)^2=1,(r,P)=1\}
 =\rho_Px+O(T\sqrt x).
 \tag{A.4}
\]

Indeed, \(\mu(n)^2=\sum_{j^2\mid n}\mu(j)\), so

\[
 R_P(x)=
 \sum_{\substack{j\le\sqrt x\\(j,P)=1}}\mu(j)
 \#\{b\le x/j^2:(b,P)=1\}.
\]

Inclusion--exclusion gives

\[
 \#\{b\le y:(b,P)=1\}
 =\frac{\varphi(P)}P y+O(T),
\]

with an absolute implied constant.  Extending the resulting \(j\)-sum to
infinity costs \(O(\sqrt x)\), and its Euler product is

\[
 \frac{\varphi(P)}P
 \sum_{\substack{j\ge1\\(j,P)=1}}\frac{\mu(j)}{j^2}
 =\frac1{\zeta(2)}\prod_{p\mid P}\frac p{p+1}=\rho_P.
\]

after multiplying by \(x\).  This proves (A.4).  Thus, uniformly for
intervals \(U,V\subset[0,2]\),

\[
 \#\{q\in aU:\mu(q)^2=1\}
 =\delta a|U|+O(\sqrt a),
 \tag{A.5}
\]

\[
 \#\{r\in aV:\mu(r)^2=1,(r,P)=1\}
 =\rho_Pa|V|+O(T\sqrt a).
 \tag{A.6}
\]

### A.2. Bounds and a modulus for \(J\)

Uniformly for \(u\in I\) and \(0<x\le3\),

\[
 0\le J(u,x)\ll_I1+\log_+\frac1x.
 \tag{A.7}
\]

For small \(x\), split the defining integral at \(x\) and at
\(u_0=\inf I>0\).  On \(x<y<u_0\), use
\(\{y/u\}=y/u\) and \(0\le\{y/x\}\le1\); the other two pieces are bounded
immediately.  This proves (A.7).

Put \(\phi_x(y)=\{y/x\}\) in
\(L^2((0,\infty),dy/y^2)\).  If \(b=\min(x,x')\) and
\(d=|x-x'|\), then

\[
 \|\phi_x-\phi_{x'}\|_2^2
 \ll \frac d{b^2}\left(1+\log_+\frac bd\right),
 \tag{A.8}
\]

with the right side interpreted as zero for \(d=0\).  For \(d\ge b/2\), this
follows from the diagonal norm bound.  Otherwise scale to
\(x'=x(1+\varepsilon)\).  On the unit interval \([j,j+1)\),
\(j\le\varepsilon^{-1}\), the phase displacement is
\(O(\varepsilon j)\), and wraparound occurs on a set of length
\(O(\varepsilon j)\).  Its weighted contribution is therefore
\(O(\varepsilon/j)\).  The intervals \(j>\varepsilon^{-1}\) contribute
\(O(\varepsilon)\) in total.  Summation and rescaling prove (A.8).

If

\[
 u,u'\in I+[-h,h],\quad v,v'\in[m,2],
 \quad |u-u'|,|v-v'|\le h,
\]

then Cauchy--Schwarz, (A.2), and (A.8) give, for every \(s\mid P\),

\[
 |J(u,sv)-J(u',sv')|
 \ll_I m^{-1}\sqrt{PhL}.
 \tag{A.9}
\]

Here dilation by \(s\) does not lose a factor: in the second-variable norm,

\[
 \frac{|sv-sv'|}{\min(sv,sv')^2}
 =\frac{|v-v'|}{s\min(v,v')^2}.
\]

The support factor \(\ell\) is bounded and Lipschitz on the active region,
while (A.7) gives \(J(u,x)\ll_IH\) for \(m\le x<2\).  Hence the deliberately
coarse bound

\[
 |k(u,sv)-k(u',sv')|
 \ll_{\theta,I}m^{-2}\sqrt{PhL}
 \tag{A.10}
\]

holds.  Consequently, on \(I\times[m,2]\),

\[
 |F_{P,\theta}(u,v)|\ll_{\theta,I}TH,
 \tag{A.11}
\]

and the oscillation of \(F_{P,\theta}^2\) on an \(h\)-by-\(h\) cell is

\[
 O_{\theta,I}\!\left(
 T^2HP^{5/2}L^{17/2}a^{-1/8}\right).
 \tag{A.12}
\]

### A.3. Uniform temporal approximation

Let \(u=q/a\in I\), \(x=d/a\in[m,2)\),
\(n_0=\max(a,q,d)\), and

\[
 \alpha=\log u,\qquad \beta=\log x,
 \qquad x_n=\log(n/a),\qquad
 \delta_n=\log\frac{n+1}{n}.
\]

The exact Cycle 45 coefficient identity is

\[
 \begin{aligned}
 w_nA_nb_q(n)b_d(n)
 ={}&Cw_n
 \left(\frac{\log q}{\log n}-\frac{1-2\theta}{C}\right)
 \left(\frac{\log d}{\log n}-\frac{1-2\theta}{C}\right)\\
 &+w_n^2\left(
 \frac{(1-2\theta)^2}{CA_n}
 -\frac{\log q\log d}{(\log n)^2}\right).
 \end{aligned}
 \tag{A.13}
\]

Since

\[
 \frac{\log q}{\log n}-\frac{1-2\theta}{C}
 =\frac1C+\frac{\alpha-x_n}{L+x_n},
\]

and similarly for \(d\), while
\(|\alpha-x_n|\ll_I1\) and \(|\beta-x_n|\ll H\), the first line of
(A.13), after multiplication by \(L\), equals

\[
 \frac{\delta_n}{C}
 +O_{\theta,I}\left(\delta_n\frac HL\right).
 \tag{A.14}
\]

All logarithmic ratios in the second line are bounded by (A.3), and
\(A_n\ge1-2\theta>0\).  Thus its total contribution after multiplication by
\(L\) is

\[
 O_{\theta,I}\left(L\sum_{n=n_0}^{2a-1}w_n^2\right)
 \ll\frac1{aL}.
 \tag{A.15}
\]

Since \(\sum_{n=n_0}^{2a-1}\delta_n=\log(2a/n_0)=\ell(u,x)\),

\[
 \left|LH_a(q,d)-\frac{\ell(u,x)}C\right|
 \ll_{\theta,I}\frac HL+\frac1{aL}.
 \tag{A.16}
\]

The exact spatial dilation identity is

\[
 a\langle\rho_q,\rho_d\rangle
 =J(u,x)-\frac1{aux}.
 \tag{A.17}
\]

Combining (A.7), (A.16), and (A.17) gives

\[
 |aLW_a(q,d)-k(u,x)|
 \ll_{\theta,I}\frac{H^2}{L}+\frac{PL^4}{a}.
 \tag{A.18}
\]

This estimate is uniform at \(x=m\).  It is also endpoint-safe.  Directly
from (A.13), when \(a\le d<2a\),

\[
 |aLW_a(q,d)|+|k(u,d/a)|
 \ll_{\theta,I}2-\frac da.
 \tag{A.19}
\]

Thus both the finite term and its zero extension vanish at \(d=2a\); no
half-weight or separate internal-threshold term occurs.

### A.4. The left layers

For \(q/a\in I\) and \(1\le d\le a\), the coefficients in the temporal sum
are bounded and \(\sum_{a\le n<2a}w_n\ll L^{-1}\), so
\(|H_a(q,d)|\ll_{\theta,I}L^{-1}\).  Moreover,

\[
 0\le a\langle\rho_q,\rho_d\rangle\le J(q/a,d/a).
\]

By (A.7),

\[
 |W_a(q,d)|
 \ll_{\theta,I}\frac{1+\log(a/d)}{aL}.
 \tag{A.20}
\]

If \(r<am=a/(PL^4)\), then \(sr<a/L^4<a\) for every \(s\mid P\), whence

\[
 |B_{P,r}^{(a)}(q)|
 \ll_{\theta,I}\frac{T(1+\log(a/r))}{aL}.
 \tag{A.21}
\]

The elementary integral comparison

\[
 \sum_{r\le R}(1+\log(a/r))^2
 \ll R(1+\log(a/R))^2+L^2
 \tag{A.22}
\]

therefore yields

\[
 L^2\sum_{q\in S_a(I)}
 \sum_{\substack{r\in\mathcal R_{P,a}\\r<am}}
 |B_{P,r}^{(a)}(q)|^2
 \ll_{\theta,I}T^2\left(
 \frac{H^2}{PL^4}+\frac{L^2}{a}\right).
 \tag{A.23}
\]

For \(0<v<m\), every \(sv<1/L^4\), so (A.7) gives

\[
 \int_I\int_0^m F_{P,\theta}(u,v)^2\,dv\,du
 \ll_{\theta,I}\frac{T^2H^2}{PL^4}.
 \tag{A.24}
\]

### A.5. Bulk comparison and the product mesh

For \(r/a=v\in[m,2)\), put
\(G_a(q,r)=aLB_{P,r}^{(a)}(q)\).  Summing (A.18) over \(s\mid P\), with the
zero extension and (A.19) at each threshold, gives

\[
 G_a(q,r)=F_{P,\theta}(u,v)+R_a(q,r),
 \qquad
 |R_a(q,r)|\ll_{\theta,I}T\left(
 \frac{H^2}{L}+\frac{PL^4}{a}\right).
 \tag{A.25}
\]

Using (A.11), \(|x^2-y^2|\le|x-y|(2|y|+|x-y|)\), and at most \(4a^2\)
pairs, we obtain

\[
 \begin{aligned}
 &\left|\frac1{a^2}\sum_{q,r}G_a(q,r)^2
 -\frac1{a^2}\sum_{q,r}F_{P,\theta}(q/a,r/a)^2\right|\\
 &\qquad\ll_{\theta,I}T^2\left(
 \frac{H^3}{L}+\frac{H^2PL^4}{a}\right),
 \end{aligned}
 \tag{A.26}
\]

where both sums in (A.26) are over
\(q\in S_a(I)\), \(r\in\mathcal R_{P,a}\), and \(r\ge am\).

Partition \(I\) and \([m,2)\) into disjoint half-open intervals
\(U_i,V_j\) of lengths at most \(h\); only the final row cell is right-closed
when needed to retain the endpoint of \(I\).  This assigns each lattice point
once and excludes \(r=2a\).  Set

\[
 Q_i=\#\{q\in aU_i:\mu(q)^2=1\},\qquad
 R_j=\#\{r\in aV_j:\mu(r)^2=1,(r,P)=1\}.
\]

Equations (A.5)--(A.6) imply

\[
 \left|Q_iR_j-\delta\rho_Pa^2\,|U_i|\,|V_j|\right|
 \ll T a^{3/2}(|U_i|+|V_j|)+Ta.
 \tag{A.27}
\]

There are \(O(h^{-1})\) cells in each coordinate.  Summing (A.27) and
dividing by \(a^2\) gives \(O(Ta^{-1/4})\).  Multiplication by the bound in
(A.11) contributes

\[
 O_{\theta,I}(T^3H^2a^{-1/4}).
 \tag{A.28}
\]

Replacing each discrete and continuum value by a representative value in its
cell costs at most the oscillation (A.12).  Hence

\[
 \begin{aligned}
 &\left|\frac1{a^2}
 \sum_{\substack{q\in S_a(I)\\r\in\mathcal R_{P,a},\ r\ge am}}
 F_{P,\theta}(q/a,r/a)^2
 -\delta\rho_P\int_I\int_m^2F_{P,\theta}(u,v)^2\,dv\,du\right|\\
 &\quad\ll_{\theta,I}
 \frac{T^2HP^{5/2}L^{17/2}}{a^{1/8}}
 +\frac{T^3H^2}{a^{1/4}}.
 \end{aligned}
 \tag{A.29}
\]

Combining (A.23)--(A.24), (A.26), and (A.29) proves the non-affine part of
(4.4).  Finally,

\[
 g_q=\frac{\log q+1-\gamma}{q}\ll_I\frac La,
 \qquad H_a^0(q)\ll_{\theta,I}\frac1L,
\]

so \(|\beta_a(q)|\ll_{\theta,I}a^{-1}\) and

\[
 L^2\|\beta_\bullet\|_2^2\ll_{\theta,I}\frac{L^2}{a}.
 \tag{A.30}
\]

This completes (4.4), with precisely the error displayed in (4.3).

### A.6. Relative asymptotic and explicit ranges

On every compact subrectangle of \(I^\circ\times(1,2)\), all \(s>1\) terms
vanish and \(F_{P,\theta}=K_\theta>0\).  Therefore

\[
 A_{P,\theta,I}\gg_{\theta,I}\rho_P.
 \tag{A.31}
\]

The elementary Euler-product bound, valid for \(y\ge3\),

\[
 \prod_{p\le y}\left(1-\frac1p\right)^{-1}\ll\log y
 \tag{A.32}
\]

implies

\[
 \rho_P\gg\frac1{\log\log(3P)}.
 \tag{A.33}
\]

For completeness, take \(y=\log(3P)\).  The factors with \(p\mid P\),
\(p\le y\), are bounded by (A.32); if \(k\) prime factors of \(P\) exceed
\(y\), then \(y^k\le P\), so their reciprocal sum is at most
\(\log P/(y\log y)\le1/\log y\), and their product is bounded.  This proves
(A.33).  Equation (A.32), in turn, follows by applying the central-binomial
coefficient bound to obtain \(\vartheta(x)\ll x\), partial summation to get
\(\sum_{p\le y}(\log p)/p\ll\log y\), and comparing the finite product with
\(\zeta(1+1/\log y)\).

Equations (A.31)--(A.33) show that (4.6) upgrades (4.4) to (4.7).

To see that (4.5) implies \(\mathcal E_a(P)\to0\), put

\[
 X=\frac{T^2H^3}{L},\qquad
 Y=\frac{T^3P^3L^{10}}{a^{1/8}}.
\]

Then

\[
 \frac{T^2H^2}{PL^4}=\frac X{PHL^3},
\]

\[
 \frac{T^2H^2PL^4}{a}
 =Y^8\frac{H^2}{T^{22}P^{23}L^{76}},
 \qquad
 \frac{T^2L^2}{a}
 =\frac{Y^8}{T^{22}P^{24}L^{78}},
\]

\[
 \frac{T^2HP^{5/2}L^{17/2}a^{-1/8}}Y
 =\frac{H}{T\sqrt P\,L^{3/2}}
 \le\frac1{4T\sqrt{PL}},
\]

and

\[
 \frac{T^3H^2}{a^{1/4}}
 =Y^2\frac{H^2}{T^3P^6L^{20}}.
\]

Thus every term in (4.3) tends to zero when \(X,Y\to0\).

If \(P\le L^{1-\eta}\), then (4.2) gives \(T^2\ll P\) and
\(T^3\ll P^{3/2}\), while \(H\ll_\eta\log L\).  Consequently

\[
 \frac{T^2H^3}{L}\ll_\eta L^{-\eta}(\log L)^3\to0,
\]

and

\[
 \frac{T^3P^3L^{10}}{a^{1/8}}
 \ll_\eta L^{10+\frac92(1-\eta)}a^{-1/8}\to0.
\]

The same estimates remain \(o(1)\) after multiplication by
\(\log\log(3P)\), proving (4.8) with the relative asymptotic.

Finally let \(P=P(z)=\prod_{p\le z}p\), put
\(c=(2\log2)^{-1}\), \(\lambda=\log L\), and assume

\[
 z\le(c-\eta)\lambda\log\lambda,
 \qquad 0<\eta<c.
\]

Set \(Z=(c-\eta)\lambda\log\lambda\).  Bounded \(z\) is immediate.  In the
remaining case, monotonicity and the prime number theorem applied at \(Z\)
give

\[
 \pi(z)\le\pi(Z)=(c-\eta+o(1))\lambda,
 \qquad
 \vartheta(z)\le\vartheta(Z)=O_\eta(\lambda\log\lambda).
\]

Since

\[
 H=\vartheta(z)+4\lambda+\log2,
 \qquad \log H=O(\log\lambda)=o(\lambda),
\]

we have

\[
 \log\frac{4^{\pi(z)}H^3}{L}
 \le-(2\eta\log2+o(1))\lambda+O(\log\lambda)\to-\infty.
 \tag{A.34}
\]

Also

\[
 \log\left(\frac{T^3P^3L^{10}}{a^{1/8}}\right)
 =3\pi(z)\log2+3\vartheta(z)+10\lambda-\frac L8
 =-\frac L8+O_\eta(\lambda\log\lambda)\to-\infty.
 \tag{A.35}
\]

Finally \(\log\log(3P(z))\ll_\eta\log\lambda\).  The first error in
(A.34) decays like a fixed negative power of \(L\),
\(T^2H^2/(PL^4)\le(8/3)H^2/L^4\), and every term containing
\(a^{-1/8}\), \(a^{-1/4}\), or \(a^{-1}\) is
\(\exp\{-c_0L+O_\eta(\lambda\log\lambda)\}\) for some \(c_0>0\).
Therefore (4.6) holds as well.  This proves (4.9) and completes the proof of
Theorem 4.1. \(\square\)

## 5. Exact temporal-row contraction

For \(a\le n<2a\), put

\[
 L_n=\log n,\qquad
 w_n=1-\frac{L_n}{L_{n+1}},\qquad
 A_n=2(1-\theta)-w_n,
\]

\[
 \eta_n=\frac{1-2\theta}{A_n},\qquad
 b_d(n)=\frac{\log d}{L_n}-\eta_n.
\]

In

\[
 H=L^2([1,\infty),dt/t^2),
 \qquad \chi(t)=1,\qquad \rho_d(t)=\{t/d\},
\]

define

\[
 U_n=\chi+\sum_{d\le n}\mu(d)\rho_d,
 \qquad
 \mathscr D_n=\sum_{d\le n}\mu(d)(\log d)\rho_d,
\]

\[
 Z_n=\frac{\mathscr D_n}{L_n}-\eta_nU_n
 =-\eta_n\chi+\sum_{d\le n}\mu(d)b_d(n)\rho_d.
 \tag{5.1}
\]

The affine vector \(\chi\) is essential; deleting it invalidates the initial
block formula below.  For squarefree \(q<2a\), set

\[
 \alpha_{q,n}=w_nA_nb_q(n),
 \qquad \mathcal K_{q,n}=\langle\rho_q,Z_n\rangle_H.
\]

### Theorem 5.1: exact row contraction

\[
 \boxed{
 \widehat c_a(q)=
 \sum_{n=\max(a,q)}^{2a-1}\alpha_{q,n}\mathcal K_{q,n}.}
 \tag{5.2}
\]

No \(n=2a\) term occurs.  This is obtained by reversing the finite divisor and
time sums in the Cycle 45 definition.

## 6. Gcd-grouped finite summation by parts

Define

\[
 m_n=\sum_{d\le n}\frac{\mu(d)}d,
 \qquad
 \ell_n=\sum_{d\le n}\frac{\mu(d)\log d}{d},
\]

\[
 s_n=\frac{\ell_n}{L_n}-\eta_nm_n,
 \qquad
 g_q=\langle\chi,\rho_q\rangle
 =\frac{\log q+1-\gamma}{q}.
\]

### Theorem 6.1: exact gcd decomposition

For every contributing \(n\ge q\),

\[
 \boxed{
 \mathcal K_{q,n}=
 -\eta_ng_q-\frac{s_n}{q}
 +\sum_{h\mid q}\frac{\mu(h)}h
 \sum_{\substack{r\le\lfloor n/h\rfloor\\(r,q)=1}}
 \mu(r)b_{hr}(n)J(q/h,r).}
 \tag{6.1}
\]

The squarefree bijection is

\[
 d=hr,\qquad h=(q,d),\qquad h\mid q,
 \qquad (r,q)=1.
\]

The stronger condition \((r,q)=1\), rather than merely
\((r,q/h)=1\), is essential.  Spatial dilation gives

\[
 \langle\rho_q,\rho_{hr}\rangle_H
 =\frac1hJ(q/h,r)-\frac1{qhr},
\]

so the restricted-domain rank-one correction contracts exactly to
\(-s_n/q\).

If

\[
 M_q(x)=\sum_{\substack{r\le x\\(r,q)=1}}\mu(r),
 \quad X=\lfloor n/h\rfloor,
 \quad \Phi(r)=b_{hr}(n)J(q/h,r),
\]

then ordinary finite summation by parts yields

\[
 \boxed{
 \sum_{\substack{r\le X\\(r,q)=1}}\mu(r)\Phi(r)
 =M_q(X)\Phi(X)+
 \sum_{r=1}^{X-1}M_q(r)(\Phi(r)-\Phi(r+1)).}
 \tag{6.2}
\]

There is no omitted lower endpoint, and the second sum is empty for \(X=1\).
All sums in (5.2), (6.1), and (6.2) are finite; no continuation of
\(1/\zeta\) is used.

## 7. Initial non-wrapped interval and tail

For \(n\ge q\), define

\[
 \mathcal F_{q,n}=\int_1^q\rho_q(t)Z_n(t)\frac{dt}{t^2},
 \qquad
 \mathcal T_{q,n}=\mathcal K_{q,n}-\mathcal F_{q,n}.
\]

The interval \(1\le t<q\) is the initial non-wrapped block of \(\rho_q\); this
terminology avoids confusion with cotangent period functions.

Set

\[
 C_q=\sum_{m<q}\Lambda(m)\log\frac qm.
\]

### Theorem 7.1: exact initial-block formula

\[
 \boxed{
 \mathcal F_{q,n}=
 \frac{q-1}{q}s_n+\frac{C_q}{qL_n}.}
 \tag{7.1}
\]

Indeed, for \(1\le k<q\le n\), the complete finite convolutions are

\[
 1-\sum_{d\le n}\mu(d)\left\lfloor\frac kd\right\rfloor=0,
\]

\[
 -\sum_{d\le n}\mu(d)(\log d)
 \left\lfloor\frac kd\right\rfloor=\psi(k).
\]

Thus \(Z_n(t)=s_nt+\psi(k)/L_n\) on \(k<t<k+1\), while
\(\rho_q(t)=t/q\).  Integration and the finite telescope

\[
 \sum_{k=1}^{q-1}\psi(k)\log\frac{k+1}{k}
 =\sum_{m<q}\Lambda(m)\log\frac qm
\]

prove (7.1).  The formula also holds at \(q=1\), with both sides zero.

Writing

\[
 E_q=C_q-(q-1),\qquad
 R_n=\frac{\ell_n+1}{L_n}-\eta_nm_n=s_n+\frac1{L_n},
\]

gives the Chebyshev-\(\psi\)/reciprocal-Möbius-moment split

\[
 \boxed{
 \mathcal F_{q,n}=
 \frac{E_q}{qL_n}+\frac{q-1}{q}R_n.}
 \tag{7.2}
\]

Define the row vectors

\[
 P_a(q)=\sum_{n=\max(a,q)}^{2a-1}
 \alpha_{q,n}\mathcal F_{q,n},
 \qquad
 T_a(q)=\widehat c_a(q)-P_a(q).
\]

Then exactly

\[
 \boxed{
 D_a(I)=\|P_a+T_a\|_2^2
 =\|P_a\|_2^2+\|T_a\|_2^2
 +2\langle P_a,T_a\rangle.}
 \tag{7.3}
\]

The source functions supported on \([1,q)\) and \([q,\infty)\) are
orthogonal in \(H\), but their contractions through the common row
\(\rho_q\) are not.  Hence that source orthogonality cannot delete the cross
term in (7.3).

The only safe one-dimensional row-space estimate is the following.  If
\(P_a\ne0\), let

\[
 \gamma_a=1+\frac{\langle P_a,T_a\rangle}{\|P_a\|^2},
 \qquad
 R_a=P_a+T_a-\gamma_aP_a.
\]

Then \(R_a\perp P_a\), and

\[
 \boxed{
 D_a(I)=\gamma_a^2\|P_a\|^2+\|R_a\|^2
 \ge
 \frac{(\|P_a\|^2+\langle P_a,T_a\rangle)^2}
      {\|P_a\|^2}.}
 \tag{7.4}
\]

When \(P_a=0\), the quotient is not used and
\(D_a(I)=\|T_a\|^2\).  A sufficient target-scale theorem would be

\[
 \|P_a\|^2\ge c_0L^{-3},
 \qquad
 \langle P_a,T_a\rangle
 \ge-(1-\varepsilon)\|P_a\|^2
 \tag{7.5}
\]

with fixed \(c_0,\varepsilon>0\).  Neither premise is proved, and (7.5)
retains the unresolved anti-cancellation.

## 8. Certified physical counterexample

At \(\theta=2/5\), \(a=512\), and the squarefree row
\(q=742=2\cdot7\cdot53\), the fail-closed 256-bit verifier gives

\[
 \begin{aligned}
 P_a^\psi(742)&=
 [-1.0684594597330754558\cdot10^{-4}
  \mathbin{+/-}1.70\cdot10^{-44}],\\
 P_a^M(742)&=
 [8.4854750258150568658\cdot10^{-5}
  \mathbin{+/-}6.76\cdot10^{-46}],\\
 P_a(742)&=
 [-2.1991195715156976923\cdot10^{-5}
  \mathbin{+/-}2.34\cdot10^{-45}],\\
 T_a(742)&=
 [2.2349344543199367292\cdot10^{-5}
  \mathbin{+/-}3.51\cdot10^{-45}],\\
 \widehat c_a(742)&=
 [3.5814882804239036936\cdot10^{-7}
  \mathbin{+/-}3.34\cdot10^{-47}].
 \end{aligned}
 \tag{8.1}
\]

Thus

\[
 \frac{\widehat c_a(742)^2}{P_a(742)^2}
 =0.0002652341138898903\ldots,
 \tag{8.2}
\]

and

\[
 \frac{\widehat c_a(742)^2}
      {P_a(742)^2+T_a(742)^2}
 =0.0001304748392503447\ldots.
 \tag{8.3}
\]

This is a physical finite counterexample to any universal finite pointwise rule
that retains the initial-block square, the initial-plus-tail diagonal, or the
Chebyshev square as a lower bound before restoring its signed cross terms.  It
is not an asymptotic counterexample to (7.5), and proves no failure of the
Cycle 45 liminf target.

## 9. Verification and literature boundary

The accompanying certificate

- checks 504 exact grouping cases;
- checks 5,381 adjoining-prime column identities and 504 formal diagonal
  increment identities;
- checks 160 Möbius/Chebyshev convolution cases, 120 formal prime-log
  telescopes, and 600 coprime-Mertens Abel identities;
- certifies the physical nonmonotonicity (3.4)--(3.5);
- performs a three-path internal reconstruction of (8.1) by coefficient-index,
  nested temporal, and prefix-spatial contractions; and
- fails closed on runtime or bound-input hash changes.

Reproduce from the repository root with

```bash
env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 \
  uv run --isolated --no-project \
  --python 3.12.13 --with python-flint==0.9.0 \
  python -I -B \
  millennium-prize/riemann-hypothesis/cycle46_finite_identity_verifier.py \
  > /tmp/cycle46.out
cmp millennium-prize/riemann-hypothesis/cycle46-finite-identity-verifier.out \
    /tmp/cycle46.out
```

The fixed-prime grouping is elementary finite inclusion-exclusion; the density
is a standard squarefree-sieve fact; finite Abel summation and Mellin--Plancherel
are standard.  The defensible contribution here is their exact assembly for
the moving Möbius--Vasyunin matrix and the finite certified counterexamples.
No claim of bibliographic priority is made for an identity merely because it
was not located in the focused search.

Primary references for the imported fractional-part and cotangent identities
are Vasyunin (1995/1996), Báez-Duarte (2002, 2003),
Báez-Duarte--Balazard--Landreau--Saias (2005), and Bettin--Conrey (2013).
The Euclidean continued-fraction evaluation tested during this cycle is the
published formula of Goubi--Bayad--Hernane (2017), with the period-function
coefficient convention \(g_1=+1/2\) recorded by Akatsuka--Murakami (2025).
That evaluator remains prototype infrastructure until its precision-to-tail
policy is integrated fail closed.

## 10. Surviving frontier

Cycle 46 changes coordinates but does not lower the arithmetic difficulty.
The physical vector is unchanged under finite-prime grouping, while the
finite grouped diagonal changes and is not monotone in the certified example.
The initial non-wrapped block is an explicit Chebyshev/reciprocal-Möbius
expression, but a physical row can be almost exactly canceled by the tail.

The next theorem must therefore control a **signed cross term** rather than a
separate diagonal.  Two exact formulations are:

1. the original weighted two-point Möbius packet inequality (Cycle 45,
   equation (11.3)); or
2. for one fixed interval, a target-scale form of (7.5), with the complete tail
   (6.1)--(6.2) and every affine, gcd, endpoint, and Vasyunin term retained.

No partial theorem in this note is a solution of RH.
