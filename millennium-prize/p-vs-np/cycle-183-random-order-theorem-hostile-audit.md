# Cycle 183: hostile audit of the random-order MCSP OBDD theorem

## Verdict

The counting step in Cycle 182 is valid.  If `D` is the disagreement set of
`f,g`, `w=|D|`, and a fixed table `h` can equal `f star_A g`, then `h` fixes one
specific set `R=A cap D`.  Among midpoint sets `A` of size `N/2`, the exact
number realizing that prescription is

\[
{N-w\choose N/2-|R|},
\]

with value zero when infeasible.  This is at most `2^(N-w)`.  Since the first
half of a uniform permutation is uniform among the `binom(N,N/2)` midpoint
sets,

\[
\Pr[f\star_A g=h]
=\frac{\binom{N-w}{N/2-|R|}}{\binom N{N/2}}
\le (N+1)2^{-w}.
\]

Thus the unconditional atom bound is sound.  The earlier warning that,
conditional on `|A cap D|=k`, the splice has support only `binom(w,k)` is also
sound, but it does not contradict this argument: Cycle 182 averages over all
values of `k` and bounds one prescribed atom by counting balanced midpoint
sets directly.

## Fixed-table and union-bound checks

On `D`, the two values `f(x)` and `g(x)` differ, so `h(x)` determines whether
`x` belongs to `A`.  Off `D`, the splice is forced to equal the common value of
`f` and `g`.  Hence a fixed `h` determines at most one `R`, not several.

The circuit-table count

\[
L_{n,s}=(s+1)(n+s+2)\bigl(3(n+s+2)^2\bigr)^s
\]

is a valid overcount for circuits of at most `s` gates in the stated basis.
Union bounding over at most `L_{n,s}` easy tables and all
`2^K(2^K-1)` ordered codeword pairs therefore gives the displayed theorem
bound.  Requiring every ordered off-diagonal splice to be hard is stronger than
needed for pair separation, but causes no logical error.

## Explicit `n>=20` check

For `d=2`,

\[
K={n^2+n+2\over2},\qquad W={N\over4},\qquad
s=\left\lfloor{N\over64n}\right\rfloor.
\]

For every `n>=20`,

\[
2^n>64n(n^2+n+2),
\]

so `s>=2K`.  The inequality holds at `n=20` (`1048576>540160`) and persists
by induction because the polynomial on the right grows by a factor less than
two.  Also `s+1<=N` and `n+s+2<=N`, whence

\[
\log_2 L_{n,s}\le 2n+(2n+2)s.
\]

Using `log_2(N+1)<=n+1`, the logarithm of the failure bound is at most

\[
-{N\over4}+n^2+4n+3+{N\over32}\left(1+{1\over n}\right).
\]

Finally `n^2+4n+3<=N/64` for `n>=20` (already `483<=16384` at `n=20`, with
the same induction), and

\[
{1\over64}+{1\over32}\left(1+{1\over n}\right)
\le {1\over16}.
\]

Therefore the failure probability is indeed at most `2^(-3N/16)`.

## Errors and limitations found

No fatal mathematical error was found in the theorem or its explicit
specialization.  The persisted proof did have two presentation gaps: it stated
only the coarse `2^(N-w)` count instead of the exact binomial count, and it
asserted the `n>=20` estimates without displaying them.  Cycle 182 has been
expanded to close both gaps.

The result remains only a most-fixed-orders lower bound for exact deterministic
OBDDs.  It does not cover best-order OBDDs, randomized or repeated-read
branching programs, RAM algorithms, relational search MCSP, or unrestricted
circuits, and it does not imply `P != NP`.
