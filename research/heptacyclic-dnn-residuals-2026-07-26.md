# Exact sharp-DNN residual cycle multisets for connected heptacyclic cacti

**Date:** 2026-07-26

## Scope and status

This note performs only the cycle-length classification left by the sharp
cactus DNN estimate. It makes no theorem claim about the sign of `sigma(G)` on
the residual families. A multiset listed below is not asserted to be a
counterexample; it is only a multiset on which this DNN lower bound by itself
is nonpositive.

All graphs under discussion are finite and simple. Write

```text
s+(G) = sum_{lambda_i>0} lambda_i^2,
s-(G) = sum_{lambda_i<0} lambda_i^2,
sigma(G) = s+(G)-|V(G)|.
```

Let `G` be a connected heptacyclic cactus, let `n=|V(G)|`, and let its seven
cyclic blocks have lengths `l_1,...,l_7`. Thus

```text
m=|E(G)|=n+6.
```

## The exact residual inequality

For every integer `l>=3`, put

```text
epsilon_l = 0                                  if l is even,
epsilon_l = l tan^2(pi/(2l))                   if l is odd.
```

If `b` is the number of bridge blocks, cactus block counting gives

```text
b + sum_{i=1}^7 l_i = m = n+6.
```

The sharp cactus DNN constant and its spectral consequence give

```text
s-(G) <= b + sum_{i=1}^7 (l_i+epsilon_{l_i})
       = n+6 + sum_{i=1}^7 epsilon_{l_i}.
```

Since `s+(G)+s-(G)=2m=2n+12`, it follows that

```text
sigma(G) >= 6 - sum_{i=1}^7 epsilon_{l_i}.             (1)
```

Thus (1) has a strictly positive right-hand side exactly when

```text
sum_{i=1}^7 epsilon_{l_i} < 6.                         (2)
```

The residual multisets are therefore exactly those for which the sum in (2)
is at least `6`.

## Exact comparison ledger

The sequence `epsilon_l` is strictly decreasing through odd integers `l>=3`.
Indeed, on writing `u=pi/(2x)`, this is equivalent to the strict increase of
`tan^2(u)/u` in `u`. The sign of its derivative reduces to

```text
2u tan(u) sec^2(u) - tan^2(u) > 0
    <=> 2u > sin(u)cos(u),
```

which holds for `0<u<=pi/6`.

The first two odd values are

```text
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5) =: a.                          (3)
```

The exact comparisons needed for the classification are

```text
0 < a < 1,
3a < 2,
2a > 1,
epsilon_5 + epsilon_7 < 1.                            (4)
```

Here `a>0` is equivalent to `2sqrt(5)<5`, certified by `20<25`, while `a<1`
follows from `2<sqrt(5)`, whose square is `4<5`. The next two comparisons have
the exact certificates

```text
3a < 2 <=> 13 < 6sqrt(5),    with 169 < 180,
2a > 1 <=> 4sqrt(5) < 9,     with 80 < 81.
```

For the final comparison, `pi<22/7` and `cos x>1-x^2/2` for `x>0` give

```text
cos(pi/7)
  > 1-(1/2)(22/49)^2
  = 2159/2401
  > 7/8,
```

where the last inequality is `17272>16807`. Hence

```text
epsilon_7
  = 7(1-cos(pi/7))/(1+cos(pi/7))
  < 7/15
  < 2sqrt(5)-4
  = 1-epsilon_5.
```

The middle strict inequality is equivalent to `67/30<sqrt(5)`, and squaring
its positive sides gives `4489<4500`. This proves every comparison in (4)
without numerical approximation.

## Exhaustive classification

Let `t` be the number of triangles in the seven-element cycle multiset. Every
nontriangle contributes at most `a`: an even cycle contributes zero, while an
odd nontriangle has length at least five and odd-index monotonicity applies.

### At most four triangles

Because `0<a<1`, for `t<=4` one has

```text
sum_i epsilon_{l_i}
  <= t+(7-t)a
  <= 4+3a
  < 6.                                                  (5)
```

Thus no multiset with at most four triangles is residual.

### Exactly five triangles

Write the two remaining lengths as `p,q`, where `3<p<=q`.

- If either length is even, then `epsilon_p+epsilon_q<=a<1`.
- If both are odd and `(p,q)!=(5,5)`, then `p>=5` and `q>=7`, so
  `epsilon_p+epsilon_q<=epsilon_5+epsilon_7<1`.
- If `p=q=5`, then `epsilon_p+epsilon_q=2a>1`.

Consequently the unique residual multiset with exactly five triangles is

```text
{3,3,3,3,3,5,5}.                                      (R1)
```

Its epsilon sum and the right-hand side of (1) are exactly

```text
5+2epsilon_5 = 15-4sqrt(5) > 6,
6-(15-4sqrt(5)) = 4sqrt(5)-9 < 0.
```

Both signs are equivalent to `2a>1`.

### At least six triangles

Every such multiset has the form

```text
{3,3,3,3,3,3,q},  q>=3.                               (R2)
```

Conversely, each member of (R2) satisfies

```text
sum_i epsilon_{l_i} = 6+epsilon_q >= 6,
6-sum_i epsilon_{l_i} = -epsilon_q <= 0.
```

More precisely, the right-hand side is zero when `q` is even and is
`-epsilon_q<0` when `q` is odd. The parameter value `q=3` is the
seven-triangle multiset.

## Classification returned

Up to permutation, the complete set of seven-cycle-length multisets for which
the sharp-DNN estimate

```text
sigma(G) >= 6-sum_i epsilon_{l_i}
```

does not yield a strict positive lower bound is exactly

```text
{3,3,3,3,3,5,5},
{3,3,3,3,3,3,q} for an arbitrary integer q>=3.
```

This is one isolated multiset and one one-parameter family. They are disjoint:
the isolated multiset has exactly five triangles, whereas every member of the
parametric family has at least six. For every other seven-cycle multiset, the
right-hand side of (1) is strictly positive. This is only an exact
classification of the sharp-DNN residuals and makes no theorem claim about
`sigma(G)` on either residual family.
