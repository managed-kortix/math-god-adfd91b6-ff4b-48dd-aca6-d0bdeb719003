# Cycle 44: fixed-strength boundary-envelope diagnostic

## Scope and verdict

This note tests one post--fixed-family architecture and nothing more.  Fix

\[
 \theta=\frac25
\]

on the dyadic block \([a,2a)\).  For an integer \(0\le h\le a-1\), let

\[
 \mathcal E(a,h)=
 \operatorname{span}\{p_q:a-h\le q<2a,\ \mu(q)^2=1\},
 \tag{44.1}
\]

where \(p_q\) is the exact triangular divisor column in the Cycle 43 completed
square.  The affine column is excluded.  Write

\[
 \Pi_{\rm env}(a,h)=\|\operatorname{Proj}_{\mathcal E(a,h)}X\|^2,
 \qquad
 M(a,h)=\Pi_{\rm env}(a,h)-N_{2/5}(a,2a).
 \tag{44.2}
\]

A complete restricted-Gram calculation with outward Arb arithmetic proves the
following finite facts.

1. The full current-admission span \(\mathcal E(a,0)\) fails at
   \(a=128,256,512\).
2. The natural old-boundary width \(h=\lceil a/\log a\rceil\) passes at
   \(a=128\), but fails at \(a=256,512\).
3. The exact least passing widths in this declared nested family are

   \[
   h_*(128)=19,\qquad h_*(256)=53,\qquad h_*(512)=361.
   \tag{44.3}
   \]

   Thus

   \[
   \frac{h_*(a)\log a}{a}
   =0.720223\ldots,\ 1.148025\ldots,\ 4.398506\ldots
   \tag{44.4}
   \]

   at these three scales.

The sharp rise at \(512\) falsifies the first canonical choice
\(h=\lceil a/\log a\rceil\) on two tested blocks.  These five samples are too
short and nonmonotone to support either stabilization or divergence of the
normalized width.  In particular, they do **not** prove that every fixed
multiple of \(a/\log a\) eventually fails, do not address an affine
augmentation or unrelated probes, and are not an RH result.

## 1. Exact completed-square definitions

Put

\[
 L_n=\log n,\qquad
 w_n=1-\frac{L_n}{L_{n+1}},
\]

\[
 A_n=1+\frac{L_n}{L_{n+1}}-2\theta,
 \qquad
 \eta_n=\frac{1-2\theta}{A_n},
 \qquad
 B_n=2\theta+\frac{(1-2\theta)^2}{A_n}.
\]

With

\[
 U_n=\chi+\sum_{d\le n}\mu(d)\rho_d,
 \qquad
 D_n=\sum_{d\le n}\mu(d)(\log d)\rho_d,
\]

set

\[
 Z_n=\frac{D_n}{L_n}-\eta_nU_n,
 \qquad
 X=(\sqrt{w_nA_n}\,Z_n)_{a\le n<2a}.
\]

The exact divisor column is

\[
 p_q(n)=\mathbf1_{q\le n}\sqrt{w_nA_n}\,\mu(q)
 \left(\frac{\log q}{L_n}-\eta_n\right)\rho_q.
 \tag{44.5}
\]

The completed-square identity is

\[
 P_a-P_{2a}-2\theta\sum_{a\le n<2a}w_nP_n
 =\|X\|^2-N_\theta(a,2a),
 \tag{44.6}
\]

where

\[
 N_\theta(a,2a)=
 \sum_{a\le n<2a}w_nB_n\|U_n\|^2.
 \tag{44.7}
\]

For a family \(S\), the exact probe Gram and correlation are

\[
 G_{qr}=\langle\rho_q,\rho_r\rangle
 \sum_{a\le n<2a}w_nA_n\,\phi_q(n)\phi_r(n),
 \tag{44.8}
\]

\[
 c_q=\sum_{a\le n<2a}w_nA_n\,\phi_q(n)
 \langle Z_n,\rho_q\rangle,
 \tag{44.9}
\]

with

\[
 \phi_q(n)=\mathbf1_{q\le n}\mu(q)
 \left(\frac{\log q}{L_n}-\eta_n\right).
\]

Thus

\[
 \Pi_S=c_S^TG_S^{-1}c_S
 \tag{44.10}
\]

whenever \(G_S>0\).  Here positivity is known independently because \(G_S\)
is the Gram matrix of the explicitly declared probe vectors; the computation
certifies its determinant strictly positive, hence nonsingularity, before the
Arb solve.  Determinant sign alone would not establish positive definiteness
for an arbitrary symmetric matrix.

## 2. Why the binary threshold is exact

The families are nested:

