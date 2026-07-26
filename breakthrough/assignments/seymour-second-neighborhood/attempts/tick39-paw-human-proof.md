# Tick 39: human elimination of the paw hole shape

Use the isolated-root `m=9,k=4` normal form and the shape-independent notation
of `tick38-c4-human-proof.md`. Its B-row degree count uses only the four-hole
budget and proves that the set P of A' predecessors of common C-dominators has

```
|P|>=4.                                             (1)
```

Suppose instead that the four T-holes form a paw. Label them

```
01, 02, 12, 03,
```

so 0,1,2 form the triangle and 3 is pendant at 0.

Fix `a in P` and put `S={a} union N_T+(a)`. As in tick 38, badness forces at
least two vertices of `T\S` to be inaccessible by a two-walk in T. If `t` is
inaccessible and `q(t)` holes join it to S, then every present pair between t
and S points from t into S. Exact outdegree eight gives

```
q(t)>=1,                                           (2)
```

and when `q(t)=1`, those eight forced outneighbors exhaust its entire row.
Every inaccessible vertex is therefore on the paw.

There cannot be three inaccessible vertices. Any triple containing both 0 and
3 leaves 3 with no hole into S; the triple 012 leaves one of 1,2 with no hole
into S; and for 123, all three crossing-hole counts are one, so the present
pairs 13 and 23 cannot both be oriented without giving an inaccessible vertex
an additional outneighbor. Hence every source has exactly two inaccessible
vertices.

The pair 03 is impossible by (2). The remaining five packets and their exact
row identities are

```
P01: S=N+(1) union {2},
P02: S=N+(2) union {1},
P12: S=N+(1) union {0},
P13: S=N+(3) union {0},
P23: S=N+(3) union {0}.                           (3)
```

For example, in P01 vertex 2 lies in S and inaccessible vertex 1 has exactly
one crossing hole, so `N+(1)=S\{2}`. The other identities follow symmetrically;
in P13, vertex 3 has its sole hole-neighbor 0 in S and is saturated, while the
endpoint-packing inequality forces 2 into S. Thus every packet determines S
from a fixed global outneighborhood row. Since one fixed closed outneighborhood
S supports at most one source, each packet supports at most one member of P.

It remains to compare packet types. Define the orientations of the two present
pairs incident with 3 by

```
x=1 iff 1->3,   y=1 iff 2->3.
```

Saturation gives the complete compatibility table

```
packet   required condition
P01      x=1 iff 3 is in S        (y unrestricted)
P02      y=1 iff 3 is in S        (x unrestricted)
P12      x=y
P13      (x,y)=(1,0)
P23      (x,y)=(0,1).
```

For P12, if 3 is in S then both inaccessible vertices dominate it; if 3 is
outside S, both are saturated and the present pairs point from 3 toward them.
For P13, saturation of 3 forces `1->3`, while 2 lies in S and hence `3->2`;
P23 is symmetric.

The last three conditions are pairwise incompatible. Therefore an orientation
contains at most one source of types P12, P13, P23, together with at most one
P01 source and at most one P02 source. Hence

```
|P|<=3,                                             (4)
```

contradicting (1). The paw T-hole shape is impossible uniformly in rho.

The saturation clauses are essential. A weaker packet census that records only
forced positive arcs admits spurious four-source families with two different
P23 sources; equation (3) shows that both would reconstruct the same S and
force a digon between their sources.

This is a restricted shape elimination inside `n=18,m=9,k=4`, not an order-18
elimination and not a proof of SNC.
