# Cycle 50: one-source prefix collapse, a positive square kernel, and a mixed-retention obstruction

## Status and scope

This note continues the canonical complete-prefix program of Cycles 47--49 on

\[
 I_0=[1,3/2].
\]

It proves four structural results.

1. The complete prefix has an exact pure-Möbius coefficient representation,
   with no separate affine coordinate, obtained from a finite cumulative-floor
   identity that is valid only on the prefix.
2. The same prefix has an exact one-source Möbius--von Mangoldt representation
   and a factorial closure.
3. Its current-label coefficient kernel has an explicit locally uniform limit.
   The symmetric part of that limit is positive definite on every finite set
   of labels below the endpoint, and defines an injective compact positive
   operator on the stated common square domains.
4. The physical prefix/full retention form is not governed by that positive
   square kernel.  It is a mixed rectangular cross-kernel with a
   difference-of-Grams factorization.  An interval certificate already gives a
   negative principal minor at \(a=3\).

The positive-kernel theorem is therefore a theorem about the collapsed prefix
kernel on one common square label space.  It is **not** a positivity theorem
for the nonsymmetric kernel, the physical rectangular map, the prefix/full
normal matrix, or the selected Möbius contraction.

Nothing here proves

\[
 \|B_a\|_2^2\gg (\log a)^{-3},\qquad
 \mathcal Q_a^{\rm cp}\gg (\log a)^{-3},\qquad
 D_a(I_0)\gg(\log a)^{-3},
\]

a signed tail-retention estimate, a completed-square budget, or the Riemann
hypothesis.  No entrywise current-label limit below is passed through a growing
signed Möbius sum.

Fix

\[
 a\ge2,\qquad 0<\theta<\frac12,\qquad
 C=2(1-\theta),\qquad \tau=C-1,
\]

and put

\[
 M=2a-1,\qquad L_n=\log n,\qquad
 \delta_n=\log\frac{n+1}{n},
\]

\[
 w_n=1-\frac{L_n}{L_{n+1}}=\frac{\delta_n}{L_{n+1}},
 \qquad A_n=C-w_n,\qquad \eta_n=\frac{\tau}{A_n},
\]

\[
 b_q(n)=\frac{\log q}{L_n}-\eta_n,
 \qquad \alpha_{q,n}=w_nA_nb_q(n).
 \tag{0.1}
\]

Physical rows are squarefree integers

\[
 q\in\mathcal Q_a=
 \{q:\mu(q)^2=1,\ a\le q\le 3a/2\}.
\]

The finite identities below in fact need only \(a\le q\le n\le M\), so
\(n<2q\); squarefreeness is irrelevant until rows are selected.

Write

\[
 \rho_d(t)=\{t/d\},\qquad \chi(t)=1,
 \qquad H=L^2([1,\infty),dt/t^2).
\]

For \(d\ge1\), define

\[
 P_{q,n}(d)=\int_1^{n+1}\rho_q(t)\rho_d(t)\frac{dt}{t^2},
 \tag{0.2}
\]

and distinguish the two affine integrals

\[
 P_{q,n}(0)=\int_1^{n+1}\rho_q(t)\frac{dt}{t^2}
 =\frac{\log(n+1)-1}{q}+\frac1{n+1},
 \tag{0.3}
\]

\[
 \mathfrak a_{q,n}=\int_1^{n+1}\rho_q(t)\frac{dt}{t}
 =\frac nq-\log\frac{n+1}{q}.
 \tag{0.4}
\]

In particular, \(P_{q,n}(0)\ne\mathfrak a_{q,n}\).

## 1. Exact finite prefix collapse

Put

\[
 m_n=\sum_{d\le n}\frac{\mu(d)}d,
 \qquad
 U_n(t)=1+\sum_{d\le n}\mu(d)\rho_d(t).
\]

### Lemma 1.1 (cumulative-floor identity)

For every integer \(1\le k\le n\) and every
\(t\in[k,k+1)\),

\[
 \sum_{d\le n}\mu(d)\left\lfloor\frac td\right\rfloor=1.
 \tag{1.1}
\]

Consequently, almost everywhere on \([1,n+1)\),

\[
 \boxed{U_n(t)=m_nt.}
 \tag{1.2}
\]

#### Proof

On the indicated half-open cell, terms with \(d>k\) vanish and

\[
 \begin{aligned}
 \sum_{d\le n}\mu(d)\left\lfloor\frac td\right\rfloor
 &=\sum_{d\le k}\mu(d)\left\lfloor\frac kd\right\rfloor\\
 &=\sum_{j\le k}\sum_{d\mid j}\mu(d)=1.
 \end{aligned}
\]

The last equality uses the cumulative divisor sum.  It must not be replaced
by the false assertion \(\sum_{d\mid k}\mu(d)=1\), which equals zero for
\(k>1\).  Since

