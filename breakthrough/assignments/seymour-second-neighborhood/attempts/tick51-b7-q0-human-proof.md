# Tick 51: human elimination of the B7 forced q=0 cell

## Theorem

In the order-18, six-missing-pair, vertex-minimal and then arc-minimal
counterexample normal form, the B7 subcell

```
lambda = H_RC + H_AC + H_CC = 1,
q      = H_CB = 0,
r      = e(C,B) = 0
```

is impossible.  This eliminates all 8,847 canonical forced-child parents in
that cell, independently of the placement of the five holes wholly outside C.

## Proof

Let `s` be the root, `A=N+(s)`, `B=N++(s)`, and let `C={c,d}`.  In B7,
`|A|=8`, `|B|=7`, and put `U={s} union A`, so `|U|=9`.

The exact C-row identity in this branch is

```
number of degree-nine C vertices = 3-lambda+r.
```

Thus both C vertices have outdegree nine.  Root exactness says that neither
`s` nor any vertex of A points to C.  Hence every present C-U pair points from C
to U.  Since `q=0`, every B-C pair is present, and `r=0` makes every one point
from B to C.

For `x in C`, let `h_U(x)` be its number of holes to U and let
`delta_x` be one if x sends the internal C arc and zero otherwise.  There are no
C-to-B arcs, so

```
9 = d+(x) = 9-h_U(x)+delta_x,
```

and therefore `h_U(x)=delta_x`.  Choose a C vertex c with no internal
C-outneighbor: either endpoint if the C pair is missing, or the target if it is
present.  Then `h_U(c)=0`, whence

```
N+(c)=U.
```

We next claim `N++(c)=B` exactly.  Every `b in B` has an A-predecessor,
because `b in N++(s)`: choose `a in A` with `s->a->b`.  Then
`c->a->b`, so B is contained in the exact second neighborhood of c.  No vertex
of U is exact-second because every such vertex is already a first neighbor.
The other C vertex cannot be reached through U, since neither s nor A points to
C.  This exhausts the vertex partition, proving the claim.  Consequently

```
d+(c)=9,  d++(c)=7.
```

The arc `c->s` is present, since c has no U-hole.  Delete it.  The first
neighborhood of c becomes A.  Its exact second neighborhood remains B: all
paths `c->a->b` above survive, while no `a in A` points to s or to C.  Thus c
still has `d+=8>d++=7` after deletion.

For every other vertex, first neighborhoods are unchanged and deleting an arc
cannot create a new two-walk; hence its exact second neighborhood can only
shrink.  No other vertex can become Seymour.  The deleted graph is therefore
still a counterexample, contradicting arc-minimality.  This proves the theorem.

## Audits and scope

Two independent proof routes and a hostile exact-distance audit checked the
argument, including the possibility that `c-s` is missing, reachability of the
other C vertex, and the sign of the arc-deletion inequality.  A CNF differential
also found the contradiction by propagation for all 8,847 rows using only the
arc-minimality blocks for the two possible C-to-root arcs.  The human proof is
authoritative; the differential is regression evidence and not a certificate.

The hypothesis `q=0` is essential: with B-C holes, a selected C sink need not
dominate all of U or every B vertex need not point to it.  No claim is made here
for B7 `q=1,...,5`, B6, all order 18, or SNC.
