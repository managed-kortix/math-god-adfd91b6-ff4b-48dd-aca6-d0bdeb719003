# Order-seven rank-six tetrahedral residual antichains

This is an exact computational discovery record, not a theorem claim. It
classifies the residual parity orbits left by the regular-tetrahedron Gram
sieve for all 314 order-seven rank-six kernels. It does not assert that any
residual row has a DNN certificate or that any candidate packet proves the
square-energy inequality.

## Exact scope

The source census contains 700,792 physical parity rows and 519,453 exact
automorphism orbits. The tetrahedral Gram sieve has budget five and certifies
494,899 orbits. Its exact residual has 24,554 orbit representatives.

For each kernel and each fixed support of positive odd counts, the classifier
orders residual rows coordinatewise and retains every maximal row. This gives
19,695 supportwise residual antichain rows. The artifact records, for each
maximal row, its exact tetrahedral upper bound and the number and physical
orbit mass of residual representatives below it with the same support.

The support restriction is deliberate. Passing a coordinate through zero
changes the odd-edge support and the admissible colorings, so no cross-support
monotonicity is claimed. Within a fixed support, increasing an odd count
replaces even paths by additional odd paths and weakly lowers every admissible
tetrahedral cost; hence the residual set is coordinatewise downward closed.

## Candidate structural packets

The discovery script tags an antichain row when its unit-path support contains
an induced `K4`, `K5`, or `K6` whose nonempty vertex complement induces a tree.
There are 37 tagged rows on seven kernels:

`K469, K496, K502, K506, K511, K580, K635`.

These tags are candidate packet geometry only. In particular, the script does
not check owner assignments, attached-tree bookkeeping, square-energy credit,
or closure under noncanonical lengthening. A candidate must pass those audits
in a separate structural verifier before it can support a proof.

The artifact also groups all 19,695 antichain rows into 132 coarse signatures
using unit-support edge count, unit-support degree sequence, extra odd paths,
even paths, and the candidate flag. These signatures are search buckets, not
isomorphism classes and not mathematical equivalence classes.

## Artifacts

- `research/rank-six-order-seven-tetra-antichain.py` performs the exact
  supportwise classification and candidate scan.
- `research/fixtures/rank-six-order-seven-tetra-antichain.json` stores the
  antichain, domination ledger, coarse packet signatures, and candidate data.
- The artifact SHA-256 is
  `4ccdb97c3eeace00d64b0ccc25cdff25f548226cdaa61e19c5a9305fa56f7099`.

Run the exact audit in normal and optimized modes:

```text
python3 research/rank-six-order-seven-tetra-antichain.py --verify research/fixtures/rank-six-order-seven-tetra-antichain.json
python3 -O research/rank-six-order-seven-tetra-antichain.py --verify research/fixtures/rank-six-order-seven-tetra-antichain.json
```

The audit checks canonical JSON, the open-experiment flags, scope and totals,
key uniqueness, candidate totals, and byte-for-byte equality with a fresh
classification of the exact order-seven source census. `full_theorem` and
`certificate_fixture_frozen` remain false.
