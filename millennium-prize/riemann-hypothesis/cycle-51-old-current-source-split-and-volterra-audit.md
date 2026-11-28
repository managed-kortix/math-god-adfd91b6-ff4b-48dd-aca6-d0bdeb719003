# Cycle 51: old/current one-source split, normalized projection, and Volterra audit

## Status and scope

This note continues the Cycle 50 one-source representation on the fixed row
interval

\[
 I_0=[1,3/2].
\]

It proves the following finite and asymptotic structural statements.

1. Splitting the one-source Möbius sum at the moving cutoff \(m=a\) gives an
   exact two-vector decomposition \(B_a=O_a+U_a\).  The current block
   \(U_a\) has an exact reciprocal-Möbius formula: all nontrivial von
   Mangoldt terms vanish there.
2. Projection onto \(\operatorname{span}\{O_a,U_a\}\) is exactly the
   canonical complete-prefix line projection plus one orthogonal tail-retention
   channel.  This supplies a legitimate fallback target, but does not imply the
   canonical line bound.
3. The raw Gram ratio \(\det G/(\operatorname{tr}G)^2\) is not an intrinsic
   angular statistic and is redundant in the proposed sufficient lower-bound
   criterion.  Column-normalized moments give a rank-safe, scale-invariant
   replacement.
4. The current one-source columns have an explicit locally uniform Volterra
   limit, with a factorization and adjoint.  This entrywise limit cannot be
   passed through the growing signed Möbius contraction.
5. Standard quantitative PNT and reciprocal-zeta estimates give only
   source-channel upper bounds which are much too large, after summing the
   rows, to settle the target energy scale.

The finite scripts stored with this note are IEEE-754 binary64 diagnostics,
not interval certificates.  They support the algebra and expose severe,
nonmonotone conditioning at tested scales, but prove no eventual statement.

Nothing here proves

\[
 \|B_a\|_2^2\gg(\log a)^{-3},\qquad
 \mathcal Q_a^{\rm cp}\gg(\log a)^{-3},\qquad
 D_a(I_0)\gg(\log a)^{-3},
\]

or the Riemann hypothesis.

## 1. Definitions and the exact source split

Retain all notation of Cycle 50.  Thus

\[
 M=2a-1,
\]

physical rows are

\[
 \mathcal Q_a=\{q:\mu(q)^2=1,\ a\le q\le3a/2\},
\]

and

\[
 B_a(q)=-\sum_{m=1}^{M}\mu(m)\mathscr V_a(q,m),
 \tag{1.1}
\]

where

\[
 \mathscr V_a(q,m)=\sum_{n=\max(q,m)}^{M}
 \frac{\alpha_{q,n}}{L_n}\mathscr K_{q,n}(m),
 \tag{1.2}
\]

\[
 \mathscr K_{q,n}(m)=
 \sum_{r\le\lfloor n/m\rfloor}\Lambda(r)P_{q,n}(mr)
 +\frac{\eta_nL_n\mathfrak a_{q,n}}m,
 \tag{1.3}
\]

and

\[
 \mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q}.
\]

Define, on the same physical row space,

\[
 O_a(q)=-\sum_{m<a}\mu(m)\mathscr V_a(q,m),
 \qquad
 U_a(q)=-\sum_{a\le m\le M}\mu(m)\mathscr V_a(q,m).
 \tag{1.4}
\]

Then, exactly,

\[
 \boxed{B_a=O_a+U_a.}
 \tag{1.5}
\]

The labels “old” and “current” refer to the convolutional source index \(m\)
in (1.1).  They do not refer to the direct collapsed columns \(W_B(q,d)\) of
Cycle 50.  These are distinct pure-Möbius gauges; their individual columns and
continuum kernels must not be compared as though their source labels agreed.

## 2. Exact collapse of the current channel

Put

\[
 m_x=\sum_{d\le x}\frac{\mu(d)}d.
\]

