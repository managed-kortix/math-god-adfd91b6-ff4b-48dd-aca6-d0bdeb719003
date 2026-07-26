# Adversarial audit of the centered quadratic channel

## Scope and verdict

Let `n=N/2`, `m=N-1`, `L=log N`, `L_2=log(2N)`, and

\[
 Q_N=-{1\over L^2}\sum_{k=n}^m{E_k^2\over k(k+1)}
 +{1\over LL_2}\sum_{k=n}^m{E_kF_k\over k(k+1)}.
\]

This is the quadratic channel in the centered correlation. The conclusions of
this audit are:

1. A diagonal/fixed-shift split is a valid finite bookkeeping device only after
   the increment basis, orientation, and endpoint convention have been fixed.
   It is not an invariant or sign-preserving decomposition.
2. The odd endpoint `2k+1` is not part of the bulk `psi(2k)` rectangle. Folding
   it into a shift sum without its interpolation coefficient loses an endpoint
   term.
3. Positive semidefiniteness of the two prefix Gram kernels gives no sign for
   `Q_N`; the mixed kernel is a polarization between two independently
   steerable prefix vectors.
4. PNT, even in the much stronger surrogate form `psi(x)=x+O(1)`, gives no sign.
5. The diagonal and even a single fixed-shift piece can each exceed the
   completed prefix energy by a factor of order `N`. They must not be estimated
   separately.

The safest quadratic grouping is the complete prefix packet

\[
 \boxed{\sum_{k=n}^m {E_k\over k(k+1)}
 \left({F_k\over LL_2}-{E_k\over L^2}\right).}
\]

For a contraction claim even this is not complete enough: retain the full
image-space packet `-2 w_k u_k delta_k-w_k delta_k^2` together with the exact
odd jump square assigned to the same pair.

## Endpoint-safe increment expansion

Write

\[
 x_r=\Lambda(r)-1,\qquad S(t)=\sum_{r\leq t}x_r,
 \qquad \rho_k={k\over2k+1}.
\]

Then

\[
 E_k=S(k),\qquad F_k=S(2k)+\rho_k(x_{2k+1}+1).
\]

Define the finite suffix kernel

\[
 K_N(t)=\sum_{k=\max(n,t)}^m{1\over k(k+1)},
\]

with `K_N(t)=0` when `t>m`. Exact expansion gives

\[
 \sum_{k=n}^m{E_k^2\over k(k+1)}
 =\sum_{i,j\leq m}x_ix_jK_N(\max(i,j)),
\]

and

\[
\begin{aligned}
 \sum_{k=n}^m{E_kF_k\over k(k+1)}
 ={}&\sum_{i\leq m}\sum_{j\leq2m}
 x_ix_jK_N\!\left(\max\left(i,\left\lceil{j\over2}\right\rceil\right)\right)\\
 &+\sum_{k=n}^m{\rho_k\over k(k+1)}
 \left(\sum_{i\leq k}x_i\right)(x_{2k+1}+1).
\end{aligned}
\]

These formulas are endpoint-safe. In particular:

- increments below `n` remain in every shell prefix and cannot be discarded;
- `j=2k+1` is excluded from the bulk rectangle and occurs in the second line;
- the upper bulk endpoint is `2m=2N-2`, while the endpoint line reaches
  `2m+1=2N-1`;
- `K_N` contains the lower truncation `max(n,...)`, so it is not a
  translation-invariant shift kernel.

Partitioning the two finite double sums by `h=j-i` is algebraically exact if
all four facts are retained. Calling `h=0` the diagonal is conventional, but
the resulting pieces depend on using the centered increments `Lambda-1`, on
the orientation of the rectangular mixed form, and on whether the endpoint
line is kept separate. Symmetrizing `EF` also reallocates every off-diagonal
coefficient. Thus the split is not canonical in a way that can support an
arithmetic sign argument.

## PSD supplies no sign

The prefix maps `x -> (S(k))` and `x -> (S(2k))` have PSD Gram matrices.
However, `Q_N` contains a negative square plus a mixed polarization, not a
nonnegative quadratic form. At the image level, if `E_k=H` and `F_k=T` on the
whole shell, then

\[
 Q_N=\left(\sum_{k=n}^m{1\over k(k+1)}\right)
 \left(-{H^2\over L^2}+{HT\over LL_2}\right).
\]

For `H=1`, this is negative at `T=0` and positive at `T=2` for every dyadic
`N>=4`. Both image pairs are realizable by bounded nonnegative increments, as
shown next. Therefore no PSD, Cauchy--Schwarz, Loewner, or prefix-kernel
argument can determine the required sign without an additional arithmetic
angle theorem.

## Bounded PNT countermodels of both signs

Start from the nonnegative baseline `lambda(r)=1`, put `x_r=lambda(r)-1`, and
fix one dyadic `N>=4`. Set all unspecified `x_r` to zero and prescribe

