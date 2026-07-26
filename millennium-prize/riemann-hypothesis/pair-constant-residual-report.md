# Pair-constant left-null residual audit

The analyzer `analyze_pair_constant_residual.py` evaluates the remaining term

\[
 \|(I-P_C)(\bar c-Hx)\|_{W_-}^2
\]

in the dyadic first-block decomposition.  Here rows are indexed by
`N/2 <= k < N`,

\[
 C_{k,d}=\lfloor k/d\rfloor,\qquad
 (W_-)_{k,k}={N\over k(k+1)},
\]

and the actual affine vector uses

\[
 A=\sum_{d\leq2N}{\mu(d)\over d}
       {\log(2N/d)\over\log(2N)},
 \quad
 \bar c_k=1+A\left(2k+{k\over2k+1}\right),
\]

\[
 x_q=\mu(q){\log(2N/q)\over\log(2N)},\qquad
 H_{kq}=\left\lfloor{2k\over q}\right\rfloor
       +{k\over2k+1}{\bf1}_{q\mid2k+1}.
\]

All floor-matrix and nullspace calculations are exact over the rationals;
only `A`, `x`, the residual coordinates, and energies use 192-bit Arb balls.

## Exact left-null construction

For a general matrix `C`, the code computes a canonical RREF basis
`L=(ell_1,...,ell_s)` of `ker(C^T)`.  The weighted orthogonal complement is
spanned by `W_-^{-1} ell_i`, with exact Gram matrix

\[
 K_{ij}=\ell_i^T W_-^{-1}\ell_j.
\]

For `v=bar c-Hx`, its Arb moments and residual coordinates are

\[
 m_i=\ell_i^Tv,\qquad a=K^{-1}m,
 \qquad (I-P_C)v=W_-^{-1}La,
\]

and its weighted projection energy is independently evaluated as both
`m^T K^{-1}m` and the direct weighted norm of the reconstructed residual.
The analyzer also lists the exact support of every left-null vector, the
supports carrying certified nonzero coordinates, and the certified support of
the reconstructed residual.

## Exact full-rank theorem

The expected sparse collision correction does not occur for this coarse
matrix.  This is an all-`N` theorem, not just a finite observation.  Restrict
the columns to `N/2<=d<N`.  For row and column indices in this range,

\[
 C_{k,d}=\left\lfloor{k\over d}\right\rfloor
 =\mathbf1_{d\le k},
\]

because `k<2d`.  This square submatrix is unit lower triangular.  Therefore

\[
 \operatorname{rank}C=N/2,\qquad \ker C^T=0
\]

for every even `N`.  The finite table below is an independent implementation
check through `N=128`.

| N | rows | rank(C) | left nullity | residual energy | scaled odd diagonal |
|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 1 | 0 | 0 | 0.139561452 |
| 4 | 2 | 2 | 0 | 0 | 0.167331409 |
| 8 | 4 | 4 | 0 | 0 | 0.105472584 |
| 16 | 8 | 8 | 0 | 0 | 0.135777594 |
| 32 | 16 | 16 | 0 | 0 | 0.089908252 |
| 64 | 32 | 32 | 0 | 0 | 0.091012125 |
| 128 | 64 | 64 | 0 | 0 | 0.080296855 |

Thus the Arb coordinate tuple and every sparse-support diagnostic are empty,
and

\[
 \boxed{(I-P_C)(\bar c-Hx)=0}
\]

exactly, independently of the actual Mobius-log values.  The apparent
`collisions of truncated divisor-incidence rows` do not produce a left kernel
for the matrix used in the weighted dyadic decomposition.  They appear only if
the decisive shell columns are deleted.

For comparison, the table's final column is the same `W_-`-scaled odd
prime-power diagonal

\[
 D_N={N\over\log^2(2N)}
 \sum_{\substack{N<r<2N\\r\text{ odd}}}{\Lambda(r)^2\over r^2}.
\]

It is strictly positive in every tested shell.  In ordinary unscaled fine
weights this becomes `D_N/(2N)`, exactly the odd Schur residual

\[
 {1\over2\log^2(2N)}
 \sum_{\substack{N<r<2N\\r\text{ odd}}}{\Lambda(r)^2\over r^2}.
\]

Consequently the pair-constant affine residual neither cancels nor reinforces
the odd diagonal: it vanishes.  The full affine odd residual still contains
the nonzero jump square with `A-Lambda(r)/log(2N)`; this audit does not remove
that term or establish contraction.

Indeed the complete affine odd residual now reduces exactly to

\[
 \boxed{\mathcal R_{\rm odd}
 =\sum_{k=N/2}^{N-1}{N\over(2k+1)^2}
 \left(A-{\Lambda(2k+1)\over\log(2N)}\right)^2.}
\]

The next comparison must therefore keep this full affine prime square together
with the effective embedded-coarse energy.  No left-null correction remains.

## Reproduction

```sh
uv run --with python-flint python analyze_pair_constant_residual.py
uv run --with python-flint python -m unittest -v test_pair_constant_residual.py
```
