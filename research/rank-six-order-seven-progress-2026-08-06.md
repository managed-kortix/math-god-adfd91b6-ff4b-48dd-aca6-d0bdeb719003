# Rank-six order-seven kernel frontier: exact progress report

## Scope

The active single-block frontier consists of all 314 loopless no-cut-vertex
rank-six suppressed kernels on seven branch vertices. Every kernel has twelve
suppressed paths. A physical family chooses, for each parallel class, how many
paths have odd length. Kernel automorphisms act on these rows.

The target theorem is:

> For every order-seven rank-six kernel `K`, every simple subdivision `B` of
> `K`, and every graph `G` obtained by attaching an arbitrary finite rooted
> tree at each vertex of `B`, `s+(G) >= |V(G)|`.

This theorem is not yet claimed here.

## Exact census

`positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py`
reuses the order-six orbit and regular-tetrahedron sieve with precomputed
permutation actions, restricted set-partition colorings, integer-scaled costs,
and multiprocessing across kernels. It independently obtains:

| set | exact count |
|:---|---:|
| kernels | 314 |
| labeled physical parity rows | 700,792 |
| automorphism orbits | 519,453 |
| coarse DNN certified orbits | 494,899 |
| coarse residual orbits | 24,554 |
| canonical plus twelve coordinate frontiers | 319,202 |

The canonical census artifact has SHA-256
`2e38e09a1b7f800e0a17faa9a05c12adda2bfc45367aecd999b10e121b34bdb3`.
It remains marked `full_theorem=false` and
`certificate_fixture_frozen=false`.

## Rational frontier machinery

`positive-square-energy/experiments/rank6_order7_dim7_rational_frontier.py`
provides deterministic, chunkable dimension-seven optimization. Floating
point computations only propose vectors. A target is accepted only after the
branch and internal path vectors are reconstructed from reduced rational
stereographic parameters and every cost `(1-r)/(1+r)` is summed over
`Fraction`; the exact total must be at most five.

The initial ten-residual smoke chunk covers 130 canonical/coordinate targets
with 130 exact rational certificates and no finite residual. This is a pipeline
test, not statistically meaningful theorem coverage. The committed verifier
does not depend on this temporary chunk.

## Fail-closed frontier verifier

`research/rank-six-order-seven-frontier-verifier.py` derives all 319,202 target
keys from the source-locked census, rejects duplicate or out-of-scope keys,
invokes exact rational reconstruction for every loaded record, and accepts a
structural residual only after rebuilding its physical path ledger and checking
an induced unit-path clique plus a nonempty complementary unit-path tree.

It prints `theorem_status=PROVED` only when the loaded key set equals the full
frontier and every key is closed by an exact rational DNN certificate or an
audited structural record. Otherwise it prints `theorem_status=OPEN`. Normal
execution internally reruns the same audit under `python3 -O` and requires
byte-identical output. Five hostile mutations are rejected on a nonempty
chunk.

## Current verdict

The order-seven kernel universe, physical rows, automorphism orbits, coarse DNN
partition, and complete finite frontier have exact reproducible counts. The
rational and structural closure ledger is not complete. Therefore:

```text
order-seven rank-six single-block theorem: OPEN
exact finite frontier: 319202 targets
committed theorem certificates: incomplete
```

Arbitrary same-parity subdivisions will follow from the established
fixed-parity path monotonicity once all frontier targets close. Arbitrary rooted
trees then follow from the same owner-exact attachment argument used for orders
two through six; neither analytic implication is used to hide a finite
frontier gap.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json
python3 -O positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json
python3 research/rank-six-order-seven-frontier-verifier.py
python3 -O research/rank-six-order-seven-frontier-verifier.py
```
