# Common-`C` reduction in the distinct-low-witness `m=7` family

## Scope

Let `D` be an order-18 oriented SNC counterexample chosen first
vertex-minimal and then arc-minimal, with exactly seven missing pairs.  Its two
outdegree-nine vertices are `r,q`; every other vertex has outdegree eight.
Assume the disjoint low-witness family `D` from the exhaustive witness-pattern
cover: low vertices `u != v` robustly witness `u->r` and `v->q`, and no low
vertex robustly witnesses both highs.

Write, for `s in {u,v}`,

```
A_s=N+(s),  B_s=N++(s),  C_s=V(D)\({s} union A_s union B_s),
S_s={s} union A_s.
```

Thus `|S_s|=9`, `|B_s|=7`, and `|C_s|=2`.  This note treats the common
inaccessible-pair branch

```
C_u=C_v=C.                                             (1)
```

It proves a sharp first reduction.  Put

```
t=|S_u intersect S_v|,
U=S_u union S_v,
P=S_u\S_v, Q=S_v\S_u,
W=V(D)\(C union U),
T=D-C,
x=e(C,W), z=h(C,W), h=h(T).
```

Here `h(X,Y)` counts missing pairs across a cut and `h(T)` counts holes wholly
inside `T`.

> **Theorem.** In (1), necessarily
>
> ```
> t=8,  x+z+h=2,  h>=1.                              (2)
> ```
>
> Consequently the entire common-`C` distinct-low branch reduces to exactly
> three aggregate cells:
>
> ```
> (x,z,h)=(0,0,2), (0,1,1), (1,0,1).                 (3)
> ```

This is a reduction, not an elimination of family `D`, of `m=7`, or of SNC.
No claim is made about the three cells in (3).

## 1. Exact overlap identity

The common pair `C` contains neither high vertex: `r in A_u` and `q in A_v`.
Hence its two vertices have total outdegree 16.  Every present pair from `C`
to `U` points from `C` to `U`, since neither root nor either first layer can
point to its inaccessible pair.  If `m` indicates that the pair internal to
`C` is missing, then

```
16 = (2|U|-h(C,U)) + x + (1-m).
```
Since `|U|=18-t`, this is

```
h(C,U)+m = 21-2t+x.                                  (4)
```
All seven holes split disjointly into the left side of (4), the `z` holes
across `C--W`, and the `h` holes of `T`.  Therefore

```
7 = 21-2t+x+z+h,
2t = 14+x+z+h.                                        (5)
```

Thus `t>=7`.  The case `t=9` would give `S_u=S_v`; then `v in A_u` and
`u in A_v`, a forbidden digon.  Hence `t in {7,8}`.  Equation (5) gives

```
t=7  => (x,z,h)=(0,0,0),
t=8  => x+z+h=2.                                      (6)
```

It remains to exclude the first line and the `h=0` part of the second.

## 2. A tournament source lemma

We use the following exact lemma.

> **Lemma.** Suppose `T` is a tournament on 16 vertices, every vertex of the
> full graph has outdegree at most nine, a vertex `a` has T-outdegree eight,
> and the two deleted vertices `C={c0,c1}` are exact second neighbors of `a`.
> Then `a` cannot be bad in the full graph.

Indeed, `a` has seven T-inneighbors.  Badness of `a`, after adding the two exact
C-second-neighbors, permits at most five exact T-second-neighbors.  Thus at
least two T-inneighbors are not reached from `a` by a T-two-walk.  Any such
vertex dominates `a` and all eight T-outneighbors of `a`, and hence has
T-outdegree at least nine.  Its full outdegree is at most nine, so its nine
listed T-outneighbors exhaust its outneighborhood.  For two such inaccessible
vertices, however, the tail of their tournament arc has the other as a tenth
T-outneighbor, a contradiction.

In the applications below, `a` lies in a root first layer, so `a` has no arc to
`C`; a vertex `w` with `w->C` and `a->w` makes both members of `C` exact second
neighbors of `a`.  Notice that the lemma does not need the identities of the
two high vertices or any separate hypothesis on their C-arcs.

## 3. Excluding `t=7`

By (6), `T` is a tournament and every member of `W` dominates both vertices of
`C`.  Here

```
|S_u intersect S_v|=7, |P|=|Q|=2, |W|=5.
```

