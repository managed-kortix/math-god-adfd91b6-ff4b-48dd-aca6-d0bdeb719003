# Cycle 182: a random-order exact OBDD lower bound for MCSP

This note records the unconditional restricted-model theorem surviving the
hostile audit.  It uses simultaneous cross-splice packing of low-degree
Reed--Muller truth tables.  It is a theorem about exact fixed-order OBDDs, not
about unrestricted circuits or `P versus NP`.

Let `N=2^n`.  Fix the fan-in-two basis `{AND,XOR,NOT}` with constants, and let
`MCSP_(n,s)` accept the truth tables computed by circuits of at most `s` gates.
For `1<=d<=n`, put

\[
K=\sum_{j=0}^d{n\choose j},\qquad W=2^{n-d},
\]

and

\[
L_{n,s}=(s+1)(n+s+2)\bigl(3(n+s+2)^2\bigr)^s.
\]

**Theorem.**  Assume `s>=dK`, and choose a uniformly random permutation `pi`
of the `N` truth-table coordinates.  With probability at least

\[
1-2^K(2^K-1)L_{n,s}(N+1)2^{-W},
\]

every exact deterministic `pi`-OBDD for `MCSP_(n,s)` has midpoint width at
least

\[
\boxed{2^K.}
\]

## Proof

The degree-at-most-`d` Reed--Muller code `RM(d,n)` has dimension `K`, size
`2^K`, and minimum distance `W`.  Every codeword is an easy MCSP input: write
its algebraic normal form as an XOR of at most `K` monomials.  Computing each
monomial and then XORing them uses at most `dK` gates.

Let `A` be the first `N/2` coordinates in the random order.  For distinct
`f,g in RM(d,n)`, define the oriented splice

\[
(f\star_Ag)|_A=f|_A,\qquad
(f\star_Ag)|_{\bar A}=g|_{\bar A}.
\]

Let `D={x:f(x)!=g(x)}` and `w=|D|>=W`.  For any fixed truth table `h`, equality
`f star_A g=h`, if possible, uniquely specifies `A cap D`.  For a prescribed
subset `R subset D`, writing `r=|R|`, the number of balanced `A` with `A cap
D=R` is exactly

\[
{N-w\choose N/2-r},
\]

with the value understood as zero when the lower index is infeasible.  In
particular it is at most `2^(N-w)`.  Since

\[
{N\choose N/2}\ge {2^N\over N+1},
\]

one has

\[
\Pr_A[f\star_Ag=h]\le(N+1)2^{-w}\le(N+1)2^{-W}.       \tag{182.1}
\]

The number of truth tables computed by circuits of size at most `s` is at most
`L_(n,s)`: enlarge every gate-input choice to `n+s+2`, use three gate types,
choose the output, and sum over `0<=t<=s`.  Union bounding (182.1) over every
easy `h` and all `2^K(2^K-1)` ordered pairs proves that, outside the displayed
failure probability, every off-diagonal splice is hard.

Fix such a good order.  For every codeword `f`, follow the prefix assignment
`f|_A` to its midpoint OBDD state.  Distinct `f,g` cannot reach the same state:
the common suffix assignment `g|_(bar A)` accepts from the state reached by
`g|_A`, because the completed table is `g`, and rejects from the state reached
by `f|_A`, because the completion is the hard splice `f star_A g`.  Thus there
are at least `2^K` midpoint states.

## Explicit parameter instance

Take `d=2`, `n>=20`, and

\[
s=\left\lfloor {N\over64n}\right\rfloor.
\]

Then `s>=2K`, `W=N/4`, and elementary bounds on `L_(n,s)` give failure
probability at most `2^(-3N/16)`.  Here are the explicit inequalities.  For
`n>=20`, both `s+1<=N` and `n+s+2<=N`, and therefore

\[
\log_2 L_{n,s}\le 2n+(2n+2)s.
\]

Also

\[
s\ge 2K,
\qquad
n^2+4n+3\le {N\over64}.
\]

The first inequality follows from
`2^n>64n(n^2+n+2)` and the second from
`2^n>=64(n^2+4n+3)`; each holds at `n=20` and is preserved when `n` is
incremented because its right-hand polynomial grows by a factor less than two.
Consequently the base-two logarithm of the failure bound is at most

\[
-{N\over4}+2K+2n+(2n+2)s+(n+1)
\le -{N\over4}+{N\over64}+{N\over32}\left(1+{1\over n}\right)
\le -{3N\over16}.
\]

Hence, with probability at least `1-2^(-3N/16)`,

\[
\boxed{
\operatorname{width}_{\pi\text{-OBDD}}(MCSP_{n,s})
\ge2^{(n^2+n+2)/2}.
}
\]

This yields an `Omega(n^2)` state-bit lower bound for most fixed orders at this
large threshold.  It strengthens a query-depth statement by forbidding residual
state merging, but it remains far below a fixed-power `N^epsilon` space lower
bound.

## Scope

The theorem does not cover the best variable order, adaptive or repeated-read
branching programs, randomized computation, random-access RAMs, unrestricted
circuits, or the exact relational `search-MCSP^SAT` problem used in known
magnification theorems.  At the MMW threshold
`s=N^(1/log^* n)`, any easy-table packing contains at most
`2^{O(s log(n+s))}` words and can force only `N^o(1)` state bits.  No
`P != NP` conclusion is claimed.
