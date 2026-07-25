# Tick 7: five-missing-pair structural frontier

At order 18, five missing pairs force exactly four outdegree-nine vertices; all
others have outdegree eight. For either root branch the exact scalar systems are
now written down, but they do not alone contradict badness.

## Six-vertex second layer (`|C|=3`)

Let `k` be degree excess outside `C`, `r=e(C,B)`, `q=m(C,B)`, and `h` the
missing pairs wholly outside `C`. Exact counting gives

```
k+q+h+r=3,                                           (1)
```

so `k in {1,2,3}`. Every `c in C` must have at least one missing pair to
`U=A union {s}`; otherwise it dominates all nine vertices of `U` and has at
most six exact second neighbors. If `r=0`, arc minimality forces `D[C]` to be
transitively closed: an unclosed path `c->d->e` would make deletion of `c->d`
lose `e` with no gain.

The first five-edge missing graph outside all verified blanket theorem classes
is `P6`. Exact placement and degree equations reduce its unresolved part to 18
path-type rows and 71 local degree ledgers; the `k=3` rows are eliminated by the
preceding transitive-closure condition. This is a finite next shard, not a
solution.

## Seven-vertex second layer (`|C|=2`)

Let the five missing pairs be counted by locations `AA,AB,AC,BB,BC,sB,sC,CC`.
With `R_C` the number of degree-nine vertices in `C`, exact counting yields

```
e(C,B)=R_C+m(A,C)+m(s,C)+m(C)-3,                    (2)
```

and for each `c in C`, with `alpha_c=m(c,A)`, `beta_c=1[sc missing]`, and
`delta_c=1[c sends the internal C arc]`,

```
e(c,B)=x(c)+alpha_c-1+beta_c-delta_c >=0.           (3)
```

These are the exact individual remainder constraints. Scalar counting leaves
residual incidence families; completion requires exact two-path coverage and
arc-deletion private-endpoint restrictions.

## Decision

The next structural target is the `P6` missing graph in the B6 branch, where a
small finite ledger is available. Search should canonicalize path placements
and enforce the full gain/loss inequalities, rather than rerun an unsharded
five-missing-pair model.
