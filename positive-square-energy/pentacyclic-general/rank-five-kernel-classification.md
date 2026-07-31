# Classification of the rank-five suppressed kernels

This note records only the finite classification needed for a loopless
no-cut-vertex pentacyclic block after all degree-two vertices are suppressed.
Parallel edges are retained.  For two vertices, deleting either vertex leaves
one vertex and is counted as connected.

## Classification

Let `K` be a finite loopless multigraph with at least two vertices, no cut
vertex, minimum degree at least three, and

`beta(K)=|E(K)|-|V(K)|+1=5`.

Then `2 <= |V(K)| <= 8`, and `K` is isomorphic to exactly one of the 118 rows
in `research/fixtures/rank-five-kernels.json`.  The counts by order are

| `n` | 2 | 3 | 4 | 5 | 6 | 7 | 8 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| classes | 1 | 3 | 13 | 24 | 38 | 23 | 16 | 118 |

The fixture uses vertices `0,...,n-1` and stores multiplicities in
lexicographic upper-triangle order
`01,02,...,0(n-1),12,...,(n-2)(n-1)`.  Rows are sorted first by `n` and then
by the lexicographically least code over all vertex labellings.

The canonical fixture bytes have SHA-256 checksum

`027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884`.

## Degree ledger

The handshake identity gives

`sum_v (deg(v)-2)=2(|E|-|V|)=8`.

Thus the positive excess degrees form a partition of eight.  The surviving
degree multisets and class counts are:

| degree multiset | count |
|:---|---:|
| `6,6` | 1 |
| `6,5,3` | 1 |
| `6,4,4` | 1 |
| `5,5,4` | 1 |
| `6,4,3,3` | 2 |
| `5,5,3,3` | 4 |
| `5,4,4,3` | 4 |
| `4,4,4,4` | 3 |
| `6,3,3,3,3` | 2 |
| `5,4,3,3,3` | 11 |
| `4,4,4,3,3` | 11 |
| `5,3,3,3,3,3` | 7 |
| `4,4,3,3,3,3` | 31 |
| `4,3,3,3,3,3,3` | 23 |
| `3,3,3,3,3,3,3,3` | 16 |

These counts sum to 118 and refine the order ledger.

## Hand classification

Write `n=|V(K)|` and `m=|E(K)|`.  Rank five gives `m=n+4`, so the displayed
degree-excess identity follows.  Every summand is positive, hence `n<=8`;
looplessness and minimum degree exclude `n=1`.

For each positive partition of eight of length `n`, add two to its parts to
obtain a candidate degree multiset.  Introduce a nonnegative integer `a_ij`
for each pair `i<j` and solve the incidence equations

`sum_{j != i} a_min(i,j),max(i,j)=d_i`.

Discard a solution when deleting some vertex disconnects its positive
support.  Quotient the remaining solutions by simultaneous permutation of
the rows and columns.  This gives precisely the degree ledger and the
`1,3,13,24,38,23,16` order ledger above.  Distinct canonical upper-triangle
codes are nonisomorphic, while every incidence solution maps to one retained
code, establishing existence, exhaustion, and pairwise distinction for this
classification.

## Executable audit

`research/rank-five-kernel-census-verifier.py` independently regenerates the
incidence solutions from the degree partitions; its generator does not read
the fixture while constructing candidates.  It checks rank, looplessness,
minimum degree, every vertex deletion, canonicality, the two ledgers, exact
fixture equality, and the checksum.  Nine hostile fixture and policy
mutations must be rejected through explicit exceptions, not assertions.

Run both modes:

```text
python3 research/rank-five-kernel-census-verifier.py
python3 -O research/rank-five-kernel-census-verifier.py
```

This is a classification statement only.  It asserts no spectral, DNN, or
other theorem for the 118 kernels or their subdivisions.
