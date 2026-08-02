# Tick 52: rooted clean-sink theorem and residual application

## Status and scope

The theorem below is a proved local consequence of the rooted order-18 normal
form.  Its exhaustive application eliminates 34,810 **memberships** in the
frozen 23-group residual campaign.  A membership is a pair consisting of a
canonical parent and one feasible aggregate pointwise C state `(r,t)`; one
parent may have several memberships.  Therefore 34,810 must not be reported as
34,810 distinct parents.  This result does not alter, solve, or certify UNSAT
for any of the 23 frozen group CNFs, and it is not an order-18 or SNC theorem.

## Definitions

Let `s` be the fixed root, `A=N+(s)`, `B=N++(s)`, and let `C` be the remaining
cell.  Put `U={s} union A`, so `|U|=9`.  Root exactness gives no arc from `U` to
`C`; hence every present U-C pair is directed from C to U.

For `c in C`, write

```
delta(c) = number of internal-C arcs directed out of c,
x(c)     = number of arcs from c to B,
tau(c)   = 1 if d+(c)=9, and 0 if d+(c)=8.
```

A **clean sink** is a C vertex satisfying

```
tau(c)=1,  delta(c)=0,  x(c)=0.
```

Here "sink" refers only to the internal-C orientation and C-to-B choices; the
vertex dominates every present vertex of U.

## Rooted clean-sink theorem

In the order-18, six-missing-pair, vertex-minimal and then arc-minimal
counterexample normal form, no feasible realization contains a clean sink.

### Proof

Let `c` be a clean sink and let `h_U(c)` count missing pairs from `c` to U.
All present U-C pairs point from c to U.  The three parts of its outdegree are
therefore

```
d+(c) = 9-h_U(c) + delta(c) + x(c).
```

Since c is high and clean, the left side is 9 and the last two terms vanish.
Thus `h_U(c)=0` and

```
N+(c)=U.
```

Every `b in B=N++(s)` has some predecessor `a in A` with `s->a->b`.  Because
`c->a`, every B vertex is reached by a surviving two-walk `c->a->b`.  No vertex
of U is an exact second neighbor because it is already a first neighbor.  No
other C vertex is reached through U, since root exactness forbids all arcs from
U to C.  Finally c has no C outneighbor and no B outneighbor.  The partition
`{c},U,B,C\{c}` therefore proves

```
N++(c)=B.
```

Delete the present arc `c->s`.  The first neighborhood of c becomes A and its
exact second neighborhood remains B: all walks `c->a->b` remain, while no
vertex of A points to s or C.  Hence c remains bad, with `d+=8>d++`, after the
deletion.  Every other first neighborhood is unchanged, and deleting an arc
cannot create a two-walk, so no other bad vertex can become Seymour.  The
deleted graph is still a counterexample, contradicting arc minimality.  This
proves the theorem.

## Exhaustive residual predicate

For each frozen residual membership `(parent,r,t)`, the application enumerates:

1. every orientation of every present internal-C pair;
2. independently for each C vertex, each target degree in `{8,9}` compatible
   with its forced C-to-U arcs, chosen internal-C outdegree, and available C-B
   pairs; and
3. only products whose sums are exactly `r=sum x(c)` and `t=sum tau(c)`.

The membership is eliminated exactly when **every** such pointwise realization
contains a clean sink.  Universal quantification is essential: finding one
clean realization does not eliminate a membership.  The frozen streams retain
the group membership identity, accepted-parent ordinal, and cover index, so
membership counts and distinct-parent counts remain separately auditable.

`experiments/m6_clean_sink_manifest.py` is the producer.
`experiments/check_m6_clean_sink_manifest.py` independently reconstructs the
full residual membership universe directly from the frozen placement cover and
filter, re-enumerates all pointwise realizations, and requires exact bytewise
agreement with both disposition streams and their count/hash manifest.

## Limitations

The theorem uses root exactness, degree target 9, and arc minimality.  It says
nothing when the zero-internal-outdegree vertex is low, sends an arc to B, has a
hole to U, or occurs only in some feasible pointwise realizations.  Remaining
memberships are campaign targets; they are not asserted satisfiable.
