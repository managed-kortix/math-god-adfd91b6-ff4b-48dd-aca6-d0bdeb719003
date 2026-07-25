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

For every integer `Q >= 1`,

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
correlation). Expanding `g_N^2` yields the formula. QED.

### Assessment

This replaces the coefficient-`l1` error by the exact mean square, but its
relative slack is controlled by `L/Q`. Since `lcm(1,...,N)` grows
exponentially, taking `Q >> L` is unsuitable for an efficient large-`N`
certificate. The lemma is nevertheless an exact theorem and a useful audit:
it exposes that bare periodicity alone cannot supply a polynomial-cost tail
bound.

### Next queued main-funnel step

Derive a **short-block** tail estimate that does not pay the full period `L`.
The concrete target is to bound, uniformly in real `T >= Q`,

\[
\int_T^{T+H}g_N(t)^2dt
\]

for a polynomial block length `H=N^k`, by expanding the gcd kernel plus an
explicit discrepancy term for incomplete sawtooth periods. Determine whether
the discrepancy can be bounded by `O(N^A log^B N)` rather than by `L` or the
coefficient `l1` norm; simultaneously search exact small `N,T,H` values for a
counterexample to any proposed uniform discrepancy exponent.