\[
 U_n(t)=1+t\sum_{d\le n}\frac{\mu(d)}d
       -\sum_{d\le n}\mu(d)\left\lfloor\frac td\right\rfloor,
\]

(1.2) follows.  No assertion is made for \(t>n+1\).  At the terminal point
\(t=n+1\), the value is immaterial to every integral used here.  \(\square\)

Pairing (1.2) with \(\rho_q\mathbf1_{[1,n+1]}\) gives the exact collapse

\[
 \boxed{
 P_{q,n}(0)+\sum_{d\le n}\mu(d)P_{q,n}(d)
 =m_n\mathfrak a_{q,n}.}
 \tag{1.3}
\]

The complete-prefix cell is

\[
 \mathcal B_{q,n}
 =\frac1{L_n}\sum_{d\le n}\mu(d)(\log d)P_{q,n}(d)
 -\eta_n\left(P_{q,n}(0)+\sum_{d\le n}\mu(d)P_{q,n}(d)\right).
 \tag{1.4}
\]

Using (1.3) and \(m_n=\sum_{d\le n}\mu(d)/d\) yields

\[
 \mathcal B_{q,n}
 =\sum_{d\le n}\mu(d)
 \left[\frac{\log d}{L_n}P_{q,n}(d)
       -\frac{\eta_n\mathfrak a_{q,n}}d\right].
 \tag{1.5}
\]

Therefore the actual complete-prefix vector has the exact pure-Möbius form

\[
 \boxed{B_a(q)=\sum_{d=1}^{M}\mu(d)W_B(q,d),}
 \tag{1.6}
\]

where

\[
 \boxed{
 W_B(q,d)=\sum_{n=\max(q,d)}^{M}\alpha_{q,n}
 \left[\frac{\log d}{L_n}P_{q,n}(d)
       -\frac{\eta_n\mathfrak a_{q,n}}d\right].}
 \tag{1.7}
\]

This gauge differs from the augmented-affine coefficient gauge of Cycle 49:
it redistributes the finite prefix affine packet among the Möbius columns.
Both gauges give the same selected vector, but their individual columns and
their entrywise limits differ.

### Endpoint ledger

Equation (1.7) includes all of the following.

- The column \(d=1\) remains; \(\log1=0\), but its collapse term does not
  vanish.
- The column \(d=M\) has the single temporal term \(n=M\).
- The final complete cell \(n=M=2a-1\) is included.  There is no temporal
  term \(n=2a\).
- There is no affine label \(d=0\) in (1.6), and there is no outer
  \(\mu(q)\).
- There are no endpoint half-weights.
- When \(q=a,n=M\), the possible second wrap \(t=2q=2a\) is only the
  terminal singleton and has zero integral mass.

## 2. One-source Möbius--von Mangoldt and factorial forms

Define

\[
 \mathcal R_{q,n}=L_n\mathcal B_{q,n}
 =\sum_{d\le n}\mu(d)
 \left[(\log d)P_{q,n}(d)
       -\frac{\eta_nL_n\mathfrak a_{q,n}}d\right],
 \tag{2.1}
\]

and, for \(1\le m\le n\),

\[
 \boxed{
 \mathscr K_{q,n}(m)=
 \sum_{r\le\lfloor n/m\rfloor}\Lambda(r)P_{q,n}(mr)
 +\frac{\eta_nL_n\mathfrak a_{q,n}}m.}
 \tag{2.2}
\]

The convolution identity

\[
 (\mu*\Lambda)(d)=-\mu(d)\log d
 \tag{2.3}
\]

includes \(d=1\), where both sides vanish.  Finite reindexing of (2.1)
therefore gives

\[
 \boxed{\mathcal R_{q,n}=-\sum_{m\le n}\mu(m)\mathscr K_{q,n}(m).}
 \tag{2.4}
\]

Thus

\[
 \boxed{
 B_a(q)=-\sum_{m=1}^{M}\mu(m)V_a(q,m),
 \qquad
 V_a(q,m)=\sum_{n=\max(q,m)}^{M}
 \frac{\alpha_{q,n}}{L_n}\mathscr K_{q,n}(m).}
 \tag{2.5}
\]

Both signs in (2.2)--(2.5) are essential: the affine term is **plus** inside
\(\mathscr K\), and the outer Möbius sum has a leading **minus**.

Put

\[
 A_N^{\Lambda}=\sum_{r\le N}\frac{\Lambda(r)}r,
 \qquad A_0^{\Lambda}=0.
\]

For \(1\le t<n+1\),

\[
 \sum_{r\le\lfloor n/m\rfloor}\Lambda(r)
 \left\lfloor\frac{t}{mr}\right\rfloor
 =\log\!\left(\left\lfloor\frac tm\right\rfloor!\right).
 \tag{2.6}
\]

Indeed, with \(K=\lfloor t/m\rfloor\), the active range is exactly
\(r\le K\), up to the null terminal singleton when \(m\mid n+1\), and

