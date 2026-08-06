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

The finite frontier is now closed by exact certificates. Together with the
fixed-parity path monotonicity and owner-exact attachment theorem cited below,
this proves the stated single-block theorem.

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

## Equality-frontier closure

The complete batched run supplies 319,163 exact rational certificates. Its 39
null witnesses are exactly three targets on each of 13 source rows, on kernels
K469, K511, K534, and K548. They are closed by rational equality templates:
signed five-cycle quotients for K534 and K548, and tetrahedron-plus-apex Grams
for K469 and K511.

`research/rank-six-order-seven-equality-frontier-verifier.py` locks the six
compressed XZ artifacts, their decompressed canonical JSON streams, and both
ordered manifests by SHA-256. The artifacts total 45,176,376 bytes. The
standard-library-only verifier identifies the 39 null-witness keys,
reconstructs every equality Gram, checks all principal minors and costs over
`Fraction`, and verifies uniform same-parity lengthening by explicit zero-cost
repeated vectors. It ignores the stored numerical costs.

`research/rank-six-order2-7-master-verifier.py` now integrates this closure with
the exact rank-six census and the theorem owners for orders two through six.
It authenticates the `1+4+26+84+216+314=645` order-two-through-seven kernel
partition, invokes every digest-locked dependency, rejects omission and scope
widening, and requires byte-identical normal and `python3 -O` output. Its
manifest expressly excludes orders eight through ten and any all-hexacyclic
claim.

## Historical clique/tree candidates

The earlier tetrahedral-antichain experiment marked 37 rows as possible
clique/tree packet candidates. They are not a theorem dependency. The complete
exact DNN run covers all 481 canonical-plus-coordinate targets on those rows:
36 rows have shared rational witnesses for all 13 targets, while one K511 row
(source index 14191) has ten batched witnesses and its canonical, coordinate-2,
and coordinate-5 targets are among the exact equality templates.

`research/rank-six-order-seven-clique-tree-packet-verifier.py` now audits this
redundancy against the same digest-locked chunks and equality closure. It does
not certify the abandoned structural idea: a bare K4-plus-trees decomposition
does not by itself show that the K4 packet survives subdivision of one of its
six edges. No packet fixture or packet lemma is used by the order-seven proof.

## Current verdict

The order-seven kernel universe, physical rows, automorphism orbits, coarse DNN
partition, and complete finite frontier have exact reproducible counts. Every
frontier target now has an exact rational certificate. Therefore:

```text
order-seven rank-six single-block theorem: PROVED
exact finite frontier: 319202 targets
exact DNN certificates: 319163 batched plus 39 equality templates
```

Arbitrary same-parity subdivisions follow from established fixed-parity path
monotonicity; the equality verifier additionally gives an explicit zero-cost
lengthening construction for its 39 targets. Arbitrary rooted trees follow from
the same owner-exact attachment argument used for orders two through six.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json
python3 -O positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json
python3 research/rank-six-order-seven-frontier-verifier.py
python3 -O research/rank-six-order-seven-frontier-verifier.py
python3 research/rank-six-order-seven-equality-frontier-verifier.py
python3 -O research/rank-six-order-seven-equality-frontier-verifier.py
python3 research/rank-six-order-seven-clique-tree-packet-verifier.py
python3 -O research/rank-six-order-seven-clique-tree-packet-verifier.py
python3 research/rank-six-order2-7-master-verifier.py
python3 -O research/rank-six-order2-7-master-verifier.py
```
