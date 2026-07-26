# Tick 21: elimination of the `rho=3` one-internal-hole branch

In the order-18, `m=8` normal form, let `rho=e(C,B)=3`. The row equations give
two residual missing pairs. Suppose exactly one lies inside
`T=D[{v} union A union B]` and the other lies between `B` and `C`.

There are ten B-to-C arcs, so at least three vertices of `B` dominate both
vertices of `C`; call their set `K`. Fix `b in K` and any predecessor
`a in A'=A\{r}`. Both C vertices are exact second neighbors of `a`.

Put `X=N_T+(a)`, so `|X|=8`. Among the seven remaining T-vertices, an
inaccessible vertex not supported by the unique T-hole dominates `a` and all
of `X`, hence has outdegree at least nine and must be `r`. The hole supports at
most one further inaccessible vertex. Badness after the two C second neighbors
forces equality: exactly two vertices are inaccessible, one is `r`, and the
other uses the hole. The hole cannot meet `r`; consequently

```
N_T+(r)={a} union N_T+(a).                              (1)
```

At most one `a in A'` satisfies (1), since two such vertices would point to
each other in both directions. Therefore a single `a*` is the sole A'
predecessor of every member of `K`.

Choose `b in K` not incident with the T-hole. (The B-C hole cannot meet `K`,
and `|K|>=3`.) Then `b` dominates both C vertices, `v`, and all six vertices of
`A'\{a*}`. These are nine distinct outneighbors, contradicting `d+(b)=8`.

Thus the branch with one internal T-hole is impossible. Together with the
previous tournament argument, this leaves only the branch in which both
residual holes lie inside `T`.
