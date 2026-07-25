# Tick 3: universal `A -> B` incidence is impossible

In the `|A|=8,|B|=6` branch, suppose every one of the 48 arcs from `A` to `B`
is present. Then orientation forbids all arcs from `B` back to `A`. Let

```
U = (union_{b in B} N+(b)) \ B.
```

Every `u in U` is an exact second neighbor of every `a in A`. Boundary minimum
outdegree requires at least 48 outgoing arcs in total; at most 15 lie inside
`B`, so at least 33 go to `U`, and every target receives at most six. Hence
`|U|>=6`.

Let `H=D[A]`. Since `H` is an eight-vertex oriented graph, the established
`delta+<=7` theorem gives a Seymour vertex `a` in `H`. Exact-distance semantics
gives the disjoint identity

```
N++_D(a)=N++_H(a) disjoint-union U,
N+_D(a)=N+_H(a) disjoint-union B.
```

Therefore

```
d++_D(a) >= d+_H(a)+6 = d+_D(a),
```

contradicting badness. Thus every viable obstruction must have non-universal
predecessor signatures and selected `B->A` arcs. This rigorously kills the
tick-2 circulant partial obstruction and all its completions retaining universal
`A->B` incidence.
