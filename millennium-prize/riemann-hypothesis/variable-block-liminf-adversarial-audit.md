# Variable-block dissipation: adversarial liminf audit

## 1. Abstract form

Let `(P_n)_(n>=1)` be nonnegative.  A variable-block argument normally seeks
indices

\[
 N_0<N_1<N_2<\cdots\longrightarrow\infty
\]

and nonnegative coefficients `q_(j,n)`, of finite support in the `j`th block,
such that

\[
 P_{N_j}-P_{N_{j+1}}
 \ge \sum_n q_{j,n}P_n-\epsilon_j.                 \tag{1}
\]

The coefficient `q_(j,n)` must include every factor actually present in the
proposed estimate: the decrement constant, logarithmic weight, normalization,
and any block-dependent loss.  Divergence of a nominal weight before one of
these factors is inserted has no logical force.

## 2. Weakest clean theorem

**Theorem (variable-block liminf criterion).**  Suppose (1) holds, the blocks
form an endpoint chain as displayed above, and

\[
 E_*:=\sup_{J\ge0}\sum_{j=0}^J\epsilon_j<\infty.   \tag{2}
\]

Summability of `epsilon_j^+` is a convenient sufficient condition for (2), but
is not necessary; signed errors may cancel in their prescribed block order.

Assume also that the effective coefficient measure

\[
 \nu(n):=\sum_jq_{j,n}
\]

has infinite mass in every tail:

\[
 \sum_{n\ge X}\nu(n)=\infty\qquad(X<\infty).       \tag{3}
\]

Then

\[
 \boxed{\liminf_{n\to\infty}P_n=0.}
\]

No covering assumption on the interiors of the blocks is needed.  Their
supports may have gaps, and individual decrements may be negative when the
cumulative error budget permits it.

*Proof.*  Sum (1) through block `J`.  Endpoint chaining and `P_(N_(J+1))>=0`
give

\[
 \sum_{j=0}^J\sum_nq_{j,n}P_n
 \le P_{N_0}+\sum_{j=0}^J\epsilon_j
 \le P_{N_0}+E_*.
\]

Thus `sum_n nu(n)P_n<infinity`.  If `liminf P_n=L>0`, then for some `X` one
has `P_n>=L/2` for every `n>=X`.  Condition (3) makes the weighted tail
infinite, a contradiction.  This proves the claim.

The truly minimal dissipation hypothesis is slightly more general than an
endpoint chain: for inequalities `Delta_j>=sum_n q_(j,n)P_n-epsilon_j`, it is
enough that `sup_J sum_(j<=J)(Delta_j+epsilon_j)<infinity`.  This uniform
cumulative budget, together with (3), is the abstract weakest condition used by
the proof.  Taking `Delta_j=P_(N_j)-P_(N_(j+1))` and (2) is the weakest clean,
readily checkable endpoint formulation.

For disjoint interval blocks with `q_(j,n)=kappa_j w_n 1_[N_j,N_(j+1))(n)`,
conditions (2)--(3) reduce to

\[
 \sum_j\sum_{N_j\le n<N_{j+1}}\kappa_jw_n=\infty.  \tag{4}
\]

For these escaping disjoint blocks, divergence in (4) is equivalent to (3).
It is this effective tail mass, not block count, interval coverage, or
unweighted logarithmic mass, that matters.

## 3. Audit of the existing proposed conditions

### Dyadic weighted-interior inequality

The condition

\[
 P_N-P_{2N}\ge 2\kappa\sum_{N\le n<2N}w_nP_n,
 \qquad w_n=h_n\log n,
\]

on one eventual dyadic partition is valid.  Here `epsilon_j=0`,
`q_(j,n)=2 kappa w_n`, and `sum_n w_n=infinity`.  It implies exactly
`liminf P_n=0`; it does not imply `P_n->0` or decay of the dyadic endpoints.

### Endpoint-weighted dyadic inequality

The stronger condition

\[
 P_N-P_{2N}\ge2\kappa W_NP_N
\]

does force decay along the dyadic endpoint chain because
`sum_j W_(2^jN_0)=infinity`.  This is stronger than required for the RH funnel.

### Fixed-length multiscale inequality

For fixed `L>=1`, the proposed condition

\[
 P_N-P_{2^LN}\ge
 2\kappa\sum_{r=0}^{L-1}W_{2^rN}P_{2^rN}            \tag{5}
\]

is sufficient when applied on the chain `N_j=2^(Lj)N_0`.  The sampled scales
over all blocks are every dyadic scale, and

\[
 \sum_{j,r}W_{2^{Lj+r}N_0}=\infty.
\]

