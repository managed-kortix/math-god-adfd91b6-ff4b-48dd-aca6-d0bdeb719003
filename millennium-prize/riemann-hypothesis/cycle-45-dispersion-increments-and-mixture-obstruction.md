# Cycle 45: exact dispersion increments and a physical mixture obstruction

## Online dispersion formula

Retain the Cycle 44 notation and put

\[
h_r={1\over\log r}-{1\over\log(r+1)},\qquad
W_{M,r}=\sum_{m=M}^rw_m.
\]

The exact physical update is `F_(r+1)-F_r=h_rD_r`. If
`V_(M,B)=sum_(n=M)^B w_n||F_n-bar F_(M,B)||^2`, then adjoining endpoint `b`
gives

\[
\boxed{
V_{M,b}-V_{M,b-1}={w_b\over W_{M,b}W_{M,b-1}}
\left\|\sum_{r=M}^{b-1}W_{M,r}h_rD_r\right\|^2.}       \tag{45.1}
\]

Consequently,

\[
\boxed{
V_{M,B}=\sum_{b=M+1}^B{w_b\over W_{M,b}W_{M,b-1}}
\left\|\sum_{r=M}^{b-1}W_{M,r}h_rD_r\right\|^2.}       \tag{45.2}
\]

**Proof.** The online weighted-variance identity is

\[
V_{M,b}-V_{M,b-1}={w_bW_{M,b-1}\over W_{M,b}}
\|F_b-\bar F_{M,b-1}\|^2.
\]

Moreover,

\[
W_{M,b-1}(F_b-\bar F_{M,b-1})
=\sum_{m=M}^{b-1}w_m(F_b-F_m)
=\sum_{r=M}^{b-1}W_{M,r}h_rD_r.
\]

Substitution proves (45.1), and summing proves (45.2).

Writing `D_r=sum_(a<=r)mu(a)log(a)rho_a` makes every square in (45.2) a
finite complete restricted Vasyunin Gram contraction. Thus this formula keeps
all physical Mobius correlations and uses no infinite entrywise Gram limit.

## Why increments alone cannot dominate the anchor

The proposed terminal comparison is `V_(M,B)<=||F_M||^2`. No theorem of this
form can follow solely from the increments, their complete Gram correlations,
and Gram positivity. Indeed, translate the whole path by a fixed Hilbert vector
`v`. Every difference, every `D_r`, and the complete dispersion (45.2) remain
unchanged. Choosing `v=-F_M` makes the new anchor energy zero while leaving
positive dispersion whenever the path is nonconstant.

This is not a counterexample to the physical path: translation destroys its
distinguished affine anchor. It proves that a successful estimate must couple
the explicit physical anchor `F_M` to the future Mobius--Vasyunin increments;
an increment-only Bessel or PSD argument is insufficient.

## Positive power-mixture route falsified on the physical tail

A possible anchor coupling was a positive reciprocal-log power mixture

\[
A_n=(\log n)P_n=\int_0^\infty e^{-t y_n}\,d\nu(t),
\qquad y_n=\log\log n,\quad \nu\ge0.              \tag{45.3}
\]

Such a representation requires complete monotonicity, hence
`(-1)^k[y_(n_0),...,y_(n_k)]A>=0`. The first-order test is exactly the
singleton monotonicity already encoded by `H_n`. Even after the last certified
negative singleton `H_226`, the first genuinely new condition fails.

At 256-bit precision, complete restricted Vasyunin evaluation certifies

\[
[A_{228},A_{229}]_y
=-0.0207084899333378834337551502556680\ldots,
\]

\[
[A_{229},A_{230}]_y
=-0.111689575008181597029324481906762\ldots,
\]

and therefore

\[
\boxed{[A_{228},A_{229},A_{230}]_y
=-56.6044269708146824460293273557439\ldots<0.}   \tag{45.4}
\]

Convexity required by (45.3) has the opposite sign. Hence the actual physical
data rule out this positive-mixture geometry even on the proposed post-episode
tail beginning at `227`. This finite obstruction does not rule out a signed
measure, a later tail, or a more general non-diagonal transform.

## Reproduction and scope

Run

```text
uv run --with python-flint python verify_cycle45_tail_mixture.py
```

Equations (45.1)--(45.2) are exact identities. Equation (45.4) is a rigorous
finite Arb certificate. Neither supplies a uniform anchored dispersion bound,
an infinite-tail estimate, or an RH result.
