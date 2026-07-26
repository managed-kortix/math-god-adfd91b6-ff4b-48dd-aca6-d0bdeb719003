# Cycle 38: adaptive renewal in exact Mobius--Chebyshev arithmetic

## 1. One-step endpoint channels

For an integer `n>=3`, put

\[
 L_n=\log n,\qquad
 c_a(n)=\mu(a){\log(n/a)\over L_n}\quad(a\le n),
\]

and use the reciprocal-variable realization

\[
 G_n(t)=1+\sum_{a\le n}c_a(n)\{t/a\},
 \qquad
 P_n=\int_1^\infty G_n(t)^2{dt\over t^2}.
 \tag{38.1}
\]

This `P_n` is exactly the restricted `(0,1)` energy after `t=1/x`. Define

\[
 h_n={1\over L_n}-{1\over L_{n+1}}>0,
 \qquad
 D_n(t)=\sum_{a\le n}\mu(a)\log a\,\{t/a\}.
 \tag{38.2}
\]

The endpoint coefficient at `a=n+1` is zero, so coefficient comparison gives

\[
 G_{n+1}=G_n+h_nD_n.                         \tag{38.3}
\]

It is convenient to set `d_n=-D_n` and

\[
 q_n(t)=2G_n(t)d_n(t)-h_nd_n(t)^2.
 \tag{38.4}
\]

Then the complete one-step identities are

\[
 \boxed{P_n-P_{n+1}=h_n\int_1^\infty q_n(t){dt\over t^2}
 =2h_nE_n,}                                  \tag{38.5}
\]

\[
 E_n=-\langle G_n,D_n\rangle
       -{h_n\over2}\|D_n\|_2^2.
 \tag{38.6}
\]

Thus the desired quantity is a compensated Mobius correlation, not the mixed
term alone. Dropping the quadratic cost in (38.6) changes the theorem.

## 2. Exact unit-cell arithmetic

On `(k,k+1)`, define

\[
 A_n=\sum_{a\le n}{c_a(n)\over a},
 \qquad
 B_n=-\sum_{a\le n}{\mu(a)\log a\over a},                 \tag{38.7}
\]

\[
 b_{n,k}=1-\sum_{a\le n}c_a(n)\lfloor k/a\rfloor,
 \qquad
 e_{n,k}=\sum_{a\le n}\mu(a)\log a\lfloor k/a\rfloor.   \tag{38.8}
\]

Then, exactly,

\[
 G_n(t)=A_nt+b_{n,k},\qquad d_n(t)=B_nt+e_{n,k}.           \tag{38.9}
\]

Set

\[
 \begin{aligned}
 C_n&=2A_nB_n-h_nB_n^2,\\
 Z_{n,k}&=2(A_ne_{n,k}+B_nb_{n,k})-2h_nB_ne_{n,k},\\
 H_{n,k}&=2b_{n,k}e_{n,k}-h_ne_{n,k}^2.
 \end{aligned}                                             \tag{38.10}
\]

The existing complete-cell formula now becomes

\[
 \boxed{J_{n,k}:=\int_k^{k+1}q_n(t){dt\over t^2}
 =C_n+Z_{n,k}\log(1+1/k)+{H_{n,k}\over k(k+1)}.}          \tag{38.11}
\]

No analytic transform is hidden here: every coefficient in (38.11) is a
finite expression in `mu`, integer floors, and logarithms. The divisor-impulse
updates are

\[
 \boxed{b_{n,k+1}=b_{n,k}-\sum_{a\mid k+1}c_a(n),
 \qquad
 e_{n,k+1}=e_{n,k}+\sum_{a\mid k+1}\mu(a)\log a.}         \tag{38.12}
\]

For `1<=k<=n`, the two classical convolutions

\[
 \sum_{a\le k}\mu(a)\lfloor k/a\rfloor=1,
 \qquad
 \sum_{a\le k}\mu(a)\log a\lfloor k/a\rfloor=-\psi(k)
\]

