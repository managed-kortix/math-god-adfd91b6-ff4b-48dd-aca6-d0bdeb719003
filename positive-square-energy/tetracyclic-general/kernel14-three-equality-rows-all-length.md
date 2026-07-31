# Kernel 14: the three equality rows at all lengths

## Scope and theorem

This note closes exactly the three kernel-14 physical parity rows left as
equality candidates by `cubic-kernels-residual-rational-frontiers.md`. It does
not modify either frontier verifier or a main manuscript.

Use upper-triangle pair order

`01,02,03,04,05,12,13,14,15,23,24,25,34,35,45`.

Kernel 14 has multiplicity vector

`(0,0,0,1,2,0,1,2,0,2,0,1,0,0,0)`.

Thus its three doubled bundles are `05,14,23`, and its three single paths are
`04,13,25`. For each of the following rows, every simple realization, at all
allowed path lengths and with arbitrary rooted trees attached at arbitrary
vertices, satisfies

`kappa(G) <= |E(G)|+3`

and consequently `s^+(G)>=|V(G)|`:

```text
(0,0,0,0,1,0,0,1,0,1,0,1,0,0,0)
(0,0,0,0,1,0,1,1,0,1,0,1,0,0,0)
(0,0,0,1,1,0,1,1,0,1,0,1,0,0,0).
```

The certificate has exact excess three at the canonical vector and excess at
most three at every longer vector. In particular it certifies every
one-coordinate `+2` target, including the twelve targets at physical
coordinates `0,3,8` that were unresolved by the rational strict-frontier
search.

## Exact path reduction

For a path of length `l` whose branch-endpoint Gram correlation is `r`, exact
path elimination gives the excess

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                         (1)

For fixed `r` and fixed parity, `f_l(r)` is nonincreasing under `l -> l+2`.
The three doubled bundles in all three rows have one odd and one even path.
At their first lengths `1,2`, put `x=tan(acos(r)/4)`. Then

```text
f_1(r)+f_2(r)
 = (1-x^2)^2/(4x^2)+2x^2
 = 1 + (3x^2-1)^2/(4x^2) >= 1.                 (2)
```

Equality holds at `x^2=1/3`, equivalently `r=-1/2`. Hence each mixed doubled
bundle has canonical cost exactly one at correlation `-1/2`, and has cost at
most one after either member is increased by any even amount.

For a single path, correlation `r=(-1)^l` makes the argument of `acos` in (1)
equal to one. Its cost is therefore exactly zero at every length of the fixed
parity, not merely at its canonical length.

## Symbolic Gram table

Let `epsilon_e=1` when the single path `e` is even and `epsilon_e=-1` when it
is odd. Choose unit vectors `a,b,c` for vertices `0,1,2`, and set

`u_0=a, u_1=b, u_2=c, u_4=epsilon_04 a,`
`u_3=epsilon_13 b, u_5=epsilon_25 c`.                         (3)

It remains only to choose the Gram matrix `Q=Gram(a,b,c)`. The complete table
is as follows. The three-bit word records the parities of `04,13,25` in that
order.

| full physical row | single word | `(epsilon_04,epsilon_13,epsilon_25)` | `(a.b,a.c,b.c)` | `det Q` | total excess |
|---|:---:|:---:|:---:|---:|---:|
| `(0,0,0,0,1,0,0,1,0,1,0,1,0,0,0)` | `001` | `(1,1,-1)` | `(-1/2,1/2,-1/2)` | `1/2` | `3` |
| `(0,0,0,0,1,0,1,1,0,1,0,1,0,0,0)` | `011` | `(1,-1,-1)` | `(-1/2,1/2,1/2)` | `0` | `3` |
| `(0,0,0,1,1,0,1,1,0,1,0,1,0,0,0)` | `111` | `(-1,-1,-1)` | `(1/2,1/2,1/2)` | `1/2` | `3` |

Each `Q` has diagonal one and every two-by-two principal minor equal to `3/4`.
The displayed nonnegative determinant therefore proves `Q` positive
semidefinite. For a direct coordinate realization one may use

```text
001: a=(1,0,0), b=(-1/2,sqrt(3)/2,0),
     c=(1/2,-1/(2sqrt(3)),sqrt(2/3));

011: a=(1,0), b=(-1/2,sqrt(3)/2), c=(1/2,sqrt(3)/2);

111: a=(1,0,0), b=(1/2,sqrt(3)/2,0),
     c=(1/2,1/(2sqrt(3)),sqrt(2/3)).
```

Equation (3) makes every single path have correlation equal to its parity
sign, so all three single-path costs vanish. It also gives

```text
u_0.u_5 = epsilon_25 (a.c) = -1/2,
u_1.u_4 = epsilon_04 (a.b) = -1/2,
u_2.u_3 = epsilon_13 (b.c) = -1/2
```

in every table row. Thus the doubled bundles `05,14,23` cost at most one each
by (2) and fixed-parity monotonicity. The total excess is at most three for
every allowed length vector. At the first-simple vector it is exactly three,
which explains why a search restricted to strict rational costs cannot accept
these equality targets.

## Physical-coordinate frontier table

Expanding nonzero pairs in pair order gives the nine physical coordinates

`0:04, 1:05a, 2:05b, 3:13, 4:14a, 5:14b, 6:23a, 7:23b, 8:25`.

For all three rows the certificate disposition is therefore

| target length vector | changed path type | certificate cost |
|---|---|---:|
| canonical first-simple vector | three singles and three mixed doubled bundles | `3` |
| canonical `+2` at `0` | single `04` | `3` |
| canonical `+2` at `3` | single `13` | `3` |
| canonical `+2` at `8` | single `25` | `3` |
| canonical `+2` at any of `1,2,4,5,6,7` | member of a doubled bundle | `<=3` |
| any coordinate increased by any nonnegative even amount | same fixed physical parity row | `<=3` |

The first four lines are the twelve unresolved verifier targets. The final two
lines show that the same symbolic certificate is stronger than the requested
frontier closure: it covers every all-length realization in each of the three
physical rows.

## Spectral and attachment conclusion

Let the subdivided kernel core have `L` edges. Its cyclomatic rank is four, so
it has `L-3` vertices. The table and exact path elimination give

`kappa(H)-L <= 3`.

Since `s^-(H)<=kappa(H)` and `s^+(H)+s^-(H)=2L`,

`s^+(H) >= 2L-(L+3)=L-3=|V(H)|`.

If rooted trees with `t` edges in total are attached by one-vertex sums, DNN
constants add and a tree contributes exactly its number of edges. Hence

`kappa(G)<=L+3+t=|E(G)|+3`,

while `|V(G)|=L-3+t`; the same trace calculation proves
`s^+(G)>=|V(G)|`. This includes trees based at internal path vertices and
completes the three rows without an induced-deletion argument.
