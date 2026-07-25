# Tick 9: high-missing order-18 structure

## Nine missing pairs

Every vertex has outdegree eight. If the missing graph is a perfect matching,
there is a complete human contradiction. For each root, its uncovered set has
at least two vertices. A fixed vertex can be uncovered from at most one
non-mate root and possibly its mate root, so double counting forces exactly two
uncovered vertices per root and forces every missing mate to be uncovered.
This makes all four arcs between any two matched pairs point uniformly. After
contracting the nine pairs one obtains a regular tournament on nine vertices;
second neighborhoods in the original graph are unions of full pairs and hence
even, contradicting the forced size seven.

Thus any residual `m=9` counterexample must have both an isolated missing-graph
vertex and a vertex of missing degree at least two. Around any isolated vertex,
a robust deletion witness has a two-vertex inaccessible layer containing at
least three missing incidences. The equality configurations remain locally
feasible, so proving that the missing graph has no isolated vertex is the exact
human bottleneck.

## Eight missing pairs

There is a unique degree-nine vertex `r`. A robust deletion witness `v->r`
has `|A|=8,|B|=7,|C|=2` and gives

```
h(A)+h(B)+h(A,B)+h(B,C)+h(v,B)+e(C,B)=5,             (1)
e(A,B)=37+h(A),                                      (2)
```

while every `B` column hit by `r` has another predecessor in `A`. If
`p=e(r,A)` and `t=e(r,B)`, then `p+t=9` and `2<=p,t<=7`. The two C-row equations
give `e(C,B)=p_C-3`, leaving exactly five aggregate `(missing around C,
e(C,B))` rows. This is a sharp finite normal form but not yet contradictory.
