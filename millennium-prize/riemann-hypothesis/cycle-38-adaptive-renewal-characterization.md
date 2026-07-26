# Cycle 38: exact characterization of finite adaptive renewals

## 1. Setup and verdict

Fix `n_0>=2` and write

\[
 w_n=\left({1\over\log n}-{1\over\log(n+1)}\right)\log n
 ={\log(1+1/n)\over\log(n+1)}.
\]

Thus `w_n>0`, `w_n->0`, and `sum_(n>=n_0)w_n=infinity`. Fix `c>0`;
in the RH block normalization of Cycle 37, `c=2kappa`. A finite renewal from
`a` is an integer `b>a` such that

\[
 P_a-P_b\ge c\sum_{a\le n<b}w_nP_n.                 \tag{38.1}
\]

The first such `b`, when one exists, is the adaptive stopping time. Let `AR_c`
denote the assertion that a finite renewal exists from every `a>=n_0`.

For arbitrary nonnegative sequences, the exact logical relation is

\[
 \boxed{AR_c\quad\Longrightarrow\quad\liminf_{n\to\infty}P_n=0,}
\]

and the converse is false, even for positive sequences satisfying `P_n->0`
and `sum w_nP_n<infinity`. Hence finite renewal from every start is strictly
stronger than zero liminf, not weaker and not equivalent.

## 2. Nonlocal arithmetic characterization

Define the tail load and residual budget

\[
 T_a:=\sum_{n=a}^\infty w_nP_n,
 \qquad Q_a:=P_a-cT_a.                              \tag{38.2}
\]

**Theorem 38.1 (tail Hardy criterion).** For a nonnegative sequence `P`,
`AR_c` holds if and only if all three conditions below hold:

1. `sum_(n>=n_0)w_nP_n<infinity`;
2. `P_a>=cT_a` for every `a>=n_0`;
3. the equality set
   \[
   Z_c:=\{a>=n_0:P_a=cT_a\}
   \]
   has no largest element, with the empty set allowed.

Condition 2 is a reverse weighted Hardy inequality at every integer. Condition
3 is only a boundary condition: a zero residual budget cannot be renewed from
unless another zero residual budget occurs later. Equivalently, `Q_a>=0` for
all `a`, and every zero of `Q` has a later zero.

*Proof: necessity.* Assume `AR_c` and start at an arbitrary `a=a_0`. Repeatedly
choose a renewal `a_(j+1)>a_j`. The endpoints tend to infinity, and summing
(38.1) gives

\[
 c\sum_{a\le n<a_J}w_nP_n
 \le P_a-P_{a_J}\le P_a.
\]

Letting `J` tend to infinity proves both finiteness of `T_a` and
`P_a>=cT_a`. In particular, the full weighted energy is finite. If equality
holds at `a` and `b` is any renewal from `a`, then

\[
 P_b+c(T_a-T_b)\le P_a=cT_a,
\]

so `P_b<=cT_b`. The already proved reverse inequality at `b` forces equality.
Thus every member of `Z_c` has a later member.

*Proof: sufficiency.* Weighted summability and `sum w_n=infinity` imply
`liminf P_n=0`; otherwise a positive lower bound on a tail would make
`sum w_nP_n` diverge. Also `T_n->0`. Under condition 2, `Q_n>=0`, while along
a subsequence on which `P_n->0` one has `0<=Q_n<=P_n->0`. Therefore

\[
 \liminf_{n\to\infty}Q_n=0.                         \tag{38.3}
\]

If `Q_a>0`, (38.3) supplies a finite `b>a` with `Q_b<Q_a`. If `Q_a=0`,
condition 3 supplies a finite `b>a` with `Q_b=Q_a`. In either case,
`Q_b<=Q_a`, which is exactly

\[
 P_a-P_b\ge c(T_a-T_b)
 =c\sum_{a\le n<b}w_nP_n.
\]

Thus a finite renewal exists from every `a`. QED.

Strict inequalities `P_a>cT_a` at every start automatically give all finite
stops. Endpoint search is needed only at the equality boundary.

## 3. Cumulative-potential formulation

There is a useful finite-prefix version. Put

\[
 R_a:=P_a+c\sum_{n_0\le n<a}w_nP_n.                 \tag{38.4}
\]

Then (38.1) is exactly

\[
 R_b\le R_a.                                        \tag{38.5}
\]

