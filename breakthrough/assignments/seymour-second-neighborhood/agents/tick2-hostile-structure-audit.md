# Tick 2 hostile audit of the root-signature lemma

Verdict: the conclusions in `tick1-structure.md` survive, but the arc-deletion
argument omitted a necessary non-tail monotonicity proof.

For `e=x->y`, deleting `e` can alter `N++(v)` for `v != x`: it may delete `y`
when every two-walk from `v` to `y` used `x->y`. It leaves `N+(v)` unchanged
and cannot create an exact second neighbor. Hence a non-Seymour non-tail vertex
cannot become Seymour after deletion. Arc minimality therefore forces the tail
`x` to become Seymour, which validates

```
g_e - |L_e| >= m(x)-1,
m(x)=d+(x)-d++(x).
```

This supplies the missing proof that every deficit is 1 or 2. Consequently a
minimum-outdegree-eight root has `|B| in {6,7}`, and the singleton predecessor
signature and edge-count consequences in `tick1-structure.md` remain valid.

The three-vertex path `v->x->y` is a hostile reminder that non-tail second
neighborhoods are not unchanged; they only move monotonically downward.

Without arc minimality, `|B|=5` is possible at a degree-eight root (though not
necessarily in a counterexample), so the stronger `{6,7}` funnel must always be
labelled with the lexicographic vertex-then-arc minimality hypothesis.
