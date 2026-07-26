# Tick 13: corrected `m=8` shard design

The witness-rooted B7 branch has a unique degree-nine vertex `r` and remainder
`C={c0,c1}`. Put

```
p = missing pairs from C to {v} union A, plus the internal C pair,
rho = e(C,B),
e = all other missing pairs.
```

Exact degree and missing counts give

```
p-rho=3, e+rho=5, p+e=8.                         (1)
```

Therefore there are **six**, not five, aggregate rows:

```
(p,rho,e)=(3,0,5),(4,1,4),(5,2,3),
           (6,3,2),(7,4,1),(8,5,0).              (2)
```

The omitted sixth row has an explicit exact local realization satisfying all
root degree and robust-column constraints, so excluding it was unsound. It must
remain until global badness/arc minimality eliminates it.

For each `ci`, let `pi` count its missing pairs to `{v} union A`, let
`rho_i=e(ci,B)`, and let `delta_i=1[ci->cj]`. The exact row equation is

```
pi=rho_i+1+delta_i,
delta_0+delta_1+h(c0,c1)=1.                         (3)
```

Safe symmetry uses `rho_0<=rho_1`; if tied, retain only missing `c0c1` or
`c0->c1`.

Naive cellwise missing-degree sharding produces about 1.6 million sequences
before orientation feasibility. The correct front-end is instead the colored
eight-edge missing graph plus C-state. Coarse C margins yield only 762 rows;
then generate colored missing graphs under `S7(A') x S7(B)` and apply exact
orientation circulation before SAT. This should produce hundreds/low thousands
of actual shards rather than millions of degree abstractions.
