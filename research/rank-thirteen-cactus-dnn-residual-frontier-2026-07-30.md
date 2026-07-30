# Exact rank-thirteen cactus DNN residual frontier

**Date:** 2026-07-30

## Scope

This note classifies exactly the cycle-length multisets on which the sharp
cactus DNN lower bound is nonpositive at cyclomatic rank `13`. It does not by
itself prove positivity on either residual family or the rank-thirteen theorem.

Run the fail-closed exact audit, including its hostile mutations, with Python
3.10 or newer:

```bash
python3 research/rank-thirteen-cactus-dnn-residual-frontier-verifier.py
python3 -O research/rank-thirteen-cactus-dnn-residual-frontier-verifier.py
```

## Sharp-DNN reduction

For cycle-block lengths `l_1,...,l_13`, define

```text
epsilon_l = 0                         for even l,
epsilon_l = l tan^2(pi/(2l))          for odd l.
```

A connected rank-thirteen cactus on `n` vertices has `m=n+12`. If `b` is its
number of bridge blocks, block counting gives `b+sum_i l_i=n+12`. The sharp
cactus DNN formula therefore gives

```text
s-(G) <= n+12+sum_i epsilon_(l_i),
sigma(G)=s+(G)-n >= 12-sum_i epsilon_(l_i).              (1)
```

Thus the exact failure set of this estimate is `sum_i epsilon_(l_i)>=12`.

## Exact comparisons

For real `x>=3`, `epsilon_x=x tan^2(pi/(2x))` decreases strictly. With
`u=pi/(2x)`, the derivative of `tan^2(u)/u` has the sign of
`2u-sin(u)cos(u)>0`; since `u` decreases with `x`, the claim follows. Hence
every nontriangle contributes at most

```text
a=epsilon_5=5-2sqrt(5).
```

The required exact inequalities are

```text
0<a<1,             3a<2,             2a>1,
a+epsilon_7<1.                                             (2)
```

After moving radicals to positive sides, the first comparisons have squaring
certificates `20<25`, `4<5`, `169<180`, and `80<81`. For the final comparison,
`cos(pi/7)>2159/2401>7/8` implies `epsilon_7<7/15`, while
`7/15<2sqrt(5)-4=1-a` follows from `(67/30)^2<5`.

## Exhaustive classification

Let `t` be the number of triangles. If `t<=10`, monotonicity and `a<1` show
that `t+(13-t)a` is increasing in `t`, and

```text
sum_i epsilon_(l_i) <= 10+3a < 12.
```

If `t=11`, two nontriangles remain. Their total is less than one if either is
even. If both are odd but not both pentagons, it is at most
`epsilon_5+epsilon_7<1`. The sole residual pair is `PP`, since `2a>1`.

If `t>=12`, the multiset is `T^12Q` for a cycle `Q=C_q`, `q>=3`, and its sum
is `12+epsilon_q>=12`. Conversely every such multiset is residual. Therefore,
up to permutation, the exact frontier is

```text
T^12Q,
T^11PP.
```

The two families are disjoint by triangle count. The companion verifier freezes
this classification with exact `Fraction` and `Q(sqrt(5))` arithmetic and
rejects four hostile ledger mutations. Its certificate SHA-256 is
`afed9ecb78b7def1cf0daf14655730e64f52fe59a1e8a38f1b9f115b5aecce76`;
the verifier-file SHA-256 is
`7da0684ff251c57a6832c5ce5077c76105af3d116eb30532f54007c2a5ec7fa9`.