### Theorem 2.1 (current-source collapse)

For every physical row \(q\in\mathcal Q_a\),

\[
 \boxed{
 U_a(q)=-\sum_{n=q}^{M}
 \alpha_{q,n}\eta_n\mathfrak a_{q,n}
 \bigl(m_n-m_{a-1}\bigr).}
 \tag{2.1}
\]

#### Proof

Interchanging the two finite sums gives

\[
 U_a(q)=-\sum_{n=q}^{M}\frac{\alpha_{q,n}}{L_n}
 \sum_{m=a}^{n}\mu(m)\mathscr K_{q,n}(m).
 \tag{2.2}
\]

Every active triple satisfies

\[
 a\le m\le n\le M=2a-1<2m.
\]

Consequently \(\lfloor n/m\rfloor=1\), while
\(\Lambda(1)=0\).  Formula (1.3) therefore reduces exactly to

\[
 \boxed{
 \mathscr K_{q,n}(m)=\frac{\eta_nL_n\mathfrak a_{q,n}}m.}
 \tag{2.3}
\]

Substitution in (2.2) proves (2.1).  \(\square\)

### Endpoint and quantifier ledger

- The hypothesis is \(a\le m\le n\le M\), not merely \(m\ge a\) and
  \(n\le M\).
- The endpoints \(m=a\), \(m=n\), and \(n=M\) are included.
- In particular,
  \(\mathscr K_{q,n}(n)=\eta_nL_n\mathfrak a_{q,n}/n\ne0\).
- At \(m=M\), only the term \(n=M\) remains.
- There is no \(n=2a\) temporal term and no endpoint half-weight.
- The cutoff is sharp: at \((m,n)=(a,2a)\), the index \(r=2\) becomes active,
  so (2.3) fails.
- For a nonphysical row \(q<a\), the reordered temporal sum starts at
  \(n=a\), not at \(n=q\).

Thus the current channel contains no nontrivial von Mangoldt contribution.
All terms with \(\Lambda(r)\ne0\), hence \(r\ge2\), lie in the old channel.

### Corollary 2.2 (exact old residual)

Let

\[
 E_x=\sum_{k=2}^{x}\psi(k-1)\log\frac{k}{k-1}-(x-1),
\]

and use the Cycle 49 notation \(\mathfrak j_{q,n}\) and
\(\ell_n=\sum_{d\le n}\mu(d)\log d/d\).  Subtracting (2.1) from the exact
Cycle 49 complete-prefix residual gives

\[
 \boxed{
 O_a(q)=\sum_{n=q}^{M}\frac{\alpha_{q,n}}{L_n}
 \left[
 \frac{E_{n+1}}q+\mathfrak j_{q,n}
 +\mathfrak a_{q,n}
 \bigl(1+\ell_n-\eta_nL_nm_{a-1}\bigr)
 \right].}
 \tag{2.4}
\]

This is a simplification, not a positivity or anti-cancellation theorem.

## 3. Exact source-span projection

Put

\[
 C_a=\widehat{\mathbf c}_a=B_a+H_a
\]

and

\[
 S_a=\operatorname{span}\{O_a,U_a\}
     =\operatorname{span}\{B_a,U_a\}.
\]

Define

\[
 \mathcal Q_a^{\rm src}=\|\operatorname{Proj}_{S_a}C_a\|_2^2.
 \tag{3.1}
\]

For rank-safe formulas, set

\[
 \Phi(x,d)=
 \begin{cases}
 |x|^2/d,&d>0,\\
 0,&d=0.
 \end{cases}
 \tag{3.2}
\]

If \(B_a\ne0\), define

\[
 R_a=U_a-\frac{\langle U_a,B_a\rangle}{\|B_a\|_2^2}B_a;
 \tag{3.3}
\]

