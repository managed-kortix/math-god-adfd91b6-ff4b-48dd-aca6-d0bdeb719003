# Classification of the rank-four suppressed kernels

This note classifies the kernels obtained from a loopless 2-connected
tetracyclic block by suppressing every vertex of degree two.  Parallel edges
are retained.  Here 2-connected means connected and without a cut vertex; the
two-vertex dipole is allowed under this convention.

## Statement

Let `K` be a finite loopless multigraph, with at least two vertices, no cut
vertex, minimum degree at least three, and cyclomatic rank

`beta(K)=|E(K)|-|V(K)|+1=4`.

Then `2 <= |V(K)| <= 6`, and `K` is isomorphic to exactly one of the 17
multigraphs in the list below.  There are respectively

`1, 2, 5, 4, 5`

types on `2,3,4,5,6` vertices.

## Encoding and list

For vertices `0,...,n-1`, encode a multigraph by the multiplicities in the
lexicographic upper-triangle order

`01,02,...,0(n-1),12,...,(n-2)(n-1)`.

The displayed representative is the lexicographically least such vector over
all vertex labellings.  The final column is its simplicity cost

`sigma(K)=sum_{u<v} max(m_uv-1,0)=|E(K)|-|supp(K)|`.

This is the minimum number of degree-two subdivision vertices required to
turn all parallel kernel edges into internally disjoint paths in a simple
subdivision: at most one edge in each parallel class can remain direct.

| No. | `n` | degree multiset | canonical upper triangle | `sigma` |
|---:|---:|:---|:---|---:|
| 1 | 2 | `5,5` | `5` | 4 |
| 2 | 3 | `5,4,3` | `1,2,3` | 3 |
| 3 | 3 | `4,4,4` | `2,2,2` | 3 |
| 4 | 4 | `5,3,3,3` | `0,1,2,1,2,1` | 2 |
| 5 | 4 | `4,4,3,3` | `0,1,2,2,1,1` | 2 |
| 6 | 4 | `4,4,3,3` | `0,1,2,2,2,0` | 3 |
| 7 | 4 | `4,4,3,3` | `0,1,2,3,1,0` | 3 |
| 8 | 4 | `4,4,3,3` | `1,1,1,1,1,2` | 1 |
| 9 | 5 | `4,3,3,3,3` | `0,0,1,2,1,0,2,2,0,0` | 3 |
| 10 | 5 | `4,3,3,3,3` | `0,0,1,2,1,1,1,1,1,0` | 1 |
| 11 | 5 | `4,3,3,3,3` | `0,0,1,2,1,1,1,2,0,0` | 2 |
| 12 | 5 | `4,3,3,3,3` | `0,1,1,1,1,1,1,0,1,1` | 0 |
| 13 | 6 | `3,3,3,3,3,3` | `0,0,0,1,2,0,1,1,1,2,1,0,0,0,0` | 2 |
| 14 | 6 | `3,3,3,3,3,3` | `0,0,0,1,2,0,1,2,0,2,0,1,0,0,0` | 3 |
| 15 | 6 | `3,3,3,3,3,3` | `0,0,0,1,2,1,1,0,1,1,1,0,1,0,0` | 1 |
| 16 | 6 | `3,3,3,3,3,3` | `0,0,1,1,1,0,1,1,1,1,1,1,0,0,0` | 0 |
| 17 | 6 | `3,3,3,3,3,3` | `0,0,1,1,1,1,0,1,1,1,0,1,1,0,0` | 0 |

For the published checksum, relabel each row first by nondecreasing vertex
degree and then by the least upper-triangle vector among degree-preserving
labellings.  Serialize its degree multiset in nonincreasing order and its
nonzero one-based edges, omitting exponent one; for example the first line is
`n=2; deg=(5, 5); edges=12^5`.  The 17 lines, including one final LF, have
checksum

`d89e6e60c66e480ba89e662ab90b5ace211cbcff7292f92ad1614bb0937eb8e9`.

## Hand proof of completeness

Put `n=|V(K)|` and `m=|E(K)|`.  Rank four gives `m=n+3`.  The handshake
lemma therefore gives

`sum_v (deg(v)-2)=2m-2n=6`.                                      (1)

Every summand in (1) is at least one, so `n<=6`.  A loopless graph of minimum
degree three cannot have one vertex, hence `2<=n`.  Moreover, writing
`x_v=deg(v)-2`, the positive integers `x_v` form a partition of six.  The
loopless incidence equations and the no-cut-vertex condition reduce those
partitions as follows.

| `n` | possible degree multisets after the incidence test | no-cut types |
|---:|:---|---:|
| 2 | `5,5` | 1 |
| 3 | `5,4,3`; `4,4,4` | 1+1 |
| 4 | `5,3,3,3`; `4,4,3,3` | 1+4 |
| 5 | `4,3,3,3,3` | 4 |
| 6 | `3,3,3,3,3,3` | 5 |

Here is a direct way to perform the small incidence test.  Introduce one
nonnegative integer `a_ij` for every pair `i<j`.  For each candidate degree
multiset solve

`sum_{j != i} a_min(i,j),max(i,j) = d_i`                         (2)

up to permutations preserving the degree multiset.  Reject a solution if its
positive support is disconnected or if deleting one vertex disconnects that
support.  Parallel multiplicities do not affect this deletion test.  Ordering
the surviving vectors lexicographically over all vertex permutations gives
exactly the rows in the table.

For `n=2`, (2) forces `a_01=5`.  For `n=3`, the three equations uniquely give

`a_01=(d_0+d_1-d_2)/2`, `a_02=(d_0+d_2-d_1)/2`,
`a_12=(d_1+d_2-d_0)/2`,

and integrality plus the no-cut deletion test leaves precisely `(1,2,3)` and
`(2,2,2)`.
For `n=4`, a degree-six vertex is impossible because its three neighbors have
total degree only six and would spend all incidences on it, leaving a star
support and making the center a cut vertex.  The excess partitions `3+1+1+1`
and `2+2+1+1` give the two degree rows shown; solving (2) and deleting each
vertex leaves one and four orbits, rows 4--8.  For `n=5`, the unique excess
partition `2+1+1+1+1` gives degrees `4,3,3,3,3`; solving (2) and applying the
deletion test gives rows 9--12.  For `n=6`, equality in (1) forces every degree to be three;
the loopless cubic multigraph solutions without a cut vertex are rows 13--17.
This proves existence, exhaustion, and pairwise nonisomorphism because
distinct canonical vectors cannot lie in the same relabelling orbit.

## Independent executable audit

`research/rank-four-kernel-census-verifier.py` does not generate from this
proof table.  For each `2<=n<=6` it independently enumerates every weak
composition of `n+3` over the `n choose 2` unordered pairs.  It then checks
minimum degree, connectivity after deletion of each vertex, and all `n!`
vertex relabellings.  It recovers 1, 7, 54, 255, and 550 labelled survivors,
which collapse to the 17 canonical classes above.  The script also checks the
rank and degree-excess identities, every simplicity cost, the exact list and
checksum, hostile mutations, and identical behavior with Python assertions
disabled.

Run it with

```text
python research/rank-four-kernel-census-verifier.py
python -O research/rank-four-kernel-census-verifier.py
```

The classification concerns suppressed multigraph kernels.  It does not say
that every row is itself simple; `sigma` records exactly the unavoidable
subdivision cost when the ambient tetracyclic block is simple.
