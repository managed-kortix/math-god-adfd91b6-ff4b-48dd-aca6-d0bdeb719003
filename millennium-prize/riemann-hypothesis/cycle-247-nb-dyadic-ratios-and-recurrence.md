# Cycle 247: dyadic Nyman--Beurling ratios and exact recurrence

## Decision

For the Cycle 242 logarithmic approximants, a directed scan was made on the
single ray

\[
 N=3\,2^j,\qquad 0\leq j\leq 8.
\]

The first five ratios are below `3/4`, but the next four are above `3/4`.
Thus the `N=3` instance of NB242 is a small-scale event: its frozen contraction
does not persist even through this finite prefix. This is finite information
only. It proves no eventual behavior and no RH statement.

## Directed finite scan

The complete restricted Vasyunin formula was evaluated at 192-bit Arb
precision through `N=1536`. Each interval below is an outward rounding of the
stored exact dyadic rational certificate endpoints, not an error estimate from
binary floating-point arithmetic.

| `j` | `N` | directed interval for `P_(2N)/P_N` | versus `3/4` |
|---:|---:|:---|:---|
| 0 | 3 | `[0.486572104416097848, 0.486572104416097849]` | `<` |
| 1 | 6 | `[0.574231923727544675, 0.574231923727544676]` | `<` |
| 2 | 12 | `[0.615248202386648798, 0.615248202386648799]` | `<` |
| 3 | 24 | `[0.686710782390435096, 0.686710782390435097]` | `<` |
| 4 | 48 | `[0.725342800727233247, 0.725342800727233248]` | `<` |
| 5 | 96 | `[0.764994895070322653, 0.764994895070322654]` | `>` |
| 6 | 192 | `[0.788824354105060973, 0.788824354105060974]` | `>` |
| 7 | 384 | `[0.807899116662782590, 0.807899116662782591]` | `>` |
| 8 | 768 | `[0.834777224168894026, 0.834777224168894027]` | `>` |

Exact rational cross multiplication proves every displayed threshold verdict.
It also proves that these nine intervals are strictly increasing. Neither fact
may be extrapolated beyond `N=768`.

## Exact dyadic recurrence

Write `rho_a(x)={1/(ax)}`, `L=log N`, `h=log 2`, and

\[
 \alpha_N={L\over L+h},\qquad \beta_N={h\over L+h}=1-\alpha_N.
\]

Since the coefficient at the endpoint is zero, define

\[
 Q_N=\chi+\sum_{a<N}\mu(a)\rho_a,
 \qquad
 S_N=\sum_{N\leq a<2N}\mu(a)
       \left(1- {\log a\over\log(2N)}\right)\rho_a.
\]

For every old index `a<N`, direct coefficient comparison gives

\[
 \mu(a)\left(1-{\log a\over\log(2N)}\right)
 =\alpha_N c_a(N)+\beta_N\mu(a).
\]

Consequently the approximants satisfy the exact Hilbert-space recurrence

\[
 \boxed{F_{2N}=\alpha_NF_N+R_N,\qquad
 R_N=\beta_NQ_N+S_N.}                              \tag{247.1}
\]

Putting

\[
 C_N=\langle F_N,R_N\rangle,\qquad B_N=\|R_N\|_2^2,
\]

gives the exact scalar recurrence

\[
 \boxed{P_{2N}=\alpha_N^2P_N+2\alpha_NC_N+B_N.}     \tag{247.2}
\]

This isolates the analytic issue more sharply than the raw dense Gram formula:
the new dyadic block and the coefficient retapering are both contained in
`R_N`, while the signed old/new interaction is the single scalar `C_N`.

## Inequality target

For any fixed `q`, (247.2) makes dyadic contraction equivalent to

\[
 \boxed{C_N\leq
 {\bigl(q-\alpha_N^2\bigr)P_N-B_N\over2\alpha_N}.}   \tag{247.3}
\]

Thus a proof cannot discard the off-diagonal interaction or replace it by an
unsigned estimate. Cauchy--Schwarz alone yields only

\[
 \left(\max\{0,\alpha_N\sqrt{P_N}-\sqrt{B_N}\}\right)^2
 \leq P_{2N}\leq
 \left(\alpha_N\sqrt{P_N}+\sqrt{B_N}\right)^2,       \tag{247.4}
\]

which has no forced contraction sign.

For `q=3/4`, the coefficient `alpha_N^2` itself exceeds `q` once

\[
 \log N>{\sqrt{3/4}\over1-\sqrt{3/4}}\log 2,
\]

in particular at `N=96`. Beyond that elementary crossover, (247.3) demands a
quantitatively negative correlation large enough to overcome both
`(alpha_N^2-q)P_N` and the nonnegative `B_N`. The directed scan says this demand
already fails at `N=96` on the chosen ray. It does not show that every fixed
`q<1` eventually fails, because that would require an asymptotic theorem not
proved here.

## Verification

`cycle247-nb-dyadic-certificate.json` stores directed rational intervals for
every `P_N`, `P_(2N)`, and ratio. The verifier recomputes all complete energies
through `1536`, checks enclosure, and decides comparison with `3/4` using exact
`Fraction` arithmetic.

```text
uv run --with python-flint python verify_cycle247_nb_dyadic.py
uv run --with python-flint python -m unittest -v test_cycle247_nb_dyadic.py
```

No cofinal contraction and no Riemann-hypothesis result is claimed.
