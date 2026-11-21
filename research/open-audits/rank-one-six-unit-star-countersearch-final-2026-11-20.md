# Final countersearch: exact obstructions on the rank-`(1,6)` / unit-star lane

Date: 2026-11-20. Status: **NONPROMOTIONAL COUNTERSEARCH REPORT**.

## 1. Verdict and claim boundary

Write

`Phi(X)=s^+(X)=sum_{lambda_i(A_X)>0} lambda_i(A_X)^2`

and `sigma(X)=Phi(X)-|V(X)|`.  The search target was a graph obtained by
joining a connected hostile unicyclic graph `U` to a connected rank-six graph
`R` by one bridge, and, more generally, the unit-star residual assembled from
several such hostile rank-one arms.

The final verdict is deliberately narrow.

* **No graph counterexample was found:** this work does not exhibit any
  admissible graph `G` with `sigma(G)<0`.
* **No exact counterexample was found to the negative-part-resolvent
  certificate** `sigma(R)+rho^2 >= -sigma(U)`.
* Two exact local proof routes do fail:
  1. the standard nonnegative-projector correction alone cannot pay even one
     hostile rank-one arm in the rank-`(1,6)` state; and
  2. the true bridge gain is not uniformly at least `2/3` in that state.
* The unit-star problem therefore remains a **coupled reserve--gain** problem.
  Neither obstruction permits the rank-six reserve to be discarded.

All accepted comparisons below are exact.  Decimal spectral searches run
while hunting for stronger examples were exploratory only and are not used as
certificates in this report.

## 2. Exact unit-star bookkeeping

Delete all physical hull bridges from a unit-star residual.  Denote the
central component by `C`, the rank-one arms by `U_1,...,U_r`, and the bridge
from `U_i` to `C` by `u_i v_i`.  Cyclomatic rank is additive across bridges,
so in total rank seven

`beta(C)=7-r`.                                                   (1)

Deleting the `i`-th bridge leaves a rank-six complement

`R_i=C + {U_j : j != i} + {their bridges}`,                     (2)

and the exact bridge-restoration gain

`Gamma_i=Phi(G)-Phi(R_i)-Phi(U_i)`                              (3)

satisfies

`sigma(G)=sigma(R_i)+Gamma_i-delta_i`,                          (4)

where `delta_i=-sigma(U_i)>0`.  Summing (4) gives

`r sigma(G)=sum_i sigma(R_i)+sum_i Gamma_i-sum_i delta_i`.      (5)

Thus a local inequality involving `Gamma_i` alone is stronger than the actual
need: the missing theorem may trade small gain against positive
`sigma(R_i)`.  The counterfamilies below identify precisely this obstruction.

There is also a joint standard variational certificate.  If

`a_i=(Pi_(>=0)(A(C)))_(v_i v_i)`,
`b_i=(Pi_(>=0)(A(U_i)))_(u_i u_i)`,

then grouping the center only once and compressing all bridge edges gives

`sigma(G) >= sigma(C)-sum_i delta_i+sum_i a_i b_i`.             (6)

The arm summands in (6) have no favorable cross-arm term.  Section 3 proves
that even one such summand can be much smaller than its hostile debit.

## 3. Exact projector-product obstruction

### 3.1 The family

For `r>=1`, let `B_r` consist of `r` pentagons sharing one common vertex `c`,
plus a pendant vertex `u` adjacent to `c`.  Then

`|V(B_r)|=4r+2`, `|E(B_r)|=5r+1`, and `beta(B_r)=r`.             (7)

Partitioning into the center, the `2r` cycle vertices adjacent to it, the
other `2r` cycle vertices, and the leaf gives the divisor

```
D_r = [0  2r 0 1]
      [1   0 1 0]
      [0   1 1 0]
      [1   0 0 0].
```

Its factorization, including all transverse petal modes, is

`chi_(B_r)(x)`
` =(x-1)(x^2-x-1)^(r-1)(x^2+x-1)^r`
`   (x^3-(2r+2)x-1)`.                                         (8)

In particular `det A(B_r)=-1`, so `B_r` is nonsingular and
`Pi_(>=0)=Pi_+`; the obstruction is not manufactured by zero modes.

Let `lambda_r>2` be the unique positive root of

