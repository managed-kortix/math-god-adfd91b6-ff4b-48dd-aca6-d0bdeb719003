# Tick 1 hostile verifier/model audit

The two verifier implementations must share only the mathematical contract:

```
N1(v) = row support of A,
N2(v) = support(Boolean A^2 row v) \ (N1(v) union {v}).
```

Differential tests compare every set, not only rejection, because no positive
counterexample fixture is known. Named hostile cases cover zero outdegree,
universal versus existential quantifiers, strict versus non-strict comparison,
direct neighbors also reached in two steps, distance three, duplicate two-walk
endpoints, missing pairs, and malformed certificates.

A sound baseline fixed-order SAT model uses adjacency bits `a[v,z]`, path bits
for conjunctions `a[v,y] & a[y,z]`, Boolean reachability `r[v,z]`, and exact
second bits `q[v,z] <-> r[v,z] & !a[v,z]`, with all Tseitin equivalences in both
directions. Impose `sum_z q[v,z] + 1 <= sum_z a[v,z]` for every vertex. Block
adjacency projections, not auxiliary assignments.

Safe staged symmetry: put a minimum-outdegree root at 0, then make its
outneighbors an initial block, and only use permutations stabilizing previous
choices. Individually valid normalizations may be unsound in combination.
Strong connectivity is sound for a minimum-order search, not automatically for
unrestricted exact-order satisfiability.
