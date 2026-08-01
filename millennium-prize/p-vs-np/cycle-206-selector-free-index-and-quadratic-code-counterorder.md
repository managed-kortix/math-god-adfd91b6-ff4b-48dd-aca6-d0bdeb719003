# Cycle 206: selector-free INDEX and a quadratic-code counterorder

## Exact all-order benchmark

For `m>=1`, put `M=8m` and define the hidden weighted bit function

\[
  HWB_M(x_1,\ldots,x_M)=x_{|x|},
\]

with the value at `|x|=0` fixed arbitrarily. This is an explicit
polynomial-time Boolean family and has no separate selector variables: the
address is the Hamming weight of the same input that contains the addressed
bit.

**Theorem.** For every order of the `M` variables, the communication matrix at
the midpoint contains the `m`-bit `INDEX` matrix. Consequently every exact
OBDD for `HWB_M`, in every variable order, has midpoint width at least `2^m`.

Let `P` be the first `4m` variable indices in the order and let `Q=[M]\P`.
Consider the two integer intervals

\[
  J_0=[m,5m],\qquad J_1=[3m,7m].
\]

At least one contains `m` members of `P`. Indeed, their union is `[m,7m]`,
whose complement has only `2m-1` indices. Thus

\[
 |P\cap(J_0\cup J_1)|\ge 4m-(2m-1)=2m+1.
\]

If both intersections had size at most `m-1`, their union would have size at
most `2m-2`, a contradiction.

Choose `r=m` when `J_0` works and `r=3m` when `J_1` works, and choose distinct
data indices `i_1,...,i_m` in `P\cap[r,r+4m]`. Pair them with distinct
compensator indices `c_1,...,c_m` in `P` outside the data set. For every
`z in {0,1}^m`, define a prefix assignment by

\[
 x_{i_j}=z_j,\qquad x_{c_j}=1-z_j.
\]

If `r=m`, set all other prefix variables to zero. If `r=3m`, set all remaining
`2m` prefix variables to one. In either case the prefix has constant weight
`r` and stores the arbitrary data word `z` at the indices `i_j`.

For query `j`, choose any suffix assignment on `Q` of weight `i_j-r`; this is
possible because `0<=i_j-r<=4m`. The completed input has weight exactly `i_j`,
and hence

\[
 HWB_M(\alpha_z,\beta_j)=x_{i_j}=z_j.
\]

The rows `alpha_z` and columns `beta_j` therefore form the exact one-way
communication-matrix minor `INDEX_m`. Its `2^m` rows are distinct, proving the
width bound. This construction avoids the quantifier reversal caused by an
input-readable matching selector, although it is the classical hidden-weighted-
bit benchmark rather than an MCSP lower bound.

## Exact counterorder for the natural quadratic-code splice

Let truth-table coordinates be indexed by `F_2^n`, let

\[
 C=RM(2,n),\qquad A=\{u:u_1=0\},
\]

and order all coordinates in `A` before all coordinates outside `A`. This is a
balanced midpoint order. Its cut indicator is `a(u)=1+u_1`. For any
`f,g in C`, the splice using `f` on `A` and `g` off `A` is

\[
 f\star_A g=a f+(1-a)g=(1+u_1)f+u_1g.
\]

After multilinear reduction this has degree at most three, so

\[
 f\star_A g\in RM(3,n)
\]

in both orientations. Every member of `RM(3,n)` has an `{AND,XOR,NOT}` circuit
with constants of size at most

\[
 3\sum_{j=0}^3 {n\choose j}.
\]

Therefore, for every MCSP threshold

\[
 s\ge 3\sum_{j=0}^3 {n\choose j},
\]

all quadratic-code cross-splices at this midpoint are easy. The induced
easy/hard matrix is identically easy and contains no nonconstant communication
minor, in particular no `INDEX` minor of order one or larger.

The same counterorder applies after any invertible affine relabeling of the
evaluation points: put one affine hyperplane first. More generally, for
`RM(d,n)` a degree-`t` cut indicator sends every splice into `RM(d+t,n)`.
Thus any affine-invariant bounded-degree evaluation-code proposal that seeks an
all-order MCSP minor solely from codeword cross-splices fails on an affine-
hyperplane order whenever the MCSP threshold contains the next Reed--Muller
layer.

## Scope

The first theorem gives the requested explicit selector-free all-order `INDEX`
minor, but for `HWB`, not for MCSP. The second theorem is an exact obstruction
to the natural quadratic Reed--Muller transfer: replacing `HWB` data words by
easy quadratic truth tables loses the all-order property at the displayed
hyperplane order. Neither result supplies an unrestricted circuit lower bound,
a lower bound for relational `search-MCSP^SAT`, or a `P != NP` conclusion.
