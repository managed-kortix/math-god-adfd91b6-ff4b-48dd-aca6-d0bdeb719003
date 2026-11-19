# Hostile audit of the order-18, seven-hole normal form

## Scope and minimality hypotheses

Let `D` be an order-18 SNC counterexample chosen first vertex-minimal and then
arc-minimal, and suppose exactly seven unordered pairs are missing. This note
only sharpens the resulting finite normal form and breaks one tempting witness
separation claim. It does not eliminate `m=7`.

Arc counting gives 146 arcs, so (using `delta+(D)>=8`) exactly two vertices
`r,q` have outdegree nine and all other vertices have outdegree eight. The
**vertex-minimal** deletion argument, not arc minimality, says that for each
high vertex `h` there is `w->h` such that

```
d+(w)=d++(w)+1,
N++_{D-h}(w)=N++_D(w).                               (1)
```

Indeed a Seymour vertex of `D-h` must point to `h`; restoring `h` increases its
first degree by one and cannot remove an exact second neighbor. Strict badness
in `D` makes every inequality tight. For this **vertex deletion**, exact second neighborhoods can only shrink:
paths are removed, while direct arcs between surviving vertices are unchanged;
moreover `h` was a first neighbor, not an exact second neighbor.  Consequently
(1) is equivalent here to every old exact-second endpoint retaining a two-walk
that avoids `h`.  The possibility of creating a new exact-second endpoint
belongs to **arc deletion** (when the deleted head ceases to be a first
neighbor), not vertex deletion.

Arc minimality is separate. For an arc `x->y`, if `g_xy` records that `y`
becomes an exact second neighbor after deletion and `L_xy` is the set of old
exact second endpoints whose every two-walk starts through `y`, then

```
g_xy-|L_xy| >= (d+(x)-d++(x))-1.                    (2)
```

Nothing below silently derives (2) from vertex minimality.

At least one high vertex has a low witness: choose one witness for each of
`r,q`; if both chosen witnesses were high, the two arcs would form a digon.
Fix a low witness `v->r` and put

```
A=N+(v), B=N++(v), C=V(D)\({v} union A union B).
```

Then `|A|=8, |B|=7, |C|=2`, `r in A`, and `q` lies in exactly one of `A,B,C`.
Every `b in B` has an `A\{r}` predecessor, since its old exact-two status
survives deletion of `r`; and no arc goes from `{v} union A` to `C`.

## Exact two-row ledger

Write `C={c0,c1}` and use the following labelled variables:

```
x_i = 1[d+(c_i)=9],              so x_0+x_1=epsilon=1[q in C],
m   = 1[c0c1 is missing],
d_i = 1[c_i->c_(1-i)],           so d_0+d_1=1-m,
a_i = number of holes c_i--({v} union A),
b_i = number of holes c_i--B,
r_i = e({c_i},B),                rho=r_0+r_1.
```

All present pairs from `c_i` to `{v} union A` point out of `c_i`. Its exact
outdegree row is therefore

```
8+x_i = 9-a_i+d_i+r_i,
r_i = x_i+a_i-1-d_i.                               (3)
```

Let `h` be the number of holes in the complementary rooted graph
`T={v} union A union B`. All seven holes occur in these two C cuts, inside `C`,
or in `T`, and the tick-11 zone is

```
Z_v = holes incident with C but not C--B,
|Z_v|=a_0+a_1+m=3+rho-epsilon,                     (4)
|M\Z_v|=b_0+b_1+h=4+epsilon-rho.                   (5)
```

In particular the actual location ranges are sharper than the old prose:

```
q in A or B: 0 <= rho <= 4;
q in C:      0 <= rho <= 5.                         (6)
```

For a fixed `epsilon`, the C-row possibilities do not depend on whether a
non-C high lies in A or B. A transparent integer census imposing (3), seven holes, nonnegative `h`,
and `0<=r_i<=7-b_i` gives:

```
epsilon=0: 210 labelled rows, 108 modulo swapping c0,c1,
             rho multiplicities 45,60,54,36,15 for rho=0,...,4;
epsilon=1: 756 labelled rows, 378 modulo swapping c0,c1,
             rho multiplicities 126,180,180,144,90,36 for rho=0,...,5.
```

These corrected totals supersede the preliminary `h=0` counts
`105/54` and `336/168`; those omitted complementary T-holes and must not be
used. These are scalar rows only, not graph completions. They are the natural
first finite cover; each row still needs hole placement, C--B orientation,
predecessor support, exact badness, both vertex-deletion witnesses, and (2).

## Exact-distance-two warning

For the low root, `B=N++(v)` means exact distance two:

```
b in B iff v not->b and exists a in A with a->b.
```

A length-two walk ending at a member of `A=N+(v)` does not put that endpoint in
`B`. Likewise, when an arc `x->y` is deleted, `y` is a gain only when an
alternate `x->z->y` exists, because the old first-neighbor exclusion has
vanished. Any model using raw length-two-walk endpoints in either place is
unsound.

## A concrete breaker: the two high vertices need not have distinct low witnesses

A tempting strengthening of tick 12 is that the two high vertices can be
assigned distinct low robust witnesses (and hence two distinct zones). This
does **not** follow from the degree census, the seven-hole budget, or one rooted
exact-distance-two layer.

`experiments/m7_same_low_witness_relaxation.py` constructs an exact local
realization with highs `1,2` and a single low vertex `0` witnessing deletion of
both. It has seven holes

```
0-10, 0-12, 1-17, 2-16, 5-10, 5-11, 6-16.
```

outdegrees `d+(1)=d+(2)=9` and all other outdegrees eight, and

```
N+(0)={1,...,8},
N++(0)={9,...,15},
N++_{D-1}(0)=N++_{D-2}(0)={9,...,15}.
```

Thus vertex `0` is a valid tight deletion witness for both highs in this local
relaxation. Its zone has `rho=0, epsilon=0, |Z_0|=3`, exactly as (4) requires.
The realization is deliberately **not** an SNC counterexample: several other
vertices are Seymour, and global arc minimality is not imposed. Its rigorous
use is narrower: any overlap proof that starts by asserting two distinct low
witnesses or two distinct zones has a missing argument. A complete m=7 split
must include a shared-low-witness branch.

The high--high alternative likewise cannot be killed by a bare “three targets
need three B supports” count: a single B outneighbor of the high witness can
dominate the low root and both members of its C-set. Additional badness or
arc-gain/loss information is indispensable.

## Next finite split

A sound cover begins with three witness patterns, not the two-zone assumption:

1. one low vertex witnesses both highs;
2. two distinct low witnesses (their inaccessible C-pairs may overlap in 0, 1,
   or 2 vertices; tick-12's `2x2` statement applies only to overlap 0);
3. a low witness `v->q` and a high witness `q->r` (or the symmetric ordering).

The location refinement is pattern-specific: the shared root has the other high
in `A`; two distinct low roots each require the other-high `A/B/C` split; and
in the mixed chain `v->q->r`, the other high lies in `A_v` or `B_v`.
The exhaustive coarse cover is recorded separately in
`2026-11-19-m7-witness-pattern-cover.md`.
