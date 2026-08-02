# Cycle 264: exact dyadic endpoint divisor-sum functional

## Decision

`R264-NB-DYADIC` stops at its symbolic-output gate.  For the actual
logarithmically tapered Mobius coefficients, the complete `N -> 2N` endpoint
decrement is exactly equivalent to the signed divisor-sum inequality (264.9)
below.  The formula includes every physical cell, with no harmonic truncation,
tail cutoff, or omitted constant or linear term.

This is an exact reformulation, not a proof that the inequality holds.  No
finite positivity, asymptotic estimate, or Riemann-hypothesis claim is made.

## Frozen endpoint

Let

\[
 N=2^m,\qquad m\geq1,\qquad L=\log N,\qquad h=\log2,
 \qquad \alpha={h\over L+h}={1\over m+1}.
\]

For `Y` equal to `N` or `2N`, put

\[
 c_a(Y)=\begin{cases}
 \displaystyle\mu(a){\log(Y/a)\over\log Y},&a<Y,\\
 0,&a\geq Y,
 \end{cases}
 \qquad
 G_Y(t)=1+\sum_{a<Y}c_a(Y)\{t/a\}.
\tag{264.1}
\]

The restricted Nyman--Beurling energy is

\[
 P_Y=\int_1^\infty G_Y(t)^2{dt\over t^2}.
\]

Freeze the two coefficient channels

\[
 u_a=c_a(N),\qquad d_a={c_a(N)-c_a(2N)\over\alpha}
 \quad(1\leq a\leq2N).
\tag{264.2}
\]

Thus `u_a=0` for `a>=N`, while the second channel is explicitly

\[
 d_a=\begin{cases}
 0,&a=1,\\
 \displaystyle-\mu(a){\log a\over L},&2\leq a\leq N,\\
 \displaystyle-\mu(a){\log(2N/a)\over h},&N<a<2N,\\
 0,&a=2N.
 \end{cases}
\tag{264.3}
\]

Set

\[
 f(t)=1+\sum_{a\leq2N}u_a\{t/a\}=G_N(t),\qquad
 d(t)=\sum_{a\leq2N}d_a\{t/a\}.
\]

Coefficient comparison in (264.2) gives the exact identity

\[
 G_{2N}=f-\alpha d,
 \qquad
 P_N-P_{2N}=\alpha\mathcal E_N,
\tag{264.4}
\]

where the one frozen complete endpoint functional is

\[
 \boxed{\mathcal E_N=\int_1^\infty
       \bigl(2f(t)d(t)-\alpha d(t)^2\bigr){dt\over t^2}.}
\tag{264.5}
\]

## Signed divisor sums

Define the two divisor impulses and their cumulative transforms by

\[
 x_n=\sum_{\substack{a\mid n\\a\leq2N}}u_a,
 \qquad
 y_n=\sum_{\substack{a\mid n\\a\leq2N}}d_a,
 \qquad
 X_k=\sum_{n\leq k}x_n,
 \qquad Y_k=\sum_{n\leq k}y_n.
\tag{264.6}
\]

These are finite signed Mobius divisor sums.  In particular, on the complete
initial range they reduce exactly to

\[
 x_1=1,\quad y_1=0,\qquad
 x_n=y_n={\Lambda(n)\over L}\quad(2\leq n\leq N),
\tag{264.7}
\]

so `1-X_k=-psi(k)/L` and `-Y_k=-psi(k)/L` for `1<=k<=N`.
No such simplification is imposed after `N`; the truncated signed Mobius sums
in (264.6) are retained.

Put

\[
 A=\sum_{a\leq2N}{u_a\over a},\qquad
 D=\sum_{a\leq2N}{d_a\over a},\qquad
 C=2AD-\alpha D^2.
\tag{264.8}
\]

On `(k,k+1)`, divisor inversion gives
`f(t)=At+1-X_k` and `d(t)=Dt-Y_k`.  Exact integration of that affine product
therefore yields the following single symbolic inequality:

\[
\boxed{\begin{aligned}
\mathscr D_m:=\sum_{k=1}^{\infty}\Bigg[&C
+\Bigl(2D(1-X_k)-2(A-\alpha D)Y_k\Bigr)
       \log\!\left(1+{1\over k}\right)\\
&+{2(X_k-1)Y_k-\alpha Y_k^2\over k(k+1)}\Bigg]\geq0.
\end{aligned}}
\tag{264.9}
\]

The bracket in (264.9), rather than any of its three terms separately, is the
exact cell integral.  The series of grouped brackets is absolutely convergent:
`f` and `d` are bounded finite sawtooth sums, so the sum of the absolute cell
integrals is bounded by a constant times `sum_k 1/[k(k+1)]`.

The three displayed pieces retain, respectively, the constant--constant,
constant--sawtooth/linear, and signed sawtooth--sawtooth contributions.  The
cells `1<=k<2N` are the retained physical interval and the cells `k>=2N` are
the complete oscillatory tail; neither range has been discarded or enclosed by
a cutoff remainder.

Finally, (264.4) and the cell calculation prove the exact equivalence

\[
 \boxed{P_{2N}\leq P_N\quad\Longleftrightarrow\quad
        \mathcal E_N=\mathscr D_m\geq0.}
\tag{264.10}
\]

## Stop rule

Equation (264.9) is the requested exact signed divisor-sum inequality with
symbolic dyadic scale `m`.  Its difficult term remains the correlated signed
quadratic transform `2(X_k-1)Y_k-alpha Y_k^2` after the initial Chebyshev
range.  Splitting it into absolute bounds would destroy the required sign.

The scout stops here under the first-output rule.  No search over larger `N`,
no cutoff escalation, and no RH transfer is authorized or performed.
