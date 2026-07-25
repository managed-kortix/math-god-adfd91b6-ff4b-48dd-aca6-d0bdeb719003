# Tick 6: human elimination of order 18, `|B|=6`, `m=3`

Assume an arc-minimal counterexample. Every vertex has outdegree 8 or 9 and
deficit one or two. With three missing pairs, total excess over outdegree eight
is six. Let `C` be the three vertices outside `{s} union A union B`, let
`r=e(C,B)`, and let `k` be total excess outside `C`. Exact layer counting gives

```
k + m(C,B) + m(outside C) + r = 3.                 (1)
```

Since each `c in C` has excess at most one, total excess in `C` is at most
three, so `k>=3`. Equation (1) forces equality everywhere:

```
k=3, m(C,B)=m(outside C)=r=0.
```

Thus every `c in C` has outdegree nine, all three missing pairs are between
`C` and `A union {s}` or internal to `C`, and every `C-B` pair is `B->C`.

For `c in C`, let `M_c` count its missing pairs to `A union {s}` and let `t_c`
be its internal outdegree in `D[C]`. Its row equation is `t_c=M_c`. No `M_c`
can vanish: then `N+(c)=A union {s}`, while only the six vertices in `B` can be
exact second neighbors, giving deficit at least three. Therefore every `M_c=1`
and there are no missing pairs inside `C`. The orientation `D[C]` is a directed
triangle.

Take an internal arc `c0->c1`, with the triangle continuing `c1->c2->c0`.
No other outneighbor of `c0` points to `c1`, because all eight others lie in
`A union {s}` and that set has no arcs into `C`. Thus deleting `c0->c1` does
not demote `c1` to an exact second neighbor (`g=0`). It does destroy the unique
two-walk `c0->c1->c2`, so the loss set is nonempty. This violates the universal
arc-minimality inequality `g-|L|>=mu(c0)-1>=0`.

Hence this shard is impossible by a complete human argument. The earlier Z3
UNSAT observation is no longer needed.
