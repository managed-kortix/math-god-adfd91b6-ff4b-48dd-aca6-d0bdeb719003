# Cycle 53: current-adjoint injectivity, monotone-tail obstruction, and retention audit

## Status and scope

Fix

\[
 0<\theta<\frac12,
 \qquad C=2(1-\theta),
 \qquad \tau=C-1,
 \qquad M=2a-1,
\]

and the physical row set

\[
 \mathcal Q_a=\left\{q\in\mathbb Z:
   \mu(q)^2=1,\ a\le q\le\left\lfloor\frac{3a}{2}\right\rfloor
 \right\}.
\]

This note continues the Cycle 50--52 exact one-source and complete-prefix
analysis.  It proves the following limited structural facts.

1. The convolutional current one-source matrix, using every source column
   \(a\le m\le M\), has full row rank.  Equivalently, its adjoint is
   injective on physical row tests.  This is qualitative finite rank only;
   it gives no uniform lower singular-value bound and no selected Mobius
   noncancellation.
2. Every nonzero nonnegative row test produces a strictly positive, strictly
   decreasing current transform on `a<=m<=2a-1`. An exact rational abstract
   reciprocal-tail packet with the actual Mobius signs nevertheless has zero
   Mobius contraction.
   Thus positivity, strict decrease, and the reciprocal-tail shape alone
   cannot prove the required lower bound.
3. At fixed \(\theta=2/5\), elementary enumeration and strict concavity show
   that \(a=10\) is the first scale capable of refuting exact three-mode
   closure, and a standalone 256-bit Arb certificate proves that closure
   already fails there. It reconstructs the prefix by two algebraically
   distinct paths: literal fractional-part cell integrals and the
   cancellation-preserving residual.
4. The temporal prefix and tail sources are orthogonal before one applies the
   common analysis operator, but their output vectors need not be. Existing
   physical certificates rule out rowwise contraction, while compatible
   prefix and complete-gauge columns at physical current labels, combined
   with nonphysical coefficients, rule out coefficient-blind operator
   contraction. The actual aggregate Mobius retention inequality remains
   open.
5. A bounded nonrigorous Perron-test screen found a near-zero at \(a=4056\).
   This is finite heuristic evidence only, but it rejects promotion of the
   Perron current singular vector as a preferred proof route.

Nothing here proves

\[
 \|B_a\|_2^2\gg(\log a)^{-3},\qquad
 \mathcal Q_a^{\rm cp}\gg(\log a)^{-3},\qquad
 D_a(I_0)\gg(\log a)^{-3},
\]

or the Riemann hypothesis.

## 1. Exact row-dual transform

Retain the Cycle 50 definitions

\[
 \mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q},
\]

\[
 \mathscr K_{q,n}(m)=
 \sum_{r\le\lfloor n/m\rfloor}\Lambda(r)P_{q,n}(mr)
 +\frac{\eta_nL_n\mathfrak a_{q,n}}m,
\]

and

\[
 \mathscr V_a(q,m)=
 \sum_{n=\max(q,m)}^M
 \frac{\alpha_{q,n}}{L_n}\mathscr K_{q,n}(m).
\]

Then

\[
 B_a(q)=-\sum_{m=1}^M\mu(m)\mathscr V_a(q,m).
 \tag{1.1}
\]

For a real row test \(y=(y_q)_{q\in\mathcal Q_a}\), put

\[
 \Gamma_y(m)=\sum_{q\in\mathcal Q_a}y_q\mathscr V_a(q,m).
 \tag{1.2}
\]

Finite interchange gives the endpoint-complete identity

\[
 \boxed{\begin{aligned}
 \Gamma_y(m)={}&
 \sum_{n=\max(a,m)}^M\frac1{L_n}
 \sum_{\substack{q\in\mathcal Q_a\\q\le n}}
 y_q\alpha_{q,n}\\
 &\quad\times\left[
 \sum_{r\le\lfloor n/m\rfloor}\Lambda(r)P_{q,n}(mr)
 +\frac{\eta_nL_n\mathfrak a_{q,n}}m
 \right].
 \end{aligned}}
 \tag{1.3}
\]

Consequently

\[
 \boxed{
 \langle y,B_a\rangle
 =-\sum_{m=1}^M\mu(m)\Gamma_y(m).}
 \tag{1.4}
\]

