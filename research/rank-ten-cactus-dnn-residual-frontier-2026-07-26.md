# Exact rank-10 cactus DNN residual frontier

**Date:** 2026-07-26

## Scope

This note performs only the symbolic sharp-DNN calculation for connected
cacti of cyclomatic rank `10`. It identifies exactly the cycle-length
multisets on which that lower bound is nonpositive. It makes no theorem claim
about the actual sign of the spectral surplus on either residual family, and
it does not identify counterexamples.

Write

```text
s+(G) = sum_{lambda_i>0} lambda_i^2,
s-(G) = sum_{lambda_i<0} lambda_i^2,
sigma(G) = s+(G)-|V(G)|.
```

Let `G` be a connected rank-`10` cactus on `n` vertices, with cyclic-block
lengths `l_1,...,l_10`. Then

```text
m=|E(G)|=n+9.
```

## Sharp-DNN lower bound

For every integer `l>=3`, set

```text
epsilon_l = 0                                  if l is even,
epsilon_l = l tan^2(pi/(2l))                   if l is odd.
```

If `b` is the number of bridge blocks, block counting gives

```text
b + sum_{i=1}^10 l_i = m = n+9.
```

The sharp cactus DNN constant gives

```text
s-(G) <= b + sum_{i=1}^10 (l_i+epsilon_{l_i})
       = n+9 + sum_{i=1}^10 epsilon_{l_i}.
```

Since `s+(G)+s-(G)=2m=2n+18`, one obtains

```text
sigma(G) >= 9 - sum_{i=1}^10 epsilon_{l_i}.              (1)
```

Thus the sharp-DNN estimate itself is strictly positive exactly when

```text
sum_{i=1}^10 epsilon_{l_i} < 9.                          (2)
```

The residual frontier consists precisely of the ten-cycle multisets for
which the sum in (2) is at least `9`.

## Symbolic comparison ledger

The values `epsilon_l` decrease strictly as `l` runs through the odd integers
`l>=3`. To see this without numerical approximation, put `u=pi/(2x)`. Up to a
positive constant,

```text
x tan^2(pi/(2x)) = tan^2(u)/u.
```

For `0<u<=pi/6`,

```text
d/du (tan^2(u)/u) > 0
    <=> 2u tan(u) sec^2(u)-tan^2(u) > 0
    <=> 2u > sin(u)cos(u),
```

and the last inequality follows strictly from `sin(u)<u` and
`cos(u)<=1`. Since `u` decreases with `x`, the original expression decreases
strictly with `x`.

The first two odd values are

```text
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5) =: a.
```

The required comparisons are

```text
0 < a < 1,                                             (3)
3a < 2,                                                (4)
2a > 1,                                                (5)
epsilon_5 + epsilon_7 < 1.                             (6)
```

The first three have exact squaring certificates:

```text
a>0       <=> 2sqrt(5)<5,       certified by 20<25,
a<1       <=> 2<sqrt(5),        certified by 4<5,
3a<2      <=> 13<6sqrt(5),      certified by 169<180,
2a>1      <=> 4sqrt(5)<9,       certified by 80<81.
```

For (6), use `pi<22/7` and `cos(x)>1-x^2/2` for `x>0`:

```text
cos(pi/7)
  > 1-(1/2)(22/49)^2
  = 2159/2401
  > 7/8,
```

where the last comparison is `17272>16807`. Hence

```text
epsilon_7
  = 7(1-cos(pi/7))/(1+cos(pi/7))
  < 7/15
  < 2sqrt(5)-4
  = 1-epsilon_5.
```

The remaining comparison is also certified symbolically:

```text
7/15 < 2sqrt(5)-4
    <=> 67/30 < sqrt(5),
```

whose positive sides may be squared, giving `4489<4500`. This proves (6).

## Exhaustive rank-10 classification

Let `t` be the number of triangles among the ten cyclic blocks. Every
nontriangle contributes at most `a`: an even cycle contributes zero, and an
odd nontriangle has length at least five.

### At most seven triangles

Because `a<1`, the expression `t+(10-t)a` increases with `t`. Therefore, for
`t<=7`,

```text
sum_i epsilon_{l_i}
  <= t+(10-t)a
  <= 7+3a
  < 9
```

by (4). No multiset with at most seven triangles is residual.

### Exactly eight triangles

Write the remaining lengths as `p,q`, where `3<p<=q`.

- If either length is even, then
  `epsilon_p+epsilon_q<=a<1`.
- If both are odd and `(p,q)!=(5,5)`, then `p>=5` and `q>=7`, so monotonicity
  and (6) give
  `epsilon_p+epsilon_q<=epsilon_5+epsilon_7<1`.
- If `p=q=5`, then (5) gives
  `epsilon_p+epsilon_q=2a>1`.

Thus the unique residual multiset with exactly eight triangles is

```text
{3,3,3,3,3,3,3,3,5,5}.                                (R1)
```

Its epsilon sum and DNN lower-bound value are exactly

```text
8+2epsilon_5 = 18-4sqrt(5) > 9,
9-(18-4sqrt(5)) = 4sqrt(5)-9 < 0.
```

Both signs are equivalent to `2a>1`.

### At least nine triangles

Every such multiset has the form

```text
{3,3,3,3,3,3,3,3,3,q},  q>=3.                          (R2)
```

Conversely, each member of (R2) satisfies

```text
sum_i epsilon_{l_i} = 9+epsilon_q >= 9,
9-sum_i epsilon_{l_i} = -epsilon_q <= 0.
```

The lower-bound value is zero exactly when `q` is even and is strictly
negative when `q` is odd. The choice `q=3` includes the all-triangle
rank-`10` multiset.

## Frontier

Up to permutation, the complete rank-`10` residual frontier of the sharp-DNN
calculation is

```text
{3,3,3,3,3,3,3,3,3,q},  q>=3,
{3,3,3,3,3,3,3,3,5,5}.
```

Writing `T=C_3`, `P=C_5`, and `Q=C_q`, this confirms exactly

```text
T^9 Q,
T^8 P P.
```

The families are disjoint: `T^8PP` has exactly eight triangles, whereas every
member of `T^9Q` has at least nine. Every other rank-`10` cycle-length
multiset makes the right-hand side of (1) strictly positive.

This is only a classification of the failure set of the sharp-DNN lower bound.
It does not assert that `sigma(G)<=0`, or make any theorem claim about actual
rank-`10` cacti, on either residual family.
