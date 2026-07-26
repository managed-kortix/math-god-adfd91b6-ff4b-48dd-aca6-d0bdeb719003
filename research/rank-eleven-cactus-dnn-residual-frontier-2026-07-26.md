# Exact rank-eleven cactus DNN residual frontier

**Date:** 2026-07-26

## Scope and status

This note carries out only the sharp-DNN calculation for connected cacti of
cyclomatic rank `11`. It classifies exactly the cycle-length multisets for
which that particular lower bound is nonpositive. It does not determine the
actual sign of the spectral surplus on a residual multiset, does not identify
counterexamples, and makes no rank-eleven cactus theorem claim.

The companion arithmetic audit is

```bash
python3 research/rank-eleven-cactus-dnn-residual-frontier-verifier.py
python3 -O research/rank-eleven-cactus-dnn-residual-frontier-verifier.py
```

All graphs below are finite and simple. Write

```text
s+(G) = sum_{lambda_i>0} lambda_i^2,
s-(G) = sum_{lambda_i<0} lambda_i^2,
sigma(G) = s+(G)-|V(G)|.
```

Let `G` be a connected rank-`11` cactus on `n` vertices, and let the lengths
of its eleven cyclic blocks be `l_1,...,l_11`. Connectedness and the
cyclomatic identity give

```text
m=|E(G)|=n+10.
```

## Sharp-DNN reduction

For every integer `l>=3`, put

```text
epsilon_l = 0                                  if l is even,
epsilon_l = l tan^2(pi/(2l))                   if l is odd.
```

If `b` denotes the number of bridge blocks, cactus block counting gives

```text
b + sum_{i=1}^11 l_i = m = n+10.
```

The sharp cactus DNN constant therefore yields

```text
s-(G) <= b + sum_{i=1}^11 (l_i+epsilon_{l_i})
       = n+10 + sum_{i=1}^11 epsilon_{l_i}.             (1)
```

Because the adjacency spectrum has squared sum `2m`,

```text
s+(G)+s-(G)=2m=2n+20.
```

Subtracting (1) from this identity and then subtracting `n` gives the exact
sharp-DNN lower bound

```text
sigma(G) >= 10 - sum_{i=1}^11 epsilon_{l_i}.            (2)
```

Thus this bound proves `sigma(G)>0` precisely when

```text
sum_{i=1}^11 epsilon_{l_i} < 10.                        (3)
```

The DNN residual frontier is the purely algebraic failure set where the sum
in (3) is at least `10`.

## Exact comparison ledger

The odd-index values `epsilon_l` decrease strictly for odd `l>=3`. For a real
variable `x>=3`, set `u=pi/(2x)`. Apart from the positive constant `pi/2`,

```text
x tan^2(pi/(2x)) = (pi/2) tan^2(u)/u.
```

For `0<u<=pi/6`, differentiation and multiplication by positive factors give

```text
d/du (tan^2(u)/u) > 0
  <=> 2u tan(u)sec^2(u)-tan^2(u) > 0
  <=> 2u > sin(u)cos(u).
```

The last inequality is strict because
`sin(u)cos(u)<u<2u`. Hence `tan^2(u)/u` increases with `u`; since `u`
decreases with `x`, the original expression decreases strictly with `x`.

The first two odd values are exact:

```text
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5) =: a.
```

Only the following comparisons are needed:

```text
0 < a < 1,                                             (4)
3a < 2,                                                (5)
2a > 1,                                                (6)
epsilon_5+epsilon_7 < 1.                               (7)
```

The algebraic comparisons in (4)--(6) have integer squaring certificates:

```text
a>0       <=> 2sqrt(5)<5,       since 20<25,
a<1       <=> 2<sqrt(5),        since 4<5,
3a<2      <=> 13<6sqrt(5),      since 169<180,
2a>1      <=> 4sqrt(5)<9,       since 80<81.
```

