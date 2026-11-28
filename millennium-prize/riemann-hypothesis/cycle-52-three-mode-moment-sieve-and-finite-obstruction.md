# Cycle 52: exact three-mode moment sieve and finite smooth-span obstruction

## Status and scope

This note follows the Cycle 51 suggestion to test the sampled row functions

\[
 1,\qquad q/a,\qquad \log(q/a)
\]

against the actual Cycle 49 canonical complete-prefix vector \(B_a\) on

\[
 \mathcal Q_a=\{q\in\mathbb Z:\mu(q)^2=1,
                 \ a\le q\le\lfloor3a/2\rfloor\}.
\]

It proves five structural facts.

1. The complete prefix has an exact cancellation-preserving suffix normal
   form.  This form retains every Chebyshev term, reciprocal-Mobius term,
   moving lower endpoint, sign, and terminal cell.
2. Orthogonal projection onto the three sampled functions gives an exact
   rank-safe moment decomposition.  In particular, a lower bound of size
   \(a(\log a)^{-3}\) for the squared three-moment vector would prove the
   desired prefix norm scale.
3. The existing finite algebra does not close on the three functions.  A
   standalone 256-bit Arb certificate at \(a=11\) rigorously refutes a
   universal exact three-function identity on every finite physical row set.
4. Standalone 256-bit Arb certificates at \(a=8192,16384\) show that this
   span captures only \(76.9089\ldots\%\) and \(42.5849\ldots\%\) of the
   prefix energy.  These are finite counterexamples to universal high finite
   capture.  They are not an asymptotic no-go.
5. Exact first, second, and third row differences, and an exact four-point
   annihilator of the three sampled modes, all retain dense moving arithmetic
   interior and boundary packets.  They do not create a sparse sign-controlled
   source.

The moment criterion concerns \(\|B_a\|_2\).  It does not control the signed
prefix/full correlation and therefore does not prove the canonical retention
quantity \(\mathcal Q_a^{\rm cp}\).

An additional exact finite-difference audit closes first, second, and third
row-difference formulas and an exact four-point annihilator of the three
sampled modes.  Both leave the full moving arithmetic interior and boundary
packets.  Thus neither supplies a sparse sign-controlled source.  The formulas
are recorded in Section 7.

Nothing here proves

\[
 \|B_a\|_2^2\gg(\log a)^{-3},\qquad
 \mathcal Q_a^{\rm cp}\gg(\log a)^{-3},\qquad
 D_a(I_0)\gg(\log a)^{-3},
\]

or the Riemann hypothesis.

## 1. Exact cancellation-preserving normal form

Put

\[
 M=2a-1,\qquad L_n=\log n,\qquad \tau=C-1,
\]

and retain the Cycle 49 definitions

\[
 w_n=1-\frac{L_n}{L_{n+1}},\qquad A_n=C-w_n,
 \qquad \eta_n=\frac{\tau}{A_n},
\]

\[
 \alpha_{q,n}=w_nA_n\left(\frac{\log q}{L_n}-\eta_n\right),
\]

\[
 m_n=\sum_{d\le n}\frac{\mu(d)}d,
 \qquad
 \ell_n=\sum_{d\le n}\frac{\mu(d)\log d}{d}.
\]

To distinguish the Chebyshev convolution from the parameter \(C\), define

\[
 \mathscr C_r=\sum_{d<r}\Lambda(d)\log\frac rd,
 \qquad
 \Pi_N=\sum_{k=1}^N\frac{\psi(k)}{k(k+1)},
 \qquad \Pi_0=0,
\]

and put

\[
 T_n=\ell_n-\eta_nL_nm_n.
\]

The exact Cycle 49 complete-prefix residual is

\[
 B_a(q)=\sum_{n=q}^{M}\frac{\alpha_{q,n}}{L_n}\mathcal R_{q,n},
 \tag{1.1}
\]

where

\[
 \mathcal R_{q,n}=\frac{E_{n+1}}q+\mathfrak j_{q,n}
 +\mathfrak a_{q,n}(1+T_n),
\]

\[
 \mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q}.
\]

The exact identities

\[
 E_{n+1}=\mathscr C_{n+1}-n,
 \qquad
 \mathfrak j_{q,n}=\log\frac{n+1}{q}-(\Pi_n-\Pi_{q-1})
\]

make the deterministic \(1\)-packet cancel:

\[
 -\frac nq+\log\frac{n+1}{q}+\mathfrak a_{q,n}=0.
\]

Therefore

