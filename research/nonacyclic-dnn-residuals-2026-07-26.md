# Exact sharp-DNN residual cycle multisets for rank-9 cacti

**Date:** 2026-07-26

## Scope and status

This note only classifies the cycle-length multisets on which the sharp cactus
DNN lower bound is nonpositive. It makes no theorem claim about the actual sign
of `sigma(G)` on those multisets. In particular, no listed multiset is asserted
to be a counterexample.

All graphs are finite and simple. Write

```text
s+(G) = sum_{lambda_i>0} lambda_i^2,
s-(G) = sum_{lambda_i<0} lambda_i^2,
sigma(G) = s+(G)-|V(G)|.
```

Let `G` be a connected cactus of cyclomatic rank `9`, let `n=|V(G)|`, and let
its nine cyclic blocks have lengths `l_1,...,l_9`. Thus

```text
m=|E(G)|=n+8.
```

## Exact sharp-DNN inequality

For every integer `l>=3`, define

```text
epsilon_l = 0                                  if l is even,
epsilon_l = l tan^2(pi/(2l))                   if l is odd.
```

If `b` is the number of bridge blocks, cactus block counting gives

```text
b + sum_{i=1}^9 l_i = m = n+8.
```

The sharp cactus DNN constant and its spectral consequence give

```text
s-(G) <= b + sum_{i=1}^9 (l_i+epsilon_{l_i})
       = n+8 + sum_{i=1}^9 epsilon_{l_i}.
```

Since `s+(G)+s-(G)=2m=2n+16`, it follows exactly that

```text
sigma(G) >= 8 - sum_{i=1}^9 epsilon_{l_i}.              (1)
```

Consequently, the sharp-DNN estimate itself gives a strict positive lower
bound exactly when

```text
sum_{i=1}^9 epsilon_{l_i} < 8.                          (2)
```

The residual problem is purely algebraic: classify the nine-element multisets
for which the sum in (2) is at least `8`.

## Exact symbolic comparisons

The sequence `epsilon_l` is strictly decreasing through odd integers `l>=3`.
Indeed, put `u=pi/(2x)`. Up to a positive constant,
`x tan^2(pi/(2x))=tan^2(u)/u`, and

```text
d/du (tan^2(u)/u) > 0
    <=> 2u tan(u) sec^2(u)-tan^2(u) > 0
    <=> 2u > sin(u)cos(u).
```

The last inequality is strict for `0<u<=pi/6`. Hence the original expression
decreases strictly as `x` increases.

The first two odd values are

```text
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5) =: a.
```

The complete comparison ledger needed below is

```text
0 < a < 1,                                             (3)
3a < 2,                                                (4)
2a > 1,                                                (5)
epsilon_5 + epsilon_7 < 1.                             (6)
```

All four comparisons admit exact certificates:

```text
a>0       <=> 2sqrt(5)<5,       certified by 20<25,
a<1       <=> 2<sqrt(5),        certified by 4<5,
3a<2      <=> 13<6sqrt(5),      certified by 169<180,
2a>1      <=> 4sqrt(5)<9,       certified by 80<81.
```

For (6), use `pi<22/7` and `cos x>1-x^2/2` for `x>0`:

```text
cos(pi/7)
  > 1-(1/2)(22/49)^2
  = 2159/2401
  > 7/8,
```

where the final rational comparison is `17272>16807`. Therefore

```text
epsilon_7
  = 7(1-cos(pi/7))/(1+cos(pi/7))
  < 7/15
  < 2sqrt(5)-4
  = 1-epsilon_5.
```

The remaining strict comparison is exact:

```text
7/15 < 2sqrt(5)-4
    <=> 67/30 < sqrt(5),
```

and squaring its positive sides gives `4489<4500`. This proves (6) without a
decimal approximation.

## Exhaustive rank-9 classification

Let `t` be the number of triangles in the nine-cycle multiset. Every
nontriangle contributes at most `a`: an even cycle contributes zero, while an
odd nontriangle has length at least five and odd-index monotonicity applies.

### At most six triangles

