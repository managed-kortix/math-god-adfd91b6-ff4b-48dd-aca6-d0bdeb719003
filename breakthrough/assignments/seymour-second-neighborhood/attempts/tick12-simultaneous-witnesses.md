# Tick 12: simultaneous robust-witness frontiers

## Seven missing pairs

There are two degree-nine vertices `r,q`. Either both have degree-eight robust
witnesses, or one high vertex robustly witnesses the other and the witnessing
high vertex itself has a degree-eight witness. Mutual high-high witnessing is
impossible in an oriented graph.

For a degree-eight witness `w->h`, let `C_w` be its two inaccessible vertices,
let `epsilon_w` indicate that the other high vertex lies in `C_w`, and put
`rho_w=e(C_w,B_w)`. Its missing-zone identity is

```
|Z_w|=3+rho_w-epsilon_w,
|M\Z_w|=4+epsilon_w-rho_w.                         (1)
```

For two distinct low witnesses `u,v`, their zones are subsets of the same
seven missing pairs, hence

```
|Z_u intersect Z_v| >= rho_u+rho_v-1-epsilon_u-epsilon_v. (2)
```

If their inaccessible pairs are disjoint, every common zone edge must lie in
the explicit `2 x 2` cut between them. This is a finite overlap shard.

In the high-high branch, root at a low witness `v->q` with `q->r` robust. Both
highs avoid `C_v`; rooting also at `q` forces `{v} union C_v` into `N++(q)`.
Robustness after deleting `r` then forces vertices of `B_v` dominated by `q`
to cover `v` and both members of `C_v`. This concrete three-target support
gadget is the strongest current overlap constraint, but one B-vertex can still
cover all three, so no contradiction follows yet.

## Nine missing pairs

Missing-degree sequences with an isolated vertex are canonically indexed by:

```
k = number of isolates,
partition lambda of k giving excess degrees d-1 of high missing-degree vertices,
a simple core F on those high vertices,
forced leaf counts, and a residual matching.
```

For every isolated missing vertex `z`, its inaccessible set has size two or
three in the minimal branch and every inaccessible in-neighbor must have a
missing neighbor in `N+(z)`. This gives a graph-only witness-star skeleton.
One high missing-degree vertex yields exactly star plus matching and is covered
by known theorems; harder residuals have at least two/three high vertices or a
non-star/cyclic core.
