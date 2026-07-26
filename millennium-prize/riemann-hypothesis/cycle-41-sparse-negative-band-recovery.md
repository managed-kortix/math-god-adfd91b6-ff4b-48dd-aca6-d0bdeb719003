# Cycle 41: sparse negative bands, finite recovery, and divergent mass

## Abstract

Let

\[
 L_n=\log n,\qquad
 w_n={\log(1+1/n)\over L_{n+1}},\qquad
 \beta_n={\log(1+1/n)\over L_nL_{n+1}^2},
\]

and let `H_n` be the Cycle 40 norm defect. The exact half-strength residual is

\[
 \mathcal R(a,b):=P_a-P_b-\sum_{a\le n<b}w_nP_n
 =\sum_{a\le n<b}\beta_nH_n.                         \tag{41.1}
\]

This note gives a deterministic sufficient condition that permits `H_n<0` on
sparse finite bands. Each negative band must be followed, before the next
negative band, by enough positive unweighted `H`-mass to pay its entire debt
after allowing for the decrease of `beta`. This gives a finite recovery from
every starting index. Iterating the first recoveries produces consecutive
blocks, retains every interior `w_n`, and therefore has divergent effective
mass. The condition is sharp at the level of aggregate band data: sparse signs
or unweighted compensation alone do not suffice when the compensation is moved
to a scale on which `beta` is much smaller. A limiting compensation whose
weighted sum approaches zero from below also does not give a finite stop.

No estimate proved here establishes the hypotheses for the Mobius norm defects.

## 1. Exact and aggregate recovery criteria

Write `x_n=beta_n H_n`. A negative band is an integer interval

\[
 I_j=[p_j,q_j),\qquad
 2\le p_j<q_j\le r_j<p_{j+1},                           \tag{41.2}
\]

such that `H_n>=0` outside the union of the `I_j`. The interval
`J_j=[q_j,r_j)` is its proposed recovery window. Empty gaps and empty recovery
windows are allowed only when the band debt is zero.

For `a in I_j`, define the weighted suffix debt and recovery gain

\[
 D_j(a)=\sum_{a\le n<q_j}\beta_nH_n^-,\qquad
 G_j(t)=\sum_{q_j\le n<t}\beta_nH_n^+,
 \quad q_j\le t\le r_j.                                \tag{41.3}
\]

Here `y^+=max(y,0)` and `y^-=max(-y,0)`.

**Theorem 41.1 (finite band recovery).** Suppose `beta_n>0`. If, for every
`j` and every `a in I_j`, there is a finite `t=t(j,a)<=r_j` for which

\[
 G_j(t)\ge D_j(a),                                      \tag{41.4}
\]

then every start `a>=2` has a finite half-strength recovery block. More
precisely, one may take `b=a+1` when `H_a>=0`, and `b=t(j,a)` when
`a in I_j`.

*Proof.* If `H_a>=0`, (41.1) gives
`R(a,a+1)=beta_aH_a>=0`. If `a in I_j`, there is no negative index between
`q_j` and `t`, and hence, after retaining any favorable terms inside the band,

\[
 \mathcal R(a,t)
 \ge-D_j(a)+G_j(t)\ge0.
\]

This is a finite recovery block. The alternatives cover every index. QED.

Condition (41.4) is a direct deterministic suffix condition for a recovery
restricted to the prescribed negative-free window. It is also necessary when
the band itself has no favorable terms and the recovery endpoint is fixed at
the first crossing. A simpler condition loses the suffix information:

\[
 \boxed{\sum_{q_j\le n<r_j}\beta_nH_n^+
 \ge \sum_{p_j\le n<q_j}\beta_nH_n^-.}                 \tag{41.5}
\]

It implies (41.4) with `t=r_j`, because every suffix debt is at most the full
band debt. Among assertions using only the two aggregate weighted masses in
(41.5), this condition is sharp: if the left side is smaller, a band whose
negative mass is concentrated at its last index has no recovery by `r_j`.

## 2. A checkable unweighted theorem with beta distortion

Assume now that `beta_n` is nonincreasing. Set

\[
 d_j=\sum_{p_j\le n<q_j}H_n^-,\qquad
 g_j=\sum_{q_j\le n<r_j}H_n^+,
 \qquad K_j={\beta_{p_j}\over\beta_{r_j-1}}.            \tag{41.6}
\]

**Corollary 41.2 (band balance after decay).** Under (41.2), every start has a
finite recovery if

\[
 \boxed{g_j\ge K_jd_j\qquad\text{for every }j.}          \tag{41.7}
\]

*Proof.* Monotonicity gives