`lambda^3-(2r+2)lambda-1=0`,                                  (9)

and put

`p_r=(Pi_(>=0)(A(B_r)))_(uu)`.                                 (10)

Deleting the leaf from the divisor gives

`x^3-x^2-(2r+1)x+2r`.                                         (11)

Taking residues of the exact rooted resolvent and eliminating `r` by (9)
gives

`p_r=(3lambda_r^3+3lambda_r^2+2lambda_r+1)`
`    /[(2lambda_r^3+1)(lambda_r^2+lambda_r+1)]`.               (12)

Moreover,

`p_r-1/(r+2)`
` =-[(lambda_r-1)(lambda_r^2-lambda_r-1)`
`     (lambda_r^3+3lambda_r^2+2lambda_r+1)]`
`   /[(2lambda_r^3+1)(lambda_r^2+lambda_r+1)`
`     (lambda_r^3+2lambda_r-1)] < 0.                           (13)

Every factor after the minus sign is positive because `lambda_r>2`.
Consequently, for the rank-`(1,6)` pair rooted at the two pendant vertices,

`p_1 p_6 < 1/(3*8)=1/24`.                                     (14)

### 3.2 The hostile debit is larger

The graph `B_1` is a pentagon with one pendant leaf and

`chi_(B_1)(x)=(x-1)(x^2+x-1)(x^3-4x-1)`.                      (15)

If `lambda` is the positive root of `x^3-4x-1`, then

`delta(B_1)=-sigma(B_1)=(7+sqrt(5))/2-lambda^2`.               (16)

The cubic is increasing on `[2,infinity)`, and

`(423/200)^3-4(423/200)-1=6967/8000000>0`,                    (17)

so `lambda<423/200`.  Also `sqrt(5)>559/250`, since
`5*250^2-559^2=19>0`.  Therefore

`delta(B_1)`
` >(7+559/250)/2-(423/200)^2`
` =5791/40000 > 1/7`.                                         (18)

Combining (14) and (18),

`p_1 p_6 < 1/24 < 1/7 < delta(B_1)`.                           (19)

This is an exact rank-`(1,6)` obstruction to paying a hostile arm with the
standard nonnegative-projector correction alone.  It is **not** a graph
counterexample: joining the marked `B_1` and `B_6` gives a cactus, and the
large rank-six reserve has intentionally been thrown away in the failed local
route.  In a multiarm unit-star, (19) likewise says that the additive terms in
(6) cannot be charged arm-by-arm without using `sigma(C)` or another coupled
reserve.

## 4. Exact obstruction to a universal `2/3` bridge gain

### 4.1 The family and characteristic polynomials

For `t>=1`, form `H_t` from a pentagon by attaching `t` leaves to one cycle
vertex `a`, and mark one of those leaves `u`.  Let `K=K_5`, mark a vertex `v`,
and add the bridge `uv`; call the result `G_t`.  Then

`beta(H_t)=1`, `beta(K)=6`, and `Phi(K)=16`.                    (20)

Define

`Gamma_t=Phi(G_t)-Phi(H_t)-Phi(K)`.                             (21)

Put

`q(x)=x^2+x-1`,

`p_t(x)=x^4-x^3-(t+3)x^2+(t+2)x+t`,                            (22)

and

`g_t(x)=x^7-4x^6-(t+5)x^5+(4t+19)x^4+(3t+5)x^3`
`       -(11t+15)x^2+(4-2t)x+3t-3`.                            (23)

Equitable-quotient expansion gives

`chi_(H_t)(x)=x^(t-1) q(x) p_t(x)`,                            (24)

and, for `t>=2`,

`chi_(G_t)(x)=x^(t-2)(x+1)^3 q(x) g_t(x)`.                     (25)

(The formal `x^(-1)` at `t=1` cancels a factor `x` of `g_1`.)

### 4.2 A finite exact witness

At `t=10`, Sturm sequences isolate the two positive roots of `p_10` in

`(15215/10000,15216/10000)`,
`(35011/10000,35012/10000)`,                                   (26)

and the four positive roots of `g_10` in

`(4476/10000,4477/10000)`,
`(15233/10000,15234/10000)`,
`(34930/10000,34931/10000)`,
`(40636/10000,40637/10000)`.                                  (27)

The common positive root of `q` cancels from (21); zeros and the factor
`(x+1)^3` add no positive-square energy.  Squaring the rational interval
endpoints in the adverse directions therefore gives the two-sided exact
certificate

`66101461/100000000 < Gamma_10`
`                         < 66392469/100000000 < 2/3`.          (28)

The final gap is

`2/3-66392469/100000000=822593/300000000>0`.                   (29)

Hence the full one-edge gain itself is not uniformly at least `2/3` in the
rank-`(1,6)` state.  Notice also that (28) proves this particular finite gain
is positive and greater than `3/5`; this finite member is not a
`sigma(G)<0` counterexample and does not threaten the much smaller pentagon
debit `sqrt(5)-2`.

### 4.3 Persistent limiting obstruction

Let

`f(x)=x^3-3x^2-5x+3`,                                         (30)

and let `alpha` be its unique negative root.  Exact root tracking from

`p_t(x)/t -> -(x^2-x-1)`,
`g_t(x)/t -> -(x^2-x-1)f(x)`                                  (31)

must also account for one positive and one negative escaping root in each
polynomial.  With `e=t^(-1/2)` and `x=z/e`, both positive escaping roots have

`z=1+e^2+O(e^3)`,                                              (32)

so their squared contributions differ by `o(1)`.  Vieta's identities for
`f` then give

`lim_(t->infinity) Gamma_t=3-alpha^2`.                          (33)

Descartes' rule gives one negative root.  The exact signs

`f(-77/50)=-8383/125000<0`,
`f(-3/2)=3/8>0`                                                (34)

show

`-77/50<alpha<-3/2`,                                          (35)

and hence

`3-alpha^2>1571/2500>3/5`.                                    (36)

On the other side,

`f(-sqrt(7/3))=-4+8sqrt(21)/9>0`,                              (37)

because `1344=64*21>36^2=1296`, whereas `f(-2)=-7<0`.  Uniqueness
of the negative root yields `alpha^2>7/3`, so

`3-alpha^2<2/3`.                                               (38)

Thus

`3/5 < lim Gamma_t < 2/3`.                                    (39)

The family persistently rules out a `2/3` or one-unit bridge credit, but it
does not rule out a debit-scale gain.

## 5. Scope relative to the negative-part-resolvent certificate

Let `A_-` denote the positive-semidefinite negative part.  For a single bridge
between marked `U,u` and `R,v`, form

`Z=-(A(U)_- direct_sum A(R)_-) + e_u e_v^T+e_v e_u^T`,         (40)

with coordinates understood across the two blocks, and let

`rho=max(0,lambda_max(Z))`.                                    (41)

The associated sufficient route is

`sigma(R)+rho^2 >= -sigma(U)`.                                 (42)

Nothing above refutes (42):

* (19) concerns the standard nonnegative-projector product, not `rho^2`;
* (28) concerns the actual bridge gain and only disproves a much larger
  proposed universal gain; and
* neither family has `sigma(G)<0`.

Exploratory finite and random searches performed during this countersearch
found no violation of (42), but those computations used floating-point
spectral discovery and are **not proof** of any bounded theorem.  They are not
promoted to a certificate here.

## 6. Final stopping point

The strongest exact conclusion is therefore an obstruction, not a
counterexample to the graph theorem:

1. projector leverage alone can be strictly smaller than one hostile arm's
   debit, even for a nonsingular exact rank-`(1,6)` pair;
2. full bridge gain alone has no universal `2/3` lower bound; and
3. a successful unit-star proof must retain and couple the rank-six reserves
   in (5), or prove the stronger negative-part-resolvent tradeoff (42).

No `STATE` or publication file is changed by this report.

## 7. Exact reproduction

Run

```text
python research/nonnegative-projector-c5-bouquet-counterfamily-verifier.py
uv run --with sympy python research/rank-one-six-bridge-gain-obstruction-verifier.py
python research/rank-one-six-unit-star-countersearch-final-verifier.py
```

The first and third scripts are dependency-free.  The second uses SymPy for
exact polynomial identities and Sturm counts.  Any decimal printed by that
script is explicitly orientation-only and is not an accepted comparison.
