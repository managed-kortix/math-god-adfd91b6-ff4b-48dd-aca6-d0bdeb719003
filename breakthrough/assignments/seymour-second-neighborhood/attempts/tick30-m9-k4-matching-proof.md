# Tick 30: the four-matching T-hole shape is impossible

In the isolated-root `m=9,k=4` normal form, let the four holes inside `T` form
a matching. There are twelve B-to-C arcs, so some `b in B` dominates both C
vertices. Choose a robust predecessor `a in A'` of `b`. Both C vertices are
exact second neighbors of `a`.

Put `S={a} union N_T+(a)`, so `|S|=9`. Badness of `a` forces at least two
vertices `t,u` outside S to be inaccessible from `a` by a two-walk in T. Every
present pair from either such vertex to S points into S. Hence each must have a
T-hole into S, or it would have nine outneighbors.

Because the T-holes form a matching, an inaccessible `t` has exactly one hole,
say `t-tbar` with `tbar in S`. It therefore dominates all eight vertices of
`S\{tbar}`; exact outdegree eight gives

```
N+(t)=S\{tbar}.
```

Similarly `N+(u)=S\{ubar}`. Since both `t,u` lie outside S, neither points to
the other. Their pair must therefore be missing. But the unique hole at `t`
has other endpoint `tbar in S`, whereas `u` is outside S, a contradiction.

Thus the four-matching shape is impossible, uniformly in rho.
