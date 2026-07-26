# Exact harmonic completions and low-mode comparison

`verify_harmonic_completions.py` has two deliberately separate layers.

## Exact layer

Write `L` for a formal scale logarithm and

\[
 \Lambda_j(n)=(\mu*\log^j)(n),\qquad \Lambda_0=\epsilon.
\]

For degrees `r=0,1,2,3`, the verifier proves by rational formal-polynomial
arithmetic that

\[
 \sum_{d\mid n}\mu(d)(\log d-L)^r
 =\sum_{j=0}^r(-1)^j{r\choose j}
   (\log n-L)^{r-j}\Lambda_j(n).
\]

Formal logarithms are represented in the independent prime basis, so
`log(12)=2 log(2)+log(3)` is imposed exactly and no floating-point logarithm
enters the check. The same engine verifies both pointwise cutoff residuals

\[
 R_{r,X}(n)=\sum_{\substack{d\mid n\\d>X}}
 \mu(d)(\log d-L)^r
\]

and their cumulative floor-convolution identities

\[
 \sum_{n\le H}R_{r,X}(n)
 =\sum_{X<d\le H}\left\lfloor{H\over d}\right\rfloor
 \mu(d)(\log d-L)^r.
\]

These are exact finite algebraic identities. `verify_exact_identities` returns
only after every formal coefficient agrees.

The polynomial identities are derivatives of an exact entire Mellin
completion.  For every complex `z`,

\[
 \sum_{N<r\le2N}\mu(r)(r/N)^z
 =-\sum_{d\le N}\mu(d)(d/N)^z
 \left[
 \sum_{m\le\lfloor2N/d\rfloor}m^z
 -\sum_{m\le\lfloor N/d\rfloor}m^z
 \right].
\]

Indeed, after writing `r=dm`, the complete divisor sum is
`sum_(d|r) mu(d)=0` for every `r>N`.  Both sides are finite sums of
exponentials in `z`, so differentiation is unconditional.  In particular this
identity applies exactly at the low-mode exponents `z=-1/2+i beta_j`; only the
subsequent replacement of the discrete eigenvector by its continuum profile is
approximate.

The first derivative also identifies the precise prime-power residual if the
weight is left on the divisor instead of transported to `r=dm`:

\[
 \sum_{N<r\le2N}\mu(r)\log(r/N)
 =-\sum_{d\le N}\mu(d)
 \left(\left\lfloor{2N\over d}\right\rfloor
 -\left\lfloor{N\over d}\right\rfloor\right)\log(d/N)
 -\bigl(\psi(2N)-\psi(N)\bigr).
\]

Thus degree one cancels the von Mangoldt channel only after the full divisor
completion.  It is not a pointwise identity for the raw truncated Mobius
source.

For cumulative transforms define

\[
 Z_X(k)=\sum_{d\le X}\mu(d)\log(X/d)\left\lfloor{k\over d}\right\rfloor.
\]

Opening the floor and using
`sum_(d|m) mu(d) log(X/d)=log(X) epsilon(m)+Lambda(m)` gives

\[
 Z_X(k)=\log X+\psi(k)\qquad(k\le X).
\]

On the first endpoint block the complete tracking difference therefore has the
exact two-scale square completion

\[
 \boxed{
 \sum_{k=N}^{2N-1}{1\over k(k+1)}
 \left[
 \left(kA+1-{Z_N(k)\over\log N}\right)^2
 -\left(k(A-\alpha D)+1-{Z_{2N}(k)\over\log(2N)}\right)^2
 \right].}
\]

This absorbs every explicit prime term before squaring.  It does **not** turn
the answer into boundary terms: expanding the two `Z`-squares leaves a
difference of dense floor Gram forms at scales `N` and `2N`.

Degree two gives a sharp obstruction to extending the degree-one cancellation
with the existing prime channel alone.  If

\[
 \Lambda_2=\mu*\log^2,
\]

then the unmatched source is

\[
 \Lambda_2(n)-2\log(n)\Lambda(n).
\]

At a prime `p` this equals `-log^2 p`, so it is not identically zero.  Any
degree-two completion must retain this generalized-von-Mangoldt channel.

## Approximate layer

For the max kernel on `N<n<=2N`, the script separately computes the discrete
eigenvector projections of `mu(n) log(n/N)`. It compares those with samples of
the normalized continuum profile

\[
 x^{-1/2}\left(\cos(\beta_j\log x)
 +{\sin(\beta_j\log x)\over2\beta_j}\right),
 \qquad \tan(\beta_j\log2)=-2\beta_j.
\]

It also replaces `log(x)` times this profile by its Taylor polynomials through
degrees `0,1,2,3`, evaluating the resulting moments through the exact
convolution completions. This last replacement and the continuum-to-discrete
mode comparison are numerical approximations, not certificates and not
asymptotic claims. The reported `completion_roundoff` concerns only numerical
evaluation of an identity already certified in the exact layer.

There is also a deterministic limitation on any fixed-mode strategy.  If
`P_J` projects onto the first `J` max-kernel eigenvectors, the exact completed-
square high-mode remainder obeys

\[
 |\mathcal T_{>J}|\le\lambda_{J+1}
 \left(\|(I-P_J)(a-c)\|_2^2+\|(I-P_J)c\|_2^2\right).
\]

Since `lambda_(J+1)` is of order `J^-2` while the raw source norm is of order
`N^(1/2)`, generic bounded-source control gives only `O(N/J^2)`.  Fixed `J` is
therefore insufficient.  Taking a bounded multiple of the `(J+1)`-st
eigenvector kills the first `J` moments exactly while retaining energy of order
`N/J^2`.  A successful low-mode route needs growing `J` or an arithmetic
cumulative-sum estimate for the high-mode residual.

Run both layers with, for example,

```text
uv run --with numpy --with scipy python verify_harmonic_completions.py --N 128 --modes 3
```