give the exact Chebyshev specialization

\[
 \boxed{b_{n,k}=-{\psi(k)\over L_n},\qquad
 e_{n,k}=-\psi(k).}                                      \tag{38.13}
\]

Consequently, on the full initial range,

\[
 \boxed{\begin{aligned}
 Z_{n,k}&=-2A_n\psi(k)-{2B_n\psi(k)\over L_n}
          +2h_nB_n\psi(k),\\
 H_{n,k}&=\left({2\over L_n}-h_n\right)\psi(k)^2.
 \end{aligned}}                                           \tag{38.14}
\]

Beyond `k=n`, (38.8) is the exact truncated Mobius endpoint transform; replacing
it by a Chebyshev main term would erase the active correlation.

For completeness, the same cells give an exact arithmetic expression for the
energy on the right side of a renewal inequality:

\[
 \boxed{K_{n,k}:=\int_k^{k+1}G_n(t)^2{dt\over t^2}
 =A_n^2+2A_nb_{n,k}\log(1+1/k)
  +{b_{n,k}^2\over k(k+1)},}                              \tag{38.15}
\]

with `P_n=sum_(k>=1) K_(n,k)`. All infinite sums in this note mean limits of
complete prefixes; the direct endpoint tail estimate supplies a rigorous
finite enclosure when one is needed computationally.

## 3. Complete adaptive renewal inequality

For integers `3<=a<b`, define the exact block surplus

\[
 \boxed{\begin{aligned}
 \mathfrak S_\kappa(a,b)
 &:={1\over2}\sum_{n=a}^{b-1}h_n\sum_{k\ge1}J_{n,k}
   -\kappa\sum_{n=a}^{b-1}h_nL_n\sum_{k\ge1}K_{n,k}\\
 &=\sum_{n=a}^{b-1}h_n
 \left[-\langle G_n,D_n\rangle-{h_n\over2}\|D_n\|_2^2
       -\kappa L_nP_n\right].
 \end{aligned}}                                           \tag{38.16}
\]

Equations (38.7)--(38.15) rewrite every term in the first line solely through
Mobius coefficients, Chebyshev values, divisor floors, and elementary cell
weights. By (38.5), the same quantity is

\[
 \boxed{\mathfrak S_\kappa(a,b)
 ={P_a-P_b\over2}
 -\kappa\sum_{n=a}^{b-1}h_nL_nP_n.}                       \tag{38.17}
\]

The full RH-sufficient adaptive rule would be

\[
 \tau_\kappa(a)=\min\{b>a:\mathfrak S_\kappa(a,b)\ge0\}. \tag{38.18}
\]

If one fixed `kappa>0` makes every successive stopping time finite, then the
resulting blocks are consecutive and

\[
 P_a-P_{\tau_\kappa(a)}
 \ge2\kappa\sum_{a\le n<\tau_\kappa(a)}h_nL_nP_n.         \tag{38.19}
\]

Since `sum h_nL_n` diverges, iteration forces `liminf P_n=0` and hence RH by
the already proved off-critical-zero floor. Negative `E_n`, negative cells,
and arbitrarily long blocks are all permitted. Merely defining (38.18) does
not prove that its set is nonempty.

## 4. One correlation target below the RH-sufficient threshold

The full fixed-`kappa` stopping theorem cannot honestly be called weaker than
RH: together with the exact identities above it implies RH. A deliberately
weakened pilot theorem, which isolates the same arithmetic correlation but has
only summable effective mass, is the following.

**Target C38 (summably weakened adaptive correlation).** There are constants
`kappa>0`, `C>1`, and `a_0` such that for every `a>=a_0` there is an integer
`b` with

\[
 a<b\le a^C                                                     \tag{38.20}
\]

and