\[
 \sum_{I_j}\beta_nH_n^-
 \le\beta_{p_j}d_j,
 \qquad
 \sum_{J_j}\beta_nH_n^+
 \ge\beta_{r_j-1}g_j.
\]

Thus (41.7) implies (41.5), and Theorem 41.1 applies. QED.

The factor `K_j` cannot be replaced uniformly by a smaller factor if only
monotonicity and the endpoint locations are known: place all negative mass at
`p_j` and all positive mass at `r_j-1`. The resulting weighted balance is
exactly `beta_(r_j-1)g_j>=beta_(p_j)d_j`.

For the physical weight, elementary logarithmic bounds make (41.7) explicit.
Since

\[
 {1\over n+1}\le\log(1+1/n)\le {1\over n},             \tag{41.8}
\]

for `2<=p<=m` one has

\[
 \boxed{{\beta_p\over\beta_m}
 \le {m+1\over p}
 {\log m\over\log p}
 \left({\log(m+1)\over\log(p+1)}\right)^2.}             \tag{41.9}
\]

Consequently, if `r_j<=C p_j` for one fixed `C`, then `K_j` is bounded by a
constant depending only on `C` after deletion of finitely many bands. Thus a
uniform aggregate gain `g_j>=K d_j`, with `K` larger than that constant,
guarantees all recoveries. More sharply, if `(r_j-p_j)/p_j->0`, then
`K_j=1+o(1)`. In contrast, no bounded gain/debt ratio can compensate a recovery
window moved to scales `r_j/p_j->infinity`, because

\[
 \beta_n\asymp {1\over n(\log n)^3}.                    \tag{41.10}
\]

The bands need not have bounded width and their gaps need not satisfy a density
condition. What matters for finite stopping is finite weighted debt, payment
before the next band, and the beta distortion across that payment interval.
Calling the bands sparse without these quantitative clauses has no force.

## 3. Consecutive recovery implies divergent mass

Let `tau(a)` be the first `b>a` with `R(a,b)>=0`, whose finiteness follows from
Theorem 41.1. Starting at any `a_0`, define `a_(k+1)=tau(a_k)`. These blocks are
finite, consecutive, and cover the integer tail. Since the arithmetic energies
`P_n` are nonnegative, equation (41.1) gives

\[
 P_{a_k}-P_{a_{k+1}}
 \ge\sum_{a_k\le n<a_{k+1}}w_nP_n.                     \tag{41.11}
\]

Summing through block `K` yields

\[
 \sum_{a_0\le n<a_K}w_nP_n\le P_{a_0}.                 \tag{41.12}
\]

The retained coefficient mass is exactly, with no overlap or omission,

\[
 \sum_k\sum_{a_k\le n<a_{k+1}}w_n
 =\sum_{n\ge a_0}w_n=\infty,                            \tag{41.13}
\]

because `w_n>=1/((n+1)log(n+1))`. Hence a positive tail lower bound for `P_n`
would contradict (41.12), and

\[
 \boxed{\liminf_{n\to\infty}P_n=0.}                    \tag{41.14}
\]

This conclusion does not require a bound on recovery lengths. Sparsity is used
only to isolate a negative band from its positive payment window; divergence
comes from retaining every integer between consecutive stopping endpoints.

For lossy block inequalities

\[
 P_{a_k}-P_{a_{k+1}}
 \ge c_k\sum_{a_k\le n<a_{k+1}}w_nP_n,
 \qquad 0\le c_k\le1,                                  \tag{41.15}
\]

the exact abstract threshold is

\[
 \boxed{\sum_k c_kW_k=\infty,
 \qquad W_k=\sum_{a_k\le n<a_{k+1}}w_n.}                \tag{41.16}
\]

It is sufficient by the same positive-lower-bound contradiction and sharp for
the renewal mechanism: if the series converges, the recursion
`p_(k+1)=p_k(1-c_kW_k)` (after deleting finitely many terms so that
`c_kW_k<1`) has a positive limit and satisfies the block inequality with
equality for a block-constant model. Full band recovery has `c_k=1`, so
(41.16) follows automatically from (41.13).

## 4. Counterexamples delimiting the theorem

### 4.1 Sparse signs do not defeat beta decay

Let `p_j<r_j<p_(j+1)` grow so fast that `beta_(r_j)<=beta_(p_j)/4`, and set

\[
 H_{p_j}=-1,\qquad H_{r_j}=2,
\]

with `H_n=0` elsewhere. The negative bands are isolated singletons and each has
twice as much later unweighted positive mass. Nevertheless, after the `j`th
pair its weighted contribution is at most

\[
 -\beta_{p_j}+2\beta_{r_j}\le-\tfrac12\beta_{p_j}<0.
\]