\[
 \sum_{r\le K}\Lambda(r)\left\lfloor\frac Kr\right\rfloor
 =\sum_{j\le K}\sum_{r\mid j}\Lambda(r)=\log(K!).
 \tag{2.7}
\]

Substituting \(\rho_{mr}(t)=t/(mr)-\lfloor t/(mr)\rfloor\) into (2.2)
gives the exact factorial representation

\[
 \boxed{
 \mathscr K_{q,n}(m)
 =\frac{\mathfrak a_{q,n}}m
   \left(A_{\lfloor n/m\rfloor}^{\Lambda}+\eta_nL_n\right)
 -\int_1^{n+1}\rho_q(t)
   \log\!\left(\left\lfloor\frac tm\right\rfloor!\right)
   \frac{dt}{t^2}.}
 \tag{2.8}
\]

Two finite convolution closures are

\[
 \boxed{
 \sum_{m\le k}\mu(m)
 \log\!\left(\left\lfloor\frac km\right\rfloor!\right)=\psi(k),}
 \tag{2.9}
\]

and, with \(\ell_n=\sum_{d\le n}\mu(d)\log d/d\),

\[
 \boxed{
 \sum_{m\le n}\frac{\mu(m)}m
 A_{\lfloor n/m\rfloor}^{\Lambda}=-\ell_n.}
 \tag{2.10}
\]

At the last source index,

\[
 \boxed{
 \mathscr K_{q,n}(n)=\frac{\eta_nL_n\mathfrak a_{q,n}}n>0.}
 \tag{2.11}
\]

It cannot be dropped from an Abel transform.

## 3. Positivity does not give complete monotonicity

Every term in (2.2) is nonnegative, and in the present range the affine term
is positive.  A tempting route was to seek complete monotonicity in the source
index \(m\), then combine it with an Abel transform of the Mertens function.
That route is false in an actual physical cell.

Let

\[
 Df(m)=f(m)-f(m+1).
\]

At

\[
 \theta=\frac25,\qquad a=4,\qquad q=5,\qquad n=6,
\]

one has a physical squarefree row and cell:
\(4\le5\le6\le7\) and \(5\le3a/2\).  Exact integration gives

\[
 P_{5,6}(4)=\frac5{14}+\frac{\log4}{5}
 +\frac{\log5}{4}-\frac9{20}\log7,
 \tag{3.1}
\]

\[
 P_{5,6}(6)=\frac{47}{210}+\frac{\log5}{6}
 +\frac{\log6}{5}-\frac{11}{30}\log7.
 \tag{3.2}
\]

Writing \(\mathscr K(m)=H(m)+c/m\), the only relevant prime-power multiples
are

\[
 H(2)=(\log2)P_{5,6}(4)+(\log3)P_{5,6}(6),
 \qquad H(3)=(\log2)P_{5,6}(6),
\]

and \(H(m)=0\) for \(m\ge4\).  Hence

\[
 D^3\mathscr K(2)
 =(\log2)P_{5,6}(4)
 +(\log3-3\log2)P_{5,6}(6)+\frac c{20},
 \tag{3.3}
\]

where

\[
 c=\eta_6\log6\left(\frac65-\log\frac75\right),
 \qquad
 \eta_6=\frac{1/5}{1/5+\log6/\log7}
 =\frac{\log7}{\log54432}.
\]

The exact-rational certificate
`cycle50_kernel_shape_counterexample.py` encloses every logarithm by a
200-term atanh series with a rigorous geometric remainder and proves

\[
 -\frac1{100}<D^3\mathscr K(2)<-\frac1{125}<0.
 \tag{3.4}
\]

Its much narrower stored interval is

```text
[-0.008804097414090616079618426963744036,
 -0.008804097414090616079618426963744035].
```

Thus complete monotonicity is false even in the physical finite range.
Ordinary first-difference monotonicity is not proved or disproved by this
example, and even such monotonicity would provide only a signed Mertens Abel
identity, not an anti-cancellation lower bound.

## 4. The collapsed current-label prefix kernel

Let \(L=\log a\), and for current labels put

\[
 u=\frac qa,\qquad v=\frac da,\qquad s=\frac na,
 \qquad R=\max(u,v),\qquad \lambda=\frac{C-1}{C}.
\]

For \(s\ge R\), define

\[
 A(u,s)=\frac su-\log\frac su,
 \tag{4.1}
\]

\[
 J_{\le s}(u,v)=\int_0^s
 \left\{\frac yu\right\}\left\{\frac yv\right\}\frac{dy}{y^2}.
 \tag{4.2}
\]

### Theorem 4.1 (locally uniform entrywise limit)

For every compact \(E\Subset[1,2)^2\), uniformly over integer labels
\((q/a,d/a)\in E\),

