# Notebook

## Tick 1 — exact finite enclosure lemma

Fix integers `N >= 3` and `Q >= N`, and set `epsilon=1/Q`. Define `c_a` and
`F_N` as in `routes.md`, and

\[
A_N=\sum_{a\le N}c_a/a,\qquad M_N=1+\sum_{a\le N}|c_a|.
\]

Let the sorted breakpoint set be

\[
\mathcal B=\{1/Q,1\}\cup
\{1/(ak):1\le a\le N,\ 1\le k\le\lfloor Q/a\rfloor\}.
\]

### Lemma 1 (finite exact enclosure)

If consecutive distinct points of `B` are `l<r`, choose any rational
`m in (l,r)` and put

\[
n_a(l,r)=\lfloor1/(am)\rfloor,
\quad B_{l,r}=1-\sum_{a\le N}c_an_a(l,r).
\]

Then

\[
S_{N,Q}\le\|F_N\|_2^2\le S_{N,Q}+M_N^2/Q,
\]

where

\[
S_{N,Q}=A_N^2+\sum_{(l,r)}\left[
A_N^2(1/l-1/r)+2A_NB_{l,r}\log(r/l)+B_{l,r}^2(r-l)
\right].
\]

### Proof

Every discontinuity of `floor(1/(ax))` in `[1/Q,1]` is `1/(ak)` with
`k <= floor(Q/a)`. Hence on `(l,r)`,

\[
F_N(x)=A_N/x+B_{l,r},
\]

and direct integration gives the summand. For `x>1`, all floors vanish and
`F_N(x)=A_N/x`, whose squared integral is `A_N^2`. On `(0,1/Q)`, each
fractional part lies in `[0,1)`, so `|F_N| <= M_N`; integration gives the
stated omitted-origin bound. Endpoints have measure zero. QED.

This is an exact reduction to rational arithmetic and certified logarithms;
it is not an asymptotic theorem. The crude origin error grows with the
coefficient `l1` norm and must never be replaced by `1/Q`.

## Tick 2 — periodic tail lemma proved

After `t=1/x`, the omitted part is

\[
\int_Q^\infty |1+\sum_{a\le N}c_a\{t/a\}|^2\,dt/t^2.
\]

The numerator is periodic with period `L=lcm(1,...,N)`.

### Lemma 2 (period-average tail enclosure)

Put

\[
g_N(t)=1+\sum_{a\le N}c_a\{t/a\},\qquad
\mathcal A_N=\frac1L\int_0^L g_N(t)^2dt.
\]

For every real `Q > 0`,

\[
\boxed{
 \frac{\mathcal A_N}{Q+L}
 \le \int_Q^\infty\frac{g_N(t)^2}{t^2}dt
 \le \mathcal A_N\left(\frac1Q+\frac L{Q^2}\right).}
\]

Moreover the period average has the finite closed form

\[
\boxed{
\mathcal A_N=
\left(1+\frac12\sum_{a\le N}c_a\right)^2+
\frac1{12}\sum_{a,b\le N}c_ac_b
\frac{\gcd(a,b)^2}{ab}.}
\]

### Proof

Write `h=g_N^2`. It is nonnegative and `L`-periodic. On the block
`[Q+jL,Q+(j+1)L]`, monotonicity of `t^-2` and invariance of the integral of
`h` under a phase shift give

\[
\frac{L\mathcal A_N}{(Q+(j+1)L)^2}
\le \int_{Q+jL}^{Q+(j+1)L}\frac{h(t)}{t^2}dt
\le\frac{L\mathcal A_N}{(Q+jL)^2}.
\]

For the decreasing function `x -> (Q+Lx)^-2`, integral comparison gives

\[
\sum_{j\ge0}\frac1{(Q+(j+1)L)^2}\ge\frac1{L(Q+L)},
\]

and

\[
\sum_{j\ge0}\frac1{(Q+jL)^2}
\le\frac1{Q^2}+\frac1{LQ}.
\]

Summing proves the enclosure.

For the closed form, over any common period,

\[
\operatorname{avg}\{t/a\}=\frac12,
\quad
\operatorname{avg}\left[
(\{t/a\}-\tfrac12)(\{t/b\}-\tfrac12)
\right]=\frac{\gcd(a,b)^2}{12ab}.
\]

The second identity follows by reducing to the common period
`lcm(a,b)` and summing the elementary integrals between its integer
breakpoints (equivalently, the first periodic Bernoulli polynomial
correlation). The convention for the centered sawtooth at its jump points is
irrelevant to these integrals. Expanding `g_N^2` yields the formula. QED.

### Assessment

This replaces the coefficient-`l1` error by the exact mean square, but its
relative slack is controlled by `L/Q`. Since `lcm(1,...,N)` grows
exponentially, taking `Q >> L` is unsuitable for an efficient large-`N`
certificate. The lemma is nevertheless an exact theorem and a useful audit:
it exposes that bare periodicity alone cannot supply a polynomial-cost tail
bound.