if \(B_a=0\), set \(R_a=U_a\).  Then \(B_a\perp R_a\) and
\(S_a=\operatorname{span}\{B_a,R_a\}\).  Since
\(\langle R_a,B_a\rangle=0\), one has
\(\langle R_a,C_a\rangle=\langle R_a,H_a\rangle\).  Therefore

\[
 \boxed{
 \mathcal Q_a^{\rm src}
 =\Phi(\langle B_a,C_a\rangle,\|B_a\|_2^2)
 +\Phi(\langle R_a,H_a\rangle,\|R_a\|_2^2).}
 \tag{3.4}
\]

The first term is exactly the canonical Cycle 48 quantity
\(\mathcal Q_a^{\rm cp}\).  Hence

\[
 \boxed{
 \mathcal Q_a^{\rm cp}\le \mathcal Q_a^{\rm src}\le D_a(I_0).}
 \tag{3.5}
\]

The gain is one additional tail-retention contrast.  There is no reverse
comparison.  For example, in \(\mathbb R^2\),

\[
 O=e_1,\qquad U=e_2,\qquad C=e_1-e_2
\]

gives \(\mathcal Q^{\rm src}=2\), whereas \(B=e_1+e_2\) and
\(\mathcal Q^{\rm cp}=0\).

Nor can a well-conditioned source Gram force retention.  In \(\mathbb R^3\),

\[
 O=e_1,\qquad U=e_2,\qquad C=e_3
\]

has the ideal normalized source Gram \(I_2\) but
\(\mathcal Q^{\rm src}=0\).  Here one may take \(H=C-O-U\), so the exact
relation \(C=B+H\) is retained.

## 4. Why the raw determinant target is nonintrinsic

Let

\[
 G_a^{\rm src}=
 \begin{pmatrix}
 \langle O_a,O_a\rangle&\langle O_a,U_a\rangle\\
 \langle O_a,U_a\rangle&\langle U_a,U_a\rangle
 \end{pmatrix},
 \qquad
 z_a^{\rm src}=
 \binom{\langle O_a,C_a\rangle}{\langle U_a,C_a\rangle}.
 \tag{4.1}
\]

Then, with the Moore--Penrose inverse,

\[
 \mathcal Q_a^{\rm src}
 =(z_a^{\rm src})^T(G_a^{\rm src})^+z_a^{\rm src}.
 \tag{4.2}
\]

For nonzero \(O_a,U_a\), write

\[
 r=\frac{\|U_a\|}{\|O_a\|},
 \qquad
 \rho=\frac{\langle O_a,U_a\rangle}
 {\|O_a\|\|U_a\|}.
\]

Then

\[
 \boxed{
 \frac{\det G_a^{\rm src}}{(\operatorname{tr}G_a^{\rm src})^2}
 =\frac{r^2(1-\rho^2)}{(1+r^2)^2}.}
 \tag{4.3}
\]

Thus the ratio conflates angular separation with norm balance.  It changes
under independent nonzero rescalings of the two generators, although their
span and \(\mathcal Q_a^{\rm src}\) do not.  It is not an intrinsic measure
of the source plane.

More importantly, the determinant condition is redundant in the proposed
sufficient implication.  For every nonzero positive semidefinite Gram matrix,
\(z_a^{\rm src}\) lies in its range, and

\[
 \boxed{
 \mathcal Q_a^{\rm src}
 \ge\frac{\|z_a^{\rm src}\|_2^2}
 {\lambda_{\max}(G_a^{\rm src})}
 \ge\frac{\|z_a^{\rm src}\|_2^2}
 {\operatorname{tr}G_a^{\rm src}}.}
 \tag{4.4}
\]

Consequently

\[
 \|z_a^{\rm src}\|_2^2
 \gg(\log a)^{-3}\operatorname{tr}G_a^{\rm src}
 \tag{4.5}
\]

