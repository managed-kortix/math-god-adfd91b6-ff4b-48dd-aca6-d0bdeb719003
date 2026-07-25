# Tick 1 independent structural derivation

Choose a counterexample first minimizing vertices and then arcs.

## Verified lemmas

1. **Strong connectivity.** A sink strongly connected component preserves all
   first and second out-neighborhoods of its vertices, hence vertex minimality
   forces it to be the whole graph.
2. **Vertex deletion witness.** For every vertex `u`, some `w -> u` satisfies
   `d++(w)=d+(w)-1` and `N++_{D-u}(w)=N++_D(w)`. Proof: a Seymour vertex in
   `D-u` must lose `u` as a first neighbor, and all inequalities then tighten.
3. **Arc deletion identity.** For an arc `x -> y`, let `g_xy=1` when another
   `x`-outneighbor points to `y`; let `L_xy` be old exact second neighbors of
   `x` whose every two-walk starts through `y`. Arc minimality implies
   `g_xy-|L_xy| >= m(x)-1`, where `m(x)=d+(x)-d++(x)`. Thus every deficit is 1
   or 2. If it is 2 then `g_xy=1,L_xy=empty` for every outgoing arc; if it is 1
   then `|L_xy|<=g_xy`.

The gain term is essential: deleting `x->y` can make `y` a new exact second
neighbor via `x->z->y`.

## Root signature compression

Let `delta+=8`, `A=N+(s)`, `B=N++(s)`, and for each `b in B` put
`P_b={a in A:a->b}`. Applying the arc-deletion identity at every `s->a` gives:

- `|B|` is 6 or 7 (stronger than the nonminimal 5--7 funnel);
- every `P_b` is nonempty;
- `d^+_{D[A]}(a) + |{b:a in P_b}| >= 8`;
- if `|B|=6`, every `a` has positive indegree in `D[A]` and no `P_b` is a
  singleton;
- if `|B|=7`, the number of singleton signatures `{a}` is zero when `a` has no
  in-neighbor in `D[A]`, and at most one otherwise;
- summing row degrees gives `e(D[A])+sum_b |P_b| >= 64`, hence `e(D[A])>=16`
  for `|B|=6` and `>=8` for `|B|=7`.

These constraints are sound but feasible (for example, dense signatures), so
badness and global completion constraints are indispensable.