For `t<=6`, using `a<1` and (4),

```text
sum_i epsilon_{l_i}
  <= t+(9-t)a
  <= 6+3a
  < 8.
```

Thus no multiset with at most six triangles is residual.

### Exactly seven triangles

Write the remaining lengths as `p,q`, with `3<p<=q`.

- If either length is even, then
  `epsilon_p+epsilon_q<=a<1`.
- If both are odd and `(p,q)!=(5,5)`, then `p>=5`, `q>=7`, so monotonicity and
  (6) give `epsilon_p+epsilon_q<=epsilon_5+epsilon_7<1`.
- If `p=q=5`, then (5) gives `epsilon_p+epsilon_q=2a>1`.

Hence the unique residual multiset with exactly seven triangles is

```text
{3,3,3,3,3,3,3,5,5}.                                  (R1)
```

Its epsilon sum and the right-hand side of (1) are exactly

```text
7+2epsilon_5 = 17-4sqrt(5) > 8,
8-(17-4sqrt(5)) = 4sqrt(5)-9 < 0.
```

Both signs are the comparison `2a>1` in equivalent forms.

### At least eight triangles

Every such multiset has the form

```text
{3,3,3,3,3,3,3,3,q},  q>=3.                            (R2)
```

Conversely, every member of (R2) has

```text
sum_i epsilon_{l_i} = 8+epsilon_q >= 8,
8-sum_i epsilon_{l_i} = -epsilon_q <= 0.
```

The lower-bound value is exactly zero when `q` is even and is strictly
negative when `q` is odd. The parameter value `q=3` is the all-triangle
nine-cycle multiset.

## Rank-9 result of the calculation

Up to permutation, the complete set of rank-9 cycle-length multisets for which
the sharp-DNN bound (1) does not itself give `sigma(G)>0` is

```text
{3,3,3,3,3,3,3,5,5},
{3,3,3,3,3,3,3,3,q} for an arbitrary integer q>=3.
```

Writing `T=C_3`, `P=C_5`, and `Q=C_q`, these are exactly

```text
T^7 P P,
T^8 Q.
```

The two classes are disjoint: the isolated multiset has exactly seven
triangles, while every member of the parametric family has at least eight.
Every other rank-9 cycle multiset makes the right-hand side of (1) strictly
positive.

## All-rank pattern check

The same calculation is independent of rank. Let `r>=2`, and let `k` be the
number of nontriangular cycles in an `r`-cycle multiset. The rank-`r` DNN bound
is

```text
sigma(G) >= r-1-sum_{i=1}^r epsilon_{l_i}.              (7)
```

Since every nontriangle contributes at most `a`,

```text
sum_i epsilon_{l_i} <= (r-k)+ka = r-k(1-a).
```

If the right-hand side of (7) is nonpositive, then necessarily

```text
k(1-a) <= 1.                                           (8)
```

Comparison `3a<2` is exactly `3(1-a)>1`, so (8) forces `k<=2`.

- For `k=0` or `k=1`, the multiset is `T^(r-1)Q`, allowing `Q=T`.
- For `k=2`, the two nontriangle excesses must sum to at least one. An even
  cycle contributes zero. Among two odd nontriangles, monotonicity and
  `epsilon_5+epsilon_7<1` exclude every pair except `(5,5)`, while `2a>1`
  retains `(5,5)`. This gives `T^(r-2)PP`.

Conversely, the two displayed patterns really are residual for the DNN
calculation:

```text
T^(r-1)Q:   (r-1)-sum epsilon = -epsilon_q <= 0,
T^(r-2)PP:  (r-1)-sum epsilon = 1-2a = 4sqrt(5)-9 < 0.
```

Thus the rank-9 answer is the `r=9` instance of the exact all-rank sharp-DNN
pattern

```text
T^(r-1)Q  or  T^(r-2)PP,  r>=2.
```

This final statement remains only a classification of where the sharp-DNN
lower bound fails to be strictly positive. It does not assert the sign of the
actual spectral surplus on either residual family and is not a theorem claim
about rank-9 or all-rank cacti.
