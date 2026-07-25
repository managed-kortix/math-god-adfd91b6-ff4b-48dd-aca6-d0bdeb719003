# Tick 5: order 18, seven-vertex second layer

Let `C={p,q}` be outside `{s} union A union B`. With `m` missing pairs,
`x(v)=d+(v)-8`, and `r=e(C,B)`, exact counting gives

```
sum_v x(v)+m=9,
x(C)=3+r-k,
r+x(V\C)+ell=6,
```

where `k` counts missing pairs in `C-A`, `C-{s}`, and inside `C`, while `ell`
counts all others. In particular `k>=1+r`, so `m=0` is impossible. For `c in
C`, if `M_c=m(c,A union {s})`, `t_c` indicates the outgoing internal `C` arc,
and `r_c=e({c},B)`, then

```
M_c=1+t_c+r_c-x(c).                                    (1)
```

For `m=1`, budgets force `k=1,r=ell=0,x(C)=2`. Either `pq` is missing or the
head of the oriented `C` pair is a degree-nine vertex `c` dominating
`A union {s}`. Then exactly `N++(c)=B`, so its deficit is two. But for `c->s`,
no alternate outneighbor points to `s` because all are in `A` and `s->A`,
contradicting the deficit-two arc-minimality requirement. Hence `m=1` is
impossible.

For `m=2`, all cases reduce, up to swapping `p,q`, to

```
T0: p->q, x(p)=1, x(q)=0, M_p=M_q=1, e(C,B)=0.
T1: p->q, q->b0 uniquely, x(p)=x(q)=1, M_p=M_q=1.
```

Scalar budgets alone admit these. The known theorem for tournaments missing at
most two edges eliminates them globally, but this compression is retained as an
independent structural check.
