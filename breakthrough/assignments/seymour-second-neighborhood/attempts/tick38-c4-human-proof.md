# Tick 38: human elimination of the four-cycle hole shape

Work in the isolated-root `m=9,k=4` normal form. Every vertex has outdegree
eight, `T={w} union A union B` has sixteen vertices, `A'=A\{z}`, and every
`b in B` has a predecessor in `A'`. Suppose the four holes in `T` form the
cycle

```
h0h1, h1h2, h2h3, h3h0
```

with indices modulo four. Put `H={h0,h1,h2,h3}`.

## Predecessor lower bound

Let `K` be the vertices of `B` that dominate both vertices of `C`. There are
twelve arcs from B to C. If `x=|K|`, then
`12<=2x+(7-x)`, so `x>=5`; and `x!=7`, because seven common dominators would
contribute fourteen arcs. Hence `x` is five or six. Let

```
P = union_{b in K} (N-(b) intersect A'),   r=|P|.
```

For `b in K`, put

```
p_b=|N-(b) intersect A'|,
h_b=number of holes from b to {w} union A',
q_b=1[b->z].
```

Exact outdegree eight gives the row identity

```
d_B+(b)=p_b+h_b-2-q_b.                         (1)
```

Indeed, `b` has two outneighbors in C; among the seven pairs to A', exactly
`7-p_b-h_b` point from `b` to A' after accounting for holes when `bw` is
present (and the same combined count results when `bw` is a hole). The arc
`w->b` is absent because `b in B=N++(w)`; the pair `wb`, if present, is
oriented `b->w`; and the present pair `bz` contributes `q_b`.

Let `eta` count holes internal to K. Counting the present pairs in K, applying
`p_b<=r`, and then using the disjoint four-hole budgets gives

```
C(x,2)-eta <= sum_K d_B+(b)
             <= xr + sum_K h_b - 2x,
eta + sum_K h_b <= 4.
```

Consequently

```
C(x,2) <= x(r-2)+4.                             (2)
```

For either `x=5` or `x=6`, (2) implies

```
r>=4.                                            (3)
```

## Inaccessible-pair classification

Fix `a in P`, choose `b in K` with `a->b`, and put

```
S_a={a} union N_T+(a).
```

Both C vertices are reached through `b`, and the normal form has no arcs from A
to C, so they are exact second neighbors of `a`; also `|S_a|=9`. If `j`
vertices of `T\S_a` are two-walk-accessible in T, then
`d++(a)>=j+2`. Badness and `d+(a)=8` give `d++(a)<=7`, hence `j<=5` and at
least two of the seven vertices of `T\S_a` are inaccessible. For an
inaccessible `t`, let `q_a(t)` count holes from `t` into `S_a`. Every present
pair between `t` and `S_a` is oriented from `t` into `S_a`; otherwise an
outneighbor of `a` reaches `t`. Thus `t` has
`9-q_a(t)` forced outneighbors in `S_a`, whence

```
q_a(t)>=1.                                       (4)
```

Every inaccessible vertex consequently lies in H. There cannot be three of
them: among any three cycle vertices outside `S_a`, one has no cycle neighbor
in `S_a`, contradicting (4). Hence exactly two are inaccessible. Call their
pair `I_a`.

There are two types.

### Adjacent pair

If `I_a={h_i,h_{i+1}}`, then (4) forces the other two cycle vertices into
`S_a`; each inaccessible vertex has exactly one hole into `S_a`. Exact degree
eight gives

```
N+(h_i)     = S_a\{h_{i-1}},
N+(h_{i+1}) = S_a\{h_{i+2}}.                    (5)
```

In particular, `I_a` determines `S_a`. It also forces the two present diagonal
orientations

```
h_i -> h_{i+2},   h_{i+1} -> h_{i+3}.           (6)
```

### Opposite pair

If `I_a={h_i,h_{i+2}}`, both inaccessible vertices have the same two hole
neighbors, so their crossing-hole counts into `S_a` are equal. The pair between
them is present. The endpoint-packing inequality

```
q_a(t)+q_a(u)+1[tu is a hole]>=3
```

and equality of their q-values force both hole-neighbors `h_{i+1},h_{i+3}`
into `S_a`. Put `X=S_a\{h_{i+1},h_{i+3}}`. Both inaccessible vertices dominate
all seven members of X and each has one remaining outgoing slot. The oriented
diagonal uses the eighth outgoing slot of exactly one endpoint. The other
endpoint has one outgoing slot outside X, but cannot point to either deleted
hole-neighbor. Therefore no additional common outneighbor exists, and

```
N+(h_i) intersect N+(h_{i+2}) = X,              (7)
```

so the opposite pair also determines `S_a`.

A fixed set `S subset T` can equal `{a} union N_T+(a)` for at most one source
`a in T`: two distinct sources with the same closed outneighborhood would point
to one another in both directions. Hence each of the six possible pairs `I_a`
supports at most one member of P.

Finally, at most one of the four adjacent pairs can occur. Their forced
orientations of the two diagonals are

```
{h0,h1}: h0->h2, h1->h3
{h1,h2}: h2->h0, h1->h3
{h2,h3}: h2->h0, h3->h1
{h3,h0}: h0->h2, h3->h1.
```

Any two rows disagree on at least one diagonal. Thus P contains at most one
adjacent-pair source and at most one source for each of the two opposite pairs:

```
r<=3.                                            (8)
```

This contradicts (3). Therefore the four-cycle T-hole shape is impossible,
uniformly for `rho=0,1,2`.

This eliminates one shape inside the order-18 `m=9` normal form. It is not an
order-18 elimination and not a proof of SNC.
