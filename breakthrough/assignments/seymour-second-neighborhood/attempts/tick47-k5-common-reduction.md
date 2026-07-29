# Tick 47: common reduction for the two final k=5 rows

Both residual rows `(rho,k)=(0,5)` and `(1,5)` project to one 16-vertex
relaxation. Let `T={w,z} union A' union K union {s}`, where `|A'|=7` and
`|K|=6`. The six vertices in `K` dominate both deleted C vertices. The remaining
B vertex is `s`.

After deleting C the exact outdegrees are 8 on `w,z,A'`, 6 on `K`, and 7 on
`s`. Their sum is 115, so exactly five of the 120 pairs in T are holes. The
rooted constraints persist: `w->{z} union A'`, no `w->B`, z is incident with no
hole, and every B vertex has an A' predecessor.

For `a in A'`, every B-outneighbor supplies at least one exact C second
neighbor. If `a` points into K, both C vertices are exact second neighbors, so
badness forces at least two T-inaccessible vertices. Otherwise its required B
outneighbor is s, supplying one C second neighbor, and badness forces at least
one T-inaccessible vertex. This gives the sound conditional reduced model in
`experiments/k5_reduced_cnf.py`.

The model has 3,112 variables and 12,177 clauses. Two independent hostile
audits verified the projection and CNF semantics. A direct ten-minute CaDiCaL
scout remained unresolved, so the next step is semantic packet strengthening,
not the historical full-model grind.

For a selected inaccessible pair `{t,u}`, write `delta(v)=8-d_T^+(v)`, let h be
the source-hole count, and let `i_v=[v->a]`. Exact degree and the five-hole count
give

```
e+({t,u},R)+h_other = 4-h-i_t-i_u-delta(t)-delta(u).
```

For a singleton witness t the corresponding identity is

```
e+(t,R)+h_other = 5-h-i_t-delta(t).
```

These defect-weighted packet equations are queued for explicit-hole encoding
and a symmetry cover under `S7(A') x S6(K)`.
