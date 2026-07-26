# Generic cross-scale source counterexamples

This audit replaces the arithmetic coefficients by arbitrary bounded effective
source vectors.  It therefore tests only identities or inequalities claimed to
follow from the floor geometry.  It says nothing adverse about a statement
that uses the particular Mobius vector.

For `k=N,...,2N-1`, put

\[
 w_k={1\over k(k+1)},\qquad
 (F_Nx)_k=\sum_d x_d\left\lfloor{k\over d}\right\rfloor,
 \qquad \langle u,v\rangle_w=\sum_kw_ku_kv_k.
\]

For one bounded source `a=(a_d)`, define the normalized transform

\[
 \widehat Z_X^a(k)={1\over\log X}\sum_{d\le X}
 a_d\log(X/d)\left\lfloor{k\over d}\right\rfloor.
\]

Replacing `mu(d)` by `a_d` in the exact completed square gives

\[
 \sum_{k=N}^{2N-1}w_k\left[
 \left(kA+1-\widehat Z_N^a(k)\right)^2-
 \left(k(A-\alpha D)+1-\widehat Z_{2N}^a(k)\right)^2
 \right].
\]

This is the requested arbitrary-source version; the arithmetic identity
`Z_X=log X+psi` is, of course, special to the Mobius source and is not asserted
for general `a`.

The counterexample below uses only the rational normalized tapers at `d=1`
and, for `N=2`, `d=2`.  No logarithmic approximation is involved.

Suppose an old transform is `b` and the newly available source gives increment
`c`.  The homogeneous part of the two-scale completed-square difference is

\[
 Q(b,c)=\|b\|_w^2-\|b+c\|_w^2
       =-2\langle b,c\rangle_w-\|c\|_w^2.
\]

Consequently neither positivity of the two individual Gram forms nor square
completion gives a sign, a Loewner order, a contraction, or martingale
orthogonality.  Affine deterministic centers do not change this obstruction:
the same quadratic form is obtained on differences of sources.

## Minimal half-open certificate

The normalized formula requires `N>=2`, so `N=2` is the smallest admissible
scale.  Take source support `{1,2}`.  The `d=1` column has normalized taper one
at both scales.  The `d=2` column has taper zero at scale `2` and taper
`log(4/2)/log(4)=1/2` at scale `4`.  On `k=2,3`, the old column `b` and the
cross-scale increment `c` are

\[
 w=(1/6,1/12),\qquad b=(2,3),\qquad c=(1/2,1/2).
\]

Their exact Gram data are

\[
 \|b\|_w^2={17\over12},\qquad
 \langle b,c\rangle_w={7\over24},\qquad
 \|c\|_w^2={1\over16}.
\]

After padding the old form by a zero fresh coordinate, its difference from the
fine form on the coefficient coordinates `(old,fresh)` is

\[
 K_{\rm old}-K_{\rm fine}=
 \begin{pmatrix}0&-7/24\\-7/24&-1/16\end{pmatrix},
 \qquad \det=-{49\over576}<0.
\]

This single matrix supplies all requested certificates:

* Cross-scale sign and Loewner order: source `(1,1)` gives `-31/48`, while
  source `(1,-1)` gives `25/48`.  Hence the difference is indefinite.
* Contraction: the coarse norm is `17/12`.  The fine norms for `(1,1)` and
  `(1,-1)` are respectively `33/16` and `43/48`, so neither direction of norm
  monotonicity is generic.  The squared-norm ratios are `99/68` and `43/68`.
* Martingale orthogonality: the old/increment inner product is `7/24`, not zero.

Thus `N=2` is minimal.  The source certificate vectors `(1,1)` and `(1,-1)`
have entries in `{-1,1}` and obey the unit source bound.

Run the independent exact check with

```text
python search_cross_scale_sources.py
```
