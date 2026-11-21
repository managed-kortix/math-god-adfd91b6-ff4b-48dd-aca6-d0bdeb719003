# Human exclusion of the shared-low family-S `h(T)=0` cell

## Status and exact scope

This note proves a computation-free terminal theorem and then applies it to the
committed order-18, seven-hole normal form.  It excludes exactly the globally
strict-bad, shared-low family-S cell in which

```text
T={w} union N+(w) union N++(w)
```

has no internal hole.  It does **not** exclude family D, family H, every
seven-hole graph, every order-18 graph, or a counterexample to Seymour's Second
Neighborhood Conjecture.

The standalone terminal theorem is stronger than the historical family-S cell:
it uses neither minimality nor deletion robustness once its rooted partition,
degrees, strict badness, and tournament core have been supplied.  The corollary
still uses vertex- and arc-minimality upstream to obtain those data.

Throughout, `N++(v)` is the exact second out-neighborhood: an endpoint reached
by a directed two-walk is excluded when it is already in `N+(v)` or is `v`.
For an induced subgraph `D[X]`, the notation `N++_{D[X]}(v)` has the same exact
meaning inside that induced graph.

## 1. Terminal theorem

> **Theorem (family-S tournament-core exclusion).** Let `D` be an oriented
> graph whose vertex set has a disjoint partition
>
> ```text
> V(D)={w} dotunion A dotunion B dotunion C,
> |A|=8, |B|=7, |C|=2.
> ```
>
> Let `r,q` be distinct vertices of `A`.  Suppose that:
>
> 1. `N_D+(w)=A`;
> 2. no arc points from `A` to `C`;
> 3. `d_D+(r)=d_D+(q)=9`, while every vertex of
>    `(A\{r,q}) union B` has outdegree eight;
> 4. every `a in A\{r,q}` is strictly bad:
>    `d_D++(a)<d_D+(a)=8`;
> 5. for `T={w} union A union B`, the induced graph `D[T]` is a
>    tournament.
>
> Then no such `D` exists.

### Proof

Put

```text
U={w} union A,
T={w} union A union B.
```

No vertex of `U` points to `C`: this is Hypothesis 2 for vertices of `A`, and
for `w` it follows from `N_D+(w)=A`.  Hence every outneighbor of every `u in U`
lies in `T`, and

```text
d_D[T]+(u)=d_D+(u)  for every u in U.                 (1)
```

Because `D[T]` is a tournament on sixteen vertices,

```text
sum_{t in T} d_D[T]+(t)=binom(16,2)=120.              (2)
```

The score sum over `U` is

```text
sum_{u in U} d_D[T]+(u)
 =d+(w)+d+(r)+d+(q)+sum_{a in A\{r,q}} d+(a)
 =8+9+9+6*8
 =74.                                                  (3)
```

Consequently

```text
sum_{b in B} d_D[T]+(b)=120-74=46.                   (4)
```

Every `b in B` has full outdegree eight, and the only vertices outside `T` are
the two vertices of `C`.  Thus

```text
e_D(B,C)
 =sum_{b in B} |N_D+(b) intersect C|
 =sum_{b in B} (8-d_D[T]+(b))
 =7*8-46
 =10.                                                  (5)
```

This counts actual arcs from `B` to `C`; no completeness of the `B--C` cut is
assumed.  Set `x_b=|N_D+(b) intersect C|`.  Since `x_b<=2` and the seven
values sum to ten, some `b in B` dominates both vertices of `C`.  Fix one such
`b`, so

```text
C subseteq N_D+(b).                                   (6)
```

We show that no ordinary vertex of `A` points to `b`.  Suppose instead that
`a->b` for some `a in A\{r,q}`, and write

```text
X=N_D[T]+(a).
```

By (1), `|X|=d_D+(a)=8`, so `a` has seven inneighbors in the 16-vertex
tournament `D[T]`.

