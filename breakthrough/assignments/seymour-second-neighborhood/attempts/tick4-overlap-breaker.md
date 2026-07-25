# Tick 4: breaker for naive internal-overlap inequalities

For `H=D[A]`, define `Y_a=N_H^{++}(a)`, let `R_a` be exact second endpoints in
`A` created via `a->B->A`, and let `W_a` be non-first vertices of `B` reached
via `a->A->B`. Then the always-valid direct lower bound is

```
L-e >= sum_a (|Y_a union R_a| + |W_a| + sigma_a) - e.    (1)
```

The union is essential. A tournament `H` on eight vertices with score sequence
`(3,6,5,6,2,2,2,2)`, all `A->B` arcs except one reversal `b0->a0`, and no
`B->s` arcs satisfies all root row, no-singleton, and Hall constraints but has

```
e=28, L=18, L-e=-10.
```

The reversed endpoint is already a first or exact second neighbor whenever it
is reached, so charging reversed/missing pairs separately double-counts. Hence
no inequality `L>=e`, nor a positive correction based only on Hall expansion or
the number of exceptional `A-B` pairs, is valid. The next inequality must use
full vertexwise badness/exterior budgets, not root overlap data alone.
