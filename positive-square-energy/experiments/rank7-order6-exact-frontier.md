# Rank-seven order-six exact frontier

## Result

The order-six lane is closed as an exact finite DNN computation.  All `914`
rank-seven kernels of order six produce `1,094,367` physical parity orbits.
The tetrahedral coarse sieve owns `1,092,850` and leaves exactly `1,517`
residual orbits.  Materializing the canonical target and twelve one-coordinate
lengthenings gives `19,721` frontier keys.

The dimension-six, budget-six search found one exact owner for every residual
orbit.  A common rational branch Gram owns all thirteen targets for `1,515`
orbits.  The remaining two are exact atomic equality geometries:

| geometry | residual orbits | frontier targets |
|---|---:|---:|
| six mixed pairs | 1 | 13 |
| regular tetrahedron plus three mixed pairs | 1 | 13 |
| unresolved | 0 | 0 |

The first symbolic row is the signed six-cycle mixed-pair quotient.  In the
second, the six unit edges force the regular tetrahedron (cost three) and the
three mixed pairs force correlation `-1/2` (cost three).  A PSD completion is
obtained by assigning the two remaining unit vectors their forced projections
onto the tetrahedron span and choosing their free unit directions with inner
product `-5/9`.  Thus both rows have exact cost six.  Coordinate lengthening is
strictly cheaper unless it lengthens a zero-cost contraction, in which case the
cost is unchanged.

This closes only the order-six finite lane.  It does not by itself close the
rank-seven one-block theorem or either global branch, so every artifact retains
`full_theorem=false`.

## Fail-closed artifacts

`rank7_order6_exact_frontier.py` has four commands:

1. `census` regenerates and materializes all residuals and all frontier keys.
2. `search` emits an independently auditable source interval.
3. `verify-chunk` reconstructs every rational unit vector and path chain over
   `Fraction`, checks denominator authentication and exact cost at most six,
   and audits symbolic atom scope.
4. `aggregate` rejects source-digest changes, gaps, overlaps, and unresolved
   records by default.  `--allow-unresolved` is report-only.

The committed complete artifacts are:

| artifact | SHA-256 |
|---|---|
| exact residual/frontier census | `941f6cf2b35a65f76183c1282c20e7662919f7e0380cdd88a55ff5cdc75c94d1` |
| exact witness chunk | `6779df73ff72d38d1776f776f38821d9fb591a89de5b7d63d16be46bb7fab93f` |
| aggregate | `3ef27a6b7003b26f4ca7205e07d29cb975bd8a85b8bf654314dcad19023ab315` |

## Reproduction

From the repository root:

```text
python3 positive-square-energy/experiments/rank7_order6_exact_frontier.py census
python3 positive-square-energy/experiments/rank7_order6_exact_frontier.py search --start 0 --restarts 6 --iterations 900 --output positive-square-energy/experiments/rank7_order6_dim6_chunk_0000_1517.json
python3 -O positive-square-energy/experiments/rank7_order6_exact_frontier.py verify-chunk positive-square-energy/experiments/rank7_order6_dim6_chunk_0000_1517.json
python3 positive-square-energy/experiments/rank7_order6_exact_frontier.py aggregate positive-square-energy/experiments/rank7_order6_dim6_chunk_0000_1517.json --output positive-square-energy/experiments/rank7_order6_dim6_aggregate.json
```
