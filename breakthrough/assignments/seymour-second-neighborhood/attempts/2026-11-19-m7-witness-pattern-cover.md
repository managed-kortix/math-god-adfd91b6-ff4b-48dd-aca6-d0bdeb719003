# Exhaustive witness-pattern cover for order 18, `m=7`

## Status and scope

Let `D` be an oriented SNC counterexample on 18 vertices, chosen first
vertex-minimal and then arc-minimal, with exactly seven missing pairs. Let its
two outdegree-nine vertices be `r,q`; all other vertices have outdegree eight.
For each high vertex `h`, vertex minimality supplies at least one **robust
witness** `w->h` satisfying

```
d+(w)=d++(w)+1,
N++_{D-h}(w)=N++_D(w).
```

This note gives an exhaustive cover of the possible *chosen witness types* and
the first layer/overlap splits. It is not a cover of graph completions, and it
does not eliminate `m=7`. The companion script
`experiments/m7_witness_pattern_cover.py` checks only this coarse combinatorial
partition. It deliberately does not claim SAT/UNSAT or impose global badness.

## 1. Top-level cover

Choose one robust witness `w_r->r` and one `w_q->q`. A high witness for `r`
can only be `q`, and a high witness for `q` can only be `r`. Therefore the four
ordered low/high choices are

```
(w_r low, w_q low),
(w_r low, w_q=r),
(w_r=q,   w_q low),
(w_r=q,   w_q=r).
```

The last choice requires both `q->r` and `r->q`, a digon, and is impossible in
an oriented graph. Splitting equality in the first choice leaves exactly these
three admissible families, up to exchanging `r,q`:

```
S. shared low:    one low w satisfies w->r and w->q;
D. distinct lows: u->r and v->q with low u != v;
H. mixed:         v->q is low and q->r is high.
```

This is exhaustive even when a high has several witnesses.  It can be made
disjoint without an arbitrary selector: if the two sets of low witnesses
intersect, use `S`; otherwise, if each high has a low witness, use `D`; if one
high has no low witness, its witness must be the other high and the other high
must have a low witness (mutual high witnessing is impossible), so use `H`.

## 2. Family S: one low witness for both highs

Root at `w` and put

```
A=N+(w), B=N++(w), C=V(D)\({w} union A union B).
```

Then `|A|=8, |B|=7, |C|=2`. Because `w->r` and `w->q`, **both highs lie in
`A`**. Thus the other-high location is forced to `A`, `epsilon=0`, and only the
corrected epsilon-zero scalar ledger applies:

```
210 labelled C-rows, 108 modulo swapping the two C vertices,
rho=0,1,2,3,4 with labelled multiplicities 45,60,54,36,15.
```

There is one rooted partition, one inaccessible pair, and one zone—not two
independent witness zones. Robustness has to hold simultaneously after deleting
`r` and after deleting `q`. Equivalently, for every `b in B` there is

```
an A\{r} predecessor of b, and an A\{q} predecessor of b.       (S1)
```

This does **not** always force two distinct predecessors: one vertex of
`A\{r,q}` can satisfy both requirements. More exactly, if
`P_b={a in A:a->b}`, then (S1) says

```
P_b is not {r} and is not {q}.                                  (S2)
```

Hence a singleton `P_b` is allowed precisely when its member lies in
`A\{r,q}`. Any proposed shared-low contradiction that silently replaces (S2)
by `|P_b|>=2` is invalid.

The explicit local realization checked by
`m7_same_low_witness_relaxation.py` shows that this family is nonempty under
the degree, hole-budget, rooted exact-two, and simultaneous-deletion clauses.
It is not a counterexample and does not satisfy the full global hypotheses.

## 3. Family D: two distinct low witnesses

In the disjoint top-level classification, neither high's low-witness set meets
the other's; choose `u->r` and `v->q`.  For the coarse positive constraints
below, root simultaneously at these two distinct lows:

```
X_u={u} union A_u union B_u union C_u,
X_v={v} union A_v union B_v union C_v,
```

where each `A` has size 8, each `B` size 7, and each `C` size 2. For the first
coarse cover record

```
lambda_u = location of q in A_u,B_u,C_u;
lambda_v = location of r in A_v,B_v,C_v;
sigma_u  = location of v in A_u,B_u,C_u;
sigma_v  = location of u in A_v,B_v,C_v;
k         = |C_u intersect C_v|.
```

The pair `(sigma_u,sigma_v)=(A,A)` is impossible, because it would assert both
`u->v` and `v->u`. No other ordered location pair is excluded merely by the
root definitions.

There are two elementary caps on `k`. Viewed from the `u` partition, `C_v`
contains neither its root `v` nor its witnessed high `q`.  Of the two vertices
of `C_u`, remove `v` if `sigma_u=C` and remove `q` if `lambda_u=C`. These are
distinct because `v` is low. Hence