All quantities squared here are positive, so every equivalence preserves the
strict inequality.

For (7), use the strict classical bounds `pi<22/7` and
`cos x>1-x^2/2` for `x>0`. They imply

```text
cos(pi/7)
  > 1-(1/2)(22/49)^2
  = 2159/2401
  > 7/8,
```

where the final rational comparison is `8*2159=17272>16807=7*2401`.
The half-angle identity then gives

```text
epsilon_7
  = 7(1-cos(pi/7))/(1+cos(pi/7))
  < 7(1-7/8)/(1+7/8)
  = 7/15.                                               (8)
```

Finally,

```text
7/15 < 2sqrt(5)-4
  <=> 67/30 < sqrt(5),
```

and the positive sides square to `4489/900<5`, equivalently `4489<4500`.
Since `2sqrt(5)-4=1-a`, (8) proves

```text
epsilon_7 < 1-a,
epsilon_5+epsilon_7 < 1,
```

which is (7), without numerical approximation.

## Exhaustive rank-eleven classification

Let `t` be the number of triangles among the eleven cyclic blocks. Every
nontriangle contributes at most `a`: an even cycle contributes zero, while an
odd nontriangle has length at least five and is controlled by monotonicity.

### At most eight triangles

Since `a<1`, the function `t+(11-t)a` increases with `t`. If `t<=8`, then

```text
sum_i epsilon_{l_i}
  <= t+(11-t)a
  <= 8+3a
  < 10                                                     (9)
```

by (5). Therefore no multiset with at most eight triangles lies on the
residual frontier.

### Exactly nine triangles

Write the two nontriangle lengths as `p,q`, where `3<p<=q`.

- If either length is even, then
  `epsilon_p+epsilon_q<=a<1`.
- If both are odd but `(p,q)!=(5,5)`, then `p>=5` and `q>=7`; monotonicity and
  (7) give
  `epsilon_p+epsilon_q<=epsilon_5+epsilon_7<1`.
- If `p=q=5`, then (6) gives
  `epsilon_p+epsilon_q=2a>1`.

Since the nine triangles contribute exactly `9`, the unique residual
multiset in this case is

```text
{3,3,3,3,3,3,3,3,3,5,5}.                              (R1)
```

Its epsilon sum and DNN margin are exactly

```text
9+2epsilon_5 = 19-4sqrt(5) > 10,
10-(19-4sqrt(5)) = 4sqrt(5)-9 < 0.                     (10)
```

Both strict signs in (10) are equivalent to `2a>1`, whose certificate is
`80<81`.

### At least ten triangles

Every such eleven-element multiset has the form

```text
{3,3,3,3,3,3,3,3,3,3,q},  q>=3.                       (R2)
```

Conversely, every member of (R2) satisfies

```text
sum_i epsilon_{l_i} = 10+epsilon_q >= 10,
10-sum_i epsilon_{l_i} = -epsilon_q <= 0.              (11)
```

The margin in (11) is zero exactly when `q` is even and is strictly negative
when `q` is odd. The value `q=3` includes the all-triangle multiset.

## Residual frontier of the calculation

Up to permutation, the complete rank-eleven cycle-multiset frontier on which
the sharp-DNN lower bound (2) is nonpositive is

```text
{3,3,3,3,3,3,3,3,3,3,q},  q>=3,
{3,3,3,3,3,3,3,3,3,5,5}.
```

Writing `T=C_3`, `P=C_5`, and `Q=C_q`, these are exactly

```text
T^10 Q,
T^9 P P.
```

The families are disjoint: `T^9PP` has exactly nine triangles, whereas every
member of `T^10Q` has at least ten. Every other rank-eleven cycle-length
multiset makes the right-hand side of (2) strictly positive.

This is only an exact classification of the failure set of the sharp-DNN
estimate. A nonpositive lower bound does not imply `sigma(G)<=0`; no statement
about the actual sign of `sigma(G)` on either residual family is claimed here.