Fix `w in W`.  Robustness of `u->r` gives a predecessor of `w` in
`A_u\{r}`.  The tournament source lemma excludes every low predecessor.
Therefore the only possible predecessor is the other high `q`; in particular
`q in A_u` and `q->w`.  Applying the symmetric argument at `v` gives
`r in A_v` and `r->w`.  This holds for every `w in W`, so `r,q` both lie in
`S_u intersect S_v` and both dominate `W`.

Because family `D` has no shared low robust witness, `u` is not robust for
deleting `q`.  Since `u->q` and `u` is already tight, there is some
`b_q in B_u` whose only `A_u`-predecessor is `q`:

```
P_u(b_q):={a in A_u:a->b_q}={q}.                     (7)
```
Similarly there is `b_r in B_v` with `P_v(b_r)={r}`.  No member of `W` can be
either private endpoint, because every member has both `q` and `r` as
predecessors.  Hence

```
b_q in Q,  b_r in P.                                 (8)
```

Now classify the two roots.  They cannot both lie in `S_u intersect S_v`,
which would create the digon `u<->v`.  They cannot both lie outside the
intersection either: then `u in P`, `v in Q`, so each root puts the other in
its exact-second layer, forbidding both directions of the pair `uv`; but `T`
is a tournament.  Thus exactly one root lies in the intersection.  Suppose
without loss that `u` does.  Then `u in A_v`, while every member of `P` is an
outneighbor of root `u`.  In particular `u->b_r`, contradicting
`P_v(b_r)={r}` because `u != r`.  This excludes `t=7`.

## 4. Excluding the `t=8,h=0` cells

Now `|P|=|Q|=1`, `|W|=6`, and `T` is again a tournament.  Equation (6) says
`x+z=2`.  Let

```
K={w in W : w dominates both vertices of C}.
```

Every C-to-W arc or C--W hole is a defect from membership in `K`; there are
only `x+z=2` such pair-defects.  Hence `|K|>=4`.  Applying the tournament
source lemma and robustness to any `w in K` forces

```
q in A_u, r in A_v, and q,r -> K.                    (9)
```

The same private-endpoint argument gives `b_q in B_u` with sole predecessor
`q` and `b_r in B_v` with sole predecessor `r`.  Both roots cannot lie in the
intersection, and if neither does then `P={u}`, `Q={v}` makes the root pair
mutually forbidden despite `T` being a tournament.  Thus exactly one root lies
in the intersection.  Suppose `u` does.  Then `Q={v}` and `P={p}`.  The endpoint
`b_q` is not `v` because `v->q`; the endpoint `b_r` is not `p` because
`u in A_v` and `u->p`.  Neither endpoint lies in `K` by (9).  Therefore

```
b_q,b_r are distinct members of W\K.                 (10)
```

They are distinct: if `b_q=b_r=b`, the first private relation gives `q->b`
and `r` not pointing to `b` (because `r in A_u`), whereas the second gives
`r->b` and `q` not pointing to `b` (because `q in A_v`), a contradiction.

There are two distinct vertices in (10), and only two C--W pair-defects in
total.  Thus `W\K={b_q,b_r}` and each private endpoint is incident with exactly
one defect.  Whether that defect is a C-to-endpoint arc or a hole, the endpoint
dominates the other C vertex.  It has full outdegree eight and therefore
T-outdegree exactly seven.

The private relation `P_u(b_q)={q}` now forces `b_q` to dominate all seven
members of `A_u\{q}`.  These are its complete seven T-outneighbors, so it does
not dominate `b_r`, and the tournament forces `b_r->b_q`.  Symmetrically,
`P_v(b_r)={r}` and T-outdegree seven force `b_q->b_r`.  This is a digon,
contradiction.  Therefore `h` cannot be zero.

Combining this with (6) proves (2)--(3).

## Reproducibility and scope guard

The transparent companion audit

```
python3 experiments/m7_family_d_common_c_reduction.py
```

checks the exact overlap arithmetic, the tournament-source count, all
root-intersection cases used in the two tournament branches, the distinctness
repair for the private endpoints, and the three surviving aggregate cells.  It
is a finite audit of the displayed case split, not a graph-completion solver
and not an UNSAT certificate for the remaining cells.