## Tick 3 — pair-period discrepancy and strategic falsification

The queued request for merely *some* polynomial incomplete-period discrepancy
bound is too weak: pairwise expansion gives one immediately.

Put

\[
\beta_a(t)=\{t/a\}-\tfrac12,\qquad
C_N=1+\tfrac12\sum_{a\le N}c_a,
\]

so that `g_N=C_N+sum c_a beta_a` almost everywhere. For `d=(a,b)`, put

\[
\mu_{a,b}=\frac{d^2}{12ab},\qquad
L_{a,b}=\operatorname{lcm}(a,b)=\frac{ab}{d}.
\]

### Lemma 3 (elementary pair-period discrepancy)

For all real `T` and `H >= 0`,

\[
\left|\int_T^{T+H}\beta_a(t)dt\right|\le \frac a8
\]

and

\[
\left|\int_T^{T+H}
[\beta_a(t)\beta_b(t)-\mu_{a,b}]dt\right|
\le \frac{L_{a,b}}3.
\]

Consequently, if

\[
\mathcal A_N=C_N^2+\sum_{a,b\le N}c_ac_b\mu_{a,b},
\]

then

\[
\boxed{
\left|\int_T^{T+H}g_N(t)^2dt-H\mathcal A_N\right|
\le \frac{|C_N|}{4}\sum_{a\le N}a|c_a|
+\frac13\sum_{a,b\le N}|c_ac_b|L_{a,b}.}
\]

For the route coefficients `|c_a| <= 1`, this is `O(N^4)` uniformly in
`T,H`, with an absolute effective constant.

### Proof

The periodic primitive

\[
\frac a2 B_2(\{t/a\}),\qquad B_2(x)=x^2-x+\tfrac16,
\]

has derivative `beta_a` away from jumps. The oscillation of `B_2` on
`[0,1]` is `1/4`, proving the first bound. The function
`beta_a beta_b-mu_(a,b)` has period `L_(a,b)` and mean zero by Lemma 2.
Delete all complete pair periods from `[T,T+H]`. The remaining interval has
length below `L_(a,b)`, while

\[
|\beta_a\beta_b-\mu_{a,b}|\le\tfrac14+\tfrac1{12}=\tfrac13.
\]

This proves the pair bound. Expanding `g_N^2`, subtracting its mean, and
applying the triangle inequality gives the boxed estimate. Finally,
`L_(a,b)<=ab`, `|C_N|<=1+N/2`, and elementary sums give `O(N^4)`. QED.

### Strategic consequence

This proves the literal polynomial-discrepancy target but does **not** advance
the RH-strength estimate. Indeed the even simpler pointwise bound
`|g_N|<=N+1` already makes the weighted tail below `O(1/log N)` by taking a
polynomial cutoff `Q >> N^2 log N`. The hard part is the norm on the retained
range, not certification of the far tail. Pairwise absolute values erase the
Möbius cancellation.

This is a decisive falsification of the short-block route *at the strength
previously queued*. No rotation of the main RH funnel is warranted; the
bottleneck is sharpened instead.

## Tick 3 arithmetic audit — the period variance is elementary

The gcd quadratic form in `A_N` has the exact positive decomposition

\[
E_N:=\sum_{a,b\le N}c_ac_b\frac{(a,b)^2}{ab}
=\sum_{d\le N}\rho(d)
\left(\sum_{m\le N/d}\frac{c_{dm}}m\right)^2,
\quad
\rho(d)=\frac{J_2(d)}{d^2}\in(0,1].
\]

This follows from `(a,b)^2=sum_(d|a,d|b) J_2(d)` and finite rearrangement.
For the route coefficients, an absolute estimate already gives

\[
\boxed{0\le E_N\le\frac{14N}{(\log N)^2}\qquad(N\ge2).}
\]

To verify the constant, set `X=N/d`. Squareful `d` contribute zero. For
squarefree `d`, `mu(dm)=mu(d)mu(m)` when `(d,m)=1` and is zero otherwise, so

\[
\left|\sum_{m\le X}\frac{c_{dm}}m\right|
\le\frac{\log X+\frac12\log^2X}{\log N}.
\]

The summand is bounded by
`Phi(log(N/d))/log^2 N`, where
`Phi(t)=(t+t^2/2)^2`. Monotone integral comparison and `x=N exp(-t)` give

\[
\sum_{d\le N}\Phi(\log(N/d))
\le N\int_0^\infty(t^2+t^3+t^4/4)e^{-t}dt=14N.
\]

Thus neither the gcd variance nor the far tail is, by itself, the hidden
RH obstruction. At cutoff `Q=N`, however, a Fourier-tail argument does not
show that the constant mode dominates: distinct reduced frequencies can be
only `1/N^2` apart, so their products are effectively nonoscillatory on a
length-`N` scale.

## Next queued main-funnel step

Replace cutoff analysis by the known exact rational autocorrelation formula
for the complete Gram entry

\[
\langle\rho_a,\rho_b\rangle
=\int_0^\infty\{t/a\}\{t/b\}\,dt/t^2,
\]