alone would imply
\(\mathcal Q_a^{\rm src}\gg(\log a)^{-3}\).  If conditions are written only
with weak inequalities, \(G=z=0\) is a rank-zero quantifier hole; one must
require \(\operatorname{tr}G>0\) or treat zero columns explicitly.

### Column-normalized replacement

Omit zero source columns.  Define

\[
 R=\begin{pmatrix}1&\rho\\ \rho&1\end{pmatrix},
 \qquad
 h=\binom{
 \langle O_a,C_a\rangle/\|O_a\|}
 {\langle U_a,C_a\rangle/\|U_a\|}.
 \tag{4.6}
\]

Then

\[
 \boxed{
 \mathcal Q_a^{\rm src}=h^TR^+h
 \ge\frac{\|h\|_2^2}{1+|\rho|}
 \ge\frac12\|h\|_2^2.}
 \tag{4.7}
\]

Hence the scale-invariant, rank-safe sufficient target is

\[
 \boxed{
 \frac{|\langle O_a,C_a\rangle|^2}{\|O_a\|_2^2}
 +\frac{|\langle U_a,C_a\rangle|^2}{\|U_a\|_2^2}
 \gg(\log a)^{-3},}
 \tag{4.8}
\]

with every zero-column summand defined as zero.  If rank-two angular
conditioning is independently wanted, the intrinsic condition is

\[
 1-\rho^2\ge\kappa,
\]

not (4.3).  It is neither necessary for (4.7) nor sufficient without a
selected correlation estimate.

## 5. Current source-gauge Volterra limit

Fix the physical parameter range \(1<C<2\), and put

\[
 \lambda=\frac{C-1}{C},\qquad L=\log a.
\]

For current source labels, write

\[
 u=\frac qa,\qquad v=\frac ma,\qquad
 R=\max(u,v),
\]

and define

\[
 A(u,s)=\frac su-\log\frac su.
 \tag{5.1}
\]

### Theorem 5.1 (current one-source Volterra kernel)

For every compact \(E\Subset[1,2)^2\), uniformly over integers
\(a\le q,m\le M\) such that \((q/a,m/a)\in E\),

\[
 \boxed{
 aL\,\mathscr V_a(q,m)
 =H_{\rm cur}(u,v)+O_{C,E}(L^{-1}+a^{-1}),}
 \tag{5.2}
\]

where

\[
 \boxed{
 H_{\rm cur}(u,v)
 =\frac{\lambda}{v}\int_R^2A(u,s)\frac{ds}{s}}
 \tag{5.3}
\]

and, equivalently,

\[
 \boxed{
 H_{\rm cur}(u,v)
 =\frac{\lambda}{v}\left[
 \frac{2-R}{u}
 -\frac12\left(
 \log^2\frac2u-\log^2\frac Ru
 \right)
 \right].}
 \tag{5.4}
\]

It is positive for \(u,v<2\).  This is the limit of the positive source
column \(\mathscr V_a\).  Since \(U_a\) has the outer sign in (1.4), the
coefficient of \(\mu(m)\) in the current contraction is
\(-\mathscr V_a(\cdot,m)\), with limit \(-H_{\rm cur}\).

#### Proof

The exact collapse (2.3) gives, for \(N=\max(q,m)\),

\[
 \mathscr V_a(q,m)
 =\frac1m\sum_{n=N}^{M}
 \alpha_{q,n}\eta_n\mathfrak a_{q,n}.
 \tag{5.5}
\]

Uniformly on the stated compact range, with \(s=n/a\),

\[
 aL\alpha_{q,n}=\frac1s+O_{C,E}(L^{-1}+a^{-1}),
 \tag{5.6}
\]

\[
 \eta_n=\lambda+O_C((aL)^{-1}),
 \tag{5.7}
\]

and

\[
 \mathfrak a_{q,n}
 =\frac su-\log\frac{s+1/a}{u}
 =A(u,s)+O_E(a^{-1}).
 \tag{5.8}
\]

Indeed, (5.6) follows directly from