```
k <= 2 - 1[sigma_u=C] - 1[lambda_u=C].              (D1)
```

Symmetrically,

```
k <= 2 - 1[sigma_v=C] - 1[lambda_v=C].              (D2)
```

A safe coarse overcover is therefore

```
lambda_u,lambda_v in {A,B,C};
sigma_u,sigma_v in {A,B,C}, not both A;
0 <= k <= min(the two bounds D1,D2).                  (D3)
```

The checker counts 139 formal ordered labelled rows in this overcover (some may
later be empty after arc and hole-budget constraints):

```
k=0: 72,  k=1: 55,  k=2: 12.
```

Modulo exchanging the two rooted triples `(u,r)` and `(v,q)`, there are 76
orbits:

```
k=0: 39,  k=1: 30,  k=2: 7.
```

These numbers count only location/overlap indices, not the 108/378 scalar
C-row ledgers and certainly not full graphs.

For each root, use the corrected ledger according to its own epsilon:

```
epsilon_u=1[lambda_u=C], epsilon_v=1[lambda_v=C].
```

Thus a root with epsilon zero has 108 scalar row orbits and a root with epsilon
one has 378; the two choices cannot simply be multiplied, because they describe
the same seven holes and the same oriented graph.

The zone lower bound remains

```
|Z_u intersect Z_v| >= rho_u+rho_v-1-epsilon_u-epsilon_v.        (D4)
```

but its geometric interpretation depends on `k`:

* `k=0`: every common zone hole lies in the explicit `2 x 2` cut
  `C_u--C_v`; this is the valid tick-12 shard.
* `k=1`: write `C_u={z,a}`, C_v={z,b}`. Common-zone holes may be `a--b` **or**
  holes incident with the shared vertex `z`; a `2 x 2`-only argument is not
  valid.
* `k=2`: `C_u=C_v`; common-zone holes can occur throughout the common pair's
  incident zone. Treating this as the disjoint-pair shard is invalid.

The `k=1,2` bullets are warnings, not complete formulas for the intersection;
membership in a zone also excludes that root's `C--B` holes.

## 4. Family H: one low and one high witness

Up to swapping the high labels, take

```
v->q, q->r,
```

with low `v`.  In the partition rooted at `v`, `q` lies in `A_v`.  The walk
`v->q->r` shows that the other high `r` lies in `A_v` or `B_v`, never `C_v`.
Thus `epsilon_v=0`, only the 108 corrected epsilon-zero C-row orbits occur, and
there are two low-root location leaves:

```
r in A_v;  or  r in B_v.                              (H1)
```

In the second leaf, robustness of `v` under deletion of `q` gives an alternate
`A_v\{q}` predecessor of `r`; the displayed two-walk through `q` alone is not
enough.

The high root `q` has

```
d+(q)=9, d++(q)=8,
N++_{D-r}(q)=N++_D(q).
```

Let

```
A_q=N+(q), B_q=N++(q).
```

Then `|A_q|=9`, `|B_q|=8`, and these disjoint sets exhaust all 17 vertices
other than `q`.  There is no residual `C_q` layer and no second low-root
C-row ledger.  Since `v->q`, the reverse arc `q->v` is forbidden, so

```
v in B_q.                                             (H2)
```

Also, for every `c in C_v`, the arc `q->c` is absent: `q in A_v` and no arc
goes from `{v} union A_v` to `C_v`.  Exhaustion of the high-root layers then
gives

```
{v} union C_v subset B_q.                             (H3)
```

Robustness of `q` after deleting `r` requires alternate two-walks from `q` to
all three vertices in `{v} union C_v` through `A_q\{r}`.  A single
intermediary may cover all three targets, so no three-distinct-support
conclusion follows.

## 5. Correct finite refinement order

A sound exhaustive refinement architecture is therefore (the coarse positive
projections may overlap unless the top-level witness-set exclusions are also
encoded):

```
S: shared low
   -> one low-root ledger, epsilon=0 (108 scalar row orbits)
   -> simultaneous r/q robust-column signatures (S2)
   -> exact hole placement/orientation/global badness/arc minimality.

D: distinct lows
   -> one of 76 root-swap location/overlap orbits (or 139 labelled rows)
   -> each root's corrected epsilon-specific scalar ledger
   -> common seven-hole synchronization and zone intersection, split k=0/1/2
   -> both robust systems/global badness/arc minimality.

H: v->q->r
   -> low-root location r in A_v/B_v and epsilon=0 (108 scalar row orbits)
   -> forced v in B_q and alternate support of {v} union C_v through A_q\{r}
   -> global badness/arc minimality.
```

At every stage exact distance two, rather than raw length-two reachability, must
be used. The scalar rows are necessary projections only. Multiplying orbit
counts without synchronizing labels and the common seven-hole set is not a
cover proof.