Choose the pairs recursively so that all still later positive weighted mass is
less than `beta_(p_j)/4`. Then the start `p_j` never recovers. Thus arbitrarily
sparse negative bands and favorable unweighted balance do not replace (41.7).

### 4.2 A zero limit is not a finite stop

Fix a start `p`, put `x_p=-1`, and choose positive `x_n` for `n>p` with
`sum_(n>p)x_n=1` but every finite partial sum strictly below `1`. Setting
`H_n=x_n/beta_n` gives

\[
 \sum_{p\le n<m}\beta_nH_n<0\quad\text{for every finite }m,
 \qquad
 \lim_{m\to\infty}\sum_{p\le n<m}\beta_nH_n=0.
\]

The weighted debt is paid only at infinity, so no finite recovery exists. This
is the attained-zero obstruction from Cycle 40 in band language.

### 4.3 Sparse successful blocks need not carry divergent mass

Let `N_j=2^{2^j}` and retain only the isolated dyadic blocks `[N_j,2N_j)`.
Their masses satisfy

\[
 \sum_{N_j\le n<2N_j}w_n\ll {1\over\log N_j}\asymp2^{-j},
\]

so their total mass is finite. Even perfect residual positivity on all these
blocks cannot force zero liminf by the renewal telescope. The missing point is
not their sign but their failure to form a consecutive tail. Theorem 41.1
avoids this loss by proving a stop from every start and then iterating stops.

## 5. Arithmetic estimates still needed

The deterministic theorem reduces a Mobius proof to the following estimates.

1. **Band localization.** Prove that the negative set of the complete defect
   `H_n` is contained in disjoint finite intervals `I_j`. Finite computation
   through a cutoff does not give this asymptotic assertion.
2. **Complete debt bound.** Bound `d_j=sum_(I_j)H_n^-`, or preferably the exact
   weighted debt `sum_(I_j)beta_nH_n^-`. The Vasyunin diagonal alone is not a
   valid proxy because its off-diagonal cancellation is of the same scale.
3. **Nearby positive gain.** Produce `r_j<p_(j+1)` and a lower bound for the
   complete gain on `[q_j,r_j)`. A useful theorem must control `r_j/p_j` or pay
   the explicit distortion (41.9).
4. **Tail cells.** In the divisor-floor expansion of `H_n`, Chebyshev
   simplification is exact only for cells `k<=n`. The cells `k>n` need a
   one-sided cumulative bound at the band scale.
5. **Compensated correlation.** Estimate the polarized full expression
   `<D_n-R_nU_n,D_n+R_nU_n>` or an exact block sum of it. Separate norm,
   diagonal, or averaged-factor estimates need an error small enough to
   preserve (41.5).
6. **Finite attainment.** A limsup or asymptotic equality is insufficient at
   zero. The estimate must exhibit a finite `r_j`, or give a strict positive
   weighted margin that forces a finite crossing.
7. **Mass bookkeeping.** If the arithmetic argument proves only selected or
   lossy blocks, verify coverage and (41.16) after all losses. Nominal
   divergence of `sum w_n` cannot be used after sparse sampling.

There are three concrete routes to items 1--5, already exposed by the exact
Cycle 41 formulas.

- **Event recurrence.** At nonsquarefree `n+1`, the one-step formula produces
  a pure negative scale drift. At squarefree events, one must control the signed
  contraction
  `L_(n+1)<D_n,rho_(n+1)>-C_(n+1)<U_n,rho_(n+1)>` strongly enough to bound the
  depth and duration of each downward episode. Prime or `mu=-1` events are not
  automatically favorable without a sign and magnitude estimate for this
  contraction.
- **Gcd-aggregated Vasyunin packets.** On a complete weighted block, aggregate
  common gcds before estimating. Opposite-Mobius-sign reduced pairs are
  favorable, while equal-sign pairs, the diagonal packet, and the constant
  packet are unfavorable. The needed estimate compares the complete favorable
  packet plus the linear contraction against all unfavorable packets; a
  triangle inequality on individual cotangent sums loses the exact packet
  compensation.
- **Divisor-floor/zero coordinates.** The initial `k<=n` Chebyshev cells and
  the endpoint-safe affine zero Gram are exact reorganizations, but neither
  signs the complete defect. Any zero truncation must retain its affine
  remainder, and the limit must be taken after the full contraction. A useful
  bound must be uniform enough in `n` to imply a finite packet inequality, not
  merely an asymptotic or averaged identity.

The strongest clean arithmetic target is the exact weighted packet inequality
(41.5). The more flexible target is (41.7) together with an explicit bound on
`r_j/p_j`. Either would convert genuinely sparse negative defects into finite
half-strength recovery blocks; proving either for the physical Mobius defects
remains RH-sufficient and is not established here.
