# Exact rank-twelve cactus DNN residual frontier

**Date:** 2026-07-30

## Scope

This note classifies exactly the cycle-length multisets on which the sharp
cactus DNN lower bound is nonpositive at cyclomatic rank `12`. It proves only
that frontier calculation. It does not prove positivity on either residual
family and does not prove the rank-twelve cactus theorem.

The fail-closed companion audit uses only `Fraction` and exact arithmetic in
`Q(sqrt(5))`:

```bash
python3 research/rank-twelve-cactus-dnn-residual-frontier-verifier.py
python3 -O research/rank-twelve-cactus-dnn-residual-frontier-verifier.py
```

## Sharp-DNN reduction

Let the twelve cyclic blocks have lengths `l_1,...,l_12`, and define

```text
epsilon_l = 0                         for even l,
epsilon_l = l tan^2(pi/(2l))          for odd l.
```

For a connected rank-twelve cactus on `n` vertices, `m=n+11`. If `b` is the
number of bridge blocks, cactus block counting and the sharp DNN estimate give

```text
s-(G) <= b + sum_i(l_i+epsilon_{l_i})
       = n+11+sum_i epsilon_{l_i}.
```

Since `s+(G)+s-(G)=2m=2n+22`, the surplus `sigma(G)=s+(G)-n` obeys

```text
sigma(G) >= 11-sum_i epsilon_{l_i}.                    (1)
```

Thus the exact failure set of this estimate is `sum_i epsilon_{l_i}>=11`.

## Exact monotonicity

The function `epsilon_x=x tan^2(pi/(2x))` decreases strictly for real `x>=3`.
Put `u=pi/(2x)`, so `0<u<=pi/6` and, apart from the positive factor `pi/2`,
the function is `tan^2(u)/u`. Multiplication by positive factors gives

```text
d/du [tan^2(u)/u] > 0
  <=> 2u tan(u)sec^2(u)-tan^2(u) > 0
  <=> 2u > sin(u)cos(u).
```

Here `sin(u)cos(u)<u<2u`, strictly. Hence the expression increases with `u`;
because `u` decreases with `x`, `epsilon_x` decreases strictly with `x`. In
particular every nontriangle contributes at most

```text
a := epsilon_5 = 5-2sqrt(5).
```

## Exact inequalities

The classification uses

```text
0<a<1,             3a<2,             2a>1,             a+epsilon_7<1.    (2)
```

The first three statements have positive-side squaring certificates

```text
a>0   <=> 2sqrt(5)<5       because 20<25,
a<1   <=> 2<sqrt(5)        because 4<5,
3a<2  <=> 13<6sqrt(5)      because 169<180,
2a>1  <=> 4sqrt(5)<9       because 80<81.
```

For the last statement, `pi<22/7` and `cos x>1-x^2/2` for `x>0` imply

```text
cos(pi/7)>2159/2401>7/8.
```

The half-angle identity and the strict decrease of `(1-c)/(1+c)` yield

```text
epsilon_7=7(1-cos(pi/7))/(1+cos(pi/7))<7/15.
```

Finally `7/15<2sqrt(5)-4=1-a` because
`(67/30)^2=4489/900<5`. This proves `a+epsilon_7<1` exactly.

## Exhaustive classification

Let `t` be the number of triangles.

If `t<=9`, monotonicity and `a<1` show that `t+(12-t)a` increases with `t`, so

```text
sum_i epsilon_{l_i} <= 9+3a < 11.
```

These multisets are DNN-positive.

Suppose `t=10`, and write the two nontriangle lengths as `p<=q`. If one is
even, their total contribution is at most `a<1`. If both are odd and are not
both five, then `p>=5`, `q>=7`, and exact monotonicity gives
`epsilon_p+epsilon_q<=epsilon_5+epsilon_7<1`. The unique remaining pair is
`p=q=5`, for which `epsilon_p+epsilon_q=2a>1`. Therefore the unique residual
with exactly ten triangles is

```text
T^10PP.
```

If `t>=11`, the multiset is `T^11Q` for some cycle `Q=C_q`, `q>=3`. Its sum is
`11+epsilon_q>=11`; equality occurs exactly for even `q`. Conversely every
such multiset is residual.

Therefore, up to permutation, the sharp-DNN rank-twelve frontier is exactly

```text
T^11Q,
T^10PP.
```

These families are disjoint by triangle count. A nonpositive DNN lower bound
does not imply a nonpositive spectral surplus; no positivity or counterexample
claim is made for either family.