We use a simple tournament fact.  If `z->a` and `z` is not reached from `a` by
a directed two-walk inside `T`, then `z->x` for every `x in X`: otherwise
`a->x->z`.  Therefore

```text
{a} union X subseteq N_D[T]+(z),
d_D[T]+(z)>=9.                                         (7)
```

But `d_D[T]+(z)<=d_D+(z)`, and Hypothesis 3 says that only `r,q` among the
vertices of `T` can have full outdegree at least nine.  Every `T`-inneighbor of
`a` except possibly `r,q` is therefore reached by an `a`-started two-walk in
`T`.  Such a reached inneighbor is an exact second neighbor in `D[T]`, so

```text
|N_D[T]++(a)|>=5.                                     (8)
```

By (6) and `a->b`, each `c in C` is the endpoint of `a->b->c`.  Hypothesis 2
says `a` does not point directly to `c`; hence both vertices of `C` are exact
second outneighbors of `a` in `D`.  They lie outside `T`.  Combining this with
(8) gives `d_D++(a)>=7`.  Strict badness and `d_D+(a)=8` give
`d_D++(a)<=7`.  Equality holds throughout: exactly five of the seven
`T`-inneighbors of `a` are exact second neighbors in `D[T]`, and exactly two
are inaccessible by a `T`-two-walk.  By (7), those two vertices must be
precisely `r,q`.

Applying (7) to each high gives

```text
{a} union X subseteq N_D[T]+(r),
{a} union X subseteq N_D[T]+(q).                      (9)
```

The set `{a} union X` has nine vertices, while each high has full outdegree
nine.  Yet the pair `rq` is present in the tournament `D[T]`.  Neither high is
in `{a} union X`, because both are inneighbors of `a`.  Whichever of `r,q` is
the tail of their mutual arc consequently has the nine outneighbors in
`{a} union X` and the other high as a tenth outneighbor, a contradiction.
Thus

```text
a not-> b  for every a in A\{r,q}.                    (10)
```

Finally, `w not-> b` because `N_D+(w)=A`; tournament completeness gives
`b->w`.  Equation (10) and tournament completeness similarly give
`b->a` for every one of the six vertices in `A\{r,q}`.  Together with (6),
the vertex `b` has the nine distinct outneighbors

```text
{w} union (A\{r,q}) union C,
```

of cardinality `1+6+2=9`.  This contradicts Hypothesis 3, which gives
`d_D+(b)=8`.  The theorem follows. `square`

The argument actually shows from (5) that at least three vertices of `B`
dominate both `C` vertices, but existence of one is enough.

## 2. Entry from the committed normal form

We now verify that the terminal theorem applies to the intended finite cell.
This dependency order matters: the exact degree sequence does not follow from
146 arcs and minimum outdegree eight alone.

### Minimum degree and lexicographic minimality

The frozen assignment records the established theorem that SNC holds whenever
`delta+(D)<=7`; hence a counterexample has minimum outdegree at least eight.
Choose a hypothetical counterexample first vertex-minimal and then arc-minimal,
as in `agents/tick1-structure.md`.

For an arc `x->y`, that note defines a gain indicator `g_xy`, the set `L_xy`
of exact-second endpoints lost on deleting the arc, and the deficit

```text
mu(x)=d+(x)-d++(x).
```

Arc minimality gives

```text
g_xy-|L_xy| >= mu(x)-1.
```

The necessary non-tail monotonicity argument is supplied in
`agents/tick2-hostile-structure-audit.md`: deleting `x->y` leaves every
non-tail first neighborhood unchanged and can only shrink a non-tail exact
second neighborhood, so only the tail can become Seymour.  Since `g_xy<=1`
and `|L_xy|>=0`, every deficit satisfies

```text
1<=mu(v)<=2.                                           (11)
```

### The missing maximum-degree step and exact census

For every vertex `v` of an order-18 graph, the three sets

```text
{v}, N+(v), N++(v)
```

are pairwise disjoint.  By (11),

