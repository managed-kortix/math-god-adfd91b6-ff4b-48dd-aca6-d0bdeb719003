# Tick 20: human elimination of the `m=8, rho=4` row

## Theorem

In the order-18, eight-missing-pair normal form of tick 13, the row
`(p,rho,e)=(7,4,1)` is impossible.

## Proof

Retain the notation of tick 18:

```
A=N+(v), B=N++(v), C={c0,c1}, T=D[{v} union A union B].
```

Here `|A|=8`, `|B|=7`, the unique degree-nine vertex `r` lies in `A`, every
other vertex has outdegree eight, no arc points from `A` to `C`, and every
`b in B` has a predecessor in `A'=A\{r}`. In the present row seven missing
pairs are charged to the C--`({v} union A)` zone and one further pair remains.

If the further missing pair lies between `B` and `C`, then `T` is a tournament.
There are nine B-to-C arcs, so some `b in B` dominates both C vertices. Choose
`a in A'` with `a->b`. The tournament argument of tick 18 gives at least six
exact second neighbors of `a` in `T`, and the two C vertices are two more,
contradicting badness. We may therefore assume every B--C pair is present and
`T` has exactly one missing pair.

There are now ten B-to-C arcs. Hence the set

```
S={b in B: b->c0 and b->c1}
```

has size at least three.

Fix `b in S` and any predecessor `a in A'` of `b`. Both C vertices are exact
second neighbors of `a`. Put `X=N_T+(a)`. Then `|X|=8`; among the seven other
vertices of `T`, call a vertex inaccessible if it is not reached from `a` by a
two-walk in `T`. An inaccessible vertex not using the unique missing pair must
dominate `a` and every member of `X`, and therefore has outdegree at least nine;
it must be `r`. The unique missing pair can support at most one additional
inaccessible vertex. Thus there are at most two inaccessible vertices.

Badness of `a`, after the two additional exact second neighbors in `C`, forces
there to be exactly two inaccessible vertices. One is `r`; the other is
supported by the unique missing pair. In particular the missing pair is not
incident with `r`, and

```
r->a, r->X, N_T+(r)={a} union N_T+(a).                 (1)
```

At most one vertex `a in A'` can satisfy (1). Indeed, if distinct `a,a'` did,
then equality with the same nine-element set `N_T+(r)` would imply both
`a->a'` and `a'->a`. Consequently there is a single vertex `a* in A'` such
that every predecessor in `A'` of every member of `S` equals `a*`. Since each
member has at least one such predecessor,

```
N-(b) intersect A'={a*} for every b in S.               (2)
```

Now choose `b in S` not incident with the unique missing pair; this is possible
because `|S|>=3`. The following nine distinct arcs leave `b`:

* `b->c0,b->c1`, by membership in `S`;
* `b->v`, because `v->b` is forbidden by `b in N++(v)` and the pair is present;
* `b->a` for each of the six vertices `a in A'\{a*}`, by (2) and presence of
  the pairs.

Thus `d+(b)>=2+1+6=9`. But `b in B` and the unique degree-nine vertex is
`r in A`, so `d+(b)=8`, a contradiction.

## Hostile audit notes

The essential quantifier in (2) is pointwise: `a*` is not merely the unique
common predecessor of all members of `S`; it is the only `A'` predecessor of
each one. This follows because *every* such predecessor enters the equality
case (1), and at most one vertex can satisfy (1). The unique T-hole can spoil
the final nine-neighbor count for at most one member of `S`, since every counted
pair has exactly one endpoint in `S`. A proposed local evasion template failed
this check: its unspoiled common dominators already had the nine forced
outneighbors above.