Hence the theorem yields a zero liminf (indeed among the sampled dyadic
endpoints).  The word **fixed** is essential to that quick verification.  For
variable lengths, (5) remains sufficient only after checking divergence of the
actual accumulated effective weights.  If all intermediate terms in (5) are
retained, a chained partition of all dyadic scales still gives divergence; if
only one representative or endpoint weight per increasingly long block is
retained, divergence can fail.

### Complete versus restricted decrement

Every left side must be the complete endpoint difference for the same `P` that
appears in the liminf target.  Positivity or averaging of a restricted-shell
difference supplies no instance of (1) unless all omitted ranges are restored
with a one-sided, cumulatively summable error.  Boundedness or convergence of a
shell energy is not a substitute for a finite weighted sum of the complete
`P_n` values.

## 4. Counterexamples to weaker formulations

All examples use nonnegative sequences and therefore isolate logical defects,
not arithmetic ones.

### A. Bounded or convergent endpoints

Take `P_n=1`.  Every sampled subsequence is bounded and convergent, and every
zero lower bound `P_(N_j)-P_(N_(j+1))>=0` holds, but `liminf P_n=1`.  Endpoint
boundedness, endpoint convergence, and nonnegative telescoping alone do not
force a zero liminf.

### B. Positive contractions with summable strength

Let `a_j=2^(-j-2)` and set endpoint values recursively by

\[
 P_{N_{j+1}}=(1-a_j)P_{N_j},\qquad P_{N_0}=1.
\]

Fill all other values with `1`.  Then

\[
 P_{N_j}-P_{N_{j+1}}=a_jP_{N_j},
\]

but `P_(N_j)` converges to the positive product `prod_j(1-a_j)>0`, and the full
liminf is positive.  A contraction at every block is insufficient when its
effective strengths are summable.

### C. Divergent nominal weights with a summable block constant

Let every nominal block mass be `W_j=1`, let `kappa_j=2^(-j-2)`, and use the
preceding construction.  Then `sum_jW_j=infinity` but
`sum_j kappa_jW_j<infinity`, and no zero liminf follows.  Divergence must be
tested after every block-dependent constant is included.

### D. Unchained positive decrements

Set `P_(2j)=2` and `P_(2j+1)=1`.  On each pair take a coefficient of mass
`1/2` supported at `2j+1`.  Then

\[
 P_{2j}-P_{2j+1}=1\ge\tfrac12P_{2j+1},
\]

and the effective mass over all disjoint blocks diverges, yet
`liminf P_n=1`.  The drops reset between blocks.  Disjointness and divergent
mass do not replace endpoint chaining (or a uniform cumulative-decrement
bound).

### E. Reusing bounded indices

Let `P_1=0` and `P_n=1` for `n>=2`, and repeatedly put all coefficient mass at
index `1`.  The weighted right sides vanish and their formal coefficient mass
can diverge, but the tail liminf is `1`.  This is why infinite total mass must
be strengthened to infinite mass in every tail.

### F. Why the conclusion is only a liminf

For `j>=1`, let `N_j=2j`, put `P_(2j)=1` and `P_(2j+1)=0`, and support one unit
of block mass at `2j+1`.  Then

\[
 P_{2j}-P_{2j+2}=0\ge P_{2j+1}=0
\]

for every chained block, while the effective mass diverges.  The theorem gives
the correct conclusion `liminf P_n=0`, but `P_n` does not converge and the
endpoint values stay equal to `1`.  Any claim of full convergence needs extra
regularity or endpoint-weighted dissipation.

### G. Nonsummable leakage

Take `P_n=1`, one unit of effective mass in each chained block, and
`epsilon_j=1`.  Then (1) reads `0>=1-1`, but the liminf is positive.  Therefore
an error described merely as `o(1)` per block is unsafe: its positive parts
must have bounded cumulative sum (summability is a simple sufficient condition),
or be absorbed into the effective coefficient mass with a uniform favorable
remainder.

## 5. Safe statement for future use

To prove the RH-sufficient target by variable blocks, it is enough to exhibit a
chained sequence of complete endpoint differences and prove

\[
 P_{N_j}-P_{N_{j+1}}
 \ge\sum_nq_{j,n}P_n-\epsilon_j,
\]

with `q_(j,n)>=0`, a uniformly bounded-above cumulative error, and infinite
effective coefficient mass in every tail.  Summable positive
leakage is a simpler sufficient error hypothesis.  No pointwise monotonicity,
fixed block length, bounded ratio `N_(j+1)/N_j`, or full covering is required.
Conversely, none of bounded subsequences, convergent endpoints, positive but
summable contractions, divergent pre-normalization weights, unchained drops,
or restricted-shell dissipation is enough.