\[
 \boxed{
 aL\,W_B(q,d)=K_B(u,v)+O_{C,E}(L^{-1}+a^{-1}),}
 \tag{4.3}
\]

where

\[
 \boxed{
 K_B(u,v)=\int_R^2
 \left[J_{\le s}(u,v)-\lambda\frac{A(u,s)}v\right]\frac{ds}{s}.}
 \tag{4.4}
\]

There is no factor \(1/C\) in front of \(J_{\le s}\).  The exact lower
support is \(R=\max(u,v)\).

#### Quantitative proof

The exact dilation of (0.2) is

\[
 aP_{q,n}(d)=\int_{1/a}^{s+1/a}
 \left\{\frac yu\right\}\left\{\frac yv\right\}\frac{dy}{y^2}
 =J_{\le s+1/a}(u,v)-\frac1{auv},
\]

because both fractional parts are linear on \([0,1/a]\).  Thus, uniformly on the stated compact sets,

\[
 aP_{q,n}(d)=J_{\le s}(u,v)+O_E(a^{-1}).
 \tag{4.5}
\]

Likewise,

\[
 a\frac{\mathfrak a_{q,n}}d
 =\frac1v\left[\frac su-\log\frac{s+1/a}{u}\right]
 =\frac{A(u,s)}v+O_E(a^{-1}).
 \tag{4.6}
\]

From (0.1), directly and uniformly,

\[
 aL\alpha_{q,n}=\frac1s+O_{C,E}(L^{-1}+a^{-1}),
 \quad
 \frac{\log d}{L_n}=1+O_E(L^{-1}),
 \quad
 \eta_n=\lambda+O_C((aL)^{-1}).
 \tag{4.7}
\]

Consequently,

\[
 aL W_B(q,d)
 =\frac1a\sum_{n=\max(q,d)}^{M}
 \frac{J_{\le s}(u,v)-\lambda A(u,s)/v}{s}
 +O_{C,E}(L^{-1}+a^{-1}).
 \tag{4.8}
\]

Here one may equivalently view the summation cells
\([n/a,(n+1)/a]\) as partitioning the support interval through the terminal
endpoint \(2\); replacing left endpoints by the exact cell integrals costs only
the displayed Riemann error.

On \(1\le u,v\le s\le2\), there is at most one wrap of either fractional
part, apart from a null endpoint.  The exact formula below makes the summand
uniformly piecewise Lipschitz across the moving diagonal.  A direct Riemann
estimate therefore proves (4.3).  Mere chamberwise convergence followed by an
appeal to continuity would not justify the asserted uniform rate.

### Closed form

For \(R\le s\le2\),

\[
 \boxed{
 J_{\le s}(u,v)=
 \frac{s}{uv}+\frac1R-\frac1s
 -\frac{\log(s/u)}v-\frac{\log(s/v)}u.}
 \tag{4.9}
\]

Put

\[
 X=\log\frac2u,\qquad Y=\log\frac2v.
\]

Integrating (4.9) in (4.4) gives, on \(u\le v\),

\[
 \boxed{
 \begin{aligned}
 K_B(u,v)={}&\frac12+\frac{Y-1}{v}-\frac{Y^2}{2u}\\
 &+\frac1C\left[
 \frac2{uv}-\frac1u-\frac{XY}{v}+\frac{Y^2}{2v}
 \right],
 \end{aligned}}
 \tag{4.10}
\]

and, on \(v\le u\),

\[
 \boxed{
 \begin{aligned}
 K_B(u,v)={}&\frac12+\frac{X-1}{u}+\frac{X^2}{2u}
 -\frac{XY}{u}\\
 &+\frac1C\left[
 \frac2{uv}-\frac1v-\frac{X^2}{2v}
 \right].
 \end{aligned}}
 \tag{4.11}
\]

The two formulas agree on \(u=v\).  The kernel is generally nonsymmetric.
It extends continuously to \([1,2]^2\) and vanishes whenever one label equals
\(2\).

## 5. Positivity on one common square domain

Let

\[
 S_B(u,v)=\frac{K_B(u,v)+K_B(v,u)}2.
\]

For a fixed \(s\), activate only labels \(u,v\le s\), and set

\[
 x=\log(s/u),\qquad y=\log(s/v),
\]

\[
 p(x)=x,
 \qquad r(x)=e^x,
 \qquad k(x,y)=e^{\min(x,y)}-1.
\]

The identity (4.9) gives

\[
 sJ_{\le s}(u,v)
 =k(x,y)+r(x)r(y)-p(x)r(y)-r(x)p(y).
 \tag{5.1}
\]

Also

\[
 s\frac{A(u,s)}v=(r(x)-p(x))r(y).
\]

Symmetrizing the collapse correction therefore gives

\[
 \boxed{
 B_{C,s}(x,y)=k(x,y)+\frac1C r(x)r(y)
 -\frac{C+1}{2C}\bigl(p(x)r(y)+r(x)p(y)\bigr),}
 \tag{5.2}
\]

