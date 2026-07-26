# Exact sharp-DNN residual cycle multisets for connected hexacyclic cacti

**Date:** 2026-07-26

## Scope and status

This note performs only the cycle-length classification left by the sharp
cactus DNN estimate. It does not assert a theorem about the sign of
`sigma(G)` on the residual families. In particular, a multiset appearing in
the classification below is not a counterexample: it is merely a multiset for
which this DNN lower bound alone is nonpositive.

All graphs under discussion are finite and simple. Write

`s+(G) = sum_{lambda_i>0} lambda_i^2`,
`s-(G) = sum_{lambda_i<0} lambda_i^2`, and
`sigma(G) = s+(G)-|V(G)|`.

Let `G` be a connected hexacyclic cactus, let `n=|V(G)|`, and let its six
cyclic blocks have lengths `l_1,...,l_6`. Thus `m=|E(G)|=n+5`.

## The exact residual inequality

For an integer `l>=3`, put

```text
epsilon_l = 0                                  if l is even,
epsilon_l = l tan^2(pi/(2l))                   if l is odd.
```

If `b` is the number of bridge blocks, cactus block counting gives

```text
b + sum_{i=1}^6 l_i = m = n+5.
```

The sharp cactus DNN constant and its spectral consequence give

```text
s-(G) <= b + sum_{i=1}^6 (l_i+epsilon_{l_i})
       = n+5 + sum_{i=1}^6 epsilon_{l_i}.
```

Since `s+(G)+s-(G)=2m=2n+10`, it follows exactly that

```text
sigma(G) >= 5 - sum_{i=1}^6 epsilon_{l_i}.             (1)
```

Consequently, (1) is a strict positive lower bound precisely when

```text
sum_{i=1}^6 epsilon_{l_i} < 5.                         (2)
```

The task is therefore to classify the complementary multisets, for which the
sum is at least `5`.

## Exact comparison ledger

The odd-indexed sequence `epsilon_l` is strictly decreasing for odd
`l>=3`. Indeed, on writing `u=pi/(2x)`, monotonicity reduces to the strict
increase of `tan^2(u)/u` in `u`; its derivative is positive because

```text
2u tan(u) sec^2(u) - tan^2(u) > 0
    <=> 2u > sin(u)cos(u).
```

The first two odd values are

```text
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5).                                (3)
```

Set `a=epsilon_5`. The comparisons needed below are all strict and symbolic:

```text
3a < 2,
```

because this is equivalent to `13<6sqrt(5)`, and `169<180`; whereas

```text
2a > 1,
```

because this is equivalent to `4sqrt(5)<9`, and `80<81`.

We also need the sharp separation after the pair of pentagons:

```text
epsilon_5 + epsilon_7 < 1.                             (4)
```

Here is a rationally certified derivation. From `pi<22/7` and
`cos x>1-x^2/2` for `x>0`,

```text
cos(pi/7) > 1-(1/2)(22/49)^2 > 7/8.
```

Therefore

```text
epsilon_7
 = 7(1-cos(pi/7))/(1+cos(pi/7))
 < 7/15
 < 2sqrt(5)-4
 = 1-epsilon_5.
```

The middle inequality is exact: it is equivalent to
`67/30<sqrt(5)`, whose square is `4489<4500`. This proves (4) without
decimal approximation.

## Exhaustive classification

Let `t` be the number of entries equal to `3` in the six-element cycle
multiset. Every nontriangle contributes at most `a`, because an even length
contributes zero and an odd nontriangle has length at least five.

### At most three triangles

Since `a<1`, for `t<=3` one has

```text
sum_i epsilon_{l_i} <= t+(6-t)a <= 3+3a < 5.
```

Thus the DNN bound is strict for every multiset with at most three triangles.

### Exactly four triangles

Write the remaining lengths as `p,q`, with `3<p<=q`.

- If either length is even, then `epsilon_p+epsilon_q<=a<1`.
- If both are odd but `{p,q}!={5,5}`, then `p>=5`, `q>=7`, and monotonicity
  together with (4) gives
  `epsilon_p+epsilon_q<=epsilon_5+epsilon_7<1`.
- If `p=q=5`, then

```text
sum_i epsilon_{l_i}
 = 4+2epsilon_5
 = 14-4sqrt(5)
 > 5,
```

  where the last inequality is exactly `2epsilon_5>1`.

Hence the unique four-triangle residual multiset is

```text
{3,3,3,3,5,5}.                                        (R1)
```

Its residual right-hand side in (1) is

```text
5-(14-4sqrt(5)) = 4sqrt(5)-9 < 0.
```

### At least five triangles

Every such multiset can be written

```text
{3,3,3,3,3,q},  q>=3.                                 (R2)
```

Conversely, every multiset in (R2) satisfies

```text
sum_i epsilon_{l_i} = 5+epsilon_q >= 5,
```

so the lower bound (1) is not strict. More precisely:

- for even `q`, its right-hand side is exactly `0`;
- for odd `q`, its right-hand side is `-epsilon_q<0`.

The value `q=3` includes the six-triangle multiset.

## Classification returned

Up to permutation, the complete set of six-cycle-length multisets for which
the sharp-DNN lower bound

```text
sigma(G) >= 5-sum_i epsilon_{l_i}
```

does not give a strict positive bound is exactly

```text
{3,3,3,3,5,5},
{3,3,3,3,3,q} for an arbitrary integer q>=3.
```

These are one isolated multiset and one one-parameter family. The two parts
are disjoint: the isolated multiset has exactly four triangles, while every
member of the parametric family has at least five.

Equivalently, the bound is strict for every other multiset of six cycle
lengths. This is only an exact reduction of the sharp-DNN estimate; settling
`sigma(G)` on (R1) and (R2) requires arguments beyond that estimate.
