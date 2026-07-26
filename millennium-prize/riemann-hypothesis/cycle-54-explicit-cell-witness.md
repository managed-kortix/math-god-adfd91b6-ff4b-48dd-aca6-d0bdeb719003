# Cycle 54: cellwise reserve witnesses (superseded optimization)

> **Cycle 55 correction.** The cellwise bound below is valid, but it is not
> optimal. The claim below that the larger global staircase witness is invalid
> is false: on every complete cell below `M`, Möbius inversion makes
> `U_(M-1)(t)=m_(M-1)t` with one global slope. Therefore the global witness is
> orthogonal to the full probe span and captures roughly 94--98% of the
> historical reserve. See `cycle-55-optimal-below-M-witness-correction.md`.

## Exact cell witnesses

Work in reciprocal coordinates with measure `dt/t^2`. Fix
`M<B<=M+12`, and put

\[
Z=\operatorname{span}\{U_{M-1},\rho_M,\ldots,\rho_{B-1}\},
\qquad D=D_{M-1}.
\]

On a complete cell `k<t<k+1<M`, the old vectors have the forms

\[
U_{M-1}(t)=u_k t,
\qquad D_{M-1}(t)=d_k t+\psi(k),                  \tag{54.1}
\]

while every new row satisfies `rho_q(t)=t/q`. Define

\[
\lambda_k=\log(1+1/k),\qquad
\tau_k={1\over k(k+1)},
\]

and

\[
h_k(t)=\psi(k)(1-\lambda_kt)\mathbf1_{(k,k+1)}(t).
\]

Direct integration gives

\[
\langle h_k,t\rangle=0,
\]

so `h_k` is orthogonal to `U_(M-1)` and every new row globally. Moreover,

\[
\boxed{
\|h_k\|^2=\langle D,h_k\rangle
=\psi(k)^2(\tau_k-\lambda_k^2).}                 \tag{54.2}
\]

The supports are disjoint. Bessel's inequality therefore yields the explicit
full-span lower bound

\[
\boxed{
\|(I-\Pi_Z)D_{M-1}\|^2\ge
\widetilde W_M:=\sum_{k=1}^{M-1}\psi(k)^2
\left[{1\over k(k+1)}-\log^2(1+1/k)\right].}     \tag{54.3}
\]

This genuinely escapes the generic Hilbert no-go by using the exact physical
rank-one behavior of all probes on cells below `M`.

The `k=1` term vanishes. For every `M>=3`, the `k=2` term gives

\[
\boxed{
\widetilde W_M\ge(\log2)^2
\left({1\over6}-\log^2{3\over2}\right)
=0.0010880880776877185\ldots.}                   \tag{54.4}
\]

There is no factor `1/2` in this contribution.

## Superseded claim: the larger global variance

It is tempting to project the complete staircase `psi(floor t)` on `(1,M)`
away from one global copy of `t`, obtaining

\[
W_M=\sum_{k<M}{\psi(k)^2\over k(k+1)}
-{1\over M-1}\left(\sum_{k<M}\psi(k)\lambda_k\right)^2.
\]

Cycle 55 found that this paragraph's conclusion is false. The coefficient in
`U_(M-1)` does **not** vary from cell to cell: the floor contribution cancels
identically. The difference below is the valid nonnegative between-cell
variance captured by the optimal global witness:

\[
W_M-\widetilde W_M
=\sum_{k<M}\psi(k)^2\lambda_k^2
-{1\over M-1}\left(\sum_{k<M}\psi(k)\lambda_k\right)^2.
\]

Thus (54.3) remains valid, but is unnecessarily weak.

## Scale and finite payment

The cellwise sum increases to a finite positive constant:

\[
\widetilde W_M\nearrow\widetilde W_\infty\in(0,\infty),
\]

because

\[
{1\over k(k+1)}-\log^2(1+1/k)
={1\over12k^4}+O(k^{-5}),
\qquad \psi(k)\sim k.
\]

For a bounded-length window,

\[
A=\sum_{n=M}^{B-1}\beta_n\asymp{B-M\over M\log^3M},
\]

so the explicit payment `A tilde W_M` has size `1/(M log^3 M)`. The full
old-`D` reserve can be of the natural larger scale `1/(M log M)`; the explicit
cell witnesses capture only a small component.

At the eleven historical delayed windows, the certified payment fractions of
the actual old-`D` reserve are approximately `0.00639` to `0.00845`. The witness
repairs none of the Cycle 52 negative projection bounds. At `[219,231)`,

\[
A\widetilde W_{219}=0.0000051564961389\ldots,
\]

whereas the needed repair is

\[
0.0008009403417390\ldots.
\]

Hence the cellwise witnesses are rigorous but quantitatively weak. Cycle 55
restores the between-cell component with an exact globally orthogonal witness.

## Scope

Compact support alone gives no coercivity: functions with both affine cell
moments zero are orthogonal to the entire fractional-part dictionary and hence
to `D` as well. The useful witnesses work because they remove only the common
linear profile while retaining the Chebyshev staircase. The unit lower-
triangular floor block also prevents a nonzero detectable witness built from
only twelve generic post-`M` cell masses against twelve new rows.

Thus (54.3) is an exact non-tautological physical reserve bound, but it neither
pays the projected deficit nor proves additive-12 recovery. No RH result is
claimed.
