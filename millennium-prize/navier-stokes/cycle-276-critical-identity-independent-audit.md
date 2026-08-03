# Cycle 276: independent audit of the critical excursion identity

## Verdict

Equation `(276.1)` is correct with the stated pressure convention. The
componentwise vector Laplacian makes `mathcal D` nonnegative, and the constants
`3`, `7/24`, `7/8`, `8`, and `2` are mutually consistent. Two foundational
qualifications were missing from the original formulation:

1. the strict conjecture is false as written for the zero solution (`0<0`), so
   it must exclude `X(0)=0` and handle that trivial solution separately; and
2. `(CEB)` is, via `(276.1)`, exactly the desired factor-two record-maximum
   bound, not an independently supported estimate. An experiment can be trusted
   only if it supplies a genuinely new inequality proving that budget.

The source formulation has been corrected accordingly. No experiment was run
and no regularity result is claimed.

## Identity and signs

Use

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad X=\int_{\mathbb T^3}|u|^3.
\]

Pairing with `|u|u` gives

\[
 \int |u|u\cdot\partial_tu={1\over3}X',
 \qquad
 \int |u|u\cdot(u\cdot\nabla)u
 ={1\over3}\int u\cdot\nabla|u|^3=0.
\]

For the pressure term, periodic integration by parts and incompressibility give

\[
 \int |u|u\cdot\nabla p
 =-\int p\,\nabla\cdot(|u|u)
 =-\int p\,u\cdot\nabla|u|=-\mathcal P(u).
\]

The definition is independent of the additive constant in `p`, since
`int u dot grad|u|=int div(|u|u)=0`. Finally, with `Delta` acting on each
component,

\[
\begin{aligned}
 -\int |u|u\cdot\Delta u
 &=\sum_{i,j}\int \partial_j(|u|u_i)\,\partial_j u_i\\
 &=\int |u||\nabla u|^2
   +\sum_j\int (\partial_j|u|)(u\cdot\partial_j u)\\
 &=\int |u|\bigl(|\nabla u|^2+|\nabla|u||^2\bigr)\geq0.
\end{aligned}
\]

Regularizing `|u|` by `sqrt(|u|^2+epsilon^2)` and passing to the limit justifies
the calculation at zeros. Therefore

\[
 {1\over3}X'=\mathcal P-\nu\mathcal D,
 \qquad
 X(t)-X(0)=3\int_0^t(\mathcal P-\nu\mathcal D)\,ds.
\]

## Constants and first excursion

At a record time `tau`, `(CEB)` and `(276.1)` say

\[
 X(\tau)-X(0)<\frac78X(\tau).
\]

Hence `X(tau)/8<X(0)`, so

\[
 \|u(\tau)\|_3=X(\tau)^{1/3}
 <8^{1/3}X(0)^{1/3}=2\|u(0)\|_3.
\]

Equivalently, a first time with `X(tau)=8X(0)` would make the two sides equal
and contradict the strict budget. For an arbitrary finite `T`, choose a
maximizer of continuous `X` on `[0,T]`; it is either the initial time or a
record time covered by `(CEB)`. This gives a uniform bound through the maximal
smooth interval, which is the input needed by the endpoint `L^infinity_t L^3_x`
continuation theorem.

The one-split target `int(P-nu D)<7X(tau)/24` has the right normalization,
because multiplication by the identity's factor `3` gives `7X(tau)/8`.
Replacing `<` by `<=` loses strictness but still gives `||u||_3<=2||u_0||_3`,
which remains finite and is enough for continuation.

## Trust boundary for the proposed experiment

The pressure equation and Calderon--Zygmund estimates do not by themselves
produce the budget. Any `PASS` must exhibit, with constants and inequality
directions, an estimate strictly stronger than the identity-equivalent target;
restating `(276.1)`, using the record-maximum condition alone, or numerically
observing small growth earns no evidence. Until such an inequality is proved,
the one-split proposal is an untested proof mechanism, not experimental support
for `(CEB)`.
