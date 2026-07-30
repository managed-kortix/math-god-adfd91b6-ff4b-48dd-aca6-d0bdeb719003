# Tick 48: complete closure of the nine-hole branch

Let H be the missing graph of a putative order-18 counterexample with nine
missing pairs. The exact degree budget forces every oriented-graph outdegree to
equal eight.

If H has no isolated vertex, then its degree sum is 18 on 18 positive-degree
vertices. Hence every missing degree is one and H is exactly `9K2`. This branch
was eliminated by the matching-pair contraction argument in
`tick9-high-missing-structure.md`.

Otherwise choose any isolate z of H. Vertex minimality supplies a robust tight
in-neighbor witness w with `w->z`. Relabel w as 0, z as 1, the other seven
outneighbors as `A'`, the seven exact second neighbors as B, and the remaining
two vertices as C. This is exactly the isolated-root normal form partitioned by
the 28 aggregate cells

```
0 <= rho <= 6,  0 <= k <= 6-rho.
```

All 28 cells are eliminated: k at most 4 by written human proofs, `(0,6)` by
the retained 1,110-leaf reduced campaign, and `(0,5),(1,5)` by the retained
931-leaf common reduced campaign. Multiple isolates cause no uncovered case,
because one may choose any isolate and its deletion witness before relabelling.

Therefore the complete `m=9` branch is impossible. The remaining order-18
frontier is exactly `m in {5,6,7}`; this statement is still only an order-18
structural theorem, not SNC.