\[
 \boxed{
 \mathcal R_{q,n}
 =\frac{\mathscr C_{n+1}}q-(\Pi_n-\Pi_{q-1})
  +\mathfrak a_{q,n}T_n.}
 \tag{1.2}
\]

Let \(x_q=\log q\) and define

\[
 p_n=\frac{w_nA_n}{L_n^2},\qquad
 r_n=-\frac{w_n\tau}{L_n},
 \tag{1.3}
\]

\[
 A_n^\star=\mathscr C_{n+1}+nT_n,
 \qquad
 D_n^\star=-\Pi_n-L_{n+1}T_n.
 \tag{1.4}
\]

Then, exactly,

\[
 \frac{\alpha_{q,n}}{L_n}=p_nx_q+r_n
 \tag{1.5}
\]

and

\[
 \mathcal R_{q,n}
 =x_qT_n+\frac{A_n^\star}{q}+\Pi_{q-1}+D_n^\star.
 \tag{1.6}
\]

Indeed, the right side of (1.6) expands to

\[
 \frac{\mathscr C_{n+1}}q-(\Pi_n-\Pi_{q-1})
 +T_n\left(\frac nq-L_{n+1}+x_q\right),
\]

and the parenthesis is \(\mathfrak a_{q,n}\).  Thus

\[
 \boxed{
 B_a(q)=\sum_{n=q}^{M}(p_nx_q+r_n)
 \left(x_qT_n+\frac{A_n^\star}{q}
       +\Pi_{q-1}+D_n^\star\right).}
 \tag{1.7}
\]

For \(S_X(q)=\sum_{n=q}^{M}X_n\), expansion gives the exact linear-time
suffix form

\[
 \boxed{\begin{aligned}
 B_a(q)={}&x_q^2S_{pT}(q)\\
 &+x_q\{S_{rT+pD^\star}(q)+\Pi_{q-1}S_p(q)\}\\
 &+\{S_{rD^\star}(q)+\Pi_{q-1}S_r(q)\}\\
 &+\frac1q\{x_qS_{pA^\star}(q)+S_{rA^\star}(q)\}.
 \end{aligned}}
 \tag{1.8}
\]

### Endpoint and sign ledger

- The temporal range is exactly \(q\le n\le M=2a-1\), with both endpoints.
- The terminal cell uses \(\mathscr C_{2a}\) and \(L_{2a}\), but there is no
  temporal \(n=2a\) summand.
- There are no endpoint half-weights.
- There is no outer \(\mu(q)\).  Squarefreeness selects rows only.
- Every Mobius sign remains inside \(m_n,\ell_n,T_n\).
- The signs in \(r_n=-w_n\tau/L_n\) and
  \(D_n^\star=-\Pi_n-L_{n+1}T_n\) are negative.

The finite certificate in Section 5 evaluates (1.7) and, at five rows per
large scale, independently replays the unsummed defining formula (1.1).

## 2. Exact three-mode projection and moment sieve

Use the ordered functions

\[
 f_0(u)=1,\qquad f_1(u)=u,\qquad f_2(u)=\log u,
 \qquad u=q/a.
\]

Let \(F_a(q,j)=f_j(q/a)\) on \(\mathcal Q_a\), and define

\[
 G_a=F_a^TF_a,
 \qquad
 \mathbf m_a=F_a^TB_a.
 \tag{2.1}
\]

Thus

\[
 \mathbf m_a=
 \begin{pmatrix}
 \sum_{q\in\mathcal Q_a}B_a(q)\\
 \sum_{q\in\mathcal Q_a}(q/a)B_a(q)\\
 \sum_{q\in\mathcal Q_a}\log(q/a)B_a(q)
 \end{pmatrix}.
 \tag{2.2}
\]

Substituting (1.7) and interchanging finite sums gives the exact arithmetic
formula

\[
 \boxed{
 (\mathbf m_a)_j=
 \sum_{n=a}^{M}\ \sum_{\substack{q\in\mathcal Q_a\\q\le n}}
 f_j(q/a)(p_nx_q+r_n)
 \left(x_qT_n+\frac{A_n^\star}{q}
       +\Pi_{q-1}+D_n^\star\right).}
 \tag{2.3}
\]

This retains the squarefree-row restriction, all endpoints, every Chebyshev
term, and every Mobius sign.

Let \(G_a^+\) be the Moore--Penrose inverse, and put

\[
 \beta_a=G_a^+\mathbf m_a,
 \qquad
 R_a^{(3)}=B_a-F_a\beta_a.
 \tag{2.4}
\]

