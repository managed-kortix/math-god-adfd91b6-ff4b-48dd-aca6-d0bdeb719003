# Exact cycle-support witnesses for fixture rows 80 and 118

## Result

Let `B` be a simple subdivision of fixture row 80 or fixture row 118 in the
rank-five kernel classification. Every kernel edge denotes one path, and an
edge of multiplicity two denotes two internally disjoint paths with the same
ends. For every physical row in which each support edge has an odd member and
the second member of each doubled edge is even, there is a DNN path-vector
certificate of excess at most four. The canonical shortest lengths attain
exactly four.

This packet is independent of the main paper. It neither changes the frozen
118-row classification nor claims a certificate for the other parity rows of
these two kernels.

## Path cost

After alternating the vector signs on an odd path, endpoints of correlation
`r` have transformed correlation `-r`; on an even path the transformed
correlation is `r`. If all transformed consecutive correlations are equal,
the exact excess of a path of length `l` is

`h_l(t)=l tan^2(arccos(t)/(2l))`.

At branch correlation `r=-1/2`, a direct odd path therefore costs

`h_1(1/2)=1/3`,

while a length-two even path costs

`h_2(-1/2)=2/3`.

The latter witness is algebraic without trigonometric coordinates: if its
branch vectors are `u,v` with `u dot v=-1/2`, the internal vector is `u+v`.
It is unit and has correlation `1/2` with both endpoints, so the two rational
step costs are each `(1-1/2)/(1+1/2)=1/3`.

Thus an odd/even doubled edge costs exactly one. Antipodal endpoints make a
direct odd edge cost zero. Fixed-parity path monotonicity shows that increasing
any canonical length by two cannot increase these costs. The branch Gram
matrices below, together with equal-angle planar interpolation on each path,
are consequently exact all-length witnesses.

## Fixture row 80

The support cycle, with doubled edges marked by `=`, is

`0-5=2-3=4-1=6=0`.

Use four unit Gram vectors `A,B,C,D` with exact matrix

```text
       A     B     C     D
A      1     0    1/2  -1/2
B      0     1   -1/2  -1/2
C     1/2  -1/2   1     0
D    -1/2  -1/2   0     1
```

This matrix is positive semidefinite: for example take orthonormal
`e1,e2,e3,e4` and

```text
A = e1,
B = e2,
C = (e1-e2)/2 + e3/sqrt(2),
D = -(e1+e2)/2 + e4/sqrt(2).
```

Assign branch vectors

```text
(u0,u1,u2,u3,u4,u5,u6)=(A,B,C,-C,-B,-A,D).
```

Every single support edge has correlation `-1`; every doubled support edge has
correlation `-1/2`. Hence the four odd/even pairs cost `4(1/3+2/3)=4`, while
the three remaining odd paths cost zero. This is nonuniform: it is neither a
simplex coloring nor a constant-correlation cycle.

## Fixture row 118

Here the support cycle is

`0-1=7-4=5-3=6-2=0`.

The four doubled edges form a matching. Use unit vectors `A,B,C,D` with Gram
matrix

```text
       A     B     C     D
A      1    1/2    0    1/2
B     1/2    1    1/2    0
C      0    1/2    1    1/2
D     1/2    0    1/2    1
```

This is positive semidefinite: it is `I+(1/2)A(C4)` and has eigenvalues
`0,1,1,2`. Assign

```text
(u0,u1,u2,u3,u4,u5,u6,u7)=(A,-A,-D,-C,-B,C,D,B).
```

Again every single edge is antipodal and every doubled edge has correlation
`-1/2`, so the exact canonical excess is four and every same-parity lengthening
has excess at most four.

## Matching-doubled cycle lemma

The row-118 construction is the following reusable statement.

**Lemma.** Let an even support cycle consist of `2d` edges alternating between
`d` single edges and `d` doubled edges, where `d>=3`. On every support edge
choose one odd path, and on every doubled edge let its companion be even. Then
the subdivision has a DNN certificate of excess at most `d`.

To construct the vectors, take the exact cyclic Gram matrix

`R=I+(1/2)A(C_d)`.

It is positive semidefinite because its eigenvalues are
`1+cos(2 pi k/d)>=0`. Thus it is the Gram matrix of unit vectors
`x_0,...,x_(d-1)` with cyclic adjacent correlations `1/2`. Assign `x_i` and
`-x_i` to the ends of the intervening single edge. Those odd paths have
antipodal endpoints and cost zero. At a doubled edge the branch correlation is
`-x_i dot x_(i+1)=-1/2`, so its odd and even paths cost at most `1/3` and
`2/3`. Summing gives `d`.

For `d=4`, this is the displayed `C4` Gram matrix and gives the pentacyclic
budget four. The branch assignment is nonuniform around the original `2d`
cycle: alternating edges are collapsed antipodally, while the other edges use
the rational correlation `-1/2`. This is the matching-doubled extension of the
alternating-cycle construction.

## Exact audit

Run both modes:

```text
python3 research/rank-five-cycle-support-witness-verifier.py
python3 -O research/rank-five-cycle-support-witness-verifier.py
```

The verifier digest-locks the kernel fixture, selects explicit rows 80 and
118, checks every principal minor of both base and pulled-back branch Gram
matrices using rational arithmetic, checks the support correlations, and
reconstructs the exact excess `4` from four contributions `1/3+2/3`.