\[
 A_nb_q(n)=1-w_n+A_n\frac{\log(q/n)}{L_n},
\]

\(n\log(1+1/n)=1+O(a^{-1})\), and
\(L/L_{n+1}=1+O_E(L^{-1})\).  Since \(m=av\), substituting
(5.6)--(5.8) into (5.5) gives

\[
 aL\mathscr V_a(q,m)
 =\frac1a\sum_{n=N}^{M}
 \frac{\lambda}{v}\frac{A(u,n/a)}{n/a}
 +O_{C,E}(L^{-1}+a^{-1}).
\]

The cells \([n/a,(n+1)/a]\), \(N\le n\le M\), partition \([R,2]\),
including the terminal cell \([2-1/a,2]\).  A uniform left-Riemann estimate
proves (5.2), and direct integration gives (5.4).  \(\square\)

### Volterra factorization and adjoint

For a Riemann-normalized input density \(f(v)\,dv\), the continuum operator
satisfies

\[
 \boxed{
 (T_{\rm cur}f)(u)
 =\int_1^2H_{\rm cur}(u,v)f(v)\,dv
 =\lambda\int_u^2A(u,s)
 \left[\int_1^s\frac{f(v)}v\,dv\right]\frac{ds}{s}.}
 \tag{5.9}
\]

On the output interval \(u\in[1,3/2]\), its Lebesgue adjoint is

\[
 \boxed{
 (T_{\rm cur}^*y)(v)
 =\frac{\lambda}{v}\int_v^2
 \left[
 \int_1^{\min(s,3/2)}y(u)A(u,s)\,du
 \right]\frac{ds}{s}.}
 \tag{5.10}
\]

These are continuum and Nyström identities only.  They do not justify
inserting (5.2) into the unnormalized, growing, signed sum against \(\mu(m)\).
The old and current inputs occupy disjoint source ranges.  Any claim about the
angle of the two selected output vectors needs new arithmetic control after
the Möbius contractions.

In particular, a previously explored numerical Hilbert--Schmidt cosine was
invalid: it compared the current source-gauge kernel (5.3) with the direct
collapsed-column kernel \(K_B\) of Cycle 50.  The gauges are incompatible, so
that comparison is withdrawn and is not evidence for an old/current angle.

## 6. What quantitative PNT estimates do and do not give

Let

\[
 D(x)=\exp(-c_0\sqrt{\log x}).
\]

The standard zero-free-region package supplies both

\[
 \psi(x)-x\ll xD(x)
 \qquad\text{and}\qquad
 M(x)=\sum_{n\le x}\mu(n)\ll xD(x).
 \tag{6.1}
\]

The first estimate alone does not formally imply the second; the
reciprocal-zeta estimate is a separate required input.

Partial summation, the exact formulas (2.1) and (2.4), and the uniform weight
bounds from Cycle 49 give the safe unabsorbed estimate

\[
 \boxed{
 |O_a(q)|+|U_a(q)|
 \ll L^{-1/2}e^{-c_1\sqrt L}+a^{-1}L^{-2}}
 \tag{6.2}
\]

uniformly for physical rows.  After reducing the exponential constant, this
may be written

\[
 \boxed{
 |O_a(q)|+|U_a(q)|\ll L^{-2}e^{-c\sqrt L}.}
 \tag{6.3}
\]

The reduction of \(c\) is essential when polynomial factors are absorbed.
Korobov--Vinogradov estimates only strengthen the subexponential factor.

There are \(O(a)\) physical rows, so (6.3) yields only

\[
 \|O_a\|_2^2+\|U_a\|_2^2+\|B_a\|_2^2
 \ll aL^{-4}e^{-2c\sqrt L}.
 \tag{6.4}
\]

Relative to the target \(L^{-3}\), this upper envelope has ratio

\[
 aL^{-1}e^{-2c\sqrt L}
 =\exp(L-2c\sqrt L-\log L)\longrightarrow\infty.
\]