Equations (1.3)--(1.4) are Cycle 52's dual transform, repeated here only to
fix the current-matrix theorem's notation.  In particular, the outer minus
sign is part of the identity, the old-source temporal lower endpoint is
\(a\), and there is no temporal \(n=2a\) term.

## 2. Full row rank of the exact current matrix

Define the convolutional current matrix

\[
 \mathsf V_a^{\rm cur}
 =\bigl(\mathscr V_a(q,m)\bigr)_
 {q\in\mathcal Q_a,\ a\le m\le M}.
 \tag{2.1}
\]

This is the Cycle 50--51 convolutional source gauge.  It is not the direct
collapsed \(W_B(q,d)\) gauge.

### Theorem 2.1 (finite current-adjoint injectivity)

For every integer \(a\ge2\) and \(0<\theta<1/2\),

\[
 \boxed{
 \operatorname{rank}\mathsf V_a^{\rm cur}=\#\mathcal Q_a.}
 \tag{2.2}
\]

Equivalently,

\[
 \boxed{
 (\mathsf V_a^{\rm cur})^Ty=0\Longrightarrow y=0.}
 \tag{2.3}
\]

#### Proof

For every active current triple,

\[
 a\le m\le n\le M=2a-1<2m.
\]

Therefore \(\lfloor n/m\rfloor=1\), and \(\Lambda(1)=0\) removes the
von Mangoldt part of \(\mathscr K_{q,n}(m)\).  Hence

\[
 \boxed{
 \mathscr V_a(q,m)=\frac1m
 \sum_{n=\max(q,m)}^M
 \alpha_{q,n}\eta_n\mathfrak a_{q,n}.}
 \tag{2.4}
\]

Let temporal rows and columns be indexed by \(a,\ldots,M\), and set

\[
 T_{q,n}=
 \mathbf 1_{q\le n}\alpha_{q,n}\eta_n\mathfrak a_{q,n},
 \qquad
 R_{n,m}=\frac{\mathbf 1_{m\le n}}m.
 \tag{2.5}
\]

Then (2.4) gives the exact factorization

\[
 \mathsf V_a^{\rm cur}=TR.
 \tag{2.6}
\]

The matrix \(R\) is lower triangular (rows indexed by \(n\), columns by
\(m\)) with diagonal \(1/m\), so it is invertible.  Order the physical rows as
\(q_1<\cdots<q_r\), and select from \(T\) the columns
\(n=q_1,\ldots,q_r\).  The resulting square matrix is upper triangular:
\(T_{q_i,q_j}=0\) for \(j<i\).  Its diagonal is

\[
 T_{q,q}=
 \alpha_{q,q}\eta_q
 \left(1-\log\left(1+\frac1q\right)\right)>0.
 \tag{2.7}
\]

Here \(\alpha_{q,q}>0\) is the Cycle 49 temporal-weight theorem,
\(\eta_q>0\) uses \(0<\theta<1/2\), and
\(\log(1+1/q)<1/q<1\).  Thus the selected minor of \(T\) is nonzero,
so \(T\), and therefore \(TR\), has full row rank.  \(\square\)

### Scope

The theorem uses every current column \(a\le m\le M\). Adjoining old
columns preserves full row rank, so the adjoint of the full convolutional
matrix is also injective. The theorem does not prove injectivity of the primal
wide source-to-row map, transfer to the direct `W_B` gauge, stable inversion,
or any useful scale-uniform lower bound for the least nonzero singular value.
It gives no nonvanishing bound for contraction with the current Mobius vector
and says nothing about cancellation against the old source block. At the
excluded endpoint \(\theta=1/2\), one has \(\eta_n=0\), and the current
matrix is zero.

## 3. Strict current monotonicity and its exact obstruction

Suppose \(y_q\ge0\) on \(\mathcal Q_a\) and \(y\ne0\).  For
\(a\le m\le M\), define

\[
 c_y(n)=\eta_n
 \sum_{\substack{q\in\mathcal Q_a\\q\le n}}
 y_q\alpha_{q,n}\mathfrak a_{q,n}.
 \tag{3.1}
\]

Then \(c_y(n)\ge0\), and (2.4) gives

\[
 \boxed{
 \Gamma_y(m)=\frac1m\sum_{n=m}^Mc_y(n).}
 \tag{3.2}
\]

Every physical row is at most \(M\), so \(c_y(M)>0\).  Therefore, for
\(a\le m<M\),

\[
 \boxed{\begin{aligned}
 \Gamma_y(m)-\Gamma_y(m+1)
 ={}&\frac{c_y(m)}m
 +\frac1{m(m+1)}\sum_{n=m+1}^Mc_y(n)>0.
 \end{aligned}}
 \tag{3.3}
\]

The affine summand in (1.3) also shows
\(\Gamma_y(m)>0\) for every \(1\le m\le M\).  Hence the current block
sharpens Cycle 52's nonincreasing statement to

\[
 \boxed{
 \Gamma_y(a)>\Gamma_y(a+1)>\cdots>\Gamma_y(M)>0.}
 \tag{3.4}
\]

No monotonicity is claimed for the old indices \(m<a\), or for signed row
tests.

### Proposition 3.1 (exact reciprocal-tail Mobius zero)

Let

\[
 (h_8,\ldots,h_{15})
 =\left(1,1,1,1,1,\frac{5767}{2037},1,1\right)
 \tag{3.5}
\]

and

\[
 \gamma_m=\frac1m\sum_{n=m}^{15}h_n.
 \tag{3.6}
\]

Exact rational arithmetic gives

\[
 (\gamma_8,\ldots,\gamma_{15})=
 \left(
 \frac{10013}{8148},\frac{17989}{18333},
 \frac{7976}{10185},\frac{1265}{2037},
 \frac{5939}{12222},\frac{757}{2037},
 \frac17,\frac1{15}
 \right).
 \tag{3.7}
\]

All entries are positive, and their consecutive differences are

\[
 \left(
 \frac{18161}{73332},\frac{18161}{91665},
 \frac{1651}{10185},\frac{1651}{12222},
 \frac{1397}{12222},\frac{466}{2037},\frac8{105}
 \right)>0.
 \tag{3.8}
\]

Nevertheless, with the actual Mobius values on this interval,

\[
 (\mu(8),\ldots,\mu(15))=(0,0,1,-1,0,-1,1,1),
\]

one has

\[
 \boxed{
 \sum_{m=8}^{15}\mu(m)\gamma_m=0.}
 \tag{3.9}
\]

Indeed, if \(S_n=\sum_{m=8}^n\mu(m)/m\), then

\[
 S_{13}=-\frac{97}{1430},
\]

and the terms in \(\sum_nh_nS_n\) other than \(n=13\) sum to
\(5767/30030\), while the \(n=13\) term is \(-5767/30030\).

This packet is not asserted to arise from one physical row test.  Its exact
logical consequence is narrower:

> positive temporal masses, a positive strictly decreasing reciprocal-tail
> transform, and the actual Mobius signs do not by themselves imply a nonzero
> current contraction.

Thus a proof must use the coupled physical dependence of \(c_y(n)\) on one
row test, or another arithmetic input.  Qualitative full row rank does not
repair the loss.

## 4. Minimal finite three-mode nonclosure certificate

At \(\theta=2/5\), hence \(C=6/5\), the physical row set at \(a=10\) is

\[
 \mathcal Q_{10}=\{10,11,13,14,15\}.
 \tag{4.1}
\]

For \(2\le a<10\), direct enumeration gives at most three physical rows.
On at most three distinct positive points, the sampled functions

\[
 1,\qquad q/a,\qquad\log(q/a)
\]

have full row rank: for three rows this follows from strict concavity of
\(\log\).  Hence every row vector lies tautologically in their sampled span,
and \(a=10\) is the first scale at which nonclosure can occur.

On the four-row subset \(\{10,11,14,15\}\), form

\[
 \mathsf A=
 \left(1,\frac q{10},\log\frac q{10},B_{10}(q)\right).
 \tag{4.2}
\]

Elementary enumeration and strict concavity prove the minimality statement;
the standalone artifact proves nonclosure at that first capable scale.
The artifact

```text
cycle52_a10_cell_nonclosure_certificate.py
cycle52-a10-cell-nonclosure-certificate.out
```

pins CPython 3.12.13, python-flint 0.9.0, FLINT 3.6.0, and 256-bit Arb.  It
constructs the Mobius table independently by trial factorization and a linear
sieve and verifies the divisor convolution.  It reconstructs every
\(B_{10}(q)\) by two independent routes.

The first is the cancellation-preserving residual

\[
 B_{10}(q)=\sum_{n=q}^{19}\frac{\alpha_{q,n}}{L_n}
 \left[
 \frac{\mathscr C_{n+1}}q-(\Pi_n-\Pi_{q-1})
 +\left(\frac nq-\log\frac{n+1}{q}\right)
 (\ell_n-\eta_nL_nm_n)
 \right].
 \tag{4.3}
\]

The second uses literal fractional-part cell integrals.  For
\(1\le k\le n\), put \(Q_k=\lfloor k/q\rfloor\) and
\(D_k=\lfloor k/d\rfloor\).  Then

\[
 \begin{aligned}
 P_{q,n}(d)=\sum_{k=1}^n\biggl[&
 \frac1{qd}
 -\left(\frac{Q_k}{d}+\frac{D_k}{q}\right)
   \log\frac{k+1}{k}\\
 &+Q_kD_k\left(\frac1k-\frac1{k+1}\right)
 \biggr],
 \end{aligned}
 \tag{4.4}
\]

\[
 P_{q,n}(0)=\sum_{k=1}^n\left[
 \frac1q\log\frac{k+1}{k}
 -Q_k\left(\frac1k-\frac1{k+1}\right)
 \right],
 \tag{4.5}
\]

and the cell route is

\[
 \begin{aligned}
 B_{10}^{\rm cell}(q)=
 \sum_{n=q}^{19}\alpha_{q,n}\biggl[&
 -\eta_nP_{q,n}(0)\\
 &+\sum_{d\le n}\mu(d)
 \left(\frac{\log d}{\log n}-\eta_n\right)P_{q,n}(d)
 \biggr].
 \end{aligned}
 \tag{4.6}
\]

Every rowwise difference between (4.3) and (4.6) contains zero with absolute
upper bound below \(2^{-170}\).  Both paths independently evaluate the
four-by-four determinant by the 24-term Leibniz formula and certify

\[
 \boxed{
 \det\mathsf A=
 [1.5197573366214305638022462131155847370578536699179450070895374840
 \times10^{-5}\ \mathbin{+/-}\ 4.49\times10^{-70}]>0.}
 \tag{4.7}
\]

Therefore

\[
 \boxed{
 B_{10}\notin
 \operatorname{span}\{1,q/10,\log(q/10)\}
 \quad\text{on }\mathcal Q_{10}.}
 \tag{4.8}
\]

The unused fifth row \(q=13\) cannot lower the rank proved by this nonzero
four-row minor.  This is a finite obstruction to universal exact closure.  It
does not refute eventual closure, asymptotic approximation, a positive
capture liminf, or the moment lower-bound route.

The same script verifies Proposition 3.1 entirely with exact rational
arithmetic.  Its audited SHA-256 hashes are

```text
5251454b1f736df3acbffa97db922da8e67de3cba016d17238bd4dd7c86ab4a1  cycle52_a10_cell_nonclosure_certificate.py
628a0188f3269aa8f659bedb2197ee0762afb1ef173483b209ccc21b874b1328  cycle52-a10-cell-nonclosure-certificate.out
8a2777389ba05cc4e63a305b12871804311863897f8bd167550069fd282f37c4  captured closure manifest
```

Replay from the repository root with

```bash
rm -f /tmp/cycle52-a10-cell-nonclosure-certificate.out && \
env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C \
uv run --isolated --no-project --python 3.12.13 \
  --with python-flint==0.9.0 \
  python -I -B \
  millennium-prize/riemann-hypothesis/cycle52_a10_cell_nonclosure_certificate.py \
  > /tmp/cycle52-a10-cell-nonclosure-certificate.out && \
cmp /tmp/cycle52-a10-cell-nonclosure-certificate.out \
  millennium-prize/riemann-hypothesis/cycle52-a10-cell-nonclosure-certificate.out
```

The trusted boundary pins versions but does not binary-attest the interpreter,
wheel, native library, operating system, hardware, or `uv` launcher.

## 5. Temporal support splitting and retention

Let

\[
 H=L^2([1,\infty),dt/t^2),
 \qquad
 \mathscr H_a=\bigoplus_{n=a}^MH,
\]

and define the orthogonal projections

\[
 E_nf=\mathbf1_{[1,n+1]}f,
 \qquad
 E_a=\bigoplus_{n=a}^ME_n.
\]

Put \(z_a=(Z_n)_{n=a}^M\),

\[
 p_a=E_az_a,
 \qquad
 t_a=(I-E_a)z_a.
\]

The singleton boundary is null, so \(p_a\perp t_a\) in
\(\mathscr H_a\).  Define the common analysis operator

\[
 (\mathscr A_af)(q)=
 \sum_{n=q}^M\alpha_{q,n}\langle\rho_q,f_n\rangle_H.
 \tag{5.1}
\]

Then exactly

\[
 \boxed{
 B_a=\mathscr A_ap_a,
 \qquad H_a=\mathscr A_at_a,
 \qquad C_a=\mathscr A_a(p_a+t_a).}
 \tag{5.2}
\]

Thus

\[
 \langle B_a,H_a\rangle
 =\langle p_a,\mathscr A_a^*\mathscr A_at_a\rangle.
 \tag{5.3}
\]

The positive normal operator \(\mathscr A_a^*\mathscr A_a\) need not
preserve the orthogonal support split.  Explicitly, if

\[
 \mathcal B_{q,n}=\langle\rho_q,E_nZ_n\rangle,
 \qquad
 \mathcal T_{q,n}=\langle\rho_q,(I-E_n)Z_n\rangle,
\]

then

\[
 \boxed{\begin{aligned}
 \langle B_a,H_a\rangle
 =\sum_{q\in\mathcal Q_a}
 \sum_{m,n=q}^M
 \alpha_{q,m}\alpha_{q,n}
 \mathcal B_{q,m}\mathcal T_{q,n}.
 \end{aligned}}
 \tag{5.4}
\]

All equal-time and unequal-time terms remain in the exact expansion; source
orthogonality eliminates none of them structurally. Individual terms can
still vanish or cancel arithmetically. Source orthogonality therefore does
not give output orthogonality or retention.

For \(b=\|B_a\|\), \(h=\|H_a\|\), and
\(c=\langle B_a,H_a\rangle\), the zero-safe canonical line quantity is

\[
 \mathcal Q_a^{\rm cp}=
 \begin{cases}
 (b^2+c)^2/b^2,&b>0,\\
 0,&b=0.
 \end{cases}
 \tag{5.5}
\]

When \(b>0\), put

\[
 s_a=h^2-\frac{c^2}{b^2}
 =\left\|H_a-\frac{c}{b^2}B_a\right\|^2.
 \tag{5.6}
\]

With `sgn(0)=0`, one then has

\[
 \boxed{
 \mathcal Q_a^{\rm cp}
 =\left(b+\operatorname{sgn}(c)\sqrt{h^2-s_a}\right)^2.}
 \tag{5.7}
\]

This is an exact reformulation, not a new estimate.  It shows that only the
component of \(H_a\) parallel to \(B_a\) can cancel the prefix.  A sufficient
retention condition, weaker than total tail contraction, is

\[
 \boxed{
 |\langle B_a,H_a\rangle|
 \le\kappa\|B_a\|^2
 \quad\text{for some fixed }0\le\kappa<1.}
 \tag{5.8}
\]

Together with \(\|B_a\|^2\ge c_0(\log a)^{-3}\), it would give

\[
 \mathcal Q_a^{\rm cp}\ge
 (1-\kappa)^2c_0(\log a)^{-3}.
 \tag{5.9}
\]

Condition (5.8) can hold even when \(\|H_a\|>\|B_a\|\), provided the large
tail component is sufficiently transverse.  It is still unproved.

### Exact architecture obstructions

1. **Rowwise contraction is physically false.**  The Cycle 49 certificate at
   \(\theta=2/5,a=218,q=327\) gives

   \[
   B_a(q)=-5.2781989809000\ldots\times10^{-5},
   \qquad
   H_a(q)=+5.3834622376955\ldots\times10^{-5}.
   \]

   Both signs and \(|H_a(q)|>|B_a(q)|\) are outward-certified.  This refutes
   a universal pointwise \(|H_a(q)|\le\kappa|B_a(q)|\) with
   \(\kappa<1\).  It does not refute an aggregate eventual theorem.

2. **Coefficient-blind operator contraction is false.**  Cycle 50's compatible
   delta-gauge certificate proves that physical prefix and full current
   columns are not proportional already at \(\theta=2/5,a=3\).  A nonphysical
   real coefficient vector can therefore annihilate the prefix while leaving
   a nonzero tail.  Thus no inequality

   \[
   \|W_Hx\|\le\kappa\|W_Bx\|
   \]

   can hold for every coefficient vector.  This rules out generic Loewner or
   operator domination, not a theorem for the actual Mobius vector.

3. **One-point PNT/Mertens bounds are insufficient.**  They give upper
   envelopes for prefix and tail packets, but no lower bound for \(\|B_a\|\)
   and no relative mixed-kernel estimate.  The physical retention target is a
   selected moving two-kernel Mobius quadratic inequality.  Improving the
   zero-free-region upper bounds does not supply its missing phase control.

The exact sign-free retention condition paired with a prefix lower bound is

\[
 \boxed{
 |\langle B_a,C_a\rangle|
 =|\|B_a\|^2+\langle B_a,H_a\rangle|
 \ge\varepsilon\|B_a\|^2.}
 \tag{5.10}
\]

A convenient sufficient one-sided replacement is

\[
 \boxed{
 \langle B_a,H_a\rangle
 \ge-(1-\varepsilon)\|B_a\|^2.}
 \tag{5.11}
\]

It excludes sign-reversing overcancellation and is stronger than necessary,
but unlike total-tail contraction it asks only for the signed component that
enters the canonical line projection. All temporal, affine, old/current, and
Mobius cross terms must remain.

## 6. Bounded Perron-test diagnostic

A natural prescribed test is obtained from the exact current matrix.  Every entry of \(\mathsf V_a^{\rm cur}\) is strictly positive by (2.4), so
\(\mathsf V_a^{\rm cur}(\mathsf V_a^{\rm cur})^T\) is entrywise strictly
positive. Perron--Frobenius therefore gives a simple top eigenvalue and a
unique positive unit dominant left singular vector \(p^{(a)}>0\). Prescribe

\[
 y_q^{(a)}=\mu(q)p_q^{(a)}.
 \tag{6.1}
\]

This test is independent of the observed prefix vector, but it optimizes the
positive current matrix before the row Mobius signs, source Mobius signs, and
old block are inserted.

A temporary binary64 screen at \(\theta=2/5\), retaining the complete
old/current contraction, found at \(a=4056\)

\[
 |\langle y^{(a)},B_a\rangle|(\log a)^{3/2}
 \approx4.6861872\times10^{-7},
 \tag{6.2}
\]

while the separately normalized old and current pieces were approximately

\[
 +4.4712429\times10^{-4},
 \qquad
 -4.4665567\times10^{-4}.
 \tag{6.3}
\]

A long-double replay with the computed singular vector fixed returned the same
near-zero to the shown digits. These calculations are nonrigorous finite
session diagnostics, not a committed reproducible artifact, interval
certificate, or asymptotic counterexample. They are recorded only as route
selection evidence: Perron positivity or singular-value separation cannot be
used as a sign or dominance proof. No theorem is inferred from the displayed
numbers.

The exact self-diagonal remains negligible for every unit positive profile:

\[
 \left|\sum_{q\in\mathcal Q_a}
 p_q^{(a)}\mathscr V_a(q,q)\right|
 \le\left(\sum_q\mathscr V_a(q,q)^2\right)^{1/2}
 \ll\frac1{\sqrt a\log a}
 =o((\log a)^{-3/2}).
 \tag{6.4}
\]

Thus any successful Mobius-modulated Perron proof would still need the full
old plus current-off-diagonal two-point noncancellation estimate.  The finite
near-zero makes this test less attractive than the simpler unsigned moment
channels; it proves no eventual failure.

## 7. Surviving checkpoints

The prefix norm and retention remain separate.

A sufficient prescribed-test prefix statement is: choose, before observing
\(B_a\), a nonzero family \(y^{(a)}\), and prove with constants uniform in
\(a\)

\[
 \boxed{
 \left|\sum_{m=1}^{2a-1}\mu(m)\Gamma_{y^{(a)}}(m)\right|
 \gg\|y^{(a)}\|_2(\log a)^{-3/2}.}
 \tag{7.1}
\]

The finite rank theorem proves only that a nonzero row test has a nonzero
*vector* current transform.  Proposition 3.1 proves that its qualitative
positive-tail shape cannot replace (7.1).  No result established in Cycles 47--53 proves (7.1) for the constant, smooth
Gram--Schmidt, character, Mobius-modulated, or Perron test families considered
here.

Independently, retention requires (5.10), or another equivalent estimate
implying

\[
 |\langle B_a,C_a\rangle|
 \ge\varepsilon\|B_a\|^2.
 \tag{7.2}
\]

Only after both (7.1), or an equivalent prefix lower bound, and (7.2) are
proved can one infer

\[
 \mathcal Q_a^{\rm cp}\gg(\log a)^{-3}.
\]

A later passage from that intrinsic projection bound to the full physical
budget would still require the separate normalization and upper-budget gates
from Cycles 45--48.  No completed-square budget and no RH result is proved.
