# Rank-seven parity/coarse-DNN digest census

## Scope

This experiment processes all `17,133` candidate rank-seven kernels from the
committed frontier source.  It is deliberately not a theorem artifact: the
kernel source still carries its removable-ear completeness obligation, and the
coarse sieve leaves residuals.

Orders two through six are exact.  Orders seven through twelve report exact
parity-orbit counts and deterministic Monte Carlo estimates of coarse-DNN
residual orbit counts.  No residual witness list or frontier target list is
materialized.

## Sparse source and sieve

Each dense upper-triangle kernel code is reduced in memory to the ordered tuple
of nonzero triples `(u,v,multiplicity)`.  The artifact commits to that complete
ordered stream by SHA-256.  Automorphisms are computed on the resulting simple
support graph with multiplicity as an edge color.

A physical parity row records, for each support pair of multiplicity `m`, the
number `a` of odd physical paths, where `0 <= a <= m`.  Full multiplicity-colored
kernel automorphisms act on these rows.  The tetrahedral coarse cost is the
rank-six cost with the rank-seven budget changed from five to six.  All sieve
decisions use integer costs scaled by 30.

For orders two through six, every row is enumerated, canonicalized under the
full automorphism group, and sieved exactly.  Per-kernel orbit and residual
streams are hashed and then discarded.  The compact JSON retains order totals
and a digest of the exact per-kernel manifest.

For larger orders, Burnside's lemma gives the parity-orbit count exactly.  For
each automorphism, the code samples uniformly from its fixed-row product space
and estimates the number of fixed residual rows.  Averaging these estimates
over the automorphism group estimates residual orbits directly, avoiding the
bias that would result from sampling labelled rows and dividing by an average
orbit size.  Seeds are fixed by kernel, automorphism, and sample count.

## Results

| order | kernels | parity orbits | coarse residuals |
|---:|---:|---:|---:|
| 2 | 1 | 9 | 0 exact |
| 3 | 6 | 236 | 0 exact |
| 4 | 47 | 6,772 | 0 exact |
| 5 | 233 | 109,342 | 15 exact |
| 6 | 914 | 1,094,367 | 1,517 exact |
| 7 | 2,270 | 6,749,936 | 40,913 estimated (`+/-666` SE) |
| 8 | 4,015 | 26,426,026 | 497,139 estimated (`+/-3,628` SE) |
| 9 | 4,495 | 65,167,570 | 2,831,465 estimated (`+/-12,821` SE) |
| 10 | 3,396 | 98,342,348 | 8,195,161 estimated (`+/-30,781` SE) |
| 11 | 1,391 | 82,561,174 | 11,461,505 estimated (`+/-50,659` SE) |
| 12 | 365 | 29,747,798 | 6,055,511 estimated (`+/-45,122` SE) |

The standard errors are the independent with-replacement sampling errors
propagated through the Burnside sum.  They quantify this estimator only; they
do not account for any mathematical incompleteness in the candidate kernel
source.

## Reproduction

From the repository root:

```text
python3 positive-square-energy/experiments/rank7_parity_coarse_digest_census.py --jobs 8 --samples 256
python3 positive-square-energy/experiments/rank7_parity_coarse_digest_census.py --verify positive-square-energy/experiments/rank7_parity_coarse_digest_census.json
python3 -O positive-square-energy/experiments/rank7_parity_coarse_digest_census.py --verify positive-square-energy/experiments/rank7_parity_coarse_digest_census.json
```

The `256`-sample artifact SHA-256 is
`9b9a94c021b673565ba4f3067bba08e9ef77bd2285e9f0cd0488ffd35e9a7110`.
