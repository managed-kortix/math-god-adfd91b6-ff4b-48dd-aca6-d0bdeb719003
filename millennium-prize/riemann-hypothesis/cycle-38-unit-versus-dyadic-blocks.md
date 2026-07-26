# Cycle 38: unit endpoint blocks versus adaptive dyadic blocks

## Exact unit refinement

Put

\[
 h_n={1\over\log n}-{1\over\log(n+1)},\qquad
 w_n=h_n\log n={\log(1+1/n)\over\log(n+1)}.
\]

For the complete endpoint energy,

\[
 P_n-P_{n+1}=2h_nE_n.
\tag{38.1}
\]

Consequently every integer endpoint block has the exact refinement

\[
 \boxed{P_a-P_b=\sum_{a\le n<b}(P_n-P_{n+1})
 =2\sum_{a\le n<b}h_nE_n.}
\tag{38.2}
\]

In particular,

\[
 \boxed{P_N-P_{2N}=2\sum_{N\le n<2N}h_nE_n.}
\tag{38.3}
\]

Thus a dyadic endpoint decrement is a consecutive packet of unit endpoint
decrements. Its advantage is only that cancellation among signed `E_n` is
allowed before seeking the complete weighted estimate

\[
 P_a-P_b\ge 2\kappa\sum_{a\le n<b}w_nP_n.
\tag{38.4}
\]

A pointwise unit estimate would imply (38.4), but is strictly stronger and is
incompatible with the observed possibility of negative one-step decrements.

## Covering and multiplicity identities

Let `S` be a locally finite multiset of dyadic starts and attach nonnegative
coefficients `lambda_N`, combining duplicates at one start. Define

\[
 c_n=\sum_{N:\,N\le n<2N}\lambda_N
     =\sum_{n/2<N\le n}\lambda_N.
\tag{38.5}
\]

For every finite family, or every finite truncation of a locally finite family,

\[
 \boxed{\sum_N\lambda_N(P_N-P_{2N})
 =\sum_n c_n(P_n-P_{n+1}),}
\tag{38.6}
\]

and

\[
 \boxed{\sum_N\lambda_N\sum_{N\le n<2N}w_nP_n
 =\sum_n c_nw_nP_n.}
\tag{38.7}
\]

These identities separate interior multiplicity from endpoint resets. On a
finite integer interval `[A,B]`, discrete Abel summation gives

\[
 \sum_{n=A}^{B}c_n(P_n-P_{n+1})
 =c_AP_A+\sum_{n=A+1}^{B}(c_n-c_{n-1})P_n-c_BP_{B+1}.
\tag{38.8}
\]

The positive variations of `c_n` are restart terms. Bounded overlap, tail
coverage, or divergence of (38.7) does not control them. Exact multiplicity one
makes (38.8) telescope; a general adaptive cover does not.

## Rigidity of exact dyadic covering

**Proposition.** Fix `a>=2`. Suppose `lambda_N>=0`, `lambda_N=0` for `N<a`,
and

\[
 \sum_{N:\,N\le n<2N}\lambda_N=1\qquad(n\ge a).
\tag{38.9}
\]

Then

\[
 \lambda_N=\begin{cases}
 1,&N=2^ja\text{ for some }j\ge0,\\
 0,&\text{otherwise}.
 \end{cases}
\tag{38.10}
\]

*Proof.* At `n=a`, (38.9) gives `lambda_a=1`. For `a<n<2a`, the interval
starting at `a` remains active, so nonnegativity forces every new `lambda_n` to
vanish. At `n=2a`, the first interval has expired and all intervening
coefficients vanish, hence `lambda_(2a)=1`. Repeating on
`[2^ja,2^(j+1)a)` proves (38.10) by induction. QED.

Therefore the unique nonnegative exact conversion of anchored dyadic blocks
into every unit block is the ordinary chain

\[
 [a,2a),[2a,4a),[4a,8a),\ldots.
\tag{38.11}
\]

Arbitrary adaptive starts create overlap or gaps, not a new consecutive
partition. Splitting at every endpoint only produces atoms with multiplicities
`c_n`, and (38.8) retains the restart obstruction. Signed covering
coefficients could cancel multiplicities algebraically, but would destroy the
nonnegative effective measure required by the liminf theorem.

## Valid adaptive grouping

Adaptivity is harmless when it groups consecutive members of one dyadic chain.
Let

\[
 K_r=2^ra,\qquad 0=r_0<r_1<r_2<\cdots.
\]

Then `I_j=[K_(r_j),K_(r_(j+1)))` are consecutive integer blocks, and

\[
 \boxed{P_{K_{r_j}}-P_{K_{r_{j+1}}}
 =\sum_{r=r_j}^{r_{j+1}-1}(P_{K_r}-P_{2K_r})
 =\sum_{n\in I_j}(P_n-P_{n+1}).}
\tag{38.12}
\]

Likewise,

\[
 \boxed{\sum_{r=r_j}^{r_{j+1}-1}\sum_{K_r\le n<2K_r}w_nP_n
 =\sum_{n\in I_j}w_nP_n.}
\tag{38.13}
\]

An adaptive stopping rule may therefore choose `r_(j+1)` after seeing all
packets since `r_j`, provided its proved inequality retains the complete
interior in (38.13). No bounded stopping length or bounded endpoint ratio is
needed. Isolated blocks `[N_j,2N_j)` with unrelated starts are not an endpoint
chain; even bounded-multiplicity tail coverage needs a separate summable-reset
estimate.

## Exact divergent weight accounting

For the chain (38.11), let `W_N=sum_(N<=n<2N) w_n`. Multiplicity one gives

\[
 \boxed{\sum_{j=0}^{J-1}W_{2^ja}
 =\sum_{a\le n<2^Ja}w_n.}
\tag{38.14}
\]

The weight diverges without an asymptotic assumption. Since

\[
 \log(1+1/n)\ge {1\over n+1},
\]

we have

\[
 w_n\ge {1\over(n+1)\log(n+1)},
\tag{38.15}
\]

and comparison with `int dx/(x log x)` proves

\[
 \sum_{n\ge a}w_n=\sum_{j\ge0}W_{2^ja}=\infty.
\tag{38.16}
\]

If group `j` proves (38.4) with loss `kappa_j`, the actual effective mass is

\[
 \boxed{\sum_j\kappa_j\sum_{n\in I_j}w_n
 =\sum_{n\ge a}\kappa_{j(n)}w_n,}
\tag{38.17}
\]

not the nominal mass in (38.16). It must diverge after every loss is inserted.
Keeping only one representative per increasingly long group can lose
divergence. Indeed,

\[
 W_N\le\sum_{N\le n<2N}{1\over n\log n}\le {1\over\log N},
\tag{38.18}
\]

so sampling only `N_j=2^(2^j)a` gives `sum_j W_(N_j)<infinity`. Retaining all
constituent dyadic packets instead recovers (38.14), regardless of stopping
lengths.

## Verdict

Unit and dyadic endpoint blocks are exactly related by (38.2)--(38.3). The only
nonnegative multiplicity-one tail partition by anchored `[N,2N)` blocks is the
rigid geometric chain. Adaptive grouping along that chain converts exactly into
complete consecutive integer blocks by (38.12)--(38.13). Arbitrary adaptive
starts face a genuine reset obstruction measured by (38.8). The divergent RH
weight survives complete grouping exactly, but may disappear if intermediate
packets, block constants, smoothing factors, or boundary losses are omitted.

This is a bookkeeping and obstruction theorem. It supplies no
Mobius-specific lower bound of the form (38.4), so it does not prove RH.
