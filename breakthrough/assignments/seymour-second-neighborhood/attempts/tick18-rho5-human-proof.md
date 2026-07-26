# Tick 18: human elimination of the corrected `m=8, rho=5` row

## Theorem

Let `D` be a vertex-minimal counterexample on 18 vertices with exactly eight
missing unordered pairs and minimum outdegree at least eight. Let `r` be its
unique degree-nine vertex, let `v` be a Seymour vertex of `D-r`, and put

```
A=N+(v), B=N++(v), C=V(D)\({v} union A union B).
```

Then `|A|=8,|B|=7,|C|=2`, and the branch `e(C,B)=5` is impossible.

## Proof

There are `C(18,2)-8=145` arcs. Minimum outdegree eight therefore forces one
vertex `r` of outdegree nine and all other vertices to have outdegree eight.

By vertex minimality, `D-r` has a Seymour vertex `v`. If `v` did not point to
`r`, deleting `r` would leave its first neighborhood unchanged and could only
shrink its exact second neighborhood, contradicting badness in `D`. Hence
`v->r`. The Seymour inequality in `D-r` and badness in `D` force

```
d+(v)=8, d++(v)=7, N++_{D-r}(v)=N++_D(v)=B.           (1)
```

Thus `|A|=8,|B|=7,|C|=2`, `r in A`, and every `b in B` has a predecessor in
`A\{r}` in `D-r`. Also no arc goes from `A` to `C`, since such an arc would put
its endpoint in `N++(v)`.

Write `rho=e(C,B)`. Counting the two degree-eight rows in `C` gives that the
number `p` of missing pairs between `C` and `{v} union A`, together with the
possible internal missing pair of `C`, is

```
p=rho+3.                                               (2)
```

If `rho=5`, all eight missing pairs are counted by `p`. Hence

```
T=D[{v} union A union B]
```

is a tournament on 16 vertices, and every B-C pair is present. Of the 14 B-C
pairs, five point from `C` to `B`, so nine point from `B` to `C`. By
pigeonhole, some `b in B` dominates both vertices of `C`. By (1), choose
`a in A\{r}` with `a->b`. Then `a->b->c` for both `c in C`; since `A->C` is
forbidden, both are exact second neighbors of `a`.

Now `a != r`, so `d_D+(a)=8`, and all its outneighbors lie in `T`. Hence
`d_T+(a)=8`, and `a` has seven inneighbors in the 16-vertex tournament `T`.
If a T-inneighbor `z` is not reached from `a` by a two-walk in `T`, then `z`
must dominate `a` and all eight T-outneighbors of `a`. Thus `d_T+(z)>=9`, so
`d_D+(z)>=9`. The degree census forces `z=r`. Therefore at most one of the
seven T-inneighbors is inaccessible, and at least six are exact second
neighbors of `a` in `T`.

These six vertices are disjoint from the two exact second neighbors in `C`.
Therefore

```
d_D++(a)>=6+2=8=d_D+(a),
```

contradicting that every vertex of `D` is bad. Hence `rho=5` is impossible.

## Audit

Three independent hostile routes checked the exact proof. Two reconstructed it
line by line and found no flaw. A generic agent produced counterexamples to
unrelated lifting statements that lack the common B-dominator and degree-census
hypotheses; those do not apply here. The previously checked LRAT leaves remain
useful regression artifacts, but no computational certificate is needed for
this row.

One independent route initially reported only the consistent scalar equalities
and stopped before the common-dominator argument. This is not an objection to
the proof: the contradiction uses exact robustness and a single `b` carrying
both B-to-C arcs, information absent from the scalar ledger. A later formal
reconstruction supplied the complete proof above, and a line-by-line audit
verified each exact-distance and degree-census step.
