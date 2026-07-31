# Cycle 182: hostile audit of random-order MCSP splice packing

Let `N=2^n`, let `E=E_{n,s}` be the truth tables having fan-in-two
circuits of size at most `s`, and let `C` be a code contained in `E`. The
proposed midpoint argument has a valid restricted-model core, but it does not
give the fixed-power MMW lower bound.

## What the splice argument actually proves

Fix distinct `x,y in C`, a permutation `pi` of the `N` coordinates, and its
first half `P`. The two oriented splices are

\[
 z_{x,y}=x|_P\,y|_{\bar P},\qquad
 z_{y,x}=y|_P\,x|_{\bar P}.
\]

If either splice is outside `E`, then an exact decision algorithm must have
different midpoint states on `x` and `y`. For example, if `z_{x,y}` is hard,
the continuation `y|_{\bar P}` accepts from the state reached on `y|_P` and
rejects from the state reached on `x|_P`. The opposite orientation uses the
continuation from `x`. Thus pair-dependent orientation is harmless for exact
decision MCSP.

If `D={i:x_i != y_i}`, `d=|D|`, and `k=|P\cap D|`, then, conditional on `k`, an
oriented splice is uniform on only

\[
 \binom d k
\]

tables, not on all `2^N` truth tables. Consequently the available estimate is

\[
 \Pr[z_{x,y}\in E\mid k]\leq
 \min\left(1,{|E|\over\binom d k}\right).
\]

The same bound applies to the other orientation. In fact, failure of the
separation argument requires both orientations to be easy, so bounding either
one already suffices; there is no necessary factor-two orientation loss.
Hypergeometric concentration puts `k` near `d/2`. A union bound over all pairs
works only when

\[
 d \gg \log_2|E|+2\log_2|C|.
\]

Under that inequality, one obtains a permutation for which all codeword pairs
have distinct midpoint states, hence midpoint width at least `|C|` and space at
least `log_2|C|`.

## Flaws in the stronger claim

1. **Balance is not hardness.** Knowing only that the permutation puts about
   half of each disagreement set on either side gives no hard splice. For
   `x=0^N`, `y=1^N`, the balanced set consisting of inputs whose first bit is
   one produces, according to orientation, `z(u)=u_1` or `z(u)=not u_1`.
   Hardness comes from the
   conditional uniform distribution over balanced subsets and the displayed
   counting bound, not from balance itself.

2. **The denominator is the splice support.** A bound such as
   `|E|/2^N` is invalid for a splice unless the resulting table is uniform on
   all truth tables. It is supported on at most `binom(d,k)` tables. Small
   distance can therefore make the candidate-hard-table union bound vacuous.

3. **The packing ceiling is subpolynomial in the MMW regime.** Standard
   circuit encoding gives

   \[
   \log_2|C|\leq\log_2|E|=O(s\log(n+s)).
   \]

   At `s=2^{n/log^* n}=N^{1/log^* n}`, this is `N^{o(1)}`. Thus even an
   optimal packing of easy tables can force only `N^{o(1)}` state bits by this
   method. It cannot exclude an `N^epsilon`-space solver for any fixed
   `epsilon>0`; such a solver has much more than the forced space for all
   sufficiently large `n`.

4. **Average-order correctness does not supply one globally good cut.** The
   width proof is sound for an algorithm correct on every input and every
   order. Constant success probability over the order separately for each
   input does not imply a single permutation on which the algorithm is correct
   on all `Theta(|C|^2)` pair-dependent splices. A direct union bound would
   require error far below `1/|C|^2`, or a new distributional argument.

5. **Decision width does not transfer to relational search or update time.**
   The continuation test distinguishes YES from NO for decision MCSP. It does
   not lower-bound every valid output strategy for exact relational
   `search-MCSP^SAT`, and it imposes no fixed-power per-item update-time lower
   bound. Both transfers are required before invoking McKay--Murray--Williams.

There is a nonvacuous bounded theorem here. For suitable explicit
low-complexity codes with distance large compared with
`s log(n+s)+log|C|`, exact all-order decision MCSP has midpoint width at least
`|C|` for some, and with the quantitative union bound most, permutations. Its
space consequence is capped by `O(s log(n+s))=N^{o(1)}` in the target parameter
range. It is therefore a random-order decision/width result, not a route to
`P != NP`.

No separation is claimed.