and

\[
 \boxed{
 S_B(u,v)=\int_1^2
 \mathbf1_{u\le s}\mathbf1_{v\le s}
 B_{C,s}(\log(s/u),\log(s/v))\frac{ds}{s^2}.}
 \tag{5.3}
\]

The measure in (5.3) is \(ds/s^2\), not \(ds/s\).  Equivalently,
\(B_{C,s}/s\) is integrated against \(ds/s\).

The symmetrized collapse correction itself is

\[
 -\lambda\,r\otimes r
 +\frac{\lambda}{2}(p\otimes r+r\otimes p).
 \tag{5.4}
\]

Its cross contribution is positive.

### Lemma 5.1 (Brownian support inequality)

On the range \(0\le x\le\log2\),

\[
 \boxed{k\succeq2p\otimes p.}
 \tag{5.5}
\]

#### Proof

For a finite signed measure \(f\), put

\[
 H_f(t)=\int_{x\ge t}df(x).
\]

Then

\[
 \iint k(x,y)\,df(x)df(y)
 =\int_0^{\log2}e^tH_f(t)^2dt,
\]

whereas

\[
 \int p(x)df(x)=\int_0^{\log2}H_f(t)dt.
\]

Weighted Cauchy--Schwarz and
\(\int_0^{\log2}e^{-t}dt=1/2\) prove (5.5).  For a fixed
\(s<2\), the same proof gives a strictly stronger constant.  \(\square\)

Replacing \(k\) by the lower bound in (5.2) leaves the two-dimensional
matrix in the \((p,r)\) coordinates

\[
 \boxed{
 \begin{pmatrix}
 2&-(C+1)/(2C)\\
 -(C+1)/(2C)&1/C
 \end{pmatrix}.}
 \tag{5.6}
\]

Its determinant is

\[
 \frac{8C-(C+1)^2}{4C^2}.
 \tag{5.7}
\]

### Theorem 5.2 (square-domain PSD theorem)

The symmetric kernel \(S_B\) is positive semidefinite on every common square
label domain in \([1,2]\), with one common finite positive measure and the
same real test function in both slots, whenever

\[
 \boxed{3-2\sqrt2\le C\le3+2\sqrt2.}
 \tag{5.8}
\]

The residual matrix (5.6) is positive definite in the interior of this
interval.  In particular, all physical parameters \(1<C<2\) lie strictly in
the positive range.

For physical \(C\), the following refinements hold.

1. Every Gram matrix on finitely many distinct labels in \([1,2)\) is positive
   definite.  The endpoint \(u=2\) must be excluded because its kernel row is
   zero.
2. For every finite positive measure \(\nu\) with no atom at \(2\), the
   integral operator on \(L^2(\nu)\) is injective.  It is enough, and often
   cleaner, to work on \([1,b]\) with \(b<2\).
3. The operator is compact: the continuous bounded kernel is
   Hilbert--Schmidt for finite \(\nu\).
4. If \(L^2(\nu)\) is infinite-dimensional, compactness and injectivity imply
   noncoercivity.  This conclusion is false without the infinite-dimensional
   hypothesis; a finite atomic space may have a positive smallest eigenvalue.

For injectivity, vanishing of the quadratic form forces, for almost every
\(s\), both active moments in the positive definite residual to vanish.  In
particular,

\[
 s\int_{[1,s]}\frac{f(u)}u\,d\nu(u)=0.
\]

Right-continuity of this cumulative signed measure then gives \(f=0\)
\(\nu\)-almost everywhere, except for the invisible endpoint atom that was
excluded.

This theorem supplies no PSD order for the nonsymmetric \(K_B\), for a
rectangular map with output labels \([1,3/2]\) and input labels \([1,2)\), or
for a cross product with a different kernel.

## 6. Exact compatible full and tail gauges

Let

\[
 G(q,d)=\langle\rho_q,\rho_d\rangle_H,
 \qquad g_q=\langle\rho_q,\chi\rangle_H
 =\frac{\log q+1-\gamma}{q}.
 \tag{6.1}
\]

Here \(G(q,d)\) is the standard full \((0,\infty)\) Vasyunin entry minus
exactly

\[
 \frac1{qd},
\]

the contribution of \((0,1)\).  Put

\[
 T_{q,n}(d)=G(q,d)-P_{q,n}(d).
\]

Let \(C_a=B_a+H_a=\widehat{\mathbf c}_a\) denote the complete physical
contraction.  A full-space gauge directly compatible with the collapsed
prefix columns (1.7) is

\[
 \boxed{
 W_C^\delta(q,d)=
 \sum_{n=\max(q,d)}^{M}\alpha_{q,n}
 \left[
 \left(\frac{\log d}{L_n}-\eta_n\right)G(q,d)
 -\eta_n\mathbf1_{d=1}g_q
 \right].}
 \tag{6.2}
\]

