# Cycle 207: optimal constant for the complementary-pair HWB minor

## Exact improved theorem

Use one-based coordinates `[6m]={1,...,6m}` and define

\[
 \operatorname{HWB}_{6m}(x)=
 \begin{cases}
  x_{|x|},& |x|>0,\\
  0,& |x|=0.
 \end{cases}
\]

The chosen value at weight zero is immaterial below.

**Theorem.** Let `m>=1`, and let `pi` be any ordering of the `6m` variables.
Put

\[
 P=\{\pi(1),\ldots,\pi(4m)\},\qquad Q=[6m]\setminus P.
\]

In the communication matrix whose rows are assignments to `P`, whose columns
are assignments to `Q`, and whose entries are `HWB_(6m)` on the completed
assignment, there are rows `alpha_z`, indexed by `z in {0,1}^m`, and columns
`beta_j`, indexed by `j in [m]`, such that

\[
 \operatorname{HWB}_{6m}(\alpha_z\cup\beta_j)=z_j.
\]

Thus this cut matrix contains the data-rows/query-columns `INDEX_m` matrix.
Consequently every exact deterministic OBDD for `HWB_(6m)` in order `pi` has
width at least `2^m` at the level immediately after the first `4m` variables,
and hence has size at least `2^m`.

**Proof.** Consider the inclusive integer intervals

\[
 J_0=[m,3m],\qquad J_1=[3m,5m].
\]

Their union is `[m,5m]`. Its complement in `[6m]` is
`[1,m-1] union [5m+1,6m]`, of size `(m-1)+m=2m-1`. Since `|P|=4m`,

\[
 |P\cap(J_0\cup J_1)|\ge 4m-(2m-1)=2m+1.
\]

If both `|P cap J_0|` and `|P cap J_1|` were at most `m-1`, then

\[
 |P\cap(J_0\cup J_1)|
 \le |P\cap J_0|+|P\cap J_1|\le 2m-2,
\]

a contradiction. Choose `a in {0,1}` for which `|P cap J_a|>=m`, set
`r=m` if `a=0` and `r=3m` if `a=1`, and choose distinct data coordinates

\[
 i_1,\ldots,i_m\in P\cap[r,r+2m].
\]

There are `3m` coordinates in `P` outside the data set, so choose distinct
compensators `c_1,...,c_m` among them. Let

\[
 R=P\setminus\{i_1,\ldots,i_m,c_1,\ldots,c_m\};
\]

then `|R|=2m`. For each `z in {0,1}^m`, define the row assignment
`alpha_z` by

\[
 x_{i_j}=z_j,\qquad x_{c_j}=1-z_j\quad(j\in[m]),
\]

and set every coordinate in `R` to zero when `r=m`, or every coordinate in
`R` to one when `r=3m`. Every complementary pair contributes exactly one,
so in the first case `|alpha_z|=m`; in the second case the pairs contribute
`m` and `R` contributes `2m`, so `|alpha_z|=3m`. In either case,

\[
 |\alpha_z|=r. \tag{1}
\]

For each `j`, put `t_j=i_j-r`. Because `i_j in [r,r+2m]`,
`0<=t_j<=2m=|Q|`. Choose any assignment `beta_j` to `Q` having exactly
`t_j` ones. The domains of `alpha_z` and `beta_j` are disjoint, so (1) gives

\[
 |\alpha_z\cup\beta_j|=r+t_j=i_j.
\]

Moreover `i_j in P`, so the suffix assignment does not alter the data bit at
that coordinate. Therefore

\[
 \operatorname{HWB}_{6m}(\alpha_z\cup\beta_j)
 =x_{i_j}=z_j. \tag{2}
\]

The data coordinates are distinct, hence the `t_j` are distinct; assignments
of different Hamming weights cannot be duplicate columns. Equation (2) is
therefore an exact `2^m`-by-`m` `INDEX_m` submatrix. Its rows are all the
distinct words `z`, so the `2^m` chosen prefix assignments induce pairwise
distinct residual functions on `Q`.

In a deterministic OBDD respecting `pi`, two assignments that reach the same
state after the first `4m` variables induce the same residual function on the
remaining variables. Hence those assignments require `2^m` distinct states at
that level. This proves the width, and therefore the size, lower bound. `□`

