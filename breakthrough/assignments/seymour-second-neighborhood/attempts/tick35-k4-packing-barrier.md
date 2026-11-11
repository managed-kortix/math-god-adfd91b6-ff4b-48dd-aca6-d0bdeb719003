# Tick 35: exact endpoint-packing lemma and its sharp barrier

Work in the isolated-root `m=9,k=4` normal form.  Thus every vertex has
outdegree eight, `T={w} union A union B` has sixteen vertices, and the two
vertices outside `T` form `C`.  Let `b in B` dominate both vertices of `C`, and
choose a robust predecessor `a in A'` of `b`.  Put

```
S={a} union N_T+(a).
```

Then `|S|=9`. Both C vertices are accessible exact second neighbors, so badness
of `a` forces at least two vertices in `T\S` to be inaccessible from `a` by a
two-walk in `T`.

For such an inaccessible vertex `t`, let `q(t)` be the number of T-holes from
`t` into `S`.  Every present pair between `t` and `S` points from `t` into `S`:
an arc from a member of `N_T+(a)` to `t` would make `t` accessible.  Hence `t`
has exactly `9-q(t)` forced outneighbors in `S`.  Since its total outdegree is
eight, `q(t)>=1`, and it has at most `q(t)-1` outgoing slots outside `S`.

Consequently, for two inaccessible vertices `t,u`,

```
q(t)+q(u)+1[tu is a hole] >= 3.                 (1)
```

Indeed, if `tu` is present, one of its directions consumes an outside outgoing
slot of `t` or `u`, so `(q(t)-1)+(q(u)-1)>=1`; if it is a hole, the individual
bounds `q(t),q(u)>=1` suffice.

Equation (1) gives the four-matching contradiction in
`tick30-m9-k4-matching-proof.md`: there `q(t)=q(u)=1`, so `tu` must be a hole,
although each endpoint has already used its unique matching hole into `S`.
It does not extend uniformly to the other shapes.  The bound is sharp already
for the shape `P3 + 2K2`.  Label its holes

```
01, 12, 34, 56.
```

Choose `t=1`, `u=4`, and let `S` contain `0,2,3` and six hole-isolated
vertices, one of which is `a`. Orient `a` toward the other eight members of
`S`, orient `t` toward the seven members of `S\{0,2}` and toward `u`, and
orient `u` toward all eight members of `S\{3}`. The two vertices are
inaccessible, have exact outdegree eight, and use the sharp profile
`(q(t),q(u);1[tu hole])=(2,1;0)`.  The fourth hole `56` is unused.  Remaining
present pairs incident with `t` or `u` must point toward them; this is all that
is required for the local statement.

This is not a completion to a counterexample.  It is a counterconfiguration to
the tempting claim that four-hole endpoint packing alone synchronizes all
robust predecessor sets. A successful argument needs additional information,
for example coupling the different sets `S_a` associated with several
predecessors or using the badness and B-column degree equations of the five or
six common C-dominators. The computational `lambda` split records part of this
missing coupling.