Since \(\mu(1)=1\), finite expansion gives exactly

\[
 \boxed{C_a=W_C^\delta\mu.}
 \tag{6.3}
\]

Define

\[
 W_H^\delta=W_C^\delta-W_B.
\]

Then

\[
 \boxed{
 \begin{aligned}
 W_H^\delta(q,d)=
 \sum_{n=\max(q,d)}^{M}\alpha_{q,n}\bigg[&
 \frac{\log d}{L_n}T_{q,n}(d)-\eta_nG(q,d)\\
 &-\eta_n\mathbf1_{d=1}g_q
 +\frac{\eta_n\mathfrak a_{q,n}}d
 \bigg],
 \end{aligned}}
 \tag{6.4}
\]

and \(H_a=W_H^\delta\mu\).  The formulas retain \(d=1\), \(n=M\), the
affine source, and the restricted \(-1/(qd)\) correction.  There is no outer
\(\mu(q)\).

### Current-label full and tail limits

Define

\[
 J_\infty(u,v)=\int_0^\infty
 \left\{\frac yu\right\}\left\{\frac yv\right\}\frac{dy}{y^2}.
 \tag{6.5}
\]

For moving current labels \(d\asymp a\), the exceptional \(d=1\) packet is
absent.  The same direct dilation and Riemann argument as in Section 4 gives,
locally uniformly on compact current-label sets,

\[
 \boxed{
 aL W_C^\delta(q,d)\longrightarrow
 K_C^\delta(u,v)=
 \frac1C\log\frac2{\max(u,v)}\,J_\infty(u,v).}
 \tag{6.6}
\]

Therefore

\[
 \boxed{K_H^\delta=K_C^\delta-K_B.}
 \tag{6.7}
\]

These are entrywise statements, not limits after summing against the growing
vector \((\mu(d))\).

There is, however, a rigorous current-current limit for each fixed moving
normal-matrix entry.  If \(d/a\to v\in[1,2)\) and \(e/a\to w\in[1,2)\),
with \(v,w\) in fixed compact subsets, then squarefree-row equidistribution
and the locally uniform entrywise limits give

\[
 \boxed{
 aL^2\bigl[(W_B)^TW_C^\delta\bigr]_{d,e}
 \longrightarrow N_{BC}(v,w),}
 \tag{6.8}
\]

where

\[
 \boxed{
 N_{BC}(v,w)=\frac6{\pi^2}\int_1^{3/2}
 K_B(u,v)K_C^\delta(u,w)\,du.}
 \tag{6.9}
\]

The real quadratic form uses

\[
 \boxed{
 S_{BC}(v,w)=\frac3{\pi^2}\int_1^{3/2}
 \bigl[K_B(u,v)K_C^\delta(u,w)
      +K_C^\delta(u,v)K_B(u,w)\bigr]du.}
 \tag{6.10}
\]

Equations (6.8)--(6.10) cover only the current-current block.  They do not
control old columns \(d<a\), old/current cross terms, operator convergence, or
the growing selected Möbius sum.

### The finite mixed/Krein form

Let \(b_q\) and \(c_q\) denote row vectors of \(W_B\) and
\(W_C^\delta\).  Exactly,

\[
 \langle B_a,C_a\rangle
 =\mu^T(W_B)^TW_C^\delta\mu
 =\mu^T\operatorname{sym}(N_a)\mu,
 \qquad N_a=(W_B)^TW_C^\delta.
 \tag{6.11}
\]

Moreover,

\[
 \boxed{
 \begin{aligned}
 \operatorname{sym}(N_a)
 &=\sum_{q\in\mathcal Q_a}\frac{b_q\otimes c_q+c_q\otimes b_q}{2}\\
 &=\frac14\sum_{q\in\mathcal Q_a}
 \bigl[(b_q+c_q)\otimes(b_q+c_q)
      -(b_q-c_q)\otimes(b_q-c_q)\bigr].
 \end{aligned}}
 \tag{6.12}
\]

This is a Krein, or difference-of-Grams, factorization.  A one-row fiber is
PSD only when one row vector vanishes or when \(c_q=\kappa b_q\) for some
\(\kappa\ge0\).  Prefix square-kernel positivity contains no information about
that relative alignment.

## 7. Finite certified obstructions

### 7.1 Compatible delta gauge

At \(\theta=2/5\), \(a=3\), the physical row set is
\(\mathcal Q_a=\{3\}\).  On the two current columns \(d=3,5\), an independent
256-bit Arb reconstruction of (1.7) and (6.2) gives

\[
 \begin{aligned}
 b_3&=0.047857964455618318685953060282229\ldots,\\
 c_3&=0.065840226215251131181923198819356\ldots,\\
 b_5&=0.007372156589521812266269549747475\ldots,\\
 c_5&=0.009464412186358339258486337044503\ldots.
 \end{aligned}
 \tag{7.1}
\]