Because
\(\operatorname{Ran}(F_a^T)=\operatorname{Ran}(F_a^TF_a)\), one has
\(\mathbf m_a\in\operatorname{Ran}G_a\).  Therefore, in every rank,

\[
 \boxed{
 B_a=F_aG_a^+\mathbf m_a+R_a^{(3)},
 \qquad F_a^TR_a^{(3)}=0,}
 \tag{2.5}
\]

and

\[
 \boxed{
 \|B_a\|_2^2
 =\mathbf m_a^TG_a^+\mathbf m_a+\|R_a^{(3)}\|_2^2.}
 \tag{2.6}
\]

The remainder is explicit:

\[
 \boxed{\begin{aligned}
 R_a^{(3)}(q)={}&
 \sum_{n=q}^{M}(p_nx_q+r_n)
 \left(x_qT_n+\frac{A_n^\star}{q}
       +\Pi_{q-1}+D_n^\star\right)\\
 &-\sum_{i,j=0}^2f_i(q/a)(G_a^+)_{ij}(\mathbf m_a)_j.
 \end{aligned}}
 \tag{2.7}
\]

This is a tautological orthogonal decomposition, not an arithmetic low-rank
theorem.  Its useful exact content is that all three ordered moments of the
remainder vanish.

## 3. A rank-safe finite norm implication

For \(a\ge2\),

\[
 \#\mathcal Q_a\le\lfloor a/2\rfloor+1\le a.
\]

On \(1\le u\le3/2\), one has \(0\le\log u<1/2\), so every sampled row
contributes less than

\[
 1+u^2+(\log u)^2<1+\frac94+\frac14=\frac72
\]

to \(\operatorname{tr}G_a\).  Hence every positive eigenvalue of \(G_a\)
is less than \(4a\).  Since \(\mathbf m_a\in\operatorname{Ran}G_a\), the
spectral decomposition on that range gives

\[
 \boxed{
 \|B_a\|_2^2\ge \mathbf m_a^TG_a^+\mathbf m_a
 \ge\frac{\|\mathbf m_a\|_2^2}{4a}.}
 \tag{3.1}
\]

If \(G_a=0\), then \(\mathbf m_a=0\), so the second inequality is simply
\(0\ge0\).  Thus (3.1) has no rank-zero division.

Consequently the exact every-scale moment estimate

\[
 \boxed{
 \|\mathbf m_a\|_2^2\gg a(\log a)^{-3}}
 \tag{3.2}
\]

would prove

\[
 \|B_a\|_2^2\gg(\log a)^{-3}.
\]

It would also suffice to prove one ordered moment bound

\[
 |(\mathbf m_a)_j|\gg\sqrt a\,(\log a)^{-3/2}.
\]

Independently, (2.6) shows that

\[
 \|R_a^{(3)}\|_2^2\gg(\log a)^{-3}
 \tag{3.3}
\]

would suffice.  Neither (3.2) nor (3.3) follows from the exact identities,
quantitative-PNT upper bounds, or the finite screens.

### Continuum nondegeneracy supplement

Squarefree equidistribution gives

\[
 \frac1aG_a\longrightarrow\frac6{\pi^2}\Gamma,
 \qquad
 \Gamma_{ij}=\int_1^{3/2}f_i(u)f_j(u)\,du.
\]

Writing \(h=\log(3/2)\), direct integration gives

\[
 \boxed{
 \Gamma=
 \begin{pmatrix}
 \frac12&\frac58&\frac32h-\frac12\\[2mm]
 \frac58&\frac{19}{24}&\frac98h-\frac5{16}\\[2mm]
 \frac32h-\frac12&\frac98h-\frac5{16}&
 \frac32h^2-3h+1
 \end{pmatrix}.}
 \tag{3.4}
\]

The first two leading principal minors are \(1/2\) and \(1/192\), and

\[
 \boxed{
 \det\Gamma
 =-\frac{456h^2-360h+71}{1536}.}
 \tag{3.5}
\]

An exact sign proof uses

\[
 h=2\sum_{k\ge0}\frac1{(2k+1)5^{2k+1}}.
\]

This gives

\[
 \frac25<h<\frac{3041}{7500}<H:=\frac{40547}{100000}.
\]