\[
 x_n=1,\qquad x_N=T-1,
\]

where `T` is either `0` or `2`. For
`k=n,n+1,...,m`, prescribe

\[
 x_{2k+1}=-1,
\]

and, whenever it is needed before the next even prefix, prescribe

\[
 x_{2k+2}=+1.
\]

After the shell, use at most two further increments in `{-1,+1}` to return the
total centered sum to zero. Every resulting `lambda(r)` belongs to `{0,1,2}`. On the
shell,

\[
 S(k)=1,
 \qquad S(2k)=T,
 \qquad x_{2k+1}+1=0,
\]

so `E_k=1` and `F_k=T` identically. Hence `T=0` and `T=2` give opposite strict
signs for `Q_N`.

Each block has bounded partial centered sum and zero total centered mass.
Place disjoint copies at dyadic scales growing fast enough that their supports
do not overlap, alternating `T=0` and `T=2`. The resulting single nonnegative
sequence satisfies

\[
 \sum_{r\leq x}\lambda(r)=x+O(1),
\]

yet `Q_N` has both signs along infinitely many selected scales. This is much
stronger aggregate control than PNT. It proves that PNT-sized information,
with no exact prime or Mobius structure, cannot imply a local dyadic sign.

## Huge diagonal cancellation

Take the bounded alternating centered increments `x_r=(-1)^r`. Then
`S(t)` is bounded, so

\[
 N\sum_{k=n}^m{S(k)^2\over k(k+1)}=O(1).
\]

In the increment expansion of the same PSD prefix energy, its diagonal alone
is

\[
 D_N=N\sum_{i\leq m}x_i^2K_N(\max(n,i)).
\]

For every `i<=n`, `K_N(n)=1/n-1/N=1/N`; those indices alone contribute
`n=N/2`. Thus `D_N>=N/2`, while the complete energy is `O(1)`. The sum of the
off-diagonal shifts is consequently `-D_N+O(1)`. This cancellation occurs
inside a PSD form: PSD controls the completed total, not its diagonal or any
individual shift class.

Indeed the oriented `h=1` pair, including its symmetric multiplicity, is

\[
 2N\sum_{i\leq m-1}x_ix_{i+1}K_N(i+1)
 =-2N\sum_{i\leq m-1}K_N(i+1).
\]

The indices `i<n` alone give magnitude at least `N-2`. Thus the diagonal and
one fixed shift already have opposite order-`N` sizes, although the completed
PSD energy is bounded. Further shifts finish the cancellation.

The same example has `lambda(r)=1+(-1)^r` in `{0,2}` and summatory function
`x+O(1)`. Therefore neither nonnegativity nor PNT prevents diagonal and
off-diagonal pieces from being individually order `N` larger than their sum.
Any estimate that takes absolute values after the diagonal/fixed-shift split
destroys exactly the cancellation that makes the centered errors small.

## Safest complete grouping

There are three levels of grouping, in decreasing order of safety.

1. For the actual shell decrement, use the invariant image-space identity

   \[
   E_N-E_{2N}=\sum_{k=n}^m
   \left[-2w_ku_k\delta_k-w_k\delta_k^2-r_k^{\rm jump}\right],
   \]

   where `w_k=N/[k(k+1)]` and `r_k^{jump}` is the exact nonnegative odd-pair
   jump contribution. This retains polarization and the prime-square cost.

2. If only the centered correlation is under study, retain all slope, linear,
   and quadratic terms at a fixed `k` before summing. This preserves the exact
   cancellation that produced `u_k` and `delta_k` from the uncentered channels.

3. If the quadratic channel must be isolated, retain

   \[
   {E_k\over k(k+1)}
   \left({F_k\over LL_2}-{E_k\over L^2}\right)
   \]

   as one packet. Do not separate its increment diagonal, fixed shifts, odd
   endpoint, or historical-prefix terms before obtaining a signed theorem for
   the complete packet.

The diagonal/fixed-shift expansion may still identify what new theorem would
be needed, but it cannot itself provide the sign. A successful estimate must
be cancellation-preserving and must use exact arithmetic structure beyond PSD
and beyond PNT.

## Certified finite decomposition

`analyze_effective_shell.py` implements one endpoint-safe bookkeeping split of
the complete quadratic packet into:

1. the literal centered increment diagonal;
2. a same-prefix fixed-shift family;
3. the structured odd-dilation endpoint;
4. the remaining cross-window off-diagonal rectangle.

This split is diagnostic rather than canonical, for the reasons above.  Arb
certifies its recombination through `N=8192`.  At that endpoint the four pieces
are approximately

\[
-0.0040256251,
\quad +0.0040046379,
\quad -0.0000015132,
\quad -0.0003930616,
\]

which sum to `-0.0004155620`.  The diagonal and fixed-shift family nearly
cancel; the residual is controlled by the generic off-diagonal rectangle in
this particular bookkeeping.  No asymptotic sign is inferred.