The wedge is strictly nonzero:

\[
 b_3c_5-b_5c_3
 =-3.24369555403121376537410867416\ldots\times10^{-5}.
 \tag{7.2}
\]

For one row, the corresponding \(2\times2\) principal determinant is
identically

\[
 \boxed{
 -\frac14(b_3c_5-b_5c_3)^2
 =-2.63039021181046570498404130134\ldots\times10^{-10}<0.}
 \tag{7.3}
\]

The minor lies wholly in the current block \(v=1,5/3\), and uses neither old
labels nor the affine \(d=1\) packet.  Thus the exact finite mixed retention
kernel is indefinite.

This does not make the selected physical contraction negative.  At this scale
both selected scalars are negative and

\[
 \langle B_a,C_a\rangle=0.01748412654\ldots>0.
\]

The obstruction refutes a universal kernel-sign theorem, not eventual
physical retention.

### 7.2 Independent compatible floor gauge

There is another finite-exact redistribution, using

\[
 \sum_{d\le n}\mu(d)\left\lfloor\frac nd\right\rfloor=1
\]

simultaneously in the prefix, tail, and full contractions.  In that gauge,

\[
 W_B^F(q,d)=\sum_n\alpha_{q,n}
 \left[b_d(n)P_{q,n}(d)
 -\eta_n\left\lfloor\frac nd\right\rfloor P_{q,n}(0)\right],
 \tag{7.4}
\]

\[
 W_C^F(q,d)=\sum_n\alpha_{q,n}
 \left[b_d(n)G(q,d)
 -\eta_n\left\lfloor\frac nd\right\rfloor g_q\right],
 \tag{7.5}
\]

where each sum begins at \(n=\max(q,d)\) and ends at \(M\).  The standalone
192-bit Arb artifact `cycle50_floor_gauge_obstruction.py` reconstructs the
prefix, tail, and full vectors both from (7.4)--(7.5) and directly from every
original temporal \(Z_n\).  It checks all declared identities at \(a=3,8\),
with maximum residual upper balls below \(1.5\times10^{-56}\).

At \(a=3,q=3,d=3,5\), it independently certifies

\[
 \det\operatorname{sym}\bigl((W_B^F)^TW_C^F\bigr)_{\{3,5\}}
 =[-4.76098916825480300610247341488696904258\ldots
 \times10^{-12}\ \pm 4.88\times10^{-60}]<0.
 \tag{7.6}
\]

The column values differ from (7.1), as they must: coefficient kernels depend
on the redistribution gauge, while the selected physical vectors agree.

Individual floor-gauge current columns do **not** have a finite \(aL\) limit.
Indeed,

\[
 aP_{q,n}(0)=\frac Lu+\frac{\log s-1}{u}+\frac1s+o(1),
 \tag{7.7}
\]

so the redistributed affine packet is one logarithmic order larger.  Only its
selected Möbius sum cancels.  The delta gauge (6.2) is the appropriate gauge
for an entrywise current-label full limit.

## 8. Correction and no-go ledger

The following statements are false or unsupported and must not be used.

1. **False cumulative proof:** \(\sum_{d\mid k}\mu(d)=1\) for \(k>1\).
   The correct identity is the cumulative floor sum in (1.1).
2. **False global collapse:** \(U_n(t)=m_nt\) for all \(t\).  It holds only
   almost everywhere on \([1,n+1)\).  In particular, it gives no formula such
   as
   \(\sum_{d\le n}\mu(d)G(q,d)=-g_q-m_n/q\).
3. **False full columns:** any full-space coefficient, limit, or numerical
   experiment obtained by extending (1.2) beyond the prefix and inserting an
   extra \(-\eta_n/(qd)\) collapse column.  Use (6.2).
4. **False floor-gauge scaling:** a finite \(aL\) limit for an individual
   compatible floor-gauge current column.  Equation (7.7) prevents it.
5. **Wrong cross sign:** a negative cross contribution from the collapse
   correction.  The correct term is the positive cross term in (5.4).
6. **Wrong measure:** integrating \(B_{C,s}\) against \(ds/s\).  The correct
   measure is \(ds/s^2\), as in (5.3).
7. **Invalid PSD transfer:** prefix square-kernel PSD implies positivity of
   \(K_B\), of the physical rectangular map, or of
   \((W_B)^TW_C^\delta\).  Equation (7.3) directly refutes the last claim.
8. **Endpoint overstatement:** strictness at label \(2\), where the kernel row
   vanishes.
9. **Coercivity overstatement:** compact injectivity implies noncoercivity on a
   finite atomic \(L^2\) space.  Infinite dimension is required.
10. **Uniformity gap:** chamberwise convergence plus continuity automatically
    gives a quantitative uniform estimate across a moving diagonal.  The
    direct dilation and Riemann estimate in (4.5)--(4.8) is required.
