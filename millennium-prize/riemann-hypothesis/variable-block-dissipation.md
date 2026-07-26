# Exact variable-block dissipation theorem

## Exact interval specialization

Let `(P_n)_(n>=n_0)` be a nonnegative real sequence and let `(w_n)` be
nonnegative weights. Let

\[
 n_0=a_0<a_1<a_2<\cdots,
 \qquad I_j=[a_j,a_{j+1})\cap\mathbb Z,
\]

where `a_j` tends to infinity. Thus the variable-length endpoint blocks are
consecutive: they have neither gaps nor overlaps. Suppose that one constant
`kappa>0` satisfies, for every `j`,

\[
 \boxed{P_{a_j}-P_{a_{j+1}}
 \ge \kappa\sum_{n\in I_j}w_nP_n.}\tag{VB}
\]

If

\[
 \sum_{n=n_0}^{\infty}w_n=\infty,
\]

then

\[
 \boxed{\liminf_{n\to\infty}P_n=0.}
\]

No monotonicity of `P_n`, no lower bound on an individual block length, and no
positivity of an individual one-step decrement is assumed. The exact-chain
hypothesis can be replaced by the weaker abstract requirement that the
cumulative decrements have a uniform upper bound and that the effective
coefficient mass is infinite in every tail. The chain is one
directly checkable condition supplying the cumulative bound. It does not by
itself prevent repeated interior supports; the tail-mass condition handles that.

## Proof

Sum (VB) for `0<=j<J`. Consecutive endpoints telescope exactly, giving

\[
 \kappa\sum_{n=n_0}^{a_J-1}w_nP_n
 \le P_{n_0}-P_{a_J}\le P_{n_0}.\tag{1}
\]

Assume for contradiction that `liminf P_n=L>0`. Choose `epsilon` with
`0<epsilon<L`. There is an `N` such that `P_n>=epsilon` for every `n>=N`.
Since deleting finitely many terms cannot change divergence of a nonnegative
series,

\[
 \sum_{n\ge N}w_n=\infty.
\]

The left side of (1), along endpoints `a_J` tending to infinity, is therefore
at least

\[
 \kappa\epsilon\sum_{N\le n<a_J}w_n\longrightarrow\infty,
\]

contradicting its fixed upper bound `P_(n_0)`. Hence `liminf P_n=0`. QED.

For the RH lane, `P_n` is the restricted energy. The already established
finite-zero argument says that `liminf P_n=0` is sufficient for RH. The theorem
here is only an abstract implication: it does not prove (VB), weight divergence,
or RH for the arithmetic sequence.

## Why these sufficient hypotheses are present

- **Divergent total weight.** Set `P_n=1+2^(-n)`, use singleton blocks, and set
  `w_n=(P_n-P_(n+1))/P_n`. Then (VB) holds with `kappa=1`, but
  `sum w_n<1` and `liminf P_n=1`.
- **Cumulative decrement control.** Across each selected unchained block use
  the drop `2 -> 1`, then reset to `2` before the next block. Unit block weights
  can diverge while every `P_n>=1`. Exact endpoint chaining prevents this.
- **No uncontrolled repetitions.** Arbitrary repetition can manufacture
  divergent counted weight without new tail dissipation. The general theorem
  permits overlaps when total effective mass at each fixed index is finite;
  disjoint consecutive blocks are only a simple sufficient setup.
- **Escaping blocks.** Even disjointly described weight cannot force a tail
  conclusion if it is repeatedly placed on finitely many indices.
- **Nonnegative energies and weights.** They are used both in (1) and when a
  positive tail lower bound turns divergent weight into divergent weighted
  energy.

These examples are encoded with exact rational arithmetic in
`test_variable_blocks.py`.

The sharper criterion, including bounded cumulative signed errors and the fact
that full interior coverage is unnecessary, is in
`variable-block-liminf-adversarial-audit.md`.

## Exact finite verifier

`verify_variable_blocks.py` checks a finite prefix using only `Fraction`
arithmetic. It validates nonnegativity, a positive rational `kappa`, exact
adjacency of all blocks, every block inequality, and the identities

\[
 \sum_j(P_{a_j}-P_{a_{j+1}})=P_{a_0}-P_{a_J},
 \qquad
 \sum_j\sum_{n\in I_j}w_nP_n
 =\sum_{a_0\le n<a_J}w_nP_n.
\]

A finite run deliberately does not claim that `sum w_n` diverges. Existing
finite `P_N` or decrement data may be supplied after conversion to rigorous
rational enclosures or exact values; floating-point and Arb midpoint data are
rejected because they are not exact theorem certificates.

## RH normalization and adaptive renewal target

For the present approximants,

\[
h_n={1\over\log n}-{1\over\log(n+1)},
\qquad w_n=h_n\log n
={\log(1+1/n)\over\log(n+1)}
\sim{1\over n\log n}.
\]

The exact one-step identity is

\[
P_n-P_{n+1}=2h_nE_n.
\]

Hence the complete arithmetic block target on `[a,b)` is

\[
\boxed{
\sum_{a\le n<b}h_nE_n
\ge\kappa\sum_{a\le n<b}h_n(\log n)P_n.}
\]

Negative individual `E_n` are allowed. An adaptive version chooses the first
future endpoint for which this reserve inequality holds. If every stopping time
is finite, the blocks partition the tail and force zero liminf. Proving that
finiteness is itself the missing Möbius-specific renewal theorem.

Bounded block ratios are unnecessary for the implication. Gapped blocks need
summable positive endpoint resets; otherwise one-step gaps can replenish every
dissipated amount while keeping all energies bounded away from zero.