\[
 \mathcal E(a,h)\subseteq\mathcal E(a,h+1).
\]

Orthogonal projection norms are monotone under subspace inclusion, so
\(\Pi_{\rm env}(a,h)\) is nondecreasing in \(h\).  The computation uses this
fact only to choose queries.  Minimality of each reported \(h_*\) is then
proved by two independent Arb sign certificates:

\[
 M(a,h_*-1)<0<M(a,h_*).
 \tag{44.11}
\]

No floating comparison controls a verdict.  An unresolved sign, nonpositive
Gram determinant, or failed solve aborts.

## 3. Certified results

The following table uses 192-bit Arb for the complete scan.  The six delicate
threshold signs were independently reproduced at 256 bits.

| \(a\) | current rank | \(M(a,0)\) | \(\lceil a/\log a\rceil\) | its rank | its margin | \(h_*\) | threshold rank |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 32 | 19 | \(+0.007520586646847648\) | 10 | 25 | \(+0.018458815177864610\) | 0 | 19 |
| 64 | 39 | \(+0.004831445333665951\) | 16 | 47 | \(+0.005915924374207931\) | 0 | 39 |
| 128 | 79 | \(-0.001429561998886122\) | 27 | 96 | \(+0.000785196813432702\) | 19 | 90 |
| 256 | 157 | \(-0.000592668393207887\) | 47 | 187 | \(-0.000031013999404949\) | 53 | 190 |
| 512 | 310 | \(-0.002513871026176487\) | 83 | 364 | \(-0.001929911669857115\) | 361 | 532 |

The exact adjacent threshold enclosures at 256 bits are:

\[
\begin{array}{c|c|c}
a& M(a,h_*-1)&M(a,h_*)\\ \hline
128&[-6.31310179552773154055949177703021\!\times10^{-5}\ \pm1.92\!\times10^{-71}]
&[2.01383816933790689019101795329740\!\times10^{-4}\ \pm2.06\!\times10^{-71}]\\
256&[-1.73616099464593302764940546340982\!\times10^{-5}\ \pm3.99\!\times10^{-70}]
&[1.01787243191570431805486822340252\!\times10^{-5}\ \pm4.65\!\times10^{-70}]\\
512&[-1.66960916652184977763859075986806\!\times10^{-5}\ \pm4.32\!\times10^{-69}]
&[5.55217263546428688470974601919283\!\times10^{-6}\ \pm5.42\!\times10^{-69}].
\end{array}
\tag{44.12}
\]

The production JSON retains full Arb intervals, families, ranks, projections,
budgets, determinants, and both sides of each threshold.  The first two rows
have \(h_*=0\), so no predecessor certificate is needed there.

## 4. Exact consequences and nonconsequences

Because projection onto the full current span fails at \(a=128,256,512\),
every current-only cohort or selected family contained in that span also fails
on the corresponding block.  This is an exact finite no-go for those blocks,
not an asymptotic no-go: it cannot exclude a theorem asserted only for all
sufficiently large \(a\).

Likewise, at \(a=256,512\), every construction contained in the full envelope
with \(h=\lceil a/\log a\rceil\) fails.  In particular, no compression or
better choice of basis inside that exact span can repair those blocks.

The result does not exclude:

- a wider historical window;
- the affine column;
- probes outside the declared divisor span;
- non-dyadic or adaptive blocks;
- a theorem beginning beyond the tested range;
- a successful compensated inequality proved without this projection
  certificate.

The rank at the final tested threshold is \(532\), not \(O(\log a)\).
Consequently the computation does not support a low-rank cohort theorem yet.
Its next falsification gate is to extend the exact envelope threshold and test
whether a predeclared cohort basis preserves a noncollapsing fraction of the
full envelope projection.

## 5. Reproduction

From this directory:

```text
uv run --with python-flint python cycle44_boundary_envelope_scan.py \
  --starts 32 64 128 256 512 --theta 2/5 --bits 192 \
  --json cycle44-boundary-envelope-results.json
```

The independent reproducer did not reuse the production `CompensatedBlock`
assembly.  It imported only the restricted Vasyunin evaluator, Möbius sieve,
and complete-energy evaluator, rebuilt all contractions, and checked (44.6)
directly.  Its 256-bit threshold rerun agrees digit for digit with (44.12).

Artifacts:

- `cycle44_boundary_envelope_scan.py` — fail-closed production scan;
- `cycle44-boundary-envelope-results.json` — complete 192-bit certificate
  output;
- `test_cycle44_boundary_envelope_scan.py` — cache-reset, exact-family,
  monotonicity, threshold, and integer-ceiling regressions.

These are finite computational certificates and no solution claim is made.