```text
18 >= 1+d+(v)+d++(v)
   = 1+2d+(v)-mu(v)
   >= 2d+(v)-1.
```

Thus `d+(v)<=9` for every vertex.  This is the required maximum-degree
argument; it is not an independent solver constraint.

Seven missing unordered pairs leave

```text
binom(18,2)-7=146
```

arcs.  Since every degree lies in `{8,9}` and

```text
sum_v (d+(v)-8)=146-18*8=2,
```

exactly two vertices `r,q` have outdegree nine and the other sixteen have
outdegree eight.  This supplies the premise omitted in the bare degree-census
sentence of `attempts/2026-11-19-m7-hostile-normal-form.md`.

### Shared-low layers and the barrier

Vertex minimality supplies a tight deletion witness for each high; the exact
semantics and equality argument are audited in
`attempts/2026-11-19-m7-hostile-normal-form.md`.  The exhaustive witness split
in `attempts/2026-11-19-m7-witness-pattern-cover.md` has families S, D, and H.
In family S, one low vertex `w` witnesses both highs.  Therefore

```text
w->r, w->q,
A=N+(w), |A|=8,
B=N++(w), |B|=7,
C=V(D)\({w} union A union B), |C|=2,
r,q in A.
```

There is no arc from `A` to `C`: if `a->c` with `a in A` and `c in C`, then
`w->a->c`; because `c notin N+(w) union {w}`, exact-distance semantics would
put `c in N++(w)=B`, a contradiction.  Also `w` has no outarc to `C` by the
definition of `A`.

A counterexample is globally strictly bad, so in particular all six ordinary
vertices of `A` satisfy the terminal badness hypothesis.  Finally, `h(T)=0`
means that no unordered pair is missing inside
`T={w} union A union B`.  Since `D` is oriented, `D[T]` is a tournament.
Every hypothesis of the terminal theorem now holds.

> **Corollary.** In the committed order-18, seven-hole,
> vertex-minimal-then-arc-minimal SNC-counterexample normal form, no shared-low
> family-S configuration has `h(T)=0`.

The exact family-S refinement proves
`b_0+b_1+h(T)=4-rho` with nonnegative integer terms, and its complete census
contains exactly the five cells `h(T)=0,1,2,3,4`.  The corollary together with
the retained checked exclusions for `h(T)=1,2,3,4` therefore eliminates this
family-S branch of the committed normal form.  Families D and H remain, so no
full seven-hole, order-18, or SNC conclusion follows.

## 3. Dependency and hypothesis audit

The terminal theorem does **not** use:

- vertex or arc minimality;
- strong connectivity;
- deletion-robustness or its alternate-support condition after the partition
  is fixed;
- badness outside the six ordinary vertices of `A`;
- the degrees of the two vertices of `C`;
- the seven-hole count separately from the already-derived degree data and
  `h(T)=0`;
- a feed-vertex theorem, Landau sufficiency, SAT, or a proof certificate.

Robustness is used only upstream to identify the shared-low root and its exact
`8/7/2` layers.  Arc minimality is used only upstream for (11), hence the
maximum-degree cap and degree census.  The historical name “family S” still
refers to that upstream robust-witness reduction; dropping robustness from the
standalone terminal theorem does not remove it from the classification.

The following inputs are sharp for this proof route:

- exact-second semantics supplies the `A not-> C` barrier and makes the two
  `C` endpoints exact seconds of an ordinary predecessor;
- tournament completeness supplies both the inaccessible-inneighbor lemma and
  the reversal from `a not-> b` to `b->a`;
- both `C` endpoints and strict badness force two, not one, inaccessible
  `T`-inneighbors;
- the full score census makes those two vertices exactly `r,q`;
- six ordinary `A` vertices plus `w` and `C` give the final sharp count nine.

The dependency-free script `experiments/verify_m7_family_s_h0_human.py` checks
these arithmetic and local finite-logic steps.  It is an audit aid, not a
certificate for the upstream normal-form reduction and not an exhaustive
search over order-18 graphs.
