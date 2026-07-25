# Tick 1 construction-route no-go results

## Cayley orientations

For `D=Cay(G,S)` with `S cap S^{-1}=empty`,

```
N1(x)=xS,
N2(x)=x((SS) \ (S union {1})).
```

The Moser--Scherck--Kemperman--Wehn sumset inequality applied to
`A=S union {1}` gives `|SS \ (S union {1})| >= |S|`. Hence every vertex is
Seymour. Positive independent blow-ups also cannot be counterexamples: summing
the weighted first/second degrees over all quotient positions gives totals
`|S|W` and at least `|S|W`, so strict deficit everywhere is impossible.

## Exact substitution identity

For a substitution `D=B[H_1,...,H_m]`, module sizes `w_i`, and `x in H_i`,

```
d2_D(x)-d1_D(x)
 = (d2_Hi(x)-d1_Hi(x))
 + sum_{k in N2_B(i)} w_k - sum_{j in N1_B(i)} w_j.
```

Therefore a substituted graph has a Seymour vertex whenever a module has a
Seymour vertex and its quotient weighted defect is nonnegative. In particular,
a vertex-minimal counterexample is substitution-prime. Complete cyclic gluing
of graphs satisfying SNC also satisfies SNC: selected Seymour vertices would
otherwise force cyclic strict inequalities `w_{i+2}<w_{i+1}`.

No candidate arose. Future construction searches must use genuinely nonuniform
interfaces rather than Cayley symmetry or complete-module substitution.