It therefore neither proves nor obstructs the target lower bound.  Nor do
small generator norms or angular separation alone force selected retention:
for any prescribed nonzero \(O,U\), taking
\(H=-O-U+Z\) with \(Z\perp\operatorname{span}\{O,U\}\) gives
\(C=Z\) and \(\mathcal Q^{\rm src}=0\).

## 7. Reproducible finite diagnostics

The script

```text
cycle51_source_split_diagnostic.py
```

uses binary64 arithmetic and a cotangent evaluator for the restricted
Vasyunin Gram.  At \(\theta=2/5\), \(C=6/5\), and dyadic starts
\(a=32,64,128,256,512,1024\), it checks the following numerically:

- \(B_a=O_a+U_a\), with the broad script evaluating \(O_a\) through the
  exact residual formula (2.4);
- the current-source temporal and source summation orders agree;
- \(C_a=B_a+H_a\) and \(B_a=Y_a+V_a\);
- the closed Gram formula for \(\mathcal Q_a^{\rm src}\) agrees with a QR
  projection;
- both source and Cycle 47 planes contain \(B_a\), so one exact principal
  angle is zero.

The stored output is

```text
cycle51-source-split-diagnostic.out
```

The script and output SHA-256 hashes are respectively
`d59d9072e17b6ff227fbb7388ed4d91207aabc4fd1254178ee9e9b724359c5ed`
and
`e386ce06e732cdd1c9e483af6e29b1a061f6790e0285eaa7ab550c07cdf332ab`.
The script hash differs from the original broad diagnostic because the hostile
audit corrected its comment to say explicitly that the broad implementation
uses the exact residual formula (2.4), rather than independently contracting
the old source.  The executable statements and stored output are unchanged.
The output omits elapsed wall times so that it reproduces byte for byte.
It is reproduced by

```bash
python3 cycle51_source_split_diagnostic.py \
  > cycle51-source-split-diagnostic.out
```

A separate slow script

```text
cycle51_source_split_direct_check.py
```

reconstructs the old source block directly from (1.3), using finite cell
integrals rather than defining \(O_a=B_a-U_a\), for
\(a=32,64,128\).  Its maximum relative discrepancies are respectively

\[
 1.373\times10^{-14},\quad
 4.800\times10^{-15},\quad
 3.070\times10^{-14}.
\]

A second binary64 implementation independently evaluated the same old-source
finite cell convolution at all six broad-diagnostic scales.  Its maximum
absolute residuals in \(B_a-(O_a+U_a)\), for
\(a=32,64,128,256,512,1024\), were respectively

\[
 3.49\times10^{-17},\ 6.26\times10^{-17},\
 4.40\times10^{-17},\ 5.52\times10^{-17},\
 1.56\times10^{-16},\ 1.05\times10^{-16}.
\]

The scout script and its small-scale JSON output had SHA-256 hashes
`59c7a41a89f4c0eb58156b76c4b2c4d000ca64ccf3e060e3754160f517d55a8a`
and
`bd24fbeeeedce8c0cc91dd9b8c1ec238f610e7df2e23974bf18e0e33ffa52188`,
respectively.  Those floating scout files were not promoted to repository
certificates; the two replayable repository scripts in this section are the
durable artifacts.

The broad script therefore checks the old/current algebra but is not an
independent old-source reconstruction.  The separate slow script above supplies
that direct cross-check through \(a=128\).

The direct check's stored replay is

```text
cycle51-source-split-direct-check.out
```

The script and output SHA-256 hashes are respectively
`bbd21b20b9582173e4dc2cfaf81627942552b1890688fc47d8d9d65af9e1225e`
and
`25d90a036da1b4ea2f5cc6e4d51e0911453f7dbf7a9d2693240abc877e63fc24`.
This output also omits elapsed wall times and reproduces byte for byte.  Run

