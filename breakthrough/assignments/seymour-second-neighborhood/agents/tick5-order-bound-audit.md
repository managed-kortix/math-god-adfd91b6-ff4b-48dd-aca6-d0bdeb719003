# Tick 5 hostile audit of the triangular order bound

Seacrest arXiv:1808.06293v3 intends the valid statement that a counterexample
of minimum outdegree `delta` implies one on at most `binom(delta+1,2)` vertices.
The printed set-distance convention creates a gap: members of a set can have
positive distance from that same set, invalidating identities used in Lemma 4.

Repair the proof with external set neighborhoods

```
Gamma+(S)=N+(S)\S,
Gamma2+(S)=N+(Gamma+(S)) \ (S union Gamma+(S)).
```

For an arc-minimal counterexample, the corrected deletion argument gives
`|Gamma2+(S)|<|Gamma+(S)|`. For positive-distance layers `L_i` from `r`, use
`S_1={r}` and `S_k=L_1 union ... union L_{k-1}` for `k>=2`; then exactly
`Gamma+(S_k)=L_k` and `Gamma2+(S_k)=L_{k+1}`. Including `r` in every prefix is
false when `r` returns on a directed cycle; the directed triangle is the
smallest breaker.

Layer sizes strictly decrease from `q=delta+(H)` in an arc-minimal spanning
counterexample `H`. A sink SCC in the positively reachable set is itself a
counterexample and has at most `q+...+1` vertices. Since `q<=delta`, the bound
follows. Thus a globally vertex-minimal degree-eight counterexample has at most
36 vertices. Our use relies on this repaired proof, not literally on the flawed
printed convention.
