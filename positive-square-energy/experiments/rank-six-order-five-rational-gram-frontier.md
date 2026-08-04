# Rank-six order-five exact rational Gram frontier

## Status

This remains the frozen experimental search artifact. Its 13 reported
canonical/frontier residuals are now closed by the independent exact theorem
and verifier in
`positive-square-energy/hexacyclic-general/order-five-rank-six-kernel-theorem.md`.
The raw artifact is deliberately not rewritten or promoted, and no main/master
theorem file is changed.

## Exact census

The digest-locked rank-six kernel fixture contains exactly 84 order-five
kernels. Every kernel has ten suppressed paths, in pair order

`01,02,03,04,12,13,14,23,24,34`.

For a multiplicity row `m`, a physical row records the odd-path count in every
bundle. Direct Cartesian enumeration gives 33,151 physical rows. Quotienting
only by the genuine vertex automorphism group of each kernel gives 25,168
orbits. A regular-tetrahedron Gram sieve at excess budget five partitions them
exactly as

`25,168 = 25,065 tetra-certified + 103 residual orbits`.

The coarse path costs are the exact rational upper bounds `1/2` for the first
odd path in a bundle, `1/6` for each additional odd path, and `3/5` for each
even path. Equal-colored endpoints allow only even paths, at zero cost. The
census stores each canonical row, its physical orbit size, first minimizing
coloring, exact minimum rational upper bound, and status.

## Canonical plus frontiers

For each of the 103 residual rows, the search attacks the canonical shortest
length vector and all ten one-coordinate length-plus-two vectors. Thus the
all-length monotonicity budget has exactly

`103 * (1+10) = 1,133 targets`.

A dimension-five search numerically proposes branch and internal path vectors.
Every positive result is then rebuilt from rational stereographic parameters
and checked with `Fraction`; numerical costs alone certify nothing. The frozen
partition is

| method/status | targets |
|:---|---:|
| exact rational Gram cost at most five | 1120 |
| residual | 13 |
| total | 1133 |

## Former structural residual

The 13 targets belong to three exact kernel/row types:

| kernel | kernel code | physical row | open targets | numerical indication |
|---:|:---|:---|---:|:---|
| 61 | `(0,0,2,2,2,0,2,2,0,0)` | `(0,0,1,1,1,0,1,1,0,0)` | canonical only | `5.0` equality candidate |
| 98 | `(1,0,1,1,0,1,1,2,2,1)` | `(1,0,1,1,0,1,1,1,1,1)` | canonical only | `5.0` equality candidate |
| 110 | `(1,1,1,1,1,1,1,1,1,1)` | all odd | canonical plus ten frontiers | `6.0`; frontiers about `5.00582080171` |

Kernels 61 and 98 have exact symbolic equality Grams of cost five. Kernel 110
is the all-odd `K5` subdivision family: its all-unit DNN optimum is exactly six,
while a structural split plus two strict two-long Gram orbit certificates
closes every subdivision with arbitrary rooted-tree attachments. Those proofs
belong to the theorem artifact, not to this historical search output.

## Fail-closed artifacts

Run:

```text
python3 research/rank-six-order-five-tetra-census.py
python3 -O research/rank-six-order-five-tetra-census.py
python3 research/rank-six-order-five-dim5-rational-gram-search.py --audit
python3 -O research/rank-six-order-five-dim5-rational-gram-search.py --audit
```

The census verifier regenerates all physical rows and genuine automorphism
orbits from the source-locked 84 kernels, recomputes the tetrahedral minima,
checks the orbit-size partition, and rejects hostile mutations. Its fixture
SHA-256 is

`9656146c9dfefacc1c8df15fa9e7c8423f04b12c802c08af93f6e3f3e520bf22`.

The result audit locks all 1,133 target keys and rational vector records,
requires the exact `1120+13` partition and the three residual signatures, and
forbids theorem promotion. Its fixture SHA-256 is

`ae5f78b189a04e9a3e790188c5f4577a92c5dd19463267aceaec1a8f54bbd2c0`.

The search command remains reproducible but heuristic; rerunning it may find
different rational witnesses. Only the digest-locked result and exact audit are
the frozen artifact.
