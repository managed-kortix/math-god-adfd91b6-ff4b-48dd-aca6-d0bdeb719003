# Cycle 256: exhaustive Cycle 255 N=64 numerical screen

## Scope

This is a floating-point Galerkin candidate screen, not a PDE certificate or a
family exclusion theorem. The executable uses the square two-thirds mask at
`N=64`, cutoff 21, classical RK4 with `dt=1/2048`, and normalized-Haar grid
cubature for the velocity `L^3` norm. Every exactly feasible Cycle 255 family
member is integrated in both time directions.

## Completed coverage

The frozen family contains 149,952 members. Exact rational feasibility accepts
10,038 and rejects 139,914. The two parity shards are complete through
enumeration index 149,952:

| shard | feasible rows | first index | last feasible index |
|---:|---:|---:|---:|
| 0 | 6,570 | 1 | 149,923 |
| 1 | 3,468 | 386 | 149,924 |

The merged checkpoint indices and exact member metadata match all 10,038
records in `cycle255-exact-analytic-feasibility.json`, in order, with no
duplicates, omissions, non-finite diagnostics, or tuple mismatches.

## Numerical result

No member reaches the promotion threshold 1.5. The largest bidirectional ratio
is `1.0002951424615105`, at one-based family index 7,272:

```text
a = (1,-2,-1,0,0)
sigma = 1/24
epsilon = 1/1024
T = 1/2
forward ratio = 1.0002951424615105
reverse ratio = 0.9996997113898980
```

Across all feasible members, 372 ratios are at least 1.0001, none is at least
1.001, and none is at least 1.01. The maximum recorded relative energy drift is
`5.329070518200751e-15`; the maximum relative enstrophy drift is
`7.327471962526033e-15`.

## Validation

`python -m unittest -v test_cycle255_candidate_screen.py test_cycle255_independent_screen.py`
passes three tests. These cover checkpoint
creation and deterministic resume, byte reproducibility of fresh short runs,
status and non-certificate labels, family cardinality, a stationary-shear
control, and the independent small reproducer. The exact-feasibility replay
also passes with `10038/149952` feasible.

The completed checkpoints were additionally replayed against the exact
feasibility artifact. The replay checks shard parity, complete merged coverage,
member and feasibility-tuple identity, finite diagnostics, ratio identities,
and agreement between checkpoint row counts and final JSON summaries.

## Artifacts

```text
cycle255_candidate_screen.cpp
  sha256 a9ea2650fa6d0e21c168aadd4051648167831c0b1ecd9b8f952eef281d13d22f
cycle255-screen-N64-shard0.checkpoint.tsv
  sha256 64b2db2038184fa8cf4c259a1a9fa759403ca7ee856b90eaa5280aaf21391021
cycle255-screen-N64-shard1.checkpoint.tsv
  sha256 2cae3d251c4db23354b1e031f0c93fe93cdd6970ec2cc6c6e6d94420a096b306
cycle255-screen-N64-shard0.json
  sha256 c42945dca86659b2035cede8cd2cc288f89d593e076116612cf4aeaad2b45ee4
cycle255-screen-N64-shard1.json
  sha256 c4abc702db3a0f0c0d2df0943c5ac0ba50742c505fca9871cb82fb04b62ae319
```

The production compiler was GCC 13.3.0 with
`-O3 -std=c++20 -Wall -Wextra -pedantic`; GMP supplies exact rational
feasibility arithmetic. The result is
valid only as numerical evidence that this frozen `N=64` funnel promotes no
candidate.