\[
 \boxed{{1\over2}\sum_{n=a}^{b-1}h_n\sum_{k\ge1}J_{n,k}
 \ge {\kappa\over\log a}
 \sum_{n=a}^{b-1}h_nL_n\sum_{k\ge1}K_{n,k}.}               \tag{38.21}
\]

This is one compensated Mobius--Chebyshev correlation target: its left side
retains the mixed term and its exact quadratic cost, and (38.11)--(38.15) are
its complete arithmetic expansion. It is quantitatively weaker than the needed
renewal statement because the block coefficient is `kappa/log a` rather than a
fixed positive constant.

Indeed, for a consecutive chain satisfying (38.20), `n<b<=a^C` implies
`1/log a<=C/log n`, and therefore its total effective mass is bounded by

\[
 C\kappa\sum_{n\ge a_0}h_n<\infty.                         \tag{38.22}
\]

Thus (38.21), even on every block, does not feed the divergent-mass liminf
criterion and does not imply RH by the renewal argument. Abstract nonnegative
sequences with summable contraction strength show that no implication can be
deduced from this inequality's quantifiers alone. This does not prove the
stronger model-theoretic claim that the particular arithmetic assertion could
have no other consequence for zeta. It is a useful first target
because it tests the exact signed correlation and adaptive stopping mechanism
without concealing an RH conclusion in the theorem statement. Any upgrade must
improve `1/log a` to a block factor whose effective mass actually diverges.

## 5. Adversarial circularity audit

1. **Logical strength.** A fixed positive coefficient in (38.19) on a complete
   chained tail is RH-sufficient. Calling that theorem "weaker than RH" because
   it is averaged, adaptive, or allows negative increments would be false.
2. **Stopping-time tautology.** The identity (38.17) permits one to define a
   first favorable endpoint, but gives no proof that it exists. Assuming every
   stopping time is finite is exactly the missing arithmetic theorem.
3. **Complete versus restricted pieces.** The left side of (38.21) uses all
   cells `k>=1`. A restricted shell, finite prefix, oscillatory component, or
   smoothed surrogate cannot replace it without a one-sided cumulative error.
4. **Compensation.** A lower bound for `-<G_n,D_n>` alone is insufficient. The
   term `h_n||D_n||^2/2` in (38.6) is mandatory and can erase the mixed gain.
5. **No reciprocal-zeta substitution.** The sums in (38.7)--(38.12) are finite
   Mobius polynomials. Replacing them by `1/zeta(s)` and shifting through the
   critical strip imports poles at zeta zeros; a critical-line bound there is
   RH-level input, not a proof of (38.21).
6. **No hidden Mertens hypothesis.** Pointwise `M(x)=O(x^(1/2+epsilon))` for all
   `epsilon>0` is equivalent to RH. Square-root cancellation for the positive
   max-kernel channel is likewise too strong when separated from the mixed
   channel. The target must estimate the compensated expression as written.
7. **Chebyshev scope.** Formula (38.13) is exact only for `k<=n`. Extending it
   past the endpoint deletes the truncated Mobius transform. Unconditional
   Chebyshev bounds for `psi` do not control that transform at the required
   correlation scale.
8. **No factorization after averaging.** Averaging products in (38.16) cannot
   be replaced by products of averaged endpoint coefficients. That operation
   destroys the common-`n` quadratic correlation.
9. **Effective mass after losses.** The weakened factor in (38.21) makes the
   mass summable by (38.22). One may not cite divergence of the nominal
   `sum h_nL_n` before this factor is inserted.
10. **Finite evidence.** Exact cell certificates can verify bounded blocks and
    test (38.21), but no finite range proves the universal stopping assertion or
    an asymptotic correlation theorem.

The safe conclusion is therefore narrow: (38.16) is the complete requested
arithmetic rewrite; (38.21) is one correlation target below the
RH-sufficient renewal threshold; and the fixed-strength version remains the
RH-sufficient missing lemma rather than a weaker theorem.
