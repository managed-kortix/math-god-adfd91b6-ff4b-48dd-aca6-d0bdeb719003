# Tick 25: human elimination of the `m=9` strips `k=0,1,2`

Use the isolated-root normal form of tick 24. All vertices have outdegree eight,
`T={w} union A union B` has 16 vertices, `|A|=8`, `|B|=7`, `C` has size two,
and every `b in B` has a predecessor in `A'=A\{z}`. There are `8+k` arcs
from B to C, so at least `1+k` vertices of B dominate both C vertices; call
their set `K`.

Fix `b in K` and `a in A'` with `a->b`. Both C vertices are exact second
neighbors of `a`. Put `S_a={a} union N_T+(a)`, so `|S_a|=9`. Badness forces at
least two of the other seven T vertices to be inaccessible from `a` by a
two-walk.

Every inaccessible vertex must be incident with a T-hole crossing to `S_a`:
otherwise it dominates all nine vertices of `S_a`, contradicting outdegree
eight. One crossing hole supports at most one inaccessible vertex, since its
other endpoint lies in `S_a`. Hence `k=0,1` are immediately impossible.

Now let `k=2`. Exactly two vertices are inaccessible, and each of the two holes
supports exactly one. In particular no inaccessible vertex can consume both
holes, since the second inaccessible vertex would then have no supporting hole.
If a hole is `ty`, with inaccessible endpoint `t` and `y in S_a`, exact degree
eight gives

```
N+(t)=S_a\{y}, equivalently S_a=N+(t) union {y}.        (1)
```

For either fixed hole, choosing its inaccessible endpoint (two choices) fixes
`S_a` by (1). A fixed `S_a` supports at most one `a`, because two distinct
sources with the same closed outneighborhood would point to one another both
ways. Therefore the union `P` of A' predecessors of members of K has size at
most two.

For `b in K`, let `p_b=|N^-(b) intersect A'|<=2`, and let `h_b` count holes
from `b` to `{w} union A'`; put `q_b=1[b->z]`. Counting the two C
outneighbors, the present arcs toward `{w} union A'`, the arc on the present
`bz` pair, and B-outneighbors gives

```
d_B+(b)=p_b+h_b-2-q_b <= h_b-q_b.               (2)
```

Let `x=|K|>=3`, let `H_K` count holes internal to K, and put
`Q=sum_{b in K}q_b`. Counting the arcs internal to K and applying (2),

```
C(x,2)-H_K <= sum_K d_B+(b) <= sum_K h_b-Q.
```

The holes counted by `H_K` and by `sum h_b` are disjoint T-holes, so their sum
is at most two. It follows that `C(x,2)<=2-Q<=2`, contradicting `x>=3`.
Thus `k=2` is impossible as well.

The argument uses crucially that in the `m=9` branch there is no degree-nine
exceptional vertex: every inaccessible vertex must consume a hole. A hostile
audit that introduced an exceptional `r` was applying the `m=8` degree census
and does not apply here.