For \(p(t)=456t^2-360t+71\), one has \(p'(t)>0\) for
\(t>15/38\), and exact rational arithmetic gives

\[
 p(H)=-\frac{125087}{1250000000}<0.
\]

Thus

\[
 \boxed{
 \det\Gamma>
 \frac{125087}{1920000000000}>0.}
 \tag{3.6}
\]

The continuum Gram is positive definite.  It identifies the natural moment
scaling and gives eventual nondegeneracy, but supplies no arithmetic lower
bound.  The finite inequality (3.1) is the primary implication.

## 4. Exact algebraic nonclosure

For fixed \(a\),

\[
 \operatorname{span}\{1,q/a,\log(q/a)\}
 =\operatorname{span}\{1,q,\log q\}.
\]

But (1.8) contains

\[
 (\log q)^2,\qquad q^{-1},\qquad (\log q)/q,
 \qquad \Pi_{q-1},\qquad (\log q)\Pi_{q-1},
\]

and suffix coefficients whose lower endpoint moves with \(q\).  Even if the
suffix coefficients were constant, these extra analytic functions do not
belong to the three-mode span.  With \(x=\log q\), for example,

\[
 W(1,e^x,x,x^2)=2e^x\ne0,
 \qquad
 W(1,e^x,x,e^{-x})=2\ne0.
\]

Therefore Cycles 49--51 provide no exact three-function closure.  Such a
closure would require additional simultaneous arithmetic cancellation of all
the terms in (1.8).

This obstruction is also certified at an exact physical finite scale.  Set
\(\theta=2/5\), \(C=6/5\), \(a=11\), and \(M=21\).  The exact physical row
set is

\[
 \mathcal Q_{11}=\{11,13,14,15\}.
\]

Let

\[
 \mathsf A=
 \left(1,\ q/11,\ \log(q/11),\ B_{11}(q)\right)_{
 q\in\mathcal Q_{11}}.
\]

The 256-bit Arb certificate described in Section 5 independently constructs
each \(B_{11}(q)\) from both the direct Cycle 49 residual and (1.7).  It then
evaluates the determinant by the 24-term Leibniz formula and certifies

\[
 \boxed{
 \det\mathsf A=
 [4.86281800877624871977171334657598329077305169556515745633990
 \times10^{-6}\ \mathbin{+/-}\ 1.38\times10^{-67}]>0.}
 \tag{4.1}
\]

This is a rigorous interval sign certificate, not a claim that its displayed
midpoint is an elementary exact value.  It refutes any universal exact identity
asserting

\[
 B_a(q)=c_0(a)+c_1(a)q/a+c_2(a)\log(q/a)
\]

on every finite physical row set.  It does not refute an identity only for all
sufficiently large \(a\), asymptotic rank-three behavior, a vanishing relative
remainder, or eventual high capture.

## 5. Fail-closed Arb finite capture audit

The repository artifacts are

```text
cycle52_smooth_span_certificate.py
cycle52-smooth-span-certificate.out
cycle52_a11_nonclosure_certificate.py
cycle52-a11-nonclosure-certificate.out
```

They pin CPython 3.12.13, python-flint 0.9.0, FLINT 3.6.0, and 256-bit Arb.
The large-scale script performs every logarithm, prefix, suffix, Gram, solve,
and energy computation in outward-rounded Arb arithmetic.  It fails closed if
runtime versions differ, a direct residual cross-check misses zero, a leading
Gram minor is not positive, the determinant contains zero, an energy lacks the
required sign, a ratio leaves \((0,1)\), or the finite breakdown threshold
fails.

At each scale, the basis is exactly

\[
 (1,q/a,\log(q/a))
\]

in the counting inner product on the exact squarefree row list.  The script
certifies the Gram matrix positive definite via Sylvester's criterion, then
uses an Arb matrix solve.  The row-list hashes are

\[
\begin{array}{c|c}
 a&\operatorname{SHA256}(\text{comma-separated rows})\\ \hline
8192&\texttt{8ccd611dadc13ee67c09dda56c2a51685f90060c38b76d362691a508868142f4}\\
16384&\texttt{cd0dbff2378851506446fc8815992ed05e98a71e206ef3b643aa1f6098dd3fd6}.
\end{array}
\]

The certified intervals are

\[
\begin{array}{c|c|c}
 &a=8192&a=16384\\ \hline
\#\mathcal Q_a&2487&4977\\
\det G_a&
[11928.60494151604755284830439947561643036\ {+/-}\ 1.02\!\times\!10^{-36}]&
[94863.14868191557218291300611423174799481\ {+/-}\ 2.76\!\times\!10^{-36}]\\
\|B_a\|^2&
[6.342440172033891285839548615418998765668\!\times\!10^{-7}\ {+/-}\ 2.99\!\times\!10^{-47}]&
[2.044832576630238038151784641870340013978\!\times\!10^{-7}\ {+/-}\ 3.01\!\times\!10^{-47}]\\
\|\operatorname{Proj}B_a\|^2&
[4.877902483019187960797480875490482839884\!\times\!10^{-7}\ {+/-}\ 2.39\!\times\!10^{-47}]&
[8.707918710817575375950330450273785131718\!\times\!10^{-8}\ {+/-}\ 2.40\!\times\!10^{-48}]\\
\|R_a^{(3)}\|^2&
[1.464537689014703325042067739928515925784\!\times\!10^{-7}\ {+/-}\ 6.00\!\times\!10^{-48}]&
[1.174040705548480500556751596842961500806\!\times\!10^{-7}\ {+/-}\ 1.25\!\times\!10^{-47}]\\
\text{capture}&
[0.7690892386384062745203402182068545077941\ {+/-}\ 4.70\!\times\!10^{-41}]&
[0.4258499600572534571268165158873465342271\ {+/-}\ 3.83\!\times\!10^{-41}]\\
\text{omitted}&
[0.2309107613615937254796597817931454922059\ {+/-}\ 4.70\!\times\!10^{-41}]&
[0.5741500399427465428731834841126534657729\ {+/-}\ 3.83\!\times\!10^{-41}].
\end{array}
\]

The second leading Gram minors are exactly enclosed around
\(129279.3965701758861541748046875\) and
\(515861.96570561826229095458984375\), respectively.  Five direct unsummed
Cycle 49 residual checks per scale agree with the suffix evaluation with
summed absolute discrepancy balls of radius at most \(6.55\times10^{-72}\).

These intervals rigorously refute any claim that this exact canonical vector,
row set, and basis capture at least \(96\%\) at every finite scale.  They do
not disprove eventual capture, a positive liminf, an asymptotic rank-three
closure, a quantitative remainder theorem, \(\mathcal Q_a^{\rm cp}\), or RH.
Later non-rigorous binary64 recovery is nonmonotone and makes an asymptotic
negative inference especially unavailable.

Run the certificates in an isolated pinned environment with

```bash
env LC_ALL=C PYTHONDONTWRITEBYTECODE=1 \
  uv run --isolated --no-project --python 3.12.13 \
  --with python-flint==0.9.0 python -I -B \
  cycle52_smooth_span_certificate.py

env LC_ALL=C PYTHONDONTWRITEBYTECODE=1 \
  uv run --isolated --no-project --python 3.12.13 \
  --with python-flint==0.9.0 python -I -B \
  cycle52_a11_nonclosure_certificate.py
```

The committed SHA-256 hashes are

```text
cb245e4cc9c5f14a3a3741a7738346bdb01ee709cde7bec957059c23bf6a9c32  cycle52_a11_nonclosure_certificate.py
61e9462e88e973cebb19a1d75e352cc3442c569c4408e7c0836acfd38fd6eca1  cycle52-a11-nonclosure-certificate.out
a82771f0a157fc24962e767d9a4c785e70c8595e0888e37ac61704339601ddee  cycle52_smooth_span_certificate.py
a2664f3314bdef90b245dc7a1d417a6aead4a536269b8e82861e6d2bd5b51306  cycle52-smooth-span-certificate.out
```

## 6. Exact dual transforms and the one-point blocker

The moment criterion has an equivalent row-dual formulation which exposes the
remaining arithmetic input.  Let \(y=(y_q)\) be any real test supported on
\(\mathcal Q_a\).  With the Cycle 50 one-source column \(\mathscr V_a\), set

\[
 \Gamma_y(m)=\sum_{q\in\mathcal Q_a}y_q\mathscr V_a(q,m).
\]

Expanding the finite column and interchanging sums gives

\[
 \boxed{\begin{aligned}
 \Gamma_y(m)={}&\sum_{n=\max(a,m)}^{M}\frac1{L_n}
 \sum_{\substack{q\in\mathcal Q_a\\q\le n}}
 y_q\alpha_{q,n}\\
 &\quad\times\left[
 \sum_{r\le\lfloor n/m\rfloor}\Lambda(r)P_{q,n}(mr)
 +\frac{\eta_nL_n\mathfrak a_{q,n}}m
 \right].
 \end{aligned}}
 \tag{6.1}
\]

Every endpoint is present: \(m=n\), \(m=M\), the terminal \(n=M\) cell, the
positive affine term inside the bracket, every nontrivial von Mangoldt term,
and the exact squarefree row restriction.  The one-source identity becomes

\[
 \boxed{
 \sum_{q\in\mathcal Q_a}y_qB_a(q)
 =-\sum_{m=1}^{M}\mu(m)\Gamma_y(m).}
 \tag{6.2}
\]

For the current block \(a\le m\le M\), every active \(n\) satisfies
\(n<2m\), so \(\Lambda(1)=0\) removes the von Mangoldt part and

\[
 \boxed{
 \Gamma_y^U(m)=\frac1m\sum_{n=m}^{M}\eta_n
 \sum_{\substack{q\in\mathcal Q_a\\q\le n}}
 y_q\alpha_{q,n}\mathfrak a_{q,n}.}
 \tag{6.3}
\]

If \(y_q\ge0\), then \(\Gamma_y^U(m)>0\) and it is nonincreasing.  With

\[
 A_a(t)=\sum_{a\le m\le t}\mu(m)=M(t)-M(a-1),
\]

finite Abel summation is

\[
 \boxed{\begin{aligned}
 \sum_{m=a}^{M}\mu(m)\Gamma_y^U(m)
 ={}&A_a(M)\Gamma_y^U(M)\\
 &+\sum_{m=a}^{M-1}A_a(m)
 [\Gamma_y^U(m)-\Gamma_y^U(m+1)].
 \end{aligned}}
 \tag{6.4}
\]

All coefficients multiplying the block-Mertens values are nonnegative.  This
is an exact transformed identity, not a lower bound: the block-Mertens values
have both signs, and the old block \(m<a\), which contains all nontrivial
von Mangoldt terms, can cancel the current block.

Cauchy gives the target whenever

\[
 \left|\sum_m\mu(m)\Gamma_y(m)\right|
 \gg \|y\|_2(\log a)^{-3/2}.
 \tag{6.5}
\]

For bounded nonzero smooth tests, \(\|y\|_2\asymp\sqrt a\).  Standard
one-point bounds for \(M(x)\), \(\psi(x)-x\), \(m_x\), and \(1+\ell_x\)
are upper bounds and do not imply the every-scale lower bound (6.5).  Known
omega results are subsequential and also do not control old/current
cancellation.

Taking \(y\) successively to be \(1,q/a,\log(q/a)\) recovers the moment
vector of Section 2.  Exact Gram--Schmidt variants are only basis changes;
they replace (6.1) by the same linear combinations and generally lose the
positivity of (6.3).  Sparse differences give
\(B_a(q)-B_a(q')\), but no unconditional local-oscillation theorem supplies
the required every-scale size.

A natural arithmetic test makes the two-point obstruction explicit.  For a
bounded function \(f\), take

\[
 y_q=\mu(q)f(q/a),\qquad q\in\mathcal Q_a.
\]

Then

\[
 \boxed{
 \langle y,B_a\rangle
 =-\sum_{q\in\mathcal Q_a}\sum_{m=1}^{M}
 \mu(q)\mu(m)f(q/a)\mathscr V_a(q,m).}
 \tag{6.6}
\]

The positive self-diagonal is too small.  Since \(M<2q\),

\[
 \mathscr V_a(q,q)
 =\frac1q\sum_{n=q}^{M}
 \alpha_{q,n}\eta_n\mathfrak a_{q,n}>0,
 \tag{6.7}
\]

including both \(n=q\) and \(n=M\).  Uniformly it is
\(O((a\log a)^{-1})\), whence

\[
 \frac{\left|\sum_{q\in\mathcal Q_a}
 f(q/a)\mathscr V_a(q,q)\right|^2}
 {\sum_{q\in\mathcal Q_a}f(q/a)^2}
 \le\sum_{q\in\mathcal Q_a}\mathscr V_a(q,q)^2
 \ll\frac1{a(\log a)^2}=o((\log a)^{-3}).
 \tag{6.8}
\]

Thus this particular arithmetic dual test requires an every-scale weighted
two-point noncancellation estimate of the form

\[
 \boxed{
 \left|\sum_{q\in\mathcal Q_a}\sum_{m\ne q}
 \mu(q)\mu(m)f(q/a)\mathscr V_a(q,m)\right|
 \gg\|f\|_{\ell^2(\mathcal Q_a)}(\log a)^{-3/2},}
 \tag{6.9}
\]

with enough signed control to prevent cancellation with the negligible
diagonal.  Formula (6.9) is a sufficient missing estimate for this test, not a
logically necessary condition for every possible dual proof.  Its weight has
moving ratio support, the full old/current source range, and pointwise-in-\(a\)
quantifiers.  Fixed-shift or logarithmically averaged Chowla estimates do not
imply it.

There is also a sharp limitation on the current input package.  In (1.1), the
surrogate one-point data

\[
 \psi(k)=k,\qquad m_n=0,\qquad 1+\ell_n=0
\]

obey every absolute zero-free-region upper envelope used in Cycles 49--51,
yet leave only a deterministic discretization residual of size
\(O((\log a)/a)\), which gives

\[
 \|B_a\|_2^2\ll\frac1{a(\log a)^2}=o((\log a)^{-3}).
\]

This surrogate is not claimed to arise from an arithmetic Mobius sequence.
It proves only that those one-point upper bounds, by themselves, cannot entail
the desired lower bound.  A proof needs a genuine arithmetic coupling or
noncancellation theorem such as (6.5) or, for the specific signed test,
(6.9).

## 7. Exact finite differences and smooth-mode annihilator

The suffix normal form also permits an endpoint-complete test of the tempting
finite-difference route.  Write

\[
 F_n(q)=(p_nx_q+r_n)
 \left(T_nx_q+\frac{A_n^\star}{q}+\Pi_{q-1}+D_n^\star\right),
 \qquad x_q=\log q,
 \tag{7.1}
\]

so that \(B_a(q)=\sum_{n=q}^M F_n(q)\), and let
\(\Delta f(q)=f(q+1)-f(q)\).  Direct finite reindexing gives

\[
 \boxed{\Delta B_a(q)=
 \sum_{n=q+1}^M\Delta F_n(q)-F_q(q),}
 \tag{7.2}
\]

\[
 \boxed{\begin{aligned}
 \Delta^2B_a(q)={}&\sum_{n=q+2}^M\Delta^2F_n(q)\\
 &+F_q(q)+F_{q+1}(q)-2F_{q+1}(q+1),
 \end{aligned}}
 \tag{7.3}
\]

and

\[
 \boxed{\begin{aligned}
 \Delta^3B_a(q)={}&\sum_{n=q+3}^M\Delta^3F_n(q)-F_q(q)-F_{q+1}(q)\\
 &+3F_{q+1}(q+1)-F_{q+2}(q)+3F_{q+2}(q+1)\\
 &-3F_{q+2}(q+2).
 \end{aligned}}
 \tag{7.4}
\]

Empty sums are zero.  More generally,

\[
 \Delta^jB_a(q)=\sum_{i=0}^j(-1)^{j-i}{j\choose i}
 \sum_{n=q+i}^M F_n(q+i).
 \tag{7.5}
\]

These formulas retain every moving-lower-end cell.  They do not localize the
arithmetic packet.  Indeed, with

\[
 g_q=\frac{\psi(q)}{q(q+1)},\qquad
 H_n(q)=T_n\log q+\frac{A_n^\star}{q}+\Pi_{q-1}+D_n^\star,
\]

one has, for \(j\ge1\),

\[
 \Delta^jH_n(q)=T_n\Delta^j\log q
 +A_n^\star\frac{(-1)^jj!}{q(q+1)\cdots(q+j)}
 +\Delta^{j-1}g_q.
 \tag{7.6}
\]

The coefficient of \(\psi(q)\) in the last term is
\((-1)^{j-1}j!/[q(q+1)\cdots(q+j)]\ne0\).  Moreover, expansion of
\(F_n(q)\) shows that the coefficient of the cumulative \(\Pi_{q-1}\)
channel after \(\Delta^j\) contains \(p_n\Delta^j\log q\ne0\).  Thus no fixed
ordinary difference reduces the interior to finitely many local prime values.
In particular,

\[
 \Delta^3\log q=
 \log\frac{(q+3)(q+1)^3}{q(q+2)^3}>0,
 \tag{7.7}
\]

because the numerator minus the denominator before taking logarithms is
\(2q+3\).

There is an exact variable-coefficient four-point test which does annihilate
all three sampled modes.  Set

\[
 d_i=\log\frac{q+i+1}{q+i}\quad(0\le i\le2)
\]

and

\[
 \begin{aligned}
 c_0&=d_2-d_1,&c_1&=d_0+d_1-2d_2,\\
 c_2&=-2d_0+d_1+d_2,&c_3&=d_0-d_1.
 \end{aligned}
 \tag{7.8}
\]

Then \(\sum c_i=\sum i c_i=\sum c_i\log(q+i)=0\), so
\(\mathcal A_qf=\sum_{i=0}^3c_if(q+i)\) annihilates
\(1,q/a,\log(q/a)\).  Its moving-boundary identity is

\[
 \boxed{\begin{aligned}
 \mathcal A_qB_a={}&\sum_{n=q+3}^M\mathcal A_qF_n+c_0F_q(q)\\
 &+c_0F_{q+1}(q)+c_1F_{q+1}(q+1)\\
 &+c_0F_{q+2}(q)+c_1F_{q+2}(q+1)+c_2F_{q+2}(q+2).
 \end{aligned}}
 \tag{7.9}
\]

For each fixed interior cell,

\[
 \boxed{\begin{aligned}
 \mathcal A_qF_n={}&p_nT_n\sum_{i=0}^3c_i\log^2(q+i)\\
 &+A_n^\star\sum_{i=0}^3c_i
 \frac{p_n\log(q+i)+r_n}{q+i}\\
 &+\sum_{i=0}^3c_i[p_n\log(q+i)+r_n]\Pi_{q+i-1}.
 \end{aligned}}
 \tag{7.10}
\]

Hence even the exact smooth-mode annihilator leaves quadratic-logarithmic,
reciprocal, and arithmetic-prefix channels, together with the boundary cells.
This is a no-go for these specific first/second/third-difference and four-point
architectures, not for every longer variable-coefficient test.

On a full consecutive row interval, the elementary operator estimate
\(\|\Delta^jf\|_2\le2^j\|f\|_2\) gives

\[
 \|f\|_2^2\ge4^{-j}\|\Delta^jf\|_2^2.
 \tag{7.11}
\]

For consecutive selected squarefree rows \(s_i\), one likewise has

\[
 \sum_i|B_a(s_i)|^2\ge\frac14
 \sum_i|B_a(s_{i+1})-B_a(s_i)|^2.
 \tag{7.12}
\]

These Poincare inequalities are valid, but useful only after a new arithmetic
lower bound for the full signed differenced expression.  Ordinary all-row
differences also involve nonsquarefree extensions and cannot be transferred to
the physical squarefree norm without a separate sampling theorem.

## 8. Retention remains independent

Let

\[
 C_a=\widehat{\mathbf c}_a=B_a+H_a,
 \qquad
 \mathbf d_a=F_a^TC_a.
\]

From (2.5),

\[
 \boxed{
 \langle B_a,C_a\rangle
 =\mathbf m_a^TG_a^+\mathbf d_a
  +\langle R_a^{(3)},C_a\rangle.}
 \tag{8.1}
\]

With every zero denominator interpreted by the existing zero-safe convention,

\[
 \boxed{
 \mathcal Q_a^{\rm cp}
 =\frac{\left|\mathbf m_a^TG_a^+\mathbf d_a
 +\langle R_a^{(3)},C_a\rangle\right|^2}
 {\mathbf m_a^TG_a^+\mathbf m_a+\|R_a^{(3)}\|_2^2}.}
 \tag{8.2}
\]

Neither numerator term has a controlled sign, and they may cancel.  Thus a
proof of (3.2), a proof of (3.3), or even exact three-mode closure would not by
itself prove retention.

A valid sufficient pair remains

\[
 \|B_a\|_2^2\ge c_0(\log a)^{-3}
 \tag{8.3}
\]

and, independently,

\[
 |\langle B_a,C_a\rangle|
 \ge\varepsilon\|B_a\|_2^2.
 \tag{8.4}
\]

Then

\[
 \mathcal Q_a^{\rm cp}
 \ge\varepsilon^2c_0(\log a)^{-3}.
\]

The three-mode moment sieve addresses only the first requirement.

## 9. Surviving checkpoint

The finite smooth-span heuristic has been demoted.  The exact useful target is
now the selected arithmetic moment estimate (3.2), the orthogonal remainder
estimate (3.3), or another proof of their total energy scale, together with the
separate signed retention estimate (8.4).  Formula (2.3) states the moment
problem without hiding any arithmetic packet.

The canonical stronger target remains

\[
 \boxed{\mathcal Q_a^{\rm cp}\gg(\log a)^{-3}.}
\]

The Cycle 51 source-plane quantity remains a fallback below the physical norm,
but neither it nor the three-mode projection replaces the canonical signed
retention problem.