which is expressible for rational `a/b` through finite Vasyunin cotangent
sums (Báez-Duarte--Balazard--Landreau--Saias, arXiv:math/0306251). Independently
derive and verify every normalization, then expand the route coefficients.
The next exact lemma must isolate the signed Möbius--Vasyunin bilinear sum and
state a quantitatively sufficient cancellation bound. It must not replace
that signed sum by pairwise absolute values or claim that the constant Fourier
mode dominates.

## Tick 4 — exact full Gram reduction, with truncation correction

The rational autocorrelation formula supplies a cutoff-free finite expression,
but a hostile audit found an essential domain correction that must be retained.
Set

\[
\rho_a(x)=\{1/(ax)\},\quad \chi=1_{(0,1)},\quad
C_0=\log(2\pi)-\gamma.
\]

For coprime positive integers `p,q`, use the convention

\[
V(p,q)=\sum_{k=1}^{q-1}\{kp/q\}\cot(\pi k/q),\qquad V(p,1)=0.
\]

For `d=(a,b)`, `p=a/d`, `q=b/d`, and `l=lcm(a,b)`, the published rational
autocorrelation formula and the change of variables `t=1/x` give

\[
\boxed{
\langle\rho_a,\rho_b\rangle=
\frac{(q-p)\log(p/q)+(p+q)C_0
-\pi[V(p,q)+V(q,p)]}{2l}-\frac1{ab}.}
\]

The final term is mandatory. The autocorrelation
`A(a/b)=integral_0^infty {t/a}{t/b}dt/t^2` includes `0<t<1`, where the
integrand is exactly `1/(ab)`, whereas `x in (0,1)` transforms to `t>1`.
This correction was missed in the first scout derivation and caught before
publication. Checks include

\[
\langle\rho_a,\rho_a\rangle=C_0/a-1/a^2
\]

and

\[
\langle\chi,\rho_a\rangle=(\log a+1-\gamma)/a.
\]

Primary source: Báez-Duarte--Balazard--Landreau--Saias,
arXiv:math/0306251, especially the rational formula for the multiplicative
fractional-part autocorrelation. The subtraction `-1/(ab)` is our domain
conversion, not an amendment to their formula.

### Exact route identity

Write `L=log N`,

\[
w_a=\mu(a)(L-\log a),\qquad c_a=w_a/L,
\]

and define

\[
M_0=\sum_{a\le N}w_a,\quad M_1=\sum_{a\le N}w_a/a,
\]

\[
L_0=\sum_{a\le N}w_a\log a,\quad
L_1=\sum_{a\le N}w_a\log a/a.
\]

Finally put

\[
\mathcal V_N=\frac\pi2\sum_{a,b\le N}w_aw_b\frac{(a,b)}{ab}
\left[V\left(\frac a{(a,b)},\frac b{(a,b)}\right)
+V\left(\frac b{(a,b)},\frac a{(a,b)}\right)\right].
\]

Finite expansion of the Gram form gives the exact identity

\[
\boxed{
\begin{aligned}
\|F_N\|_2^2={}&1+\frac2L[L_1+(1-\gamma)M_1]\\
&+\frac1{L^2}[C_0M_0M_1+M_0L_1-M_1L_0
-\mathcal V_N-M_1^2].
\end{aligned}}
\]

Here the elementary kernel factorizations are

\[
\sum_{a,b}w_aw_b\frac{a+b}{2ab}=M_0M_1,
\]

\[
\sum_{a,b}w_aw_b\frac{b-a}{2ab}\log(a/b)=M_0L_1-M_1L_0,
\]

and the truncation correction contributes `-M_1^2`. All sums are finite, so
no convergence interchange occurs.

Define the combined signed quantity

\[
\mathcal W_N=\mathcal V_N-M_0L_1+M_1L_0+M_1^2.
\]

Then, for any fixed `C*>0`, the desired estimate at this `N` is exactly

\[
\boxed{
\|F_N\|_2^2\le C_*/L
\iff
\mathcal W_N\ge
L^2+2L[L_1+(1-\gamma)M_1]+C_0M_0M_1-C_*L.}
\]

This is an equivalent finite reformulation, not progress on the inequality.
Cotangent reciprocity does not annihilate the symmetric Vasyunin sum, and
termwise bounds `|V(p,q)| << q log q` are far too large after absolute
summation.

## Next queued main-funnel step

Derive exact small-`N` values of `mathcal W_N` in a symbolic field generated
by logarithms, `pi`, cotangents, and `gamma`, independently checking the Gram
identity against breakpoint integration. Use the data only to test structural
decompositions. In parallel, rewrite `mathcal V_N` through Estermann values
and Bettin--Conrey reciprocity and seek a signed bilinear transform that
preserves the Möbius coefficients. The next candidate lemma must give the
displayed lower bound for `mathcal W_N` uniformly; any use of RH-level Mertens
cancellation or unqualified cotangent cancellation is circular or false.
