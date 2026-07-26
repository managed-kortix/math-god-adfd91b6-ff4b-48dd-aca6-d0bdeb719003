# Exact sharp-DNN residual cycle multisets for connected octacyclic cacti

**Date:** 2026-07-26

## Scope and status

This note performs only the exact cycle-length classification left by the sharp
cactus DNN estimate. It makes no theorem claim about the sign of `sigma(G)` on
the residual families. A multiset listed below is not asserted to be a
counterexample; it is only a multiset on which this DNN lower bound is
nonpositive.

All graphs are finite and simple. Write

```text
s+(G) = sum_{lambda_i>0} lambda_i^2,
s-(G) = sum_{lambda_i<0} lambda_i^2,
sigma(G) = s+(G)-|V(G)|.
```

Let `G` be a connected octacyclic cactus, let `n=|V(G)|`, and let its eight
cyclic blocks have lengths `l_1,...,l_8`. Thus

```text
m=|E(G)|=n+7.
```

## Exact sharp-DNN inequality

For every integer `l>=3`, put

```text
epsilon_l = 0                                  if l is even,
epsilon_l = l tan^2(pi/(2l))                   if l is odd.
```

If `b` is the number of bridge blocks, cactus block counting gives

```text
b + sum_{i=1}^8 l_i = m = n+7.
```

The sharp cactus DNN constant and its spectral consequence give

```text
s-(G) <= b + sum_{i=1}^8 (l_i+epsilon_{l_i})
       = n+7 + sum_{i=1}^8 epsilon_{l_i}.
```

Since `s+(G)+s-(G)=2m=2n+14`, one obtains

```text
sigma(G) >= 7 - sum_{i=1}^8 epsilon_{l_i}.             (1)
```

Therefore (1) is strictly positive exactly when

```text
sum_{i=1}^8 epsilon_{l_i} < 7.                         (2)
```

The residual problem is to classify, up to permutation, all eight-element
cycle-length multisets for which the epsilon sum is at least `7`.

## Exact symbolic comparisons

The sequence `epsilon_l` is strictly decreasing over odd `l>=3`. To see this,
write `u=pi/(2x)`. The required monotonicity reduces to the strict increase of
`tan^2(u)/u` in `u`, whose derivative is positive because

```text
2u tan(u) sec^2(u) - tan^2(u) > 0
    <=> 2u > sin(u)cos(u).
```

The first two odd values are

```text
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5) =: a.
```

The following comparisons suffice for the classification:

```text
3a < 2,                                                (3)
2a > 1,                                                (4)
epsilon_5 + epsilon_7 < 1.                             (5)
```

They are exact. Comparison (3) is equivalent to `13<6sqrt(5)` and follows by
squaring from `169<180`. Comparison (4) is equivalent to `4sqrt(5)<9` and
follows from `80<81`.

For (5), use `pi<22/7` and `cos x>1-x^2/2` for `x>0` to obtain

```text
cos(pi/7) > 1-(1/2)(22/49)^2 > 7/8.
```

Consequently,

```text
epsilon_7
 = 7(1-cos(pi/7))/(1+cos(pi/7))
 < 7/15
 < 2sqrt(5)-4
 = 1-epsilon_5.
```

The only radical comparison here is exact: `7/15<2sqrt(5)-4` is equivalent to
`67/30<sqrt(5)`, and its square is `4489<4500`.

## Exhaustive classification

Let `t` be the number of triangular entries in the eight-cycle multiset. Every
nontriangle contributes at most `a`: even lengths contribute zero, while odd
nontriangle lengths are at least five and odd-index monotonicity applies.

### At most five triangles

For `t<=5`, since `a<1`,

```text
sum_i epsilon_{l_i} <= t+(8-t)a <= 5+3a < 7
```

by (3). Thus every multiset with at most five triangles satisfies the strict
condition (2).

### Exactly six triangles

Write the two remaining lengths as `p,q`, where `3<p<=q`.

- If either length is even, then `epsilon_p+epsilon_q<=a<1`.
- If both are odd and `(p,q)!=(5,5)`, then `p>=5` and `q>=7`, so monotonicity
  and (5) give

```text
epsilon_p+epsilon_q <= epsilon_5+epsilon_7 < 1.
```

- If `p=q=5`, then by (4)

```text
sum_i epsilon_{l_i}
 = 6+2epsilon_5
 = 16-4sqrt(5)
 > 7.
```

Hence the unique residual multiset with exactly six triangles is

```text
{3,3,3,3,3,3,5,5}.                                   (R1)
```

Its right-hand side in (1) is exactly

```text
7-(16-4sqrt(5)) = 4sqrt(5)-9 < 0.
```

### At least seven triangles

Every such multiset has the form

```text
{3,3,3,3,3,3,3,q},  q>=3.                             (R2)
```

Conversely, each member of (R2) has

```text
sum_i epsilon_{l_i} = 7+epsilon_q >= 7.
```

The DNN right-hand side is therefore exactly `-epsilon_q`: it is zero when
`q` is even and strictly negative when `q` is odd. The value `q=3` is the
eight-triangle multiset.

## Classification returned

Up to permutation, the complete set of eight-cycle-length multisets for which
the sharp-DNN lower bound

```text
sigma(G) >= 7-sum_i epsilon_{l_i}
```

does not itself yield a strict positive bound is exactly

```text
{3,3,3,3,3,3,5,5},
{3,3,3,3,3,3,3,q} for an arbitrary integer q>=3.
```

The two classes are disjoint: the isolated multiset has exactly six triangles,
whereas the parametric family has at least seven. Every other multiset of eight
cycle lengths makes the right-hand side of (1) strictly positive. This is only
an exact symbolic reduction of the sharp-DNN estimate; determining the actual
sign of `sigma(G)` on (R1) and (R2) requires arguments beyond this note.