The cut after `4m` variables is deliberately not the midpoint of the `6m`
variables. This causes no gap: for every order `pi`, the positions
`pi(1),...,pi(4m)` form an OBDD level. Width lower bounds apply at every level,
not only at the midpoint. Equivalently, in a convention allowing skipped
levels, subdivide edges by dummy states; the `2^m` distinct residuals force
`2^m` distinct frontier states across this cut.

## Why the interval method cannot reach `1/5`

Consider the general fixed-cut form of this method, with `p` prefix and
`q=N-p` suffix coordinates, seeking an `INDEX_k` minor. Complementary pairs
and fixed prefix bits impose

\[
 k\le r\le p-k.
\]

For base weight `r`, all `k` data coordinates must belong to the accessible
address interval

\[
 W_r=[r,r+q],
\]

because the suffix can add a weight only between zero and `q`. Thus the
method succeeds for a prefix set `P` only if some allowed `W_r` contains at
least `k` members of `P`.

This universal fixed-cut interval guarantee has asymptotic ceiling
`k/N=1/6`. All
allowed windows miss the two endpoint regions outside

\[
 U=[k,N-k],
\]

which together hold `2k+O(1)` coordinates. Put as many prefix coordinates as
possible there and distribute the remaining `p-2k+O(1)` nearly uniformly in
`U`. The average occupancy scale of a length-`q` allowed window is

\[
 \frac{q(p-2k)}{N-2k}+O(1).
\]

For fixed `N,k`, maximizing this expression over the cut position gives

\[
 \max_p\frac{(N-p)(p-2k)}{N-2k}
 =\frac{N-2k}{4}.
\]

If `k>(1/6+epsilon)N`, this is below `k` by a linear margin. A uniformly
random choice of the required central prefix coordinates, followed by a
hypergeometric tail bound and a union bound over the `O(N)` allowed windows,
produces, for all sufficiently large `N`, a prefix set for which every window
has fewer than `k` prefix coordinates. Cuts with `p<2k` cannot even supply the
data/compensator pairs. Therefore no choice of a fixed cut and accessible
address intervals in this method guarantees a larger asymptotic ratio.

The best asymptotic exponent obtainable from this exact fixed-weight,
prescribed-cut complementary-pair/suffix-weight interval mechanism is
therefore

\[
 \boxed{1/6}.
\]

The known universal `HWB` lower-bound exponent `1/5` must exploit more of the
residual-function structure than this exact `INDEX` extraction; optimizing
these intervals at one prescribed cut cannot recover it. The obstruction does
not by itself rule out a materially different proof that adaptively chooses a
cut from the whole order, because the adverse prefix sets constructed for
different cut sizes need not be nested prefixes of one permutation.

## Comparison with the classical `1/5`

The theorem gives `width(HWB_N)>=2^(N/6)` on the subsequence `N=6m`. This is
strictly weaker in its exponential constant than the classical universal HWB
bound customarily stated with exponent `1/5`. It does not improve that bound.
Its narrower contribution is the explicit certificate: one prescribed cut in
every order contains an exact `INDEX_(N/6)` minor, with no selector variables.
The classical argument may distinguish more residuals without organizing them
as this particular fixed-weight INDEX minor.

The interval-method ceiling above concerns only the declared mechanism:
complementary data/compensator pairs, one constant prefix weight, suffix weight
as the address increment, and one prescribed cut. It is not an upper bound on
OBDD width, does not rule out another exact-minor construction, and does not
rule out choosing a cut adaptively from the whole order. The result is only a
restricted-model deterministic OBDD lower bound. It gives no unrestricted
circuit lower bound, no MCSP lower bound, and no `P != NP` conclusion. No
literature-novelty claim is made without a dedicated primary-source comparison.

## Exact finite verifier

The dependency-free script `verify_cycle207_hwb_6m_index.py` exhaustively
enumerates every set `P subset [6m]` of size `4m` for small `m`. For every cut
it constructs the data coordinates, compensators, all `2^m` prefix rows, and
all `m` suffix queries; directly evaluates `HWB_(6m)`; and checks that the
materialized matrix is exactly `K(z,j)=z_j`. Its default range is `m<=3`, or
`15+495+18564=19074` cuts. It also checks representative certificates through
`m=64` without materializing all rows.

Run from the repository root:

```text
python3 millennium-prize/p-vs-np/verify_cycle207_hwb_6m_index.py
```

This finite computation checks the construction and boundary conventions; it
does not replace the quantified proof.