Consequently, `AR_c` says that the cumulative arithmetic potential `R` has no
strict right-to-left record: every value is followed by a value no larger.
When the weighted energy is finite, `R_a=Q_a+cT_(n_0)`, so (38.4) and the tail
Hardy criterion are the same characterization. The tail form is sharper
because it separates the automatic strict-budget case from the exceptional
equality case.

The potential has the local arithmetic increment

\[
 R_{a+1}-R_a=P_{a+1}-(1-cw_a)P_a.                   \tag{38.6}
\]

Thus `R` can be computed without testing all endpoint pairs. For the RH
energies, each `P_a` in (38.2), (38.4), or (38.6) has the exact finite
Mobius--fractional-part Gram expansion, while the one-step term has the exact
Mobius--Chebyshev cell expansion in
`cycle-38-adaptive-renewal-arithmetic.md`. This turns the criterion into a
literal arithmetic inequality rather than a renamed stopping-time assertion.

## 4. Counterexamples to the converse

### 4.1 Positive convergence and finite weighted energy are insufficient

Fix `c>0`. Since

\[
 A_b:=\sum_{n>b}{w_n\over n}=O\left({1\over b\log b}\right),
\]

choose `N` so large that

\[
 c\left(A_b+{w_b\over b}\right)<{1\over b}
 \qquad(b>N).
\]

Let

\[
 P_n={1\over n}\quad(n\ne N),
 \qquad A_N:=\sum_{n>N}{w_n\over n},
 \qquad P_N={cA_N\over2}.
\]

Every term is positive, `P_n->0`, and `sum_n w_nP_n<infinity`, because
`w_n asymp 1/(n log n)`. But

\[
 Q_N=P_N-c\left(w_NP_N+A_N\right)
 <P_N-cA_N=-{cA_N\over2}<0.
\]

Moreover, `Q_b=1/b-cA_b-cw_b/b>0` for every `b>N`, whereas `Q_N<0`. Hence no
`b>N` has `Q_b<=Q_N`, so no renewal can start at `N`. Thus even convergence to
zero plus finite weighted energy does not imply `AR_c`. The obstruction is a
single value too small to pay for its positive future tail.

### 4.2 Zero liminf can also have infinite weighted energy

Set `P_(2^k)=1/k` and `P_n=1` away from powers of two. Then `liminf P_n=0`, but
removing the powers of two removes only finite `w`-mass, so
`sum w_nP_n=infinity`. If `AR_c` held, the necessity proof would force this
weighted sum to be finite, a contradiction.

### 4.3 Isolated zeros expose the obstruction directly

Set `P_N=0` at one index and `P_n=1/n` elsewhere. The weighted energy is finite
and the liminf is zero. A renewal from `N` would require

\[
 -P_b\ge c\sum_{N\le n<b}w_nP_n,
\]

which is impossible because all later `P_n` are positive. Equivalently,
`Q_N=-cT_N<0`.

## 5. Sharp model realizing renewal

Choose `n_0` so large that `cw_n<1` for `n>=n_0`, set `P_(n_0)=1`, and define

\[
 P_{n+1}=(1-cw_n)P_n.                               \tag{38.7}
\]

Then every term is positive and

\[
 P_n-P_{n+1}=cw_nP_n,
\]

so `b=n+1` is a renewal from every start. Since `sum w_n=infinity`, the product
in (38.7) tends to zero. Telescoping gives

\[
 P_a=c\sum_{n=a}^\infty w_nP_n,
\]

so this model lies exactly on the equality boundary `Q_a=0` at every index.
It demonstrates why the unbounded equality-set clause in Theorem 38.1 is
necessary and sharp.

## 6. Consequence for the RH lane

The adaptive stopping proposal is not a reformulation of the already known
target `liminf P_n=0`. For arbitrary nonnegative data it asserts the much more
rigid family of arithmetic tail inequalities

\[
 \boxed{P_a\ge 2\kappa\sum_{n=a}^\infty
 {\log(1+1/n)\over\log(n+1)}P_n\qquad(a>=n_0),}
\]

together with the exact equality-boundary recurrence. Proving finite stops for
the Mobius approximants would therefore prove zero liminf, but zero liminf by
itself cannot supply those stops. The useful non-tautological target is the
tail Hardy inequality, preferably strict, not an unconstrained search for a
future endpoint.
