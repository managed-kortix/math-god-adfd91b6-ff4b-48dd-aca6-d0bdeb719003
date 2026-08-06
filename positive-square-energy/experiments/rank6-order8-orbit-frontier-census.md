# Order-eight rank-six orbit and coordinate-frontier census

## Scope

This is the next finite rank-six single-block experiment. It covers all 325
order-eight kernels, numbered K646--K970 in the locked rank-six kernel fixture.
It is a census and search frontier only. It makes no theorem claim.

The implementation reuses the order-seven parity-row, automorphism-orbit,
tetrahedral DNN, canonical path, and one-coordinate lengthening conventions.
Automorphisms are generated inside invariant vertex-signature cells rather than
by scanning all `8!` vertex permutations.

## Exact census

The complete run gives:

| quantity | exact count |
|:--|--:|
| kernels | 325 |
| physical parity rows | 1,598,512 |
| automorphism orbits | 1,045,292 |
| coarse tetrahedral DNN closures | 942,304 |
| residual orbits | 102,988 |
| canonical plus 13 coordinate targets | 1,441,832 |

All tetrahedral acceptance costs are integral after scaling by 30. The budget is
150, and only rows whose minimum coarse cost is strictly greater than 150 enter
the residual stream.

The canonical JSON census has SHA-256
`724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e`.
Ordered stream commitments are:

| stream | SHA-256 |
|:--|:--|
| kernels | `37646f53c89bd904c7e04c687ce90e52be3aea414810499e749ce95493aab0ea` |
| per-kernel orbit digest manifest | `40ce2900c0e2f9887d46f9bf1dfe4eb21ad8b0cc1c4e71179a56d49b34220b3e` |
| residuals | `b451837e04a30e5b71eba5fe631841eee73bbb8f3722a0b6bd25b666ad4fe900` |
| frontier keys | `52439257eaa2b5a6bc2976f5c4199a5a06e3e3b6ab8afc61b2ad7c734876e97d` |

The frontier-key digest commits, in order, to each source index, kernel, parity
row, and frontier label (`null` for canonical, then coordinates 0--12). Thus it
authenticates all 1,441,832 targets without expanding them in the census JSON.

## Rational search

`rank6_order8_batched_exact_gram.py` implements a scalable chunked search in
dimension eight. For each residual orbit it optimizes one tetrahedrally warmed
canonical realization, attempts one shared rational witness for all 14 targets,
then uses per-target fallback optimization only when needed. Every accepted
witness is reconstructed and costed over `Fraction` before output.

A four-row smoke chunk closed all 56 targets exactly and passed the verifier
under both normal Python and `python3 -O`. This only establishes feasibility;
the complete 102,988-row rational search has not been run.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order8_orbit_frontier_census.py \
  --jobs 16 --progress
python3 positive-square-energy/experiments/rank6_order8_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order8_orbit_frontier_census.json

mkdir -p positive-square-energy/experiments/rank6_order8_batched_chunks
python3 positive-square-energy/experiments/rank6_order8_batched_exact_gram.py \
  --start 0 --count 1000 --workers 16
```

The census verifier rejects noncanonical JSON, nonstandard numerical constants,
wrong source scope, malformed or unordered residuals, inconsistent totals, and
changed ordered stream digests. The rational verifier rejects missing or shifted
source indices, duplicate targets, malformed fractions, unauthenticated
denominators, changed path ledgers, nonfinite numerical metadata, and any exact
cost above five. `full_theorem` is required to remain false.
