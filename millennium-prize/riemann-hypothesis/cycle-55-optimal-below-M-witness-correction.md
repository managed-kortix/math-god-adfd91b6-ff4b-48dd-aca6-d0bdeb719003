# Cycle 55: correction and optimal below-`M` reserve witness

## Correction to Cycle 54

In reciprocal coordinates, for every complete cell `k<t<k+1<M`, exact Möbius
inversion gives

\[
\boxed{U_{M-1}(t)=m_{M-1}t,\qquad
D_{M-1}(t)=\ell_{M-1}t+\psi(k),}                 \tag{55.1}
\]

where

\[
m_{M-1}=\sum_{a<M}{\mu(a)\over a},\qquad
\ell_{M-1}=\sum_{a<M}{\mu(a)\log a\over a}.
\]

The slope of `U_(M-1)` is global, not cell-dependent. Every new row also
restricts to `rho_q(t)=t/q` on `(1,M)`. Therefore the complete Cycle 54 probe
span restricts to the single line spanned by `t`. The Cycle 54 rejection of the
global staircase witness was erroneous; its weaker cellwise inequality remains
true.

## Exact optimal witness

Let `Psi(t)=psi(floor t)` on `(1,M)` and define

\[
c_M={1\over M-1}\sum_{k=1}^{M-1}\psi(k)\log(1+1/k),
\]

\[
\boxed{g_M(t)=\mathbf1_{(1,M)}(t)[\Psi(t)-c_Mt].} \tag{55.2}
\]

Then `g_M` is orthogonal to `U_(M-1)` and every `rho_q`, `q>=M`. Moreover,

\[
\boxed{
\langle D_{M-1},g_M\rangle=\|g_M\|^2=W_M,}      \tag{55.3}
\]

where

\[
\boxed{
W_M=\sum_{k=1}^{M-1}{\psi(k)^2\over k(k+1)}
-{1\over M-1}\left(\sum_{k=1}^{M-1}
\psi(k)\log(1+1/k)\right)^2.}                   \tag{55.4}
\]

Riesz projection proves optimality:

\[
\boxed{
\sup_{\substack{\operatorname{supp}h\subset(1,M)\\h\perp Z}}
{|\langle D_{M-1},h\rangle|^2\over\|h\|^2}=W_M.} \tag{55.5}
\]

Thus

\[
\boxed{\|(I-\Pi_Z)D_{M-1}\|^2\ge W_M.}          \tag{55.6}
\]

No witness supported below `M` can improve this payment.

The Cycle 54 cellwise quantity is

\[
\widetilde W_M=\sum_{k<M}\psi(k)^2
[1/(k(k+1))-\log^2(1+1/k)],
\]

and the exact difference is the between-cell variance

\[
\boxed{
W_M-\widetilde W_M
=\sum_{k<M}\psi(k)^2\lambda_k^2
-{1\over M-1}\left(\sum_{k<M}\psi(k)\lambda_k\right)^2\ge0.} \tag{55.7}
\]

## Finite historical power

For the eleven delayed first-success windows, certified old-`D` reserves were
already computed in Cycle 53. Evaluating the exact finite Chebyshev expression
(55.4) shows that `A W_M` captures about `94.3%--97.6%` of those reserves. It
repairs eight of the eleven failed local projections and misses only

```text
[219,231), [220,231), [222,226).
```

At the decisive window,

\[
W_{219}=2.340708063678477\ldots,
\]

\[
A_{219,231}W_{219}=0.000785809199762998\ldots,
\]

while the required repair is

\[
0.000800940341739027\ldots.
\]

The exact shortfall is

\[
\boxed{0.000015131141976029\ldots.}               \tag{55.8}
\]

So the optimal complete below-`M` witness nearly closes the critical window but
does not prove it. The remaining reserve necessarily lives outside `(1,M)` or
in correlations not detected by below-`M` support.

## Asymptotic scope

The decomposition

\[
W_M=\widetilde W_M+
\sum_{k<M}(\psi(k)\lambda_k-\overline a_M)^2
\]

shows `W_M=o(M)` unconditionally by PNT, while the cellwise term converges to a
positive constant. PNT alone does not determine whether `W_M` remains bounded
or diverges. A zero-explicit-formula heuristic suggests logarithmic growth with
coefficient `2+gamma-log(4pi)`, but this is not a theorem used here.

For bounded window length, `A~1/(M log^3 M)`. Even logarithmic `W_M` would pay
only `1/(M log^2 M)`, one logarithm below the natural full reserve scale. The
three finite failures already show that an additional post-`M` or global
Vasyunin component is required.

This correction restores the exact optimal physical witness but proves no
additive-12 theorem or RH result.
