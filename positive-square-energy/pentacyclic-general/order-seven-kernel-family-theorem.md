# Complete order-seven rank-five kernel-family theorem

## Theorem

Let `K` be any of the 23 order-seven kernels in the exact rank-five suppressed
kernel classification. Let `B` be any simple subdivision of `K`, and obtain
`G` by attaching an arbitrary rooted tree at each vertex of `B`. Then

`s^+(G) >= |V(G)|`.

Every case has a DNN certificate of excess at most four. The finite proof
ledger consists of 44,616 strict rational path-vector certificates and 24
exact symbolic equality certificates.

## Exhaustive ledger

The source-locked census independently reconstructs the following sets.

| set | exact count |
|:---|---:|
| order-seven kernels | 23 |
| labeled physical parity rows | 31,112 |
| automorphism orbits | 18,026 |
| regular-tetrahedron certificates | 14,306 |
| residual orbits | 3,720 |
| canonical plus eleven coordinate frontiers | 44,640 |

Every kernel has eleven suppressed paths. For each residual parity orbit, the
finite frontier is its canonical shortest vector and the eleven vectors formed
by adding two to one path length. Fixed-parity path monotonicity covers every
coordinatewise longer length vector. The exact frontier partition is

| method | exact targets |
|:---|---:|
| strict rational stereographic path vectors | 44,616 |
| exact K80 cycle-support Gram equalities | 24 |
| total | 44,640 |

The key audit derives all 44,640 keys directly from the census residuals and
the frontier set `{canonical,0,...,10}`. It rejects duplicate, omitted, and
extraneous raw keys. Removing the strict rational keys leaves exactly six K80
parity rows at each of `canonical`, `0`, `3`, and `6`, and no other key.

## Strict rational certificates

For each of 44,616 targets, the raw result fixture records six rational
stereographic parameters for every branch and internal vector. The verifier
reconstructs the seven-dimensional unit vectors over `Fraction`, rebuilds the
eleven physical paths and their exact lengths, and sums the transformed step
costs

`(1-r)/(1+r)`.

It requires the sum to equal the stored reduced fraction and to be strictly
less than four. Floating-point optimizer values have no proof role.

## Exact K80 cycle-support lemma

In pair order

`01,02,03,04,05,06,12,13,14,15,16,23,24,25,26,34,35,36,45,46,56`,

K80 has support cycle

`0-5=2-3=4-1=6=0`,

where the four edges incident with branch `6` through `0,1` and the two links
`25,34` are doubled. Physical path coordinates `0,3,6` are the three single
support edges `05,23,14`. The six unresolved parity rows are precisely

`(q05,q23,q14) in {(0,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1),(1,1,1)}`,

where `q=0` means the canonical path is even and `q=1` means it is odd. Every
doubled edge has one odd and one even path.

For signs

`a=(-1)^q05`, `b=(-1)^q23`, and `c=(-1)^q14`,

use four unit vectors `X0,X1,X2,X3` with cyclic Gram matrix

```text
       X0      X1      X2      X3
X0      1    -a/2       0     -1/2
X1   -a/2       1    -b/2        0
X2      0    -b/2       1     -c/2
X3   -1/2       0    -c/2        1
```

When `abc=1`, this is the exact sign-switch transport of
`I-(1/2)A(C4)`, whose eigenvalues are `0,1,1,2`. When `abc=-1`, the same
switching leaves one frustrated cycle edge and the eigenvalues are
`1-1/sqrt(2),1-1/sqrt(2),1+1/sqrt(2),1+1/sqrt(2)`. Thus every one of the six
matrices is positive semidefinite. Assign branch vectors

```text
(u0,u1,u2,u3,u4,u5,u6)=(X0,cX2,X1,bX1,X2,aX0,X3).
```

The verifier does not rely only on this factorization argument. For every one
of the six sign rows it reconstructs the exact `4 x 4` base matrix and its
pulled-back `7 x 7` branch matrix, then checks every principal minor of both.

Each single path has transformed endpoint correlation `1`, independent of
whether it is even or odd, and hence costs zero. Each doubled support edge has
branch correlation `-1/2`; its direct odd path costs `1/3`, while its
length-two even path costs `2/3`. For the latter the verifier checks the exact
three-vector midpoint Gram matrix with correlations `1/2,1/2,-1/2`. Thus the
four doubled edges contribute exactly

`4(1/3+2/3)=4`.

Lengthening coordinates `0`, `3`, or `6` by two leaves a zero-cost path because
its transformed endpoints still coincide. This proves all 24 equality keys,
not merely one representative parity row or one canonical target.

## All descendants

For each of the six K80 rows, the canonical and coordinate `0,3,6` targets use
the symbolic equality. The other eight one-coordinate frontiers are strict
rational certificates. Consequently every same-parity descendant is covered:
use a strict coordinate frontier if any path outside `{0,3,6}` grows, and use
the symbolic canonical/coordinate witness otherwise. Fixed-parity path
monotonicity then permits all additional increments by two. The verifier
explicitly checks the complete eleven-coordinate ledger for every residual,
including this symbolic/rational split for all six K80 rows.

## Fail-closed audit

| artifact | SHA-256 |
|:---|:---|
| rank-five kernel source | `027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884` |
| order-seven tetra census | `a9a05f50cf3db61cf104cd88c966f11064671d7b8027a83d065721e8b395d8b1` |
| raw rational experiment results | `7d581bfaa5d02f2ee7642f998371f48c29cdb961c2cebc43d3d2d666632c1a17` |
| theorem fixture | `1de37116d406f72abba33f85678be9f2eba38e71347a79c67bad5f159e2f1c16` |

The raw census and search retain `full_theorem=false`; theorem promotion occurs
only in the separately generated theorem fixture. Its verifier checks all
44,640 exact keys, every rational vector and cost, all 24 symbolic matrices and
path costs, all descendants, raw source locks, and ten hostile mutations. Run
both modes so no check can depend on `assert`:

```text
python3 pentacyclic/research/order7-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order7-kernel-family-theorem-verifier.py
```