```bash
python3 cycle51_source_split_direct_check.py \
  > cycle51-source-split-direct-check.out
```

The broad diagnostic finds, among other finite values,

\[
\begin{array}{c|c|c|c}
 a&\det G/(\operatorname{tr}G)^2&
 \mathcal Q_a^{\rm src}/D_a&\mathcal Q_a^{\rm cp}/D_a\\ \hline
 64&2.22364\times10^{-5}&0.998965&0.998817\\
 256&4.46290\times10^{-5}&0.995157&0.995155\\
 1024&1.47225\times10^{-2}&0.997931&0.979757
\end{array}
\]

At \(a=64\), the source cosine is approximately \(-0.999095\) and the
smaller/larger norm ratio is approximately \(0.1123\).  At \(a=128\), the
norm ratio is approximately \(0.0370\), while \(1-\rho^2\approx0.307\).
These examples illustrate the two different causes of a small raw determinant
ratio: near collinearity and severe norm imbalance.

All these computations are floating diagnostics.  They are not outward
interval certificates, asymptotic counterexamples, evidence for eventual
rank, or evidence for a positive liminf.  In particular, six dyadic values do
not disprove an eventual lower bound on (4.3), and near-total relative capture
does not establish the absolute \((\log a)^{-3}\) scale.

### Additional finite prefix screen

A separate binary64 scout extended the direct complete-prefix quantities to
\(a=2048\).  It found

\[
 \|B_{2048}\|_2^2\approx1.4361899\times10^{-6},\qquad
 (\log2048)^3\|B_{2048}\|_2^2\approx6.36600\times10^{-4},
\]

\[
 \frac{\langle B_{2048},C_{2048}\rangle}{\|B_{2048}\|_2^2}
 \approx1.19237,
 \qquad
 \frac{\mathcal Q_{2048}^{\rm cp}}{D_{2048}}\approx0.984958.
\]

At \(a=32,64,128,256,512,1024,2048\), projection of the finite vector
\(B_a(q)\), over the selected physical rows, onto the sampled smooth span

\[
 \operatorname{span}\left\{1,\frac qa,\log\frac qa\right\}
\]

captured respectively approximately

\[
 99.766\%,\ 99.796\%,\ 99.637\%,\ 99.596\%,\
 96.207\%,\ 99.380\%,\ 97.311\%
\]

of \(\|B_a\|_2^2\).  Single tested arithmetic feature vectors were much more
unstable.  This suggests testing an exact projection identity and arithmetic
remainder against these three row functions as a finite next experiment.  There is at
present no arithmetic three-moment closure: every finite vector has a
tautological orthogonal projection decomposition, and smooth dependence on
\(q/a\) does not select this particular span or control its remainder.  The
sampled basis is also numerically ill-conditioned because \(\log u\) is nearly
affine on \([1,3/2]\); its design condition number ranges from about \(391\) to
\(418\) over these seven scales.  Thus the nonmonotone binary64 captures prove
no low-rank asymptotic, no small orthogonal remainder, and no retention
theorem.  A run at \(a=4096\) timed out and produced no result.

## 8. Surviving checkpoint

The source split supplies a valid fallback projection target

\[
 \boxed{\mathcal Q_a^{\rm src}\gg(\log a)^{-3},}
\]

and (4.8) is a sufficient scale-invariant formulation.  But the stronger,
intrinsic Cycle 48 checkpoint remains preferred:

\[
 \boxed{\mathcal Q_a^{\rm cp}\gg(\log a)^{-3}.}
\]

Neither is proved.  The current collapse and Volterra limit reduce the
arithmetic that a future proof must control, but they supply no anti-cancellation
for the selected Möbius phase and no retention theorem.  Any successful next
step must estimate the normalized selected correlations in (4.8), or directly
control the canonical prefix line and its tail correlation, while retaining
all Möbius signs and all endpoint terms.