11. **False complete monotonicity:** \(m\mapsto\mathscr K_{q,n}(m)\) is
    completely monotone.  The physical certificate (3.4) refutes it.
12. **Unproved limit interchange:** inserting (4.3) or (6.6) into a growing
    signed sum over \(\mu(d)\), controlling old labels from the current theorem,
    obtaining an operator inverse or eigenvalue floor, or inferring any RH
    consequence.

## 9. Surviving arithmetic frontier

The one-source identity (2.5) rewrites the prefix checkpoint exactly as

\[
 \boxed{
 \sum_{q\in\mathcal Q_a}
 \left|\sum_{m=1}^{M}\mu(m)V_a(q,m)\right|^2
 \gg(\log a)^{-3}.}
 \tag{9.1}
\]

This is a moving weighted-Möbius noncompression theorem.  The square-kernel
PSD result does not choose the Möbius phase, and the complete-monotonicity
route is false.

For any nonzero row test \(y=(y_q)\), Cauchy--Schwarz gives the exact dual
lower bound

\[
 \|B_a\|_2^2\ge
 \frac{\left|\sum_m\mu(m)\Phi_{a,y}(m)\right|^2}{\|y\|_2^2},
 \qquad
 \Phi_{a,y}(m)=\sum_qy_qV_a(q,m).
 \tag{9.2}
\]

Without an independently constructed arithmetic phase for \(y\), (9.2) is
only a tautological dual reformulation.  It identifies the honest next task:
construct a short, explicit family of row tests whose transformed source
weights admit a quantitative Möbius discrepancy lower bound, while preserving
all affine and endpoint terms.

Even (9.1) is only the norm half of the canonical projection target.  The
retention half remains

\[
 \left|\langle B_a,C_a\rangle\right|
 \ge\varepsilon\|B_a\|_2^2,
 \tag{9.3}
\]

or an equivalent two-channel estimate when the prefix line nearly cancels.
By (6.11)--(6.12), this is a selected mixed/Krein arithmetic estimate, not a
consequence of prefix PSD.  A proof of (9.1) and (9.3) would still leave the
separate completed-square budget upper bound.  No Riemann-hypothesis result is
claimed.

## 10. Reproducibility ledger

The three finite artifacts are fail-closed and keep their canonical replay
commands in the first two lines of the corresponding stored output.  From the
repository root, the commands are:

```bash
rm -f /tmp/cycle50-kernel-shape-counterexample.out
env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C \
  uv run --isolated --no-project --python 3.12.13 python -I -B \
  millennium-prize/riemann-hypothesis/cycle50_kernel_shape_counterexample.py \
  > /tmp/cycle50-kernel-shape-counterexample.out
cmp /tmp/cycle50-kernel-shape-counterexample.out \
  millennium-prize/riemann-hypothesis/cycle50-kernel-shape-counterexample.out

rm -f /tmp/cycle50-delta-gauge-obstruction.out
env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C \
  uv run --isolated --no-project --python 3.12.13 \
  --with python-flint==0.9.0 python -I -B \
  millennium-prize/riemann-hypothesis/cycle50_delta_gauge_obstruction.py \
  > /tmp/cycle50-delta-gauge-obstruction.out
cmp /tmp/cycle50-delta-gauge-obstruction.out \
  millennium-prize/riemann-hypothesis/cycle50-delta-gauge-obstruction.out

rm -f /tmp/cycle50-floor-gauge-obstruction.out
env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C \
  uv run --isolated --no-project --python 3.12.13 \
  --with python-flint==0.9.0 python -I -B \
  millennium-prize/riemann-hypothesis/cycle50_floor_gauge_obstruction.py \
  > /tmp/cycle50-floor-gauge-obstruction.out
cmp /tmp/cycle50-floor-gauge-obstruction.out \
  millennium-prize/riemann-hypothesis/cycle50-floor-gauge-obstruction.out
```

The committed source/output SHA-256 pairs are, respectively,

```text
d7239ce4dde9348b591f22cbb72ba79e6d3c70244a9ca7838675deddfca957c1
b6607856cc635d54ed16533567e85e7df4152a13c0a8eaf3a97e8fe6e852c4ae

3f584e0c16821d960ed6ca767bf3c6cb1fffcf86ac2388931bf8681b18498be5
c7ba80e9409e4f4a9079971979da07a3d2160cc6fec97dac5cb4cf484a52a1c9

7a5ffa3d37c5335fe7e48563abc862a150586ace511a3df837d7ce709daa46ba
c6b402a35b5fe5505eed54625ac872ce1897b937bf3b7b3635927fab8d695ef0
```

All three replays were rerun from a clean import state and matched the stored
outputs byte for byte.  The two Arb artifacts pin python-flint `0.9.0` and
FLINT `3.6.0`; the complete-monotonicity artifact uses only exact standard-
library rational arithmetic.
